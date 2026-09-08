# EEG-CAR-01 Rev C -- work report

**Not a controlled document.** It is the report on the work of 8 September 2026 that
ECO-EEG-030 to ECO-EEG-033 record, and it says what was run, what the repository
contradicted, what was assumed, and what is still open.
**Licence:** CC BY-SA 4.0

---

## 1. What was run, and what it printed

### 1.1 Baseline, on the untouched tree

| Command | Result |
|---|---|
| `tools/emit_all.py --cached` | **run.** 0 violations, 145 of 145 nets connected, 3 745 segments, 552 vias, minimum clearances 0.260 / 0.285 / 0.285 / 0.275 mm. Every text output reproduced **byte for byte** against the committed files; only the PNG, PDF and zip outputs differed, on embedded timestamps |
| `tools/simulate_production.py` | **run.** 186 passed, 0 failed, 5 open -- **not** the 193 / 0 / 6 the register stated. See 2.1 |
| `kicad-cli --version` | **NOT RUN.** KiCad is not installed on this machine and could not be installed. No ERC and no DRC result is claimed anywhere in this work |

Four Python packages had to be installed before anything would run at all: `shapely`,
`scikit-image`, `numpy` (present) and `trimesh`. **`cadquery` could not be installed**: the
machine had 472 MB of free disk and `cadquery-ocp` needs several times that. `tools/mech_gen.py`
imports cadquery at module scope, so it cannot even be imported here, and **no printed part was
regenerated in this work**.

### 1.2 The Rev B geometry under the new rule set

`tools/grade_revb.py`, on the released `kicad/EEG-CAR-01_RevB_routed.kicad_pcb` and
`tools/routed.pkl`, census checked first (3 745 segments, 552 vias):

| Finding | Rule | Count |
|---|---|---|
| 1 | vias inside an SMD pad | **67** |
| 2a | dangling track ends | **5** |
| 2b | redundant copper loops outside a plane | **221**, on 22 nets |
| 3 | angle below 90 degrees between two segments | **171** |
| 3 | segments off a 0/45/90/135 degree axis | **158** |
| 4 | off-centre pad entries | **299** |
| 5 | conductors under their class minimum | **322** |
| 5 | net classes on a forbidden layer | **50** |
| 5 | vias on a class that forbids them | **18** |
| | **total** | **1 311** |

The Rev B DRC report is **not withdrawn**. It measured the twelve rules it had, correctly.

Two counts in `tools/drc_geometry.py` were wrong before they were right, and both are recorded
in the source rather than quietly fixed. The loop check first modelled copper as touching
polygons and reported **3 356** loops, where three mutually touching polygons are not a loop;
re-modelled topologically -- junctions as nodes, segments as edges, T-junctions split -- it
reported **476**; excluding degenerate edges, where a segment's two ends land on the same via,
it reports **221**. The first two numbers are wrong and are not quoted anywhere else.

### 1.3 The schematic against the design source

`tools/sch_netlist.py` parses the emitted `.kicad_sch` files back -- pin geometry from their own
embedded `lib_symbols`, wires, junctions, labels, hierarchical labels, power symbols -- and
diffs. It does not ask the generator what it meant.

| | `design.py` | schematic |
|---|---|---|
| nets | 156 | **156** |
| pins | 614 | **614** |
| structural problems | -- | **0** |
| netlist differences | -- | **0** |

It found four real errors on its first run: R50, R51, R52 and R94 were wired by geometry rather
than by pin number and had pin 2 where `design.py` has pin 1, and R94/R95 were drawn as a
divider instead of two I2C pull-ups. A resistor is symmetric, so the circuit was right and the
netlist was wrong. Both are fixed and the helper that caused it now wires by pin number.

### 1.4 ERC, DRC and the collision check

| Check | State |
|---|---|
| `kicad-cli sch erc` | **NOT RUN.** KiCad is not installed |
| `kicad-cli pcb drc` | **NOT RUN.** Same |
| structural ERC (`tools/sch_netlist.py`) | **run: 0 findings.** Every pin on a net; no designator placed twice and every unit of a multi-unit part placed once; no accidental single-pin net; every power net driven by a power symbol |
| board read-back (`tools/emit_revc.py`) | **run: passes.** 211 footprints, 636 pads, 156 nets, **0 segments, 0 vias**, 37 locked, netlist identical to `design.py`, every rule area present under the name the `.kicad_dru` uses, project classes and all 156 assignments complete, `track_dangling` at error |
| footprint audit (`tools/footprint_audit.py`) | **run: 183 PASS, 0 FAIL, 3 OPEN, 0 UNRECOGNISED, 25 fabricated features** over all 211 designators |
| collision check (`tools/collision_check.py`) | **run: 15 findings. Three of its four cases are open.** See 1.5 |
| `.kicad_dru` bracket check | **run: 37 rules, balanced** |
| STEP structural check | **run: all files closed, no dangling entity reference.** **No STEP reader was available**, so no CAD kernel has opened them |
| `tools/simulate_production.py`, after | **run: 193 passed, 0 failed, 7 open** |

### 1.5 The collision check, in full

| Case | Result |
|---|---|
| A -- carrier parts against the plate underside | **clear.** Tallest is J15 at 10.00 mm against a plate underside at 18.0 mm |
| B -- the DevKit against the plate opening | **OPEN. The opening is 2 mm too short.** J6/J7 are 1x22, so the pin span is 53.34 mm and the ESP32-S3-DevKitC-1 PCB is 63.0 mm: it needs carrier Y 3.2 to 66.2 mm and MP-01's opening runs 4.0 to 65.0 mm |
| C -- modules against each other and jumper reach | **OPEN. Six of twelve cannot be placed**, and **four cannot reach their connector within the 60 mm of ICD-EEG-006 section 3.2 from any position on the plate** -- M4 to J10 is 86 mm at best, M5 to J11 is 72 mm at best. That 60 mm is a crosstalk limit |
| D -- plan area | **OPEN. 17 356 mm2 of modules into 12 409 mm2 of plate: 140 % fill** |

**Case D does not rest on the assumed envelopes.** The two ADS1299 boards alone are 7 345 mm2,
**59 % of the net usable plate**, and that figure is the Raspberry Pi HAT mechanical standard
rather than a guess: the PiEEG-8 is a Pi shield. **Halving every other envelope still leaves
12 351 mm2 against 12 409 mm2.**

### 1.6 Reproducibility

Two consecutive runs of `tools/emit_all.py` produce **byte-identical SHA-256 checksums across
all 51 files** of the handover set. Every uuid in the schematic is uuid5 over a fixed
namespace, so a regeneration is diffable against the last one.

---

## 2. Where the repository contradicted the brief

| # | The brief said | The repository says |
|---|---|---|
| 1 | the simulator's last run was **193 passed, 0 failed, 6 open** | On this machine the untouched tree printed **186 / 0 / 5**. Six checks need `cadquery` and one open item needs `trimesh`; installing `trimesh` gave 187 / 0 / 6, and `cadquery` could not be installed. **The register's 193 was obtained on a machine with cadquery.** The run behind this work prints **193 / 0 / 7** and is *not the same 193*: six checks were added and six lost, and they cancel. A machine with cadquery would print **199** |
| 2 | "four op-amp packages moving from SOIC to TSSOP" | **Three.** U1, U2 and U3. There is no U4; U7 is the SOT-23-5 comparator |
| 3 | the Murata part number should be corrected "if it does not encode 600 Ω" | The part number **does** encode 600 Ω -- Murata's own numbering page reads the three figures as two significant digits and a count of zeros, so `601` is 600 Ω. The reviewer's reading was wrong. **The defect is elsewhere and is real**: `PG` is the large-current series and it is not made at 600 Ω in 1608, whose range stops at 470 Ω. `BLM18PG601SN1D` is not a part. Corrected to `BLM18AG601SN1D` |
| 4 | three BOM errors | **Four.** `Omron B3F-4055` is a **12 x 12 mm** switch on a 6 x 6 mm land pattern, and at 260 gf it also misses AVL-EEG-017's own 160 ± 50 gf window. Found by the audit the brief asked for, not by any reviewer. Corrected to `B3F-1052` |
| 5 | ICD-EEG-006 section 1 is the one home of the connector table | **Four of its coordinates disagreed with `design.py`**: J4 (41.0, 36.0 against 41.0, 50.0), J9 (66.0, 78.0 against 114.0, 62.0), J22 (30.0, 116.0 at 90° against 15.7, 73.5 at 270°) and J26 (128.0, 104.0 against 117.0, 8.0). Two moved at ECO-EEG-018 and the table never followed. `design.py` governs; the table is corrected and RUL-EEG-021 ruling 6 is added |
| 6 | `design.py` carries 68 kΩ (ECO-EEG-024) | The **value** did. `design.py`'s `NOTES`, which are printed onto the fabrication and assembly drawings, still said **47 kΩ**; also said the analogue rails arrive at "J2 pins 11-14", where J2 has ten ways and they arrive at J23; and said the keep-outs are clear "on both layers" on a four-layer board. All three corrected |
| 7 | emit `kicad/EEG-CAR-01_RevC_unrouted.kicad_pcb` **and** `EEG-CAR-01_RevC.kicad_pro` | **Those two names are incompatible.** A KiCad project expects its board to share the project's stem; a differently named board opens standalone, without the net classes, the 156 assignments or the DRC severities. The board is `EEG-CAR-01_RevC.kicad_pcb`. See open question 1 |
| 8 | the rule sheet is **one page** | It is **three**. See open question 2 |
| 9 | five release-state paragraphs say "released for review" | **Sixteen documents did**, sixty-two occurrences. The five named are corrected, and so are the other six live statements in the four documents this round re-issued. Eight documents it did not re-issue still carry it. See open question 3 |
| 10 | the DRC report is the authority for the routed result | It is, and it is authoritative **about the rule set it had**. RUL-EEG-021 ruling 5 now says that a DRC report states the rule set it measured against |

---

## 3. Assumptions

Every one is registered or flagged. None is a sign-off.

| # | Assumption | Where it is registered | Confidence |
|---|---|---|---|
| 1 | The twelve module envelopes, and their placement on MP-01 | **ASM-EEG-023 Rev B, MECH-D6-MODULE-ENVELOPES**, new and **blocks a build** | judgement. **No vendor drawing was consulted for any of them.** Two are form-factor derived: the PiEEG-8 is a Pi HAT (65.0 x 56.5 mm) and the Pololu S13V15F5 is a 0.5 x 0.8 inch board |
| 2 | `ELECTRODE` minimum width 0.25 mm, above the board's 0.20 mm floor | `tools/rules.py`, flagged `confirm`; printed in LAY-EEG-034 section 5 | judgement. Open question 4 |
| 3 | `ELECTRODE` on L1 only, no vias | same | DSN-EEG-003 section 3.3 rule 3 read literally. Open question 4 |
| 4 | `ANALOGUE_REF` minimum width 0.30 mm | same | impedance, not current. Open question 4 |
| 5 | Pad entry within 25 % of the pad's minor dimension | `tools/rules.py`; LAY-EEG-034 section 6 | judgement: finding 4 has no number in it |
| 6 | The schematic sheet split, nine sheets | `tools/emit_kicad_sch.py`, checked to be a partition of `design.C` | judgement |
| 7 | KiCad 8 -- `(kicad_sch 20231120)`, `(kicad_pcb 20240108)` | the handover README, with an offer to re-emit | assumed, as the brief instructed. Open question 5 |
| 8 | Carrier component heights per footprint class | `tools/mech_bodies.py`, each with its source | datasheet, except the DIN 42802 socket at 10.00 mm, which has no qualified part |
| 9 | The DevKit stands 13.6 mm and its PCB is 63.0 x 25.5 mm | ICD-EEG-006 section 4 (*calculated*) and Espressif's published outline | derived |

---

## 4. Open questions

**1. The board file name.** The brief asked for `EEG-CAR-01_RevC_unrouted.kicad_pcb` beside
`EEG-CAR-01_RevC.kicad_pro`. A KiCad project expects board and schematic to share its stem, and
a board opened standalone loses the eight net classes, the 156 assignments and the severity that
makes `track_dangling` an error -- most of the specification.
*Recommended default, and what is implemented:* the board is `EEG-CAR-01_RevC.kicad_pcb`, and
that it is unrouted is said in its title block, its comments, LAY-EEG-034 and the README.

**2. The rule sheet is three pages, not one.** Compressing it means dropping the derivation of
each net-class number, and a rule whose reason is invisible is a rule that gets relaxed at the
first difficulty.
*Recommended default:* leave it at three. If one page is needed for the order paperwork,
sections 5 and 6 alone fit on one and the rest becomes an annex.

**3. Eight documents still say the data is "released for review".** ASM-EEG-007, PARTS-EEG-019,
QP-EEG-010, REG-EEG-012, RFQ-EEG-001, RISK-EEG-011, SVC-EEG-013 and TST-EEG-004. Three of them
are out of scope by instruction (RISK-EEG-011, REG-EEG-012 and the research documents), and
RFQ-EEG-001 additionally carries E-26's self-contradicting switch class.
*Recommended default:* one sweep ECO covering the five that are not out of scope, plus the RFQ
at its next issue. It is mechanical and it is the defect RUL-EEG-021 section C ruling 4 forbids.

**4. Four net-class numbers need your confirmation** before the order goes out, because they
constrain the contractor and they are this programme's proposals, not transcriptions: the
`ELECTRODE` minimum width of 0.25 mm; `ELECTRODE` restricted to L1 with **no vias at all**; the
`ANALOGUE_REF` minimum width of 0.30 mm; and the 25 % pad-entry tolerance.
*Recommended default:* confirm all four. The electrode restriction is the one worth a second
look -- it is DSN-EEG-003 section 3.3 rule 3 read literally and it is achievable on the present
placement, but if the contractor says it forces a respin, relaxing it is a decision and not a
concession to be made silently.

**5. Which KiCad version is JLCPCB on?** Everything is emitted for KiCad 8. Re-emitting for
another major version costs nothing because it is generated.
*Recommended default:* ask Lyle He before the order and re-emit if the answer is not 8.

**6. MP-01 cannot carry twelve modules.** 140 % fill, and the plate's DevKit opening is 2 mm
short. Four routes would each move it -- a larger plate; a second tier of standoffs; an ADS1299
breakout that is not a Pi HAT, which AVL-EEG-017 section 2 M1 permits under qualification even
though the *device* may not change; or moving the modules whose jumpers cannot reach onto the
carrier as fitted parts. **None is decided and none is costed.**
*Recommended default:* buy one of each module and measure it before deciding anything, because
ten of the twelve envelopes are assumptions. The two that are not -- the ADS1299 boards -- are
59 % of the plate on their own, so **the measurement most likely to settle it is the PiEEG-8's
actual outline.**

**7. Should the in-house router produce a reference route for comparison?** It was not done:
the brief puts it last and everything ahead of it took the time.
*Recommended default:* no, until the contractor's placement is in. A reference route against a
placement nobody has confirmed compares two guesses.

**8. `firmware/main/board_pins.h` is still hand-maintained** against a check in
`tools/simulate_production.py`. Untouched here, as instructed; no pin assignment moved, so it
did not need to move.
*Recommended default:* leave it until a change forces a pin move, then generate it.

---

## 5. The handover set

`kicad/RevC_layout_inputs/` -- **51 files, 2.6 MB**, with `SHA256SUMS.txt` carrying a SHA-256
and a one-line description for each. The manifest is the authority and is not reproduced here.

| Group | Files |
|---|---|
| project | `EEG-CAR-01_RevC.kicad_pro` |
| schematic | `EEG-CAR-01_RevC.kicad_sch` + nine sheets, `EEG-CAR-01.kicad_sym` |
| board | `EEG-CAR-01_RevC.kicad_pcb`, `EEG-CAR-01_RevC.kicad_dru` |
| netlist and BOM | `EEG-CAR-01_RevC-IPC-D-356A.ipc`, `EEG-CAR-01_RevC_BOM.csv`, `footprint_audit_RevC.md` |
| placement | two provisional CPLs, `EEG-CAR-01_RevC_outline_and_fixed_connectors.dxf` |
| 3D | 22 footprint bodies under `step/footprints/`, three assembly bodies under `step/` |
| evidence | `EEG-CAR-01_RevC_schematic_netlist_check.txt`, `EEG-CAR-01_RevC_collision_check.txt` |
| rules | `LAY-EEG-034_RevA_carrier_layout_rule_sheet.pdf` and `.md` |
| covering note | `README_layout_inputs.md`, `SHA256SUMS.txt` |

**Nothing was sent.** No tool in `tools/` transmits anything.

---

## 6. Commits

| Commit | Work package |
|---|---|
| `c652258` | **WP1** revision bookkeeping and the Rev B withdrawal ECO (ECO-EEG-030) |
| `34feea1` | **WP2** BOM and footprint corrections (ECO-EEG-031) |
| `553bec1` | **WP3** the seven findings encoded as rules, and Rev B regraded (ECO-EEG-032) |
| `e15724c` | **WP4** the native KiCad schematic (ECO-EEG-033 part 1) |
| `b142243` | **WP5** unrouted board, project file and DXF (part 2) |
| `9e96ce1` | **WP6** 3D bodies and the collision check (part 3) |
| `0fb4e9d` | **WP7** LAY-EEG-034, the layout rule sheet (part 4) |
| `4b87f44` | **WP8** the handover set and its README (part 5) |
| `385429a` | **WP9** document register close-out |
| `17c02ad` | **WP9 (cont)** release-state statements in the four re-issued documents |

Documents advanced a letter: DSN-EEG-003 to **D**; ECO-EEG-016, ICD-EEG-006, JIG-EEG-009 and
AVL-EEG-017 to **C**; FW-EEG-001 to **D**; ASM-EEG-023 and RUL-EEG-021 to **B**. **LAY-EEG-034
is new at Rev A.** 218 citations and 24 file names followed, by `tools/revision_bump.py`.

---

**Nothing in this package has been manufactured or measured. No safety engineer has reviewed
this design. No layout engineer has seen Rev C, because Rev C has no layout yet.**
