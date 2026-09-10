# Third-party datasheets — index

**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Owned by:** ECO-EEG-016 Rev C. Referenced by AVL-EEG-017, DSN-EEG-003 and JIG-EEG-009.

---

## What this directory is, and what it is not

Manufacturers quoting this package keep having to ask for datasheets the package does not
carry. Three have now asked for the Stäubli socket at J15–J17, and two have proposed the
wrong part against the OPA4376 line — a SOIC-14 package, then the dual OPA2376 — either of
which a datasheet in the package would have stopped at the first reading.

**This is an index of links, not a library of files.** Every entry below points at the
manufacturer's own canonical URL. No datasheet PDF is stored in this repository.

**Nothing here is licensed by this programme.** Manufacturer datasheets are third-party
copyrighted works. This repository's CC BY-SA 4.0 grant does not extend to them and cannot:
see `third_party/LICENCE_NOTE.md` and the licence statements in `README.md` and
`README_package_index.txt`, all of which now state the exclusion.

## How to read the "checked" column

| Mark | Meaning |
|---|---|
| **fetched** | the URL was retrieved and the document opened; what is claimed from it was read out of it |
| **resolved** | the URL returned the document, but its contents were not read against the claim |
| **blocked** | the manufacturer's site refused an automated request. The URL is the manufacturer's published address for the part and has NOT been confirmed to resolve |

Retrieval date is 2026-09-10 for every row. That is the date the link was checked, and it
is not a statement about fabrication of anything.

---

## 1. Stäubli — the patient-connected socket at J15, J16, J17

**This row is the urgent one, and it does not resolve. Read it before quoting the part.**

`design.py` gives J15, J16 and J17 the manufacturer part number **`Staubli SLB1,5-F /
LB-I1,5`**, footprint `DIN42802_1p5mm_Socket`, and DSN-EEG-003 makes them
non-substitutable because they are the connection to a person.

**Neither designation appears in either of Stäubli's published catalogues.**

| Catalogue | URL | Checked | Result |
|---|---|---|---|
| Medical technology main catalogue, doc. **11014109** | <https://www.staubli.com/content/dam/ecs/catalogs-brochures/medical/MED-Main-11014109-en.pdf> | **fetched** (3 547 338 bytes) | no occurrence of `SLB1,5` or `LB-I1,5` |
| Test & Measurement main catalogue, doc. **11014124** | <https://www.staubli.com/content/dam/ecs/catalogs-brochures/TM/TM-Main-11014124-en.pdf> | **fetched** (19 699 228 bytes) | no occurrence of either; the `SLB` series is `SLB2-*` and `SLB4-*` only |

In the `SLB` series the numeral is the **contact diameter in millimetres** — `SLB2-F` is a
2 mm socket, `SLB4-F` a 4 mm socket. `SLB1,5-F` is what that pattern would produce for a
1.5 mm part, and it is not a designation Stäubli publishes.

**What Stäubli does publish at Ø 1.5 mm to DIN 42802**, read out of the medical catalogue:

| Designation | What the catalogue calls it |
|---|---|
| `MEB1,5-R` | insulated **panel terminal** to DIN 42802, rigid gold-plated Ø 1.5 mm **pin**, accepting spring-loaded Ø 1.5 mm sockets; pressed into pre-drilled panels |
| `MLB1,5-R` | the same panel terminal, surface-mounted or assembled flush into pre-drilled panels. Assembly instruction MA H511 |
| `LS1,5-B` | in-line gold-plated Ø 1.5 mm **socket** with spring-loaded MULTILAM, for self-assembly onto a lead; mates with `MEB1,5-R` and `MLB1,5-R` |
| `MS1,5-S` / `S-MS1,5-S` | in-line gold-plated Ø 1.5 mm rigid **plug**, for self-assembly onto a lead |
| `MLK1,5-B` | in-line coupler |

**A correction to an earlier reading in this file.** ECO-EEG-035 first recorded here that
"a plug and a pin cannot both be right", because Stäubli's panel-mount parts present a **pin**
while the carrier footprint is named `..._Socket` and kit BOM row 36 buys leads with a
**plug**. **That was over-called.** In DIN 42802 trade usage the lead-end part is called a
*touch-proof plug* and is **electrically female**, and the instrument-end part is called an
*input socket* and carries the **recessed male pin**. Two independent manufacturers describe
it that way — see `RISK-EEG-011` open item **SR-13**, where the evidence is set out. So
Stäubli's panel terminals presenting a pin, a carrier footprint called a socket, and leads
called plugs are **mutually consistent**, not contradictory.

What remains genuinely open is in SR-13: the convention is read from vendor documentation
rather than from DIN 42802 or IEC 60601-1 themselves, and `WH-EEG-008` calls the lead-end
parts "**male** plugs" where those manufacturers call the same part female.

**Nothing in `design.py` has been changed.** The part number is recorded here as not found;
correcting a non-substitutable patient-connected part is a person's decision.

Stäubli's own contact address for the part, from the search that produced these catalogues:
`ec.ch@staubli.com`.

---

## 2. Texas Instruments — OPA4376

The quad op-amp at **U1, U2, U3**. Two manufacturers have proposed wrong parts against this
line: SOIC-14, and the dual OPA2376.

| Item | Value |
|---|---|
| Part fitted | `TI OPA4376AIPWR` (`design.py`) |
| Footprint | `TSSOP-14_4.4x5mm_P0.65mm` — **TSSOP-14, not SOIC-14** |
| Datasheet | <https://www.ti.com/lit/ds/symlink/opa4376.pdf> |
| Checked | **resolved** (1 697 245 bytes) |

The `PW` in `OPA4376AIPWR` is TI's package suffix for TSSOP; the `R` is tape-and-reel. The
quad is `OPA4376`; `OPA2376` is the dual and has four fewer channels than the design uses.

---

## 3. Murata — BLM18AG601SN1D

The ferrite bead at **L1**. One manufacturer proposed a 60 Ω part against this 600 Ω line.

| Item | Value |
|---|---|
| Part fitted | `Murata BLM18AG601SN1D` (`design.py`) |
| Specified as | 600 Ω at 100 MHz, 500 mA (`design.py` L1) |
| Product page | <https://www.murata.com/en-global/products/productdetail?partno=BLM18AG601SN1D> |
| Checked | **resolved** |

In Murata's `BLM18AG` part numbering the three digits before the letter are the impedance in
the usual two-significant-figures-plus-multiplier form: `601` is 60 × 10¹ = **600 Ω**, not
60 Ω. A part reading `600` would be 60 × 10⁰ = 60 Ω. That single digit is the whole
difference and is the likely source of the substitution offered.

**Do not re-propose `BLM18PG601SN1D`.** Rev B named that part at 1.5 A and **there is no such
part**: `PG` is Murata's large-current power-supply series, which is not made at 600 Ω in
1608 — its 0603 range stops at 470 Ω. It was corrected to the `AG` general series under
**ECO-EEG-031**, and the 1.5 A came with the wrong part number and had no requirement behind
it. L1 feeds VDD_ISO, tens of milliamperes, so the 0.38 Ω DC resistance costs about 10 mV.
AVL-EEG-017 row L1 is the governing entry.

---

## 4. Omron — B3F-1052

The tactile switch. Omron's part site refuses automated requests, so the URL below is
Omron's published address for the part and has **not** been confirmed to resolve.

| Item | Value |
|---|---|
| Part | `Omron B3F-1052` |
| Product page | <https://components.omron.com/us-en/products/detail/B3F-1052> |
| Checked | **blocked** (HTTP 403 to an automated request) |

Note that `design.py` records a ruling against this line: AVL-EEG-017 section 1.4 asks for
6.0 × 6.0 mm at 160 gf ± 50, and the fitted part is a 1.47 N (150 gf) four-terminal switch
chosen against that. Read the `design.py` comment at the switch before quoting it.

---

## 5. Texas Instruments — ADS1299

The converter. It is on a purchased module, not on the carrier, so it is not in the carrier
BOM — see ICD-EEG-006 for the module interface.

| Item | Value |
|---|---|
| Datasheet | <https://www.ti.com/lit/ds/symlink/ads1299.pdf> |
| Checked | **resolved** (1 842 419 bytes) |

RISK-EEG-011 already records that **no ADS1299 datasheet figure answers for a third-party
module's output**. The datasheet bounds the silicon, not the breakout.

---

## 6. Texas Instruments — TS5A3159

Not fitted anywhere today. It is the analogue switch in the **fallback** for kit BOM row 11,
the room microphone with hardware mute (E-15), which is an open item and not a design.

| Item | Value |
|---|---|
| Datasheet | <https://www.ti.com/lit/ds/symlink/ts5a3159.pdf> |
| Checked | **resolved** (834 457 bytes) |

---

## 7. Omron — G6K-2F-Y — **the fixture blocker**

Not a product part. It is the signal relay assumed by **FIX-01**, and it is the reason the
fixture boards have no copper.

`tools/fixture_gen.py` states the dependency plainly: laying out 83 relays and 144 precision
resistors turns on one dimension, "the land pattern of the Omron G6K-2F-Y — a datasheet this
package does not carry". `fixtures/pcb/FIX-01/README_fixture_pcb_data.txt` puts the area
budget at 60 % occupancy against a 60 % working limit, with the largest land pattern the
160.0 × 100.0 mm outline can carry at **70.7 mm²** against an **assumed** 70.0 mm² — a margin
of **1.0 %**.

| Item | Value |
|---|---|
| Product page | <https://components.omron.com/us-en/products/detail/G6K-2F-Y> |
| Checked | **blocked** (HTTP 403 to an automated request) |

**Until this land pattern is read off the datasheet and checked against 70.7 mm², the FIX-01
outline is provisional and no fixture layout should be commissioned.** That is WP3's
stage-one finding as much as this index's.

---

## What is still missing

**Three of these need a person, and `OPEN_LOOKUPS.md` is the sheet to work through** — one
page, three figures, each with the URL, the number needed, where to record it and what it
unblocks. Start there rather than here.


- The Stäubli part, which does not resolve at all (section 1).
- The two Omron land patterns, which need a person to open the pages an automated request
  cannot reach (sections 4 and 7).
- ES8388, bq24074, MAX17048, TPS63020, ADuM4160, MAX4466 and the 74HC595 — the purchased
  modules. These are specified **by interface** in ICD-EEG-006 rather than by part, so a
  datasheet index entry would name a candidate the package has deliberately not fixed. They
  are left out on purpose; ICD-EEG-006 is the document a bidder should be sent.

Licence: this file is CC BY-SA 4.0. **The documents it links to are not.**
