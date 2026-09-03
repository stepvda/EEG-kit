# ATECC608B CONFIGURATION-ZONE TEMPLATE

**Status: PROPOSAL. Not reviewed, never written to a part, not released for production.**
**Owner of the decision: the programme, with a security reviewer. Not the manufacturer.**

**Document:** this file, `firmware/tools/ATECC608B_CONFIG_TEMPLATE.md`
**Generated artefacts:** `atecc608b_config.bin`, `atecc608b_config.mask.bin` and
`atecc608b_config.txt`, all three written by `firmware/tools/atecc608b_config.py`
**Licence:** CC BY-SA 4.0 for this document; the generator is MIT, like the rest of the
firmware source (FW-EEG-001 header)
**Governing documents:** RFQ-EEG-001 Rev E F-18 and E-21, FW-EEG-001 Rev C section 7,
TST-EEG-004 Rev C T6, ASM-EEG-007 Rev B section 6.1

---

## 1. Why this file exists

ASM-EEG-007 section 6.1 step 5 tells the operator at the provisioning station that the script
"writes the ATECC608B configuration zone from the template, locks it, generates the P-256 key
pair in slot 0". There was no template. Not in `docs/`, not in `firmware/`, not in `webtest/`:
no SlotConfig or KeyConfig byte block, no `.bin`, no JSON and no table in any document. An
operator following that instruction had nothing to point the script at, and the script had no
step that would have used one.

That is not a missing file so much as a missing decision, and it is the reason this template is
a proposal rather than a release. The configuration zone decides three things that cannot be
decided later:

* whether the private key in slot 0 can ever be used to sign, which is what F-08's signature
  chain and TST-EEG-004 T16 depend on;
* whether it can be read out or written in from outside, which is what E-21 exists to prevent;
* whether it can be replaced in the field, which is what makes the identity on the M-03 label
  mean anything.

**Locking the zone is irreversible.** A part locked with the wrong template is scrap. J11 is
socketed, so the loss is one ATECC breakout rather than one board, and the manufacturer holds
10 % spares -- but a template that is wrong in a way nobody notices produces a fleet of units
whose identity is worth less than the label claims, and that failure is silent.

## 2. What is in the template

The instrument uses one slot. So the template specifies four bytes and masks out the other 124.

| Offset | Value | Field | Intent |
|---|---|---|---|
| 20 | `0x81` | SlotConfig[0] low | external signatures permitted; IsSecret set; EncryptRead clear; LimitedUse clear |
| 21 | `0x20` | SlotConfig[0] high | WriteKey 0; WriteConfig = "GenKey may create, no command may write" |
| 96 | `0x33` | KeyConfig[0] low | Private; PubInfo; KeyType P-256; Lockable |
| 97 | `0x00` | KeyConfig[0] high | AuthKey 0; ReqAuth clear; PersistentDisable clear; X509id 0 |

As the part reads them: **SlotConfig[0] = `0x2081`, KeyConfig[0] = `0x0033`.** The per-bit
reasoning is written out in `atecc608b_config.py` beside each bit, and the annotated dump
`atecc608b_config.txt` reproduces it next to the byte values, so a reviewer never has to
reconstruct an intent from a hex constant.

Three of those choices are load-bearing enough to restate here:

**PubInfo must be set.** With PubInfo clear, GenKey mode `0x00` -- provisioning step 4, "read
back the public key" -- is refused. The unit would then hold a key that nobody can name: no
fingerprint for the M-03 label, nothing in the Data Matrix, and nothing for `verify_stream.py`
to check T16's chain against.

**LimitedUse must be clear.** A limited-use slot consumes a monotonic counter on every use.
This key signs a block every 2048 samples -- about one signature every two seconds at 1000 Hz --
for the working life of a kit that circulates between participants. Any counter runs out, and
the unit stops signing part-way through a session rather than at a boundary anyone would notice.

**ECDH is not enabled.** The stream is signed and never encrypted to the host (ICD-EEG-006), so
key agreement is a capability this instrument has no use for. A permission nothing needs is a
permission not to grant.

## 3. Why it specifies four bytes and not 128

A 128-byte template states 124 bytes this programme has no opinion about, and every one of them
would then be a value invented here and locked into silicon on the strength of that invention.
So the template ships as an image plus a **mask**: `atecc608b_config.mask.bin` carries `0xFF`
for each byte this programme specifies and `0x00` for each byte the writer must leave at
whatever the part arrived with.

The cost is stated plainly: the configuration of slots 1 to 15 is then **inherited from the
factory default rather than chosen**. That is checklist item 5 below. A reviewer may decide the
unused slots must be explicitly locked down, in which case the answer is more masked bytes in
`atecc608b_config.py` -- not a different mechanism, and not a hand-edited binary.

## 4. How it reaches the part

The ATECC writes the configuration zone in four-byte words, so a template that specifies some
bytes of a word needs a read-modify-write. The proposed device command does that:

```
CMD_ATECC_WRITE_CONFIG = 0x4A          (proposed; not implemented in the shipped firmware)

payload, 65 bytes:
    0        block index, 0 to 3       (block n covers configuration-zone bytes 32n .. 32n+31)
    1..32    the 32 mask bytes of that block   (0xFF = overlay this byte, 0x00 = leave it)
    33..64   the 32 image bytes of that block

device behaviour, for each four-byte word with at least one masked byte:
    read the word from the configuration zone             (Read, opcode 0x02, zone 0)
    overlay the bytes whose mask byte is 0xFF
    write the word back                                   (Write, opcode 0x02, zone 0)
    refuse, with a distinct status, any word inside bytes 0..15 or 84..87
    skip, without an error, a block whose mask is all zero
```

65 bytes fits comfortably: the whole frame is 80 bytes, 81 COBS-encoded, against the 256-byte
receive accumulator in `main.c` `rx_poll()`.  `provision.py` computes that length before it
sends anything and refuses a frame the device could not receive.

Bytes 0 to 15 are read-only on the part; bytes 84 to 87 are the lock bytes and belong to the
Lock command (`0x47`), which is provisioning step 2c. The device must refuse both rather than
attempt them.

For this template the word map is trivial and `atecc608b_config.txt` prints it: block 0 word 5
(SlotConfig[0]) and block 3 word 0 (KeyConfig[0]). Two words, eight bytes touched, four of them
overlaid from the template and four preserved from the part.

For this template `provision.py` sends two of the four blocks -- block 0 for SlotConfig[0] and
block 3 for KeyConfig[0] -- and skips the other two, because their masks are empty and there is
nothing in them this programme has an opinion about.

**None of this exists in the shipped firmware.** `firmware/main/main.c` `handle_provision()` has
no `0x4A` case and `firmware/main/drivers.c` exposes only genkey, pubkey, config_locked and
lock_config. Those two files are the coordinator's, not this station's. Until the opcode lands,
`provision.py --write-config` will send `0x4A`, receive the unknown-opcode status and stop
**before** anything irreversible happens; it says so in those words.

## 5. The order the silicon requires, which is not the order the documents give

FW-EEG-001 section 7.3 puts GenKey at step 3 and the configuration-zone lock at step 8. On a
factory-fresh part that sequence cannot work: the part will not generate a key into a slot whose
configuration has not been written and locked, so step 3 fails, and step 8 would then lock the
default Microchip configuration -- permanently scrapping the breakout without ever creating the
device identity.

`provision.py` therefore runs, and FW-EEG-001 section 7.3 must be corrected to:

| # | Step | Opcode | Irreversible |
|---|---|---|---|
| 1 | enter provisioning mode | `0x40` | no |
| 2 | read the ATECC608B serial | `0x43` | no |
| **2b** | **write the configuration zone from this template** | **`0x4A` (proposed)** | no, but it is the last chance to get it right |
| **2c** | **lock the configuration zone** | **`0x47`** | **yes** |
| 3 | generate the P-256 key pair in slot 0 | `0x41` | **yes** |
| 4 | read back the public key | `0x42` | no |
| 5..7 | USB identifiers, hardware revision, unit serial, calibration | `0x44` `0x45` `0x49` `0x46` | no |
| **7b** | **read the constants back and compare, which is T6's acceptance limit** | **`0x4B` (proposed)** | no |
| 8/9 | read the state back and confirm the lock took | `0x48` | no |
| 10 | leave provisioning mode | `0x4F` | no |

FW-EEG-001 section 7.3 already says that where the table and the script differ, the script is
what runs. The table still needs correcting, and that document is not this station's to edit.

## 6. Reviewer checklist

Nobody may write or lock a part until every item here is answered by a named person against the
ATECC608B datasheet. The programme owns this list; the manufacturer must not close any item on
it.

1. **`WriteConfig` encoding.** The template sets the `WriteConfig` nibble of SlotConfig[0] to
   `0x2` with the intent "GenKey may create the key in this slot; no command may write a private
   key in from outside". **This encoding was not verified against the datasheet's WriteConfig
   table.** It is the single most consequential unverified value in this package: too permissive
   and a key can be written in from outside, which defeats E-21; too restrictive and GenKey is
   refused after the zone is locked, which scraps the part. Check it against the SlotConfig
   WriteConfig bit table for the 608B specifically, not the 508A.
2. **`ReadKey` permission bits for an ECC private-key slot.** The template sets bit 0 only,
   intending "external signatures permitted, internal signatures and ECDH not". Confirm the bit
   meanings and confirm that bit 0 alone is sufficient for the Sign command the F-08 block
   signing will use.
3. **The `0x4A` framing itself** (section 4). The opcode number, the 65-byte payload and the
   read-modify-write behaviour are proposed here and implemented on the host side only. Confirm
   them before `main.c` and `drivers.c` are written to them, because after that the two ends
   have to change together.
4. **The data-zone lock.** Confirm whether Sign requires the data zone to be locked as well as
   the configuration zone. If it does, provisioning needs a further irreversible step and a
   further opcode -- `drivers.c` exposes only `drv_atecc_lock_config()` (Lock mode `0x80`) and
   there is no data-zone equivalent anywhere in the firmware. **If this is required and is
   missing, T16 cannot pass on any unit**, and that is a firmware gap, not a template gap.
5. **The fifteen unused slots.** This template leaves SlotConfig[1..15] and KeyConfig[1..15] at
   the factory default (section 3). Decide whether that default is an acceptable posture on a
   locked part, or whether the unused slots must be explicitly configured as unusable. If the
   latter, extend `FIELDS` in `atecc608b_config.py` and regenerate.
6. **`ChipMode` and the watchdog.** The template leaves ChipMode at the factory default. The
   longest command the firmware issues is GenKey, for which `drivers.c` allows 115 ms. Confirm
   that the default watchdog duration exceeds the worst-case GenKey time for the 608B, because a
   watchdog that expires mid-GenKey on a locked part is not recoverable by retrying.
7. **The part number.** The template assumes **ATECC608B-SSHDA**. The **-TNGTLS variant must
   never be substituted**: it arrives with its configuration zone already locked and its keys
   owned by Microchip, so F-18 and E-21 are impossible on it. ASM-EEG-007 section 3 and
   AVL-EEG-017 both say so; confirm the parts received are SSHDA before the first write.
8. **One part, written and read back, before any production run.** Write this template to a
   sample part, read the configuration zone back and diff it against
   `atecc608b_config.bin`/`.mask.bin` on the masked bytes, then lock, then GenKey, then export
   the public key and verify one signature end to end with `verify_stream.py`. Until that has
   happened on one part, nothing here is more than reasoning.

## 7. What this template does not claim

* No part has been written with it, and none has been locked. Every statement about how the
  silicon will behave is read from the datasheet's published semantics or reasoned from the
  design, and is marked where it is not certain.
* The firmware opcode it needs does not exist.
* The `WriteConfig` encoding is unverified (item 1).
* Nobody has reviewed it.

`provision.py` therefore refuses to write it without `--write-config`, refuses to lock the zone
without `--lock` and an echoed-back unit serial, and records the SHA-256 of the template it sent
into the per-unit record so that a fleet can be told apart by which template made it.


---

## Review of this template, and the sequence it must be written in

*Settled 2 September 2026.  Decided from the package's own numbers, attacked by an
independent reviewer, and re-decided against that attack.  It is a DECISION and not an
approval: The programme's named security reviewer, countersigned by the programme lead, against the ATECC608B datasheet — the template's own §6 says the manufacturer may not close any checkl*

**The question.**

Is the proposed ATECC608B configuration-zone template
(firmware/tools/ATECC608B_CONFIG_TEMPLATE.md + atecc608b_config.bin) right, and what must a
security reviewer check before a part is locked?

**The decision.**

SPLIT. Adopt the template bytes unchanged. Reject the sequence ruling and replace it. KEEP —
the four bytes and the mask, verified byte-for-byte against the shipped binaries: - offset
20 = 0x81, offset 21 = 0x20 → SlotConfig[0] = 0x2081 (ReadKey = 0x1 external signatures
only; NoMac 0; LimitedUse 0; EncryptRead 0; IsSecret 1; WriteKey 0x0; WriteConfig 0x2) -
offset 96 = 0x33, offset 97 = 0x00 → KeyConfig[0] = 0x0033 (Private 1; PubInfo 1; KeyType =
(0x33>>2)&7 = 4 = P-256; Lockable 1; ReqRandom/ReqAuth 0; AuthKey 0; PersistentDisable 0;
X509id 0) - mask 0xFF on exactly bytes 20, 21, 96, 97 and 0x00 on the other 124 (confirmed:
mask non-zero indices are exactly [20, 21, 96, 97]) Also keep, unchanged: reject FW-EEG-001
§7.3's GenKey-at-step-3 / lock-at-step-8 order; reject a full 128-byte template; refuse to
self-close checklist item 1 (the WriteConfig nibble must be read off the 608B's own table by
a named person); ban ATECC608B-TNGTLS; and record the J11 die marking per lot at T00 (AVL-
EEG-017 M5 names "Adafruit 4314", which has carried both 608A and 608B, while ASM-EEG-007 §3
requires 608B-SSHDA). DROP — the mandated data-zone lock as step 2d between the config lock
and GenKey. Do not mandate it now, and do not put it before GenKey. NEW ITEM 9, OPCODE
ALLOCATION — blocks any write, not merely any lock. 0x4A is double-allocated: -
firmware/main/main.c:321 `CMD_READ_CALIBRATION = 0x4A`, implemented at main.c:435 and
exempted from the g_prov_open gate at main.c:374-375 - firmware/tools/provision.py:116-117
`CMD_ATECC_WRITE_CONFIG = 0x4A` / `CMD_READ_CALIBRATION = 0x4B` - docs/FW-EEG-001_RevC:470
documents 0x4A as CMD_READ_CALIBRATION — the governing document sides with the firmware.
Resolution: keep 0x4A = READ_CALIBRATION (firmware and FW-EEG-001 already agree), move
provision.py's CMD_READ_CALIBRATION 0x4B → 0x4A and CMD_ATECC_WRITE_CONFIG 0x4A → 0x4B. Note
0x4B is currently occupied in provision.py, so this is a two-line swap, not a one-line move.
Re-check every new opcode against main.c's enum, never against provision.py's. UNTIL THAT IS
DONE, `provision.py --write-config --lock` IS UNSAFE ON ANY UNIT THAT HOLDS A CALIBRATION
BLOB. Verified arithmetic: write_config_zone() sends block 0 as
[0x4A][blk=0][msk[0:32]][img[0:32]] and block 3 as [0x4A][blk=3][msk[96:128]][img[96:128]]
(blocks 1 and 2 are skipped by `if not any(msk[...])`). main.c's READ_CALIBRATION reads off
= c[1] | c[2]<<8, want = c[3], i.e. block 0 → off = 0x0000, want = 0; block 3 → off =
0xFF03, want = 255 → clamped. With "calib" present, block 0 memcpys zero bytes and block 3
trips `off >= clen`; BOTH return status 0x00, rlen 0. write_config_zone() returns True,
rec["config_zone_written"] = True, the "STOPPING BEFORE THE LOCK" guard at provision.py:605
is bypassed, and 0x47 irreversibly locks a FACTORY-DEFAULT configuration zone — with a
record that falsely carries the template sha256. Gate the lock on positive evidence instead
of on the write's ACK: expose an ATECC Read (opcode 0x02, zone 0, word 5 for bytes 20-23 and
word 24 for bytes 96-99), diff the four masked bytes against atecc608b_config.bin, and
refuse 0x47 unless the read-back matches. DATA-ZONE LOCK — leave as template checklist item
4, open. If a named reviewer confirms Sign requires it, place it AFTER GenKey, after pubkey
read, and after any data-slot write: lock config → GenKey → pubkey → write data → lock data.
CMD_ATECC_LOCK_DATA / drv_atecc_lock_data() with Lock opcode 0x17, mode 0x81, param2 0x0000
is the right shape; 0x4C is genuinely free in both tables (main.c uses 0x40-0x4A + 0x4F,
provision.py 0x40-0x4B + 0x4F), so that number survives — but take it from the table fixed
in item 9. Resolve FW-EEG-001:1108 first ("writes the string unchanged into the USB
iSerialNumber, the ATECC608B data zone and the provisioning record"): the code writes NVS
only (CMD_WRITE_UNIT_SERIAL → drv_nvs_set_str("unit_serial")), so either the document is
stale and must be corrected, or the data lock must come after that write. KEEP, with a
correction — extending CMD_READ_PROVISION_STATE (0x48) to report LockValue (config byte 86 =
word 21 byte 2) beside LockConfig (byte 87) is worth doing and is wire-compatible
(provision.py tests `len(state) >= 1`). It needs a named drv_atecc_data_locked() sibling
reading w[2] of word 21, mirroring drv_atecc_config_locked()'s w[3]; without it the change
is not buildable as stated. ALSO REQUIRED, found in verification and in neither the decision
nor the attack: - firmware/tools/provision_selftest.py:69-70 models the shipped firmware as
one "which has no 0x4A and no 0x4B and answers status 0x01 for both". That is false against
main.c:321, so the package's own self-test can never catch this collision — it validates a
fiction. The simulator must model the real 0x4A. - The "STOPPING BEFORE THE LOCK" guard sits
INSIDE `if write_config:`, while step 2c sits under a separate `if lock:`. So `--lock`
without `--write-config` reaches the irreversible 0x47 with no guard at all, on a zone that
was never written. Guard 2c unconditionally. - Move the NVS constants (0x44, 0x45, 0x49,
0x46, 0x4A-serial) BEFORE the irreversible steps. They have no ATECC dependency, and
main.c:381-386 refuses CMD_ENTER_PROV once the config zone is locked, so any interruption
after 2c leaves a board that cannot be re-entered to finish. - Add an item for the absent
signing path: drivers.c exposes only genkey/pubkey/config_locked/lock_config/present — no
Sign, no Nonce — and main.c:739-740 marks the signing task "not shown". T16 cannot pass on
any unit regardless of lock state, so the data-zone-lock question should be decided together
with that implementation, not ahead of it. No part is written or locked until items 1-9 are
signed by a named reviewer.

**What the adversarial review changed.**

CONCEDED — the attack is right on every point I could check, and I verified each cited line
rather than taking it on trust. 1. The 0x4A collision is real and I confirmed all three
citations: main.c:321 defines CMD_READ_CALIBRATION = 0x4A (implemented at main.c:435, gate-
exempt at main.c:374-375); provision.py:116-117 assigns 0x4A to CMD_ATECC_WRITE_CONFIG and
0x4B to CMD_READ_CALIBRATION; FW-EEG-001:470 documents 0x4A as READ_CALIBRATION. My original
survey ("0x40-0x4B and 0x4F are taken in provision.py") checked the host table only and
never opened main.c's enum. That was the method error, and it propagated: I ratified the
template's §4 claim that "main.c has no 0x4A case", provision.py's error text "implements
0x40-0x49 and 0x4F only", and README_provisioning.md item 7 — all three are false against
this package. 2. I ran the framing arithmetic rather than accepting the attack's word for
it, and it lands exactly as described: block 0 → off = 0x0000/want = 0; block 3 → off =
0xFF03/want = 255. Both return status 0x00 with rlen 0 when "calib" exists, so the write
silently no-ops, the guard passes, and 0x47 locks a factory-default zone. 3. I went further
than the attack on reachability, which it asserted but did not pin down. Inside a single
fresh run the hazard is NOT live: provision.py locks at 2c before writing calibration at
step 7, and on a virgin part drv_nvs_get_blob("calib") fails, so 0x4A returns status 0x06
and the run dies safely (misdiagnosed, but safe). The live route is the ATECC swap. SVC-
EEG-013 §5.8 item 1 requires a replacement J11 module to be re-provisioned including
"calibration constants, configuration-zone lock", and item 4 keeps the TIOV-B-nnnn serial
with the unit — i.e. the ESP32 and its `calib` NVS blob are retained while a fresh, unlocked
ATECC is fitted. That is precisely "calib present, config zone unlocked". TST-EEG-004:741
routes T16 failures down the same path. Running --write-config --lock there destroys the new
breakout. So the attack's conclusion holds and is better supported than it argued. 4. The
"safe-if-wrong" ordering inference was invalid, and I concede it. On the 608 the slot
permissions are enforced against the data-zone lock state — the unlocked data zone is the
permissive one — so "GenKey permitted before the data lock" does not imply "permitted
after". My order converted checklist item 1, the WriteConfig nibble I explicitly refused to
close, into an irreversible fleet-wide dependency and deleted the fallback. Reversed. 5.
Conceded: the data-zone lock is verbatim checklist item 4 of the very document under review,
not a new finding, so there was no urgency justifying a second irreversible step in an
unverified order. 6. Conceded: FW-EEG-001:1108 does say the serial is written into the ATECC
data zone. My "this design writes no data slot" is true of the CODE (CMD_WRITE_UNIT_SERIAL
lands in NVS via drv_nvs_set_str) but the document says otherwise, and that contradiction
must be resolved before any data lock, not after. 7. Conceded: drivers.c has no Sign and no
Nonce; main.c:739-740 marks the signing task "not shown". T16 cannot pass today for reasons
that precede any lock. KEPT — the attack did not touch these, and I re-verified them
independently. The four bytes and the mask: img[20,21] = 0x81,0x20 and img[96,97] =
0x33,0x00, mask non-zero at exactly [20,21,96,97]. The decode holds bit for bit, including
KeyType = (0x33>>2)&7 = 4 = P-256. LimitedUse clear stays load-bearing (one signature per
2048 samples ≈ every 2.05 s at 1000 Hz would exhaust a monotonic counter mid-session);
PubInfo set stays load-bearing (GenKey mode 0x00 and the M-03 label fingerprint). Also kept:
rejecting FW-EEG-001 §7.3's order, rejecting a 128-byte template, refusing to self-close
item 1, banning -TNGTLS, the 0x48/LockValue extension, and the AVL/ASM die-marking item.
CORRECTED IN THE ATTACK — two places. Its fix (a) says "move CMD_ATECC_WRITE_CONFIG to 0x4B"
without noting 0x4B is already CMD_READ_CALIBRATION in provision.py; it is a two-line swap.
And its dismissal of "0x4C-0x4E are free" as "right only by luck" concedes too little to
itself: I checked both tables and 0x4C-0x4E are in fact free in each, so the LOCK_DATA
number stands even though the method that produced it was wrong. ADDED — two defects neither
side caught. provision_selftest.py:69-70 hard-codes the fiction that the shipped firmware
"has no 0x4A and no 0x4B and answers status 0x01 for both", so the package's own regression
test structurally cannot catch this collision. And the "STOPPING BEFORE THE LOCK" guard is
nested inside `if write_config:` while step 2c hangs off a separate `if lock:`, so `--lock`
without `--write-config` reaches the irreversible 0x47 with no guard whatsoever.

**Reasoning.**

I treated the attack as a hypothesis and opened every file and line it cited. All of them
held: main.c:321, 374-375, 381-386, 435, 739-740; provision.py:116-117, 487, 577-612;
drivers.c:431 (atecc_cmd(0x17, 0x80, 0x0000)) and 422-429 (config_locked reads w[3] = byte
87, so byte 86 = w[2] is the right sibling for LockValue); FW-EEG-001:470 and :1108. I also
independently decoded the two binaries rather than trusting either party's transcription,
and reproduced the write_config_zone → READ_CALIBRATION framing collision numerically. The
four-byte half of my original decision survives untouched because it is checkable and I re-
checked it. The sequence half does not survive, and it fails for a reason that indicts the
method rather than the conclusion: I surveyed opcode allocation in the host tool and treated
that as the allocation table. The device is the authority on what an opcode does, and the
device disagrees. Everything downstream of that survey — "0x4A write config" in the ratified
order, the claim that an absent opcode fails safe with an unknown-opcode refusal, the
confidence that the "STOPPING BEFORE THE LOCK" guard protects the irreversible step —
inherits the error. The severity turns on reachability, so I chased it rather than asserting
it. Within one run on a virgin part the sequence is self-protecting: the lock at 2c precedes
the calibration write at step 7, and with no `calib` key drv_nvs_get_blob fails and 0x4A
answers 0x06, killing the run. The hazard needs a board whose ESP32 NVS holds a calibration
blob while its ATECC is fresh and unlocked. SVC-EEG-013 §5.8 creates exactly that state as
routine service work: swap the J11 module, keep the unit and therefore its NVS, re-
provision. That makes this a live scrap path on spares that SVC §6 stocks precisely two of,
not a theoretical one. On the ordering, the attack's physics is better than mine. The
permissive state on a 608 is the unlocked data zone; the restrictive state is the locked
one, where SlotConfig.WriteConfig governs. Mandating lock-data-before-GenKey therefore bets
the whole fleet on WriteConfig = 0x2 being the correct GenKey permit — the single nibble I
had already declared unfit for me to close — and removes the fallback that would have caught
me being wrong. Ordering GenKey first costs nothing if the data lock turns out to be
required, because the lock can still follow; ordering the lock first is unrecoverable if the
nibble is wrong. That is the real safe-if-wrong direction, and it is the reverse of what I
wrote. I am not answering the underlying 608B questions here, and I should not: whether Sign
requires a locked data zone, and whether WriteConfig bit 1 is the GenKey permit, are
datasheet facts this package does not contain. My original decision leaned on "Microchip's
reference configurations" as corroboration, which is exactly the kind of half-remembered
authority that should not stand behind an irreversible step. Those stay open items for a
named reviewer with the datasheet in front of them. What I can settle from the files — the
four bytes, the mask, the opcode collision, its consequence, the guard defect, and the self-
test blind spot — I have settled. The overall question is still answerable, so this is not a
cannot-decide-here: the template's bytes are right, and the reviewer checklist is enumerable
and now has a ninth item that must be closed before anyone runs --write-config, not merely
before the lock.

**What would overturn it.**

On the bytes: the 608B WriteConfig table showing bit 1 is not the GenKey permit, or that 0x2
also permits PrivWrite — either changes the nibble before any part is locked. On the
sequence: a datasheet or CryptoAuthLib check showing Sign does not require a locked data
zone would retire checklist item 4 entirely; one showing it does would schedule the lock
after GenKey/pubkey/data-write, not before. A datasheet statement that GenKey into slot 0 is
permitted with the data zone LOCKED under WriteConfig = 0x2 would be the only thing that
could rehabilitate my original 2d ordering, and it would still be the more fragile of the
two. On the collision: nothing. It is settled from the files in this package and needs a
decision, not a measurement — pick one opcode table and make main.c, provision.py, FW-
EEG-001 §5, README_provisioning.md item 7, ATECC608B_CONFIG_TEMPLATE.md §4 and
provision_selftest.py's simulator agree. The measurement that converts the rest from
reasoning to fact is checklist item 8's one-part trial on a sacrificial breakout, and it
must now be run with the read-back gate in place: write the masked bytes, READ THEM BACK
from the config zone and diff before locking anything, then lock config, GenKey, export, and
verify one signature with verify_stream.py. If that trial is run before item 9 is closed, it
proves nothing, because the write never reaches the part.
