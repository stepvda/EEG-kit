# Rulings Register

**Document:** RUL-EEG-021  **Revision:** A  **Date:** 1 September 2026
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and `tools/design.py` disagree, `design.py` governs.

## Why this document exists

A cross-document audit on 1 September 2026 found sixty places where seventeen documents, written from one fact base, still disagreed with each other. Each disagreement needed one answer, made once, that every document could be corrected against. This is that set of answers. It began life as an internal worksheet and is registered as a controlled document because four released documents cite it.

Nothing in this package has been manufactured or measured, and no safety engineer has reviewed this design.

---


## Corrections in this issue

**This register is generated from `tools/RULINGS.md` by `tools/finalise_docs.py` job 4, and it
was regenerated on 2 September 2026.** The issue of 1 September was written before its own
worksheet was corrected, so the register had drifted from its source. Five things change, and
no ruling is reversed:

1. The **RFQ E-28**, **45 °C charge inhibit** and **maximum acoustic output** rows cite
   **RFQ-EEG-001 Rev E**, which is the revision that carries E-28, E-23 and E-29. The first
   issue said Rev D. That was current when the rulings were made and it is not current now.
2. The **Host USB connection** row no longer states that the host connector is the USB-C
   receptacle on the ADuM4160 module. It contradicted the **Isolator module USB connector**
   row immediately below it, and it contradicted `design.py` at J10.
3. The **C1–C16 dielectric** row withdraws the claim that TST-EEG-004's filter corner
   tolerance was widened to match the X7R Sallen-Key capacitors. It was not, and
   TST-EEG-004 section 16 item 16 records that it was not.
4. The **HM-08** and **HM-09** figures are the model values in `mech/MANIFEST.json`
   (6.87 cm³; 17.93 × 17.93 × 40.20 mm, 3.88 cm³) rather than the rounded
   ones of the first issue. No part has been printed, so neither set is a measurement.
5. The header above still reads **Revision A** and **1 September 2026**, because
   `tools/finalise_docs.py` writes that header as a fixed literal. The corrections listed here
   were made on **2 September 2026**, and this note is the record of that until the generator
   takes its date and revision from the worksheet.

A correction made by hand in this register and not back-ported to `tools/RULINGS.md` is
reverted, without a warning, on the next run.

## A. Geometry, from the source files

**Two things changed during layout, and both are engineering findings rather than
preferences. Every document must carry them.**

**The board grew from 130 × 124 mm to 150 × 130 mm.** Thirty connectors, 211 parts and
156 nets would not close at the smaller size. At these quantities the extra 33.8 cm² of bare
board costs a few euro per unit against a real risk of an unroutable design.

**The board went from two layers to four.** Package v1's architecture argument was that a
two-layer carrier is cheap and easy to route. Actually laying it out showed that it is not:
on two layers the bottom side has to be both the reference plane and the second routing
surface, and it cannot be both. Four layers — L1 signal, L2 reference plane, L3 reference
plane, L4 signal — gives two full routing surfaces AND a continuous reference under every
analogue trace, which is exactly what DSN-EEG-002 section 13's "layout rules that are
requirements, not preferences" asks for and which a swiss-cheesed two-layer pour cannot
deliver. At 2 units a four-layer board is about €35 more in total; at 50 units it is about
€3 per board. That is the right trade for a sixteen-channel EEG front end, and it is the
single most important thing package v2 learned by doing the work instead of asserting it.

The enclosure grew with the board.

| Item | Ruling | Source |
|---|---|---|
| Carrier outline | **150.0 × 130.0 mm** | `design.py` |
| Layer count | **four**: L1 signal, L2 reference plane, L3 reference plane, L4 signal | `router.py` |
| Stack-up | mask / 35 µm L1 / prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask = **1.60 mm ± 10 %** | `design.py` NOTES |
| Reference planes | AGND_REF left of x = 62 mm and DGND right of it, **on both L2 and L3**, tied together by stitching vias | `build_board.py` |
| Vias | **through vias only**, no blind, buried, back-drilled, filled or plugged | ruling |
| Zone split | **x = 62 mm**: analogue left, digital right | `design.py` |
| Mounting holes | **M3, 3.2 mm NPTH at (5,5), (145,5), (5,125), (145,125)**, 6 mm copper keep-out | `design.py` |
| Isolation keep-out | **x ≥ 141 mm, y = 2 to 22 mm**, no copper on any of the four layers | `design.py` |
| Vias | **0.60 mm pad / 0.30 mm finished hole**, 0.15 mm annular ring, tented | `design.py` |
| Minimum track / clearance | **0.20 mm / 0.20 mm**; electrode nets keep **0.35 mm** to everything else | `drc.py` |
| MP-01 module plate | **146.0 × 126.0 × 3.0 mm**, 8 mm solid border, 12 × 3 mm jumper slots on a 16 × 7 mm grid, Ø2.7 mm M2.5 fixing holes between the slot rows, one 31 × 61 mm opening over the DevKit | `mech_gen.py` |
| Carrier-to-plate standoff | **M3 × 18 mm nylon hex, female–female, four off, with eight M3 × 6 nylon pan screws** | ruling |
| POD-P1 base | **163.0 × 143.0 × 58.0 mm external; 158.0 × 138.0 × 55.5 mm internal**; 2.5 mm walls; 1.6 × 1.2 mm gasket groove | `mech_gen.py` |
| POD-P1 lid | **163.0 × 143.0 × 6.0 mm**, with a 2.0 mm spigot | `mech_gen.py` |
| Stack budget | floor 2.5 + boss 6.0 + carrier 1.6 + standoff 18.0 + plate 3.0 + modules ≤ 18.0 = **49.1 mm** against 55.5 mm internal. **Margin 6.4 mm.** | ruling |
| HM-04 | 12.4 × 12.4 × 18.0 mm, 1.9 cm³ | `mech_gen.py` |
| HM-08 battery hatch | 48.0 × 36.0 × 6.5 mm, 6.87 cm³ | `mech_gen.py` |
| HM-09 service key | 17.93 × 17.93 × 40.20 mm, 3.88 cm³ | `mech_gen.py` |
| FIT-01 coupon | 60.0 × 24.0 × 10.0 mm, bores 9.20 / 9.35 / 9.15 mm | `mech_gen.py` |

**RISK-EEG-011 SR-08 is closed by the standoff ruling.** The slant path from carrier copper,
over the edge of the isolation keep-out and up the 18 mm standoff to any host-side conductor
on MP-01 is ≥ 18 mm, which is more than twice the 8 mm the safety case asks for.

## B. The instrument

| Question | Ruling |
|---|---|
| **Where is the microphone preamplifier?** | **On the MP-01 module plate, connected at J21.** The boom carries the bare electret capsule and its screen, on the pigtail at J18. `design.py` governs: J21 is a carrier socket. DESIGN_FACTS §2, RFQ §2, RFQ E-14 and DSN-EEG-003 §2 all said "on the boom" and are corrected. WH-EEG-008's "on the carrier" is corrected to "on MP-01". |
| **Which preamplifier?** | **Not settled, and it must be stated as not settled.** The MAX9814 has automatic gain control, which RFQ E-14 forbids ("AGC off"); disabling it is a module-dependent modification. The preferred route is a fixed-gain part (MAX4466 class). Until a part is bought and measured, the module is specified **by interface** in ICD-EEG-006 and the MAX9814 is named only as the package-v1 candidate. AVL-EEG-017 keeps it "not approved". |
| **Contact-light drive** | **1 kΩ series, Vf 2.0 V, (3.3 − 2.0)/1000 = 1.3 mA per site, 10.4 mA total from GPIO48.** Every document uses these figures. DSN-EEG-003 §10 finding 3's "1.6 mA / 13 mA" is corrected. |
| **Light phase rate** | **240 Hz** (`LIGHT_PHASE_HZ` in `board_pins.h`). "Above 100 Hz" is the requirement; 240 Hz is the fitted value. |
| **Contact-light driver status** | **Not implemented.** `lights_write()` and `lights_task()` are on/off only. The bicolour phase scheme is specified and not yet coded. TST T11 cannot pass until it is. Say so in FW-EEG-001, TST-EEG-004 and DSN-EEG-003 §11. |
| **Envelope filter group delay** | **4.40 ms at DC** = 1/(Q·2π·f₀) with f₀ = 48.77 Hz and Q = 0.7416. TST-EEG-004's 4.61 ms uses √2/(2πf₀), which is only correct at Q = 0.7071. JIG-EEG-009 is right. |
| **Sample-stream bandwidth** | **50.7 kB/s of frame payload at 1000 Hz** (1015 bytes every 20 ms). RFQ E-20's "≈70 kB/s" and F-12's "≈64 kB/s" are allowances that include STATUS and SIGNATURE frames and filesystem overhead. State the 50.7 figure with that explanation; do not change the requirement. |
| **T7 10 µV point** | A **linearity check with a ±5 % limit**. The 0.5 % gain limit of E-04 applies at the 100 µV and 1 mV points. The measurement uncertainty at 10 µV is **0.22 % (k = 2)**; JIG-EEG-009's derivation governs and QP-EEG-010's "1σ" label is corrected. |
| **Patient terminations** | **Fourteen**: eight scalp, two ear references, one bias, three EMG. The two EOG spares are not fitted in a standard build. |
| **Connectors on the carrier** | **Thirty**, J1 to J30. Seventeen are module connectors. |
| **Purchased modules** | **Twelve module types; thirteen module assemblies per unit** (the ADS1299 breakout is fitted twice). Twelve assemblies mount on MP-01; the ESP32-S3-DevKitC-1 is inserted directly into J6 and J7. |
| **D1–D16** | **BAV99**, not BAT54S. Schottky leakage across a 47 kΩ series resistor is an offset error on a 10 µV input. BAT54S is used only at D20, D40, D60 (the envelope rectifiers). TST T1 is corrected. |
| **Phase 3 quantity** | **10 to 40 further kits, 25 to 50 in total.** |
| **IPC classes** | **IPC-6012 class 2** (fabrication), **IPC-A-600 class 2** (bare-board acceptance), **IPC-A-610 class 2** (assembly). All three, everywhere. |
| **ECO numbering** | The change register is the document **ECO-EEG-016**. The individual changes are **ECO-EEG-001 … ECO-EEG-015, ECO-EEG-017 and ECO-EEG-018**, and ECO-EEG-016 has since issued **ECO-EEG-019 … ECO-EEG-027** for the changes settled after this register was first written. **ECO-EEG-028 and ECO-EEG-029 are withdrawn**; their two findings belong to ECO-EEG-018. ECO-EEG-016 §2 is the authority for all of them. The routing-scope change, previously numbered ECO-EEG-016, becomes **ECO-EEG-018**, so no ECO shares a number with the document. |
| **RFQ E-28** | Corrected in Rev E: **TP1–TP18 plus a 1×6 UART debug header at J26**. The 2×5 1.27 mm JTAG/SWD header of Rev C is **withdrawn** — the ESP32-S3 is programmed over UART0 and its native USB and no JTAG connector is fitted. J26 way 6 is **NC_GPIO0**, a spare way, because GPIO0 is committed to LED_SR_LATCH (ECO-EEG-009). Every "E-28 deviation" note is deleted. |
| **45 °C charge inhibit** | It is **RFQ E-23**, restored in Rev E: "Charger IC with thermal regulation; no charging above 45 °C." Cite E-23, not S-04, for the temperature and S-04 for the thermistor. |
| **Thermistor** | **Not met, and it stays not met.** There is no NTC net in `design.py` and no thermistor way on J12 or J13. It is an open hardware item against S-04, listed in DSN-EEG-003 §11 and RISK-EEG-011. Do not describe it as met anywhere. |
| **Per-unit isolation test** | **A 500 V DC insulation-resistance measurement across the barrier, not a hipot.** The 2.5 kV RMS type test is the module supplier's certificate, checked once at incoming inspection. JIG-EEG-009's per-unit 2500 V AC station is deleted. |
| **Fixture naming** | **FIX-01 to FIX-04**, with sub-assemblies FIX-01/A, FIX-01/B and so on. TST-EEG-004's "Part A…G" naming is replaced by FIX references. |
| **T11 method** | **A TCS34725-class colorimeter head, FIX-01/E, reading the R/G ratio at each site.** JIG-EEG-009 adds it to the FIX-01 BOM; the LED current-sense idea is dropped. |
| **End-of-line flashing** | Through the **DevKitC-1's own UART USB-C port**, which carries the auto-reset circuit (DTR and RTS to EN and IO0) on the DevKit itself. The carrier's J26 is console and recovery only and **cannot** enter download mode, because GPIO0 is LED_SR_LATCH. The module is reachable through the MP-01 opening. |
| **Jumper keying** | **Decided.** Module end: a 2.54 mm shrouded polarised IDC header where the module has one, otherwise pin 1 marked and the jumper labelled. Carrier end: the printed keying shroud **WH-KEY-01**, part of the MP-01 print set, over every socket that takes a jumper. ICD-EEG-006 section 6 lists which. |
| **Host USB connection** | **A socket, not a captive cable.** The host connector is on the ADuM4160 isolator module and is presented through a gasketed aperture in POD-P1. WH-08 and the cable gland are deleted from the Phase 1 build; the captive lead through a gland is a **Phase 2** item for the helmet shell. The kit ships the two cables of A-07 and one of them is the host lead. **What the participant plugs into is a USB-C panel receptacle on WH-ADP-04, and on the only named candidate module it is reached through the WH-09 pigtail, because the module itself presents USB-B.** *The first issue of this register said the host connector was "the USB-C receptacle on the ADuM4160 module". That is **withdrawn**: it contradicted the very next row of this table and it contradicts `design.py`, which records at J10 that "the module's host receptacle is USB-B on the qualified part, not USB-C; WH-09 adapts it". No module with a USB-C host receptacle has been qualified, so USB-C at the module is a requirement, not a fact.* |
| **Isolator module USB connector** | The named candidate presents USB-B, and E-24 asks for USB-C. **The resolution is a short USB-B-to-USB-C panel pigtail (WH-09) until an isolator module with a USB-C host connector is qualified.** State it as a live non-conformance with that interim answer, not as settled. |
| **C1–C16 dielectric** | **C0G is the requirement and the part number in `design.py` is wrong.** `GCM188R71H103KA37D` is an X7R part. The correct C0G part is **`GCM1885C1H103JA16D`** (10 nF, C0G, 50 V, 0603) and the 100 nF Sallen-Key capacitors C21/C41/C61 become **`GCM188R71H104KA57D` X7R is also wrong**: a 100 nF C0G in 0603/50 V is not a stocked part, so C21/C41/C61 are specified as **X7R with a stated 15 % capacitance tolerance over temperature**. *The first issue of this ruling added "and the filter corner tolerance in TST-EEG-004 widens to match". That sentence is **withdrawn, because it was never true**: TST-EEG-004 had no f₀ limit to widen, and none was written. TST-EEG-004 section 16 item 16 says so in those terms.* What that document does instead is **T12e, which measures and records f₀ per unit against 42 to 58 Hz**, the band the fitted parts can hold. ±15 % over temperature moves f₀ between 42.4 and 57.4 Hz, which does not fit inside the 45 to 55 Hz of RFQ E-11 wherever the centre sits, so **the 50 Hz ±10 % half of E-11 is not met with the approved parts** and must be stated as not met. Either E-11 is restated to 42 to 58 Hz or a stocked C0G part is qualified; neither has been done. Record both part-number changes as ECO-EEG-019 in ECO-EEG-016. |
| **Headphones** | **A-04 is restated as 32 to 64 Ω** and the calibrated output level is measured per model. The ATH-M20x is 47 Ω, and the test load becomes **47.0 Ω** to match the shipped part. TST T17 and JIG-EEG-009 are corrected. |
| **J15–J17 part** | **Open, and named as open.** `design.py` names Stäubli SLB1,5-F as a class, not a confirmed PCB part. A touch-proof 1.5 mm socket with a PCB-mount signal pin and two 1.5 mm retention posts must be sourced and first-articled before Phase 2; AVL-EEG-017 carries a 12-week lead-time risk against it. |
| **Serial number** | Format **`TIOV-B-nnnn`**: programme prefix, hardware revision letter, four digits. Phase 1 uses 0001–0009, Phase 2 0010–0099, Phase 3 0100–0999. It appears identically in the label text, the Data Matrix, the USB `iSerialNumber`, the calibration record and the packing list. |
| **Public-key fingerprint** | The **first 8 bytes of SHA-256 over the 64-byte uncompressed public key, printed as 16 uppercase hex characters in four groups of four**. Defined once, in FW-EEG-001 section 7; everyone else cites it. |
| **Fiducials** | **Three 1.0 mm round fiducials with 3.0 mm mask openings are added to the carrier** at **(12, 10), (144, 100) and (12, 120)**, as generated by `tools/design.py` and listed in `kicad/EEG-CAR-01_RevB_CPL_SMT_top.csv`. *The (8, 8), (142, 8) and (8, 122) of this register's first issue were a transcription error and are withdrawn.* The vision-teach workaround is withdrawn. Record as ECO-EEG-020. |
| **Conformal coating** | **Not coated for Phases 1 and 2.** The decision is taken, not deferred: the board lives inside a gasketed enclosure, and coating a board with 30 connectors and a socketed DevKit costs more in masking than it buys. Revisited before Phase 3 if a unit returns with corrosion. |
| **eFuses on Phase 1 prototypes** | **Not burned.** Secure boot and flash encryption are enabled from Phase 2. The two prototypes run unsigned images so the firmware volunteer can iterate. TST T25 is marked "Phase 2 onward" and is not a Phase 1 gate. |
| **Charger and gauge** | **One combined charger-plus-gauge assembly on a single J12 jumper is the baseline.** If two separate breakouts are supplied, the gauge mounts on MP-01 and its VBAT and I²C taps are made at the MP-01 end of the J12 jumper — a Y jumper, drawn in ICD-EEG-006 section 3.3, not a hand-built variation. |
| **I²C pull-ups** | **Two 4.7 kΩ resistors, R94 and R95, are added to the carrier** on SDA and SCL to DVDD3V3. Depending on whatever the modules happen to carry is not a design. Record as ECO-EEG-021. |
| **VBUS_DET level** | **R85 changes from 56 kΩ to 150 kΩ**, giving 5 × 150/250 = 3.0 V, above the 2.48 V V_IH of a 3.3 V ESP32-S3 input. The 1.79 V of Rev B would not reliably assert the first of the two S-01 interlocks. Record as ECO-EEG-022. |
| **ENV_CMP level** | **U7 is powered from DVDD3V3 and DGND rather than AVDD and AVSS**, so its output swings 0 to 3.3 V into GPIO3 with full margin, and the D23 clamp becomes a belt-and-braces part rather than the only thing between ±2.5 V and a 3.3 V pin. Its inputs stay analogue-referenced; the TLV3201 has a rail-to-rail input stage that reaches its negative rail, and AGND_REF sits 2.5 V above DGND, so **the comparator inputs are re-referenced to a DVDD3V3/2 divider and the envelope is AC-coupled into it.** Record as ECO-EEG-023 and state plainly that this is a change the safety and layout reviewer must check. |
| **DevKit 3V3 rail** | The carrier draws a **calculated 288 mA worst case** from the DevKit's on-board regulator. That is inside its rating but dissipates about 0.5 W inside a closed pod. **Phase 1 measures it (TST T3) and reports the case temperature; if it exceeds 85 °C, a 3.3 V regulator on the carrier fed from V5V is an ECO against Rev C.** Do not present it as solved. |
| **Buttons** | RFQ E-26 is restated: **a 6 mm tactile switch with a 12 mm coloured cap on an extender**. The panel openings are **13.0 mm** on a **14 mm pitch** at y = 76, 90 and 104 mm on the POD-P1 right wall. The Rev C "≥ 12 mm actuator" wording described the cap, not the switch. |
| **Calibration certificate** | Travels in the **case lid pocket** beside the quick-start card. PKG-EEG-015's foam schedule is corrected to put it there. |
| **A-03 headband** | **Withdrawn as a kit item.** The eight electrodes are fixed to the HM-01 frame at manufacture; a headband with fixed holders at the same eight sites would duplicate them. What the kit needs and does not have is the **chin strap (HM-06) and the occipital yoke (HM-03)**, both of which are on the frame. RFQ A-03 is rewritten to cover those, the packing list drops the headband line, and SVC-EEG-013 drops its wash schedule. |
| **M-02 LED opening** | **Withdrawn.** All eight lights are in the helmet. The pod carries no indicator; its state is read from the session runner. M-02 is corrected. |
| **EOG panel sockets** | **Not fitted in a standard build.** J22 exists on the carrier and the two channels are protected; the panel sockets, their cable and their drawing are a **Phase 2 option** and are listed as such in PARTS-EEG-019 with no part number yet. |
| **Maximum acoustic output** | **A new requirement, E-29:** the headphone output must not exceed **100 dB SPL** at any commanded level, measured on an artificial ear, and the firmware must clamp the codec volume register to the value measured at calibration. Calculated full-scale output is about 110 dB SPL, which is why the requirement is needed. Add to RFQ Rev E, TST-EEG-004 as a type test, and RISK-EEG-011. |
| **S-02 single-fault DC** | **Calculated at 53.2 µA against a 50 µA limit — it fails.** The fix is to raise the series resistors from 47 kΩ to 68 kΩ, which gives 2.5 V / 68 kΩ = 36.8 µA, keeps the corner at 234 Hz (−0.75 dB at 100 Hz, so **E-10 must widen to ±1.0 dB**) and raises Johnson noise to 0.28 µV (total 0.31 µV, still well inside E-03). **Record as ECO-EEG-024 and carry it as a Phase 1 decision for the safety reviewer, with 47 kΩ fitted on the prototypes and the measurement made before Phase 2.** Do not claim S-02 is met. |
| **F-06 ring buffer** | 12 MB of the 8 MB PSRAM is impossible. **The ring is 6 MiB (6,291,456 bytes), which is 126 seconds of raw samples at 1000 Hz -- 124 seconds if counted over the framed stream -- not the three minutes of F-06.** *The 118 seconds of this register's first issue divided 6 MB decimal by the framed rate; the ring is 6 MiB and it stores raw samples. The depth is arithmetic, not a design change: RING_BYTES stays 6 MiB and F-06 stays relaxed to 90 s, so this is a correction recorded under ECO-EEG-025, not a new ECO.* Either F-06 relaxes to 90 seconds or the microSD backfill covers the gap. **Ruling: F-06 is relaxed to 90 seconds of ring plus unlimited backfill from the microSD copy**, and the reason is stated. Record as ECO-EEG-025. |
| **E-04 crosstalk** | **−100 dB is not achievable through a 60 mm un-interleaved ribbon and is 40 dB below this instrument's noise floor, so it is not measurable either.** E-04 is restated as **−80 dB at 50 Hz, measured on the carrier**, with the ribbon contribution characterised once on the first prototype. Record as ECO-EEG-026. |
| **E-11 AC-coupling corner** | The fitted 1 µF into 10 kΩ gives **15.9 Hz, not the 0.1 Hz of E-11**. For an envelope of a speech signal that is the wrong corner: it removes the envelope itself. **C20/C40/C60 change to 10 µF and R20/R40/R60 stay 10 kΩ, giving 1.6 Hz**, and E-11 is restated as **≤ 2 Hz**. Record as ECO-EEG-027. |

## C. Structural rulings

1. **One table, one home.** The board specification lives in DSN-EEG-003 §3.2. The
   module-to-connector table lives in ICD-EEG-006 §1. The GPIO map lives in ICD-EEG-006 §5.
   The ECO register lives in ECO-EEG-016 §2. The 47 kΩ noise-and-flatness arithmetic lives in
   RISK-EEG-011 §4. The isolation keep-out and the star-point rule live in DSN-EEG-003 §3.3.
   The lithium-shipping procedure lives in PKG-EEG-015 §7 and REG-EEG-012 §3 states only the
   obligation. Everyone else **cites**, and does not restate.

2. **TST-EEG-004 Rev C owns the step numbers.** Every other document cites T-numbers from it
   and never invents one. If a document needs a step that does not exist, it says so and
   raises it as an open item rather than numbering it itself.

3. **The "nothing has been built" paragraph stays in every document.** That repetition is
   deliberate.

4. **Where a requirement is not met, say so in the same sentence as the requirement.** Do not
   put "met" in a compliance table and the exception three sections later.
