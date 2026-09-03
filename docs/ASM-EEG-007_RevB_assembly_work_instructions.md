# ASSEMBLY WORK INSTRUCTIONS -- EEG FIELD KIT

**Document:** ASM-EEG-007  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs.

**Revision note, Rev A to Rev B:** the carrier is now 150.0 x 130.0 mm and FOUR layers,
so the part and hole census, the IQC check, the reflow profiling and the stack-up note are
all recomputed from `tools/design.py`; the enclosure grew to match; end-of-line flashing
moves from J26 to the DevKitC-1's own UART USB-C port; the standoff, the module count, the
socket-family list, the serial-number format, the host USB connection and the ICD
cross-references are corrected; the fiducial and E-28 open items are closed and replaced by
the open items that the layout work actually produced.

**Corrections within Rev B, 2026-09-02: this document is brought into line with the released
POD-P1-01 and HM-01 geometry.** Section 3.3's standoff, section 5.1 item 1's boss fixings,
item 3's harness entry, item 4's stack fixing and the stage 4 torque table all described a pod
that `tools/mech_gen.py` does not generate: the released base has eight Ø4.00 mm brass-insert
bores where this document expected Ø2.5 mm thread-forming pilots, two Ø12.50 mm cable-gland
harness entries where this document said there were none, and a carrier fixing that needs a
male-female standoff where section 3.3 bought a female-female one. **Where this document and
the released geometry disagree, the geometry is the fact and this document was wrong.** The
sizes and lengths the geometry needs are in `mech/HARDWARE_SCHEDULE.md`, generated from the
model by `tools/mech_gen.py`; the parts themselves are still to be chosen and that file says
so line by line. Section 4 gains the helmet end of the two umbilicals, which had no entry
geometry and no strain relief at all.

**Corrections within Rev B, 2026-09-02, after the design and firmware changes of that day.**
Two part values on the incoming-goods list changed and one open item closed, and the operator
must build to the new values: **R1 to R16 are 68 kΩ**, not 47 kΩ (ECO-EEG-024 applied, so
RFQ S-02 is met at 36.8 µA), and **C21, C41 and C61 are 10 nF C0G** with **C22, C42, C62 at
22 nF C0G** and their Sallen-Key resistors at **215 kΩ**, in place of the 100 nF X7R
compromise, so RFQ E-11 is met with the approved parts. Section 1.3, section 2's diode note,
section 4.3 and section 11 items 4 and 6 are restated for it, and **section 4.3's contact-light
phase driver now exists**. Build to the BOM and to `tools/design.py`, which govern: a board
stuffed with 47 kΩ or with 100 nF X7R is a board built to the superseded values.

**Corrections within Rev B, after the second cross-document audit of 2026-09-01: findings 1.7 and
4.2 are closed.** The routing result and the release status are now stated from
`kicad/EEG-CAR-01_RevB_DRC_report.txt` wherever the board is described -- zero DRC violations, all
145 nets connected, every geometric rule passing, the isolation strip clear on all four layers, and
169 connections the router had to relax to get there -- and the fiducial ruling is cited as
RUL-EEG-021 section A, the controlled rulings register, in place of the uncontrolled worksheet
`tools/RULINGS.md`.

## Why this document exists

The v1 package told a manufacturer what the kit contained and never told anyone how to
build one. There was no stencil specification, no reflow profile, no through-hole process,
no module fitting instruction, no bonding specification for the eight electrode assemblies,
no torque anywhere in the package, and no per-stage labour that a contract manufacturer
could quote against. A fourteen-agent audit of v1 listed those omissions as blocking. This
document is the answer: the complete build of one unit, in six stages, in the order an
operator performs them, with the tooling, the process parameters, the acceptance criteria
and the sign-off at each stage.

**Nothing in this package has been manufactured, and no safety engineer has reviewed this
design.** Every time in section 8 is an estimate derived from the part counts in
`tools/design.py`, not a measured standard, and every process parameter is a starting
envelope that the manufacturer confirms on the first article and reports back.

---

## 1. Scope, ESD, workmanship and tooling

### 1.1 Scope

This document covers the build of one complete EEG field kit from bare boards, purchased
modules, printed parts and bought-in mechanical items to a packed kit. It does not cover
the harness build (WH-EEG-008), the production test (TST-EEG-004 Rev C), the test fixtures
(JIG-EEG-009) or the packing list contents (PKG-EEG-015). It applies to Phase 1 (2
prototypes), Phase 2 (10 kits) and Phase 3 (10 to 40 further kits, 25 to 50 in total);
where the process differs by phase, both are stated.

| Stage | Title | Output |
|---|---|---|
| 1 | Carrier PCBA (EEG-CAR-01 Rev B) | one populated, inspected carrier |
| 2 | Module preparation and the MP-01 plate | one electronics stack |
| 3 | Helmet build (HM-01) | one wired, bonded helmet |
| 4 | Pod integration | one closed pod, Phase 1 POD-P1 |
| 5 | Firmware load and provisioning | one serialised, identified instrument |
| 6 | Final assembly, labelling and kit packing | one packed kit |

### 1.2 ESD controls

The instrument is a 16-channel high-impedance front end. An ESD-damaged ADS1299 input does
not fail the power-on or seating tests; it appears as a noisy channel at TST-EEG-004 T8
against a 1.0 uV RMS limit, or drifts later in a kit that circulates to twenty
participants. ESD control is therefore a build requirement, not a housekeeping preference.

| Control | Requirement |
|---|---|
| Programme | Manufacturer declares compliance with ANSI/ESD S20.20 or national equivalent and states its EPA arrangements in the quotation |
| EPA scope | Bare-board handling, all SMT and THT operations on EEG-CAR-01, module insertion, MP-01 assembly, firmware and provisioning, and every step of TST-EEG-004 |
| Personnel | Wrist strap through 1 MΩ, or heel straps on a dissipative floor, verified at shift start and logged |
| Ionisation | Ioniser over the module insertion bench and over the provisioning station |
| Packaging | Boards and modules move between operations in shielded (metallised) bags, not pink poly |
| Surface | Working surfaces 1e6 to 1e9 ohm to ground; charged surface potential below 100 V |

ESD-critical items on this build, by name: both ADS1299 modules, the ATECC608B breakout,
the ESP32-S3-DevKitC-1-N16R8, U1 to U3 (OPA4376AID, SOIC-14), U7 (TLV3201AIDBV), and the
finished carrier once modules are fitted.

Moisture sensitivity applies only to parts that pass through reflow. On this board that is
U1 to U3 (SOIC-14), U7 (SOT-23-5), the 21 SOT-23 diodes, F1 (1206) and the 127 0603
passives. No purchased module is ever reflowed, so no module is baked. MSL ratings and
floor life are carried per line in AVL-EEG-017; where a bag has been open beyond floor
life, bake per J-STD-033 before use and record it.

### 1.3 Workmanship standard

| Standard | Revision | Applies to |
|---|---|---|
| IPC-A-610 class 2 | Rev H | assembled board acceptance |
| IPC J-STD-001 class 2 | Rev H | the soldering process itself |
| IPC-7711/7721 class 2 | Rev C | rework and repair |
| IPC-A-600 / IPC-6012 class 2 | current | the bare board (fabricator's responsibility, verified at IQC) |

All three classes apply to this build and none of them is optional: IPC-6012 class 2 for
fabrication, IPC-A-600 class 2 for bare-board acceptance and IPC-A-610 class 2 for
assembly.

Four criteria are tightened beyond class 2 for this instrument, each for a stated reason.
The first two tighten an IPC workmanship criterion -- the J15 to J17 wetting goes past class 3
rather than only up to it -- and the last two are not IPC criteria at all, so no inspection
standard will catch them:

| Tightened item | Criterion applied here | Reason |
|---|---|---|
| J15, J16, J17 (DIN 42802, 1.70 mm barrels) | 100 % circumferential wetting on both sides. **Vertical fill stays at ≥ 75 %, which is what class 2 already asks of every barrel on this board -- the tightening here is the wetting, not the fill** | these three barrels carry the EMG electrode connection to a person (RFQ S-02) |
| U1, U2, U3 (OPA4376AID) | no voiding visible at AOI, no partial heel fillet | the envelope gain sets TST-EEG-004 T12 |
| R90 and R91 | no touch-up permitted; a re-flowed part is replaced | the star topology is a copper property and a re-worked link is not verifiable |
| R1 to R16 (**68 kΩ** 0.1 %, corrected 2026-09-02 from 47 kΩ by ECO-EEG-024) | correct value confirmed by measurement on the first article of each lot | a wrong value on all sixteen is a silent, systematic error (RFQ E-07, E-03) |

Two part-value points that no inspection standard catches, and that the buyer must not
substitute away:

- C1 to C16 are **10 nF C0G**, Murata GCM1885C1H103JA16D (ECO-EEG-019). An X7R part of the
  same value is not acceptable: its capacitance shift with temperature and bias moves the
  input corner -- **234 Hz with the 68 kΩ of ECO-EEG-024, corrected 2026-09-02 from the
  339 Hz this line carried at 47 kΩ** -- and shows up as a gain error at TST-EEG-004 T7.
- **Corrected 2026-09-02.** C21, C41 and C61 are **10 nF C0G**, Murata GCM1885C1H103JA16D --
  the same part as C1 to C16 -- with **C22, C42 and C62 at 22 nF C0G**, Murata
  GCM1885C1H223JA16D, and their Sallen-Key resistors at **215 kΩ**. Until that date these
  three positions were **100 nF X7R with a stated 15 % capacitance tolerance**, Murata
  GCM188R71E104KA57D, because a 100 nF C0G in 0603 at 50 V is not a stocked part, and this
  list called that a deliberate, recorded compromise under which **RFQ E-11's 50 Hz ±10 %
  half was not met with the approved parts**. The network stopped asking for 100 nF instead:
  scaling the capacitors down by ten and the resistors up by ten leaves f0 at 49.9 Hz and Q
  at 0.742, and C0G's ±5 % holds the corner inside **47.5 to 52.5 Hz**, so **E-11 is met with
  the approved parts**. Two consequences for the buyer and the operator. **X7R is not an
  acceptable substitute at these six positions**, for the same reason it is not at C1 to C16.
  And TST-EEG-004 still measures and records the corner per unit at **T12e against its 42 to
  58 Hz window**, which was written for the X7R part: that window is wider than the parts now
  need, it is not evidence that E-11 is met, and TST-EEG-004 owns its own tolerance. Build to
  the part numbers in the BOM and in `tools/design.py`, which govern.

### 1.4 Tooling list

| Item | Specification | Stage |
|---|---|---|
| Stencil | 0.12 mm laser-cut stainless 304, electropolished, top side only, tensioned frame; programme-owned tooling | 1 |
| Stencil printer | manual or semi-automatic, board support for 150.0 x 130.0 mm | 1 |
| Placement | pick and place with 0603 and 1.27 mm pitch capability and fiducial recognition, or a microscope and vacuum pen for Phase 1 | 1 |
| Reflow oven | forced convection, minimum 5 zones, profiling capability | 1 |
| Profiling recorder | 4-channel, K-type, with a sacrificial **four-layer** profiling board from the same fabrication lot | 1 |
| AOI | top-side, 0603 and 1.27 mm pitch, polarity capable | 1 |
| Soldering station | temperature controlled, 350 to 370 °C tip, ESD safe; 2.4 mm chisel for socket strips, 3.0 mm for DIN barrels | 1 |
| Selective solder | Phase 3 only; no pallet is needed, see 2.7 | 1 |
| Socket comb jig | holds J6 and J7 parallel at 22.86 mm; a manufacturing aid, not yet numbered (see 3.6) | 1 |
| Torque screwdriver | 0.2 to 1.2 N·m, calibrated, ±6 % | 2, 4 |
| Bonding fixture | eight-station HM-04 alignment fixture, from JIG-EEG-009 | 3 |
| Draw cord | 3.0 mm nylon, 1.5 m, with a threading eye | 3 |
| Force gauge | 0 to 200 N digital, for the bond pull-off sample and the strap anchor check | 3 |
| Heat-set insert tool | M3 brass inserts into PA12, 240 °C tip. **Required, not conditional**: every M3 thread in POD-P1 is an insert (5.1 item 1) | 4 |
| Drill and reamer, Ø12.5 mm | the two umbilical entries OE-1 and OE-2 through the HM-01 occipital shell floor, using HM-12 as the jig (4.1 step 5). Not needed once a parametric HM-01 prints the bores | 3 |
| Spanner, 17 mm | cable-gland locknuts, two in the pod and two in the helmet. Size assumed with the gland and confirmed with it | 3, 4 |
| Provisioning station | offline PC, Windows 11 or Ubuntu 22.04, Python 3.11, USB hub, barcode scanner | 5 |
| Label printer | thermal transfer, 50 x 25 mm matt polyester, Data Matrix capable | 6 |

JIG-EEG-009 owns fixture numbering and uses **FIX-01 to FIX-04** with sub-assemblies
FIX-01/A, FIX-01/B and so on. This document does not allocate a fixture number. The socket
comb of 1.4 and the retention bar of 3.6 are assembly aids that JIG-EEG-009 Rev B must
number; until it does, they are named by function here and that is an open item (section
11).

---

## 2. Stage 1 -- carrier PCBA, EEG-CAR-01 Rev B

### 2.1 What is on the board

From `tools/design.py`: **211 reference designators, 636 pads and 156 nets on a
150.0 x 130.0 mm four-layer board**. SMT is on the top side (L1) only and every
through-hole part is inserted from the top. L4, the solder side, carries copper and legend
only, which is the single most useful fact in this stage: there is nothing on the solder
side to mask, so selective soldering needs no pallet.

| Group | Count | Pads |
|---|---|---|
| 0603 resistors | 72 | 144 |
| 0603 capacitors | 54 | 108 |
| 0603 ferrite (L1) | 1 | 2 |
| 1206 PTC (F1) | 1 | 2 |
| SOT-23 (D1 to D16, D20, D40, D60, D23, D24) | 21 | 63 |
| SOT-23-5 (U7) | 1 | 5 |
| SOIC-14, 1.27 mm pitch (U1, U2, U3) | 3 | 42 |
| **SMD placements** | **153** (152 fitted; R89 is DNP) | **366** |
| Test-point pads TP1 to TP18 | 18 | 18 |
| Fiducials FID1 to FID3 | 3 | copper and mask apertures, no paste |
| 2.54 mm socket strips (J1 to J12, J14, J18 to J23, J25 to J30) | 25 strips | 217 |
| Tactile switches SW1, SW2, SW3 (Omron B3F-4055) | 3 | 12 |
| DIN 42802 sockets J15, J16, J17 | 3 | 3 signal + 6 NPTH posts |
| JST PH headers J13, J24 | 2 | 4 |
| M3 mounting holes MH1 to MH4 | 4 | 4 NPTH |
| **Through-hole subtotal** | **33 parts** | **236 plated, 10 non-plated** |

The through-hole figure is 33 parts and 236 plated holes and it is arithmetic, not an
estimate: 217 socket-strip ways plus 12 switch pins plus 4 JST pins plus 3 DIN signal pins.
Where another document in this package quotes 24 parts and 201 holes, that document is
wrong and design.py governs.

Drill census on the plated side: 217 holes at 1.00 mm (socket strips), 12 at 1.20 mm
(tactile switches), 4 at 0.90 mm (JST PH), 3 at 1.70 mm (DIN 42802 signal pin), plus the
through vias at 0.30 mm finished. Non-plated: four 3.2 mm at MH1 to MH4 and six 1.50 mm DIN
retention posts. The six retention holes carry no copper and no mask (ECO-EEG-012); do not
solder to them and do not let solder wick into them.

**The routing result, taken from `kicad/EEG-CAR-01_RevB_DRC_report.txt`.** EEG-CAR-01 Rev B is
routed on four layers, 150.0 x 130.0 mm, with 3 745 track segments and **552 through vias**. All
145 nets are fully connected: none is left unclosed and none is left without copper. Each
reference plane is one continuous island per net on both inner layers. Every geometric rule
passes: the smallest measured clearance is 0.260 mm on F.Cu, 0.275 mm on B.Cu and 0.285 mm on the
planes against a 0.20 mm rule; the narrowest conductor is 0.200 mm; the smallest plated hole is
0.300 mm; copper stands 2.00 mm clear of every non-plated hole; no digital net enters the analogue
zone; there are no duplicate track segments and no duplicate via positions; and there is exactly
one AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND bridge. The report raises no isolation
violation either, so the isolation strip of DSN-EEG-003 section 3.3 is free of copper on all four
layers, the two inner planes included. The report's own line is: "VIOLATIONS: 0 -- none. The board
passes every rule listed above." That is written here because the report says it, not because it
was intended.

**The board closes at minimum geometry, not at preferred geometry.** Getting to zero cost the
router 169 relaxed connections: 36 took a conductor narrower than the 0.25 mm preferred width, and
133 kept full width and took a reduced gap instead. Every one of the 169 is at or above the
0.20 mm minimum conductor and the 0.20 mm minimum gap, so every one passes -- but a board that
closes at the minimum is not the same board as one that closes with margin everywhere, and the
difference is real even though no rule is broken. The DRC report lists all 169, pad to pad, so the
layout reviewer can see exactly where the squeeze is.

**The fabrication data is RELEASED FOR REVIEW under RFQ-EEG-002A. It is not released for
fabrication.** The gate in ECO-EEG-016 section 3 -- zero DRC violations, every net one connected
copper island, both inner planes continuous under the analogue zone -- is met on all three counts.
What has not happened is the human layout review: the routing was produced by the programme's own
tools and no layout engineer has looked at it. Fabrication release waits on that review. Stage 1
below is written against boards that still have to be fabricated.

**The board is four layers, and that changed during layout.** Package v1 asserted that a
two-layer carrier would be cheap and easy to route. Doing the layout showed that it is not:
on two layers the bottom side has to be both the reference plane and the second routing
surface, and it cannot be both. The stack is now L1 signal, L2 reference plane, L3
reference plane, L4 signal, which gives two full routing surfaces and a continuous
reference under every analogue trace. Both inner layers carry AGND_REF left of x = 62 mm
and DGND right of it, tied together by stitching vias. Vias are **through vias only**, 0.60
mm pad on a 0.30 mm finished hole, 0.15 mm annular ring, tented both sides; no blind,
buried, back-drilled, filled or plugged vias are permitted. Stack-up: mask / 35 µm L1 /
prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask =
1.60 mm ± 10 %.

**None of that changes the SMT process.** The board is still built from one side, with one
stencil, one reflow pass and one AOI pass. What it changes is the bare-board specification,
the IQC check in 2.2 and the reflow profiling in 2.5, and each of those is called out
below.

Coordinate convention: the design source uses a top-left origin with Y down; Gerber, drill
and CPL use a bottom-left origin with Y up. The conversion `y_out = 130.0 - y_design` is
applied once, in `tools/gerber.py`, and is stated in the layer-map README.

### 2.2 Incoming board check (IQC)

The full board specification lives in **DSN-EEG-003 Rev C section 3.2** and is not restated
here. This section lists only what the receiving operator does with it.

Per board, before it enters the EPA:

1. Confirm the fabricator's certificate of conformance names IPC-6012 class 2, IPC-A-600
   class 2 and the 100 % IPC-D-356A electrical test.
2. Measure the outline: **150.0 x 130.0 mm ±0.1**, thickness **1.60 mm ±10 %**.
3. Confirm **four layers** against the fabricator's stack-up report, and confirm the report
   matches the stack in 2.1 (35 / 17 / 17 / 35 µm copper, 0.200 prepreg, 1.065 core).
   ENIG finish, green mask both sides, white legend both sides.
4. **Confirm the inner layers from the fabricator's data, not by eye.** L2 and L3 are
   invisible on a finished board. Require, with each fabrication lot, the inner-layer AOI
   images or the inner-layer films, and check on them: the AGND_REF and DGND plane split at
   x = 62 mm with no bridge between them, and that the isolation keep-out at
   **x ≥ 141 mm, y = 2 to 22 mm** is bare on **all four layers** (RFQ S-03; DSN-EEG-003 Rev C section 3.3, which owns this rule). An assembler who cannot see the inner layers
   and is not given the evidence has no way to accept the board, and this is the one IQC
   step the layer change adds.
5. Confirm every via is tented on both sides and that no via is open in the mask.
6. Confirm the four 3.2 mm holes at (5,5), (145,5), (5,125) and (145,125) are unplated and
   clear of copper for 6 mm diameter (ECO-EEG-007), and the six 1.50 mm DIN retention holes
   are unplated and unmasked (ECO-EEG-012).
7. Confirm the three fiducials FID1 to FID3 are present, 1.0 mm copper with a 3.0 mm mask
   opening, clean and unoxidised.
8. Confirm every refdes on the legend is legible, and that pin 1 of every socket strip is a
   square pad with a legend marker outside the socket body.
9. Record the fabricator lot and date code against the board serial in the as-built record.

The first board of each fabrication lot additionally goes through the bare-board FAI in
QP-EEG-010. On a four-layer board that FAI now has to include **layer-to-layer registration
and inner-layer copper thickness** on the microsection coupon, alongside the ENIG
thickness, hole-wall copper and mask registration it already carried.

> **The board has fiducials, and where they are**
>
> `tools/design.py` places three global fiducials, FID1 at (12.0, 10.0), FID2 at
> (144.0, 100.0) and FID3 at (12.0, 120.0) in the design convention, each 1.0 mm copper in
> a 3.0 mm mask opening (ECO-EEG-020). The Rev A two-point vision teach on the test-point
> pads of TP10 and TP14 is **withdrawn**; do not price it. **RUL-EEG-021 section B** now gives
> the same positions, (12, 10), (144, 100) and (12, 120). Its first issue transcribed them as
> (8, 8), (142, 8) and (8, 122); that transcription error is corrected in the register, and
> `tools/design.py` governs where any two documents disagree. The
> uncontrolled worksheet `tools/RULINGS.md` is no longer cited by this document; RUL-EEG-021 Rev A
> is the controlled rulings register and is listed in ECO-EEG-016 section 1.

### 2.3 Stencil and paste

The stencil is **0.12 mm laser-cut stainless 304, electropolished, top side only.** There
are no bottom-side parts, so no bottom stencil exists and none is to be cut.

Aperture rules, by package:

| Package | Parts | Land (mm) | Aperture (mm) | Rule | Area ratio at 0.12 mm |
|---|---|---|---|---|---|
| 0603 resistor / ferrite | 73 | 0.80 x 0.95 | 0.72 x 0.95 | 10 % reduction in X | 1.71 |
| 0603 capacitor | 54 | 0.875 x 0.95 | 0.79 x 0.95 | 10 % reduction in X | 1.80 |
| 1206 (F1) | 1 | 1.125 x 1.75 | 1.03 x 1.75 | 9 % reduction in X | 2.70 |
| SOT-23 | 21 | 1.025 x 0.60 | 0.95 x 0.60 | 7 % reduction in X | 1.53 |
| SOT-23-5 (U7) | 1 | 1.10 x 0.60 | 1.00 x 0.60 | 9 % reduction in X | 1.56 |
| SOIC-14, 1.27 mm pitch | 3 | 1.95 x 0.60 | 1.85 x 0.55 | reduced both axes against heel bridging | 1.77 |
| Test-point pads D1.5 mm | 18 | ⌀1.5 | none | no paste, these are probe pads | -- |
| Fiducials | 3 | ⌀1.0 | none | no paste, no mask, no part | -- |
| All plated through-holes | 236 | -- | none | pin-in-paste and intrusive reflow are **prohibited** | -- |

An aperture is cut for R89 and the part is not placed; see 2.4.

The area ratio is `(L x W) / (2 x (L + W) x t)`. Every aperture on this board is above the
0.66 limit with margin; the smallest is the SOT-23 at 1.53. These are calculated values. If
the manufacturer chooses a different foil thickness it re-derives the table and reports it
with the first article.

The move from a 0.65 mm TSSOP-14 to a 1.27 mm SOIC-14 for U1 to U3 was made during layout
so that a 0.25 mm track could pass between adjacent lands. It also lifts the tightest area
ratio on the board from 1.15 to 1.53, which is a printing margin the manufacturer keeps for
free.

Paste: SAC305, Type 4 (20 to 38 µm), no-clean ROL0 per J-STD-004. Printed at 20 to 25 °C
and 40 to 60 % RH. Underside wipe every 5 prints on the Phase 1 build of two, every 10
thereafter. Where the line has solder-paste inspection, inspect 100 % of boards in Phases 1
and 2, with U1, U2 and U3 as mandatory sites; volume window 70 to 140 % of aperture volume.

### 2.4 SMT placement

153 placements, all top side, of which 152 are fitted. Orientation-critical parts and how
they are checked:

| Part | Package | Orientation rule | Consequence of 180° error |
|---|---|---|---|
| D1 to D16 | SOT-23, BAV99 | pin 1 to AVSS, pin 2 to AVDD, pin 3 common to the protected node | shorts AVDD to AVSS through the clamp; kills the front end |
| D20, D40, D60 | SOT-23, BAT54S | **pin 3 at the op-amp output** (ECO-EEG-005) | rectifier inverts, envelope channel reads nothing |
| D23 | SOT-23, BAV99 | pin 1 DGND, pin 2 DVDD3V3, pin 3 ENV_CMP | clamps the GPIO to the wrong rails |
| D24 | SOT-23, PESD5V0S2BT | pin 1 VBUS_CHG, pins 2 and 3 DGND | charge input unprotected |
| U1, U2, U3 | SOIC-14, OPA4376AID | pin 1 dot to the legend dot; pin 4 is AVDD and pin 11 is AVSS | supply reversal on a ±2.5 V rail pair |
| U7 | SOT-23-5, TLV3201AIDBV | pin 1 is the output (CMP_RAW) | comparator inverted; TST-EEG-004 T12 fails |

**D1 to D16 are BAV99 and are not interchangeable with BAT54S.** Schottky leakage across a
68 kΩ series resistor -- 47 kΩ before ECO-EEG-024 was applied on 2026-09-02, and worse now
that the resistor is larger -- is an offset error on a 10 µV input. BAT54S is used only at D20, D40
and D60, the envelope rectifiers. Any substitute for the BAV99 must match the Nexperia
BAV99,215 SOT-23 pinout exactly. This is a named acceptance condition, not a preference.

Do not place **R89**. It is 2k2 1 %, electret bias for the boom capsule, and it is
**DO NOT POPULATE** by default. Fit it only on the written instruction of the programme,
and only if the boom preamp module does not supply its own microphone bias (ICD-EEG-006
section 7.2). R89 appears in the CPL with a DNP flag; the feeder is not loaded.

R92 and R93 (0R links, AVDD2 to AVDD and AVSS2 to AVSS) **are** fitted by default. Remove
both only if ADS1299 module #2 regulates its own analogue rails (ECO-EEG-011,
ICD-EEG-006 section 7.1). R78 is 0R fitted; 47R is the approved alternate and is not fitted
without an ECO. R94 and R95 (4k7) are the carrier's own I²C pull-ups and are always fitted
(ECO-EEG-021); do not omit them on the assumption that a module carries pull-ups.

> **U7 is subject to an open change, ECO-EEG-023, that is not yet in design.py**
>
> As fitted, U7 is powered from AVDD and AVSS (pins 5 and 2) and its output reaches GPIO3
> through R83 and the D23 clamp. ECO-EEG-023 moves U7 to DVDD3V3 and DGND and re-references
> its inputs to a DVDD3V3/2 divider with the envelope AC-coupled into it, so that the output
> swings 0 to 3.3 V with full margin. `tools/design.py` still shows the AVDD/AVSS
> arrangement, so **the prototypes are built as drawn** and the change is one the safety and
> layout reviewer must check before it is cut. Build to the board you are given; do not
> anticipate the ECO.

### 2.5 Reflow profile, SAC305

The whole assembly is lead-free. Leaded solder is prohibited everywhere, including rework
and touch-up.

| Phase of profile | Envelope |
|---|---|
| Ramp, ambient to 150 °C | 1.0 to 3.0 K/s |
| Soak, 150 to 200 °C | 60 to 100 s |
| Time above 217 °C liquidus | 45 to 90 s |
| Peak, measured at the U1 body | 235 to 245 °C |
| Maximum anywhere on the board | 245 °C |
| Cooldown from peak | ≤ 4 K/s, target 2 to 3 K/s |
| Total time above 150 °C | ≤ 5 min |
| ΔT across the board at peak | ≤ 10 K |
| Reflow passes, any part | maximum 2 |

**The envelope is unchanged by the layer count; the oven recipe that reaches it is not.**
Two 17 µm inner planes add thermal mass and spread heat laterally, so the profiling board
must be a **four-layer board from the same fabrication lot as the production boards**, not
a two-layer coupon and not a board from an earlier lot. A recipe proved on a two-layer
board will under-soak this one.

The thermal asymmetry to watch is the pour split: AGND_REF on both inner layers left of
x = 62 mm, DGND on both inner layers right of it (DSN-EEG-003 Rev C section 3.3). Four
thermocouples on the profiling board, in design coordinates:

| TC | Location | Design (x, y) mm | Why |
|---|---|---|---|
| TC1 | U1 body, SOIC-14 | 47.0, 81.0 | the peak reference, and the largest reflowed package |
| TC2 | C1, 0603, analogue zone | 28.0, 5.0 | coolest corner over the AGND_REF planes |
| TC3 | C74, 0603, right edge | 145.0, 67.0 | hottest corner over the DGND planes |
| TC4 | bare laminate near MH3 | 5.0, 125.0 | laminate reference, no part |

Nitrogen is not required. If the line uses it, say so in the first-article report, because
it changes wetting on ENIG. Cleaning: **no-clean, no aqueous wash.** The 25 socket strips
and the three DIN 42802 sockets will trap wash residue, and the board later sees conductive
EEG paste in service.

The profile trace is returned with the first-article package and is re-run whenever the
panel format, the oven or the phase quantity changes.

### 2.6 AOI

100 % top-side AOI at all quantities. Phases 1 and 2 are two and ten units, so 100 % is
affordable and sampling is not permitted below 25 units. AOI checks presence, value where
the marking allows, offset, tombstoning, bridging, and polarity on all 22 SOT-23 and
SOT-23-5 parts and all three SOIC-14 parts against the detail views in the assembly
drawing. **152 parts are expected present. R89 must be reported as absent; a populated R89
is a defect.**

### 2.7 Through-hole

Insertion order is fixed: SMT reflow first, then through-hole inserted from the top, then
soldered from the bottom. There is no second reflow.

| Part group | Refdes | Joints | Baseline process |
|---|---|---|---|
| 2.54 mm socket strips | J1 to J12, J14, J18 to J23, J25 to J30 | 217 | Phases 1 and 2: hand. Phase 3: selective solder |
| JST PH 2-way | J13, J24 | 4 | Phases 1 and 2: hand. Phase 3: selective solder |
| Tactile switches | SW1, SW2, SW3 | 12 | hand, all phases |
| DIN 42802 sockets | J15, J16, J17 | 3 | hand, all phases |

**Four layers make hand-soldering the ground pins harder, and the design already answers
it.** Every through-hole pad that lands on a reference plane is connected through a
four-spoke thermal relief with a 0.40 mm annulus and 0.60 mm spokes (`tools/pours.py`);
surface-mount pads on the planes are connected solid. Without the reliefs, a DGND pin on
J12, J14 or J30 would sink heat into two inner planes and the barrel would not fill. Do not
let a rework operator flood a relief; if a relieved pad is bridged to the plane by a repair,
the board goes to the disposition table in section 10.

Selective soldering is available at Phase 3 without a pallet, because the solder side
carries no components. It is priced separately in the RFQ-EEG-002B template so that the
programme can see the crossover.

Seating and coplanarity, per part:

| Part | Rule |
|---|---|
| J6 and J7 | soldered with a mating ESP32-S3-DevKitC-1 or the socket comb in place. Row spacing 22.86 mm (ECO-EEG-008). Coplanar within 0.15 mm over the 53.34 mm length, perpendicular within 2°. A DevKit that will not seat across both rows is the most expensive error in this stage |
| J2, J4, J23, J29 | analogue signal and rail sockets. Body flush, gap ≤ 0.1 mm, perpendicular within 2°. Do not solder to the retention area under the module outline; no via or copper is permitted there (design.py NO_VIA_ZONES) |
| J14, J30 | the two harness sockets. Pin 1 is the square pad; the legend marker sits outside the socket body and must remain visible after fitting |
| SW1, SW2, SW3 | 5.0 mm actuator height, perpendicular within 2°, body flush. The 12 mm caps and the lid boss engagement are set in stage 4 |
| J15, J16, J17 | the two 1.50 mm retention posts on each socket body locate in the unplated holes. They are a location feature, not a fastener and not a solder joint. Socket face height is set against the POD-P1 panel in stage 4 |
| J13, J24 | JST B2B-PH-K, 0.90 mm holes. J13 pin 1 = VBAT, pin 2 = DGND. J24 pin 1 = VBUS_IN, pin 2 = DGND. Both are keyed housings; a reversed header is a scrap-level defect |

Barrel fill: IPC-A-610 class 2, vertical fill ≥ 75 % on all 0.90, 1.00 and 1.20 mm barrels.
Read that as written: **≥ 75 % vertical fill is the class 2 figure**, class 3 asks for the same
75 %, and what class 3 adds is a stricter circumferential wetting. So the tightening on J15,
J16 and J17 in 1.3 is the wetting -- 100 % on both sides -- and their vertical fill is the
same ≥ 75 % as every other barrel on the board. There is no barrel here with a lower fill
limit than any other.

### 2.8 The two star points, and R89

Three parts on this board carry a rule that no inspection standard will catch. The rule
itself, and the reason for it, live in **DSN-EEG-003 Rev C section 3.3**; what follows is
the operator's action.

**R90 is the single star point between AGND_REF and DGND.** Fit exactly one 0R link at R90
(56.0, 58.0). Never bridge it with a wire, never add a second link anywhere, never repair
it with solder across the pads. On a four-layer board there is one further way to get this
wrong: a stitching via that lands in the wrong plane region would join the two planes a
second time. That is a layout property, checked by the DRC at
`kicad/EEG-CAR-01_RevB_DRC_report.txt`, not something the assembler can see -- so accept
the boards only against a DRC report that shows exactly one AGND_REF-to-DGND bridge.

**R91 is the single star point between HARN_SHIELD and DGND**, at the pod end only
(56.0, 62.0). Same rule. The helmet harness screen is grounded here and nowhere else, which
is why the frame carries no loop (DSN-EEG-002 Rev E section 6).

**R89 is DO NOT POPULATE** (122.0, 114.0). See 2.4.

Both R90 and R91 are on the no-touch-up list in 1.3. If either is disturbed, replace the
part; do not re-flow it.

---

## 3. Stage 2 -- module preparation and the MP-01 plate

Purchased modules do not plug into the carrier sockets. They mount on the printed module
plate **MP-01**, 146.0 x 126.0 x 3.0 mm, above the carrier and connect with keyed 2.54 mm
ribbon jumpers per ICD-EEG-006. The one exception is the ESP32-S3-DevKitC-1-N16R8, which
inserts directly into J6 and J7 and stands up through the 31 x 61 mm opening in the plate.

There are **twelve module types and thirteen module assemblies per unit** -- the ADS1299
breakout is fitted twice. Twelve assemblies mount on MP-01; the DevKit does not.

### 3.1 Incoming inspection of the modules

Before anything is mounted, each module is inspected and recorded. Thirteen assemblies per
unit, of twelve types:

| Module | Socket | Confirm at IQC |
|---|---|---|
| ADS1299 8-channel breakout ×2 | J1/J2/J23 and J3/J4/J29 | converter date code and lot visible and recorded for each; DAISY_IN and CLKOUT exposed; serialise the pair so they travel together |
| ESP32-S3-DevKitC-1 | J6, J7 | variant is **-N16R8**, 16 MB flash and 8 MB PSRAM; headers pre-fitted; row pitch 22.86 mm; **its own UART USB-C port is present and undamaged, because stage 5 flashes through it** |
| ES8388 codec | J8, J9 | headphone amplifier present; HP tap accessible |
| ADuM4160 isolator | J10 | host connector present on the module; **the supplier's ≥ 2.5 kV RMS isolation type-test certificate is checked once, here, at incoming inspection** (RFQ E-24, S-03). There is no per-unit hipot; the per-unit test is a 500 V DC insulation-resistance measurement across the barrier in TST-EEG-004 Rev C |
| ATECC608B breakout | J11 | part is **ATECC608B-SSHDA**, not -TNGTLS. A TNGTLS part arrives with its configuration zone locked and cannot be provisioned |
| Charger with power path and CE pin | J12 | CE pin brought out |
| Fuel gauge | J12 (I²C) | see the note below |
| Buck-boost, TPS63020 class | J25 | 5.00 V, 1 A output, EN pin brought out |
| microSD breakout | J20 | wired for one-bit SDMMC |
| Boom microphone preamplifier | J21 (1×6) | **the part is not settled.** Accept only against the interface in ICD-EEG-006; the MAX9814 named in package v1 is an automatic-gain-control part, RFQ E-14 requires AGC off, and AVL-EEG-017 carries it as not approved. The preferred route is a fixed-gain part of the MAX4466 class. **This module lives on MP-01, not on the boom** -- the boom carries the bare electret capsule and its screen on the pigtail at J18 |
| Room microphone module | J28 | hardware mute line present (RFQ E-15) |
| 74HC595 breakout | J19 | Q0 to Q7 brought out (ECO-EEG-001) |

Record per unit: manufacturer, module serial or lot, ADS1299 date code and lot for each of
the two converters, and which of the two is device #1 on the daisy chain. The rule is that
the module whose DOUT feeds the other's DAISY_IN is device 2 in the firmware's frame order.
A swapped pair passes the seating and power tests and only appears at TST-EEG-004 T7 as a
gain of 12 where 24 was expected, so the labelling at IQC is what prevents it.

> **Charger and gauge on one socket**
>
> J12 is a single 1x8 socket carrying VBAT, DGND, VBUS_CHG, CHG_CE, SDA, SCL, VSYS and one
> no-connect. **The baseline is one combined charger-plus-gauge assembly on a single J12
> jumper.** If two separate breakouts are supplied, the gauge mounts on MP-01 and its VBAT
> and I²C taps are made at the MP-01 end of the J12 jumper as a **Y jumper drawn in
> ICD-EEG-006 section 3.3** -- a drawn part, not a hand-built variation invented on the
> bench. Build only from the drawing.

### 3.2 Male headers

Several breakouts ship with their header strips loose. Fitting them is a real operation
with a real cost and it is listed in AVL-EEG-017 under "module interface hardware": 2.54 mm
male break-away header, gold flash, 1x40 strips, six strips per unit with attrition.

Fit strips from the component side and solder on the underside. Body flush, perpendicular
within 2°. Use the carrier itself, or the module's own socket on MP-01, as the alignment
fixture so the module mates first time.

### 3.3 Standoffs and the plate

| Fastener | Where | Torque | Note |
|---|---|---|---|
| M3 x **18 mm** nylon hex standoff, **male-female** | MH1 to MH4, carrier to MP-01 and to the pod boss below | 0.40 N·m | four off. The male stud passes the carrier's Ø3.4 mm clearance hole and enters the brass insert in the POD-P1 floor boss, so one fastener carries the carrier and the standoff both. Stud 4.6 to 7.1 mm; a catalogue 6 mm stud engages 4.40 mm of insert (`mech/HARDWARE_SCHEDULE.md` H-4). Nylon; do not use a metal standoff, the M3 holes have a 6 mm copper keep-out and no ground connection |
| M3 x 6 mm nylon pan screw | the top of each standoff, into MP-01 | 0.40 N·m | **four off**, one per standoff. Rev B said eight, for a female-female standoff that is superseded by the line above |
| M2.5 x 6 mm nylon standoff and screw | each module to MP-01 | 0.25 N·m | two per module minimum, 24 per unit for twelve assemblies |

The standoff is **18 mm**, not the 12 mm of Rev A. Two things depend on it. The stack budget
in ICD-EEG-006 section 4 is floor 2.5 + boss 6.0 + carrier 1.6 + standoff 18.0 + plate 3.0 +
modules ≤ 18.0 = **49.1 mm against 55.5 mm of POD-P1 internal depth, a margin of 6.4 mm**.
And RISK-EEG-011 SR-08 asks for 8 mm of creepage from carrier copper to any host-side
conductor on MP-01: the slant path over the edge of the isolation keep-out and up an 18 mm
standoff is at least 18 mm, more than twice what the safety case asks. A 12 mm standoff
does not give that and must not be substituted.

All torques are applied with a calibrated driver set to the value in the table. Nylon
threads strip above about 0.5 N·m at M3 and 0.3 N·m at M2.5; the settings above carry
deliberate margin.

> **Settled -- one fixing does both jobs**
>
> MH1 to MH4 are the only four fixings on the carrier, and both the POD-P1 floor bosses
> (below) and the MP-01 standoffs (above) land on them. Rev B recorded this as open, with
> two possible resolutions. **The released model has taken the first.** `pod_base()` bores
> each floor boss for an M3 brass heat-set insert and the standoff becomes male-female: its
> stud passes down through the carrier into that insert, its female end takes the M3 x 6
> nylon screw that carries MP-01, and the carrier is clamped between the standoff shoulder
> and the boss face. The alternative -- four additional fixings -- would need four more holes
> in a carrier that is a different file at a different revision, and a boss pattern clear of
> MH1 to MH4 would have nothing to bolt to. Nothing about the stack height changes:
> 2.5 + 6.0 + 1.6 + 18.0 + 3.0 = 49.1 mm against 55.5 mm, and the 18 mm slant path that
> RISK-EEG-011 SR-08 rests on is the same 18 mm.
>
> **AVL-EEG-017 section 1.6 and kit BOM item 31 still buy the female-female part**, with
> eight M3 x 6 screws for a joint that now takes four. A female-female standoff has no stud,
> so with that part in hand nothing fastens the carrier to the pod floor and the eight
> Ø4.00 mm bores in the pod are clearance holes holding no thread at all. Do not improvise
> it on the bench: raise it against AVL-EEG-017 and the BOM. What the released geometry
> needs, and what has and has not been chosen, is in `mech/HARDWARE_SCHEDULE.md`.

### 3.4 Module orientation and keying

The carrier has interchangeable socket geometries, and this is the inventory from
`design.py`:

| Family | Refdes |
|---|---|
| 1×3 | J22 |
| 1×4 (seven) | J5, J9, J10, J11, J18, J27, J28 |
| 1×6 (five) | J21, J23, J25, J26, J29 |
| 1×8 (two) | J12, J20 |
| 1×10 (three) | J2, J4, J30 |
| 1×12 (three) | J1, J3, J14 |
| 1×14 | J8 |
| 1×16 | J19 |
| 1×22 (two) | J6, J7 |

That is 25 socket strips out of the **thirty connectors J1 to J30**, seventeen of which are
module connectors. Note that **J21 is a 1×6, not a 1×4** -- Rev A of this document listed it
in the 1×4 family and left out J5, the ADS #1 DAISY_IN / CLKOUT stub.

A 1×4 module will physically enter a foreign 1×4 socket, so keying matters, and it is now
decided rather than procedural:

1. **Module end:** a 2.54 mm shrouded polarised IDC header wherever the module has one.
   Where it does not, pin 1 is marked on the module and the jumper is labelled.
2. **Carrier end:** the printed keying shroud **WH-KEY-01**, part of the MP-01 print set,
   over every socket that takes a jumper. **ICD-EEG-006 section 6** lists which sockets get
   one; do not decide it here.
3. Every ribbon jumper is labelled at **both** ends with the carrier refdes and the module
   name, on heat-shrink, before it is fitted.
4. Pin 1 on the carrier is the square pad, marked outside the socket body on the legend.
5. The seating check in 3.6 enumerates each socket by refdes and the operator ticks it.

### 3.5 Ribbon jumper set

One jumper per module connection, built to the cut lengths in ICD-EEG-006. Phase 1 builds
them by hand from 2.54 mm ribbon and IDC connectors; Phase 2 onward buys pre-made sets. The
jumper is a hand-built item per unit and that is a known cost of the module architecture
(DSN-EEG-003 Rev C section 8, open item 5).

Fit checks per jumper: full pin engagement, no bent pin, ribbon not strained across the
plate edge, service slack ≤ 15 mm so nothing can chafe on the pod wall.

### 3.6 DevKit insertion and stack sign-off

Insert the ESP32-S3-DevKitC-1 into J6 and J7 with even pressure at both ends. Check: module
body parallel to the carrier within 1 mm across its length, no bent pin, full engagement.
Check also that its own UART USB-C port sits clear inside the MP-01 opening and can be
reached with a cable, because stage 5 flashes through it.

Then, with the whole stack assembled, verify the stack height against the **POD-P1 internal
depth of 55.5 mm** before the pod is committed: carrier 1.6 mm, socket mating height,
standoff 18 mm, MP-01 plate 3.0 mm, module PCB, tallest module component, on top of the
6.0 mm boss. The budget says 49.1 mm and the margin is 6.4 mm. Record the measured figure.

For transit in a hard case, fit a retention bar over the ADS pair and the DevKit. A module
that walks out of its socket in the post is the most likely field failure of this
architecture. The bar is a JIG-EEG-009 item and has no fixture number yet (see 1.4).

---

## 4. Stage 3 -- helmet build

### 4.1 HM-01 frame preparation

1. Confirm the print against the MJF process specification: dyed, bead-blasted, engraved
   site names (Fz, Cz, Pz, C3, C4, T7, T8, F7) legible, no paint or lacquer on any
   skin-contact face.
2. **Pull a 3.0 mm nylon draw cord end to end through every internal channel** and record
   pass or fail per channel per serial. This is the only way to prove the powder cleared. A
   frame with a blocked channel is scrap at this point, not at wiring.
3. Blow every channel through with dry compressed air at 4 bar.
4. Wipe the outer surfaces with 70 % IPA and allow to dry.
5. **Make the two umbilical entries, OE-1 and OE-2.** The released HM-01 mesh has no entry
   hole of any kind, because it is a v1 mesh with no parametric source (PARTS-EEG-019 OA-1),
   so until a parametric frame prints them the two bores are made here. They go through the
   **floor plate of the occipital shell**, which is 2.40 mm of PA12, flat, at
   x = -16.00 mm (OE-1, the electrode cable WH-01) and x = +16.00 mm (OE-2, the light cable
   WH-02), y = -103.01 mm, Ø12.50 mm, axis vertical.

   Use **HM-12**, the entry plate, as the jig, because it carries the same two bores at the
   same 32.00 mm centres: lay it on the underside of the floor with **8.0 mm of floor showing
   at the front edge and 8.0 mm at the rear edge, and 27.0 mm from each end of the plate to
   the outside of the side wall**, clamp it, pilot both holes through it and open them to
   Ø12.50 mm. Setting it by those four equal margins is what puts the bores on the
   coordinates above; there is no datum feature on the frame to work from.

   Drill from the outside, support the floor from inside the cavity, and take the swarf out
   with the vacuum before it travels: PA12 chips in a wiring channel are not recoverable
   once the covers are on. Break both edges of each bore lightly. Then repeat step 2's draw
   cord on the rear sagittal channel **and on both halo branches**: those are the three
   channels the conductors from these entries run into, all three open into the cavity the
   swarf falls into, and a chip in one of them is not recoverable once the covers are on.
6. Leave HM-12 in place. It is not bonded and not screwed: the two cable glands of section
   4.4 are what clamp it, and it comes off with them at service.

### 4.2 Bonding the eight HM-04 electrode assemblies

This is the joint the entire electrode geometry depends on: eight bonds per helmet, each
carrying the spring load, the gel-port seal and the participant's own "slide that assembly a
few millimetres" adjustment.

| Parameter | Value |
|---|---|
| HM-04 body | **12.4 x 12.4 x 18.0 mm square prism** (`mech_gen.py`), not a cylinder; the square section is its own anti-rotation feature and no flat is required |
| Pocket in HM-01 | nominally 12.55 mm square, giving a 0.075 mm bond gap per face. **Not verified:** HM-01 is a carried-over STL that no source file in `tools/` generates, so this figure must be measured on the print before the first bond |
| Insertion depth | 12.0 ±0.2 mm to the HM-01 outer face shoulder |
| Orientation | the light window faces outward and the gel port faces up; the window is on one side of the body only |
| Surface preparation | abrade the pocket with 320-grit or plasma treat, IPA wipe, dry 10 minutes |
| Adhesive | two-part structural methacrylate suited to unprimed PA12: 3M DP8010NS blue, or Loctite AA 3038 as the approved alternate |
| Bead | 0.25 ml per joint, applied to the pocket, not the part |
| Fixture | the eight-station bonding fixture of JIG-EEG-009, which holds each port axis normal to the local scalp tangent and each light window facing out |
| Cure | 24 h at 23 °C, or 2 h at 60 °C accelerated |
| Acceptance | 100 N axial pull-off on one sample assembly per build lot; visual fillet on all eight; gel-port water leak check before the frame is wired |

The order matters: **dye before bond.** A dyed MJF surface bonds less well than raw powder,
and if the frame is dyed after bonding the dye bath attacks the joint. Both adhesives above
are named on manufacturer data for unprimed PA12; neither has been tested on this
programme's actual dyed MJF surface, and the first-article pull-off is the first real
evidence. State the measured figure in the FAI report.

Rework: a bonded HM-04 cannot be removed without damaging the pocket. One bad bond scraps a
133.6 cm³ frame. That is why the pull-off sample is per lot and the fixture is not optional.

### 4.3 Contact-light LEDs

Eight two-lead bicolour LEDs, one per site, fitted into the HM-04 body behind the light
window and wired between LEDn and the LED_V common. Each site is driven through a 1 kΩ
series resistor (R70 to R77) at (3.3 − 2.0)/1000 = **1.3 mA per site, 10.4 mA total from
GPIO48**.

The LEDs are anti-parallel, so there is no electrically wrong way round -- but there is a
wrong way round for meaning. Phase A (LED_V high, Qn low) must show **green** and phase B
(LED_V low, Qn high) must show **red**; alternating at the fitted **240 Hz**
(`LIGHT_PHASE_HZ` in `board_pins.h`, against a requirement of "above 100 Hz") shows amber.
The marked lead goes to the LEDn conductor and the unmarked lead to LED_V.

**Corrected 2026-09-02: the bicolour phase driver is written.** Until that date
`lights_write()` and `lights_task()` were on/off only and this paragraph said the amber scheme
was not coded and T11 could not pass. `lights_task()` now drives a green phase and a red phase
from the converter's own lead-off word, at about 250 Hz once the half-phase is quantised to
the FreeRTOS tick. **For the operator, nothing changes yet.** No unit has ever lit an LED and
**T11 has not been run**, so a reversed LED is still not detectable at test: the marked-lead
orientation is verified by the operator at fitting and signed for in section 9, exactly as
before, until T11 has been run on a real unit and passed.

Nothing can light at boot whatever the shift register contains, because LED_V is GPIO48 and
is an input at reset. Do not add a pull-up to LED_V during any bench check.

### 4.4 Threading the harness

Two cables, not one (ECO-EEG-014). They are **specified** to run in separate channels and to
be never bundled; the released frame does not give them separate channels, which is the box
at the end of this section and is not something the operator can fix.

| Cable | Ways | Socket | Contents |
|---|---|---|---|
| Electrode cable, screened | 12 | J14 | E_Fz, E_Cz, E_Pz, E_C3, E_C4, E_T7, E_T8, E_F7, REF_L, REF_R, BIAS_EL, HARN_SHIELD |
| Light cable | 10 | J30 | LED1 to LED8, LED_V, LED_GND |

Build and pinout are in WH-EEG-008. In this stage the operator:

1. **Fits the two entries first.** HM-12 goes on the underside of the occipital shell floor
   over OE-1 and OE-2 (section 4.1 step 5), and an M12 x 1.5 cable gland goes up through each
   bore from below with its locknut inside the cavity, 17 mm spanner, seated square. Nothing
   else holds HM-12; the two glands are what clamp it, and the plate is what stops the
   locknut bearing on 2.40 mm of printed floor alone.
2. **Feeds each umbilical in through its own gland** -- WH-01 through OE-1, WH-02 through
   OE-2 -- and tightens the clamping nut onto the jacket **before any conductor is dressed**.
   That clamp is the strain relief at this end and it is what the 15 N site-end pull of
   WH-EEG-008 H6 reacts against; a jacket cut back before it is clamped leaves the pull on
   the terminations instead. Cut the jacket back inside the cavity, not outside it.
3. Threads each cable with the draw cord, entering the assembly from below, along its arch
   or halo channel to the crown, then rearward.
4. Leaves a **120 mm service loop** at the pod end of each cable, so a conductor can later be
   drawn through without dismantling the far end (WH-EEG-008 section 3 cut schedule owns this
   dimension).
5. Terminates the screen of the electrode cable at the pod end only. The helmet harness screen
   HARN_SHIELD reaches DGND at exactly one point, R91 on the carrier. The three pod-internal
   pigtail drains at J18.2, J27.3 and J28.2 are not part of that system (WH-EEG-008 section
   5.3).
6. Fits the snap-in cover strips on the skull-facing side of every section, with a plastic
   pick, working from the crown outward.

> **What the released frame does not give this harness**
>
> WH-EEG-008 section 7 gives every frame section **two** channels, A for the electrode cable
> and B for the light cable, at least 6 mm apart. **The released HM-01 mesh has one.**
> Sectioning it finds a single Ø3.78 mm bore in the halo band, one in each sagittal arm, one
> in each coronal arm and one branch on each side that leaves the halo at about y = -50 mm
> and descends to the occipital shell -- every run a single channel, never the pair section 7
> specifies, so the two cables share a channel wherever they run together.
>
> Where those channels end is the other half of it. All three that reach the occiput open
> into the **shell cavity** and nowhere else: the rear sagittal one through the roof plate at
> (0.00, -95.38, 29.60), and the two halo branches through the wall at (±45.41, -82.41,
> -11.25). That is where node N1 has to be, and the trunk from the entries to it is not a
> channel at all -- it is open cavity, 55.5 mm to the nearer halo mouth and 85.1 mm to the
> roof mouth, with nothing along it that anchors a conductor.
>
> Two consequences, neither of which an operator can fix and neither of which may be papered
> over on the bench. The section 7 fill limit of 50 % is exceeded on the shared rear sagittal
> run -- 4.24 + 4.42 mm² of conductor in an 11.34 mm² bore is 76 % -- so the conductors are
> laid in, never pulled, and a replacement conductor cannot be drawn through. And
> RISK-EEG-011 H-05 and SF-9 exclude an LED conductor contacting an electrode conductor on
> the strength of separate channels, which this frame does not have. Record both on the build
> record. They are open items 19 and 20 and they belong to the parametric HM-01, not to this
> stage.

### 4.5 Yoke, chin strap, boom and pads

| Item | Fitting | Torque or check |
|---|---|---|
| HM-03 occipital yoke and ratchet dial | into the two rear halo anchor pockets | M3 x 10 A2 into a brass heat-set insert, 0.50 N·m; 2 mm per click; must hold 20 N for 2 h without slipping |
| HM-06 chin strap and chin cup | 20 mm webbing through the two temple anchor slots | anchor pull test 200 N on the FAI sample; the strap must remain removable by the participant without a tool |
| HM-07 boom microphone arm | 120 mm gooseneck into the left temple socket, keyed so it cannot be fitted rotated | M3 x 6 A2, 0.50 N·m; capsule sets about 30 mm from the mouth corner, and that geometry is a measurement requirement, not comfort. The boom carries the **bare electret capsule and its screen only**, on the pigtail to J18; the preamplifier is on MP-01 at J21 |
| HM-02 TPU pads ×4 | brow, occiput ×2, crown, tool-free seats | consumable; replaced every turnaround |

**Three of the four fittings in that table are not located on any released drawing.** The
two rear halo anchor pockets, the two temple anchor slots and the left temple socket are not
in the HM-01 mesh, and MECH-EEG-020 sheet 3 -- the only released HM-01 drawing -- is three
silhouettes and an overall 191.05 x 229.56 x 158.00 mm with no internal feature on it at all.
What *is* dimensioned is the yoke: `tools/mech_gen.py hm03a_yoke()` puts its two anchor pads
on the halo ellipse fitted to the mesh, at azimuth 235° and 305° -- (-46.5, -79.3) and
(+46.5, -79.3), a 93.0 mm chord -- each with a Ø3.4 mm clearance hole and a 5.00 mm pad, so
an M3 x 10 leaves 5.00 mm in the insert. Set the yoke from those two points and mark the
frame from the yoke. Do not look for a pocket that is not there and do not cut one to a
dimension nobody has issued; it is open item 21.

HM-03 and HM-06 are part of the frame, not kit accessories. The A-03 headband of the v1
packing list is withdrawn: the eight electrodes are fixed to the HM-01 frame at manufacture
and a headband with fixed holders at the same eight sites would duplicate them.

---

## 5. Stage 4 -- pod integration

### 5.1 Phase 1: POD-P1

POD-P1 is the bench enclosure. From `tools/mech_gen.py`: base **163.0 x 143.0 x 58.0 mm
external, 158.0 x 138.0 x 55.5 mm internal**, 2.5 mm walls, a 1.6 x 1.2 mm gasket groove in
the rim, four carrier bosses standing 6.0 mm off the internal floor; lid **163.0 x 143.0 x
6.0 mm** with a 2.0 mm spigot. It grew with the carrier. The helmet connects to it by the
harness. Phase 1 exists to prove the front end and the timing chain, not the ergonomics
(RFQ M-01).

1. **Boss fixings.** Every M3 thread in POD-P1 is a **brass heat-set insert**, and the bore
   for each one is printed. The four floor bosses and the four corner bosses under the lid
   screws each carry a **Ø4.00 mm bore with a Ø5.00 x 0.5 mm lead-in**, 5.50 mm deep in the
   floor bosses and 7.00 mm deep in the lid bosses (`tools/mech_gen.py`, `INSERT_BORE_D`).
   **There is no drilling operation and there is no Ø2.5 mm pilot.** Rev B of this document
   described a Ø2.5 mm hole for a thread-forming screw and left the insert question open;
   the released model has decided it the other way, and MECH-EEG-020 sheet 18 says the same.
   Driving an M3 thread-forming screw into a Ø4.00 mm bore strips it on the first turn.

   The reason for the decision is in section 3.3: these joints are torqued to 0.60 N·m and a
   thread formed straight into PA12 strips at about 0.5 N·m, so the joint as Rev B drew it
   was being asked to hold more than it holds.

   Set each insert with the heat-set tool, square to the boss face and flush to 0.3 mm below
   it, and let it cool before anything is screwed into it. The insert length each bore
   accepts is in `mech/HARDWARE_SCHEDULE.md` H-1 and H-2 -- the floor bore is **blind**, so
   an insert that is too long bottoms and stands proud -- and **the insert itself is not yet
   a chosen part**. Do not fit one that has not been approved against those criteria.

   The two Ø2.50 mm holes in the harness-entry pads are **not** insert bores. They are
   thread-forming pilots for the two POD-P1-04 P-clip screws, which are hand-tight cable
   retainers at about 0.3 N·m and stay under the strip limit without an insert (H-7).
2. **Gasket.** Cut **1.5 mm** silicone O-cord, 60 Shore A, to the internal rim perimeter.
   Butt-bond the ends at one corner with cyanoacrylate. Seat it in the **1.6 x 1.2 mm**
   groove in the base rim. That gives about 20 % compression and about 92 % groove fill.
   The fill is at the top of the usual limit and the groove is narrow for the cord, so the
   first article measures the closed-lid gap; if the lid will not pull down, the groove is
   widened by ECO rather than the cord squeezed in.
3. **Panel parts, in this order.** The panel openings are generated in `mech_gen.py` and
   there are twelve of them:
   - J15, J16, J17 DIN 42802 sockets aligned to the three Ø8.2 mm apertures on the left
     wall at y = 76, 88 and 100 mm, colour-coded per RFQ E-09, socket faces flush to the
     outer panel face within 0.5 mm.
   - Data USB-C: the host connector is the receptacle **on the ADuM4160 module**, presented
     through the 10 x 4 mm aperture at (146, 12) with a gasketed bushing. **No carrier
     copper crosses the barrier.** It is a socket, not a captive cable: the participant
     plugs in one of the two A-07 cables shipped with the kit. The WH-08 captive lead and
     its gland are **deleted from the Phase 1 build**; a captive lead through a gland is a
     Phase 2 item for the helmet shell.
   - **Live non-conformance:** the only named candidate isolator module presents **USB-B**
     and RFQ E-24 asks for USB-C. The interim answer is a short USB-B-to-USB-C panel pigtail,
     **WH-09**, until an isolator with a USB-C host connector is qualified. Check which
     connector the delivered module has before cutting or dressing this aperture.
   - Charge USB-C pigtail to J24, through the 10 x 4 mm aperture at (143, 80). Charge only;
     no data conductor enters here.
   - microSD aperture, 13 x 3 mm, clearing the push-push eject stroke. **It belongs at
     (136, 72), which is where the J20 microSD breakout sits in `design.py`. The released
     model does not put it there: `mech_gen.py` cuts it at (136, 60), and (136, 60) is
     J13, the battery connector. It is the wrong connector's coordinate, copied 12 mm low,
     so as generated the slot misses the card edge and instead opens the wall directly over
     the cell header.** Do not cut or print a pod to the current model at this feature and
     do not correct it on the bench; it needs an ECO against `mech_gen.py` before POD-P1
     is made. The other eleven openings were checked against `design.py` for this
     correction: the three DIN sockets, both microphone ports, the headphone port, the
     charge port and the three button openings all land on their own part's coordinate,
     and the data USB-C at (146, 12) is the isolator module's own receptacle rather than
     a carrier connector, so it has no coordinate to agree with.
   - 3.5 mm headphone jack pigtail to J27 at (128, 72); boom TRRS pigtail to J18 at
     (122, 90).
   - Room-microphone port at (122, 102) with a hydrophobic acoustic mesh insert.
   - Three Ø13.0 mm openings on the right wall at y = 76, 90 and 104 mm on a 14 mm pitch,
     for **12 mm coloured caps on extenders over the 6 mm tactile switches** SW1 (green,
     BTN_A), SW2 (blue, BTN_B) and SW3 (red, BTN_STOP). RFQ E-26 requires a distinct colour
     and a distinct tactile feel on the stop button; check by feel, not by sight.
   - Silicone boots over the three actuators.
   - **There is no LED opening and no pod indicator.** All eight lights are in the helmet;
     the pod's state is read from the session runner. RFQ M-02 is corrected accordingly.
   - **Harness entries, two of them.** The two helmet cables enter through **two
     M12 x 1.5 cable glands**, one per cable, in Ø12.50 mm bores at the harness layer,
     z = 21.0 mm. Each entry is on the wall nearest its own connector and on that
     connector's own coordinate: WH-01 through the left wall opposite J14, WH-02 through the
     long wall opposite J30. Each bore sits in a raised pad that makes 3.5 mm of panel for the
     gland and carries a 22.0 mm flat seat for the locknut inside, and each pad also carries
     a Ø8.0 mm boss with a Ø2.5 mm pilot for the POD-P1-04 P-clip. **Two entries and not one
     is a safety decision**: RISK-EEG-011 H-05 and SF-9 exclude an LED conductor contacting
     an electrode conductor on the strength of two separate cables in two separate glands,
     and a shared entry puts that exclusion back in play. Fit both glands, with their
     locknuts inside, **before** the stack goes in; there is no access to the locknut once
     MP-01 is fitted. The gland is the primary strain relief at this end and the P-clip is
     secondary, which is the reverse of what WH-EEG-008 section 6 assumes.

     **The gland is not yet a chosen part.** `mech/HARDWARE_SCHEDULE.md` H-8 states the
     clamping range, panel thickness, locknut size and retention the released bore needs, and
     AVL-EEG-017 has to choose one against them. The Rev B statement that there is no harness
     entry in the model is withdrawn: the entries are in POD-P1-01 Rev B and are printed.
4. **Stack in.** Lower the carrier and MP-01 stack onto the four base bosses so that the
   four standoff studs enter the four floor inserts. **There is no separate screw at this
   joint.** The male-female standoff's own stud is the fastener (section 3.3), and the
   carrier is clamped between the standoff shoulder and the boss face. Tighten at the
   standoff, **0.40 N·m**, diagonal sequence -- 0.40 and not 0.60 because the stud is nylon.
   The four M3 x 8 A2 pan screws of Rev B are deleted: with a stud in the insert there is
   nothing for them to enter.
5. **Battery.** The protected 18650 mates J13 through the keyed carrier. Fit the cell only
   after TST-EEG-004 T3 has passed on a bench supply. **RFQ E-23 requires that there be no
   charging above 45 °C and S-04 requires the thermistor that measures it; there is no NTC
   net in `design.py` and no thermistor way on J12 or J13, so this requirement is NOT met on
   Rev B.** It is an open hardware item carried in DSN-EEG-003 section 11 and RISK-EEG-011,
   and it is not closed by anything an assembler can do. Fit the cell knowing that.
6. **Close.** Fit the lid over the gasket. Four M3 x 12 A2 pan screws, **0.60 N·m**, in two
   passes, diagonal sequence. Design target for the pod is IP54 and it has not been tested;
   IP67 belongs to the travel case (RFQ M-05), not to the pod, and no IP67 claim is made for
   POD-P1.

Torque summary for this stage:

| Fastener | Count | Torque | Sequence |
|---|---|---|---|
| M3 x 18 nylon standoff stud, carrier stack into the floor insert | 4 | 0.40 N·m | diagonal |
| M3 x 12 A2, lid into the corner insert | 4 | 0.60 N·m | diagonal, two passes |
| M3 x 10 A2, yoke anchor (stage 3) | 2 | 0.50 N·m | -- |
| M3 x 6 A2, boom mount (stage 3) | 1 | 0.50 N·m | -- |
| M3 x 6 nylon, standoff top to MP-01 (stage 2) | 4 | 0.40 N·m | diagonal |
| M3 x 8 thread-forming, P-clip bosses | 2 | hand tight, about 0.3 N·m | -- |
| M2.5 x 6 nylon, module to MP-01 (stage 2) | 24 | 0.25 N·m | -- |
| M12 x 1.5 gland locknut, harness entries | 2 | the gland maker's figure, once one is chosen | -- |

Every fastener in this table is counted per pod, and every one of them is derived from a
feature in the released model rather than from a catalogue. `mech/HARDWARE_SCHEDULE.md`
carries the arithmetic and, line by line, what is still an open purchasing choice.

**The M12 gland of Rev A is a different part and is still gone.** It belonged to WH-08, the
captive host lead, and both are deleted from the Phase 1 build. The two glands above are the
helmet harness entries, in the pod wall, and they are fitted.

### 5.2 Phase 2: the occipital shell

The HM-01 frame carries a 116 x 46 x 88 mm occipital shell for Phase 2. The Rev B carrier is
**150 x 130 mm and does not fit it**, and the growth from 130 x 124 mm has made that worse,
not better. If the Phase 1 measurements confirm that the module route is the fleet route,
the carrier is re-panelled into two boards split at the zone line at x = 62 mm, and this
document is re-issued with a Rev C stage 4 covering the two-board stack, the shell gasket
and the quarter-turn HM-08 battery hatch. **That design does not exist yet, and the board
sizes it would need have not been calculated.** Nothing in stage 5.2 can be quoted or built
today, and a bidder should price Phase 2 pod integration as an option with that stated.

> **Conformal coating -- the decision, taken and written down**
>
> EEG-CAR-01 is **not conformally coated** for Phases 1 and 2. This is a decision, not a
> deferral, and it supersedes any statement elsewhere in the package that no coating
> decision has been taken. The reasoning: the board sits in a gasketed POD-P1 on a bench,
> never near the head, coating cannot be retrofitted once the modules are inserted, and
> masking a board with thirty connectors and a socketed DevKit costs more than it buys. The
> mitigations are the POD-P1 gasketing above, the no-clean flux residue left in place, and a
> service rule that a gel-contaminated board is cleaned and re-tested to TST-EEG-004 T8 and
> T9 rather than wiped and returned to service (SVC-EEG-013). It is revisited before Phase 3,
> when the electronics move onto the head, or sooner if a unit returns with corrosion. If
> coating is later adopted, the masking list is essentially every connector: all 25 socket
> strips, J13, J15 to J17, J24, SW1 to SW3, the four M3 holes, TP1 to TP18, FID1 to FID3 and
> the label area.

---

## 6. Stage 5 -- firmware load and provisioning at end of line

Run with the pod open, before the lid goes on, so that the eFuse state, the ATECC608B
serial and the board serial are bound in one operation and recorded together.

### 6.1 What the operator runs

1. Scan the board serial with the barcode scanner. The station will not proceed without it.
2. **Connect the flashing lead to the DevKitC-1's own UART USB-C port**, reached through the
   31 x 61 mm opening in MP-01. That port carries the auto-reset circuit -- DTR and RTS to
   EN and IO0 -- **on the DevKit itself**, which is what puts the module into download mode.
   **Do not flash through J26.** J26 is a 1×6 console and recovery header (DVDD3V3, DGND,
   UART0 TX, UART0 RX, RESET_EN and NC_GPIO0) and it **cannot** enter download mode, because
   GPIO0 is committed to LED_SR_LATCH (ECO-EEG-009) and way 6 is a spare that does not reach
   it. A fixture that toggles J26 way 6 will do nothing.
3. Verify the release integrity first. Compare the SHA-256 of every file against
   `manifest.json` from the release manifest. Do not flash an image whose hash does not
   match.
4. Flash:

   ```
   esptool.py --chip esp32s3 --port <p> --baud 921600 write_flash \
     --flash_mode qio --flash_size 16MB \
     0x0 bootloader.bin 0x8000 partition-table.bin \
     0xF000 ota_data_initial.bin 0x20000 eeg_field_kit.bin
   ```

5. Run the provisioning script named in FW-EEG-001 section 7.2. It opens the CDC port, reads
   back the UNPROVISIONED iSerial, writes the ATECC608B configuration zone from the
   template, locks it, generates the P-256 key pair in slot 0, reads the public key and the
   9-byte device serial, and writes the NVS `eegcfg` namespace.
6. Reboot and confirm the device re-enumerates within 2 s with the provisioned iSerial
   (RFQ F-05).
7. After TST-EEG-004 completes, run the write-back step to store the calibration constants
   into NVS and the caldata partition. That write-back includes the **codec volume clamp
   required by RFQ E-29**: the headphone output must not exceed 100 dB SPL at any commanded
   level, the calculated full-scale output is about 110 dB SPL, and the clamp value is the
   one measured at calibration. A unit whose clamp is not written is not finished.

> **Irreversible steps -- read before running**
>
> Locking the ATECC608B configuration zone cannot be undone. The script requires an explicit
> `--lock` and prints the scanned board serial back for confirmation. A board locked with the
> wrong template loses only the ATECC breakout, because J11 is socketed; hold 10 % spare
> breakouts.
>
> **eFuses are not burned on the Phase 1 prototypes.** Secure boot and flash encryption are
> disabled for both prototypes so that the firmware volunteer can iterate on unsigned images,
> and are enabled from Phase 2 onward. This is a scoped, recorded deviation against RFQ F-19.
> TST-EEG-004 T25 is therefore a **Phase 2 onward** step and is not a Phase 1 gate; do not
> hold a prototype for it. Once the eFuses are burned, the ESP32-S3 module is part of the
> instrument identity and is no longer a field-swappable part, which qualifies the general
> claim in DSN-EEG-003 section 2 that any module can be unplugged. The manufacturer never
> holds the signing key; it receives pre-signed binaries and a public-key digest file only.

### 6.2 What is recorded

Per unit, into the as-built and calibration record (schema in QP-EEG-010):

| Field | Source |
|---|---|
| Unit serial, format **`TIOV-B-nnnn`** | allocated by the programme in blocks |
| Carrier board serial, fabrication lot, fabrication date | stage 1 IQC |
| Module type, manufacturer, serial or lot, for all thirteen assemblies | stage 2 IQC |
| ADS1299 date code and lot, per module, and which is device #1 | stage 2 IQC |
| 18650 cell lot and the UN 38.3 test summary reference | stage 4 |
| microSD model and lot | stage 2 IQC |
| Firmware version, image SHA-256, flash date, station id | stage 5 |
| ATECC608B serial (18 hex), public key, fingerprint | stage 5 |
| Codec volume clamp value written (RFQ E-29) | stage 5 |
| eFuse summary output | stage 5, Phase 2 onward |
| Operator id and date, per stage | sections 8 and 9 |

The public-key fingerprint is defined once, in **FW-EEG-001 section 7**, and is not
redefined here. It appears on the label, in the record and in the USB descriptor chain, and
the three must agree.

**Serial format.** The serial is `TIOV-B-nnnn`. The format is defined once, in **PKG-EEG-015
section 5**, and is not redefined here; the `OV-EEG-<phase><nnn>` form used in Rev A of this
document is withdrawn, along with the two competing forms that appeared in v1 drafts. The same
string appears identically in the label text, the Data Matrix, the USB `iSerialNumber`, the
calibration record and the packing list. QP-EEG-010 section 9 owns the device history record in
which each allocated serial is entered.

---

## 7. Stage 6 -- final assembly, labelling and kit packing

1. **Safety check before labelling.** Confirm the DevKitC-1's own USB-C connectors are not
   reachable from outside the closed pod, and that the only exposed host connector is the
   ADuM4160 module's (RFQ E-24, S-03). They are used at the factory only, for the stage 5
   flashing, and must not be accessible to a participant. Confirm the charge input at J24
   carries no data conductor. Confirm the helmet cannot be worn while the charge cable is
   connected, which is what the two interlocks of RFQ S-01 exist to guarantee.
2. **Label.** ART-LBL-01, 50 x 25 mm, matt polyester with permanent acrylic adhesive,
   IPA-resistant, applied to the flat keep-out on the POD-P1 lid outer face. Content: unit
   serial in the `TIOV-B-nnnn` form, hardware revision `EEG-CAR-01-B`, the key fingerprint
   plus a Data Matrix of the full value, `RESEARCH INSTRUMENT -- NOT A MEDICAL DEVICE`, and
   one.witysk.org (RFQ M-03). A duplicate goes inside the case lid.
3. **Verify the label against the record.** Scan the Data Matrix and compare it with the
   provisioning output. The label is generated from the record, so a mismatch means the
   wrong label went on the wrong unit and both are quarantined.
4. **Kit.** Pack per PKG-EEG-015 and tick its packing list line by line. The list is the
   authority; this document does not duplicate it. The calibration certificate travels in
   the **case lid pocket**, beside the quick-start card. The helmet travels assembled and
   upright, supported at the halo, so nothing bears on the electrode cups.
5. **Confirm the HM-09 service key is NOT in the kit.** It is deliberately absent from the
   participant's kit and is held by the operator.
6. **Lithium.** The protected 18650 is fitted in the pod. Whether a charged spare travels in
   the case is a programme decision recorded in PKG-EEG-015; either way the cell is packed in
   a protective sleeve and the carton carries the correct UN 3481 packed-with-equipment
   marking and the courier declaration text. The procedure lives in **PKG-EEG-015 section 7**
   and is not restated here. Do not ship without it.
7. **Outer carton.** Double-wall, with a transparent pocket for the pre-paid return label
   (RFQ M-07). The travel case is not the shipping container.

---

## 8. Per-stage labour estimate

These are **estimates**, derived from the part counts in `tools/design.py` and normal
industry rates. Nothing has been built and no time has been measured. They exist so that a
manufacturer has a starting point to price against and can tell the programme where the
estimate is wrong. Minutes of hands-on labour per unit, excluding batch set-up and excluding
TST-EEG-004.

| Step | Phase 1 (2 units, hand) | Phase 2 (10, machine SMT) | Phase 3 (25 to 50, selective THT) |
|---|---|---|---|
| 1.1 Incoming bare-board check, including the inner-layer evidence | 8 | 8 | 8 |
| 1.2 Stencil print | 3 | 3 | 3 |
| 1.3 SMT placement, 152 fitted parts | 102 | 4 | 4 |
| 1.4 Reflow | 6 | 6 | 6 |
| 1.5 AOI and touch-up | 12 | 5 | 5 |
| 1.6 Through-hole, 236 joints | 95 | 95 | 16 |
| 1.7 Through-hole inspection | 12 | 12 | 12 |
| **Stage 1 subtotal** | **238** | **133** | **54** |
| 2.1 MP-01 preparation, standoffs | 12 | 12 | 12 |
| 2.2 Module IQC and recording, 13 assemblies | 18 | 18 | 18 |
| 2.3 Module mounting on MP-01 | 20 | 20 | 20 |
| 2.4 Ribbon jumper set | 60 | 25 | 25 |
| 2.5 DevKit insertion and seating check | 5 | 5 | 5 |
| 2.6 Jumper fitting and keying check | 20 | 20 | 20 |
| **Stage 2 subtotal** | **135** | **100** | **100** |
| 3.1 HM-01 IQC and channel pull-through | 20 | 20 | 20 |
| 3.2 Bond 8 x HM-04 (plus 24 h cure) | 40 | 40 | 40 |
| 3.3 Contact-light LEDs | 30 | 30 | 30 |
| 3.4 Thread both harnesses | 45 | 45 | 45 |
| 3.5 Cover strips | 10 | 10 | 10 |
| 3.6 Yoke and ratchet | 12 | 12 | 12 |
| 3.7 Chin strap | 8 | 8 | 8 |
| 3.8 Boom | 10 | 10 | 10 |
| 3.9 TPU pads | 5 | 5 | 5 |
| 3.10 Umbilical entries: jig, drill and ream OE-1 and OE-2, deburr, re-run the draw cord, fit HM-12 and both glands (4.1 step 5, 4.4 steps 1 and 2) | 15 | 15 | 15 |
| **Stage 3 subtotal** | **195** | **195** | **195** |
| **Stage 4 pod integration**, including the two pod harness glands and their locknuts | **82** | **82** | **82** |
| **Stage 5 firmware and provisioning** | **16** | **16** | **16** |
| **Stage 6 final assembly and packing** | **43** | **43** | **43** |
| **Total hands-on per unit** | **709 min (11.8 h)** | **569 min (9.5 h)** | **490 min (8.2 h)** |

Line 3.10 and the five minutes added to stage 4 are new at this issue and are estimates on
the same basis as the rest of the table: they are the operations the released harness
entries need, which did not exist when the table was first written. **Line 3.10 disappears
once a parametric HM-01 prints OE-1 and OE-2**, leaving only the two minutes it takes to fit
the plate and the glands; it is drilling work that exists because the frame is a carried-over
mesh, and a bidder should be told that it is temporary rather than find it in the price
forever.

Batch set-up, once per build and not per unit: stencil and printer set-up 20 min, feeder
load 90 min (Phases 2 and 3), reflow profiling 45 min on a four-layer profiling board,
selective solder programme 40 min (Phase 3), provisioning station 20 min, bonding fixture
15 min. The vision-teach set-up of Rev A is gone: the board now carries three fiducials and
the machine registers on them.

The Phase 3 total assumes the ribbon jumper set is bought pre-made and the through-hole is
selectively soldered. If either assumption fails, add 35 and 79 minutes respectively.

The "25 minutes per unit" test figure that appeared in DSN-EEG-003 Rev A.2 is withdrawn; it
was arithmetically impossible. Test time is costed in TST-EEG-004 Rev C, which owns the step
numbers and their durations, not here.

---

## 9. Per-stage sign-off

The operator completes one of these per unit. It travels with the unit and is scanned into
the as-built record at stage 6. A stage cannot begin until the previous stage is signed.

**Unit serial: TIOV-B-______  Carrier board serial: ____________  Build date: __________**

| Stage | Check | Value or tick | Operator | Date |
|---|---|---|---|---|
| 1 | Bare board IQC passed, fab lot recorded | lot: ________ | | |
| 1 | Outline 150.0 x 130.0 mm, thickness 1.60 mm | ____ x ____ mm | | |
| 1 | Four layers confirmed against the stack-up report | ☐ | | |
| 1 | Inner-layer evidence received; plane split at x = 62 mm and the isolation keep-out bare on all four layers | ☐ | | |
| 1 | Vias tented both sides; FID1 to FID3 present and clean | ☐ | | |
| 1 | Reflow profile within the section 2.5 envelope, four-layer profiling board | peak ____ °C, TAL ____ s | | |
| 1 | AOI clean, **152 parts present and correct** | ☐ | | |
| 1 | **R89 absent** | ☐ | | |
| 1 | **R90 fitted, single link, not bridged** | ☐ | | |
| 1 | **R91 fitted, single link, not bridged** | ☐ | | |
| 1 | R92, R93, R94 and R95 fitted (or ECO removal noted) | ☐ | | |
| 1 | Through-hole vertical fill ≥ 75 % (class 2) on every barrel; J15 to J17 additionally 100 % circumferential wetting both sides; no thermal relief flooded | ☐ | | |
| 1 | J6 to J7 spacing 22.86 mm, DevKit seats | ☐ | | |
| 2 | Thirteen module assemblies inspected, serials recorded | ☐ | | |
| 2 | ADuM4160 isolation type-test certificate seen and recorded | ☐ | | |
| 2 | ADS device #1 identified and labelled | #1 = ________ | | |
| 2 | ATECC part is -SSHDA, not -TNGTLS | ☐ | | |
| 2 | Standoffs are M3 x 18 mm **male-female**, four nylon screws at the plate end | ☐ | | |
| 2 | Torques applied: 0.40 / 0.25 N·m | ☐ | | |
| 2 | Every jumper labelled both ends, WH-KEY-01 shrouds fitted per ICD-EEG-006 section 6 | ☐ | | |
| 2 | Stack height measured against 55.5 mm internal (budget 49.1 mm) | ____ mm | | |
| 3 | All 10 frame channels pull-through passed | ☐ | | |
| 3 | OE-1 and OE-2 at x = -16.00 / +16.00, y = -103.01, Ø12.50 mm; swarf cleared and the rear sagittal channel re-proved | ☐ | | |
| 3 | HM-12 fitted and both glands clamped onto the jacket **before** the jacket was cut back | ☐ | | |
| 3 | Eight HM-04 bonded, fixture used, cured | cure start ______ | | |
| 3 | Bond pull-off sample (per lot) | ____ N | | |
| 3 | Eight LEDs fitted, marked lead to LEDn, windows outward | ☐ | | |
| 3 | Both harnesses threaded, 120 mm service loop | ☐ | | |
| 3 | Screen terminated at pod end only | ☐ | | |
| 3 | Yoke, strap, boom fitted at stated torque | ☐ | | |
| 4 | Gasket seated, no twist, joint at a corner | ☐ | | |
| 4 | Panel parts fitted and aligned; isolator connector type recorded | USB-B / USB-C | | |
| 4 | Eight M3 brass inserts set square, flush to 0.3 mm below the boss face; insert part recorded | insert: ________ | | |
| 4 | Both harness glands fitted with their locknuts inside, before the stack went in; gland part recorded | gland: ________ | | |
| 4 | Lid closed, 4 x M3 at 0.60 N·m, two passes | ☐ | | |
| 4 | Cell fitted only after T3 passed (no thermistor fitted, S-04 open) | ☐ | | |
| 5 | Firmware image hash verified against manifest | fw: ________ | | |
| 5 | Flashed through the DevKitC-1 UART USB-C port | ☐ | | |
| 5 | Flash and provisioning completed | ☐ | | |
| 5 | ATECC serial and fingerprint recorded | fp: ________ | | |
| 5 | Codec volume clamp written (RFQ E-29) | ____ | | |
| 5 | Re-enumeration within 2 s confirmed | ☐ | | |
| 6 | DevKit USB not externally reachable | ☐ | | |
| 6 | Label applied, Data Matrix verified against record | ☐ | | |
| 6 | Kit packed, PKG-EEG-015 list ticked, certificate in the case lid pocket | ☐ | | |
| 6 | HM-09 service key **not** in the kit | ☐ | | |
| 6 | Lithium marking and documentation present | ☐ | | |

---

## 10. Rework rules

| Situation | Rule |
|---|---|
| SMD pad, any | maximum 2 reflow or rework cycles per pad, then the board is scrap |
| Plated through-hole barrel | maximum 2 rework cycles per barrel |
| Alloy at rework | SAC305 only. Leaded solder is prohibited everywhere |
| R90 or R91 disturbed | replace the part. Touch-up is not permitted |
| Thermal relief flooded to a reference plane during rework | the joint is reworked back to a four-spoke relief, or the board is scrap. A solid plane connection at a socket pin is not a cosmetic defect |
| Socket strip replacement | full removal, barrel cleaning, re-inspection. No partial pin repair on J2, J4, J14, J23, J29 or J30 |
| J2, J4 or J14 replaced | the board re-runs TST-EEG-004 T7, T8 and T9 in full |
| Reversed SOT-23 or SOIC found after power-up | treat the associated rail as suspect: replace the part **and** the parts it could have back-fed, then re-run T3 and T8 |
| Bonded HM-04 defect | the frame is scrap. There is no approved de-bond process |
| Blocked frame channel | scrap at stage 3.1, before wiring |
| ATECC config zone locked with a wrong template | replace the breakout at J11 only; the board is not scrap |
| eFuses burned in error (Phase 2 onward) | the ESP32-S3 module is scrap; the unit returns to the programme for re-provisioning under a new serial |
| Anything else | a written concession signed by the programme before shipment. No verbal changes, no build from a file that did not arrive under an ECO |

Every rework is logged per serial, with the refdes, the reason, the cycle count and the
operator, and the log is returned with the unit.

Defect disposition, applied at AOI and at final inspection:

| Class | Examples on this board | Disposition |
|---|---|---|
| Critical | reversed BAV99 (16 opportunities), reversed OPA4376, R90 or R91 bridged, populated R89, DevKit that will not seat across J6 and J7, a BAT54S fitted at D1 to D16 | scrap or full rework with re-test; never accept |
| Major | tombstoned 0603 (127 opportunities), bridged SOIC-14 lead, insufficient barrel fill, flooded thermal relief, non-perpendicular socket strip, bent module pin | rework, re-inspect, log |
| Minor | legend smear, cosmetic mask blemish clear of a pad, flux residue outside a joint | accept with a note |

---

## 11. What this document does not settle

Stated plainly, because the manufacturer will otherwise assume it has been decided.

| # | Item | Effect on this build |
|---|---|---|
| 1 | **No safety engineer has reviewed the design.** | Blocks use on a person. Does not block building, testing or quoting. |
| 2 | The routing is machine-generated and **has not been reviewed by a human layout engineer**. The DRC report at `kicad/EEG-CAR-01_RevB_DRC_report.txt` lists **zero violations**: all 145 nets are fully connected, each reference plane is one continuous island per net, the isolation strip is free of copper on all four layers, and every geometric rule passes -- clearance, width, annular ring, hole size, edge, non-plated hole, isolation and via keep-out. The same report lists **169 connections the router had to relax** to get there: 36 narrower than the 0.25 mm preferred width, 133 at full width with a reduced gap, all at or above the 0.20 mm minimum conductor and gap. The board closes at minimum geometry, not with margin, and that is what the layout review has to judge. | **The fabrication data is RELEASED FOR REVIEW under RFQ-EEG-002A, not released for fabrication**; that review is the human layout review the routing has not had. Stage 1 still needs boards that have been fabricated, and none has been. |
| 3 | ECO-EEG-023 moves U7 to DVDD3V3 and DGND and is **not yet in `design.py`** (section 2.4). | The prototypes are built as drawn. The safety and layout reviewer must rule on the change before it is cut. |
| 4 | **Corrected 2026-09-02: ECO-EEG-024 is applied and R1 to R16 are 68 kΩ**, so RFQ S-02 single-fault DC current is **calculated at 36.8 µA against a 50 µA limit and is met on the calculation**. This item read "calculated at 53.2 µA … therefore not met with the 47 kΩ resistors fitted". | **Build with 68 kΩ.** Do not substitute 47 kΩ, which is now the superseded value. Measure it at T23 all the same, and do not record S-02 as *verified*: nothing has been measured and the safety reviewer has not signed SR-01. |
| 5 | RFQ E-23 and S-04 require a charge inhibit above 45 °C; **there is no thermistor net or connector way on Rev B, so it is not met** (section 5.1 item 5). | Open hardware item. It does not block assembly and it does block use on a person. |
| 6 | **Corrected 2026-09-02: the contact-light bicolour phase driver is written** (section 4.3), so T11 is no longer blocked by missing code. This item read "not implemented, so TST-EEG-004 T11 cannot pass". T11 has still never been run, because no unit exists. | LED orientation is verified by the operator at fitting until T11 has been run and passed on a real unit. |
| 7 | **Closed in the model, still open in the purchasing documents.** The standoff and the POD-P1 boss want the same four M3 holes; `pod_base()` resolves it with a brass insert in the boss and a **male-female** standoff (section 3.3). *Was: "no fastener arrangement is drawn".* | AVL-EEG-017 section 1.6 and kit BOM item 31 still buy a **female-female** standoff, which has no stud and cannot make this joint. The pod cannot be closed on the part that is currently on order. |
| 8 | **Closed.** POD-P1-01 Rev B carries two M12 x 1.5 cable-gland harness entries, one per helmet cable, with locknut seats and P-clip bosses (section 5.1 item 3). *Was: "POD-P1 has no harness entry feature".* | The bores are printed; the gland itself is not a chosen part (item 18). |
| 18 | **None of the fixing hardware the released geometry needs has a vendor part.** Eight M3 brass inserts, four M3 x 12 lid screws, four male-female standoffs, two P-clip screws and four M12 x 1.5 glands per kit. The size and length of each is derived in `mech/HARDWARE_SCHEDULE.md`; the part behind each is not chosen, and three of the lines are on no purchasing document at all. | A pod cannot be ordered complete. Sizes are settled, so nothing is blocked at the bench once the parts are bought. |
| 19 | **The released HM-01 has one wiring channel per branch where WH-EEG-008 section 7 has two**, so both cables share a channel and the shared rear sagittal run is at 76 % fill against a 50 % limit (section 4.4). | Conductors are laid in and never pulled, and a single conductor cannot be replaced by drawing it through. It belongs to the parametric HM-01, not to this stage. |
| 20 | RISK-EEG-011 H-05 and SF-9 exclude an LED conductor contacting an electrode conductor **on the strength of separate channels the released frame does not have** (section 4.4). | The exclusion is not supported by the geometry as built. It blocks the safety argument, not the build. |
| 21 | The two rear halo anchor pockets, the two temple anchor slots and the left temple socket that section 4.5 fits parts into **are located and dimensioned nowhere** -- not in the HM-01 mesh, not on MECH-EEG-020 sheet 3. | Set the yoke from its own two anchor points and mark the frame from the yoke. Nothing else in section 4.5 can be checked against a drawing. |
| 22 | **HM-12 and the harness-entry gland carry proposed identifiers, not issued ones.** PARTS-EEG-019 section 1.2 reserves HM-12 to HM-19 for Phase 2 and has POD-P1-01 to -05 allocated; HM-12 and POD-P1-06 are proposed in `mech/HARDWARE_SCHEDULE.md`. | HM-12 ships **unmarked** until the register issues a number, against the section 4.1 marking rule, and is identified by its bag label. |
| 9 | The isolator module's host connector is USB-B on the named candidate, against RFQ E-24's USB-C; WH-09 is the interim pigtail. | Check the delivered module before dressing the panel. |
| 10 | The boom preamplifier part is **not settled**; the module is specified by interface only (section 3.1). | Accept against ICD-EEG-006, not against a part number. |
| 11 | J15, J16 and J17 are named as a class, Stäubli SLB1,5-F, not as a confirmed PCB part. | A touch-proof 1.5 mm socket with a PCB-mount signal pin and two 1.5 mm retention posts must be sourced and first-articled; AVL-EEG-017 carries a 12-week lead-time risk. |
| 12 | The adhesive in 4.2 has not been tested on this programme's dyed MJF PA12, and the HM-01 pocket dimension is not generated by any source file. | The first-article 100 N pull-off is the first evidence. Measure the pocket before the first bond. |
| 13 | The carrier draws a calculated 288 mA worst case from the DevKit's on-board 3.3 V regulator, about 0.5 W inside a closed pod. | TST-EEG-004 T3 measures it and reports the case temperature. Above 85 °C, a carrier-side 3.3 V regulator is an ECO against Rev C. This is not solved. |
| 14 | The Phase 2 occipital shell needs a two-board carrier that does not exist, and the 150 x 130 mm board does not fit the shell. | Stage 5.2 cannot be built or quoted today. |
| 15 | The ribbon jumper set is hand-built per unit. | It is the largest avoidable cost in stage 2 and the reason a Phase 2 consolidation is planned. |
| 16 | JIG-EEG-009 has not numbered the socket comb or the transit retention bar in its FIX-01 to FIX-04 scheme. | Named by function in sections 1.4 and 3.6 until it does. |
| 17 | Nothing in this package has been manufactured or measured. | Every figure marked calculated or estimated is exactly that. |
