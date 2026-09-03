# PRODUCTION TEST SPECIFICATION -- EEG FIELD KIT

**Document:** TST-EEG-004  **Revision:** C  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs. The binding rulings are
**RUL-EEG-021 Rev A**, a controlled document in `docs/`; the uncontrolled worksheet
`tools/RULINGS.md` is not part of the release and is not cited here.

**Rev C in one line:** the carrier is now 150.0 x 130.0 mm on four layers; this document
publishes the definitive step list T00 to T30 and the TP1 to TP18 assignment table, adopts
the FIX-01 to FIX-04 fixture names, adds the E-29 maximum acoustic output type test as T28
and the S-09 lithium check as T29, and corrects sixteen cross-document disagreements found
in the audit of 2026-09-01. **T30, the host link check run with the TOOL-EEG-022
connectivity test program, is added within Rev C on 2026-09-02**, because that program now
exists as `webtest/EEG-Connectivity-Test.html` and a manufacturer following this document
would otherwise never be told to run it.

## Why this document exists

Revision A of this specification was eighteen table rows inside DSN-EEG-003, each row a
one-line method, a one-line limit and a one-line record. A contract manufacturer cannot
quote a test line, buy equipment, build a fixture or write an operator instruction from
that, and two manufacturers executing it would produce numbers that are not comparable --
which is fatal for a study whose own requirement is that device identity must not become a
confound. Revision B made the specification standalone and executable: every step carries
its purpose, the requirement it verifies, the equipment and the accuracy that equipment
must have, the fixture, the procedure, the limit, the uncertainty of the measurement, what
is written down, and what happens when it fails. Revision C keeps all of that, corrects it
to the board as it was actually laid out, and closes the numbering and naming
disagreements that would have made a manufacturer build the wrong test station.

**No hardware in this package has been manufactured or measured**; every expected value below
is calculated from `tools/design.py` and is labelled as calculated. The one thing that has been
built is the **firmware**: an ESP-IDF v5.2.5 image for esp32s3 in `firmware/release/`, which
has been booted under QEMU and never on hardware (section 4). No board, no fixture, no unit. **No safety engineer has
reviewed this design.** Passing every step in this document does not make a unit fit to
wear.

---

## 1. Scope and the device under test

The device under test (DUT) is one complete electronics assembly: the **EEG-CAR-01 Rev
B** carrier (**150.0 x 130.0 mm, four layers**, 211 reference designators, 156 nets, 636
pads of which 620 are netlist pins), the twelve purchased module assemblies on the
**MP-01** module plate joined by keyed 2.54 mm ribbon jumpers per ICD-EEG-006, the
ESP32-S3-DevKitC-1-N16R8 inserted directly into J6 and J7, the protected 18650 cell, and
the microSD card, in the POD-P1 enclosure for Phase 1 or the HM-01 occipital shell for
Phases 2 and 3. Twelve module **types** are purchased; **thirteen module assemblies**
are fitted per unit, because the ADS1299 breakout is fitted twice. Twelve of those
thirteen sit on MP-01; the DevKitC-1 is the exception and plugs into the carrier.

**A pad and a netlist pin are not the same thing, and the two counts differ.** A pad is a
physical land or plated hole on the board; a netlist pin is a pad that carries a net, and so
is a point the bare-board test has to probe. The carrier has **636 pads** -- 390 surface-mount
lands, 236 plated through-holes and 10 non-plated holes, counted in
`kicad/EEG-CAR-01_RevB_PCB_spec_sheet.txt` -- and **620 of them carry a net**. The shipped
IPC-D-356A file `kicad/gerber/EEG-CAR-01-IPC-D-356A.ipc` says the same thing independently:
620 component-pad records and **552** via records, **1 172** test points in all, over 156 nets
-- 788 type-317 through-hole records plus 384 type-327 SMD records. *Corrected 2026-09-02:
this read "551 via records, 1 171 test points", one short on each; SIM-EEG-018 Rev A and T0
carry the corrected pair.* The
16 pads that carry no net are the six entries the three fiducials FID1 to FID3 contribute --
each is a copper land plus its mask opening -- the four M3 mounting holes and the six DIN
42802 retention posts, none of which is an electrical connection. **The figure of "614
netlist pins" used earlier in Rev C is withdrawn**: it counted distinct `designator.pin`
names rather than pads, and the three B3F-4055 tactile switches SW1 to SW3 each present four
pads under two pin numbers, so it under-counts the probe list by six.

**The carrier is four layers, and that is a finding, not a preference.** Package v1
asserted that a two-layer carrier would be cheap and easy to route. Doing the layout showed
that it is not: on two layers the bottom side has to be both the reference plane and the
second routing surface, and it cannot be both. The stack is **L1 signal, L2 reference
plane, L3 reference plane, L4 signal**, which gives two full routing surfaces and a
continuous reference under every analogue trace. The reference planes carry **AGND_REF left
of x = 62 mm and DGND right of it, on both L2 and L3**, tied together by stitching vias.
Vias are **through vias only**, 0.60 mm pad on a 0.30 mm finished hole. The stack-up is
mask / 35 um L1 / prepreg 0.200 / 17 um L2 / core 1.065 / 17 um L3 / prepreg 0.200 / 35 um
L4 / mask = **1.60 mm +/- 10 %**. The board grew from 130 x 124 mm to 150 x 130 mm for the
same reason: thirty connectors, 211 parts and 156 nets would not close at the smaller size.
Every step below that names a layer, a coordinate or a via size uses these figures. The
routing result is recorded in `kicad/EEG-CAR-01_RevB_DRC_report.txt`, which is the
authority for it, and the figures below are read from that report rather than asserted.
EEG-CAR-01 Rev B is routed on four layers with **3 745 track segments and 552 through vias**,
and **each reference plane is one continuous island per net** -- four pours in all, AGND_REF
and DGND on L2 and again on L3. **All 145 nets are fully connected**: none is left unclosed,
and none is left without copper. Against the 0.20 mm general rule the smallest measured
clearance is **0.260 mm on L1, 0.285 mm on the two planes and 0.275 mm on L4**. The narrowest
conductor is **0.20 mm** and the smallest plated hole is **0.30 mm**; no copper comes within
**2.00 mm** of a non-plated hole, and there are **no zone crossings**, **no duplicate copper
segments and no duplicate via positions**. **No digital net enters the analogue zone**, and
there is **exactly one AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND bridge**. The
report records **no violation of any rule it applies**, and that includes the isolation strip:
it is clear of copper on all four layers. This document says that because the report says it,
not because the rule was written down.

**The board closes, and the fabrication data is released for review, not for fabrication.**
The Rev B DRC report's own line is "VIOLATIONS: 0 -- none.  The board passes every rule listed
above." All 145 nets are connected, every net is one connected copper island, and both inner
planes are continuous under the analogue zone -- the three conditions ECO-EEG-016 section 3
sets for releasing fabrication data, and **all three are now met**. The data is therefore
**RELEASED FOR REVIEW under RFQ-EEG-002A**, and **fabrication release awaits that review**:
the routing was produced by the programme's own tools and **no human layout engineer has
looked at it**. How the board closes matters as much as that it closes. **169 connections are
relaxed** -- 36 take a conductor narrower than the 0.25 mm preferred width, and 133 keep full
width and take a reduced gap instead -- every one of them at or above the 0.20 mm minimum
conductor and the 0.20 mm minimum gap. A board that closes at minimum geometry is not the same
board as one that closes at preferred geometry, even when every rule passes, and those 169 are
the first thing the layout reviewer should look at. T0 still cannot be run, for a reason that
has nothing to do with the DRC: **no board has been fabricated**, and no hardware in this
package has been built or measured.

The helmet, the harness and the kit contents are tested under WH-EEG-008 and ASM-EEG-007.
This specification covers the electronics assembly and the final kit closure only.

This is a research instrument. It is not a medical device and is not placed on the market.
Passing every step in this document does not make a unit fit to wear: that gate is the
programme's electrical safety review (RISK-EEG-011), which has not yet happened.

## 2. The definitive step list

**This document owns the step numbers.** Every other document in the package cites
T-numbers from the table below and never invents one. If a document needs a step that does
not exist here, it says so and raises it as an open item rather than numbering it itself.
JIG-EEG-009 Rev B, REG-EEG-012 Rev B, PARTS-EEG-019 Rev B, RISK-EEG-011 Rev B,
PKG-EEG-015 Rev B and IFU-EEG-014 Rev B all cite T19 to T25 with meanings this table does
not give them; those citations are wrong and are corrected against this table, not the
other way round.

| Step | Name | What it does in one line |
|---|---|---|
| T00 | Incoming inspection | Rejects a wrong-variant, cloned or damaged module, and a non-C0G C1 to C16, before assembly |
| T0 | Bare-board electrical test | 100 % continuity and isolation to the IPC-D-356A netlist, plus four dedicated checks |
| T1 | Visual and AOI | IPC-A-610 class 2 plus the named polarity, DNP, star-point, fiducial and test-point checks |
| T2 | Module seating and keying | Every module present, keyed and electrically connected |
| T3 | Power-on current and DevKit regulator temperature | Idle and recording current, and the case temperature of the DevKit's 3V3 regulator |
| T4 | Charge current with a session active | Proves the charger is actually off while a session runs (S-01 mechanism 2) |
| T5 | USB enumeration | CDC-ACM plus WinUSB on three hosts, before (T5a) and after (T5b) provisioning |
| T6 | Provisioning | Key generation, identity and the measured constants written into the device |
| T7 | Front-end gain | T7a eight EEG at gain 24, T7b three EMG at gain 12, T7c two spares |
| T8 | Noise floor | Input-referred noise through the fitted protection network |
| T9 | Crosstalk and CMRR | T9a crosstalk at 50 Hz on the carrier, T9b common-mode rejection, **T9c contact-light interference through the fitted harness (type test, E-30)** |
| T10 | Lead-off calibration | Turns the raw lead-off reading into the impedance the participant is shown |
| T11 | Contact lights | Colour, site mapping and the two dark states, read with a colorimeter |
| T12 | Envelope channels | T12a scaling, T12b group delay, T12c comparator, T12d AC-coupling corner, T12e low-pass corner f0 |
| T13 | Timing self-test | The stimulus timestamp the study depends on |
| T14 | microSD throughput and integrity | 30 minutes at 1000 Hz, card copy compared frame for frame |
| T15 | Ring-buffer backfill | A 60 s disconnect is recovered from the declared ring |
| T16 | Signature chain | Every SIGNATURE frame verifies and the chain is unbroken |
| T17 | Buttons, mute, headphone level | Participant controls, mute depth, calibrated level into 47.0 Ohm, clamp readback |
| T18 | Final assembly and kit closure | Enclosure, panel openings, label, kit contents against KPL-EEG-001 |
| T19 | Star-point continuity | Exactly one AGND_REF-to-DGND path and one shield path |
| T20 | Isolation-barrier insulation resistance | 500 V DC across the barrier. **There is no per-unit hipot** |
| T21 | VBUS detection and charge-path interlock | Both S-01 mechanisms, and the VBUS_DET logic level |
| T22 | Frequency response | The passband E-10 requires, on the network that sets it |
| T23 | Leakage current at the applied parts | Fourteen terminations, normal condition and one single fault |
| T24 | Radio silent | No carrier, no SSID, no BLE advertisement |
| T25 | Firmware security posture | eFuse readback and one forced rollback. **Phase 2 onward** |
| T26 | Re-enumeration timing | A host sleep or a browser reload does not cost the session |
| T27 | Converter clock, sample rate and daisy order | The two converters really are one sixteen-channel instrument |
| T28 | Maximum acoustic output | E-29, 100 dB SPL ceiling on an artificial ear. **Type test, once per lot** |
| T29 | Lithium marking and shipping documents | S-09, verified at kit closure against PKG-EEG-015 section 7 |
| T30 | Host link check with TOOL-EEG-022 | The browser connectivity test program proves the computer and the instrument speak the same protocol, before any step that needs a decoded frame is attempted |

Rev A step numbers T1 to T18 are unchanged in identity and meaning, so a manufacturer who
quoted against Rev A can see exactly what has been added. T00, T0 and T19 to T27 were added
in Rev B; T28 and T29 are added in Rev C, and T30 is added within Rev C on 2026-09-02.

**There are thirty-two steps: T00, T0 and T1 to T30.** Any document quoting eighteen,
twenty-nine, thirty or thirty-one is citing a superseded count and is corrected against the
table above. Of those thirty-two, **eleven produce numbers that only a host stream decoder
can produce -- T7, T8, T9, T10, T12, T13, T14, T15, T16, T26 and T27** (section 16 item 10);
"nine of twenty-nine" is a Rev B-era figure and is withdrawn. T30 is not one of the eleven:
it decodes no channel and takes no measurement.

**T28 exists, it is the maximum acoustic output type test against E-29, and it is listed as a
type test in section 14 of this document.** A statement that the maximum acoustic output "has
no T-number", or that it sits in section 13, is wrong on both counts: section 13 is the
calibration-certificate template.

## 3. Precedence, and what changed from Rev B

Precedence, highest first: DSN-EEG-003 Rev C, RFQ-EEG-001 Rev E, ICD-EEG-006, SCH-EEG-005,
DSN-EEG-002 Rev E, PARTS-EEG-019 Rev B, the BOM workbook. Where a number appears here and
in `tools/design.py`, design.py governs and this document is corrected.

**Which rendition governs.** This document exists in three files with the same revision
letter: `docs/TST-EEG-004_RevC_production_test_specification.md`, `.docx` and `.pdf`. **The
Markdown is the source and the other two are renditions generated from it** by
`tools/make_docs.py`; where they disagree the Markdown governs and the renditions are stale.
That is not a hypothetical. On 2 September 2026 T30 was added to the Markdown and the
`.docx` and `.pdf` were not rebuilt, so for fifty-five minutes the two renditions a
manufacturer would normally be issued said "thirty-one steps, T00, T0 and T1 to T29",
carried no T30, gave a section 11 total of 93 attended minutes instead of 95, and would have
sent a technician to build a station that never runs the connectivity check. The Markdown
was not malformed and the renderer was not at fault: the renditions were simply older than
their source. **A rendition is stale whenever its file is older than the `.md` beside it**,
which is a check anyone can make with `ls`, and `tools/make_docs.py` is what fixes it.

| Change in Rev C | Reason |
|---|---|
| Carrier restated as 150.0 x 130.0 mm on four layers throughout | The layout would not close at 130 x 124 mm on two layers; see section 1 |
| Section 2 publishes the definitive step list T00 to T29 | Five documents had renumbered these steps, and two of the renumberings would have built the wrong station |
| Fixtures renamed FIX-01 to FIX-04 with lettered sub-assemblies | JIG-EEG-009 defines FIX-01 to FIX-04; Rev B's "Part A to G" naming collided with JIG's own use of "Part" |
| T28 added: maximum acoustic output against the new requirement E-29 | Calculated full-scale output is about 110 dB SPL and there was no requirement and no test |
| T29 added: lithium marking and shipping documents | S-09 was mandatory and had no row in the traceability matrix |
| TP1 to TP18 published as a table (section 6) | E-28 names eighteen test points and no document said what they were |
| T1: D1 to D16 are **BAV99**, not BAT54S | Schottky leakage across a 68 kOhm series resistor (47 kOhm when this row was written) is an offset error on a 10 uV input. BAT54S is used only at D20, D40, D60 |
| T7: the 10 uV point is a linearity check with a **+/- 5 %** limit, uncertainty 0.22 % at k = 2 | JIG-EEG-009 section 1.4's derivation governs; the "1 sigma" label on that figure was wrong |
| T9a: E-04 restated as **-80 dB at 50 Hz measured on the carrier** (ECO-EEG-026) | -100 dB is not achievable through a 60 mm un-interleaved ribbon and sits 40 dB below this instrument's noise floor, so it is not measurable either |
| T12b: group delay is **4.40 ms**, from 1/(Q x 2 pi x f0) | Rev B used sqrt(2)/(2 pi f0), which is only correct at Q = 0.7071. The fitted Q is 0.7416 |
| T12d: E-11 restated as **<= 2 Hz**, fitted 10 uF gives 1.6 Hz (ECO-EEG-027) | 1 uF into 10 kOhm gave 15.9 Hz, which removes the speech envelope it is meant to pass |
| T14: frame payload is **50.7 kB/s** at 1000 Hz | 1015 bytes every 20 ms. E-20's 70 kB/s and F-12's 64 kB/s are allowances that include STATUS and SIGNATURE frames and filesystem overhead |
| T15: F-06 relaxed to **90 s of ring plus unlimited microSD backfill** (ECO-EEG-025) | 12 MB of ring in 8 MB of PSRAM is impossible; the fitted ring is 6 MB, which is 126 s |
| T17: headphone load is **47.0 Ohm** | A-04 restated as 32 to 64 Ohm; the shipped ATH-M20x is 47 Ohm |
| T20: the note now says plainly that no per-unit hipot exists | JIG-EEG-009's per-unit 2500 V AC station is deleted |
| T21: R85 is **150 kOhm**, junction 3.00 V (ECO-EEG-022) | 1.79 V would not reliably assert the first S-01 interlock against a 2.48 V input-high threshold |
| T22: E-10 stated in both its states -- +/- 0.5 dB at 47 kOhm, +/- 1.0 dB at 68 kOhm | The S-02 fix raises R1 to R16 to 68 kOhm, which costs 0.75 dB at 100 Hz. **Corrected 2026-09-02: ECO-EEG-024 is applied in `tools/design.py`, R1 to R16 are 68 kOhm, and +/- 1.0 dB is the branch in force.** Rev C's "47 kOhm is on the prototypes, so the wider band is not yet earned" is superseded on that date; E-10 already stated both branches, so the resistor change moves the design to a branch the requirement carries and does not breach it |
| T23: S-02 stated against the fitted resistor value | **Corrected 2026-09-02: S-02 is met in the design at 36.8 uA against the 50 uA limit**, ECO-EEG-024 having raised R1 to R16 to 68 kOhm. Rev C's "not met, at 53.2 uA calculated" was true of the 47 kOhm build and is superseded on that date. Met in the design is not signed off: SR-01 belongs to the electrical safety reviewer of RISK-EEG-011 section 7, that review has not started, and T23 remains a stand-in for the IEC 60601-1 method |
| T25 marked **Phase 2 onward** | The two Phase 1 prototypes run unsigned images so the firmware volunteer can iterate |
| Every "E-28 deviation" note deleted | **RFQ-EEG-001 Rev E**, the revision this document governs to, asks for TP1 to TP18 plus a 1x6 debug header at J26 and withdraws the 2x5 JTAG header, so there is no deviation to record. Rev C's citation of "RFQ Rev D" here was stale |
| Golden unit is **TIOV-B-0001** | One serial format, **defined once in PKG-EEG-015 section 5** and cited, not restated, by everyone else including this document. The ruling behind it is RUL-EEG-021 section B |

**The rulings this revision applies are the registered ones.** RUL-EEG-021 Rev A is a
controlled document in `docs/` and is what this specification cites, by section letter. The
uncontrolled worksheet `tools/RULINGS.md` is not part of the release and is cited nowhere
below. The end-to-end exercise of this specification is **SIM-EEG-018 Rev A**, the production
simulation. Run against this package on 2026-09-02, `tools/simulate_production.py` prints
**`193 passed, 0 failed, 6 open`** (SIM-EEG-018 Rev A), and the six it holds open are: that
the linked image reports one byte free of the 16,384-byte static IRAM window; that the v1
HM-01 mesh is two disconnected bodies; that no human layout engineer has reviewed the routing;
that E-27 has never been seen to light, because no unit exists; that the two board-current
figures cannot both be right; and that SR-01 is closed in the design and not yet signed off,
S-02 now being met at 36.8 uA after ECO-EEG-024. **Corrected 2026-09-02.** This figure was
**superseded and is withdrawn: `171 passed, 0 failed, 5 open`**, whose five were the layout review, E-11's low-pass half,
the absent E-27 phase driver, the board-current disagreement and S-02 at 53.2 uA; and before
that "169 checks passed, none failed, and four known open items", one of which was the DRC
violations open at the time. Both sets of figures are withdrawn. Three of the five moved on
2026-09-02: the phase driver was written, ECO-EEG-024 was applied so S-02 is met in the
design, and the E-11 item left the simulation's list when `tools/design.py` rescaled the
Sallen-Key to C0G. The tool's own printed line is the authority, and any document quoting a
different one is quoting a stale run. **Those six are the simulation's own scoped count and
not a package total**: they are the open items that reach into the checks SIM-EEG-018 ran,
whereas the production-test register is section 16 of this document and lists **eighteen**
items, and the programme-level register is RFQ-EEG-001 Rev E section 12 and lists **fifteen**
-- three different scopes of one programme. **Was "sixteen" for section 16; corrected
2026-09-02**, the register having gained items 17 and 18 within Rev C. Section 16 and RFQ
section 12 are still not reconciled with each other: the T9b CMRR item is section 16 item 15,
and items 17 and 18 -- what the record's SHA-256 covers, and the schema never having seen a
real record -- have no counterpart in the RFQ either. Rev C's "fourteen", and its claim that
the E-11 item exists only in this document, are both corrected against RFQ-EEG-001 Rev E as
shipped. **Three of section 16's items are answered elsewhere and are not restated here, and
that is a gap this document owns.** RFQ-EEG-001 Rev E section 12 now marks its items 2, 4 and
15 **CLOSED 2026-09-02** -- S-02 by ECO-EEG-024, E-27 by the phase driver, and E-11 by the
Sallen-Key's rescale to a **10 nF / 22 nF C0G pair with 215 kOhm**, f0 = 49.9 Hz, which
`tools/design.py` fits and which SIM-EEG-018 Rev A no longer holds open. Section 16 items 3
and 5 are restated below against the first two. **Item 16 and the T12 rows are not**: they
still describe the X7R build and its 42.4 to 57.4 Hz spread. That is a change to the basis of
a limit this document sets -- T12e's 42 to 58 Hz band exists only because the X7R parts could
not hold 45 to 55 -- so it belongs to an ECO and to this document's owner, not to a
cross-reference fix, and it is flagged rather than made.

## 4. Test environment and preconditions

| Condition | Value | Why |
|---|---|---|
| Ambient temperature | 18 to 25 degC, recorded | Thin-film tempco and the ADS1299 reference drift |
| Relative humidity | 30 to 70 %, non-condensing | Surface leakage at the 68 kOhm nodes |
| Mains field at the bench | < 1 V/m at 50 Hz, screened bench for T8, T9, T22 | T8's limit is 1.0 uV RMS, and T9a now injects at 50 Hz |
| DUT supply | Battery only for T3, T7 to T13, T22, T23 (S-01) | Mains-referenced supplies defeat the isolation |
| Warm-up | 30 min powered before T7, T8, T9, T22 | ADS1299 reference and analogue rail settling |
| ESD | EPA per IEC 61340-5-1, wrist strap logged | 68 kOhm inputs into a CMOS front end |
| Firmware | Released image only, SHA-256 recorded in every record | See the readiness gate below |

**Firmware readiness gate.** Production test may not begin until an image is released that
(a) compiles under a named ESP-IDF 5.x with the TinyUSB component version pinned,
(b) enumerates as CDC-ACM plus a WinUSB vendor interface with the BOS and MS OS 2.0
descriptors, (c) implements the codec tone driver, the SDMMC append and free-space calls,
the ATECC608B serial read and block-signing task, the fuel-gauge read, the envelope onset
detector and **the bicolour contact-light phase driver**, (d) publishes a SHA-256 that
is copied into every unit record, and (e) **passes the protocol interop harness
`webtest/tests/interop/run.sh`**.

That harness is the build-verification gate for the wire format, and it is the reason (e)
exists as a separate condition. It compiles the shipped `firmware/main/main.c` against small
ESP-IDF stubs, wires the simulated USB endpoints to standard input and output, and drives the
result with the same `webtest/js/protocol.js` that the TOOL-EEG-022 connectivity test program
and the study runner use, so a disagreement about framing, CRC, the ten-byte header, an
opcode or the acknowledgement layout fails the build instead of reaching a unit. It needs a C
compiler and Node 18 or later, and no hardware. On the image in this package it reports **49
passed, 0 failed** over nine groups, dispatching fourteen opcodes and exercising the S-01
charge interlock and two malformed-traffic cases. **Corrected 2026-09-02: was "32 passed, 0
failed over six groups, dispatching eleven opcodes".** The harness gained the calibration
read-back and ATECC config-zone groups, which is also where `0x4A` is pinned as the
calibration reader against `0x4B` as the config write, so a repeat of the provisioning opcode
collision fails the build. It is run, and its output filed, for every image
whose SHA-256 enters a unit record. It is a build gate and not a per-unit step; the per-unit
equivalent is T30, which runs the same protocol code from a browser against a real unit.

**Corrected 2026-09-02. Rev C's "the firmware has never been compiled for the target or run
on hardware, and five drivers are stubs" is superseded**, and what replaces it is narrower
than it sounds. The firmware **is built**: `firmware/release/` carries `bootloader.bin`,
`partition-table.bin`, `ota_data_initial.bin` and `eeg_field_kit.bin` with a
`manifest.json` of their SHA-256, produced by ESP-IDF **v5.2.5** for target **esp32s3**, the
application image 405,360 bytes on disk against a linked size of 405,245. The firmware has
also **run, under emulation**: `firmware/release/qemu_boot.log` is one full boot cycle on
`qemu-system-xtensa -M esp32s3` in which the bootloader reads this package's partition table,
the app loads from the factory slot, `app_main()` runs, and the microSD and ES8388 bring-up
paths degrade as written. It ends in an **abort and a reboot**, and that is the written
behaviour rather than a defect: QEMU has no octal PSRAM, so the 6 MiB ring buffer will not
allocate and FW-D13 refuses to continue silently. It has **never run on hardware**, no board
exists, and QEMU's esp32s3 machine emulates none of the peripherals this firmware talks to --
no octal PSRAM, no microSD, no ES8388, no ADS1299 -- so the run proves nothing about a
register value, a daisy-chain order or an SPI timing. A build is not a bring-up. Two things
in the image bear on this document and are recorded in RFQ-EEG-001 Rev E section 12 item 12:
**IRAM is 16,383 of 16,384 bytes used** (`firmware/release/size.json`), so any further
`IRAM_ATTR` code fails to link, and the sample-accurate tone start and the sub-sample onset
interpolation are written as **partial**, which is what T12b and T13 will be grading.

**The readiness gate above is therefore not met, and no step below moves out of DEFERRED.**
Condition (a) is met -- ESP-IDF v5.2.5, with `espressif/esp_tinyusb` pinned at `~1.4.2` in
`firmware/main/idf_component.yml` and resolved by `firmware/dependencies.lock` -- and so is
(e), at 49 passed and 0 failed. Condition (c) is met in part: the bicolour contact-light
phase driver is written (T11 Note 1), and so are the codec tone driver, the SDMMC append and
free-space calls, the ATECC608B serial read, the fuel-gauge read and the envelope onset
detector, but the **block-signing task is not** -- `firmware/main/main.c` line 832 emits
`FT_SIGNATURE` from a task that is marked "not shown". Conditions (b) and (d) are not
evidenced by a QEMU run. Until the gate is met, T6, T11, T12, T13, T14, T15, T16, T17,
T24, T26 and T28 are recorded as **DEFERRED** with the reason and the image hash, the
units are labelled "not for participant use", and the deferred steps are re-run in
Brussels before any Phase 2 release. A deferral is a tracked state, never a blank field.
`tools/DESIGN_FACTS.md` section 8 item 3, which this paragraph used to cite, still carries
the old sentence and is owed the same correction.

**The sentence "`lights_write()` and `lights_task()` are on/off only, so the bicolour phase
scheme is not implemented and T11 cannot pass until it is" is superseded on 2026-09-02.**
The E-27 phase driver is written: `firmware/main/main.c` now captures both halves of the
converter's lead-off status, computes a colour per site from them, and alternates the two
phases in `lights_phase()`. T11 is rewritten against what that code does and is no longer
held out of the flow by a missing driver -- it is deferred for the same reason as the ten
steps beside it, which is that **no unit exists to run an image on**. *Corrected 2026-09-02:
this sentence said "no image has been built for the target and no unit exists to run one on".
An image has since been built and booted under QEMU; the half of the reason that survives is
the half that matters here, which is that there is no hardware.* What the driver's arrival
does **not** close is stated in T11 itself: the red state cannot be produced on the image as
it stands, because the negative lead-off detectors are never enabled.

## 5. Equipment, required accuracy, and the calibration schedule

| Item | Required accuracy or specification | Example | Calibration |
|---|---|---|---|
| Digital multimeter, 6.5 digit, true RMS | DCV <= 0.01 % of reading at 1 V, 1 uV resolution; ACV <= 0.1 % from 10 to 100 Hz; 4-wire ohms <= 0.02 %, 100 mOhm range | Keysight 34465A | 12 months, traceable |
| Function generator | Frequency <= 1 ppm; amplitude stability <= 0.05 % per hour; 50 Ohm output; amplitude is **measured, never trusted** | Keysight 33500B | 12 months |
| DC bench supply | 3.900 V +/- 0.010 V, 1 A, current readback 0.1 mA | any lab supply | 12 months |
| Current shunt | 1.000 Ohm 0.1 %, 0.5 W, for J13 and J24 lines, in FIX-04/A | Vishay Y0785 | 12 months |
| Leakage measuring resistor | 100 kOhm 0.1 %, 25 ppm/degC, screened, in FIX-04/C | Vishay VHP4 | 12 months |
| Oscilloscope | >= 100 MHz, 4 channels, >= 1 GSa/s, timebase <= 25 ppm | any | 12 months |
| Insulation resistance tester | 500 V DC, range to 100 GOhm, +/- 5 % | Megger MIT525 | 12 months |
| Contact thermometer or thermal camera | +/- 2 degC from 20 to 120 degC | any | 12 months |
| Audio analyser or calibrated interface | level +/- 0.1 dB, residual THD+N <= 0.01 % | any | 12 months |
| Dummy load | **47.0 Ohm +/- 1 %**, 1 W, non-inductive, in FIX-02/D | any | verify at shift start |
| Artificial ear and sound level meter, class 1 | IEC 60318-1 coupler and its SLM mount. This is **FIX-02/C, and it is not yet built or priced**: JIG-EEG-009 section 7 records that it is in neither the FIX-02 bill of materials at that document's section 2.4 nor its section 6 cost tables. SLM +/- 1.0 dB at 1 kHz | B&K 4153 class | 12 months, T28 only -- and nothing is on a schedule until the coupler and the meter are bought (section 16 item 12) |
| Colorimeter head | RGB ratio repeatability <= 2 %, in FIX-01/E | TCS34725 class | verify against the reference card at shift start |
| 2.4 GHz receiver or SDR with near-field probe | noise floor <= -90 dBm over 2.400 to 2.4835 GHz | RTL-SDR class | annual functional check |
| Host PCs | Windows 11, macOS 14 or later, Ubuntu 22.04 or later | -- | -- |
| Host connectivity test program, **TOOL-EEG-022** (`webtest/EEG-Connectivity-Test.html`) | one self-contained file run from local disk in Chrome or Edge on Windows 10 or later or macOS 11 or later; no installation, no administrator rights, no network. File SHA-256 recorded | -- | its own self-checks S1 to S5 at the start of every run, filed with the result; the section 4 interop harness re-run for every firmware image |
| Host stream-decoding tool for T7 to T16, T26 and T27 | programme-supplied, version and SHA-256 recorded. **This tool does not exist yet**, and TOOL-EEG-022 is not it: the connectivity test program decodes no channel and takes no measurement (section 16 item 10) | -- | golden-vector self-test at shift start, once it exists |

Instrument asset numbers and calibration due dates are copied into every per-unit record.
An instrument out of calibration invalidates every record taken with it since its last
verified use; that is why the asset number is a record field and not a wall chart.

**Fixture verification.** JIG-EEG-009 self-test at the start of every shift: the FIX-01/F
divider ratio against the DMM, the three FIX-01/A reference resistors (**4k99, 10k0, 49k9**),
continuity of all twelve FIX-01/A pins, the three DIN plugs of FIX-01/B, the FIX-01/C
reference lead, and the two FIX-04/A shunts read 4-wire. Logged; a failed self-test halts the
line.

**Golden unit.** Unit **TIOV-B-0001** is retained by the programme and re-measured on the
fixture at the start of every build lot. Its T7 gains, T8 noise and T10 offsets are the
fixture's control chart. A gain drift above 0.2 % or a noise drift above 0.15 uV halts the
line.

## 6. Fixtures and test points

### 6.1 Fixtures -- the authoritative sub-assembly table

**This table is the authority for fixture names in the package.** The fixtures themselves are
designed, dimensioned, built and priced in **JIG-EEG-009**, which uses these designators and
no others. Four fixtures exist, FIX-01 to FIX-04, and every part of a fixture that a step, a
bill-of-materials line or a calibration entry needs to name has a letter here. There is no
second fixture namespace: the bare letters **H-A, H-B and H-C**, the coupler names **CPL-V
and CPL-R**, and the form **FIX-04/H-D** are all withdrawn, and so is the use of the word
"Part" for a fixture sub-assembly anywhere in the package.

| Sub-assembly | Mates | Contents | Steps |
|---|---|---|---|
| FIX-01/A | J14, 1x12, keyed, pin 1 marked E_Fz | eleven channel networks: 1000:1 tap, selectable **4k99 / 10k0 / 49k9** 0.1 % thin-film reference, short-to-common, open. Relay-switched, state readable by the host tool | T7a, T8, T9a, T10, **T11**, T22, T23 |
| FIX-01/B | J15, J16, J17 DIN 42802 1.5 mm, 12 mm pitch | three identical channel networks for EMG1 cheek, EMG2 submental, EMG3 laryngeal | T7b, T22, T23 |
| FIX-01/C | J22.2 (AGND_REF), second position TP13 | analogue reference lead, marked "ANALOGUE REFERENCE -- NOT DGND" | T7, T8, T9, T22 |
| FIX-01/D | all eleven J14 analogue pins and SRB1 | common-mode injection network, one source into all inputs through matched 100 Ohm | T9b |
| FIX-01/E | J30, 1x10 | TCS34725-class colorimeter head over the eight contact-light positions, reading the R/G ratio at each site. **It reads the colour; it does not set it** -- the colour is computed by the firmware from the converter's lead-off status, so the states are produced with FIX-01/A and the relay matrix (T11) | T11 |
| FIX-01/F | the FIX-01 injection input, with a DMM tap | the 1000:1 ratio divider, two cascaded stages, 100:1 then 10:1, feeding FIX-01/A, FIX-01/B and FIX-01/G | T7, T22 |
| FIX-01/G | J22, 1x3 | spare-channel injection for EOGIN1 (J22.1) and EOGIN2 (J22.3) | T7c |
| FIX-02/A | the boom capsule, windscreen removed | voice coupler, 2.0 cm3, delivering 70.0 dB SPL at 1 kHz at the capsule | T12a, T12b, T13 |
| FIX-02/B | the room-microphone port and its mesh | room coupler, 3.5 cm3, sealed over the port | T12a |
| FIX-02/C | the shipped headphone model | IEC 60318-1 artificial ear and the class 1 sound level meter mount | T28 |
| FIX-02/D | J27 headphone pigtail, and a scope tap | 47.0 Ohm load and the electrical-onset marker | T12, T13, T17 |
| FIX-03/A | DevKitC-1 UART USB-C port, card reader, host PC | flashing and provisioning nest | T5, T6, T16, T30 |
| FIX-03/B | J26, 1x6 | console and recovery lead. **It cannot enter download mode**, because GPIO0 is LED_SR_LATCH | T25, bench diagnosis |
| FIX-04/A | J13 and J24 JST PH pigtails | two 1.000 Ohm 0.1 % shunts, one in the battery line and one in the charge line | T00, T3, T4, T21 |
| FIX-04/B | host-side USB shell, VBUS, D+ and D- on the ADuM4160 | insulation head that reaches the module without touching the carrier | T20 |
| FIX-04/C | applied-part group and protective earth | 100 kOhm 0.1 % measuring resistor, screened, and the earth lead | T23 |
| FIX-04/D | 12-way electrode end, 10-way light end, three EMG snap leads | harness continuity and pull heads | WH-EEG-008 section 9, steps H1 to H10 |

Three consequences of this table are written out so they are not read as accidents. **The
shunts are FIX-04/A, not a FIX-01 sub-assembly**: they sit in the battery and the charge
lines, which is FIX-04's side of the instrument, and two documents already name them that
way. **FIX-04/C is a fixture and not a loose instrument**: the 100 kOhm resistor and its earth
lead are screened, serialised and self-tested with the rest of the set, because T23 is the
only routine per-unit safety measurement that exists and it cannot rest on whatever resistor
is on the bench that morning. **FIX-02/C has to be built, priced and calibrated, and
none of the three has happened yet**: the artificial ear and the class 1 sound level meter
that T28 needs are named in section 5 and belong to FIX-02, but JIG-EEG-009 section 7 states
that they are in neither the FIX-02 bill of materials at its section 2.4 nor the cost tables
at its section 6, so the one-off fixture-set price quoted there is short by that coupler and
that meter. The letter is settled and the hardware is not; it is open item 12 of section 16,
and it blocks the T28 type test rather than the per-unit line.

Rev B of this document used "Part A" to "Part G". They map as: A to FIX-01/A, B to FIX-01/B,
C to FIX-01/C, D to FIX-02/D, E to FIX-01/E, F to FIX-04/A, G to FIX-01/G. The LED
current-sense method once proposed for T11 is dropped in favour of the colorimeter head at
FIX-01/E, and the colorimeter is a FIX-01 bill-of-materials line, not an idea.

**Where things live in this document**, because several documents have cited the wrong
section of it. Fixtures are **section 6.1**. Test points are section 6.2. Equipment, required
accuracy and the calibration schedule are **section 5**. The requirements-to-test
traceability matrix is section 10. The test time and station plan is **section 11**. The
calibration-certificate template is **section 13**. The type tests, T28 among them, are
**section 14**. A citation to "TST-EEG-004 section 5" for the fixture table, to "section 10"
for the station plan, or to "section 13" for a type test is stale, and is corrected against
these numbers rather than the other way round.

FIX-01/F, the 1000:1 divider, is two cascaded ratio-matched stages, 100:1 then 10:1, output
impedance **18.0 Ohm**: the second stage is R103 180 Ohm over R104 20.0 Ohm and 180 || 20 is
18.0. Rev C said "about 90 Ohm" here, which was the **first** stage's 9.90 kOhm || 100 Ohm =
99.0 Ohm read as though it were the fixture's output; the buffer U1 stands between the two
stages, so the first stage's impedance never reaches the DUT. JIG-EEG-009 section 1.3 derives
the 18.0 Ohm and uses it throughout its accuracy budget, and that figure governs. Johnson
noise of 18.0 Ohm over 0.5 to 70 Hz is **0.0046 uV RMS** at 300 K (calculated; the 0.0102 uV
printed in Rev C is the 90 Ohm figure), negligible against the 1.0 uV limit of E-03. The DUT presents 68 kOhm in series into 10 nF
to AGND_REF (47 kOhm before ECO-EEG-024); at 10 Hz the capacitor is 1.59 MOhm, so the divider
is not loaded either way. Do not
"improve" the divider impedance.

### 6.2 Test points TP1 to TP18

RFQ E-28 asks for test points on SPI, DRDY, I2S, the three envelope outputs, all supply
rails and the analogue reference, numbered TP1 to TP18. This is the assignment, taken from
`design.py`. Coordinates are in the design source convention, **top-left origin, Y down**;
Gerber, drill and CPL flip Y with `y_out = 130.0 - y_design`, and that constant changed with
the board height.

| TP | Net | Zone | x, y (mm, design source) | Used by |
|---|---|---|---|---|
| TP1 | SCLK | digital | 66.0, 126.5 | T27b |
| TP2 | MOSI | digital | 71.0, 126.5 | bench diagnosis only |
| TP3 | MISO | digital | 76.0, 126.5 | bench diagnosis only |
| TP4 | DRDY | digital | 81.0, 126.5 | T27c |
| TP5 | I2S_BCLK | digital | 86.0, 126.5 | bench diagnosis only |
| TP6 | I2S_LRCK | digital | 91.0, 126.5 | bench diagnosis only |
| TP7 | ENV_STIM | analogue | 56.0, 80.0 | T12a, T12c |
| TP8 | ENV_VOICE | analogue | 56.0, 92.0 | T12a |
| TP9 | ENV_ROOM | analogue | 56.0, 104.0 | T12a |
| TP10 | AVDD | analogue | 54.0, 31.0 | T00, T3 |
| TP11 | AVSS | analogue | 54.0, 35.0 | T00, T3 |
| TP12 | DVDD3V3 | digital | 96.0, 126.5 | T3 |
| TP13 | AGND_REF | analogue | 54.0, 39.0 | T8, T19, FIX-01/C |
| TP14 | DGND | digital | 101.0, 126.5 | T19 |
| TP15 | VSYS | digital | 106.0, 126.5 | T3 |
| TP16 | V5V | digital | 111.0, 126.5 | T3 |
| TP17 | NC_DRDY2 | digital | 116.0, 126.5 | T27d |
| TP18 | CLK_ADS | digital | 121.0, 126.5 | T27a |

**E-28 is met in part, and the gap is stated here rather than in an annex.** Eighteen test
points exist, the three envelope outputs are on TP7 to TP9 and the analogue reference is on
TP13, but **CS, I2S_MCLK, I2S_DIN, I2S_DOUT, VBAT and VBUS_CHG are not brought to a test
point**, so "SPI", "I2S" and "all supply rails" are covered only in part. Closing that gap
needs six more pads and is an ECO against Rev C of the board, not a line decision. The
other half of E-28 is met without qualification: the **1x6 UART debug header at J26**
carries 3V3, DGND, UART0 TX, UART0 RX, EN and, on way 6, **NC_GPIO0**, a spare way, because
GPIO0 is committed to LED_SR_LATCH by ECO-EEG-009. The 2x5 1.27 mm JTAG/SWD header of
earlier drafts is **withdrawn**: the ESP32-S3 is programmed over UART0 and its native USB,
and no JTAG connector is fitted. Any note elsewhere calling this an "E-28 deviation" is
stale and is deleted.

## 7. Sampling rule

**Every step in section 8 is performed on 100 % of units, with one named exception: T28 is
a type test run once per lot.** There is no other sampling. The reasons, in order of
weight:

1. Each unit's own measured constants -- sixteen channel gains, three envelope scalings,
   three group delays, eight lead-off offsets and slopes, the headphone level, the acoustic
   clamp value -- are written into the device at provisioning and travel with it as study
   metadata. A sampled unit contributes nothing to the unit next to it.
2. Total fleet size is 25 to 50 (Phase 3 is 10 to 40 further kits). A c=0 attribute plan at
   that lot size gives no useful confidence, so sampling would buy nothing but a shorter
   test line.
3. The unit is loaned to a distressed participant and used unsupervised at home. The
   per-unit record is the only routine safety evidence that exists.
4. RFQ-EEG-001 section 9.3 makes acceptance in Brussels conditional on the per-unit record.

Sampling applies only outside this specification: incoming lots under QP-EEG-010, and the
type tests in section 14, which are once per phase or once per lot and are named as such.

## 8. The steps

Each step is one table. "Verifies" cites RFQ-EEG-001 requirement IDs. "Uncertainty" is the
expanded uncertainty at k = 2 unless stated. All expected values are **calculated**.

### T00 -- Incoming inspection of purchased modules and carrier passives

| | |
|---|---|
| Purpose | Reject a wrong-variant, cloned or damaged module before it is assembled into a unit |
| Verifies | E-01, E-18, E-24, E-21, S-04 (in part), S-05 |
| Equipment | Bench I2C/SPI adapter, esptool, DMM, camera |
| Fixture | Module bench adapters, FIX-04/A |
| Procedure | ADS1299 modules: photograph the package marking, read the ID register, measure the on-module AVDD and AVSS, confirm DAISY_IN and CLKOUT are exposed and record whether J5 needs a jumper. DevKitC-1: `esptool flash_id` must report 16 MB flash and 8 MB PSRAM. ADuM4160 module: part marking, host connector type recorded, no component bridging the barrier, supplier isolation certificate on file -- this is where the **2.5 kV RMS type-test certificate is collected**. ATECC608B: read the factory serial, confirm the config zone is UNLOCKED. Codec, gauge, charger, preamp, shift register, microSD breakout: functional presence and header pin order against J8, J12, J21, J19, J20. Where the charger and gauge arrive as two separate breakouts rather than the combined baseline assembly, confirm the Y jumper of ICD-EEG-006 section 3.3 is present, built and labelled. Cell: OCV 3.4 to 3.9 V, protection PCM present, UN 38.3 report and MSDS on file per lot. Carrier passives: verify C1 to C16 are **C0G by part number -- `Murata GCM1885C1H103JA16D`** -- and R1 to R16 are 0.1 % thin film |
| Limit | Every check pass; DevKit variant exactly N16R8; cell OCV in band; documents present |
| Uncertainty | Attribute checks. OCV +/- 0.5 mV; AVDD/AVSS +/- 1 mV |
| Record | Per module type: quantity, lot, pass/fail, ADS1299 marking photograph reference, DevKit flash and PSRAM sizes, ATECC factory serials, cell OCV values, isolator host connector type, certificate references |
| On failure | Quarantine the lot, raise a supplier NCR under QP-EEG-010. No lot enters SMT until its record is closed. **An X7R part in the C1 to C16 position is a hard reject**, checked by part number here, because T22 catches it only by a hundredth of a decibel at the fitted 68 kOhm -- see T22 Note 2. *Corrected 2026-09-02: this row read "because T22 no longer catches it at the fitted resistor value", which was written with 47 kOhm fitted. The instruction is unchanged: the part number is the control, not the measurement* |
| Note | The named ADuM4160 candidate presents a **USB-B** host receptacle where E-24 asks for USB-C. This is a **live non-conformance**, and the interim answer is the short USB-B-to-USB-C panel pigtail **WH-09** until an isolator module with a USB-C host connector is qualified. T00 records which connector the delivered module actually has |

### T0 -- Bare-board electrical test

| | |
|---|---|
| Purpose | Prove the fabricated board matches the released netlist before any part is placed |
| Verifies | E-07, E-08, S-03 (carrier contribution) |
| Equipment | Fabricator's flying-probe or dedicated fixture tester, IPC-9252B class 2 |
| Fixture | Fabricator's |
| Procedure | 100 % continuity and isolation test to the supplied IPC-D-356A netlist `kicad/gerber/EEG-CAR-01-IPC-D-356A.ipc`: **156 nets and 620 netlist pins**, which are the 620 of the board's 636 pads that carry a net (section 1), on four layers. The same file also carries **552** via records, so a fabricator who probes vias as well tests **1 172** points (620 pads + 552 vias; counted in `kicad/gerber/EEG-CAR-01-IPC-D-356A.ipc`, 788 type-317 plus 384 type-327 records). *Corrected 2026-09-02: was "551 via records ... 1 171 points", one short on each, and SIM-EEG-018 Rev A carries the corrected pair.* Then four dedicated checks: (a) isolation AGND_REF to DGND -- on a bare board R90 does not exist, so this is the "R90 lifted" measurement taken without any rework, and it must be made against **both inner reference planes**, not only the outer layers; (b) isolation HARN_SHIELD to DGND and to AGND_REF; (c) no conductor of **any of the four layers** inside the isolation keep-out defined in DSN-EEG-003 section 3.3, checked against the copper plots of L1, L2, L3 and L4; (d) the four 3.2 mm M3 holes at (5,5), (145,5), (5,125) and (145,125) and the six 1.50 mm DIN retention holes are unplated (ECO-EEG-012) |
| Limit | Continuity <= 10 Ohm, and <= 5 Ohm on VBAT, VSYS, V5V, DVDD3V3, DGND, AGND_REF; isolation >= 10 MOhm at 100 V, and >= 100 MOhm at 250 V for AGND_REF to DGND; no copper in the keep-out on any layer; NPTH holes unplated |
| Uncertainty | Tester repeatability, typically +/- 2 % of reading; well inside a 10 Ohm / 10 MOhm decision |
| Record | Fabricator's ET certificate per lot, board serial or panel position, the four dedicated check results, the stack-up as built against the 1.60 mm +/- 10 % specified, and the netlist file hash the test was run against |
| On failure | Board scrapped by the fabricator. A systematic failure of check (c) or (d) is a Gerber or drill-file escape and stops fabrication release pending a re-issue. A failure of check (a) that appears only on the inner layers is a plane-split escape and is the failure mode the four-layer stack was adopted to make visible |
| Note | **T0 cannot be run yet, because no board has been fabricated.** That is now the only reason it cannot be run. The Rev B DRC report records **zero violations**, all 145 nets connected, every net one connected copper island and both inner planes continuous under the analogue zone, so the ECO-EEG-016 section 3 gate is met and the data is **released for review under RFQ-EEG-002A**. **Fabrication release awaits that review**: the routing came from the programme's own tools, no human layout engineer has looked at it, and **169 of its connections are relaxed** to the minimum conductor or the minimum gap rather than the preferred 0.25 mm width. The same report records the isolation strip **clear of copper on all four layers**, no width, annular-ring, hole-size, edge, NPTH, clearance or via keep-out violation, and each reference plane as one continuous island per net -- which is what check (c) will confirm on a fabricated board, and is not the same thing as having measured it |

### T1 -- Visual and AOI

| | |
|---|---|
| Purpose | Catch workmanship and placement defects while rework is still cheap |
| Verifies | E-07, E-28, and IPC-A-610 class 2 as called by DSN-EEG-003 |
| Equipment | AOI machine or 10x stereo microscope, calibrated illumination |
| Fixture | None |
| Procedure | Inspect to IPC-A-610 class 2. Explicit checks beyond the general standard: polarity and pin-1 orientation of every socket strip (pin 1 is the square pad, marked on the legend); U1 to U3 OPA4376 orientation; **D1 to D16 are BAV99** and are checked for orientation as clamp pairs; **D20, D40 and D60 are BAT54S**, with **BAT54S pin 3 on the op-amp output** (ECO-EEG-005); D23 is a BAV99; R89 **not** populated (DNP); R90, R91, R92, R93 each fitted once and never bridged with a wire or a solder blob; R94 and R95, the I2C pull-ups added by ECO-EEG-021, both fitted; the three 1.0 mm fiducials with 3.0 mm mask openings added by ECO-EEG-020 present and unobscured; TP1 to TP18 present and clean against the table in section 6.2; the legend carries the board part number, revision B and the date code |
| Limit | No class 2 defect; every explicit check pass |
| Uncertainty | Attribute inspection. Operator agreement is the dominant term; two-person check on the first five boards of a lot |
| Record | Pass or fail, defect codes, images of any rework site, operator ID |
| On failure | Rework per QP-EEG-010, maximum two hand-rework cycles per site. Thin-film R1 to R16 are re-measured to 0.1 % after any rework at their site. **A BAT54S found at any of D1 to D16 is a hard reject, not a rework**: Schottky leakage across a 68 kOhm series resistor is an offset error on a 10 uV input |
| Note | The board is **not conformally coated** for Phases 1 and 2. That is a decision, not a deferral: the board lives inside a gasketed enclosure, and masking 30 connectors and a socketed DevKit costs more than the coating buys. It is revisited before Phase 3 if a unit returns with corrosion |

### T2 -- Module seating and keying

| | |
|---|---|
| Purpose | Prove every module is present, correctly keyed and electrically connected |
| Verifies | E-01, E-13, E-18, E-24, E-09 |
| Equipment | DMM in continuity mode |
| Fixture | None |
| Procedure | With power off, confirm the **twelve module assemblies on MP-01** are present with keyed jumpers seated, and the DevKitC-1 is fully inserted in J6 and J7 (row spacing 22.86 mm, ECO-EEG-008) -- thirteen module assemblies in total. Confirm the printed keying shroud **WH-KEY-01** is fitted over every carrier socket that ICD-EEG-006 section 6 lists as taking a jumper, and that each module-end connector is either a shrouded polarised IDC header or is pin-1 marked and labelled. Ring out one supply and one signal pin per jumper: J1.1 to module DVDD3V3, J2.1 to IN1, J23.1 to AVDD, J3.1, J4.1, J29.1, J8.1, J10.1, J11.1, J12.1, J19.1, J20.1, J21.1, J25.1, J28.1 |
| Limit | All present and continuous, < 1 Ohm per checked pin; every jumper keyed at both ends |
| Uncertainty | Attribute |
| Record | Pass or fail, plus the module serials or lot codes where the module carries one |
| On failure | Re-seat, maximum two insertion cycles per socket, cycles logged. A socket that has taken two cycles and still fails goes to MRB |

### T3 -- Power-on current and DevKit regulator temperature

| | |
|---|---|
| Purpose | Detect a short, a wrong regulator or an unexpected load before any functional test, and measure the thermal question the DevKit's 3V3 rail leaves open |
| Verifies | E-22, E-25 |
| Equipment | Bench supply 3.900 V +/- 0.010 V; 1 Ohm 0.1 % shunt and the 6.5-digit DMM; contact thermometer or thermal camera |
| Fixture | FIX-04/A on J13 |
| Procedure | Battery disconnected. Apply 3.900 V at J13. Record current at idle after 60 s settling, then command a recording session at 1000 Hz and record current after a further 60 s. Measure DVDD3V3 at TP12, VSYS at TP15, V5V at TP16, AVDD at TP10 and AVSS at TP11. Then, **with the pod closed**, run 30 minutes at 1000 Hz and record the case temperature of the DevKitC-1's on-board 3.3 V regulator |
| Limit | Idle < 90 mA; recording at 1000 Hz < 150 mA; rails within 3 %; **regulator case temperature < 85 degC** |
| Uncertainty | Shunt 0.1 % + DMM 0.01 % + supply setting 0.26 %, combined 0.28 %, U(k=2) = 0.56 %, i.e. +/- 0.8 mA at 150 mA. Temperature +/- 2 degC |
| Record | Two currents in mA to 0.1 mA, five rail voltages, regulator case temperature in degC, supply voltage as measured, ambient temperature |
| On failure | Above the current limit: inspect for a short at the analogue rails, do not power a second time until the fault is found. Below 20 mA at idle: a rail is not starting; check R86 and the J25 buck-boost |
| Note | The carrier draws a **calculated 288 mA worst case** from the DevKit's on-board regulator. That is inside its rating but dissipates about 0.5 W inside a closed pod, and **this is not solved, it is measured**. If the case temperature exceeds 85 degC on the Phase 1 prototypes, a 3.3 V regulator on the carrier fed from V5V is an ECO against Rev C of the board |

### T4 -- Charge current with a session active

| | |
|---|---|
| Purpose | Prove the charger is actually off while a session runs |
| Verifies | S-01, E-23 (in part) |
| Equipment | 1 Ohm shunt, 6.5-digit DMM (10 uA resolution at 10 uV) |
| Fixture | FIX-04/A on J24 and J13 |
| Procedure | Battery fitted. Start a session with VBUS absent. Apply 5.00 V at J24 through the shunt. Measure the current into VBUS_CHG and the net current at J13 for 60 s |
| Limit | Charge current < 1 mA while the session is active |
| Uncertainty | Shunt 0.1 %, DMM 10 uV, combined U(k=2) < 30 uA. TUR against 1 mA is 33:1 |
| Record | Charge current in mA, plus the negative control (session inactive, charging permitted) so a dead charger cannot pass by accident |
| On failure | Quarantine, do not rework and re-test in place. A failed interlock is a safety nonconformance that feeds RISK-EEG-011 |
| Note | E-23 requires a charger IC with thermal regulation and **no charging above 45 degC**; T4 tests the interlock, not the temperature. **The 45 degC inhibit is not tested and cannot be, because there is no NTC net in `design.py` and no thermistor way on J12 or J13.** S-04's thermistor-monitored charging is **not met and stays not met**; it is an open hardware item carried in DSN-EEG-003 section 11 and RISK-EEG-011 |

### T5 -- USB enumeration

| | |
|---|---|
| Purpose | Prove the host link works on every supported operating system with no driver installation |
| Verifies | F-01, F-02, F-03, F-04, E-24 |
| Equipment | Three host PCs; one of the two A-07 cables shipped with the kit |
| Fixture | FIX-03/A. **The host connector is the USB receptacle on the ADuM4160 module, presented through a gasketed aperture in POD-P1.** It is a socket, not a captive cable; WH-08 and the cable gland are deleted from the Phase 1 build |
| Procedure | **T5a**, before provisioning: connect to Windows 11, macOS and Linux in turn; confirm a CDC-ACM port appears and a WinUSB-bound vendor interface is visible with no driver prompt and no manual action; record the enumerated VID and PID. **T5b**, after T6: re-enumerate once and confirm iSerialNumber equals the unit serial in the form `TIOV-B-nnnn` and matches the label and the calibration record character for character |
| Limit | Both interfaces visible on all three hosts with no driver installation; VID and PID equal to the values programmed in T6; iSerial equal to the unit serial |
| Uncertainty | Attribute |
| Record | Pass or fail per host with the OS build string, VID, PID, iSerial, and the descriptor dump saved by the host tool; and whether the WH-09 USB-B-to-USB-C pigtail was in the path |
| On failure | Descriptor or binding failure is a firmware defect, not a build defect: hold the unit, report the descriptor dump to the programme. A failure on one host only is recorded with that host's OS build |

### T6 -- Provisioning

| | |
|---|---|
| Purpose | Give the unit its identity and write its measured constants into it |
| Verifies | E-21, F-03, F-18 |
| Equipment | Host PC, the programme's provisioning script |
| Fixture | FIX-03/A |
| Procedure | Run the provisioning script: generate the P-256 key pair inside the ATECC608B, export the public key and the device serial, program VID, PID, the unit serial `TIOV-B-nnnn` and the hardware revision, write the calibration constants measured in T7, T10, T12, T17 and T28, then lock the configuration zone and read back to prove the lock took. T6 therefore runs **after** the characterisation steps; only T5a and T30a precede it |
| Limit | Key generated, public key exported, lock confirmed by readback, constants read back byte-identical to those written |
| Uncertainty | Attribute |
| Record | ATECC factory serial (18 hex), uncompressed P-256 public key in PEM, its fingerprint **as defined in FW-EEG-001 section 7** and exactly as printed on the label, unit serial, VID, PID, hardware revision, the full constant block, lock confirmation |
| On failure | A locked config zone cannot be undone. A failed lock scraps the ATECC module; a replaced ATECC module means a new identity, a new label and a re-issued record under the same unit serial |

### T7 -- Front-end gain

| | |
|---|---|
| Purpose | Measure the absolute gain of every channel and the matching between channels |
| Verifies | E-04 (matching within 0.5 %), E-01, E-02, F-18 |
| Equipment | Function generator; 6.5-digit DMM to **measure** the divider input; host test tool |
| Fixture | FIX-01/A, FIX-01/B, FIX-01/C, FIX-01/F and FIX-01/G. All channels of a group are driven simultaneously through the relay matrix so the record length is spent once, not eight times |
| Procedure | 10 Hz sine through the 1000:1 divider. **T7a**, eight EEG channels at J14.1 to J14.8, gain 24, at 1 mV (60 s), 100 uV (60 s) and 10 uV (240 s). **T7b**, three EMG channels at J15, J16, J17, gain 12, same levels and record lengths. **T7c**, two spare channels at J22.1 and J22.3, 100 uV only, 60 s. Estimator in all cases: coherent single-bin FFT at the generator frequency, rectangular window, an integer number of cycles, bin width 1/T; the tool reports amplitude, phase, residual and the in-band noise used for the uncertainty |
| Limit | **Matching** between the eight EEG channels within 0.5 % after calibration, **at the 100 uV and 1 mV points only**. The 10 uV point is a **linearity check with a +/- 5 % limit**; the 0.5 % matching limit of E-04 does not apply there and the uncertainty budget will not support it. Absolute gain is recorded and becomes the F-18 constant, not a pass or fail |
| Uncertainty | See section 9.1. U(k=2) = 0.134 % at 100 uV and 1 mV (TUR 3.7:1 against 0.5 %); **U(k=2) = 0.22 % at 10 uV**, which JIG-EEG-009 section 1.4 derives and which governs (TUR 23:1 against 5 %). Any document labelling that 0.22 % as a 1 sigma figure is wrong |
| Record | 8 x 3 EEG gains, 3 x 3 EMG gains, 2 spare gains, all in ppm of nominal; sixteen gain constants; the measured divider input voltage at each level; generator frequency; record lengths |
| On failure | One channel out of family: inspect its R / D / C protection group, which must sit in a straight line from the harness to the module. Two or more: layout escape, MRB. A channel-9 gain reading 24 rather than 12 means the daisy order is reversed -- see T27 |
| Note | T7c exercises the two spare channels, but **the EOG panel sockets are not fitted in a standard build**. J22 exists and the two channels are protected; the panel sockets, their cable and their drawing are a Phase 2 option with no part number yet (PARTS-EEG-019) |

### T8 -- Noise floor

| | |
|---|---|
| Purpose | Measure the input-referred noise the participant's data will actually carry |
| Verifies | E-03 |
| Equipment | Host test tool; screened bench |
| Fixture | FIX-01/A and FIX-01/C, relay matrix in the short-to-common position |
| Procedure | Battery only, USB disconnected, 30 min warm-up. Short E_Fz to E_F7 and REF_L, REF_R **at the J14 pins** to the FIX-01/C AGND_REF lead, so R1 to R10 and their 10 nF are in circuit -- that is the chain the participant sees. Record 60 s at 1000 Hz. Remove DC and linear drift, apply a 4th-order zero-phase Butterworth band-pass 0.5 to 70 Hz, bin-exclude 50 Hz and 100 Hz, compute RMS over the whole record and over ten 6 s epochs |
| Limit | <= 1.0 uV RMS on each EEG channel; pass on the median epoch. **Calculated expectation 0.31 uV RMS** with the 68 kOhm now fitted (ECO-EEG-024, applied in `tools/design.py` 2026-09-02); it was **0.27 uV RMS** at the 47 kOhm this row used to name as fitted, and that figure is now the superseded one. Either way the limit is met with margin. The derivation of both lives in RISK-EEG-011 section 4 and is not repeated here; **RISK-EEG-011 has not yet been restated against the applied ECO** |
| Uncertainty | Estimator 0.8 % (2BT = 8340 independent estimates over 60 s), band definition 2 %, gain calibration 0.13 %; combined 2.2 %, U(k=2) = 4.3 %, i.e. +/- 0.04 uV. TUR against 1.0 uV is 23:1 |
| Record | 8 whole-record RMS values, 8 epoch-median values, all in uV; the excluded bins; ambient temperature; the fitted series-resistor value |
| On failure | Above 1.0 uV: check the FIX-01/C reference lead is on AGND_REF and not DGND, then re-run. A genuine failure above 0.5 uV with the expectation at 0.27 uV points at a cold joint on an R1 to R16 site or a damaged clamp diode |

### T9 -- Crosstalk and common-mode rejection

| | |
|---|---|
| Purpose | Prove one channel does not contaminate another, and that mains common mode is rejected |
| Verifies | E-04 (crosstalk, as restated by ECO-EEG-026). **The CMRR limit below has no requirement behind it.** RFQ section 9.1 item 6 names CMRR as one of the things T9 measures but states no figure, and no E-item in RFQ section 5 states one either; the >= 100 dB is set by this document and is unsourced until an E-item exists (section 16 item 15). Rev C cited "RFQ section 9.1 item 4", which is the seating, power-on, thermal, charge and interlock item and carries no CMRR at all |
| Equipment | Function generator; host test tool; screened bench |
| Fixture | FIX-01/A, FIX-01/C and FIX-01/F for T9a; **FIX-01/D** for T9b, the common-mode network that drives all eleven J14 analogue pins and SRB1 from one source through matched 100 Ohm |
| Procedure | **T9a crosstalk**: 1.000 mV RMS at **50.000 Hz** into channel 1, all other channels held at the fixture common; record **600 s** at 1000 Hz; coherent single-bin FFT at 50.000 Hz on every victim channel. Repeat with the aggressor on channel 8 to catch coupling at both ends of the analogue zone. Run the same 600 s record once with the aggressor off and report that bin as the ambient floor. **T9b CMRR**: DUT on battery, USB disconnected, 1 V RMS at 50 Hz common mode; record 60 s; CMRR = 20 log10(1 V / differential response) |
| Limit | **Crosstalk < -80 dB, measured on the carrier**; **CMRR >= 100 dB -- a provisional limit that this document sets and no requirement carries.** No E-item in RFQ section 5 states a CMRR figure, so the >= 100 dB stands only until section 16 item 15 closes, either by an E-item that states the figure or by T9b recording CMRR with no pass/fail decision. The detection floor and the aggressor-off ambient bin must be recorded next to every crosstalk value, and each must sit at least 10 dB below the -80 dB decision |
| Uncertainty | Crosstalk: U(k=2) = 0.4 dB at -80 dB with a 600 s record, where the floor is -106.2 dB (section 9.3) and the margin is 26.2 dB. CMRR: source amplitude 0.5 % and injection-resistor matching; U(k=2) = 0.5 dB |
| Record | 8 crosstalk values in dB each with its detection floor and its aggressor-off ambient bin, for both aggressor positions; 8 CMRR values in dB; the aggressor amplitude **as measured** |
| On failure | One channel below limit is a rework candidate. Two or more is a layout escape and goes to MRB, because the routing has not been reviewed by a human layout engineer (DESIGN_FACTS section 8 item 4) |
| Note | **E-04's original -100 dB is withdrawn and is not tested, because it is neither achievable nor measurable here.** A 60 mm un-interleaved ribbon cannot deliver it, and -100 dB sits some 40 dB below this instrument's own noise floor. ECO-EEG-026 restates E-04 as -80 dB at 50 Hz on the carrier, and the ribbon's own contribution is characterised once on the first prototype as a type test (section 14). Injecting at 50 Hz on a screened bench is deliberate: the generator is locked, so its energy sits in one 1.667 mHz bin, while mains wanders by tens of millihertz and spreads across hundreds of bins. The aggressor-off record is what proves that separation held on the day |

### T9c -- Contact-light interference on the electrode channels

| Field | Value |
|---|---|
| Verifies | **E-30** (added 2026-09-02). The contact lights must not corrupt the measurement they report |
| Why it exists | E-27 drives the lights from the converter's own lead-off measurement, so a lit light means a live measurement on the same electrode: the two are concurrent by design, and only recording blocks are exclusive with them. WH-EEG-008 section 4 used to justify leaving WH-02 unscreened by asserting that no electrode channel is ever live while the light cable switches; that assertion was wrong and is withdrawn. The design's controls -- two occipital entries, channel A and channel B at minimum 6 mm centre to centre, the LED_GND guard conductor down the middle of the WH-02 bundle, J30 in the digital zone, source impedance below 1.1 kOhm -- are real, and none of them had ever been measured. **T9a does not cover this**: it injects channel to channel on the carrier through FIX-01, with no harness fitted and the lights dark |
| Type | **Type test, on the first prototype of each build standard, plus any unit whose harness is rebuilt.** Not per unit |
| Fixture | The assembled helmet with WH-01 and WH-02 fitted in their own channels -- **this test is void on a bare carrier**, because the coupling it measures is in the harness and at the HM-04 body, where the frame's 6 mm separation does not apply and the electrode conductor is at full electrode impedance because R1-R16 are on the board |
| Procedure | Electrodes shorted to the fixture common at the cup through 10 kOhm each, to present a realistic source without a person in the loop. Record 300 s at 1000 Hz with **all eight lights dark** (`CMD_LIGHTS` off), then 300 s with the lights enabled and the phase driver running. Compute input-referred noise in 0.5-70 Hz for each of the eight EEG channels in both records. The added noise is the quadrature difference, sqrt(lit^2 - dark^2), per channel. **What "every site lit" now means is set by the driver and not by the operator**, and it is not the same aggressor in the two states the fixture can produce: with a 10 kOhm source every site reads contact-good and shows **green**, so the eight LED lines sit static and only LED_V alternates, whereas the maximum-switching case is every site **amber**, in which all eight lines swing 0x00 to 0xFF against LED_V every half-phase. Amber requires every site to be in lead-off, which is not the realistic source this test is built on, so the two cannot be had in one record. Record the green case, which is the condition a worn unit is actually in, and state it as such |
| Limit | **Added noise below 0.5 µV RMS in 0.5-70 Hz on every channel**, which is half the 1.0 µV RMS E-03 allows the channel in the same band. Also record the bin at the **measured alternation frequency, about 250 Hz** (T11 Note 2: the compiled `LIGHT_PHASE_HZ` is 240 and the FreeRTOS tick quantises the half-phase to 2 ms, so the alternation is 4 ms and 250 Hz), and its first two harmonics explicitly: a clean total with a visible line at the phase frequency is a coupling path that happens to be small today and will not stay small across builds. **"the 240 Hz bin" of Rev C is superseded on 2026-09-02**; report the bin at the rate the unit actually alternates at and state that rate beside it |
| Uncertainty | Dominated by the 300 s record length and the stability of the dark reference; state the dark-record noise beside every result. Where lit and dark differ by less than the measurement uncertainty, report "below the floor" and give the floor, rather than a difference that is arithmetic on noise |
| Record | 8 added-noise values in µV RMS with the dark reference beside each; the alternation-frequency bin and two harmonics per channel; whether the phase driver was running, and which colour state the eight sites were in (see below) |
| On failure | Screen WH-02 and re-run, or separate channel B further, and raise an ECO. Do not accept a failing unit on the argument in WH-EEG-008 section 4; that argument is what this test exists to check |
| Note | **Rev C's "this test cannot be run to its full intent until the E-27 bicolour phase driver is written" is superseded on 2026-09-02.** The driver exists (T11 Note 1) and the alternation happens, so the limit is now written against something the unit does. What is still a lower bound is the **worst case**, for the reason in the procedure row: the amber state is the one that swings all eight LED lines, and it is only reachable with every site in lead-off, which is not the source condition this test is measured at. A result taken in the green state is reported as what it is -- the coupling with the common alternating and the site lines static -- and whether an amber-state record is worth taking on an open input, where the victim channel is no longer at a realistic source impedance, is for TST-EEG-004's owner with the E-27 owner to decide before the first prototype is characterised. It is not decided here |


### T10 -- Lead-off calibration

| | |
|---|---|
| Purpose | Turn the raw lead-off reading into the contact impedance the participant is shown |
| Verifies | E-06, E-07, F-18 |
| Equipment | Host test tool |
| Fixture | FIX-01/A reference resistors, **4k99 / 10k0 / 49k9, 0.1 % thin film** (Vishay TNPW0603 class) |
| Procedure | Fix the excitation at LOFF_MAG = 6 nA and LOFF_FREQ = **7.8 Hz** (at 7.8 Hz the 10 nF shunt is 2.041 MOhm, against 510 kOhm at 31.2 Hz) and confirm the register readback. Record the OPEN position, then **4k99, 10k0 and 49k9** on each of the eight EEG channels, 10 s each. Least-squares fit gives a per-channel offset R_off and slope k. Calculated raw expectations with the fitted **68 kOhm** in series (ECO-EEG-024, applied 2026-09-02) and the 10 nF shunt (2.041 MOhm at 7.8 Hz) in parallel: **4k99 reads 70.5 kOhm, 10k0 reads 75.1 kOhm, 49k9 reads 111.5 kOhm**, and R_off is fitted against 68 kOhm. *Corrected 2026-09-02: this row named 47 kOhm as fitted and its 50.7 / 55.5 / 92.5 kOhm as the live expectations, with the 68 kOhm set held out as conditional. The two sets of figures are unchanged; which one is live has swapped, and the 47 kOhm set is now the superseded one* |
| Limit | R_off within the fitted series-resistor value +/- 5 % (a wrong or badly joined R1 to R8 shows here), and after correction each of the three reference points reported within 15 % |
| Uncertainty | Reference resistors 0.1 %, shunt model 0.5 %, converter estimator 1 %; U(k=2) = 2.3 %. TUR against 15 % is 6.5:1 |
| Record | 8 x 3 raw impedances plus the OPEN residual, and 8 pairs of (R_off, k) -- 32 raw values and 16 constants |
| On failure | R_off outside +/- 5 % on one channel: rework that protection group. On all channels: suspect the excitation register or the fixture, not the board |
| Note | The FIX-01/A references are the **E96 values 4k99, 10k0 and 49k9**, which is what a 0.1 % thin-film part is actually made in; "5 k / 10 k / 50 k" was Rev B's rounding of them. The rounding mattered at one point only, and the arithmetic is now run at the fitted 68 kOhm: 49k9 in series with 68 kOhm, shunted by the 10 nF, reads **111.5 kOhm**, 5.5 % low against the 117.9 kOhm of the bare pair and still well inside the 15 % limit. *Corrected 2026-09-02: the figure this note used to quote was the 47 kOhm one, "49k9 in series with 47 kOhm reads 92.5 kOhm and not the 92.6 kOhm that 50 k would give". That remains the right contrast against the rounded name and is why the E96 values are used; it is no longer the fitted case.* The ECO-EEG-024 expectations rose by about 19 kOhm rather than the full 21 kOhm of the resistor change, because the 2.041 MOhm shunt compresses the top of the range |

### T11 -- Contact lights

| | |
|---|---|
| Purpose | Prove the eight helmet lights show the right colour at the right site, and are dark when they must be |
| Verifies | E-27, and the fitting procedure of DSN-EEG-002 |
| Equipment | Colorimeter head; host test tool |
| Fixture | FIX-01/E on J30, TCS34725 class, over the eight contact-light positions, **and** FIX-01/A's reference resistors switched by the FIX-01 relay matrix, which is what puts a site into and out of lead-off. The colour is not commanded, so the fixture that sets it is the electrode fixture and not the light fixture |
| Procedure | **The colour is computed, not written.** `lights_task()` reads the converter's own lead-off status and derives one colour per site from it; the host's only control is `CMD_LIGHTS`, which enables and disables the whole set. The three states are therefore produced at the electrode inputs. **Green:** neither lead-off detector of the site has let go -- present 10k0 from FIX-01/A at all eight sites. **Amber:** exactly one of the two has let go -- open one channel at a time at the relay matrix. **Red:** both have let go; **see Note 3, which is why this state cannot be produced on the image as it stands.** The driver lights green in phase A only (LED_V high, the site's shift-register output low), red in phase B only (LED_V low, the output high) and amber in both, alternating at `LIGHT_PHASE_HZ`. Read the red-to-green channel ratio R/G at FIX-01/E for each state, 300 ms integration, one site at a time on the indexed carrier (JIG-EEG-009 section 1.7). Then the two dark states: **at boot**, before the host has enabled anything, and **during a recording block** (E-27). Both are the same branch of `lights_task()`, which writes the shift register clear and returns LED_V to an **input** rather than driving it low: with the common floating, no current can flow through any site whatever the register holds, and an input is the state GPIO48 already holds at reset. Record the clear channel for both |
| Limit | Mapping correct site for site, LED1 to LED8 against helmet sites 1 to 8; green state ratio R/G <= 0.30; red state R/G >= 3.0; amber state 0.6 <= R/G <= 1.7; both dark states below 2 % of the green-state luminance. The limits are unchanged. **The red-state limit stands as written and is recorded DEFERRED, with Note 3 as the reason, on any image that does not enable the negative lead-off detectors** -- a state that cannot be produced is not a state that passed |
| Uncertainty | Colorimeter ratio repeatability 2 %; the decision bands are wide by design, so the measurement is an attribute test with a numeric trail. The alternation frequency does not enter the ratio: the two half-phases are equal, so the duty is 50/50 whatever the tick quantisation of Note 2 does to the rate |
| Record | 8 sites x 3 colour ratios, 2 dark-state luminances, mapping pass or fail, LIGHT_PHASE_HZ as read back |
| On failure | Wrong site: the J30 harness or the shift-register wiring; check R70 to R77 and the J19 to J30 path. All sites dark: R87 (OE) or R88 (MR). **Every site amber where green was expected** is the lead-off excitation and not the light -- confirm T10's 6 nA at 7.8 Hz is running before anything is touched in the harness. Lights on at boot is a **safety-relevant** failure of the LED_V scheme and goes to MRB, not to rework |
| Note 1 | **The bicolour phase driver exists as of 2026-09-02, and this step is written against what it does.** Rev C's "this step cannot pass today ... `lights_write()` and `lights_task()` in the current firmware are on/off only and the bicolour phase scheme is specified and not yet coded" is **superseded on that date**. `firmware/main/main.c` reads the converter's positive-side lead-off comparator at **two thresholds** and derives the colour per site as: trips neither **green**, trips only the sensitive threshold **amber**, trips both **red**. That is the converter's own lead-off measurement, which is what E-27 asks for, and the middle state is measured rather than invented. **Corrected again 2026-09-02 (FW-D17):** this sentence read that the driver used both halves of the status word, LOFF_STATP and LOFF_STATN. It did, and that was the defect -- see Note 3. T11 is still DEFERRED under the section 4 gate. **Corrected 2026-09-02: the reason is now "no unit exists", not "no image has been built for the target"** -- an image has been built with ESP-IDF v5.2.5 and booted under QEMU, which emulates no LED, no shift register and no converter, so nothing in that run has seen a light. T11 has never been run. It is no longer deferred for want of a driver either |
| Note 2 | **The alternation is about 250 Hz, not 240 Hz, and the document owns that rather than quoting the constant.** `LIGHT_PHASE_HZ` is 240, so a half-phase is 1/480 s = 2.083 ms; the driver delays with `vTaskDelay`, so the half-phase quantises to the FreeRTOS tick, which is 2 ms at the 1 kHz tick. Two equal 2 ms half-phases are a 4 ms period, that is **250 Hz**, 4 % above the compiled constant. E-27's requirement is "above 100 Hz" and 250 Hz meets it with 2.5x to spare; the duty stays 50/50 so no colour shifts; and the colorimeter reads a ratio over a 300 ms integration, which at 250 Hz is 75 whole periods exactly, so the ratio does not depend on where the window starts. Exactly 240 Hz would need a hardware timer rather than a task delay. **The record carries `LIGHT_PHASE_HZ` as read back, which is the compiled 240 and not the rate the hardware produces**; if the measured rate is ever to be recorded per unit, section 12's field count and the `records/` schema move in the same change |
| Note 3 | **FINDING RAISED AND CLOSED HERE, 2026-09-02 (FW-D17). The red state was unreachable; it is not any more, and the fix is not the one this note first proposed.** As raised: `main.c` wrote `LOFF_SENSP` = 0xFF and never wrote `LOFF_SENSN`, so LOFF_STATN read zero on every channel, the red term `LOFF_STATP AND LOFF_STATN` was always zero, and **a site with no contact at all displayed amber, never red**. This note then asked whether enabling `LOFF_SENSN` was the answer. **It was not, and the note's own second paragraph is why:** `MISC1` = 0x20 makes SRB1 the reference for all eight channels, and J2 carries IN1 to IN8 with one shared SRB1 and BIASOUT, so the montage is single-ended and an enabled LOFF_SENSN would have reported the one shared reference eight times over rather than eight sites separately. There is no per-site negative electrode to detect. **What was done instead:** the driver sweeps `COMP_TH` -- the positive-side comparator's threshold -- between a sensitive setting and an insensitive one and latches LOFF_STATP at each, so green is a site that trips neither, amber a site that trips only the sensitive threshold, and red a site that trips both. The insensitive set is a subset of the sensitive one, so the three states are exhaustive and cannot overlap. `tools/simulate_production.py` now carries a check that fails if any colour depends on state `ads_init()` never enables, and that check fails against the pre-FW-D17 source. **What T11 still cannot fix:** the two `COMP_TH` values are the ADS1299's documented endpoints, not measured trip points, so the reference resistances that put a site in each band are unknown until the first unit is characterised. T11 exercises all three colours and the dark states; the **resistor values** in its procedure are provisional and are set at first bring-up, with the firmware owner and E-27's owner in DSN-EEG-003 section 11 |
| Note 4 | The current per site is 1.3 mA -- (3.3 - 2.0) / 1000 with the 1 kOhm R70 to R77 -- and 10.4 mA total from GPIO48. That total is the instantaneous figure with all eight sites lit in one phase; with the phases alternating, a green or a red site is lit for half the period and an amber site in both, which is calculated and not measured |

### T12 -- Envelope channels, scaling and group delay

| | |
|---|---|
| Purpose | Characterise the three envelope channels and measure the delay the study must subtract |
| Verifies | E-11, E-12, E-14, E-15, E-16, F-11 |
| Equipment | Function generator, oscilloscope >= 100 MHz, audio source, sound level meter |
| Fixture | **FIX-02/D** (47.0 Ohm load at J27 and the electrical-onset scope tap), **FIX-02/A** (voice coupler on the boom capsule) and **FIX-02/B** (room coupler at J28) |
| Procedure | **T12a scaling**: drive each source to produce a 1.1 V peak envelope and confirm the ADS1299 input sees 100 mV at gain 1 (the 22 k / 2 k2 divider is x0.0909, calculated). Sources: channel 1 HP_TAP via J8.10 driven by the codec, channel 2 VOICE_PRE via the boom capsule at a stated SPL and distance, channel 3 ROOM_PRE via the room microphone module at J28. **T12b group delay**: 1 kHz burst with a hard electrical onset, 40 repetitions per channel; "electrical onset" is the first sample at which the burst crosses 50 % amplitude at the fixture tap, captured on the scope simultaneously with the ENV_CMP marker. Report the median and IQR of (envelope onset sample minus electrical onset sample). **T12c comparator**: confirm the TLV3201 at U7 trips; calculated threshold 2.5 V x 10 k / 480 k = **52 mV** with about 5 mV of hysteresis from R82. **T12d low-frequency corner**: sweep the AC-coupling corner and record it. **T12e low-pass corner**: from the same sweep, measure the -3 dB corner f0 of the Sallen-Key on each envelope channel and record it |
| Limit | Scaling within +/- 5 % of 100 mV at the converter input. Group delay: the **spread** must be <= 2 samples; the absolute offset is recorded as a constant, not judged. Calculated expectation for the absolute offset: the Sallen-Key at **f0 = 48.77 Hz and Q = 0.7416** has a DC group delay of **1 / (Q x 2 pi x f0) = 1 / 227.2 = 4.40 ms = 4.40 samples at 1000 Hz**. Comparator trips between 45 and 60 mV. **T12d: AC-coupling corner <= 2 Hz**, calculated expectation 1.6 Hz. **T12e: f0 between 42 and 58 Hz**, calculated expectation 48.8 Hz, recorded per unit. That band is what the approved parts can hold and it is **wider than RFQ E-11's 50 Hz +/- 10 %**, which no build with the fitted X7R capacitors can be held inside; Note 1 and section 16 item 16 carry that conflict |
| Uncertainty | Onset: scope timebase 25 ppm and the 1 ms sample grid dominate; U(k=2) = 0.6 sample. Scaling: 1.2 % |
| Record | 3 scaling values, 3 group-delay medians and their IQR in samples, comparator threshold in mV, the measured AC-coupling corner in Hz, the measured low-pass corner f0 in Hz |
| On failure | Spread above 2 samples: check U1 to U3 and the Sallen-Key values |
| Note 1 | Rev B of this document used sqrt(2)/(2 pi f0) = 4.61 ms for the group delay. That formula is only correct at Q = 0.7071 and the fitted Q is 0.7416; **4.40 ms is the figure, and JIG-EEG-009 was right**. The absolute value also has a wide legitimate spread: **a 100 nF C0G in 0603 / 50 V is not a stocked part**, so C21, C41 and C61 are X7R with a stated 15 % capacitance tolerance over temperature, which moves f0 between about 42.4 and 57.4 Hz and the group delay between about 3.7 and 5.1 ms. That costs nothing for the group-delay constant, which is measured per unit and written into the device. It does cost E-11 its low-pass band: 42.4 to 57.4 Hz does not fit inside the 45 to 55 Hz of 50 Hz +/- 10 %, so **that half of E-11 is not met with the approved parts**. T12e measures f0 per unit against the 42 to 58 Hz the parts can hold, and section 16 item 16 carries the requirement conflict |
| Note 2 | **E-11 is met by Rev B values and was not by the first cut.** C20, C40 and C60 are 10 uF into R20, R40, R60 of 10 kOhm, giving 1.6 Hz; the 1 uF originally fitted gave 15.9 Hz, which removes the speech envelope it exists to pass. E-11 is restated as <= 2 Hz. Recorded as ECO-EEG-027 |
| Note 3 | **ECO-EEG-023 is not in the netlist yet, and T12c measures the board as it is.** The ECO re-powers U7 from DVDD3V3 and DGND, re-references its inputs to a DVDD3V3/2 divider and AC-couples the envelope into it, so that CMP_RAW swings 0 to 3.3 V into GPIO3 with full margin. `design.py` Rev B still wires U7.2 to AVSS and U7.5 to AVDD, so as built CMP_RAW swings to +2.50 V against GPIO3's 2.48 V guaranteed input-high threshold -- **a 20 mV margin, and the D23 clamp is the only thing between the analogue rails and a 3.3 V pin**. This is a change the safety and layout reviewer must check before it is cut in |
| Note 4 | **The FIX-02/D comparator threshold is commanded, and it is set per headphone-amplifier model.** JIG-EEG-009 section 2.3 closes it on 2026-09-02 as an M2 PWM output on GP15 through a 10.0 kOhm / 10.0 kOhm divider with a 220 nF capacitor across the lower leg, giving a full-scale threshold of 3.300 x 10.0 / 20.0 = **1.6500 V** in 1000 counts, that is **1.650 mV per count**, commanded over FIXPROTO as `THR MV <millivolts, 0..1650>`. T12b's "50 % amplitude at the fixture tap" is therefore a number somebody sets, and this step says who sets it and how: **at first article for each headphone-amplifier model, measure the burst amplitude across RL201 with the oscilloscope at the resistor body** -- not 4-wire, which is the method for the 47.0 Ohm value itself -- at the level T12b actually commands and with the E-29 clamp in whatever state it is in at T12, which today is unset, then set THR to 50 % of the measured value. The value is recorded per model and re-measured at the six-monthly FIX-02 calibration. **1.650 mV per count is setting granularity and not accuracy**: the 3.3 V rail tolerance and the GPIO output resistance (330 uA into about 100 Ohm, about 33 mV, roughly 2 % of full scale) set the accuracy, and 2 % of threshold on a 1 kHz burst is about **2 us** of onset error against this step's 1 ms sample grid -- a fiftieth of a sample, which is why the commanded route is good enough. **Not closed, and deliberately not filled in with a number**: the electrical onset for the VOICE_PRE and ROOM_PRE coupler-drive channels. No document states the coupler drive in volts, no coupler has been built or calibrated, and T12b reports per envelope channel against one comparator; that half is measured when a FIX-02/A or /B coupler is first calibrated to 70.0 dB SPL |

### T13 -- Timing self-test

| | |
|---|---|
| Purpose | Prove the stimulus timestamp the study depends on is accurate |
| Verifies | F-21, F-11 |
| Equipment | Host test tool |
| Fixture | FIX-02/D, with FIX-02/A on the boom capsule |
| Procedure | Issue the timing self-test command at 1000 Hz. The device plays 40 test tones and reports the spread between the commanded onset sample index and the detected envelope onset, **corrected by the T12b group-delay constant** |
| Limit | Median <= 1 sample, 95th percentile <= 2 samples |
| Uncertainty | Quantisation at 1 ms plus the group-delay constant's own 0.6 sample; U(k=2) = 0.7 sample. TUR against a 2-sample limit is 2.9:1, which is thin and is stated here rather than hidden |
| Record | Median and p95 in samples; the group-delay constant used; all 40 residuals retained |
| On failure | Hold the unit. A timing failure is a firmware or codec defect and is never a module-swap candidate |

### T14 -- microSD throughput and integrity at 1000 Hz

| | |
|---|---|
| Purpose | Prove the authoritative on-card copy is complete at the highest sample rate |
| Verifies | E-20, F-15, F-09 |
| Equipment | Host test tool with the card reader |
| Fixture | Parking station: power and USB only |
| Procedure | One-bit SDMMC. Record 30 minutes at 1000 Hz to the card and to the host simultaneously. Count DATA frames, check the sequence numbers, then read the card back and compare it frame for frame against the host capture. Record the mean and worst-case write latency and the free space reported in the STATUS frame |
| Limit | **Zero missing sequence numbers**, and the card copy identical to the host copy. Expected frame count 90,000 at 20 samples per frame; the tool computes the expectation from the frame length the device reports, and both figures are recorded |
| Uncertainty | Counting measurement; no uncertainty beyond the clock |
| Record | Frames written, frames missing, card-versus-host mismatch count, mean and worst write latency in ms, card part number and serial |
| On failure | One missing frame is a failure. Replace the card and re-run once; a second failure is a firmware or breakout defect |
| Note | **The frame payload at 1000 Hz is 50.7 kB/s**: 1015 bytes every 20 ms. E-20's "approximately 70 kB/s" and F-12's "approximately 64 kB/s" are allowances that include STATUS and SIGNATURE frames and filesystem overhead; they are not changed, and 50.7 kB/s is the figure the arithmetic in this document uses. About 2 MB/s is available in one-bit mode, which is why the three data lines four-bit mode would have used are spent on the contact-light shift register instead |

### T15 -- Ring-buffer backfill

| | |
|---|---|
| Purpose | Prove a browser reload or a cable re-seat loses nothing |
| Verifies | F-06, F-07, F-12, F-17 |
| Equipment | Host test tool |
| Fixture | None |
| Procedure | Mid-record, disconnect USB for 60 s, reconnect, and request retransmission by sequence range. Measure the backfill rate. Then disconnect for 300 s, reconnect, and confirm the frames beyond the ring depth are recovered from the microSD copy rather than reported as lost |
| Limit | Complete recovery of the 60 s, no reset of the sample counter, GAP frames only beyond the ring depth the device declares in its STATUS frame, a **declared ring depth of at least 90 s**, and a backfill rate of at least three times the live rate (F-12). The 300 s gap must be recoverable in full from the card |
| Uncertainty | Counting |
| Record | Frames recovered, GAP frames and their index ranges, backfill rate in kB/s, **and the ring depth in seconds as declared by the device** |
| On failure | Any gap inside the declared ring depth that is not recovered from the card is a failure |
| Note | **F-06's three minutes of PSRAM ring is impossible and is relaxed, not fudged.** Twelve megabytes of ring will not fit in the 8 MB PSRAM of the mandated E-18 module. The fitted ring is 6 MB, which is **126 seconds** at 1000 Hz. F-06 is restated as **90 seconds of ring plus unlimited backfill from the microSD copy**, which is why T15 now tests a 300 s gap as well as a 60 s one. Recorded as ECO-EEG-025 |

### T16 -- Signature chain

| | |
|---|---|
| Purpose | Prove the integrity mechanism the study relies on actually works before the unit leaves |
| Verifies | F-08 |
| Equipment | Host test tool with the public key exported in T6 |
| Fixture | FIX-03/A |
| Procedure | Record a session of at least 8192 samples, then verify every SIGNATURE frame: the ECDSA P-256 signature over the SHA-256 of the block, chained to the previous block hash, chain rooted at the session identifier supplied by the host |
| Limit | Every block verifies; the chain is unbroken from the session identifier to the last block |
| Uncertainty | Attribute |
| Record | Blocks verified over blocks total, session identifier, public key fingerprint used |
| On failure | Hold. A broken chain means either the ATECC provisioning or the signing task; a re-provisioned ATECC needs T5b, T6 and T16 re-run |

### T17 -- Buttons, microphone mute, headphone level

| | |
|---|---|
| Purpose | Prove the participant's controls and the calibrated audio path |
| Verifies | E-13, E-15, E-16, E-26, E-29 (clamp readback) |
| Equipment | Audio analyser, **47.0 Ohm 1 % load**, sound level meter |
| Fixture | FIX-02/D |
| Procedure | Press SW1, SW2, SW3 in turn and confirm each sets its aux bit and that the RC debounce (10 k with 100 nF) plus the firmware debounce give a single clean event per press, ten presses each. Toggle MIC_MUTE and measure the room-microphone attenuation. Play 1 kHz at the commanded level into the 47.0 Ohm load and measure. Read back the codec volume register **clamp** value written at provisioning and confirm it equals the value established for this lot at T28 |
| Limit | 30 of 30 presses produce exactly one event; mute attenuation >= 60 dB; headphone level within 1 dB of target with THD <= 0.1 %; clamp register value equal to the T28 lot value |
| Uncertainty | Level: analyser 0.1 dB, load tolerance 1 % (0.09 dB), combined U(k=2) = 0.27 dB. TUR against 1 dB is 3.7:1 |
| Record | 3 button results with the event counts, mute attenuation in dB, headphone level in dBu into 47.0 Ohm, THD in %, the level register value read back, and the clamp register value |
| On failure | A double event is a debounce failure: check the R50/C50 group for that button. A level outside 1 dB is recorded as a constant if the codec can be trimmed, and as a failure if it cannot. **A clamp value that does not match the lot value is a hard fail and is never adjusted on the line** |
| Note | A-04 is restated as **32 to 64 Ohm** and the calibrated output level is measured per model. The shipped ATH-M20x is 47 Ohm, so the test load is 47.0 Ohm to match the part that actually ships |

### T18 -- Final assembly and kit closure

| | |
|---|---|
| Purpose | Prove the unit that leaves is the unit that was tested, and that the kit is complete |
| Verifies | M-01, M-02, M-03, M-05, M-06, M-07, A-01 to A-07 |
| Equipment | Torque driver, label printer, the kit packing list KPL-EEG-001 |
| Fixture | None |
| Procedure | Close the enclosure to the stated torque and confirm the stack fits: floor 2.5 + boss 6.0 + carrier 1.6 + M3 x 18 mm nylon standoff + MP-01 plate 3.0 + modules <= 18.0 = **49.1 mm against 55.5 mm internal**, margin 6.4 mm, in a POD-P1 base of **163.0 x 143.0 x 58.0 mm external and 158.0 x 138.0 x 55.5 mm internal** with an MP-01 plate of **146.0 x 126.0 x 3.0 mm**. Confirm every opening in M-02 is gasketed or recessed: the three DIN electrode sockets, the headphone jack, the boom TRRS connector, the room-microphone port with mesh, the charge USB-C, the host USB aperture over the ADuM4160 module's own connector, the microSD slot, and the three **13.0 mm button openings on a 14 mm pitch at y = 76, 90 and 104 mm** on the right wall. Apply the label carrying the unit serial `TIOV-B-nnnn`, hardware revision, the public-key fingerprint, "research instrument -- not a medical device" and the programme URL; tick the kit contents against KPL-EEG-001; confirm the foam cut-outs and the laminated packing photograph; place the calibration certificate in the **case lid pocket** beside the quick-start card |
| Limit | Complete; label content matches the record and the iSerial read in T5b, character for character |
| Uncertainty | Attribute |
| Record | Pass or fail, torque values, measured stack height, label photograph, packing list signed, case and foam part numbers |
| On failure | Re-work and re-check. A label that disagrees with the record is a traceability nonconformance and the unit does not ship until the record, the label and the device agree |
| Note 1 | **M-02's LED opening is withdrawn and no pod indicator is checked.** All eight lights are in the helmet; the pod's state is read from the session runner |
| Note 2 | **A-03's headband is withdrawn as a kit item.** The eight electrodes are fixed to the HM-01 frame at manufacture, so a headband with fixed holders at the same eight sites would duplicate them. A-03 now covers the chin strap **HM-06** and the occipital yoke **HM-03**, and those are what T18 ticks |
| Note 3 | The captive host lead and its cable gland are **not** part of the Phase 1 build. The host connection is a socket, and the kit ships the two A-07 cables, one of which is the host lead. The captive lead through a gland is a Phase 2 item for the helmet shell |

### T19 -- Star-point continuity

| | |
|---|---|
| Purpose | Prove there is exactly one connection between the analogue and digital references, and exactly one shield connection |
| Verifies | E-08, E-07 |
| Equipment | 6.5-digit DMM, 4-wire, 100 mOhm range |
| Fixture | Kelvin probes at TP13 (AGND_REF), TP14 (DGND) and J14.12 (HARN_SHIELD) |
| Procedure | The rule itself -- one AGND_REF-to-DGND star point at R90, one shield tie at R91 -- lives in **DSN-EEG-003 section 3.3** and is not restated here. Per unit: 4-wire resistance TP13 to TP14 across R90, and J14.12 to TP14 across R91. Per lot first article, and on any unit whose 4-wire reading is anomalous: **lift one end of R90, disconnect all module jumpers, and measure AGND_REF to DGND**, then re-solder R90 and repeat the 4-wire check. The module jumpers must come off because the ADS1299 module ties its own analogue reference to its 5 V return, which would otherwise short the measurement |
| Limit | Fitted: <= 50 mOhm across R90 and across R91. Lifted, modules disconnected: >= 10 MOhm. The 100 % evidence for the lifted case is the bare-board isolation measurement in T0, which gives the same information without rework on a 0603 pad |
| Uncertainty | 4-wire, U(k=2) = 0.5 mOhm at 20 mOhm. Insulation reading limited by probe leakage, +/- 20 % at 10 MOhm |
| Record | Two 4-wire values in mOhm; the lifted value in MOhm where taken, with the reason it was taken |
| On failure | A second path between AGND_REF and DGND is a build defect: look for a solder bridge, a wire link, or a module jumper landing on the wrong pin. On a four-layer board it can also be a **stitching via that has landed on the wrong plane region**, which is why T0's inner-layer check exists. Never "fix" a star point with a wire |

### T20 -- Isolation-barrier insulation resistance

| | |
|---|---|
| Purpose | Give routine per-unit evidence that the only path from the host to the participant is the certified isolator |
| Verifies | S-03, E-24, F-17 |
| Equipment | 500 V DC insulation tester, range to 100 GOhm, +/- 5 % |
| Fixture | FIX-04/B, a host-side adapter that reaches the module's shell, VBUS, D+ and D- without touching the carrier |
| Procedure | With the ADuM4160 module fitted, short the host-side shell, VBUS, D+ and D- together and apply **500 V DC** against the applied-part group -- J14.1 to J14.11 and J15, J16, J17 shorted together. 60 s dwell. Then re-insert into the flow and confirm functional data flow in T5 |
| Limit | >= 1 GOhm. If the module carries a cross-barrier Y-capacitor the reading is dominated by that capacitor's leakage; in that case the limit is the value recorded for that module type at T00, and this must be established once per module supplier, not per unit |
| Uncertainty | Tester +/- 5 %; humidity is the dominant environmental term, which is why RH is recorded |
| Record | Applied voltage, measured resistance, dwell, RH, module type and lot |
| On failure | Quarantine the unit. Do not repeat the test; do not increase the voltage |
| Note | **The per-unit isolation test is a 500 V DC insulation-resistance measurement and nothing else. There is no per-unit hipot anywhere in this specification, and a manufacturer must not build one.** The 2.5 kV RMS type test is the **module supplier's certificate**, collected once at T00 and never repeated per unit; The per-unit 2500 V AC station that JIG-EEG-009 Rev A carried is deleted, and JIG-EEG-009 Rev B builds none. The 8 mm creepage of S-03 is a property of the artwork and is verified once per routed Gerber revision in the first-article report, not per unit. Neither is a substitute for the safety review |

### T21 -- VBUS detection and charge-path interlock

| | |
|---|---|
| Purpose | Prove both independent mechanisms that keep the helmet off a head while the charger is plugged in |
| Verifies | S-01, E-23 (in part) |
| Equipment | 6.5-digit DMM, bench supply, oscilloscope |
| Fixture | FIX-04/A on J24 |
| Procedure | (a) Apply 5.000 V at J24 and measure the R84 / R85 junction. (b) With VBUS present, issue the session-start command and confirm the device **refuses** it, recording the ACK code. (c) With a session already running, apply VBUS and confirm CHG_CE (GPIO47, at J12.4) holds the charger disabled for the whole session and the charge current stays below the T4 limit. (d) Remove VBUS and confirm the reported state clears |
| Limit | **Junction voltage 2.85 to 3.15 V**; session start refused with the defined ACK code; CHG_CE asserted throughout; state clears within one STATUS frame |
| Uncertainty | DMM 0.01 %, but the DMM's 10 MOhm input loads the divider: 150 k in parallel with 10 M gives 2.98 V against 3.00 V unloaded, a systematic -0.6 %, and the limit band is set wide enough to absorb it |
| Record | Junction voltage in V, ACK code, CHG_CE state, charge current, clear-down latency |
| On failure | **A build defect, and it is now diagnosable as one.** With R84 = 100 kOhm and R85 = 150 kOhm the junction is 5 x 150 / 250 = **3.00 V**, comfortably above the 2.48 V guaranteed input-high threshold of a 3.3 V ESP32-S3 input, so a reading outside the band means a wrong resistor, a bad joint or a damaged divider, not a marginal design. Rework the divider and re-test |
| Note | R85 was 56 kOhm in the first cut, giving 1.79 V, which is **below** the 2.48 V threshold on a pin that is not an ADC input; whether a given unit read that as high was a device-to-device property, and the first of the two S-01 interlocks would not have asserted reliably. ECO-EEG-022 changed R85 to 150 kOhm. Any document still listing R85 as 56 kOhm is stale |

### T22 -- Frequency response

| | |
|---|---|
| Purpose | Prove the passband E-10 requires, on the network that actually sets it |
| Verifies | E-10 |
| Equipment | Function generator, DMM, host test tool |
| Fixture | FIX-01/A, FIX-01/B, FIX-01/C and FIX-01/F, as T7 |
| Procedure | 100 uV sine at 1, 10, 30, 50, 70 and 100 Hz through the 1000:1 divider into all eight EEG channels simultaneously, 60 s coherent record per point. Compute each point relative to the 10 Hz point. Repeat the 1, 50 and 100 Hz points on the three EMG channels at gain 12 |
| Limit | **E-10 has two states and the record must say which one was applied. With the 68 kOhm now fitted the limit is +/- 1.0 dB at every point; it was +/- 0.5 dB while R1 to R16 were 47 kOhm.** Calculated expectation at 100 Hz with the fitted R = 68 kOhm and C = 10.0 nF: corner **234 Hz**, response **-0.75 dB**, inside +/- 1.0 dB. At the superseded 47 kOhm: corner 339 Hz, response -0.36 dB, inside +/- 0.5 dB. *Corrected 2026-09-02: ECO-EEG-024 is applied in `tools/design.py`, so the +/- 1.0 dB branch -- which E-10 already carried -- is the one in force, and the +/- 0.5 dB branch is the historical one.* The arithmetic lives in RISK-EEG-011 section 4 |
| Uncertainty | Ratio measurement, so the divider ratio cancels; residual from the estimator and the generator's flatness, U(k=2) = 0.02 dB |
| Record | 8 x 6 response values in dB, 3 x 3 EMG values, the fitted series-resistor value, **the band applied (+/- 1.0 dB at the fitted 68 kOhm; +/- 0.5 dB was the band at the superseded 47 kOhm)**, and the deviation at 100 Hz called out separately |
| On failure | Check the C1 to C16 group on the failing channel before suspecting anything else |
| Note 1 | **E-10 is at its +/- 1.0 dB branch, and the reason is a safety fix, not a convenience.** S-02's single-fault DC limit was exceeded at 47 kOhm (T23), and the fix is 68 kOhm, which costs 0.75 dB at 100 Hz. **Corrected 2026-09-02: ECO-EEG-024 is applied, 68 kOhm is fitted, and +/- 1.0 dB is the band in force.** Rev C said the opposite -- "ECO-EEG-024 is open and 47 kOhm is fitted, so +/- 0.5 dB is the band in force today" -- and that is superseded on this date. The warning behind it is kept and inverted: testing a **47 kOhm** unit against +/- 1.0 dB would grade it against a limit that build has not earned, so the record must carry the measured series-resistor value and any 47 kOhm unit is graded at +/- 0.5 dB |
| Note 2 | **T22 catches an X7R substitution at the fitted 68 kOhm, and marginally: T00 is still the control.** At the fitted 68 kOhm an X7R part at +20 %, 12 nF, gives a corner of 195 Hz and **-1.01 dB** at 100 Hz, which fails +/- 1.0 dB by a hundredth of a decibel -- inside this step's own uncertainty, so it is not a detection anyone should rely on. At the superseded 47 kOhm the same part gave 282 Hz and -0.51 dB, which passed. *Corrected 2026-09-02: Rev C's "T22 no longer catches an X7R substitution" was written with 47 kOhm fitted.* The C0G requirement is therefore enforced at incoming inspection **by part number** -- `Murata GCM1885C1H103JA16D` -- and not by this measurement. The approved alternate is 4.7 nF, corner 720 Hz, -0.08 dB at 100 Hz; taking it is an ECO decision, not a line decision |

### T23 -- Leakage current at the applied parts

| | |
|---|---|
| Purpose | Give routine evidence, per unit, that no meaningful current flows out of an electrode |
| Verifies | S-02, partially -- **met in the design at 36.8 uA and not signed off; see the note** |
| Equipment | 100 kOhm 0.1 % measuring resistor, screened; 6.5-digit DMM in DC and true-RMS AC |
| Fixture | FIX-01/A in the open position, FIX-01/B, and FIX-04/C with its screened 100 kOhm measuring resistor and its lead to protective earth |
| Procedure | DUT on battery, session active, lead-off excitation **on** at 6 nA / 7.8 Hz (the worst case of E-06). For each of the **fourteen** applied-part terminations -- J14.1 to J14.11 and J15, J16, J17 -- connect the measuring resistor from that terminal to protective earth and read DC and AC across it. Repeat the whole set with the USB host connected and with it disconnected. Then one single-fault condition: short the isolator's device-side ground to earth and repeat |
| Limit | Normal condition <= 10 uA DC and <= 100 uA AC; single fault <= 50 uA DC. 1 nA reads as 100 uV across the measuring resistor, so the instrument resolves four decades below the limit |
| Uncertainty | Resistor 0.1 %, DMM 0.01 % DC and 0.1 % AC, thermal EMF about 2 uV (20 nA equivalent); U(k=2) < 0.5 % of reading plus 40 nA. TUR against 10 uA is far better than 4:1 |
| Record | 14 DC and 14 AC values in uA, host connected and disconnected, plus the 14 single-fault DC values -- 70 values |
| **S-02 is met in the design, and it is not signed off** | **Corrected 2026-09-02.** ECO-EEG-024 is applied in `tools/design.py`: R1 to R16 are **68 kOhm** (Vishay TNPW060368K0BEEA), so the single-fault DC current is **2.5 V / 68 kOhm = 36.8 uA calculated against the 50 uA limit of S-02 -- it passes**, with the corner at 234 Hz (-0.75 dB at 100 Hz, so E-10 sits at its +/- 1.0 dB branch, see T22) and Johnson noise at 0.28 uV for a total of 0.31 uV, still well inside E-03. **Rev C's "with the fitted 47 kOhm the current is calculated at 53.2 uA and it fails" is superseded on this date**, as is "47 kOhm is fitted on the Phase 1 prototypes and the measurement is made before Phase 2": the resistor changed in the design before any prototype was built. Three things this does **not** do. It is **calculated, not measured** -- no unit exists. It does not discharge **SR-01**: the electrical safety reviewer of RISK-EEG-011 section 7 owns the disposition, that review has not started, and the reviewer is now handed a design that meets the limit and is asked to confirm it rather than one that does not. And it does not make this step the real verification; see the row below. The arithmetic lives in RISK-EEG-011 section 4, **which has not yet been restated against the applied ECO** |
| **Limitation, stated plainly** | This step is also a **stand-in**. It is not the IEC 60601-1 patient-auxiliary-current measurement: the measuring device is a 100 kOhm resistor rather than the figure-12 network, only one single-fault condition is applied, and this programme has no accredited safety laboratory. It is the only routine per-unit safety evidence that exists, and the real S-02 verification is owed by RISK-EEG-011 and the electrical safety review |
| On failure | Quarantine. Do not rework and re-test. Any reading above 1 uA on a battery-powered, isolated instrument means something is wrong that the operator cannot diagnose |

### T24 -- Radio silent

| | |
|---|---|
| Purpose | Confirm on the finished unit what the build claims: the radio never comes up |
| Verifies | S-06, E-18 |
| Equipment | 2.4 GHz receiver or SDR with a near-field probe, noise floor <= -90 dBm |
| Fixture | Probe 10 cm from the enclosure lid |
| Procedure | With the unit powered and recording at 1000 Hz, sweep 2.400 to 2.4835 GHz for 60 s. Run this concurrently with T14 so it costs no line time. As a cross-check, a laptop scan must show no ESP-prefixed SSID and no BLE advertisement |
| Limit | No carrier above the receiver noise floor; no SSID; no advertisement |
| Uncertainty | Attribute, with the receiver noise floor recorded |
| Record | Pass or fail, receiver noise floor in dBm, firmware image SHA-256 |
| On failure | Stop the line. The manufacturer must never enable the radio for a production convenience such as wireless flashing. Build-time evidence -- the radio options disabled in sdkconfig, no Wi-Fi or Bluetooth symbols in the ELF, no phy_init partition -- is captured once per firmware version in the release manifest, not per unit |

### T25 -- Firmware security posture (Phase 2 onward)

| | |
|---|---|
| Purpose | Prove the security settings the fleet depends on are actually burned, and that a bad image rolls back |
| Verifies | F-19, F-20 |
| Equipment | Host PC, esptool |
| Fixture | FIX-03/A, with FIX-03/B on J26 for console access |
| Procedure | Read back the secure-boot and flash-encryption eFuse bits. Then force one rollback: write a deliberately failing image to the B partition, reboot, and confirm the device returns to A automatically. Order in the flow matters: the security bits are burned **after** T5 to T17 and **before** T18, and burning them is irreversible |
| Limit | Secure boot enabled, flash encryption enabled, device rejects an unsigned image, rollback completes without operator action |
| Uncertainty | Attribute |
| Record | eFuse readback, rollback pass or fail, image SHA-256 of both partitions |
| On failure | A unit whose eFuses are burned wrongly cannot be recovered. Scrap the DevKitC-1 module, re-provision, and re-run T5b, T6, T16 and T25 |
| Note 1 | **eFuses are not burned on the Phase 1 prototypes.** Secure boot and flash encryption are enabled from Phase 2. The two prototypes run unsigned images so the firmware volunteer can iterate, so **T25 is a Phase 2 gate and is not a Phase 1 gate**; on a Phase 1 unit it is recorded NOT_APPLICABLE with that reason. The manufacturer never holds the signing key |
| Note 2 | **End-of-line flashing is through the DevKitC-1's own UART USB-C port**, which carries the auto-reset circuit (DTR and RTS to EN and IO0) on the DevKit itself, and the module is reachable through the MP-01 opening. The carrier's **J26 is console and recovery only and cannot enter download mode**, because GPIO0 is committed to LED_SR_LATCH (ECO-EEG-009) and J26 way 6 is the spare net NC_GPIO0. Any procedure that describes a relay sequence on GPIO0 and EN at J26 will not work |

### T26 -- Re-enumeration timing

| | |
|---|---|
| Purpose | Prove a host sleep or a browser reload does not cost the session |
| Verifies | F-05 |
| Equipment | Host test tool with timestamping |
| Fixture | None |
| Procedure | Mid-session, force three re-enumerations: cable re-seat, host sleep and wake, browser reload. Time each from disconnect to a decoded frame |
| Limit | Re-enumeration within 2 s each time; the sample counter and the ring buffer are not reset |
| Uncertainty | Host timestamp granularity, U(k=2) = 20 ms |
| Record | Three latencies in ms, sample counter continuity pass or fail |
| On failure | Firmware defect; hold the unit and report the capture |

### T27 -- Converter clock, sample rate and daisy order

| | |
|---|---|
| Purpose | Prove the two converters really are one simultaneous sixteen-channel instrument |
| Verifies | E-01, E-02, E-19 |
| Equipment | Oscilloscope, host test tool |
| Fixture | Probes at TP18 (CLK_ADS), TP4 (DRDY), TP1 (SCLK), TP17 (NC_DRDY2) |
| Procedure | (a) Measure the shared clock at TP18: one source, 2.048 MHz. (b) Measure SCLK at TP1 during a burst. (c) Measure the DRDY period at TP4 with the rate commanded at 250, 500 and 1000 Hz in turn, and confirm the rate field in the frame header matches each time. (d) Run 60 s at 1000 Hz and confirm both devices' status words advance together, with no drift in the interleave. (e) Confirm the daisy order: at gain 24 on the EEG group and gain 12 on the EMG group, **channel 9 must read the EMG gain** -- if channel 9 reads 24 the modules are the other way round |
| Limit | Clock 2.048 MHz +/- 100 ppm from one source; SCLK >= 4 MHz; DRDY period 4.000, 2.000 and 1.000 ms within 100 ppm; status words advance together over 60 s with zero divergence; daisy order as documented in the firmware |
| Uncertainty | Scope timebase 25 ppm; period measurement U(k=2) = 60 ppm |
| Record | Clock frequency, SCLK frequency, three DRDY periods, header rate fields, divergence count, daisy order as found |
| On failure | Divergence between the two devices means the clock-enable configuration is wrong on one module -- exactly the failure that no Rev A step would have caught. Hold and report |
| Note | The channel numbering used here and in T7 is the **stream** numbering. It is not the R1 to R16 protection-network numbering of DESIGN_FACTS section 5, and it is not JIG-EEG-009 section 1.5's fixture numbering. The three lists are different things and must not be conflated; where JIG-EEG-009 says "channel 12 reads gain 12", this document's daisy check is on **channel 9** |

### T28 -- Maximum acoustic output (type test, once per lot)

| | |
|---|---|
| Purpose | Establish the ceiling on what the instrument can put into a participant's ears, and the register value that enforces it |
| Verifies | **E-29** |
| Equipment | IEC 60318-1 artificial ear, class 1 sound level meter, audio analyser |
| Fixture | **FIX-02/C**, the artificial ear and its class 1 sound level meter, with the shipped headphone model fitted and FIX-02/D's dummy load out of circuit |
| Frequency | **Once per lot, not per unit.** This is the one step in section 8 that is not run on 100 % of units |
| Procedure | With the headphone model that ships with the kit seated on the artificial ear, play 1 kHz at the maximum commanded level the session runner can request, then at a deliberate full-scale write to the codec volume register that bypasses the runner's own limit. Record dB SPL for both. Then find the largest register value whose measured output stays at or below 100 dB SPL with 3 dB of margin, and publish that value as the lot clamp for T17 and T6 |
| Limit | **<= 100 dB SPL at any commanded level.** The full-scale write is expected to exceed it: calculated full-scale output is about **110 dB SPL**, which is exactly why the requirement and the clamp exist |
| Uncertainty | SLM +/- 1.0 dB, coupler seating +/- 1.5 dB; U(k=2) = 2.0 dB, which is why the clamp carries 3 dB of margin |
| Record | Two dB SPL values, the headphone model and its impedance, the clamp register value, the coupler and SLM asset numbers |
| On failure | If no register value gives 100 dB SPL with margin, the lot does not ship. The fix is a firmware clamp plus, if necessary, a fixed attenuator in the headphone path, and that is an ECO, not a line adjustment |
| Note | E-29 is **new in RFQ Rev D** and was raised because the package had no maximum acoustic output requirement, no hardware ceiling and no numbered test, on an instrument that plays stimuli into the ears of distressed participants at home. The firmware must clamp the codec volume register to the value measured here; T17 reads that clamp back on every unit |

### T29 -- Lithium marking and shipping documents

| | |
|---|---|
| Purpose | Prove the mandatory lithium obligation is actually discharged on the unit that leaves, not only described in a procedure |
| Verifies | **S-09**, and S-04 in part |
| Equipment | None beyond the packing station |
| Fixture | None |
| Procedure | The procedure itself lives in **PKG-EEG-015 section 7** and the obligation in REG-EEG-012 section 3; neither is restated here. Confirm, on the closed kit: the cell is installed in the unit and no spare cell travels in the case; the UN 38.3 test summary and the MSDS for the installed cell lot are on file and referenced in the record; the lithium handling mark is applied to the carton; the shipping document set named in PKG-EEG-015 section 7 is present and matches the unit serial |
| Limit | All present and matching. Applying the mark is not optional even where a single-kit parcel would fall under the small-consignment exemption |
| Uncertainty | Attribute |
| Record | Cell lot, UN 38.3 report reference, MSDS reference, mark applied yes/no with a photograph, document set reference |
| On failure | The kit does not ship. This is a legal obligation on the consignor, not a quality preference |
| Note | S-09 had no row in this document's traceability matrix before Rev C, although section 10's whole premise is that a mandatory requirement with no test must be visible. T29 closes that |

### T30 -- Host link check with the TOOL-EEG-022 connectivity test program

| | |
|---|---|
| Purpose | Prove that the computer and the instrument speak the same protocol before any step that needs a decoded frame is attempted, so that a framing, CRC, sequence or dispatch fault is found in a minute at the bench rather than as an unexplained failure inside T7 to T16 |
| Verifies | **F-01 in part** -- the CDC-ACM interface is not merely enumerated but opened and made to carry frames -- and **F-10 in part**, the acknowledgement path and the two read-only opcodes. It also verifies TOOL-EEG-022 Rev A's own requirements T-01 to T-12 |
| Equipment | One of the section 5 host PCs running Chrome or Edge, and one of the two A-07 cables shipped with the kit. TOOL-EEG-022 part 3 asks for Windows 10 or later or macOS 11 or later, which the Windows and macOS hosts of section 5 exceed; Safari and Firefox cannot run the tool at all, because they do not implement Web Serial. Nothing is installed and no administrator rights are needed |
| Fixture | FIX-03/A |
| Procedure | Open `webtest/EEG-Connectivity-Test.html` from local disk and confirm the five self-checks S1 to S5 pass **before** the unit is connected; a self-check failure condemns the browser or the file and says nothing about the unit. Then connect the DUT and run the device sequence D1 to D8 of TOOL-EEG-022 section 2.4: identity, protocol-version match, provisioned serial, a 5-byte loopback containing 0x00 and 0xFF, a full 240-byte loopback, a loopback sweep of all 256 byte values, twenty round-trip latency measurements, and one second of silence with no session running. **T30a** runs immediately after T5a and before T6, when D3 is expected to warn because the unit is not yet provisioned. **T30b** runs after T6, alongside T5b, when D3 must pass and the serial the tool reads must equal the unit serial character for character. Save the report from both runs |
| Limit | Every S-check and every D-check passes at T30b, with D3's warning allowed at T30a only. Every frame-integrity counter -- CRC errors, version errors, short frames, resyncs, oversize discards, sequence gaps, frames missing -- reads zero. Median round-trip latency **<= 50 ms**, which is TOOL-EEG-022's own warning threshold; a higher figure is recorded with the host and hub arrangement rather than silently accepted, because E-13's stimulus timing rests on it |
| Uncertainty | Attribute, except the latency figures, which are host-scheduler limited and recorded to 1 ms |
| Record | The saved TOOL-EEG-022 report from both runs; the SHA-256 of the `EEG-Connectivity-Test.html` file used; the browser name and version; the identity block `CMD_IDENTIFY` returned -- protocol version, firmware major and minor, board revision letter, ring bytes, capability flags and rate code -- and the median and p95 latency |
| On failure | Hold the unit and do not start T6 or any decoding step. A D1 failure is no firmware, the wrong firmware or a charge-only cable. A D4 to D6 failure is a framing or transport fault: report it to the programme with the saved report, because it is a defect in the image or the cable rather than in the build. A D8 failure means the device streams without being asked, which is a firmware defect |
| Note | The number is T30 because this document never renumbers a step, not because the step runs last: it runs at T5. **It is not a measurement.** TOOL-EEG-022 section 1.3 is explicit that a pass says the link works and says nothing about signal quality, electrode contact, noise or whether the instrument is safe to put on a person, and it is not a substitute for any other step here. The protocol code this step runs in a browser is the same code the section 4 readiness gate proves against the shipped firmware source, which is why a T30 failure points at the unit rather than at the tool |

## 9. Measurement uncertainty budgets

Every step above carries its own uncertainty line. The three that decide study-grade
numbers are budgeted here in full. All figures are **calculated**; none has been verified on
hardware.

### 9.1 T7 gain

| Contribution | Value | Type | Note |
|---|---|---|---|
| Divider ratio | 0.020 % | B | ratio-matched network, 0.01 % ratio spec |
| Ratio tempco tracking | 0.001 % | B | <= 2 ppm/degC over 18 to 25 degC |
| Divider input voltage, **measured** | 0.060 % | B | 6.5-digit DMM true RMS at 10 Hz |
| Quantisation | negligible | B | LSB at gain 24 is 22.35 nV |
| Noise-limited estimator, 1 mV, 60 s | 0.0022 % | A | coherent single bin |
| Noise-limited estimator, 100 uV, 60 s | 0.022 % | A | |
| Noise-limited estimator, 10 uV, 60 s | 0.219 % | A | the term that decides the 10 uV point |
| Noise-limited estimator, 10 uV, 240 s | 0.110 % | A | the mandated record length at this level |
| **Combined at 100 uV and 1 mV** | **0.067 %**, U(k=2) = **0.134 %** | | TUR 3.7:1 against the 0.5 % matching limit |
| **At 10 uV** | **U(k=2) = 0.22 %** | | JIG-EEG-009 section 1.4's derivation governs. TUR 23:1 against the +/- 5 % linearity limit |

Two things about the 10 uV point, because three documents have disagreed about them. First,
the limit is a **+/- 5 % linearity check**; the 0.5 % matching limit of E-04 applies at the
100 uV and 1 mV points only, and RFQ section 9.1 item 6's "sixteen inputs, gain within
0.5 %" is superseded on both counts -- matching applies to the eight EEG channels, and not
at 10 uV. Second, the **0.22 % figure is an expanded uncertainty at k = 2**, not a 1 sigma
value; QP-EEG-010 section 12.2's "1 sigma" label is wrong and is corrected.

The ADS1299 internal 4.5 V reference is a systematic term shared by all sixteen channels.
It is absorbed into the recorded absolute gain constant and cancels out of the matching
limit. It is **not measured**, which is an item in the escape analysis.

### 9.2 T8 noise

| Contribution | Value | Type |
|---|---|---|
| RMS estimator, 2BT = 8340 over 60 s | 0.8 % | A |
| Band-pass and bin-exclusion definition | 2.0 % | B |
| Gain calibration carried from T7 | 0.13 % | B |
| **Combined** | **2.2 %**, U(k=2) = **4.3 %** = +/- 0.04 uV at 1.0 uV | |

### 9.3 T9 crosstalk

The floor is the budget. Noise density 0.120 uV/sqrt(Hz), derived from the 1.0 uV RMS over
69.5 Hz of E-03 in RISK-EEG-011 section 4.

| Record length | Bin width | Per-bin noise | Floor rel. 1.000 mV RMS | Margin at -80 dB |
|---|---|---|---|---|
| 60 s | 0.01667 Hz | 0.0155 uV | -96.2 dB | 16.2 dB |
| 240 s | 0.00417 Hz | 0.0077 uV | -102.2 dB | 22.2 dB |
| **600 s (mandated)** | 0.00167 Hz | 0.0049 uV | **-106.2 dB** | **26.2 dB** |

600 s is mandated even though 60 s would clear the restated -80 dB limit on floor alone,
because the aggressor is now at 50 Hz and the narrow bin is what separates a locked
generator from wandering mains. Against the withdrawn -100 dB limit even 600 s gave only
6.2 dB, and 60 s was unusable -- which is the arithmetic that produced ECO-EEG-026.

## 10. Requirements-to-test traceability matrix

Level from RFQ-EEG-001 Rev E: M mandatory, S should, Info informational.
"None" means exactly that, and is a decision recorded here rather than an omission.
Where a requirement is not met, that is written in its own row and not somewhere else.

| Ref | Level | Verified by | Note |
|---|---|---|---|
| E-01 | M | T27, T00 | shared clock, daisy order and simultaneity |
| E-02 | M | T27 | all three rates commanded and the header field checked |
| E-03 | M | T8 | |
| E-04 | M | T7a, T9a | **restated by ECO-EEG-026**: matching within 0.5 % at 100 uV and 1 mV, crosstalk -80 dB at 50 Hz on the carrier. The original -100 dB is neither achievable through the ribbon nor measurable on this instrument; the ribbon is characterised once as a type test |
| E-05 | M | T8, T19 | **partial**: the 4.5 V internal reference is not measured |
| E-06 | M | T10 | **partial**: 6 nA is register-set, not measured |
| E-07 | M | T0, T1, T10, T22 | T10's R_off proves each series resistor is present and in value |
| E-08 | M | T0, T19 | |
| E-09 | M | T2, T19, T18 | harness itself under WH-EEG-008 |
| E-10 | M | T22 | **+/- 1.0 dB, which is the branch E-10 carries for the 68 kOhm now fitted** (-0.75 dB at 100 Hz). *Corrected 2026-09-02: was "+/- 0.5 dB with the 47 kOhm fitted ... ECO-EEG-024 is open, so +/- 0.5 dB is the band in force". ECO-EEG-024 is applied and the requirement's own second branch is the one in force* |
| E-11 | M | T12d, T12e | **met in part**. The AC-coupling half is met at 1.6 Hz and restated to <= 2 Hz by ECO-EEG-027; the 1 uF of the first cut gave 15.9 Hz. The 50 Hz +/- 10 % low-pass half is **not met with the approved parts**: a 100 nF C0G in 0603 / 50 V is not stocked, and the fitted X7R at +/- 15 % over temperature puts f0 between 42.4 and 57.4 Hz against a 45 to 55 Hz band. T12e measures and records f0 against 42 to 58 Hz (section 16 item 16) |
| E-12 | M | T12c | raised from S to M in RFQ Rev D because the comparator is now fitted |
| E-13 | M | T17, T28 | level per unit into 47.0 Ohm, ceiling per lot |
| E-14 | M | T12a, T17 | **the preamplifier is on MP-01 at J21**, not on the boom; the boom carries the bare capsule and its screen on the J18 pigtail |
| E-15 | M | T12a, T17 | |
| E-16 | M | T12a, T17 | reference-tone gains recorded as constants |
| E-17 | M | **None per unit** | first-article only, one Phase 1 unit -- **and no method for it exists anywhere in the package**; see section 14 and section 16 item 6 |
| E-18 | M | T00, T24 | N16R8 variant and radio silence |
| E-19 | M | T27 | |
| E-20 | M | T14 per unit, 3 h soak per lot | **conflict**: E-20 as written says three hours per unit; see section 16 item 1 |
| E-21 | M | T6, T5b | |
| E-22 | M | **None per unit** | 4 h endurance run once per lot; see section 14 |
| E-23 | M | T4, T21 | **not met in part, and it stays not met**: the interlocks are tested but the 45 degC charge inhibit is not, because there is no NTC net in `design.py` and no thermistor way on J12 or J13 |
| E-24 | M | T00, T20, T5 | 2.5 kV is a supplier certificate. **Live non-conformance**: the named isolator module presents USB-B where E-24 asks for USB-C, and the interim answer is the WH-09 pigtail |
| E-25 | M | T3, T8 | **partial**: the buck-boost switching frequency is not measured; T8 is the evidence that it does not matter |
| E-26 | M | T17, T18 | 6 mm tactile switch with a 12 mm cap on an extender, 13.0 mm openings on a 14 mm pitch |
| E-27 | M | T11 | **the phase driver exists as of 2026-09-02** and T11 is written against it (T11 Note 1); the step is deferred under the section 4 gate with every other firmware step, not for want of a driver. **Met in the source**: green, amber, red and both dark states are all reachable as of FW-D17 the same day, which replaced an unreachable `LOFF_STATP AND LOFF_STATN` red term with a swept positive-side comparator threshold. What is **not** established is where the colour boundaries fall in ohms, because the two `COMP_TH` settings are datasheet endpoints rather than measured trip points, so T11's reference resistances are provisional until a unit is characterised (T11 Note 3) |
| E-28 | M | T1, section 6.2 | **met in part**: TP1 to TP18 and the J26 1x6 UART header are fitted; CS, I2S_MCLK, I2S_DIN, I2S_DOUT, VBAT and VBUS_CHG have no test point. The 2x5 JTAG header is withdrawn, so there is no deviation to record against it |
| **E-29** | **M** | **T28 per lot, T17 per unit** | new in RFQ Rev D: <= 100 dB SPL on an artificial ear, with the codec volume register clamped to the measured value |
| F-01 | M | T5a, T30 | T5a enumerates the two interfaces; T30 is where the CDC-ACM one is opened and made to carry frames |
| F-02 | M | T5a | |
| F-03 | M | T6, T5a | **open**: VID and PID are placeholders pending a pid.codes allocation |
| F-04 | M | T5b | |
| F-05 | M | T26 | |
| F-06 | M | T15 | **relaxed by ECO-EEG-025** to 90 s of ring plus unlimited microSD backfill; the fitted 6 MiB ring is 126 s of raw samples, 124 s framed, and three minutes would need 12 MB in an 8 MB part |
| F-07 | M | T15 | |
| F-08 | M | T16 | |
| F-09 | M | T14, T21 | fields read and recorded |
| F-10 | M | T13, T15, T21, T6, T30 | **partial**: each command is exercised by the step that needs it; the full set is not swept. T30 adds the acknowledgement path and the two read-only opcodes per unit, and the section 4 interop harness dispatches eleven opcodes against the shipped firmware source at build time. Neither is a sweep |
| F-11 | M | T12b, T13 | |
| F-12 | M | T15 | backfill rate measured |
| F-13 to F-16 | Info | **None** | host and server software, out of scope of a production test |
| F-17 | M | T15, T18 | isolator carries the rate; cables in the kit |
| F-18 | M | T6 | |
| F-19 | M | T25 | **Phase 2 onward**; Phase 1 prototypes do not burn eFuses |
| F-20 | M | T25 | one forced rollback, **Phase 2 onward** |
| F-21 | M | T13 | |
| A-01 to A-07 | M | T18 | against KPL-EEG-001. A-03 is the chin strap HM-06 and the occipital yoke HM-03; the headband is withdrawn |
| M-01 | M | T18 | POD-P1 163.0 x 143.0 x 58.0 mm external, 158.0 x 138.0 x 55.5 mm internal |
| M-02 | M | T18 | openings itemised in the step; **the LED opening is withdrawn** because there is no pod indicator |
| M-03 | M | T18, T6 | label content generated from the record |
| M-04 | S | **None per unit** | 1 m drop, one Phase 1 unit; section 14 |
| M-05 | M | T18 | |
| M-06 | S | T18 | |
| M-07 | M | T18 | |
| S-01 | M | T4, T21 | both mechanisms |
| S-02 | M | T23 | **met in the design, not signed off and not measured** (corrected 2026-09-02): 36.8 uA calculated against a 50 uA single-fault limit with the 68 kOhm of ECO-EEG-024 fitted in `tools/design.py`. *Was "not met: 53.2 uA ... with 47 kOhm fitted".* SR-01 stays with the electrical safety reviewer, who has not started, and T23 is also only a stand-in for the IEC 60601-1 method |
| S-03 | M | T20, T00, first article | per unit is 500 V DC insulation resistance; creepage is artwork, checked once per Gerber revision |
| S-04 | M | T00, T29 | **not met in part, and it stays not met**: cell documents are collected, but there is no thermistor net and no thermistor way, so thermistor-monitored charging is an open hardware item |
| S-05 | M | T00 | supplier declarations, a document check and not a measurement |
| S-06 | S | T24 per unit; CISPR pre-scan once | section 14 |
| S-07 | M | not used | placeholder retained so numbering is stable |
| S-08 | S | **None** | supplier documents, REG-EEG-012 |
| **S-09** | **M** | **T29** | lithium marking and shipping documents, verified at kit closure; the procedure is PKG-EEG-015 section 7 |

**Requirements with no production test at all:** E-17, F-13, F-14, F-15, F-16, M-04, S-08,
and the per-unit halves of E-20, E-22 and S-06. E-17 is the worst of these: it has a stated
reference level (70.0 dB SPL at 1 kHz) but **no method anywhere in the package** for
measuring "-40 dB relative to a 70 dB SPL voice at the boom", and no definition of
"maximum stimulus level"; writing that method is an open item, not an oversight.

**Requirements verified only in part, each said plainly in its own row above:** E-05 (the
4.5 V reference is not measured), E-06 (6 nA is register-set, not measured), E-10 (six
frequencies only, and against whichever of its two bands the fitted series resistor earns),
E-23 (no 45 degC test), E-25 (switching frequency not measured), E-28 (six named nets have
no test point), F-10 (the command set is not swept), S-02 and S-03.

**Requirements not met by the Rev B hardware as fitted:** S-04's thermistor and E-23's
45 degC inhibit. *Corrected 2026-09-02: S-02 and E-27 have left this list. S-02 is met in
the design at 36.8 uA after ECO-EEG-024 and awaits the safety reviewer; the contact-light
driver is written, so E-27 is met in the firmware and awaits a unit to light. Neither has
been measured, and "met in the design" is not "verified".*

## 11. Test time and station plan

Attended minutes are operator cost. Unattended minutes are station cost. The Rev A figure
of "25 minutes, of which 20 are unattended" is withdrawn: T14 alone is 30 minutes.
WH-EEG-008 section 9's "additional to the 25 minutes per unit of TST-EEG-004" is stale and
must cite the total below. That section defines **ten harness steps, H1 to H10**, and H10 --
the 500 V insulation check on the WH-09 pigtail that crosses the barrier -- is part of it. A
citation to "H1 to H9" leaves out the only harness step that crosses the barrier and is
corrected to H1 to H10.

| Step | Attended (min) | Unattended (min) |
|---|---|---|
| T00 incoming | 12 | -- |
| T0 bare board | at the fabricator | -- |
| T1, T2, T3, T4 | 4, 3, 3, 3 | 30 (T3 closed-pod thermal run) |
| T5, T6 | 8, 4 | -- |
| T7 (relay-switched, all channels per level) | 2 | 14 |
| T8 | 1 | 2 |
| T9a 600 s x 3 records, T9b 60 s | 2 | 31 |
| T10 | 1 | 6 |
| T11 | 3 | -- |
| T12 | 2 | 5 |
| T13 | -- | 3 |
| T14 | -- | 30 |
| T15 | 3 | 7 |
| T16 | -- | 2 |
| T17, T18 | 6, 6 | -- |
| T19, T20, T21 | 3, 4, 4 | -- |
| T22 | 1 | 6 |
| T23 | 7 | -- |
| T24 (runs during T14) | -- | 0 |
| T25 (Phase 2 onward), T26, T27 | 3, 2, 4 | -- |
| T29 | 2 | -- |
| T30 (two runs, at T5a and at T5b) | 2 | -- |
| **Total per unit** | **95** | **136** |

T30's two minutes are a plan figure and not a measurement: TOOL-EEG-022 part 0 puts one run
at about thirty seconds, and T30 is run twice. T3's thermal run, T9a's third record and
T15's 300 s gap are new in Rev C and are why the unattended figure rose from 81 to 136
minutes. T3's 30 minutes and T14's 30 minutes can be run on the same parking station in
sequence but not concurrently, because T3 needs the pod closed.

**T28 is per lot, not per unit:** 15 attended minutes plus 10 unattended, once per lot, on
one unit.

One attended bench with the full fixture set and instrument list, plus N parking stations
carrying only power and USB for T3, T9a, T14, T15 and T22. Recommended: one fixture plus
three parking stations for 10 units; two fixtures plus eight parking stations for 50.
Bidders should price **attended minutes per unit, unattended station-hours per unit, and
fixture count** separately, so that quotes are comparable. Kit BOM item 37 must be
corrected from "18 steps, ~25 min" to "**32 steps** -- T00, T0 and T1 to T30 -- 95 attended
plus 136 unattended minutes per unit".

## 12. Per-unit test record -- template

One JSON file plus one PDF per unit, named `<unit_serial>_test.json`, where the unit serial
has the form `TIOV-B-nnnn` **as defined in PKG-EEG-015 section 5**, which is the only place
the format is defined. One ZIP per lot with a lot summary CSV. Fields, all mandatory
unless marked optional:

**The schema is shipped, and it is what "validated mechanically" now means.** Rev C stated
the field counts below and shipped nothing to check them against, so nothing caught a
missing field and two manufacturers reading this prose would have emitted different key
names and different nesting for the same 70 T23 currents, 32 T10 impedances and 24 T7a
gains. Five files in `records/` close that:

| File | What it is |
|---|---|
| `records/TST-EEG-004_RevC_unit_test_record.schema.json` | JSON Schema 2020-12 for `<unit_serial>_test.json`. **Every field count stated below is a `minItems` equal to `maxItems` pair**, so a short array is a schema error and not a silent gap. The `unit`, `limit` and `uncertainty` strings are `const` values taken verbatim from each step's table in section 8, so a record cannot claim a limit this document does not set |
| `records/EXAMPLE_TIOV-B-0000_test.json` | A worked record that validates and **contains no measurements**: every number is the sentinel -9999 or 9999, every hash is sixty-four zeros, every free-text field begins `EXAMPLE-`, every step verdict is `DEFERRED` with a reason, and the serial `TIOV-B-0000` is in none of the blocks PKG-EEG-015 section 5 allocates. It is a shape, not a result |
| `records/lot_summary_template.csv` | The header row of the per-lot summary CSV. Its per-step verdict columns are generated from the section 2 step list, so a step added here appears there |
| `records/TST-EEG-004_RevC_calibration_certificate.md` | The section 13 certificate template, every placeholder a pointer into the record |
| `records/validate_test_record.py` | The validator. It runs the schema and then the checks a schema cannot express, and it has its own self-test: `python3 records/validate_test_record.py --selftest` breaks the example eleven ways and proves each break is caught |

The record is **complete when it validates**, which is a statement a person can check:

```
python3 records/validate_test_record.py --production TIOV-B-0001_test.json
```

`--production` is what goods-in in Brussels runs. It refuses a record whose `record_type`
is `example`, refuses any step still `DEFERRED`, and refuses the all-zeros placeholder
hash, so the example shipped beside the schema cannot be filed as a unit's record.

Beyond the schema the validator checks the things that make a record about **one** unit: the
iSerial read at T5b against the identity block, the ATECC serial and the fingerprint written
at T6 against the label, the acoustic clamp value across T17, T28 and the constant block,
that a `PASS` at T14, T16, T27 or T30 is not contradicted by its own counters, that every
`DEFERRED` or `NOT_APPLICABLE` step says why, that `attempt` and the retained
`previous_attempts` agree, and that `signatures.record_sha256` is the hash of the record it
sits in.

*The schema is generated from `records/make_records.py`, which reads the step list out of
section 2 of this document and refuses to run if the two disagree. That check is not
decoration: T30 was added to this document after the record template was drafted, and this
is the mechanism that catches the next one.*

**Identity.** unit_serial (`TIOV-B-nnnn`); hw_rev (`EEG-CAR-01-B`); routed-Gerber revision;
carrier board serial or panel position; firmware version; firmware SHA-256;
provisioning-script version; the SHA-256 of the TOOL-EEG-022 file used at T30, and the
stream-decoding tool's version and SHA-256 once that tool exists;
atecc_factory_serial (18 hex);
pubkey_pem; key_fingerprint, **computed as defined in FW-EEG-001 section 7** and identical
to the string printed on the label; vid; pid; module serials or lot codes for the two
ADS1299 modules, the DevKitC-1, the ADuM4160, the ES8388, the charger, the gauge, the shift
register, the microSD breakout, the preamp, the cell and the card; build lot; manufacturer;
operator ID; QA ID; date and time; fixture serial (JIG-EEG-009 unit number); ambient
temperature; relative humidity; every instrument's asset number and calibration due date.

**Results.** One object per step with `value(s)`, `unit`, `limit`, `uncertainty`,
`verdict` in {PASS, FAIL, DEFERRED, NOT_APPLICABLE}, and `attempt` (1, 2 or 3). Field
counts, fixed so a record can be validated mechanically: T00 per-module pass plus the
DevKit flash and PSRAM sizes, the cell OCV and the isolator host connector type; T0 ET
certificate reference plus four check results; T3 two currents in mA, five rail voltages
and the regulator case temperature; T4 charge current plus the negative control; T5 three
host results plus VID, PID, iSerial; T7a 24 gain values in ppm plus 8 constants; T7b 9
values; T7c 2 values; T8 8 whole-record and 8 epoch-median values in uV; T9a 16 crosstalk
values in dB each with its detection floor and its aggressor-off ambient bin; T9b 8 CMRR
values in dB; T10 32 raw impedances plus 8 (R_off, k) pairs; T11 24 colour ratios, 2 dark
luminances and LIGHT_PHASE_HZ; T12 3 scalings, 3 group-delay medians and 3 IQRs in samples,
comparator threshold in mV, AC corner in Hz; T13 median and p95 in samples plus 40
residuals; T14 frames written, frames missing, mismatches, latencies; T15 frames recovered,
GAP ranges, backfill rate, declared ring depth in seconds, 300 s card-recovery result; T16
blocks verified over blocks total; T17 3 button event counts, mute depth in dB, level in
dBu into 47.0 Ohm, THD, clamp register value; T19 two 4-wire values in mOhm; T20 resistance
in GOhm with applied voltage and RH; T21 junction voltage, ACK code, CHG_CE state, charge
current; T22 48 EEG and 9 EMG values in dB; T23 70 current values in uA; T24 pass plus
receiver noise floor; T25 eFuse readback and rollback result, or NOT_APPLICABLE with the
Phase 1 reason; T26 three latencies in ms; T27 clock, SCLK, three DRDY periods, divergence
count, daisy order; T28 the lot record reference and the two dB SPL values it carries; T29
cell lot, UN 38.3 and MSDS references, mark photograph reference; T30 the S1 to S5 and D1 to
D8 verdicts for both runs, the `CMD_IDENTIFY` identity block, the bytes-in and
frames-decoded totals with all seven frame-integrity error counters, the median and p95
round-trip latency in ms, and the saved report reference.

**Constants written to the device**, byte-exact and mirroring the NVS content: 16 channel
gains as int32 ppm correction; 3 envelope scalings as int32 uV per full scale; 3 envelope
group delays in samples to two decimals; 8 lead-off offsets in Ohm and 8 slopes; headphone
level as int16 tenths of a dB; the acoustic clamp register value; plus the config-zone lock
confirmation.

**Disposition.** Failure codes; rework sites and cycle counts; module replacements with the
re-characterisation steps that were re-run; NCR references; MRB decision where taken.

**Signatures.** Operator, manufacturer QA, and the SHA-256 of the JSON printed on the
certificate. Every attempt is retained; nothing is overwritten. A unit may be re-tested at
most twice on the same step; the second failure is an NCR.

*What the SHA-256 is taken over is a **proposal**, not a ruling.* This section required the
hash without saying what it covers, and a hash of a file that contains the hash is not
computable. The schema and the validator define it as the record serialised as UTF-8 JSON
with sorted keys, a two-space indent and a trailing newline, with `signatures.record_sha256`
itself set to sixty-four zeros. That is arbitrary in the way every canonicalisation is
arbitrary, it is implemented identically in `records/make_records.py` and
`records/validate_test_record.py`, and it needs the programme's ruling before a manufacturer
signs against it. It is carried as open item 17 in section 16.

**Refurbishment rule.** When a kit returns from a participant, T7, T8, T10, T13 and T17 are
re-run and appended as a new dated block under the same unit serial. This is what keeps
instrument drift out of the between-participant comparisons.

## 13. Calibration certificate -- template

The template is `records/TST-EEG-004_RevC_calibration_certificate.md`, generated by
`records/make_records.py` from the same table as the schema. Every field on it is a pointer
into `<unit_serial>_test.json` and into nothing else, so the certificate and the record
cannot disagree, and the verification table of item 5 below is built from the step list of
section 2 rather than retyped.

One printed A4 page per unit, generated from the record. **It travels in the case lid
pocket beside the quick-start card**, and PKG-EEG-015's foam schedule is corrected to put
it there rather than in the bottom-layer quick-start slot. Content, in this order:

1. Title, unit serial `TIOV-B-nnnn`, hardware revision `EEG-CAR-01-B`, date of test, and
   the words "Research instrument -- not a medical device".
2. Identity block: ATECC serial, public-key fingerprint as defined in FW-EEG-001 section 7
   and identical to the label, firmware version and SHA-256.
3. Environment: ambient temperature, relative humidity, and the statement that the unit was
   on battery for the characterisation steps.
4. Constants table: 16 channel gains, 3 envelope scalings, 3 group delays, 8 lead-off
   offset and slope pairs, headphone level, acoustic clamp value -- each with its unit and
   its uncertainty.
5. Verification table: measured value, limit and verdict for T3, T7a matching, T8, T9a,
   T9b, T10, T12b, T13, T14, T17, T20, T21, T22, T23.
6. Traceability: every instrument by asset number with its calibration due date, and the
   fixture serial.
7. Statement of limitations, printed in full, not summarised: this certificate is not a
   medical-device conformity statement; T23 is a stand-in for the IEC 60601-1 patient
   auxiliary current measurement and **S-02 is met by calculation at the fitted 68 kOhm
   (36.8 uA against 50 uA) and has not been reviewed by a safety engineer** -- *corrected
   2026-09-02; this line read "S-02 is not met at the fitted resistor value", which was
   true of the superseded 47 kOhm build*; the
   2.5 kV isolation figure is a component supplier's certificate and was not verified on
   this unit; the 45 degC charge inhibit is not implemented; **no safety engineer has
   reviewed this design as of the date of issue**.
8. Signatures: operator, manufacturer QA, and the SHA-256 of the source record.

Sign-off: the manufacturer's QA signs the record and the certificate; the programme
counter-signs at goods-in in Brussels after its own subset re-test, and that
counter-signature is the acceptance under RFQ-EEG-001 section 9.3.

## 14. Type tests, once per phase or once per lot

These are deliberately outside the 100 % flow. Their absence from a per-unit record is a
decision, recorded here so it cannot be read as an oversight. T28 is the one type test that
carries a step number, because other documents need to cite it. **T28 is that number and this
is that list.** Any statement that the maximum acoustic output has no T-number, or that it is
carried in section 13 of this document, is withdrawn: section 13 is the
calibration-certificate template, and the equipment T28 needs is FIX-02/C -- which has not
been bought, built or priced (section 16 item 12), so T28 is specified and not yet runnable.

| Test | Requirement | Frequency | Evidence |
|---|---|---|---|
| Headphone bleed into the boom microphone | E-17 | one Phase 1 unit | measured report -- **no method is yet written; see section 16 item 6** |
| 3 h microSD soak at 1000 Hz | E-20 | one unit per lot | frame count |
| 4 h battery endurance at 1000 Hz | E-22 | one unit per lot | runtime and gauge log |
| 1 m drop on each face, case open and kit packed | M-04 | one Phase 1 unit | re-run of T3, T7, T8, T10, T14 to the same limits, plus a cell inspection |
| CISPR 11 class B pre-scan | S-06 | one Phase 1 unit | pre-scan report |
| **Maximum acoustic output into an artificial ear (T28)** | **E-29** | one unit per lot | two dB SPL values and the clamp register value |
| Ribbon-jumper crosstalk contribution | E-04 | first prototype only | crosstalk measured with and without the 60 mm ribbon in circuit, characterised once |
| Comparison recording against an OpenBCI Cyton on a volunteer | RFQ section 9.2 | Phase 1 | N100 latency within 2 ms, amplitude within 10 % |
| Creepage and clearance across the J10 barrier region | S-03 | once per routed Gerber revision | measured from the artwork, >= 8 mm, with a copper-plot overlay of all four layers showing the keep-out of DSN-EEG-003 section 3.3 honoured. The Rev B DRC report records **no isolation keep-out violation on any of the four layers**, and that is the result the overlay must reproduce -- on artwork released for review under RFQ-EEG-002A and not yet released for fabrication |

## 15. Escape analysis -- what can still be wrong in a unit that passes every step

Written because a test specification that does not state its own blind spots is misleading.

1. **Absolute amplitude.** The ADS1299 internal 4.5 V reference is never measured. A
   reference out of tolerance shifts all sixteen channels identically, passes the matching
   limit of T7, and biases every microvolt in that unit's data.
2. **Common-mode layout defects.** T9a compares channels within one unit. A coupling path
   present on every board -- and the routing has not been reviewed by a human layout
   engineer, and 169 of its connections are relaxed to the minimum conductor or the minimum
   gap -- is systematic and cancels out of every comparison this specification makes.
   The four-layer stack makes a continuous reference plane possible; it does not prove the
   pours were split where the design says they are, and only T0's inner-layer isolation
   check looks at that at all.
3. **The isolation barrier.** T20 is 500 V DC insulation resistance on the finished unit.
   The 2.5 kV RMS rating is a supplier certificate. A module whose barrier has been degraded
   in handling can still read above 1 GOhm at 500 V.
4. **Patient auxiliary current.** T23 is a stand-in, with one single-fault condition and a
   resistor in place of the measuring network. *Corrected 2026-09-02: this item used to end
   "and the calculated single-fault current already exceeds the S-02 limit at the fitted
   resistor value", which was true at 47 kOhm and is not at the 68 kOhm now fitted -- the
   calculated current is 36.8 uA against 50 uA.* The escape is unchanged by that: a
   calculation is not a measurement, and fault conditions that were not imagined are not
   tested.
5. **Time.** The longest continuous run in this flow is 30 minutes. Infant mortality in the
   modules, electrolytic ageing, connector fretting and card wear are not screened. A card
   that degrades at hour two passes T14.
6. **Temperature.** Everything here is done between 18 and 25 degC. A unit used in a cold
   room, or one whose gains drift with the internal rise during a two-hour session, is not
   characterised. T3's closed-pod thermal run measures one regulator, not the instrument.
7. **Movement.** The bench is static. Electrode-lead intermittency, connector microphony and
   the mechanical behaviour of the harness under a moving head are not tested here at all;
   they belong to WH-EEG-008 and to the type tests.
8. **The firmware.** Only the released image is tested, and only its expected paths. One
   forced rollback in T25 is not a proof that rollback works in every failure mode, and on
   Phase 1 units T25 does not run at all.
9. **Identity after repair.** Swapping a module after provisioning silently detaches the
   serial, the key and the constants from the hardware in the box. The disposition rules
   forbid it without full re-characterisation, but the tests themselves cannot detect it.
10. **The spare channels.** T7c proves channels 15 and 16 work, but in a standard build they
    reach no panel socket, because the EOG panel sockets are a Phase 2 option. A fault there
    is inert until the option is used.
11. **Light brightness, and where the colour boundaries actually fall.** T11 measures a
    colour ratio. A shift-register clone with weak drive gives the right ratio at the wrong
    brightness, and a participant in a lit room may not see it; the ratio is blind to that by
    construction. Two earlier statements here are superseded. Rev C's "until the phase driver
    exists, T11 does not measure the amber state at all" went on 2026-09-02, when the driver
    was written. Its replacement -- "with LOFF_SENSN never enabled a site with no contact
    shows amber rather than red" -- went the same day with FW-D17, which made red reachable
    without LOFF_SENSN (T11 Note 3). **What escapes now is the boundary, not the state.** The
    two `COMP_TH` settings are datasheet endpoints, so the impedance at which a site turns
    from green to amber, and from amber to red, is not yet known to any document in this
    package. A participant could be told "re-gel this one" at an impedance that was in fact
    fine, or nothing at an impedance that was not. Closing it needs a characterised unit, and
    no step here can substitute for that.
12. **Key uniqueness.** T6 proves a key was generated and locked in one unit. Uniqueness
    across the fleet is only checked by the programme at goods-in.
13. **Acoustic ceiling.** T28 is once per lot and T17 only reads the clamp back. A codec
    register default that changes with a firmware revision escapes every per-unit step
    unless the clamp value is re-established for that image.
14. **Everything above the USB cable.** The browser worker, the websocket, the ingest
    service and the server-side signature verification are not touched by this document.
    T30 is not an exception: it tests the first of the study's three links, instrument to
    computer, and nothing above it. TOOL-EEG-022 section 1.1 draws the same boundary.

## 16. Open decisions

| # | Item | Owner | Gate |
|---|---|---|---|
| 1 | **E-20 is closed.** RFQ-EEG-001 Rev E, the revision this document governs to, carries the split verbatim: 30 minutes at 1000 Hz per unit plus a three-hour soak at 1000 Hz on one unit per lot, which is what section 8 and section 14 test. The Rev D reading of "three hours per unit" is superseded, and a bidder quoting against this document is quoting the test the RFQ asks for | programme | Closed at RFQ Rev E |
| 2 | **ECO-EEG-023 is not in the netlist.** U7 is still powered from AVDD and AVSS in `design.py`, so ENV_CMP has 20 mV of logic margin as built. The re-power and re-reference must be cut in and checked by the safety and layout reviewer | programme | ECO, and a review gate |
| 3 | **ECO-EEG-024 is applied, and the item that replaces it is the sign-off.** Corrected 2026-09-02: `tools/design.py` fits **68 kOhm** at R1 to R16, so S-02's single-fault current is 36.8 uA against 50 uA and the limit is met in the design. Rev C's "ECO-EEG-024 is not fitted; 47 kOhm is on the prototypes and S-02 fails at 53.2 uA" is superseded on that date. **What is still open**: the figure is calculated and no unit has been built to measure it on, and **SR-01 is not discharged** -- the electrical safety reviewer of RISK-EEG-011 section 7 owns the disposition and that review has not started. E-10 moves with it to its +/- 1.0 dB branch (T22) | programme, safety reviewer | Blocks use on a person, not Phase 2 |
| 4 | **S-04 thermistor and the E-23 45 degC inhibit.** There is no NTC net and no thermistor way. This is a hardware hole with no closure proposed | programme | Blocks the S-04 and E-23 claims |
| 5 | **The contact-light phase driver now exists** (T11 Note 1, `firmware/main/main.c`, 2026-09-02) and T11 is written against it, so the item as Rev C stated it is closed. **What replaced it, and what replaces that**: this row read that `LOFF_SENSN` was never written, so the red term `LOFF_STATP AND LOFF_STATN` could never be set and a site with no contact displayed amber. It also observed that enabling it would not be a one-line change, because `MISC1` = 0x20 puts SRB1 on every channel's negative input. That observation was the answer: the montage is single-ended and there is no per-site negative electrode, so FW-D17 (2026-09-02) dropped the N half entirely and sweeps the positive-side comparator threshold instead. All three colours are reachable. **What is open now** is that the two `COMP_TH` settings are the ADS1299's documented endpoints rather than measured trip points, so the impedance at which a site turns amber, and the one at which it turns red, are unknown until a unit is characterised -- which makes T11's reference resistances provisional | firmware, with DSN-EEG-003 section 11 for E-27 | T11's colour boundaries, not the step and not the red state |
| 6 | **E-17 has no method.** A reference level exists; a procedure for "-40 dB relative to a 70 dB SPL voice at the boom" does not, and neither does a definition of "maximum stimulus level" | programme | Blocks the E-17 type test |
| 7 | **Isolator host connector.** The named module presents USB-B where E-24 asks for USB-C; WH-09 is the interim pigtail until a USB-C module is qualified | programme | Live non-conformance |
| 8 | **J15 to J17 are not sourced.** `design.py` names Staubli SLB1,5-F as a class, not a confirmed PCB part; a touch-proof 1.5 mm socket with a PCB-mount signal pin and two 1.5 mm retention posts must be first-articled, against a 12-week lead-time risk | programme | Blocks Phase 2, and T23 tests a part that is not yet bought |
| 9 | **VID and PID** are placeholders pending a pid.codes allocation. T5 and T6 record whatever is programmed | programme | Blocks the fleet, not the prototypes |
| 10 | **The host stream-decoding tool does not yet exist.** Eleven steps produce numbers that only a decoder can produce -- T7, T8, T9, T10, T12, T13, T14, T15, T16, T26 and T27 -- and nothing in the package decodes a channel and reports a microvolt. **The connectivity test program is no longer part of this item, because it now exists**: TOOL-EEG-022 Rev A ships as `webtest/EEG-Connectivity-Test.html`, it is run per unit as **T30**, and the protocol code it runs is proved against the shipped firmware source by `webtest/tests/interop/run.sh`, which is condition (e) of the section 4 readiness gate. It takes no measurement, so it closes none of the eleven steps above. The provisioning script is likewise not part of this item: `firmware/tools/provision.py` exists and its ten steps are documented in FW-EEG-001 section 7, so T6 has the script it needs. **Was: "the host test tool `eegtest` does not yet exist".** That name is withdrawn: it named no file in any revision of this package, and the host-side tools that do ship are TOOL-EEG-022, `firmware/tools/provision.py` and `firmware/tools/verify_stream.py`. The remaining naming divergence is FW-EEG-001 open item 12 | programme | Blocks T12 to T17 |
| 11 | **The DevKit 3V3 rail is measured, not solved.** 288 mA calculated, about 0.5 W in a closed pod. If T3 reports a case temperature above 85 degC, a carrier-side 3.3 V regulator fed from V5V is an ECO against Rev C | programme | Phase 1 measurement |
| 12 | **Fixture naming is settled: section 6.1 is the authority and JIG-EEG-009 Rev B follows it.** The colorimeter head is FIX-01/E, the per-unit 2500 V AC station is deleted, "Part" is no longer used for a sub-assembly, and H-A, H-B, H-C, CPL-V, CPL-R and FIX-04/H-D are withdrawn. What is still open is hardware rather than naming: **FIX-02/C, the artificial ear and the class 1 sound level meter that T28 needs, is not yet built, priced or on the calibration schedule** | programme | Blocks the T28 type test, not the per-unit line |
| 13 | **No safety engineer has reviewed this design.** T20 and T23 are routine evidence for that reviewer, never a substitute for the review. **No hardware in this package has been built or measured** -- the firmware image of section 4 is the only thing that has been built, and it has run only under emulation. *Corrected 2026-09-02 from "Nothing in this package has been built or measured"* | programme | Blocks use on a person |
| 14 | **The routing closes, and it has not been reviewed.** The Rev B DRC report records zero violations, all 145 nets connected, every net one connected copper island and both inner planes continuous under the analogue zone, so the ECO-EEG-016 section 3 gate is met and the data is **released for review under RFQ-EEG-002A**. It is **not released for fabrication**: routing produced by the programme's own tools has not been seen by a human layout engineer, and 169 connections are relaxed -- 36 narrower than the 0.25 mm preferred width, 133 at full width with a reduced gap, all at or above the 0.20 mm minimum conductor and gap. Until that review is done and boards are made, **no board exists to test** | programme, layout engineer | Blocks T0, and therefore every step in section 8 |
| 15 | **The T9b CMRR limit has no requirement behind it.** RFQ section 9.1 item 6 names CMRR as one of the things T9 measures and states no figure, and RFQ section 5 carries no CMRR E-item at all, so T9's >= 100 dB is set by this document alone. Either an E-item states the figure, or T9b records CMRR without a pass/fail decision | programme | A unit is accepted or rejected against a limit no requirement carries |
| 16 | **E-11's 50 Hz +/- 10 % low-pass band cannot be met with the approved parts.** A 100 nF C0G in 0603 / 50 V is not a stocked part, so C21, C41 and C61 are X7R at +/- 15 % over temperature and f0 moves between 42.4 and 57.4 Hz against a 45 to 55 Hz band. T12e now measures and records f0 against the 42 to 58 Hz the parts can hold. Either RFQ E-11 is restated to that band or a stocked C0G part is qualified. **ECO-EEG-019 and AVL-EEG-017 both record that "the Sallen-Key corner tolerance in TST-EEG-004 is widened to match"; before T12e there was no f0 limit in this document to widen, and T12e's band is the one this specification sets** | programme | Blocks the E-11 claim, not the line |
| 17 | **What the record's SHA-256 is taken over is not ruled.** Section 12 requires the SHA-256 of the JSON on the certificate and does not say what it covers, and a file cannot contain its own hash. `records/` proposes the record serialised as UTF-8 JSON with sorted keys, a two-space indent and a trailing newline, with `signatures.record_sha256` set to sixty-four zeros, and implements that identically in the generator and the validator. Until it is ruled, two manufacturers can both be right and disagree | programme | Blocks the first signed record, not the build |
| 18 | **The schema has never seen a real record**, because no unit has been built. It is checked against its own worked example and against eleven deliberate defects in `validate_test_record.py --selftest`, which proves the checker and not the fit to a manufacturer's data. The first Phase 1 record is where a field that is the wrong shape will be found | manufacturer, at the first unit | Closed by the first real record |

## 17. Revision history

| Rev | Date | Change |
|---|---|---|
| A | 2026-08-31 | Eighteen rows inside DSN-EEG-003 Rev A.2 section 6 |
| B | 2026-09-01 | Standalone specification. T00, T0 and T19 to T27 added; T7, T9, T10 and T12 rewritten; uncertainty budgets, traceability matrix, record and certificate templates, time budget, sampling rationale, type-test list, escape analysis and open-decision register added. Aligned to EEG-CAR-01 Rev B and ECO-EEG-001 to ECO-EEG-014 |
| C | 2026-09-01 | Corrected to the 150.0 x 130.0 mm four-layer carrier; published the definitive step list T00 to T29 and the TP1 to TP18 table; renamed the fixtures FIX-01 to FIX-04; added T28 (E-29 maximum acoustic output) and T29 (S-09 lithium marking); corrected the group delay to 4.40 ms, the 10 uV limit to +/- 5 %, the frame payload to 50.7 kB/s, D1 to D16 to BAV99, the headphone load to 47.0 Ohm, R85 to 150 kOhm, E-04 to -80 dB, E-10 to +/- 0.5 dB with the fitted 47 kOhm and +/- 1.0 dB only with ECO-EEG-024, E-11 to <= 2 Hz and F-06 to 90 s; stated S-02, S-04, E-23 and E-27 plainly as not met; deleted every E-28 deviation note and the per-unit hipot. **Corrections within Rev C, after the second cross-document audit of 2026-09-01: findings 1.3, 1.4, 1.7, 2.3, 2.4, 2.5, 4.2 and 4.3 are closed** -- section 6.1 now publishes the authoritative FIX-nn/X sub-assembly table, T28's place in the section 14 type-test list is confirmed, the routing result and the NOT RELEASED FOR FABRICATION status are stated wherever the board is described, the step count is stated as thirty-one, WH-EEG-008's harness steps are cited as H1 to H10, the lead-off references are the E96 values 4k99/10k0/49k9, RUL-EEG-021 replaces every citation of the uncontrolled `tools/RULINGS.md`, and E-10's two bands are stated together. **Four further corrections within Rev C, from the third cross-document audit of 2026-09-01:** section 5 and section 6.1 no longer say FIX-02/C is built, priced and carried in JIG-EEG-009's bill of materials and calibration schedule -- it is none of those, which is what JIG-EEG-009 section 7 and section 16 item 12 here have said all along; FIX-01/F's output impedance is corrected from "about 90 Ohm" to the **18.0 Ohm** JIG-EEG-009 section 1.3 derives, with the Johnson-noise figure recomputed to 0.0046 uV RMS; SIM-EEG-018's "four known open items" is labelled as the simulation's own scope against the sixteen of section 16 and the fourteen of RFQ-EEG-001 section 12; and T9b's CMRR >= 100 dB is marked provisional in the limit row itself, not only in the row above it |
| C | 2026-09-02 | **The routing closes.** The Rev B DRC report now records zero violations, all 145 nets fully connected, no net without copper, both inner planes continuous, 3 745 track segments and 552 through vias. Every statement in this document that was gated on the twenty-five open items -- section 1, the T0 note, the section 14 creepage row, escape-analysis item 2 and section 16 item 14 -- is restated: the data is **released for review under RFQ-EEG-002A** and **not released for fabrication**, because no human layout engineer has looked at routing produced by the programme's own tools. The two 0.328 mm electrode-clearance vias are gone; the measured clearances are corrected to 0.260 mm on L1, 0.285 mm on the planes and 0.275 mm on L4; and the **169 relaxed connections** are stated wherever routing quality is discussed. T0's blocking reason is corrected from the unreleased data to the fact that no board has been fabricated. S-02, E-23 and S-04 are untouched by any of this and remain not met |
| C | 2026-09-02 | **Corrections from the fourth cross-document audit, and one new step.** **T30 is added**: TOOL-EEG-022 Rev A, the browser connectivity test program, exists as `webtest/EEG-Connectivity-Test.html`, and a manufacturer following Rev C as issued would never have been told to run it. It is numbered, timed in section 11, given record fields in section 12 and traced in section 10, and its build-verification harness `webtest/tests/interop/run.sh` becomes condition (e) of the section 4 firmware readiness gate. Section 16 item 10 is corrected: the tool it said did not exist now does, the name `eegtest` is withdrawn as naming no shipped file, and what remains open is the stream-decoding tool that the eleven decoding steps need. **The pad census is corrected**: the carrier has 636 pads of which 620 carry a net, the two figures derived from `kicad/EEG-CAR-01_RevB_PCB_spec_sheet.txt` and `kicad/gerber/EEG-CAR-01-IPC-D-356A.ipc`; the "614 netlist pins" of section 1 and T0 is **withdrawn** as a count of distinct pin names rather than pads, six short because three four-pad tactile switches carry two pin numbers each, and T0's netlist filename is corrected to the file the package actually ships. **The production-simulation figures are corrected to the tool's own output**, `171 passed, 0 failed, 5 open`, and Rev C's "169 checks passed, none failed, four known open items" is withdrawn. **RFQ-EEG-001 Rev E section 12 lists fifteen items, not fourteen**, and its item 15 is the E-11 low-pass item, so this document's claim that the E-11 item exists only here is withdrawn; the T9b CMRR item still does. The E-28 note in section 3 is corrected from "RFQ Rev D" to RFQ-EEG-001 Rev E, which is the revision this document governs to. The step count is restated as **thirty-two** |
| C | 2026-09-02 | **The per-unit record becomes machine-readable, revision letter unchanged.** Section 12 has said since Rev C that the field counts are "fixed so a record can be validated mechanically" and the package shipped nothing to validate against: no schema, no example, no lot-summary template and no certificate template. `records/` now carries all four plus a validator, generated from one table by `records/make_records.py`, which reads the step list out of section 2 and refuses to run if the document and the table disagree. Every field count in section 12 is a `minItems` equal to `maxItems` pair in the schema; the `unit`, `limit` and `uncertainty` strings are `const` values taken verbatim from section 8. Section 13 now names the certificate template. Two things are **added rather than found**: what the record's SHA-256 is taken over was never stated and is proposed in section 16 item 17, and the schema has never seen a real record, which is item 18. Section 3 now states which of the three renditions of this document governs, after the `.docx` and `.pdf` were left behind the `.md` for fifty-five minutes on the day T30 was added |
| C | 2026-09-02 | **T11 is written against a driver that now exists, and the one thing it still cannot reach is named.** `firmware/main/main.c` implements E-27's bicolour phase scheme: the ADS1299's positive-side lead-off comparator is read at two thresholds, the colour per site is trips neither **green**, trips the sensitive threshold only **amber**, trips both **red** (FW-D17 -- as first written it used both halves of the status word and red was unreachable), and the two phases alternate with green in phase A, red in phase B and amber in both. Every statement in this document that was gated on the driver not existing is restated -- the section 4 readiness gate, T9c, T11, the E-27 traceability row, escape-analysis item 11 and section 16 item 5. T11's procedure is rewritten to produce the three states **at the electrode inputs with FIX-01's relay matrix**, because the colour is computed from lead-off and cannot be written to the shift register by a host command. Two things are stated rather than smoothed over. The alternation **quantises to the FreeRTOS tick**: `LIGHT_PHASE_HZ` is 240, the half-phase is 2 ms on a 1 kHz tick, and the unit alternates at about **250 Hz** against E-27's "above 100 Hz" -- 300 ms of colorimeter integration is 75 whole periods of it. And **`LOFF_SENSN` is never written**, so the red term can never be set and a site with no contact shows amber; that is carried as a finding in T11 Note 3, in section 16 item 5 and in escape-analysis item 11, and it belongs to the firmware owner with E-27's owner. T12 gains Note 4: the FIX-02/D comparator threshold is commanded at 1.650 mV per count over a 0 to 1.650 V range and is set to 50 % of a **measured** burst amplitude per headphone-amplifier model. No limit in this document changes. The step numbers, the field counts of section 12 and the `records/` schema are untouched |
| C | 2026-09-02 | **Three things this document said were not true stop being said, revision letter unchanged.** **The firmware is built.** Section 4's "the firmware has never been compiled for the target or run on hardware, and five drivers are stubs" is superseded: `firmware/release/` carries a bootloader, partition table, OTA data and a 405,360-byte application image built with **ESP-IDF v5.2.5** for **esp32s3**, with a `manifest.json` of their SHA-256, and `qemu_boot.log` is a full boot cycle on `qemu-system-xtensa -M esp32s3` in which this package's partition table is read, the app loads from the factory slot and `app_main()` runs. It has **never run on hardware** and QEMU emulates none of the peripherals, so the readiness gate is still not met and every DEFERRED step stays deferred -- condition (c) fails on the **block-signing task**, which `main.c` line 832 still marks "not shown". T11 Note 1's deferral reason is corrected from "no image has been built" to "no unit exists". **S-02 is met in the design.** ECO-EEG-024 is applied in `tools/design.py`: R1 to R16 are **68 kOhm**, the single-fault current is **36.8 uA** against 50 uA, and E-10 moves to the **+/- 1.0 dB** branch it already carried. Rev C's "47 kOhm is fitted and S-02 fails at 53.2 uA" is superseded wherever it appeared -- section 3, T22, T23, the E-10 and S-02 traceability rows, the certificate limitation, escape item 4 and section 16 item 3 -- and the 47 kOhm figures are kept beside the new ones as the superseded set. **This is met in the design and not signed off**: nothing is measured, no unit exists, and SR-01 stays with the electrical safety reviewer, who has not started. T10's calculated lead-off expectations become 70.5 / 75.1 / 111.5 kOhm and T8's noise expectation 0.31 uV RMS, both figures the document already carried as the ECO case. **Two counts are corrected.** T0's netlist figures become **552 via records and 1 172 test points**, counted in `kicad/gerber/EEG-CAR-01-IPC-D-356A.ipc` (788 type-317 plus 384 type-327); section 3's "section 16 lists sixteen items" becomes **eighteen**; the production simulation becomes **193 passed, 0 failed, 6 open** with SIM-EEG-018 Rev A's own list; and the section 4 interop harness result becomes **49 passed, 0 failed over nine groups, fourteen opcodes**. **One reconciliation is deliberately not made**: SIM-EEG-018 no longer holds E-11's low-pass half open, because `design.py` has rescaled the Sallen-Key to C0G, while section 16 item 16 and the T12 rows still describe the X7R build. That is a change to a limit's basis; it needs an ECO and this document's owner, and section 3 now says so. `tools/DESIGN_FACTS.md` section 8 item 3 and RISK-EEG-011 section 4 are cited here and are owed the same corrections |

A change to any limit in this document requires an ECO under ECO-EEG-016 and a change note
against DSN-EEG-003. The manufacturer may not change a limit, a record length or a fixture
arrangement without one. This document owns the T-numbers; no other document may create,
renumber or reassign one.
