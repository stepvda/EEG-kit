#!/usr/bin/env python3
"""
provision_selftest.py -- station rehearsal for provision.py, with no unit and no hardware.

WHAT THIS IS FOR
  FW-EEG-001 section 7.2 makes `--dry-run` the way an operator is trained and a station is
  validated "before a board exists".  `--dry-run` proves the script starts and prints its
  sequence; it does not prove the sequence is right, because it touches nothing.  This does:
  it drives the real `provision()` against a simulated device that answers the way the shipped
  firmware answers, and asserts what came out.

      python3 provision_selftest.py            (exit 0 = the station is behaving)

  It checks the four things a station most needs to be true before a real part is in front of
  it, all of which were broken or absent in the shipped script:

      1. a run completes and produces the identity block -- fingerprint, raw hex and PEM --
         and the three agree with each other
      2. the serial format gate rejects what PKG-EEG-015 section 5 does not allow
      3. with the configuration-zone template unwritten, a --lock run STOPS BEFORE the
         irreversible step instead of locking a default configuration and scrapping the part
      4. once the two proposed opcodes exist, the whole sequence runs and the calibration
         constants read back byte-identical, which is TST-EEG-004 T6's acceptance limit

  The simulated device is not a model of the ATECC608B and proves nothing about the silicon.
  It answers the protocol, so what is tested here is this station's logic and nothing else.
  T6 on a real part is still the step that proves the rest.

  `cryptography` is used only to cross-check the PEM if it is installed; the check is skipped,
  and said to be skipped, if it is not.

Licence: MIT, matching firmware/tools/provision.py and the rest of the firmware source.
"""
from __future__ import annotations
import binascii
import hashlib
import json
import os
import struct
import pathlib
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import provision                                            # noqa: E402

# The 64 bytes the simulated device returns as its public key.  Where `cryptography` is
# installed this is a real, freshly generated point on P-256, so the PEM can be parsed back and
# compared; where it is not, it is 64 synthetic bytes, which still exercise the fingerprint and
# the PEM structure but are not on the curve and cannot be parsed.  Either way no private half
# exists anywhere and nothing here signs.
def _public_point():
    try:
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import serialization
        k = ec.generate_private_key(ec.SECP256R1()).public_key()
        return k.public_bytes(serialization.Encoding.X962,
                              serialization.PublicFormat.UncompressedPoint)[1:], True
    except ImportError:
        return bytes((i * 7 + 3) & 0xFF for i in range(64)), False


FAKE_PUB, FAKE_PUB_IS_ON_CURVE = _public_point()
FAKE_ATECC_SERIAL = b"0123456789ABCDEF01"


class SimulatedDevice:
    """Answers the provisioning opcode family the way firmware/main/main.c does.

    `implement_proposed` switches between the firmware as shipped -- which has no 0x4A and no
    0x4B and answers status 0x01 for both -- and the firmware as ATECC608B_CONFIG_TEMPLATE.md
    section 4 proposes it."""

    def __init__(self, implement_proposed=False):
        self.implement_proposed = implement_proposed
        self.opcodes = []
        self.locked = False
        self.calibration = b""

    def command(self, cmd, payload=b"", deadline=provision.ACK_TIMEOUT_S):
        provision.check_command_fits(cmd, payload)
        self.opcodes.append(cmd)
        if cmd == provision.CMD_ENTER_PROVISIONING:
            if self.locked:
                raise provision.CommandRefused(cmd, 0x02)   # main.c: already provisioned
            return b""
        if cmd == provision.CMD_ATECC_READ_SERIAL:
            return FAKE_ATECC_SERIAL
        if cmd in (provision.CMD_ATECC_GENKEY, provision.CMD_ATECC_READ_PUBKEY):
            return FAKE_PUB
        if cmd == provision.CMD_ATECC_LOCK_CONFIG:
            self.locked = True
            return b""
        if cmd == provision.CMD_READ_PROVISION_STATE:
            return bytes([1 if self.locked else 0, 1])
        if cmd == provision.CMD_WRITE_CALIBRATION:
            self.calibration = payload
            return b""
        if cmd in (provision.CMD_ATECC_WRITE_CONFIG, provision.CMD_READ_CALIBRATION):
            if not self.implement_proposed:
                raise provision.CommandRefused(cmd, provision.ACK_UNKNOWN_OPCODE)
            if cmd == provision.CMD_READ_CALIBRATION:
                off, n = struct.unpack("<HB", payload)
                return self.calibration[off:off + n]
            return b""
        return b""                                          # 0x44, 0x45, 0x49, 0x4F

    def close(self):
        pass


def run(tmp, name, simulated, serial="TIOV-B-0007", calibration=None, **kw):
    provision.Device = lambda port: simulated
    out = os.path.join(tmp, f"{name}.json")
    rec = provision.provision("/dev/simulated", serial, calibration, out,
                              provision.DEFAULT_VID, provision.DEFAULT_PID, False, **kw)
    return rec, out


def main() -> int:
    failures = []

    def check(label, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'}  {label}{(' -- ' + detail) if detail else ''}")
        if not ok:
            failures.append(label)

    with tempfile.TemporaryDirectory() as tmp:
        print("1. a run completes and the identity block agrees with itself")
        sim = SimulatedDevice(implement_proposed=False)
        rec, _ = run(tmp, "identity", sim)
        expect_fp = hashlib.sha256(FAKE_PUB).hexdigest()[:16].upper()
        check("public_key_fingerprint is FW-EEG-001 section 7.4's definition",
              rec.get("public_key_fingerprint", "").replace(" ", "") == expect_fp,
              rec.get("public_key_fingerprint", "-"))
        check("the fingerprint is printed in four groups of four",
              [len(g) for g in rec.get("public_key_fingerprint", "").split()] == [4, 4, 4, 4])
        check("device_public_key is the 128-hex raw form FW-EEG-001 section 7.4 specifies",
              rec.get("device_public_key") == binascii.hexlify(FAKE_PUB).decode())
        pem = rec.get("device_public_key_pem", "")
        check("device_public_key_pem is the PEM TST-EEG-004 T6 and JIG-EEG-009 section 3.4 ask "
              "for",
              pem.startswith("-----BEGIN PUBLIC KEY-----")
              and pem.rstrip().endswith("-----END PUBLIC KEY-----"))
        if FAKE_PUB_IS_ON_CURVE:
            from cryptography.hazmat.primitives import serialization
            back = serialization.load_pem_public_key(pem.encode())
            raw = back.public_bytes(serialization.Encoding.X962,
                                    serialization.PublicFormat.UncompressedPoint)
            check("the PEM parses back to the same point", raw[1:] == FAKE_PUB)
        else:
            print("  SKIP  the PEM cross-check needs `cryptography`, which is not installed.")
            print("        Its structure is checked above; that it decodes to the same point "
                  "is not.")
        check("an unlocked unit is recorded as unlocked",
              rec.get("config_zone_locked") is False)

        print("2. the serial gate rejects what PKG-EEG-015 section 5 does not allow")
        for bad in ("NOT-A-SERIAL", "TIOV-B-0000", "TIOV-B-1000", "TIOV-EEG-0007",
                    "tiov-b-0007", "TIOV-B-007"):
            try:
                provision.check_serial(bad)
                check(f"rejects {bad}", False, "it was accepted")
            except SystemExit:
                check(f"rejects {bad}", True)
        check("accepts TIOV-B-0007 and names its phase block",
              provision.check_serial("TIOV-B-0007") == "Phase 1")
        check("accepts TIOV-B-0099 as Phase 2",
              provision.check_serial("TIOV-B-0099") == "Phase 2")

        print("3. --lock stops before the irreversible step when the template did not go in")
        sim = SimulatedDevice(implement_proposed=False)
        stopped = False
        try:
            run(tmp, "stop", sim, lock=True, confirm="TIOV-B-0007", write_config=True)
        except SystemExit:
            stopped = True
        check("the run stopped", stopped)
        check("no lock command was sent",
              provision.CMD_ATECC_LOCK_CONFIG not in sim.opcodes,
              " ".join(f"0x{c:02X}" for c in sim.opcodes))
        rec = json.load(open(os.path.join(tmp, "stop.json")))
        check("the record was written before the run ended, and says the zone was not written",
              rec.get("config_zone_written") is False)

        print("4. with the proposed opcodes present, the whole sequence runs")
        cal_path = os.path.join(tmp, "cal.json")
        # Deliberately minimal, so that it fits one command frame today; the schema override is
        # therefore exercised too.  A conforming file does not currently fit -- section 4 item 3
        # of README_provisioning.md is exactly that.
        json.dump({"schema": "EEG-CAL-1", "unit_serial": "TIOV-B-0007",
                   "measured_utc": "2026-09-02T00:00:00Z", "example_only": False},
                  open(cal_path, "w"))
        sim = SimulatedDevice(implement_proposed=True)
        rec, _ = run(tmp, "full", sim, calibration=cal_path, lock=True,
                     confirm="TIOV-B-0007", write_config=True, schema_override=True)
        check("the configuration zone was written from the template",
              rec.get("config_zone_written") is True)
        check("only the blocks the mask names were written",
              sim.opcodes.count(provision.CMD_ATECC_WRITE_CONFIG) == 2,
              f"{sim.opcodes.count(provision.CMD_ATECC_WRITE_CONFIG)} of 4 blocks")
        check("the lock came before GenKey, as the silicon needs",
              sim.opcodes.index(provision.CMD_ATECC_LOCK_CONFIG)
              < sim.opcodes.index(provision.CMD_ATECC_GENKEY))
        check("the lock was confirmed by a read-back",
              rec.get("config_zone_locked") is True)
        check("the constants read back byte-identical (TST-EEG-004 T6's limit)",
              rec.get("calibration_readback_verified") is True)
        check("the override was recorded rather than swallowed",
              rec.get("calibration_schema_override") is True)
        check("the template's sha256 is in the record, so a fleet can be told apart by it",
              len(rec.get("config_template_sha256", "")) == 64)

        print("5. the shipped example calibration file cannot be written into a unit")
        example = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "cal_TIOV-B-0000.example.json")
        refused = False
        try:
            provision.load_calibration(example, "TIOV-B-0000", False)
        except SystemExit:
            refused = True
        check("example_only stops the template being written as if it were a measurement",
              refused)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed:")
        for f in failures:
            print("  -", f)
        return 1
    print("station self-test passed.  This proves the script's logic, not the silicon:")
    print("TST-EEG-004 T6 on a real ATECC608B is still the step that proves the rest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


def test_opcodes_are_unique():
    """Every CMD_ constant in provision.py must name a different opcode, and each must
    agree with main.c.

    This check exists because its absence cost two bugs in one day.  0x4A was allocated to
    CMD_READ_CALIBRATION in the firmware and to CMD_ATECC_WRITE_CONFIG here; moving the
    host constant to 0x4B put it on top of a value THIS FILE was already using.  Nothing
    caught either, because no shipped test imported provision.py at all.
    """
    import re
    import provision as P

    cmds = {k: v for k, v in vars(P).items()
            if k.startswith("CMD_") and isinstance(v, int)}
    seen = {}
    for name, op in sorted(cmds.items()):
        if op in seen:
            raise AssertionError(
                f"opcode 0x{op:02X} is used by BOTH {seen[op]} and {name}")
        seen[op] = name

    # ...and against the firmware, which is the authority.
    fw = (pathlib.Path(__file__).resolve().parents[1] / "main" / "main.c").read_text()
    fw_ops = {m.group(1): int(m.group(2), 16)
              for m in re.finditer(r"(CMD_[A-Z0-9_]+)\s*=\s*(0x[0-9A-Fa-f]+)", fw)}
    for name, op in cmds.items():
        if name in fw_ops and fw_ops[name] != op:
            raise AssertionError(
                f"{name} is 0x{op:02X} here and 0x{fw_ops[name]:02X} in main.c")
    return f"{len(cmds)} opcodes, all unique and matching main.c"
