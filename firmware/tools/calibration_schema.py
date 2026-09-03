#!/usr/bin/env python3
"""
calibration_schema.py -- the schema for the calibration file end-of-line provisioning consumes.

WHAT THIS IS
  TST-EEG-004 T6 requires the provisioning station to write "the calibration constants measured
  in T7, T10, T12, T17 and T28", and `provision.py --calibration cal_TIOV-B-0007.json` is how
  they get there.  No document, example or template defined a single key name, unit, scaling or
  range, so `provision.py` read the file as an opaque blob and `drv_nvs_set_blob()` stored it
  without inspection.  Two shops would have produced two mutually unreadable files, and the
  constants written into the fleet would not have been comparable -- which is the confound
  RFQ-EEG-001 section 9 exists to prevent.

  This module is the single definition.  It carries the constant table, it validates a file
  against it, and it generates the two artefacts that sit next to it:

      calibration_schema.json        JSON Schema (2020-12), generated from the table below
      cal_TIOV-B-0000.example.json   a worked example carrying NO measurements

  Regenerate:   python3 calibration_schema.py --emit
  Check:        python3 calibration_schema.py --check          (exit 1 if the files drifted)
  Validate:     python3 calibration_schema.py --validate cal_TIOV-B-0007.json

  `provision.py` imports `validate()` from here and refuses a file that does not conform unless
  the operator passes `--calibration-schema-override`, which is recorded in the unit record.

WHERE EVERY KEY COMES FROM, AND WHERE IT DOES NOT
  Every key below is one quantity a numbered test says it records, and every bound below is a
  limit that test states.  Nothing here is a measurement and nothing here is a new requirement.
  The `source` field on each entry names the test, so a disagreement between this file and
  TST-EEG-004 is resolved in favour of TST-EEG-004 and fixed here.

  Where a test records a quantity but states no unit or no bound, this file says so in the
  entry's `note` rather than choosing one.  Three such holes are open and are listed in
  README_provisioning.md section 4.

STATUS: PROPOSAL.  The key names, the nesting and the file-level identity block are choices,
and FW-EEG-001 section 10 assigns the calibration-record schema to CAL-EEG-012.  The programme
owns those choices; this file makes them explicit and testable so that they can be reviewed
instead of being made independently at each shop.

Licence: MIT, matching firmware/tools/provision.py and the rest of the firmware source
(FW-EEG-001: "CC BY-SA 4.0 for this document; the firmware source is MIT").
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "calibration_schema.json")
EXAMPLE_PATH = os.path.join(HERE, "cal_TIOV-B-0000.example.json")

SCHEMA_ID = "EEG-CAL-1"

# ICD-EEG-006 section 5.2, normative channel map.  The stream numbering, not the R1-R16
# protection-network numbering of DSN-EEG-003; the two are different things.
EEG_CHANNELS = [1, 2, 3, 4, 5, 6, 7, 8]            # Fz Cz Pz C3 C4 T7 T8 F7, gain 24
EMG_CHANNELS = [9, 10, 11]                          # cheek, submental, laryngeal, gain 12
ENV_CHANNELS = [12, 13, 14]                         # ENV_STIM, ENV_VOICE, ENV_ROOM, gain 1
SPARE_CHANNELS = [15, 16]                           # spare / EOG, gain 24
GAIN_CHANNELS = EEG_CHANNELS + EMG_CHANNELS + SPARE_CHANNELS   # the thirteen T7 measures

CHANNEL_NAMES = {
    1: "Fz", 2: "Cz", 3: "Pz", 4: "C3", 5: "C4", 6: "T7", 7: "T8", 8: "F7",
    9: "EMG cheek", 10: "EMG submental", 11: "EMG laryngeal",
    12: "ENV_STIM", 13: "ENV_VOICE", 14: "ENV_ROOM",
    15: "spare / EOG 1", 16: "spare / EOG 2",
}

SERIAL_RE = re.compile(r"^TIOV-B-\d{4}$")           # PKG-EEG-015 section 5


class Num:
    """One numeric constant: where it comes from, what it is measured in, and what bounds the
    test that produces it states.  `lo`/`hi` are None where the test states no bound -- an
    unbounded number is recorded as unbounded rather than given an invented range."""

    def __init__(self, key, unit, source, lo=None, hi=None, integer=False, note=None):
        self.key, self.unit, self.source = key, unit, source
        self.lo, self.hi, self.integer, self.note = lo, hi, integer, note

    def json_schema(self):
        s = {"type": "integer" if self.integer else "number",
             "description": f"{self.unit}. Source: {self.source}."
                            + (f" {self.note}" if self.note else "")}
        if self.lo is not None:
            s["minimum"] = self.lo
        if self.hi is not None:
            s["maximum"] = self.hi
        return s

    def check(self, value, path, problems):
        if self.integer and isinstance(value, bool):
            problems.append(f"{path}: expected a number, found a boolean")
            return
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            problems.append(f"{path}: expected a number, found {type(value).__name__}")
            return
        if self.integer and not float(value).is_integer():
            problems.append(f"{path}: expected an integer, found {value}")
            return
        if self.lo is not None and value < self.lo:
            problems.append(f"{path}: {value} is below the {self.source} limit of {self.lo} "
                            f"{self.unit}")
        if self.hi is not None and value > self.hi:
            problems.append(f"{path}: {value} is above the {self.source} limit of {self.hi} "
                            f"{self.unit}")


# --------------------------------------------------------------------------- the constants
#
# T7 -- front-end gain.  Record: "8 x 3 EEG gains, 3 x 3 EMG gains, 2 spare gains, all in ppm of
# nominal ... Absolute gain is recorded and becomes the F-18 constant, not a pass or fail", so
# there is no bound here on purpose.  The per-level values and the divider voltage stay in the
# test record; what the unit carries is one constant per channel.
GAIN = Num("gain_ppm", "ppm of nominal gain", "TST-EEG-004 T7",
           note="Deviation from nominal, signed: 0 means the channel measured its nominal "
                "gain (24 for channels 1-8 and 15-16, 12 for 9-11). T7 records the absolute "
                "gain as a constant and does not pass or fail on it.")

# T10 -- lead-off calibration.  Record: "8 pairs of (R_off, k) -- 32 raw values and 16
# constants".  The acceptance rule is relative to the fitted series resistor, which is why
# `protection_series_resistor_ohm` is required: without it the file cannot be interpreted,
# because ECO-EEG-024 changes that resistor from 47 kOhm to 68 kOhm and moves every expectation.
R_OFF = Num("r_off_ohm", "ohm", "TST-EEG-004 T10", lo=0.0,
            note="Fitted offset. T10's limit is 'within the fitted series-resistor value "
                 "+/- 5 %', which is 47 kOhm today and 68 kOhm if ECO-EEG-024 is taken, so the "
                 "bound is relative to protection_series_resistor_ohm and is checked there.")
K_SLOPE = Num("k", "slope of the least-squares fit", "TST-EEG-004 T10",
              note="OPEN: T10 states neither the unit nor the range of k. Until the programme "
                   "states whether the raw lead-off reading is in ADC counts or in ohms, two "
                   "shops can produce two incomparable numbers here. README_provisioning.md "
                   "section 4 item 1.")

# T12 -- envelope channels.  Record: "3 scaling values, 3 group-delay medians and their IQR in
# samples, comparator threshold in mV, the measured AC-coupling corner in Hz, the measured
# low-pass corner f0 in Hz".
ENV_SCALING = Num("scaling_mv_at_converter", "mV at the ADS1299 input for a 1.1 V peak envelope",
                  "TST-EEG-004 T12a", lo=95.0, hi=105.0,
                  note="T12a's limit is 'within +/- 5 % of 100 mV at the converter input'.")
ENV_DELAY = Num("group_delay_median_samples", "samples at 1000 Hz", "TST-EEG-004 T12b",
                note="The absolute offset is recorded as a constant and is not judged; the "
                     "calculated expectation is 4.40 samples (1 / (Q x 2 pi x f0), Q = 0.7416, "
                     "f0 = 48.77 Hz).")
ENV_IQR = Num("group_delay_iqr_samples", "samples at 1000 Hz", "TST-EEG-004 T12b",
              lo=0.0, hi=2.0,
              note="T12b's limit is on the spread: '<= 2 samples'.")
ENV_F0 = Num("lowpass_f0_hz", "Hz", "TST-EEG-004 T12e", lo=42.0, hi=58.0,
             note="T12e's band. It is wider than RFQ E-11's 50 Hz +/- 10 %, which no build with "
                  "the fitted X7R capacitors can hold; TST-EEG-004 Note 1 carries that conflict.")
ENV_COMPARATOR = Num("comparator_threshold_mv", "mV", "TST-EEG-004 T12c", lo=45.0, hi=60.0,
                     note="One TLV3201 at U7, so one value. Calculated expectation 52 mV "
                          "(2.5 V x 10 k / 480 k) with about 5 mV of hysteresis from R82.")
ENV_AC = Num("ac_coupling_corner_hz", "Hz", "TST-EEG-004 T12d", lo=0.0, hi=2.0,
             note="T12d's limit is '<= 2 Hz'; the calculated expectation is 1.6 Hz. T12d's "
                  "record row states one corner and not one per channel, so this is a file-level "
                  "value; T12e's f0 is explicitly per channel and is nested per channel.")

# T17 -- buttons, mute, headphone level.  Only the constants are here; the button event counts
# are an attribute result and belong in the test record, not in the instrument.
MUTE_ATT = Num("mic_mute_attenuation_db", "dB", "TST-EEG-004 T17", lo=60.0,
               note="T17's limit is '>= 60 dB'.")
HP_LEVEL = Num("level_dbu_into_47r", "dBu into 47.0 ohm", "TST-EEG-004 T17",
               note="T17's limit is 'within 1 dB of target'; the target is per headphone model "
                    "and is not stated numerically in TST-EEG-004, so no bound is imposed here.")
HP_THD = Num("thd_percent", "%", "TST-EEG-004 T17", lo=0.0, hi=0.1,
             note="T17's limit is 'THD <= 0.1 %'.")
HP_LEVEL_REG = Num("level_register", "codec register value", "TST-EEG-004 T17",
                   lo=0, integer=True,
                   note="OPEN: no document in this package states the width of the codec volume "
                        "register, so no upper bound can be imposed. "
                        "README_provisioning.md section 4 item 2.")

# T28 -- maximum acoustic output, a type test run once per lot.  The clamp register value is the
# one constant here the firmware itself must act on (RFQ E-29), and T17 reads it back per unit.
CLAMP_REG = Num("clamp_register", "codec register value", "TST-EEG-004 T28",
                lo=0, integer=True,
                note="The lot clamp. RFQ E-29 requires the firmware to clamp the codec volume "
                     "register at this value; T17 reads it back and 'a clamp value that does "
                     "not match the lot value is a hard fail and is never adjusted on the line'. "
                     "Same missing register width as level_register.")
SPL_CLAMPED = Num("spl_db_at_max_commanded", "dB SPL on an IEC 60318-1 artificial ear",
                  "TST-EEG-004 T28", hi=100.0,
                  note="T28's limit is '<= 100 dB SPL at any commanded level'.")
SPL_FULL = Num("spl_db_at_full_scale", "dB SPL on an IEC 60318-1 artificial ear",
               "TST-EEG-004 T28",
               note="The deliberate full-scale write that bypasses the runner's limit. It is "
                    "expected to exceed 100 dB SPL -- the calculated figure is about 110 -- "
                    "which is why the clamp exists, so no bound is imposed on it.")
HP_IMPEDANCE = Num("headphone_impedance_ohm", "ohm", "TST-EEG-004 T28", lo=32.0, hi=64.0,
                   note="RFQ A-04 as restated by T17: 32 to 64 ohm. The shipped ATH-M20x is "
                        "47 ohm, which is why the T17 load is 47.0 ohm.")

SERIES_R = Num("protection_series_resistor_ohm", "ohm", "DSN-EEG-003 R1-R16 / ECO-EEG-024",
               lo=0.0, integer=True,
               note="The series protection resistor actually fitted: 47000 on the Phase 1 "
                    "prototypes, 68000 if ECO-EEG-024 is taken. T10's R_off acceptance is "
                    "+/- 5 % of this value, so a file without it cannot be interpreted.")

SERIES_R_ALLOWED = [47000, 68000]


def _channel_block(nums, channels, title):
    return {"channels": channels, "nums": nums, "title": title}


def validate(doc, path="<calibration>"):
    """Return a list of human-readable problems.  An empty list means the file conforms."""
    problems = []

    if not isinstance(doc, dict):
        return [f"{path}: the calibration file must be a JSON object"]

    # ---- identity block
    if doc.get("schema") != SCHEMA_ID:
        problems.append(f"{path}: \"schema\" must be \"{SCHEMA_ID}\", found "
                        f"{doc.get('schema')!r}")
    serial = doc.get("unit_serial")
    if not isinstance(serial, str) or not SERIAL_RE.match(serial):
        problems.append(f"{path}: \"unit_serial\" must match TIOV-B-nnnn "
                        f"(PKG-EEG-015 section 5), found {serial!r}")
    if not isinstance(doc.get("measured_utc"), str):
        problems.append(f"{path}: \"measured_utc\" must be an ISO-8601 UTC timestamp string")
    if not isinstance(doc.get("example_only"), bool):
        problems.append(f"{path}: \"example_only\" must be present and boolean. It exists so "
                        f"that a template cannot be mistaken for a measurement.")

    # ---- the fitted series resistor, which every T10 bound depends on
    sr = doc.get(SERIES_R.key)
    SERIES_R.check(sr, f"{path}.{SERIES_R.key}", problems) if sr is not None else \
        problems.append(f"{path}: \"{SERIES_R.key}\" is required")
    if isinstance(sr, (int, float)) and sr not in SERIES_R_ALLOWED:
        problems.append(f"{path}.{SERIES_R.key}: {sr} is neither 47000 (as built) nor 68000 "
                        f"(ECO-EEG-024). If a third value is fitted, that is an ECO and this "
                        f"schema follows it.")

    # ---- T7 gains, thirteen channels
    gains = doc.get("channel_gain_ppm")
    if not isinstance(gains, dict):
        problems.append(f"{path}: \"channel_gain_ppm\" must be an object keyed by stream "
                        f"channel number (ICD-EEG-006 section 5.2)")
    else:
        for ch in GAIN_CHANNELS:
            k = str(ch)
            if k not in gains:
                problems.append(f"{path}.channel_gain_ppm: channel {ch} "
                                f"({CHANNEL_NAMES[ch]}) is missing")
            else:
                GAIN.check(gains[k], f"{path}.channel_gain_ppm.{ch}", problems)
        for k in gains:
            if not k.isdigit() or int(k) not in GAIN_CHANNELS:
                problems.append(f"{path}.channel_gain_ppm: {k!r} is not one of the thirteen "
                                f"channels T7 measures (1-11, 15, 16)")

    # ---- T10 lead-off, eight EEG channels
    lo = doc.get("lead_off")
    if not isinstance(lo, dict):
        problems.append(f"{path}: \"lead_off\" must be an object keyed by EEG channel number")
    else:
        for ch in EEG_CHANNELS:
            k = str(ch)
            e = lo.get(k)
            if not isinstance(e, dict):
                problems.append(f"{path}.lead_off: channel {ch} is missing or is not an object")
                continue
            R_OFF.check(e.get(R_OFF.key), f"{path}.lead_off.{ch}.{R_OFF.key}", problems)
            K_SLOPE.check(e.get(K_SLOPE.key), f"{path}.lead_off.{ch}.{K_SLOPE.key}", problems)
            r = e.get(R_OFF.key)
            if isinstance(r, (int, float)) and isinstance(sr, (int, float)) and sr:
                if not (0.95 * sr <= r <= 1.05 * sr):
                    problems.append(
                        f"{path}.lead_off.{ch}.{R_OFF.key}: {r} ohm is outside the fitted "
                        f"series-resistor value {sr} ohm +/- 5 % ({0.95*sr:.0f} to "
                        f"{1.05*sr:.0f}), which TST-EEG-004 T10 makes the acceptance limit")
        for k in lo:
            if not k.isdigit() or int(k) not in EEG_CHANNELS:
                problems.append(f"{path}.lead_off: {k!r} is not one of the eight EEG channels "
                                f"T10 measures (1-8)")

    # ---- T12 envelope, three channels plus two file-level values
    env = doc.get("envelope")
    if not isinstance(env, dict):
        problems.append(f"{path}: \"envelope\" must be an object keyed by envelope channel "
                        f"number (12, 13, 14)")
    else:
        for ch in ENV_CHANNELS:
            k = str(ch)
            e = env.get(k)
            if not isinstance(e, dict):
                problems.append(f"{path}.envelope: channel {ch} ({CHANNEL_NAMES[ch]}) is "
                                f"missing or is not an object")
                continue
            for n in (ENV_SCALING, ENV_DELAY, ENV_IQR, ENV_F0):
                n.check(e.get(n.key), f"{path}.envelope.{ch}.{n.key}", problems)
        for k in env:
            if not k.isdigit() or int(k) not in ENV_CHANNELS:
                problems.append(f"{path}.envelope: {k!r} is not an envelope channel (12, 13, 14)")
    for n in (ENV_COMPARATOR, ENV_AC):
        if n.key not in doc:
            problems.append(f"{path}: \"{n.key}\" is required ({n.source})")
        else:
            n.check(doc[n.key], f"{path}.{n.key}", problems)

    # ---- T17 audio
    hp = doc.get("headphone")
    if not isinstance(hp, dict):
        problems.append(f"{path}: \"headphone\" must be an object")
    else:
        for n in (HP_LEVEL, HP_THD, HP_LEVEL_REG):
            n.check(hp.get(n.key), f"{path}.headphone.{n.key}", problems)
    if MUTE_ATT.key not in doc:
        problems.append(f"{path}: \"{MUTE_ATT.key}\" is required ({MUTE_ATT.source})")
    else:
        MUTE_ATT.check(doc[MUTE_ATT.key], f"{path}.{MUTE_ATT.key}", problems)

    # ---- T28 acoustic, per lot
    ac = doc.get("acoustic")
    if not isinstance(ac, dict):
        problems.append(f"{path}: \"acoustic\" must be an object carrying the T28 lot values")
    else:
        for n in (CLAMP_REG, SPL_CLAMPED, SPL_FULL, HP_IMPEDANCE):
            n.check(ac.get(n.key), f"{path}.acoustic.{n.key}", problems)
        if not isinstance(ac.get("headphone_model"), str):
            problems.append(f"{path}.acoustic.headphone_model: required, a string. T28 records "
                            f"the headphone model because the clamp is only valid for it.")
        if not isinstance(ac.get("lot"), str):
            problems.append(f"{path}.acoustic.lot: required, a string. T28 is run once per lot, "
                            f"so the file must say which lot its clamp came from.")
    known = {"schema", "unit_serial", "measured_utc", "example_only", SERIES_R.key,
             "channel_gain_ppm", "lead_off", "envelope", ENV_COMPARATOR.key, ENV_AC.key,
             MUTE_ATT.key, "headphone", "acoustic", "instruments", "_note"}
    for k in doc:
        if k not in known:
            problems.append(f"{path}: {k!r} is not a key this schema defines. A constant that "
                            f"belongs in the file belongs in calibration_schema.py first, so "
                            f"that every shop writes it under the same name.")
    return problems


# --------------------------------------------------------------------------- generated files
def json_schema():
    def obj(props, required):
        return {"type": "object", "properties": props, "required": required,
                "additionalProperties": False}

    gain_props = {str(c): dict(GAIN.json_schema(),
                               title=f"channel {c} ({CHANNEL_NAMES[c]})")
                  for c in GAIN_CHANNELS}
    lead_props = {str(c): obj({R_OFF.key: R_OFF.json_schema(), K_SLOPE.key: K_SLOPE.json_schema()},
                              [R_OFF.key, K_SLOPE.key]) for c in EEG_CHANNELS}
    env_nums = [ENV_SCALING, ENV_DELAY, ENV_IQR, ENV_F0]
    env_props = {str(c): obj({n.key: n.json_schema() for n in env_nums},
                             [n.key for n in env_nums]) for c in ENV_CHANNELS}

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://one.witysk.org/eeg/calibration_schema.json",
        "title": f"EEG field-kit calibration file ({SCHEMA_ID})",
        "description":
            "The file firmware/tools/provision.py writes into the unit at TST-EEG-004 T6. "
            "GENERATED by firmware/tools/calibration_schema.py -- edit that file and run it "
            "again, do not edit this one. PROPOSAL: the key names and nesting are the "
            "programme's decision (FW-EEG-001 section 10 assigns the calibration-record schema "
            "to CAL-EEG-012); every key and every bound here is one quantity a numbered test "
            "says it records. Licence: CC BY-SA 4.0.",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema", "unit_serial", "measured_utc", "example_only",
                     SERIES_R.key, "channel_gain_ppm", "lead_off", "envelope",
                     ENV_COMPARATOR.key, ENV_AC.key, MUTE_ATT.key, "headphone", "acoustic"],
        "properties": {
            "schema": {"const": SCHEMA_ID},
            "unit_serial": {"type": "string", "pattern": "^TIOV-B-[0-9]{4}$",
                            "description": "PKG-EEG-015 section 5. provision.py refuses a file "
                                           "whose unit_serial is not the serial it was given."},
            "measured_utc": {"type": "string",
                             "description": "when the constants were measured, ISO-8601 UTC"},
            "example_only": {"type": "boolean",
                             "description": "true in the shipped example. provision.py refuses "
                                            "to write a file with example_only true, so a "
                                            "template cannot reach a unit."},
            SERIES_R.key: dict(SERIES_R.json_schema(), enum=SERIES_R_ALLOWED),
            "channel_gain_ppm": obj(gain_props, [str(c) for c in GAIN_CHANNELS]),
            "lead_off": obj(lead_props, [str(c) for c in EEG_CHANNELS]),
            "envelope": obj(env_props, [str(c) for c in ENV_CHANNELS]),
            ENV_COMPARATOR.key: ENV_COMPARATOR.json_schema(),
            ENV_AC.key: ENV_AC.json_schema(),
            MUTE_ATT.key: MUTE_ATT.json_schema(),
            "headphone": obj({n.key: n.json_schema() for n in (HP_LEVEL, HP_THD, HP_LEVEL_REG)},
                             [n.key for n in (HP_LEVEL, HP_THD, HP_LEVEL_REG)]),
            "acoustic": obj({
                CLAMP_REG.key: CLAMP_REG.json_schema(),
                SPL_CLAMPED.key: SPL_CLAMPED.json_schema(),
                SPL_FULL.key: SPL_FULL.json_schema(),
                HP_IMPEDANCE.key: HP_IMPEDANCE.json_schema(),
                "headphone_model": {"type": "string"},
                "lot": {"type": "string"},
            }, [CLAMP_REG.key, SPL_CLAMPED.key, SPL_FULL.key, HP_IMPEDANCE.key,
                "headphone_model", "lot"]),
            "_note": {"type": "array", "items": {"type": "string"},
                      "description": "optional free prose. The shipped example uses it to say, "
                                     "in the file itself, that the file carries no "
                                     "measurements."},
            "instruments": {"type": "object",
                            "description": "optional. JIG-EEG-009 section 5.2 requires the asset "
                                           "numbers of the instruments used to appear in each "
                                           "unit's record; carry them here if the station has "
                                           "them.",
                            "additionalProperties": {"type": "string"}},
        },
    }


def example():
    """A template, not a measurement.  Every numeric field carries the CALCULATED expectation the
    test specification already publishes, or the nominal, and `example_only` is true so that
    provision.py refuses to write it into a unit.  There is no measured value in this file
    because no unit has been built."""
    return {
        "schema": SCHEMA_ID,
        "unit_serial": "TIOV-B-0000",
        "measured_utc": "1970-01-01T00:00:00Z",
        "example_only": True,
        "_note": [
            "TEMPLATE. This file contains NO measurements. Every number in it is either a",
            "nominal or the calculated expectation TST-EEG-004 already publishes for that",
            "quantity, and it is here to show the shape of the file and to exercise the",
            "validator -- not to be copied into a unit record.",
            "TIOV-B-0000 is the unprovisioned default in firmware/main/drivers.c",
            "unit_serial_into(), so it can never be a real unit serial, and example_only is",
            "true, so provision.py refuses to write this file into a device.",
            "Generated by firmware/tools/calibration_schema.py --emit. Licence: CC BY-SA 4.0."
        ],
        SERIES_R.key: 47000,
        "channel_gain_ppm": {str(c): 0 for c in GAIN_CHANNELS},
        "lead_off": {str(c): {R_OFF.key: 47000.0, K_SLOPE.key: 1.0} for c in EEG_CHANNELS},
        "envelope": {str(c): {ENV_SCALING.key: 100.0,
                              ENV_DELAY.key: 4.40,
                              ENV_IQR.key: 0.0,
                              ENV_F0.key: 48.8} for c in ENV_CHANNELS},
        ENV_COMPARATOR.key: 52.0,
        ENV_AC.key: 1.6,
        MUTE_ATT.key: 60.0,
        "headphone": {HP_LEVEL.key: 0.0, HP_THD.key: 0.0, HP_LEVEL_REG.key: 0},
        "acoustic": {
            CLAMP_REG.key: 0,
            SPL_CLAMPED.key: 100.0,
            SPL_FULL.key: 110.0,
            HP_IMPEDANCE.key: 47.0,
            "headphone_model": "TEMPLATE -- the model T28 was run on",
            "lot": "TEMPLATE -- the lot T28 was run on",
        },
    }


def _dump(o):
    return json.dumps(o, indent=2, sort_keys=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--emit", action="store_true",
                    help="write calibration_schema.json and cal_TIOV-B-0000.example.json")
    ap.add_argument("--check", action="store_true",
                    help="compare the generated files on disk with this table; exit 1 if they "
                         "have drifted")
    ap.add_argument("--validate", metavar="FILE", help="validate a calibration file")
    a = ap.parse_args()

    if a.validate:
        with open(a.validate) as f:
            doc = json.load(f)
        problems = validate(doc, os.path.basename(a.validate))
        if problems:
            print(f"{len(problems)} problem(s):")
            for p in problems:
                print("  -", p)
            return 1
        print(f"{a.validate} conforms to {SCHEMA_ID}")
        if doc.get("example_only"):
            print("NOTE: example_only is true. provision.py will refuse to write this file.")
        return 0

    want = {SCHEMA_PATH: _dump(json_schema()), EXAMPLE_PATH: _dump(example())}

    if a.check:
        bad = False
        for path, text in want.items():
            try:
                have = open(path).read()
            except FileNotFoundError:
                print(f"MISSING {path}")
                bad = True
                continue
            if have != text:
                print(f"DRIFTED {path}")
                bad = True
        # the shipped example must itself conform, or the schema and the example disagree
        problems = validate(example(), "example")
        if problems:
            print("the generated example does not satisfy the generated schema:")
            for p in problems:
                print("  -", p)
            bad = True
        print("generated files match the table" if not bad else "run --emit to regenerate")
        return 1 if bad else 0

    if a.emit:
        for path, text in want.items():
            with open(path, "w") as f:
                f.write(text)
            print(f"wrote {path}")
        problems = validate(example(), "example")
        if problems:
            print("WARNING: the example does not satisfy the schema:")
            for p in problems:
                print("  -", p)
            return 1
        print("the example validates against the table it was generated from")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
