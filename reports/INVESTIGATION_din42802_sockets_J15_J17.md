# Investigation — what are J15, J16 and J17?

**Status: investigation. No part has been chosen and `tools/design.py` is unchanged.**
Changing a non-substitutable patient-connected part is Stephane's decision.

**Read §4 first if you read nothing else.** The evidence points at a footprint change, and it
is far cheaper before the layout desk starts than after.

---

## 1. Provenance — where `SLB1,5-F / LB-I1,5` came from

**It has been in the package since the first commit and has never been corrected.**

| | |
|---|---|
| Introducing commit | **`b18782a`** — the **root commit** of the repository |
| Author / date | Stephane van der Aa, 3 September 2026 |
| Form at introduction | `"Staubli SLB1,5-F / LB-I1,5"` — **byte-identical to today** |
| Commits touching the string since | 8, none of which changed the designation |

**It was never verified against a catalogue, and the package has never claimed it was.** That
second half matters, and it is the most important thing in this section.

`AVL-EEG-017` §1.4.1 — *"The DIN 42802 sockets — the one line with no qualified vendor"* —
already states:

> `design.py` names *Stäubli SLB1,5-F / LB-I1,5*. **That is a class of part, not a confirmed
> PCB part: those are cable and panel parts.** … **No catalogue part has been confirmed to fit
> it.**

The AVL register row reads **OPEN WITH CRITERIA**; the risk table reads **"None qualified …
This is the highest-risk line in the file because it has no vendor at all and it is a
patient-safety part"**, with a **12-week first-article lead time**. `tools/footprint_audit.py`
reports J15–J17 as **OPEN**, never as a pass. `ECO-EEG-012` records the part status as open.

**ECO-EEG-031 is the near miss.** That change audited four part numbers that "could not be
bought or could not be fitted" and corrected three of them outright — the OPA4376 package, the
ferrite bead series, the tactile switch body size. For J15–J17 it did something different: it
added a `NOT_SUBSTITUTABLE` flag so a buyer reading the BOM could see the constraint. Its own
words: *"The part number is a class and not a qualified PCB part, which AVL-EEG-017 §1.4.1 and
ICD-EEG-006 §1 both already said. What was missing is that a buyer reading the BOM could not
see it."*

**So the audit that fixed three neighbouring part numbers deliberately did not fix this one —
it flagged it.** Nobody checked whether the designation exists.

### 1.1 What ECO-EEG-035 added, and what it did not

ECO-EEG-035 fetched and searched both Stäubli catalogues and found **neither designation
anywhere in either**. That is new: the package's prior position was that these were real
Stäubli *cable and panel* parts that merely were not PCB parts. They are not published parts
at all.

**A refinement to AVL-EEG-017 §1.4.1**, which says the named parts "are cable and panel parts".
On the evidence in §3 below, `SLB1,5-F` and `LB-I1,5` are **not Stäubli designations of any
kind**. The AVL's conclusion — no qualified vendor, sample required — is unaffected and
correct. Its characterisation of the two strings is not. **AVL-EEG-017 is not amended here.**

### 1.2 The part of this that is a communication error, not a package error

The package has said "class, not a confirmed part; OPEN; none qualified" consistently and in
several documents. **Three manufacturers were nevertheless told in writing that the part was
genuine and non-substitutable.** "Non-substitutable" is correct and is what `design.py`
records. "Genuine", in the sense of an orderable catalogue part, is a claim **the package
never made**. One manufacturer has priced something at USD 13.73 each against it, and what
they priced cannot now be identified. That is recorded in ECO-EEG-016 under ECO-EEG-036.

## 2. The requirement, stated without reference to any manufacturer

Assembled from `AVL-EEG-017` §1.4.1, `QP-EEG-010` §11.2, `DSN-EEG-003`, `RISK-EEG-011` and
`tools/fplib.py`. **This is what a candidate must meet. No brand appears in it.**

| # | Requirement | Source |
|---|---|---|
| 1 | Touch-proof 1.5 mm connector to **DIN 42802-1** | AVL §1.4.1 |
| 2 | **Finger-safe to IEC 60601-1 for a type BF applied part**; no accessible conductive part with the mating part withdrawn | AVL §1.4.1; RISK-EEG-011 |
| 3 | Instrument-side member of the pair — the carrier is the machine, not the lead | WH-EEG-008 §3.1.2; RISK-EEG-011 **SR-13** (gender itself is open) |
| 4 | Termination: **one Ø1.7 mm PCB pin on the footprint centre, two Ø1.5 mm retention posts at ±3.5 mm** — *or a documented deviation with a drawing* | AVL §1.4.1; `fplib.py` |
| 5 | Body within **9.8 × 7.8 mm**, 14 mm pitch between adjacent positions | `fplib.py` `DIN42802_1p5mm_Socket` |
| 6 | **Three distinct colours**, recorded per site (EMG1 cheek / EMG2 submental / EMG3 laryngeal) | AVL §1.4.1; WH-EEG-008 |
| 7 | Current rating **≥ 1 A stated on the datasheet** | AVL §1.4.1 |
| 8 | Mating force stated, repeatable over **≥ 500 cycles** | AVL §1.4.1 |
| 9 | Evidence: dimensioned drawing, RoHS/REACH, **ISO 10993-5 and -10** if touchable (S-05), CoC per lot | AVL §1.4.1 |
| 10 | **Class A supplier**; physical sample approved **in writing** before the fleet order | QP-EEG-010 §11.1; AVL §1.4.1 |

Requirement 4 is the one that decides everything below, and it already carries its own escape
hatch — *"or a documented deviation with a drawing"*.

## 3. Candidates, with evidence

**Rule applied: a candidate without a fetched document is not a candidate.** Everything in the
unverified list stays out of the comparison.

### 3.1 Verified — documents fetched and read

| Designation | Manufacturer | Document | Retrieved | Mount | Meets req. 4? |
|---|---|---|---|---|---|
| `MEB1,5-R` | Stäubli | Medical catalogue, doc. **11014109** | 2026-09-10 | **panel**, pressed into a pre-drilled panel | **No** — not a PCB part |
| `MLB1,5-R` | Stäubli | doc. **11014109**, assembly instruction MA H511 | 2026-09-10 | **panel**, surface-mounted or flush into a pre-drilled panel | **No** |
| `LS1,5-B` | Stäubli | doc. **11014109** | 2026-09-10 | **in-line, on a lead** | **No** — wrong end of the pair |
| `MS1,5-S` / `S-MS1,5-S` | Stäubli | doc. **11014109** | 2026-09-10 | **in-line, on a lead** | **No** — wrong end |
| `MLK1,5-B` | Stäubli | doc. **11014109** | 2026-09-10 | in-line coupler | **No** |
| `NL844P` | Digitimer | product page | 2026-09-10 | **lead-end plug**, 1.5 mm female DIN 42802 | **No** — wrong end |

**The decisive negative result.** Stäubli's medical catalogue, searched in full as fetched
text, contains **no occurrence of "PCB", "printed circuit", "solder pin", "through-hole" or
"board mount" anywhere in the document.** Every 1.5 mm DIN 42802 part Stäubli publishes is a
panel part or a cable part.

**No verified candidate meets requirement 4. Not one.**

### 3.2 Unverified — named, not evidenced, kept out of the comparison

AVL-EEG-017 §1.4.1 already directs that these be approached. Nothing here is a candidate until
a document is fetched.

| Lead | Why it is named | Status |
|---|---|---|
| Stäubli, **a PCB-terminated variant of the LB-I1,5 family** | AVL §1.4.1's own first suggestion. Would be bespoke; may carry tooling on top of the 12 weeks | **unverified** — no such variant appears in doc. 11014109 |
| **Wuhan Greentek** | an existing programme supplier (electrodes, kit BOM rows 34–36) with a DIN 42802 range | **unverified** — no document fetched |
| **Plastics One / Bio-Medical Instruments** | AVL §1.4.1 | **unverified** |
| **NEUROSPEC** — "DIN 1.5 mm touch-proof sockets, for soldering" | a solderable socket is the closest description seen to req. 4 | **unverified** — the shop URL redirect-looped and no datasheet was obtained |

**NEUROSPEC is the one worth a person's five minutes**, because "for soldering" is the only
phrase encountered anywhere that suggests a board-terminated part. It is in
`docs/datasheets/OPEN_LOOKUPS.md`.

## 4. The footprint consequence — flagged loudly, as asked

**Every part that exists is a panel part or a cable part. The carrier footprint is a PCB part.
On the evidence, `DIN42802_1p5mm_Socket` describes something no manufacturer publishes.**

`tools/fplib.py`'s own docstring already half-says it: *"Touch-proof 1.5 mm DIN 42802 **panel
socket, PCB-mount version**"* — a panel socket adapted to a board, which is a description of
something that was drawn rather than sourced.

AVL-EEG-017 §3 already names the fallback and its cost:

> The fallback, which needs an ECO, is **a panel-mount socket on a flying lead into a 1×3
> header, which moves the part off the carrier footprint entirely.**

### 4.1 What that costs, if it is taken

| | Change |
|---|---|
| **Carrier** | Three `DIN42802_1p5mm_Socket` footprints leave the board. Their three 1.7 mm plated holes and six 1.5 mm NPTH retention posts go with them — **`design.py` fabrication note 7 currently names 1.70 mm as the largest plated hole on the board**, and note 8's non-plated census changes |
| **Replaced by** | One 1×3 header, or three 1×1 positions, in the analogue zone — a much smaller footprint, on nets that are ELECTRODE class (L1 only, 0.35 mm clearance, no vias) |
| **Harness** | Gains three leads from the panel sockets to the header. WH-EEG-008 gains a part, a length, a colour per site and a pull-test row |
| **Enclosure** | POD-P1 gains three panel apertures. `mech_gen.py` and the POD-P1 drawings change |
| **Documents** | DSN-EEG-003 §3.2 hole census, AVL-EEG-017, WH-EEG-008, PARTS-EEG-019, QP-EEG-010 §11.2, ICD-EEG-006 |

### 4.2 Why the timing is the whole point

**The Rev C layout desk has not started.** The three sockets sit in the analogue zone among
the sixteen protection networks, on the tightest clearance rule on the board. Removing three
9.8 × 7.8 mm bodies and their nine holes, or moving them, is a **placement** change. Placement
is the first thing the layout desk does.

Done now, it is an edit to `design.py` and a re-emission of the Rev C inputs — the same
generators that already produce them. Done after placement, it is a re-place and a re-route of
the most constrained region of the board, and the 15-day layout leg is paid twice.

**This is a recommendation, stated as a recommendation:** settle whether J15–J17 are
board-mounted or panel-mounted **before** the layout desk is released to place, even if the
part itself is not chosen by then. The *mounting decision* is what the layout needs; the
*part* can follow.

## 5. What is not decided here

- **No part is chosen**, and `design.py` is untouched.
- **AVL-EEG-017 is not amended**, though §1.4.1's characterisation of the two strings is
  refined by §1.1 above.
- The **gender question is separate and also open** — `RISK-EEG-011` **SR-13**.
- The **USD 13.73 quotation** cannot be matched to a part; ECO-EEG-036 records it.

---

*Sources: `git log` on `tools/design.py` (`b18782a`, root commit); `docs/AVL-EEG-017_RevC`
§1.4.1, §3 and the J15–J17 register row; `docs/ECO-EEG-016_RevC` ECO-EEG-012 and ECO-EEG-031;
`tools/fplib.py`; `tools/footprint_audit.py`; `docs/QP-EEG-010_RevB` §11.1–11.2; Stäubli
medical catalogue doc. 11014109 and T&M catalogue doc. 11014124, both fetched 2026-09-10;
Digitimer NL844P page, fetched 2026-09-10. Licence: CC BY-SA 4.0.*
