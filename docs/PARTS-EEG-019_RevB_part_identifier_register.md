# PART IDENTIFIER REGISTER

**Document:** PARTS-EEG-019  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs.

**Revision note, Rev A to Rev B.** Re-issued against the 150.0 x 130.0 mm four-layer
carrier and the enlarged POD-P1 and MP-01: every bounding box and volume in section 2 is
regenerated from the released `tools/mech_gen.py` meshes, WH-08 is withdrawn and WH-09,
WH-KEY-01, WH-BUS-01 and the five WH-ADP adapters are registered, the unit serial format
is settled as `TIOV-B-nnnn`, and the duplicated foam-pocket and fixture-step lists are
replaced by cross-references.

**The findings of the second cross-document audit that name this register are closed in
this issue, within Rev B and without a further revision letter**: the layout-rule citation
is corrected to DSN-EEG-002 section 13 and DSN-EEG-003 section 3.3, the fixture
sub-assembly names and the fixture-to-step citations are aligned to TST-EEG-004 Rev C
section 6.1, the MP-01 slot figure is restated as a slot size taken from
`tools/mech_gen.py`, and RUL-EEG-021 is recorded as a document identifier.

**Also within Rev B and without a further revision letter (2026-09-02):** the EEG-CAR-01 row in
section 2.4 is restated against the re-routed board. `kicad/EEG-CAR-01_RevB_DRC_report.txt` now
records 145 of 145 nets fully connected and **zero DRC violations**, so the twenty-five open
items and the two electrode-clearance vias at 0.328 mm are withdrawn from that row, and the
fabrication data is **released for review under RFQ-EEG-002A, with fabrication release awaiting
that review**. What has not changed: the routing has still not been read by a human layout
engineer, 169 of its connections were relaxed to close, and no board has been fabricated.

**Also within Rev B and without a further revision letter (2026-09-02), after the independent
review of package v2.2:** section 2.3 is re-registered against what `mech/` actually holds. The
two Rev B foam files this register named are withdrawn and deleted; the seven CASE-00 **Rev C**
layer files are shipped, and CASE-00-03 to CASE-00-07 are registered here for the first time.
The register had been carrying two layers against a seven-layer part, and pointing a foam cutter
at two filenames that no longer exist. OA-8 is closed by the Rev C bay, and the honest part of
it survives in section 2.3: the seven files are drawn and **not released for cutting**.

**Also within Rev B and without a further revision letter (2026-09-02), after the design and
firmware changes of that day:** the EEG-CAR-01 row in section 2.4 no longer says that 47 kΩ
is fitted and S-02 is not met -- **ECO-EEG-024 is applied, R1-R16 are 68 kΩ and S-02 is met
at 36.8 µA on the calculation**, with the safety sign-off still owed -- and the FW-EEG-001 and
FIX-01 rows in section 2.5 no longer say the firmware has never been compiled or that the
contact-light phase driver does not exist. **The firmware is built and the driver is written.**
Neither has run on hardware, no unit exists, and T11 has not been run.

**A note on DSN-EEG-002 Rev E, which this register cites throughout.** It has not been
re-issued since package v2.1 and the shipped file is byte-identical, so its **sections 7, 10
and 11** are cited here for geometry, materials and fitting only, and are **superseded on three
points**: section 10's `HM-07` / `HM-08` part numbering is superseded by sections 3.1 and
3.2 of this register (HM-08 is the battery hatch, HM-10 the keyed cell carrier, HM-07A/B/C the
boom arm), and section 7's "a charged spare travels in the case" is superseded by
REG-EEG-012 Rev B section 3.1 and RISK-EEG-011 Rev B section 6.1, which record zero spare cells
in circulation. Its **section 11** travel-case figure, FIG-19 in the map of section 3.3 below,
draws the two-layer foam and is superseded by the CASE-00 Rev C schedule of PKG-EEG-015
section 2.2 and by section 2.3 above. ECO-EEG-016 section 1.1 records the file as "released,
not reissued in this round"; its re-issue is an open document action, not a decision still to
be taken.

**Also within Rev B and without a further revision letter (2026-09-02), after the completeness
audit of package v2.3: twelve printed parts are re-registered from "to be created" to
"exists".** HM-02B, HM-02C, HM-03A, HM-05B, HM-10, HM-11A, HM-11B, HM-11C, POD-P1-04,
WH-ADP-02, WH-ADP-03 and WH-ADP-04 all have STL, STEP, a MECH-EEG-020 sheet and a
`mech/MANIFEST.json` entry, and all three WH-KEY-01 forms do too; the register was telling a
shop that parts sitting in `mech/stl/` did not exist. Their model figures are read from the
released meshes, the MECH-EEG-020 sheet numbers throughout §2 are corrected against
`mech/drawings/MECH-EEG-020_sheet_index.csv` -- the set is now 25 sheets, not 10 -- and
AVL-EEG-017 K24 names them so a print bureau can quote them. **WH-BUS-01's entry is corrected
on both counts WH-EEG-008 open item 15 raised**: it is a two-layer board, and its Gerber,
drill, netlist and README set exists in `kicad/wh-bus-01/`. POD-P1-01's volume is restated at
144.42 cm³ from the released mesh. Two new identifiers, **HM-04A** and **HM-05C**, are
registered for the halves of the HM-04 electrical termination that WH-EEG-008 §3.1.1 proposes,
and both are marked PROPOSED rather than allocated to a released part -- OA-14, OA-15 and
OA-16. **The seven printed fixture solids released in `fixtures/` are registered in §2.4 for the
first time**, named by their TST-EEG-004 §6.1 sub-assembly letter and their filename, because
this register allocates none of that letter set itself -- OA-17.

**Also within Rev B and without a further revision letter (2026-09-02), after the design changes
of 2 September 2026.** Two released helmet parts were re-cut, a bought-in class of connector
arrives in the register for the first time, and one harness number is reserved. **HM-04 and HM-05B now assemble.** The pair as
released did not: the HM-05B lug stood at an outer radius of 5.40 mm against a 5.30 mm slot --
0.10 mm of radial interference and zero tangential clearance -- and `hm04()` cut two straight
axial slots with no circumferential run behind them, so the carrier could not enter and, if it
had, could not turn. The lug is corrected to 5.20 mm, which is what `hm05b()`'s own docstring has
always said, and raised to z 1.20--3.30; the entry slots are 1.70 mm wide at an outer radius of
5.55 mm and 3.60 mm deep; and HM-04 gains a **100° circumferential run at z 1.10--3.80 with
1.10 mm of retaining lip below it**. `tools/simulate_production.py` measures the two solids at four
rotations and three axial positions on every run and reports 0.000 mm³ through the quarter turn,
0.000 mm³ through the carrier's 0.40 mm of spring travel and 1.557 mm³ of lip engagement when the
seated carrier is pulled down. **HM-04's contact-light window is now two pockets** with 1.60 mm of
printed PA12 between them, an outboard LED seat and an inboard conductor run, where it was one box
straight through the body -- the arrangement RISK-EEG-011 SF-9 describes. **HM-04's spring seat is
6.60 mm deep**, not 4.50, which takes the free height above the HM-05B spigot from 1.40 mm to
3.50 mm. The model figures of both parts move with all of this and are restated in §2.1 from the
released meshes; **both parts are owed a revision letter** under rule 5 of §1.3, and the deepened
seat is in `tools/mech_gen.py` and not yet in a released mesh -- OA-18. Separately, **WH-10 is
reserved** for the Fpz bias lead, and the 1.5 mm touch-proof DIN 42802-1 sockets for the two ear
references and for the bias lead are registered in §2.4 as bought-in parts that take no identifier
under rule 4 -- OA-16, extended, and OA-19. Nothing here has been printed, and every one of these
changes is a change to a source file and a mesh, not to a part.

**Nothing in this package has been manufactured or measured, and no safety engineer has
reviewed this design.** Every dimension, volume and mass in this register is calculated
from a released model file. No part has been printed, no board has been fabricated, and the
first thing Phase 1 does is find out which of these figures are wrong.

## Why this document exists

Package v1 used the code `HM-xx` for two different things at once: as figure labels in
DSN-EEG-002 Rev E and as part numbers in the same document's section 10. Only `HM-01`
happened to mean the same thing in both. The consequence was not cosmetic. `HM-07` named
the boom microphone arm in DSN-EEG-002 section 10 and the battery hatch in DSN-EEG-003
section 4, in `mech/HM-07_battery_hatch.stl`, in `mech/MANIFEST.json`, in kit BOM item 17
and in the RFQ Rev C scope line -- so a contract manufacturer printing "HM-07" produced a
gooseneck arm or a quarter-turn hatch depending on which document was open, and whichever
one was printed, the other part was silently dropped from the kit. DSN-EEG-002 section 10
also requires part IDs to be engraved into the model, so the wrong identifier would have
been moulded into the part. This register fixes one identifier for each part in the
package, states which file defines it and which document specifies it, and is cited by
every other document in package_v2.3 (DSN-EEG-003 Rev C Annex A lists it sixth in the
precedence order). It closes contradictions XD-01, XD-02 and XD-03 and gaps
`mech-hm07-part-number-conflict` and `mech-missing-part-files`.

Rev B exists because the geometry moved underneath the register. Two findings came out of
actually laying the carrier out instead of asserting that it would lay out, and both
propagate into every printed part this document names.

**The carrier grew from 130 x 124 mm to 150.0 x 130.0 mm.** Thirty connectors, 211 parts
and 156 nets would not close at the smaller size. At Phase 1 and Phase 2 quantities the
extra 33.8 cm2 of bare board costs a few euro per unit against a real risk of an unroutable
design, so the board grew.

**The carrier went from two layers to four.** Package v1's architecture argument was that a
two-layer carrier is cheap and easy to route. Doing the layout showed that it is not: on
two layers the bottom side has to be both the reference plane and the second routing
surface, and it cannot be both. Four layers -- L1 signal, L2 reference plane, L3 reference
plane, L4 signal -- give two full routing surfaces and a continuous reference under every
analogue trace, which is what DSN-EEG-002 section 13's "layout rules that are requirements,
not preferences" require, and what the zoning, star-point and isolation rules of
DSN-EEG-003 section 3.3 require, and which a swiss-cheesed two-layer pour cannot deliver.
The two citations are not interchangeable: DSN-EEG-002 section 13 carries the layout rules
that are requirements, and DSN-EEG-003 has sections 1 to 11 plus annexes and no section 13,
so a reference to "DSN-EEG-003 section 13" is stale and is corrected to one of these two.
At 2 units the four-layer board is about EUR 35 more in total; at 50 units it is about
EUR 3 per board.

The enclosure and the module plate grew with the board, and MP-01, POD-P1-01 and POD-P1-02
are therefore at new revisions in this issue. The change is recorded against EEG-CAR-01 in
section 2.4 and in the migration table of section 3.2.

---

## 1. Naming rules

### 1.1 Four namespaces, never mixed

| Namespace | Form | Owner | Example |
|---|---|---|---|
| Part identifiers | `<PREFIX>-nn`, optional letter suffix for a member of an assembly | this document | `HM-08`, `HM-02A` |
| Document identifiers | `<TYPE>-EEG-nnn Rev X` | ECO-EEG-016 | `DSN-EEG-002 Rev E` |
| Requirement identifiers | `E-nn`, `F-nn`, `A-nn`, `M-nn`, `S-nn`, `O-nn` | RFQ-EEG-001 Rev E | `M-05`, `S-09` |
| Reference designators | `R`, `C`, `D`, `J`, `L`, `F`, `U`, `SW`, `TP`, `FID`, `MH` + number | `tools/design.py` | `J14`, `R90`, `TP13`, `FID2`, `MH1` |
| Figure labels | `FIG-nn` | the document that carries the figure | `FIG-18` |

`TP` and `FID` are in the designator list because Rev B of the carrier has eighteen test
points (TP1 to TP18, RFQ E-28) and three global fiducials (FID1 to FID3, ECO-EEG-020) that
Rev A of this register did not list. They are reference designators owned by `design.py`,
not part identifiers, and no fiducial or test point is ever given an `HM`, `POD` or `MP`
number.

A figure label must never begin with a part prefix. This is the rule that XD-02 exists to
create: in package v1 the caption "HM-07 -- the frame unmounted" and the part "HM-07 boom
microphone arm" sat eleven lines apart in the same section. Figures are numbered `FIG-01`
upward in document order within each document, and are cited from outside as
`DSN-EEG-002 FIG-18`. Section 3.3 gives the full v1-to-v2 figure map for DSN-EEG-002.

**The document namespace is ECO-EEG-016's, and it currently has the same fault this
register was written to fix for parts.** The package cites as governing or required about
nineteen document numbers that are not on the ECO-EEG-016 section 1 register, and six of
them collide numerically with registered documents -- REL-EEG-009 against JIG-EEG-009,
PROV-EEG-007 against ASM-EEG-007, KEY-EEG-008 against WH-EEG-008, SD-EEG-013 against
SVC-EEG-013, OTA-EEG-014 against IFU-EEG-014 and CAL-EEG-012 against REG-EEG-012. That is
not this register's namespace to repair and it is recorded here only as OA-11, against
ECO-EEG-016. Two of the numbers that were unregistered when Rev A was written are now on
that register: **RUL-EEG-021**, the rulings register, and **SIM-EEG-018**, the production
simulation report, both at Rev A in `docs/`.

**RUL-EEG-021 is a document identifier and never a part identifier.** It is a controlled
document on the ECO-EEG-016 section 1 register, it takes the `<TYPE>-EEG-nnn Rev X` form of
row 2 of the table above, and it is cited as **RUL-EEG-021 with a section letter** -- for
example RUL-EEG-021 section A for the geometry rulings and section B for the instrument
rulings. No `RUL` prefix exists in the part namespace of section 1.2, no `RUL` number is
ever allocated to a printed, bought-in or fabricated item, and nothing in section 2 of this
register carries one. SIM-EEG-018 is read the same way: a document number, and a record
rather than a specification.

### 1.2 Prefixes and number ranges

| Prefix | Covers | Range | Allocated | Reserved for |
|---|---|---|---|---|
| `HM` | Helmet: frame, pads, fixation, electrode assemblies, hatch, key, cell carrier, channel covers | HM-01 to HM-19 | HM-01 to HM-11 | HM-12 to HM-19, Phase 2 |
| `POD` | Electronics enclosure and its fittings. Phase variant in the identifier: `-P1` bench, `-H2` in-helmet | POD-P1-01 to -19, POD-H2-01 to -19 | POD-P1-01 to -05 | Phase 2 occipital shell |
| `CASE` | Travel case, foam, packing printed matter | CASE-00 (foam family, historic), CASE-01 to CASE-09 | CASE-00-01 to -07, CASE-01 to -03 | CASE-04 to -09 |
| `MP` | Module plate and its hardware | MP-01 to MP-09 | MP-01 | plate variants |
| `WH` | Cable and harness assemblies, and their named sub-assemblies | WH-01 to WH-19, plus `WH-KEY-nn`, `WH-BUS-nn`, `WH-ADP-nn` | WH-01 to WH-07, WH-09; **WH-10 reserved and not issued** (Fpz bias lead -- §2.4, OA-19); WH-KEY-01, WH-BUS-01, WH-ADP-01/-01B/-02/-03/-04 | Phase 2 umbilicals |
| `EEG-CAR` | Carrier printed circuit board | EEG-CAR-01 to -09 | EEG-CAR-01 | EEG-CAR-02/-03, the Phase 2 split boards |
| `FIX` | Production test fixtures, and their own printed parts as `FIX-nn-mm` | FIX-01 to FIX-19 | FIX-01 to FIX-04 | further stations |
| `FIT` | Fit-test and process coupons | FIT-01 to FIT-09 | FIT-01 | collar and lug coupon |
| `FW` | Firmware images and host tools | `FW-EEG-nnn` | FW-EEG-001 | host tools |

`FIT` is a ninth prefix, not in the original scheme. It is here because
`mech/stl/FIT-01_fit_test_coupon.stl` was released before this register and
`tools/mech_gen.py` governs the filename; inventing a tenth name for a file that already
exists would recreate the fault this document is closing.

**The three `WH` sub-forms are the one exception to the `<PREFIX>-nn` rule**, and they are
here for the same reason `FIT` is: WH-EEG-008 Rev B already uses `WH-KEY-01`, `WH-BUS-01`
and `WH-ADP-01` to `WH-ADP-04` in its wire lists, its build order and its test record, and
renaming them into the plain `WH-nn` run would put a keying shroud and a cable in the same
number series and invite exactly the confusion described above. The sub-form is read as
"WH namespace, `KEY` / `BUS` / `ADP` family, member nn". No `WH-nn` cable number is ever
reused for a sub-assembly and no sub-assembly number is ever shortened to `WH-nn`.

**WH-08 is withdrawn and its number is not reused.** It named a captive 2 m host USB-C lead
leaving the pod through a Lapp SKINTOP gland. The host connection is a socket, not a captive
cable, so WH-08 and the gland are deleted from the Phase 1 build; see section 2.4 and
WH-EEG-008 Rev B section 1.

### 1.3 Rules of use

1. **One identifier, one part.** If two things can be ordered, printed, inspected or
   scrapped separately, they are two parts and they get two identifiers.
2. **The filename begins with the identifier.** `HM-08_battery_hatch.stl` is HM-08. The
   two exceptions are the POD-P1 and CASE-00 families, whose filenames carry the family
   token and whose members are distinguished by the descriptive tail; the register table
   in section 2 gives the mapping explicitly for those four files.
3. **A letter suffix means a member of a named assembly**, not a revision. `HM-02A` is the
   brow pad; the revision of HM-02A is carried in its own column and is never written into
   the identifier.
4. **Bought-in catalogue items get no identifier** unless the programme modifies them or a
   printed interface part exists for them. An unmodified Nanuk case, an Ambu snap pad or a
   Panasonic cell is identified by its supplier part number and its AVL-EEG-017 line. The
   ratchet mechanism, the gooseneck and the sintered cup *are* modified or mated to printed
   parts, so they carry identifiers.
5. **A revision letter belongs to the part, not to the package.** Any change to a released
   file raises the letter. HM-04 and HM-08 are at Rev B because their models were rebuilt
   parametrically; MP-01, POD-P1-01 and POD-P1-02 are at Rev B because the carrier grew and
   they were resized to match. Neither is because the package revised.
6. **Nothing in this register has been manufactured.** Every dimension and volume quoted is
   calculated from the released mesh, not measured on a part.

---

## 2. The register

Bounding boxes and volumes are calculated from the released STL in
`package_v2.4/mech/stl/` (bounding box from the vertex extremes, volume by the divergence
theorem over the closed mesh). They are model figures. No part has been printed, so no
figure here has been verified against hardware.

### 2.1 Helmet, prefix HM

| ID | Name | Rev | Material and process | Qty/kit | Defining file | Status | Specified in |
|---|---|---|---|---|---|---|---|
| HM-01 | Frame monocoque: halo, sagittal arch, coronal arch, rail stubs, occipital shell, internal channels | A | PA12, MJF, bead-blast, dyed graphite. 191.1 × 229.6 × 158 mm, 133.6 cm³, about 240 g | 1 | `package/mech/HM-01_frame_monocoque.stl` (v1 release, carried over unchanged) | Exists as STL only. No STEP, no parametric source. See OA-1 | DSN-EEG-002 Rev E §10; RFQ M-01 |
| HM-02A | TPU comfort pad, brow | A | TPU 85A, printed or cast. 85.00 × 22.00 × 8.00 mm, 14.44 cm³ | 1 + 1 spare | `mech/stl/HM-02_brow_pad.stl`, `mech/step/HM-02_brow_pad.step` | Exists. **MECH-EEG-020 sheet 6** | MECH-EEG-020; RFQ S-05; AVL-EEG-017 K24 |
| HM-02B | TPU comfort pad, occiput | A | TPU 85A, printed or cast. **50.00 × 22.00 × 8.00 mm, 8.38 cm³** | 2 + 2 spare | `mech/stl/HM-02B_occiput_pad.stl` + `.step` | **Exists.** MECH-EEG-020 sheet 4 | DSN-EEG-002 Rev E §10; AVL-EEG-017 K24 |
| HM-02C | TPU comfort pad, crown | A | TPU 85A, printed or cast. **72.00 × 26.00 × 8.00 mm, 13.13 cm³** | 1 + 1 spare | `mech/stl/HM-02C_crown_pad.stl` + `.step` | **Exists.** MECH-EEG-020 sheet 5 | DSN-EEG-002 Rev E §10; AVL-EEG-017 K24 |
| HM-03A | Occipital yoke | A | PA12, MJF. **114.04 × 34.13 × 20.00 mm, 13.40 cm³** | 1 | `mech/stl/HM-03A_occipital_yoke.stl` + `.step` | **Exists.** MECH-EEG-020 sheet 7. Now also carries what RFQ A-03 asks for -- see the note below. **The interface to the bought-in HM-03C ratchet is still not defined**, so the yoke exists and the joint to the ratchet does not | ASM-EEG-007 §4.3; RFQ A-03; AVL-EEG-017 K24 |
| HM-03B | Ratchet dial housing | -- | PA12, MJF, POM pawl | 1 | none | **To be created** | ASM-EEG-007 §4.3 |
| HM-03C | Ratchet mechanism | -- | Bought-in hard-hat ratchet, 2 mm per click, 52--62 cm band travel | 1 | none | Supplier part not yet named | AVL-EEG-017; kit BOM item 21 |
| HM-04 | Electrode assembly body: cup bore, spring seat, bayonet entry slots and circumferential run, gel port, two contact-light pockets | B, **C owed** | PA12, MJF. **12.40 × 12.40 × 18.00 mm, 1.86 cm³** from the mesh released on 2026-09-02; the 1.90 cm³ this row carried until then is superseded | **8 fitted + 2 spare = 10** | `mech/stl/HM-04_electrode_assembly_body.stl` + `.step` | **Exists, and re-cut on 2026-09-02.** MECH-EEG-020 sheet 8. **The bayonet turns.** The entry slots are 1.70 mm wide at an outer radius of 5.55 mm, cut 3.60 mm deep, and behind them `hm04()` cuts a **100° circumferential run at z 1.10--3.80** with **1.10 mm of solid material below it as the retaining lip**; the run's ceiling clears the carrier's whole 0.40 mm of axial float, because that float is the travel the cup makes when it is pressed against the scalp and not slack. Measured rather than asserted: `tools/simulate_production.py` intersects the two solids at four rotations and three axial positions on every run and records **0.000 mm³ through the quarter turn, 0.000 mm³ through the 0.40 mm of spring travel and 1.557 mm³ of lip engagement** when the seated carrier is pulled down (SIM-EEG-018 Rev A, station 01). **The contact-light window is two pockets**, 3.20 mm wide, with **1.60 mm of printed PA12 between them** -- outboard the LED seat, inboard the electrode conductor's run -- where it was one box straight through the body; RISK-EEG-011 restates SF-9 and H-05 against it as materially reduced and explicitly not eliminated. **The spring seat is 6.60 mm deep, not 4.50**, taking its roof from z 13.50 to z 15.60 and the free height above the HM-05B spigot top from 1.40 mm to **3.50 mm**; the seat is 0.10 mm larger than the spigot on the radius, so no coil fits around the spigot and the spring bears on its top face -- which is why AVL-EEG-017 K12's "3--6 N stainless 302 compression spring" could not have been bought as the geometry stood (ASM-EEG-023 Rev A, D5-K12-SPRING-ENVELOPE). K12 still reads against the outside of the body and is still unspecified -- OA-20. **Two of the four features OA-14 listed are still owed**: an anchorage for HM-04A that holds 15 N, and a dressed conductor exit at the inboard pocket. **Three cautions on the figures above.** The released mesh, its sha256 and its `mech/MANIFEST.json` entry carry the bayonet and the two pockets and **not** the deepened spring seat, which is in `tools/mech_gen.py` and has not been regenerated -- OA-18. Nothing has been printed: a 0.000 mm³ intersection says two solids do not overlap, not that PA12 printed to ±0.15 mm turns by hand, and FIT-01 still gates no bayonet feature -- OA-3. And the re-cut raises this part's revision letter under rule 5 of §1.3, so **Rev C is owed** with sheet 8 and an ECO-EEG-016 entry | DSN-EEG-002 Rev E §4; RFQ A-01; WH-EEG-008 §3.1.1; SIM-EEG-018 Rev A |
| HM-05A | Sintered Ag/AgCl cup | -- | Bought-in sintered cup, modified for the service bayonet | 8 + 2 spare | none | Modification not yet drawn. **The tail is not defined either**: AVL-EEG-017 K1 buys the cup with a 1.5 m lead and WH-EEG-008 §3.1.1 terminates it on a tail of tens of millimetres inside the assembly, so the purchase order cannot state a length until that section is approved | RFQ A-01; kit BOM item 25; AVL-EEG-017 K1 |
| HM-05B | Cup bayonet carrier | A, **B owed** | PA12, MJF. **10.40 × 9.10 × 12.10 mm, 0.52 cm³** from the mesh released on 2026-09-02: a Ø9.10 × 8.60 body in HM-04's Ø9.20 bore, a Ø6.60 × 3.50 spigot in its spring seat, a Ø2.40 axial gel passage, two bayonet lugs and two HM-09 drive notches. The **10.80 mm** across-flats figure this row carried until then is superseded: that dimension is twice the lug's outer radius, and the lug moved from 5.40 to 5.20 mm | 8 + 2 spare | `mech/stl/HM-05B_cup_bayonet_carrier.stl` + `.step` | **Exists, re-cut on 2026-09-02, and the bayonet turns.** MECH-EEG-020 sheet 9. The lug is 1.40 mm wide standing 0.65 mm proud at r 4.55 -- **outer radius 5.20 mm, which is what `hm05b()`'s own docstring has always claimed** -- because the 0.40 mm of union overlap that widens the box is now taken off its centre as well as added to its width. Until it was, the mesh put the lug at 5.40 mm into HM-04's 5.30 mm slot: 0.10 mm of radial interference, zero tangential clearance in a material printed to ±0.15 mm, and no circumferential run to turn into. The lug is also raised to **z 1.20--3.30**, so it comes to rest ON HM-04's 1.10 mm retaining lip instead of inside it. **Superseded on 2026-09-02**: this row read "**the bayonet does not yet turn**, because HM-04 has the entry slots and no circumferential run behind them", and that is no longer true of either part. **Still not settled**: the 7.00 × 3.00 mm cup pocket remains **provisional**, sized by the wall left over rather than by a cup, because HM-05A's modification for the service bayonet has never been drawn. The flank solder-tag pocket stays **superseded by WH-EEG-008 §3.1.1** and withdrawn, and `hm05b()` still cuts it -- **1.60 × 1.60 × 0.80 mm at z 5.60**, not the 1.60 × 1.20 × 0.80 mm this row recorded, a figure corrected here against the source -- so the model carries a feature the register has withdrawn until it is removed (OA-18). The re-cut raises this part's revision letter under rule 5 of §1.3: **Rev B is owed**, with sheet 9 and an ECO-EEG-016 entry | DSN-EEG-002 Rev E §4.1; WH-EEG-008 §3.1.1; AVL-EEG-017 K24; SIM-EEG-018 Rev A |
| HM-04A | Electrode termination contact: the fixed half of the site joint, anchored in the HM-04 body, bearing axially on HM-05C | -- | Bought-in sprung contact, gold over nickel on the bearing face | 8 + 2 spare | none | **PROPOSED, not released.** WH-EEG-008 §3.1.1 specifies it as a proposal and AVL-EEG-017 K25 carries it as OPEN WITH CRITERIA. It gets an identifier under rule 4 of §1.3 because it is a bought part with a printed interface part, and it is registered now so that the harness, the assembly instruction and the purchase order can name the same thing. **The site end of both helmet cables cannot be built until it is approved**. **2026-09-02**: the volume this contact has to live in changed on the same day and in its favour. HM-04's inboard pocket is now a separate cavity with 1.60 mm of PA12 between it and the LED, and the spring seat is 2.10 mm deeper, so the free height above the HM-05B spigot is 3.50 mm rather than 1.40 mm. **Neither the contact nor its anchorage is issued by that**: ASM-EEG-023 Rev A, D1-HM04-CROWN-AND-LEAF holds the joint and issues only the bayonet run, and it puts the safety reviewer's disposition of SF-9 and H-05 against a named HM-04 geometry **first**, because that disposition decides the cavity. The anchorage that holds WH-EEG-008 H6's 15 N is still not drawn -- OA-14 | WH-EEG-008 §3.1.1; AVL-EEG-017 K25 |
| HM-05C | Cup contact crown: the rotating half, an annulus let into the top face of the HM-05B spigot, clear of the Ø2.40 gel passage | -- | Bought-in or fabricated annulus, gold over nickel on the upper face, joined to HM-05A's tail | 8 + 2 spare | none | **PROPOSED, not released.** WH-EEG-008 §3.1.1; AVL-EEG-017 K26. Rotation-invariant by construction, because the carrier turns 90° at every service. It goes into the ultrasonic bath with the cup. **2026-09-02**: the crown's own dimensions are still held, not issued. ASM-EEG-023 Rev A, D1-HM04-CROWN-AND-LEAF issues the crown annulus as a **vendor criterion and not as released geometry**, and the free band it shares with the contact leaf and the K12 spring moved on the same day: HM-04's spring seat roof went from z 13.50 to 15.60, so the height above the spigot top at z 12.10 is 3.50 mm rather than 1.40 mm. That reopens what form of spring is buyable and it does not by itself dimension anything here. AVL-EEG-017 K26 carries the criteria; no value in this row is released until the safety reviewer has disposed of SF-9 and H-05 and the mechanical reviewer has allocated the band once on MECH-EEG-020 sheet 8 | WH-EEG-008 §3.1.1; AVL-EEG-017 K26 |
| HM-06A | Chin cup | -- | PA12, MJF | 1 | none | **To be created.** Now also carries what RFQ A-03 asks for -- see the note below | ASM-EEG-007 §4.3; RFQ A-03 |
| HM-06B | Chin cup liner | -- | TPU 85A, consumable, replaced each turnaround | 1 + 1 spare | none | **To be created** | RFQ S-05; REG-EEG-012 §6 |
| HM-06C | Chin strap set: 20 mm webbing, buckle, anchors | -- | Bought-in | 1 | none | Supplier part not yet named | kit BOM item 23; RFQ A-03 |
| HM-07A | Boom arm temple mount and cheek sleeve | -- | PA12, MJF; keyed so it cannot be fitted rotated | 1 | none | **To be created** | ASM-EEG-007 §4.3; DSN-EEG-002 Rev E §8 |
| HM-07B | Gooseneck, 120 mm | -- | Bought-in | 1 | none | Supplier part not yet named | kit BOM item 22 |
| HM-07C | Boom capsule and windscreen | -- | Bought-in electret capsule and its screen. **The preamplifier is not on the boom**: it is a module on MP-01 at J21, and which preamplifier is not settled | 1 | none | Supplier part not yet named | kit BOM item 30; RFQ E-14; ICD-EEG-006 §2.9 |
| HM-08 | Battery hatch, quarter-turn, three lugs, coin slot, seal groove | B | PA12, MJF. 48.00 × 36.00 × 6.50 mm, 6.87 cm³ | 1 | `mech/stl/HM-08_battery_hatch.stl` + `.step` | Exists. **Renamed from HM-07 in v1** -- section 3 | **MECH-EEG-020 sheet 10**; DSN-EEG-003 Rev C §4 |
| HM-09 | Service key for the cup bayonet | A | PA12, MJF. Ø17.93 × 40.20 mm, 3.88 cm³ | **1 per operator. NOT in the participant kit** | `mech/stl/HM-09_service_key.stl` + `.step` | Exists. **MECH-EEG-020 sheet 11** | SVC-EEG-013 §3; ASM-EEG-007 §7 step 5 |
| HM-10 | Keyed 18650 cell carrier | A | PA12, MJF; cannot be inserted reversed (RFQ S-04). **74.30 × 43.00 × 23.50 mm, 18.26 cm³** | 1 | `mech/stl/HM-10_keyed_cell_carrier.stl` + `.step` | **Exists.** MECH-EEG-020 sheet 12. Split out of v1 HM-08 -- section 3.2 | RFQ S-04; REG-EEG-012 §7; AVL-EEG-017 K24 |
| HM-11A | Channel cover strip, halo | A | PA12, MJF, printed with HM-01. **173.20 × 185.81 × 1.60 mm, 7.46 cm³** | 1 | `mech/stl/HM-11A_channel_cover_halo.stl` + `.step` | **Exists.** MECH-EEG-020 sheet 13 | DSN-EEG-002 Rev E §10; AVL-EEG-017 K24 |
| HM-11B | Channel cover strip, sagittal arch | A | PA12, MJF, printed with HM-01. **11.00 × 180.42 × 44.01 mm, 3.34 cm³** | 1 | `mech/stl/HM-11B_channel_cover_sagittal.stl` + `.step` | **Exists.** MECH-EEG-020 sheet 14 | DSN-EEG-002 Rev E §10; AVL-EEG-017 K24 |
| HM-11C | Channel cover strip, coronal arch | A | PA12, MJF, printed with HM-01. **135.50 × 11.00 × 34.40 mm, 2.52 cm³** | 1 | `mech/stl/HM-11C_channel_cover_coronal.stl` + `.step` | **Exists.** MECH-EEG-020 sheet 15 | DSN-EEG-002 Rev E §10; AVL-EEG-017 K24 |

**There is no `HM` identifier for a headband or cap, and none is needed.** RFQ A-03 asked
for "an adjustable headband or cap with fixed holders at the eight 10--20 positions". That
part is withdrawn as a kit item: the eight electrodes are fixed to the HM-01 frame at
manufacture, so a headband carrying holders at the same eight sites would duplicate them.
A-03 is rewritten to cover what the kit actually needs and does not yet have -- the chin
strap set HM-06A/B/C and the occipital yoke HM-03A, both of which are on the frame and both
of which are still "to be created". The packing list drops the headband line and
SVC-EEG-013 drops its wash schedule.

### 2.2 Enclosure, prefix POD

POD-P1 is the Phase 1 bench enclosure of RFQ M-01. The `-P1` element is the phase variant
and follows the convention WH-EEG-008 already uses for WH-01-P1 and WH-01-H2.

| ID | Name | Rev | Material and process | Qty/kit | Defining file | Status | Specified in |
|---|---|---|---|---|---|---|---|
| POD-P1-01 | Enclosure base: **158.0 × 138.0 × 55.5 mm internal**, 2.5 mm walls, gasket groove 1.6 × 1.2 mm in the rim, four carrier bosses standing 6.0 mm off the internal floor with M3 tapping holes on the carrier pattern (5,5) (145,5) (5,125) (145,125), panel openings per RFQ M-02 | **B** | PA12 MJF; FDM PETG for Phase 1 form studies only. **163.00 × 143.00 × 58.00 mm, 144.42 cm³** | 1 | `mech/stl/POD-P1_prototype_enclosure_base.stl` + `.step` | Exists, **resized in Rev B for the 150 × 130 mm carrier**. MECH-EEG-020 **sheet 18**, regenerated from this mesh -- OA-9 | RFQ M-01, M-02; ASM-EEG-007 §5.1 |
| POD-P1-02 | Enclosure lid: 4.0 mm plate with a 2.0 mm locating spigot 157.6 × 137.6 mm, four Ø3.4 mm corner holes 6 mm in from each edge, label keep-out | **B** | PA12, MJF. **163.00 × 143.00 × 6.00 mm, 136.36 cm³** | 1 | `mech/stl/POD-P1_prototype_enclosure_lid.stl` + `.step` | Exists, **resized in Rev B**. MECH-EEG-020 **sheet 19**, regenerated from this mesh -- OA-9 | RFQ M-01, M-03 |
| POD-P1-03 | Seal cord, **1.5 mm** silicone O-cord, 60 Shore A, for the 1.6 × 1.2 mm rim groove | -- | Bought-in | 1 | none | Supplier part not yet named. The cut length changes with the Rev B rim | ASM-EEG-007 §5.1 |
| POD-P1-04 | Harness P-clip | A | PA12, MJF, screwed to a base boss 40 mm behind the connector. **20.00 × 8.00 × 7.40 mm, 0.45 cm³** | one per clipped cable end, per WH-EEG-008 §6 | `mech/stl/POD-P1-04_harness_p_clip.stl` + `.step` | **Exists.** MECH-EEG-020 sheet 17. Rev B adds a third use: retaining the WH-09 module-end USB-B plug. **`pod_base()` still carries no boss for any of the three**, so the clip exists and has nothing to screw into -- WH-EEG-008 open item 21 | WH-EEG-008 §3.8, §6; AVL-EEG-017 K24 |
| POD-P1-05 | Cable gland for a captive host lead | -- | Bought-in | **0 in Phase 1** | none | **Withdrawn from the Phase 1 build.** The host connection is a socket, not a captive cable, so there is no gland; no thread, bore or IP rating is decided and no gland feature exists in POD-P1-01. Retained as a Phase 2 placeholder for the helmet shell only | WH-EEG-008 Rev B §1; RFQ E-24 |

**The three button openings are 12.4 mm on a 14 mm pitch, in the LID** (corrected 2026-09-02; they were 13.0 mm in the right end wall, where they lined up with nothing and merged with four connector openings), at y = 76, 90 and 104 mm on the
POD-P1 right wall, for the 6 mm tactile switches SW1 to SW3 with 12 mm coloured caps on
extenders (RFQ E-26). That leaves 1.0 mm of wall between adjacent openings, which is thin in
PA12 and is a first-article check at ASM-EEG-007 §5.1, not a settled result.

**The host USB connector is a socket in the panel, not a captive cable.** The USB-C
receptacle is carried on adapter WH-ADP-04, gasketed behind its flange in a POD-P1 aperture,
and reaches the ADuM4160 module's USB-B receptacle through the pigtail WH-09. That is a live
non-conformance against RFQ E-24, which asks for USB-C at the module: see section 2.4,
WH-09.

### 2.3 Case and packing, prefix CASE

| ID | Name | Rev | Material and process | Qty/kit | Defining file | Status | Specified in |
|---|---|---|---|---|---|---|---|
| CASE-00-01 | Foam insert, layer 1 of 7. 516 × 390 mm sheet, all nine bays, the helmet bay at the 181 × 220 mm shelf opening the halo lands on | C | 25 mm closed-cell PE, 28--33 kg/m³, die-cut or laser-cut | 1 | `mech/CASE-00_foam_layer_1.dxf` | Exists, **Rev C**, written by `tools/mech_gen.py` `foam_dxf()`. Not released for cutting -- see the note below | RFQ M-05, M-06; PKG-EEG-015 §2.2; IFU-EEG-014 §1 |
| CASE-00-02 | Foam insert, layer 2 of 7. 516 × 390 mm sheet, all nine bays, the helmet bay at the full 197 × 236 mm | C | 25 mm closed-cell PE, 28--33 kg/m³, die-cut or laser-cut | 1 | `mech/CASE-00_foam_layer_2.dxf` | Exists, **Rev C**, written by `tools/mech_gen.py` `foam_dxf()`. Not released for cutting | RFQ M-05, M-06; PKG-EEG-015 §2.2; IFU-EEG-014 §1 |
| CASE-00-03 | Foam insert, layer 3 of 7. 516 × 390 mm sheet, five bays: HELMET HM-01, HEADPHONES, POD-P1 ENCLOSURE, CONSUMABLES, CABLES + CHARGER | C | 25 mm closed-cell PE, 28--33 kg/m³, die-cut or laser-cut | 1 | `mech/CASE-00_foam_layer_3.dxf` | Exists, **Rev C**, written by `tools/mech_gen.py` `foam_dxf()`. Not released for cutting | RFQ M-05, M-06; PKG-EEG-015 §2.2; IFU-EEG-014 §1 |
| CASE-00-04 | Foam insert, layer 4 of 7. 516 × 390 mm sheet, two bays: HELMET HM-01, HEADPHONES | C | 25 mm closed-cell PE, 28--33 kg/m³, die-cut or laser-cut | 1 | `mech/CASE-00_foam_layer_4.dxf` | Exists, **Rev C**, written by `tools/mech_gen.py` `foam_dxf()`. Not released for cutting | RFQ M-05, M-06; PKG-EEG-015 §2.2; IFU-EEG-014 §1 |
| CASE-00-05 | Foam insert, layer 5 of 7. 516 × 390 mm sheet, one bay: HELMET HM-01 | C | 25 mm closed-cell PE, 28--33 kg/m³, die-cut or laser-cut | 1 | `mech/CASE-00_foam_layer_5.dxf` | Exists, **Rev C**, written by `tools/mech_gen.py` `foam_dxf()`. Not released for cutting. Layers 5, 6 and 7 are the same cut and are supplied as three files so that no sheet can be laid into the stack at the wrong height | RFQ M-05, M-06; PKG-EEG-015 §2.2; IFU-EEG-014 §1 |
| CASE-00-06 | Foam insert, layer 6 of 7. 516 × 390 mm sheet, one bay: HELMET HM-01 | C | 25 mm closed-cell PE, 28--33 kg/m³, die-cut or laser-cut | 1 | `mech/CASE-00_foam_layer_6.dxf` | Exists, **Rev C**, written by `tools/mech_gen.py` `foam_dxf()`. Not released for cutting | RFQ M-05, M-06; PKG-EEG-015 §2.2; IFU-EEG-014 §1 |
| CASE-00-07 | Foam insert, layer 7 of 7. 516 × 390 mm sheet, one bay: HELMET HM-01 (lowest layer, open to the case floor) | C | 25 mm closed-cell PE, 28--33 kg/m³, die-cut or laser-cut | 1 | `mech/CASE-00_foam_layer_7.dxf` | Exists, **Rev C**, written by `tools/mech_gen.py` `foam_dxf()`. Not released for cutting | RFQ M-05, M-06; PKG-EEG-015 §2.2; IFU-EEG-014 §1 |
| CASE-01 | Hard-shell travel case, IP67 class. Internal envelope **per PKG-EEG-015 §3.2**, which is its single home; the 340 × 250 × 210 mm this row used to carry is the withdrawn Rev D figure and RFQ M-05 no longer states it | -- | Bought-in. **Peli 1560** baseline (published internal 518 × 392 × 229 mm), **Nanuk 960** the alternate (552 × 358 × 226 mm). The "Nanuk 915 / Peli 1450 class" of the previous issue is withdrawn -- neither reaches the envelope | 1 | none | **Shell not finally selected.** PKG-EEG-015 §3.2 and AVL-EEG-017 K21 now name the same two shells, so the disagreement this row used to report is closed; what is still open is the decision itself -- K21 reads "OPEN, a decision is required", and PKG-EEG-015 §3.2 carries it as its open item 10 because the Nanuk 960 is 32 mm short on the second axis and would need a Rev D of the CASE-00 cut file. Both sets of dimensions are published-and-unverified until the first shell is measured | RFQ M-05; kit BOM item 34 |
| CASE-02 | Laminated card set: quick-start card and packing photograph | -- | Print, laminated | 1 | none | Artwork owned by PKG-EEG-015 | RFQ A-06, M-06 |
| CASE-03 | Outer shipping carton, double-wall, with return-label pocket | -- | Bought-in | 1 | none | Owned by PKG-EEG-015 | RFQ M-07, S-09 |

**The bay schedule is not repeated here.** Which bays exist, what goes in each of them
and what the case lid pocket carries are specified once, in **PKG-EEG-015 section 2.2**,
against the cut files named above. Rev A of this register listed the pocket names as well,
which made a fourth copy of a list that already disagreed with itself across three documents.
This register records only the sheet size, the layer number and which bays are cut in each
layer, which are properties of the part.

**Seven layers, at Rev C, drawn and not released for cutting.** The two-sheet Rev B pair
`CASE-00_foam_top_layer.dxf` and `CASE-00_foam_bottom_layer.dxf` is **withdrawn and deleted
from `mech/`**, because PKG-EEG-015 section 2.4 shows 50 mm of foam cannot hold a 158 mm
helmet and a superseded cut file left beside a live one is eventually cut. The identifiers
CASE-00-01 and CASE-00-02 are re-used at Rev C for the first two layers of the new stack;
CASE-00-03 to CASE-00-07 are registered here for the first time. All seven files are in
`mech/` and are listed in `mech/MANIFEST.json`. **None of them is released for cutting.**
Their 516.0 × 390.0 mm sheet is the Peli 1560's *published* internal footprint minus 2 mm on
each plan axis; no shell has been bought or measured, and 2 mm is inside the tolerance of a
moulded case, so a shell that measures short does not make the sheet tight, it makes it
scrap. The sheet is re-drawn to the measured footprint before foam is bought -- PKG-EEG-015
section 3.2 and its open items 1 and 2. Six of the nine bays hold parts that are dimensioned
nowhere in package v2 and are confirmed or corrected at the trial pack of PKG-EEG-015
section 2.4.

### 2.4 Module plate, carrier, harness, coupons, fixtures, firmware

| ID | Name | Rev | Material and process | Qty/kit | Defining file | Status | Specified in |
|---|---|---|---|---|---|---|---|
| MP-01 | Module mounting plate: 8 mm solid border, a field of 12 × 3 mm jumper slots on a 16 × 7 mm grid, Ø2.7 mm M2.5 module fixing holes between the slot rows, one 31 × 61 mm opening over the ESP32-S3-DevKitC-1, four Ø3.4 mm M3 holes on the carrier pattern **(5,5) (145,5) (5,125) (145,125)** | **B** | PA12, MJF, 3.0 mm. **146.00 × 126.00 × 3.00 mm, 37.25 cm³** | 1 | `mech/stl/MP-01_module_plate.stl` + `.step` | Exists, **resized in Rev B for the 150 × 130 mm carrier**. MECH-EEG-020 **sheet 16**, regenerated from this mesh -- OA-9. It still has **no relief over J14 or J30**, so with the plate fitted the two helmet cables cannot leave their sockets -- WH-EEG-008 open item 18 | ICD-EEG-006 §4; RFQ M-01 |
| EEG-CAR-01 | Carrier printed circuit board, **150.0 × 130.0 mm, four layers** (L1 signal, L2 reference plane, L3 reference plane, L4 signal), FR-4 Tg ≥ 150, ENIG, **211 designators** | B | Fabricated to the Gerber X2 set generated by `tools/emit_all.py` | 1 | `tools/design.py` and `kicad/gerber/` | Exists, Rev B. ECO-EEG-001 to -014 and ECO-EEG-018 to -027 applied **except ECO-EEG-023, which is OPEN and not implemented — U7 remains on AVDD/AVSS**. **ECO-EEG-024 is applied**: R1-R16 are **68 kΩ**, so **S-02 single-fault patient current is met at 36.8 µA against a 50 µA limit** on the calculation, and E-10 sits on its ±1.0 dB branch. **Corrected 2026-09-02**: this row said ECO-EEG-024's 68 kΩ was a Phase 1 decision, that 47 kΩ was fitted on the prototypes and that S-02 was not met at 53.2 µA. Nothing has been measured and **SR-01 is closed in the design and not signed off**. Routed on four layers with 3 745 track segments and 552 through vias. **All 145 nets are fully connected**, none is unclosed, none is without copper, and each inner plane is one continuous island per net on both In1.Cu and In2.Cu. Every geometric rule passes: the smallest measured clearance is 0.260 mm on F.Cu, 0.275 mm on B.Cu and 0.285 mm on the planes against a 0.20 mm rule; the narrowest conductor is 0.20 mm; the smallest plated hole is 0.30 mm; copper stands 2.00 mm off every non-plated hole; no digital net enters the analogue zone; and there is exactly one AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND bridge. The report also lists no clearance, width, annular-ring, hole-size, edge, non-plated-hole, isolation keep-out or via keep-out violation, so the isolation strip is clear of copper on all four layers **in that report**, which is why it is said here. **`kicad/EEG-CAR-01_RevB_DRC_report.txt` records zero DRC violations**, which meets all three conditions of the ECO-EEG-016 §3 gate, so the fabrication data is **RELEASED FOR REVIEW under RFQ-EEG-002A and is not yet released for fabrication**. Two things stand between it and a fabricator, and both are stated here rather than in an annex: **169 connections were relaxed to close** -- 36 narrower than the 0.25 mm preferred width and 133 at full width with a reduced gap, all at or above the 0.20 mm minimum conductor and gap -- so the board closes at minimum geometry in places; and the **routing has not been read by a human layout engineer**. No board has been fabricated | DSN-EEG-003 Rev C §3 |
| FIT-01 | Fit-test coupon, 60.00 × 24.00 × 10.00 mm, 12.39 cm³, three bores at 9.20, 9.35 and 9.15 mm | A | PA12, printed in the same build as the batch it qualifies | 1 per print build (not a kit item) | `mech/stl/FIT-01_fit_test_coupon.stl` + `.step` | Exists. MECH-EEG-020 sheet 2. **Carries the bayonet fit only** -- see OA-3 | QP-EEG-010 IP-9; DSN-EEG-002 Rev E §10 |
| WH-01 | Helmet electrode cable, 12-way screened, to J14. Variants WH-01-P1 (1500 mm) and WH-01-H2 (180 mm) | B | Custom cable assembly | 1 | WH-EEG-008 §3.1 wire list | Specified, not built. Only the -P1 variant is being built; the -H2 length cannot be fixed until the Phase 2 shell is resized for the 150 × 130 mm carrier. **Its site end cannot be built at all**: the joint at the eight HM-04 assemblies and the two ear references are proposals -- WH-EEG-008 §3.1.1 and §3.1.2, open items 22 and 23. Materials and connectors are now purchasable: AVL-EEG-017 K25--K28, K31--K34 and §1.6.1. **2026-09-02**: the ear-reference end is decided and not yet signed. ASM-EEG-023 Rev A, D2-EAR-REFERENCE-COUPLER rules that conductors 9 and 10 terminate in free-hanging 1.5 mm touch-proof DIN 42802-1 **sockets** -- AVL-EEG-017 K27, bought on the same order as the K2 ear clips -- in place of the bare crimp onto the clip, and it leaves the cut length at 2140 mm. Those sockets take no part identifier: see the note below this table and OA-16. The site end is still blocked, but less of it than before: HM-04's inboard pocket is now a separate cavity for the conductor with 1.60 mm of PA12 between it and the LED, while the termination itself, HM-04A's anchorage and the dressed exit remain proposals in §3.1.1 -- OA-14, and ASM-EEG-023 Rev A, D1-HM04-CROWN-AND-LEAF holds the joint | WH-EEG-008; RFQ E-09; AVL-EEG-017 §4 |
| WH-02 | Helmet contact-light cable, 10-way, to J30. Variants -P1 and -H2 | B | Custom cable assembly | 1 | WH-EEG-008 §3.2 | Specified, not built. Its sixteen site-end LED leads have no seat and no lead passage in HM-04 -- WH-EEG-008 §3.1.1, open item 22. Materials and connectors: AVL-EEG-017 K29, K33, K34 and §1.6.1. **2026-09-02**: HM-04 now has an outboard pocket for the LED, separated from the electrode conductor's pocket by 1.60 mm of printed PA12, which is what RISK-EEG-011 SF-9 asked for and is why H-05's control is no longer contradicted by the electrode body. **The seat itself and the two lead passages are still a WH-EEG-008 §3.1.1 proposal** and are not released geometry, so open item 22 stays open at the site end of this cable | WH-EEG-008; ECO-EEG-014; AVL-EEG-017 §4 |
| WH-03 | Boom microphone pigtail, 4-way screened, to J18 (with sub-assembly WH-03B, the boom lead) | B | Custom cable assembly | 1 | WH-EEG-008 §3.3 | Specified, not built. Materials, connector and tooling now purchasable: AVL-EEG-017 K28, K31--K37 and §1.6.1. **Still no row in the bidders' kit BOM** -- WH-EEG-008 open item 27 | WH-EEG-008; AVL-EEG-017 §4 |
| WH-04 | Headphone panel pigtail, 4-way, to J27 | B | Custom cable assembly | 1 | WH-EEG-008 §3.4 | Specified, not built. Purchasable through AVL-EEG-017 K28, K31--K37 and §1.6.1; **no row in the bidders' kit BOM** -- WH-EEG-008 open item 27 | WH-EEG-008; RFQ A-04; AVL-EEG-017 §4 |
| WH-05 | Room microphone cable, 4-way screened, to J28 | B | Custom cable assembly | 1 | WH-EEG-008 §3.5 | Specified, not built. **No catalogue room-microphone module is known to meet RFQ E-15's hardware mute**, so the module end is specified against a candidate. **Its carrier end is the same connector ICD-EEG-006 §3.3 also counts as JMP-28**; only WH-05 is built, and AVL-EEG-017 §1.6.1 counts the housing once. Materials: AVL-EEG-017 K28, K31--K34 and §1.6.1; **no row in the bidders' kit BOM** -- WH-EEG-008 open item 27 | WH-EEG-008; RFQ E-15; ICD-EEG-006 §3.3 |
| WH-06 | EMG DIN 42802 lead set, three leads | B | Custom or bought-in leads to J15--J17 | 3 | WH-EEG-008 §3.6 | Specified, not built. **The J15--J17 PCB socket part is open**: `design.py` names Stäubli SLB1,5-F as a class, not a confirmed PCB part | RFQ A-02, E-09; AVL-EEG-017 |
| WH-07 | Charge-port pigtail, 2-way, to J24 | B | Custom cable assembly | 1 | WH-EEG-008 §3.7 | Specified, not built. Purchasable through AVL-EEG-017 K30, K36, K38 and K39; **no row in the bidders' kit BOM** -- WH-EEG-008 open item 27 | ECO-EEG-003; RFQ S-01; AVL-EEG-017 §4 |
| WH-08 | *(withdrawn -- captive host USB-C link and gland)* | -- | -- | **0** | none | **Withdrawn. The number is not reused.** The host connection is a socket on WH-ADP-04, not a captive cable; the captive lead through a gland is a Phase 2 candidate for the helmet shell | WH-EEG-008 Rev B §1 |
| WH-09 | Isolator host pigtail: ADuM4160 module USB-B plug to the panel USB-C receptacle on WH-ADP-04, 150 mm, shielded, braid bonded at both ends of this cable and to nothing else | A | Bought-in shielded USB 2.0 assembly, re-terminated | 1 | WH-EEG-008 §3.8 | Specified, not built. **This is a live non-conformance against RFQ E-24**, which asks for USB-C at the module: the named isolator candidate presents USB-B, so E-24 is met at the panel and not at the module. WH-09 is deleted and E-24 met properly if an isolator module with a USB-C host receptacle is qualified. Its base assembly, panel receptacle and CC pull-downs are now purchasable: AVL-EEG-017 K38, K39 and K40; **no row in the bidders' kit BOM** -- WH-EEG-008 open item 27 | WH-EEG-008 §3.8; RFQ E-24, S-03; AVL-EEG-017 §4 |
| WH-10 | **Fpz bias lead**: about 150 mm, a 1.5 mm touch-proof DIN 42802-1 plug to a snap stud, turquoise, mating the free-hanging bias socket at the HM-01 halo-front channel mouth and carrying BIAS_EL to a disposable pre-gelled Ag/AgCl snap pad off the existing K4 pack | -- | Bought-in lead of the K3 class | 1 | WH-EEG-008 §3.1.3, which specifies it at this issue as the ninth controlled assembly; ASM-EEG-023 Rev A, D3-BIAS-FPZ-TERMINATION | **RESERVED, not issued.** The number is taken so that the harness document, the assembly instruction and a purchase order can name the same thing, which is why HM-04A and HM-05C are registered too; it is not a released part and nothing may be ordered against it. What it replaces: conductor 11 landed on an "Fpz bias pad, solder tag" with no part number, no drawing and no feature on any model, and that pad is deleted as a helmet feature. **Three things are owed before this number may be issued.** The safety reviewer signs that a K27-class touch-proof socket is the right patient-side form for the driven output and states the residual cross-mate, now that the kit has six sockets and six plugs of the same 1.5 mm family. The mechanical reviewer answers open items 22 and 26: the halo-front channel mouth, the dressed exit and the strain relief are new features on a carried-over HM-01 STL that no source file generates -- OA-1 -- and the coupler's retention figure depends on whether an anchorage is drawn at all. And ECO-EEG-016 carries the change. **Two numbers this register will not carry forward.** The 1980 mm cut length of WH-01 conductor 11 is withdrawn: a free-hanging coupler needs a free tail and 1980 mm has none, so the wire list carries 1940 mm plus a stated free tail F, and F is set at the first fitting trial and not invented. The pull test is not WH-EEG-008 H6's 15 N, which acts on a body anchorage this part does not have; either an HM-01 anchorage that takes 15 N is drawn, or retention is set at or below H5's 13 N minimum for 28 AWG. **Its AVL line is not allocated here, and it is contested**: WH-EEG-008 §3.1.3 names **K47** for this lead, while MECH-D5 of ASM-EEG-023 Rev A issues K47 to K52 for the heat-set inserts, screws, gland and O-cord, having verified K46 as the highest line issued. AVL-EEG-017's owner settles it -- OA-19 | WH-EEG-008; ASM-EEG-023 Rev A; AVL-EEG-017 K3, K4, K27 |
| FIX-01 | Front-end injection, lead-off and contact-light fixture. Sub-assemblies **FIX-01/A to FIX-01/G** | A | Fixture, printed shrouds and a wired interface board | not a kit item | JIG-EEG-009 §1 | Designed, not built. FIX-01/E, the TCS34725-class colorimeter head for T11, **is now in the JIG-EEG-009 Rev B fixture bill of materials** as U21, an ams TCS34725FN breakout (JIG §1.7, §1.8); the head is ready, and **corrected 2026-09-02**, so is the bicolour phase firmware it reads -- this row said the firmware was not written and T11 could not pass. T11 now waits only on a unit: no light has ever been lit, and this build enables `LOFF_SENSP` only, so a lost site shows amber where the specification says red | TST-EEG-004 Rev C §6.1: T7, T8, T9, T10, T11, T22, T23 |
| FIX-02 | Audio loopback, onset and acoustic-output fixture. Sub-assemblies **FIX-02/A to FIX-02/D** | A | Fixture with printed couplers and an artificial-ear coupler | not a kit item | JIG-EEG-009 §2 | Designed, not built. **FIX-02/C, the IEC 60318-1 artificial ear and its class 1 sound level meter mount for T28, is still not in JIG-EEG-009 Rev B**: JIG §7 records it as an open item and prices neither item, while TST-EEG-004 Rev C §5 and §6.1 place both inside FIX-02. That gap is carried here as OA-13 | TST-EEG-004 Rev C §6.1: T12, T13, T17, T28 |
| FIX-03 | Flashing and provisioning fixture. Sub-assemblies **FIX-03/A and FIX-03/B** | A | Fixture | not a kit item | JIG-EEG-009 §3 | Designed, not built. Boot-mode entry is through the DevKitC-1's own UART USB-C port on FIX-03/A; **FIX-03/B on J26 cannot enter download mode** because GPIO0 is LED_SR_LATCH (ECO-EEG-009) | TST-EEG-004 Rev C §6.1: T5, T6, T16, T25 |
| FIX-04 | Battery, charge, insulation, leakage and harness fixture. Sub-assemblies **FIX-04/A to FIX-04/D** | A | Fixture | not a kit item | JIG-EEG-009 §4 | Designed, not built. The per-unit isolation test is a **500 V DC insulation-resistance measurement** and JIG-EEG-009 Rev B's per-unit 2500 V AC hipot station is deleted. **FIX-04/C is a fixture and not a loose bench instrument**: the 100 kOhm 0.1 % measuring resistor and its earth lead are screened, serialised and calibrated with the rest of the set, because T23 is the only routine per-unit safety measurement there is | TST-EEG-004 Rev C §6.1: T00, T3, T4, T20, T21, T23, and the harness heads FIX-04/D for WH-EEG-008 §9 steps H1 to H10 |
| FW-EEG-001 | Device firmware image | C | ESP-IDF build for ESP32-S3-DevKitC-1-N16R8 | 1 image per unit | `firmware/`, and `firmware/release/` for the built images | **Built 2026-09-02, never run on hardware.** Corrected on that date: this row read "never compiled, never run on hardware … the bicolour contact-light phase scheme is specified and not coded, so TST T11 cannot pass". `firmware/release/` now holds `bootloader.bin`, `partition-table.bin`, `ota_data_initial.bin` and `eeg_field_kit.bin` built with **ESP-IDF v5.2.5** for esp32s3, with each SHA-256 in `manifest.json`; the linked image is 405,245 bytes. It has booted once under **QEMU**, which emulates none of this kit's peripherals, and never on silicon. The **contact-light phase driver is written** and T11 is no longer blocked by missing code, only by the absence of a unit. **Five driver stubs remain** (ES8388, SDMMC, ATECC608B, MAX17048, the envelope onset detector), and no image has been released against a serial | DSN-EEG-003 Rev C §5; RFQ F-01 to F-18 |

**MP-01's "12 × 3 mm" is a slot size, not a slot count.** `tools/mech_gen.py` governs and
cuts each jumper slot with `slot2D(12.0, 3.0, 0)` -- 12 mm long by 3 mm wide -- on a grid of
16 mm in x by 7 mm in y, and its own docstring calls the field "a field of 12 x 3 mm jumper
slots". How many slots the plate ends up with is a result of the `clear()` test in
`mp01()`, which drops any slot that falls in the 8 mm border, inside the DevKit opening and
its margin, or within 8 mm of a mounting hole. It is not twelve, it is not a fixed number,
and no document should quote one. Any reading of "twelve 3 mm jumper slots" is a
misreading of the slot size and is corrected against this paragraph and against
`mech_gen.py`.

**The three 1.5 mm touch-proof sockets on the helmet cables take no part identifier.** WH-01's
two ear-reference couplers, and the bias socket that WH-10 mates at the HM-01 halo front, are
bought-in catalogue connectors to **DIN 42802-1** -- AVL-EEG-017 **K27**, which carries all three
units against one set of criteria. Under rule 4 of §1.3 a bought-in catalogue item is identified
by its supplier part number and its AVL line unless the programme modifies it or a printed
interface part exists for it, and nothing printed mates these: they hang on the cable. That is
OA-16's ruling for the two ear couplers, made when they were registered as deliberately
unidentified, and it is extended here to the bias socket for the same reason and recorded so that
the absence reads as a decision rather than an omission. **It is conditional in one direction.**
If HM-01 gains a dedicated seat, anchorage or strain relief for the bias socket at the halo-front
channel mouth -- which is what open items 22 and 26 are about, and what the coupler's retention
figure depends on -- then a printed interface part exists for it, the second limb of rule 4
catches it, and the register owner allocates an identifier in that same change. No such feature
exists today: the HM-01 mesh is carried over from v1 and no source file generates it (OA-1).
Neither socket is released either; both wait on the safety reviewer, as WH-10 and OA-19 record.

Named harness sub-assemblies. They carry conductors or fix connectors and would otherwise
fall between documents; WH-EEG-008 Rev B is their specification and this register only fixes
their identifiers.

| ID | What it is | Rev | Defining file | Status |
|---|---|---|---|---|
| WH-03B | Boom lead: capsule to a **4-pole 3.5 mm plug with solder buckets and a screwed or crimped barrel**, 1700 mm. Two 7/0.1 mm PTFE conductors, overall foil and 30 AWG drain, TPU jacket OD ≤ 2.2 mm | B | WH-EEG-008 §3.3 and **§4**, which gains a WH-03B column at this issue | Specified, not built. Rev B registered it with **no cable specification at all** -- no gauge, insulation, screen, jacket, OD, bend radius or rating -- and no purchasing line; §4 and AVL-EEG-017 K41 now carry both. The word "moulded" in the earlier text is withdrawn: an over-moulded plug cannot be built in a harness shop, pull-tested to 30 N or repaired at service |
| WH-BUS-01 | Contact-light bus board: 14.0 × 10.0 × **0.80 mm, two-layer** FR-4, ten 1.60 mm pads on **0.80 mm plated holes**, no components. Sits at frame node N1 and splits LED_V into eight tails without a crimp splice | A | WH-EEG-008 §1, §3.2.1; fabrication data `kicad/wh-bus-01/`, written by `tools/wh_bus.py` | **Corrected at this issue.** The board is **two layers, not one** -- the pads are plated through holes and plating needs two layers, and a 28 AWG conductor on a surface-only pad is held by the pad's peel strength alone. The **Gerber X2, Excellon, IPC-D-356A and README set now exists** in `kicad/wh-bus-01/`, so "no Gerber set has been generated" is withdrawn. Purchasable: AVL-EEG-017 K42, panel 20 up. Nothing has been fabricated. This closes WH-EEG-008 open item 15 |
| WH-KEY-01 | Printed keying shroud, part of the MP-01 print set. Surrounds a carrier socket and accepts the housing's polarising rib in one orientation only. Three forms: **J14 8.30 × 33.68 × 12.50 mm, 1.57 cm³; J30 8.30 × 28.60 × 12.50 mm, 1.36 cm³; J22 8.30 × 10.82 × 12.50 mm, 0.57 cm³** | A | `mech/stl/WH-KEY-01_shroud_J14.stl`, `_J30.stl`, `_J22.stl` + `.step`; `tools/mech_gen.py wh_key01()` | **Exists, all three forms.** MECH-EEG-020 sheets 23, 24 and 25. ICD-EEG-006 §6.1 lists the seventeen module sockets that also take one and **those forms are not modelled** -- WH-EEG-008 open item 19. The cavity is cut to a **4.20 mm** Harwin M20 housing body and a **4.00 mm** contact protrusion, and both figures are UNCONFIRMED: measure the housing at IQC before printing (AVL-EEG-017 §1.6.1 criteria C1 to C3) |
| WH-ADP-01 | Boom microphone panel jack adapter: a **bought** 4-conductor 3.5 mm panel jack in a 6.5 mm hole in the right-hand wall at design (122.0, 90.0). **No printed part**: the wall is 2.5 mm and the jack's own thread and nut hold it | -- | WH-EEG-008 §3.9; AVL-EEG-017 K37 | **Specified as a bought-part class.** No identifier-bearing part is made for it; the "POD-P1 underside" of the earlier text is withdrawn, because `mech_gen.py` cuts nothing in the underside |
| WH-ADP-01B | Headphone panel jack adapter: the same bought jack part, at design (128.0, 72.0) | -- | WH-EEG-008 §3.9; AVL-EEG-017 K37 | **Specified as a bought-part class.** One jack part number serves both positions, which is why a 4-pole part is used for a stereo output. Whether the part bought carries the switched insertion-detect contact J27.4 reserves is open |
| WH-ADP-02 | Room-microphone carrier: a printed plate over the 4.0 mm acoustic port, carrying the analogue MEMS capsule and the hardware mute switch on an M2.5 grid. **32.00 × 24.00 × 3.40 mm, 1.96 cm³** | A | `mech/stl/WH-ADP-02_room_microphone_carrier.stl` + `.step`; `tools/mech_gen.py wh_adp02()` | **Exists.** MECH-EEG-020 sheet 20. The plate is drilled to a **grid** rather than to a hole pattern precisely because **the module it carries is not qualified** -- no catalogue part is known to meet RFQ E-15's hardware mute (WH-EEG-008 open item 5) |
| WH-ADP-03 | Charge-only USB-C receptacle plate at the panel, for WH-07. **34.00 × 20.00 × 5.00 mm, 2.18 cm³** | A | `mech/stl/WH-ADP-03_charge_usb_c_plate.stl` + `.step`; `tools/mech_gen.py wh_adp_usb()` | **Exists.** MECH-EEG-020 sheet 21. The rim takes any receptacle flange up to 24.0 × 14.0 × 1.6 mm rather than being cut to one part, because no receptacle has been bought (AVL-EEG-017 K38). Bonded to the wall: `pod_base()` carries no boss -- WH-EEG-008 open item 21 |
| WH-ADP-04 | Host USB-C panel receptacle plate, with two 5.1 kΩ CC pull-downs and a flange gasket, for WH-09. **34.00 × 20.00 × 7.40 mm, 2.65 cm³** | A | `mech/stl/WH-ADP-04_host_usb_c_plate.stl` + `.step`; `tools/mech_gen.py wh_adp_usb()` | **Exists.** MECH-EEG-020 sheet 22. Its rim is 0.8 mm deeper for the flange gasket and a 2.0 mm skirt adds 4.0 mm of surface path, because **every node on this plate is on the host side of the isolation barrier** (WH-EEG-008 §3.8, test H10). Receptacle and pull-downs: AVL-EEG-017 K38 and K39 |

**The keying decision is taken.** At the module end a jumper uses a 2.54 mm shrouded
polarised IDC header where the module has one, and where it does not, pin 1 is marked and
the jumper is labelled. At the carrier end the printed shroud **WH-KEY-01** goes over every
socket that takes a jumper. The ad-hoc names `SHR-14-A`, `SHR-30-A` and `SHR-22-A` in the
older JIG-EEG-009 text are the legacy numbering of the same parts and are superseded by
WH-KEY-01.

**There is one fixture sub-assembly namespace and TST-EEG-004 Rev C section 6.1 owns it.**
Sub-parts are numbered `FIX-nn/m` with a single letter, JIG-EEG-009 Rev B uses those letters
and no others, and this register cites them rather than inventing them. The coupler names
`CPL-V` and `CPL-R`, the bare harness-head letters `H-A`, `H-B` and `H-C`, the form
`FIX-04/H-D` and the use of the word "Part" for a fixture sub-assembly are all **withdrawn**.
`CPL-V`, the voice coupler, is **FIX-02/A**; `CPL-R`, the room coupler, is **FIX-02/B**. The
identifiers `FXT-EEG-005` and `FIX-EEG-010`, which appear in the v1 audit, are superseded by
FIX-01 and FIX-03 and must not be reused.

The full letter set, for reference only, is FIX-01/A to FIX-01/G, FIX-02/A to FIX-02/D,
FIX-03/A and FIX-03/B, and FIX-04/A to FIX-04/D. What each letter is, what it mates and
which step it serves is TST-EEG-004 Rev C section 6.1's table, and is not restated here.

**The printed fixture parts, registered here for the first time.** Seven solids are released
in `fixtures/stl/` and `fixtures/step/`, generated by `tools/fixture_gen.py` and listed with
their SHA-256 in `fixtures/MANIFEST.json`, which uses this register's OA-2 schema. Figures are
read from those meshes and no fixture part has been printed.

| Sub-assembly | File | Rev | Material and process | Model figures | What it is |
|---|---|---|---|---|---|
| FIX-01/E | `FIX-01E_colorimeter_manifold` | A | PA12, MJF, **dyed black -- the inside must not be reflective** | 184.00 × 30.00 × 19.00 mm, 46.08 cm³ | Light-tight manifold: eight LED sites at 20.0 mm pitch, a reference-card position, and a rebate with nine index notches for the sensor carrier |
| FIX-01/E | `FIX-01E_sensor_carrier` | A | PA12, MJF, dyed black | 30.00 × 27.00 × 9.00 mm, 3.16 cm³ | Sliding carrier with a 6.0 mm sensor window, a pocket for a TCS34725 breakout up to 24 × 20 × 2.0 mm, and the index peg. **The released mesh is not watertight**, so the volume is indicative and the file needs repair before it is printed |
| FIX-02/A | `FIX-02A_voice_coupler_body` | A | PA12, MJF, bead-blast | 24.00 × 24.00 × 17.95 mm, 5.10 cm³ | The 2.0 cm³ boom-capsule coupler: 16.0 mm bore, 13 mm driver recess, reference-microphone port at 90° |
| FIX-02/A | `FIX-02A_sealing_lip` | A | **TPU 85A**, MJF | 24.00 × 23.99 × 4.50 mm, 1.05 cm³ | Compliant sealing lip, 10.0 mm mouth. **The diameter it has to seal on is not a known number** -- JIG-EEG-009 records it |
| FIX-02/B | `FIX-02B_room_coupler_body` | A | PA12, MJF, bead-blast | 28.00 × 28.00 × 18.14 mm, 6.34 cm³ | The 3.5 cm³ room coupler, sealing over the POD-P1 4.0 mm acoustic port: 20.0 mm bore, annular gasket seat |
| FIX-02/B | `FIX-02B_sealing_lip` | A | **TPU 85A**, MJF | 28.00 × 27.99 × 4.50 mm, 0.97 cm³ | Flat gasket ring with a raised bead, sealing on the pod wall |
| FIX-03/A | `FIX-03A_carrier_nest` | A | PA12, MJF, bead-blast | 180.00 × 160.00 × 15.50 mm, 199.55 cm³ | Flashing and provisioning nest for the 150.0 × 130.0 mm carrier on its four M3 holes, edge-supported with a relief pocket |

**Two of those sub-assemblies are two printed parts each, and rule 1 of §1.3 says two things
that are printed and scrapped separately are two parts.** FIX-01/E is a manifold plus a
sliding carrier; FIX-02/A and FIX-02/B are each a body plus a TPU lip in a different material.
Under this register's own rule they want four more identifiers, and **this register does not
allocate them, because the `FIX-nn/m` letter set is TST-EEG-004 Rev C section 6.1's and not
this document's** -- the same reason the `CPL-V` and `H-A` names were withdrawn. Until
TST-EEG-004 allocates the letters, each part is named by its sub-assembly letter **and its
filename**, which is what the table above and `fixtures/MANIFEST.json` both do, and which is
unambiguous even though it is not an identifier. It is OA-17.

**No fixture part is a kit item**, so none of them carries a per-kit quantity. They are printed
once per fixture set and they belong in the fixture cost of JIG-EEG-009 section 6.1, not in
the kit BOM. AVL-EEG-017 K46 is the line a print bureau quotes them against.

### 2.5 Registered as Phase 2 options, with no identifier allocated

Two things are specified in the RFQ, exist as carrier features, and have no part, no
supplier and no drawing. They are listed here so that a bidder can see that they are out of
scope rather than missing, and no identifier is allocated to either until a drawing exists.

| Item | Carrier feature | Why there is no identifier | Consequence in a standard build |
|---|---|---|---|
| EOG panel sockets and their cable | J22, a 1×3 socket carrying the protected spare channels EOGIN1 and EOGIN2 and their AGND_REF screen | The panel sockets, their cable and their drawing are a **Phase 2 option**. WH-EEG-008 Rev B registers no cable that lands on J22, and AVL-EEG-017 §1.4.1 scopes the DIN socket line to J15--J17 only | RFQ E-09's two spare channels are protected and tested at T7c, and **they reach no panel socket**. RFQ M-02's "two optional openings for the EOG channels" are not cut |
| POD-H2 occipital shell and the WH-01-H2 / WH-02-H2 umbilicals | none -- Phase 2 moves the electronics into HM-01 | RFQ M-01 sizes the Phase 2 shell for a carrier that no longer exists at that size. The shell cannot be dimensioned until the 150 × 130 mm carrier is either re-partitioned or the shell is redrawn | Only the -P1 variants are being built. The `POD-H2-nn` range stays reserved and empty |

---

## 3. The HM-07 decision, and the v1 to v2 migration

### 3.1 The decision and the reasoning

**HM-07 is the boom microphone arm. The battery hatch is HM-08. The file
`mech/HM-07_battery_hatch.stl` is renamed `mech/stl/HM-08_battery_hatch.stl`.**

The alternative -- keeping HM-07 for the hatch and giving the boom arm a new number -- was
rejected for four reasons.

1. DSN-EEG-002 Rev E section 10 already used HM-08 for "Pod hatch and keyed cell carrier".
   Calling the hatch HM-08 makes the STL agree with the older and more specific of the two
   documents instead of overruling it, and needs no new number.
2. The boom arm's identity is textual and appears in several documents (DSN-EEG-002 §8 and
   §10, ASM-EEG-007 stage 4, REG-EEG-012 §6 material table, kit BOM item 22). The hatch's
   identity is a filename in one place. Renaming a file costs one rename; renaming the arm
   costs edits in five documents and risks missing one.
3. The hatch is a print deliverable and the boom arm is a hybrid of a printed mount and
   bought-in hardware. Keeping the print set's identifiers stable against the print-file
   naming rule (rule 1.3.2) matters more for the party who has to build the part.
4. Nothing physical has been made under either reading, so the migration cost is entirely
   documentary.

The register also splits the old HM-08 in two, because "Pod hatch and keyed cell carrier,
qty 1 each" was two parts on one line. HM-08 is now the hatch only. The keyed 18650 cell
carrier is **HM-10**. Any document that says "the HM-08 keyed carrier" is at the v1
numbering and must be corrected (OA-4).

**The v1 numbering is still live in three documents at the time of this issue.** REG-EEG-012 Rev B §2.3, §3.1, §3.3, §3.4 and §6.2 write "the HM-07 hatch" and "the HM-08 keyed carrier";
RISK-EEG-011 Rev B §6.1 and hazard H-31 write "the HM-07 quarter-turn hatch"; and
PKG-EEG-015 Rev B §1.1 line 1.11 re-merges the split part as "HM-08 -- quarter-turn battery
hatch and keyed cell carrier". All three are wrong against section 3.1 and are corrected
under OA-4. This is recorded plainly rather than assumed closed, because the whole point of
this register is that a live namespace collision costs a printed part.

### 3.2 Part identifier migration

| v1 identifier | v1 meaning | v2 identifier | v2 meaning | Note |
|---|---|---|---|---|
| HM-01 | Frame monocoque | HM-01 | unchanged | The only v1 code that meant one thing |
| HM-02 | TPU pads, 4 shapes on one line | HM-02A / HM-02B / HM-02C | brow / occiput / crown | Split; only HM-02A has a file |
| HM-03 | Occipital yoke and ratchet dial | HM-03A / HM-03B / HM-03C | yoke / dial housing / bought-in ratchet | Split: the printed and bought-in halves are separately ordered |
| HM-04 | Electrode assembly | HM-04 | unchanged, Rev B | Qty fixed at 10 -- section 3.4 |
| HM-05 | Ag/AgCl cups on service bayonet | HM-05A / HM-05B | bought-in cup / bayonet carrier | Split |
| HM-06 | Chin strap and chin cup with liner | HM-06A / HM-06B / HM-06C | chin cup / liner / webbing set | Split; the liner is a consumable and the other two are not |
| HM-07 (part, DSN-EEG-002 §10) | Boom microphone arm | HM-07A / HM-07B / HM-07C | temple mount / gooseneck / capsule | **Keeps HM-07**, split three ways |
| HM-07 (file, DSN-EEG-003 §4 and the STL set) | Battery hatch | **HM-08** | Battery hatch | **The rename. XD-01.** |
| HM-08 | Pod hatch **and** keyed cell carrier | HM-08 + **HM-10** | hatch / cell carrier | Split; HM-08 now names one part |
| HM-09 | Service key | HM-09 | unchanged | Still explicitly not in the kit |
| (unnamed, "channel cover strips printed with it") | Channel covers | HM-11A/B/C | halo / sagittal / coronal | Named for the first time |
| POD-P1 (base, lid) | Prototype enclosure | POD-P1-01 / POD-P1-02 | base / lid | Filenames unchanged; **both at Rev B**, resized for the 150 × 130 mm carrier |
| CASE-00 | Foam insert, two layers | CASE-00-01 to CASE-00-07 | the seven stacked 25 mm layers of the Rev C insert | v1 had no bottom layer at all; the v2.1 Rev B pair is withdrawn, CASE-00-01 and -02 are re-used at Rev C and CASE-00-03 to -07 are new |
| (none) | -- | MP-01 | Module plate | New in v2; **Rev B**, resized with the carrier |
| (none) | -- | FIT-01 | Fit-test coupon | v1 promised coupons and shipped none |
| WH-08 | Captive host USB-C link, 2 m, through a gland | **(withdrawn)** + **WH-09** | number retired; host pigtail is WH-09 | The host connection is a socket. WH-08 is not reused |
| (unnamed shrouds `SHR-14-A`, `SHR-30-A`, `SHR-22-A`) | Carrier-end keying shrouds | **WH-KEY-01** | one printed keying shroud part | Named for the first time; the JIG names are legacy |
| (none) | -- | WH-BUS-01, WH-ADP-01/-01B/-02/-03/-04 | bus board and five panel adapters | Named for the first time; they carry conductors and had no identifier |
| EEG-CAR-01 Rev A | Carrier board, 130 × 124 mm, two layers | EEG-CAR-01 Rev B | **150.0 × 130.0 mm, four layers**, 211 designators | Same identifier, new revision. ECO-EEG-001 to -014 and ECO-EEG-018 to -027 |

**The board size and layer count have no ECO number yet, and they need one.** ECO-EEG-016
allocates ECO-EEG-018 to the routing scope and ECO-EEG-019 to ECO-EEG-027 to the circuit
changes; nothing in the register covers "the outline grew to 150.0 × 130.0 mm and the
stack-up went from two layers to four", which is the largest single change between Rev A and
Rev B of the board and changes the fabrication drawing, the price and the three printed
parts that bolt to it. Raised as OA-10 against ECO-EEG-016. This register does not allocate
document or ECO numbers and does not invent one here.

### 3.3 Figure label migration, DSN-EEG-002 Rev D to Rev E

Every figure in DSN-EEG-002 is renumbered. `HM-xx` no longer appears in any caption.

| Rev D label | Section | Subject | Rev E label |
|---|---|---|---|
| HM-00 | 1 | The helmet worn | FIG-01 |
| HM-01 | 2 | Face-on, halo above the brow line | FIG-02 |
| HM-02 | 2 | Front, left, rear and top | FIG-03 |
| HM-03 | 2 | The eight sites, two three-quarter views | FIG-04 |
| HM-14 | 4 | Section through one electrode assembly | FIG-05 |
| HM-04 | 5 | The same helmet in two contact states | FIG-06 |
| HM-05 | 5 | The same information read in a mirror | FIG-07 |
| HM-06 | 5 | The session runner during set-up | FIG-08 |
| HM-15 | 5 | The same moment in three dimensions | FIG-09 |
| HM-08 | 6 | Routing inside the frame | FIG-10 |
| W1 | 6 | The harness as a schedule | FIG-11 |
| POD-00 | 7 | Pod as drawn for a consolidated board (superseded) | FIG-12 |
| HM-09 | 7 | Battery access, quarter-turn hatch and keyed carrier | FIG-13 |
| HM-10 | 8 | The two microphones | FIG-14 |
| HM-11 | 8 | Reference and bias | FIG-15 |
| HM-12 | 8 | The host USB connection at the panel | FIG-16 |
| HM-13 | 9 | Fitting in three steps | FIG-17 |
| HM-07 | 10 | The frame unmounted | FIG-18 |
| CASE-00 | 11 | Case side section and foam plan | FIG-19 |
| S1 | 13 | Devices, buses and reference pin assignments | FIG-20 |
| S2 | 13 | Battery-only operation and the charger interlock | FIG-21 |
| S3 | 13 | Envelope detector | FIG-22 |
| S4 | 13 | Electrode input protection | FIG-23 |

W1 and S1--S4 did not collide with any part number. They are renumbered anyway, because a
document with two figure-labelling schemes is how the collision arose in the first place.

FIG-16's subject changed with WH-08. Rev D captioned it "the captive two-metre cable"; the
Phase 1 pod has no captive cable, so the figure is redrawn as the panel socket and its
gasketed aperture when DSN-EEG-002 Rev E is issued.

### 3.4 HM-04 quantity

**HM-04 is 8 fitted + 2 spare = 10 per kit.** This is the figure in DSN-EEG-003 Rev C §4,
in the RFQ Rev E pricing template line "MJF prints: HM-01 frame, HM-04 ×10, HM-08 hatch,
MP-01 (per kit)", in `tools/mech_gen.py` and in QP-EEG-010's sampling table (100 / 250 /
500 at 10 / 25 / 50 kits). It supersedes the qty 8 in DSN-EEG-002 Rev E §10 and the RFQ
Rev C scope line "HM-04 ×8".

The two spares are stated here so that their origin stops being undocumented: a bonded
HM-04 cannot be removed without destroying the HM-01 bore (ASM-EEG-007 §4.2), so a body
damaged during handling before bonding must be replaced from stock or the frame is scrapped
at forty times the cost of a spare body. The two spares belong to HM-04 for that reason
alone. HM-05 separately carries 8 + 2 spare cups, for the different reason that cups are
replaced by the operator about every 25 sessions (RFQ A-01). The two quantities are
independent and both are 10.

**Whether the two spare bodies travel in the case is not decided.** This register fixes the
procurement quantity at ten per kit, which is the number a print bureau quotes and prints.
PKG-EEG-015 §1.2 corrects kit BOM item 16 to "8 bonded, 2 spare bodies held as build stock,
not kit content", which is a packing decision, not a quantity decision, and it does not
change the ten. Nothing in the package rules on it, the foam has no HM-04 pocket either way,
and it is carried as OA-12 rather than settled here.

---

## 4. Serial numbers, marking and revision

### 4.1 What is marked

| Item | Marking | Method | Verified by | Signed off by |
|---|---|---|---|---|
| Every printed part with a flat face of at least 20 × 8 mm | Identifier and revision letter, e.g. `HM-08 B` | Modelled into the part, recessed 0.4 mm minimum, stroke width 0.6 mm minimum | First-off inspection of each print build, read at 10× after bead-blast, dye and a 70 % IPA wipe | Print bureau QA, countersigned at goods-in per QP-EEG-010 IP-9 |
| HM-01 | Identifier, revision, the eight site names (Fz, Cz, Pz, C3, C4, T7, T8, F7), and the print build number inside the occipital shell | Modelled in, as above | First-off, plus 100 % visual for legibility of site names | Print bureau QA and programme goods-in |
| HM-04, HM-02A/B/C, FIT-01 | **Nothing.** Too small, or too soft to hold a legible engraving | -- | Identified by the bag label at kitting | Kitting operator |
| EEG-CAR-01 | Part number, revision `EEG-CAR-01-B`, date code, licence attribution, and a 20 × 8 mm bare silkscreen serial area centred at board **(87.0, 118.0)** in the `design.py` convention | White LPI legend; serial applied as laser or label at TST-EEG-004 T18 | Read back and compared with the test record | CM test operator, countersigned by CM QA |
| The assembled unit | Label ART-LBL-01, 50 × 25 mm matt polyester with permanent acrylic adhesive, IPA-resistant, on the flat keep-out of POD-P1-02: unit serial, hardware revision, ATECC608B key fingerprint plus a Data Matrix, "RESEARCH INSTRUMENT -- NOT A MEDICAL DEVICE", one.witysk.org, and the S-01 charging warning | Printed label, artwork in PKG-EEG-015 | Data Matrix scanned and compared with the provisioning record; a mismatch quarantines both units | CM QA per TST-EEG-004 T18 and RFQ M-03 |
| WH-01 and WH-02 | Harness serial, revision and phase variant on a label at the pod end, material rated for a 70 % IPA wipe | Printed label | Continuity record H1 to H9 filed against that serial | Harness operator and CM QA per WH-EEG-008 |

The serial area moved in Rev B. Rev A put it at board (100.0, 90.0), which was clear copper
on the 130 × 124 mm outline; on the 150.0 × 130.0 mm board that position is under SW2, the
middle tactile switch at (102.0, 90.0). Board (87.0, 118.0) is the nearest position in the
digital zone with 28 × 16 mm clear of every placement in `design.py`.

The key fingerprint printed on the label is **defined once, in FW-EEG-001 section 7**: the
first 8 bytes of SHA-256 over the 64-byte uncompressed public key, printed as 16 uppercase
hex characters in four groups of four. This register cites that definition and does not
restate it.

### 4.2 Serial versus lot

Only three things in the kit carry a unique serial: the carrier, the assembled unit and
each harness. Everything else is **lot-traced**: the print build number and date, recorded
against the FIT-01 coupon for that build and on the bag, is the whole of the traceability
for printed parts. That is a deliberate limit. Engraving a unique serial into every one of
ten HM-04 bodies per kit would mean ten model variants per kit and no way to check them,
and the failure mode it would protect against -- one bad body in a batch -- is caught by the
coupon and the IP-9 sample, not by traceability after the fact.

**The unit serial format is settled: `TIOV-B-nnnn`, and it is defined once, in
PKG-EEG-015 section 5.** This register cites that definition and does not own it. It is a
programme prefix, the hardware revision letter, and four digits: Phase 1 uses 0001 to 0009, Phase 2 0010 to 0099 and
Phase 3 0100 to 0999. Five competing forms were in circulation across the package --
`OV-EEG-<phase><nnn>` in ASM-EEG-007 §6, `TIOV-EEG-<phase>-<nnn>` in QP-EEG-010 §9,
`OV-EEG-<p><nnn><C>` with a check character in PKG-EEG-015 §5, `TIOV-B-nnnn` in
FW-EEG-001 §7, and the bare `SN0001` of the golden unit in TST-EEG-004 §4 and
JIG-EEG-009 §1.12 -- and three documents each claimed to own the register. All five are
withdrawn in favour of the form above. The same string must then appear identically in the
label text, the Data Matrix, the USB `iSerialNumber` (RFQ F-04, E-21), the calibration
record and the packing list; if any two disagree the unit is quarantined. Rev A of this
register recorded only two of the five competing forms and gated the first serial allocation
on reconciling them; that action, OA-6, is closed, and the single home for the format is
PKG-EEG-015 section 5.

### 4.3 Revision rules

1. Any change to a released geometry file raises the part's revision letter. There is no
   such thing as a silent re-export: `tools/mech_gen.py` is the source and a changed source
   is a changed part.
2. A change that affects a fit, an interface or a marking requires an ECO under
   ECO-EEG-016 before the file is released, and the new letter is engraved.
3. Parts at a superseded revision may be used up only under a written concession recorded
   in ECO-EEG-016, naming the units it applies to. Mixed-revision stock without a
   concession is scrap.
4. A revision letter never appears inside an identifier. `HM-08 B` is HM-08 at Rev B; there
   is no part called HM-08B.
5. The revision of the package and the revision of a part are unrelated. HM-04, HM-08,
   MP-01, POD-P1-01 and POD-P1-02 are at Rev B while HM-02A, HM-09, FIT-01 and WH-09 are at
   Rev A, in the same package revision.
6. Rule 2 was not followed for the Rev B geometry. MP-01, POD-P1-01 and POD-P1-02 were
   resized in `tools/mech_gen.py` when the carrier grew, and no ECO was raised before the
   files were released. That is the same gap as OA-10 and is recorded, not excused.

---

## 5. Cross-reference: v1 file to v2 file to defining document

| v1 file (`package/`) | v2 file (`package_v2.4/`) | Identifier | Defining document |
|---|---|---|---|
| `mech/HM-01_frame_monocoque.stl` | not yet copied -- see OA-1 | HM-01 | DSN-EEG-002 Rev E §10 |
| `mech/HM-04_electrode_assembly_body.stl` | `mech/stl/HM-04_electrode_assembly_body.stl`, `mech/step/HM-04_electrode_assembly_body.step` | HM-04 | MECH-EEG-020 sheet 5 |
| `mech/HM-07_battery_hatch.stl` | **`mech/stl/HM-08_battery_hatch.stl`**, `mech/step/HM-08_battery_hatch.step` | HM-08 | MECH-EEG-020 sheet 6 |
| `mech/POD-P1_prototype_enclosure_base.stl` | `mech/stl/POD-P1_prototype_enclosure_base.stl` + `.step` (regenerated at 163 × 143 × 58 mm) | POD-P1-01 | MECH-EEG-020 sheet 9 -- needs reissue, OA-9 |
| `mech/POD-P1_prototype_enclosure_lid.stl` | `mech/stl/POD-P1_prototype_enclosure_lid.stl` + `.step` (regenerated at 163 × 143 × 6 mm) | POD-P1-02 | MECH-EEG-020 sheet 10 -- needs reissue, OA-9 |
| `mech/CASE-00_foam_top_layer.dxf` | **withdrawn and deleted from `mech/`**; superseded by `mech/CASE-00_foam_layer_1.dxf` and `mech/CASE-00_foam_layer_2.dxf` | CASE-00-01, CASE-00-02 | `tools/mech_gen.py` `foam_dxf()`; PKG-EEG-015 §2.2 |
| `mech/MANIFEST.json` | `mech/MANIFEST.json`, regenerated -- 56 file entries, `"schema": "PARTS-EEG-019 Rev B OA-2"` | -- | `tools/mech_gen.py` `manifest()` |
| -- | `mech/CASE-00_foam_layer_3.dxf` to `mech/CASE-00_foam_layer_7.dxf` | CASE-00-03 to CASE-00-07 | `tools/mech_gen.py` `foam_dxf()`; PKG-EEG-015 §2.2 |
| -- | `mech/stl/MP-01_module_plate.stl` + `.step` (regenerated at 146 × 126 × 3 mm) | MP-01 | ICD-EEG-006 §4; MECH-EEG-020 sheet 8 -- needs reissue, OA-9 |
| -- | `mech/stl/HM-02_brow_pad.stl` + `.step` | HM-02A | MECH-EEG-020 sheet 4 |
| -- | `mech/stl/HM-09_service_key.stl` + `.step` | HM-09 | MECH-EEG-020 sheet 7; SVC-EEG-013 §3 |
| -- | `mech/stl/FIT-01_fit_test_coupon.stl` + `.step` | FIT-01 | MECH-EEG-020 sheet 2; QP-EEG-010 IP-9 |
| -- | `mech/drawings/MECH-EEG-020_RevA_printed_part_drawings.pdf` | -- | **25 sheets**, one per released solid, numbered in `mech/stl/` filename order and indexed in `mech/drawings/MECH-EEG-020_sheet_index.csv`. Verified: the PDF carries 25 pages and the index 25 rows. The set is regenerated from the released meshes by `tools/mech_drawings.py`, so MP-01, POD-P1-01 and POD-P1-02 -- now sheets 16, 18 and 19 -- are drawn at the Rev B geometry and OA-9's dimensional half is answered; **what OA-9 still owes is the document revision letter and its ECO entry**, because the file is named Rev A and carries fifteen sheets it did not have. The "10 sheets" and the "sheets 6, 7 and 8" of earlier issues of this row are both withdrawn |
| `kicad/EEG-CAR-01.kicad_pcb` (Rev A, 130 × 124 mm, two layers) | `kicad/` regenerated from `tools/design.py` (Rev B, 150.0 × 130.0 mm, four layers) | EEG-CAR-01 | DSN-EEG-003 Rev C §3 |
| `firmware/main.c` | `firmware/` with build system, partitions, provisioning | FW-EEG-001 | DSN-EEG-003 Rev C §5 |

---

## 6. Audit closure

| Audit item | Status | How |
|---|---|---|
| **XD-01** (blocking) -- HM-07 names two parts; the boom arm and the pod hatch have no file and no BOM line under their own IDs | **Closed in this register, open in three documents** | HM-07 stays with the boom microphone arm and is split into HM-07A/B/C; the hatch STL is renamed HM-08; the old HM-08's cell carrier becomes HM-10. Reasoning in §3.1, migration in §3.2. Kit BOM item 17 reads "HM-08 battery hatch", RFQ Rev E §1 scope and the pricing template read "HM-08 hatch". REG-EEG-012, RISK-EEG-011 and PKG-EEG-015 still carry the v1 numbering -- OA-4 |
| **XD-02** (major) -- HM-xx used as figure labels and part numbers in one document | **Closed** | Figure labels are `FIG-nn` and may never begin with a part prefix (§1.1). All 23 DSN-EEG-002 figures mapped in §3.3 for reissue as Rev E |
| **XD-03** (major) -- HM-04 print quantity differs 8 vs 10 between the governing document and the BOM | **Closed** | Fixed at **8 fitted + 2 spare = 10** per kit, with the origin of the two spares stated (§3.4). Propagated to DSN-EEG-003 Rev C §4, RFQ Rev E scope and pricing template, kit BOM item 16, QP-EEG-010 §9 and `tools/mech_gen.py`. Whether the two spares travel in the case is separately open -- OA-12 |
| gap `mech-hm07-part-number-conflict` | **Closed** | This register replaces the proposed `mech/MECH_part_number_register_RevA.csv`. XD-01's fix text names it PARTS-EEG-005; it is issued as PARTS-EEG-019, which is the number DSN-EEG-003 Rev C §4 and Annex A cite |
| gap `mech-missing-part-files` | **Mostly closed at this issue** | **Twelve of the parts this row listed as having no geometry now have STL, STEP, a MECH-EEG-020 sheet and a `mech/MANIFEST.json` entry, and are registered above with their model figures**: HM-02B, HM-02C, HM-03A, HM-05B, HM-10, HM-11A, HM-11B, HM-11C, POD-P1-04, WH-ADP-02, WH-ADP-03 and WH-ADP-04, together with all three WH-KEY-01 forms. WH-BUS-01 has a full fabrication data set in `kicad/wh-bus-01/`. AVL-EEG-017 K24 names them, so they are inside the line a print bureau quotes against for the first time. **Four are still to be created**: HM-03B ratchet housing, HM-06A chin cup, HM-06B liner and HM-07A boom temple mount; HM-01 exists as STL only and has no STEP (OA-1). WH-ADP-01 and WH-ADP-01B are bought-part classes and correctly have no geometry. **Nothing has been printed** |
| XD-04 -- printed versus bought-in for HM-03, HM-06, the boom arm | **Identifiers closed, cost open** | Each is split into a printed part and a bought-in part with separate identifiers, so a BOM line can exist for both. Which supplier part, and what it costs, is AVL-EEG-017 work |
| Cross-document 1.2 -- MP-01 plate size and hole grid given three ways | **Closed** | §2.4: 146.00 × 126.00 × 3.00 mm, 37.25 cm³, 8 mm border, slots **12 mm long by 3 mm wide** on a 16 × 7 mm grid, Ø2.7 mm M2.5 holes between the slot rows, one 31 × 61 mm DevKit opening, four M3 holes at (5,5) (145,5) (5,125) (145,125) -- all regenerated from `mech_gen.mp01()` |
| Cross-document 1.3 and 1.4 -- POD-P1 internal depth and external geometry given four ways | **Closed** | §2.2: internal **158.0 × 138.0 × 55.5 mm**, base **163.00 × 143.00 × 58.00 mm, 144.42 cm³**, lid **163.00 × 143.00 × 6.00 mm, 136.36 cm³**, all regenerated from `mech_gen.pod_base()` and `pod_lid()`. The v1 figures 146.8 × 140.8 × 44 and the 41.6 mm measured depth are both superseded |
| Cross-document 1.15 and 5.8 -- five unit serial formats, three claimed owners | **Closed** | §4.2 records all five and cites the format `TIOV-B-nnnn`, which is defined once in PKG-EEG-015 §5. OA-6 is closed |
| Cross-document 2.8 -- documents that renumber TST-EEG-004's steps | **Closed** | §2.4 cites the fixture-to-step mapping from **TST-EEG-004 Rev C §6.1**, which is where the fixture table lives, and invents no step numbers. FIX-02 now serves T28, the new E-29 acoustic-output type test; FIX-03 serves T25, not T23 |
| Cross-document 2.12 -- jumper keying decided three ways | **Closed** | §2.4: shrouded polarised IDC at the module end where the module has one, the printed shroud **WH-KEY-01** at the carrier end, and the JIG `SHR-` names recorded as legacy |
| Cross-document 2.13 and 5.1 -- host USB socket or captive cable | **Closed** | §2.2 and §2.4: a socket on WH-ADP-04, WH-08 and the gland withdrawn from Phase 1, WH-09 registered, and the E-24 non-conformance stated in the same sentence as the part |
| Cross-document 2.14 -- HM-07 / HM-08 still live in REG, RISK and PKG | **Named, not closed** | §3.1 names all three documents and the exact lines. The corrections belong to those documents and are carried as OA-4 |
| Cross-document 2.22 -- spare cell decided "none", foam still cuts a pocket | **Referred** | §2.3 no longer restates the bay schedule. Whether the SPARE CELL bay stays in the Rev C stack -- it is cut in `mech/CASE-00_foam_layer_1.dxf` and `_2.dxf` and travels empty -- is PKG-EEG-015 §2.2's decision, not this register's |
| Cross-document 3.1 -- A-03 headband has no design, no drawing and no packing line | **Closed** | The note under §2.1: A-03 is withdrawn as a kit item and rewritten onto HM-06A/B/C and HM-03A, so no headband identifier is needed |
| Cross-document 3.4 -- EOG panel sockets have no cable, no part, no drawing | **Closed as a stated omission** | §2.5 lists them as a Phase 2 option with no identifier allocated and states the consequence: channels 15 and 16 are protected and tested and reach no panel socket |
| Cross-document 4.12 -- foam pocket schedule written out in four documents | **Closed here** | §2.3 cites PKG-EEG-015 §2.2 and keeps only the sheet size, the layer number and which bays each layer cuts |
| Cross-document 5.23 -- unregistered and colliding document numbers | **Named, not closed** | §1.1 records the collisions and refers them to ECO-EEG-016 as OA-11 |

### Open actions

| # | Action | Owner | Gate |
|---|---|---|---|
| OA-1 | Copy `package/mech/HM-01_frame_monocoque.stl` into `package_v2.4/mech/stl/` unchanged, and produce a STEP model of it. HM-01 is the only released part with no STEP, because it is a rendered form study rather than a parametric model and its geometry changes once the Stage 0 fit measurement is done | Mechanical | Blocks a dimensioned drawing of HM-01; does not block printing |
| OA-2 | *(closed)* `mech/MANIFEST.json` is regenerated by `tools/mech_gen.py` `manifest()` and carries 56 file entries, each with part id, revision, description, material, process, units, marking, byte count, SHA-256, source and -- for the solids -- watertight flag, bounding box, volume and triangle count. It names itself `"schema": "PARTS-EEG-019 Rev B OA-2"`, and the seven CASE-00 Rev C foam layers are among its entries | -- | -- |
| OA-3 | FIT-01 as released carries three bores at 9.20 / 9.35 / 9.15 mm -- the cup bayonet fit only. QP-EEG-010 IP-9 checks "the HM-04 bayonet, collar and hatch fits against the fit coupons", and the collar and lug fits are not on the coupon. Either extend FIT-01 to Rev B or add FIT-02. **Restated and sharpened on 2026-09-02.** `fit01()` is three plain cylindrical bores and nothing else -- no entry slot, no circumferential run, no lug -- so it gates **no bayonet feature whatever**, and its own docstring, which says it carries the cup bayonet, is wrong about that. Now that HM-04 and HM-05B do assemble as solids, this coupon is the only acceptance there is for whether they assemble in printed PA12 at ±0.15 mm: it must gain the 1.70 mm entry slot at outer radius 5.55, the 100° run at z 1.10--3.80, the 1.10 mm lip and a lug to match, be printed in the batch, and be **turned and pulled**. SVC-EEG-013 R10's 10 N retention and WH-EEG-008 H6's 15 N are demonstrated on it before the bayonet run is called released (ASM-EEG-023 Rev A, D1-HM04-CROWN-AND-LEAF, conditions (i) and (ii)) | Mechanical + QA | Blocks IP-9 as written, and now also gates the release of the bayonet run: a 0.000 mm³ boolean is not a turned coupon |
| OA-4 | Correct the v1 part numbering still live in three documents: REG-EEG-012 Rev B §2.3, §3.1, §3.3, §3.4 and §6.2 ("HM-07 hatch", "HM-08 keyed carrier"); RISK-EEG-011 Rev B §6.1 and H-31 ("HM-07 quarter-turn hatch"); PKG-EEG-015 Rev B §1.1 line 1.11 ("HM-08 -- quarter-turn battery hatch and keyed cell carrier"). All become HM-08 hatch and HM-10 cell carrier, and REG gains the HM-07A/B/C boom rows | Regulatory, safety and packing | Erratum under ECO-EEG-016. This is the collision this register exists to close, so it is a release gate, not a tidy-up |
| OA-5 | DSN-EEG-003 Rev C §4, ASM-EEG-007 §5.1, WH-EEG-008 §1 and PKG-EEG-015 §2.4 quote superseded bounding boxes for POD-P1-01, POD-P1-02 and MP-01. Correct at the next revision to the figures in §2 above | Design | Documentary, but a CM cutting foam or a bidder pricing an enclosure from the old figures buys the wrong part |
| OA-6 | *(closed)* Unit serial format reconciled -- `TIOV-B-nnnn`, §4.2 | -- | -- |
| OA-7 | Name supplier parts for HM-03C, HM-05A, HM-06C, HM-07B, HM-07C, POD-P1-03, CASE-01 in AVL-EEG-017, and name the J15--J17 touch-proof 1.5 mm PCB socket, which is a class and not a part | Procurement | Blocks a comparable quote on the bought-in mechanical group. AVL-EEG-017 carries a 12-week lead-time risk against the J15--J17 socket |
| OA-8 | *(closed)* The Rev B bottom-layer `POD-P1 ENCLOSURE` pocket was cut 152 × 90 mm in 25 mm foam and could take neither the plan nor the depth of the 163 × 143 × 58 mm pod. The CASE-00 **Rev C** schedule of PKG-EEG-015 §2.2 gives the pod a 169 × 149 mm bay cut through layers 1 to 3, 75 mm deep over a 10 mm packer, and the seven Rev C files in `mech/` draw it; the Rev B pair is deleted. What is still open is not this bay but the release of the cut files, which PKG-EEG-015 §3.2 gates on measuring the bought shell -- §2.3 above | -- | -- |
| OA-9 | **Dimensionally answered, documentarily open.** MECH-EEG-020 is regenerated from the released meshes and now carries **25 sheets**, so MP-01, POD-P1-01 and POD-P1-02 are drawn at the Rev B geometry on sheets 16, 18 and 19 and no released sheet disagrees with its STEP. What is still owed is the **revision letter and the ECO entry**: the file is named `MECH-EEG-020_RevA_...` and carries fifteen sheets that Rev A did not have, which under §4.3's rules is a new revision of the drawing set | Mechanical, through ECO-EEG-016 | No longer blocks first-article inspection; it blocks the drawing set's own release record |
| OA-14 | **Two of the four features are cut; two are still owed.** WH-EEG-008 §3.1.1 named four things HM-04 needed: the **circumferential bayonet run**, without which HM-05B is a plug fit that cannot rotate and the HM-09 key cannot reach its drive notches; a **seat and lead passages for the contact-light LED**; an **anchorage for HM-04A that holds 15 N**; and a **dressed conductor exit** at the inboard slot opening. On 2026-09-02 the first is cut -- a 100° run at z 1.10--3.80 over a 1.10 mm retaining lip, with the entry slots widened to 1.70 mm at outer radius 5.55 and the HM-05B lug corrected to r 5.20 and raised to z 1.20--3.30, measured at 0.000 mm³ of interference through the turn and 1.557 mm³ of lip engagement -- and the LED half is separated: the window is two pockets with 1.60 mm of PA12 between them, an outboard LED pocket and an inboard conductor pocket, where it was one undivided cavity. **The seat itself and its two lead passages are not drawn**, and neither is the HM-04A anchorage or the dressed exit, so the four are one cut, one half-cut and two owed. HM-05B additionally still needs a spigot recess for HM-05C and a dry tail groove, and its flank solder-tag pocket stays withdrawn on paper while `hm05b()` still cuts it -- OA-18 | Mechanical, then the safety reviewer | **Still blocks the site end of both helmet cables** and MECH-EEG-020 sheets 8 and 9. It no longer blocks SVC-EEG-013's cup-release procedure in the model, because the carrier turns; it blocks it in fact until a coupon has been turned by hand (OA-3) |
| OA-15 | **HM-04A and HM-05C are registered here and are proposals.** They exist so that WH-EEG-008 §3.1.1, ASM-EEG-007's missing termination step and AVL-EEG-017 K25 and K26 can name the same thing. If the mechanical reviewer takes the alternative route of §3.1.1 -- a leaded cup with the joint in the frame channel -- both identifiers are withdrawn and their numbers are not reused | Mechanical, with OA-14 | Nothing can be ordered against either until the decision is taken |
| OA-17 | **Four printed fixture parts have geometry and no identifier of their own.** FIX-01/E is a manifold plus a sliding sensor carrier and FIX-02/A and FIX-02/B are each a PA12 body plus a TPU 85A lip, so under rule 1 of §1.3 there are eleven printed things behind seven files and four sub-assembly letters. The `FIX-nn/m` letter set belongs to **TST-EEG-004 Rev C §6.1** and this register allocates none of it; until it does, §2.4's table names each part by its letter and its filename. Two further things are owed with the letters: **dimensioned sheets** -- the fixture solids are in `fixtures/`, not `mech/`, so MECH-EEG-020's 25 sheets do not cover them -- and a **repair of `FIX-01E_sensor_carrier.stl`, whose released mesh is not watertight** | Test engineering, through TST-EEG-004 §6.1 and JIG-EEG-009 | Blocks nothing in the product. It blocks a first-article inspection of the fixture set, and a non-watertight mesh blocks that one part's printing |
| OA-16 | **The ear-reference couplers and the bias socket are deliberately given no identifier.** Under rule 4 of §1.3 they are unmodified bought-in catalogue connectors with no printed interface part, exactly like the Harwin M20 housings and the JST PHR-2, so each is identified by its supplier part number and its AVL-EEG-017 line (**K27**, which carries all three units) and not by an `HM`, `POD`, `MP` or `WH` number. **Extended on 2026-09-02** from the two ear couplers to the bias socket at the HM-01 halo front, on the same reasoning and with the same condition: if HM-01 gains a seat, anchorage or strain relief for that socket -- open items 22 and 26 -- a printed interface part exists and rule 4's second limb catches it, and an identifier is allocated in that change. Recorded here so that the absence reads as a decision rather than an omission | -- | Nothing. This is a note, not an action. The parts themselves are not released: see WH-10 and OA-19 |
| OA-10 | Allocate an ECO number for the carrier outline change (130 × 124 mm to 150.0 × 130.0 mm) and the two-layer to four-layer stack-up change, and for the consequent resizing of MP-01, POD-P1-01 and POD-P1-02. ECO-EEG-016 owns the number; this register does not allocate one | Programme, through ECO-EEG-016 | Blocks the fabrication drawing release and the RFQ price revision |
| OA-11 | About nineteen document numbers are cited as governing or required and are not on the ECO-EEG-016 §1 register, and six collide with registered numbers (REL-EEG-009, PROV-EEG-007, KEY-EEG-008, SD-EEG-013, OTA-EEG-014, CAL-EEG-012). Register or renumber them | Programme, through ECO-EEG-016 | The document namespace has the fault this register closed for parts |
| OA-12 | Decide whether the two spare HM-04 bodies travel in the kit or are held as build stock. The procurement quantity is ten either way; only the packing list and the foam change | Programme with packing | Blocks nothing; it stops the two documents drifting further apart |
| OA-13 | Build, price and calibrate **FIX-02/C**, the IEC 60318-1 artificial ear and the class 1 sound level meter mount that TST-EEG-004 Rev C T28 needs. TST-EEG-004 §5 and §6.1 put both inside FIX-02; JIG-EEG-009 Rev B §2.4 carries neither in the FIX-02 bill of materials, §5.2 calibrates neither, and §6.1 prices neither. JIG-EEG-009 records the same gap in its own §7 | Test engineering, through JIG-EEG-009 | Blocks T28, and T28 is the only measurement that shows the 100 dB SPL limit of RFQ E-29 is held |
| OA-18 | **Regenerate the HM-04 and HM-05B meshes for the deepened spring seat, and raise both revision letters.** The bayonet re-cut and the two contact-light pockets are in the released meshes and in `mech/MANIFEST.json`; the **spring seat deepened from 4.50 to 6.60 mm is in `tools/mech_gen.py` only**, so HM-04's released model figures, its sha256 and its manifest entry are one change behind the generator and its volume falls again when they are regenerated. Under rule 5 of §1.3 a change to a released file raises the part's letter, so **HM-04 goes to Rev C and HM-05B to Rev B**, with MECH-EEG-020 sheets 8 and 9 redrawn from the new meshes and the letters written into `manifest()`. Two smaller things travel with it: `hm05b()` still cuts the 1.60 × 1.60 × 0.80 mm flank solder-tag pocket that WH-EEG-008 §3.1.1 superseded and this register records as withdrawn, and `hm05b()`'s docstring still describes HM-04's spring seat as Ø6.80 × 4.50 mm | Mechanical, through ECO-EEG-016 | Blocks the drawing set's release record and any first-article inspection quoted against a model figure. It does not block printing, and it does not block the bayonet, which the released mesh already carries |
| OA-19 | **Issue WH-10 and settle the bias lead's AVL line.** WH-10 is reserved in §2.4 for the Fpz bias lead and is not issued: it waits on the safety reviewer, for the K27-class socket as the patient-side form of the driven output and for a written statement of the residual cross-mate now that the kit carries six sockets and six plugs of one 1.5 mm family, and on the mechanical reviewer for open items 22 and 26, because the halo-front channel mouth, the dressed exit and the strain relief are features of a carried-over HM-01 mesh that no source file generates (OA-1) and the retention figure depends on whether an anchorage is drawn. The wire list states the free tail explicitly -- 1980 mm is withdrawn -- and the pull test is not H6's 15 N. **The AVL line number is not this register's to allocate and it is contested**: WH-EEG-008 §3.1.3 names K47 for the lead, and MECH-D5 of ASM-EEG-023 Rev A issues K47 to K52 for the heat-set inserts, screws, gland and O-cord on the strength of K46 being the highest line issued. Both are written down and they cannot both stand. AVL-EEG-017's owner allocates | Programme: safety reviewer, then mechanical, then AVL-EEG-017 and ECO-EEG-016 | Blocks the purchase and the build of the bias termination, and with it conductor 11's site end |
| OA-20 | **AVL-EEG-017 K12 is still unbuyable as written, and the geometry it is written against changed on 2026-09-02.** K12 reads "3--6 N at working length, stainless 302 ... selected against the HM-04 drawing envelope (12.4 × 12.4 × 18.0 mm)", which is the outside of the body and never was the volume the spring sits in. The volume is the seat above the HM-05B spigot, and it was 1.40 mm of free height in an annulus 0.10 mm wide on the radius -- no coil occupies that, which is the finding ASM-EEG-023 Rev A, D5-K12-SPRING-ENVELOPE records. HM-04's seat is now 6.60 mm deep, so the free height is **3.50 mm** and the spring bears on the Ø6.60 spigot top inside a Ø6.80 bore. **This register states no envelope and no force.** What must happen, in order: the mechanical reviewer allocates the z 11.70--15.60 band once on MECH-EEG-020 sheet 8 across the HM-04A anchorage, the LED seat and its passages, the conductor exit and the contact leaf, and gives HM-05C a dimension and the spring a capture feature; the safety reviewer signs the solid-height bound -- a rigid stack solid inside travel puts unbounded helmet force into the scalp for a two-hour session -- and the presence of a stainless preload member inside the gel volume; then AVL-EEG-017 specifies K12 against five measured samples on a printed HM-04/HM-05B pair. Only then can this register say what the part is, and whether it takes an identifier at all: it is a catalogue item today, and the rule 4 re-cut proposed in MECH-D5 -- which excludes standard threaded fastening hardware by class and nothing else -- would bring a spring seated in a printed part inside the second limb. That re-cut, with HM-12 and POD-P1-06, is not applied in this issue | Mechanical, then the safety reviewer, then AVL-EEG-017 | Blocks the purchase of K12 and the assembly step that fits it, which ASM-EEG-007 does not have |

**Model figures regenerated in Rev B.** The left column is what the earlier files measured
and what four documents still quote; the right is what the released package_v2.3 files measure
today. Both are calculated from the mesh by the divergence theorem, and neither has been
weighed or measured on a part.

| Part | Figure still quoted elsewhere | Released v2 file | Why it changed |
|---|---|---|---|
| HM-04 | 12.4 × 12.4 × 18 mm, 1.5 cm³, and the 1.90 cm³ this register carried until 2026-09-02 | **12.40 × 12.40 × 18.00 mm, 1.86 cm³** | The v2 model added the bayonet slots, the spring seat and the light window the v1 mesh never had. The re-cut of 2026-09-02 then added the 100° circumferential run and split the light window into two pockets with 1.60 mm of PA12 between them, which is the 1.90 to 1.86 cm³. **The spring seat deepened from 4.50 to 6.60 mm is not in this figure**: it is in the generator and not yet in a mesh -- OA-18 |
| HM-05B | 10.80 × 9.10 × 12.10 mm, 0.52 cm³ | **10.40 × 9.10 × 12.10 mm, 0.52 cm³** | The x extent is twice the bayonet lug's outer radius, so this figure is the defect and its repair: the lug was generated at 5.40 mm against its own docstring's 5.20 mm, because the 0.40 mm of union overlap was added to the box width without being taken off its centre, and a 5.40 mm lug does not enter a 5.30 mm slot. The volume is unchanged at two decimal places |
| HM-08 | 48 × 36 × 6.5 mm, 3.3 cm³ | 48.00 × 36.00 × 6.50 mm, 6.87 cm³ | The v2 model adds three lugs, the coin slot and the seal groove |
| HM-09 | -- | Ø17.93 × 40.20 mm, 3.88 cm³ | Unchanged in Rev B; listed for completeness |
| HM-02A | -- | 85.00 × 22.00 × 8.00 mm, 14.44 cm³ | Unchanged in Rev B |
| FIT-01 | -- | 60.00 × 24.00 × 10.00 mm, 12.39 cm³ | Unchanged in Rev B |
| MP-01 | 126.00 × 120.00 × 3.00 mm, 29.17 cm³ | **146.00 × 126.00 × 3.00 mm, 37.25 cm³** | The plate is the carrier outline less 4 mm on each axis, and the carrier grew to 150.0 × 130.0 mm |
| POD-P1-01 | 146.8 × 140.8 × 44 mm, 105.9 cm³, and 147.00 × 141.00 × 44.00 mm, 109.51 cm³ | **163.00 × 143.00 × 58.00 mm, 144.42 cm³**; internal 158.0 × 138.0 × 55.5 mm | Resized for the 150 × 130 mm carrier plus the 18 mm standoff, the 3 mm MP-01 plate and up to 18 mm of module height. 158 × 138 mm internal plus 2 × 2.5 mm walls is 163 × 143 mm |
| POD-P1-02 | 146.8 × 140.8 × 4.4 mm, 86.6 cm³, and 147.00 × 141.00 × 6.00 mm, 121.09 cm³ | **163.00 × 143.00 × 6.00 mm, 136.36 cm³** | Matches the resized base. The lid is a 4.0 mm plate plus a 2.0 mm locating spigot |
| EEG-CAR-01 | 130.0 × 124.0 mm, two layers, 206 designators | **150.0 × 130.0 mm, four layers, 211 designators** | Thirty connectors and 156 nets would not close at the smaller size on two layers. See the note in "Why this document exists" |

The internal stack budget that these enclosure figures have to satisfy -- floor, boss,
carrier, standoff, plate and module height against the 55.5 mm internal depth -- is
specified once, in **ICD-EEG-006 section 4**, and is not restated here.

Nothing in this register has been manufactured or measured on hardware, and no safety
engineer has reviewed this design. Every dimension, volume and mass above is calculated from
a model file or from `tools/design.py`, and the first thing Phase 1 does is find out which
of them are wrong.
