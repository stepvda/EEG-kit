# Change Control and Document Register

**Document:** ECO-EEG-016 **Revision:** B **Date:** 1 September 2026, corrected 2 September 2026
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this document
and `tools/design.py` disagree, `design.py` governs.

**Revision note, Rev A to Rev B.** The routing-scope change is renumbered from ECO-EEG-016
to ECO-EEG-018 so that no change shares a number with this document; nine further changes
(ECO-EEG-019 to ECO-EEG-027) are recorded; the enlargement of the carrier to 150.0 ×
130.0 mm and its move from two layers to four are recorded inside ECO-EEG-018, which is the
change that found them; the document register is rewritten with the revision letter of every
document in the 1 September 2026 correction release, with the document identifiers that the
package cites but never registered, and with the statement, which Rev A omitted, that
nothing has been built.

**Corrections within Rev B, made on 1 September 2026, closing the findings of the second
cross-document audit that name this document.** RUL-EEG-021 and SIM-EEG-018 are registered
in section 1.1; every revision letter this document states is brought to the letters of that
section and the escape clause that let citations drift is withdrawn; the numbers
ECO-EEG-028 and ECO-EEG-029 are withdrawn and their two findings are recorded inside
ECO-EEG-018, which is where RUL-EEG-021 puts them; the claim that the board is DRC-clean is
replaced by what `kicad/EEG-CAR-01_RevB_DRC_report.txt` actually reports; and the MP-01 slot
geometry is corrected to the 12 × 3 mm that `tools/mech_gen.py` cuts. The revision letter is
deliberately not advanced: these are corrections inside the same release.

**Correction within Rev B, made on 2 September 2026: the board closed.** The DRC now reports
**zero violations and all 145 nets connected**, so the fabrication-release gate of section 3
is met and that section is rewritten to say so. ECO-EEG-018's routed-result table carries the
current figures and **section 2B records what was changed to close the board and what closing
it cost**. The fabrication data is **released for review under RFQ-EEG-002A and is still not
released for fabrication**, because no human layout engineer has read the routing. The
revision letter is again not advanced: this is a correction inside the same release.

**Further corrections within Rev B, made on 2 September 2026, closing the findings of an
independent external review of the package that name this document.** **TOOL-EEG-022 Rev A
is registered in sections 1.1 and 1.5**, having shipped, and been cited by two released
documents, while this register said that a document not on its list is not part of the
release; the three workbooks in `docs/` and the built `webtest` page are named in section 1.2
as the generated artifacts they are; RFQ-EEG-002A and RFQ-EEG-002B are ruled in section 1.3
as scopes of work rather than documents. Every production-simulation total this document
states is brought to the run of 2 September 2026 -- *171 passed, 0 failed, 5 open at the time
this note was written; **superseded later the same day by 193, 0 and 6**, see section 1.1* --
and the total in the C-01 row of section 2A is marked as the history it is. **ECO-EEG-019's
claim that the Sallen-Key corner tolerance in TST-EEG-004 "is widened to match" the X7R
substitution is withdrawn**: no such limit existed to widen, and E-11's low-pass half was not
met with the approved parts *-- it is met later the same day on C0G parts, which is recorded
under ECO-EEG-019 and does not revive the withdrawn sentence*. **Section 2D is added**,
recording the firmware and test-tool defects found and closed on the same day. The revision letter is again not advanced: these
are corrections inside the same release.

**Further corrections within Rev B, made on 2 September 2026, after the firmware was built
and after four requirements moved.** **Section 1.6 is added**, registering the four released
trees that were on no list at all -- `fixtures/`, `records/`, `kicad/wh-bus-01/` and the
provisioning and ATECC tooling under `firmware/tools/`. That is the defect of section 1.3
reappearing in the register for the second time, now against shipped data rather than
against a document, while section 1.1 went on saying that what is not on its list is not
part of the release. **Section 1.2's claim that everything under `kicad/` is produced by
`emit_all.py` from `design.py` is corrected**: `kicad/wh-bus-01/` is written by
`tools/wh_bus.py`, which imports nothing from `design.py` and is not called by
`emit_all.py`. **Every production-simulation total this document states is brought to the
run of 2 September 2026 -- 193 passed, 0 failed, 6 open** -- and the claim that the
simulator wrote this register's copy of that total is **withdrawn**: it writes SIM-EEG-018
and nothing here, which is exactly why the figure could drift and did. **Section 2E is
added**, recording the first real ESP-IDF build, the five defects it found, the emulator run
and the provisioning opcode collision. **ECO-EEG-024 is implemented**, so S-02 is met in the
design at 36.8 µA; **E-11's low-pass half is met** on C0G parts; **E-27's phase driver is
written**; and the bias-lead topology finding of section 2C is fixed. Each of those is
corrected where this document states it, with its date, rather than deleted. The revision
letter is again not advanced: these are corrections inside the same release.

**Nothing in this package has been manufactured, assembled or measured, and no safety
engineer has reviewed this design.** Every figure marked *calculated* is a calculation.
Every ECO below that is marked *implemented* is implemented in the design source, not in
copper. That statement is repeated in every controlled document on purpose.

**The firmware is the single exception to "nothing has been built", and it is a narrow
one.** Since 2 September 2026 it compiles against a real ESP-IDF -- v5.2.5, target esp32s3
-- and the four images in `firmware/release/` with the SHA-256 manifest beside them are that
build; it has also run one boot cycle under QEMU. **It has never run on hardware, because no
unit exists**, and the emulator carries none of the peripherals the firmware talks to. Built
is not run, and run in an emulator is not brought up. Section 2E states what that build and
that run do and do not prove.

## Why this document exists

Package v1 had no change control and no document register. Revisions were recorded inside
each document's own front matter, so nothing said which revisions belonged together, nothing
recorded why a change was made, and a manufacturer holding four files had no way to tell
whether they were the same release. Worse, the same part identifier meant two different
parts in two documents and nobody noticed, because there was no register to notice it in.

Package v2 Rev A fixed the part-identifier namespace and then reproduced the same failure in
its own: it numbered one of its changes ECO-EEG-016, which is also this document's number,
and it registered twenty-one documents while the package went on to cite eighteen more that
were on no list at all, six of them colliding numerically with documents that are. Rev B
closes both.

This document does four things: it registers every controlled document and its current
revision; it names the identifiers the package cites that are **not** controlled documents,
and says what they are instead; it records every engineering change from package v1 to v2,
with the reason, the verification and the impact; and it states the procedure for the next
change.

---

## 1. Document register

### 1.1 Controlled documents

Every controlled document in package v2, at the revision released on 1 September 2026. A
document not on this list is not part of the release. Section 1.3 deals with the identifiers
that other documents cite and that are not on this list, and **section 1.6, added on
2 September 2026, deals with the released data sets that carry no document identifier at
all**. Until section 1.6 existed, four substantial trees -- `fixtures/`, `records/`,
`kicad/wh-bus-01/` and the provisioning tooling under `firmware/tools/` -- shipped inside a
release whose own register said that what is not listed is not part of it.

| ID | Title | Rev | Status | Governs |
|---|---|---|---|---|
| DSN-EEG-003 | Manufacturing design package | **C** | released | architecture, carrier, precedence -- **the governing document** |
| RFQ-EEG-001 | RFQ and engineering specification | **E** | released | requirements and acceptance (M/S/O), pricing |
| ICD-EEG-006 | Interface control document | **B** | released | module interfaces, jumper schedule, GPIO map |
| SCH-EEG-005 | Schematic set, 8 sheets | B | generated | the circuit |
| DSN-EEG-002 | Helmet design and assembly | E | released, **not reissued in this round** | helmet, electrodes, wiring, fitting, case |
| PARTS-EEG-019 | Part identifier register | **B** | released | every part number in the package |
| ASM-EEG-007 | Assembly work instructions | **B** | released | how one unit is built |
| WH-EEG-008 | Harness and cable assembly | **B** | released | every cable, every conductor |
| TST-EEG-004 | Production test specification | **C** | released | what every unit is tested to, and it owns the T-numbers |
| JIG-EEG-009 | Test fixture design | **B** | released | the fixtures TST-EEG-004 needs, FIX-01 to FIX-04 |
| QP-EEG-010 | Quality plan | **B** | released | IQC, FAI, AQL, records, traceability |
| RISK-EEG-011 | Risk analysis and safety review pack | **B** | **released as an input** | the pack the safety reviewer receives |
| REG-EEG-012 | Regulatory and compliance file | **B** | released | RoHS, REACH, UN38.3, CISPR, 60601 gap analysis |
| SVC-EEG-013 | Service and refurbishment manual | **B** | released | the turnaround between participants |
| IFU-EEG-014 | Participant quick-start and placement guide | **B** | released | what goes in the case lid |
| PKG-EEG-015 | Packing, labelling and shipping | **B** | released | packing list, labels, foam, lithium shipping |
| ECO-EEG-016 | Change control and document register | **B** | released | this document |
| AVL-EEG-017 | Approved vendor list | **B** | released | sourcing, alternates, substitution |
| SIM-EEG-018 | End-to-end production simulation report | A | **released, generated** | the dry run of the manufacturing route against the data package |
| FW-EEG-001 | Firmware build and provisioning | **C** | released | firmware, build, provisioning, host tool, key fingerprint |
| MECH-EEG-020 | Printed part drawings | A | generated | dimensioned drawings of every printed part |
| RUL-EEG-021 | Rulings register | A | **released** | one answer to each cross-document disagreement, cited by section letter |
| TOOL-EEG-022 | Connectivity test program: specification, technical description and user manual | A | **released** | the browser tool that tests the USB link, and the browser client the study reuses |
| ASM-EEG-023 | Register of programme assumptions | A | released, issued 2 September 2026 | every open question the completeness audit left that was a DECISION rather than a missing file, each decided, attacked by an independent reviewer and re-decided against that attack. Twenty-two entries, ten of which block a build, three of which cannot be decided from what exists. **Nothing in it is a sign-off** |

Four entries need reading carefully rather than counting.

**SIM-EEG-018** is a report written by `tools/simulate_production.py` on each run. It is a
file in `docs/`, but it is never edited by hand: it is the output of the last run, and a
correction to it is a correction to the simulator or to `design.py`. **The last run of
2 September 2026 reports 193 checks passed, 0 failed and 6 open items**, and
`docs/SIM-EEG-018_RevA_production_simulation.md` states those three figures because the
simulator wrote that file. **It did not write this one.** Rev B said the totals agreed
"because the simulator wrote both"; that is false and is **withdrawn on 2 September 2026**.
The copy in this section is typed by hand from the run, which is precisely how it came to
stand at 171 while the report had moved to 193, and it is checked against the report rather
than trusted.

The six open items of that run are: the static IRAM pool, which links with **one byte free
of 16,384**; the carried-over v1 HM-01 mesh, which is watertight and is two disconnected
bodies; that **no human layout engineer has read the routing**, which is the
fabrication-release gate of section 3; that **E-27 has never been seen to light** -- the
phase driver is written and the current budget is met, but no unit exists, so TST-EEG-004
T11 has not been run; the unreconciled board current; and that **SR-01 is closed in the
design and not yet signed off** -- S-02 is met at 36.8 µA because ECO-EEG-024 was
implemented, and applying the fix an analysis pointed to is not the same as having it
approved.

**Three figures, three dates, and only the last one is the total.** 169 passed, 0 failed,
5 open at the 1 September 2026 issue, whose first open item was the 25 DRC violations; 171,
0 and 5 earlier on 2 September, which is what Rev B stated and is now history; **193, 0 and
6 at the run behind this release**. Between the two runs of 2 September, **one item left**
the list -- E-11's low-pass half, because the Sallen-Key moved to C0G; **two joined it** --
the IRAM pool and the HM-01 mesh, both found by measuring things nobody had measured; and
**two were restated rather than closed** -- E-27's moved from *the phase driver is not
written* to *it has never been seen to light*, and S-02's from *the single-fault current
fails* to *SR-01 is closed in the design and not signed off*. The DRC violations had left
the list before either run, when the report reached zero. The passed count moves
because the check set moves and not because anything is graded more leniently. The failed
count is 0 in every run. **A total quoted anywhere in this package that is not the total of
the last run is stale**, and the total to quote is whatever `tools/simulate_production.py`
last printed, not a figure copied between documents -- including this paragraph, which is a
copy like any other.

**RUL-EEG-021** began as an internal audit worksheet, `tools/RULINGS.md`. Four released
documents came to cite it, which made an uncontrolled file part of the release by the back
door. It is now a controlled document at Rev A and is cited as **RUL-EEG-021 with a section
letter** -- section A for the geometry taken from the source files, section B for the
instrument, section C for the structural rulings. The worksheet under `tools/` is not the
controlled copy and is not cited by any released document.

**DSN-EEG-002 Rev E** is the helmet document. It was not reissued in this correction round,
so it still carries the package v1 statement that the microphone preamplifier is on the
boom, which RUL-EEG-021 section B and ICD-EEG-006 section 2.9 correct to the MP-01 module
plate at J21. Until the next issue of DSN-EEG-002, ICD-EEG-006 governs on that point and
DSN-EEG-002 is wrong on it.

**TOOL-EEG-022** is the connectivity test program: one self-contained HTML page,
`webtest/EEG-Connectivity-Test.html`, built by `webtest/build.py` from the modules under
`webtest/js/`. It is the browser end of the wire format, and the study's own client is the
same `protocol.js`, `transport.js` and `sinks.js` with a different sink, so it is production
code and not a throwaway page. It was **added to this register on 2 September 2026**, having
been written, issued at Rev A and cited by other documents while appearing on no list at
all. That is the defect ECO-EEG-015 was raised against in the part namespace and section 1.3
was written to close in this one, reappearing in the register itself: this section states
that a document not on this list is not part of the release, so for one release TOOL-EEG-022
was formally not part of a release it shipped in. **FW-EEG-001 Rev C section 5 is normative
for the wire format and governs where the tool and the specification disagree**, and
TST-EEG-004 owns the T-numbers under which the tool is run -- **T30, the host link check** --
so a step that uses the tool is cited from TST-EEG-004 and not from TOOL-EEG-022.

### 1.2 Generated artifacts

Everything under `kicad/`, `kicad/gerber/`, `schematic/` and `graphics/` is produced by
`tools/emit_all.py` from `tools/design.py` -- **with one exception, corrected here on
2 September 2026: `kicad/wh-bus-01/`.** That directory is the WH-BUS-01 Rev A fabrication
set for the contact-light bus board, and it is written by `tools/wh_bus.py`, which
`emit_all.py` does not call and which imports nothing from `design.py`, `gerber.py`,
`pcbgen.py` or `router.py`. That independence is deliberate -- WH-BUS-01 is ten pads and one
copper bar, and running it through a 211-part four-layer board's router and DRC would couple
two boards that have no reason to be coupled -- but it means **re-running `emit_all.py` does
not regenerate WH-BUS-01, and does not prove `kicad/` current**. Everything else in the rule
stands: these files are not edited by hand, and if one of them is wrong the source is wrong
and the fix goes in the source.

The mechanical trees follow the same rule under tools that `emit_all.py` does not call:
`mech/stl` and `mech/step` from `tools/mech_gen.py`, with the board-outline STEP and the
carried-over HM-01 STL from `tools/emit_extras.py`; `mech/drawings` from
`tools/mech_drawings.py`; `mech/renders` from `tools/assembly_render.py`. A full reissue
is therefore several commands, not one, and `emit_all.py` alone does not prove the
mechanical set current. `firmware/main/board_pins.h` is declared generated from
`design.py` and is not: no tool under `tools/` writes it, and `tools/simulate_production.py`
only reads it back and checks it against `design.py`. It is maintained by hand against
that check, and that is an open item.

**Three more trees are generated by tools `emit_all.py` does not call**, and until
2 September 2026 no section of this register named any of them: `fixtures/` from
`tools/fixture_gen.py` (except `fixtures/firmware/`, which is hand-written), `records/` from
`records/make_records.py`, and `kicad/wh-bus-01/` from `tools/wh_bus.py`. Section 1.6
registers all three with the document that owns each.

**The three workbooks in `docs/` are in this class and were named nowhere in this register
until 2 September 2026.** `EEG_kit_BOM_for_bidders_RevC.xlsx`,
`EEG_kit_BOM_INTERNAL_RevC_costed.xlsx` and `EEG_kit_manufacturer_contacts_RevB.xlsx` are
written by `tools/emit_workbooks.py`, which calls `tools/emit_costed_bom.py` for the second
of them, and `emit_all.py` does not call any of it. They carry revision letters in their file
names, so they read as controlled documents and are not: they are output, they are not edited
by hand, and section 1.4 ranks the kit BOM workbook last in precedence for that reason. The
same applies to `webtest/EEG-Connectivity-Test.html`, which `webtest/build.py` inlines from
the modules under `webtest/js/` and which TOOL-EEG-022 owns.

SCH-EEG-005 is in this class. Its revision letter follows the board revision letter in
`design.py`, which is **Rev B**, and it is regenerated rather than edited whenever the
netlist changes. The board is still Rev B after ECO-EEG-019 to ECO-EEG-027, because Rev A
was the package v1 carrier and Rev B is the package v2 carrier throughout its drafting.

### 1.3 Identifiers the package cites that are not controlled documents

Package v2 Rev A registered twenty-one documents and stated that nothing else is part of the
release, and then the seventeen documents went on to cite eighteen further identifiers as
though they were controlled. Six of those collide numerically with registered documents,
which is exactly the failure ECO-EEG-015 was raised to fix in the part namespace. This
register owns the document namespace, so it rules on them here.

**Withdrawn, because they collide with a registered document.** The content is a numbered
section of the document that already owns it, and is cited that way.

| Withdrawn identifier | Collides with | Cite instead |
|---|---|---|
| REL-EEG-009 | JIG-EEG-009 | FW-EEG-001 section 9 (release and versioning) |
| PROV-EEG-007 | ASM-EEG-007 | FW-EEG-001 section 7 (provisioning) |
| KEY-EEG-008 | WH-EEG-008 | FW-EEG-001 section 7 (key handling and fingerprint) |
| SD-EEG-013 | SVC-EEG-013 | FW-EEG-001 section 10 (microSD file format) |
| OTA-EEG-014 | IFU-EEG-014 | FW-EEG-001 section 9 (field update) |
| CAL-EEG-012 | REG-EEG-012 | QP-EEG-010 section 12 (calibration record) |
| ETH-EEG-001, DIS-EEG-001, KPL-EEG-001, QSC-EEG-001, PLG-EEG-001 | RFQ-EEG-001 | the research documents of section 4, PKG-EEG-015 section 1 (packing list) and PKG-EEG-015 section 4 (quick-start card) as applicable |

**Not documents at all.** ART-LBL-01 to ART-LBL-07, ART-PACK-01, ART-DIS-01, ART-RET-01 and
DRW-LBL-PLACEMENT are label and packaging **artwork files** controlled as generated
artifacts under `graphics/` by PKG-EEG-015 section 5. QF-EEG-006-01 is a **quality form**,
controlled by QP-EEG-010 section 8. They keep their identifiers as file names; they are not
registered as documents and they carry no revision letter of their own, only the revision of
the document that owns them.

**RFQ-EEG-002A and RFQ-EEG-002B are scopes of work, not documents.** RFQ-EEG-002A is cited
in fifteen of the documents in `docs/`, and it is what the fabrication-release gate of
section 3 waits on; until 2 September 2026 no register named it at all. They are defined in
RFQ-EEG-001 Rev E section 1.1: **002A** is the review and sign-off of the supplied carrier
routing, which is the gate of section 3 below, and **002B** is the prototype builds and
complete field kits in three phases. Neither has a file, a revision letter or an author, and
neither may be cited as though it had one; the document that carries them is RFQ-EEG-001 at
the letter in section 1.1, and a statement about what 002A covers is a citation of
RFQ-EEG-001 Rev E section 1.1.

**MECH-EEG-020** was cited before it was registered. It is now registered in section 1.1 as
a generated artifact. **TOOL-EEG-022 was cited before it was registered too**: two
released documents, FW-EEG-001 section 5 and RFQ-EEG-001 Rev E, named it while this register
did not. It is registered in section 1.1 and section 1.5 as of 2 September 2026, and what it
is is set out under section 1.1.

**`tools/RULINGS.md` and the simulation report were cited before they were registered too**,
which is the same defect in a worse place: four released documents -- TST-EEG-004 section 3,
ASM-EEG-007 section 2.2, AVL-EEG-017 and this document at ECO-EEG-020 -- cited an
uncontrolled worksheet under `tools/` as though it were a released document, and several
cited the production simulation by name. Both are now controlled documents in section 1.1:
the worksheet is issued as **RUL-EEG-021 Rev A** and is cited as RUL-EEG-021 with a section
letter, and the simulation report is **SIM-EEG-018 Rev A**. The file `tools/RULINGS.md` is
not a document, is not the controlled copy, and is not cited by anything in the release.

The unit serial-number format is not a document but it was claimed by three of them. It is
ruled: **`TIOV-B-nnnn`** -- programme prefix, hardware revision letter, four digits, Phase 1
using 0001 to 0009. It is defined once in PKG-EEG-015 section 5 and appears identically in
the label text, the Data Matrix, the USB `iSerialNumber`, the calibration record and the
packing list. Every other form that appeared in package v1 and in package v2 Rev A drafts is
withdrawn.

### 1.4 Precedence

Highest first: **DSN-EEG-003 → RFQ-EEG-001 → ICD-EEG-006 → SCH-EEG-005 → DSN-EEG-002 →
PARTS-EEG-019 → the kit BOM workbook.** Where a number appears in a document and in
`tools/design.py`, **`design.py` governs**.

### 1.5 Revision letters in this release

Every document marked in bold in section 1.1 was reissued on 1 September 2026 and its
revision letter advanced by one. RUL-EEG-021, SIM-EEG-018 and TOOL-EEG-022 are new, at
Rev A; TOOL-EEG-022 was issued at Rev A on that date but was not registered here until
2 September 2026, which is a defect in this register and not a second issue of the tool.
**ASM-EEG-023 is also new at Rev A and was issued on 2 September 2026**, one day after the
rest, which is why it is the one document in section 1.1 whose date is not 1 September. The
file names in `docs/` carry the letters, and the letters in section 1.1 are the release.

A cross-reference names a document by its identifier and section, not by its revision. Where
a cross-reference does give a letter, that letter must be the one in section 1.1:

| Document | Letter to cite |
|---|---|
| DSN-EEG-003, the governing document | Rev C |
| RFQ-EEG-001 | Rev E |
| TST-EEG-004 | Rev C |
| FW-EEG-001 | Rev C |
| DSN-EEG-002 | Rev E |
| ICD-EEG-006, SCH-EEG-005, PARTS-EEG-019, ASM-EEG-007, WH-EEG-008, JIG-EEG-009, QP-EEG-010, RISK-EEG-011, REG-EEG-012, SVC-EEG-013, IFU-EEG-014, PKG-EEG-015, ECO-EEG-016, AVL-EEG-017 | Rev B |
| SIM-EEG-018, MECH-EEG-020, RUL-EEG-021, TOOL-EEG-022, ASM-EEG-023 | Rev A |

An older letter in a cross-reference is a defect to be corrected, not a synonym. **Rev A of
this document said that an older letter "means the same document as corrected in this
release"; that escape clause is withdrawn**, because a package whose citations are allowed
to drift cannot be checked against itself, which is the failure the whole register exists to
prevent. A release is the whole set at the letters in section 1.1 or it is nothing.

Two letters are easy to trip over, and both are correct as written. **The board is
EEG-CAR-01 Rev B and stays Rev B** through this correction round, so "an ECO against Rev C
of the board" in section 2.3 means the *next* board revision and not DSN-EEG-003 Rev C.
**SCH-EEG-005's letter follows the board's letter**, not the document round's, which is why
it is B while the documents around it are B or C for a different reason.

### 1.6 Released data sets that carry no document identifier

**Added 2 September 2026.** Four trees ship in this release, are relied on by released
documents, and were named in no register at all. That is the failure of section 1.3
reappearing for the second time inside the register itself, and on a larger scale than the
TOOL-EEG-022 case, because none of these is a single file: `fixtures/` alone carries two
fixture board sets, seven printed parts and a firmware project. They are **not** promoted to
controlled documents -- none of them is a document -- they are registered here as released
data, each with the document that owns it, the tool that writes it, and what it is not.

| Tree | What it is | Owned by | Written by | Status |
|---|---|---|---|---|
| `fixtures/` | the FIX-01 to FIX-04 test-fixture data: board data for `pcb/FIX-01` and `pcb/FIX-04`, seven printed parts in `step/` and `stl/`, the M1-M3 fixture controller firmware under `fixtures/firmware/`, and `MANIFEST.json` with a SHA-256 for every file | JIG-EEG-009 Rev B | `tools/fixture_gen.py`, except `fixtures/firmware/`, which is hand-written C | released as fixture data. **The two fixture boards are NOT a fabrication set** -- there is no copper layer on either, and `fixtures/README_fixture_data_index.txt` says why |
| `records/` | the machine-readable per-unit test record: the JSON schema, a worked example record, the lot-summary CSV header and the calibration-certificate template | TST-EEG-004 Rev C sections 12 and 13 | `records/make_records.py`, which reads the step list out of TST-EEG-004 at generation time and fails rather than writes if the document and the table disagree | released, generated |
| `kicad/wh-bus-01/` | the WH-BUS-01 Rev A fabrication data for the contact-light bus board: Gerbers, drill, IPC-D-356A netlist, placement and BOM note, and the checksum file | PARTS-EEG-019 Rev B registers the part; WH-EEG-008 Rev B owns the harness it serves | `tools/wh_bus.py` -- **not** `emit_all.py`; see section 1.2 | released, generated |
| `firmware/tools/` | the provisioning station: `provision.py` and `provision_selftest.py`, `atecc608b_config.py` and the three configuration files it writes, `calibration_schema.py` and its schema, and `verify_stream.py` | FW-EEG-001 Rev C section 7 | hand-written, except the three ATECC configuration files and the calibration schema, which their own generators write and check | released as tooling. **`ATECC608B_CONFIG_TEMPLATE.md` is a PROPOSAL in its own words** -- not reviewed, never written to a part, not released for production |

Two files in that last tree read like documents and are not. `firmware/tools/README_provisioning.md`
and `firmware/tools/ATECC608B_CONFIG_TEMPLATE.md` both open with a `Document:` line, a
licence and a list of governing documents, which is the front matter of a controlled
document in this package. **They carry no revision letter and they are not controlled
documents**: they are the tooling's own documentation, owned by FW-EEG-001 section 7, and
where either disagrees with FW-EEG-001 the specification governs. Front matter does not make
a document; section 1.1 does.

**Where the boundary is.** A tree in this section is part of the release and may be cited by
a released document, by path and by the owning document's section. It is not cited as though
it had a revision letter, and a statement about what it contains is a citation of its owner
in section 1.1. Anything shipped that is on neither list is the defect this section exists
to stop, and the next one is raised against this section rather than discovered by an
outside reviewer, which is how these four were found.

---

## 2. Engineering changes, package v1 to v2

Twenty-six changes: twenty-one to the carrier design, three to the package structure, and
two that change a requirement without changing the carrier. That split is the register in
section 2.1 counted: carrier is ECO-EEG-001 to ECO-EEG-014, ECO-EEG-019 to ECO-EEG-024 and
ECO-EEG-027; package structure is ECO-EEG-015, ECO-EEG-017 and ECO-EEG-018; requirement-only
is ECO-EEG-025 and ECO-EEG-026.

Eight of the twenty-six are classed blocking -- ECO-EEG-001 to ECO-EEG-004, ECO-EEG-007 to
ECO-EEG-009 and ECO-EEG-013 -- and every one of them is a package v1 defect that meant the
board could not have been built. ECO-EEG-018 is classed scope and carries two further
blocking findings of its own, that the board as drafted at 130 × 124 mm on two layers could
not have been routed; that is why it is the longest entry in the register. ECO-EEG-024 is
classed blocking for Phase 2. Rev B recorded two changes as **not implemented**, ECO-EEG-023
and ECO-EEG-024; **corrected on 2 September 2026, ECO-EEG-024 is implemented** and only
ECO-EEG-023 remains open. Both are still addressed to the safety reviewer, because taking a
change in the design source is not the same as having it approved: ECO-EEG-024's own row in
RISK-EEG-011, SR-01, is closed in the design and unsigned.

**ECO-EEG-016 is this document's identifier and is deliberately not used as a change
number.** The change numbers run **ECO-EEG-001 to ECO-EEG-015 and ECO-EEG-017 to
ECO-EEG-027**, which is exactly what the table in section 2.1 contains, what RUL-EEG-021
section B rules, and what DSN-EEG-003 section 9 and RFQ-EEG-001 read the register as
containing. In package v2 Rev A the routing-scope change was numbered ECO-EEG-016, so a
citation of "ECO-EEG-016" was ambiguous everywhere it appeared; it is now **ECO-EEG-018**.

**ECO-EEG-028 and ECO-EEG-029 are withdrawn.** A Rev B draft of this document briefly gave
the board size and the layer count their own numbers. No ruling creates them, and
RUL-EEG-021 section A treats both as findings of the routing work rather than as changes in
their own right, so they are recorded inside ECO-EEG-018 under their own headings. Neither
number is reused: as with the part identifiers of ECO-EEG-015, a withdrawn number stays
withdrawn.

**This register is the one home for the change list.** DESIGN_FACTS section 7 and
DSN-EEG-003 section 9 index the same fourteen changes in their own phrasings; both are
indexes, this section is the register, and where they differ this section governs.

### 2.1 The register

| ECO | Class | Subject | Status |
|---|---|---|---|
| ECO-EEG-001 | blocking | contact lights had no driver | implemented |
| ECO-EEG-002 | blocking | nothing supplied the 3.3 V rail | implemented |
| ECO-EEG-003 | blocking | there was no charge input | implemented |
| ECO-EEG-004 | blocking | the envelope filter was not in circuit | implemented |
| ECO-EEG-005 | major | rectifier diode pair the wrong way round | implemented |
| ECO-EEG-006 | major | filter in the wrong place in frequency | implemented |
| ECO-EEG-007 | blocking | the board had no mounting holes | implemented |
| ECO-EEG-008 | blocking | the DevKit would not have fitted | implemented |
| ECO-EEG-009 | blocking | the pin map used the PSRAM pins | implemented |
| ECO-EEG-010 | major | four functions declared and not connected | implemented |
| ECO-EEG-011 | major | no analogue reference at the module connectors | implemented |
| ECO-EEG-012 | major | non-plated holes would have been plated | implemented |
| ECO-EEG-013 | blocking | analogue module connectors could not be escaped | implemented |
| ECO-EEG-014 | major | light lines ran through the electrode harness | implemented |
| ECO-EEG-015 | major, documentation | part identifiers meant two different things | implemented |
| ECO-EEG-017 | major, compliance | lithium shipping was never mentioned | implemented |
| ECO-EEG-018 | scope, with two blocking findings | the routing is now supplied, and doing it grew the carrier to 150.0 × 130.0 mm and took it from two layers to four | implemented |
| ECO-EEG-019 | major | C1–C16 carried an X7R part number under a C0G requirement | implemented |
| ECO-EEG-020 | minor | the board had no fiducials | implemented |
| ECO-EEG-021 | major | the I²C bus had no pull-ups on the carrier | implemented |
| ECO-EEG-022 | major | VBUS_DET did not reach a guaranteed logic high | implemented |
| ECO-EEG-023 | major | ENV_CMP swings ±2.5 V into a 3.3 V pin | **OPEN, not implemented** |
| ECO-EEG-024 | blocking for Phase 2 | S-02 single-fault DC fails at 53.2 µA | **implemented 2 September 2026**, was OPEN; S-02 now met in the design at 36.8 µA and not signed off |
| ECO-EEG-025 | major | F-06's three-minute ring buffer does not fit the PSRAM | implemented |
| ECO-EEG-026 | major | E-04's −100 dB crosstalk is neither achievable nor measurable | implemented |
| ECO-EEG-027 | major | the envelope AC-coupling corner removed the envelope | implemented |
| ~~ECO-EEG-028~~ | -- | withdrawn; the board size is a finding of ECO-EEG-018 | withdrawn |
| ~~ECO-EEG-029~~ | -- | withdrawn; the layer count is a finding of ECO-EEG-018 | withdrawn |

### ECO-EEG-001 -- the contact lights had no driver

**Class:** blocking. **Found by:** netlist connectivity check (single-pad nets).
**Was:** the eight `LED1`–`LED8` nets existed on the harness connector J14 and nowhere
else. The 74HC595 module socket J19 carried only power, ground, the three shift-register
control lines and a nominal LED supply pair; the module's eight Q outputs were not brought
to the carrier at all. The contact lights -- which the whole self-fitting design depends on,
and which DSN-EEG-002 section 5 argues for at length -- could not have worked.
**Now:** J19 is a 1×16 socket exposing Q0–Q7 as well as OE and MR. Q0–Q7 drive the harness
lines through R70–R77 (1 kΩ), giving (3.3 − 2.0) / 1000 = **1.3 mA per site and 10.4 mA
total** from GPIO48. The three colours come from eight lines and one common by driving
two-lead bicolour LEDs in two phases at a nominal 240 Hz (see FW-EEG-001 and SCH-EEG-005
sheet 8). **Corrected 2 September 2026:** the driver that now exists alternates on the
FreeRTOS tick, so the real rate is **about 250 Hz rather than exactly 240**; both halves are
equal, so the duty is 50/50 and the colour does not shift. E-27 is written against "above
100 Hz" and 250 Hz meets it. The rate is stated rather than rounded back to 240.
**Verified:** every `LEDn` net is one connected copper island in the DRC connectivity check;
the drive current is computed in `tools/simulate_production.py` station 9.
**Impact:** J19 pin count, eight new resistors, a firmware change, and a change to the
bicolour LED part in the kit BOM.
**Was not closed by this ECO, and was closed on 2 September 2026:** Rev B recorded that the
bicolour phase scheme was specified and **the driver was not written** -- `lights_write()`
and `lights_task()` were on/off only, so E-27's amber state had no implementation and
TST-EEG-004 T11 could not pass. **The driver is now written.** Both halves of the ADS1299
lead-off word are read, where only `LOFF_STATP` was before: one bit per site cannot express
three colours, which is where amber had been lost. Neither detector gone is green, exactly
one is amber, both is red; green in phase A, red in phase B, amber in both.
**What is still open is different and smaller, and it is open item 4 of the simulation run:
E-27 has never been seen to light.** No unit exists, so nothing has been driven and T11 --
which reads the red-to-green ratio with a colorimeter -- has not been run. A driver that
compiles is not a light that is amber. FW-EEG-001 owns the FW-Dnn status.

### ECO-EEG-002 -- nothing supplied the 3.3 V rail

**Class:** blocking. **Found by:** netlist connectivity check.
**Was:** `DVDD3V3` had twelve pads, all of them module supply inputs, and no source. The
charger module's SYS output, the ESP32-S3-DevKitC-1's 5 V pin and both ADS1299 module
supply pins were unconnected nets. The board could not have powered up.
**Now:** the charger's power-path output is `VSYS`; a TPS63020-class buck-boost module at
J25 makes `V5V`; `V5V` feeds the DevKit at J6.21 and both ADS modules at J1.11 and J3.11;
the DevKit's on-board regulator makes `DVDD3V3`. R86 pulls the buck-boost enable to VSYS so
the rail starts before `DVDD3V3` exists. C70–C74 are the bulk decoupling.
**Verified:** power tree drawn on SCH-EEG-005 sheet 7; every rail is one connected island.
**Impact:** one new module in the BOM, one new socket, six new passives, a change to the
pricing template.
**Not closed by this ECO:** the carrier draws a **calculated 288 mA worst case** from the
DevKit's on-board regulator, which is inside its rating but dissipates about 0.5 W inside a
closed pod, so **the rail is not proven**. Phase 1 measures it at TST-EEG-004 T3 and reports
the case temperature; see section 2.3.

### ECO-EEG-003 -- there was no charge input

**Class:** blocking. **Found by:** netlist connectivity check.
**Was:** `VBUS_CHG` had one pad, on the charger module socket. Nothing brought power to it.
RFQ-EEG-001 Rev C E-23 called for "a USB-C connector for charging and data", which cannot be
reconciled with S-03's requirement that no conductive path exist from the host connector to
the patient side.
**Now:** two separate connectors. Data is the USB-C on the ADuM4160 module and carries no
power to the instrument. Charging is a separate charge-only receptacle wired to J24 through
F1 (1.1 A PTC) and D24 (transient suppressor), with a divider (R84/R85) giving `VBUS_DET`
on GPIO46. RFQ E-23 has been rewritten to say so and to carry the 45 °C charge inhibit --
"charger IC with thermal regulation; no charging above 45 °C" -- which is E-23, not S-04.
**Verified:** two independent interlocks are described and tested in TST-EEG-004; the
current path is drawn on SCH-EEG-005 sheet 7.
**Impact:** one panel part, one pigtail, an enclosure opening, a label warning, and a line
in the participant card.
**Not closed by this ECO:** the divider value was wrong and is corrected by ECO-EEG-022.
The **thermistor of S-04 is not fitted and S-04 is not met** -- there is no NTC net in
`design.py` and no thermistor way on J12 or J13 -- so the 45 °C inhibit rests on the charger
IC's own thermal regulation alone. DSN-EEG-003 section 11 and RISK-EEG-011 carry it as an
open hardware item.
**Also not closed:** the host connector on the named ADuM4160 module is **USB-B while E-24
asks for USB-C**, which is a live non-conformance. The interim answer is a short
USB-B-to-USB-C panel pigtail, WH-09, until an isolator module with a USB-C host connector is
qualified. The host connection is a socket, not a captive cable; the captive lead through a
gland is a Phase 2 item.

### ECO-EEG-004 -- the envelope filter was not in circuit

**Class:** blocking. **Found by:** netlist connectivity check (single-pad nets `ENVn_F_INM`).
**Was:** each envelope channel used one dual OPA2376. The second amplifier's inverting input
was unconnected and its non-inverting input was tied to `AGND_REF`, so the Sallen-Key network
around it drove nothing and the amplifier's output was an unconstrained buffer of the
reference. The 50 Hz filter that RFQ E-11 requires did not exist electrically.
**Now:** one OPA4376 quad per channel: A is the precision half-wave rectifier, B is the
inverting summer that makes the absolute value, C is the Sallen-Key low-pass with both loops
closed, D is the output buffer after the divider.
**Verified:** SCH-EEG-005 sheet 3 draws every connection; `simulate_production.py` computes
the corner frequency and Q from the fitted values.
**Impact:** U1–U3 change from SOIC-8 to TSSOP-14 and from dual to quad; three new resistors
per channel.

### ECO-EEG-005 -- the rectifier diode pair was the wrong way round

**Class:** major. **Found by:** review of the netlist against the BAT54S datasheet pinout.
**Was:** `D20.1` was the op-amp output, `D20.2` the summing node and `D20.3` the rectified
node. On a BAT54S, pin 3 is the common point of the series pair, so this connects two
anodes into one node rather than forming a feedback rectifier.
**Now:** pin 3 is the op-amp output; pin 1 is the rectified node and pin 2 the inverting
input. The loop closes for both polarities, which is what makes it a precision rectifier.
**Verified:** SCH-EEG-005 sheet 3; the topology is stated in the drawing note.
**Impact:** netlist only. Same part, same footprint.
**Scope note:** BAT54S is used **only** at D20, D40 and D60, the envelope rectifiers.
D1–D16, the electrode clamps, are **BAV99**: Schottky leakage across the series resistor --
47 kΩ when this was written, **68 kΩ since ECO-EEG-024 was implemented on 2 September 2026**,
which makes the same argument harder, not easier -- is an offset error on a 10 µV input. TST-EEG-004 T1 is corrected to say so.

### ECO-EEG-006 -- the filter was in the wrong place in frequency

**Class:** major. **Found by:** computing the transfer function from the fitted values.
**Was:** R = 33 kΩ, both capacitors 100 nF. Equal R and equal C in a unity-gain Sallen-Key
gives Q = 0.5 and a −3 dB point at 0.64 × f₀ = 31 Hz, not the 50 Hz ± 10 % of RFQ E-11.
**Now:** R = 22 kΩ, C to ground 100 nF, feedback C 220 nF → f₀ = 48.77 Hz, Q = 0.7416
(Butterworth), −3 dB at ≈ 50 Hz. The group delay at DC is 1 / (Q × 2π × f₀) = **4.40 ms**,
which is 4.40 samples at 1000 Hz; the √2 / (2π f₀) form that gives 4.61 ms is only correct at
Q = 0.7071 and is withdrawn.
**Verified:** computed in `simulate_production.py` station 9 and checked against E-11;
JIG-EEG-009 section 2.3 carries the derivation.
**Impact:** three resistor values and three capacitor values.

### ECO-EEG-007 -- the board had no mounting holes

**Class:** blocking. **Found by:** comparing the specification sheet with the board file.
**Was:** `EEG-CAR-01_PCB_spec_sheet.txt` promised "4 × M3 mounting holes (see placement
PDF)" and DSN-EEG-003 Rev A.2 section 3 said "400 of 406 pads; the six unassigned are
mounting holes". Neither was true: the six unassigned pads were the retention posts of the
DIN 42802 sockets, and there was no M3 hole anywhere in the file. The assembled carrier
could not have been fastened into POD-P1 or into the helmet shell.
**Now:** MH1–MH4, 3.2 mm non-plated, at **(5, 5), (145, 5), (5, 125) and (145, 125)** on the
150 × 130 mm outline of ECO-EEG-018, each with a 6 mm diameter copper keep-out on **all four
layers**. The same pattern is carried into the MP-01 module plate and the POD-P1 bosses.
The carrier is held to MP-01 on four M3 × 18 mm nylon hex female-female standoffs with eight
M3 × 6 nylon pan screws.
**Verified:** on the fabrication drawing, in the NPTH drill file, and in the DRC keep-out
check.
**Impact:** four holes, a copper keep-out, and matching features on two printed parts.

### ECO-EEG-008 -- the DevKit would not have fitted

**Class:** blocking. **Found by:** checking the socket placement against the
ESP32-S3-DevKitC-1 mechanical drawing.
**Was:** J6 at x = 70 mm and J7 at x = 92 mm, a 22.0 mm row spacing. The DevKitC-1 header
rows are 22.86 mm (0.900 in) apart.
**Now:** J6 at x = 78.0 and J7 at x = 100.86.
**Verified:** `simulate_production.py` station 5 measures the spacing from the design source.
**Impact:** placement only.

### ECO-EEG-009 -- the firmware pin map used the PSRAM pins

**Class:** blocking. **Found by:** checking the pin map against the ESP32-S3-DevKitC-1-N16R8
datasheet.
**Was:** `LED_SR_DATA` on GPIO35, `LED_SR_CLK` on GPIO36 and `LED_SR_LATCH` on GPIO37.
On the -N16R8 those three pins carry the **octal SPI PSRAM**, which the firmware needs for
the ring buffer of RFQ F-06. Using them would have made the ring buffer and the shift
register mutually exclusive. GPIO45, also used, is the VDD_SPI strapping pin.
**Now:** the shift register moved to GPIO41, GPIO42 and GPIO0, and the microSD interface
dropped from four-bit to **one-bit SDMMC** to release them. The sample stream is **50.7 kB/s
of frame payload at 1000 Hz** -- 1015 bytes every 20 ms -- against about 2 MB/s available on
one-bit SDMMC, so the headroom is ample. RFQ E-20's "≈70 kB/s" and F-12's "≈64 kB/s" are
allowances that include STATUS and SIGNATURE frames and filesystem overhead; they remain the
requirement and 50.7 kB/s is the payload figure. J7 positions 11, 12, 13 and 15 are
explicitly unconnected and are marked so on the assembly drawing and in `board_pins.h`.
**Verified:** `board_pins.h` is generated from `design.py`; the simulator checks that none of
the four reserved GPIOs appears in it.
**Impact:** firmware pin map, three carrier nets, RFQ E-18 and E-20 wording.
**Consequence for J26:** GPIO0 is now LED_SR_LATCH, so J26 way 6 is **NC_GPIO0**, a spare
way, and the carrier's J26 is console and recovery only and **cannot** enter download mode.
End-of-line flashing goes through the DevKitC-1's own UART USB-C port, which carries the
auto-reset circuit on the DevKit itself and is reachable through the MP-01 opening.
**Ring-buffer size:** the "12 MB ring buffer" this ECO cited in Rev A was never possible on
an 8 MiB part. See ECO-EEG-025.

### ECO-EEG-010 -- four functions were declared and not connected

**Class:** major. **Found by:** netlist connectivity check.
**Was:** `ENV_CMP` (the stimulus comparator of RFQ E-12) had one pad and no comparator;
`MIC_BIAS` had one pad; `SPARE1` and `SPARE2` (the two spare converter channels of RFQ 3.1,
"brought out to the connector") had one pad each and no protection; and `ROOM_PRE` had no
source at all, because the room microphone that RFQ E-15 requires had no connector.
**Now:** U7 (TLV3201) with its threshold divider, hysteresis and output clamp implements
E-12 and it is raised from Should to Mandatory; the electret bias is R89, fitted only if the
preamp module does not provide its own (**ICD-EEG-006 section 7.2** gives the decision); the
two spare channels get protection networks R15/R16, D15/D16, C15/C16 and are brought to J22;
J28 is the room-microphone module socket.
**Verified:** every one of those nets is now a connected island; E-12 and E-15 have named
test steps in TST-EEG-004.
**Impact:** one new device, one new socket, six new passives, two RFQ requirement changes.
**Not closed by this ECO:** U7's output logic level is wrong for a 3.3 V input. See
ECO-EEG-023, which is open. The **EOG panel sockets on J22 are not fitted in a standard
build**; the sockets, their cable and their drawing are a Phase 2 option and PARTS-EEG-019
lists them with no part number yet.

### ECO-EEG-011 -- no analogue reference at the module connectors

**Class:** major. **Found by:** review of the module interface.
**Was:** neither analogue module connector carried an analogue reference pin, so the module's
own reference and the carrier's `AGND_REF` pour met only through the supply rails. Both
modules' `AVDD` and `AVSS` were also hard-commoned, which parallels two regulators.
**Now:** `AGND_REF` is on J23.4 and J29.4. Module #2's rails are separate nets (`AVDD2`,
`AVSS2`) joined to the carrier rails by R92 and R93, which are fitted by default and removed
if module #2 regulates its own rails. **ICD-EEG-006 section 7.1** gives the measurement that
decides; Rev A of this document cited section 4, which is the mechanical stack, and is
corrected.
**Verified:** SCH-EEG-005 sheet 4.
**Impact:** two connector pins, two 0 Ω links, one decision recorded in the build record.

### ECO-EEG-012 -- the non-plated holes would have been plated

**Class:** major. **Found by:** reading the footprint definitions.
**Was:** the six DIN 42802 retention holes were declared `(pad "" np_thru_hole circle …
(layers *.Cu *.Mask))`. A CAM operator taking a naive export gets six plated barrels with
mask openings, in the analogue zone, tying the bodies of the three **touch-proof** EMG
sockets to the analogue reference pour. It is a silent defect: the boards look right and
fail leakage.
**Now:** non-plated pads carry no copper and no mask on any of the four layers, and both they
and the four M3 holes are supplied in a separate `-NPTH.drl` file. The fabrication drawing
calls them out.
**Verified:** the simulator checks that the non-plated hole count matches the design and that
no hole appears in both drill files.
**Impact:** footprint definitions, drill output, one fabrication note.
**Part status:** the J15–J17 socket itself is **open**. `design.py` names Stäubli SLB1,5-F as
a class, not a confirmed PCB part; a touch-proof 1.5 mm socket with a PCB-mount signal pin
and two 1.5 mm retention posts must be sourced and first-articled before Phase 2, and
AVL-EEG-017 carries a 12-week lead-time risk against it.

### ECO-EEG-013 -- the analogue module connectors could not be escaped

**Class:** blocking. **Found by:** the router failing to reach the inner row.
**Was:** J2 and J4 were 2×10 sockets carrying twenty analogue nets between them. With no
vias permitted under the module outline, the inner row of a 2×10 has no route out: the outer
row's pads block the only direction, and going round the connector needs a corridor wider
than the board provides.
**Now:** each is split into a 1×10 analogue-signal socket (J2, J4) and a 1×6 rail socket
(J23, J29). Every analogue signal pin now escapes sideways on L1.
**Verified:** every analogue signal pin on J2, J4, J23 and J29 has a route out on L1 in the
released routing. What this ECO closes is that the escape is now geometrically possible,
which it was not with two 2×10 sockets; it is not a statement about the board as a whole. The
full routing result -- which now closes, at zero violations and 145 of 145 nets -- is stated
once, in ECO-EEG-018, and `kicad/EEG-CAR-01_RevB_DRC_report.txt` is the authority for it.
**Impact:** four connectors instead of two, a change to the jumper schedule in ICD-EEG-006.
**Note on the move to four layers.** Going to four layers does not restore the 2×10 option.
Vias are still not permitted under a module outline, so the inner row still has no escape,
and the split stands.

### ECO-EEG-014 -- the light lines ran through the electrode harness

**Class:** major. **Found by:** the router, which could not get eight digital lines from
x = 5 mm to the shift register without crossing the whole analogue zone.
**Was:** one 22-way harness socket at the far left of the analogue zone carried **twelve
electrode conductors -- eleven electrode signals and one drain -- and ten contact-light
conductors, LED1 to LED8 plus LED_V and LED_GND**. DSN-EEG-003 Rev A.2 recorded this as
finding 10 and **accepted** it on the grounds that the lights are dark during recording.
That was the wrong call: it forces eight digital conductors to run the full width of the
analogue zone on the board as well as sharing a cable with eight high-impedance electrode
leads.
**Now:** two cables and two sockets. A 12-way screened electrode bundle at J14 in the
analogue zone, and a 10-way light ribbon at J30 in the digital zone next to the shift
register. Conductor count is unchanged at twenty-two; the crossing is gone.
**Verified:** the DRC checks that no digital net enters the analogue zone and the simulator
checks that no digital net shares the electrode harness. Both results are clean in the
released routing: the DRC report records **zero zone crossings**, so no digital net enters
the analogue zone. The rest of the routing result, including what is still open in it, is
stated once in ECO-EEG-018.
**Impact:** two harness assemblies instead of one (WH-EEG-008), one extra connector, a
change to the helmet cable routing in DSN-EEG-002.

### ECO-EEG-015 -- part identifiers meant two different things

**Class:** major, documentation. **Found by:** cross-document audit.
**Was:** `HM-xx` was used both as a figure label and as a part number in DSN-EEG-002, and the
two namespaces collided. **HM-07 named the boom microphone arm in DSN-EEG-002 section 10 and
the battery hatch in DSN-EEG-003 section 4, in the STL set, in the kit BOM and in the RFQ
scope.** A manufacturer printing "HM-07" produced a different part depending on which
document was open, and the real boom arm and pod hatch had no file under their own
identifiers. Section 10 also requires the part ID to be engraved in the model, so the wrong
identifier would have been moulded into the part.
**Now:** PARTS-EEG-019 is the single register. Figures are `FIG-nn`; `HM-xx` is reserved for
parts; the battery hatch is `HM-08` and its file is `HM-08_battery_hatch.stl`. A migration
table maps every v1 filename to its v2 identifier.
**Impact:** one file rename, four documents, the kit BOM and the RFQ scope line.
**Extended in Rev B:** the same failure had been reproduced in the **document** namespace.
Section 1.3 of this document closes it.

### ECO-EEG-017 -- lithium shipping was never mentioned

**Class:** major, compliance. **Was:** every kit contains an 18650 cell and is posted to a
participant and back. Package v1 said nothing about UN3481, packing instruction PI967, state
of charge, marking or carrier documentation.
**Now:** RFQ S-09 is new, REG-EEG-012 section 3 states the obligation and PKG-EEG-015
section 7 gives the procedure for both the outbound and the return leg. The procedure has
one home, in PKG-EEG-015 section 7; REG-EEG-012 cites it and does not restate it.
**Verified:** the packing list and the shipping label set are checked against PI967 in
PKG-EEG-015 section 7.
**Impact:** one new requirement, two documents, the outer carton artwork, and a carrier
declaration per shipment.

### ECO-EEG-018 -- the routing is now supplied, and what doing it found

**Class:** scope, and it carries two blocking findings.
**Renumbered:** this change was ECO-EEG-016 in package v2 Rev A, which is also this
document's number. Cite it as **ECO-EEG-018**. RUL-EEG-021 section B rules the numbering and
RUL-EEG-021 section A rules that the board size and the layer count are findings of this
work rather than changes in their own right; both are recorded below. The numbers
ECO-EEG-028 and ECO-EEG-029, which a Rev B draft briefly used for them, are withdrawn.
**Was:** RFQ-EEG-002A asked a bidder to route the carrier.
**Now:** the routing is supplied, on four layers, and RFQ-EEG-002A becomes a **review** of
it. The routing was produced by the programme's own constraint-aware router and **has not
been reviewed by a human layout engineer**; the DRC report lists every connection the router
had to relax, so a reviewer can go straight to the tight places. The board did not close when
this ECO was first written -- 122 of 145 nets, 25 violations -- and it closes now; **section
2B records what was changed to close it** and is where the before-and-after belongs.

**The routed result.** This is the one home for the figures; every other document cites this
paragraph or the report behind it, `kicad/EEG-CAR-01_RevB_DRC_report.txt`, which is the
authority. If the two ever differ, the report is right.

| Measured | Value | Against |
|---|---|---|
| Board | 150.0 × 130.0 mm, four layers | -- |
| Track segments | 3 745 | -- |
| Through vias | 552 | no blind, buried or filled vias |
| Reference planes | one continuous island per net, on both inner layers | the star-point rule of DSN-EEG-003 section 3.3 |
| Smallest clearance, L1 | 0.260 mm | 0.20 mm rule |
| Smallest clearance, the planes | 0.285 mm | 0.20 mm rule |
| Smallest clearance, L4 | 0.275 mm | 0.20 mm rule |
| Narrowest conductor | 0.20 mm | 0.20 mm minimum |
| Connections the router had to relax | **169** -- 36 narrower than the 0.25 mm preferred width, 133 at full width with a reduced gap | every one at or above the 0.20 mm minimum conductor and gap |
| Smallest plated hole | 0.30 mm | 0.30 mm rule |
| Digital nets in the analogue zone | zero zone crossings | none permitted |
| AGND_REF-to-DGND bridges | exactly one, at R90 | exactly one |
| HARN_SHIELD-to-DGND bridges | exactly one, at R91 | exactly one |
| Duplicate copper | zero segments, zero via positions | none |
| Nets fully connected | **145 of 145**, none without copper | 145 |
| **Violations** | **0** | zero to release fabrication data |

**Nothing in the rule set is breached.** The report's own line is "VIOLATIONS: 0 -- none.
The board passes every rule listed above": no clearance violation -- the two vias that sat
0.328 mm from an electrode net are gone -- and no width, annular-ring, hole-size, board-edge,
non-plated-hole, isolation keep-out or via keep-out violation. The isolation keep-out is
worth naming, because an earlier routing put inner-plane copper inside it: **the strip at
x ≥ 141 mm is now free of copper on all four layers, and the report says so.** It is free
because the keep-out is now enforced against copper edges rather than track centrelines
(section 2B). That is the only ground on which the sentence may be repeated. Anyone about to
write it in another document reads the report first.

**What that does not settle.** The board passes every rule it was given, on 169 connections
by taking the tightest geometry those rules allow. **A board that closes at minimum geometry
is not the same board as one that closes at preferred geometry, even when every rule passes**;
the previous route relaxed 19 connections and this one relaxes 169. Nothing on this board has
been manufactured or measured, and no human layout engineer has read the routing.

**The gate of section 3 is therefore met and the fabrication data in `kicad/` is RELEASED FOR
REVIEW under RFQ-EEG-002A. It is NOT RELEASED FOR FABRICATION**, and what holds it back is
now the review rather than the report: no human layout engineer has read this routing.
Reviewing the whole
routing -- the 169 relaxed connections first -- correcting what is wrong and signing it off is
the scope of RFQ-EEG-002A. No document in this package may say that the fabrication data is
released for fabrication, or that boards may be ordered from it, before that review closes,
and no document may state a DRC result without reading the report first, which is
RUL-EEG-021 section C ruling 4 applied to the layout.

**Verified:** `tools/emit_all.py` regenerates the board, the pours and the DRC report from
`design.py` on every run, and `tools/simulate_production.py` writes SIM-EEG-018. The
simulation run that Rev B pointed at predated the routing close and still carried the DRC
violations as an open item. **Corrected 2 September 2026: the run behind this release is
later than the close** -- 193 passed, 0 failed, 6 open -- **and carries no DRC item at all**,
because the report records no violations.
**Impact:** RFQ section 1.1, section 8, the pricing template, and the covering email.

#### ECO-EEG-018, first finding -- the carrier would not close at 130 × 124 mm

**Class:** blocking. **Found by:** doing the layout. The router could not close the board at
the package v1 size.
**Was:** the carrier was specified as **130.0 × 124.0 mm**. Package v1 asserted that size and
never routed it. Thirty connectors, 211 parts and 156 nets do not fit: the escape corridors
around the module sockets, the 6 mm mounting keep-outs, the isolation keep-out at the right
edge and the 0.35 mm electrode-net clearance together leave no channel wide enough to get the
analogue zone out to the converters.
**Now:** the carrier is **150.0 × 130.0 mm**. The extra 33.8 cm² of bare board costs a few euro
per unit at these quantities, against a real risk of an unroutable design; that is not a
close trade. Everything dimensioned from the outline moves with it: mounting holes to
(5, 5), (145, 5), (5, 125), (145, 125); the zone split to **x = 62 mm**, analogue left and
digital right; the isolation keep-out to **x ≥ 141 mm, y = 2 to 22 mm**, no copper on any
layer.
**The enclosure grew with the board:** POD-P1 base **163.0 × 143.0 × 58.0 mm external and
158.0 × 138.0 × 55.5 mm internal** with 2.5 mm walls and a 1.6 × 1.2 mm gasket groove; POD-P1
lid **163.0 × 143.0 × 6.0 mm** with a 2.0 mm spigot; MP-01 module plate **146.0 × 126.0 ×
3.0 mm** with an 8 mm solid border, a field of **12 × 3 mm jumper slots on a 16 × 7 mm
grid**, Ø2.7 mm M2.5 fixing holes between the slot rows and one 31 × 61 mm opening over the
DevKit. The slot figure is a size, not a count: `mech_gen.py` cuts each slot with
`.slot2D(12.0, 3.0, 0)`. The stack budget is floor 2.5 + boss 6.0 + carrier 1.6 + standoff
18.0 + plate 3.0 + modules ≤ 18.0 = **49.1 mm against 55.5 mm internal, a margin of 6.4 mm**.
**Verified:** `design.py` `BOARD_W` and `BOARD_H`, the fabrication drawing note 1, the DRC
outline and keep-out checks, and `mech_gen.py` for every printed part.
**Impact:** the board specification in DSN-EEG-003 section 3.2, every mechanical dimension in
ICD-EEG-006 section 4, PARTS-EEG-019 sections 2.2 and 2.4, the MECH-EEG-020 drawing set, the
foam schedule in PKG-EEG-015, the bare-board price, and the Phase 2 helmet shell, which was
sized for a carrier that no longer exists and is recorded as such in RFQ M-01.
**Consequence for the standoff argument:** the slant path from carrier copper, over the edge
of the isolation keep-out and up the 18 mm standoff to any host-side conductor on MP-01 is
≥ 18 mm, more than twice the 8 mm the safety case asks for. RISK-EEG-011 SR-08 is closed by
that, and the claim in Rev A that the standoff is not dimensioned is withdrawn.

#### ECO-EEG-018, second finding -- two layers cannot carry both the routing and the reference

**Class:** blocking. **Found by:** doing the layout. This is the single most important thing
package v2 learned by doing the work instead of asserting it.
**Was:** **two layers, F.Cu and B.Cu.** Package v1's architecture argument was that a
two-layer carrier is cheap and easy to route, and package v2 Rev A repeated it. Actually
laying the board out showed that it is not true. On two layers the bottom side has to be both
the continuous reference plane and the second routing surface, and it cannot be both: every
track routed on the bottom cuts the pour that the analogue traces above it are referenced to.
What comes out is a swiss-cheesed pour with return currents taking whatever path is left,
which is precisely what DSN-EEG-002 section 13's "layout rules that are requirements, not
preferences" forbids. The zoning, star-point and isolation rules that the same layout has to
satisfy are DSN-EEG-003 section 3.3.
**Now:** **four layers -- L1 signal, L2 reference plane, L3 reference plane, L4 signal.**
That gives two full routing surfaces **and** a continuous reference under every analogue
trace. The reference planes are split the same way on both inner layers: **AGND_REF left of
x = 62 mm and DGND right of it, on both L2 and L3**, tied together by stitching vias, with
AGND_REF joining DGND at R90 only and HARN_SHIELD joining DGND at R91 only.
**Stack-up:** mask / 35 µm L1 / prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 /
prepreg 0.200 / 35 µm L4 / mask = **1.60 mm ± 10 %**, FR-4 with Tg ≥ 150 °C, outer copper
1 oz and inner copper 0.5 oz.
**Vias: through vias only.** No blind, buried, back-drilled, filled or plugged vias, at
**0.60 mm pad on a 0.30 mm finished hole** with a 0.15 mm annular ring, tented both sides.
The smaller via than package v1's 0.80/0.40 is what makes the escape corridors fit; through
vias only is what keeps the board a class 2 commodity four-layer job rather than an HDI one.
**Cost:** at 2 units a four-layer board is about €35 more in total; at 50 units it is about
€3 per board. For a sixteen-channel EEG front end that is the right trade, and it is a real
answer to package v1's cost argument rather than a refusal of it.
**Verified:** `design.py` fabrication note 2 and the layer map in
`kicad/gerber/README_layer_map_and_checksums.txt`; the pour and stitching checks in the DRC
report, which records each reference plane as one continuous island per net; the layer count
and stack-up on the fabrication drawing. The counts are in the routing-result table above.
**Impact:** the board specification in DSN-EEG-003 section 3.2, the Gerber layer map and the
checksum file, the fabrication drawing, the IPC-6012 class 2 / IPC-A-600 class 2 fabrication
scope, the bare-board price line in the RFQ pricing template, the electrical-test netlist,
and the argument in DSN-EEG-003 section 2 that package v1 made for two layers, which is
withdrawn.

### ECO-EEG-019 -- C1–C16 carried an X7R part number under a C0G requirement

**Class:** major. **Found by:** cross-document audit, reading the Murata dielectric code in
the part number against the requirement in the same table.
**Was:** every document demanded C0G for the electrode-input capacitors and TST-EEG-004 T00
made X7R a hard reject, but the named part was `GCM188R71H103KA37D`, whose `R7` code is X7R.
A buyer running the AVL-EEG-017 section 8 checklist line "the order does not contain the word
X7R against that line" could not execute it, because the part number itself is an X7R part.
The same defect appeared at C21/C41/C61, named as "100 nF C0G 50 V" against
`GCM188R71H104KA57D`, also X7R.
**Now:** C1–C16 are **`Murata GCM1885C1H103JA16D`**, 10 nF, C0G, 50 V, 0603.

**Corrected 2 September 2026, and the correction changes the answer for C21/C41/C61.** Rev B
recorded that there was no fix of that kind for the Sallen-Key capacitors, because **a 100 nF
C0G in 0603 at 50 V is not a stocked part**, and specified them as **X7R with a stated
±15 % capacitance tolerance over the operating range**, `Murata GCM188R71E104KA57D`, with
the C0G requirement holding at C1–C16 and **deliberately not met** at C21/C41/C61. That
stood for one day. The fix was to stop asking for 100 nF: scale the capacitors down by ten
and the resistors up by ten, and f₀ and Q land where they were on parts that exist.
**C21/C41/C61 are now 10 nF C0G -- the same `GCM1885C1H103JA16D` this board already buys
sixteen of -- C22/C42/C62 are 22 nF C0G `GCM1885C1H223JA16D`, and R25/R26, R45/R46 and
R65/R66 are 215 kΩ.** Same 0603 footprints, same nets, no new purchasing line, and the
board does not move: it is a BOM change. The only X7R parts left in the envelope channels
are C23/C43/C63 and C24/C44/C64, the AVDD and AVSS decoupling at U1–U3, where the
dielectric is not an E-11 question; `design.py` carries them as "100n X7R 25V",
`GCM188R71E104KA57D`, whose `E` code is the 25 V the value string states.

**Withdrawn on 2 September 2026: the sentence "and the Sallen-Key corner tolerance in
TST-EEG-004 is widened to match".** It described a test limit that did not exist. Before
T12e was written there was no f₀ limit in TST-EEG-004 to widen, so nothing was widened and
the requirement was not made met by this change; TST-EEG-004 section 16 item 16 says so
against this ECO by name. What was true was narrower and worse: **T12e measures and records
f₀ per unit against 42 to 58 Hz, which was the band the fitted X7R parts could hold and is
wider than RFQ E-11's 50 Hz ±10 %**, so E-11's low-pass half was **not met with the approved
parts** and no widened E-11 limit existed to appeal to. Either E-11 had to be restated to
that band or a stocked C0G part had to be qualified; at the time neither had been done, and
it was carried as RFQ-EEG-001 Rev E section 12 item 15 and TST-EEG-004 section 16 item 16. A dielectric substitution that
a test limit is said to accommodate is a substitution nobody has to argue for, which is why
the sentence is withdrawn here rather than quietly reworded.

**Superseded later the same day: the second of those two alternatives was taken.** A stocked
C0G part was qualified -- the 10 nF the board already buys -- and the network was rescaled
around it, so **E-11's 50 Hz ± 10 % low-pass half is met in the design**: `design.py`
computes f₀ = **49.9 Hz** with Q = 0.742 unchanged, and C0G's ± 5 % with no temperature
coefficient holds the corner inside **47.6 to 52.6 Hz** against a 45 to 55 Hz band, where the
X7R network ranged 42.4 to 57.4 Hz and no build of it could have been held inside. **The
withdrawal above stands and is not softened by this**: no test limit was ever widened, and
what closed E-11 was changing the parts, not the limit. T12e's 42 to 58 Hz band was set
around the X7R spread and is now wider than the fitted parts need; whether TST-EEG-004
restates it is TST-EEG-004's, and this register does not restate a limit it does not own.
E-11 is met **in the design**: nothing has been built and no corner has been measured.

**Verified:** the part numbers are in `design.py` and flow to the BOM and the CPL through
`emit_all.py`; AVL-EEG-017 section 1.2 and QP-EEG-010 section 2.3 carry the same numbers.
**Impact:** two AVL lines, the incoming-inspection check, and the BOM. **No test limit was
widened by this change**; T12e's 42 to 58 Hz band is set by TST-EEG-004 and is a measurement
recorded per unit, not an acceptance of E-11.

### ECO-EEG-020 -- the board had no fiducials

**Class:** minor. **Found by:** assembly review. ASM-EEG-007 section 2.2 recorded that
`design.py` placed no fiducial footprints and proposed a two-point vision teach on the plated
pads of TP14 and TP10, priced by the manufacturer.
**Was:** no global fiducial anywhere on the board. Teaching a placement machine on test-point
pads is slower, less repeatable and a per-lot cost for no reason.
**Now:** **three 1.0 mm round copper fiducials with 3.0 mm mask openings**, FID1 to FID3, at
**(12.0, 10.0), (144.0, 100.0) and (12.0, 120.0)** in `design.py`. The vision-teach workaround
is withdrawn. **RUL-EEG-021 section B** now carries the same three positions. Its first
issue transcribed them as (8, 8), (142, 8) and (8, 122); that error is corrected in the
register, and under section 1.4 `design.py` governs in any case. RUL-EEG-021 is a controlled document at Rev A and is registered in section 1.1; the
`tools/RULINGS.md` worksheet it grew out of is not cited.
**Verified:** the footprints are in the placement file and the fiducial layer of the assembly
drawing.
**Impact:** three footprints, one assembly-drawing note, and one deleted paragraph in
ASM-EEG-007. Panel fiducials remain the fabricator's choice.

### ECO-EEG-021 -- the I²C bus had no pull-ups on the carrier

**Class:** major. **Found by:** ICD-EEG-006 section 8 open point 1.
**Was:** SDA and SCL reach J6/J7, J8, J11 and J12 and there was **no pull-up resistor
anywhere in `design.py`**. The bus depended entirely on whatever pull-ups the purchased
modules happened to carry, which is not a design: it changes when a module is substituted,
it is not on any drawing, and there is no test that would catch its absence.
**Now:** **R94 and R95, 4.7 kΩ 1 %, from SDA and SCL to DVDD3V3**, in the digital zone at
(132, 26) and (132, 30).
**Verified:** SCH-EEG-005 sheet 5; the nets are one island each in the connectivity check.
**Impact:** two new passives, two AVL lines, one build instruction, and an I²C bus scan in
the production test.

### ECO-EEG-022 -- VBUS_DET did not reach a guaranteed logic high

**Class:** major. **Found by:** ICD-EEG-006 section 8 open point 2 and TST-EEG-004 T21,
which recorded the defect and dispositioned it as "design escalation, not rework". No ECO
had been raised against it, so it would have gone to fabrication.
**Was:** R84 = 100 kΩ and R85 = 56 kΩ gives 5 × 56 / 156 = **1.79 V** at VBUS = 5.00 V,
against a guaranteed V_IH of 2.48 V on a 3.3 V ESP32-S3 input. **The first of the two S-01
charge interlocks would not have asserted reliably.**
**Now:** **R85 changes from 56 kΩ to 150 kΩ**, `Vishay CRCW0603150KFKEA`, giving
5 × 150 / 250 = **3.00 V**, comfortably above V_IH. R84 is unchanged at 100 kΩ.
**Verified:** the value is in `design.py`; TST-EEG-004 T21's limit band is restated around
3.00 V; the interlock itself is tested end to end.
**Impact:** one resistor value, one AVL line, one test limit band.

### ECO-EEG-023 -- ENV_CMP swings ±2.5 V into a 3.3 V pin

**Class:** major. **Status: OPEN. This change is specified and is NOT implemented in
`design.py`, so the defect it describes is still in the design as released.**
**Found by:** cross-document audit of the comparator supply nets against the GPIO it drives.
**Is:** U7, a TLV3201, is powered from **AVDD (+2.5 V) and AVSS (−2.5 V)** and its output
`CMP_RAW` therefore swings ±2.5 V. It reaches GPIO3 through R83 (10 kΩ) and the D23 BAV99
clamp to DGND and DVDD3V3, so **the clamp is the only thing between a −2.5 V output and a
3.3 V input**, and the logic-high margin is set by the clamp rather than by design.
**Proposed:** power U7 from **DVDD3V3 and DGND** so that the output swings 0 to 3.3 V into
GPIO3 with full margin and D23 becomes a belt-and-braces part. The comparator's inputs cannot
simply follow: AGND_REF sits 2.5 V above DGND, so the inputs must be **re-referenced to a
DVDD3V3/2 divider with the envelope AC-coupled into it**. The TLV3201 has a rail-to-rail
input stage that reaches its negative rail, so the topology works, but it moves a signal
across the analogue-to-digital reference boundary.
**Why it is open:** this is a change to a circuit that straddles the reference split, and
**the safety and layout reviewer must check it before it is cut in.** Implementing it
silently would defeat the review.
**Impact if implemented:** two U7 supply pins, a new divider, one new capacitor, a change to
the star-point argument in DSN-EEG-003 section 3.3, and a re-issue of RISK-EEG-011.

### ECO-EEG-024 -- S-02's single-fault DC limit is not met

**Class:** blocking for Phase 2. **Status: IMPLEMENTED 2 September 2026.** Rev B carried this
ECO as OPEN and not implemented, with 47 kΩ fitted and S-02 not met at 53.2 µA against a
50 µA limit. `design.py` now fits **68 kΩ at R1–R16** and the calculated single-fault DC
patient auxiliary current is **36.8 µA. S-02 is met in the design and is not signed off** --
see below.
**Found by:** the patient-current budget in RISK-EEG-011 section 4.5, reached independently
by WH-EEG-008 section 5.5 and JIG-EEG-009 section 4.3.
**Was:** with R1–R16 at 47 kΩ, the single-fault DC patient auxiliary current is calculated at
**53.2 µA against the 50 µA of S-02, which is a 6.4 % overrun and a failure.** RISK-EEG-011
classes it Critical.
**Now:** R1–R16 are **68 kΩ**, `68k 0.1% 25ppm`, `Vishay TNPW060368K0BEEA`. That gives
2.5 V / 68 kΩ = **36.8 µA**, keeps the input corner at 234 Hz, which is −0.75 dB at 100 Hz,
and raises Johnson noise to 0.28 µV for a total of 0.31 µV, still well inside E-03. **RFQ
E-10 moves to its ±1.0 dB at 100 Hz branch**, which the requirement already states for
exactly this case and which is now the live branch because the 68 kΩ is what is fitted; the
±0.5 dB branch belonged to the 47 kΩ build and is history. Same footprint, same nets, same
pad count: the board does not move.
**Why it was open, and why that reasoning is withdrawn:** Rev B held the change back so that
the two prototypes could be built with 47 kΩ and the current **measured rather than
calculated** before Phase 2. That left a 6.4 % overshoot on a **safety** limit standing in
the released design through three revisions in order to measure the failing state, when the
series resistor is the one component in the patient path whose value can be changed without
moving anything else. The measurement does not go away: it changes from measuring a known
failure to confirming a calculated pass.
**What implementing it did NOT close.** The safety review. **RISK-EEG-011 SR-01 is closed in
the design and unsigned**; the electrical safety reviewer of RISK-EEG-011 section 7 owns it
and that review has not started, which is open item 6 of the simulation run of 2 September
2026. Nothing has been built and nothing has been measured: **36.8 µA is a calculation,
exactly as the 53.2 µA before it was.** "Met in the design" is what may be written; "met" on
its own, and "signed off", may not.
**Verified:** the value is in `design.py` and flows to the BOM and the CPL through
`emit_all.py`; `tools/simulate_production.py` recomputes the single-fault current from it.
TST-EEG-004's patient auxiliary current step, on FIX-04, measures it on the first unit.
**Impact:** sixteen resistor values, the live branch of RFQ E-10, one AVL line, the noise
budget in RISK-EEG-011 section 4, and a re-issue of RISK-EEG-011.

### ECO-EEG-025 -- F-06's three-minute ring buffer does not fit the PSRAM

**Class:** major. **Found by:** FW-EEG-001 section 5.8, where the allocation returns NULL.
**Was:** RFQ F-06 asked for a ring buffer of at least three minutes at 1000 Hz and put the
figure at "≈12 MB in PSRAM". The mandated module is the ESP32-S3-DevKitC-1-**N16R8**, which
is not substitutable under E-18 and has **8 MiB** of PSRAM. Three minutes is 9.13 MB and
`main.c` asked for 12 MiB, so **the requirement could not be met on the mandated part** and
the request failed at run time. ECO-EEG-009 also cited the 12 MB figure in its justification
and is corrected above.
**Now:** the ring is **6 MiB, which is 126 seconds of raw samples at 1000 Hz (124 s framed)**, and **RFQ F-06 is relaxed to
90 seconds of ring plus unlimited backfill from the microSD copy.** The ring covers a
transport dropout; anything longer is recovered from the card, which holds the byte-identical
frame stream. The 90-second figure is the requirement and 126 seconds is the fitted margin.
**Verified:** the constant is in the firmware build and reported in the STATUS frame;
TST-EEG-004's dropout-and-recovery step exercises the backfill, not just the ring.
**Impact:** one RFQ requirement, one firmware constant, the IFU sentence that told the
participant the instrument keeps three minutes, and the test step that checked it.

### ECO-EEG-026 -- E-04's crosstalk limit is neither achievable nor measurable

**Class:** major. **Found by:** ICD-EEG-006 section 3.2 and raised at ICD-EEG-006 section 8
item 7 without ever reaching the RFQ.
**Was:** RFQ E-04 asked for **−100 dB** channel-to-channel crosstalk. That is not achievable
through a 60 mm un-interleaved ribbon, and it is about 40 dB below this instrument's own
noise floor, so **it is not measurable on this hardware either**. TST-EEG-004 T9a
nevertheless tested to −100 dB with 6.2 dB of detection-floor margin, and measured only the
carrier.
**Now:** E-04 is restated as **−80 dB at 50 Hz, measured on the carrier**, with the ribbon's
contribution characterised once on the first prototype and recorded rather than tested per
unit. The restatement is honest about what the instrument can see: a limit that cannot be
measured is not a limit.
**Verified:** TST-EEG-004's crosstalk step is rewritten to the −80 dB carrier measurement and
JIG-EEG-009's detection-floor calculation is restated against it.
**Impact:** one RFQ requirement, one test step, one fixture note, and one characterisation
report on the first prototype.

### ECO-EEG-027 -- the envelope AC-coupling corner removed the envelope

**Class:** major. **Found by:** ICD-EEG-006 section 8 item 4, computing the corner from the
fitted values.
**Was:** C20/C40/C60 were **1 µF** into R20/R40/R60 at 10 kΩ, which is a **15.9 Hz** corner,
not the 0.1 Hz of RFQ E-11. `design.py`'s own descriptive text claimed 0.1 Hz and
AVL-EEG-017 listed the part as "1 µF … 0.1 Hz corner". For the envelope of a speech signal
15.9 Hz is not merely the wrong number, it is the wrong side of the signal: **it removes the
envelope the stage exists to pass.**
**Now:** **C20/C40/C60 change from 1 µF to 10 µF**, `Murata GRM188R61C106MA73D`, with
R20/R40/R60 unchanged at 10 kΩ, giving a **1.6 Hz** corner. **RFQ E-11's AC-coupling clause
is restated as ≤ 2 Hz**, because 0.1 Hz into 10 kΩ needs 160 µF, which is not a 0603 part and
buys nothing for a speech envelope.
**Verified:** the values are in `design.py`; the corner is computed in
`simulate_production.py` station 9; TST-EEG-004 measures it and the deviation note that
recorded 15.9 Hz is deleted.
**Impact:** three capacitor values, one AVL line, one RFQ requirement, one test limit, and
one corrected description in `design.py`.

### 2.2 Requirement changes and where they come from

Every RFQ-EEG-001 requirement that changed between Rev C and this release, with the change
that caused it. The requirement text lives in RFQ-EEG-001; this table is the index, not a
restatement.

| Requirement | Change | Source |
|---|---|---|
| E-04 | crosstalk restated from −100 dB to −80 dB at 50 Hz, measured on the carrier | ECO-EEG-026 |
| E-10 | **±1.0 dB at 100 Hz.** That is the branch E-10 already carried for this case, and it became the live one on 2 September 2026 when ECO-EEG-024 was implemented and R1–R16 went to 68 kΩ. The ±0.5 dB branch belonged to the 47 kΩ build and is history, not an alternative | ECO-EEG-024, implemented |
| E-11 | AC-coupling corner restated from 0.1 Hz to ≤ 2 Hz, and **met** at a calculated 1.6 Hz. The 50 Hz ± 10 % low-pass is **unchanged and, since 2 September 2026, met in the design**: the Sallen-Key moved X7R → C0G at 10 nF / 22 nF with 215 kΩ, giving f₀ = 49.9 Hz and a corner inside 47.6 to 52.6 Hz against the 45 to 55 Hz band. It was **not** met with the X7R parts, which ranged 42.4 to 57.4 Hz. Unchanged here still means not restated | ECO-EEG-027 for the AC coupling; the low-pass closed under ECO-EEG-019, 2 September 2026 |
| E-12 | raised from Should to Mandatory, because the comparator is now fitted | ECO-EEG-010 |
| E-18, E-20 | pin map and throughput wording; 50.7 kB/s of payload stated against the ≈70 kB/s allowance | ECO-EEG-009 |
| E-23 | rewritten as a separate charge-only receptacle, and the 45 °C charge inhibit restored to E-23 rather than cited from S-04 | ECO-EEG-003 |
| E-24 | **live non-conformance**: the named isolator module presents USB-B against a USB-C requirement; interim answer is the WH-09 panel pigtail | no ECO; open |
| E-26 | restated as a 6 mm tactile switch with a 12 mm coloured cap on an extender; panel openings 13.0 mm on a 14 mm pitch | correction, no ECO |
| E-27 | unchanged, and **met in the design since 2 September 2026**: the bicolour phase driver is written, alternating on the FreeRTOS tick at about 250 Hz against E-27's "above 100 Hz". No unit exists, so no light has ever been driven and T11 has not been run | ECO-EEG-001 |
| E-28 | restated as TP1–TP18 plus a 1×6 UART debug header at J26; the 2×5 1.27 mm JTAG/SWD header is **withdrawn** and every "E-28 deviation" note is deleted | correction, no ECO |
| E-29 | **new**: headphone output not to exceed 100 dB SPL at any commanded level on an artificial ear, with the codec volume register clamped at the calibrated value. Calculated full-scale output is about 110 dB SPL, which is why the requirement is needed. Added as a type test and to RISK-EEG-011 | new requirement, no ECO |
| F-06 | ring relaxed from three minutes to 90 seconds plus unlimited microSD backfill | ECO-EEG-025 |
| S-02 | unchanged, and **met in the design since 2 September 2026** at a calculated 36.8 µA against 50 µA, R1–R16 having gone to 68 kΩ. Not signed off: RISK-EEG-011 SR-01 is closed in the design and the safety review has not started | ECO-EEG-024, implemented |
| S-04 | unchanged, and **not met**: no NTC net and no thermistor way exists | no ECO; open hardware item |
| S-09 | **new**: lithium shipping under UN3481 and PI967 | ECO-EEG-017 |
| A-03 | headband **withdrawn** as a kit item and rewritten to cover the HM-06 chin strap and the HM-03 occipital yoke, both on the frame | correction, no ECO |
| M-01 | POD-P1 enlarged to 163 × 143 × 58 mm external; the Phase 2 helmet-shell figures are sized for a carrier that no longer exists | ECO-EEG-018, first finding |
| M-02 | LED opening **withdrawn**: all eight lights are in the helmet and the pod carries no indicator | correction, no ECO |

### 2.3 Foreseen and not raised

Two things are known, are not defects today, and would become ECOs if a measurement goes the
wrong way. They are listed here so that they are not discovered as surprises.

1. **The DevKit 3V3 rail.** The carrier draws a calculated 288 mA worst case from the
   DevKit's on-board regulator, which dissipates about 0.5 W in a small package inside a
   closed pod. Phase 1 measures it at TST-EEG-004 T3 and reports the regulator case
   temperature. **If it exceeds 85 °C, a 3.3 V regulator on the carrier fed from V5V is an
   ECO against Rev C of the board.** It is not solved today; it is measured.
2. **Conformal coating.** The board is **not coated for Phases 1 and 2**, and that is a
   decision rather than a deferral: the board lives inside a gasketed enclosure, and coating
   a board with thirty connectors and a socketed DevKit costs more in masking than it buys.
   It is revisited before Phase 3 if a unit returns with corrosion.

---

## 2A. Corrections made by the third cross-document audit

A third pass, run after the second audit's corrections were applied, looked for one thing
only: a number, a citation or a claim in one document that a different document contradicts.
It found thirteen. **None of them is a design change** -- no schematic, netlist, layout,
firmware or mechanical part moves -- so none takes an ECO number. They are corrections, and
they are listed here so that anyone holding a printed copy can see what changed and why.

| # | What was wrong | Where | Now |
|---|---|---|---|
| C-01 | SIM-EEG-018 graded the DRC as a **pass** while its own evidence column read "25 violations", and the headline said "1 known open item" | `tools/simulate_production.py` | the check now asserts only that the violations are of the two known kinds, and the 25 are raised as an open item. **History, and true when this row was written: the headline was 169 passed, 0 failed, 5 open.** Superseded on 2 September 2026: the DRC reports zero violations, so the exception has nothing left to except and that open item is gone. The headline stood at 171 passed, 0 failed, 5 open when that sentence was written and **is 193 passed, 0 failed, 6 open at the run behind this release** -- section 1.1 states it and names the six, and this row is not the place to read it from, which is the second time this row has had to be corrected for exactly the reason it warns about. A total written into a table as prose is a total that stops moving when the run does not; that is the second thing this row now guards. The first stands: a check that graded a DRC as a pass while its own evidence column read 25 violations is what it was raised against |
| C-02 | Two different byte rates were both called "the stream": 50.0 kB/s in SIM, 50.7 kB/s everywhere else | SIM-EEG-018 | both are reported, named: **50.0 kB/s of raw sample payload**, **50.7 kB/s framed** (1014 bytes of frame, 1015 after COBS, every 20 ms) |
| C-03 | The ring buffer was **118 s** in seven documents, 126 s in two | RUL-EEG-021, RFQ-EEG-001, TST-EEG-004, DSN-EEG-003, AVL-EEG-017, ECO-EEG-016, IFU-EEG-014 | **126 s.** The 118 s divided 6 MB *decimal* by the *framed* rate; the ring is **6 MiB = 6,291,456 bytes** and it holds raw samples. 124 s if counted framed. RING_BYTES and the 90 s of F-06 are unchanged, so this is arithmetic recorded under ECO-EEG-025, not a new ECO |
| C-04 | Ten documents said "no clearance violation" while the same page reported two of them. The Rev B closure named six and corrected three | corrected at Rev B: PARTS-EEG-019, the PCB spec sheet, `README_package_index.txt`. Named at Rev B but left unqualified until now: TST-EEG-004, ASM-EEG-007, RFQ-EEG-001. Never in the Rev B scope and also unqualified: ICD-EEG-006, QP-EEG-010, REG-EEG-012, FW-EEG-001 | each of the ten was made to say *beyond those two electrode-net via clearances*, which is what the DRC report supported at the time. **Withdrawn on 2 September 2026:** those two vias are gone and the report records no clearance violation at all, so the qualifier is now itself wrong and the plain sentence is correct. What survives is the rule, not the wording -- no document states a DRC result it has not read in the report. The Rev B row was written as closed before three of the six it named had been edited; the scope is restated here rather than closed a second time. No automatic check guards the wording yet, so review holds it until one is added to `tools/simulate_production.py`; a copy of the sentence found without the qualifier is a reintroduction and is to be raised against this row |
| C-05 | SIM reported **156** surface-mount placements against 153 everywhere else | SIM-EEG-018 | **153 placed parts, of which R89 is do-not-populate; the CPL has 156 rows because it also carries the three fiducials**, which take copper and mask apertures but no paste |
| C-06 | The PCB spec sheet said TST-EEG-004 has **30** steps; TST-EEG-004 says thirty-one | `kicad/EEG-CAR-01_RevB_PCB_spec_sheet.txt` | **31 steps (T00, T0, T1 to T29)** |
| C-07 | RUL-EEG-021 printed the fiducials at (8, 8), (142, 8) and (8, 122), and three documents called that a transcription error while the register still carried it | RUL-EEG-021, DSN-EEG-003, ASM-EEG-007, QP-EEG-010 | the register carries **(12, 10), (144, 100) and (12, 120)**, matching `design.py` and the CPL, and the withdrawal is stated in the register itself |
| C-08 | RUL-EEG-021 listed the ECOs as 001–015, 017 and 018, omitting the nine issued since | RUL-EEG-021 | **001–015, 017, 018 and 019–027**, with **028 and 029 withdrawn** |
| C-09 | RUL-EEG-021 said the isolation keep-out is clear on "either layer" | RUL-EEG-021 | **all four layers** |
| C-10 | SIM graded **E-27** a pass on the light current alone, while ECO-EEG-016 and TST-EEG-004 T11 both record E-27 as not met | SIM-EEG-018 | the current check is retitled *current only*, and E-27's missing bicolour phase driver is an open item. **Superseded 2 September 2026:** the driver is written, so the open item is no longer the missing driver but *E-27 has never been seen to light* -- no unit exists and T11 has not been run. The split between a current check and a colour check is what this row bought, and it stands |
| C-11 | SIM graded **E-22** on a 150 mA board current that ICD-EEG-006 disputes at about 440 mA | SIM-EEG-018 | E-22 is checked at **both** figures -- 20.0 h and 6.8 h, so it is met either way -- and the unreconciled current is an open item, as RFQ-EEG-001 Rev E open item 14 |
| C-12 | The DRC report's "CONDUCTORS BELOW THE 0.25 mm PREFERRED WIDTH: 19" contained entries at 0.28 and 0.56 mm, and disagreed with the "200" under MEASURED | `tools/drc.py` | the section is **CONNECTIONS THE ROUTER HAD TO RELAX**, split into *narrower than 0.25 mm* and *full width with a reduced gap*, and it states that it counts connections while MEASURED counts segments. The counts move with the route: **169 as the board now stands, 36 and 133**, against 19 when this row was written |
| C-13 | Four citations pointed at things that do not exist: `firmware/pinmap_EEG-CAR-01.h` (twice), "DSN-EEG-003 Rev B section 5", "ASM-EEG-007 stage 2" for the reflow profile, and "FW-EEG-001 section 8" for F-08 | ICD-EEG-006, SIM-EEG-018 | `firmware/main/board_pins.h`, **Rev C** section 5, **ASM-EEG-007 section 2.5**, **FW-EEG-001 section 5.6**. The reflow figures now match ASM-EEG-007 section 2.5 exactly: 45–90 s above liquidus, 235–245 °C at the U1 body, 245 °C maximum anywhere |

### 2A.1 What package v1 had and package v2 had dropped

A fourth pass compared every file in `package/` against `package_v2.4/` by CONTENT, not by
name -- twenty-eight artefacts, including the four workbooks and the zip that sit beside
the package folder. Twenty-three were covered outright. Five were not, and all five were
cases of package v2 carrying a file forward in name while losing what was inside it. None
was noticed by any of the three earlier audits, because all three read package v2 against
itself and never opened package v1.

| # | What v1 had that v2 had lost | Severity | Now |
|---|---|---|---|
| C-14 | **The entire internal cost model.** `EEG_kit_BOM_INTERNAL_costed.xlsx` held an Assumptions sheet, 436 price cells across four quantity breaks, and a subsystem roll-up. `EEG_kit_BOM_INTERNAL_RevB_costed.xlsx` was a copy of the *bidders'* workbook with two renamed columns and **zero numeric price cells** -- it even carried the bidders' footer, "no prices are given in this file by design" | **major** | Rebuilt as `EEG_kit_BOM_INTERNAL_RevC_costed.xlsx` from `tools/emit_costed_bom.py`, on v2's 47-line part list, with the Assumptions sheet, per-line prices at 2/10/25/50, a per-line **price basis** column, the subsystem roll-up, the programme build-up with spares and NRE, and a v1-versus-v2 comparison. The empty Rev B file is deleted |
| C-15 | **The mirrored solder-side view.** v1 shipped `EEG-CAR-01_placement_bottom.pdf`. v2's assembly drawing had a "bottom side" sheet, but it used the *same* transform as the top sheet, so it was the top view with a different title and every left-right instruction on it was wrong | **major** | `tools/drawings.py` gained a `mirror` transform. ASM 2 of 2 is now drawn as seen from underneath and says so on its face. This matters because ASM-EEG-007 §2.7 solders 217 socket-strip, 4 JST, 12 switch and 3 DIN joints from the bottom, and QP-EEG-010 IQC-B10 inspects against the sheet |
| C-16 | **The nine manufacturers' replies**, and with them the only commercial evidence either package holds: Makerfabs' blank-sheet ODM quotation of **US$20-30k for Phase 1 design plus two samples** | minor | Restored as DSN-EEG-003 §8.1, with the arithmetic that makes it matter: a blank-sheet engagement is four to seven times the whole of Phase 1 at the two-unit break, which is *why* the instrument is module-on-carrier |
| C-17 | **The RFQ cover email**, RFQ-EEG-001 Rev C Annex A -- the only text in the package written for a reader who has opened nothing yet | minor | Restored as RFQ-EEG-001 Rev E **Annex A**, updated: four layers not two, and routing supplied not requested. It stated the twenty-five open items in the letter rather than leaving them to be discovered after quoting; since 2 September 2026 what it must state instead is that the data is released for review and not for fabrication, and that the routing is unreviewed. The reference-document list moves to **Annex B** |
| C-18 | **Every foam corner radius.** v1 specified sheet R14, HELMET R40, HEADPHONES/ELECTRODES R10 and the small pockets R8. Both v2 DXFs drew every profile square, and no document stated a radius | minor | `tools/mech_gen.py` draws true arcs at v1's radii. PKG-EEG-015 §2.3 orders a steel-rule die for Phase 3, and steel rule cannot be folded to a true 90 degree inside corner -- a square profile either tears the foam or silently becomes whatever radius the die maker picks |

Three findings raised by the same pass were **refuted** on re-check and are recorded here so
they are not raised a fourth time: the netlist report's two USB route rules (the geometry
survives in v2 rule 6 and the stub prohibition in RFQ F-12), the Ø104 mm circle in v1's foam
top layer (a helmet dome relief made unnecessary by the two-layer split), and the three
cover-email variants of v1's Annex A (carried by DSN-EEG-003 Annex B's conditional wording).

**The lesson is the one C-01 to C-13 already taught, applied to a different axis.** Those
thirteen were package v2 contradicting itself. These five are package v2 contradicting
package v1 -- a file kept by name and emptied of content. A name-by-name diff finds none of
them; only opening both files does.

---

Two further corrections were made at the same time and are not numbered above because they
close a finding rather than resolve a contradiction: **FW-D15** is marked closed, because the
header it complained about now reads RFQ-EEG-001 Rev E; and SIM-EEG-018's manual-handling note
now states the two-to-three-minute fitting time as IFU-EEG-014 does -- *once the participant
has done it once*, with five minutes allowed for a first-timer.

---

## 2B. How the board was closed, 2 September 2026

**Class:** not a change to the instrument. No schematic, netlist, BOM, mechanical part or
firmware line moves in this section: parts moved on the board and three faults in the
programme's own tools were corrected. **It takes no ECO number.** The placement comments in
`tools/design.py` label these changes ECO-EEG-028, which is a number this register withdrew
under section 2 and does not reuse; the record is here, and the next free ECO number is still
**ECO-EEG-030**.

**Was:** the route ECO-EEG-018 was first written against -- **122 of 145 nets connected, 23
unclosed, 7 of those with no copper at all, 25 DRC violations**.
**Now:** **145 of 145 connected, 0 unclosed, 0 without copper, 0 violations.** Four things did
it, and the order matters, because each one exposed the next.

1. **Placement, before routing.** **J4 moved 14 mm south**, from y = 36 to y = 50, so that its
   analogue pins face the protection rows that feed them instead of fanning diagonally through
   one window and sealing each other in. **R92 and R93**, the separable AVDD2/AVSS2 rail links,
   moved off x = 54 -- where the rail trunk ran between them and J29, which is why AVSS2 shipped
   with no copper at all -- to the mid-latitude of the pins they serve, so no rail net runs the
   length of the socket. **J22** moved from the bottom edge to directly under the protection
   ladder, which shortened two electrode runs from about 50 mm to under 9 mm and freed the
   ladder's own escape lane. Smaller moves went with them: C80/C81, J9, J26, R94/R95, TP10/TP11,
   and one millimetre of extra pitch between the clamp and capacitor columns for a rail lane.
2. **The isolation keep-out was being measured from centrelines.** The router blanked the cells
   of the strip but ignored the width of the copper it was carrying, so a 0.56 mm track whose
   *centreline* stayed outside the keep-out could still overhang it. The blank is now inflated
   per layer by the carried copper radius, so **copper edges** stay out of the strip. This is
   the mechanism behind the inner-plane copper that earlier revisions found inside it.
3. **The pre-placed reference vias were stamped on two layers of four.** `_place_ground_via`
   stamped each one on the top layer and the first inner layer only, while `Router.rebuild()`
   stamps all four, so **69 vias were invisible to the bottom-layer router**: it routed over
   them, and at AGND_REF pad U1.3 it ran a track through one and disconnected it. Stamping
   every reference via on all four layers is a one-line fix and it closed most of what was
   left open.
4. **Two targeted repairs.** An **AGND_REF stub outward from U1.3 with a through-via** onto
   the planes, which reports itself skipped if the pad is already joined; and the **SPARE2
   corridor**, R16.2 to D16.3, freed by ripping AVDD, AVSS, AGND_REF, EMGIN3 and EOGIN1 where
   they crossed it, routing SPARE2 first at its full electrode class and then **re-joining all
   five ripped nets at their own full class**. Rotating R16 was measured and rejected: pad 2
   already faces D16, and turning it would move the pad away and push EOGIN2 across the lane
   SPARE2 needs.

**What it cost, and it is not nothing.** Connections the router had to relax rose from **19 to
169** -- 36 with a conductor narrower than the 0.25 mm preferred width, 133 at full width with
a reduced gap, every one at or above the 0.20 mm minimum conductor and gap, so none of them is
a violation. Track segments went from 3 370 to **3 745** and through vias from 498 to **552**.
**A board that closes at minimum geometry is not the same board as one that closes at preferred
geometry, even when every rule passes.** The 169 are listed in the DRC report by net and by pad
pair, and they are the first thing RFQ-EEG-002A's reviewer is asked to read.

**Verified:** `kicad/EEG-CAR-01_RevB_DRC_report.txt` -- violations 0, 145 of 145 nets fully
connected with none left without copper, minimum clearance 0.260 mm on F.Cu, 0.275 mm on B.Cu
and 0.285 mm on the planes against a 0.200 mm rule, narrowest track 0.200 mm, smallest plated
hole 0.300 mm, zero zone crossings, exactly one AGND_REF-to-DGND bridge and one
HARN_SHIELD-to-DGND bridge, no duplicate segments and no duplicate via positions, and one
continuous plane island per net on both inner layers.

### 2C  Two findings of 2 September 2026, after the gate was met

Both came out of auditing the package against a question it had not been asked -- whether
anything attaches to the wrist -- and neither is a routing defect.

**The pad model.** `tools/fplib.py:171` gives every through-hole header pin but pin 1 the
shape `oval`, which at equal sides is a circle; that is the KiCad convention and what
`kicad_write.py` emitted. `pours.py` modelled every non-circular pad as a box and
`gerber.py` apertured it `R,1.6X1.6`, so the connectivity check, the clearance check and the
copper that would have been fabricated all carried a 1.6 mm square where the design has a
1.6 mm round pad. The corners are 27 % of the pad area and the router used them: 145 of 145
nets closed on the square, 62 of 145 on the round pad. **Fixed** -- `gerber.py` now emits
`C,w` for a square `oval` and `pours.py` models a circle, so the fabricated copper, the
KiCad file and the check agree. 184 stranded track ends were given entry stubs to the pad
centre by the new `tools/pad_snap.py`, added rather than substituted because moving an end
rotates its segment and the first attempt put MISO 0.158 mm from a via of START. Re-checked:
**145 of 145, VIOLATIONS: 0** on the round pads. Segments 3 560 -> 3 744, vias unchanged.
That 3 744 is the figure at that repair and **not the census of the released board**, which is
**3 745 segments and 552 vias** -- the bias-lead fix below added one of each. The routing-result
table in ECO-EEG-018 and `kicad/EEG-CAR-01_RevB_DRC_report.txt` carry the current figures.

**The bias-lead protection topology.** *As found:* `design.py` wired all sixteen protection
networks as src(patient) -[Rn]- dst(module) with `Dn.3` and `Cn.1` on dst, and then overrode
channel 11 to put `D11.3` and `C11.1` on `BIAS_EL`, the patient side. A shorted D11 half
therefore reached the Fpz electrode **with no series resistor in the path at all** (183.6 uA
on this programme's bound B, against S-02's 50 uA), and a shorted C11 bonded that electrode
to AGND_REF -- the earth connection IFU-EEG-014 tells the participant does not exist.
Rev B recorded it as **not fixed, and not fixable by layout** -- RISK-EEG-011 **SF-1a**,
**SF-6a** and **SR-12** -- with the sheet-2 schematic note that claimed every conductor
reaching a person passes through one resistor and one clamp corrected against it.

**Fixed on 2 September 2026, and it is a netlist change, not a layout one.** The channel-11
exception in `design.py` is deleted: the row is generated by the same loop as the other
fifteen, so **`D11.3` and `C11.1` sit on `BIASOUT`, behind the series resistor**, and the
Fpz electrode is no longer reachable through a shorted clamp half with nothing in the path.
**SF-1a collapses into the ordinary SF-1**, and no part is added and no value changes: an
exception is removed. ECO-EEG-024 alone would not have closed this -- D11 had no resistor in
its fault path at all, so a larger resistor elsewhere changed nothing, which is why the two
had to be taken together. Getting four re-labelled pads back into a closed board took a
repair rather than a re-route: `tools/repair_nets.py` runs a full DRC afterwards and refuses
to write unless the board comes out at least as good as it went in, and it refused twice.
The board is **145 of 145 nets, 0 violations, 3 745 segments and 552 vias** -- one segment
and one via more than before the fix. **It is still for the electrical safety review that has
not happened:** RISK-EEG-011 owns SF-1, SF-6 and SR-12, and a fault path removed in the
netlist is not a fault path reviewed.

**Impact:** the fabrication-release gate of section 3 is met, and the data in `kicad/` is
**released for review under RFQ-EEG-002A**; the routing-result table in ECO-EEG-018 above and
section 3.4 of DSN-EEG-003 are restated from the report. Nothing else moves. **Nothing here has
been manufactured or measured, and no human layout engineer has reviewed the routing.**
Rev B closed this section by naming two requirements that were not met and were untouched by
the routing work: S-02 at a calculated 53.2 µA, and S-04's charge thermistor. **Corrected
2 September 2026: S-02 is met in the design at 36.8 µA under ECO-EEG-024, and unsigned.
S-04 is unchanged and still not met** -- there is no NTC net in `design.py` and no thermistor
way on J12 or J13, so it does not exist and cannot be tested.

---

### 2D  The firmware and the test tool, 2 September 2026

**Class:** not a change to the instrument, and **it takes no ECO number.** No requirement,
schematic, netlist, BOM, mechanical part or pin assignment moves in this section. What moved
is firmware source that did not do what FW-EEG-001 Rev C already required of it, and browser
source that did not either. FW-EEG-001 owns the firmware defect register and the FW-Dnn
numbers; this section records what happened so that the register is not the only place it is
written down. The next free ECO number is unchanged at **ECO-EEG-030**.

**The firmware could not have been built.** `firmware/main/drivers.h` did not exist. `main.c`
called seven functions that `drivers.c` defines -- `sd_free_mb`, `unit_serial_into`,
`atecc_serial_into`, `battery_percent`, `envelope_onset_after`, `codec_play_tone_at` and the
`drv_*` group -- with no declaration in scope. In C99 and later an implicit declaration is an
error rather than a warning, and ESP-IDF compiles with
`-Werror=implicit-function-declaration`, so the build stops. Where a toolchain does accept it,
the failure is quieter and worse: an undeclared function is assumed to return `int`, so
`sd_free_mb()`'s `uint32_t` and the pointer returns are truncated or misread at run time with
no diagnostic. **Now:** `drivers.h` declares the API and is included by both `main.c` and
`drivers.c`, so the compiler checks the definitions against the prototypes the callers use.
`main.c` also now includes `board_pins.h` and `esp_attr.h`, which it had been using without
including.

**FW-D14: every command the browser sent started a recording session.** A host command is a
full frame -- the ten-byte header of FW-EEG-001 section 5.1, then the opcode, then the
opcode's own payload. `rx_task()` handed `handle_command()` the frame from byte 0, so what
the firmware read as the opcode was header byte 0, the protocol version. `PROTO_VERSION` is 1
and `CMD_START_SESSION` is 0x01, so **IDENTIFY, LOOPBACK, CLOCK_XCHG and the rest all
dispatched as START_SESSION**, and the one command that appeared to work did so by that
coincidence and not because anything was right. **Now:** `rx_poll()` strips the ten-byte
header and validates the version and the frame type before dispatch, and the body of
`rx_task()` is factored into `rx_poll()` so a host harness can drive the real decode path
rather than a copy of it. FW-D14's status in the defect register belongs to FW-EEG-001.

**The acknowledgement did not have the shape the specification gives it.** FW-EEG-001
section 6.2 fixes the CMD_ACK payload as opcode echoed, one reserved zero byte, status,
result length, then the result. Every ack went out as two bytes with the status at offset 1
and no length, and IDENTIFY, LOOPBACK and CLOCK_XCHG skipped the shape altogether and
returned their result at offset 0. That is not tidiness: with no opcode echoed on three
replies, a host cannot tell which command an acknowledgement answers, and a queue that
resolves the next pending command with whatever arrives will mis-attribute a reply under any
load at all. **Now:** the firmware emits the section 6.2 shape, with defined statuses for
ok, unknown opcode, the VBUS charge interlock of S-01 and not-implemented; and the browser
tool's `transport.js` and its simulated device were corrected to read and write the same
shape.

**Two capability bits said something they did not mean.** CMD_IDENTIFY never set CAP_CODEC
under any condition, although TOOL-EEG-022 section 2.3 defines bit 3 as *codec initialised* and
the tool displays it, so a working codec always read as absent. CAP_ATECC was set only when
the ATECC608B's configuration zone was locked, conflating *the chip is fitted* with *the unit
is provisioned* -- different questions, asked at different stations, and the second is what
T6 turns on. **Now:** CAP_CODEC is set when the codec is ready, CAP_ATECC when the chip
answers, and CAP_PROVISIONED when the configuration zone is locked.

**Why none of this was caught, which is the part worth keeping.** The browser tool's own test
suites passed throughout, and they still pass. They could not have failed. The host and the
simulated device it is tested against are **both JavaScript, written together from the same
reading of the specification, and they shared the same misunderstanding**: the JS device
answered an acknowledgement of `{ opcode, 0xFF }`, the JS host expected exactly that, they
agreed with each other on every run, and they agreed with neither FW-EEG-001 section 6.2
nor `main.c`. There were three acknowledgement shapes in the package -- the specification's, the
firmware's and the JavaScript pair's -- and the only pair ever compared was the one that
could not disagree. The header defect was invisible for the same reason: the JS device read
the header the JS host wrote, so nothing in that suite ever asked where the opcode was.
It is not a weak test; it is a test of the wrong thing, and no quantity of it would have
found FW-D14.

**Now:** `webtest/tests/interop/` removes the shared author. It compiles the shipped
`firmware/main/main.c` against small ESP-IDF stubs -- on a copy, with one `_Static_assert` on
a TinyUSB descriptor length neutralised because the stubs cannot expand that macro, and the
shipped source is not modified -- wires its USB endpoints to a pipe, and drives it with the
browser tool's own `protocol.js` and `transport.js` under Node. The C firmware and the
JavaScript host are therefore checked against each other rather than each against its own
reflection. It runs **57 checks, all of which pass and none of which fail** -- 32 when this section was
written, and the count moved as checks were added, most recently for the provisioning opcodes
of section 2E -- and is invoked as `sh webtest/tests/interop/run.sh`. It needs a C compiler and Node, and neither ESP-IDF nor
hardware. That total is the interop harness's own; the production-simulation total is the one
in section 1.1, and the two are not to be quoted for each other.

**Impact:** firmware source, the browser tool's transport and simulated device, and one new
test directory. **Nothing here has been run on hardware** -- no unit exists, the interop
harness runs the firmware's dispatch path on a host compiler against stubs, and what it
proves is that the two implementations agree with the specification and with each other, not
that either works on the instrument. *Rev B wrote "nothing here has been built or run on
hardware"; the "built" half became false later the same day and is corrected in section 2E,
which records the first real ESP-IDF build. The "run on hardware" half stands.* **Three documents carry the consequences and not this
one:** FW-EEG-001 owns the FW-Dnn register, the section 5 wire format and the section 6.3
opcode table that places CMD_IDENTIFY and CMD_LOOPBACK; TOOL-EEG-022 owns the tool's own file
list and its account of what the tool is tested against; TST-EEG-004 owns the T-numbers, and
**the interop harness has none and is not a production test step** -- TST-EEG-004 requires it
re-run for every firmware image as a control on the tool, which is a different thing from a
step a unit passes.

---

### 2E  The firmware was built, and then it was run, 2 September 2026

**Class:** not a change to the instrument, and **it takes no ECO number.** No requirement,
schematic, netlist, BOM, mechanical part or pin assignment moves here. What moved is the
firmware project's own build configuration and one host script. FW-EEG-001 owns the firmware,
the FW-Dnn numbers and the opcode table; this section records what happened, because until
2 September 2026 no document in this package could say that the firmware had ever been
through a compiler, and several said the opposite as a matter of record. The next free ECO
number is unchanged at **ECO-EEG-030**.

#### The build

**ESP-IDF v5.2.5, target esp32s3.** `firmware/release/` holds the four images ASM-EEG-007
section 6.1 and FW-EEG-001 section 9 tell the operator to flash -- `bootloader.bin` at 0x0,
`partition-table.bin` at 0x8000, `ota_data_initial.bin` at 0xF000 and `eeg_field_kit.bin` at
0x20000 -- with **`manifest.json` recording the SHA-256 of each**, and the production
simulation verifies every digest on every run. The application image is **405,360 bytes** as
flashed, and `esp_idf_size` reports **405,245 bytes** of linked image in
`firmware/release/size.json`. The build is the Phase 1 configuration,
`sdkconfig.defaults` + `sdkconfig.phase1`: secure boot, flash encryption and anti-rollback
off, so a prototype burns no eFuses and stays re-flashable (RUL-EEG-021 section B).

That closes a hole the package had carried since v1: the shop had a flashing procedure and
nothing to run it on, while the same documents forbid the shop building the firmware itself.

#### The five defects the build found, none of which any check in this package could have found

The interop harness of section 2D compiles `main.c` against stubs, and **a stub agrees with
anything.** A real toolchain does not.

1. **`esp_driver_i2c` does not exist at ESP-IDF 5.2.** The I²C driver was split into its own
   component at 5.3 and `main/idf_component.yml` permits 5.2, so the project required a
   component by name at a version where it is absent, and configuration stopped dead. The
   `driver` component provides I²C at both versions.
2. **`sdkconfig.phase1` set `CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK` twice** -- `=n`, with a
   comment explaining why a Phase 1 prototype has none, and `=y` eleven lines later in a
   block added to close FW-D11. **The later duplicate silently wins**, so the Phase 1 intent
   was being undone by a line that read as an addition. It also fails the build outright:
   ESP-IDF refuses anti-rollback on a partition table carrying a `factory` partition, and
   `partitions.csv` has one. That is how it was found -- the first real build stopped there.
3. **`CONFIG_TINYUSB_VENDOR_ENABLED` does not exist.** esp_tinyusb 1.4.x calls it
   `TINYUSB_VENDOR_COUNT`, and **ESP-IDF warns on an unrecognised key rather than failing**,
   so the setting looked present while `CFG_TUD_VENDOR` stayed 0, `tusb.h` declared none of
   the `tud_vendor_*` functions, and **the WebUSB interface this whole instrument is built
   around would not have existed.** It surfaced as an implicit declaration of
   `tud_vendor_mounted` the first time the firmware met a real compiler.
4. **Three descriptor callbacks were defined twice.** `main.c` defined
   `tud_descriptor_device_cb`, `_configuration_cb` and `_string_cb` **and** passed the same
   descriptors through `tinyusb_config_t`; esp_tinyusb defines those three itself, so the
   link failed with three multiple-definition errors. With `CONFIG_TINYUSB_DESC_CUSTOM` the
   descriptors are data and the component owns the callbacks. `tud_descriptor_bos_cb` stays,
   because the component defines no BOS callback and without BOS there is no WebUSB.
5. **`firmware/main/drivers.h` did not exist**, so `main.c` called seven functions with no
   declaration in scope. That one was found earlier the same day and is recorded in section
   2D above; it is counted here because it is the same class of defect and the same compiler
   would have caught it.

**One more thing the build measured rather than fixed.** Static IRAM links with **one byte
free of 16,384**. That is a cliff, not a pass: the next function anyone marks `IRAM_ATTR`
fails the link with an error naming a section rather than a cause, and this design has more
interrupt work coming. Two ISRs this firmware does not use -- there is no SPI slave in the
design and nothing uses gptimer -- were taken out of IRAM and **the figure did not move by a
single byte**, so that is not the cause and is not to be recorded as the fix. It is open
item 1 of the simulation run, and settling it means reading the linker map against hardware.

#### The QEMU run, and what it does not prove

`firmware/release/qemu_boot.log` is one full boot cycle from qemu-system-xtensa 9.0.0,
`-M esp32s3`, against this build with an emulation overlay -- `sdkconfig.qemu`, which sets
`CONFIG_SPIRAM_IGNORE_NOTFOUND` because QEMU's esp32s3 has no octal PSRAM, and which is an
emulation overlay and not a build configuration for any unit. What executed, none of which
ever had: the second-stage bootloader read **this** partition table, all nine entries, and
loaded the app from the factory slot at 0x20000; `app_main()` reached its own banner; the
microSD mount failed, as it must with no card, and the firmware continued with the warning it
was written to give; the ES8388 failed and degraded the same way; and the 6 MiB ring would
not allocate, where **FW-D13's NULL guard caught it and named the cause**,
`CONFIG_SPIRAM_MODE_OCT` and the -N16R8 part. Three bring-up paths exercised, three behaved
as designed.

**It has never run on hardware, and QEMU carries none of the peripherals this firmware talks
to** -- no octal PSRAM, no microSD, no ES8388, no ADS1299. No register value, no daisy-chain
order and no SPI timing has met silicon. The run proves the part that needs none of them.
About the instrument it proves nothing.

**And it found a failure mode, which is what running things is for.** Two subsystems degrade
and one aborts: a missing card and a missing codec are warnings, a missing ring calls
`abort()`, and the unit reboots into the same abort for ever. On a bench that is right --
without the ring there is no recording. In a participant's home it is the worst available
behaviour: **a boot loop is indistinguishable from a flat battery or a broken cable**, the
device never enumerates, and the browser tool that exists precisely to answer "what is wrong
with this unit" can never reach it. It is raised against F-06 and TOOL-EEG-022 and it is not
closed here.

#### The provisioning opcode collision, and the guard that was missing

`firmware/tools/provision.py` and `main.c` both allocated **0x4A** on 2 September 2026 -- the
host for the ATECC configuration-zone write, the firmware for `CMD_READ_CALIBRATION` --
because each picked the next free opcode without the other. Moving the host's config write to
0x4B then landed on an opcode **the same file was already using**, so for a short time both
`CMD_ATECC_WRITE_CONFIG` and `CMD_READ_CALIBRATION` stood at 0x4B: a second collision, made
while fixing the first, and this one inside a single file. Provisioning step 7b's read-back
would have sent a three-byte request that the firmware parses as a 65-byte configuration
write and answers bad-length, so **TST-EEG-004 T6's acceptance read-back would have failed on
every unit.**

**Both collisions are closed, and `main.c` is the authority: 0x4A reads calibration, 0x4B
writes the configuration zone**, which is what the firmware implements and what
`provision.py` now sends. The guard matters more than the fix. **`provision_selftest.py` now
asserts that every `CMD_` constant in that file is unique and matches `main.c`** -- the check
whose absence let one opcode be allocated twice in a single day -- and two of the interop
harness's 57 checks pin the meanings from the other end, refusing a short config write with
bad-length and confirming that 0x4A still answers as the calibration reader. An opcode table
belongs in one place; until it is in one place, a test has to hold it.

**Impact:** the firmware project's component list and build configuration, one host script
and its self-test, and four release images with a manifest. **Nothing here changes the
instrument, and nothing here is a bring-up.** **Three documents carry the consequences and
not this one:** FW-EEG-001 owns the FW-Dnn register, the section 6.3 opcode table and the
ESP-IDF version it pins; TOOL-EEG-022 owns what the tool is tested against; TST-EEG-004 owns
T6 and the T-numbers. **Any document still saying that the firmware has never been compiled
is wrong as of 2 September 2026**, and each of those documents corrects that for itself --
this register records the fact, it does not amend other documents from here.

---

## 3. Change procedure from here

1. **Raise.** Anyone may raise a change. It is written as one paragraph: what is wrong, how
   it was found, and what it stops someone doing.
2. **Classify.** *Blocking* -- something cannot be built, tested or used safely. *Major* -- a
   requirement is not met, or a document says two different things. *Minor* -- everything else.
3. **Assess.** State the impact on: the board, the firmware, the mechanical parts, the BOM,
   the test specification, the safety case, and the cost of any units already built.
4. **Change the source, not the output.** If the change touches the carrier, edit
   `tools/design.py` and run `tools/emit_all.py`. If it touches a printed part, edit
   `tools/mech_gen.py`. Never edit a generated file.
5. **Verify.** Re-run `tools/emit_all.py` and `tools/simulate_production.py` and attach both
   reports to the ECO. Two gates apply, and they are not the same gate.

   **The gate for releasing fabrication data** is that the DRC reports **zero violations**,
   that every net is one connected copper island, and that both inner planes remain
   continuous under the analogue zone. **That gate is met, as of the DRC report of
   2 September 2026:** zero violations, 145 of 145 nets connected with none left without
   copper, and one continuous plane island per net on both inner layers. What met it is
   recorded in section 2B. **The data in `kicad/` is therefore RELEASED FOR REVIEW under
   RFQ-EEG-002A, and it is still not released for fabrication** -- that release waits on the
   review itself, because the routing was produced by the programme's own tools and **no
   human layout engineer has read it**, and because the board closed by taking the tightest
   geometry the rules allow on **169 connections**. Nothing may be ordered from this data
   until RFQ-EEG-002A has reviewed the routing and signed it off. A future change that
   reopens a net or raises a violation puts the gate back where it was, and this paragraph
   is rewritten again rather than quietly left standing.

   **The gate for an ECO inside this release** is narrower, because the release is a review
   package rather than a fabrication package: the change must add no violation, must not
   increase the count of nets that are not one island, must not put copper in the isolation
   keep-out on any layer, and every violation it closes must be named in the ECO. Now that
   the report is at zero, a change that adds one is a regression and is reverted rather than
   argued. The simulator must stay at zero failures; its open items are counted and named.
   The DRC item is gone, because the report records no violations. **The six that stand are
   the static IRAM pool with one byte free, the carried-over v1 HM-01 mesh being two
   disconnected bodies, the unreviewed routing, E-27 never having been seen to light, the
   unreconciled board current, and SR-01 being closed in the design and not signed off** --
   193 passed, 0 failed, 6 open, which is what the last run of 2 September 2026 printed and
   what section 1.1 states. E-11's low-pass half and E-27's missing driver were on this list
   at the previous run and are gone from it because both were closed, not because either was
   regraded. A change that raises the failure
   count is a regression. A change that moves the passed count moves it because the check
   set moved, and the ECO says which checks it added or withdrew.
6. **Record.** Add the ECO to section 2 with the same fields as the entries above and take
   the next free number in the ECO-EEG-0nn sequence, which is **ECO-EEG-030**. Never
   ECO-EEG-016, which is this document, and never ECO-EEG-028 or ECO-EEG-029, which are
   withdrawn under section 2 and are not reused. Bump the revision of every document the
   change touches, and update sections 1.1, 1.5 and 2.1.
7. **Release.** A release is the whole package or nothing. Regenerate the checksums in
   `kicad/gerber/README_layer_map_and_checksums.txt` and the package manifest.

**A change that affects the safety case** -- anything touching the electrode path, the
isolation, the battery, the charge interlock or the patient-current budget -- additionally
requires RISK-EEG-011 to be re-issued and the safety reviewer to be told, whether or not the
review has already happened. **ECO-EEG-023 and ECO-EEG-024 are both in that class and both
are open**, so the safety reviewer receives them as part of the pack rather than as changes
already made.

**A change that needs a test step** cites a T-number from TST-EEG-004, which owns the step
numbers. If the step does not exist, the ECO says so and raises it as an open item; it does
not invent a number.

## 4. What is deliberately not under change control

The experiment design document, the participant information sheet and the pre-registration
are the programme's research documents and are controlled elsewhere. They are cited from
this package but are not part of it. Where package v2 documents cited them as ETH-EEG-001,
DIS-EEG-001 or KPL-EEG-001, those identifiers are withdrawn under section 1.3 and the
documents are cited by title.
