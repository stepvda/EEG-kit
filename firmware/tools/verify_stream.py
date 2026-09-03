#!/usr/bin/env python3
"""
verify_stream.py -- host-side decoder and verifier for the EEG field kit frame stream.

This is the tool the production test uses at steps T5, T13, T14 and T16, and the same tool
the programme uses to check a returned microSD card. It reads the frame stream from a
serial port or from a file, decodes it, and reports on the four things that can be wrong
without anyone noticing:

    * a corrupted frame               -- CRC-32 over the decoded body
    * a lost frame                    -- sequence number continuity, and GAP frames
    * a discontinuous timeline        -- first-sample-index continuity against the rate
    * an unverifiable block           -- ECDSA P-256 signature chain against the device
                                         public key exported at provisioning

    python3 verify_stream.py --file session.bin --pubkey records/TIOV-B-0007.json
    python3 verify_stream.py --port /dev/ttyACM0 --seconds 60 --pubkey ... --json out.json

Exit status is 0 only if every check passes, so it can be used as a test step directly.

Licence: MIT.
"""
from __future__ import annotations
import argparse
import binascii
import hashlib
import json
import struct
import sys
import time

FT = {1: "DATA", 2: "STATUS", 3: "EVENT", 4: "GAP", 5: "SIGNATURE", 6: "CMD_ACK"}
RATES = {0: 250, 1: 500, 2: 1000}
HDR = struct.Struct("<BBHIBB")          # version, type, seq, first_sample, rate, n_samples
SAMPLE_BYTES = 16 * 3 + 2               # 16 x int24 plus the 16-bit auxiliary field


def cobs_decode(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(data):
        code = data[i]
        if code == 0:
            break
        out += data[i + 1:i + code]
        if code < 0xFF and i + code < len(data) and data[i + code] != 0:
            out.append(0)
        i += code
    return bytes(out)


def frames(stream: bytes):
    """Yield decoded frame bodies. A decoder joining mid-stream resynchronises at the
    next 0x00 delimiter, which is exactly what the field format is for."""
    for chunk in stream.split(b"\x00"):
        if not chunk:
            continue
        body = cobs_decode(chunk + b"\x00")
        if len(body) >= HDR.size + 4:
            yield body


def int24(b):
    v = b[0] | (b[1] << 8) | (b[2] << 16)
    return v - (1 << 24) if v & 0x800000 else v


class Verifier:
    def __init__(self, pubkey_hex=None):
        self.pubkey_hex = pubkey_hex
        self.n = {k: 0 for k in FT.values()}
        self.n["BAD_CRC"] = 0
        self.n["UNKNOWN"] = 0
        self.errors = []
        self.seq = None
        self.next_sample = None
        self.rate = None
        self.blocks = 0
        self.blocks_verified = 0
        self.chain = b"\x00" * 32
        self.block_hash = hashlib.sha256()
        self.samples = 0
        self.gaps = []
        self.first_sample = None
        self.last_sample = None

    def feed(self, body: bytes):
        if binascii.crc32(body[:-4]) & 0xFFFFFFFF != struct.unpack("<I", body[-4:])[0]:
            self.n["BAD_CRC"] += 1
            self.errors.append("CRC-32 mismatch")
            return
        ver, typ, seq, first, rate, nsamp = HDR.unpack_from(body, 0)
        name = FT.get(typ, "UNKNOWN")
        self.n[name] = self.n.get(name, 0) + 1
        if self.seq is not None and seq != (self.seq + 1) & 0xFFFF:
            self.errors.append(f"sequence jump {self.seq} -> {seq}")
        self.seq = seq
        if name == "DATA":
            self.rate = RATES.get(rate, rate)
            if self.first_sample is None:
                self.first_sample = first
            if self.next_sample is not None and first != self.next_sample:
                self.errors.append(f"sample-index discontinuity: expected "
                                   f"{self.next_sample}, got {first}")
            self.next_sample = first + nsamp
            self.last_sample = first + nsamp
            self.samples += nsamp
            payload = body[HDR.size:HDR.size + nsamp * SAMPLE_BYTES]
            if len(payload) != nsamp * SAMPLE_BYTES:
                self.errors.append(f"frame {seq} is short: {len(payload)} bytes for "
                                   f"{nsamp} samples")
            self.block_hash.update(body[:-4])
        elif name == "GAP":
            lo, hi = struct.unpack_from("<II", body, HDR.size)
            self.gaps.append((lo, hi))
            self.next_sample = hi + 1
        elif name == "SIGNATURE":
            self.blocks += 1
            sig = body[HDR.size:HDR.size + 64]
            digest = hashlib.sha256(self.chain + self.block_hash.digest()).digest()
            self.chain = digest
            self.block_hash = hashlib.sha256()
            if self._verify(digest, sig):
                self.blocks_verified += 1

    def _verify(self, digest, sig):
        if not self.pubkey_hex:
            return False
        try:
            from cryptography.hazmat.primitives.asymmetric import ec, utils
            from cryptography.hazmat.primitives import hashes
            raw = binascii.unhexlify(self.pubkey_hex)
            if len(raw) == 64:
                raw = b"\x04" + raw
            key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), raw)
            r = int.from_bytes(sig[:32], "big")
            s = int.from_bytes(sig[32:64], "big")
            key.verify(utils.encode_dss_signature(r, s), digest,
                       ec.ECDSA(utils.Prehashed(hashes.SHA256())))
            return True
        except Exception as e:
            self.errors.append(f"block signature did not verify: {e}")
            return False

    def report(self):
        dur = self.samples / self.rate if self.rate else 0.0
        lost = sum(hi - lo + 1 for lo, hi in self.gaps)
        ok = (self.n["BAD_CRC"] == 0
              and not [e for e in self.errors if "discontinuity" in e or "sequence" in e]
              and (self.blocks == 0 or self.blocks_verified == self.blocks))
        return {
            "frames": {k: v for k, v in self.n.items() if v},
            "samples": self.samples,
            "sample_rate_hz": self.rate,
            "duration_s": round(dur, 3),
            "first_sample_index": self.first_sample,
            "last_sample_index": self.last_sample,
            "gap_frames": len(self.gaps),
            "samples_lost_to_gaps": lost,
            "signature_blocks": self.blocks,
            "signature_blocks_verified": self.blocks_verified,
            "errors": self.errors[:40],
            "error_count": len(self.errors),
            "pass": ok,
        }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", help="a captured stream, or the microSD copy")
    g.add_argument("--port", help="CDC-ACM port to read live")
    ap.add_argument("--seconds", type=float, default=30.0, help="how long to read a port")
    ap.add_argument("--pubkey", help="the provisioning record, or a raw hex public key")
    ap.add_argument("--json", help="write the report here")
    a = ap.parse_args()

    pub = None
    if a.pubkey:
        if a.pubkey.endswith(".json"):
            pub = json.load(open(a.pubkey)).get("device_public_key")
        else:
            pub = a.pubkey

    if a.file:
        data = open(a.file, "rb").read()
    else:
        import serial
        s = serial.Serial(a.port, 115200, timeout=0.2)
        buf = bytearray()
        t0 = time.time()
        while time.time() - t0 < a.seconds:
            buf += s.read(4096)
        s.close()
        data = bytes(buf)

    v = Verifier(pub)
    for body in frames(data):
        v.feed(body)
    rep = v.report()
    print(json.dumps(rep, indent=2))
    if a.json:
        json.dump(rep, open(a.json, "w"), indent=2)
    sys.exit(0 if rep["pass"] else 2)


if __name__ == "__main__":
    main()
