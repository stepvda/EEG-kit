# EEG field kit — package v2 design facts

**This file is the fact base every document in package_v2.3 must agree with.**
**It is superseded, where they differ, by RUL-EEG-021 -- the rulings register -- which
records the answers made after the cross-document audit of 1 September 2026.**
It is maintained by hand alongside `design.py`; where a number appears in both, `design.py`
governs and this file is corrected to match. Date 2026-09-01. Board revision B.
**This file is not on ECO-EEG-016 section 1.1's controlled list, so it is not itself part of
the release, yet ICD-EEG-006, WH-EEG-008, TST-EEG-004, JIG-EEG-009, SVC-EEG-013 and
AVL-EEG-017 cite it as an authority. Where it differs from a controlled document, the
controlled document governs.**

**Two things changed during layout and every document carries them.** The carrier grew from
130 x 124 mm to **150.0 x 130.0 mm**, and it went from two layers to **four**: L1 signal,
L2 reference plane, L3 reference plane, L4 signal. Both are engineering results rather than
preferences, and DSN-EEG-003 Rev C section 3 explains why. The enclosure grew with the board.

---

## 1. What the instrument is

A sixteen-channel research EEG instrument with co-registered audio, EMG and response
channels, streamed over an isolated USB link to a browser-based session runner. It is a
**loaned, circulating field kit**: shipped to a participant, used for two or three
recording sessions at home, returned, refurbished, shipped to the next participant.
It is **not a medical device** and is not placed on the market.

Programme: TI One Voice research programme, Brussels, Belgium — one.witysk.org.
Licence: hardware and documents CC BY-SA 4.0; firmware MIT.

Phases: **1** — 2 prototypes. **2** — 10 kits. **3** — 10 to 40 further kits (25–50 total).

## 2. Architecture

Purchased, proven modules on one custom **four-layer** carrier, **EEG-CAR-01**.

| Block | Module | Carrier connectors |
|---|---|---|
| Analogue front end ×2 | ADS1299 8-channel breakout (PIEEG-8 class) | #1: J1 (1×12 digital), J2 (1×10 analogue signals), J23 (1×6 rails). #2: J3, J4, J29 |
| Controller | ESP32-S3-DevKitC-1-N16R8 | J6, J7 (1×22 each, 22.86 mm apart) |
| Audio codec | ES8388 module with headphone amplifier | J8 (1×14), J9 (1×4) |
| USB isolation | ADuM4160 module, host connector on the module. The named candidate presents **USB-B** where RFQ E-24 asks for USB-C: a live non-conformance, with the WH-09 USB-B-to-USB-C panel pigtail as the interim answer (RUL-EEG-021 §B) | J10 (1×4) |
| Secure element | ATECC608B breakout | J11 (1×4) |
| Power | bq24074-class charger + MAX17048 gauge | J12 (1×8), J13 (battery), J25 (1×6 buck-boost) |
| Storage | microSD breakout, **one-bit** SDMMC | J20 (1×8) |
| Voice microphone | fixed-gain preamp module **on MP-01**; the boom carries the bare capsule | J21 (1×6), J18 (1×4 pigtail) |
| Room microphone | MEMS/electret module with hardware mute | J28 (1×4) |
| Contact lights | 74HC595 shift register | J19 (1×16), J30 (1×10 harness) |

**Modules do not plug directly into the carrier.** They sit on the printed module plate
**MP-01** above the carrier and are joined with keyed 2.54 mm ribbon jumpers per
ICD-EEG-006. The one exception is the ESP32-S3-DevKitC-1, which is inserted directly
into J6 and J7.

## 3. Carrier board EEG-CAR-01 Rev B — the numbers

| Property | Value |
|---|---|
| Size | **150.0 × 130.0 mm**, rectangular, no cut-outs |
| Layers | **4**: F.Cu (L1 signal), In1.Cu (L2 plane), In2.Cu (L3 plane), B.Cu (L4 signal) |
| Material | FR-4, Tg ≥ 150 °C, 1.60 mm ± 10 %; 1 oz (35 µm) outer, 0.5 oz (17 µm) inner |
| Stack-up | mask / 35 µm L1 / prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask |
| Finish | ENIG, Au 0.05–0.10 µm over Ni 3.0–6.0 µm |
| Mask / legend | green LPI both sides; white legend both sides |
| Minimum track / clearance | 0.20 mm / 0.20 mm; most conductors are 0.25 mm or wider |
| Electrode-net clearance | 0.35 mm minimum to anything else |
| Vias | **0.60 mm pad / 0.30 mm finished hole**, through only, tented both sides |
| Plated holes | 0.30 mm (vias), 0.90 mm (JST PH), 1.00 mm (socket strips), 1.20 mm (tactile switches), 1.70 mm (DIN 42802 signal pin) |
| Non-plated holes | 4 × 3.2 mm at (5,5) (145,5) (5,125) (145,125), 6 mm copper keep-out; 6 × 1.50 mm (DIN retention posts) |
| Zone split | analogue x < **62** mm, digital x > **62** mm |
| Reference planes | AGND_REF left of the split and DGND right of it, on **both inner layers**; the signal layers are not poured |
| Star points | AGND_REF↔DGND at **R90 only**; HARN_SHIELD↔DGND at **R91 only** |
| Isolation keep-out | x ≥ **141.0** mm, 2.0 ≤ y ≤ 22.0 mm, no copper on **any** layer |
| IPC class | IPC-6012 class 2, IPC-A-600 class 2, IPC-A-610 class 2 |
| Electrical test | 100 % to the supplied IPC-D-356A netlist |

Parts: **211 reference designators**, 636 pads, 156 nets, thirty connectors. SMT on the top side only; all
through-hole parts on the top side. The bottom side carries copper and legend only; both inner layers are solid reference planes.

Coordinate convention: the design source uses a **top-left origin with Y down**; Gerber,
drill and CPL use a **bottom-left origin with Y up**. The conversion `y_out = 130.0 − y_design`
is applied once, in `tools/gerber.py`, and is stated in the layer-map README.

## 4. Power tree

```
18650 protected cell ─ J13 ─ VBAT ─ J12.1 (bq24074 BAT)
panel USB-C (charge only) ─ J24 ─ F1 (PTC 1.1 A) ─ D24 (TVS) ─ VBUS_CHG ─ J12.3
                                                  └ R84/R85 ─ VBUS_DET ─ J6.14 (GPIO46)
J12.7 (SYS) ─ VSYS ─ J25.1 (TPS63020 buck-boost, EN pulled up by R86 to VSYS)
J25.3 ─ V5V (5.00 V, 1 A) ─ J6.21 (DevKit 5 V in), J1.11 and J3.11 (ADS modules)
DevKit on-board LDO ─ DVDD3V3 (3.30 V) ─ all 3.3 V logic
DVDD3V3 ─ L1 (600 R ferrite) ─ VDD_ISO ─ J10.1 (isolator device side)
ADS1299 module #1 ─ AVDD = +2.50 V, AVSS = −2.50 V ─ J23 ─ carrier analogue rails
AGND_REF = analogue 0 V mid-rail
```

**AGND_REF is not ground.** With AVDD = +2.5 V and AVSS = −2.5 V it is the analogue
mid-rail and the reference every electrode, clamp and op-amp input is measured against.

Charge interlock (RFQ S-01), two independent mechanisms:
1. firmware refuses `CMD_START_SESSION` while VBUS_DET is high;
2. CHG_CE (GPIO47) holds the charger disabled for the whole of a session.
**The helmet is never worn while the charge cable is connected.**

## 5. Signal chain

**Input protection ×16** — R1–R16 (47 kΩ 0.1 % 25 ppm; ECO-EEG-024 proposes 68 kΩ so that the single-fault current of S-02 is met, and that decision belongs to the safety reviewer), D1–D16 (BAV99 clamp to
AVDD/AVSS), C1–C16 (10 nF C0G to AGND_REF). Corner 1/(2π·47k·10n) = **339 Hz**;
loss at 100 Hz **0.36 dB** (RFQ E-10 allows ±0.5 dB). Johnson noise of 47 kΩ over
0.5–70 Hz = **0.233 µV RMS**; with the ADS1299's 0.14 µV that is **0.27 µV RMS**
against the 1.0 µV limit of E-03. 4.7 nF is the approved alternate.

Assignment: 1 Fz, 2 Cz, 3 Pz, 4 C3, 5 C4, 6 T7, 7 T8, 8 F7, 9 REF_L, 10 REF_R,
11 bias (runs outward: BIASOUT → R11 → BIAS_EL), 12–14 EMG cheek/submental/laryngeal,
15–16 EOG spares. **Sixteen, not fourteen** — the two spare channels of RFQ 3.1 are
protected like every other electrode lead, which is what DSN-EEG-002 §13.4 always said.

**Envelope detectors ×3** — U1–U3, OPA4376 quad (**SOIC-14**, chosen over TSSOP because a 0.25 mm track fits between SOIC lands and does not fit between TSSOP lands), one per channel:
- input AC coupling C20/C40/C60 = **10 µF** into 10 kΩ: 1.6 Hz corner (ECO-EEG-027)
- A: precision half-wave rectifier, BAT54S with **pin 3 at the op-amp output**
- B: inverting summer → full-wave absolute value (R/2 = 4k99, R = 10 k)
- C: Sallen-Key 2nd-order low-pass, R = 22 k, C_gnd = 100 nF, C_fb = 220 nF →
  f₀ = **48.8 Hz**, Q = **0.74** (Butterworth), −3 dB at ≈50 Hz, inside E-11's ±10 %
- D: unity buffer after a 22 k / 2 k2 divider (×0.0909): a 1.1 V peak envelope becomes
  100 mV at the ADS1299 input at gain 1
Sources: channel 1 HP_TAP (J8.10) → ENV_STIM → J4.4; channel 2 VOICE_PRE → ENV_VOICE →
J4.5; channel 3 ROOM_PRE → ENV_ROOM → J4.6.

**Stimulus comparator (RFQ E-12)** — U7 TLV3201, threshold 2.5 V × 10 k / 480 k =
**52 mV**, hysteresis ≈5 mV via R82 (1 MΩ), output through R83 (10 k) and the D23 clamp
to DGND/DVDD3V3, into GPIO3. Latched in the DRDY interrupt.

**Contact lights** — eight two-lead bicolour LEDs, one per site, between LEDn and the
LED_V common. Phase A (LED_V high, Qn low) shows green; phase B (LED_V low, Qn high)
shows red; alternating at 240 Hz shows amber. LED_V is GPIO48, an input at reset, so
**nothing can light at boot whatever the shift register contains**. Dark during recording
blocks (RFQ E-27). Series resistors R70–R77 = 1 kΩ.

**Harness** — two cables, not one:
- **electrode cable**, 12-way screened → J14: E_Fz, E_Cz, E_Pz, E_C3, E_C4, E_T7, E_T8,
  E_F7, REF_L, REF_R, BIAS_EL, HARN_SHIELD
- **light cable**, 10-way → J30: LED1–LED8, LED_V, LED_GND

## 6. ESP32-S3-DevKitC-1 pin map (Rev B)

| GPIO | Net | GPIO | Net |
|---|---|---|---|
| 1 | SDA | 15 | START |
| 2 | SCL | 16 | RESET |
| 3 | ENV_CMP | 17 | I2S_MCLK |
| 4 | BTN_A | 18 | I2S_BCLK |
| 5 | BTN_B | 19 | USB D− |
| 6 | BTN_STOP | 20 | USB D+ |
| 7 | I2S_DIN | 21 | MIC_MUTE |
| 8 | I2S_LRCK | 38 | SD_CMD |
| 9 | I2S_DOUT | 39 | SD_CLK |
| 10 | CS | 40 | SD_D0 |
| 11 | MOSI | 41 | LED_SR_DATA |
| 12 | SCLK | 42 | LED_SR_CLK |
| 13 | MISO | 46 | VBUS_DET |
| 14 | DRDY | 47 | CHG_CE |
| 0 | LED_SR_LATCH (strapping, pulled up on the DevKit) | 48 | LED_PWM / LED_V |
| 43 / 44 | UART0 console | 35/36/37 | **NOT CONNECTED — octal PSRAM on N16R8** |
| 45 | **NOT CONNECTED — VDD_SPI strapping pin** | | |

microSD is **one-bit SDMMC**. 70 kB/s is needed at 1000 Hz and about 2 MB/s is
available, so the three data lines four-bit mode would have used are spent on the
contact-light shift register instead.

## 7. Engineering changes from Rev A (each is an ECO)

**This is an index, not the register. ECO-EEG-016 section 2 is the register and governs
where the two differ.**

| ECO | Finding in Rev A | Change in Rev B |
|---|---|---|
| ECO-EEG-001 | LED1–LED8 existed on the harness connector with **nothing driving them**; the 74HC595 module's outputs were not on the carrier. The contact lights could not work. | J19 widened to 1×16 exposing Q0–Q7; R70–R77 added; bicolour phase scheme defined |
| ECO-EEG-002 | **No source for DVDD3V3 at all.** The charger's SYS output, the DevKit's 5 V pin and the ADS module supplies were unconnected nets. The board could not power up. | J25 buck-boost socket, F1, D24, R84–R86, C70–C74 added; V5V rail defined |
| ECO-EEG-003 | **No charge input.** VBUS_CHG had one pad. | J24 charge-only pigtail, PTC, TVS, VBUS_DET divider |
| ECO-EEG-004 | The second amplifier of the dual OPA2376 had its inverting input unconnected and its non-inverting input tied to AGND_REF: the 50 Hz filter was not in circuit. | OPA4376 quad; all four loops closed; full-wave rectifier + Butterworth filter + buffer |
| ECO-EEG-005 | BAT54S orientation wrong — the common pin was on the rectified node instead of the op-amp output. | pin 3 to the op-amp output |
| ECO-EEG-006 | Sallen-Key with equal R and equal C gives Q = 0.5 and −3 dB at 31 Hz, outside E-11. | R = 22 k, C_gnd = 100 nF, C_fb = 220 nF → 48.8 Hz, Q = 0.74 |
| ECO-EEG-007 | **No mounting holes**, although the spec sheet promised four M3. | MH1–MH4 at (5,5), (145,5), (5,125), (145,125), 3.2 mm NPTH, 6 mm keep-out |
| ECO-EEG-008 | J6/J7 row spacing 22.0 mm. The ESP32-S3-DevKitC-1 header spacing is 22.86 mm; the DevKit would not have fitted. | 22.86 mm |
| ECO-EEG-009 | LED_SR_DATA/CLK/LATCH assigned to GPIO35/36/37, which carry the **octal PSRAM** on the -N16R8. The firmware pin map was unbuildable. | moved to GPIO41/42/0; SD dropped to one-bit; 35/36/37/45 left open |
| ECO-EEG-010 | ENV_CMP (E-12), MIC_BIAS and SPARE1/2 were dangling; the room microphone had no connector. | U7 comparator added; J28 room-mic socket added; spares protected and brought to J22 |
| ECO-EEG-011 | No analogue-ground pin on the module connectors; AVDD/AVSS of both modules hard-paralleled. | AGND_REF on J23.4 and J29.4; R92/R93 separable links |
| ECO-EEG-012 | NPTH pads declared on `*.Cu` and `*.Mask` — the six DIN retention holes would have been plated, tying the touch-proof sockets to the analogue pour. | NPTH pads carry no copper and no mask; separate NPTH drill file |
| ECO-EEG-013 | The 2×10 analogue connectors could not be escaped on two layers: the inner row had no route out. | split into a 1×10 signal socket and a 1×6 rail socket per module |
| ECO-EEG-014 | Eight digital contact-light lines ran through the electrode harness socket at x = 5 mm, so they had to cross the whole analogue zone. | harness split into a 12-way screened electrode cable (J14) and a 10-way light cable (J30) |

## 8. What is still open

| # | Item | Gate |
|---|---|---|
| 1 | **No safety engineer has reviewed this design.** | Blocks use on a person. Does not block fabrication or quoting. |
| 2 | USB VID/PID are placeholders; a pid.codes allocation is pending. | Blocks the fleet, not the prototypes |
| 3 | The firmware has never been compiled or run on hardware; five driver stubs remain. | Blocks a working prototype; TST-EEG-004 T5 is the acceptance test |
| 4 | The routing was produced by the programme's own constraint-aware autorouter. `kicad/EEG-CAR-01_RevB_DRC_report.txt` reports **VIOLATIONS: 0** — all 145 routable nets are one connected copper island, none is left without copper, and both inner planes are continuous under the analogue zone — so **the fabrication-release gate of ECO-EEG-016 §3 is met and the data is RELEASED FOR REVIEW under RFQ-EEG-002A**. It is **not released for fabrication**, because it has **not** been reviewed by a human layout engineer. The report also records **169 connections routed at relaxed geometry** (36 narrower than the 0.25 mm preferred width, 133 at full width with a reduced gap, all at or above the 0.20 mm minimum). | RFQ-EEG-002A asks for review and sign-off, not routing; a board that closes at minimum geometry is not the board that closes at preferred geometry, and that judgement is what fabrication release waits on |
| 5 | Module header geometry is not fixed; ribbon jumpers and the MP-01 plate remove the dependency, at the cost of a hand-built jumper set per unit. | Phase 2 consolidation |
| 6 | Nothing in this package has been manufactured or measured. Every figure marked *calculated* is exactly that. | Phase 1 |

## 9. Document set

The revisions below are taken from ECO-EEG-016 section 1.1, which is the controlled list.
This table is a copy for convenience; **ECO-EEG-016 governs**, and a document not on its
list is not part of the release.

| Document | What it governs |
|---|---|
| DSN-EEG-003 Rev C | manufacturing design package — architecture, carrier, precedence (**governing**) |
| RFQ-EEG-001 Rev E | requirements and acceptance (M/S/O), pricing template |
| DSN-EEG-002 Rev E | helmet, electrodes, wiring, fitting, case — **not reissued in this round**, so it still says the microphone preamplifier is on the boom, which ICD-EEG-006 corrects to MP-01 at J21 |
| SCH-EEG-005 Rev B | schematic set, 8 sheets (generated) |
| ICD-EEG-006 Rev B | interface control: every module pinout and jumper |
| PARTS-EEG-019 Rev B | part identifier register: every part number in the package |
| ASM-EEG-007 Rev B | carrier and kit assembly work instructions |
| WH-EEG-008 Rev B | harness and cable assembly |
| TST-EEG-004 Rev C | production test specification; it owns the T-numbers |
| JIG-EEG-009 Rev B | test fixture design, FIX-01 to FIX-04 |
| QP-EEG-010 Rev B | quality plan, IQC, FAI, AQL |
| RISK-EEG-011 Rev B | risk analysis and the safety-review pack |
| REG-EEG-012 Rev B | regulatory and compliance file |
| SVC-EEG-013 Rev B | service and refurbishment manual |
| IFU-EEG-014 Rev B | participant quick-start and placement guide |
| PKG-EEG-015 Rev B | packing, labelling and shipping |
| ECO-EEG-016 Rev B | change control and document register — **section 1.1 is the controlled list** |
| AVL-EEG-017 Rev B | approved vendor list |
| SIM-EEG-018 Rev A | end-to-end production simulation report (generated by `tools/simulate_production.py`; never edited by hand) |
| FW-EEG-001 Rev C | firmware build and provisioning, host tool, key fingerprint |
| MECH-EEG-020 Rev A | dimensioned drawings of every printed part (generated) |
| RUL-EEG-021 Rev A | rulings register: one answer to each cross-document disagreement, cited by section letter |

Precedence, highest first: DSN-EEG-003 Rev C → RFQ-EEG-001 Rev E → ICD-EEG-006 Rev B →
SCH-EEG-005 Rev B → DSN-EEG-002 Rev E → the BOM workbook. Where a number appears in a
document and in `tools/design.py`, **design.py governs**. Where this file disagrees with
RUL-EEG-021 Rev A, the rulings register governs.
