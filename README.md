# EEG Field Kit — Design & Production Package v2.4

**TI One Voice research programme** — [one.witysk.org](https://one.witysk.org), Brussels, Belgium
Board revision B · 2 September 2026

The complete manufacturing package for **EEG-CAR-01 Rev B**: a battery-powered, 16-channel EEG headset
built around an ESP32-S3 carrier board, together with the helmet and enclosure, the electrode harness,
the firmware, the production test programme and fixtures, and all the packing, quality and regulatory
documentation needed to produce the finished kit — flight case included.

The package is designed so that a manufacturer can quote, review and build from it directly: the
Gerbers, drill files, netlist, BOM and CPL files are included, along with every printed part, the
assembly work instructions and an end-to-end test programme that runs from Chrome over USB. For the
study itself — participants, collaborators, grant bodies and funders — see
[one.witysk.org/studies](https://one.witysk.org/studies).

---

## Status at a glance

**Nothing in this package has been manufactured or measured.** No board has been fabricated, no part
has been printed, no firmware has been flashed to silicon, and no electrode has touched a person.
Every performance figure is calculated, and each is labelled as calculated where it appears.

| Area | State |
|---|---|
| Carrier board routing | **Complete.** 145 of 145 nets connected, 0 DRC violations. **Released for review under RFQ-EEG-002A — not yet released for fabrication:** no human layout engineer has reviewed it, and 169 connections close at relaxed width or gap. |
| Firmware | **Built and boots under QEMU** (ESP-IDF v5.2.5, esp32s3). Never run on real hardware — no hardware exists. |
| Mechanical parts | 29 STL + 28 STEP released. Nothing has been printed. Foam case insert **not released for cutting** until the helmet shell is measured. |
| Test programme | Written and self-tested (57/57 interop checks). Never run against a physical unit. |
| Production simulation | 193 checks passed, 0 failed, 6 open items. |
| Safety | **Not done.** The safety review gates Phase 2; nothing goes on a head before it. |

**Read [`KNOWN_ISSUES.txt`](KNOWN_ISSUES.txt) before quoting or building anything.** It is the short
list, in one place, of what is wrong with the data as shipped — 6 open items and 22 unapproved
assumptions in 15 sections. Everything in it is also in the controlled documents; the file exists so
that problems are found here rather than at CAM time.

---

## Orientation — read in this order

1. **`README_package_index.txt` + `KNOWN_ISSUES.txt`** — the orientation pair. The index says what
   every folder is for and gives the rebuild commands (its header is stale at v2.2; this package
   is v2.4).
2. **`docs/RFQ-EEG-001 Rev E`** — the actual request: numbered requirements (E-, S-, F-, T-), the
   pricing template, and §9.4's correction-iteration terms for prototypes that arrive not working.
3. **`docs/DSN-EEG-003 Rev C`** — the governing document. Architecture, the carrier board, and the
   precedence rules that decide which document wins when two disagree.

**Precedence:** DSN-EEG-003 Rev C > RFQ-EEG-001 Rev E > ICD-EEG-006 > SCH-EEG-005 > DSN-EEG-002 >
PARTS-EEG-019 > RUL-EEG-021 > the bidder BOM. Where a number appears in a document *and* in
`tools/design.py`, **design.py governs** — `tools/emit_all.py` regenerates every fabrication file
from it in one pass, so the package cannot drift.

---

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | 21 controlled documents (Rev-controlled, in `.md`, `.docx` and `.pdf`): the RFQ, the manufacturing design package, interface control, schematic set, assembly work instructions, harness wire list, test specification, fixture design, quality plan, risk & safety pack, regulatory file (incl. lithium shipping UN3481/PI967), service & refurbishment, participant card, packing & labelling, change control, approved vendor list, production simulation, part register, firmware build & provisioning, rulings register — plus the three workbooks: bidder BOM, internal costed BOM, manufacturer contacts. |
| `kicad/` | **EEG-CAR-01 Rev B fabrication pack:** routed `.kicad_pcb`, DRC report, BOM, two CPL files, fabrication/assembly/copper drawings, PCB spec sheet, machine-readable net report — and `gerber/`: 11 Gerber X2 layers, two Excellon drills, IPC-D-356A netlist, zipped, with a SHA-256 for every file. |
| `kicad/wh-bus-01/` | The second, tiny PCB: 14 × 10 × 0.8 mm bus board that splits the harness LED_V into eight contact-light tails. The helmet doesn't work without it. |
| `schematic/` | SCH-EEG-005 Rev B, an 8-sheet A3 schematic set (PDF + PNGs), generated from `tools/design.py`. Drawings only — there is no editable `.kicad_sch`. |
| `mech/` | Every printed and cut part: `stl/` (29 printable meshes), `step/` (28 parametric solids for dimensioning and inspection), `drawings/` (25 dimensioned sheets), `renders/` (25 shaded views), 7 foam-layer DXFs for the flight case, the hardware schedule and the mechanical release status. |
| `firmware/` | The ESP-IDF project (main.c, drivers, provisioning opcodes) and `release/`: four flashable ESP32-S3 images (bootloader, partition table, OTA data, app) with a SHA-256 manifest and the exact `esptool` command — no toolchain needed to program a board. `firmware/tools/` is the end-of-line provisioning station: ATECC608B keying, serial & calibration writes, signed-stream verification. |
| `webtest/` | **TOOL-EEG-022**, the connectivity test: one self-contained 52 kB HTML file an assembler double-clicks in Chrome to prove browser–computer–USB–device connectivity (no measurement, no server, nothing to install). The interop harness compiles the real `main.c` against ESP-IDF stubs and drives it with the real host protocol module — 57/57 checks green. |
| `fixtures/` | The four production test fixtures of JIG-EEG-009 as buildable data: PCB outlines and netlists (deliberately no copper), printed-part geometry, and RP2040 controller firmware speaking the FIXPROTO v1 line protocol. Nothing here has been built. |
| `records/` | The machine-readable per-unit test record of TST-EEG-004 §12: a JSON Schema, a stdlib-only validator, and a worked example (all-DEFERRED). No unit has been built, so the schema has never met real output. |
| `graphics/` | Board plots (four copper layers, fabrication drawing, drill map, assembly views, 3D renders) and `labels/`: the packing and marking artwork of PKG-EEG-015 — unit label, kit ID plate, 9 foam bay tags, carton set, lithium mark, tamper seal, disinfection card (22 SVG + 11 PDF). |
| `tools/` | The generator: 42 Python modules, 19,072 lines, 27 entry points. `design.py` is the single source of truth for the board; `mech_gen.py` for the printed parts. Five re-runnable verification gates check connectivity, DRC, placement, cross-document consistency and the 15-station production dry run. Every figure in this package can be regenerated from source. |
| `project/` | Why the kit exists: the 3-page partner proposal, the 161-page experiment design v4.2, and the 11-page project plan with its schedule and workstreams (supplier costs are placeholders). |
| `reports/` | Working DRC reports, metrics and the placement checklist from the routing campaign. |
| `constraints/` | Net rules used by the router. |

---

## The board

**EEG-CAR-01 Rev B** — 150.0 × 130.0 mm, four layers (L1 signal, L2/L3 reference planes split
AGND_REF/DGND, L4 signal), 30 connectors, 211 reference designators, 156 nets.

- 3,745 track segments, 552 through vias, 0 duplicates
- 145 of 145 nets one connected copper island; **0 DRC violations**
- Smallest clearance 0.260 mm, narrowest conductor 0.200 mm, smallest plated hole 0.300 mm
- No digital net in the analogue zone; exactly one AGND_REF-to-DGND bridge and one
  HARN_SHIELD-to-DGND bridge

The layout was produced by the programme's own constraint-aware autorouter and verified by
measurement on the finished polygons — but it has **not** been reviewed by a human layout
engineer. The DRC report lists every one of the 169 relaxed connections so a reviewer can go
straight to the places that need attention.

## Firmware

ESP-IDF v5.2.5, target esp32s3, Phase 1 configuration (secure boot off). Four release images with
SHA-256 checksums, a 920-line `main.c` with 16 host commands and 13 provisioning opcodes, drivers
for the ES8388 codec, SDMMC, ATECC608B, MAX17048 gauge and the envelope onset detector.

| What has happened | What it proves | What it does not |
|---|---|---|
| It builds, clean at `-Wall -Werror=all` | The image links and fits | That any of it is right |
| It boots under QEMU (esp32s3) | Bootloader, partition table and `app_main()` behave as written | Any peripheral — QEMU has no PSRAM, SD, ES8388 or ADS1299 |
| It agrees with the browser tool (57/57) | Framing, CRC, opcodes, the S-01 interlock | Anything about ESP-IDF or hardware |

**It has never run on silicon, and no hardware exists.** The SPI timing, every ADS1299 register
value, USB enumeration and the whole analogue front end are assumptions no silicon has answered.
F-08 (block signing) is unimplemented; the ATECC608B config template is only 4 of 128 bytes
reviewed — that write is irreversible, so it gates on a real part.

## Testing & quality

- **TST-EEG-004 Rev C** — the per-unit test: 32 steps T00–T30, with a 5,033-line JSON Schema and a
  stdlib-only validator so any two vendors emit the same record file.
- **JIG-EEG-009 Rev B + `fixtures/`** — four test fixtures as buildable data, with RP2040
  controller firmware passing 154 host checks.
- **TOOL-EEG-022** — the browser connectivity test (`webtest/EEG-Connectivity-Test.html`) and the
  interop harness that keeps firmware and protocol from drifting apart.
- **SIM-EEG-018** — a production simulation that walks one unit through all fifteen stations,
  purchase order to refurbishment: **193 passed, 0 failed, 6 open**.
- **ECO-EEG-016** — the change register that owns the document namespace and explains why
  everything is the way it is.

## Rebuilding the package from source

```sh
python3 tools/run_build.py          # route, pour, check            (~20 min)
python3 tools/emit_all.py --cached  # Gerbers, drawings, schematic
python3 tools/emit_extras.py        # spec sheet, netreport, STEP, manifest
python3 tools/mech_gen.py           # STL and STEP for every printed part
python3 tools/mech_drawings.py      # dimensioned drawings and renders
python3 tools/emit_workbooks.py     # the three spreadsheets
python3 tools/simulate_production.py --report docs/SIM-EEG-018_....md
python3 tools/make_docs.py          # A4 .docx and .pdf of every document

python3 tools/check_consistency.py  # cross-document consistency gate
python3 webtest/build.py            # rebuild the single-file connectivity tester
node webtest/tests/*.mjs            # protocol tests
sh webtest/tests/interop/run.sh     # firmware-vs-protocol interop (57 checks)
```

## Production phases

1. **Phase 1** — 2 prototypes
2. **Phase 2** — 10 kits
3. **Phase 3** — 10 to 40 further kits (25 to 50 total)

## Sponsorship

This study is run by a non-profit and funded by donations and grants that have not yet all been
secured. Any part of the work treated as sponsorship — a discounted prototype build, parts at
cost, donated units — is welcome, in return for named credit in the published open-hardware design
files, acknowledgement in the resulting papers and on the platform, and the case study of an
instrument you built being used in a pre-registered study.

## Licence & contact

Hardware and documents: **CC BY-SA 4.0** · Firmware: **MIT**

**Stephane van der Aa** — Founder, TI One Voice
[one.witysk.org](https://one.witysk.org) · stephane@stepvda.com · +32 493 70 16 01
