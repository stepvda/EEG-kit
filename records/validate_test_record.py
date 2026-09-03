#!/usr/bin/env python3
"""
validate_test_record.py -- check a per-unit test record against TST-EEG-004 Rev C section 12.

Section 12 says the field counts are "fixed so a record can be validated mechanically".
This is the thing that does the validating.  It runs in two passes:

  1.  The JSON Schema in `TST-EEG-004_RevC_unit_test_record.schema.json`.  If the
      `jsonschema` package is installed it is used; if it is not, the subset checker below
      does the work.  The package has no third-party runtime dependencies and this file does
      not add one: a manufacturer must be able to run this on a test-cell PC with a stock
      Python and no network.

  2.  The checks a schema cannot express, and which are the ones that actually catch a bad
      record: that a step which was not performed says why, that the serial the host read at
      T5b is the serial in the identity block, that the fingerprint written at T6 is the
      fingerprint on the label, that the clamp value in the unit is the clamp value from the
      lot, that a PASS at T30 really did have all seven frame-integrity counters at zero,
      and that the SHA-256 printed on the certificate is the SHA-256 of the record.

Usage:
    python3 records/validate_test_record.py <record.json> [<record.json> ...]
    python3 records/validate_test_record.py --production <record.json>

`--production` additionally refuses a record whose `record_type` is `example`, refuses a
record with any DEFERRED step, and refuses the all-zeros hash.  It is what a goods-in check
in Brussels runs; without it the example record shipped beside the schema would pass.

Exit status is 0 when every record is valid, 1 when any is not.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "TST-EEG-004_RevC_unit_test_record.schema.json")
ZERO_HASH = "0" * 64

# The eleven steps of TST-EEG-004 Rev C section 2 that "produce numbers that only a host
# stream decoder can produce", and section 16 item 10 records that no such tool exists.
DECODING_STEPS = ["T7", "T8", "T9", "T10", "T12", "T13", "T14", "T15", "T16", "T26", "T27"]


# ---------------------------------------------------------------------------------------
# A JSON Schema 2020-12 subset checker.  It covers exactly the keywords the generated schema
# uses -- type, const, enum, oneOf, properties, required, additionalProperties, items,
# minItems, maxItems, minLength, pattern, minimum and maximum -- and REFUSES to validate
# against a schema that uses anything else, rather than quietly ignoring a keyword and
# passing a record it should have rejected.
# ---------------------------------------------------------------------------------------

KNOWN = {"$schema", "$id", "$comment", "title", "description", "type", "const", "enum",
         "oneOf", "properties", "required", "additionalProperties", "items", "minItems",
         "maxItems", "minLength", "pattern", "minimum", "maximum"}

TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def _is_type(value, name):
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    return isinstance(value, TYPES[name])


def check(schema, value, path="$", errors=None):
    errors = [] if errors is None else errors
    unknown = set(schema) - KNOWN
    if unknown:
        raise SystemExit(f"{path}: schema uses keywords this checker does not implement: "
                         f"{sorted(unknown)}. Install `jsonschema` or extend this file; "
                         f"silently ignoring a keyword would pass records it should fail.")

    def err(msg):
        errors.append(f"{path}: {msg}")

    if "const" in schema and value != schema["const"]:
        err(f"must be {schema['const']!r}, got {value!r}")
        return errors
    if "enum" in schema and value not in schema["enum"]:
        err(f"must be one of {schema['enum']}, got {value!r}")
        return errors
    if "oneOf" in schema:
        hits = [i for i, sub in enumerate(schema["oneOf"])
                if not check(sub, value, path, [])]
        if len(hits) != 1:
            err(f"must match exactly one of the {len(schema['oneOf'])} alternatives; "
                f"matched {len(hits)}")
            return errors
    if "type" in schema:
        want = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is_type(value, t) for t in want):
            err(f"must be {'/'.join(want)}, got {type(value).__name__}")
            return errors
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            err(f"must be at least {schema['minLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            err(f"must match {schema['pattern']!r}, got {value!r}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            err(f"must be >= {schema['minimum']}, got {value}")
        if "maximum" in schema and value > schema["maximum"]:
            err(f"must be <= {schema['maximum']}, got {value}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            err(f"must have at least {schema['minItems']} items, got {len(value)}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            err(f"must have at most {schema['maxItems']} items, got {len(value)}")
        if "items" in schema:
            for i, item in enumerate(value):
                check(schema["items"], item, f"{path}[{i}]", errors)
    if isinstance(value, dict):
        for k in schema.get("required", []):
            if k not in value:
                err(f"missing mandatory field {k!r}")
        props = schema.get("properties", {})
        for k, v in value.items():
            if k in props:
                check(props[k], v, f"{path}.{k}", errors)
            else:
                extra = schema.get("additionalProperties", True)
                if extra is False:
                    err(f"field {k!r} is not in the schema")
                elif isinstance(extra, dict):
                    check(extra, v, f"{path}.{k}", errors)
    return errors


def schema_validate(schema, record):
    try:
        import jsonschema                                    # noqa: F401
    except ImportError:
        return check(schema, record), "built-in subset checker"
    import jsonschema
    v = jsonschema.Draft202012Validator(schema)
    return ([f"{'.'.join(str(p) for p in e.absolute_path) or '$'}: {e.message}"
             for e in sorted(v.iter_errors(record), key=lambda e: list(e.absolute_path))],
            f"jsonschema {jsonschema.__version__}")


# ---------------------------------------------------------------------------------------
# The checks a schema cannot make.
# ---------------------------------------------------------------------------------------

def canonical_bytes(record):
    """The byte string signatures.record_sha256 is taken over.

    Defined in records/README.txt: the record serialised as UTF-8 JSON with sorted keys, a
    two-space indent and a trailing newline, with signatures.record_sha256 set to
    sixty-four zeros -- otherwise the hash would have to contain itself.  That definition is
    a PROPOSAL of this package and needs the programme's ruling before a manufacturer signs
    against it; TST-EEG-004 section 12 requires the hash without saying what it covers.
    """
    r = copy.deepcopy(record)
    r.setdefault("signatures", {})["record_sha256"] = ZERO_HASH
    return (json.dumps(r, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf8")


def cross_checks(record, filename, production):
    errors, warnings = [], []
    ident = record.get("identity", {})
    results = record.get("results", {})
    consts = record.get("constants", {})

    def data(step, *keys, default=None):
        d = results.get(step, {}).get("data", {})
        for k in keys:
            if not isinstance(d, dict) or k not in d:
                return default
            d = d[k]
        return d

    # -- the record is what it says it is ------------------------------------------------
    serial = ident.get("unit_serial")
    if serial:
        want = f"{serial}_test.json"
        got = os.path.basename(filename)
        # The worked example is deliberately named EXAMPLE_<serial>_test.json so that it can
        # never be filed as a unit's record by a directory sweep.
        allowed = {want} if record.get("record_type") == "production" \
            else {want, f"EXAMPLE_{want}"}
        if got not in allowed:
            (errors if production else warnings).append(
                f"filename is {got!r}; TST-EEG-004 section 12 names the file {want!r}")

    if production:
        if record.get("record_type") != "production":
            errors.append("record_type is "
                          f"{record.get('record_type')!r}; a deliverable under "
                          "RFQ-EEG-001 Rev E section 9.3 must be `production`")
        if record.get("signatures", {}).get("record_sha256") == ZERO_HASH:
            errors.append("signatures.record_sha256 is the all-zeros placeholder")

    # -- every step accounts for itself ---------------------------------------------------
    for sid, step in sorted(results.items()):
        v = step.get("verdict")
        if v in ("DEFERRED", "NOT_APPLICABLE") and not step.get("deferral_reason"):
            errors.append(f"results.{sid}: verdict {v} with no deferral_reason")
        if production and v == "DEFERRED":
            errors.append(f"results.{sid}: DEFERRED. A production record has no deferred "
                          f"steps; a step that cannot be run is NOT_APPLICABLE with a "
                          f"reason, or the unit is not accepted")
        attempt = step.get("attempt")
        prev = step.get("previous_attempts", [])
        if isinstance(attempt, int) and len(prev) != attempt - 1:
            errors.append(f"results.{sid}: attempt {attempt} but {len(prev)} previous "
                          f"attempts retained. Section 12: every attempt is retained, "
                          f"nothing is overwritten")

    # -- the three identifiers are one unit ------------------------------------------------
    pairs = [
        ("results.T5.data.iserial_t5b", data("T5", "iserial_t5b"),
         "identity.unit_serial", ident.get("unit_serial"),
         "T5b requires the iSerialNumber to equal the unit serial character for character"),
        ("results.T6.data.atecc_factory_serial", data("T6", "atecc_factory_serial"),
         "identity.atecc_factory_serial", ident.get("atecc_factory_serial"),
         "the ATECC factory serial is written at T6 and printed on the label"),
        ("results.T6.data.key_fingerprint", data("T6", "key_fingerprint"),
         "identity.key_fingerprint", ident.get("key_fingerprint"),
         "the fingerprint is FW-EEG-001 section 7's and is identical to the label"),
        ("results.T16.data.key_fingerprint_used", data("T16", "key_fingerprint_used"),
         "identity.key_fingerprint", ident.get("key_fingerprint"),
         "T16 verifies the chain with the unit's own key"),
    ]
    for an, a, bn, b, why in pairs:
        if a is not None and b is not None and a != b:
            errors.append(f"{an} = {a!r} but {bn} = {b!r}. PKG-EEG-015 section 5: if any "
                          f"two disagree the unit is quarantined -- {why}")

    # -- the acoustic clamp is one value in three places -----------------------------------
    clamps = {"constants.acoustic_clamp_register_value":
                  consts.get("acoustic_clamp_register_value"),
              "results.T17.data.clamp_register_value":
                  data("T17", "clamp_register_value"),
              "results.T28.data.clamp_register_value":
                  data("T28", "clamp_register_value")}
    seen = {k: v for k, v in clamps.items() if v is not None}
    if len(set(seen.values())) > 1:
        errors.append("the acoustic clamp register value disagrees between "
                      + ", ".join(f"{k} = {v!r}" for k, v in seen.items())
                      + ". T17's limit is that it equals the T28 lot value")

    # -- a PASS means what the limit says --------------------------------------------------
    if results.get("T30", {}).get("verdict") == "PASS":
        counters = data("T30", "frame_integrity_counters", default={}) or {}
        nonzero = {k: v for k, v in counters.items() if v}
        if nonzero:
            errors.append(f"results.T30 is PASS but these frame-integrity counters are not "
                          f"zero: {nonzero}. Every one of the seven must read zero")
        med = data("T30", "latency_median_ms")
        if isinstance(med, (int, float)) and med > 50:
            warnings.append(f"results.T30 median round-trip latency {med} ms exceeds "
                            f"TOOL-EEG-022's 50 ms warning threshold. Record the host and "
                            f"hub arrangement beside it; E-13's stimulus timing rests on it")
    if results.get("T14", {}).get("verdict") == "PASS":
        if data("T14", "frames_missing"):
            errors.append("results.T14 is PASS with frames_missing non-zero. The limit is "
                          "zero missing sequence numbers")
        if data("T14", "card_versus_host_mismatches"):
            errors.append("results.T14 is PASS with card-versus-host mismatches")
    if results.get("T16", {}).get("verdict") == "PASS":
        v, t = data("T16", "blocks_verified"), data("T16", "blocks_total")
        if isinstance(v, int) and isinstance(t, int) and v != t:
            errors.append(f"results.T16 is PASS with {v} of {t} blocks verified. The limit "
                          f"is every block")
    if results.get("T27", {}).get("verdict") == "PASS" and data("T27", "divergence_count"):
        errors.append("results.T27 is PASS with a non-zero status-word divergence count")

    # -- the eleven steps that need a tool nobody has ---------------------------------------
    if ident.get("stream_decoder") is None:
        passed = [s for s in DECODING_STEPS
                  if results.get(s, {}).get("verdict") == "PASS"]
        if passed:
            warnings.append(
                f"identity.stream_decoder is null but {', '.join(passed)} are PASS. "
                f"TST-EEG-004 section 16 item 10 records that the host stream-decoding tool "
                f"does not exist, and these steps produce numbers only a decoder can "
                f"produce. Either the tool now exists and belongs in identity, or these "
                f"verdicts are not supported by a measurement")

    # -- the hash on the certificate is the hash of the record ------------------------------
    claimed = record.get("signatures", {}).get("record_sha256")
    if claimed and claimed != ZERO_HASH:
        actual = hashlib.sha256(canonical_bytes(record)).hexdigest()
        if claimed != actual:
            errors.append(f"signatures.record_sha256 is {claimed} but the record hashes to "
                          f"{actual}. TST-EEG-004 section 13 item 8 prints this on the "
                          f"certificate")
    return errors, warnings


def validate(path, production=False):
    with open(path, encoding="utf8") as fh:
        record = json.load(fh)
    with open(SCHEMA_PATH, encoding="utf8") as fh:
        schema = json.load(fh)

    errors, engine = schema_validate(schema, record)
    x_errors, warnings = cross_checks(record, path, production)
    errors += x_errors

    name = os.path.basename(path)
    print(f"{name}")
    print(f"  schema : {os.path.basename(SCHEMA_PATH)}  ({engine})")
    print(f"  mode   : {'production' if production else 'template'}")
    for w in warnings:
        print(f"  WARN   {w}")
    for e in errors:
        print(f"  ERROR  {e}")
    print(f"  {'VALID' if not errors else 'INVALID'}"
          f"  -- {len(errors)} error(s), {len(warnings)} warning(s)")
    return not errors


EXAMPLE = os.path.join(HERE, "EXAMPLE_TIOV-B-0000_test.json")


def selftest():
    """Break the example record eight ways and prove each break is caught.

    A validator that has never rejected anything is a validator nobody has tested.  Each
    case below is a defect a real record could carry: a short array, a serial that does not
    match the label, a clamp value from another lot, a PASS that contradicts its own
    counters, a hash that is not the record's.
    """
    base = json.load(open(EXAMPLE, encoding="utf8"))
    schema = json.load(open(SCHEMA_PATH, encoding="utf8"))
    ok = True

    def case(name, mutate, expect):
        nonlocal ok
        r = copy.deepcopy(base)
        mutate(r)
        errs, _ = schema_validate(schema, r)
        x, _w = cross_checks(r, EXAMPLE, production=False)
        errs += x
        hit = any(expect in e for e in errs)
        ok &= hit
        print(f"  [{'ok ' if hit else 'FAIL'}] {name}")
        if not hit:
            print(f"         expected an error containing {expect!r}; got {errs}")

    case("a short T23 array is rejected",
         lambda r: r["results"]["T23"]["data"]["dc_single_fault_ua"].pop(),
         "at least 14 items")
    case("a 69th T23 value is rejected",
         lambda r: r["results"]["T23"]["data"]["dc_normal_host_connected_ua"].append(0.0),
         "at most 14 items")
    case("a missing mandatory step is rejected",
         lambda r: r["results"].pop("T30"),
         "missing mandatory field 'T30'")
    case("an invented field is rejected",
         lambda r: r["results"]["T3"]["data"].update({"invented_field": 1}),
         "not in the schema")
    case("a serial that is not the label's serial is rejected",
         lambda r: r["results"]["T5"]["data"].update({"iserial_t5b": "TIOV-B-0007"}),
         "PKG-EEG-015 section 5")
    case("a clamp value from another lot is rejected",
         lambda r: r["results"]["T17"]["data"].update({"clamp_register_value": 1}),
         "acoustic clamp register value disagrees")
    case("a T30 PASS with a non-zero counter is rejected",
         lambda r: (r["results"]["T30"].update({"verdict": "PASS"}),
                    r["results"]["T30"]["data"]["frame_integrity_counters"]
                    .update({"crc_errors": 3})),
         "frame-integrity counters are not zero")
    case("a DEFERRED step with no reason is rejected",
         lambda r: r["results"]["T1"].pop("deferral_reason"),
         "no deferral_reason")
    case("a hash that is not the record's is rejected",
         lambda r: r["signatures"].update({"record_sha256": "a" * 64}),
         "but the record hashes to")
    case("an unsupported verdict is rejected",
         lambda r: r["results"]["T3"].update({"verdict": "PROBABLY"}),
         "must be one of")

    # and the unmodified example must still pass
    errs, _ = schema_validate(schema, base)
    x, _w = cross_checks(base, EXAMPLE, production=False)
    good = not (errs + x)
    ok &= good
    print(f"  [{'ok ' if good else 'FAIL'}] the shipped example validates unchanged")
    if not good:
        print("        ", errs + x)

    # and it must be refused as a production deliverable
    _e, _w = cross_checks(base, EXAMPLE, production=True)
    refused = any("must be `production`" in e for e in _e)
    ok &= refused
    print(f"  [{'ok ' if refused else 'FAIL'}] the example is refused in --production mode")

    print("  self-test", "PASSED" if ok else "FAILED")
    return ok


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest() else 1
    production = "--production" in argv
    paths = [a for a in argv[1:] if not a.startswith("--")]
    if not paths:
        print(__doc__.strip().split("Usage:")[1].split("`--production`")[0].strip())
        return 2
    ok = True
    for p in paths:
        ok &= validate(p, production)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
