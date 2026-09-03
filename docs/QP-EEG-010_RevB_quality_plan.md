# QUALITY PLAN -- EEG FIELD KIT

**Document:** QP-EEG-010  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs.
**Revision note (Rev B):** carrier corrected to 150.0 x 130.0 mm and to four layers, with
inner-layer registration, plane continuity and misregistration added to incoming inspection,
first article and the delivery audit; through-hole part and hole counts recounted from
design.py; the T7 10 uV limit and its k = 2 uncertainty corrected; the C1-C16 and
C21/C41/C61 part numbers, the fiducials, the conformal-coating decision, the serial format,
the per-unit isolation test and the headphone load brought into line with the package
rulings. The findings of the second cross-document audit of 1 September 2026 are closed in
this issue: the "has passed the DRC" claim is replaced by the measured routing result and the
twenty-five open DRC items, the layout-rule citation is corrected to DSN-EEG-002 section 13,
the governing-document revisions are restated, the rulings are cited as the controlled
document RUL-EEG-021, and incoming-inspection row IQC-B15 is added so that a fabrication
release is accepted only against a DRC report with zero open items. The revision letter is
unchanged: these are corrections within the same release.

**Further corrections (2026-09-01, third audit), revision letter again unchanged:** **E-11 is no longer written as though TST-EEG-004 had widened a limit to accommodate the X7R capacitors** -- both Sallen-Key capacitors are X7R at 15 %, f0 moves to 42.4 to 57.4 Hz, that is wider than E-11's 45 to 55 Hz, and the incoming row and FA-09 now say the 50 Hz half of E-11 is not met and that T12e's 42 to 58 Hz is the band this package sets; **E-23 is stated as met in part everywhere it appears**, with the thermal-regulation half met on the charger IC and the 45 C inhibit half not met and untestable for want of a cell temperature; and **the pad census in section 1 says what it counts**, against AVL-EEG-017's smaller figure. The Sallen-Key capacitors are also corrected from 50 V to the 25 V `design.py` actually fits.

**The routing correction (2026-09-02), revision letter again unchanged:** the Rev B DRC report now records **zero violations** -- all 145 nets fully connected, no net without copper, both inner planes continuous under the analogue zone -- so the twenty-five open DRC items stated throughout the previous issue of this plan are gone, and so are the two 0.328 mm electrode-clearance vias. Section 1.1, row IQC-B15, row FB-09 and open item 13 of section 14.2 are restated accordingly: the fabrication data is **released for review under RFQ-EEG-002A** and is **not released for fabrication**, because no human layout engineer has looked at routing produced by the programme's own tools and 169 of its connections close at the minimum conductor or the minimum gap rather than the preferred width. No hardware in this package has been built or measured. S-04, with E-23's 45 C charge inhibit, is untouched by the routing and stays not met. *Corrected 2026-09-02: this sentence also named "S-02 at 53.2 uA" as staying not met. ECO-EEG-024 was applied the same day and S-02 is met in the design at 36.8 uA; see the correction below.*

**Corrections after the firmware build and ECO-EEG-024 (2026-09-02), revision letter again unchanged.** Two things this plan asserted throughout stopped being true on the day it was issued, and both are restated rather than deleted. **S-02 is met in the design.** ECO-EEG-024 is applied in `tools/design.py`: R1 to R16 are **68 kOhm** (Vishay TNPW060368K0BEEA), the single-fault DC current is **36.8 uA** against the 50 uA limit, and E-10 moves to the **+/- 1.0 dB** branch the requirement already carried. Row IQC-2.3, row FA-03, section 1.4's pointer row and open item 3 of section 14.2 are restated; the 47 kOhm figures are kept beside the new ones as the superseded set. **Met in the design is not signed off**: nothing is measured, no unit exists, and the electrical safety reviewer named in open item 1 has not started, so S-02 remains that reviewer's item. **The contact-light driver is written.** `firmware/main/main.c` implements E-27's bicolour phase scheme -- both halves of the converter's lead-off status are captured, neither detector gone is green, exactly one is amber, both is red -- so open item 7's "the bicolour phase scheme is specified and not yet coded, so the contact-light test step cannot pass" is superseded. TST-EEG-004 T11 is written against it and has never been run: no unit exists. The firmware itself is now **built** -- ESP-IDF v5.2.5, target esp32s3, images and SHA-256 manifest in `firmware/release/` -- and has run only under QEMU emulation, never on hardware.

**Corrections after the verification review of package v2.2 (2026-09-02), revision letter again unchanged:** two figures are corrected to the artefacts they describe. Row IQC-B15 dated the released DRC report 1 September; `kicad/EEG-CAR-01_RevB_DRC_report.txt` is dated 2 September on its own `Generated` line, and the date an inspector compares is the date printed on the report. Section 12.4's fixture self-test named the lead-off references by the rounded values 5 k / 10 k / 50 k; FIX-01/A switches the E96 parts **4k99 / 10k0 / 49k9**, which is what JIG-EEG-009 Rev B section 0.1 and TST-EEG-004 Rev C T10 already name, and the rounding is not harmless at the top of the range. Both are corrections of wording to fitted fact; nothing about the plan, the sampling or the limits changes.

## Why this document exists

The v1 package named quality in three fragments -- "visual and AOI inspection to IPC-A-610
class 2" in RFQ-EEG-001 section 9.1 and TST-EEG-004 step T1, "IPC class 2" on the PCB
specification sheet, and "X-ray on the converter packages for the Phase 1 units" -- and
nothing tied them together. The 14-agent audit of v1 raised five findings in this domain:
`quality-plan-aql` (no inspection points, no sampling, no first-article procedure, no
non-conformance route, no ESD requirement), `iqc-incoming-inspection-modules` (no incoming
inspection for the twelve purchased module types the whole architecture rests on),
`sampling-plan-and-msa` (no sampling plan, no gauge R&R, no golden unit, no fixture
verification interval), `failure-disposition-and-rework` (nothing says what happens when a
unit fails), and `supplier-quality-and-avl` (no supplier quality requirements or change
notification). Contradiction XD-15 additionally showed that a review finding recorded as
closed -- the correction of a bidder's certification status -- had never been applied. This
plan closes all six. It is a contractual annex to RFQ-EEG-001 Rev E: bidders price against
it, and the programme audits against it.

No hardware in this package has been manufactured or measured; the firmware image in
`firmware/release/` is the only thing that has been built, and it has run only under
emulation. **No safety engineer has reviewed this design.** Every figure below marked *calculated* is exactly that, and every limit that
depends on a measurement the programme has not yet made is flagged as such.

---

## 1. Scope, and the standards actually claimed

This plan covers the carrier board EEG-CAR-01 Rev B (150.0 x 130.0 mm, **four layers**, 211
reference designators, **636 pads in total on the board**, 156 nets, 30 connectors J1 to J30 of
which seventeen are module connectors), the twelve purchased module types, the helmet and harness assemblies,
the kit contents and the packed travel case, across all three phases: Phase 1 (2
prototypes), Phase 2 (10 kits) and Phase 3 (10 to 40 further kits, 25 to 50 in total).

Of the 211 designators, 186 are purchased placements: 153 surface-mount, of which **R89 is
do-not-populate**, and **33 through-hole**. The remaining 25 designators are 18 test pads,
3 fiducials and 4 mounting holes. Thirteen module assemblies are fitted per unit from the
twelve purchased types, because the ADS1299 breakout is fitted twice. Twelve assemblies
mount on the MP-01 module plate; the ESP32-S3-DevKitC-1-N16R8 is inserted directly into J6
and J7.

**What the 636 counts, exactly.** Every pad in `tools/design.py`, with nothing left out:
390 surface-mount, of which 18 are test pads and 6 are the pads of the three fiducials;
236 plated through-hole; and 10 non-plated, being the four mounting holes and the six
anchor holes of the DIN sockets J15 to J17. **620 of the 636 carry a net**, so the netlist
pin count is 620, not 636; the 16 that carry none are the 6 fiducial pads and the 10
non-plated holes. This plan inspects against the 636, because a stencil, an AOI recipe and
a bare-board test all have to account for pads that no netlist mentions.

**AVL-EEG-017 Rev B section 1 gives 614 for the same board, and that figure is not this
one.** The difference is exactly 22: the 18 test pads plus the 4 mounting-hole pads. So 614
is this board with those left in place and left out of the count -- the six fiducial pads
are in both figures -- and it is neither a different board nor the 620 netlist pins.
AVL-EEG-017 does not say which pads its figure omits. Where a pad count is inspected
against, this plan's 636 governs, and AVL-EEG-017 is corrected to it at its next revision.

### 1.1 Two things changed during layout, and this plan inspects both

**The board grew from 130 x 124 mm to 150 x 130 mm.** Thirty connectors, 211 parts and 156
nets would not close at the smaller size. The extra 33.8 cm² of bare board costs a few euro
per unit at these quantities, against a real risk of an unroutable design.

**The board went from two layers to four.** Package v1 asserted that a two-layer carrier
was enough. Doing the layout showed that it is not: on two layers the bottom side has to be
both the reference plane and the second routing surface, and it cannot be both. Four layers
-- L1 signal, L2 reference plane, L3 reference plane, L4 signal -- give two full routing
surfaces and a continuous reference under every analogue trace, which is what DSN-EEG-002
section 13's "layout rules that are requirements, not preferences" require, and which a
swiss-cheesed two-layer pour cannot deliver. At 2 units the four-layer board costs about
EUR 35 more in total; at 50 units it is about EUR 3 per board. For a sixteen-channel EEG
front end that is the right trade, and it is the single most important thing package v2
learned by doing the work instead of asserting it.

Two citations in that sentence are worth being exact about, because this plan inspects
against both. The layout rules "that are requirements, not preferences" are **DSN-EEG-002
section 13**. The zoning rule, the star-point rule and the isolation keep-out are
**DSN-EEG-003 section 3.3**. DSN-EEG-003 runs to section 11 plus its annexes and has no
section 13, so a citation to "DSN-EEG-003 section 13" is wrong wherever it appears.

The quality consequence is that three characteristics which did not exist on a two-layer
board now have to be inspected on every fabrication lot: **inner-layer registration**,
**plane continuity on both inner layers**, and the **layer-to-layer misregistration limit**.
They are rows IQC-B11, IQC-B12 and IQC-B13 in section 2.1, rows FB-21 to FB-24 in section
4.3, and row A-23 in section 13.

The geometry this plan inspects against, taken from `design.py` and `mech_gen.py`:

| Item | Value |
|---|---|
| Carrier outline | 150.0 x 130.0 mm, rectangular, no cut-outs |
| Layers | four: L1 signal, L2 reference plane, L3 reference plane, L4 signal |
| Stack-up | mask / 35 um L1 / prepreg 0.200 / 17 um L2 / core 1.065 / 17 um L3 / prepreg 0.200 / 35 um L4 / mask = 1.60 mm +/- 10 % |
| Copper | 1 oz (35 um) outer, 0.5 oz (17 um) inner, both finished |
| Reference planes | AGND_REF left of x = 62 mm and DGND right of it, on **both** L2 and L3, tied together by stitching vias |
| Vias | **through vias only** -- no blind, buried, back-drilled, filled or plugged vias. 0.60 mm pad on a 0.30 mm finished hole, 0.15 mm nominal annular ring, tented both sides |
| Zone split | x = 62 mm: analogue left, digital right |
| Mounting holes | M3, 3.2 mm NPTH at (5,5), (145,5), (5,125), (145,125), 6 mm copper keep-out |
| Isolation keep-out | x >= 141 mm, y = 2 to 22 mm, no copper on any of the four layers |
| Fiducials | three 1.0 mm round fiducials with 3.0 mm mask openings, at (12,10), (144,100) and (12,120) |
| MP-01 module plate | 146.0 x 126.0 x 3.0 mm, 8 mm solid border, 12 x 3 mm jumper slots on a 16 x 7 mm grid |
| POD-P1 base | 163.0 x 143.0 x 58.0 mm external; 158.0 x 138.0 x 55.5 mm internal |
| POD-P1 lid | 163.0 x 143.0 x 6.0 mm, 2.0 mm spigot |
| Stack budget | floor 2.5 + boss 6.0 + carrier 1.6 + standoff 18.0 + plate 3.0 + modules <= 18.0 = 49.1 mm against 55.5 mm internal, margin 6.4 mm |

**The Rev B routing, and what it does and does not permit.** EEG-CAR-01 Rev B is routed
on four layers with 3 745 track segments and 552 through vias, and each reference plane is one
continuous island per net. **All 145 nets are fully connected**: none unclosed, none without
copper. Every rule in `kicad/EEG-CAR-01_RevB_DRC_report.txt` passes: the smallest measured
clearance is 0.260 mm on L1, 0.285 mm on the planes and 0.275 mm on L4 against a 0.20 mm rule;
the narrowest conductor is 0.20 mm and the smallest plated hole is 0.30 mm; no copper comes
within 2.00 mm of a non-plated hole; there are no zone crossings, no duplicate copper segments
and no duplicate via positions; no digital net enters the analogue zone; and there is exactly
one AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND bridge. The report's own line is
"VIOLATIONS: 0 -- none.  The board passes every rule listed above." It also records the
isolation strip as free of copper on all four layers. That last statement is made because the
report says it, not because the keep-out was assumed to have been honoured on the inner
layers.

**The board closes, and the data is released for review, not for fabrication.** ECO-EEG-016
section 3 gates a fabrication-data release on zero DRC violations, every net one connected
copper island, and both inner planes continuous under the analogue zone. **All three are now
met**, so the data is **RELEASED FOR REVIEW under RFQ-EEG-002A** -- and **fabrication release
awaits that review**, because the routing was produced by the programme's own tools and has
**not** been reviewed by a human layout engineer. How the board closes is part of what that
reviewer is for. **169 connections are relaxed**: 36 take a conductor narrower than the 0.25 mm
preferred width, and 133 keep full width and take a reduced gap instead, every one of them at
or above the 0.20 mm minimum conductor and the 0.20 mm minimum gap. A board that closes at
minimum geometry is not the same board as one that closes at preferred geometry, even when
every rule passes. Row IQC-B15 in section 2.1 remains the inspection point that keeps a board
built to a data set that is released for review under RFQ-EEG-002A but not yet released for
fabrication out of the build, and the
four-layer change is itself a change the layout and safety reviewer must check when one is
appointed.

RUL-EEG-021 section B gives the fiducial positions as (12,10), (144,100) and (12,120), which
is where `design.py` places them and what is inspected. The register's first issue transcribed
them as (8,8), (142,8) and (8,122); that error is corrected, and `design.py` governs in any
case.

### 1.2 Standards required

| Standard | Revision | Applies to | Required? |
|---|---|---|---|
| IPC-A-610 class 2 | Rev H or later, stated in the quote | Assembled carrier workmanship, T1 | **Required** |
| IPC J-STD-001 class 2 | Rev H or later | Soldering process, SMT and the 236 plated through-holes | **Required** |
| IPC-A-600 class 2 / IPC-6012 class 2 | current | Bare board acceptance, including the four-layer characteristics of section 2.1 | **Required** |
| IPC-7711/7721 | current | Rework and repair, with the limits in section 7 | **Required** |
| IPC-9252 | current | 100 % bare-board electrical test to the supplied IPC-D-356A netlist | **Required** |
| ANSI/ESD S20.20 or IEC 61340-5-1 | current | An EPA covering bare carriers, ADS1299 modules, U1-U3 and U7 | **Required** |
| ISO 9001 | 2015 | Manufacturer's quality system | **Not required.** Asked for as information only |
| ISO 13485 | -- | Medical device quality system | **Not required, and not wanted** |

All three IPC classes apply and all three are named: IPC-6012 class 2 for fabrication,
IPC-A-600 class 2 for bare-board acceptance, IPC-A-610 class 2 for assembly. Where another
document in the package lists only two of them, this row and DSN-EEG-003 section 3.2 govern.

### 1.3 Why ISO 13485 is not asked for, and a correction to the record

The instrument is a loaned research field kit. It is not a medical device and is not placed
on the market. It is designed to the applicable principles of IEC 60601-1 for a type BF
applied part (RFQ section 8) because that is good engineering for something connected to a
person's head, but certification is not requested and no medical claim is made. Requiring
ISO 13485 would add cost and lead time without adding assurance for this product, and it
would give a false signal about the device's regulatory status. Bidders who hold ISO 13485
are not preferred over bidders who do not.

**Correction to the record.** DSN-EEG-003 Rev A.2 section 7, adversarial-review finding 11,
recorded that "Regulus corrected our assumption of ISO 13485 -- contact list was wrong for
one company", with the action shown as complete. The correction was never applied to the
file. Regulus Electronics (New Taipei, Taiwan) holds **ISO 9001 and does not hold ISO
13485**; the manufacturer contact list continued to assert "ISO 13485 capable" against them
until package_v2.2. Two further contact corrections recorded as complete were also never
applied: RayPCB should read PCBSync (contact stan@pcbsync.com), and NextPCB was to be
dropped from the mailing but remained listed twice. All three are corrected in AVL-EEG-017 Rev B, which is now the single source for supplier identity and certification status. No
certification claim about any bidder is to be restated in a programme document without a
copy of the certificate on file.

### 1.4 What this plan does not restate

One table, one home. This plan cites the following and does not repeat them:

| Content | Its one home |
|---|---|
| Board specification (size, stack, finish, tracks, holes, classes) | DSN-EEG-003 section 3.2 |
| Isolation keep-out and the star-point rule | DSN-EEG-003 section 3.3 |
| Module-to-connector table and the jumper set | ICD-EEG-006 section 1 |
| ESP32-S3 GPIO map | ICD-EEG-006 section 5 |
| ECO register | ECO-EEG-016 section 2 |
| 68 kOhm / 10 nF noise-and-flatness arithmetic (47 kOhm before ECO-EEG-024) | RISK-EEG-011 section 4, **which has not yet been restated against the applied ECO** |
| Test step numbers and their names | TST-EEG-004 Rev C |
| Public-key fingerprint definition | FW-EEG-001 section 7 |
| Lithium shipping procedure | PKG-EEG-015 section 7 |
| Foam pocket schedule and label artwork | PKG-EEG-015 sections 2 and 5 |
| Serial format `TIOV-B-nnnn` | PKG-EEG-015 section 5 |
| The rulings that settled the cross-document disagreements | RUL-EEG-021 Rev A |

The geometry recap in section 1.1 is the one deliberate exception: the two layout changes
must be visible in every document of the release, and the inspection rows below refer back
to it rather than repeating the coordinates a second time.

### 1.5 Roles and sign-off authority

| Role | Held by | Signs |
|---|---|---|
| Programme technical lead | TI One Voice, Brussels | ECOs, deviations, concessions, FAI approval |
| Programme quality lead | TI One Voice, Brussels (named on the purchase order) | IQC waivers, NCR disposition at MRB, first-delivery audit |
| Electrical safety reviewer | External, engaged by the programme; **not yet appointed** | Release of Phase 2; any change to a risk-control component |
| Manufacturer QA manager | Manufacturer | IQC records, FAI report, lot release, CAPA closure |
| Manufacturer test operator | Manufacturer, named and trained | TST-EEG-004 records per serial |

The programme has no full-time quality function. The quality lead is a named programme
member with other duties. This plan is written so that it can be operated by one person on
the programme side and one QA manager on the manufacturer side.

---

## 2. Incoming quality control (IQC)

No lot enters SMT, assembly or kitting until its IQC record is closed. Rejected material
goes to a physically separate, labelled quarantine location and is dispositioned under
section 7.

### 2.1 Bare boards

| # | Check | Method | Accept | Reject |
|---|---|---|---|---|
| IQC-B1 | Fabrication CoC: IPC-6012 class 2, IPC-A-600 class 2, laminate FR-4 Tg >= 150 C, four layers | Document | Present, lot-specific | Missing or generic |
| IQC-B2 | 100 % electrical test certificate to the supplied IPC-D-356A netlist, 156 nets | Document | Present, states "100 %" | Sampled, or netlist not the released one |
| IQC-B3 | Outline 150.0 x 130.0 mm (section 1.1) | Callipers, 2 boards per lot | +/- 0.20 mm | Outside |
| IQC-B4 | Thickness 1.60 mm +/- 10 % over the four-layer stack of section 1.1 | Micrometer, 4 points, 2 boards | 1.44-1.76 mm | Outside |
| IQC-B5 | ENIG thickness Au 0.05-0.10 um over Ni 3.0-6.0 um | XRF, fabricator report + 1 board per lot | Within band | Outside, or no report |
| IQC-B6 | NPTH holes carry no copper and no mask (ECO-EEG-012): 4 x 3.2 mm at MH1-MH4 and 6 x 1.50 mm DIN retention posts | Visual x10 | Bare laminate in every one | Any plating or mask -- **hard reject, whole lot** |
| IQC-B7 | Isolation keep-out per DSN-EEG-003 section 3.3, free of copper on **all four layers** | Visual against the fab drawing, plus the inner-layer artwork check of IQC-B13 | No copper | Any copper -- **hard reject** (S-03) |
| IQC-B8 | J6/J7 hole-row spacing 22.86 mm (ECO-EEG-008) | Pin gauge or CMM, 2 boards | +/- 0.10 mm | Outside -- the DevKit will not fit |
| IQC-B9 | Bow and twist | Surface plate, 2 boards | <= 0.75 % | Outside |
| IQC-B10 | Legend legibility, date code and UL mark on the bottom legend | Visual | Legible, inside the outline, clear of pads | Illegible or over a pad |
| IQC-B11 | **Inner-layer registration.** Microsection of the lot coupon: four copper layers in the order L1 signal / L2 plane / L3 plane / L4 signal; dielectric thicknesses within +/- 10 % of section 1.1; internal annular ring measured at a through via | Microsection, 1 coupon per fabrication lot, report retained | Four layers in the right order; internal annular ring >= 0.025 mm (IPC-6012 class 2) | Wrong layer order, a missing plane, or any internal annular ring below 0.025 mm -- **hard reject, whole lot** |
| IQC-B12 | **Layer-to-layer misregistration.** A 0.60 mm pad on a 0.30 mm hole gives a 0.15 mm nominal internal annular ring, so class 2's 0.025 mm minimum survives at most 0.125 mm of misregistration. That is the limit | Fabricator registration report plus the IQC-B11 coupon | <= 0.125 mm at every measured location | Above 0.125 mm |
| IQC-B13 | **Plane continuity and the plane split.** Inner-layer artwork compared with the released Gerbers for voids, starved etch and slots under the analogue traces; 4-wire resistance corner to corner on each plane region through stitching vias; AGND_REF to DGND open on a bare board, where R90 is not yet fitted | Artwork comparison on every lot; 4-wire DMM on 2 boards, and the insulation tester at 250 V DC for the plane separation | Plane regions <= 0.10 Ohm corner to corner; AGND_REF to DGND **>= 100 MOhm at 250 V DC** (TST-EEG-004 Rev C T0, which owns the limit); no void that breaks the reference under an analogue trace | Any short between the plane regions, or a void under an analogue trace -- **hard reject** |
| IQC-B14 | Three fiducials, 1.0 mm copper in a 3.0 mm mask opening, at the positions of section 1.1 (ECO-EEG-020) | Visual, 2 boards | All three present, clean, unmasked | Missing or masked -- the placement machine falls back to a vision teach the programme no longer pays for |
| IQC-B15 | **The DRC report that accompanies the fabrication data release has zero open items.** The report issued with the Gerber, drill and IPC-D-356A set names the same design revision as the boards in the lot, and it lists no violation of any class: no unclosed connection, no clearance, width, annular-ring, hole-size, edge, non-plated-hole, isolation-keep-out and no via-keep-out entry, every net one connected copper island, and both inner planes continuous under the analogue zone | Document. The report is read line by line against the released data set and retained in the IQC pack; the revision on the report is compared with the revision marked on the boards | `VIOLATIONS: 0`, no unclosed connection, and the report's design revision identical to the boards' | Any non-zero violation count, any net that is not one copper island, or a report from a different design revision -- **hard reject, whole lot**, and the boards do not enter the build. The Rev B report that accompanies this release, `kicad/EEG-CAR-01_RevB_DRC_report.txt`, is dated **2 September 2026** on its own `Generated` line and records `VIOLATIONS: 0`, all 145 nets connected as one copper island each, and both inner planes continuous, so it satisfies every criterion in this row. *Was: "dated 1 September 2026"* -- that was the date of the routing run this plan was first written against, and the report it names was re-generated on 2 September; the date on the report itself is the one an inspector compares, so it is the one stated here. That is not by itself a fabrication release: the data is released for review under RFQ-EEG-002A, the human layout review has not happened, and until it has, no lot can be presented against this row (section 1.1) |

Sampling for the dimensional rows is two boards per fabrication lot for Phase 1 and Phase 2,
and the c=0 plans of section 6 for Phase 3. Rows IQC-B1, B2, B6, B7, B11, B12, B13 and B15
are checked on **every** board, or on the lot coupon or the released document that represents
it -- B6, B7 and B13 are safety characteristics, B11 and B12 cannot be seen from the outside
of a four-layer board, and B2 and B15 are documents. IQC-B15 is checked first, because a
fabrication release whose DRC report still carries open items is not a release, and no lot
built against one is accepted whatever the boards themselves measure.

### 2.2 Purchased modules

Twelve module types, thirteen assemblies per unit. 100 % inspection for Phases 1 and 2. From
Phase 3, the rows marked "sample" drop to the c=0 plans of section 6; the rows marked
"every" stay at 100 % for the life of the fleet.

| Module | Rate | Check | Accept / reject |
|---|---|---|---|
| ADS1299 breakout x2 (J1/J2/J23, J3/J4/J29) | every | Photograph of the TI package marking, date code and lot recorded; continuity of the 1x12 digital header to the J1 pin order and the 1x10 signal header to the J2 pin order; DAISY_IN and CLKOUT physically exposed; record whether the module needs the J5 jumper; bench power-up and ADS1299 ID register read; AVDD/AVSS measured on-module | Reject on any pinout mismatch, absent DAISY_IN or CLKOUT, ID register mismatch, or AVDD/AVSS outside +2.50/-2.50 V +/- 5 % |
| ESP32-S3-DevKitC-1-N16R8 | every | `esptool flash_id` read back; the module's own UART USB-C port exercised, because that port and not J26 is the end-of-line flashing route | Accept only 16 MB flash **and** 8 MB PSRAM. The -N16R8 is not substitutable (E-18); mislabelled boards are common |
| ADuM4160 isolator module | every | Part marking; **host connector type recorded**; barrier visually intact with no component, track or label bridging it; supplier isolation certificate >= 2.5 kV RMS on file, checked once per module lot | Reject on any bridging or a missing certificate. **This is the single safety-critical purchased part** (E-24, S-03). The named candidate presents **USB-B and E-24 asks for USB-C, so E-24 is not met**; the interim answer is the WH-09 USB-B to USB-C panel pigtail, and a USB-B module is accepted only while WH-09 is fitted |
| ATECC608B breakout | every | Factory serial read over I2C and recorded; config zone confirmed UNLOCKED on arrival | Reject a locked part |
| ES8388 codec | sample | Header pin order against J8 and J9; I2C presence check | Reject the lot on any pin-order mismatch. **AVL-EEG-017 carries this line as OPEN WITH CRITERIA**: no vendor is qualified and an approved sample must be on file before the fleet order. |
| bq24074-class charger | sample | Header pin order against J12; charge-enable pin responds to CHG_CE | Reject the lot on any pin-order mismatch. **E-23 is met in part, and the two halves must always be stated together.** The thermal-regulation half is met on the charger IC, which is what this incoming check confirms. **The 45 C charge inhibit is not met and cannot be tested**: it needs a cell temperature, and there is no NTC net in design.py and no thermistor way on J12 or J13, so nothing on the carrier can read the cell. **S-04's thermistor-monitored charging is not met either** -- the two hardware holes are the same hole (section 14.2; RFQ-EEG-001 Rev E E-23, S-04 and section 12 item 3; AVL-EEG-017 K16) |
| MAX17048 gauge | sample | Header pin order against J12; I2C presence check | As above. Where a combined charger-plus-gauge assembly is supplied, which is the baseline, the two rows are inspected as one against both sets of criteria; where two separate breakouts are supplied, the gauge mounts on MP-01 and its taps are made at the MP-01 end of the J12 Y jumper drawn in ICD-EEG-006 section 3.3 |
| TPS63020-class buck-boost (J25) | sample | Header pin order against J25; output measured at 5.00 V into 0.5 A | Reject the lot on any pin-order mismatch or an output outside 4.90-5.10 V. This is the part ECO-EEG-002 added to make the board power up at all, and it is easy to leave off a kitting list. **AVL-EEG-017 carries this line as OPEN WITH CRITERIA**: no vendor is qualified and an approved sample must be on file before the fleet order. |
| microSD breakout | sample | Header pin order against J20; one-bit SDMMC lines present | Reject the lot on any pin-order mismatch |
| Boom preamplifier module (J21, mounted on MP-01) | sample | Header pin order against J21; gain fixed, **automatic gain control absent**; noise floor recorded | **The part is not settled and must not be recorded as settled.** The MAX9814 named in package v1 is an AGC part and E-14 forbids AGC, so it is not approved; the module is specified by interface in ICD-EEG-006 and a fixed-gain part of the MAX4466 class is the preferred route. Reject any module with AGC that cannot be disabled without modifying it |
| Room-microphone module (J28) | sample | Header pin order against J28; hardware mute line exercised | **No module is yet known to meet the hardware-mute requirement of E-15**, so this row is written against an unsourced part; reject anything whose mute is firmware-only |
| 74HC595 breakout (J19) | sample | Header pin order against J19; Q0-Q7 exposed | Reject the lot on any pin-order mismatch. **AVL-EEG-017 carries this line as OPEN WITH CRITERIA**: no vendor is qualified and an approved sample must be on file before the fleet order. |
| Protected 18650 cell | every | OCV 3.4-3.9 V; internal resistance recorded; protection PCM present and mechanically sound; cell lot recorded; UN 38.3 report and safety data sheet collected per lot (S-04) | Reject a cell outside the OCV band, any cell with a damaged wrap or PCM, any lot without a UN 38.3 report |
| 32 GB industrial microSD | sample | Capacity and part number; full-card write-read verify on the sample | Reject on capacity mismatch or any read error |

The boom preamplifier sits on the MP-01 module plate and connects at J21. The boom itself
carries the bare electret capsule and its screen on the J18 pigtail. Package v1 put the
preamplifier on the boom; `design.py` governs and it does not.

### 2.3 Carrier passives -- the ones that carry the specification

| Item | Rate | Check | Accept / reject |
|---|---|---|---|
| R1-R16, **68 k** 0.1 % 25 ppm, Vishay **TNPW060368K0BEEA** | reel label 100 %, plus 5 pieces per reel measured | 4-wire DMM | Reject the reel if any piece is outside 0.1 %. These resistors set both the T7 source impedance and the T10 lead-off offset. **A 47 k part in this position is a hard reject**, not a substitution: at 47 kOhm the S-02 single-fault DC current is 53.2 uA against a 50 uA limit and the unit is a safety non-conformance. *Corrected 2026-09-02: this row specified 47 k / TNPW060347K0BEEA and recorded S-02 as not met. ECO-EEG-024 is applied in `tools/design.py`, S-02 is met in the design at 36.8 uA, and E-10 moves to its +/- 1.0 dB branch (TST-EEG-004 T22). The figure is calculated and unsigned-off; see section 14.2 items 1 and 3* |
| C1-C16, 10 n **C0G** 50 V, Murata **GCM1885C1H103JA16D** | reel label 100 % | Manufacturer part number on the reel | **X7R is a hard reject.** The v1 part number GCM188R71H103KA37D carries the R7 dielectric code and is an X7R part; it is superseded by GCM1885C1H103JA16D (ECO-EEG-019). X7R is +/- 15 % with a voltage and temperature coefficient on top, and the common-mode rejection of the input network is set by the match of the sixteen RC time constants |
| C21, C41, C61, 100 n **25 V** and C22, C42, C62, 220 n 25 V Sallen-Key capacitors, Murata GCM188R71E104KA57D and GCM188R71E224KA64D | reel label 100 % | Manufacturer part number on the reel | **Both are X7R, declared, with a stated 15 % capacitance tolerance over temperature.** A 100 nF C0G in 0603/50 V is not a stocked part, so these are X7R by decision and not by accident (ECO-EEG-019). The consequence is stated in section 4.3 row FA-09: the envelope corner cannot be held inside E-11's +/- 10 % by the fitted dielectric, and **E-11's 50 Hz +/- 10 % half is therefore not met** -- TST-EEG-004 T12e measures f0 per unit against 42 to 58 Hz, which is the band TST-EEG-004 sets against the parts approved here and not a widening of any E-11 limit that was ever written (TST-EEG-004 section 16 item 16). IQC cannot inspect its way round this: a reel that conforms to its own part number still gives a corner outside E-11. *Both are 25 V parts: the "50 V" of the previous issue of this row was wrong against `design.py`, which governs, and against the `71E` rating code in both part numbers* |
| Envelope-chain thin films (R20-R28, R40-R48, R60-R68, all 0.1 %), U1-U3 **OPA4376AID (SOIC-14), TI OPA4376AIDR**, U7 TLV3201AIDBVR | reel and tube labels | Part number and date code | Reject on any substitution not carrying an approved ECO. The v1 "OPA4376AIPW" TSSOP part number is superseded; `design.py` fits the SOIC-14 |
| D1-D16, **BAV99**, Nexperia BAV99,215 | reel label 100 % | Manufacturer part number on the reel | **BAT54S is a hard reject in the D1-D16 positions.** Schottky leakage across a 68 kOhm series resistor is an offset error on a 10 uV input. BAT54S is fitted only at D20, D40 and D60, the envelope rectifiers |
| R94, R95, 4k7 1 % I2C pull-ups | reel label 100 % | Part number | Added by ECO-EEG-021 so that the bus does not depend on whatever the modules happen to carry |

**Verification and sign-off.** IQC is performed by the manufacturer's goods-in inspector and
signed by the manufacturer QA manager. The programme quality lead countersigns the Phase 1
IQC pack before the first build and audits it thereafter under section 13.

---

## 3. In-process inspection points

| IP | Point in the flow | What is checked | Rate | Record |
|---|---|---|---|---|
| IP-1 | Solder paste, before placement | Stencil part number and revision; paste alloy and lot; SPI or a 3-board first-off visual; the three fiducials read by the placement machine | First-off + 1 per shift | Board serial, paste lot |
| IP-2 | After reflow, before THT | AOI to IPC-A-610 class 2; polarity of D1-D16 (BAV99), D23, D24; **BAT54S pin 3 to the op-amp output** on D20, D40 and D60 (ECO-EEG-005); U1-U3 and U7 pin 1 | 100 % | AOI report per board |
| IP-3 | THT and socket insertion | **33 through-hole parts, 236 plated holes**, plus the 10 non-plated holes of IQC-B6 which stay bare; socket strips seated flush, standoff <= 0.5 mm; pin 1 square pad against the legend; J15-J17 DIN sockets perpendicular with retention posts engaged | 100 % | Operator initials |
| IP-4 | Star points and links | The star-point rule of DSN-EEG-003 section 3.3: R90 fitted exactly once; R91 fitted exactly once; **no wire link or solder bridge across either**; R92 and R93 fitted by default; R89 not populated | 100 % | Tick sheet |
| IP-5 | Isolation keep-out | The strip of DSN-EEG-003 section 3.3 free of solder, flux residue, adhesive and any part body, on both outer layers | 100 % | Photograph retained |
| IP-6 | Cleanliness | J-STD-001 class 2; no-clean residue acceptable; if an aqueous process is used, ionic cleanliness per the manufacturer's own qualified limit | 1 per lot | Certificate |
| IP-7 | Module fitting | Modules on the MP-01 plate (146.0 x 126.0 x 3.0 mm), keyed ribbon jumpers per ICD-EEG-006 with the WH-KEY-01 printed keying shrouds fitted; four M3 x 18 mm nylon female-female standoffs and eight M3 x 6 nylon pan screws; the DevKit inserted directly into J6/J7 with no bent pins | 100 % | TST-EEG-004 T2 |
| IP-8 | Harness build | Continuity of every conductor on the 12-way screened electrode cable to J14 and the 10-way light cable to J30; screen continuity; screen landed at one end only; insulation resistance | 100 % | Wire-list tick sheet per WH-EEG-008 |
| IP-9 | Printed parts, goods-in from the print bureau | Dimensional check of the HM-04 bayonet, collar and hatch fits against the FIT-01 coupon (60.0 x 24.0 x 10.0 mm, bores 9.20 / 9.35 / 9.15 mm); powder fully removed from internal channels | First-off per build, then sampled | Coupon result |
| IP-10 | Pod closure | Stack height measured against the 55.5 mm internal depth of POD-P1 (49.1 mm calculated, margin 6.4 mm); openings gasketed or recessed; **no LED opening -- M-02 is withdrawn and the pod carries no indicator**; no gel path to the board; label applied per PKG-EEG-015 | 100 % | T18 |
| IP-11 | ESD | Operator wrist strap and mat verified at shift start; EPA verified per ANSI/ESD S20.20 | Per shift | ESD log |

IP-11 exists because the ADS1299 front end, the three OPA4376 quads at U1-U3 and the sixteen
high-impedance input networks are exactly the parts that electrostatic damage degrades
silently into a noisier channel that still passes a functional check.

The 18 mm standoff at IP-7 is also a safety characteristic. The slant path from carrier
copper, over the edge of the isolation keep-out and up the standoff to any host-side
conductor on MP-01, is at least 18 mm, which is more than twice the 8 mm the safety case
asks for. This is what closes RISK-EEG-011 SR-08, so a shorter standoff is not a
substitution the line may make.

---

## 4. First-article inspection (FAI)

An FAI is required before the first batch of each phase, and again after any ECO that touches
the board, a printed part, the harness or the firmware pin map. It follows the AS9102
three-form structure, adapted: this is not an aerospace part and no AS9102 compliance is
claimed. FAI is performed on the **first assembled carrier** and the **first complete kit**,
and is approved in writing by the programme technical lead before the balance of the batch is
built.

### 4.1 Form 1 -- part number accountability

| Field | Entry |
|---|---|
| Part number / revision | EEG-CAR-01 Rev B (carrier); TIOV-EEG-KIT Rev A (kit) |
| Part name | Sixteen-channel research EEG carrier / EEG field kit |
| Serial number | First unit of the batch, programme serial as allocated (section 9) |
| FAI type | Full (first article) or partial (state which characteristics are re-verified and why) |
| Drawing / data set | design.py Rev B, released four-layer Gerber and drill set, IPC-D-356A netlist, CPL, ASM-EEG-007, WH-EEG-008, kit BOM, and the DRC report issued with them. No FAI is opened against a data set whose DRC report carries open items (IQC-B15) |
| Detail parts and assemblies | 211 reference designators, of which 186 are purchased placements; 12 purchased module types in 13 assemblies; the printed parts listed in PARTS-EEG-019 section 2; harness; case and foam |
| Reason for FAI | New design / ECO number / process change / vendor change / lapse > 24 months |

### 4.2 Form 2 -- product accountability: materials, processes, testing

| Item | Requirement | Evidence |
|---|---|---|
| Laminate and stack-up | FR-4, Tg >= 150 C, four layers, 1.60 mm +/- 10 %, 1 oz outer and 0.5 oz inner copper, per section 1.1 | Fabricator CoC, lot number, stack-up drawing as built |
| Inner layers | Microsection coupon per IQC-B11; misregistration per IQC-B12; plane continuity per IQC-B13 | Microsection report, registration report, 4-wire results |
| Surface finish | ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um | XRF report |
| Solder alloy | Stated by the manufacturer (SAC305 assumed unless declared otherwise); flux type | Alloy CoC, reflow profile record |
| Reflow profile | Board-specific profile with the thermocouple trace | Profile record |
| Through-hole process | Hand or selective solder, J-STD-001 class 2, 236 plated holes | Process sheet |
| Printed parts | MJF PA12, dyed; orientation, powder removal, finishing per the print specification | Print bureau CoC, FIT-01 coupon results |
| Skin-contact materials | ISO 10993-5 / -10 supplier declarations for cups, ear clips, TPU pads, the HM-06 chin strap and the HM-03 occipital yoke (S-05). The A-03 headband is withdrawn as a kit item, so there is no declaration to collect against it | Declarations on file |
| Cell | Protected 18650, UN 38.3 report per lot (S-04) | Report reference recorded in the DHR |
| Special processes with no qualification | Laser marking. **Conformal coating is not applied**: the decision is taken, not deferred (section 14.2) | -- |
| Functional testing | TST-EEG-004 Rev C, all steps, on the FAI unit | Full record, all numeric values |
| Type tests, once per model rather than per unit | Maximum acoustic output <= 100 dB SPL on an artificial ear at any commanded level (E-29), with the firmware codec volume clamp set to the value measured at calibration; the ADuM4160 supplier's 2.5 kV RMS isolation certificate | Type-test report; supplier certificate |

E-29 is a new requirement and it exists because the calculated full-scale output of the
headphone chain is about 110 dB SPL, which is above the limit. Until the type test is run on
the shipped headphone model, the clamp value is provisional.

### 4.3 Form 3 -- characteristic accountability

Every characteristic below is measured on the first article and recorded with its actual
value, not a tick. "Calculated" marks a design value that has never been measured on
hardware. The requirement values are not restated here: they are in DSN-EEG-003 section 3.2
for the board and in section 1.1 above for the two layout changes. What this form adds is the
gauge, the sample and the signature.

**Bare board**

| # | Characteristic | Requirement | Method / gauge | Signed by |
|---|---|---|---|---|
| FB-01 | Outline length | 150.0 +/- 0.20 mm | Callipers | QA |
| FB-02 | Outline width | 130.0 +/- 0.20 mm | Callipers | QA |
| FB-03 | Thickness | 1.60 mm +/- 10 % | Micrometer, 4 points | QA |
| FB-04 | Layer count and order | **4: L1 signal, L2 reference plane, L3 reference plane, L4 signal** | Micro-section of the lot coupon | QA + programme |
| FB-05 | Outer copper | 1 oz / 35 um | Fabricator report | QA |
| FB-06 | Inner copper | 0.5 oz / 17 um | Fabricator report, confirmed on the micro-section | QA |
| FB-07 | Dielectric thicknesses | prepreg 0.200 / core 1.065 / prepreg 0.200, each +/- 10 % | Micro-section | QA |
| FB-08 | ENIG Au / Ni | 0.05-0.10 um / 3.0-6.0 um | XRF | QA |
| FB-09 | Minimum track | >= 0.20 mm at the narrowest conductor named in `kicad/EEG-CAR-01_RevB_DRC_report.txt`. The routing released for review measures 0.20 mm at its narrowest, and 36 of its 169 relaxed connections take a conductor narrower than the 0.25 mm preferred width. The report is the authority for which conductor is measured, and it is accepted for a fabrication release only under IQC-B15 | Optical comparator | QA |
| FB-10 | Minimum clearance | >= 0.20 mm | Optical comparator | QA |
| FB-11 | Electrode-net clearance | >= 0.35 mm to anything else | Optical comparator on two named nets | QA + programme |
| FB-12 | Via construction | **Through vias only**: 0.60 mm pad / 0.30 mm finished hole, tented both sides, no blind, buried, back-drilled, filled or plugged vias | Pin gauge, visual, micro-section | QA |
| FB-13 | Plated hole sizes | 0.30 (vias) / 0.90 / 1.00 / 1.20 / 1.70 mm, +/- 0.08 mm | Pin gauges | QA |
| FB-14 | NPTH 3.2 mm at MH1-MH4 | Positions (5,5), (145,5), (5,125), (145,125) in design coordinates; 6 mm copper keep-out on all four layers | Callipers, visual | QA |
| FB-15 | NPTH 1.50 mm DIN retention posts x6 | No copper, no mask (ECO-EEG-012) | Visual x10 | QA + programme |
| FB-16 | Isolation keep-out | Per DSN-EEG-003 section 3.3, no copper on any of the four layers | Visual against fab drawing and inner-layer artwork | Programme + safety reviewer |
| FB-17 | Reference planes | AGND_REF left of x = 62 mm and DGND right of it, **on both L2 and L3**, stitched | Inner-layer artwork against the released Gerbers | Programme |
| FB-18 | Fiducials | Three, 1.0 mm copper in a 3.0 mm mask opening, at the section 1.1 positions | Visual, optical comparator | QA |
| FB-19 | J6-J7 row spacing | 22.86 mm +/- 0.10 mm (ECO-EEG-008) | Pin gauge or CMM | QA |
| FB-20 | Electrical test | 100 % to the IPC-D-356A netlist, 156 nets | IPC-9252 flying probe or bed of nails | QA |
| FB-21 | Internal annular ring | >= 0.025 mm, IPC-6012 class 2 | Micro-section (IQC-B11) | QA + programme |
| FB-22 | Layer-to-layer misregistration | <= 0.125 mm, derived in IQC-B12 | Registration report + micro-section | QA + programme |
| FB-23 | Plane continuity | <= 0.10 Ohm corner to corner within each plane region, both inner layers | 4-wire DMM through stitching vias | Programme |
| FB-24 | Plane separation | AGND_REF plane to DGND plane **>= 100 MOhm on the bare board, R90 not fitted** (TST-EEG-004 Rev C T0, which owns the limit) | Insulation tester at **250 V DC** | Programme |
| FB-25 | Bow and twist | <= 0.75 % | Surface plate | QA |
| FB-26 | Mask and legend | Green LPI both sides, white legend both sides, legible | Visual | QA |
| FB-27 | Marking | Fabricator date code and UL mark on the bottom legend, inside the outline, clear of all pads | Visual | QA |

**Assembled carrier**

| # | Characteristic | Requirement | Method | Signed by |
|---|---|---|---|---|
| FA-01 | Bill of material as built | 211 designators; 186 purchased placements of which 33 are through-hole; R89 not populated; R90, R91, R92, R93 per section 3 IP-4; R94 and R95 fitted (ECO-EEG-021) | Ref-by-ref against the released BOM | QA |
| FA-02 | Workmanship | IPC-A-610 class 2, no waivers | Visual + AOI (T1) | QA |
| FA-03 | R1-R16 value | **68 k** 0.1 % as fitted (ECO-EEG-024, applied in `tools/design.py` 2026-09-02), measured on 4 of 16 in circuit or on the reel sample. At this value S-02's single-fault DC current is **36.8 uA calculated against 50 uA and the limit is met**; the measured resistor value is recorded, and the E-10 band applied at TST-EEG-004 T22 follows from it (+/- 1.0 dB at 68 k, +/- 0.5 dB at 47 k). *Corrected 2026-09-02: was "47 k as fitted on the Phase 1 prototypes ... S-02 is not met at this value"* | 4-wire DMM | QA + programme |
| FA-04 | C1-C16 dielectric | C0G, part number GCM1885C1H103JA16D | Reel label, retained photograph | QA |
| FA-05 | D20/D40/D60 orientation | BAT54S pin 3 at the op-amp output (ECO-EEG-005); D1-D16 are BAV99 and are checked at IP-2 | Visual x10 | QA |
| FA-06 | V5V rail | 5.00 V, measured at TP16 | DMM | Test operator |
| FA-07 | AVDD / AVSS | +2.50 V / -2.50 V at TP10 / TP11 | DMM | Test operator |
| FA-08 | AGND_REF | Analogue mid-rail present at TP13, not tied to DGND anywhere but R90 | DMM + continuity | Programme |
| FA-09 | Envelope corner | f0 = 48.77 Hz *calculated*, Q = 0.7416 *calculated*, from R = 22 k, C_gnd = 100 nF, C_fb = 220 nF; AC-coupling corner 1.59 Hz *calculated* from 10 uF into 10 k (ECO-EEG-027), against E-11 restated as <= 2 Hz. Measured f0 recorded per unit at TP7, TP8, TP9 against **TST-EEG-004 T12e's 42 to 58 Hz**. **The 50 Hz +/- 10 % half of E-11 is not met by the fitted parts and this row does not grade it as met**: C21/C41/C61 and C22/C42/C62 are both X7R at 15 %, f0 goes as 1/sqrt(C1 C2), so a common 15 % moves it to 42.4 to 57.4 Hz -- a spread wider than the +/- 10 % E-11 asks for wherever the centre sits. T12e's 42 to 58 Hz is the band this package sets against the parts it approved; it is not a widened E-11 limit, because no f0 limit existed to widen (TST-EEG-004 section 16 item 16, RFQ-EEG-001 Rev E section 12 item 15). The measured value is what the record carries | Swept sine | Test operator + programme |
| FA-10 | Comparator threshold | 52 mV *calculated*, hysteresis ~5 mV *calculated*; measured value recorded (E-12). Record which comparator configuration was built: `design.py` Rev B powers U7 from AVDD/AVSS, and ECO-EEG-023 re-powers it from DVDD3V3/DGND with the inputs re-referenced to a DVDD3V3/2 divider and the envelope AC-coupled into it. **ECO-EEG-023 is not in the released design.py and must be checked by the safety and layout reviewer before it is cut in** | Ramp at the ENV_STIM node | Test operator + programme |
| FA-11 | Input network loss at 100 Hz | **0.75 dB** *calculated* at the fitted **68 k** / 10 n; measured value recorded against E-10's **+/- 1.0 dB** branch. At the superseded 47 k the loss was 0.36 dB against +/- 0.5 dB. *Corrected 2026-09-02: ECO-EEG-024 is applied and the two figures have swapped roles.* The arithmetic is in RISK-EEG-011 section 4 and is not repeated here | Swept sine through the T7 fixture | Programme |
| FA-12 | Noise floor | **0.31 uV RMS** *calculated* at the fitted 68 k (0.27 uV at the superseded 47 k), both against the 1.0 uV limit of E-03; measured per T8. *Corrected 2026-09-02 to name the fitted value first.* | TST-EEG-004 T8 | Test operator |
| FA-13 | Test access | TP1-TP18 present and probeable, and the 1x6 UART debug header at J26 fitted, way 6 being the spare NC_GPIO0 because GPIO0 is committed to LED_SR_LATCH (E-28, ECO-EEG-009). No JTAG connector is fitted and none is required | Visual + probe | QA |
| FA-14 | Full TST-EEG-004 record | Every step, every numeric value | TST-EEG-004 Rev C | Test operator + QA |

**Harness and kit**

| # | Characteristic | Requirement | Method | Signed by |
|---|---|---|---|---|
| FH-01 | Electrode cable | 12 conductors, screened, to J14; from-to per WH-EEG-008 | Continuity, conductor by conductor | QA |
| FH-02 | Light cable | 10 conductors to J30 | Continuity | QA |
| FH-03 | Screen | Continuous, landed at the pod end only (R91) | Continuity + insulation resistance | QA |
| FH-04 | Insulation resistance | Conductor to conductor and conductor to screen, at the voltage stated in WH-EEG-008 | Insulation tester | QA |
| FH-05 | Barrier insulation, per unit | **500 V DC insulation resistance across the isolation barrier.** There is no per-unit hipot: the 2.5 kV RMS type test is the module supplier's certificate, checked once at incoming inspection | Insulation tester | QA + programme |
| FK-01 | Helmet fit | Adjustment range and electrode positions per DSN-EEG-002 Rev E | Headform gauge | QA |
| FK-02 | Pod | Closed, gasketed, no gel path, no indicator opening (M-02 withdrawn) | Visual | QA |
| FK-03 | Label | Serial, hardware revision, key fingerprint, "research instrument -- not a medical device", programme URL (M-03) | Read back and compare with the calibration record and the USB iSerial from T5 | QA + programme |
| FK-04 | Case and foam | Cut-outs match every item; labels legible (M-05, M-06); the printed calibration certificate in the case lid pocket beside the quick-start card | Pack and unpack once | QA |
| FK-05 | Packing list | Every line ticked (T18) | Tick sheet | QA |
| FK-06 | Consumables | Quantities per A-05; expiry dates recorded. A-03 is the chin strap HM-06 and the occipital yoke HM-03, not a headband | Count | QA |
| FK-07 | Cell | Installed cell lot and OCV recorded; **no spare cell in the case**, per PKG-EEG-015 section 7 | Record | QA + programme |

---

## 5. Sampling: what it is for, and what it is not for

At 2, 10, 25 and 50 units, **sampling the assembled units makes no sense and is not
practised**. Every unit gets every step of TST-EEG-004, plus the label and packing checks.
The arithmetic is plain: under ISO 2859-1 / ANSI-ASQ Z1.4 general inspection level II, a lot
of 10 at AQL 1.0 sends you to a sample size larger than the lot itself, and a sample of 13
from a lot of 10 costs more to administer than testing all 10. Two further reasons make
100 % test the right choice here independently of cost: the per-unit numbers from T7, T8,
T9, T10, T12, T13 and T17 are *study metadata* that must travel with each instrument, so
they have to be produced for every unit anyway; and a fleet of 25 to 50 units has no
statistical population to speak of.

Sampling is therefore used for exactly three things:

1. **Consumables and multi-piece accessories** bought by the hundred or thousand, where
   100 % inspection is genuinely wasteful (section 6).
2. **Reel-level and lot-level characteristics** of passives, where the reel is the unit of
   quality, not the piece. The four-layer coupon characteristics of IQC-B11 and IQC-B12
   belong to the same class: the fabrication lot is the unit of quality, because
   registration is a property of the press cycle and not of the individual board.
3. **Destructive or slow measurements** -- electrode DC offset and drift, cell internal
   resistance, print coupon dimensions, the inner-layer micro-section -- where measuring
   every piece would consume the piece or the schedule.

---

## 6. AQL plans for the fleet builds

The named standard is **ISO 2859-1 / ANSI-ASQ Z1.4, general inspection level II**, so that a
manufacturer can operate it with the tables they already have. Where a plan is stated below,
the programme uses **zero-acceptance (c = 0)** plans and derives the sample size from the
binomial directly, so the plan can be checked without a table:

> n = ln(0.10) / ln(1 - RQL), rounded up.
> Accept on 0 defects, reject on 1. RQL is the fraction defective at which the lot is
> accepted with only a 10 % probability.

| Class | Defect examples | RQL | n (calculated) |
|---|---|---|---|
| Critical | Anything affecting S-01 to S-08: a bridged isolation barrier, copper inside the keep-out on any of the four layers, an unprotected electrode lead, a cell without a UN 38.3 report, a missing protection resistor | -- | **100 %, accept on 0.** Sampling is not used for critical characteristics |
| Major | Function-affecting: wrong dielectric, wrong header pinout, mis-cut foam, missing consumable line, illegible label | 5 % | 45 |
| Minor | Cosmetic: legend smudge, dye variation on a printed part, scuffed case | 10 % | 22 |

Applied to the fleet builds:

| Item | Qty at 10 kits | Qty at 25 | Qty at 50 | Plan |
|---|---|---|---|---|
| Sintered Ag/AgCl cup electrodes | 100 | 250 | 500 | 100 % visual; **n = 45, c = 0** for DC offset and drift |
| Ag/AgCl ear clips | 20 | 50 | 100 | 100 % visual; n = 22 for offset |
| HM-04 electrode bodies (printed) | 100 | 250 | 500 | n = 45 dimensional against FIT-01 (bayonet, collar); 100 % visual for powder residue |
| Electrode springs 3-6 N | 100 | 250 | 500 | n = 22 force check |
| Disposable EMG snap pads | 300 | 750 | 1500 | n = 22, plus 100 % expiry-date check on the packs |
| Saline wipes, paste, prep gel | 10-20 packs | 25-50 | 50-100 | 100 % expiry-date check; n = 22 on pack integrity |
| Headphones | 10 | 25 | 50 | **100 %** functional -- the calibrated output level is only transferable if the model is identical (A-04, restated as 32 to 64 Ohm) |
| USB cables, EU chargers | 10-20 | 25-50 | 50-100 | n = 22 functional; 100 % CE marking check |
| Travel cases and foam inserts | 10 | 25 | 50 | 100 % against the CASE-00 cut file; the foam is the item most likely to be wrong |
| 0603 passives | reels | reels | reels | Reel label 100 %; 5 pieces measured per reel |
| Bare-board fabrication lots | 1-2 lots | 2-3 | 3-5 | Lot coupon 100 % for IQC-B11 to IQC-B13; dimensional rows n = 2 boards per lot |

### 6.1 Switching rules

Normal inspection is the default. Switch to **tightened** (RQL halved, so n = 91 for major
and n = 45 for minor) when 2 of 5 consecutive lots are rejected on the same characteristic.
Switch back to normal after 5 consecutive lots accepted under tightened inspection. **Reduced
inspection is not used.** State plainly: with three or four production lots in the entire
programme, the switching rules will rarely fire. They are written down so that a repeated
defect cannot be normalised, not because the programme expects to run them.

---

## 7. Non-conforming material

### 7.1 Failure codes

Codes are keyed to the test that found the fault, so that first-pass yield can be reported
per step. The code is **F-T<nn>**, where nn is the step number in TST-EEG-004 Rev C. That
document owns the step numbers and their names, and they are not restated here; a code is
only valid if the step exists in TST-EEG-004 Rev C. IQC failures take the code
**F-IQC-<row>**, using the row identifiers of section 2 -- for example F-IQC-B12 for a
misregistered fabrication lot.

### 7.2 Disposition

| Disposition | When it applies | Limits |
|---|---|---|
| Re-seat and re-test | Module seating and keying faults only | Maximum 2 insertion cycles; cycles logged against the socket |
| Rework and re-test | A single joint or a single passive | Maximum 2 hand-rework cycles per site, IPC-7711/7721. R1-R16 re-measured for 0.1 % after any rework. More than 2 rework sites in the analogue zone (x < 62 mm) sends the board to scrap |
| Module replacement | Any module fault | **Mandatory full re-run of T7, T8, T9, T10 and re-write of the calibration constants.** A module may never be swapped after provisioning without re-characterisation |
| Quarantine, no rework | Any isolation-barrier damage near J10; any DIN socket (J15-J17) rework; a dropped or deformed cell; a suspected counterfeit ADS1299; any bare board that failed IQC-B11, B12 or B13, because an inner-layer defect cannot be reworked | Escalated to the programme; feeds RISK-EEG-011 |
| Scrap | Board fails the above limits, or fails the bare-board electrical test | Scrap authority: manufacturer QA manager |
| Use as is / concession | **Prohibited** for T7, T8, T9, T10, T13, for any four-layer characteristic in IQC-B11 to B13, and for any S-requirement failure | Any other concession needs the programme technical lead's written approval, an expiry date and an ECO number |

### 7.3 Material review board

Composition: manufacturer QA manager (chair), manufacturer process engineer, programme
quality lead. Any deviation affecting a value recorded in the calibration record is escalated
to the programme technical lead. Re-test rules: a unit may be re-tested at most twice on the
same step; the second failure raises a non-conformance report. **Every attempt is retained in
the record. Results are never overwritten.**

### 7.4 Records and delivery

Failed units' records are delivered with the batch, carrying the failure code and the
disposition. The lot summary reports first-pass yield per test step, so that the programme can
see which step drives yield before scaling from 10 units to 50.

---

## 8. Corrective action

A corrective action is raised on: any critical-characteristic escape; any repeat of the same
failure code on 3 units in one lot; any lot rejection at IQC; any customer (programme)
complaint after delivery; and any field return whose root cause is a build fault.

The route is an 8D-style report, on one page:

1. Team and contact.
2. Problem statement with the failure code, serials affected and the number found.
3. Containment: what is quarantined now, and how far back the suspect population reaches
   (state the serial range).
4. Root cause, with the evidence. "Operator error" is not accepted as a root cause without a
   process reason behind it.
5. Chosen corrective action.
6. Verification that the action works, with data.
7. Preventive action: the process change, the ECO number if a document or the design changes.
8. Closure, signed by the manufacturer QA manager and the programme quality lead.

Target: containment within 2 working days of raising, root cause within 10, closure within
30. Any corrective action touching a risk-control component or the isolation architecture
re-triggers the electrical safety review of RFQ section 9.2 before further units ship.

---

## 9. Device history record (DHR)

One record per programme serial. The label artwork is carried in PKG-EEG-015 section 5 and
the change register in ECO-EEG-016; the definitions below are the ones this plan records
against, so that the label, the record and the firmware agree.

- **Programme serial:** `TIOV-B-nnnn` -- programme prefix, hardware revision letter, four
  digits. Phase 1 uses 0001-0009, Phase 2 0010-0099, Phase 3 0100-0999. Serials are
  allocated by the programme in blocks and issued with the purchase order. The same string
  appears in the label text, the Data Matrix, the USB `iSerialNumber`, the calibration
  record and the packing list; if any two disagree the unit is quarantined.
- **ATECC608B device serial:** the 9-byte factory serial, read at boot, recorded in the
  device history record and printed on the label. It is **not** written into the USB
  `iSerialNumber`; that field carries the programme serial `TIOV-B-nnnn` alone (F-04,
  RUL-EEG-021 section B). The two are checked against each other at T5b.
- **Key fingerprint:** as defined in FW-EEG-001 section 7. The definition is not repeated
  here. This is what T6 records and what T16 and the label are checked against.

### 9.1 What is filed per serial, at build

| Group | Content |
|---|---|
| Configuration | Purchase order; BOM revision built to; design.py / Gerber revision and the DRC report reference; ECO numbers applied; firmware image version and SHA-256 hash |
| Material | Bare board fabrication lot and date code, with the micro-section and registration report references for that lot; ADS1299 module #1 and #2 vendor lot **and** TI device date code and lot; ADuM4160 module lot and isolation certificate reference; ATECC608B factory serial; cell lot, OCV at goods-in and UN 38.3 report reference; R1-R16 reel lot; C1-C16 reel lot |
| Process | Reflow profile record; ESD log for the shift; operator identities; station identity |
| Test | The complete TST-EEG-004 record, every numeric value, including failed attempts; test-equipment asset numbers and calibration certificate references |
| Provisioning | Provisioning log; exported public key; fingerprint; VID/PID and hardware revision written. **eFuses are not burned on Phase 1 prototypes**: secure boot and flash encryption are enabled from Phase 2, so the Phase 1 units run unsigned images and T25 is a Phase 2 step, not a Phase 1 gate |
| Release | FAI report reference (first unit of the batch); deviations and concessions applied; final assembly and packing check; dispatch record |

### 9.2 What is added per turnaround

Refurbishment record per SVC-EEG-013; parts replaced with their lots; cell cycle count and
OCV; disinfection record; re-test results if any; the participant assignment period (held by
the programme only, and kept separate from the manufacturer's copy for data-protection
reasons).

### 9.3 Where it lives and for how long

| Copy | Held by | Format | Retention |
|---|---|---|---|
| Master | TI One Voice programme, Brussels | Machine-readable calibration record (one file per unit) plus the scanned paper pack | Life of the fleet **plus 10 years** |
| Manufacturer copy | Manufacturer | Their own QMS format | 7 years from dispatch, minimum |
| Delivery copy | Travels with the unit, in the case lid pocket | Printed calibration record | Life of the unit; reissued at each refurbishment |

Acceptance in Brussels (RFQ section 9.3) is conditional on receipt of the per-unit record.
A batch delivered without records is not accepted.

---

## 10. Traceability

RFQ-EEG-001 section 10 requires "date code and lot for the two converters and the cell
recorded per unit". This plan states how.

| Item | What is recorded | How it is captured | Where it goes |
|---|---|---|---|
| ADS1299 module #1 (J1/J2/J23) | Module vendor, module board revision, module lot; TI ADS1299 package marking, date code and lot; a photograph of the marking | At IQC, before the module is fitted | DHR, material group |
| ADS1299 module #2 (J3/J4/J29) | As above | As above | DHR |
| Protected 18650 cell | Cell manufacturer, cell lot, OCV at goods-in, UN 38.3 report reference | At IQC | DHR + PKG-EEG-015 shipping file |
| ADuM4160 module | Vendor, module lot, isolation certificate reference, host connector type and whether WH-09 is fitted | At IQC | DHR |
| ATECC608B | Factory 9-byte serial | Read over I2C at IQC and again at provisioning; both recorded | DHR + label |
| Bare board | Fabrication lot and fabricator date code from the bottom legend; micro-section, registration and plane-continuity report references for the lot | At board goods-in | DHR |
| R1-R16, C1-C16 | Reel lot codes | At kitting for SMT | DHR |
| Firmware | Image version and SHA-256 | At flashing, over the DevKit's own UART USB-C port | DHR + calibration record |

The record must be able to answer, without opening a box: which units carry a given ADS1299
lot; which units carry cell lot X; which units came from a given bare-board fabrication lot;
which units are on firmware version Y; which participant had which unit and when. Those five
queries are the acceptance test for the DHR format. The fabrication-lot query is new in Rev B
and exists because an inner-layer defect is invisible from outside the board, so the only way
to bound a suspect population is by press lot.

---

## 11. Supplier quality and change notification

### 11.1 Supplier classes

| Class | Items | Requirements |
|---|---|---|
| **A** -- safety or characterisation critical | ADuM4160 module (J10); ADS1299 modules (J1-J4); protected 18650 cell; sintered Ag/AgCl cups and ear clips; DIN 42802 sockets J15-J17; the EU charger; the bare-board fabricator | Named vendor and part number; controlled revision; schematic or dimensioned drawing; certificate of conformity per lot; **change notification 90 days before any board revision, process change or site move**; isolation rating certificate for J10; ISO 10993 declarations for skin-contact items; for the fabricator, the stack-up and registration process are part of the controlled configuration and may not change without notification |
| **B** -- function critical | The remaining module types; print bureau; travel case and foam; headphones | CoC per lot; change notification before any revision; part number pinned |
| **C** -- commodity | Passives, socket strips, fasteners, consumables | CoC; traceable lot codes for R1-R16, C1-C16 and D1-D16 |

### 11.2 Rules that fall out of this

- The permissive language in the v1 kit BOM -- "Chinese equivalent", "generic", "certified
  generic", "generic ADS1299 breakout with same header pinout" -- is superseded. Every line
  in AVL-EEG-017 Rev B is either a named approved part or an explicit open-with-criteria
  entry that states the criteria.
- **J15 to J17 have no confirmed part and that is a live procurement risk.** `design.py`
  names Stäubli SLB1,5-F / LB-I1,5 as a class, not a confirmed PCB part. A touch-proof
  1.5 mm socket with a PCB-mount signal pin and two 1.5 mm retention posts must be sourced
  and first-articled before Phase 2. The criteria are: touch-proof 1.5 mm to DIN 42802,
  finger-safe per IEC 60601-1, colour-coded, stated current rating and mating force, and a
  sample submitted to the programme for approval. AVL-EEG-017 carries a 12-week lead-time
  risk against it.
- The four parts RFQ section 10 declares non-substitutable -- the two ADS1299 modules, the
  ATECC608B breakout, the ADuM4160 module and the ESP32-S3-DevKitC-1 -- may not be changed by
  any route other than a substitution request approved by the programme technical lead and
  issued as an ECO. ICD-EEG-006 names only two of the four; RFQ-EEG-001 Rev E sits above
  ICD-EEG-006 in the precedence order and all four apply.
- **Counterfeit avoidance for the ADS1299.** Purchase only through the module vendor or an
  authorised TI distributor with a documented chain. No broker or open-market purchases. The
  date code and lot are retained per unit (section 10). A T7 gain or T8 noise outlier is
  treated as a possible counterfeit indicator and quarantined, not reworked. X-ray is
  retained for Phase 1; its scope is open (section 14.2).
- **Substitution request form:** the part, the proposed alternate, the reason, a datasheet
  comparison against every affected E-nn / S-nn requirement, the test evidence, the impact on
  RISK-EEG-011, the programme's approval signature, and the resulting ECO number.

---

## 12. Gauge R&R for the gain and noise measurements

T7 (gain within 0.5 % at the 1 mV point) and T8 (noise <= 1.0 uV RMS) produce the study's
primary instrument characterisation. If the measurement system is not capable, unit-to-unit
differences in the record are fixture drift and operator technique, which is precisely the
confound RFQ section 9 exists to avoid.

### 12.1 Study design

Three units x three operators x three repeats, run on the first production fixture set
FIX-01 to FIX-04 of JIG-EEG-009, before the first fleet batch, and repeated whenever a
fixture is rebuilt or a second set is introduced. Reported as %GRR against the tolerance
band, where %GRR = 6 sigma divided by the full width of the band. **Requirement: %GRR
<= 20 %.**

### 12.2 What the arithmetic already says about T7

The estimator itself has a floor. For a sinusoid of amplitude A measured by coherent
detection over T seconds against a white noise density n, the standard deviation of the
amplitude estimate is `sigma = n / sqrt(2T)`. Taking E-03's 1.0 uV RMS over the 0.5-70 Hz
band gives n = 0.120 uV/sqrt(Hz), and at T = 60 s, sigma = **0.0110 uV (1 sigma)**. The
expanded uncertainty at **k = 2** is 0.0219 uV. JIG-EEG-009 section 1.4's derivation
governs; the v1 audit and Rev A of this plan quoted 0.219 % at the 10 uV point as a
1 sigma figure, and that label was wrong -- 0.219 % is the k = 2 value and 1 sigma is
0.110 %. All *calculated*:

| T7 point | Applied amplitude | 1 sigma at 60 s | U at k = 2 | 6 sigma | Limit | %GRR from the noise term alone |
|---|---|---|---|---|---|---|
| 1 mV | 1000 uV | 0.0011 % | 0.0022 % | 0.0066 % | +/- 0.5 % | 0.7 % |
| 100 uV | 100 uV | 0.011 % | 0.022 % | 0.066 % | +/- 0.5 % | 6.6 % |
| 10 uV | 10 uV | 0.110 % | 0.219 % | 0.657 % | +/- 0.5 % | **66 % -- not capable** |
| 10 uV | 10 uV | 0.110 % | 0.219 % | 0.657 % | +/- 5 % | 6.6 % |

So T7's gain figure as written cannot be measured to 0.5 % at the 10 uV point in a 60 s
record, however good the fixture is. Lengthening the record to 240 s only halves sigma
(0.055 %, 6 sigma = 0.33 %, still 33 % and still above the 20 % requirement). **The plan
therefore splits T7:**

- The **released gain constant** per channel is taken at the 1 mV point, limit +/- 0.5 %.
- The 100 uV point is a linearity check, limit +/- 0.5 %.
- The 10 uV point is a linearity check with a limit of **+/- 5 %**, which gives %GRR = 6.6 %
  from the noise term and leaves room for the fixture.

The +/- 5 % limit is the ruled value for the 10 uV point. TST-EEG-004 T7 and JIG-EEG-009
sections 1.4 and 7 carry +/- 2 % and are corrected to +/- 5 % by ECO against TST-EEG-004.
This is a change to TST-EEG-004 and does not weaken the instrument specification; it stops
the line from measuring something it cannot measure.

### 12.3 T8 noise

The RMS estimate over a 60 s record in a 69.5 Hz band has about 2 x 69.5 x 60 = 8340 degrees
of freedom, so its relative standard deviation is 1/sqrt(2 x 8340) = **0.77 % of reading**
(*calculated*) -- negligible against the 1.0 uV limit. The real repeatability term is the
fixture and the environment: mains pick-up into a shorted-input jig, and the operator's
cable dress. That term has never been measured and must come out of the study, not out of
arithmetic. A guard band applies: any channel reading above **0.85 uV** is re-tested with the
unit inside a screened enclosure before it is failed.

### 12.4 Golden unit and fixture control

- Unit **TIOV-B-0001** is retained by the programme as the golden unit and is re-measured
  on the production fixtures at the start of every build lot. Where another document names
  the golden unit differently, this serial and the format of section 9 govern.
- Its T7 gains, T8 noise and T10 offsets are the fixture's control chart. **Gain drift
  > 0.2 % or noise drift > 0.15 uV halts the line** until the fixture is investigated.
- Fixture self-test at shift start: divider ratio against a 6.5-digit DMM, the three
  reference resistors (**4k99, 10k0 and 49k9**, the E96 parts FIX-01/A actually switches --
  JIG-EEG-009 Rev B section 0.1 and TST-EEG-004 Rev C T10 name the same three), continuity
  of all 12 J14 pins and the three DIN plugs. Logged. *Was: "5 k, 10 k, 50 k"* -- a rounding
  of the fitted parts, and one that does not stay harmless at the top of the range:
  RISK-EEG-011 Rev B H-24 records that 49k9 read through 47 kOhm and the 10 nF shunt gives
  **92.5 kOhm**, which is not the reading a true 50 k reference would produce, so a self-test
  written to the rounded name checks the fixture against the wrong number. *Corrected
  2026-09-02: the series value is now the **68 kOhm** of ECO-EEG-024, so the same point reads
  **111.5 kOhm** (TST-EEG-004 T10). The point about the rounded name is unchanged; the number
  it is made with has moved, and RISK-EEG-011 H-24 has not yet been restated.*
- Test equipment on a 12-month traceable calibration: DMM, function generator, current shunt,
  **47.0 Ohm acoustic load** matching the shipped ATH-M20x (A-04 restated as 32 to 64 Ohm,
  and the calibrated output level measured per model), artificial ear for the E-29 type test,
  **500 V DC insulation-resistance tester** for FH-05, leakage measuring device, RF receiver,
  and the FIX-01/E colorimeter head used for the contact-light step. **There is no per-unit
  hipot station**: the 2.5 kV RMS type test is the isolator supplier's certificate. Asset
  numbers are recorded in every unit's calibration record, so that a drifting instrument can
  be traced back to the units it touched.
- Operator qualification: IPC-A-610 class 2 certification for assembly operators; a named,
  trained operator for the provisioning and test station.

---

## 13. First-delivery audit checklist

The programme performs this once, on the first delivery of each phase, at goods-in in
Brussels, against the shipped units and the shipped records. It is a document and product
audit, not a site audit; a site audit is not required for this programme.

| # | Question | Evidence | Pass criterion |
|---|---|---|---|
| A-01 | Is there an IQC record for every lot in the build? | IQC pack | One closed record per lot, none open |
| A-02 | Are the ADS1299 date codes and lots recorded per unit? | DHR | Present for both modules on every unit (RFQ section 10) |
| A-03 | Is the cell lot and its UN 38.3 report reference recorded per unit? | DHR | Present on every unit |
| A-04 | Is the ADuM4160 isolation certificate on file? | Supplier pack | Present, >= 2.5 kV RMS, matching the module part number |
| A-05 | Were the six DIN retention NPTH holes unplated? | Bare-board FAI, boards in hand | Bare laminate, no mask, on every board inspected |
| A-06 | Is the isolation keep-out clear of copper, solder and flux, on all four layers? | Photograph per board + inner-layer artwork + inspection of 2 units | Clear |
| A-07 | Are R90 and R91 each fitted exactly once, with no wire bridge? | Inspection of 2 units | Confirmed |
| A-08 | Is C1-C16 C0G, not X7R? | Reel photographs + DHR | GCM1885C1H103JA16D or an approved ECO |
| A-09 | Does the FAI report exist and is it approved? | FAI Forms 1-3 | Signed by the programme technical lead before the batch |
| A-10 | Does every unit have a complete TST-EEG-004 record with actual values? | Calibration records | No blanks, no "pass" in a numeric field |
| A-11 | Are failed attempts retained, not overwritten? | Records | Retest history visible |
| A-12 | Is first-pass yield reported per test step? | Lot summary | Present |
| A-13 | Do the label, the calibration record and the USB iSerial agree on 2 sampled units? | Read back on the bench | Identical serial in the `TIOV-B-nnnn` form, and identical fingerprint |
| A-14 | Was the golden unit re-measured at the start of the lot? | Fixture log | Present, within the drift limits |
| A-15 | Is the fixture self-test logged for every shift in the build? | Fixture log | No gaps |
| A-16 | Are the test instruments in calibration, with asset numbers in the records? | Certificates | All in date |
| A-17 | Is there an ESD log for every shift in the build? | ESD log | Present, EPA verified |
| A-18 | Were any deviations or concessions applied, and were they approved? | NCR / concession file | Every one carries a programme signature and an ECO number |
| A-19 | Are open NCRs closed or dispositioned? | NCR register | None open against delivered units |
| A-20 | Do the units match the released configuration? | As-built record vs the document register | BOM revision, Gerber revision, firmware hash all match |
| A-21 | Does the kit content match the packing list, on 2 sampled kits? | Unpack | Every line present, foam cut-outs correct (M-06), calibration certificate in the lid pocket |
| A-22 | Is the delivery free of a spare cell? | Unpack | No spare cell in the case (PKG-EEG-015 section 7) |
| A-23 | Is there a micro-section, a registration report and a plane-continuity result for every bare-board lot in the build? | Fabricator pack + IQC pack | Present per lot; four layers in the right order, internal annular ring >= 0.025 mm, misregistration <= 0.125 mm |

A finding at A-05, A-06, A-07, A-08 or A-23 stops acceptance of the whole delivery. Findings
elsewhere are raised as corrective actions under section 8.

---

## 14. Records, and what is still open

### 14.1 Records this plan creates

| Record | Owner | Retention |
|---|---|---|
| IQC record per lot, including the four-layer coupon results | Manufacturer | 7 years |
| FAI Forms 1-3 per phase | Manufacturer, approved by the programme | Life of the fleet + 10 years |
| In-process tick sheets, AOI reports, ESD log, reflow profiles | Manufacturer | 7 years |
| TST-EEG-004 record and calibration record per serial | Both | Life of the fleet + 10 years (programme copy) |
| NCR, MRB minutes, concessions | Both | Life of the fleet + 10 years |
| Corrective action reports | Both | 7 years |
| Gauge R&R study, golden-unit control chart, fixture logs | Both | Life of the fleet |
| Device history record | Programme master | Life of the fleet + 10 years |

### 14.2 Open items

> **Not yet decided or not yet possible.** These are stated here rather than papered over.
>
> 1. **No safety engineer has reviewed this design.** The electrical safety review named in
>    RFQ section 9.2 has no appointed reviewer. Rows FB-16, FA-10, A-04 and A-06 above are
>    written so that the evidence exists when a reviewer is engaged, but no sign-off can be
>    claimed until then. This blocks use on a person; it does not block fabrication or
>    quoting. The move to four layers and the ECO-EEG-023 comparator change are both
>    specifically in that reviewer's scope.
> 2. **No hardware has been manufactured or measured.** Every design value in Form 3 marked
>    *calculated* -- 48.77 Hz, Q 0.7416, 1.59 Hz, 52 mV, and, at the 68 k of ECO-EEG-024,
>    0.75 dB and 0.31 uV -- is a calculation from design.py and has never been observed on
>    hardware. *Corrected 2026-09-02: the loss and noise figures listed here were the 47 k
>    pair, 0.36 dB and 0.27 uV.* The firmware image in `firmware/release/` is the one thing in
>    the package that has been built, and it has run only under QEMU emulation. The FAI is the first
>    occasion on which any of them becomes a measurement.
> 3. **S-02 is met in the design, and the sign-off is what is still open.** *Corrected
>    2026-09-02.* ECO-EEG-024 is applied in `tools/design.py`: R1-R16 are 68 kOhm, so the
>    single-fault DC current through one protection resistor is **36.8 uA calculated against
>    the 50 uA limit**, the corner moves to 234 Hz and E-10 sits at the +/- 1.0 dB branch it
>    already carried. Rev B's "S-02 is not met as built ... 53.2 uA ... the Phase 1
>    prototypes are built at 47 kOhm" is superseded on that date; the resistor changed in the
>    design before any prototype was built. **What is open**: the figure is calculated and no
>    unit exists to measure it on, and the electrical safety reviewer of item 1 owns the
>    disposition and has not started. S-02 stays a safety-reviewer item; it is no longer a
>    stated non-conformance.
> 4. **The S-04 thermistor is not met and stays not met, and it takes half of E-23 with it.**
>    There is no NTC net in design.py and no thermistor way on J12 or J13, so nothing on the
>    carrier can read the cell temperature. **E-23's 45 C charge inhibit is therefore not met
>    and cannot be tested either**; E-23's other half, thermal regulation inside the charger
>    IC, is met on the module, and the two halves must always be stated together. The two
>    hardware holes are the same hole. No closure is proposed. This is an open hardware item
>    carried in DSN-EEG-003 section 11, RISK-EEG-011 and RFQ-EEG-001 Rev E section 12 item 3,
>    and IQC cannot inspect its way round it.
> 5. **E-24 is not met.** The named isolator module presents a USB-B host receptacle where
>    E-24 asks for USB-C. The interim answer is the WH-09 USB-B to USB-C panel pigtail, and
>    it stays a live non-conformance until an isolator module with a USB-C host connector is
>    qualified. The host connection is a socket in a gasketed aperture, not a captive cable;
>    the captive lead through a gland is a Phase 2 item.
> 6. **The boom preamplifier part is not settled.** The MAX9814 is not approved because its
>    AGC is forbidden by E-14; a fixed-gain part of the MAX4466 class is preferred; the
>    module is specified by interface in ICD-EEG-006 until one is bought and measured.
>    IQC row "boom preamplifier module" is written against that interface, not against a
>    part number.
> 7. **The contact-light driver is written, and one of its states still cannot be reached.**
>    *Corrected 2026-09-02.* Rev B's "`lights_write()` and `lights_task()` are on/off only;
>    the bicolour phase scheme at 240 Hz is specified and not yet coded, so the contact-light
>    test step cannot pass" is superseded: `firmware/main/main.c` captures both halves of the
>    converter's lead-off status and derives a colour per site -- trips neither threshold
>    **green**, trips only the sensitive one **amber**, trips both **red** -- alternating the
>    two phases at about **250 Hz**, which is `LIGHT_PHASE_HZ` = 240 quantised to the FreeRTOS
>    tick and meets E-27's "above 100 Hz". TST-EEG-004 T11 is written against it. **Corrected
>    again 2026-09-02 (FW-D17):** this item read that the colour came from two detectors and
>    that `LOFF_SENSN` was never written, so red could never be set. Red is reachable now,
>    from a swept positive-side comparator threshold rather than from the N detector, which
>    this single-ended montage does not have. **What still gates lot release**: T11 has never
>    been run, because no unit exists; and the two `COMP_TH` settings are datasheet endpoints,
>    so the impedance boundaries between green, amber and red are not yet established
>    (TST-EEG-004 T11 Note 3). That is a firmware-owner item with E-27's owner, and no unit
>    is released against T11 until the boundaries are set and T11 has actually been run.
> 8. **The gauge R&R numbers in section 12 are the estimator floor only.** The fixture and
>    operator terms are unknown until the first study runs. If the measured %GRR at the 1 mV
>    point exceeds 20 %, the fixture is the problem and the limits are not to be relaxed to
>    make it pass.
> 9. **X-ray scope is open, and the two governing documents name different objects.**
>    RFQ-EEG-001 section 9.1 asks for X-ray of the module connectors on the Phase 1 units;
>    this plan and AVL-EEG-017 ask for X-ray of the converter packages. Neither appears as a
>    numbered step in TST-EEG-004 Rev C. Both are Phase 1 only. The programme has not decided
>    which object is inspected, whether it extends to the fleet, or whether a sampling plan
>    replaces it. Bidders should price both.
> 10. **Conformal coating: decided, and the decision is no coating.** The board is not coated
>     for Phases 1 and 2. It lives inside a gasketed enclosure, and coating a board with 30
>     connectors and a socketed DevKit costs more in masking than it buys. Nothing is applied
>     and nothing is inspected. Revisited before Phase 3 if a unit returns with corrosion.
>     Rev A of this plan recorded this as an open decision; it is not one.
> 11. **Panel fiducials remain the fabricator's.** The board itself now carries three
>     fiducials (ECO-EEG-020, rows IQC-B14 and FB-18) and the vision-teach workaround is
>     withdrawn. Panelisation is still the fabricator's choice (fabrication note 12), so
>     panel-level fiducials on the rails are theirs to add, and the FAI records what was
>     actually provided.
> 12. **eFuses are not burned on the Phase 1 prototypes.** Secure boot and flash encryption
>     start at Phase 2 so that the firmware volunteer can iterate on unsigned images. The
>     eFuse step is a Phase 2 gate and is not run on the two prototypes.
> 13. **The fabrication data is released for review, not for fabrication.** The Rev B DRC
>     report records zero violations: all 145 nets fully connected, every net one connected
>     copper island, both inner planes continuous under the analogue zone, and the isolation
>     strip free of copper on all four layers. Those are the three conditions ECO-EEG-016
>     section 3 sets for a fabrication-data release, and all three are met, so the data is
>     released for review under RFQ-EEG-002A. Boards still cannot be ordered against it: the
>     routing came from the programme's own tools, no human layout engineer has reviewed it,
>     and 169 of its connections close at the minimum conductor or the minimum gap rather than
>     the preferred 0.25 mm width. Row IQC-B15 is the inspection point, and the Rev B report
>     passes it.
