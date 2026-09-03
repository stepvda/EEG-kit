#!/usr/bin/env python3
"""
make_records.py -- the machine-readable half of TST-EEG-004 Rev C section 12.

Section 12 specifies one JSON file per unit, `<unit_serial>_test.json`, and says the field
counts are "fixed so a record can be validated mechanically".  Package v2.3 shipped nothing
to validate against: no schema, no blank record, no example, no lot-summary template and no
certificate template.  Two manufacturers reading section 12's prose would emit different key
names and different nesting for the same 70 T23 currents, 32 T10 impedances and 24 T7a
gains, and neither file could be ingested without hand-mapping -- which is the comparability
failure the document's own opening calls fatal for the study.

This script writes, from one specification table:

  TST-EEG-004_RevC_unit_test_record.schema.json   JSON Schema 2020-12 for the per-unit record
  EXAMPLE_TIOV-B-0000_test.json                   a worked record, every value a placeholder
  lot_summary_template.csv                        the per-lot summary, header row only
  TST-EEG-004_RevC_calibration_certificate.md     the section 13 certificate template
  README.txt                                      what these files are and how to use them

Everything comes out of STEPS, IDENTITY, CONSTANTS, DISPOSITION and SIGNATURES below.  The
schema, the example and the CSV header are three renderings of the same table, so a field
cannot exist in one and be missing from another.  The step list itself is read out of
`docs/TST-EEG-004_RevC_production_test_specification.md` section 2 at generation time, and
this script fails rather than writes if the document's step list and this table disagree --
which is the mechanism that keeps the schema honest when a step is added, as T30 was.

THE EXAMPLE RECORD CONTAINS NO MEASUREMENTS.  Every number in it is the sentinel -9999 or
9999, every hash is sixty-four zeros, every free-text field begins `EXAMPLE-`, the unit
serial is TIOV-B-0000 which PKG-EEG-015 section 5 allocates to no phase block, and every
step verdict is DEFERRED, which is the correct verdict for a step that was not performed.
It is a shape, not a result.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import csv
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
DOCS = os.path.join(PKG, "docs")
TST = os.path.join(DOCS, "TST-EEG-004_RevC_production_test_specification.md")

SCHEMA_ID = ("https://one.witysk.org/eeg-kit/schema/"
             "TST-EEG-004_RevC_unit_test_record.schema.json")
OWNER = "TST-EEG-004 Rev C section 12"
LICENCE = "CC BY-SA 4.0"

EXAMPLE_SERIAL = "TIOV-B-0000"
NUM_PLACEHOLDER = -9999.0
INT_PLACEHOLDER = 9999
ZERO_HASH = "0" * 64

SERIAL_PATTERN = r"^TIOV-B-[0-9]{4}$"
SHA256_PATTERN = r"^[0-9a-f]{64}$"
HEX18_PATTERN = r"^[0-9A-F]{18}$"
HEX16_PATTERN = r"^[0-9A-F]{16}$"
VERDICTS = ["PASS", "FAIL", "DEFERRED", "NOT_APPLICABLE"]


# ---------------------------------------------------------------------------------------
# A very small schema DSL.  Each helper returns (schema fragment, example value), so the
# schema and the worked example are produced from the same call and cannot drift.
# ---------------------------------------------------------------------------------------

def num(desc, unit=None):
    s = {"type": "number", "description": desc}
    if unit:
        s["$comment"] = f"unit: {unit}"
    return s, NUM_PLACEHOLDER


def count(desc):
    return {"type": "integer", "minimum": 0, "description": desc}, INT_PLACEHOLDER


def integer(desc):
    return {"type": "integer", "description": desc}, INT_PLACEHOLDER


def text(desc, pattern=None, example=None):
    s = {"type": "string", "minLength": 1, "description": desc}
    if pattern:
        s["pattern"] = pattern
    return s, example if example is not None else "EXAMPLE-PLACEHOLDER"


def sha256(desc):
    return ({"type": "string", "pattern": SHA256_PATTERN, "description": desc}, ZERO_HASH)


def boolean(desc):
    return {"type": "boolean", "description": desc}, False


def enum(values, desc, example=None):
    return ({"enum": list(values), "description": desc},
            example if example is not None else values[0])


def nums(n, desc, unit=None):
    """Exactly n numbers.  This is where section 12's fixed field counts are enforced."""
    s = {"type": "array", "items": {"type": "number"}, "minItems": n, "maxItems": n,
         "description": desc}
    if unit:
        s["$comment"] = f"unit: {unit}"
    return s, [NUM_PLACEHOLDER] * n


def strings(n, desc, pattern=None):
    item = {"type": "string", "minLength": 1}
    if pattern:
        item["pattern"] = pattern
    return ({"type": "array", "items": item, "minItems": n, "maxItems": n,
             "description": desc},
            ["EXAMPLE-PLACEHOLDER"] * n)


def verdicts_n(n, desc):
    return ({"type": "array", "items": {"enum": VERDICTS}, "minItems": n, "maxItems": n,
             "description": desc},
            ["DEFERRED"] * n)


def string_list(desc, min_items=0):
    return ({"type": "array", "items": {"type": "string"}, "minItems": min_items,
             "description": desc},
            ["EXAMPLE-PLACEHOLDER"] * min_items)


def obj(fields, desc, required=None, additional=False):
    props, example = {}, {}
    for k, (s, v) in fields.items():
        props[k] = s
        example[k] = v
    s = {"type": "object", "description": desc, "properties": props,
         "required": list(required if required is not None else fields.keys()),
         "additionalProperties": additional}
    return s, example


def obj_array(fields, desc, min_items=1, max_items=None, n_example=1):
    item_schema, item_example = obj(fields, desc + " (one entry)")
    s = {"type": "array", "items": item_schema, "minItems": min_items,
         "description": desc}
    if max_items is not None:
        s["maxItems"] = max_items
    return s, [item_example] * n_example


def nullable(pair, desc=None):
    s, v = pair
    return ({"oneOf": [s, {"type": "null"}],
             "description": desc or s.get("description", "")}, None)


# ---------------------------------------------------------------------------------------
# 1.  Identity.  TST-EEG-004 Rev C section 12, "Identity".
# ---------------------------------------------------------------------------------------

MODULE_KEYS = [
    ("ads1299_a", "First ADS1299 module"),
    ("ads1299_b", "Second ADS1299 module"),
    ("devkitc1", "ESP32-S3-DevKitC-1, N16R8"),
    ("adum4160", "ADuM4160 USB isolator module"),
    ("es8388", "ES8388 codec module"),
    ("charger", "Charger module"),
    ("gauge", "MAX17048 fuel gauge module"),
    ("shift_register", "Contact-light shift register module"),
    ("microsd_breakout", "microSD breakout"),
    ("preamp", "Boom microphone preamplifier module"),
    ("cell", "Protected 18650 cell"),
    ("card", "microSD card"),
]

IDENTITY = {
    "unit_serial": text("Unit serial. The format is defined in PKG-EEG-015 Rev B section 5 "
                        "and nowhere else.", SERIAL_PATTERN, EXAMPLE_SERIAL),
    "hw_rev": ({"const": "EEG-CAR-01-B",
                "description": "Hardware revision, and the same letter as the one in the "
                               "serial (PKG-EEG-015 section 4.1)."}, "EEG-CAR-01-B"),
    "gerber_revision": text("The routed-Gerber revision the board was made from."),
    "carrier_board_serial_or_panel_position": text("Carrier board serial, or its panel "
                                                   "position where the fabricator serialises "
                                                   "by position (T0)."),
    "firmware_version": text("Firmware version string."),
    "firmware_sha256": sha256("SHA-256 of the firmware image."),
    "provisioning_script_version": text("Version of firmware/tools/provision.py used at T6."),
    "tool_eeg_022_sha256": sha256("SHA-256 of the webtest/EEG-Connectivity-Test.html file "
                                  "used at T30."),
    "stream_decoder": nullable(
        obj({"version": text("Stream-decoding tool version."),
             "sha256": sha256("SHA-256 of the stream-decoding tool.")},
            "The host stream-decoding tool."),
        "The stream-decoding tool's version and SHA-256, once that tool exists. "
        "TST-EEG-004 section 16 item 10 records that it does not, so null is the correct "
        "value today and the eleven decoding steps are DEFERRED with that reason."),
    "atecc_factory_serial": text("ATECC608B 9-byte factory serial, 18 uppercase hex "
                                 "(T00 and T6).", HEX18_PATTERN, "0" * 18),
    "pubkey_pem": text("Uncompressed P-256 public key in PEM, exported at T6.",
                       example="-----BEGIN PUBLIC KEY-----\nEXAMPLE-PLACEHOLDER\n"
                               "-----END PUBLIC KEY-----\n"),
    "key_fingerprint": text("Public-key fingerprint, computed as FW-EEG-001 Rev C section 7 "
                            "defines it, and identical to the string printed on the label.",
                            HEX16_PATTERN, "0" * 16),
    "vid": text("USB vendor ID as programmed at T6.", r"^0x[0-9A-Fa-f]{4}$", "0x0000"),
    "pid": text("USB product ID as programmed at T6.", r"^0x[0-9A-Fa-f]{4}$", "0x0000"),
    "modules": obj({k: obj({"serial_or_lot": text(f"{d}: serial where the module carries "
                                                  f"one, otherwise the lot code."),
                            "supplier": text(f"{d}: supplier.")},
                           d)
                    for k, d in MODULE_KEYS},
                   "Module serials or lot codes for the twelve module types of "
                   "TST-EEG-004 section 12."),
    "build_lot": text("Build lot identifier."),
    "manufacturer": text("Manufacturer legal entity."),
    "operator_id": text("Operator identifier."),
    "qa_id": text("Manufacturer QA identifier."),
    "date_time": text("Date and time the record was closed, ISO 8601 with an offset.",
                      r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}([+-]\d{2}:\d{2}|Z)$",
                      "1970-01-01T00:00:00Z"),
    "fixture_serial": text("Fixture serial, the JIG-EEG-009 unit number."),
    "ambient_temperature_c": num("Ambient temperature during the characterisation steps.",
                                 "degC"),
    "relative_humidity_percent": num("Relative humidity during the characterisation steps.",
                                     "%"),
    "instruments": obj_array(
        {"asset_number": text("Instrument asset number."),
         "description": text("What the instrument is."),
         "calibration_due": text("Calibration due date, ISO 8601 date.",
                                 r"^\d{4}-\d{2}-\d{2}$", "1970-01-01")},
        "Every instrument used, by asset number, with its calibration due date "
        "(TST-EEG-004 section 5).", min_items=1),
}


# ---------------------------------------------------------------------------------------
# 2.  The steps.  One entry per step of TST-EEG-004 Rev C section 2.
#
# `unit`, `limit` and `uncertainty` are the strings from that step's own table in section 8;
# they are carried in the record so a reader of the record alone can see what the number was
# judged against.  `data` is the step's "value(s)": a scalar where the step produces one, and
# an object of named arrays where section 12 fixes a count.  Every count in section 12 is a
# minItems == maxItems pair here, which is what makes the record mechanically checkable.
# ---------------------------------------------------------------------------------------

def step(unit, limit, uncertainty, data_fields, data_desc="Measured values for this step."):
    return {"unit": unit, "limit": limit, "uncertainty": uncertainty,
            "data": obj(data_fields, data_desc)}


STEPS = {
"T00": step(
    "attribute; V for OCV",
    "Every check pass; DevKit variant exactly N16R8; cell OCV in band; documents present",
    "Attribute checks. OCV +/- 0.5 mV; AVDD/AVSS +/- 1 mV",
    {"modules": obj_array(
        {"module_type": text("Module type as named in TST-EEG-004 T00."),
         "quantity": count("Quantity in the inspected lot."),
         "lot": text("Supplier lot."),
         "verdict": enum(VERDICTS, "Verdict for this module type.", "DEFERRED")},
        "Per module type: quantity, lot and verdict."),
     "ads1299_marking_photograph_ref": text("Reference to the ADS1299 package-marking "
                                            "photograph."),
     "devkit_flash_mb": ({"const": 16, "description": "esptool flash_id must report 16 MB "
                                                      "flash; the variant is exactly "
                                                      "N16R8."}, 16),
     "devkit_psram_mb": ({"const": 8, "description": "esptool flash_id must report 8 MB "
                                                     "PSRAM."}, 8),
     "atecc_factory_serials": string_list("ATECC608B factory serials read at incoming, "
                                          "18 uppercase hex each.", min_items=1),
     "cell_ocv_v": ({"type": "array", "items": {"type": "number"}, "minItems": 1,
                     "description": "Cell open-circuit voltages, 3.4 to 3.9 V."},
                    [NUM_PLACEHOLDER]),
     "isolator_host_connector": enum(["USB-B", "USB-C"],
                                     "The host receptacle the delivered ADuM4160 module "
                                     "actually has. USB-B is the live non-conformance "
                                     "against RFQ E-24 that WH-09 answers.", "USB-B"),
     "c1_to_c16_part_number": ({"const": "Murata GCM1885C1H103JA16D",
                                "description": "C1 to C16 are C0G by part number. An X7R "
                                               "part in that position is a hard reject."},
                               "Murata GCM1885C1H103JA16D"),
     "certificate_references": string_list("Certificate references collected at T00, "
                                           "including the ADuM4160 2.5 kV RMS isolation "
                                           "type-test certificate and the cell UN 38.3 "
                                           "report and MSDS.", min_items=1)}),

"T0": step(
    "Ohm, MOhm, attribute",
    "Continuity <= 10 Ohm, and <= 5 Ohm on VBAT, VSYS, V5V, DVDD3V3, DGND, AGND_REF; "
    "isolation >= 10 MOhm at 100 V, and >= 100 MOhm at 250 V for AGND_REF to DGND; no "
    "copper in the keep-out on any layer; NPTH holes unplated",
    "Tester repeatability, typically +/- 2 % of reading",
    {"et_certificate_ref": text("The fabricator's electrical-test certificate reference, "
                                "per lot."),
     "board_serial_or_panel_position": text("Board serial or panel position."),
     "checks": obj(
         {"a_agnd_ref_to_dgnd_isolation_Mohm": num("Check (a): AGND_REF to DGND isolation, "
                                                   "measured against BOTH inner reference "
                                                   "planes.", "MOhm"),
          "b_harn_shield_isolation_Mohm": nums(2, "Check (b): HARN_SHIELD to DGND and to "
                                                  "AGND_REF.", "MOhm"),
          "c_keepout_clear_all_four_layers": boolean("Check (c): no conductor of any of the "
                                                     "four layers inside the isolation "
                                                     "keep-out."),
          "d_npth_holes_unplated": boolean("Check (d): the four 3.2 mm M3 holes and the six "
                                           "1.50 mm DIN retention holes are unplated.")},
         "The four dedicated checks of T0."),
     "stackup_as_built_mm": num("Stack-up as built, against 1.60 mm +/- 10 %.", "mm"),
     "netlist_file_sha256": sha256("SHA-256 of the IPC-D-356A netlist the test was run "
                                   "against.")}),

"T1": step(
    "attribute",
    "No class 2 defect; every explicit check pass",
    "Attribute inspection; two-person check on the first five boards of a lot",
    {"defect_codes": string_list("IPC-A-610 class 2 defect codes found."),
     "rework_image_refs": string_list("Images of any rework site."),
     "two_person_check": boolean("Whether the two-person check was applied (first five "
                                 "boards of a lot)."),
     "explicit_checks_pass": boolean("Every explicit check of T1 passed: socket pin-1, "
                                     "U1 to U3 orientation, D1 to D16 BAV99, D20/D40/D60 "
                                     "BAT54S with pin 3 on the op-amp output, R89 DNP, "
                                     "R90 to R93 fitted once, R94 and R95 fitted, three "
                                     "fiducials, TP1 to TP18, legend.")}),

"T2": step(
    "Ohm",
    "All present and continuous, < 1 Ohm per checked pin; every jumper keyed at both ends",
    "Attribute",
    {"module_assemblies_present": count("Module assemblies found seated. Thirteen is the "
                                        "expected count: twelve on MP-01 plus the "
                                        "DevKitC-1 in J6 and J7."),
     "checked_pin_resistances_ohm": ({"type": "array", "items": {"type": "number"},
                                      "minItems": 1,
                                      "description": "One resistance per checked pin, in "
                                                     "the J1.1, J2.1, J23.1, J3.1, J4.1, "
                                                     "J29.1, J8.1, J10.1, J11.1, J12.1, "
                                                     "J19.1, J20.1, J21.1, J25.1, J28.1 "
                                                     "order of T2."},
                                     [NUM_PLACEHOLDER]),
     "keying_shroud_fitted": boolean("WH-KEY-01 fitted over every carrier socket that "
                                     "ICD-EEG-006 section 6 lists as taking a jumper."),
     "insertion_cycles": ({"type": "object",
                           "additionalProperties": {"type": "integer", "minimum": 0},
                           "description": "Insertion cycles per socket, logged. Maximum "
                                          "two per socket."}, {})}),

"T3": step(
    "mA, V, degC",
    "Idle < 90 mA; recording at 1000 Hz < 150 mA; rails within 3 %; regulator case "
    "temperature < 85 degC",
    "Combined 0.28 %, U(k=2) = 0.56 %, i.e. +/- 0.8 mA at 150 mA. Temperature +/- 2 degC",
    {"current_idle_ma": num("Current at idle after 60 s settling.", "mA"),
     "current_recording_1000hz_ma": num("Current recording at 1000 Hz after a further "
                                        "60 s.", "mA"),
     "rail_voltages_v": nums(5, "DVDD3V3 at TP12, VSYS at TP15, V5V at TP16, AVDD at TP10, "
                                "AVSS at TP11, in that order.", "V"),
     "regulator_case_temperature_c": num("DevKitC-1 on-board 3.3 V regulator case "
                                         "temperature after 30 minutes at 1000 Hz with the "
                                         "pod closed.", "degC"),
     "supply_voltage_measured_v": num("Bench supply voltage as measured.", "V"),
     "ambient_temperature_c": num("Ambient temperature.", "degC")}),

"T4": step(
    "mA",
    "Charge current < 1 mA while the session is active",
    "Shunt 0.1 %, DMM 10 uV, combined U(k=2) < 30 uA. TUR against 1 mA is 33:1",
    {"charge_current_session_active_ma": num("Current into VBUS_CHG with a session active.",
                                             "mA"),
     "negative_control_charge_current_ma": num("The negative control: session inactive, "
                                               "charging permitted. Without it a dead "
                                               "charger passes by accident.", "mA")}),

"T5": step(
    "attribute",
    "Both interfaces visible on all three hosts with no driver installation; VID and PID "
    "equal to the values programmed in T6; iSerial equal to the unit serial",
    "Attribute",
    {"hosts": obj_array(
        {"os_build": text("Host OS build string."),
         "cdc_acm_visible": boolean("A CDC-ACM port appeared."),
         "winusb_vendor_interface_visible": boolean("A WinUSB-bound vendor interface is "
                                                    "visible with no driver prompt."),
         "verdict": enum(VERDICTS, "Verdict for this host.", "DEFERRED")},
        "Three host results: Windows 11, macOS and Linux.", min_items=3, max_items=3,
        n_example=3),
     "vid": text("Enumerated vendor ID.", r"^0x[0-9A-Fa-f]{4}$", "0x0000"),
     "pid": text("Enumerated product ID.", r"^0x[0-9A-Fa-f]{4}$", "0x0000"),
     "iserial_t5b": text("iSerialNumber read at T5b. It must equal the unit serial "
                         "character for character.", SERIAL_PATTERN, EXAMPLE_SERIAL),
     "descriptor_dump_ref": text("Reference to the descriptor dump saved by the host tool."),
     "wh09_pigtail_in_path": boolean("Whether the WH-09 USB-B-to-USB-C pigtail was in the "
                                     "path.")}),

"T6": step(
    "attribute",
    "Key generated, public key exported, lock confirmed by readback, constants read back "
    "byte-identical to those written",
    "Attribute",
    {"atecc_factory_serial": text("ATECC608B factory serial.", HEX18_PATTERN, "0" * 18),
     "key_fingerprint": text("Fingerprint as FW-EEG-001 Rev C section 7 defines it, and "
                             "exactly as printed on the label.", HEX16_PATTERN, "0" * 16),
     "config_zone_locked": boolean("Lock confirmed by readback. A locked config zone "
                                   "cannot be undone."),
     "constants_readback_identical": boolean("The constant block read back byte-identical "
                                             "to what was written.")}),

"T7": step(
    "ppm of nominal",
    "Matching between the eight EEG channels within 0.5 % after calibration, at the 100 uV "
    "and 1 mV points only. The 10 uV point is a linearity check with a +/- 5 % limit",
    "U(k=2) = 0.134 % at 100 uV and 1 mV; U(k=2) = 0.22 % at 10 uV (JIG-EEG-009 section 1.4)",
    {"a_eeg_gains_ppm": nums(24, "T7a: eight EEG channels at three levels -- 1 mV, 100 uV "
                                 "and 10 uV -- channel-major.", "ppm"),
     "a_gain_constants_ppm": nums(8, "T7a: the eight EEG gain constants that go to the "
                                     "device.", "ppm"),
     "b_emg_gains_ppm": nums(9, "T7b: three EMG channels at three levels, channel-major.",
                             "ppm"),
     "c_spare_gains_ppm": nums(2, "T7c: the two spare channels at 100 uV only.", "ppm"),
     "divider_input_v": nums(3, "The measured divider input voltage at each level.", "V"),
     "generator_frequency_hz": num("Generator frequency.", "Hz"),
     "record_lengths_s": nums(3, "Record length at each level: 60 s, 60 s, 240 s.", "s")}),

"T8": step(
    "uV RMS",
    "<= 1.0 uV RMS on each EEG channel; pass on the median epoch. Calculated expectation "
    "0.27 uV RMS with the 47 kOhm fitted",
    "Combined 2.2 %, U(k=2) = 4.3 %, i.e. +/- 0.04 uV. TUR against 1.0 uV is 23:1",
    {"whole_record_rms_uv": nums(8, "Whole-record RMS on each EEG channel.", "uV RMS"),
     "epoch_median_rms_uv": nums(8, "Median of the ten 6 s epochs on each EEG channel.",
                                 "uV RMS"),
     "excluded_bins_hz": nums(2, "The bin-excluded frequencies: 50 Hz and 100 Hz.", "Hz"),
     "ambient_temperature_c": num("Ambient temperature.", "degC"),
     "fitted_series_resistor_kohm": num("The fitted R1 to R16 value: 47 kOhm as built, "
                                        "68 kOhm only if ECO-EEG-024 is taken.", "kOhm")}),

"T9": step(
    "dB",
    "Crosstalk < -80 dB, measured on the carrier; CMRR >= 100 dB -- a provisional limit "
    "that TST-EEG-004 sets and no requirement carries (section 16 item 15)",
    "Crosstalk U(k=2) = 0.4 dB at -80 dB with a 600 s record; CMRR U(k=2) = 0.5 dB",
    {"a_crosstalk_db": nums(16, "T9a: eight victim channels for each of the two aggressor "
                                "positions, channel 1 and channel 8.", "dB"),
     "a_detection_floor_db": nums(16, "The detection floor beside every crosstalk value. "
                                      "Each must sit at least 10 dB below the -80 dB "
                                      "decision.", "dB"),
     "a_aggressor_off_ambient_db": nums(16, "The aggressor-off ambient bin beside every "
                                            "crosstalk value.", "dB"),
     "a_aggressor_amplitude_mv_measured": num("Aggressor amplitude as measured, not as "
                                              "commanded.", "mV RMS"),
     "b_cmrr_db": nums(8, "T9b: common-mode rejection on the eight EEG channels.", "dB"),
     "c_type_test_reference": nullable(
         text("Reference to the T9c contact-light interference type test."),
         "T9c is a TYPE TEST on the first prototype of each build standard and any unit "
         "whose harness is rebuilt, not a per-unit step, so null is correct for a unit "
         "that is not that prototype.")}),

"T10": step(
    "Ohm",
    "R_off within the fitted series-resistor value +/- 5 %, and after correction each of "
    "the three reference points reported within 15 %",
    "See TST-EEG-004 T10",
    {"raw_impedances": nums(32, "Eight channels x three reference points, plus the OPEN "
                                "residual per channel: 32 raw values.", "Ohm"),
     "constants": obj_array(
         {"r_off_ohm": num("R_off for this channel.", "Ohm"),
          "k": num("Slope k for this channel.", "dimensionless")},
         "Eight (R_off, k) pairs -- sixteen constants.", min_items=8, max_items=8,
         n_example=8)}),

"T11": step(
    "ratio, cd/m2, Hz",
    "Mapping correct site for site, LED1 to LED8 against helmet sites 1 to 8; green state "
    "ratio R/G <= 0.30; red state R/G >= 3.0; amber state 0.6 <= R/G <= 1.7; both dark "
    "states below 2 % of the green-state luminance",
    "See TST-EEG-004 T11",
    {"colour_ratios": nums(24, "Eight sites x three colour states (green, red, amber), "
                               "site-major, as R/G ratios.", "ratio"),
     "dark_state_luminances": nums(2, "The two dark-state luminances.", "cd/m2"),
     "light_phase_hz": num("LIGHT_PHASE_HZ as read back from the device.", "Hz"),
     "mapping_correct": boolean("LED1 to LED8 map to helmet sites 1 to 8, site for site.")}),

"T12": step(
    "uV per full scale, samples, mV, Hz",
    "Scaling within +/- 5 % of 100 mV at the converter input. Group-delay spread <= 2 "
    "samples. Comparator trips between 45 and 60 mV. T12d AC corner <= 2 Hz. T12e f0 "
    "between 42 and 58 Hz",
    "See TST-EEG-004 T12",
    {"a_scalings": nums(3, "T12a: the three envelope-channel scalings.",
                        "uV per full scale"),
     "b_group_delay_median_samples": nums(3, "T12b: median group delay per envelope "
                                             "channel. Calculated expectation 4.40 samples "
                                             "at 1000 Hz.", "samples"),
     "b_group_delay_iqr_samples": nums(3, "T12b: interquartile range per envelope channel.",
                                       "samples"),
     "c_comparator_threshold_mv": num("T12c: comparator trip threshold.", "mV"),
     "d_ac_coupling_corner_hz": num("T12d: measured AC-coupling corner. Calculated "
                                    "expectation 1.6 Hz.", "Hz"),
     "e_lowpass_f0_hz": num("T12e: measured low-pass corner f0. Calculated expectation "
                            "48.8 Hz. The 42 to 58 Hz band is wider than RFQ E-11's "
                            "50 Hz +/- 10 %, which section 16 item 16 carries.", "Hz")}),

"T13": step(
    "samples",
    "Median <= 1 sample, 95th percentile <= 2 samples",
    "See TST-EEG-004 T13",
    {"median_samples": num("Median timing residual.", "samples"),
     "p95_samples": num("95th-percentile timing residual.", "samples"),
     "residuals": nums(40, "All forty residuals, retained.", "samples"),
     "group_delay_constant_used_samples": num("The group-delay constant the residuals were "
                                              "computed against.", "samples")}),

"T14": step(
    "frames, ms",
    "Zero missing sequence numbers, and the card copy identical to the host copy",
    "See TST-EEG-004 T14",
    {"frames_written": count("Frames written to the card."),
     "frames_expected": count("Frames expected, computed by the tool from the frame length "
                              "the device reports. 90 000 at 20 samples per frame."),
     "frames_missing": count("Missing sequence numbers. The limit is zero."),
     "card_versus_host_mismatches": count("Card-versus-host mismatch count."),
     "mean_write_latency_ms": num("Mean write latency.", "ms"),
     "worst_write_latency_ms": num("Worst write latency.", "ms"),
     "card_part_number": text("microSD card part number."),
     "card_serial": text("microSD card serial.")}),

"T15": step(
    "frames, kB/s, s",
    "Complete recovery of the 60 s, no reset of the sample counter, GAP frames only beyond "
    "the declared ring depth, a declared ring depth of at least 90 s, and a backfill rate "
    "of at least three times the live rate (F-12)",
    "See TST-EEG-004 T15",
    {"frames_recovered": count("Frames recovered after the 60 s disconnect."),
     "gap_frame_index_ranges": string_list("GAP frames and their index ranges, as "
                                           "`first-last` strings."),
     "backfill_rate_kb_s": num("Backfill rate.", "kB/s"),
     "declared_ring_depth_s": num("Ring depth in seconds as declared by the device in its "
                                  "STATUS frame.", "s"),
     "card_recovery_300s": enum(VERDICTS, "Whether the 300 s gap was recoverable in full "
                                          "from the card.", "DEFERRED")}),

"T16": step(
    "blocks",
    "Every block verifies; the chain is unbroken from the session identifier to the last "
    "block",
    "See TST-EEG-004 T16",
    {"blocks_verified": count("Blocks that verified."),
     "blocks_total": count("Blocks in the chain."),
     "session_identifier": text("Session identifier the chain starts from."),
     "key_fingerprint_used": text("Public-key fingerprint used to verify.", HEX16_PATTERN,
                                  "0" * 16)}),

"T17": step(
    "events, dB, dBu, %",
    "30 of 30 presses produce exactly one event; mute attenuation >= 60 dB; headphone level "
    "within 1 dB of target with THD <= 0.1 %; clamp register value equal to the T28 lot value",
    "See TST-EEG-004 T17",
    {"button_event_counts": nums(3, "One event count per button, 30 presses each.",
                                 "events"),
     "mute_attenuation_db": num("Microphone mute depth.", "dB"),
     "headphone_level_dbu": num("Headphone level into the 47.0 Ohm load.", "dBu"),
     "thd_percent": num("Total harmonic distortion.", "%"),
     "level_register_value": integer("Headphone level register value read back."),
     "clamp_register_value": integer("Acoustic clamp register value. It must equal the T28 "
                                     "lot value.")}),

"T18": step(
    "attribute, N.m, mm",
    "Complete; label content matches the record and the iSerial read in T5b, character for "
    "character",
    "Attribute",
    {"torque_values_nm": ({"type": "array", "items": {"type": "number"}, "minItems": 1,
                           "description": "Torque applied at each fastened site."},
                          [NUM_PLACEHOLDER]),
     "measured_stack_height_mm": num("Measured stack height.", "mm"),
     "label_photograph_ref": text("Reference to the applied-label photograph."),
     "label_matches_record_and_iserial": boolean("Data Matrix scanned at T18 and compared "
                                                 "field by field with the provisioning "
                                                 "record and the T5b iSerial. A mismatch "
                                                 "quarantines both the unit and the label."),
     "packing_list_signed": boolean("KPL-EEG-001 ticked line by line and signed by two "
                                    "people (PKG-EEG-015 section 1)."),
     "case_part_number": text("Travel-case part number as packed."),
     "foam_part_numbers": string_list("The CASE-00 layer part numbers as packed.",
                                      min_items=1)}),

"T19": step(
    "mOhm, MOhm",
    "Fitted: <= 50 mOhm across R90 and across R91. Lifted, modules disconnected: >= 10 MOhm",
    "See TST-EEG-004 T19",
    {"r90_mohm": num("Four-wire resistance across R90.", "mOhm"),
     "r91_mohm": num("Four-wire resistance across R91.", "mOhm"),
     "lifted_Mohm": nullable(num("The lifted value where it was taken.", "MOhm"),
                             "The lifted value in MOhm where taken, or null. The 100 % "
                             "evidence for the lifted case is the T0 bare-board isolation "
                             "measurement, which gives the same information without rework "
                             "on a 0603 pad."),
     "lifted_reason": nullable(text("Why the lifted measurement was taken."),
                               "The reason the lifted measurement was taken, or null.")}),

"T20": step(
    "GOhm, V, %",
    ">= 1 GOhm. Where the module carries a cross-barrier Y-capacitor the limit is the value "
    "recorded for that module type at T00",
    "See TST-EEG-004 T20",
    {"applied_voltage_v": num("Applied voltage. 500 V DC across the barrier.", "V"),
     "measured_resistance_Gohm": num("Measured insulation resistance.", "GOhm"),
     "dwell_s": num("Dwell time.", "s"),
     "relative_humidity_percent": num("Relative humidity at the measurement.", "%"),
     "module_type": text("Isolator module type."),
     "module_lot": text("Isolator module lot.")}),

"T21": step(
    "V, mA, attribute",
    "Junction voltage 2.85 to 3.15 V; session start refused with the defined ACK code; "
    "CHG_CE asserted throughout; state clears within one STATUS frame",
    "See TST-EEG-004 T21",
    {"junction_voltage_v": num("VBUS_DET junction voltage.", "V"),
     "ack_code": text("The ACK code returned when session start is refused."),
     "chg_ce_asserted_throughout": boolean("CHG_CE held the charger disabled for the whole "
                                           "of the session."),
     "charge_current_ma": num("Charge current during the interlock test.", "mA"),
     "cleardown_latency_frames": count("STATUS frames taken for the state to clear. The "
                                       "limit is one.")}),

"T22": step(
    "dB",
    "E-10 has two states and the record must say which one was applied: +/- 0.5 dB with the "
    "47 kOhm fitted, widening to +/- 1.0 dB only if ECO-EEG-024 raises R1 to R16 to 68 kOhm",
    "See TST-EEG-004 T22",
    {"eeg_response_db": nums(48, "Eight EEG channels at six frequencies, channel-major.",
                             "dB"),
     "emg_response_db": nums(9, "Three EMG channels at three frequencies, channel-major.",
                             "dB"),
     "fitted_series_resistor_kohm": num("The fitted R1 to R16 value.", "kOhm"),
     "band_applied": enum(["+/- 0.5 dB at 47 kOhm", "+/- 1.0 dB at 68 kOhm"],
                          "Which of E-10's two states was applied. The record must say."),
     "deviation_at_100hz_db": num("The deviation at 100 Hz, called out separately. "
                                  "Calculated expectation -0.36 dB at 47 kOhm.", "dB")}),

"T23": step(
    "uA",
    "Normal condition <= 10 uA DC and <= 100 uA AC; single fault <= 50 uA DC",
    "1 nA reads as 100 uV across the measuring resistor: four decades below the limit",
    {"dc_normal_host_connected_ua": nums(14, "Fourteen terminations, DC, normal condition, "
                                             "host connected.", "uA"),
     "ac_normal_host_connected_ua": nums(14, "Fourteen terminations, AC, normal condition, "
                                             "host connected.", "uA"),
     "dc_normal_host_disconnected_ua": nums(14, "Fourteen terminations, DC, normal "
                                                "condition, host disconnected.", "uA"),
     "ac_normal_host_disconnected_ua": nums(14, "Fourteen terminations, AC, normal "
                                                "condition, host disconnected.", "uA"),
     "dc_single_fault_ua": nums(14, "Fourteen terminations, DC, single fault. 14 + 14 + 14 "
                                    "+ 14 + 14 = 70 values.", "uA")}),

"T24": step(
    "dBm, attribute",
    "No carrier above the receiver noise floor; no SSID; no advertisement",
    "See TST-EEG-004 T24",
    {"radio_silent": boolean("No carrier, no SSID, no BLE advertisement."),
     "receiver_noise_floor_dbm": num("Receiver noise floor.", "dBm"),
     "firmware_image_sha256": sha256("SHA-256 of the firmware image under test.")}),

"T25": step(
    "attribute",
    "Secure boot enabled, flash encryption enabled, device rejects an unsigned image, "
    "rollback completes without operator action",
    "Attribute",
    {"efuse_readback": text("eFuse readback."),
     "rollback_result": enum(VERDICTS, "Forced-rollback result.", "DEFERRED"),
     "image_sha256_partition_a": sha256("SHA-256 of the image in partition A."),
     "image_sha256_partition_b": sha256("SHA-256 of the image in partition B."),
     "phase1_not_applicable_reason": nullable(
         text("Why the step is NOT_APPLICABLE."),
         "T25 is Phase 2 onward. On a Phase 1 unit the verdict is NOT_APPLICABLE and this "
         "field carries the reason; on a Phase 2 unit it is null.")}),

"T26": step(
    "ms",
    "Re-enumeration within 2 s each time; the sample counter and the ring buffer are not "
    "reset",
    "See TST-EEG-004 T26",
    {"latencies_ms": nums(3, "Three re-enumeration latencies.", "ms"),
     "sample_counter_continuous": boolean("The sample counter and the ring buffer were not "
                                          "reset.")}),

"T27": step(
    "Hz, ms",
    "Clock 2.048 MHz +/- 100 ppm from one source; SCLK >= 4 MHz; DRDY period 4.000, 2.000 "
    "and 1.000 ms within 100 ppm; status words advance together over 60 s with zero "
    "divergence; daisy order as documented in the firmware",
    "See TST-EEG-004 T27",
    {"clock_hz": num("Converter clock frequency.", "Hz"),
     "sclk_hz": num("SCLK frequency.", "Hz"),
     "drdy_periods_ms": nums(3, "DRDY periods at 250, 500 and 1000 Hz.", "ms"),
     "header_rate_fields": string_list("Header rate fields as read.", min_items=1),
     "divergence_count": count("Status-word divergence count over 60 s. The limit is zero."),
     "daisy_order_as_found": text("Daisy order as found. A channel-9 gain reading 24 rather "
                                  "than 12 means it is reversed.")}),

"T28": step(
    "dB SPL",
    "<= 100 dB SPL at any commanded level. Calculated full-scale output is about 110 dB SPL, "
    "which is why the requirement and the clamp exist",
    "See TST-EEG-004 T28",
    {"lot_record_reference": text("Reference to the T28 lot record. T28 is a TYPE TEST, "
                                  "once per lot, and the per-unit record carries the "
                                  "reference and the two values it holds, not a re-run."),
     "spl_db": nums(2, "The two dB SPL values the lot record carries.", "dB SPL"),
     "headphone_model": text("Headphone model."),
     "headphone_impedance_ohm": num("Headphone impedance. The shipped model is 47 Ohm.",
                                    "Ohm"),
     "clamp_register_value": integer("Clamp register value for the lot."),
     "coupler_asset_number": text("Artificial-ear coupler asset number."),
     "slm_asset_number": text("Sound level meter asset number.")}),

"T29": step(
    "attribute",
    "All present and matching. Applying the mark is not optional even where a single-kit "
    "parcel would fall under the small-consignment exemption",
    "Attribute",
    {"cell_lot": text("Cell lot."),
     "un383_report_reference": text("UN 38.3 test summary reference for the cell lot."),
     "msds_reference": text("Cell safety data sheet reference."),
     "mark_applied": boolean("ART-LBL-06 lithium battery mark applied to the outer carton."),
     "mark_photograph_ref": text("Photograph of the applied mark."),
     "document_set_reference": text("Reference to the shipment document set held per "
                                    "REG-EEG-012 Rev B section 3.7.")}),

"T30": step(
    "ms, counts, attribute",
    "Every S-check and every D-check passes at T30b, with D3's warning allowed at T30a only. "
    "Every frame-integrity counter reads zero. Median round-trip latency <= 50 ms",
    "Not a measurement. TOOL-EEG-022 section 1.3: a pass says the link works and says "
    "nothing about signal quality, electrode contact or noise",
    {"a_self_checks": verdicts_n(5, "T30a: S1 to S5, run before the unit is connected. A "
                                    "self-check failure condemns the browser or the file "
                                    "and says nothing about the unit."),
     "a_device_checks": verdicts_n(8, "T30a: D1 to D8, run after T5a and before T6. D3 is "
                                      "expected to warn because the unit is not yet "
                                      "provisioned."),
     "b_self_checks": verdicts_n(5, "T30b: S1 to S5."),
     "b_device_checks": verdicts_n(8, "T30b: D1 to D8, run after T6 alongside T5b. D3 must "
                                      "pass and the serial the tool reads must equal the "
                                      "unit serial character for character."),
     "identity": obj(
         {"protocol_version": text("Protocol version from CMD_IDENTIFY."),
          "firmware_major": integer("Firmware major version."),
          "firmware_minor": integer("Firmware minor version."),
          "board_revision_letter": text("Board revision letter.", r"^[A-Z]$", "B"),
          "ring_bytes": count("Ring buffer size in bytes."),
          "capability_flags": text("Capability flags as returned."),
          "rate_code": integer("Rate code as returned.")},
         "The CMD_IDENTIFY identity block."),
     "bytes_in": count("Total bytes in."),
     "frames_decoded": count("Total frames decoded."),
     "frame_integrity_counters": obj(
         {"crc_errors": count("CRC errors."),
          "version_errors": count("Version errors."),
          "short_frames": count("Short frames."),
          "resyncs": count("Resyncs."),
          "oversize_discards": count("Oversize discards."),
          "sequence_gaps": count("Sequence gaps."),
          "frames_missing": count("Frames missing.")},
         "All seven frame-integrity error counters. Every one of them must read zero."),
     "latency_median_ms": num("Median round-trip latency over twenty measurements. "
                              "TOOL-EEG-022's warning threshold is 50 ms.", "ms"),
     "latency_p95_ms": num("95th-percentile round-trip latency.", "ms"),
     "report_reference_a": text("Saved TOOL-EEG-022 report from the T30a run."),
     "report_reference_b": text("Saved TOOL-EEG-022 report from the T30b run."),
     "browser_name_and_version": text("Browser name and version the tool was run in.")}),
}


# ---------------------------------------------------------------------------------------
# 3.  Constants, disposition and signatures.
# ---------------------------------------------------------------------------------------

CONSTANTS = {
    "channel_gain_ppm": ({"type": "array", "items": {"type": "integer"}, "minItems": 16,
                          "maxItems": 16,
                          "description": "Sixteen channel gains as int32 ppm correction."},
                         [INT_PLACEHOLDER] * 16),
    "envelope_scaling_uv_per_full_scale": (
        {"type": "array", "items": {"type": "integer"}, "minItems": 3, "maxItems": 3,
         "description": "Three envelope scalings as int32 uV per full scale."},
        [INT_PLACEHOLDER] * 3),
    "envelope_group_delay_samples": nums(
        3, "Three envelope group delays in samples, to two decimals."),
    "lead_off_offset_ohm": nums(8, "Eight lead-off offsets.", "Ohm"),
    "lead_off_slope": nums(8, "Eight lead-off slopes."),
    "headphone_level_tenths_db": ({"type": "integer",
                                   "description": "Headphone level as int16 tenths of a dB."},
                                  INT_PLACEHOLDER),
    "acoustic_clamp_register_value": integer("The acoustic clamp register value."),
    "config_zone_lock_confirmed": boolean("Config-zone lock confirmed by readback at T6."),
}

DISPOSITION = {
    "failure_codes": string_list("Failure codes raised against this unit."),
    "rework": obj_array(
        {"site": text("Rework site, by reference designator."),
         "cycles": count("Hand-rework cycles at this site. Maximum two.")},
        "Rework sites and cycle counts.", min_items=0, n_example=0),
    "module_replacements": obj_array(
        {"module": text("Module replaced."),
         "recharacterisation_steps_rerun": string_list("The steps re-run after the "
                                                       "replacement.", min_items=1)},
        "Module replacements with the re-characterisation steps that were re-run.",
        min_items=0, n_example=0),
    "ncr_references": string_list("NCR references raised under QP-EEG-010."),
    "mrb_decision": nullable(text("The MRB decision where one was taken."),
                             "The MRB decision where taken, or null."),
}

SIGNATURES = {
    "operator": text("Operator signature or identifier."),
    "manufacturer_qa": text("Manufacturer QA signature or identifier."),
    "record_sha256": sha256(
        "SHA-256 of this record, printed on the calibration certificate (TST-EEG-004 "
        "section 13 item 8). It is computed over the record serialised as UTF-8 JSON with "
        "sorted keys, two-space indent and a trailing newline, with THIS FIELD SET TO "
        "SIXTY-FOUR ZEROS -- otherwise the hash would have to contain itself. "
        "records/validate_test_record.py computes and checks it."),
}


# ---------------------------------------------------------------------------------------
# 4.  Assembly
# ---------------------------------------------------------------------------------------

def document_step_list():
    """The step ids of TST-EEG-004 Rev C section 2, read out of the document."""
    md = open(TST, encoding="utf8").read()
    sec = md.split("## 2. The definitive step list", 1)
    if len(sec) != 2:
        raise SystemExit("TST-EEG-004 section 2 not found")
    body = sec[1].split("\n## ", 1)[0]
    ids = []
    for line in body.splitlines():
        m = re.match(r"\|\s*(T\d+)\s*\|", line.strip())
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


def build_schema():
    ids = document_step_list()
    if ids != list(STEPS.keys()):
        raise SystemExit(
            "The step list in TST-EEG-004 section 2 and the table in this script "
            f"disagree.\n  document: {ids}\n  this file: {list(STEPS.keys())}\n"
            "Add the missing step to STEPS, or correct the document. This check exists "
            "because T30 was added to the document after the record template was written.")

    step_props, step_example = {}, {}
    for sid, spec in STEPS.items():
        data_schema, data_example = spec["data"]
        fields = {
            "step": ({"const": sid, "description": "The step this object records."}, sid),
            "unit": ({"const": spec["unit"],
                      "description": "Unit of the values, from the step's table in "
                                     "TST-EEG-004 section 8."}, spec["unit"]),
            "limit": ({"const": spec["limit"],
                       "description": "The limit the values are judged against, verbatim "
                                      "from TST-EEG-004 section 8."}, spec["limit"]),
            "uncertainty": ({"const": spec["uncertainty"],
                             "description": "The expanded uncertainty at k = 2 unless the "
                                            "step says otherwise."}, spec["uncertainty"]),
            "verdict": enum(VERDICTS, "Verdict for this step.", "DEFERRED"),
            "attempt": ({"type": "integer", "minimum": 1, "maximum": 3,
                         "description": "1, 2 or 3. A unit may be re-tested at most twice "
                                        "on the same step; the second failure is an NCR."},
                        1),
        }
        s, ex = obj(fields, f"Step {sid}.")
        s["properties"]["data"] = data_schema
        s["required"].append("data")
        ex["data"] = data_example
        # Every attempt is retained; nothing is overwritten.
        s["properties"]["previous_attempts"] = {
            "type": "array", "items": {"type": "object"},
            "description": "Earlier attempts at this step, in order, each a complete step "
                           "object. Section 12: every attempt is retained; nothing is "
                           "overwritten."}
        s["properties"]["deferral_reason"] = {
            "type": "string", "minLength": 1,
            "description": "Why the step was not performed. Mandatory whenever the verdict "
                           "is DEFERRED or NOT_APPLICABLE; the validator enforces it."}
        step_props[sid] = s
        ex["deferral_reason"] = ("EXAMPLE-PLACEHOLDER. This is an example record, not a "
                                 "test result; no step was performed.")
        step_example[sid] = ex

    ident_schema, ident_example = obj(IDENTITY, "TST-EEG-004 section 12, Identity.")
    const_schema, const_example = obj(
        CONSTANTS, "TST-EEG-004 section 12, Constants written to the device, byte-exact and "
                   "mirroring the NVS content.")
    disp_schema, disp_example = obj(DISPOSITION, "TST-EEG-004 section 12, Disposition.")
    sig_schema, sig_example = obj(SIGNATURES, "TST-EEG-004 section 12, Signatures.")

    refurb_schema, refurb_example = obj_array(
        {"date": text("Date of the refurbishment re-test.", r"^\d{4}-\d{2}-\d{2}$",
                      "1970-01-01"),
         "receipt_record_reference": text("The PKG-EEG-015 section 8 receipt record this "
                                          "block follows."),
         "results": ({"type": "object",
                      "properties": {k: step_props[k] for k in
                                     ("T7", "T8", "T10", "T13", "T17")},
                      "required": ["T7", "T8", "T10", "T13", "T17"],
                      "additionalProperties": False,
                      "description": "T7, T8, T10, T13 and T17 re-run and appended. This is "
                                     "what keeps instrument drift out of the "
                                     "between-participant comparisons."},
                     {k: step_example[k] for k in ("T7", "T8", "T10", "T13", "T17")})},
        "Refurbishment blocks, appended under the same unit serial when a kit returns from "
        "a participant.", min_items=0, n_example=0)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "EEG field kit per-unit test record",
        "description": (
            "The machine-readable per-unit record of TST-EEG-004 Rev C section 12, one file "
            "per unit named `<unit_serial>_test.json`. Section 12 fixes the field counts "
            "'so a record can be validated mechanically'; every count it states is a "
            "minItems == maxItems pair in this schema, so a short array is a schema error "
            "and not a silent gap. Generated by records/make_records.py from "
            "TST-EEG-004 Rev C. Licence: " + LICENCE + "."),
        "type": "object",
        "additionalProperties": False,
        "required": ["schema", "record_type", "identity", "results", "constants",
                     "disposition", "signatures"],
        "properties": {
            "schema": ({"const": SCHEMA_ID,
                        "description": "The schema this record claims to satisfy."}),
            "record_type": {
                "enum": ["production", "example"],
                "description": "`production` for a record of a unit that was tested; "
                               "`example` for the worked example shipped with the schema. "
                               "The validator refuses to accept an `example` record as a "
                               "deliverable under RFQ-EEG-001 section 9.3."},
            "identity": ident_schema,
            "results": {
                "type": "object",
                "description": "One object per step. There are thirty-two steps: T00, T0 "
                               "and T1 to T30 (TST-EEG-004 section 2). All thirty-two are "
                               "mandatory; a step that was not performed carries the "
                               "verdict DEFERRED or NOT_APPLICABLE and a deferral_reason.",
                "properties": step_props,
                "required": list(step_props.keys()),
                "additionalProperties": False},
            "constants": const_schema,
            "disposition": disp_schema,
            "signatures": sig_schema,
            "refurbishment": refurb_schema,
        },
    }
    example = {
        "schema": SCHEMA_ID,
        "record_type": "example",
        "identity": ident_example,
        "results": step_example,
        "constants": const_example,
        "disposition": disp_example,
        "signatures": sig_example,
        "refurbishment": refurb_example,
    }
    return schema, example


def canonical_bytes(record):
    """The byte string signatures.record_sha256 is taken over.

    The field cannot contain its own hash, so the hash is computed with the field set to
    sixty-four zeros. Sorted keys and a fixed indent make the serialisation reproducible on
    any implementation.
    """
    import copy
    r = copy.deepcopy(record)
    r.setdefault("signatures", {})["record_sha256"] = ZERO_HASH
    return (json.dumps(r, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf8")


def lot_summary_columns():
    return (["kit_id", "unit_serial", "hw_rev", "build_lot", "manufacturer", "date_time",
             "operator_id", "qa_id", "atecc_factory_serial", "key_fingerprint",
             "firmware_version", "firmware_sha256", "overall_verdict"]
            + [f"verdict_{sid}" for sid in STEPS]
            + ["failure_codes", "ncr_references", "record_filename", "record_sha256",
               "certificate_filename"])


CERT_TEMPLATE = """\
# CALIBRATION AND TEST CERTIFICATE

**Template for:** TST-EEG-004 Rev C section 13   **Licence:** {licence}
**Generated by:** `records/make_records.py`   **Source record:** `<unit_serial>_test.json`

This is a TEMPLATE. Every `{{{{...}}}}` is filled from the per-unit record and from nowhere
else; the field paths beside them are JSON pointers into that record, so the certificate and
the record cannot disagree. One printed A4 page per unit. It travels in the case lid wallet
beside the quick-start card (PKG-EEG-015 Rev B section 1.1 line 6.5).

---

## 1. Identification

| | |
|---|---|
| Unit serial | `{{{{identity.unit_serial}}}}` |
| Hardware revision | `{{{{identity.hw_rev}}}}` |
| Date of test | `{{{{identity.date_time}}}}` |
| | **RESEARCH INSTRUMENT -- NOT A MEDICAL DEVICE** |

## 2. Identity block

| | |
|---|---|
| ATECC608B factory serial | `{{{{identity.atecc_factory_serial}}}}` |
| Public-key fingerprint | `{{{{identity.key_fingerprint}}}}` -- computed as FW-EEG-001 Rev C section 7 defines it, and identical to the string printed on the label |
| Firmware version | `{{{{identity.firmware_version}}}}` |
| Firmware SHA-256 | `{{{{identity.firmware_sha256}}}}` |

## 3. Environment

| | |
|---|---|
| Ambient temperature | `{{{{identity.ambient_temperature_c}}}}` degC |
| Relative humidity | `{{{{identity.relative_humidity_percent}}}}` % |
| | The unit was on battery, USB disconnected, for the characterisation steps (T8, T9b). |

## 4. Constants written to the device

Each with its unit and its uncertainty, from the step that measured it.

| Constant | Count | Value | Unit | From | Uncertainty |
|---|---|---|---|---|---|
| Channel gains | 16 | `{{{{constants.channel_gain_ppm}}}}` | ppm | T7 | `{{{{results.T7.uncertainty}}}}` |
| Envelope scalings | 3 | `{{{{constants.envelope_scaling_uv_per_full_scale}}}}` | uV per full scale | T12a | `{{{{results.T12.uncertainty}}}}` |
| Envelope group delays | 3 | `{{{{constants.envelope_group_delay_samples}}}}` | samples | T12b | `{{{{results.T12.uncertainty}}}}` |
| Lead-off offsets | 8 | `{{{{constants.lead_off_offset_ohm}}}}` | Ohm | T10 | `{{{{results.T10.uncertainty}}}}` |
| Lead-off slopes | 8 | `{{{{constants.lead_off_slope}}}}` | -- | T10 | `{{{{results.T10.uncertainty}}}}` |
| Headphone level | 1 | `{{{{constants.headphone_level_tenths_db}}}}` | tenths of a dB | T17 | `{{{{results.T17.uncertainty}}}}` |
| Acoustic clamp register | 1 | `{{{{constants.acoustic_clamp_register_value}}}}` | -- | T28 (lot) | `{{{{results.T28.uncertainty}}}}` |

## 5. Verification

{verification}

## 6. Traceability

Every instrument by asset number with its calibration due date, from
`identity.instruments`, and the fixture serial `{{{{identity.fixture_serial}}}}`
(JIG-EEG-009 unit number).

| Asset number | Instrument | Calibration due |
|---|---|---|
| `{{{{identity.instruments[n].asset_number}}}}` | `{{{{identity.instruments[n].description}}}}` | `{{{{identity.instruments[n].calibration_due}}}}` |

## 7. Statement of limitations

Printed in full, not summarised. TST-EEG-004 Rev C section 13 item 7 requires all of it.

- This certificate is **not** a medical-device conformity statement.
- T23 is a stand-in for the IEC 60601-1 patient auxiliary current measurement, and
  **S-02 is not met at the fitted resistor value**.
- The 2.5 kV isolation figure is a component supplier's certificate and was **not verified
  on this unit**.
- The 45 degC charge inhibit is **not implemented**: there is no NTC net and no thermistor
  way, so S-04's thermistor-monitored charging is not met.
- **No safety engineer has reviewed this design as of the date of issue.**

## 8. Signatures

| | |
|---|---|
| Operator | `{{{{signatures.operator}}}}` |
| Manufacturer QA | `{{{{signatures.manufacturer_qa}}}}` |
| SHA-256 of the source record | `{{{{signatures.record_sha256}}}}` |

The programme counter-signs at goods-in in Brussels after its own subset re-test, and that
counter-signature is the acceptance under RFQ-EEG-001 Rev E section 9.3.
"""

# TST-EEG-004 section 13 item 5 names the verification table's rows.
CERT_VERIFICATION_STEPS = ["T3", "T7", "T8", "T9", "T10", "T12", "T13", "T14", "T17",
                           "T20", "T21", "T22", "T23"]


def certificate_template():
    rows = ["| Step | What it verifies | Measured | Limit | Verdict |",
            "|---|---|---|---|---|"]
    names = step_names()
    for sid in CERT_VERIFICATION_STEPS:
        rows.append(f"| {sid} | {names.get(sid, '')} | `{{{{results.{sid}.data}}}}` | "
                    f"{STEPS[sid]['limit']} | `{{{{results.{sid}.verdict}}}}` |")
    note = ("\nSection 13 item 5 names T7a matching, T9a, T9b and T12b explicitly; T7, T9 "
            "and T12 are one step each in the section 2 list, so their sub-step values sit "
            "inside the one object named above. The limits are quoted from the record "
            "rather than retyped, because the record carries them verbatim from section 8.")
    return "\n".join(rows) + "\n" + note


def step_names():
    md = open(TST, encoding="utf8").read()
    body = md.split("## 2. The definitive step list", 1)[1].split("\n## ", 1)[0]
    out = {}
    for line in body.splitlines():
        m = re.match(r"\|\s*(T\d+)\s*\|\s*([^|]+?)\s*\|", line.strip())
        if m:
            out[m.group(1)] = m.group(2)
    return out


README = """\
records/ -- the machine-readable per-unit test record
=====================================================================

Owned by:   TST-EEG-004 Rev C section 12 (the record) and section 13 (the certificate)
Generated:  records/make_records.py
Licence:    {licence}

TST-EEG-004 section 12 specifies one JSON file per unit, `<unit_serial>_test.json`, and says
the field counts are "fixed so a record can be validated mechanically". Until this directory
existed there was nothing to validate against, so nothing caught a missing mandatory field,
and two manufacturers reading the same prose would have emitted different key names and
different nesting for the same 70 T23 currents, 32 T10 impedances and 24 T7a gains. Neither
file could have been ingested without hand-mapping, which is the comparability failure the
document's own opening calls fatal for the study.

FILES
---------------------------------------------------------------------
  TST-EEG-004_RevC_unit_test_record.schema.json
      JSON Schema 2020-12. Every field count section 12 states is a minItems == maxItems
      pair, so a short array is a schema error and not a silent gap. `unit`, `limit` and
      `uncertainty` are `const` strings taken verbatim from each step's table in section 8,
      so a record cannot claim a limit the specification does not set.

  EXAMPLE_TIOV-B-0000_test.json
      A worked record that validates and CONTAINS NO MEASUREMENTS. Every number is the
      sentinel -9999 or 9999, every hash is sixty-four zeros, every free-text field begins
      EXAMPLE-, every step verdict is DEFERRED with a reason, `record_type` is `example`,
      and the serial TIOV-B-0000 is in none of the blocks PKG-EEG-015 section 5 allocates.
      It is a shape, not a result.

  lot_summary_template.csv
      The header row of the per-lot summary CSV that section 12 puts in the per-lot ZIP.
      The step columns are generated from the section 2 step list, so a new step appears
      here on the next run.

  TST-EEG-004_RevC_calibration_certificate.md
      The section 13 certificate template. Every placeholder is a JSON pointer into the
      record, so the certificate and the record cannot disagree.

  validate_test_record.py
      Validates a record against the schema, then applies the checks a schema cannot
      express: that a DEFERRED or NOT_APPLICABLE step carries a reason, that the T5b
      iSerial and the T6 fingerprint match the identity block, that the seven T30 frame
      integrity counters are zero when T30 passes, and that signatures.record_sha256 is
      the hash of the record. Run it with --production to reject an example record.

  make_records.py
      Writes all of the above from one specification table. It reads the step list out of
      TST-EEG-004 section 2 and REFUSES TO RUN if the document and the table disagree.
      That check is not decoration: T30 was added to the document after the record template
      was drafted, and this is the mechanism that would have caught it.

HOW TO USE
---------------------------------------------------------------------
  python3 records/validate_test_record.py records/EXAMPLE_TIOV-B-0000_test.json
  python3 records/validate_test_record.py --production TIOV-B-0001_test.json
  python3 records/make_records.py            regenerate everything

WHAT IS NOT SETTLED
---------------------------------------------------------------------
  * The record's SHA-256 is defined here, because section 12 requires the hash on the
    certificate without saying what it is taken over. It is the record serialised as UTF-8
    JSON with sorted keys, a two-space indent and a trailing newline, with
    signatures.record_sha256 itself set to sixty-four zeros. That definition is this
    directory's PROPOSAL. It is arbitrary in the way any canonicalisation is arbitrary, and
    it needs the programme's ruling before a manufacturer signs against it.
  * The eleven steps that need a host stream decoder (T7, T8, T9, T10, T12, T13, T14, T15,
    T16, T26, T27) cannot be filled today: TST-EEG-004 section 16 item 10 records that the
    decoding tool does not exist. Their `identity.stream_decoder` is null and their verdicts
    are DEFERRED with that reason. The schema does not pretend otherwise.
  * Nothing here has been run against a real record, because no unit has been built.
"""


def main():
    schema, example = build_schema()

    p_schema = os.path.join(HERE, "TST-EEG-004_RevC_unit_test_record.schema.json")
    with open(p_schema, "w", encoding="utf8") as fh:
        json.dump(schema, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    import hashlib
    example["signatures"]["record_sha256"] = hashlib.sha256(
        canonical_bytes(example)).hexdigest()
    p_example = os.path.join(HERE, f"EXAMPLE_{EXAMPLE_SERIAL}_test.json")
    with open(p_example, "w", encoding="utf8") as fh:
        json.dump(example, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    p_csv = os.path.join(HERE, "lot_summary_template.csv")
    with open(p_csv, "w", encoding="utf8", newline="") as fh:
        csv.writer(fh).writerow(lot_summary_columns())

    p_cert = os.path.join(HERE, "TST-EEG-004_RevC_calibration_certificate.md")
    with open(p_cert, "w", encoding="utf8") as fh:
        fh.write(CERT_TEMPLATE.format(licence=LICENCE,
                                      verification=certificate_template()))

    p_readme = os.path.join(HERE, "README.txt")
    with open(p_readme, "w", encoding="utf8") as fh:
        fh.write(README.format(licence=LICENCE))

    for p in (p_schema, p_example, p_csv, p_cert, p_readme):
        print(f"  wrote {os.path.relpath(p, PKG)}  {os.path.getsize(p):,} bytes")
    print(f"  {len(STEPS)} steps, checked against TST-EEG-004 section 2")
    print(f"  {len(lot_summary_columns())} lot-summary columns")
    return 0


if __name__ == "__main__":
    sys.exit(main())
