# PACKING, LABELLING AND SHIPPING

**Document:** PKG-EEG-015  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs.

**Revision letters used below.** Every cross-reference in this document names the current
issue of the document it cites: DSN-EEG-002 Rev E, DSN-EEG-003 Rev C, RFQ-EEG-001 Rev E,
FW-EEG-001 Rev C, TST-EEG-004 Rev C, SCH-EEG-005 Rev B, ICD-EEG-006 Rev B, ASM-EEG-007
Rev B, WH-EEG-008 Rev B, JIG-EEG-009 Rev B, QP-EEG-010 Rev B, RISK-EEG-011 Rev B,
REG-EEG-012 Rev B, SVC-EEG-013 Rev B, IFU-EEG-014 Rev B, ECO-EEG-016 Rev B, AVL-EEG-017
Rev B, SIM-EEG-018 Rev A, PARTS-EEG-019 Rev B, MECH-EEG-020 Rev A and RUL-EEG-021 Rev A.
Where an earlier letter appears it is deliberate and names a superseded issue, as in the
Rev C and Rev D readings of RFQ M-05 in section 3.1.

**Rev B in one line:** the carrier is now 150.0 × 130.0 mm on four layers and the pod grew
with it to 163.0 × 143.0 × 62.0 mm closed, so every packed dimension and every calculated
mass is restated; the serial format becomes `TIOV-B-nnnn` and section 5 of this document is
stated to be its single home; the headband is withdrawn from the packing list and RFQ A-03
is met by the chin strap and the occipital yoke; the calibration certificate moves to the
case lid pocket; the invented hatch interlock is deleted; the travel-case internal
dimensions are settled in section 3 on one transcription of one shell; and the foam schedule
is now checked against part **depth** as well as footprint, which CASE-00 Rev B fails
everywhere, so section 2.2 carries a Rev C schedule drawn to the settled case.

**Closed in this issue:** the findings raised against this document by the second
cross-document audit of 1 September 2026 -- 2.2 on where the serial format lives, 2.7 on the
travel-case internals, and 4.1 on governing-document revision letters. These are corrections
within the Rev B release and the revision letter is not advanced for them.

**Corrections after the verification review of package v2.2 (2026-09-02), revision letter
again unchanged.** The kit packing list now carries **all five** of the printed items
IFU-EEG-014 Rev B section 14 puts in the case lid wallet: the placement guide and the full
IFU are added as lines 6.2 and 6.3 and group 6 is renumbered, which closes IFU-EEG-014
section 16 item 14, and sections 2.2, 2.3 and the lid row of section 3.2 count five where
they counted three. Section
1.1 gains a check of every pocket name against the seven CASE-00 Rev C cut files. The two
citations of **DSN-EEG-002 Rev E section 10** in section 1.2 are marked as pointing at a
superseded section -- that table has no HM-10, still calls CASE-00 a two-layer insert, and
reads HM-04 as 8 + 2 spare per kit -- because DSN-EEG-002 has not been re-issued and
RISK-EEG-011 Rev B section 6.1 records that it must be corrected. And the state-of-charge
row of section 7 and open item 8 now say plainly that open item 8 is the **only** register
entry the package holds for the missing fuel-gauge step, because RFQ-EEG-001 Rev E section
9.1 item 12 raises it "as an open item" against a register that carries no such item.

**The label and packaging artwork is generated, at this issue, revision letter again
unchanged.** ECO-EEG-016 Rev B section 1 has registered ART-LBL-01 to ART-LBL-07,
ART-PACK-01, ART-DIS-01, ART-RET-01 and DRW-LBL-PLACEMENT as generated artifacts under
`graphics/` since Rev B was issued, and none of them existed. Section 1.1 ticked against
three files that were not in the package, section 4.2 made the QA placement sign-off a check
against a drawing that was not in the package, and the nine foam bay tags could not be
ordered as artwork at all. `tools/artwork_gen.py` now writes all eleven into
`graphics/labels/`, reading every legend, size, substrate and piece of copy out of this
document rather than out of a person's retyping. Section 4.3 is the index. Generating them
found three things this document had wrong or unstated, and they are open items 14, 15 and
16 rather than silent corrections: the regulated lithium pictogram is not in this package
and is not drawn; the 60 x 12 mm bay tag cannot carry the 8 mm cap height section 2.3 asks
for, on any of the nine legends; and the spare-cell tag is specified one way in section 4.2
and another in section 7.

## Why this document exists

The v1 package told a manufacturer to tick a packing list that did not exist, to cut a
foam insert from one DXF with no thickness and no bottom layer, to apply a label whose
serial format was never defined, to buy a travel case that three documents sized three
different ways, and to post a lithium cell to a stranger and get it back without once
naming a UN number. This document is the packing list, the foam and case specification,
the marking set, the serial-number scheme, the carton specification and the dangerous-goods
procedure, in one place, so that final assembly step T18 of TST-EEG-004 Rev C and step 10
of RFQ-EEG-001 Rev E section 9.1 can actually be performed and signed. It closes the
v1 audit entries `kit-packing-list`, `foam-insert-layout-drawing`, `mech-foam-dxf-defects`,
`case-selection-and-fit-spec`, `foam-labelling-and-packing-photograph`,
`unit-label-artwork-and-serial-scheme`, `case-and-carton-marking-set`, `mech-label-artwork`,
`outer-carton-and-return-shipping`, `lithium-shipping-procedure`, `lithium-shipping-dossier`
and `mech-packing-and-shipping`, and the serialisation half of `serialisation-and-dhr`.

Nothing in this package has been manufactured, packed, weighed or shipped, and **no safety
engineer has reviewed this design**. Every mass, every carton dimension and every
chargeable-weight figure below is **calculated** from part geometry and stated densities,
and is marked as such. Section 2.4 records, plainly, why the two-sheet CASE-00 Rev B
insert could not pack the kit, on footprint and on depth. The seven Rev C cut files that
replace it are released with this issue and the Rev B pair is deleted; what is still not
settled is the sheet size, because it is drawn to a case internal dimension that nobody
has measured.

### What changed in the design, and what it does to the packing

Two things changed during layout. Both are engineering findings rather than preferences,
and both land on this document, because packing is where board geometry finally becomes
freight cost.

**The carrier grew from 130 × 124 mm to 150.0 × 130.0 mm.** Thirty connectors, 211 parts
and 156 nets would not close at the smaller size. At kit quantities the extra 33.8 cm² of bare
board costs a few euro per unit against a real risk of an unroutable design.

**The carrier went from two layers to four**: L1 signal, L2 reference plane, L3 reference
plane, L4 signal. Package v1 asserted that a two-layer carrier would be cheap and easy to
route. Actually laying it out showed that it is not: on two layers the bottom side has to
be both the reference plane and the second routing surface, and it cannot be both. Four
layers give two full routing surfaces and a continuous reference under every analogue
trace, which is what DSN-EEG-002 Rev E section 13's "layout rules that are requirements, not
preferences" ask for, and which a swiss-cheesed two-layer pour cannot deliver. The zoning,
star-point and isolation rules that go with them are DSN-EEG-003 Rev C section 3.3. At 2
units that is about €35 more in total; at 50 units it is about €3 per board. The reference
planes are AGND_REF left of x = 62 mm and DGND right of it, on both inner layers, with
through vias only, 0.60 mm pad on a 0.30 mm finished hole, in a stack of mask / 35 µm L1 /
prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask =
1.60 mm ± 10 %.

The enclosure grew with the board. POD-P1 is now **163.0 × 143.0 × 58.0 mm external and
158.0 × 138.0 × 55.5 mm internal**, with a lid of 163.0 × 143.0 × 6.0 mm carrying a 2.0 mm
spigot, so the pod as packed is **163.0 × 143.0 × 62.0 mm closed**. The MP-01 module plate
is 146.0 × 126.0 × 3.0 mm. The consequences for this document are not cosmetic: the
POD-P1 ENCLOSURE foam pocket is now short in both axes and in depth, the pod assembly is
about 130 g heavier, the foam sheet has to be re-cut, and both the case and the carton grow.

---

## 1. Kit packing list (KPL-EEG-001 Rev B)

This table **is** KPL-EEG-001. TST-EEG-004 Rev C T18 and RFQ-EEG-001 Rev E section 9.1
step 10 tick against it, line by line. It is derived from `EEG_kit_BOM_for_bidders_RevB`
and from the part register PARTS-EEG-019 Rev B and DSN-EEG-003 Rev C section 4; where the kit BOM
was wrong, the corrected quantity is given here and the correction is listed in section 1.2.

Pocket names are the legends of the foam schedule in section 2.2. "Fitted" means the item
is already assembled into the helmet or the pod and is ticked in place, not packed loose.
Part identifiers are those of PARTS-EEG-019, which owns them.

### 1.1 The list

| # | Part | Description | Qty | Pocket | Serialised | Tick |
|---|---|---|---|---|---|---|
| **1 INSTRUMENT** | | | | | | |
| 1.1 | HM-01 | Helmet frame monocoque, MJF PA12, with channel cover strips | 1 | HELMET HM-01 | yes (kit id) | ☐ |
| 1.2 | HM-04 | Electrode assemblies bonded into HM-01 | 8 fitted | HELMET HM-01 | no | ☐ |
| 1.3 | HM-05 | Sintered Ag/AgCl cups on service bayonets, fitted | 8 fitted | HELMET HM-01 | no | ☐ |
| 1.4 | HM-05 | Sintered Ag/AgCl cups, spare | 2 | SPARE CUPS + KEYLESS SPARES | no | ☐ |
| 1.5 | HM-02 | TPU 85A pads: brow, occiput ×2, crown, fitted | 4 fitted | HELMET HM-01 | no | ☐ |
| 1.6 | HM-02 | TPU 85A pads, spare set | 4 | SPARE CUPS + KEYLESS SPARES | no | ☐ |
| 1.7 | HM-03 | Occipital yoke, ratchet dial housing and bought-in ratchet (HM-03A/B/C), fitted. **This and line 1.8 are what satisfies RFQ A-03** | 1 fitted | HELMET HM-01 | no | ☐ |
| 1.8 | HM-06 | Chin strap, chin cup and liner (HM-06A/B/C), fitted. **With line 1.7, satisfies RFQ A-03** | 1 fitted | HELMET HM-01 | no | ☐ |
| 1.9 | HM-06B | Chin-cup liner, spare | 1 | SPARE CUPS + KEYLESS SPARES | no | ☐ |
| 1.10 | HM-07 | Boom microphone arm: HM-07A temple mount and cheek sleeve, HM-07B 120 mm gooseneck, HM-07C electret capsule and windscreen. The capsule is **bare** -- the preamplifier is on MP-01 at J21, not on the boom | 1 | BOOM MICROPHONE | no | ☐ |
| 1.11 | HM-08 | Quarter-turn battery hatch, three lugs, coin slot, fitted | 1 fitted | POD-P1 ENCLOSURE | no | ☐ |
| 1.12 | HM-10 | Keyed 18650 cell carrier, fitted behind HM-08. Cannot be inserted reversed (RFQ S-04) | 1 fitted | POD-P1 ENCLOSURE | no | ☐ |
| 1.13 | POD-P1 | Prototype enclosure base and lid, **163.0 × 143.0 × 62.0 mm closed**, **Phase 1 only** | 1 | POD-P1 ENCLOSURE | yes | ☐ |
| 1.14 | EEG-CAR-01 | Carrier assembly Rev B: **150.0 × 130.0 × 1.60 mm, four layers**, 211 reference designators, on the MP-01 plate (146.0 × 126.0 × 3.0 mm), with **thirteen module assemblies of twelve types** -- twelve on MP-01 and the ESP32-S3-DevKitC-1 inserted directly into J6 and J7 | 1 fitted | POD-P1 ENCLOSURE | **yes (unit serial)** | ☐ |
| 1.15 | WH-01 | Electrode cable, 12-way screened, helmet to J14 | 1 fitted | HELMET HM-01 | no | ☐ |
| 1.16 | WH-02 | Light cable, 10-way, helmet to J30 | 1 fitted | HELMET HM-01 | no | ☐ |
| 1.17 | WH-09 | USB-B to USB-C panel pigtail, isolator module to the host aperture. **Interim, and a live non-conformance against RFQ E-24**: the only named isolator module presents USB-B and E-24 asks for USB-C. Fitted until an isolator module with a USB-C host connector is qualified | 1 fitted | POD-P1 ENCLOSURE | no | ☐ |
| **2 ELECTRODES** | | | | | | |
| 2.1 | — | Ag/AgCl ear-clip references | 2 | EAR CLIPS + EMG LEADS | no | ☐ |
| 2.2 | — | EMG snap-to-DIN 42802 leads, 1.0 m: red EMG1 cheek, yellow EMG2 chin, green EMG3 neck | 3 | EAR CLIPS + EMG LEADS | no | ☐ |
| 2.3 | — | Disposable EMG snap pads, pack of 30 (Ambu BlueSensor N or Kendall) | 1 pack | CONSUMABLES | no | ☐ |
| **3 AUDIO** | | | | | | |
| 3.1 | — | Closed-back headphones, **32 to 64 Ω** per RFQ A-04 as restated; the shipped model is the ATH-M20x at **47 Ω**, and the calibrated output level is measured per model into the 47.0 Ω load of TST-EEG-004 T17. 3.5 mm plug, ≥ 1.2 m lead | 1 | HEADPHONES | no | ☐ |
| **4 POWER AND CABLES** | | | | | | |
| 4.1 | — | Protected 18650 cell ≥ 3000 mAh, UN 38.3, in the HM-10 keyed carrier | 1 fitted | POD-P1 ENCLOSURE | lot recorded | ☐ |
| 4.2 | — | Protected 18650, charged spare | **0 in circulation** | SPARE CELL (empty) | — | ☐ |
| 4.3 | — | USB-C to USB-A cable, 1.0 m, USB 2.0 (A-07) | 1 | CABLES + CHARGER | no | ☐ |
| 4.4 | — | USB-C to USB-C cable, 1.0 m, USB 2.0 (A-07). **One of lines 4.3 and 4.4 is the host lead**; the host connection is a socket at the panel, not a captive cable | 1 | CABLES + CHARGER | no | ☐ |
| 4.5 | — | 5 V 2 A USB charger, EU plug, CE (A-07) | 1 | CABLES + CHARGER | no | ☐ |
| 4.6 | — | microSD 32 GB high-endurance, seated in the J20 breakout | 1 fitted | POD-P1 ENCLOSURE | lot recorded | ☐ |
| **5 CONSUMABLES** (resealable labelled pouch, A-05) | | | | | | |
| 5.1 | — | Conductive EEG paste, 100 g tube | 2 | CONSUMABLES | no | ☐ |
| 5.2 | — | Abrasive prep gel, 100 g | 1 | CONSUMABLES | no | ☐ |
| 5.3 | — | Saline wipes | 30 | CONSUMABLES | no | ☐ |
| 5.4 | — | Cotton buds, pack | 1 | CONSUMABLES | no | ☐ |
| 5.5 | — | Blunt-tip syringes for the gel ports | 4 | CONSUMABLES | no | ☐ |
| **6 DOCUMENTS** | | | | | | |
| 6.1 | IFU-EEG-014 | Laminated A5 quick-start card, artwork QSC-EEG-001: sections 2, 3, 5, 7, 10 and 12 of IFU-EEG-014 condensed to two sides | 1 | case lid wallet (sections 2.3 and 3.2) | no | ☐ |
| 6.2 | IFU-EEG-014 | Laminated A5 placement guide, artwork PLG-EEG-001: IFU-EEG-014 section 13 entire, with the head diagram and the face diagram. **Neither diagram has been drawn** (IFU-EEG-014 section 16 item 7), so no artwork exists to print and this line cannot yet be ticked | 1 | case lid wallet, beside the quick-start card | no | ☐ |
| 6.3 | IFU-EEG-014 | Full IFU, sections 1 to 13, A5 booklet. IFU-EEG-014 section 14 allows the runner's on-screen help panel instead of the booklet; **if the programme takes that option this line is struck by an ECO**, so that a packer never decides it | 1 | case lid wallet | no | ☐ |
| 6.4 | ART-PACK-01 | Laminated A5 packing photograph (M-06) | 1 | case lid wallet | no | ☐ |
| 6.5 | — | Per-unit calibration and test record, printed A4 | 1 | **case lid wallet**, beside the quick-start card | per serial | ☐ |
| 6.6 | ART-DIS-01 | Disinfection guide card (A-05) | 1 | CONSUMABLES | no | ☐ |
| 6.7 | ART-RET-01 | Return-shipping instruction sheet | 1 | carton label pocket | no | ☐ |
| 6.8 | — | Pre-paid return label | 1 | carton label pocket | tracking no. | ☐ |
| **7 MUST NOT BE PACKED** -- initial each line | | | | | | |
| 7.1 | HM-09 | Service key for cup release. Operator only, one per operator | 0 | — | — | ☐ |
| 7.2 | — | Loose lithium cell of any kind (section 7) | 0 | — | — | ☐ |
| 7.3 | — | Ultrasonic tooling, spare frames, spare cups beyond the two of line 1.4 | 0 | — | — | ☐ |
| 7.4 | — | **Headband or cap.** Withdrawn as a kit item: the eight electrodes are fixed to the HM-01 frame at manufacture, so a headband with fixed holders at the same eight sites would duplicate them. RFQ A-03 is met by lines 1.7 and 1.8 | 0 | — | — | ☐ |

Footer, signed by two people: *kit complete, case closed, hasps latched, seal number
______ applied, outer carton sealed.* Packer ______ Checker ______ Date ______.

**The five printed items, and why group 6 was renumbered at this issue.** IFU-EEG-014 Rev B
section 14 lists five printed items in the case lid pocket: the quick-start card, the
placement guide, the full IFU, the per-unit calibration record and the packing photograph.
This list carried three of them, and IFU-EEG-014 section 16 item 14 records the shortfall as
this document's to close. Lines 6.2 and 6.3 are added for the placement guide and the full
IFU, and the rest of group 6 is renumbered so that the five lid-wallet items read together
in the order the wallet holds them. Nothing outside this table cites a group 6 line number:
the packing photograph of section 2.3 numbers its call-outs to the KPL lines, and it does
not exist yet. Two of the five cannot be ticked today and say so on their own line -- the
placement-guide diagrams are not drawn, and both artwork identifiers QSC-EEG-001 and
PLG-EEG-001 are unregistered and collide numerically with RFQ-EEG-001 (IFU-EEG-014 section
16 item 12). A line that cannot be ticked is still the right line to carry: the packer is
the person who would otherwise discover the gap at the case, one kit at a time.

**Pocket names checked against the cut files.** Every pocket named in the column above is
one of the nine Rev C bays of section 2.2, and all nine are used: HELMET HM-01, HEADPHONES,
POD-P1 ENCLOSURE, BOOM MICROPHONE, SPARE CUPS + KEYLESS SPARES, SPARE CELL, CONSUMABLES,
EAR CLIPS + EMG LEADS and CABLES + CHARGER. The two destinations that are not foam bays are
deliberate: the case lid wallet, which Rev C has in place of the two deleted card pockets,
and the outer carton's label pocket. No line points at a bay of the withdrawn Rev B pair.
Read against the seven cut files themselves at this issue -- `mech/CASE-00_foam_layer_1.dxf`
to `_7.dxf` -- layers 1 and 2 carry all nine bay legends, layer 3 carries five (HELMET,
HEADPHONES, POD-P1, CONSUMABLES, CABLES + CHARGER), layer 4 two (HELMET, HEADPHONES) and
layers 5 to 7 the helmet bay alone, which is exactly the "layers cut" column of the section
2.2 schedule. The patient-contact consumables the kit is useless without are on the list and
in a bay: the two Ag/AgCl ear-clip references at line 2.1 and the three EMG DIN leads at
line 2.2, both in EAR CLIPS + EMG LEADS, with the disposable snap pads at line 2.3 in
CONSUMABLES. What this check does **not** establish is fit: six of the nine bays hold parts
that are not dimensioned anywhere in the package, so a name matching a name is not a part
matching a pocket, and section 2.2 and open item 1 say which six.

### 1.2 Corrections made to the kit BOM Rev B

| BOM item | As written | Corrected here | Reason |
|---|---|---|---|
| 8 | microSD breakout, "4-bit SDMMC capable" | one-bit SDMMC | ECO-EEG-009: the three data lines drive the contact-light shift register |
| 14 | "112 footprints" on a two-layer 130 × 124 mm carrier | **211 reference designators on a 150.0 × 130.0 mm four-layer carrier** | `design.py`; the layer and size change is explained above |
| 16 | HM-04 qty 10 per kit | 8 bonded, 2 spare bodies held as build stock, not kit content. **PARTS-EEG-019 §3.4 reads the same figure as 8 fitted + 2 spare per kit; the two documents disagree and the packer follows this list until PARTS is reconciled** | **DSN-EEG-002 Rev E section 10, a superseded section** -- see the note below this table. It is cited for the eight bonded assemblies only; its own quantity column reads HM-04 as 8 + 2 spare *per kit*, which is PARTS-EEG-019's figure and not this one, so it does not support the spare-body half of this correction. That half is this document's |
| 17 | "HM-07 battery hatch" | **HM-08** battery hatch; HM-07 is the boom arm | PARTS-EEG-019 §3, part-ID register |
| 17 | HM-08 as one line, "hatch and keyed cell carrier" | **split**: HM-08 is the hatch only (line 1.11); the keyed 18650 carrier is **HM-10** (line 1.12) | PARTS-EEG-019 §3.2 |
| 18 | POD-P1, qty 1 at every phase, 146.8 × 140.8 × 44 mm | Phase 1 only; **163.0 × 143.0 × 58.0 mm external, 158.0 × 138.0 × 55.5 mm internal, 62.0 mm closed with the lid** | `mech_gen.py`; RFQ M-01: Phases 2 and 3 use the HM-01 occipital shell |
| 19 | "TPU comfort pads ×4 and chin-cup liner", qty 1 | 4 fitted + 4 spare, liner 1 fitted + 1 spare | **DSN-EEG-002 Rev E section 10, a superseded section** -- see the note below this table. Its HM-02 row reads 4 + 4 spare and its HM-06 row calls the liner consumable, and that is all that is taken from it; the liner's 1 + 1 split is this document's |
| 20 | Headband or cap (RFQ A-03) | **Line deleted.** A-03 is rewritten to cover the chin strap HM-06 and the occipital yoke HM-03, both already on the frame | The eight electrodes are fixed to HM-01 at manufacture (IFU-EEG-014 §13.1) |
| 24 | "20-way FFC to carrier" | **two** cables: 12-way screened electrode cable to J14, 10-way light cable to J30 | ECO-EEG-014 |
| 29 | Headphones "32 Ω" | **32 to 64 Ω**; the ATH-M20x is 47 Ω and the test load is 47.0 Ω | RFQ A-04 as restated; TST-EEG-004 T17 |
| 31 | Consumables, no cotton buds, no disinfection guide | both added (lines 5.4, 6.3) | RFQ A-05 |
| 32 | One line, "USB-C to USB-A and USB-C to USB-C, 2 m" | two lines, 1.0 m each | RFQ A-07 |
| 33 | WH-08 captive host lead through a cable gland | **Deleted from the Phase 1 build.** The host connection is a socket in a gasketed aperture over the isolator module's own connector; the captive lead is a Phase 2 item for the helmet shell. WH-09 pigtail added as line 1.17 | RFQ E-24 non-conformance, stated at line 1.17 |
| 34 | Case "~340 × 250 × 210 mm, Nanuk 915 / Peli 1450" | envelope enlarged and those two models withdrawn as too shallow | section 3 |
| 35 | "DXF supplied for top layer" | both layers supplied, and both superseded by the Rev C stack of section 2.4 | section 2 |
| — | No line for the room-microphone module at J28 | included in the carrier assembly, line 1.14 | ICD-EEG-006 §1 |
| — | No line for MP-01 module plate | included in the carrier assembly, line 1.14 | ICD-EEG-006 §1 |
| — | Per-unit calibration record packed in a foam card slot | packed in the **case lid wallet** beside the quick-start card | TST-EEG-004 §12 and T18 |
| — | No line for the placement guide PLG-EEG-001 or for the full IFU | both added as lines 6.2 and 6.3, and group 6 renumbered so the five lid-wallet items read in order | IFU-EEG-014 Rev B §14 lists five printed items in the lid pocket; §16 item 14 records that this list carried three |
| — | Charged spare 18650 cut a foam pocket but had no BOM line | quantity is **zero** in circulation | section 7 |

**On the two citations of DSN-EEG-002 Rev E section 10.** That section is the frame parts
table, and it is **superseded on three counts and has not been re-issued**: it has no HM-10
line at all, because the keyed cell carrier was still folded into HM-08 when it was written
(corrected at BOM item 17 above from PARTS-EEG-019 section 3.2); it describes CASE-00 as the
withdrawn two-sheet insert with both sheets supplied as DXF, where section 2 of this document
now cuts the seven-layer Rev C stack and the two Rev B files are deleted; and its HM-04 quantity is
8 + 2 spare per kit, which is the figure BOM item 16 above departs from. RISK-EEG-011 Rev B
section 6.1 records that DSN-EEG-002 Rev E must be corrected, for its section 7 statement
that a charged spare cell travels in the kit, and no re-issue has been made. The two rows
above therefore cite it as the origin of a number, not as a live source, and where this
document and that section disagree, this document governs the packing. A reader wanting the
current frame parts list takes it from PARTS-EEG-019 Rev B.

Verification: the programme's goods-in in Brussels unpacks two kits per batch against this
list (RFQ 9.3, QP-EEG-010 A-21). Sign-off: programme QA.

---

## 2. Foam insert CASE-00

### 2.1 Material and construction

| Property | Value | Verification |
|---|---|---|
| Material | Closed-cell polyethylene (PE), not PU, not XLPE | Supplier certificate per lot |
| Density | 28 to 33 kg/m³ to ISO 845 | Supplier certificate |
| Compression stress at 25 % | 30 to 50 kPa to ISO 3386-1 | Supplier certificate |
| Colour | Black through-dyed | Visual |
| Layers, Rev B | Two, loose-stacked, not bonded | Visual |
| Layers, Rev C | **Seven loose-laid 25 mm layers, not two.** Section 2.4 explains why two 25 mm sheets cannot hold this kit | First article against the section 2.2 Rev C schedule |
| Stack depth, Rev C | **175.0 mm**, seven layers of 25 mm | Caliper, 4 points |
| Thickness as drawn, Rev B | 25 mm each layer, per the title text in both DXFs | Caliper, 4 points per sheet |
| Sheet size, Rev B | 340.0 × 250.0 mm, both layers | Caliper, ±2.0 mm |
| Sheet size, Rev C | **516.0 × 390.0 mm**: the Peli 1560's published 518 × 392 mm internal footprint minus 2 mm on each axis, settled in section 3.2 | Caliper against the measured shell **before any foam is cut**. The seven cut files are drawn to the published figure and are held: a shell that measures short does not make them tight, it makes them scrap |
| Pocket tolerance | ±1.0 mm | First article, then AQL per QP-EEG-010 |
| Lid foam | 15 mm PE or PU convoluted, plain, no pockets, over the helmet bay only | Visual |

Sign-off on the material: programme QA against the supplier certificate at IQC.

### 2.2 The foam pocket schedule and the cut files

**This section is the only authoritative foam pocket schedule in the package.**
SVC-EEG-013 Rev B section 2 R12, IFU-EEG-014 Rev B section 1 and PARTS-EEG-019 Rev B
section 2.3 cite this section and do not restate the pockets. Two schedules appear below
and they are not interchangeable. The **Rev B** schedule is what the two withdrawn DXF
files contained; it is recorded because they were released in package v2.1 and a
manufacturer may still hold them, and it cannot pack this kit for the reasons in section
2.4. The **Rev C** schedule is what will be cut, and at this issue it is also what the
package supplies: `tools/mech_gen.py` `foam_dxf()` writes the seven Rev C layer files
listed below it and cannot emit the Rev B pair any more. Anyone copying pocket sizes takes
them from the Rev C table.

Every cut file is supplied 1:1, `$INSUNITS = 4` (millimetres), datum at the bottom-left
corner of the sheet with X to the right and Y up. Two named layers are used and they mean
different things: **CUT** carries the sheet outline, every bay profile and the ⌀22 mm
finger reliefs; **TEXT** carries the bay legends and the title block and is **not an
output layer** -- nothing on layer TEXT is cut or engraved. v1 shipped one file with the
legends on the same layer as the cuts, which a laser would have cut out of the foam. That
is fixed.

The two Rev B files are **withdrawn, and deleted from `mech/` at this issue** rather than
left beside the Rev C stack, because a superseded cut file next to a live one is eventually
cut. What they contained is recorded here and nowhere else.

`CASE-00_foam_top_layer.dxf` -- top layer, as cut (Rev B, deleted):

| Legend | Origin (x, y) | Size (mm) | Finger relief |
|---|---|---|---|
| HELMET HM-01 | 12, 60 | 200 × 176 | ⌀22 at (112, 72) |
| HEADPHONES | 220, 130 | 108 × 106 | ⌀22 at (274, 142) |
| CONSUMABLES | 220, 60 | 108 × 62 | ⌀22 at (274, 72) |
| CASE LID CARD | 12, 6 | 316 × 46 | ⌀22 at (170, 18) |

`CASE-00_foam_bottom_layer.dxf` -- bottom layer, as cut (Rev B, deleted):

| Legend | Origin (x, y) | Size (mm) | Finger relief |
|---|---|---|---|
| POD-P1 ENCLOSURE | 14, 150 | 152 × 90 | ⌀22 at (90, 162) |
| EAR CLIPS + EMG LEADS | 176, 150 | 150 × 90 | ⌀22 at (251, 162) |
| CABLES + CHARGER | 14, 84 | 152 × 58 | ⌀22 at (90, 96) |
| SPARE CELL | 176, 84 | 70 × 58 | ⌀22 at (211, 96) |
| SPARE CUPS + KEYLESS SPARES | 252, 84 | 74 × 58 | ⌀22 at (289, 96) |
| BOOM MICROPHONE | 14, 14 | 152 × 62 | ⌀22 at (90, 26) |
| QUICK-START CARD | 176, 14 | 150 × 62 | ⌀22 at (251, 26) |

All Rev B pockets are through-cuts in their own 25 mm layer. **Rev C deletes the two card
pockets** -- CASE LID CARD and QUICK-START CARD -- because all five printed items travel in
the case lid wallet: the quick-start card, the placement guide, the full IFU, the
calibration certificate and the packing photograph (section 1.1 lines 6.1 to 6.5,
IFU-EEG-014 Rev B section 14). That closes the mismatch IFU-EEG-014 section 14 records and
cannot fix from its own side.

**CASE-00 Rev C -- the schedule that will be cut.** Sheet 516.0 × 390.0 mm, seven
loose-laid PE layers of 25 mm, 175 mm of stack, layer 1 uppermost, datum at the bottom-left
corner with X to the right and Y up. Origin and size are the bay opening in plan. "Layers
cut" says which layers the opening passes through; the first uncut layer beneath is the
floor of the bay. "Packer" is a plain uncut PE pad, cut from offcut, laid in the bottom of
the bay so the part sits near flush in an opening whose depth can only be a multiple of
25 mm. Finger reliefs are ⌀22 mm and are cut through the same layers as their bay.

| Legend | Origin (x, y) | Size (mm) | Layers cut | Cut depth | Packer | Finger relief |
|---|---|---|---|---|---|---|
| HELMET HM-01 | 14, 14 | 197 × 236 in layers 2 to 7; **181 × 220 at (22, 22) in layer 1**, which is the 8 mm shelf the halo lands on | 1 to 7, open to the case floor | 175 | none | none -- the helmet is lifted by the halo |
| HEADPHONES | 219, 14 | 181 × 161 | 1 to 4 | 100 | 17 | ⌀22 at (309, 28) |
| POD-P1 ENCLOSURE | 219, 183 | 169 × 149 | 1 to 3 | 75 | 10 | ⌀22 at (303, 197) |
| BOOM MICROPHONE | 14, 258 | 197 × 58 | 1 to 2 | 50 | at the trial pack | ⌀22 at (112, 272) |
| SPARE CUPS + KEYLESS SPARES | 14, 324 | 96 × 52 | 1 to 2 | 50 | at the trial pack | ⌀22 at (62, 338) |
| SPARE CELL | 118, 324 | 93 × 52 | 1 to 2 | 50 | at the trial pack | ⌀22 at (164, 338) |
| CONSUMABLES | 408, 14 | 94 × 140 | 1 to 3 | 75 | at the trial pack | ⌀22 at (455, 28) |
| EAR CLIPS + EMG LEADS | 408, 162 | 94 × 100 | 1 to 2 | 50 | at the trial pack | ⌀22 at (455, 176) |
| CABLES + CHARGER | 408, 270 | 94 × 106 | 1 to 3 | 75 | at the trial pack | ⌀22 at (455, 284) |

Nine bays, not eleven: the two card pockets are gone and all five printed items live in the
lid wallet. Every bay is at least 3 mm larger than its part on every axis it is dimensioned
against, every web between bays is at least 8 mm, and every bay is at least 14 mm from the
sheet edge. The layout closes: 14 + 197 + 8 + 181 + 8 + 94 + 14 = 516 mm across, and
14 + 236 + 8 + 58 + 8 + 52 + 14 = 390 mm up. The 181 × 36 mm patch above the POD-P1 bay is
left as solid foam.

The depth column is the half of this schedule Rev B did not have. HEADPHONES is cut through
four layers, 100 mm, with a 17 mm packer, so an 80 mm folded headphone sits in an 83 mm
well. POD-P1 is cut through three layers, 75 mm, with a 10 mm packer, so the 62 mm closed
pod sits in a 65 mm well. HELMET HM-01 is cut through all seven and is open to the case
floor, because the helmet is 158 mm tall and hangs from the shelf rather than sitting on a
pocket floor.

Six of the nine bays -- BOOM MICROPHONE, SPARE CUPS + KEYLESS SPARES, SPARE CELL,
CONSUMABLES, EAR CLIPS + EMG LEADS and CABLES + CHARGER -- hold parts that are not
dimensioned anywhere in package v2. Their plan sizes above are what the layout leaves once
the three dimensioned bays are placed, and their layer counts are a first estimate. What can
be said is that each of the six has **more volume than the Rev B pocket of the same name**,
between 1.4 and 5.9 times as much, because the extra depth more than pays for a narrower
plan: the ear-clip bay, the only one that loses plan area, goes from 338 cm³ to 470 cm³.
They are confirmed or corrected at the trial pack of section 2.4, and their packers are cut
then. Saying a bay is provisional is not the same as saying it is wrong; it means nobody has
yet held the part against it.

**The Rev C cut files.** Seven files, one per layer, written by `tools/mech_gen.py`
`foam_dxf()` from the table above and from nothing else. A bay is drawn in a file only where
the schedule cuts it through that layer, so the seven are not interchangeable and each one
names itself, its layer number and its bay count in its own TEXT layer.

| File | Part id | What is cut in this layer |
|---|---|---|
| `mech/CASE-00_foam_layer_1.dxf` | CASE-00-01 | all nine bays, with the helmet bay at the 181 × 220 mm shelf opening |
| `mech/CASE-00_foam_layer_2.dxf` | CASE-00-02 | all nine bays, helmet bay at the full 197 × 236 mm |
| `mech/CASE-00_foam_layer_3.dxf` | CASE-00-03 | HELMET HM-01, HEADPHONES, POD-P1 ENCLOSURE, CONSUMABLES, CABLES + CHARGER |
| `mech/CASE-00_foam_layer_4.dxf` | CASE-00-04 | HELMET HM-01, HEADPHONES |
| `mech/CASE-00_foam_layer_5.dxf` | CASE-00-05 | HELMET HM-01 |
| `mech/CASE-00_foam_layer_6.dxf` | CASE-00-06 | HELMET HM-01 |
| `mech/CASE-00_foam_layer_7.dxf` | CASE-00-07 | HELMET HM-01 |

Layers 5, 6 and 7 are the same cut, and they are supplied as three files anyway so that a
sheet cannot be laid into the stack at the wrong height with nothing on it saying so. The
identifiers CASE-00-01 and CASE-00-02 are re-used from the two deleted Rev B files at
Rev C; CASE-00-03 to CASE-00-07 are new, and PARTS-EEG-019 Rev B carries rows for the
first two only and has still to register the other five.

**What the Rev C table does not specify, and what the cut files do with it.** The **corner
radii**: the table gives none, so the files carry the radii of the deleted Rev B file, which
took them from package v1 -- R40 on the helmet bay because the frame is domed, R10 on the
two large equipment bays and on the ear-clip bay, R8 on the rest, R14 on the sheet. Section
2.3 orders a steel-rule die at Phase 3 and steel rule cannot be folded to a true 90 degree
inside corner, so a profile with no stated radius becomes whatever radius the die maker
chooses. The **packers**: the table gives a thickness for two of the nine bays and "at the
trial pack" for the other six, and no packer outline anywhere, so no packer is drawn in any
file and all of them are cut from offcut at the trial pack. The **title block**: its wording
and its position, in the solid patch above the POD-P1 bay and in the bottom edge margin, are
this document's and not the table's.

**And one thing the schedule has wrong, which the cut files reproduce rather than quietly
correct.** Every finger-relief centre in the Rev C table sits at least 3 mm inside its own
bay opening, so each ⌀22 mm circle falls entirely within foam that the bay profile already
removes, and it cuts nothing. A relief only does work when it straddles the bay wall, and
that cannot be had by moving the circle outwards: a straddling ⌀22 mm relief needs 11 mm of
foam beyond the wall and every web in this layout is 8 mm. The two ways out are a scallop
cut in the first uncut layer beneath the bay, which is where a finger actually goes in a
deep well, or a re-columned sheet with wider webs. Both are a Rev D of this schedule and
neither is invented here. The reliefs are cut where the table puts them, they cost nothing,
and open item 12 of section 9 carries the defect.

### 2.3 Cutting: laser or die

| Quantity | Method | Kerf compensation | Why |
|---|---|---|---|
| Phase 1, 2 kits | Pluck foam, hand-fitted (kit BOM item 35 alternate) | n/a | The layout is not yet verified against a printed helmet |
| Phase 2, 10 kits | Laser, CO₂, sealed edge | Profiles drawn on size; the cutter offsets 0.5 mm per side | Seventy sheets -- ten kits of seven layers -- does not repay five dies |
| Phase 3, 10 to 40 further kits, 25 to 50 in total | Steel-rule die, **one die per distinct layer profile: five, not one.** Layers 1, 2, 3 and 4 are four different profiles and layers 5, 6 and 7 are the fifth, all at one 25 mm thickness | None; profiles are the die line | Tooling repays itself past about 30 sheets per profile, and the layer 5 to 7 die cuts three sheets per kit |

PE cuts by melting. The edge seals, which is wanted, but PE **cannot be raster-engraved
legibly** -- the letters close up as they cool. The legends of RFQ M-06 are therefore
**printed adhesive tags**, artwork ART-LBL-04, 60 × 12 mm, white on black matt polyester
with permanent acrylic adhesive, one per bay. On a shallow bay the tag is bonded to the
pocket's rear wall at mid-depth; on the helmet, pod and headphone bays, which are now deep
wells, it is bonded to the **top face of the foam beside the opening**, because a tag 80 mm
down a well cannot be read. Cap height 8 mm. Legend text is exactly the schedule legend
string, so the tag and the cut file cannot drift, and `tools/artwork_gen.py` now enforces
that rather than asserting it: the tags are generated by reading the section 2.2 Rev C
schedule, so a legend cannot be re-typed differently on a tag than it is cut in a file.

**The 8 mm cap height does not fit the 60 mm tag, and none of the nine legends fits.** This
is a measurement, not an opinion. Set on one line at an 8 mm cap height in the face the
artwork uses, `HEADPHONES` -- the least demanding of the nine -- needs about 88 mm of tag,
`CONSUMABLES` 96 mm, `POD-P1 ENCLOSURE` 126 mm, `EAR CLIPS + EMG LEADS` 154 mm, `SPARE CUPS
+ KEYLESS SPARES` 200 mm, and the section 7 form of the spare-cell tag 320 mm. A narrower
face buys perhaps fifteen per cent, not the factor of one and a half the least demanding
needs and not the factor of five the worst needs. The generated tags are therefore drawn at
the 60 x 12 mm section 4.2 fixes, at the largest cap height that fits on at most two lines,
which runs from 5.36 mm on `HEADPHONES` down to 2.68 mm on the spare-cell tag. **Allowed two
lines, a tag of about 171 x 21 mm carries every legend at 8 mm**, the spare-cell tag again
setting the width. That is a change to section 4.2's tag size and to this paragraph's cap
height, and it is open item 15 of section 9 rather than a change made here. Verification: every legend present and
legible after the kit has been packed and unpacked once (QP-EEG-010 FK-04). Sign-off: QA.

**Five printed items** are fixed inside the case lid, not in the foam, in an A4 document
wallet retained by the lid: the laminated A5 quick-start card (A-06), the laminated A5
placement guide, the full IFU, the printed A4 calibration certificate and the laminated A5
packing photograph (M-06). That is the list of IFU-EEG-014 Rev B section 14, and it is now
also lines 6.1 to 6.5 of section 1.1. *Was: three items -- photograph, card and certificate*
-- which is the count IFU-EEG-014 section 16 item 14 raised against this document, because
the two guides it left out have nowhere else to travel: Rev C cuts no paper bay at all.

The photograph is taken of the first Phase 1 kit, 300 dpi, A5 landscape, call-outs numbered
to the KPL line numbers. Until a kit exists, a rendered layout marked **PROVISIONAL --
REPLACE WITH PHOTOGRAPH AT FIRST BUILD** is used. **That render now exists**:
`graphics/labels/ART-PACK-01_packing_layout_provisional.svg`, with its control sheet
`ART-PACK-01_packing_layout_provisional.pdf`. It draws the nine Rev C bays at true relative
scale on the 516.0 x 390.0 mm sheet and numbers each one with every packing-list line whose
pocket column names it, both read out of this document at generation time. It is a plan of
layer 1 and it shows no depth, so it says where a part goes and not that it fits; open item
1 still holds. Open item 7 is closed to the extent that the stand-in exists and is marked as
one; the photograph itself is still owed at the first build.

### 2.4 What is not yet right, stated plainly

CASE-00 Rev B is a coherent cut file and it cannot pack this kit. No kit is packed to
CASE-00 Rev B, and at this issue its two files are deleted and replaced by the seven Rev C
files of section 2.2. There are two independent failures and the second is the worse of
the two.

**Footprint.** Five of the eleven Rev B pockets cannot accept the item their legend names,
measured against the part geometry in `mech_gen.py` and DSN-EEG-002 Rev E.

**Depth.** Every Rev B pocket is a through-cut in a 25 mm sheet, so no pocket can hold
anything taller than 25 mm, and the three largest items in the kit are 62, 80 and 158 mm
tall. This was missed in Rev A of this document, which checked X and Y only.

| Pocket | As cut | Item and its real size | Shortfall in X / Y | Shortfall in depth |
|---|---|---|---|---|
| HELMET HM-01 | 200 × 176 through 25 mm | HM-01 standing on the halo, 191.1 × 229.6 × 158 | 53.6 mm in Y | **133 mm** |
| POD-P1 ENCLOSURE | 152 × 90 through 25 mm | POD-P1 closed, 163.0 × 143.0 × 62.0 | 11.0 mm in X, 53.0 mm in Y | **37 mm** |
| HEADPHONES | 108 × 106 through 25 mm | ATH-M20x folded, about 175 × 155 × 80 | about 67 mm in X, 49 mm in Y | **55 mm** |
| CASE LID CARD | 316 × 46 through 25 mm | A5 laminated card, 210 × 148 | 102 mm in Y | none; pocket deleted |
| QUICK-START CARD | 150 × 62 through 25 mm | A5 laminated card, 210 × 148 | 60 mm in X, 86 mm in Y | none; pocket deleted |

The remaining Rev B pockets -- EAR CLIPS + EMG LEADS, CABLES + CHARGER, CONSUMABLES,
BOOM MICROPHONE, SPARE CUPS + KEYLESS SPARES and SPARE CELL -- **cannot be checked at all**,
because the coiled electrode set, the consumables pouch, the charger body and the boom arm
are not dimensioned anywhere in package v2. Rev C dimensions them at the trial pack. Not
being able to check a pocket is not the same as the pocket being right.

**How the helmet is actually held.** The helmet cannot be held by a pocket. HM-01 stands
158 mm tall, travels assembled and upright, and must be supported **at the halo** with
nothing bearing on the electrode cups, which is the point of the whole v2 helmet design.
Two 25 mm sheets give 50 mm of foam in total, so even stacking both layers is 108 mm short.
CASE-00 Rev C therefore stops being a two-sheet insert and becomes a **stack of seven
loose-laid 25 mm PE layers, 175 mm deep**, cut to the Rev C schedule of section 2.2 so
that:

* the helmet bay is a **well through the whole stack**, open to the case floor, with an
  opening of at least 197 × 236 mm in the layers below the top one;
* the **top layer of the helmet bay is cut about 8 mm smaller all round** than the layers
  beneath it, forming a shelf. The halo rim of HM-01 lands on that shelf and the cups hang
  free in the void beneath, touching nothing. The shelf is the only load path;
* the helmet therefore stands proud of the foam by however much of it sits above the halo
  rim. That figure comes off the first printed HM-01, not off a drawing. The 15 mm
  convoluted lid foam closes on the halo and provides the retaining force;
* the pod, headphone, electrode, boom, cable, charger, consumable and spare bays are cut
  through as many layers as their item is deep, with the first uncut layer beneath forming
  the floor of each and a plain PE packer making up the difference between the item and the
  25 mm granularity of the stack. The pod bay is 169 × 149 mm and 65 mm deep over a 10 mm
  packer; the headphone bay 181 × 161 mm and 83 mm deep over a 17 mm packer;
* every bay is at least 3 mm larger than its part on every axis, with 8 mm of foam between
  bays and 14 mm to the sheet edge.

**The depth budget, in one line.** 175 mm of foam stack, plus however much of HM-01 stands
above the shelf, plus 15 mm of convoluted lid foam, must fit inside the 229 mm of internal
depth the settled shell of section 3.2 publishes. That leaves 39 mm for the helmet to stand
proud before the lid foam is compressed at all, and convoluted foam compresses by about half
its thickness, so the working allowance is about 45 mm. Whether the halo rim of HM-01 sits
within 45 mm of the top of the frame is measured off the first printed frame and is the
single measurement that decides whether this stack closes.

**The Rev B sheet footprint is dead too, and not by a small margin.** The helmet bay alone
needs 197 × 236 mm. On a 340 × 250 mm sheet that leaves a strip 143 mm wide, and the pod bay
needs 169 mm of it. CASE-00 Rev B cannot hold this kit at any depth, in any arrangement. The
nine Rev C bays add up to 154,592 mm² of opening before a single web or edge margin is
drawn, which is more than the whole 340 × 250 mm sheet. Laid out on the rules above they
occupy **516 × 390 mm**, and that is the figure the case requirement of section 3.2 is
written from. The "about 420 × 350 mm" carried by the first issue of this revision was an
estimate rather than a layout, it was smaller than the bay openings it was meant to hold,
and it is withdrawn.

**CN-PKG-02**, entered in the ECO-EEG-016 register: CASE-00 goes to Rev C before any kit is
packed. The Rev C schedule is dimensioned in section 2.2 and no longer waits on the case
decision, because section 3.2 settles the case, and at this issue the seven Rev C cut files
are drawn to it. What still waits is the **cut**: the sheet is drawn to a case internal
dimension nobody has measured, six of the nine bays hold parts that are not dimensioned
anywhere in the package, and every packer is cut at the trial pack. Rev C is confirmed
against a physical trial pack with the first printed HM-01 and the first bought shell, not
against a drawing, because nothing here has been printed or bought. It must satisfy, in
order: the helmet stands assembled and upright on the halo with nothing bearing on the cups
(DSN-EEG-002 Rev E section 11); the foam stack plus the 158 mm helmet plus the lid foam is
inside the case internal depth, on the budget above; and every bay meets the clearance rule
above. The two card slots are deleted and the cards live in the lid. The parts decide the
case, not the other way round. Owner: programme mechanical. Gate: the trial pack is a
Phase 1 acceptance item, signed by the programme before Phase 2 is released.

---

## 3. Travel case

### 3.1 The sizes in the earlier documents, reconciled

RFQ-EEG-001 Rev C M-05 said internal approximately 300 × 220 × 110 mm, Nanuk 910 / Peli
1400 class. Kit BOM Rev B item 34 said approximately 340 × 250 × 210 mm, Nanuk 915 / Peli
1450, which agrees with the Rev B foam sheet. RFQ-EEG-001 Rev E M-05 carries the larger of
the two. AVL-EEG-017 Rev B K21 restates it no longer: at this issue K21 cites section 3.2
for the envelope, names the same shell this section names and states the same measurement
rule, so the fourth figure that was in circulation -- K21's "internal ≥ 340 × 250 × 210 mm
(M-05)" -- is withdrawn. **The three that remain are all too small**, and section 2.4 is
why: the bay schedule needs 516 × 390 mm of internal footprint and at least 185 mm of
internal depth in the base.

The helmet decides it. HM-01 is 191.1 × 229.6 × 158 mm and travels **assembled and
upright, supported at the halo**: the participant never assembles an instrument at home. A
110 mm deep case cannot take a 158 mm tall helmet in any orientation that keeps the cups off
the foam, and a 340 × 250 mm case cannot take the helmet bay and the pod bay side by side.

**CN-PKG-03**, entered in the ECO-EEG-016 register: RFQ-EEG-001 M-05's "internal size
approximately 340 × 250 × 210 mm" is superseded by the requirement in section 3.2 and must
be corrected at the next RFQ revision, and AVL-EEG-017 K21 must cite section 3.2 rather than
restate M-05. Until those revisions are issued, **M-05 as written and this document
disagree, and this document governs on the geometry** because the bay schedule is derived
from part dimensions and M-05's figure is not.

The named example models are a second problem. **Nanuk 915 and Peli 1450 are about 155 mm
deep internally**, so the kit BOM's own example models fail its own dimension. Both are
withdrawn.

### 3.2 The internal envelope, settled

**This section is the single home of the travel-case internal dimensions.** AVL-EEG-017
Rev B K21 and PARTS-EEG-019 Rev B CASE-01 cite it; RFQ-EEG-001 M-05 is corrected to it at
the next revision under CN-PKG-03. One shell, one transcription, one set of numbers, so that
the foam file of section 2.2 and the carton of section 6 can both be drawn from the same
figures instead of from two.

Two transcriptions of the same shell were in circulation. Earlier issues of this document
quoted the Peli 1560 as approximately 508 × 330 × 198 mm internal; AVL-EEG-017 K21 quotes
**518 × 392 × 229 mm**. Both are the manufacturer's published figures copied by hand and the
difference is not resolvable from paper. **AVL-EEG-017 K21's figures are adopted and this
document's 508 × 330 × 198 mm is withdrawn as a mis-transcription**, so that the package
carries one number for one shell. They remain published-and-unverified: the first shell
received is measured, in the base and in the lid separately, before a single sheet of foam
is cut.

| Requirement | Value | Verification | Sign-off |
|---|---|---|---|
| Usable internal footprint, lid closed | **≥ 516 × 390 mm**, derived bay by bay from the CASE-00 Rev C schedule of section 2.2. **Larger than RFQ M-05, see CN-PKG-03** | Measure the first shell received, before any foam is cut. The seven cut files are drawn to the published figure and are not released for cutting until that measurement is in | Programme mechanical |
| Usable internal depth | **≥ 210 mm in total, of which ≥ 185 mm in the base**, so the 175 mm foam stack stands in the base and the helmet stands proud into the lid volume on the depth budget of section 2.4 | Measure the base and the lid separately at goods-in | Programme mechanical |
| Ingress | IP67, watertight and dust-tight, gasketed lid (M-05) | Supplier datasheet filed at IQC; 30 min immersion at 1 m on one Phase 1 shell | QA |
| Pressure equalisation | Automatic valve, hydrophobic membrane, so the case opens after air freight | Present and unobstructed; **no label may cover it** | Packer, at every despatch |
| Latches | At least two lockable hasps accepting a 5 mm shackle | Visual, and one open/close cycle at goods-in | Packer |
| Handle | Integral moulded, no wheels -- the case must sit inside a carton. The settled shell is a large-format case offered in wheeled and unwheeled variants; **the purchase order must name the unwheeled variant** | Visual | QA |
| Temperature | −20 to +50 °C operating | Supplier datasheet | QA |
| Lid | Retains the A4 document wallet holding **all five printed items** -- quick-start card, placement guide, full IFU, calibration certificate and packing photograph (section 1.1 lines 6.1 to 6.5) -- without foam. The wallet is the only place paper travels: Rev C cuts no card bay | Trial pack, with the five items in the wallet and the lid closed | QA |
| Empty mass | **The ≤ 4.0 kg target of Rev A is not met and is withdrawn.** No shell that meets the envelope above is a 4.0 kg case; the settled shell's published empty mass without foam is about 5.1 kg. Chargeable weight is set by carton volume, not by mass (section 6), so the target bought nothing it claimed to buy. The requirement that replaces it: the lightest shell that meets the envelope, with its **measured** empty mass recorded | Weigh the first shell | Programme |

**The shell.** The **Peli 1560** is the baseline, at a published internal
518 × 392 × 229 mm. It meets the footprint with 2 mm to spare on each plan axis and the
total depth with 19 mm to spare. Two things about it are measured rather than read. Peli
publishes one interior depth and does not split base from lid, so the ≥ 185 mm base figure
is the one number that can still sink this shell. And 2 mm of plan margin is inside the
tolerance of a moulded case, so a shell that measures short does not make the cut file
tight, it makes it scrap. Both are why the shell is measured before the foam is ordered and
not after. The seven Rev C cut files of section 2.2 exist and they are **not released for
cutting**: their sheet is 516.0 × 390.0 mm because the published internal footprint is
518 × 392 mm, and the sheet is re-drawn to the **measured** footprint minus 2 mm on each
axis before a sheet of foam is bought or cut.

AVL-EEG-017 Rev B K21 agrees with this section at this issue. It names the Peli 1560,
unwheeled, as the baseline; it quotes the same published 518 × 392 × 229 mm; it carries the
Nanuk 960 as the alternate the CASE-00 Rev C layout does not fit; and it states the
measure-before-you-cut rule rather than a fourth set of numbers. Where the two ever differ,
this section governs and K21 is corrected to it, because the bay schedule is derived from
part dimensions and a vendor list is a transcription.

**The alternate.** AVL-EEG-017 K21 names a Nanuk **960** at a published internal
552 × 358 × 226 mm. It clears the depth, but it is 32 mm short of the 390 mm second axis, so
**the CASE-00 Rev C bay layout does not fit it as drawn.** It stays the alternate shell, and
choosing it means re-columning the boom, spare-cup, spare-cell and cable bays onto a
550 × 356 mm sheet, which is a Rev D of CASE-00 and is not drawn. The Nanuk 945 and the
Peli 1600 named in earlier issues of this section are withdrawn: neither appears in
AVL-EEG-017, and the package carries one approved vendor list.

That leaves the programme on one shell with no drawn alternate, which is recorded as open
item 10 in section 9. The model is frozen at the trial pack of section 2.4, and the chosen
shell's datasheet and its measured internal dimensions are filed in the device history
record. Whichever is chosen, CASE-00 is sheeted to the **measured** internal footprint minus
2 mm on each axis, not to the published one.

The case is part of the BOM, not packaging (M-05). It is never the shipping container
(M-07, section 6).

---

## 4. Labelling

### 4.1 Unit label -- ART-LBL-01 (RFQ M-03, E-21, TST-EEG-004 T18)

Artwork: `graphics/labels/ART-LBL-01_unit_label.svg` (the printer's file, at trim size, with
the per-unit fields drawn as `<<PLACEHOLDER>>`), `ART-LBL-01_unit_label_specimen.svg` (the
same label with a real Data Matrix, drawn for `TIOV-B-0000`) and
`ART-LBL-01_unit_label.pdf` (the control sheet a person signs). All three are generated by
`tools/artwork_gen.py` from the table below.

| Property | Value |
|---|---|
| Size | 50 × 25 mm |
| Substrate | Matt white polyester, 50 µm |
| Print | Thermal transfer, resin ribbon, black |
| Finish | Clear over-laminate, 25 µm |
| Adhesive | Permanent acrylic, service −40 to +90 °C |
| Placement, Phase 1 | POD-P1 lid outer face, on the flat 55 × 30 mm keep-out, clear of the gasket line |
| Placement, Phases 2 and 3 | HM-01 occipital shell rear face |
| Duplicate | One identical label inside the case lid |
| Durability | Legible, adherent and Data-Matrix-readable after 50 wipes with 70 % IPA and after 20 simulated round trips |

Content, in this order:

1. `TIOV-B-0001` -- unit serial, section 5, 10 pt minimum
2. `HW EEG-CAR-01-B` -- hardware revision. The revision letter here and the letter in the
   serial are the same letter and must agree
3. `FP 9F2C 4108 BB37 1D0A` -- ATECC608B public-key fingerprint, 16 uppercase hex in four
   groups (the example is illustrative)
4. ECC200 Data Matrix, 12 × 12 mm, quiet zone 2 modules
5. `RESEARCH INSTRUMENT -- NOT A MEDICAL DEVICE`
6. `Do not wear while charging` (RFQ S-01)
7. `Contains Li-ion cell -- do not incinerate`
8. `one.witysk.org` · `CC BY-SA 4.0`

Data Matrix content, pipe-delimited, no spaces:
`TIOV-B-0001|EEG-CAR-01-B|<18 hex ATECC factory serial>|<16 hex fingerprint>`

The fingerprint is defined once, in **FW-EEG-001 Rev C section 7**, and this document does
not restate the derivation. ASM-EEG-007 Rev B section 6.2, QP-EEG-010 Rev B,
TST-EEG-004 Rev C T6 and REG-EEG-012 Rev B cite the same definition, and all of them must
return the same string for the same unit. The **serial** is the other way round: FW-EEG-001
section 7 does not define it, section 5 of this document does.

Verification: at T18 the operator scans the Data Matrix and compares it field by field
with the provisioning record and with the USB `iSerialNumber` read at T5b. A mismatch
quarantines both the unit and the label. Barcode quality ISO/IEC 15415 grade C or better
after the IPA test. Sign-off: production QA, countersigned by the programme on the two
kits sampled per batch (QP-EEG-010 A-13).

### 4.2 Case, carton and cable labels

| Ref | Label | Size | Substrate | Placement |
|---|---|---|---|---|
| ART-LBL-02 | Kit ID plate: `KIT-007` in 24 pt, Code-128 of the kit id, unit serial beneath, "TI One Voice research kit -- property of TI One Voice vzw, Brussels" | 80 × 40 mm | Outdoor white polyester, permanent | Case lid exterior, upper left |
| ART-LBL-03 | Return address and if-found, EN/FR/NL, Brussels address, programme telephone, "Contains no personal data" | 100 × 60 mm | Outdoor white polyester, permanent | Case base exterior |
| ART-LBL-04 | Foam bay tags, one per bay, legend text identical to the section 2.2 schedule | 60 × 12 mm | Matt polyester, permanent | Bay rear wall at mid-depth, or the top face beside a deep well (section 2.3) |
| ART-LBL-05 | Carton marking set: FRAGILE -- RESEARCH INSTRUMENT, THIS WAY UP, gross mass, kit id | printed on the carton | — | Two opposing long faces |
| ART-LBL-06 | Lithium battery mark, UN 3481, telephone number | 120 × 110 mm, reduced 105 × 74 mm where the face is too small | White polyester | Outer carton, one side face |
| ART-LBL-07 | Numbered tamper seal | 90 × 20 mm | Void-evident, removable | Across each case hasp |

No label may cover the pressure-equalisation valve. Sign-off on placement: packer, checked
by QA against the placement drawing DRW-LBL-PLACEMENT, which is
`graphics/labels/DRW-LBL-PLACEMENT_label_placement.svg` and its A3 control sheet
`DRW-LBL-PLACEMENT_label_placement.pdf`. It carries four views -- the POD-P1 lid, the case
lid, the case base and one long face of the outer carton -- with every label drawn at its
size from this table and dimensioned from the two nearest edges. **The faces and the sizes
are this section's and are fixed; the positions on those faces are the drawing's and are a
proposal**, because no shell has been measured (section 9 open item 2) and the carton is
sized from a published figure (section 6). Dimensioning from the edges is what lets a
measured shell change the numbers without changing the arrangement. The valve is a written
constraint on that sheet and not a drawn keep-out, because its position on the bought shell
is not known.

**The SPARE CELL bay tag is specified twice and the two do not agree.** This table says the
ART-LBL-04 legends are "identical to the section 2.2 schedule", which makes the tag read
`SPARE CELL`; section 7 says the tag reads `SPARE CELL -- DEPOT ONLY, EMPTY IN CIRCULATION`.
The generated tag carries the section 7 string, because it is the one that tells a packer
why the bay is empty, and the collision is open item 16 of section 9.

Cables carry printed heat-shrink sleeves at both ends, 25 mm long, white on black, applied
before the connector is terminated (WH-EEG-008):

| ID | Cable | Sleeve text |
|---|---|---|
| CBL-01 | Electrode cable, 12-way screened, helmet to J14 | `CBL-01 ELECTRODE J14` + unit serial |
| CBL-02 | Light cable, 10-way, helmet to J30 | `CBL-02 LIGHTS J30` + unit serial |
| CBL-03 | EMG lead 1, red | `EMG1 CHEEK` |
| CBL-04 | EMG lead 2, yellow | `EMG2 CHIN` |
| CBL-05 | EMG lead 3, green | `EMG3 NECK` |
| CBL-06 | USB-C to USB-A, 1.0 m | `CBL-06 USB-C / USB-A 1.0 m` |
| CBL-07 | USB-C to USB-C, 1.0 m | `CBL-07 USB-C / USB-C 1.0 m` |
| CBL-08 | Boom microphone pigtail to J18 | `CBL-08 BOOM J18` |

The two USB cables are not function-coded, because either can serve either port. The
**ports** carry the legends instead, on the pod panel: `DATA (isolated)` at the host
aperture and `CHARGE ONLY` at J24. The host aperture is a gasketed opening over the
isolator module's own connector, not a gland and not a captive lead. On the only named
isolator module that connector is USB-B where RFQ E-24 asks for USB-C, so the WH-09 pigtail
of packing-list line 1.17 presents USB-C at the panel; that is an interim answer to a live
non-conformance, not a settled design. The EMG colour code is carried through from the lead
sleeve to the panel legend beside J15/J16/J17 so a participant matches by colour alone.

### 4.3 The artwork files

ECO-EEG-016 Rev B section 1 registers ART-LBL-01 to ART-LBL-07, ART-PACK-01, ART-DIS-01,
ART-RET-01 and DRW-LBL-PLACEMENT as "artwork files controlled as generated artifacts under
`graphics/`" owned by this document. Until 2 September 2026 none of them existed: the
register named eleven files, section 1.1 ticked against three of them, section 4.2 made the
QA placement check a check against a drawing that was not in the package, and the nine bay
tags could not be ordered, only re-typed. They are now generated, into `graphics/labels/`.

They carry **no revision letter of their own**, only Rev B of this document, which is what
ECO-EEG-016 requires. Two files per identifier: a `.svg` at exact trim size with all text
converted to outlines, which is the file a printer is given and which has no font to
substitute, and a `.pdf` control sheet with the title block, the artwork at 1:1 inside trim
marks, the variable-data table and the notes, which is the file a person reads and signs.
`graphics/labels/README_artwork.txt` lists every file with its SHA-256.

| Identifier | File stem in `graphics/labels/` | Source of its content |
|---|---|---|
| ART-LBL-01 | `ART-LBL-01_unit_label`, and `_unit_label_specimen` | Section 4.1 |
| ART-LBL-02 | `ART-LBL-02_kit_id_plate`, and `_kit_id_plate_specimen` | Section 4.2 |
| ART-LBL-03 | `ART-LBL-03_return_and_if_found` | Section 4.2 |
| ART-LBL-04 | `ART-LBL-04_bay_tag_<legend>`, nine files | Section 2.2 Rev C schedule, and section 7 for the spare-cell tag |
| ART-LBL-05 | `ART-LBL-05_carton_marking_set` | Sections 4.2 and 6 |
| ART-LBL-06 | `ART-LBL-06_lithium_battery_mark`, and `_reduced` | REG-EEG-012 Rev B section 3.5 |
| ART-LBL-07 | `ART-LBL-07_tamper_seal` | Section 4.2 |
| ART-PACK-01 | `ART-PACK-01_packing_layout_provisional` | Section 2.2 schedule and section 1.1 pocket column |
| ART-DIS-01 | `ART-DIS-01_disinfection_guide_card` | SVC-EEG-013 Rev B section 2 R5, which section 9 of that document names as this card's source |
| ART-RET-01 | `ART-RET-01_return_shipping_instructions` | Section 7, block quote |
| DRW-LBL-PLACEMENT | `DRW-LBL-PLACEMENT_label_placement` | Sections 4.1, 4.2, 3.2 and 6 |

Nothing in that table was typed into the generator. Every legend, size, substrate, placement
and piece of body copy is read out of this document's own Markdown -- or out of REG-EEG-012
and SVC-EEG-013 where those own the content -- at generation time. Correct a legend here and
re-run `python3 tools/artwork_gen.py`, and the tag follows; the artwork cannot drift from the
document that owns it, which is the property section 2.3 claimed and had no mechanism to
hold.

**Four of the eleven cannot go to a printer as they stand, and say so on their own control
sheet.** ART-LBL-03, ART-LBL-05, ART-LBL-06 and ART-RET-01 carry `<<PLACEHOLDER>>` fields
for the programme's postal address, its telephone number and its email address, none of
which appears anywhere in package v2.3. The generator does not invent them: a wrong address
on a case base is a kit that does not come back, and a dead telephone number on a regulated
dangerous-goods mark is a parcel refused at a counter with a participant standing at it.
ART-LBL-06 is incomplete for a second reason, in open item 14.

**Two barcodes are encoded rather than pasted in.** The ART-LBL-01 Data Matrix is a real
ECC200 symbol -- a 32 x 32 module symbol in the 12 x 12 mm this document specifies, so a
0.375 mm module, about 4.4 dots at 300 dpi -- and the ART-LBL-02 kit id is real Code 128
subset B. Both encoders carry a self-test, run every time the artwork is generated:
`python3 tools/artwork_gen.py --selftest` checks the Data Matrix against the ISO/IEC 16022
worked example and by decoding its own symbols, and checks the Code 128 pattern table
structurally. **That proves the encoder, not a printed label.** Section 4.1 already requires
ISO/IEC 15415 grade C or better after fifty wipes with 70 % IPA, and that first-article
verification is what releases this artwork for use. Nothing here has been printed, applied,
wiped or read by a verifier.

---

## 5. Serial number scheme

**This section is the single home of the `TIOV-B-nnnn` serial format.** It is defined here
and nowhere else. FW-EEG-001 Rev C, WH-EEG-008 Rev B, ASM-EEG-007 Rev B, QP-EEG-010 Rev B,
TST-EEG-004 Rev C, IFU-EEG-014 Rev B, PARTS-EEG-019 Rev B and RFQ-EEG-001 Rev E F-04 and
M-03 all use the format and all **cite** this section for it rather than restating it.

Three other homes have been claimed for it and none of them is one. **FW-EEG-001 section 7
defines the public-key fingerprint, not the serial**, so a document citing FW-EEG-001
section 7 for the serial format has the wrong section of the wrong document.
**PARTS-EEG-019 section 4.2 registers the three identifiers a unit carries** -- the
programme serial, the ATECC608B factory serial and the fingerprint -- and cites this section
for the format of the first of them; it settles which identifiers exist, not how the serial
is written. **RUL-EEG-021 Rev A section B** records the ruling that fixed the format; it is
the minute of the decision, and this section is the specification the ruling asked for.

Format, fixed by this document:

```
TIOV-B-nnnn                 example  TIOV-B-0001
 │    │  └── unit number, four digits, allocated in phase blocks
 │    └───── hardware revision letter of the carrier (EEG-CAR-01 Rev B)
 └────────── programme prefix
```

| Range | Reserved for |
|---|---|
| TIOV-B-0001 … 0009 | Phase 1. TIOV-B-0001 is the golden unit and is re-measured at every phase |
| TIOV-B-0010 … 0099 | Phase 2 |
| TIOV-B-0100 … 0999 | Phase 3 |

Rebuilds take the next free number in their own phase block; there is no separate rebuild
range. When the carrier goes to Rev C the revision letter in the serial changes with it, so
a serial states which hardware it names without a lookup.

**What was withdrawn, and why.** Revision A of this document specified
`OV-EEG-<p><nnn><C>` with a modulo-23 check character. That scheme is withdrawn entirely.
Five forms were in circulation across the package -- `OV-EEG-1001P` here,
`OV-EEG-<phase><nnn>` in ASM-EEG-007, `TIOV-EEG-<phase>-<nnn>` in QP-EEG-010,
`TIOV-EEG-0007` in WH-EEG-008 and `TIOV-B-0007` in FW-EEG-001 -- and the same string has to
appear on the label, in the Data Matrix, in the USB `iSerialNumber`, in the calibration
record and on this packing list. A check character that only one of six documents knows
about is worse than no check character, and the firmware already writes `TIOV-B-nnnn` into
the descriptor. One form, everywhere, wins. **CN-PKG-01** in the ECO-EEG-016 register
records the withdrawal and requires ASM-EEG-007, QP-EEG-010, WH-EEG-008, TST-EEG-004 and
JIG-EEG-009 to carry `TIOV-B-nnnn` at their next revision, including the golden unit, which
is `TIOV-B-0001` and not `SN0001` or `TIOV-EEG-1-001`.

**Proposed, and not yet ruled: `TIOV-B-0000` is reserved for artwork specimens.** The
blocks above allocate 0001 to 0009, 0010 to 0099 and 0100 to 0999, so 0000 is in none of
them. The specimen unit label of section 4.3 is drawn for `TIOV-B-0000` precisely because of
that: a specimen printed by accident, or a proof left on a bench, cannot be mistaken for the
label of a unit that exists. Reserving it costs nothing and closes a hole that a specimen
drawn for `TIOV-B-0001` -- the golden unit -- would open. The programme owns the decision;
it is open item 18 of section 9 until it is taken.

Serials are allocated by the programme in blocks and issued with the purchase order. A
manufacturer never invents one. A unit that is re-boarded keeps its serial only if the
ATECC608B moves with it; a new secure element means a new serial from the same phase block
and a new device history record cross-referenced to the old one.

**Three identifiers, one binding.** The programme serial `TIOV-B-nnnn` above is printed,
human-read, **and is what the firmware writes into the USB `iSerialNumber`** (RFQ F-04, and
RUL-EEG-021 section B rules it). It is therefore what the browser's persistent WebUSB
authorisation binds to. The ATECC608B's own 9-byte factory serial, rendered as 18 uppercase
hex characters, is a *second* identifier: it is printed and carried in the Data Matrix so a
swapped secure element can be detected, and it is **not** the descriptor string. The fingerprint of section 4.1 is derived from the
provisioned public key. All three are printed on the label, encoded in the Data Matrix,
written into the calibration record at T5b and T6 and filed in the device history record. If
any two disagree the unit is quarantined.

**Kit id versus unit serial.** `KIT-<nnn>` identifies the circulating asset -- case, foam,
helmet, consumables -- and is printed on ART-LBL-02. The unit serial identifies the
electronics. They are recorded as a pair at despatch and may be re-paired at refurbishment,
for example when a helmet frame is withdrawn and the pod moves to a new frame. The pairing
history lives in the device history record (QP-EEG-010).

---

## 6. Outer shipping carton

The travel case is **never** the shipping container (RFQ M-07). A case used as a parcel
arrives scuffed, its latches sprung and its labels abraded, and it is a BOM item that has
to survive twenty round trips.

| Property | Value |
|---|---|
| Board | Double-wall BC flute, kraft |
| Strength | Box compression ≥ 7.0 kN; edge crush ≥ 1.9 kN/m |
| Internal size | Case external plus 40 mm on every face. **640 × 535 × 345 mm** against the Peli 1560's published external of about 560 × 455 × 265 mm. Published, not measured: the carton is not ordered until the shell has been measured (section 3.2) |
| Void fill | Eight 40 mm PE foam corner blocks, 28 to 33 kg/m³. No loose fill -- the case is smooth and slides |
| Closure | H-taped, 50 mm PP tape, plus one numbered security seal |
| Uses | Two: out and back. The participant re-uses the same carton and the same corner blocks |
| Label pocket | Transparent adhesive document wallet, 225 × 165 mm, on one long face, holding the pre-paid return label, the return instruction sheet and any customs paperwork (M-07) |
| Marking | ART-LBL-05 and ART-LBL-06 (section 4.2) |
| Spares | Two spare cartons and two spare label sets per ten kits, so a crushed carton does not strand a kit in a participant's home |

**Calculated masses.** Nothing has been weighed. These figures are recalculated for the
150 × 130 mm four-layer carrier, the enlarged POD-P1 and the Rev C foam stack.

| Item | Calculated mass | Basis |
|---|---|---|
| Helmet assembly (HM-01 240 g plus fitted parts) | 500 g | Print volume × 1.01 g/cm³ |
| Pod assembly: POD-P1 base and lid 279 g, carrier 104 g, MP-01 48 g, thirteen module assemblies 130 g, cell 48 g, standoffs, screws and jumpers 37 g | **650 g** | Was 520 g in Rev A. The enclosure and the four-layer carrier account for the difference |
| Headphones | 240 g | Published |
| Cables and charger | 150 g | Published |
| Electrodes, ear clips, EMG leads | 90 g | Estimated |
| Consumables pouch | 450 g | Filled |
| Foam insert, Rev C stack, after cut-outs, plus the lid pad | **about 600 g** | 516 × 390 × 175 mm is 35.2 litres of PE at 30 kg/m³, which is 1.06 kg solid; the openings of the seven Rev C cut files remove 15.8 litres, 45 % of it, leaving 583 g, and the 15 mm convoluted lid pad over the helmet bay adds about 20 g. Taken off the cut files of section 2.2 by planimeter with the corner radii included, at the nominal 30 kg/m³ of the 28 to 33 kg/m³ band, and **not weighed**. Rev A's 90 g was the two-layer sheet and is no longer relevant |
| Documents | 60 g | A4 wallet |
| **Packed contents** | **2.74 kg** | |
| Case, empty | 5.1 kg **published, not weighed** | The Peli 1560 without foam (section 3.2). The ≤ 4.0 kg target is withdrawn: no shell that meets the internal envelope is a 4.0 kg case |
| **Gross packed case** | **7.8 kg** | |
| Carton, corner blocks, tape and seal | 0.9 kg | |
| **Gross shipping mass** | **8.7 kg** | |
| Volumetric mass, 640 × 535 × 345 mm at divisor 5000 | **23.6 kg** | With the carton above |

The consignment is charged on volume, not on mass: 23.6 kg volumetric against 8.7 kg
actual. That is worth knowing before the fleet is sized. The case is the postage cost, and
settling it on a shell large enough to stand the helmet upright took the chargeable weight
from 17.4 kg to 23.6 kg, about 35 % more on every leg, out and back. The alternative was a
case the kit does not fit in.

**Drop rating, two separate tests.** RFQ M-04 is a product test: 1 m onto concrete on each
of six faces, case open and kit packed, on one Phase 1 unit, with pass defined as a re-run
of TST-EEG-004 T3, T7, T8, T10 and T14 inside their original limits plus a cell inspection.
Section 7's package test is a transport test on the sealed carton. Both are Phase 1 type
tests, reported once per phase. Sign-off: programme, before Phase 2 is released. An
ISTA 3A-equivalent transit sequence on one packed carton is run alongside them.

---

## 7. Lithium battery shipping

**This section is the single home of the lithium-shipping procedure.** REG-EEG-012 Rev B
section 3 states the obligation and cites this section; TST-EEG-004 Rev C T29 verifies at
kit closure against this section. None of the three restates the others.

Every kit contains one protected 18650 cell installed in the instrument. At 3.6 V nominal
and 3400 to 3500 mAh that is **12.24 Wh (NCR18650B) or 12.6 Wh (Samsung 35E)** --
calculated, under the 20 Wh per cell and 100 Wh per package thresholds. One cell, no
battery pack.

**The classification decision, recorded.** DSN-EEG-002 Rev E section 7 said "a charged
spare travels in the case, so a flat cell never ends a session", and CASE-00 cuts a SPARE
CELL pocket. A loose spare makes every consignment *packed with equipment* under packing
instruction PI966, with different packing, marking and quantity rules, and it puts a bare
lithium cell in a stranger's home. **The spare cell is deleted from the circulating kit.**
The kit ships as UN 3481, lithium ion batteries **contained in equipment**, PI967
section II, on every leg. This is what RFQ-EEG-001 Rev E S-09 requires. The SPARE CELL
bay stays in the foam and stays empty in circulation; it carries a spare only on
depot-to-depot moves handled by the programme's trained shipper, and its tag reads
`SPARE CELL -- DEPOT ONLY, EMPTY IN CIRCULATION`. The compensating control is RFQ E-22:
at least four hours at 1000 Hz against a two-hour session, plus the charger of A-07.

| Control | Value | Verification | Sign-off |
|---|---|---|---|
| UN number and packing instruction | UN 3481, PI967 section II | Consignment record | DG-trained shipper |
| State of charge at despatch | **≤ 30 %** | MAX17048 gauge read at the packing station through the session runner and written on the despatch record. **TST-EEG-004 has no numbered step for this read** -- T24 is the radio-silence check and the Rev A citation of it here was wrong -- and it is raised as open item 8 in section 9. **Open item 8 is the only entry the package carries for this gap**: RFQ-EEG-001 Rev E section 9.1 item 12 says the fuel-gauge reading has no per-unit step and is "raised as an open item" without naming a register, and neither RFQ-EEG-001 section 12 nor TST-EEG-004 section 16 carries one. Until one of them does, this is where the item lives | Packer |
| Cell secured | HM-10 keyed carrier behind the quarter-turn HM-08 hatch; cannot be inserted reversed (S-04) | Shake test at T18 | Packer |
| Protection against accidental activation | **The two mechanisms of RFQ S-01, and only those two**: firmware refuses `CMD_START_SESSION` while VBUS_DET is high, and CHG_CE holds the charger disabled for the whole of a session. Rev A of this document also claimed a "hatch interlock ends a session". **No hatch interlock exists anywhere in the design and that claim is deleted** | T4 and T21 | Production QA |
| Outer packaging | Strong rigid outer, the section 6 carton | Visual | Packer |
| Package drop test | 1.2 m, six orientations, on a completed package, with no cell damage, no leakage and no shifting of contents | Once per carton design, report filed | Programme |
| Lithium battery mark | ART-LBL-06 on the outer carton, with UN 3481 and a telephone number | Visual at despatch, and T29 | Packer |

The ≤ 30 % state of charge is a **programme control, not a regulatory requirement** for
UN 3481 in equipment. It is applied because it lowers the energy in a damaged package and
because S-09 requires it. Likewise, a single-kit parcel with one cell installed falls
inside the small-package relief in PI967 section II and would not strictly need the mark;
the programme applies the mark to **every** carton anyway, because a participant handing a
parcel across a counter needs the parcel to answer the counter's question for them.
Consignments of **more than two packages** exceed the relief and require the mark regardless,
which is the threshold REG-EEG-012 section 3.3's configuration table states in its own
words. That is the whole of the programme's position on the mark, and the two documents state
one rule.

**Documents held per shipment.** UN 38.3 test summary from the cell supplier, per cell lot,
obtained before the first shipment and not after (S-04); cell safety data sheet; the package
drop-test record; the consignment record; and, where the carrier requests it, the written
statement that the consignment is UN3481 in compliance with section II of PI967. That list is
owned by **REG-EEG-012 section 3.7** and this is the packer's rendering of it. The programme
puts the statement on every air waybill rather than waiting to be asked, in the words
"Lithium ion batteries contained in equipment, UN 3481, PI967 section II, not restricted".
**That wording is not prescribed by the regulations and has not been checked against the
edition in force**; it is one of the things the DG-trained shipper verifies under REG-EEG-012
section 3.3 before each phase's despatch. No shipper's declaration for dangerous goods is
required for this configuration. Sign-off: the programme's DG-trained shipper, named in the
quality plan, with a stated refresher interval.
The manufacturer answers the same question in the RFQ compliance matrix.

**What a courier will and will not accept.** Cells installed in equipment, one per parcel,
declared, are accepted on road and on most air services by bpost, DPD, GLS, UPS and DHL.
Loose cells on a consumer counter service are refused by most of them, which is a second
reason the spare is gone. Any given carrier's consumer-return terms must be confirmed **in
writing** before a return label is bought, and the confirmation filed. One primary and one
alternate carrier are named per phase in the logistics file.

**The return leg.** The participant is legally the shipper and cannot discharge a shipper's
obligation. The programme therefore does the work in advance: a pre-paid, pre-classified
return label on a lithium-approved service is printed at despatch and travels in the
carton's document pocket, together with a printed sheet the participant can hand over. The
participant never writes a shipping document, never opens the pod and never handles a cell.
The instruction sheet ART-RET-01 reads, in substance:

> Repack the case to the photograph inside the lid, close both latches, put the case back
> in the same carton with the four foam blocks, tape it shut, and stick on the pre-paid
> label from the clear pocket. The label is already correct for the battery inside the
> instrument. If the counter asks what is inside, say: *a research instrument with a small
> rechargeable battery fitted inside it, UN 3481, already declared on the label.* Do not
> open the instrument, do not remove any battery, and do not post it in a letterbox -- hand
> it over at a counter or book a collection. If the carton is damaged, telephone us and we
> will send another; do not use a different box.

Cells are stored at the depot at 40 to 60 % state of charge, never on charge unattended, in
a metal-free box. A swollen, dropped or deep-discharged cell is quarantined against the kit
id and replaced from spares, never shipped. End-of-life cells go to the Belgian collection
scheme.

---

## 8. Despatch and receipt records

One record per leg, held against the kit id and the unit serial, in the device history
record (QP-EEG-010).

**Despatch record** -- completed by the packer, countersigned by a checker, before the
carton is sealed:

| Field | Source |
|---|---|
| Kit id, unit serial `TIOV-B-nnnn`, ATECC serial, fingerprint | Label and calibration record |
| KPL-EEG-001 ticked, both signatures | Section 1 |
| Cell lot and state of charge at despatch | Gauge read, ≤ 30 % |
| Case seal numbers, both hasps | ART-LBL-07 |
| Carton security seal number | Section 6 |
| Firmware version and image SHA-256 | Provisioning record |
| Consumables lot numbers and expiry dates | Pouch |
| Gross shipping mass, measured | Scale |
| Carrier, service, tracking number, declared value, insured yes/no | Booking |
| Outbound label and return label tracking numbers | Booking |
| Lithium mark applied, document set present | TST-EEG-004 T29 |
| Destination reference, not the participant's name | Study register |
| Packer, checker, date | Signature |

**Receipt record** -- completed at goods-in in Brussels, before the kit is opened for
refurbishment:

| Field | Check |
|---|---|
| Carton condition, crush or wet damage | Photograph if damaged |
| Carton seal number matches despatch | Yes / no |
| Case seal numbers match despatch | Yes / no. A broken seal means the case was opened in transit; quarantine |
| Photograph of the open case against the packing photograph | Filed |
| KPL-EEG-001 return column ticked | Every line |
| Missing or damaged items, with line numbers | Listed |
| Cell state of charge and gauge-reported capacity on return | Recorded |
| Quarantine 24 h before handling | Initialled |
| Reduced re-test result after refurbishment (SVC-EEG-013) | Values recorded |
| Deposit release authorised | Signature |

A kit is not released back into circulation until the receipt record, the refurbishment
record and the reduced re-test all carry a signature. Records are retained for the life of
the programme plus five years, held by the programme, with a copy of the per-unit build and
calibration record supplied by the manufacturer as a condition of acceptance under
RFQ-EEG-001 Rev E section 9.3.

---

## 9. Open items in this document

| # | Item | Gate |
|---|---|---|
| 1 | The CASE-00 Rev C **cut files are drawn** -- seven layer files, listed in section 2.2 -- and **nothing has been cut from them**. Six of the nine bays hold parts that are not dimensioned anywhere in the package, so their plan sizes and every packer are provisional until the trial pack, and the sheet is drawn to a published case dimension rather than a measured one. Phase 1 packs in pluck foam | Blocks Phase 2 kitting |
| 2 | No travel case has been bought, measured or weighed. Section 3.2 settles the internal figures on AVL-EEG-017 K21's transcription of the Peli 1560, and the foam sheet is drawn to it with only 2 mm of margin on each plan axis, so a shell that measures short makes the cut files scrap. The base-to-lid depth split is not published and the ≥ 185 mm base figure is unverified | Blocks the foam **cut**, the carton order and the freight quote. The cut files themselves are drawn |
| 3 | RFQ-EEG-001 M-05's approximately 340 × 250 × 210 mm internal is smaller than the 516 × 390 × 210 mm requirement of section 3.2 derived from the bay schedule, and it is no longer restated anywhere else: AVL-EEG-017 K21 now cites section 3.2, so half of CN-PKG-03 is closed and **RFQ-EEG-001 has still to be corrected at its next revision** | Blocks a clean acceptance against M-05 |
| 4 | Every mass, the volumetric mass and the carton size are calculated from geometry, published shell figures and assumed densities. Nothing has been weighed. The foam mass is now calculated bay by bay from the section 2.2 schedule rather than estimated, which makes it precise and still not measured | Closed by the first packed kit |
| 5 | The UN 38.3 test summary has not been obtained from a cell supplier, because no cell has been bought | Blocks the first shipment, not the build |
| 6 | Carrier consumer-return terms for UN 3481 have not been confirmed in writing with any carrier | Blocks the first participant despatch |
| 7 | The packing photograph does not exist; a rendered provisional stands in | Closed at first build |
| 8 | The state-of-charge read at despatch has no numbered step in TST-EEG-004. It is performed at the packing station and recorded, but it is not a test step, and this document does not number one for it. **This row is also the register entry for the wider gap**: RFQ-EEG-001 Rev E section 9.1 item 12 states that the MAX17048 fuel gauge has no per-unit step and is "raised as an open item", and no such item exists in RFQ-EEG-001 section 12 or in TST-EEG-004 section 16, so the reference points nowhere and this row is what it should point at | Closed when TST-EEG-004 adds a step or accepts the packing-station record as the evidence. The dangling reference is closed by RFQ-EEG-001 at its next revision |
| 9 | The host connector is a live non-conformance against RFQ E-24: the only named isolator module presents USB-B and the WH-09 pigtail is an interim answer. WH-09 is not yet in the PARTS-EEG-019 register | Blocks the panel aperture drawing and the Phase 2 module order |
| 10 | The settled shell has no drawn alternate. The Nanuk 960 of AVL-EEG-017 K21 clears the depth but is 32 mm short of the 390 mm second axis, so the CASE-00 Rev C bay layout does not fit it; using it means a Rev D of the cut file. A single-source case is a supply risk on a five-year programme | Closed by a second shell being laid out, or accepted as a risk by the programme |
| 11 | The ≤ 4.0 kg empty-case target of Rev A is withdrawn in section 3.2 because no shell that meets the internal envelope meets it. That is a requirement relaxed to fit the parts, and RFQ M-05 carries no empty-mass figure to correct it against | Closed when M-05 is revised under CN-PKG-03 |
| 12 | **The finger reliefs of the Rev C schedule remove no foam.** Every relief centre in the section 2.2 table sits at least 3 mm inside its own bay opening, so the ⌀22 mm circle falls within material the bay profile already removes; the cut files draw them there rather than differ from the schedule. They cannot be moved outwards -- a straddling relief needs 11 mm beyond the bay wall and every web is 8 mm -- so the fix is a scallop in the first uncut layer beneath each bay, or a re-columned sheet, and both are a Rev D | Decided at the trial pack, with the six undimensioned bays |
| 13 | **Four of the eleven artwork files cannot be printed.** ART-LBL-03, ART-LBL-05, ART-LBL-06 and ART-RET-01 carry `<<PLACEHOLDER>>` fields for the programme's postal address, telephone number and email address. None of the three appears anywhere in package v2.3, and the generator will not invent them. The files are drawn, dimensioned and complete apart from those fields | Programme lead, before the first label order. Blocks ART-LBL-03, ART-LBL-05, ART-LBL-06 and ART-RET-01 only |
| 14 | **ART-LBL-06 is incomplete by design: the regulated pictogram is not supplied.** The outer size, the reduced size, the hatched border, the UN3481 text and the telephone field are drawn to the figures REG-EEG-012 Rev B section 3.5 states. The battery-group-and-flame symbol belongs to the edition of ADR / IATA DGR in force, this package does not hold it, and a drawn-from-memory symbol is a mark that gets refused at a counter -- which happens to a participant, not to the programme | The programme's DG-trained shipper, per REG-EEG-012 section 3.7, before the first despatch |
| 15 | **The 60 x 12 mm bay tag cannot carry an 8 mm cap height, and this is measured.** Section 4.2 fixes the tag and section 2.3 asks for the cap height; not one of the nine legends fits on one line, the least demanding needing about 88 mm of tag and the worst 320 mm. The generated tags are set between 5.36 and 2.68 mm on the specified tag. About **171 x 21 mm** carries every legend at 8 mm on at most two lines | Programme, with the trial pack of open item 1. Changing the tag changes section 4.2 and section 2.3 together |
| 16 | **The spare-cell bay tag is specified twice and the two disagree.** Section 4.2 makes the ART-LBL-04 legends identical to the section 2.2 schedule, which reads `SPARE CELL`; section 7 makes this one tag read `SPARE CELL -- DEPOT ONLY, EMPTY IN CIRCULATION`. The generated tag carries the section 7 string. One of the two sections has to change | Programme. Closed when this document is next re-issued |
| 17 | **DRW-LBL-PLACEMENT's positions are a proposal, not a measurement.** The faces and the label sizes are section 4.2's and are fixed; where each label sits on its face is the drawing's, against a case whose external dimensions are published rather than measured (open item 2) and a carton sized from those. Positions are dimensioned from the two nearest edges so that a measured shell changes the numbers and not the arrangement. The pressure-equalisation valve is a written constraint on the sheet and not a drawn keep-out, because its position on the bought shell is not known | Packer and QA at the first packed kit, against a shell that has been measured |
| 18 | **`TIOV-B-0000` is proposed as the artwork specimen serial and is not yet ruled.** Section 5 sets out why. The specimen unit label is already drawn for it; if the programme rules otherwise the artwork is regenerated | Programme. Closed by a ruling either way |
