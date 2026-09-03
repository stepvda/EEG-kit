EEG FIELD KIT -- DESIGN AND PRODUCTION PACKAGE v2.2
TI One Voice research programme, one.witysk.org, Brussels, Belgium
1 September 2026.  Board revision B.
Licence: hardware and documents CC BY-SA 4.0; firmware MIT.
Contact: Stephane van der Aa -- stephane@stepvda.com -- +32 493 70 16 01

--------------------------------------------------------------------------------------
WHAT CHANGED FROM PACKAGE v1
--------------------------------------------------------------------------------------
v1 was honest that a manufacturer could quote from it but not build from it: the carrier
board was placed and netlisted but UNROUTED, there was no schematic, no drill data, no
assembly instructions, no harness wire list, no test fixtures and no quality plan.

v2 was produced by generating the whole carrier from one machine-readable design source
and then checking it -- netlist connectivity, geometric clearances, zone rules,
star-point uniqueness -- against that source rather than against prose.  Doing so found
FOURTEEN defects in v1, four of which made the board impossible to build at all:

  * the eight contact-light lines had NOTHING DRIVING THEM;
  * there was NO SOURCE FOR THE 3.3 V RAIL -- the board could not have powered up;
  * the envelope filter WAS NOT IN CIRCUIT (an op-amp input was unconnected);
  * the shift-register lines used GPIO35/36/37, which carry the OCTAL PSRAM.

There were also no mounting holes, the ESP32 DevKit header spacing was 0.86 mm out, and
the six non-plated retention holes of the touch-proof EMG sockets were declared on the
copper and mask layers, which would have plated them.

All fourteen are closed and logged in docs/ECO-EEG-016.

TWO THINGS THEN CHANGED BECAUSE WE DID THE LAYOUT INSTEAD OF ASSERTING IT

  * The carrier grew from 130 x 124 mm to 150.0 x 130.0 mm.  Thirty connectors, 211
    reference designators and 156 nets would not close at the smaller outline.
  * The carrier went from TWO layers to FOUR -- L1 signal, L2 reference plane, L3
    reference plane, L4 signal.  Package v1's architecture argument was that a two-layer
    carrier is cheap and easy to route.  It is not: on two layers the bottom side has to
    be both the reference plane and the second routing surface, and it cannot be both.
    Four layers give two full routing surfaces AND a continuous reference under every
    analogue trace, which is what a sixteen-channel EEG front end needs.  At 2 units that
    costs about EUR 35 in total; at 50 units about EUR 3 a board.

WHERE THE BOARD ACTUALLY STANDS

  Routed on four layers: 3 745 track segments, 552 through vias, and each reference plane
  is one continuous island per net.

  THE DRC REPORTS ZERO VIOLATIONS -- "none.  The board passes every rule listed above."
  145 of 145 nets are one connected copper island.  Smallest measured clearance 0.260 mm on
  L1, 0.275 mm on L4 and 0.285 mm on the planes against a 0.20 mm rule; narrowest conductor
  0.20 mm; smallest plated hole 0.30 mm; copper to a non-plated hole 2.00 mm; no digital net
  in the analogue zone; exactly one AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND
  bridge; no duplicate copper anywhere.

  ECO-EEG-016 section 3 sets the gate for releasing fabrication data as zero DRC violations,
  every net one connected copper island, and both inner planes continuous under the analogue
  zone.  ALL THREE ARE NOW MET.  The data is RELEASED FOR REVIEW under RFQ-EEG-002A, and
  FABRICATION RELEASE AWAITS THAT REVIEW.

  That distinction is deliberate.  Zero violations means the layout satisfies the rules the
  programme wrote down; it does not mean the layout is good, and no human layout engineer has
  looked at it.  Read KNOWN_ISSUES.txt section 1b before ordering copper: 169 connections are
  routed at reduced width or gap, all legal, but a board that closes at minimum geometry is
  not the same board as one that closes at preferred geometry.

--------------------------------------------------------------------------------------
WHAT CHANGED IN v2.2
--------------------------------------------------------------------------------------
v2.2 makes the kit buildable rather than only well described.

  * THE FIRMWARE NOW COMPILES AND LINKS.  It did neither.  main.c had C++ syntax in a .c
    file, drove the octal PSRAM bus as if it were the contact-light shift register, asked
    for a 12 MiB ring buffer from 8 MiB of PSRAM, and called seven functions that nothing
    defined.  FW-D01, D08, D12 and D13 are closed, drivers.c is written, and all ten
    provisioning opcodes exist -- as does the unit-serial write the host had been sending
    nowhere.
  * A CONNECTIVITY TEST PROGRAM, TOOL-EEG-022.  One self-contained HTML file: double-click
    it, plug in the instrument, press a button, and it tells you whether the computer and
    the instrument can talk.  No install, no server, no measurement.  Its protocol,
    transport and sink layers ARE the study runner's, so the browser client is written once
    rather than twice.
  * THE ENCLOSURE CAN BE CLOSED AND THE KIT CAN BE PACKED.  The lid had four holes and the
    base had no bosses under them; the pod had no harness entry at all; the carrier and
    MP-01 wanted the same four fixings.  All three are fixed in the model.  Nine missing
    printed parts are modelled, WH-KEY-01 has geometry, WH-BUS-01 has a fabrication set,
    and CASE-00 is cut as the seven Rev C layers with the dead Rev B files deleted.
  * A SECOND INDEPENDENT REVIEW was verified finding by finding and applied.

THE ROUTING WAS UNCHANGED AT v2.1, AND THAT WAS A RESULT RATHER THAN AN OMISSION.  The
router was pushed hard at what were then twenty-three open nets -- rip-up enabled, budget raised
tenfold, made transactional, then thirty-three minutes of direct repair -- and closed none
of them.  What finally closed the board at v2.2 was not more routing effort but three
defects in the obstacle model the router was solving against; KNOWN_ISSUES.txt section 1b
records both the wasted day and what actually worked.

--------------------------------------------------------------------------------------
WHAT CHANGED IN v2.1
--------------------------------------------------------------------------------------
v2.1 is v2 with an independent review applied.  The review made about 120 findings; each
one was checked against the files before anything was changed, and the check mattered:
32 were things the package already declared openly as open items, and 12 were wrong -- two
of them would have introduced bugs into correct firmware if applied.  97 were real and are
fixed.  The largest were:

  * DUPLICATE COPPER.  The released Rev B data contained 28 duplicate track segments and
    4 doubly-drilled via positions, and the census every document quoted counted them.
    The board was then 3 370 segments and 498 vias, not 3 398 and 502.  The de-duplication now
    runs after the via-clearance pass rather than before it, which is where the duplicates
    were coming back from, and drc.py has a uniqueness check so it cannot recur.
  * TABLES DID NOT RENDER.  In most of the .docx and .pdf, tables were not tables: every
    cell printed as its own full-width paragraph.  The reference document pandoc renders
    against was missing the table style it writes against, and its grid was 2.24 times the
    width of an A4 page.  Both fixed; the documents are rebuilt.
  * THE .kicad_pcb PLANES WERE WRONG.  The writer emitted only each polygon's outer ring,
    so 226 and 407 voids apiece -- every antipad and keep-out -- vanished and the planes
    read as solid rectangles.  The Gerbers were always correct.  See KNOWN_ISSUES.txt 4.
  * ONE SAFETY GAP THAT NOTHING DECLARED.  CMD_START_SESSION armed a session without ever
    reading VBUS_DET, so only half of S-01 existed.  Fixed, and registered as FW-D17.
  * The USB iSerialNumber was defined two ways in nine documents and the code implemented
    the one the ruling rejects.  One definition now: the unit serial TIOV-B-nnnn.

tools/check_consistency.py is new and refuses superseded figures and names.  It passes.

--------------------------------------------------------------------------------------
BEFORE YOU QUOTE OR BUILD
--------------------------------------------------------------------------------------
Read KNOWN_ISSUES.txt.  It is the short list, in one place, of what is wrong with the data
as shipped -- what closing the board cost in routing geometry, the ECO that is
specified and deliberately not applied,
the parts that are not settled and the two requirements that are not met.  Everything in it
is also in the controlled documents; the file exists so that you find them here rather than
at CAM time.

--------------------------------------------------------------------------------------
PRECEDENCE  (if two documents disagree, the higher one governs)
--------------------------------------------------------------------------------------
  1. DSN-EEG-003 Rev C   Manufacturing design package -- THE GOVERNING DOCUMENT
  2. RFQ-EEG-001 Rev E   Requirements and acceptance (M/S/O), pricing template
  3. ICD-EEG-006 Rev B   Interface control: module pinouts, jumpers, GPIO map
  4. SCH-EEG-005 Rev B   Schematic set, eight sheets
  5. DSN-EEG-002 Rev E   Helmet, electrodes, wiring, fitting, case
  6. PARTS-EEG-019 Rev B Part identifier register
  7. RUL-EEG-021 Rev A   Rulings register -- the answers the audit forced
  8. EEG_kit_BOM_for_bidders_RevC.xlsx

Where a number appears in a document AND in tools/design.py, DESIGN.PY GOVERNS.
tools/emit_all.py regenerates every fabrication file from it in one pass, so the
package cannot drift.

--------------------------------------------------------------------------------------
WHAT IS IN THE PACKAGE
--------------------------------------------------------------------------------------
docs/        Twenty-one controlled documents.  Start with DSN-EEG-003 Rev C, then the RFQ.
             New in v2: ICD-EEG-006 (module interfaces), ASM-EEG-007 (assembly work
             instructions), WH-EEG-008 (harness wire list), JIG-EEG-009 (test fixtures),
             QP-EEG-010 (quality plan), RISK-EEG-011 (risk analysis and the safety-review
             pack), REG-EEG-012 (regulatory file, including lithium shipping),
             SVC-EEG-013 (service and refurbishment), IFU-EEG-014 (participant card),
             PKG-EEG-015 (packing and labelling), ECO-EEG-016 (change control),
             AVL-EEG-017 (approved vendor list), SIM-EEG-018 (production simulation),
             PARTS-EEG-019 (part identifier register), FW-EEG-001 (firmware),
             RUL-EEG-021 (rulings register), and the three workbooks: the kit BOM Rev C,
             the internal costed BOM Rev C and the manufacturer contacts Rev B.

kicad/       EEG-CAR-01_RevB_routed.kicad_pcb    the routed board, tracks, vias, pours
             EEG-CAR-01_RevB_DRC_report.txt      every rule, every measurement
             EEG-CAR-01_RevB_BOM.csv             grouped, with manufacturer part numbers
             EEG-CAR-01_RevB_CPL_SMT_top.csv     pick-and-place, bottom-left origin, Y up
             EEG-CAR-01_RevB_CPL_THT_top.csv     through-hole positions
             EEG-CAR-01_RevB_fabrication_drawing.pdf   dimensions, drill schedule, stack-up
             EEG-CAR-01_RevB_assembly_drawing.pdf      designators, pin 1, DNP, process
             EEG-CAR-01_RevB_copper_layers.pdf         all four layers at 1:1
             EEG-CAR-01_RevB_PCB_spec_sheet.txt        for bidders who open no board file
             EEG-CAR-01_RevB_netreport.json            nets, classes and rules, machine-readable
  gerber/    Gerber X2 (four copper layers, mask, legend, paste, profile), Excellon
             PTH and NPTH, IPC-D-356A
             netlist, a zip of the lot, and README_layer_map_and_checksums.txt with a
             SHA-256 for every file so we can agree on what was quoted.

schematic/   SCH-EEG-005_RevB_schematic_set.pdf, eight sheets, plus PNGs.
             v1 had no schematic at all.

mech/  stl/       printable meshes
       step/      parametric solids for dimensioning, fit checks and inspection
       drawings/  MECH-EEG-020, a dimensioned sheet per part
       renders/   shaded views for the work instructions
       CASE-00_foam_layer_1.dxf .. _layer_7.dxf   the seven Rev C layers, 1:1 in
                  millimetres on a 516.0 x 390.0 sheet, 25 mm thick.  The Rev B pair
                  CASE-00_foam_top_layer.dxf and _bottom_layer.dxf is DELETED and its
                  names are not reused; a two-layer insert cannot pack this kit.
                  NOT RELEASED FOR CUTTING until the helmet shell is measured.
       HARDWARE_SCHEDULE.md   every fastener, standoff and gland the released geometry
                  needs, with the size derived from the model it fits
       MECH_RELEASE_STATUS.md  which printed parts have geometry, which are released,
                  and which are named but not yet drawn
       MANIFEST.json

firmware/    FW-EEG-001: main.c, the ESP-IDF project, sdkconfig.defaults and
             sdkconfig.phase1 (the Phase 1 build, without secure boot), partitions.csv,
             a GENERATED board_pins.h, the end-of-line provisioning script and the host
             stream verifier.  v1 shipped main.c alone.

webtest/     TOOL-EEG-022, the connectivity test program.  ONE SELF-CONTAINED FILE:
             EEG-Connectivity-Test.html.  Double-click it, plug the instrument into a USB
             port, press a button, and it tells you whether the computer and the instrument
             can talk.  It takes no measurement, touches no electrode and contacts no
             server.  Chrome or Edge, Windows or macOS; nothing to install and nothing to
             compile.  The source is the modules in webtest/js/, which ARE the protocol,
             transport and sink layers of the study runner -- the tester is the same client
             with an inspector sink instead of the server upload sink.  Rebuild the single
             file with `python3 webtest/build.py`; the tests run with
             `node webtest/tests/*.mjs`.  Documented in docs/TOOL-EEG-022.

             The interop harness in webtest/tests/interop/ compiles the REAL firmware
             against ESP-IDF stubs and drives it with the REAL protocol module, so the
             two cannot drift apart unnoticed: `sh webtest/tests/interop/run.sh`.

fixtures/    The four production test fixtures of JIG-EEG-009, as buildable data rather
             than a description: PCB artwork under fixtures/pcb/, printed-part geometry
             under fixtures/mech/, and the three controller firmware images under
             fixtures/firmware/ with the FIXPROTO v1 line protocol they speak.
             Regenerate with `python3 tools/fixture_gen.py`; MANIFEST.json lists
             everything.  NOTHING HERE HAS BEEN BUILT OR RUN ON HARDWARE.

records/     The machine-readable per-unit test record TST-EEG-004 section 12 requires:
             the JSON Schema, a validator, and a worked example whose values are
             obviously placeholders.  No unit has been built, so the schema has never
             met a real manufacturer's output.

graphics/    Renders and diagrams used across the documents.

graphics/labels/
             The label and packaging artwork of PKG-EEG-015, generated as SVG by
             `python3 tools/artwork_gen.py` -- ART-LBL-01 to -07, ART-PACK-01 and
             ART-DIS-01.  The lithium mark of ART-LBL-06 needs the regulated pictogram,
             which is not a thing this programme may draw for itself; see KNOWN_ISSUES.

tools/       The generator.  design.py is the single source of truth for the board and
             mech_gen.py for the printed parts; router.py, pours.py, viafix.py, drc.py,
             netcheck.py, gerber.py, drawings.py, schematic.py, kicad_write.py,
             mech_drawings.py, assembly_render.py, emit_extras.py and emit_workbooks.py
             produce everything else, and simulate_production.py walks a unit through the
             whole production route and checks that the package supports every step.

             To rebuild the package from source:
                 python3 tools/run_build.py          route, pour, check      (~20 min)
                 python3 tools/emit_all.py --cached  Gerbers, drawings, schematic
                 python3 tools/emit_extras.py        spec sheet, netreport, STEP, manifest
                 python3 tools/mech_gen.py           STL and STEP for every printed part
                 python3 tools/mech_drawings.py      dimensioned drawings and renders
                 python3 tools/emit_workbooks.py     the three spreadsheets
                 python3 tools/simulate_production.py --report docs/SIM-EEG-018_...md
                 python3 tools/make_docs.py          A4 .docx and .pdf of every document

--------------------------------------------------------------------------------------
WHAT A MANUFACTURER CAN DO WITH THIS, TODAY
--------------------------------------------------------------------------------------
  Quote the bare board ...................... YES, firm
  Fabricate the bare board .................. AFTER RFQ-EEG-002A.  The DRC gate is met;
                                              a human layout review is not
  Assemble it ............................... YES, firm quote
  Print the mechanical parts ................ YES
  Build the harness ......................... YES
  Provision and test a unit ................. YES, once the firmware image exists
  Ship a working prototype for software ..... YES for the hardware; the firmware stubs
                                              are the programme's work
  Ship a unit for use on a participant ...... NO.  The safety review has not been done.
                                              It gates Phase 2 and nothing goes on a head
                                              before it.

--------------------------------------------------------------------------------------
THE HONEST LINE
--------------------------------------------------------------------------------------
Nothing in this package has been manufactured or measured.  Every performance figure is
calculated, and each one is labelled as calculated where it appears.

The routing was produced by the programme's own constraint-aware autorouter.  Every
clearance has been measured on the finished polygons rather than on a routing grid, and
every geometric rule passes, all 145 nets are connected and the DRC reports zero
violations -- but it has NOT been reviewed by a human layout engineer, and 169 of its
connections close at the minimum conductor or the minimum gap rather than the preferred
width.  RFQ-EEG-002A is therefore a REVIEW of the supplied routing rather than the routing
itself, and the DRC report lists every one of those relaxed connections,
so a reviewer can go straight to the places that need attention.

An end-to-end production simulation walks one unit through all fifteen stations, from the
purchase order to the kit coming back for refurbishment, checking at each one that the
package contains what the operator needs and that the acceptance limits are arithmetically
reachable.  It reports 169 checks passed, 0 failed and five known open items (the single-fault
patient current of RFQ S-02).  See docs/SIM-EEG-018.

The firmware has never been compiled against a real ESP-IDF installation and has never
run on hardware.  Five drivers are stubs.

Phases: 1 -- 2 prototypes.  2 -- 10 kits.  3 -- 10 to 40 further kits (25 to 50 total).
