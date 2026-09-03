# EEG Field Kit -- Manufacturing Design Package

**Document:** DSN-EEG-003 **Revision:** C **Date:** 1 September 2026
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** hardware and documents CC BY-SA 4.0; firmware MIT
**Supersedes:** DSN-EEG-003 Rev B in its entirety
**Revision note (Rev C):** the carrier is now 150.0 × 130.0 mm and four layers rather than
130 × 124 mm and two, the enclosure and module plate grew to match, the ECO register runs to
ECO-EEG-027, and every finding of the 1 September 2026 cross-document audit is closed here or
named as open. The findings of the second cross-document audit of 1 September 2026 are also
closed in this issue: section 3.4 now carries the routing result and the release state
transcribed from the DRC report, section 6 cites TST-EEG-004 Rev C by its own section
numbers, and the rulings register RUL-EEG-021 and the production simulation SIM-EEG-018 are
in Annex A. These are corrections within the Rev C release and the revision letter is not
advanced for them.

**Correction within Rev C, 2 September 2026.** The carrier now routes to completion: the DRC
reports **zero violations, all 145 nets one connected copper island, and both inner planes
continuous under the analogue zone** -- the three conditions of the ECO-EEG-016 section 3 gate.
Section 3.4 carries the current result and the release state, which is **released for review
under RFQ-EEG-002A and not released for fabrication**, because no human layout engineer has yet
looked at the routing. ECO-EEG-016 section 2B records how the board was closed. This too is a
correction within the Rev C release and the revision letter is not advanced for it.

**Second correction within Rev C, 2 September 2026, after the independent review of package
v2.2.** Section 4's mechanical file table listed two CASE-00 foam DXFs that no longer exist:
`mech/` holds the seven **Rev C** layer files and the Rev B pair is deleted. The table is
rewritten against the shipped files, and the true part of the old entry is kept -- the seven are
drawn and **not released for cutting**. Annex A's SIM-EEG-018 figures, which stood at two
different totals in this document, are now quoted from the run of `tools/simulate_production.py`
of 2 September 2026. Annex A also marks which sections of DSN-EEG-002 Rev E are superseded,
because that document has not been re-issued and is cited here as a live source.

**Third correction within Rev C, 2 September 2026, after the design and firmware changes made
that day.** Four things this document carried as open are now closed in the design, and they
are corrected in place, with their date, rather than deleted. **S-02 is met** at 36.8 µA:
ECO-EEG-024 is applied and R1-R16 are 68 kΩ, not 47 kΩ. **E-11 is met in both halves**:
the Sallen-Key low-pass moved from X7R to C0G -- 10 nF and 22 nF with 215 kΩ, f0 49.9 Hz.
**E-27 is met**: the bicolour contact-light phase driver is written. And **the firmware is
built**, against a real ESP-IDF v5.2.5, and has booted once under QEMU. The bias-lead topology
was fixed in the same pass -- D11 and C11 now sit on BIASOUT behind the series resistor like
the other fifteen channels -- and the board came out of that repair at **145 of 145 nets, zero
violations, 3 745 track segments and 552 vias**. None of this is hardware: no board has been
fabricated, no firmware has run on silicon, and no safety reviewer has signed anything.
`KNOWN_ISSUES.txt` section 0i is the record of the change. This too is a correction within the
Rev C release and the revision letter is not advanced for it.

**This is the governing document of package v2.** Where any other document in the package
disagrees with it, this one governs -- with one exception: where a number appears both here
and in `tools/design.py`, `design.py` governs, because every fabrication file is generated
from it.

---

## Why this revision exists

Rev A.2 said, honestly, that a manufacturer could quote from the package but could not build
from it, because the carrier board was placed and netlisted but unrouted and the firmware had
never been compiled. It also said that the files had been attacked for consistency. They had
not been attacked hard enough.

Package v2 was produced by generating the whole carrier from a single machine-readable design
description and then checking it -- netlist connectivity, geometric clearances, zone rules,
star-point uniqueness -- against that description rather than against prose. Doing so found
fourteen defects in Rev A that the prose review had missed, four of which made the board
impossible to build at all:

* the eight contact-light lines existed on the harness connector with **nothing driving them**;
* there was **no source for the 3.3 V rail** -- the charger's system output, the DevKit's 5 V
  pin and both ADS1299 module supplies were all unconnected nets, so the board could not
  have powered up;
* the second amplifier of each envelope detector had **its inverting input unconnected**, so
  the 50 Hz filter was not in circuit;
* the shift-register lines were assigned to **GPIO35, 36 and 37, which carry the octal PSRAM**
  on the ESP32-S3-DevKitC-1-N16R8, so the firmware pin map could not have worked.

There were also no mounting holes, although the specification sheet promised four; the
DevKit header spacing was 22.0 mm where the real part is 22.86 mm; and the six non-plated
retention holes of the touch-proof EMG sockets were declared on the copper and mask layers,
which would have plated them and tied those sockets to the analogue reference pour.

**Rev C exists because doing the layout, rather than asserting that the layout would be
easy, changed the board twice.** Package v1 and Rev B both stated that a two-layer carrier of
130 × 124 mm was enough. It is not, and the two findings are engineering results rather than
preferences:

* **The board grew to 150.0 × 130.0 mm.** Thirty connectors, 211 reference designators and
  156 nets would not close at the smaller outline. The extra 33.8 cm² of bare board costs a few
  euro per unit at these quantities, against a real risk of an unroutable design.
* **The board went to four layers: L1 signal, L2 reference plane, L3 reference plane, L4
  signal.** On two layers the bottom side has to be both the reference plane and the second
  routing surface, and it cannot be both. Four layers give two full routing surfaces and a
  continuous reference under every analogue trace, which is exactly what the "layout rules
  that are requirements, not preferences" of **DSN-EEG-002 section 13** ask for, and what the
  zoning, star-point and isolation rules of **section 3.3 below** ask for, and which a
  swiss-cheesed two-layer pour cannot deliver. At 2 units the extra cost
  is about €35 in total; at 50 units it is about €3 per board. That is the right trade for a
  sixteen-channel EEG front end, and it is the single most important thing package v2 learned
  by doing the work instead of asserting it.

A cross-document audit of the whole package on 1 September 2026 then found sixty places where
seventeen documents written from one fact base disagreed with each other, with the fact base,
or with `design.py`. Every one has been ruled on. The rulings that change the design are
ECO-EEG-019 to ECO-EEG-027, indexed in section 9 and written out in ECO-EEG-016 section 2.

What has *not* changed is the honest line at the end of Rev A.2, and it is repeated in
section 11: no safety engineer has reviewed this design, the firmware has never run on
hardware, and nothing here has been manufactured or measured.

---

## 1. What the manufacturers said, and what package v2 answers

Nine manufacturers answered RFQ-EEG-001. Read together, their replies define the production
package a manufacturer needs. Rev A.2 delivered part of it. This is the complete list and
where each item now is.

| What a manufacturer asked for | Where it is in package v2 |
|---|---|
| Routed Gerbers | `kicad/gerber/` -- Gerber X2, one file per copper, mask, legend and paste layer plus the board profile, zipped and checksummed. Four copper layers, not two |
| Drill data | `kicad/gerber/EEG-CAR-01-PTH.drl` and `-NPTH.drl`, Excellon 2, metric, split plated / non-plated. Through vias only |
| Netlist for bare-board test | `kicad/gerber/EEG-CAR-01-IPC-D-356A.ipc` |
| BOM with part numbers | `kicad/EEG-CAR-01_RevB_BOM.csv` and AVL-EEG-017 |
| Pick-and-place | `kicad/EEG-CAR-01_RevB_CPL_SMT_top.csv` (SMT) and `_CPL_THT_top.csv` (through-hole) |
| Fabrication drawing | `kicad/EEG-CAR-01_RevB_fabrication_drawing.pdf` -- outline, drill schedule, stack-up, notes |
| Assembly drawing | `kicad/EEG-CAR-01_RevB_assembly_drawing.pdf` -- designators, pin 1, DNP list, process notes |
| Schematic | `schematic/SCH-EEG-005_RevB_schematic_set.pdf` -- eight sheets. Rev A had none at all |
| Firmware | `firmware/` -- source, build system, configuration, provisioning script, host tool |
| Validated production-test specification | TST-EEG-004 Rev C, standalone, with fixtures in JIG-EEG-009 Rev B |
| Mechanical files | `mech/` -- STL, STEP, 2D drawings in MECH-EEG-020, DXF for all seven CASE-00 Rev C foam layers |
| Everything else a line needs | ICD-EEG-006, ASM-EEG-007, WH-EEG-008, QP-EEG-010, PKG-EEG-015 |

The carrier board file name keeps its `RevB` stem because `EEG-CAR-01` is still board revision
B: Rev C of this document changes the outline and the layer count of that board, and the
fabrication set is regenerated in one pass by `tools/emit_all.py` from `tools/design.py`. A
manufacturer holding an older Gerber set with a 130 × 124 mm profile or a two-layer stack-up
has a superseded set and must ask for the current one.

Regulus's correction to our contact list is carried forward: that company is ISO 9001, not
ISO 13485. The RFQ requests no certification, so this is informational, but the contact
workbook has been corrected.

---

## 2. Architecture: modules on a carrier

Unchanged in principle from Rev A.2, and the reasoning stands: buy every block that is hard
to get right and design only the board that connects them. What has changed is that the
connection is now specified properly.

**Twelve module types, thirteen module assemblies per unit** -- the ADS1299 breakout is
fitted twice. Twelve of the thirteen mount on the MP-01 module plate; the
ESP32-S3-DevKitC-1-N16R8 is inserted directly into J6 and J7. The carrier carries **thirty
connectors, J1 to J30, of which seventeen are module connectors**.

The blocks are: two ADS1299 8-channel analogue front ends (PIEEG-8 class); the
ESP32-S3-DevKitC-1-N16R8 controller, whose radio is never initialised; an ES8388 codec module
with headphone amplifier; an ADuM4160 USB isolator module carrying the barrier and the host
socket; an ATECC608B secure element; a bq24074-class charger with power path and a MAX17048
gauge; a TPS63020-class buck-boost; a microSD breakout on one-bit SDMMC; the voice-microphone
preamplifier; a room-microphone module with hardware mute; and a 74HC595 shift-register module
for the contact lights.

**Which module lands on which connector is tabulated once, in ICD-EEG-006 section 1**, with
the pinout of every socket and the jumper schedule. That table is not repeated here; a second
copy is a second thing to keep in step, and in package v1 it had already drifted in four
places.

**Where the voice-microphone preamplifier lives.** It is **on the MP-01 module plate,
connected at J21**. The boom carries the bare electret capsule and its screen, on the pigtail
at J18. Package v1, and Rev B of this document, said the preamplifier was on the boom.
`design.py` governs and it is not: J21 is a carrier socket.

**Which preamplifier is not settled, and must not be quoted as settled.** The package-v1
candidate, the MAX9814, has automatic gain control, which RFQ E-14 forbids; disabling it is a
module-dependent modification rather than a configuration. The preferred route is a fixed-gain
part of the MAX4466 class. Until a part is bought and measured, the module is specified **by
interface** in ICD-EEG-006, and AVL-EEG-017 keeps the MAX9814 listed as not approved.

### 2.1 The change that matters: modules are not plugged directly in

Rev A.2 drew module sockets on the carrier and left the geometry to chance. No public
standard fixes the header positions of a PIEEG-8, an ES8388 breakout or a bq24074 module, so
a socket at a chosen coordinate is a guess, and a wrong guess is discovered when the boards
arrive.

Package v2 removes the dependency. **Every module except the DevKit mounts on the printed
module plate MP-01 above the carrier and connects with a keyed 2.54 mm ribbon jumper.**
The carrier sockets are then placed for routing convenience rather than to match an unknown
module footprint, and a different module of the same interface class can be fitted by making
a different jumper. ICD-EEG-006 gives the interface each module must present, the jumper
schedule and the qualification procedure for a substitute.

**Jumper keying is now decided, and is not left to the builder.** At the module end the
jumper terminates in a 2.54 mm shrouded polarised IDC header where the module has one, and
where it does not, pin 1 is marked and the jumper is labelled. At the carrier end every socket
that takes a jumper wears the printed keying shroud **WH-KEY-01**, which is part of the MP-01
print set. ICD-EEG-006 section 6 lists which sockets get one.

The ESP32-S3-DevKitC-1 is the exception: its geometry *is* public, so it is inserted directly
into J6 and J7, on the correct 22.86 mm row spacing.

The cost of this decision is honest: a hand-made jumper set per unit, roughly twenty minutes
of assembly labour, and a 60 mm length limit on the analogue jumper because the ten-way
ribbon has no interleaved grounds. That ribbon is also why RFQ E-04 has been restated:
−100 dB of channel-to-channel crosstalk is not achievable through 60 mm of un-interleaved
ribbon and is about 40 dB below this instrument's own noise floor, so it is not measurable
either. **E-04 is now −80 dB at 50 Hz, measured on the carrier**, with the ribbon's own
contribution characterised once on the first prototype (ECO-EEG-026). A consolidated board
removes the jumper set and the crosstalk argument together, and remains the right answer for a
larger fleet.

### 2.2 The ADS1299 module choice

Unchanged from Rev A.2. The package specifies the module by interface rather than by brand.
Phase 1 buys two PIEEG-8 and, as the reference amplifier for the section 8 comparison test,
one OpenBCI Cyton. ICD-EEG-006 section 2 states the exact interface a substitute must meet:
the digital header must expose SCLK, MOSI, MISO/DOUT, DRDY, CS, START, RESET, CLK, DVDD3V3,
5 V and ground; the analogue header must expose IN1–IN8, SRB1, BIASOUT, BIASIN, AVDD, AVSS
and an analogue reference pin.

---

## 3. Carrier board EEG-CAR-01 Rev B

### 3.1 What is in the package

| File | Content | Status |
|---|---|---|
| `kicad/EEG-CAR-01_RevB_routed.kicad_pcb` | routed board: tracks on L1 and L4, through vias, reference planes on L2 and L3 | regenerated by `emit_all.py` |
| `kicad/gerber/*.gbr`, `*.drl`, `*.ipc` | Gerber X2, Excellon 2, IPC-D-356A | regenerated by `emit_all.py` |
| `kicad/EEG-CAR-01_RevB_DRC_report.txt` | every rule, every measurement, every violation | **the release gate: see 3.4** |
| `kicad/EEG-CAR-01_RevB_BOM.csv` | grouped BOM with manufacturer part numbers | complete |
| `kicad/EEG-CAR-01_RevB_CPL_SMT_top.csv` | pick-and-place, bottom-left origin, Y up | complete |
| `kicad/EEG-CAR-01_RevB_CPL_THT_top.csv` | through-hole positions for selective or hand solder | complete |
| `kicad/EEG-CAR-01_RevB_fabrication_drawing.pdf` | dimensions, drill schedule, four-layer stack-up, notes | complete |
| `kicad/EEG-CAR-01_RevB_assembly_drawing.pdf` | designators, pin 1, DNP, process | complete |
| `kicad/EEG-CAR-01_RevB_copper_layers.pdf` | all four copper layers at 1:1 for review | complete |
| `schematic/SCH-EEG-005_RevB_schematic_set.pdf` | eight sheets | complete |
| `tools/` | the generator, the router, the DRC and this board's source | complete |

### 3.2 The board

This table is the single specification of the bare board. AVL-EEG-017, QP-EEG-010 and
ASM-EEG-007 cite it and do not restate it.

| Property | Value |
|---|---|
| Size | **150.0 × 130.0 mm**, rectangular, no cut-outs, no slots |
| Layers | **four**: L1 signal, L2 reference plane, L3 reference plane, L4 signal |
| Stack-up | mask / 35 µm L1 / prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask = **1.60 mm ± 10 %** |
| Material | FR-4, Tg ≥ 150 °C, 1 oz (35 µm) outer copper, 0.5 oz (17 µm) inner copper |
| Finish | ENIG, Au 0.05–0.10 µm over Ni 3.0–6.0 µm |
| Mask / legend | green LPI both sides; white legend both sides |
| Minimum track / clearance | 0.20 mm / 0.20 mm; most conductors are 0.25 mm or wider |
| Electrode-net clearance | 0.35 mm to anything else |
| Vias | **through vias only**: 0.60 mm pad, 0.30 mm finished hole, 0.15 mm annular ring, tented both sides. No blind, buried, back-drilled, filled or plugged vias anywhere |
| Plated hole sizes | 0.30 mm (vias), 0.90 mm (JST PH), 1.00 mm (socket strips), 1.20 mm (tactile switches), 1.70 mm (DIN 42802 signal pin) |
| Plated-hole census | 236 plated holes in those five sizes, across 33 through-hole parts |
| Non-plated holes | 4 × 3.2 mm (M3, 6 mm copper keep-out on every layer), 6 × 1.50 mm (DIN retention posts) |
| Mounting | M3 at (5, 5), (145, 5), (5, 125), (145, 125) |
| Zone split | x = 62.0 mm: analogue to the left, digital to the right |
| Reference planes | AGND_REF left of x = 62 mm and DGND right of it, **on both L2 and L3**, tied together by stitching vias |
| Fiducials | three 1.0 mm round fiducials with 3.0 mm mask openings, at (12, 10), (144, 100) and (12, 120) |
| Class | IPC-6012 class 2 (fabrication), IPC-A-600 class 2 (bare board), IPC-A-610 class 2 (assembly) |
| Electrical test | 100 % to the supplied IPC-D-356A netlist |
| Parts | **211 reference designators, 636 pads, 156 nets**; of the designators, 186 are placed parts (153 surface-mount, of which R89 is do-not-populate, and 33 through-hole), and the remaining 25 are 18 test points, 3 fiducials and 4 mounting holes |
| Net census | 156 nets; 620 of the 636 pads carry a net; **11 nets have a single pad** (test points, spare ways and no-connects) and **145 nets have two or more pads**. The netlist figure is 156 and the connectivity figure is 145 -- see the note at the end of 3.4 |
| Process | SMT on the top side only; all through-hole parts on the top side. L4 carries routing, copper and legend, and no parts |
| Conformal coating | **none for Phases 1 and 2.** The board lives inside a gasketed enclosure, and masking 30 connectors and a socketed DevKit costs more than the coating buys. Revisited before Phase 3 if a returned unit shows corrosion |

**A note on the fiducials.** They are new in package v2 and they replace the vision-teach
workaround of Rev B, which asked the placement machine to teach on test-point pads
(ECO-EEG-020). **RUL-EEG-021 section B** records their positions as (12, 10), (144, 100)
and (12, 120), which is where `design.py` places them and what the table above carries. The
register's first issue transcribed them as (8, 8), (142, 8) and (8, 122); that error is
corrected, and `design.py` governs in any case.

**Coordinate convention.** The design source uses a top-left origin with Y increasing
downward, which is the KiCad convention. Gerber, drill and both CPL files use a **bottom-left
origin with Y increasing upward**, which is what CAM expects. The conversion
`y_out = 130.0 − y_design` is applied once, in `tools/gerber.py`, and is stated again in
`kicad/gerber/README_layer_map_and_checksums.txt`. Rev A's CPL used negative Y values with no
stated origin; that is corrected. The constant changed with the board height at Rev C, so any
file generated against `124.0` is superseded.

### 3.3 Layout rules -- how they were applied, not just stated

Rev A.2 gave the rules as a brief for a layout engineer. In package v2 the same rules are
encoded as constraints in the router and re-measured afterwards by the DRC, on the finished
geometry rather than on the routing grid. Rules 2 and 4 below are the home of the star-point
rule and the isolation keep-out for the whole package; every other document cites this
section rather than restating them.

**A citation note, because three documents got it wrong.** This document has sections 1 to 11
and two annexes. **It has no section 13.** The phrase "layout rules that are requirements,
not preferences" belongs to **DSN-EEG-002 section 13** and any citation of it means that
document. The zoning rule, the star-point rule and the isolation keep-out belong to
**DSN-EEG-003 section 3.3**, which is this section, and any citation of them means this one.

1. **Two zones divided at x = 62 mm.** Analogue to the left: the harness socket, the sixteen
   protection networks, both ADS1299 analogue interfaces, the three envelope detectors, the
   comparator, the electrode panel. Digital to the right: MCU, codec, isolator, storage,
   charger, lights. *Verified:* the DRC counts digital nets inside the analogue zone and
   analogue nets outside it and reports zero of each. One signal crosses by design --
   CMP_RAW, the comparator output, which must reach a 3.3 V GPIO; it does so through R83 and
   the D23 clamp.

2. **AGND_REF is the analogue 0 V mid-rail, not ground.** AVDD = +2.5 V and AVSS = −2.5 V are
   generated on ADS1299 module #1 and brought onto the carrier at J23. AGND_REF is poured on
   **L2 and L3** over the whole analogue zone; L1 and L4 are left free for routing, which is
   the point of going to four layers. It joins DGND at **R90 only**; HARN_SHIELD joins DGND at
   **R91 only**. Both are 0 Ω 0603 parts, not copper bridges, so either can be lifted for a
   leakage measurement and refitted. *Verified:* the DRC counts the bridges and reports one
   of each.

3. **Every electrode net is routed on L1 with the reference plane continuous beneath it**, at
   0.35 mm clearance to any other net rather than 0.20 mm. The protection network for each
   input is placed in a straight line -- resistor, clamp, filter capacitor -- from the harness
   towards the module. On two layers this rule and rule 2 were in direct conflict, because the
   only available plane was also the only second routing surface. On four layers they are not.

4. **The isolation barrier is on the module, and the carrier stays out of its way.** The
   ADuM4160 module carries the 2.5 kV barrier; no carrier copper crosses it because nothing on
   the carrier is on the host side. What the carrier must guarantee is that no copper sits
   *under* the module's host half, so the strip **x ≥ 141.0 mm, y = 2.0 to 22.0 mm** is free of
   copper on **all four layers** and is marked on the legend and the fabrication drawing.
   *Verified:* the DRC reports no copper inside the strip on any layer.

5. **USB_DP and USB_DN** are a 0.30 mm pair on 0.35 mm spacing, routed on L1 directly over the
   DGND plane on L2 -- about 95 Ω differential on this stack-up. No coupon and no impedance
   test are required, and the fabrication drawing says so explicitly so that nobody quotes for
   one.

6. **Envelope decoupling** is within 3 mm of pins 4 and 11 of each OPA4376, and the three
   envelope outputs run directly to J4 pins 4–6.

7. **No via inside the analogue module connector outlines** (J2, J4, J23, J29). *Verified.*

8. **Non-plated holes carry no copper and no solder-mask opening**, and are supplied in a
   separate drill file. This closes ECO-EEG-012: in Rev A the six DIN retention holes were
   declared on `*.Cu` and `*.Mask`, which would have plated them and connected the
   touch-proof EMG socket bodies to the analogue reference pour.

9. **Through vias only.** Every via passes through all four layers. No blind, buried,
   back-drilled, filled or plugged via is used anywhere on the board, so the four-layer stack
   is quotable at any fabricator's standard price and there is no sequential lamination.

### 3.4 How the routing was produced, and what that means

The board was routed by the programme's own constraint-aware maze router
(`tools/router.py`): a Dijkstra search on a 0.1 mm grid over four layers with a via cost, the
rules of 3.3 encoded as hard keep-outs and zone masks, a rip-up-and-retry pass for connections
that the first pass could not make, a via-push pass that moves any via that ends up inside
another net's clearance, and reference planes built as real polygons on L2 and L3 with
four-spoke thermal reliefs on same-net through-hole pads. L1 and L4 carry signals only.

**This must be read as what it is.** The geometry is measured, not asserted: every clearance
is taken between the real polygons the Gerbers are written from. The result is transcribed
below from `kicad/EEG-CAR-01_RevB_DRC_report.txt`, which is the authority for it. This
paragraph is not the authority: if the table below and the report ever differ, the report is
right and this document is corrected.

| What the DRC measured | Value | Rule |
|---|---|---|
| Board | 150.0 × 130.0 mm, four copper layers | -- |
| Track segments | 3 745 | -- |
| Through vias | 552 | -- |
| Pour islands | 4 -- **each reference plane is one continuous island per net, on both L2 and L3** | one island per net per plane |
| Smallest clearance on L1 | 0.260 mm | 0.20 mm |
| Smallest clearance on L2 and L3 | 0.285 mm | 0.20 mm |
| Smallest clearance on L4 | 0.275 mm | 0.20 mm |
| Narrowest conductor | 0.20 mm | 0.20 mm minimum |
| Connections the router had to relax | **169** -- 36 narrower than the 0.25 mm preferred width, 133 at full width with a reduced gap | every one at or above the 0.20 mm minimum conductor and gap |
| Smallest plated hole | 0.30 mm | 0.30 mm |
| Non-plated holes | 10 | -- |
| Digital nets inside the analogue zone | **0 zone crossings** | 0 |
| AGND_REF-to-DGND bridges | **1** (R90) | exactly 1 |
| HARN_SHIELD-to-DGND bridges | **1** (R91) | exactly 1 |
| Duplicate copper | **0** segments, **0** via positions | 0 |
| Nets checked for connectivity | 145 | -- |
| Nets fully connected | **145** | 145 |
| Nets with no copper at all | **0** | 0 |
| **Violations** | **0** | 0 |

**There are no violations.** The report's own line is: "VIOLATIONS: 0 -- none.  The board
passes every rule listed above." Every net the connectivity check grades is one connected
copper island, none is left without copper, and the two electrode-clearance vias at 0.328 mm
that earlier issues of this section recorded are gone. There are no clearance violations of
any kind, and no track width, annular ring, plated-hole size, board-edge, non-plated-hole,
isolation keep-out or via keep-out violation. In particular the isolation strip at **x ≥
141.0 mm, y = 2.0 to 22.0 mm is clear of copper on all four layers**, and that is said here
because the report says it: the keep-out is now enforced against copper *edges* rather than
track centrelines, which is what earlier revisions got wrong. How the board was brought to
this state is recorded in **ECO-EEG-016 section 2B**.

**What closing it cost: 169 relaxed connections.** On 169 pad-to-pad connections the router
had to take the tightest geometry the rules allow -- 36 with a conductor narrower than the
0.25 mm preferred width, and 133 at full width with a reduced gap. Every one is at or above
the 0.20 mm minimum conductor and the 0.20 mm minimum gap, so none of them is a violation,
and none of them is comfortable either. The route this document carried before it closed
relaxed 19. **A board that closes at minimum geometry is not the same board as one that
closes at preferred geometry, even when every rule passes**, and those 169 places are where
the layout reviewer starts. The DRC report lists them by net and by pad pair, split into the
two kinds, so a reviewer can go straight to where the router had to squeeze. The list counts
*connections*; the `tracks below 0.25 mm` figure under MEASURED counts *segments*, and one
connection is many segments, which is why the two numbers differ.

**The fabrication data is RELEASED FOR REVIEW under RFQ-EEG-002A. It is not released for
fabrication.** ECO-EEG-016 section 3 sets the gate for releasing fabrication data as zero DRC
violations, every net one connected copper island, and both inner planes continuous under the
analogue zone. **All three are now met.** What has not happened is the review: the routing was
produced by the programme's own tools and no human layout engineer has looked at it, and
fabrication release awaits RFQ-EEG-002A. A manufacturer may quote from this data set and may
plan from it. **No document in this package may describe the fabrication data as released for
fabrication, or say that boards may be ordered from it, before that review is closed**, and no
document may state a DRC result -- including that the board now passes -- without checking the
report, as this section has.

**Why the DRC counts 145 nets and section 3.2 counts 156.** `design.py` declares **156 nets**
across 211 reference designators and 636 pads, 620 of which carry a net. Eleven of those 156
nets have a single pad -- test points, spare ways and no-connects -- and a net with one pad has
nothing to join, so `tools/netcheck.py` does not check it. The connectivity check therefore
reports on **145 nets, and all 145 are fully connected**. Both figures are correct for what
they count. **156 is the netlist figure**: it is what the IPC-D-356A file and the 100 % bare-board
electrical test of section 3.2 are written against. **145 is the connectivity figure**: it is
what the DRC report grades and it can never exceed 156. Any document quoting either number
states which of the two it is quoting.

The routing has *not* been reviewed by a human layout engineer, and an autorouter has no
opinion about return paths, coupling or manufacturability beyond the rules it was given.
Passing every rule it was given does not change that. RFQ-EEG-002A is therefore re-scoped
from *route this board* to **review this routing -- the 169 relaxed connections first --
correct what is wrong and sign it off**: a much smaller and cheaper task than routing from a
blank sheet, and one that starts from data that closes.

---

## 4. Printable and mechanical parts

The part-identifier register PARTS-EEG-019 is now the single authority for every part number
in the package. It exists because Rev A used `HM-xx` as two overlapping namespaces -- figure
labels and part numbers -- with the result that **HM-07 named the boom microphone arm in
DSN-EEG-002 section 10 and the battery hatch in DSN-EEG-003 section 4 and in the STL set**.
A manufacturer printing "HM-07" would have produced a different part depending on which
document was open. Figures are now `FIG-nn` and `HM-xx` is reserved for parts.

**The enclosure and the module plate grew with the board.** POD-P1 and MP-01 are generated by
`tools/mech_gen.py` from the same `BOARD_W` and `BOARD_H` as the carrier, so they follow the
outline change automatically; the figures below are the current ones.

| File | Part | Bounding box (mm) | Volume (cm³) | Process |
|---|---|---|---|---|
| `HM-01_frame_monocoque.stl` | HM-01 helmet frame | 191.1 × 229.6 × 158.0 | 133.6 | MJF PA12 |
| `HM-02_brow_pad.stl` | HM-02 brow pad | see MECH-EEG-020 | see PARTS-EEG-019 §2 | MJF PA12 or TPU |
| `HM-04_electrode_assembly_body.stl` | HM-04 electrode assembly, 8 fitted + 2 spare = 10 per kit | 12.4 × 12.4 × 18.0 | 1.9 | MJF PA12 |
| `HM-08_battery_hatch.stl` | HM-08 quarter-turn hatch (was HM-07 in Rev A) | 48.0 × 36.0 × 6.5 | 6.9 | MJF PA12 |
| `HM-09_service_key.stl` | HM-09 cup service key, one per operator, **not a kit item** | 17.9 × 17.9 × 40.2 | 3.9 | MJF PA12 |
| `MP-01_module_plate.stl` | MP-01 module mounting plate | **146.0 × 126.0 × 3.0** | see PARTS-EEG-019 §2 | MJF PA12 |
| `POD-P1_prototype_enclosure_base.stl` | POD-P1 base | **163.0 × 143.0 × 58.0 external; 158.0 × 138.0 × 55.5 internal** | see PARTS-EEG-019 §2 | MJF PA12 or FDM PETG |
| `POD-P1_prototype_enclosure_lid.stl` | POD-P1 lid, with a 2.0 mm spigot | **163.0 × 143.0 × 6.0** | see PARTS-EEG-019 §2 | MJF PA12 or FDM PETG |
| `FIT-01_fit_test_coupon.stl` | FIT-01 fit-test coupon, printed with every batch, bores 9.20 / 9.35 / 9.15 mm | 60.0 × 24.0 × 10.0 | see PARTS-EEG-019 §2 | same process as the batch |
| `CASE-00_foam_layer_1.dxf` | CASE-00-01 foam layer 1 of 7, all nine bays, helmet bay at the 181 × 220 mm shelf opening | 516.0 × 390.0 sheet, 25 thick, 1:1 in mm | -- | die-cut or laser-cut |
| `CASE-00_foam_layer_2.dxf` | CASE-00-02 foam layer 2 of 7, all nine bays, helmet bay at the full 197 × 236 mm | 516.0 × 390.0 sheet, 25 thick, 1:1 in mm | -- | die-cut or laser-cut |
| `CASE-00_foam_layer_3.dxf` | CASE-00-03 foam layer 3 of 7, five bays: helmet, headphones, pod, consumables, cables | 516.0 × 390.0 sheet, 25 thick, 1:1 in mm | -- | die-cut or laser-cut |
| `CASE-00_foam_layer_4.dxf` | CASE-00-04 foam layer 4 of 7, two bays: helmet, headphones | 516.0 × 390.0 sheet, 25 thick, 1:1 in mm | -- | die-cut or laser-cut |
| `CASE-00_foam_layer_5.dxf` | CASE-00-05 foam layer 5 of 7, helmet bay only | 516.0 × 390.0 sheet, 25 thick, 1:1 in mm | -- | die-cut or laser-cut |
| `CASE-00_foam_layer_6.dxf` | CASE-00-06 foam layer 6 of 7, helmet bay only | 516.0 × 390.0 sheet, 25 thick, 1:1 in mm | -- | die-cut or laser-cut |
| `CASE-00_foam_layer_7.dxf` | CASE-00-07 foam layer 7 of 7, helmet bay only | 516.0 × 390.0 sheet, 25 thick, 1:1 in mm | -- | die-cut or laser-cut |

The seven foam files are the **CASE-00 Rev C** stack of PKG-EEG-015 section 2.2, written by
`tools/mech_gen.py` `foam_dxf()`; the two Rev B sheets this table listed until the correction
of 2 September 2026 are withdrawn and deleted from `mech/`, because 50 mm of foam cannot hold
a 158 mm helmet. A bay is
drawn in a file only where the schedule cuts it through that layer, so the seven are not
interchangeable. **They are drawn and not released for cutting**: the 516.0 × 390.0 mm sheet is
the Peli 1560's published internal footprint minus 2 mm on each plan axis, and no shell has been
bought or measured -- PKG-EEG-015 section 3.2 re-draws the sheet to the measured footprint before
any foam is cut.

STEP files and dimensioned 2D drawings accompany each STL in `mech/step/` and
`mech/drawings/`, and MECH-EEG-020 is the drawing set. Rev A supplied STL only, from which no
one can dimension anything.

**MP-01.** An 8 mm solid border, a field of 12 × 3 mm jumper slots on a 16 × 7 mm grid, Ø2.7 mm
M2.5 clearance holes between the slot rows for the module fixings, one 31 × 61 mm opening over
the DevKit, and four Ø3.4 mm holes on the carrier mounting pattern.

**The carrier-to-plate standoff is M3 × 18 mm nylon hex, female-female, four off, with eight
M3 × 6 nylon pan screws.** Two documents previously dimensioned it and disagreed; 18 mm is the
figure, and it is load-bearing for safety, not only for fit: the slant path from carrier
copper, over the edge of the isolation keep-out and up the standoff to any host-side conductor
on MP-01 is at least 18 mm, which is more than twice the 8 mm the safety case asks for. That
closes RISK-EEG-011 SR-08. The full stack budget, which comes to 49.1 mm against 55.5 mm of
internal depth with 6.4 mm of margin, is tabulated once in ICD-EEG-006 section 4.

**POD-P1 panel openings.** The three response and stop buttons are 6 mm tactile switches with
12 mm coloured caps on extenders behind **13.0 mm openings on a 14 mm pitch** at y = 76, 90 and
104 mm on the right-hand wall. The host USB connection is **a socket, not a captive cable**:
the USB-C receptacle on the ADuM4160 module is presented through a gasketed aperture, and the
kit ships the two cables of RFQ A-07, one of which is the host lead. The cable gland and the
captive lead WH-08 are deleted from the Phase 1 build and are a Phase 2 item for the helmet
shell. **The pod carries no indicator light:** all eight lights are in the helmet and the pod's
state is read from the session runner, so the M-02 LED opening is withdrawn.

---

## 5. Firmware FW-EEG-001

`firmware/` now contains the build system, the configuration, the partition table, the
provisioning script and the host verification tool, not only `main.c`. FW-EEG-001 Rev C is
the specification, and it is the home of the public-key fingerprint definition that six other
documents cite.

**Corrected 2 September 2026.** Until that date this section said, plainly, that the firmware
*had never been compiled against a real ESP-IDF installation and had never run on hardware*.
The first half is no longer true. **The firmware is built:** ESP-IDF v5.2.5, target esp32s3,
and `firmware/release/` holds `bootloader.bin`, `partition-table.bin`, `ota_data_initial.bin`
and `eeg_field_kit.bin` with a `manifest.json` recording the SHA-256 of each; the linked image
is 405,245 bytes. It has also **run once, in an emulator**: `firmware/release/qemu_boot.log` is
a full boot cycle under `qemu-system-xtensa -M esp32s3` in which the second-stage bootloader
reads this partition table, the app is loaded from the factory slot, `app_main()` runs, the
microSD and ES8388 bring-up paths degrade gracefully when the peripherals do not answer, and
the PSRAM ring-buffer allocation failure is caught and aborted where FW-D13 says it should be.

**The second half is still true, and it is the half that matters: the firmware has never run
on hardware.** QEMU's esp32s3 machine has no octal PSRAM, no microSD, no ES8388 and no
ADS1299, so not one register value, daisy-chain order or SPI timing in this design is
evidenced by that run. A build is not a bring-up. Five drivers are still stubs (ES8388,
SDMMC, ATECC608B, MAX17048, the envelope onset detector). The pin map has been corrected
(ECO-EEG-009) and now avoids GPIO35, 36, 37 and 45. Completing the stubs and getting a clean
enumeration on three operating systems is the first task of the firmware volunteer or an ODM
line item, and TST-EEG-004 step T5 is its acceptance test.

Three firmware facts a manufacturer needs, each stated with its exception in the same
sentence:

* **The contact-light driver is written, and no light has ever been lit.** Corrected
  2 September 2026: until that date `lights_write()` and `lights_task()` were on/off only and
  this bullet said the bicolour scheme was not coded, so E-27 was not met and TST-EEG-004 step
  T11 could not pass. `lights_task()` reads the converter's positive-side
  lead-off comparator at **two thresholds** and alternates the green and red phases: a site
  that trips neither is green, one that trips only the sensitive threshold is amber, and one
  that trips both is red. `LIGHT_PHASE_HZ` is 240, but the half-phase quantises to the
  FreeRTOS tick, so the **actual alternation is about 250 Hz**, which is what E-27's "above
  100 Hz" asks for and what T11's colorimeter reads. **Corrected again 2026-09-02 (FW-D17):**
  this bullet read that the driver used both halves of the lead-off word and that red was
  unreachable until the N-side excitation was enabled. Enabling it would not have helped.
  **The montage is single-ended** -- J2 carries IN1 to IN8, one shared `SRB1` and `BIASOUT`
  -- so `LOFF_STATN` has no per-site electrode to report on, and with `SRB1` closed all eight
  N bits would have reported the one shared reference. The two-threshold sweep is what this
  hardware can actually support. One caveat stands and is not rounded away: no unit exists,
  so **T11 has not been run**, and the two `COMP_TH` values are the datasheet's endpoints
  rather than measured ones.
* **The eFuses are not burned on the Phase 1 prototypes.** Secure boot and flash encryption
  are enabled from Phase 2, so the two prototypes run unsigned images and TST-EEG-004 step T25
  is marked "Phase 2 onward" and is not a Phase 1 gate.
* **The PSRAM ring buffer is 6 MB, not the 12 MB that three minutes at 1000 Hz would need**,
  which is 126 seconds of raw samples (124 s counted over the framed stream). RFQ F-06 is therefore relaxed to 90 seconds of ring plus unlimited
  backfill from the microSD copy (ECO-EEG-025), rather than being quietly missed.

**End-of-line flashing goes through the DevKitC-1's own UART USB-C port**, which carries the
auto-reset circuit (DTR and RTS to EN and IO0) on the DevKit itself and is reachable through
the MP-01 opening. The carrier's J26 is a 1×6 console and recovery header and **cannot** enter
download mode, because GPIO0 is committed to LED_SR_LATCH (ECO-EEG-009) and J26 way 6 is a
spare, `NC_GPIO0`. No JTAG or SWD connector is fitted anywhere on the carrier; the ESP32-S3 is
programmed over UART0 and its native USB. RFQ E-28 has said so since RFQ-EEG-001 Rev D and
Rev E carries it unchanged, and the "E-28
deviation" notes that four documents carried against a 2×5 1.27 mm header are withdrawn
along with the header.

---

## 6. Production test TST-EEG-004 Rev C

Now a standalone controlled specification with fixtures designed in JIG-EEG-009 Rev B.
**TST-EEG-004 Rev C owns the step numbering for the whole package**; this document and every
other cites T-numbers from it and never invents one. Rev C runs **T00 to T29**.

It keeps the steps of Rev A and adds the ones package v2 needs: bare-board electrical test,
incoming inspection of modules, star-point verification with R90 lifted, insulation
measurement across the USB barrier, charge-interlock verification, contact-light colour
verification in all three states, one-bit SDMMC throughput at 1000 Hz, and a leakage
measurement standing in for patient auxiliary current. It carries a requirements-to-test
traceability matrix, so any mandatory requirement with no test is visible rather than assumed.

Two points of method that a test house must not get wrong:

* **The per-unit isolation test is a 500 V DC insulation-resistance measurement across the
  barrier, not a hipot.** The 2.5 kV RMS type test is the isolator module supplier's
  certificate and is checked once, at incoming inspection. No production station applies
  2500 V AC to a unit.
* **The fixtures are FIX-01 to FIX-04**, with sub-assemblies lettered FIX-01/A to FIX-01/G,
  FIX-02/A to FIX-02/D, FIX-03/A onwards and FIX-04/A to FIX-04/D. **The fixture table is
  TST-EEG-004 Rev C section 6.1**, which is its only home; JIG-EEG-009 Rev B designs the
  fixtures against those same letters and uses no others. The bare letters H-A, H-B and H-C
  and the names CPL-V and CPL-R are withdrawn. Contact-light colour is read by a
  TCS34725-class colorimeter head, FIX-01/E, taking the red-to-green ratio at each site.

A new type test is added at Rev C: **RFQ E-29 caps the headphone output at 100 dB SPL** at any
commanded level, measured on an artificial ear, with the firmware clamping the codec volume
register to the value measured at calibration. The requirement exists because the calculated
full-scale output is about 110 dB SPL. It is **step T28 of TST-EEG-004 Rev C**, listed among
the type tests in **TST-EEG-004 Rev C section 14** and run once per lot on one unit, not on
every unit.

---

## 7. What a manufacturer can and cannot do with this package

| Question | Answer | Why |
|---|---|---|
| Can you fabricate the bare board? | **Not yet: the data is released for review, not for fabrication.** | Gerber X2 for four copper layers, both drill files, IPC-D-356A netlist, fabrication drawing and stack-up are complete and checksummed; the DRC reports **zero violations** and every one of the 145 nets is one connected copper island (section 3.4). What is missing is not a number but a reader: **no human layout engineer has reviewed the routing**, and 169 connections sit at relaxed geometry. Quote from it today; fabricate from it once RFQ-EEG-002A has reviewed it and signed it off |
| Can you assemble it? | **Yes, firm** | BOM with manufacturer part numbers, SMT and through-hole CPL, paste layer, assembly drawing, work instructions |
| Can you print the mechanical parts? | **Yes** | STL, STEP and dimensioned drawings for every part. The foam is a separate answer: seven DXF layer files are drawn and **not released for cutting** until the case shell is measured -- section 4 and PKG-EEG-015 section 3.2 |
| Can you build the harness? | **Yes** | WH-EEG-008 gives a complete from-to wire list, materials, tooling and test |
| Can you provision and test a unit? | **Yes**, once the firmware image exists | TST-EEG-004 Rev C and JIG-EEG-009 Rev B are complete; the image is programme work |
| Can you ship a working prototype for software development? | **Yes for the hardware**; the firmware stubs are programme work | the prototype enumerates only once the stubs are done |
| Can you ship a unit for use on a participant? | **No** | the safety review has not been performed. It gates Phase 2 |

Quantities: Phase 1 is **2 prototypes**, Phase 2 is **10 kits**, Phase 3 is **10 to 40 further
kits, 25 to 50 in total**.

---

## 8. The re-issued RFQ

| RFQ | Scope | Sent to |
|---|---|---|
| **RFQ-EEG-002A -- layout review** | Review the supplied routing against the rules in section 3.3 -- the DRC now reports nothing to close, so the work is judgement rather than repair, starting with the 169 relaxed connections of section 3.4 -- correct what is wrong, and sign it off. Deliver a corrected board file, corrected Gerbers and a review note. One correction round. This replaces the *routing* scope of Rev A.2, because the board is now routed. Note that the board is four layers and 150 × 130 mm as of Rev C | JLCPCB layout portal, Makerfabs, Best Technology, any freelance layout engineer |
| **RFQ-EEG-002B -- manufacturing** | From the released fabrication package: 2 carriers, then 10, then 10–40; module procurement or consignment; MJF printing; harness assembly; provisioning and TST-EEG-004; kitting | HongRong, Elecrow, Regulus, PCBSync, Best Technology, Leiton, Eurocircuits, myProto, Dekimo |

Sponsorship: JLCPCB's open-source programme is applied to for the Phase 1 carrier fabrication
and prints, with the CC BY-SA repository as the application's centrepiece.

### 8.1 What the nine houses actually said

These are the replies to the first approach, in one line each, carried forward from
DSN-EEG-003 Rev A.2 Table 1. They are kept because they are the only commercial evidence
either package holds, and because the second column is the reason this design is
module-on-carrier rather than a single board of bare silicon.

| Company | Reply, in one line | Can do from a finished package | Follow-up |
|---|---|---|---|
| Leiton (Berlin) | No design capability; manufactures only from finished data | PCB + assembly | Re-send now that routed Gerbers exist |
| Regulus (Taiwan) | Scope beyond EMS; ISO 9001 not 13485; will reconsider PCBA and box-build once Gerber/ODB++, BOM, CPL, firmware and a validation plan exist | PCBA, box-build, test | Re-send the full production package; correct our ISO 13485 assumption in the contact list |
| HongRong (Shenzhen) | Good fit for PCB, PCBA, enclosure and kit; asks whether layout is done | All of it except layout | Answer: the carrier is routed, on four layers, and passes its DRC with zero violations; the routing is not yet reviewed by a layout engineer; send the package |
| Elecrow (Shenzhen) | Declines custom design and EEG; offers production, firmware flashing, test and packaging from a finalised design | Production and packaging | Send the package; ask for the PIEEG introduction |
| Makerfabs (Shenzhen) | ODM: schematic/layout/samples, files owned by customer; **Phase 1 design plus two samples US$20–30k** | Everything, at a price | Ask them to quote review of the supplied carrier file only -- a fraction of the blank-sheet number |
| JLCPCB | Layout portal, PCBA, 3D printing; will not source headphones, electrodes or cases; has a sponsorship programme | PCBA, enclosure prints, layout | Upload the carrier file to the layout portal; apply for sponsorship with the open-hardware repository |
| Best Technology / EBest | Reviewing with engineering; will quote within three weeks; sponsorship to be evaluated | Layout, PCBA, kit assembly | Send the package now so their review is of real files |
| RayPCB → PCBSync | Acquired; Stan will contact | PCB + assembly | Update contact to stan@pcbsync.com; send the package |
| NextPCB | Automated portal reply | Portal PCBA only | Drop from the mailing; portal upload now that the board is routed |

**Why this table governs the architecture.** Makerfabs' US$20–30k is a blank-sheet ODM
quotation for Phase 1 design plus two samples. The programme's entire Phase 1 materials
and assembly budget, at the two-unit break, is about EUR 4 300 including the one-off
placeholders (internal costed BOM Rev C, Kit summary). A blank-sheet design engagement is
therefore between four and seven times the whole of Phase 1, and that -- not a preference
for modules -- is why the instrument is built from breakout modules on a carrier the
programme routed itself. Six of the nine houses will work from a finished package and only
two will design one. **The package had to become the thing that is finished.**

Two of the nine replies are now out of date in the programme's favour: Leiton and NextPCB
both said "come back when it is routed", and it is routed.

---

## 9. Engineering changes

**This is an index, not the register.** ECO-EEG-016 section 2 is the register of record and
carries the finding, the reasoning, the verification and the impact of every change; where it
and this index differ, the register governs. ECO-EEG-016 is a **document** number and is not
also a change number: the change previously numbered ECO-EEG-016 is now **ECO-EEG-018**, so
that nothing shares a number with the register itself.

Fourteen changes, ECO-EEG-001 to ECO-EEG-014, are the carrier defects found in Rev A. Four of
them were blocking: the board as released in package v1 could not have been built.

| ECO | What was wrong in Rev A | Severity | What the current board does |
|---|---|---|---|
| 001 | LED1–LED8 had no driver: the 74HC595 outputs were not brought to the carrier | **blocking** | J19 widened to 1×16; R70–R77 added; bicolour phase scheme defined |
| 002 | No source for DVDD3V3; charger SYS, DevKit 5 V and both module supplies unconnected | **blocking** | J25 buck-boost socket, V5V rail, C70–C74 |
| 003 | No charge input; VBUS_CHG had one pad | **blocking** | J24 charge-only pigtail, F1 PTC, D24 TVS, VBUS_DET divider |
| 004 | Envelope filter not in circuit: op-amp B inverting input unconnected | **blocking** | OPA4376 quad, all four loops closed |
| 005 | BAT54S fitted the wrong way round in the rectifier | major | pin 3 to the op-amp output |
| 006 | Sallen-Key Q = 0.5 gave −3 dB at 31 Hz, outside E-11 | major | 22 k / 100 nF / 220 nF → 48.8 Hz, Q = 0.74. **Superseded 2 September 2026** by the C0G rescale of ECO-EEG-019's second half: **215 kΩ with 10 nF and 22 nF, f0 49.9 Hz**, Q unchanged at 0.742. The values in this row are no longer what is fitted |
| 007 | No mounting holes, although the spec sheet promised four M3 | **blocking** | MH1–MH4 with a 6 mm copper keep-out |
| 008 | J6/J7 row spacing 22.0 mm; the DevKit is 22.86 mm | **blocking** | 22.86 mm |
| 009 | Shift-register lines on GPIO35/36/37 -- the octal PSRAM on the -N16R8 | **blocking** | GPIO41/42/0; SD dropped to one-bit; 35/36/37/45 left open |
| 010 | ENV_CMP, MIC_BIAS and SPARE1/2 dangling; no room-microphone connector | major | U7 comparator, J28, protected spares to J22 |
| 011 | No analogue reference pin at the module connectors; both modules' rails hard-paralleled | major | AGND_REF on J23.4 and J29.4; R92/R93 separable |
| 012 | Non-plated holes declared on copper and mask | major | no copper, no mask, separate NPTH drill file |
| 013 | 2×10 analogue connectors had no escape route for the inner row | **blocking** | split into a 1×10 signal socket and a 1×6 rail socket per module |
| 014 | Eight digital light lines ran through the electrode harness | major | harness split into a 12-way screened electrode cable and a 10-way light cable |

Two of these -- 001 and 014 -- together resolve the finding Rev A.2 recorded as "the 74HC595
light driver and the harness LED lines are digital signals routed through the analogue
harness" and then accepted. It should not have been accepted. It is now fixed.

Three changes are structural, and one of them carries the geometry change of Rev C.

| ECO | What it changes | Severity |
|---|---|---|
| 015 | Part identifiers meant two different things: `HM-xx` was both a figure label and a part number, and HM-07 named two different parts. PARTS-EEG-019 is now the single register | major, documentation |
| 017 | Lithium shipping was never mentioned. RFQ S-09 is new, REG-EEG-012 section 3 states the obligation and PKG-EEG-015 section 7 gives the procedure for both legs | major, compliance |
| 018 | The routing is now supplied, so RFQ-EEG-002A becomes a review rather than a routing job. **Doing the routing grew the carrier from 130 × 124 mm to 150.0 × 130.0 mm and took it from two layers to four**, for the reasons given under "Why this revision exists"; POD-P1 and MP-01 follow the outline | scope, and a design change |

Nine changes come from the cross-document audit of 1 September 2026. Each is a real design
change and none is cosmetic.

| ECO | What it changes | Severity |
|---|---|---|
| 019 | C1–C16 are C0G and the package's part number was not: `GCM188R71H103KA37D` is an X7R part and is replaced by **`GCM1885C1H103JA16D`** (10 nF, C0G, 50 V, 0603). A 100 nF C0G in 0603/50 V is not a stocked part, so C21/C41/C61 were specified as X7R with a stated 15 % capacitance tolerance over temperature and the filter-corner tolerance in TST-EEG-004 was widened to match. **Corrected 2 September 2026: the network stopped asking for 100 nF.** The Sallen-Key capacitors scale down by ten and its resistors up by ten -- C21/C41/C61 are now the same **10 nF C0G `GCM1885C1H103JA16D`** the board already buys sixteen of as C1-C16, C22/C42/C62 are **22 nF C0G `GCM1885C1H223JA16D`**, and R25/R26 and their two sibling pairs are **215 kOhm** -- which leaves f0 at 49.9 Hz and Q at 0.742 and holds the corner inside 47.5 to 52.5 Hz on C0G's ±5 %. **E-11 is met in both halves**; the widened TST tolerance is no longer the reason it passes | major |
| 020 | Three 1.0 mm fiducials with 3.0 mm mask openings are added to the carrier; the vision-teach workaround is withdrawn | minor |
| 021 | R94 and R95, 4.7 kΩ to DVDD3V3, are added on SDA and SCL. Depending on whatever the modules happen to carry is not a design | major |
| 022 | R85 changes from 56 kΩ to 150 kΩ, giving 3.0 V at VBUS = 5 V, above the 2.48 V input-high threshold of a 3.3 V ESP32-S3 input. The 1.79 V of Rev B would not reliably assert the first of the two S-01 interlocks | major |
| 023 | U7 is powered from DVDD3V3 and DGND instead of AVDD and AVSS, so its output swings 0 to 3.3 V into GPIO3 with full margin and D23 becomes a belt-and-braces clamp. Its inputs are re-referenced to a DVDD3V3/2 divider and the envelope is AC-coupled into it. **The safety and layout reviewer must check this change specifically** | major |
| 024 | Single-fault DC current at the patient was **calculated at 53.2 µA against the 50 µA limit of S-02, so S-02 was not met.** Raising R1–R16 from 47 kΩ to 68 kΩ gives 36.8 µA, moves the corner to 234 Hz (−0.75 dB at 100 Hz) and raises total input noise to 0.31 µV, still inside E-03; E-10 moves from its ±0.5 dB branch to its ±1.0 dB branch, which that requirement already states for this case. **APPLIED 2 September 2026.** `design.py` fits **68 kΩ** at R1–R16 today, the same 0603 footprint on the same nets, so the board did not move; **S-02 is met at 36.8 µA**. Corrected on the same date: this row read "the ECO is open" and "47 kΩ is fitted on the Phase 1 prototypes". What is still open is the **safety sign-off** -- SR-01 is closed in the design and has not been reviewed -- and the measurement, which no unit exists to make | **was blocking for use on a person; now open for sign-off** |
| 025 | RFQ F-06 is relaxed from three minutes of ring buffer to **90 seconds plus unlimited backfill from the microSD copy**, because 12 MB of ring in 8 MB of PSRAM is impossible and the fitted 6 MB is 126 seconds | major |
| 026 | RFQ E-04 is restated from −100 dB to **−80 dB at 50 Hz, measured on the carrier**, with the ribbon's contribution characterised once on the first prototype | major |
| 027 | C20/C40/C60 change from 1 µF to 10 µF, keeping R20/R40/R60 at 10 kΩ, which moves the envelope AC-coupling corner from 15.9 Hz to 1.6 Hz; E-11 is restated as ≤ 2 Hz. At 15.9 Hz the coupling removed the speech envelope it exists to pass. **This ECO is implemented: `design.py` fits 10 µF at C20, C40 and C60 today, the corner is 1.6 Hz into 10 kΩ, and E-11 is met as fitted.** The 1 µF and its 15.9 Hz are the superseded Rev A values and are named nowhere else | major |

---

## 10. Adversarial review of package v2

Every file was attacked again, this time with the netlist and the geometry available to check
prose against, and then a cross-document audit compared all seventeen documents with each
other and with `design.py`. The ECOs above are what the attack found in the design. What
follows is what it found in the package as a whole, and what remains open.

| # | Finding | Severity | Action |
|---|---|---|---|
| 1 | The routing is machine-generated and **unreviewed by a person**. The DRC now reports **zero violations**, all 145 nets connected, each reference plane one continuous island per net -- and **169 connections at relaxed geometry**, 36 of them narrower than the preferred width. The data is therefore **released for review under RFQ-EEG-002A and not for fabrication**. Section 3.4 carries the full transcription; `kicad/EEG-CAR-01_RevB_DRC_report.txt` is the authority | **blocking for fabrication release, not for quoting** | RFQ-EEG-002A reviews the whole routing, the 169 relaxed connections first, and signs it off; the DRC report lists every squeeze |
| 2 | The analogue module jumper is a ten-way ribbon with no interleaved grounds | major | 60 mm length limit; screened ribbon specified; E-04 restated to −80 dB at 50 Hz on the carrier (ECO-EEG-026); consolidation is the Phase 2 fix |
| 3 | LED_V is driven directly by GPIO48 | medium | 1 kΩ series with Vf 2.0 V gives (3.3 − 2.0)/1000 = **1.3 mA per site and 10.4 mA total**, within the ESP32-S3 pin rating; R78 allows a 47 Ω alternate; a buffer is the fallback |
| 4 | GPIO0 is used as the shift-register latch and is a strapping pin | low | it is pulled up on the DevKit and is an input at boot; the latch is an input to the 595, so a static high is harmless. The consequence is that J26 cannot enter download mode, so end-of-line flashing uses the DevKit's own USB-C port (section 5) |
| 5 | Dropping microSD to one bit halves the headroom | low | the frame payload is **50.7 kB/s at 1000 Hz** (1015 bytes every 20 ms) against about 2 MB/s available at 20 MHz; E-20's ≈70 kB/s and F-12's ≈64 kB/s are allowances that include STATUS and SIGNATURE frames and filesystem overhead, and are not changed |
| 6 | The ADS1299 modules' analogue rails are still commoned by default | medium | R92/R93 are separable links with a stated measurement to decide |
| 7 | **Corrected 2 September 2026. S-02 is met at 36.8 µA.** This row read "single-fault patient DC current is 53.2 µA against the 50 µA of RFQ S-02, so S-02 is not met" until ECO-EEG-024 was applied | **no longer blocking on the calculation; open for safety sign-off** | ECO-EEG-024 is applied in `design.py`: R1-R16 are **68 kΩ**, not 47 kΩ, and the single-fault DC figure falls from 53.2 µA to **36.8 µA** on bound A and 30.0 µA on bound B. E-10 moves to its **±1.0 dB** branch, which that requirement already states for exactly this case. Applying the fix the analysis pointed to is not the same as having it approved: **SR-01 is closed in the design and not signed off**, and the electrical safety reviewer owns the disposition. The arithmetic for both values is in RISK-EEG-011 section 4, **which has not yet been re-issued for 68 kΩ and still prints 53.2 µA as the live state** |
| 8 | **The charge thermistor of RFQ S-04 is not implemented and stays not implemented** | major, open hardware item | there is no NTC net in `design.py` and no thermistor way on J12 or J13. It is listed as open here and in RISK-EEG-011, and it is never described as met. The 45 °C charge inhibit itself is RFQ E-23, met by the charger module's own thermal regulation |
| 9 | **Corrected 2 September 2026. The contact-light bicolour phase driver is written**, so E-27 is met in the firmware. This row read "specified and not coded" until that date | closed in the code, **open until a unit exists** | `lights_task()` reads `LOFF_STATP` and `LOFF_STATN` and alternates a green and a red phase; the alternation quantises to the FreeRTOS tick at about **250 Hz**, above E-27's 100 Hz. **TST-EEG-004 step T11 has not been run**, because no unit exists and no light has ever been driven, and a site that has lost contact currently shows amber rather than red because only `LOFF_SENSP` is enabled (section 5) |
| 10 | The isolator module's host connector is USB-B where RFQ E-24 asks for USB-C | **live non-conformance** | the interim answer is a short USB-B-to-USB-C panel pigtail, WH-09, until an isolator module with a USB-C host connector is qualified. It is not settled |
| 11 | J15–J17 have no confirmed part | open | `design.py` names Stäubli SLB1,5-F as a class, not a bought part. A touch-proof 1.5 mm socket with a PCB-mount signal pin and two 1.5 mm retention posts must be sourced and first-articled before Phase 2; AVL-EEG-017 carries a 12-week lead-time risk against it |
| 12 | The carrier draws a calculated 288 mA worst case from the DevKit's on-board 3.3 V regulator | medium, **not solved** | that is inside its rating but dissipates about 0.5 W inside a closed pod. TST-EEG-004 step T3 measures it and reports the case temperature; above 85 °C, a 3.3 V regulator on the carrier fed from V5V is **an ECO against Rev C of the board** |
| 13 | The comparator re-referencing of ECO-EEG-023 changes the only analogue-to-digital crossing on the board | major | it is called out explicitly for the safety and layout reviewer rather than buried in the ECO register |
| 14 | **Series 68 kΩ with 10 nF gives a 234 Hz corner and 0.75 dB of loss at 100 Hz.** Corrected 2 September 2026: this row read "47 kΩ … 339 Hz … 0.36 dB" until ECO-EEG-024 was applied | low | inside the **±1.0 dB branch of E-10**, which the requirement states for exactly the 68 kΩ case; the ±0.5 dB branch described the 47 kΩ that is no longer fitted. 4.7 nF is still the approved alternate |
| 15 | Nothing in this package has been manufactured or measured | **stated everywhere** | Phase 1 |
| 16 | No safety engineer has reviewed any of it | **blocking for use on a head** | RISK-EEG-011 is the pack the reviewer is given; the review gates Phase 2 |
| 17 | USB VID/PID are placeholders | medium, blocks the fleet not the prototypes | pid.codes application before Phase 2 |
| 18 | Module header geometry is still not fixed by anything | accepted | removed from the critical path by the jumper architecture; the cost is stated in 2.1 |
| 19 | The end-to-end production simulation (SIM-EEG-018 Rev A) is a simulation, not a build | **stated** | `tools/simulate_production.py`, re-run on 2 September 2026 after the design and firmware changes of that day, prints **193 checks passed, 0 failed and 6 known open items**, which is what SIM-EEG-018 Rev A carries. The six are: the linked image reports **static IRAM full with one byte free**; the v1 HM-01 mesh is two disconnected bodies; **no human layout engineer has reviewed the routing**; **E-27 has never been seen to light** (the driver exists, no unit does); the two board-current figures cannot both be right; and **SR-01 is closed in the design and not yet signed off**. Corrected 2 September 2026: this row read "171 passed, 0 failed and 5 known open items", and its five named E-11's low-pass half and E-27's missing driver, both of which are now met, and S-02's single-fault current, which is now met at 36.8 µA. It checks arithmetic, data integrity and procedure completeness; it cannot find what only a real build finds |
| 20 | Seventeen documents written in parallel from one fact base disagreed in sixty places | major, documentation | every disagreement was ruled on, the rulings that change the design are ECO-EEG-019 to ECO-EEG-027, and the structural rule from here is one table with one home and a cross-reference everywhere else |

---

## 11. The honest line

A manufacturer can quote, today, and can build most of it, today: the assembly, the printed
parts, the harness, the provisioning and the production test of TST-EEG-004 Rev C. The bare
board **cannot be fabricated yet**, and the reason has changed: the board now meets all three
conditions of the ECO-EEG-016 section 3 gate -- zero DRC violations, every net one connected
copper island, both inner planes continuous under the analogue zone -- so the fabrication data
is **released for review under RFQ-EEG-002A** -- but it stays unreleased for fabrication until
a human layout engineer has read the routing, the 169 relaxed connections of section 3.4
included, and signed it off. Nobody orders boards from it before that.

What a manufacturer still cannot do at all is ship a unit for use on a participant, because
the firmware stubs must be completed, RFQ S-04's thermistor does not exist, and
the safety review has not been passed. **Corrected 2 September 2026:** this sentence also
carried "RFQ S-02 is not met at the fitted 47 kΩ". ECO-EEG-024 is applied, R1-R16 are 68 kΩ,
S-02 is met at 36.8 µA on the calculation -- and the safety review that has to accept that
calculation still has not started, which is why the sentence still ends where it does. Those are the programme's tasks, not the
manufacturer's, and RFQ-EEG-001 Rev E says so.

No hardware in this package has been built: no board has been fabricated, nothing has been
manufactured, and nothing has been measured. **Corrected 2 September 2026:** this paragraph
began "Nothing in this package has been built", and the firmware is now an exception -- it is
built, and it has booted in an emulator, and it has never run on silicon (section 5).
**No safety engineer has reviewed this design.** Every
performance figure in it is calculated, and each one is labelled as calculated where it
appears. The first thing Phase 1 does is find out which of them are wrong.

---

## Annex A -- Package index and precedence

Precedence, highest first:

1. **DSN-EEG-003** -- this document
2. **RFQ-EEG-001** -- requirements and acceptance
3. **ICD-EEG-006** -- module interfaces
4. **SCH-EEG-005** -- schematic set
5. **DSN-EEG-002** -- helmet design and assembly
6. **PARTS-EEG-019** -- part identifier register
7. **RUL-EEG-021** -- rulings register
8. `EEG_kit_BOM_for_bidders_RevC.xlsx` -- kit BOM

**DSN-EEG-002 Rev E, at 5 in that list, has not been re-issued** since package v2.1 and the
shipped file is byte-identical; ECO-EEG-016 section 1.1 carries it as "released, not reissued
in this round". It still governs the helmet, but three of its sections are superseded and a
reader must not work from them. **Section 7** says a charged spare cell travels in the case and
describes the battery hatch as interlocked to the session state: no spare cell travels
(REG-EEG-012 Rev B section 3.1, RISK-EEG-011 Rev B section 6.1) and there is no hatch interlock
in this design and none may be claimed (REG-EEG-012 Rev B section 3.4). **Section 10**'s
`HM-07` / `HM-08` part numbering is superseded by PARTS-EEG-019 Rev B sections 3.1 and 3.2 --
HM-08 is the battery hatch, HM-10 the keyed cell carrier and HM-07A/B/C the boom arm.
**Section 11**'s travel-case figure draws the withdrawn two-layer foam and is superseded by the
CASE-00 Rev C schedule of PKG-EEG-015 section 2.2, which section 4 above follows. Its
section 13, the "layout rules that are requirements, not preferences" this document cites
throughout, is not affected. The re-issue is open document work under ECO-EEG-016, not a
decision still to be taken.

**Two documents joined the register on 1 September 2026 and are controlled.**

| Document | What it is | How to use it |
|---|---|---|
| **RUL-EEG-021** | The register of the answers the two cross-document audits of 1 September 2026 made, each made once so that every document could be corrected against it. It began as an internal worksheet and is now a controlled document because released documents cite it | Cite it as **RUL-EEG-021** with a section letter, for example RUL-EEG-021 section A for the geometry rulings and section B for the instrument rulings. It ranks below this document and RFQ-EEG-001: where a ruling has been absorbed into a higher document, that document governs, and where a ruling and `tools/design.py` disagree, `design.py` governs |
| **SIM-EEG-018** | The end-to-end production simulation record: **193 checks passed, 0 failed, 6 known open items**, as `tools/simulate_production.py` printed it on 2 September 2026 after that day's design and firmware changes -- static IRAM full with one byte free, the v1 HM-01 mesh being two disconnected bodies, the unreviewed routing, E-27 never having been seen to light, the two irreconcilable board-current figures, and SR-01 closed in the design and not yet signed off. Corrected 2 September 2026: this row read "171 passed, 0 failed, 5 open", whose list named E-11's low-pass half, E-27's missing driver and S-02's single-fault current, all three of which are now met | It is a record, not a specification, so it carries no precedence. It is evidence that the procedures and the arithmetic hang together, and it is not evidence that anything has been built |

**The current revision letter of every controlled document, and the list of which documents
are controlled at all, is in the register at ECO-EEG-016 section 1.** Revision letters are not
restated here, because a second list is a second thing to keep in step.

Where a number appears in a document and in `tools/design.py`, **`design.py` governs**, and
the document is corrected at the next revision. `tools/emit_all.py` regenerates every
fabrication file from it in one pass, so the package cannot drift.

Each of the following has exactly one home, and every other document cites it rather than
copying it.

| What | Its one home |
|---|---|
| The bare-board specification | section 3.2 here |
| The zoning rule, the star-point rule and the isolation keep-out | section 3.3 here |
| The routing result and the release state of the fabrication data | section 3.4 here, transcribed from `kicad/EEG-CAR-01_RevB_DRC_report.txt`, which is the authority |
| The "layout rules that are requirements, not preferences" | **DSN-EEG-002 section 13**. This document has no section 13 |
| The module-to-connector table and the GPIO map | ICD-EEG-006 sections 1 and 5 |
| The ECO register | ECO-EEG-016 section 2 |
| The series-resistor noise-and-flatness arithmetic, for both the 47 kΩ that was fitted and the **68 kΩ of ECO-EEG-024 that is fitted now** | RISK-EEG-011 section 4, which has not been re-issued since ECO-EEG-024 was applied and still presents 47 kΩ / 53.2 µA as the live state |
| The test step numbers, T00 to T29 | TST-EEG-004 Rev C |
| The test fixture table, FIX-01 to FIX-04 and their letters | TST-EEG-004 Rev C section 6.1 |
| The public-key fingerprint definition | FW-EEG-001 section 7 |
| The serial-number format `TIOV-B-nnnn` | PKG-EEG-015 section 5 |
| The lithium-shipping procedure | PKG-EEG-015 section 7, with REG-EEG-012 section 3 stating only the obligation |
| The rulings of the two cross-document audits | RUL-EEG-021 |

## Annex B -- Standard reply to the nine respondents

> **Subject:** RFQ -- EEG field kit -- routed four-layer production package now available (Gerbers, drill, CPL, schematic, test spec)
>
> Dear {{ organization }} team,
>
> When we last wrote, our package was complete except for the routing, and we said so. It is
> now routed. Attached is the full production data set: Gerber X2 and Excellon drill files, an
> IPC-D-356A netlist for bare-board test, a BOM with manufacturer part numbers, separate SMT
> and through-hole pick-and-place files, fabrication and assembly drawings, an eight-sheet
> schematic, the firmware with its build system and provisioning script, and a standalone
> production-test specification with its fixtures designed.
>
> Two things changed while we did the routing, and they change what you are quoting. The
> carrier is now **150.0 × 130.0 mm**, not 130 × 124 mm, and it is a **four-layer** board --
> signal, reference plane, reference plane, signal -- rather than two. We had asserted that two
> layers would be enough. Doing the layout showed that they are not: on two layers the bottom
> side has to be both the reference plane and the second routing surface, and a sixteen-channel
> EEG front end needs a continuous reference under every analogue trace. Through vias only,
> 0.60 mm pad on a 0.30 mm hole, 1.60 mm finished, no blind or buried vias.
>
> Regenerating the package from a single machine-readable source also found fourteen defects in
> the previous revision, four of which would have made the board unbuildable, and a
> cross-document audit found sixty more disagreements between the documents. They are listed in
> DSN-EEG-003 Rev C section 9. We would rather tell you that than have you find them.
>
> Two things we are asking for. First, if you have a layout desk: RFQ-EEG-002A is now a
> **review** of the supplied routing rather than the routing itself -- read it against the rules
> in section 3.3, correct what is wrong and sign it off. The DRC now reports zero violations
> and all 145 nets connected, so there is nothing left to close; what there is to judge is
> 169 connections the router had to take at relaxed geometry, and a routing no layout engineer
> has yet read. **Until that review is done the fabrication data is released for review and
> not for fabrication**, and we say so in section 3.4 rather than letting you find it.
> Second: RFQ-EEG-002B, fabrication and assembly at 2, 10, 25 and 50 units, module procurement
> or consignment, MJF printing, harness assembly, provisioning and test.
>
> The design files are and remain CC BY-SA 4.0, and we ask that any file you generate from them
> comes back to us under the same licence. The safety requirements of RFQ section 8 are
> unchanged; no certification is requested. Nothing in the package has been built and no safety
> engineer has reviewed it, which is why no unit will go on a person before that review.
>
> With thanks,
>
> Stephane van der Aa, Founder, TI One Voice -- one.witysk.org -- stephane@stepvda.com -- +32 493 70 16 01
>
> Attachments: `EEG_field_kit_package_v2.3.zip` (complete), or on request the fabrication subset
> `EEG-CAR-01_RevB_gerber_X2.zip` with `README_layer_map_and_checksums.txt`.
