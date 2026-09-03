#!/usr/bin/env python3
"""
atecc608b_config.py -- generator for the ATECC608B configuration-zone template (RFQ F-18, E-21).

WHAT THIS IS
  ASM-EEG-007 section 6.1 step 5 tells the operator that the provisioning script "writes the
  ATECC608B configuration zone from the template".  Until now no template existed anywhere in
  the package.  This script is the template: it builds the 128-byte configuration image and the
  byte mask that says which of those bytes this programme actually specifies, and it writes
  three files next to itself:

      atecc608b_config.bin        128 bytes, the configuration-zone image
      atecc608b_config.mask.bin   128 bytes, 0xFF = this byte is specified here, 0x00 = leave
                                  whatever the part shipped with
      atecc608b_config.txt        the annotated dump: every specified field, its value, why it
                                  has that value, and where that value came from

  Regenerate with:   python3 atecc608b_config.py
  Check in place:    python3 atecc608b_config.py --check      (exit 1 if the files have drifted)

THIS IS A PROPOSAL AND IT HAS NOT BEEN REVIEWED
  The configuration zone decides whether the device private key is usable, whether it can be
  read, and whether it can be replaced.  Locking it is irreversible.  Nobody has reviewed these
  values, no part has ever been written with them, and two of the four specified bytes carry a
  bit-field encoding this file could not verify against the datasheet it does not have.
  ATECC608B_CONFIG_TEMPLATE.md carries the per-field rationale and the reviewer checklist.
  `provision.py` refuses to write this template unless the operator passes `--write-config`,
  and refuses to lock the zone unless the operator passes `--lock` and echoes the unit serial
  back.

WHY IT SPECIFIES FOUR BYTES AND NOT 128
  A template that states all 128 bytes states 124 bytes this programme has no opinion about,
  and every one of them would be a value invented here and locked into silicon.  The instrument
  uses exactly one slot.  So this template specifies SlotConfig[0] and KeyConfig[0] and nothing
  else, and the mask tells the writer to leave every other byte at the value the part arrived
  with.  That is a smaller thing for a reviewer to check and a smaller thing to get wrong.  The
  cost is that the factory default for slots 1 to 15 is inherited rather than chosen, which is
  checklist item 5 in the template document -- a reviewer may decide it must be chosen, and the
  answer is then more masked bytes here, not a different mechanism.

Licence: MIT, matching firmware/tools/provision.py and the rest of the firmware source
(FW-EEG-001: "CC BY-SA 4.0 for this document; the firmware source is MIT").
"""
from __future__ import annotations
import argparse
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN_PATH = os.path.join(HERE, "atecc608b_config.bin")
MASK_PATH = os.path.join(HERE, "atecc608b_config.mask.bin")
TXT_PATH = os.path.join(HERE, "atecc608b_config.txt")

CONFIG_ZONE_BYTES = 128

# --------------------------------------------------------------------------- the zone layout
#
# Byte offsets of the ATECC608B configuration zone.  Only the regions this template touches or
# names are listed; the rest of the zone is left alone and is not described here, because a
# description of a byte nobody writes is a place for an error to hide.
#
# 0..15    serial number, revision, AES/I2C enable.  READ-ONLY: the part refuses writes here.
# 16       I2C address, factory default 0xC0 (7-bit 0x60 << 1).  drivers.c line 51 addresses the
#          part at 0x60, so the factory default is already the address the firmware uses and
#          this template does not change it.
# 19       ChipMode, which carries the watchdog duration.  Left at the factory default: the
#          longest command this instrument issues is GenKey, which drivers.c allows 115 ms
#          (drv_atecc_genkey), comfortably inside the shorter of the two watchdog settings.
# 20..51   SlotConfig[0..15], two bytes each, little-endian.
# 52..67   Counter[0..1].  Untouched -- no slot here is LimitedUse, so no counter is consumed.
# 84..87   UserExtra, UserExtraAdd, LockValue, LockConfig.  Never written by a template: the
#          lock bytes are set by the Lock command (0x17), which is provisioning step 2c.
# 88..89   SlotLocked.  Untouched.
# 96..127  KeyConfig[0..15], two bytes each, little-endian.
OFF_SLOTCONFIG = 20
OFF_KEYCONFIG = 96
SLOT_KEY = 0  # drivers.c ATECC_SLOT_KEY: the device key lives in slot 0 and never leaves it


# --------------------------------------------------------------------------- SlotConfig[0]
#
# SlotConfig is a 16-bit field stored little-endian.  Bit assignments:
#     0-3   ReadKey        for an ECC private-key slot these four bits are permissions, not a
#                          key id: bit0 external signatures, bit1 internal signatures,
#                          bit2 ECDH, bit3 ECDH master secret out in the clear
#     4     NoMac
#     5     LimitedUse
#     6     EncryptRead
#     7     IsSecret
#     8-11  WriteKey
#     12-15 WriteConfig
#
# The intent, in words, and then the value:
#
#   external signatures ENABLED.  F-08 has the device sign every 2048 samples and TST-EEG-004
#     T16 verifies that chain against the public key exported here.  Without this bit the
#     instrument cannot sign a block and T16 has nothing to check.
#   internal signatures DISABLED.  Nothing in this instrument uses GenDig-based internal
#     signing; a permission nothing needs is a permission not to grant.
#   ECDH DISABLED.  There is no key agreement anywhere in this design.  The stream is signed,
#     never encrypted to the host (ICD-EEG-006), so ECDH would only add a way to use the
#     identity key for something the instrument does not do.
#   LimitedUse OFF.  A limited-use slot burns a monotonic counter on each use.  This key signs
#     a block every 2048 samples for the working life of the instrument -- roughly one
#     signature every two seconds at 1000 Hz -- so any counter would run out and the unit
#     would stop signing mid-study.
#   IsSecret ON, EncryptRead OFF.  The private key is never readable by any means.  This is
#     E-21 and it is the whole reason the part is fitted.
#   WriteConfig = 2.  INTENT: GenKey may create the key inside the part; no command may write a
#     private key in from outside.  ** This nibble's encoding is the one value in this file
#     that could not be checked against the datasheet.  See checklist item 1. **
READKEY_EXTERNAL_SIGN = 0x1
READKEY_INTERNAL_SIGN = 0x2
READKEY_ECDH = 0x4

WRITECONFIG_GENKEY_ONLY = 0x2  # UNVERIFIED -- checklist item 1

SLOTCONFIG_0 = (
    (WRITECONFIG_GENKEY_ONLY << 12)  # WriteConfig
    | (0x0 << 8)                     # WriteKey: unused when no command may write the slot
    | (1 << 7)                       # IsSecret
    | (0 << 6)                       # EncryptRead
    | (0 << 5)                       # LimitedUse
    | (0 << 4)                       # NoMac
    | READKEY_EXTERNAL_SIGN          # ReadKey permissions
)

# --------------------------------------------------------------------------- KeyConfig[0]
#
# KeyConfig is a 16-bit field stored little-endian.  Bit assignments:
#     0     Private
#     1     PubInfo
#     2-4   KeyType   (4 = P-256 ECC)
#     5     Lockable
#     6     ReqRandom
#     7     ReqAuth
#     8-11  AuthKey
#     12    PersistentDisable
#     14-15 X509id
#
#   Private = 1, KeyType = P-256.  This is the F-18 device key.  drivers.c calls GenKey with
#     mode 0x04 to create it and mode 0x00 to read the public half back, which is only
#     meaningful for a private ECC slot.
#   PubInfo = 1.  LOAD-BEARING: with PubInfo clear, GenKey mode 0x00 -- provisioning step 4,
#     "read back the public key" -- is refused, and the unit ends up with a key nobody can
#     name.  The fingerprint on the M-03 label, the Data Matrix and T16 all come from that
#     read-back.
#   Lockable = 1.  It costs nothing today and leaves the programme the option of sealing the
#     slot individually after the key exists.  No opcode in this package uses it.
#   ReqRandom = 0, ReqAuth = 0, AuthKey = 0.  There is no second key to authorise against and
#     no host secret in the building (F-19), so an authorisation requirement here would make
#     the key unusable rather than safer.
KEYTYPE_P256 = 0x4

KEYCONFIG_0 = (
    (0 << 12)            # PersistentDisable
    | (0x0 << 8)         # AuthKey
    | (0 << 7)           # ReqAuth
    | (0 << 6)           # ReqRandom
    | (1 << 5)           # Lockable
    | (KEYTYPE_P256 << 2)
    | (1 << 1)           # PubInfo
    | (1 << 0)           # Private
)

# Every byte this template specifies, as (offset, value, field, why).  Nothing else is written.
FIELDS = [
    (OFF_SLOTCONFIG + 2 * SLOT_KEY, SLOTCONFIG_0 & 0xFF,
     "SlotConfig[0] low", "ReadKey=external-sign only, IsSecret=1, EncryptRead=0, LimitedUse=0"),
    (OFF_SLOTCONFIG + 2 * SLOT_KEY + 1, (SLOTCONFIG_0 >> 8) & 0xFF,
     "SlotConfig[0] high", "WriteKey=0, WriteConfig=GenKey-only (UNVERIFIED, checklist item 1)"),
    (OFF_KEYCONFIG + 2 * SLOT_KEY, KEYCONFIG_0 & 0xFF,
     "KeyConfig[0] low", "Private=1, PubInfo=1, KeyType=P-256, Lockable=1"),
    (OFF_KEYCONFIG + 2 * SLOT_KEY + 1, (KEYCONFIG_0 >> 8) & 0xFF,
     "KeyConfig[0] high", "AuthKey=0, ReqAuth=0, PersistentDisable=0, X509id=0"),
]


def build() -> tuple[bytes, bytes]:
    """Return (image, mask).  Unspecified bytes are zero in the image and zero in the mask;
    a writer must consult the mask, not the image, to know what to write."""
    img = bytearray(CONFIG_ZONE_BYTES)
    msk = bytearray(CONFIG_ZONE_BYTES)
    for off, val, _field, _why in FIELDS:
        img[off] = val
        msk[off] = 0xFF
    return bytes(img), bytes(msk)


def word_mask(mask: bytes, block: int) -> int:
    """Which four-byte words of one 32-byte block have any specified byte: bit i is set when any
    byte of word i is masked.  The ATECC writes the configuration zone in four-byte words, so a
    partially specified word has to be read, overlaid and written back -- which is why the
    proposed device opcode is a read-modify-write and not a blind copy.  This is derived from
    the byte mask rather than sent: the 0x4A payload carries the 32 mask bytes themselves."""
    out = 0
    for w in range(8):
        base = block * 32 + w * 4
        if any(mask[base:base + 4]):
            out |= 1 << w
    return out


def annotate(img: bytes, msk: bytes) -> str:
    sha = hashlib.sha256(img + msk).hexdigest()
    lines = [
        "ATECC608B CONFIGURATION-ZONE TEMPLATE -- annotated dump",
        "",
        "Generated by firmware/tools/atecc608b_config.py.  Do not edit: edit the generator and",
        "run it again.  Licence: CC BY-SA 4.0 (this dump); the generator is MIT.",
        "",
        "PROPOSAL, NOT REVIEWED.  No part has ever been written with these values.  Locking the",
        "configuration zone is irreversible.  Read ATECC608B_CONFIG_TEMPLATE.md, and in",
        "particular its reviewer checklist, before any part is written or locked.",
        "",
        f"template sha256(image||mask) = {sha}",
        f"bytes specified: {sum(1 for b in msk if b)} of {CONFIG_ZONE_BYTES}",
        "",
        "SPECIFIED FIELDS",
        "",
        "  offset  value  field               why",
        "  ------  -----  ------------------  ---------------------------------------------",
    ]
    for off, val, field, why in FIELDS:
        lines.append(f"  {off:>6}   0x{val:02X}  {field:<18}  {why}")
    lines += [
        "",
        "  16-bit values, as the part reads them (little-endian in the zone):",
        f"    SlotConfig[0] = 0x{SLOTCONFIG_0:04X}",
        f"    KeyConfig[0]  = 0x{KEYCONFIG_0:04X}",
        "",
        "WHAT IS NOT SPECIFIED",
        "",
        "  Every other byte of the zone is left at the value the part arrived with, including",
        "  SlotConfig[1..15] and KeyConfig[1..15], the counters, ChipMode and the I2C address.",
        "  The instrument uses slot 0 and no other slot.  Whether the factory default for the",
        "  fifteen unused slots is an acceptable posture is a decision for the reviewer, not an",
        "  omission this file is hiding: it is checklist item 5.",
        "",
        "BLOCK AND WORD MAP",
        "",
        "  provision.py sends one 0x4A command per block that has anything masked in it: the",
        "  block index, the block's 32 mask bytes, then its 32 image bytes.  The device reads",
        "  each four-byte word that has a masked byte, overlays the marked bytes and writes the",
        "  word back; a block with an empty mask is never sent at all.",
        "",
        "  block  byte range  sent  words touched",
        "  -----  ----------  ----  -------------",
    ]
    for blk in range(CONFIG_ZONE_BYTES // 32):
        wm = word_mask(msk, blk)
        words = ", ".join(str(w) for w in range(8) if wm & (1 << w)) or "none"
        sent = "yes" if wm else "no"
        lines.append(f"  {blk:>5}  {blk*32:>3}..{blk*32+31:<4} {sent:>4}  {words}")
    lines += [
        "",
        "RAW IMAGE (image byte, or '--' where the mask says leave it alone)",
        "",
    ]
    for row in range(0, CONFIG_ZONE_BYTES, 16):
        cells = " ".join(f"{img[i]:02X}" if msk[i] else "--" for i in range(row, row + 16))
        lines.append(f"  {row:>3}: {cells}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="regenerate in memory and compare with the files on disk; "
                         "exit 1 if they differ")
    a = ap.parse_args()

    img, msk = build()
    txt = annotate(img, msk)

    if a.check:
        bad = False
        for path, want in ((BIN_PATH, img), (MASK_PATH, msk), (TXT_PATH, txt.encode())):
            try:
                with open(path, "rb") as f:
                    have = f.read()
            except FileNotFoundError:
                print(f"MISSING {path}")
                bad = True
                continue
            if have != want:
                print(f"DRIFTED {path}")
                bad = True
        print("template files match the generator" if not bad else "run without --check to "
                                                                   "regenerate")
        return 1 if bad else 0

    with open(BIN_PATH, "wb") as f:
        f.write(img)
    with open(MASK_PATH, "wb") as f:
        f.write(msk)
    with open(TXT_PATH, "w") as f:
        f.write(txt)
    print(f"wrote {BIN_PATH}")
    print(f"wrote {MASK_PATH}")
    print(f"wrote {TXT_PATH}")
    print(f"sha256(image||mask) = {hashlib.sha256(img + msk).hexdigest()}")
    print("PROPOSAL: not reviewed, never written to a part.  See ATECC608B_CONFIG_TEMPLATE.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
