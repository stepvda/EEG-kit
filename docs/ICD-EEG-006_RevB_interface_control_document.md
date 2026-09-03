# INTERFACE CONTROL DOCUMENT -- CARRIER TO MODULES

**Document:** ICD-EEG-006  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs.

**Revision note.** Rev B carries the two geometry findings of the layout work -- the carrier
is 150.0 x 130.0 mm and it is a four-layer board -- regenerates the connector register from
`tools/design.py` at the new coordinates, resizes MP-01 and POD-P1 to match, and closes the
Rev A open points on keying, I2C pull-ups, VBUS_DET, ENV_CMP, E-04, E-11 and E-28 against the
package v2 rulings.

**The findings of the second cross-document audit are closed in this issue**, within the same
revision letter and without a further letter change: the module count is stated
unconditionally, the MP-01 geometry is restated from `tools/mech_gen.py`, RFQ E-23's 45 C
charge inhibit is stated as not met, and the rail budgets of sections 2.7 and 5.3 are
reconciled with each other and read against TST-EEG-004 T3. The rulings those corrections
apply are RUL-EEG-021 Rev A, which is now a controlled document in `docs/`.

**Corrections within Rev B, after the design and firmware changes of 2026-09-02**, made in
place with their date and without a further revision letter: **ECO-EEG-024 is applied**, so
the series protection resistance a module must tolerate is **68 kOhm**, not 47 kOhm, and RFQ
S-02's single-fault DC limit is **met at 36.8 uA** -- section 2.1's acceptance row, section
2.1's protection-network paragraph, the section 8 incoming-module step 8 and open item 6 are
restated for it, and E-10 now sits on the +/-1.0 dB branch its own wording provides. **The
contact-light bicolour phase driver is written**, so section 2.11 and open item 11 no longer
say the interface has nothing driving it. The interface itself did not change in either case,
and neither change has been measured on hardware: no unit exists.

## Why this document exists

EEG-CAR-01 Rev B is a carrier, not an instrument. Twelve purchased module types do the work,
and no public standard fixes where any of them puts its header. Rev A.2 drew sockets at
guessed coordinates and would have discovered the guess when the boards arrived. Package v2
removes the dependency: every module except the ESP32-S3-DevKitC-1 sits on the printed module
plate MP-01 above the carrier and is joined to it by a made-up 2.54 mm ribbon jumper, so the
carrier sockets are placed for routing and the jumper absorbs whatever geometry the module
turns out to have. That only works if somebody writes down, way by way, what each socket
carries and what each module must present. This document is that. It is the reference against
which TST-EEG-004 step T2 checks continuity, the source from which the module symbols of the
schematic set SCH-EEG-005 are generated, and the form a builder fills in before accepting a
substitute part.

There is no separate KiCad symbol library for this board. Rev A said the symbols were
generated into `kicad/EEG-CAR-01.kicad_sym`; that file does not exist and never did. The
symbols are generated from `tools/design.py` straight into the eight sheets of SCH-EEG-005.

**Nothing in this package has been built or measured, and no safety engineer has reviewed
this design.** Every derived figure is labelled *calculated* and the first article is where
the calculations stop being calculations.

---

## 1. The carrier connector register

The carrier is **150.0 x 130.0 mm** and has **four layers**: L1 signal, L2 reference plane,
L3 reference plane, L4 signal. Package v1 asserted that two layers would be enough for this
board. Doing the layout showed that they are not: on two layers the bottom side has to be
both the reference plane and the second routing surface, and it cannot be both. Four layers
give two whole routing surfaces and a continuous reference under every analogue trace, which
is what the layout rules of **DSN-EEG-002 section 13** -- the rules that are requirements and
not preferences -- ask for, and a swiss-cheesed two-layer pour cannot deliver it. The zoning,
the star point and the isolation keep-out are **DSN-EEG-003 section 3.3**. The reference
planes are AGND_REF left of x = 62 mm and DGND right of it, on **both** inner layers, tied
together by stitching vias, so every analogue trace on L1 or L4 has continuous reference
copper under it and both routing surfaces stay whole. Vias are **through vias only**,
0.60 mm pad on a 0.30 mm finished hole, no blind, buried, back-drilled, filled or plugged.
The stack is mask / 35 um L1 / prepreg 0.200 / 17 um L2 / core 1.065 / 17 um L3 /
prepreg 0.200 / 35 um L4 / mask = **1.60 mm +/- 10 %**. The full board specification is
DSN-EEG-003 section 3.2 and is not restated here.

**The routed result against this connector set.**
`kicad/EEG-CAR-01_RevB_DRC_report.txt` is the authority for it and every figure below is read
from that report. EEG-CAR-01 Rev B is routed on four layers with **3 745 track segments and
552 through vias**. **All 145 nets are fully connected** -- none unclosed, none without copper
-- and each reference plane is one continuous island per net on both inner layers. Every
geometric rule passes: the smallest measured clearance is 0.260 mm on F.Cu, 0.275 mm on B.Cu
and 0.285 mm on the planes against a 0.20 mm rule; the narrowest conductor is 0.200 mm; the
smallest plated hole is 0.300 mm; copper stands 2.00 mm clear of every non-plated hole; no
digital net enters the analogue zone; there are no duplicate segments and no duplicate via
positions; and there is exactly one AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND
bridge. The report records **no violation of any kind** -- its own line is "VIOLATIONS: 0 --
none.  The board passes every rule listed above" -- so **the isolation strip of DSN-EEG-003
section 3.3 is free of copper on all four layers**, the two inner planes included. That is
written here because the report says it, not because it was intended.

**The board closes, and it closes at minimum geometry.** The same report lists **169
connections the router had to relax**: 36 took a conductor narrower than the 0.25 mm preferred
width, and 133 kept full width and took a reduced gap instead. All 169 are at or above the
0.20 mm minimum conductor and the 0.20 mm minimum gap, so all 169 pass; a board that closes at
the minimum is still not the same board as one that closes with margin everywhere, and the
relaxed connections are listed pad by pad so a reviewer can see where.

**The fabrication data is RELEASED FOR REVIEW under RFQ-EEG-002A, not for fabrication.** The
release gate of ECO-EEG-016 section 3 -- zero DRC violations, every net one connected copper
island, both inner planes continuous under the analogue zone -- is met on all three counts.
What has not happened is a human layout review: this routing came from the programme's own
tools and no layout engineer has looked at it. That review is the scope of RFQ-EEG-002A, and
fabrication release waits on it.

**Modules to connectors.** This table is the one home of the module-to-connector mapping;
DESIGN_FACTS, RFQ-EEG-001 and DSN-EEG-003 cite it rather than repeating it.

| Block | Module type | Carrier connectors |
|---|---|---|
| Analogue front end x2 | ADS1299 eight-channel breakout (PIEEG-8 class) | #1: J1, J2, J23. #2: J3, J4, J29. Daisy stub J5 |
| Controller | ESP32-S3-DevKitC-1-N16R8 | J6, J7 (direct insertion, 22.86 mm apart) |
| Audio codec | ES8388-class codec with headphone amplifier | J8, J9 |
| USB isolation | ADuM4160 module, host receptacle on the module | J10 |
| Secure element | ATECC608B breakout | J11 |
| Charger | bq24074-class charger with power path | J12 (with the gauge), J13 cell, J24 charge input |
| Fuel gauge | MAX17048-class gauge | J12 (with the charger) |
| Rail | TPS63020-class buck-boost | J25 |
| Storage | microSD breakout, one-bit SDMMC | J20 |
| Boom microphone preamplifier | fixed-gain electret preamplifier, see 2.9 | J21, with the boom pigtail at J18 |
| Room microphone | MEMS or electret module with hardware mute | J28 |
| Contact lights | 74HC595 shift-register module | J19, with the light harness at J30 |

**Twelve module types and thirteen module assemblies per unit, unconditionally.** The
thirteenth assembly is the second ADS1299 breakout: the type is specified once and fitted
twice. The charger and the gauge are two of the twelve types and count as two assemblies
whichever way they are supplied -- the baseline combined charger-plus-gauge board of section
2.6 carries both of them on one J12 jumper, and two separate breakouts carry one each on the Y
jumper of section 3.3 -- so neither arrangement changes either count. Twelve of the thirteen
assemblies mount on MP-01; the thirteenth is the ESP32-S3-DevKitC-1, which is inserted
directly into J6 and J7. This is the count of RUL-EEG-021 section B and it is the count used
in RFQ-EEG-001, DSN-EEG-003, TST-EEG-004, ASM-EEG-007, AVL-EEG-017, QP-EEG-010, PKG-EEG-015,
SVC-EEG-013 and REG-EEG-012.

Coordinates below are the design-source convention: origin at the top-left board corner, X
right, Y down, from `tools/design.py`. Pin 1 of every socket strip is the square pad and is
marked on the top silkscreen. Way counts are the carrier socket way counts. The **Shroud**
column says whether the socket carries a WH-KEY-01 printed keying shroud (section 6.1).

| Ref | Footprint | Ways | Position (mm) | Zone | Class | Shroud | What connects |
|---|---|---|---|---|---|---|---|
| J1 | PinSocket_1x12_P2.54mm_Vertical | 12 | 66.0, 6.0 | D | module | yes | ADS1299 module #1, digital |
| J2 | PinSocket_1x10_P2.54mm_Vertical | 10 | 41.0, 5.0 | A | module | yes | ADS1299 module #1, analogue signals |
| J23 | PinSocket_1x06_P2.54mm_Vertical | 6 | 47.0, 5.0 | A | module | yes | ADS1299 module #1, analogue rails |
| J3 | PinSocket_1x12_P2.54mm_Vertical | 12 | 66.0, 42.0 | D | module | yes | ADS1299 module #2, digital |
| J4 | PinSocket_1x10_P2.54mm_Vertical | 10 | 41.0, 36.0 | A | module | yes | ADS1299 module #2, analogue signals |
| J29 | PinSocket_1x06_P2.54mm_Vertical | 6 | 47.0, 24.0 | A | module | yes | ADS1299 module #2, analogue rails |
| J5 | PinSocket_1x04_P2.54mm_Vertical | 4 | 72.0, 6.0 | D | module | yes | ADS1299 module #1 DAISY_IN / CLKOUT stub |
| J6 | PinSocket_1x22_P2.54mm_Vertical | 22 | 82.0, 8.0 | D | **direct** | no | ESP32-S3-DevKitC-1 row A |
| J7 | PinSocket_1x22_P2.54mm_Vertical | 22 | 104.86, 8.0 | D | **direct** | no | ESP32-S3-DevKitC-1 row B |
| J8 | PinSocket_1x14_P2.54mm_Vertical | 14 | 90.0, 72.0 | D | module | yes | audio codec module |
| J9 | PinSocket_1x04_P2.54mm_Vertical | 4 | 66.0, 78.0 | D | module | yes | codec microphone feeds |
| J10 | PinSocket_1x04_P2.54mm_Vertical | 4 | 136.0, 6.0 | D | module | yes | USB isolator, device side |
| J11 | PinSocket_1x04_P2.54mm_Vertical | 4 | 136.0, 20.0 | D | module | yes | secure element breakout |
| J12 | PinSocket_1x08_P2.54mm_Vertical | 8 | 136.0, 34.0 | D | module | yes | charger and fuel gauge |
| J13 | JST_PH_B2B-PH-K_1x02_P2.00mm | 2 | 136.0, 60.0 | D | cell | no, JST keyed | protected 18650 carrier |
| J14 | PinSocket_1x12_P2.54mm_Vertical | 12 | 5.0, 12.0 | A | harness | yes, WH-EEG-008 | electrode cable, 12-way screened |
| J15 | DIN42802_1p5mm_Socket | 1 | 8.0, 76.0 | A | panel | no, touch-proof | EMG1 cheek |
| J16 | DIN42802_1p5mm_Socket | 1 | 8.0, 88.0 | A | panel | no, touch-proof | EMG2 submental |
| J17 | DIN42802_1p5mm_Socket | 1 | 8.0, 100.0 | A | panel | no, touch-proof | EMG3 laryngeal |
| J18 | PinSocket_1x04_P2.54mm_Vertical | 4 | 122.0, 90.0 | D | panel | no, marked only | boom microphone TRRS pigtail |
| J19 | PinSocket_1x16_P2.54mm_Vertical | 16 | 78.0, 72.0 | D | module | yes | 74HC595 contact-light driver |
| J20 | PinSocket_1x08_P2.54mm_Vertical | 8 | 136.0, 72.0 | D | module | yes | microSD breakout, one-bit SDMMC |
| J21 | PinSocket_1x06_P2.54mm_Vertical | 6 | 122.0, 72.0 | D | module | yes | boom microphone preamplifier |
| J22 | PinSocket_1x03_P2.54mm_Vertical | 3 | 30.0, 116.0 (90 deg) | A | panel | yes, WH-EEG-008 | EOG / spare electrode header, Phase 2 option |
| J24 | JST_PH_B2B-PH-K_1x02_P2.00mm | 2 | 143.0, 80.0 | D | panel | no, JST keyed | charge-only USB-C pigtail |
| J25 | PinSocket_1x06_P2.54mm_Vertical | 6 | 128.0, 86.0 | D | module | yes | buck-boost module |
| J26 | PinSocket_1x06_P2.54mm_Vertical | 6 | 128.0, 104.0 | D | debug | no, marked only | console and recovery header |
| J27 | PinSocket_1x04_P2.54mm_Vertical | 4 | 128.0, 72.0 | D | panel | no, marked only | 3.5 mm headphone jack pigtail |
| J28 | PinSocket_1x04_P2.54mm_Vertical | 4 | 122.0, 102.0 | D | module | yes | room microphone module |
| J30 | PinSocket_1x10_P2.54mm_Vertical | 10 | 66.0, 90.0 | D | harness | yes, WH-EEG-008 | contact-light cable, 10-way |

**Thirty connectors, J1 to J30.** Seventeen are module connectors and carry the jumper set of
section 3. Two (J6, J7) take the DevKit directly. The remaining eleven are harness, panel,
cell and debug, and their cables are specified in WH-EEG-008, not here.

**J15, J16 and J17 have no confirmed part.** `design.py` names Staubli SLB1,5-F / LB-I1,5,
which is a class of touch-proof 1.5 mm socket rather than a qualified PCB part. A touch-proof
1.5 mm socket with a PCB-mount signal pin and two 1.5 mm retention posts must be sourced and
first-articled before Phase 2; AVL-EEG-017 carries a 12-week lead-time risk against it. These
are Class A patient-contact parts on every unit, so this is an open item, not a detail.

**J22 is not fitted to a panel socket in a standard build.** The socket exists on the carrier
and both spare channels are protected like every other electrode lead, but the panel DIN
sockets, their cable and their drawing are a Phase 2 option and carry no part number
(PARTS-EEG-019).

### 1.1 Pin assignments, module connectors

Every row below is taken from a `conn()` call in `tools/design.py`. Direction is stated from
the carrier's point of view. `NC_*` names are deliberate no-connects: the way exists so that a
module which needs the pin can be jumpered without a board change, and it is a single-pad net
on the carrier by design.

**J1 -- ADS1299 module #1, digital (12)**

| Way | Net | Dir | Domain | Module pin |
|---|---|---|---|---|
| 1 | DVDD3V3 | out | 3.3 V | DVDD |
| 2 | DGND | -- | 0 V | DGND |
| 3 | SCLK | out | 3.3 V CMOS | SCLK |
| 4 | MOSI | out | 3.3 V CMOS | DIN |
| 5 | MISO | in | 3.3 V CMOS | DOUT |
| 6 | DRDY | in | 3.3 V CMOS | DRDY |
| 7 | CS | out | 3.3 V CMOS | CS |
| 8 | START | out | 3.3 V CMOS | START |
| 9 | RESET | out | 3.3 V CMOS | RESET |
| 10 | CLK_ADS | **in** | 3.3 V CMOS | CLK (module #1 sources the 2.048 MHz clock) |
| 11 | V5V | out | 5.0 V | module supply input |
| 12 | DGND | -- | 0 V | DGND |

**J2 -- module #1 analogue signals (10)** and **J23 -- module #1 analogue rails (6)**

| Way | J2 net | Dir | Module pin | | Way | J23 net | Dir | Module pin |
|---|---|---|---|---|---|---|---|---|
| 1 | IN1 | out | IN1P (Fz) | | 1 | AVDD | **in** | AVDD |
| 2 | IN2 | out | IN2P (Cz) | | 2 | AVSS | **in** | AVSS |
| 3 | IN3 | out | IN3P (Pz) | | 3 | BIASIN | out | BIASIN |
| 4 | IN4 | out | IN4P (C3) | | 4 | AGND_REF | -- | analogue reference |
| 5 | IN5 | out | IN5P (C4) | | 5 | AVDD | **in** | AVDD (second conductor) |
| 6 | IN6 | out | IN6P (T7) | | 6 | AVSS | **in** | AVSS (second conductor) |
| 7 | IN7 | out | IN7P (T8) | | | | | |
| 8 | IN8 | out | IN8P (F7) | | | | | |
| 9 | SRB1 | out | SRB1 | | | | | |
| 10 | BIASOUT | **in** | BIASOUT | | | | | |

AVDD and AVSS are **power inputs to the carrier**, produced by module #1's own regulators.
The carrier is the load. BIASOUT is likewise an output of the module: it enters the carrier at
J2.10, passes through R11 and leaves as BIAS_EL on J14.11 to the Fpz electrode.
Note the asymmetry, because it matters to the safety case and not to the interface: R11 is
the only one of the sixteen protection resistors that faces outward, and D11 and C11 sit on
`BIAS_EL`, the patient side of it, where the other fifteen have their clamp and filter on the
module side. RISK-EEG-011 SF-1a, SF-6a and SR-12 carry the consequence.
BIASIN is not driven by anything on the carrier; with the internal channel-average bias loop
of E-05 selected it is not required, and the net exists only so a module needing an external
feedback return can be strapped at the module end.

**J3 -- ADS1299 module #2, digital (12)**

| Way | Net | Dir | Domain | Module pin | Difference from J1 |
|---|---|---|---|---|---|
| 1 | DVDD3V3 | out | 3.3 V | DVDD | -- |
| 2 | DGND | -- | 0 V | DGND | -- |
| 3 | SCLK | out | 3.3 V CMOS | SCLK | -- |
| 4 | MOSI | out | 3.3 V CMOS | DIN | -- |
| 5 | **DAISY** | -- | 3.3 V CMOS | DOUT | goes to J5.1, not to MISO |
| 6 | NC_DRDY2 | -- | -- | DRDY | **not used**; TP17 only |
| 7 | CS | out | 3.3 V CMOS | CS | -- |
| 8 | START | out | 3.3 V CMOS | START | -- |
| 9 | RESET | out | 3.3 V CMOS | RESET | -- |
| 10 | CLK_ADS | out | 3.3 V CMOS | CLK | module #2 **receives** the clock |
| 11 | V5V | out | 5.0 V | supply | -- |
| 12 | DGND | -- | 0 V | DGND | -- |

**J4 -- module #2 analogue signals (10)** and **J29 -- module #2 analogue rails (6)**

| Way | J4 net | Dir | Module pin | | Way | J29 net | Dir | Module pin |
|---|---|---|---|---|---|---|---|---|
| 1 | EMG1 | out | IN1P (cheek) | | 1 | AVDD2 | in | AVDD |
| 2 | EMG2 | out | IN2P (submental) | | 2 | AVSS2 | in | AVSS |
| 3 | EMG3 | out | IN3P (laryngeal) | | 3 | BIASIN | out | BIASIN |
| 4 | ENV_STIM | out | IN4P | | 4 | AGND_REF | -- | analogue reference |
| 5 | ENV_VOICE | out | IN5P | | 5 | AVDD2 | in | AVDD (second) |
| 6 | ENV_ROOM | out | IN6P | | 6 | AVSS2 | in | AVSS (second) |
| 7 | SPARE1 | out | IN7P (EOG) | | | | | |
| 8 | SPARE2 | out | IN8P (EOG) | | | | | |
| 9 | SRB1 | out | SRB1 | | | | | |
| 10 | NC_BIASOUT2 | -- | BIASOUT | | | | | |

**J5 -- daisy stub to module #1 (4):** 1 DAISY (module #2 DOUT into module #1 DAISY_IN),
2 CLK_ADS (module #1 CLKOUT), 3 DGND, 4 DGND. J5 exists because generic ADS1299 breakouts
expose DAISY_IN and CLKOUT inconsistently. If module #1's main digital header already carries
both, JMP-05 is not fitted and the two nets are picked up on J1.10 instead; record which was
done on the build record.

**J8 -- audio codec module (14) and J9 -- microphone feeds (4)**

| Way | J8 net | Dir | Domain | Codec function |
|---|---|---|---|---|
| 1 | DVDD3V3 | out | 3.3 V | digital and analogue supply |
| 2 | DGND | -- | 0 V | ground |
| 3 | I2S_MCLK | out | 3.3 V CMOS | master clock in |
| 4 | I2S_BCLK | out | 3.3 V CMOS | bit clock in |
| 5 | I2S_LRCK | out | 3.3 V CMOS | word clock in |
| 6 | I2S_DIN | in | 3.3 V CMOS | codec ADC serial data **out** |
| 7 | I2S_DOUT | out | 3.3 V CMOS | codec DAC serial data **in** |
| 8 | SDA | bidir | 3.3 V open-drain | control I2C, pulled up on the carrier by R94 |
| 9 | SCL | out | 3.3 V open-drain | control I2C, pulled up on the carrier by R95 |
| 10 | HP_TAP | in | analogue, <= 1.1 V pk | headphone-amplifier tap |
| 11 | HP_L | in | analogue | headphone left out |
| 12 | HP_R | in | analogue | headphone right out |
| 13 | HP_GND | -- | analogue | headphone return |
| 14 | V5V | out | 5.0 V | headphone amplifier supply |

All I2S names are from the **ESP32-S3's** point of view. I2S_DIN is data travelling into the
controller and therefore out of the codec. Getting this backwards is the single most common
integration error on this interface, and it is why the column above names the codec function
separately.

J9: 1 VOICE_PRE (in, analogue), 2 ROOM_PRE (in, analogue), 3 DGND, 4 MIC_MUTE (out, 3.3 V
CMOS). Way 4 is present so that a codec module with a hardware ADC-mute input can share the
line; if the chosen module has no such pin, way 4 is not mated at the module end and the mute
of record is J28.4.

**Remaining module connectors**

| Ref | Way-by-way |
|---|---|
| J10 | 1 VDD_ISO (out, 3.3 V via L1) - 2 USB_DN (bidir) - 3 USB_DP (bidir) - 4 DGND |
| J11 | 1 DVDD3V3 (out) - 2 DGND - 3 SDA (bidir) - 4 SCL (out) |
| J12 | 1 VBAT (bidir, cell) - 2 DGND - 3 VBUS_CHG (out, 5 V) - 4 CHG_CE (out, 3.3 V CMOS) - 5 SDA (bidir) - 6 SCL (out) - 7 VSYS (in, 3.0-4.4 V) - 8 NC_CHG_STAT |
| J19 | 1 DVDD3V3 (out) - 2 DGND - 3 LED_SR_DATA (out) - 4 LED_SR_CLK (out) - 5 LED_SR_LATCH (out) - 6 LED_OE (out, tied low by R87) - 7 LED_MR (out, pulled up by R88, C88 POR) - 8-15 SR_Q0...SR_Q7 (in) - 16 NC_SR_Q7S |
| J20 | 1 DVDD3V3 (out) - 2 DGND - 3 SD_CLK (out) - 4 SD_CMD (bidir) - 5 SD_D0 (bidir) - 6, 7, 8 DGND |
| J21 | 1 DVDD3V3 (out) - 2 DGND - 3 VOICE_PRE (in, analogue) - 4 VOICE_RAW (out, analogue) - 5 NC_MIC_GAIN - 6 DGND |
| J25 | 1 VSYS (out, 3.0-4.4 V) - 2 DGND - 3 V5V (in, 5.00 V) - 4 DGND - 5 BOOST_EN (out, pulled to VSYS by R86 100 kOhm) - 6 NC_BOOST_PG |
| J28 | 1 DVDD3V3 (out) - 2 DGND - 3 ROOM_PRE (in, analogue) - 4 MIC_MUTE (out, 3.3 V CMOS) |

### 1.2 Pin assignments, harness, panel, cell and debug connectors

| Ref | Way-by-way |
|---|---|
| J13 | 1 VBAT - 2 DGND (JST PH 2.00 mm, keyed) |
| J14 | 1 E_Fz - 2 E_Cz - 3 E_Pz - 4 E_C3 - 5 E_C4 - 6 E_T7 - 7 E_T8 - 8 E_F7 - 9 REF_L - 10 REF_R - 11 BIAS_EL - 12 HARN_SHIELD |
| J15 / J16 / J17 | single pole: EMGIN1 / EMGIN2 / EMGIN3 |
| J18 | 1 VOICE_RAW - 2, 3, 4 DGND |
| J22 | 1 EOGIN1 - 2 AGND_REF - 3 EOGIN2 |
| J24 | 1 VBUS_IN - 2 DGND (JST PH 2.00 mm, keyed) |
| J26 | 1 DVDD3V3 - 2 DGND - 3 UART_TX - 4 UART_RX - 5 RESET_EN - 6 NC_GPIO0 |
| J27 | 1 HP_L - 2 HP_R - 3 HP_GND - 4 NC_HP_DET |
| J30 | 1-8 LED1...LED8 - 9 LED_V - 10 LED_GND |

Nothing digital enters J14 (ECO-EEG-014). The contact lights leave on J30, a separate cable.

**J26 is console and recovery only, and it cannot enter download mode.** RFQ-EEG-001 Rev E
E-28 asks for TP1 to TP18 plus this 1x6 UART debug header; the 2x5 1.27 mm JTAG/SWD header of
Rev C is withdrawn, because the ESP32-S3 has no SWD and its JTAG pins are otherwise used.
Way 6 is **NC_GPIO0**, a spare way and not a boot-mode line: GPIO0 is committed to
LED_SR_LATCH at J7 way 14 (ECO-EEG-009). End-of-line and field flashing go through the
DevKitC-1's own UART USB-C port, which carries the auto-reset circuit (DTR and RTS to EN and
IO0) on the DevKit itself and is reachable through the MP-01 opening of section 4.

---

## 2. Required module interfaces

Each module is specified by the signals it must present, not by a brand. A part that meets the
interface may be fitted after the qualification of section 6. Two modules are explicitly not
substitutable: the ESP32-S3-DevKitC-1-N16R8 (E-18, the pin map and firmware are written to
it) and the ADuM4160 isolator (E-24, S-03, it is the safety barrier). RFQ-EEG-001 section 10
additionally names the ADS1299 modules and the ATECC608B breakout as non-substitutable; for
those two the **device** is fixed and the breakout board carrying it may be changed under the
qualification of section 6, which is the reconciliation AVL-EEG-017 section 2 records.

### 2.1 ADS1299 eight-channel front-end module, x2 (PIEEG-8 class)

**Must present** a digital header carrying DVDD (3.3 V in), DGND, SCLK, DIN, DOUT, DRDY, CS,
START, RESET and CLK; a 5 V supply input; and an analogue header carrying IN1P-IN8P, SRB1,
BIASOUT, BIASIN, AVDD, AVSS and an analogue reference pin. The module must generate AVDD =
+2.50 V and AVSS = -2.50 V on board from the 5 V input and must expose both, because the
carrier's protection clamps and envelope detectors all run from those rails.

**The carrier assumes:**

| Assumption | Value | Consequence if untrue |
|---|---|---|
| AVDD / AVSS available at the header | +/-2.50 V +/-5 % | D1-D16 clamp to the wrong level; U1-U3 have no supply |
| Spare regulator capacity beyond the converter | >= 25 mA on each rail | carrier analogue load is about 10 mA per rail *(calculated: three OPA4376 at 3.04 mA plus the dividers)* |
| Module #1 CLK is an output (CLKOUT enabled) | 2.048 MHz | both converters free-run and lose simultaneity (E-01) |
| Module #2 CLK is an input | -- | two drivers contend on CLK_ADS |
| DAISY_IN reachable, on the header or on J5 | -- | sixteen channels cannot be daisy-chained |
| Digital I/O referenced to 3.3 V | V_IH <= 2.48 V, V_OH >= 2.48 V | SPI marginal at >= 4 MHz (E-19) |
| Inputs tolerate the series protection resistance | **68 kOhm fitted** since ECO-EEG-024 was applied on 2026-09-02; this row read "47 kOhm fitted, 68 kOhm proposed" | E-03 noise budget invalid |

The protection network itself is R1-R16, D1-D16 (**BAV99**, not BAT54S -- Schottky leakage
across the series resistor is an offset error on a 10 uV input) and C1-C16 (10 nF C0G,
`GCM1885C1H103JA16D`). The noise and flatness arithmetic for that network lives in
RISK-EEG-011 section 4 and is not recomputed here, and that section has not been re-issued
since ECO-EEG-024 was applied, so it still prints the 47 kOhm figures as live. **Corrected
2026-09-02: R1-R16 are 68 kOhm.** ECO-EEG-024 is applied in `design.py`, which gives
2.5 V / 68 kOhm = **36.8 uA against S-02's 50 uA limit, so the limit is met on the
calculation**; until that date this paragraph said S-02 was not met at the fitted 47 kOhm,
at 53.2 uA, and that a module had to tolerate either value. **68 kOhm is the value a module
is qualified against from now on.** E-10's flatness band goes with the resistor: it is
**+/-1.0 dB**, the branch that requirement states for exactly the 68 kOhm case, where the
47 kOhm that is no longer fitted sat on the +/-0.5 dB branch. Nothing here has been measured,
and **SR-01 is closed in the design and not signed off**.

**Which module is #1.** The module whose DOUT feeds the other's DAISY_IN is device 2 in the
firmware's frame order. Module #1 is the one wired to J1/J2/J23 and is the clock source and
the rail source. The two modules are not interchangeable once fitted; label both at incoming
inspection and keep the pair together. A swap is not caught until TST-EEG-004 T7, where EEG
gain is 24 and EMG gain is 12.

### 2.2 ESP32-S3-DevKitC-1-N16R8 -- see section 5

### 2.3 Audio codec module (ES8388 class)

**Must present** an I2S slave port (MCLK, BCLK, LRCK, ADC data out, DAC data in), an I2C
control port, at least one stereo DAC output through a headphone amplifier able to drive the
shipped headphones to 85 dB SPL at <= 0.1 % THD (E-13), at least two single-ended ADC inputs,
and a node on the headphone-amplifier output usable as HP_TAP.

RFQ A-04 is restated as **32 to 64 Ohm** headphones and the calibrated output level is
measured per model. The shipped part is the ATH-M20x at 47 Ohm, so the bench load for the
codec measurements is **47.0 Ohm**.

**Maximum acoustic output (E-29).** The headphone output must not exceed **100 dB SPL** at
any commanded level, measured on an artificial ear, and the firmware must clamp the codec
volume register to the value measured at calibration. Calculated full-scale output is about
110 dB SPL, which is why the clamp is a requirement and not a preference; a codec module
whose amplifier gain cannot be fixed or whose volume register cannot be clamped does not meet
this interface. E-29 is verified at **TST-EEG-004 step T28**, a type test run once per lot on
one unit and listed in TST-EEG-004 section 14. There is no per-unit acoustic step and this
document does not invent one.

**HP_TAP** is the only pin on this interface that is not a standard module feature. E-16
requires the tap to be taken **after** the amplifier and **before** any user-adjustable
control. It must present between 0.1 and 1.1 V peak at the maximum programmed stimulus level,
into a source impedance of <= 1 kOhm. 1.1 V peak is the ceiling because the envelope chain's
output divider (R27/R28, 22 k / 2 k2, x0.0909) turns 1.1 V into the +/-100 mV the ADS1299
input sees at gain 1. If the module offers no tap, build one inside the JMP-08 module-end
assembly as a 10 kOhm / 1 kOhm divider from HP_L to HP_GND, tap to way 10, and record it. Do
not tap before the amplifier.

The codec supply is split: DVDD3V3 on way 1, V5V on way 14 for the headphone amplifier. A
module with a single supply pin leaves way 14 unmated and runs from 3.3 V; the 85 dB SPL
figure of E-13 must then be re-measured.

### 2.4 USB isolator module (ADuM4160, not substitutable)

**Must present** device-side VDD, D-, D+ and GND on a header, with the **host** receptacle on
the module itself, presented to the outside world through a gasketed aperture in POD-P1. The
host connection is a socket, not a captive cable: WH-08 and the cable gland are deleted from
the Phase 1 build and the captive lead through a gland is a Phase 2 item for the helmet shell.
The kit ships the two cables of RFQ A-07 and one of them is the host lead. The module must be
strapped for full speed (12 Mbit/s) upstream with the device-side pull-up disabled, because
the ESP32-S3's native USB PHY provides its own D+ pull-up.

**The host connector is a live non-conformance.** E-24 asks for USB-C and the named candidate
module presents USB-B. The interim resolution is a short USB-B-to-USB-C panel pigtail
(**WH-09**) until an isolator module with a USB-C host connector is qualified. That is an
interim answer, not a settled interface.

The carrier feeds the device side from DVDD3V3 through L1 (600 Ohm at 100 MHz ferrite) as
VDD_ISO, bulk-decoupled by C89 (10 uF) and C87 (100 nF). Isolation >= 2.5 kV RMS for one
minute and creepage >= 8 mm are S-03 requirements met **on the module**, not on the carrier;
that 2.5 kV RMS figure is a type test evidenced by the supplier's certificate at incoming
inspection and is never repeated per unit. The per-unit check is the 500 V DC
insulation-resistance measurement of TST-EEG-004 step T20.

The carrier's contribution is the isolation keep-out specified in **DSN-EEG-003 section 3.3**,
which on a four-layer board means no copper on any of L1, L2, L3 or L4 in that strip -- the
inner reference planes are cut back from it exactly as the outer layers are. The Rev B DRC
report lists no violation of any kind, isolation included, so the strip is clear on all four
layers as drawn; that
is a report result and not an assumption, and it is the artwork half of the creepage argument
REG-EEG-012 clause 8.5.2 rests on. **No conductor of
JMP-10 may terminate on any host-side pin of the module, and JMP-10 must not be routed across
the module's barrier.** MP-01 is unbroken above the barrier and is printed in PA12 with no
conductive filler and no metal insert, so nothing above the plane of the plate bridges it
either; the Rev A "20 x 12 mm isolator keep-out slot" was never in `mech_gen.py` and is
withdrawn.

### 2.5 Secure element breakout (ATECC608B)

**Must present** VDD (2.0-5.5 V), GND, SDA and SCL. Way count and order on the module are
free -- the jumper is the adapter. The referenced Adafruit 4314 presents VIN, 3Vo, GND, SCL,
SDA, which is a five-way header in a different order from J11's four ways; JMP-11 resolves it
(section 3.3). Do not back-feed the module's regulator output (3Vo). The device arrives with
its configuration zone unlocked; it is locked and provisioned at end of line (E-21). Swapping
this module after provisioning destroys the device identity the browser is bound to.

### 2.6 Charger and fuel gauge

**The baseline is one combined charger-plus-gauge assembly on a single J12 jumper**, and
JMP-12 is then a straight eight-way jumper. If the programme supplies two separate breakouts,
the gauge mounts on MP-01 beside the charger and its VBAT and I2C taps are made at the MP-01
end of the J12 jumper: that is the **Y jumper drawn in section 3.3**, a specified part and
not a hand-built variation.

**Charger must present** VBUS in (4.35-6.0 V), GND, BAT (to the cell), SYS (power-path
output), a charge-enable input, and optionally STAT. RFQ E-23 asks for a charger IC with
thermal regulation and no charging above 45 C. The module must have the thermal regulation and
a candidate without it does not meet this interface, but thermal regulation folds the charge
current back on the charger IC's **own die** temperature, which is not the cell's.
**E-23's 45 C inhibit is not met and cannot be tested, and no module choice or substitution
can close it**: there is no NTC net in `design.py` and no thermistor way on J12 or J13, so
nothing in this design measures cell temperature. **RFQ S-04's thermistor-monitored charging
is not met and stays not met** for the same reason. TST-EEG-004 T4 tests the charge interlock
and records that the 45 C inhibit is not tested and cannot be; TST-EEG-004 section 10 carries
E-23 as not met in part and staying not met; RFQ-EEG-001 Rev E says the same at E-23 and S-04.
It is an open hardware item with no closure proposed, listed in DSN-EEG-003 section 11 and
RISK-EEG-011, and a module fitted to J12 cannot close it, because the carrier gives the
thermistor nowhere to land.

CHG_CE is driven by GPIO47 and holds the charger disabled for the whole of a session (S-01,
second interlock; the first is VBUS_DET at J6.14). **Confirm the polarity of the module's
enable pin at qualification and record it**; the interlock is a safety function and a
wrong-polarity assumption disables it silently.

**Gauge must present** a cell-sense input, GND, SDA and SCL at 3.3 V logic. ALRT is not
brought to the carrier.

### 2.7 Buck-boost module (TPS63020 class)

**Must present** VIN, GND, VOUT, GND and an enable input. Output fixed at 5.00 V +/-2 %,
>= 1 A continuous, switching above 200 kHz (E-25). Input range must cover the cell across
discharge, 3.0 to 4.4 V.

The enable is the trap. R86 pulls BOOST_EN to VSYS through 100 kOhm so that V5V comes up
before DVDD3V3 exists (ECO-EEG-002). A module carrying its own 10 kOhm pull-down on EN divides
that to 3.7 x 10/110 = **0.34 V** *(calculated)*, below any sensible V_IH, and the rail never
starts. Measure BOOST_EN with the module fitted and VSYS at 3.7 V: it must read >= 1.2 V. A
module with an adjustable output must be set to 5.00 V and the trimmer locked with varnish.

**V5V load, calculated, not measured.** The DevKit's line below is the whole of the DVDD3V3
load of section 5.3, because the DevKit's on-board LDO is fed from V5V at J6.21 and passes
very nearly its own output current: an LDO is not a converter, so the 3.3 V load appears on
the 5 V rail almost one for one. Rev A's "DevKit about 120 mA" counted the module alone and
left the carrier's 3.3 V loads out of the 5 V budget; it is withdrawn, and this table and the
table of section 5.3 are now the same arithmetic seen from the two rails.

| Load on V5V | Recording, typical (mA) | Worst case simultaneous (mA) |
|---|---|---|
| DevKit, including everything its LDO feeds on DVDD3V3 (section 5.3) | 190 | 288 |
| ADS module #1 | 45 | 45 |
| ADS module #2 | 45 | 45 |
| codec headphone amplifier | 20 | 40 peak |
| **Total on V5V** | **about 300** | **about 420** |

Both columns are inside the 1 A rail. Output ripple limit 50 mV pk-pk measured at TP16 with a
20 MHz-limited probe. This module is a field-replaceable unit and belongs in the SVC-EEG-013
FRU list.

**What that means at the cell, and where it disagrees with TST-EEG-004 T3.** The buck-boost
draws the V5V load from VSYS, so at 3.900 V and an assumed 88 % efficiency the typical figure
is 5.00 V x 0.300 A / (3.900 V x 0.88) = **about 440 mA at J13** while recording, and the
worst case is about 610 mA *(calculated)*. **TST-EEG-004 T3 limits the recording current at
J13 to 150 mA, and that limit and these tables cannot both be right**: on this arithmetic
every unit would fail T3. About 440 mA is also what RFQ E-22 allows, since a 3000 mAh cell
giving four hours of recording permits 750 mA average. TST-EEG-004 owns the step and its
limit, so this document does not restate T3 and does not number a step of its own; the
disagreement is carried as open point 13 of section 8 and the first article settles it with a
measurement.

### 2.8 microSD breakout, one-bit SDMMC

**Must present** a push-push microSD socket wired **directly** to a 3.3 V header: VDD, GND,
CLK, CMD and DAT0, with no level shifter and no on-board regulator between the header and
the socket. Most "microSD modules" sold for Arduino are SPI adapters with a 5 V regulator and
a unidirectional buffer; they cannot work in SDMMC mode, where CMD and DAT0 are bidirectional.
This is a hard reject criterion. Card detect is not brought out and firmware must not rely on
it.

The sample stream is **50.7 kB/s of frame payload at 1000 Hz** (1015 bytes every 20 ms).
E-20's approximately 70 kB/s is an allowance that covers STATUS and SIGNATURE frames and
filesystem overhead; the requirement is not changed by stating the payload figure. The
one-bit interface gives about 2 MB/s *(calculated)*, which is why the three data lines
four-bit mode would have used are spent on the shift register instead (ECO-EEG-009).

### 2.9 Boom microphone preamplifier

**Must present** VDD (3.3 V), GND, a single-ended microphone input and a single-ended
amplified output. **Gain must be fixed.** E-16's reference-tone calibration reports a gain,
and a gain that moves is not a gain.

**Which part is not settled, and it must be treated as not settled.** The MAX9814 named in
package v1 is an automatic-gain-control part and RFQ E-14 forbids AGC; disabling it is a
module-dependent modification, so AVL-EEG-017 keeps the MAX9814 **not approved** and it is
named here only as the package-v1 candidate. The preferred route is a fixed-gain part of the
MAX4466 class. Until a part is bought and measured, this module is specified by the interface
above and by nothing else. If a candidate implements AGC, the AGC must be disablable by a
strap on the module and the strap position recorded; AGC that cannot be disabled disqualifies
the module.

**Where the preamplifier sits.** J21 carries VOICE_RAW **out** to the module and VOICE_PRE
**in** from it, and J18 brings VOICE_RAW in from the boom pigtail. The preamplifier is
therefore **on MP-01**, and the boom carries the bare electret capsule and its screen.
Package v1 described it as being on the boom and WH-EEG-008 Rev B described it as being on the
carrier; `design.py` governs, J21 is a carrier socket serving a plate-mounted module, and both
of those descriptions are corrected. The boom detaches at the temple for cleaning (E-14) and a
detachable preamplifier would be a second thing to lose.

Way 5, NC_MIC_GAIN, is reserved for the module's gain-select pin and is not connected on the
carrier. If a strap is needed, make it inside the module-end connector of JMP-21 to way 1 or
way 2 and record which.

### 2.10 Room microphone module

**Must present** VDD (3.3 V), GND, a single-ended analogue output and a **hardware** mute
input that gates the audio path in the analogue domain (E-15). A register-controlled mute
does not meet E-15.

MIC_MUTE is defined in this document as **mute-not**: logic high = room microphone live,
logic low or open circuit = muted. The net name is retained from `design.py`. GPIO21 is an
input at reset and floats, so the muted state must be the module's default with the line
open. The carrier carries no pull-down on this net. Verify at qualification: with JMP-28 way 4
unmated and the module powered, the audio path must be attenuated by >= 60 dB. If it is not,
fit a 100 kOhm pull-down inside the module-end connector of JMP-28 and record it.

No catalogue module is yet known to meet the hardware-mute requirement. If none does, the
fallback is an electret capsule with an analogue switch in the module-end connector of
JMP-28, which becomes a programme-designed sub-assembly with its own drawing and AVL line.
That is recorded in AVL-EEG-017 and is not closed here.

### 2.11 Shift-register module (74HC595)

**Must present** SER, SRCLK, RCLK, OE, MR (SRCLR), QA-QH, VCC and GND, all brought to the
header, running at 3.3 V. Q0-Q7 sink and source the eight contact lights through R70-R77
(1 kOhm). If the module ties OE or MR internally, ways 6 and 7 are left unmated, R87, R88 and
C88 have no effect, and that is recorded on the build record -- dark-at-boot does not depend
on them.

**Contact-light drive, calculated.** Bicolour two-lead LED, V_f = 2.0 V, series 1 kOhm:
(3.3 - 2.0) / 1000 = **1.3 mA** per site. Eight sites through the LED_V common: **10.4 mA**
sourced or sunk by GPIO48 through R78 (0 Ohm), inside the ESP32-S3's 40 mA per-pin limit and
well inside the 74HC595's 35 mA per-output and 70 mA per-package limits. LED_V is GPIO48,
an input at reset, so nothing can light at boot whatever the shift register holds. LED_MR's
power-on reset is R88 x C88 = 10 kOhm x 100 nF = **1.0 ms** *(calculated)*.

The bicolour phase scheme -- phase A green, phase B red, alternating to show amber -- is
specified here as an interface and, **corrected 2026-09-02, it is now implemented in
firmware**: until that date `lights_write()` and `lights_task()` were on and off only and
this paragraph said T11 could not pass until they were written. `lights_task()` drives both
phases from the converter's positive-side lead-off comparator, read at **two thresholds**.
One interface number moves with it: `LIGHT_PHASE_HZ` is still 240, but the half-phase
quantises to the FreeRTOS tick, so **the alternation this interface actually carries is
about 250 Hz**, which is what E-27's "above 100 Hz" requires and what T11's colorimeter
reads. The hardware interface above is unchanged and complete.

**Corrected again 2026-09-02 (FW-D17).** This paragraph read that the driver took its
colours from `LOFF_STATP` and `LOFF_STATN`, and that a build enabling `LOFF_SENSP` only
therefore showed amber where it should have shown red. That was true of the code and is no
longer, because the premise was wrong: **this interface is single-ended.** J2 carries IN1 to
IN8, one shared `SRB1` reference and `BIASOUT`, so there is no per-site negative electrode
for `LOFF_STATN` to report on, and enabling `LOFF_SENSN` would have given all eight channels
the same bit -- the state of the one shared reference. The driver now sweeps `COMP_TH`
between a sensitive and an insensitive setting and latches the positive-side result at each:
a site that trips neither is **green**, one that trips the sensitive threshold only is
**amber**, and one that trips both is **red**. The insensitive set is a subset of the
sensitive one by construction, so the three states are exhaustive and cannot overlap.
**T11 has not been run**, because no unit exists, and the two `COMP_TH` values are the
datasheet's endpoints rather than measured ones -- T11 is where they get their real values.

---

## 3. The ribbon-jumper schedule

### 3.1 The jumper part

| Property | Specification |
|---|---|
| Cable | flat ribbon, 28 AWG (7/0.127) stranded tinned copper, PVC, grey with a red stripe on conductor 1. Reference 3M 3365 series, 1.27 mm pitch, used at 2.54 mm by discarding alternate conductors |
| Analogue jumpers (JMP-02, -04, -23, -29) | screened ribbon; braid or foil with a drain wire, **drained at the carrier end only** into the AGND_REF crimp of JMP-23.4 / JMP-29.4; module end floating |
| Carrier end | 2.54 mm single-row **male** contacts (the carrier sockets are female), entering through the WH-KEY-01 shroud |
| Module end | 2.54 mm single-row **female** contacts (module headers are male) |
| Way 1 | red stripe conductor, both ends, always |
| Marking | printed heat-shrink sleeve at each end: jumper ID and the connector at that end, e.g. `JMP-10 / J10` and `JMP-10 / ISO` |
| Maximum length | **60 mm**, tolerance +0 / -10 mm, measured connector face to connector face |
| Minimum bend radius | 10 mm |
| Workmanship | IPC/WHMA-A-620 class 2 |

**Keying is decided.** At the **module end**, a 2.54 mm shrouded polarised IDC header is used
wherever the module carries one; where the module has only a plain pin strip, pin 1 is marked
on the module and the jumper is labelled. At the **carrier end**, the printed keying shroud
**WH-KEY-01** -- part of the MP-01 print set -- fits over the socket and takes the jumper's
male contacts, so the jumper can only enter one way round and only on the socket it was made
for. Section 6.1 lists which sockets carry a shroud.

**The connector system is Harwin M20, and this sentence is a correction.** Rev B as first
issued specified "a Molex KK 254 crimp build: female housings 22-01-30nn with 08-50-0114
terminals at the module end, free-hanging male housings with 08-52-0072 terminals at the
carrier end, with the exact housing part numbers per way count fixed at kitting and listed in
AVL-EEG-017". Three things were wrong with that. AVL-EEG-017 did not carry the per-way-count
part numbers, so the pointer was a dead end rather than a stated gap, and thirty-eight
connector bodies and about three hundred contacts per unit could not be put on a purchase
order. WH-EEG-008 section 6 had already specified **Harwin M20** for the five crimped harness
housings, so the kit would have carried two incompatible crimp systems and two crimp tools.
And the choice is not free: `tools/mech_gen.py` cuts the WH-KEY-01 shroud cavity at
`KEY_CAV_W = M20_HSG_W + 0.30 = 4.50 mm` and asserts both that the housing enters with
0.30 mm of clearance and that a reversed housing is stopped by 0.40 mm of interference, so a
housing outside **4.20 +0.10 / -0.20 mm across the flats** either will not enter the shroud or
will not be keyed by it. A KK 254 body is not that envelope. Taking the Molex wording would
therefore have made every printed shroud in the kit the wrong size, silently, and left the one
safety-relevant mis-mate in the kit -- a reversed WH-01 -- with a dust cover in front of it.

The system is therefore **Harwin M20 crimp**: male contacts and polarised male housings at the
carrier end, female contacts and housings at the module end, in the way counts of section 3.3
and WH-EEG-008 section 1. **AVL-EEG-017 section 1.6.1 is the single home for the per-way-count
housing and contact table, the quantities and the selection criteria**, and this document does
not restate them. No Harwin ordering suffix is confirmed: the family roots the programme has
quoted are M20-106 for bodies and M20-118 for the male contact, the female contact family has
never been named anywhere, and all of them are carried in that section as OPEN WITH CRITERIA
to be resolved at the purchase order rather than guessed here.

The qualification is unchanged: 17 jumpers built, every way rung out against the tables of
section 1.1, 20 insertion cycles with no contact resistance above 50 mOhm.

### 3.2 Why 60 mm

The ten-way analogue jumpers carry eight electrode nets, SRB1 and BIASOUT side by side with
no interleaved grounds. J2 and J4 have ten ways and every one is a signal; there is no way
left to ground. The screen keeps external fields out of the bundle but does nothing between
conductors inside it, so length is the only control the design has.

Calculated, with 3M 3365's typical mutual capacitance of 43 pF/m (13 pF/ft):

| Step | Value |
|---|---|
| Coupling capacitance between adjacent conductors at 60 mm | 43 pF/m x 0.060 m = **2.6 pF** |
| Victim node shunt (C1-C16 to AGND_REF) | 10 nF |
| Attenuation aggressor to victim | 2.6 pF / (2.6 pF + 10 nF) = 2.6 x 10^-4 = **-71.7 dB** |
| Largest realistic neighbouring artefact (electrode pop, blink) | 1 mV pk |
| Coupled into the neighbour | **0.26 uV pk** |
| Front-end noise floor (RISK-EEG-011 section 4, calculated) | 0.27 uV RMS |

60 mm is the length at which the coupled voltage from the largest artefact a neighbouring
electrode is likely to produce falls to the front end's own noise floor. Coupling scales
linearly with length: a 120 mm jumper doubles it and puts the artefact 6 dB above the floor.
The limit is applied to every jumper, not only the analogue ones, so that the assembler has
one number to remember.

**E-04 is restated at -80 dB.** The Rev C -100 dB crosstalk limit is not achievable through a
60 mm un-interleaved ribbon and, at 40 dB below this instrument's noise floor, is not
measurable on this hardware either. E-04 now reads **-80 dB at 50 Hz, measured on the
carrier**, with the ribbon's own contribution characterised once on the first prototype
(ECO-EEG-026). The -71.7 dB above is the ribbon's calculated contribution and is the honest
number for the jumper; it is not the carrier figure E-04 is graded against.

On the digital jumpers 60 mm is not a signal-integrity constraint. Propagation over 60 mm is
about 0.3 ns one way *(calculated at 5 ns/m)*; a round trip of 0.6 ns is shorter than half
the 2 ns edge of a 3.3 V CMOS driver, so no termination is required at the >= 4 MHz SPI of
E-19 or the 2.048 MHz shared clock.

### 3.3 Schedule

| Jumper | Carrier | Ways | Length (mm) | Module | Screened | Notes |
|---|---|---|---|---|---|---|
| JMP-01 | J1 | 12 | 55 | ADS #1 digital header | no | |
| JMP-02 | J2 | 10 | 45 | ADS #1 analogue header | **yes** | drain to JMP-23.4 |
| JMP-23 | J23 | 6 | 45 | ADS #1 rail header | **yes** | carries the drain of JMP-02 |
| JMP-03 | J3 | 12 | 55 | ADS #2 digital header | no | way 5 is DOUT, way 6 unmated |
| JMP-04 | J4 | 10 | 45 | ADS #2 analogue header | **yes** | drain to JMP-29.4 |
| JMP-29 | J29 | 6 | 45 | ADS #2 rail header | **yes** | see section 7.1 for ways 1, 2, 5, 6 |
| JMP-05 | J5 | 4 | 40 | ADS #1 DAISY_IN / CLKOUT | no | fitted only if needed |
| JMP-08 | J8 | 14 | 55 | codec module | no | ways 10-13 are analogue |
| JMP-09 | J9 | 4 | 50 | codec ADC inputs | no | way 4 optional |
| JMP-10 | J10 | 4 | 40 | isolator, **device side only** | no | must not cross the barrier |
| JMP-11 | J11 | 4 -> 5 | 40 | secure element | no | adapter jumper, see below |
| JMP-12 | J12 | 8, or 8 -> 6 + 4 | 55, branches 25 | charger and gauge | no | straight for a combined board, Y for two boards, see below |
| JMP-19 | J19 | 16 | 50 | 74HC595 module | no | |
| JMP-20 | J20 | 8 | 45 | microSD breakout | no | ways 6-8 all DGND |
| JMP-21 | J21 | 6 | 45 | boom preamplifier | no | ways 3, 4 analogue |
| JMP-25 | J25 | 6 | 45 | buck-boost module | no | ways 1, 3 carry rail current |
| JMP-28 | J28 | 4 | 40 | room microphone | no | |

Seventeen jumpers, 134 carrier ways.

**JMP-28 and WH-05 are the same connector, and only one of them is built.** J28 appears in the
schedule above as a 60 mm jumper to the room-microphone module, and in WH-EEG-008 section 3.5
as the carrier end of WH-05, a 180 mm cable to the module on WH-ADP-02. The room-microphone
module is **not** on MP-01: WH-EEG-008 section 3.9 bonds WH-ADP-02 to the inside of the POD-P1
wall behind the acoustic port, 180 mm away, so WH-05 is what is actually built and there is no
separate 60 mm jumper. AVL-EEG-017 section 1.6.1 counts the 4-way male housing on J28 **once**,
and a buyer must not buy two. The row is left in the schedule, and the seventeen-jumper and
134-way figures with it, because ASM-EEG-007 section 8, AVL-EEG-017 section 1.6 and
DSN-EEG-003 section 2.1 all quote them into labour estimates and a correction that is not an
ECO should not move three documents' arithmetic underneath them. The real count is **sixteen
jumpers and 130 carrier ways**, and it is corrected in this schedule at the next revision of
this document, under an ECO -- open point 15.

**ASM-EEG-007 section 8 owns the labour estimate and it
is not twenty minutes.** Building the set costs 60 minutes per unit in Phase 1, and 25 minutes
in Phases 2 and 3 where the set is bought pre-made; fitting it and running the keying check
costs a further 20 minutes in every phase (ASM steps 2.4 and 2.6). The "twenty minutes"
carried in earlier issues of this section is the size of ASM's fitting step alone and leaves
the build out, so it is withdrawn here. **DSN-EEG-003 Rev C section 2.1 still says "roughly
twenty minutes of assembly labour" and is wrong by the same margin**; it is corrected at the
next revision of that document. Either way the point it was making stands -- a hand-built
jumper set per unit is the accepted cost of the module architecture, and it is the largest
avoidable cost in stage 2.

**JMP-11, the adapter jumper.** This is the worked example of why the jumper exists.

| Carrier way | Net | Module pin (Adafruit 4314) |
|---|---|---|
| J11.1 | DVDD3V3 | VIN |
| J11.2 | DGND | GND |
| J11.3 | SDA | SDA |
| J11.4 | SCL | SCL |
| -- | -- | 3Vo -- **not mated** |

A four-way socket serves a five-way module in a different pin order, with no board change.

**JMP-12, the Y jumper.** Built only when the charger and the gauge are two separate boards.
With the combined assembly of section 2.6 fitted, JMP-12 is a straight eight-way jumper to
one module header and the branch columns below are read as one connector.

| Trunk way | Net | Charger branch | Gauge branch |
|---|---|---|---|
| 1 | VBAT | BAT | cell sense |
| 2 | DGND | GND | GND |
| 3 | VBUS_CHG | VBUS | -- |
| 4 | CHG_CE | CE | -- |
| 5 | SDA | -- | SDA |
| 6 | SCL | -- | SCL |
| 7 | VSYS | SYS | -- |
| 8 | NC_CHG_STAT | STAT (optional) | -- |

Charger branch: six ways (1, 2, 3, 4, 7, 8). Gauge branch: four ways (1, 2, 5, 6). Ways 1
and 2 are common and are made as a single crimp with two conductors, or as two crimps in
adjacent positions bridged inside the trunk connector.

### 3.4 Male headers on the modules

The carrier presents female sockets; the modules must present male pins for the jumper's
female end. Several breakouts ship with their header strips loose in the bag.

| Module | Header status | Strip needed |
|---|---|---|
| ESP32-S3-DevKitC-1-N16R8 | fitted by Espressif -- confirm the variant ordered | none |
| PIEEG-8 / ADS1299 breakout x2 | confirm part by part at incoming inspection | 1x12, 1x10, 1x6 each |
| codec module | usually loose | 1x14 (or the module's own count) |
| isolator module | usually fitted | 1x4 |
| ATECC608B breakout | loose | 1x5 |
| charger module | loose | 1x6, or 1x8 for a combined charger-plus-gauge board |
| fuel gauge module | loose | 1x4, none if combined with the charger |
| microSD breakout | loose | 1x8 |
| boom preamplifier | loose | 1x6 |
| 74HC595 module | loose | 1x16 |
| room microphone module | confirm | 1x4 |

Stock: 2.54 mm break-away male header, gold flash over nickel, 1x40 strip -- six strips per
unit with attrition. Fitted from the component side, soldered on the underside, body flush,
perpendicular within 2 degrees. Use the carrier's own socket as the alignment fixture. These
lines belong in the kit BOM under "Module interface hardware"; package v1 had none of them.

---

## 4. The module plate MP-01

MP-01 is a flat non-conductive plate that sits above the carrier on four standoffs and carries
every purchased module except the DevKit. It exists because module header geometry is not
fixed by any public standard: nothing tells the programme where a PIEEG-8, an ES8388 breakout
or a bq24074 board puts its pins, or how many ways it has, and a socket placed on the carrier
to match a guessed geometry is a board respin when the guess is wrong. Moving the modules to a
plate makes the variable a jumper and not a PCB.

Every figure below is generated by `tools/mech_gen.py`, which governs, and RUL-EEG-021
section A transcribes the same set.

| Property | Value |
|---|---|
| Material | MJF PA12, natural, **no conductive filler and no metal insert** |
| Size | **146.0 x 126.0 x 3.0 mm**, 2 mm inside the 150.0 x 130.0 mm carrier outline on every edge, corners filleted R4 |
| Board fixing | four Ø3.4 mm holes on the carrier MH1-MH4 pattern, at (5, 5), (145, 5), (5, 125) and (145, 125) |
| Standoff, carrier to plate | **M3 x 18 mm nylon hex, female-female, four off** (Würth 970200321 class), with **eight** M3 x 6 mm nylon pan screws, four up into the plate and four down into the carrier bosses |
| Jumper slots | a field of slots **12 mm long by 3 mm wide** on a **16 x 7 mm grid**, inside an **8 mm solid border**, deburred; the jumpers drop through the nearest slot to their socket. `mech_gen.py` cuts each slot with `slot2D(12.0, 3.0, 0)`, so **12 x 3 mm is the size of one slot and is not a count of slots**; the plate does not carry twelve of them |
| Module fixing | **Ø2.7 mm M2.5 clearance holes between the slot rows**, on the same 16 mm column pitch, offset 8 mm in X and 3.5 mm in Y from the slot centres |
| Module standoff | M2.5 x 6 mm nylon female-female with M2.5 x 5 mm nylon screws; M3 where the module's holes are 3.2 mm |
| DevKit opening | one **31 x 61 mm** opening over J6/J7, spanning x = 78 to 109 mm and y = 4 to 65 mm in carrier coordinates |
| Above the isolation barrier | solid plate; the slot field stops at x = 140 mm and no material is removed over the barrier |
| Retention | two adhesive cable-tie mounts per module group |

The slot-and-hole field is the answer to the geometry problem. No module's hole pattern is
known in advance, so the plate is not drilled to a pattern; any module whose holes fall on or
near the M2.5 grid picks up at least two fixings, and one that does not is held by a tie mount
and a strip of foam tape. This is deliberately crude and it is honest: it takes a per-unit
fitting decision rather than a per-module drawing revision.

**Stack budget, calculated, not measured**

| Element | mm | Running total |
|---|---|---|
| POD-P1 floor | 2.5 | 2.5 |
| Carrier boss on the internal floor | 6.0 | 8.5 |
| Carrier PCB | 1.6 | 10.1 |
| Carrier top to plate underside (M3 x 18 standoff) | 18.0 | 28.1 |
| MP-01 | 3.0 | 31.1 |
| Modules above the plate, PCB plus tallest component | <= 18.0 | **49.1** |
| POD-P1 internal depth | 55.5 | -- |
| **Margin** | **6.4** | -- |

That margin is real and it comes from the enclosure growing with the board: POD-P1 is now
163.0 x 143.0 x 58.0 mm external and 158.0 x 138.0 x 55.5 mm internal. The Rev A figures
(a 130 x 124 mm plate in a 142 x 136 x 44 mm pod, margin 0.4 mm) are withdrawn. The 18.0 mm
ceiling on module height is a limit on what may be fitted to MP-01, and it is checked at
step 9 of section 6 for every module type.

Under the plate, the DevKit occupies 8.5 mm of socket mating height plus a 1.6 mm PCB plus
about 3.5 mm of components -- **13.6 mm** *(calculated)*, leaving 4.4 mm of the 18 mm for
jumper bends. The DevKit stands in the 31 x 61 mm opening, so **its USB-C ports and its boot
and reset buttons are reachable with the plate fitted**; that is the flashing and recovery
route of section 1.2. Every jumper is nonetheless long enough to allow the plate to be lifted
and laid beside the carrier without unplugging anything.

**No metal above the analogue zone.** MP-01 is non-conductive and carries no earthed plate,
no metal standoffs and no metal screws left of **x = 62 mm**, the zone split. A conductive
plate 18 mm above sixteen high-impedance electrode nodes is a capacitive coupling path to
whatever it is tied to, and this design has no earth to tie it to.

---

## 5. The ESP32-S3-DevKitC-1 exception

The DevKit's geometry is public, so it is inserted **directly** into J6 and J7. There is no
jumper. Row spacing is **22.86 mm (0.900 in)**, the DevKitC-1 header dimension; Rev A had
22.0 mm and the board would not have accepted the module (ECO-EEG-008).

J6 and J7 carry **header positions, not GPIO numbers**. The table below is the reconciliation
between the two. It is the one home of the GPIO map -- DESIGN_FACTS and FW-EEG-001 cite this
section rather than transcribing it -- and it is the source from which
`firmware/main/board_pins.h` is generated so that the firmware and the board cannot drift.

**J6 -- DevKitC-1 row A (left header, pin 1 at the USB end)**

| Way | DevKit label | GPIO | Carrier net | Dir | Note |
|---|---|---|---|---|---|
| 1 | 3V3 | -- | DVDD3V3 | out | LDO output, see budget below |
| 2 | 3V3 | -- | DVDD3V3 | out | second conductor |
| 3 | RST | -- | RESET_EN | -- | to J26.5 only |
| 4 | IO4 | 4 | BTN_A | in | R50 pull-up, C50 debounce |
| 5 | IO5 | 5 | BTN_B | in | R51, C51 |
| 6 | IO6 | 6 | BTN_STOP | in | R52, C52 |
| 7 | IO7 | 7 | I2S_DIN | in | codec ADC data |
| 8 | IO15 | 15 | START | out | both converters |
| 9 | IO16 | 16 | RESET | out | both converters |
| 10 | IO17 | 17 | I2S_MCLK | out | |
| 11 | IO18 | 18 | I2S_BCLK | out | |
| 12 | IO8 | 8 | I2S_LRCK | out | |
| 13 | IO3 | 3 | ENV_CMP | in | **strapping pin** (JTAG source select); see 5.2 and ECO-EEG-023 |
| 14 | IO46 | 46 | VBUS_DET | in | **strapping pin**; 3.00 V at VBUS = 5 V with R85 at 150 kOhm |
| 15 | IO9 | 9 | I2S_DOUT | out | codec DAC data |
| 16 | IO10 | 10 | CS | out | |
| 17 | IO11 | 11 | MOSI | out | |
| 18 | IO12 | 12 | SCLK | out | |
| 19 | IO13 | 13 | MISO | in | |
| 20 | IO14 | 14 | DRDY | in | interrupt; the sample counter is incremented here and nowhere else |
| 21 | 5V | -- | V5V | in | DevKit supply from the buck-boost |
| 22 | GND | -- | DGND | -- | |

**J7 -- DevKitC-1 row B (right header)**

| Way | DevKit label | GPIO | Carrier net | Dir | Note |
|---|---|---|---|---|---|
| 1 | GND | -- | DGND | -- | |
| 2 | TXD0 | 43 | UART_TX | out | console, to J26.3 |
| 3 | RXD0 | 44 | UART_RX | in | console, to J26.4 |
| 4 | IO1 | 1 | SDA | bidir | shared I2C, pulled up by R94 (4k7) |
| 5 | IO2 | 2 | SCL | out | shared I2C, pulled up by R95 (4k7) |
| 6 | IO42 | 42 | LED_SR_CLK | out | |
| 7 | IO41 | 41 | LED_SR_DATA | out | |
| 8 | IO40 | 40 | SD_D0 | bidir | |
| 9 | IO39 | 39 | SD_CLK | out | |
| 10 | IO38 | 38 | SD_CMD | bidir | |
| 11 | IO37 | 37 | NC_GPIO37 | -- | **NOT CONNECTED -- octal PSRAM** |
| 12 | IO36 | 36 | NC_GPIO36 | -- | **NOT CONNECTED -- octal PSRAM** |
| 13 | IO35 | 35 | NC_GPIO35 | -- | **NOT CONNECTED -- octal PSRAM** |
| 14 | IO0 | 0 | LED_SR_LATCH | out | **strapping pin**, pulled up on the DevKit |
| 15 | IO45 | 45 | NC_GPIO45 | -- | **NOT CONNECTED -- VDD_SPI strapping pin** |
| 16 | IO48 | 48 | LED_PWM / LED_V | out | input at reset: nothing lights at boot |
| 17 | IO47 | 47 | CHG_CE | out | charge interlock (S-01) |
| 18 | IO21 | 21 | MIC_MUTE | out | mute-not, see 2.10 |
| 19 | IO20 | 20 | USB_DP | bidir | native USB |
| 20 | IO19 | 19 | USB_DN | bidir | native USB |
| 21 | GND | -- | DGND | -- | |
| 22 | GND | -- | DGND | -- | |

### 5.1 The GPIO35/36/37/45 prohibition

On the **-N16R8** variant, GPIO35, 36 and 37 carry the **octal PSRAM**. Rev A put
LED_SR_DATA, LED_SR_CLK and LED_SR_LATCH on them; the firmware pin map was unbuildable and
the shift register would have fought the memory bus. ECO-EEG-009 moved them to GPIO41, 42
and 0 and left J7 ways 11, 12 and 13 open. GPIO45 is the VDD_SPI strapping pin and way 15 is
also left open. **These four ways carry no carrier copper and no jumper. Nothing may be
connected to them by any substitution, rework or field modification.** The four nets exist in
the netlist as named single-pad no-connects so that an ERC run reports them as deliberate.

Because four-bit SDMMC is what those lines would have carried, the microSD interface is
**one-bit**. The stream needs 50.7 kB/s of payload at 1000 Hz and about 2 MB/s is available
*(calculated)*, so the trade costs nothing measurable and buys the contact lights.

### 5.2 Strapping pins at boot

| Pin | Way | Function on the carrier | Boot behaviour |
|---|---|---|---|
| GPIO0 | J7.14 | shift-register latch (RCLK) | pulled up on the DevKit; the 595's RCLK is a high-impedance input, so the strap is not loaded. Pressing BOOT clocks one latch edge, which is harmless because LED_V floats |
| GPIO3 | J6.13 | comparator output in | JTAG source select. Driven through R83 (10 kOhm) and clamped by D23; a static level either way boots normally |
| GPIO45 | J7.15 | -- | open, strap left at its DevKit default |
| GPIO46 | J6.14 | charge-present detect | R84 (100 kOhm) / R85 (150 kOhm) divider gives 5 x 150/250 = **3.00 V** at VBUS = 5 V, above the 2.48 V V_IH, so the first S-01 interlock asserts (ECO-EEG-022) |
| GPIO48 | J7.16 | contact-light common | input at reset, so **no light can be lit at boot whatever the shift register contains** (E-27) |

**ENV_CMP now arrives from a 3.3 V comparator (ECO-EEG-023).** U7 is powered from DVDD3V3 and
DGND rather than AVDD and AVSS, so CMP_RAW swings 0 to 3.3 V into GPIO3 with full margin and
the D23 clamp becomes a belt-and-braces part rather than the only thing between +/-2.5 V and a
3.3 V pin. Because AGND_REF sits 2.5 V above DGND, the comparator's inputs are re-referenced
to a DVDD3V3/2 divider and the envelope is AC-coupled into it. **This change is recorded in
ECO-EEG-016 and is not yet in `design.py`, which at Rev B still shows U7 on AVDD/AVSS with its
threshold divider referred to AGND_REF. It changes an analogue-to-digital crossing in the
patient-connected part of the design and the safety and layout reviewer must check it before
it is cut into the board.**

### 5.3 DVDD3V3 comes from the DevKit

There is no 3.3 V regulator on the carrier. DVDD3V3 is the DevKit's own LDO output, taken back
onto the board at J6.1 and J6.2, and it feeds every 3.3 V load in the design.

| Load | Recording, typical (mA) | Worst case simultaneous (mA) |
|---|---|---|
| ADS module #1 digital | 10 | 10 |
| ADS module #2 digital | 10 | 10 |
| codec module, digital and analogue | 25 | 25 |
| secure element | 0, idle between sessions | 3 peak |
| 74HC595 plus eight lights at 1.3 mA | 12 | 12 |
| microSD breakout | 5 between write bursts | 100 peak, during write |
| boom preamplifier | 3 | 3 |
| room microphone module | 5 | 5 |
| isolator device side (VDD_ISO through L1) | 20 | 20 |
| ESP32-S3 itself, radio off | 100 | 100 |
| **Total on DVDD3V3** | **about 190** | **about 288** |

U7's 40 uA moves onto this rail **when** ECO-EEG-023 is cut into `design.py`, which has not
happened: at Rev B U7 is still on AVDD and AVSS (section 5.2), so the 40 uA is not on DVDD3V3
yet. It is inside the rounding of the table either way, so no figure in the table moves when
the ECO lands. The worst-case column is the 288 mA figure the rest of the package quotes,
including TST-EEG-004 T3's note and RUL-EEG-021 section B. Both columns also appear on V5V, because the LDO passes
them: section 2.7 carries the 5 V budget and the current at J13 that follows from it, and the
two tables are one calculation.

**The carrier assumes the DevKit's 3V3 pin will supply 350 mA continuous, and that assumption
has not been verified.** At 288 mA the on-board LDO drops 5.0 - 3.3 = 1.7 V and dissipates
about **0.5 W** *(calculated)* in a small package inside a closed pod. **This is not solved.**
Phase 1 measures it at TST-EEG-004 T3: run the unit at full load, measure DVDD3V3 at TP12,
which must stay at or above 3.20 V, and report the regulator's case temperature. If the case
exceeds 85 C, a 3.3 V regulator on the carrier fed from V5V is an ECO against Rev C. It is
never a field modification.

---

## 6. Qualifying a substitute module

Run this before a module type not already in AVL-EEG-017 is fitted to any unit. Record on form
QF-EEG-006-01. Steps 1 to 9 are all performed on the bench, on one sample, before the module
touches a carrier.

| # | Step | Acceptance |
|---|---|---|
| 1 | Obtain the module's schematic and a dimensioned drawing. Confirm the licence permits publishing its pinout, since this package is CC BY-SA. | both obtained |
| 2 | Measure header pitch, way count, pin length, pin 1 position and marking. | 2.54 +/- 0.10 mm; pin 1 identifiable with the module fitted |
| 3 | With the module unpowered, ring out every header pin to its device pin. Write the result into the section 2 table for that module. | every way accounted for, including no-connects |
| 4 | Confirm the module's supply range includes the carrier rail it is fed. Measure quiescent current at that rail. | inside the budget of 2.7 or 5.3 |
| 5 | Measure any on-module regulator output with the carrier rail applied. | recorded; drives the section 7 decisions |
| 6 | For every module output that reaches an ESP32-S3 GPIO, measure V_OH and V_OL under the real load. | V_OH >= 2.48 V, V_OL <= 0.83 V (0.75 and 0.25 x 3.3 V) |
| 7 | For an I2C module, measure its own pull-up to its own VDD, in parallel with the carrier's R94/R95 pair (4k7 each, 2.35 kOhm combined). | recorded; the parallel total must stay above 1.1 kOhm, so that the bus still pulls to <= 0.4 V within the ESP32-S3's 3 mA sink *(calculated)*. If it does not, remove the module's own pull-up |
| 8 | For a module on an electrode net, measure leakage from the input pin to any supply at 2.5 V bias. | <= 10 nA, which develops <= 0.7 uV across the **68 kOhm** series resistor fitted since ECO-EEG-024 was applied on 2026-09-02 (it was <= 0.5 uV across the 47 kOhm this step used to name as fitted) |
| 9 | Measure height above MP-01 and check the hole pattern picks up at least two M2.5 grid holes. | <= 18.0 mm above the plate, inside the section 4 stack budget |
| 10 | Build the jumper and its WH-KEY-01 shroud, fit, and run TST-EEG-004 in full on one unit. | all steps pass |

**Sign-off.** Phases 1 and 2: the programme's build engineer signs QF-EEG-006-01 and the entry
is added to AVL-EEG-017 with an ECO against the affected jumper. Phase 3: the contract
manufacturer's engineer signs and the programme countersigns. **No substitution is permitted
for the ESP32-S3-DevKitC-1-N16R8 (E-18) or the ADuM4160 isolator (E-24).** A substitution
touching the charger, the cell or the isolator additionally requires the electrical safety
review that is still outstanding.

### 6.1 Keying: the socket families and the WH-KEY-01 shroud

The carrier's socket strips repeat: J6 and J7 are both 1x22; J1 and J3 are both 1x12; J2 and
J4 are both 1x10; **J21, J23, J25, J26 and J29 are all 1x6**; **J5, J9, J10, J11, J18, J27 and
J28 are all 1x4**. Without a physical key, a 1x4 jumper fits a foreign 1x4 socket and a
reversed DevKit across J6 and J7 puts DVDD3V3 onto DGND.

The key is the printed shroud. **WH-KEY-01 is fitted over every socket that takes a ribbon
jumper**, which is the seventeen module connectors:

| Family | Sockets carrying a WH-KEY-01 shroud |
|---|---|
| 1x16 | J19 |
| 1x14 | J8 |
| 1x12 | J1, J3 |
| 1x10 | J2, J4 |
| 1x8 | J12, J20 |
| 1x6 | J21, J23, J25, J29 |
| 1x4 | J5, J9, J10, J11, J28 |

Each shroud is printed with the socket designator raised on its outer face and is polarised so
that a jumper made for a different socket of the same way count will not enter. The three
harness sockets **J14, J22 and J30** take the same shroud at the carrier end, specified with
the cables in WH-EEG-008 section 6. The SHR-14-A, SHR-30-A and SHR-22-A names of
JIG-EEG-009 Rev A are withdrawn: JIG-EEG-009 Rev B calls all three WH-KEY-01.
**J26 (debug), J18 and
J27 (panel pigtails), J13 and J24 (JST PH, keyed by the connector itself) and J6/J7 (the
DevKit, which is keyed by its own 22-way-by-22.86 mm geometry) carry no shroud** and rely on
marking and way count.

Three procedural defences stand behind the shroud and are not withdrawn:

1. **Way 1 is the red stripe** on every jumper, and way 1 of every socket is the square pad
   with a silkscreen triangle placed outside the socket body so it survives insertion.
2. **Every jumper end carries a printed sleeve** naming both the jumper and the connector.
3. **Where a socket has an NC way** -- J3.6, J4.10, J12.8, J19.16, J21.5, J25.6, J26.6,
   J27.4 and J7.11/12/13/15 -- that way is a second key: clip the pin from the jumper's
   carrier end and plug the socket way with a length of 0.6 mm nylon rod.

The second operator check of ASM-EEG-007 before first power-up remains the last defence.

---

## 7. Two build decisions and the measurements that settle them

This section is the only home of the R92/R93 and R89 decisions. Documents that need them cite
**ICD-EEG-006 section 7.1** and **section 7.2**. ASM-EEG-007, WH-EEG-008 and ECO-EEG-016 once
cited "section 4" and "section 5"; all three now cite 7.1 and 7.2 and that correction is
made.

### 7.1 R92 and R93 -- module #2's analogue rails

R92 links AVDD2 to AVDD; R93 links AVSS2 to AVSS. Both are 0 Ohm 0603 and both are **fitted by
default**, which parallels module #2's analogue rails onto module #1's regulators
(ECO-EEG-011). Removing them lets module #2 run on its own regulators.

**Measurement.** Fit both modules to MP-01. Fit JMP-01, JMP-03, JMP-23 and JMP-25, but **do
not fit JMP-29**. Power the carrier from the cell. Measure at module #2's own AVDD and AVSS
header pins, referred to AGND_REF at TP13.

| Reading at module #2 | Decision | Then |
|---|---|---|
| AVDD and AVSS both within +/-100 mV of 0 V | module #2 does not regulate | **fit R92 and R93**; mate JMP-29 with all six ways |
| module #2 produces +/-2.5 V and \|AVDD1 - AVDD2\| <= 25 mV and \|AVSS1 - AVSS2\| <= 25 mV | either is acceptable | keep R92 and R93 fitted; one rail pair, one clamp reference |
| module #2 produces +/-2.5 V and either difference > 25 mV | the two regulators would fight | **remove R92 and R93**; mate JMP-29 ways 3 and 4 only, and leave ways 1, 2, 5 and 6 unmated |

The third case carries a consequence that must be written on the build record: D12-D16 clamp
the EMG and EOG inputs to **module #1's** AVDD and AVSS. With R92 and R93 removed, the clamp
reference and module #2's supply are different nodes and can differ by the sum of two
regulator tolerances. That difference must stay below 100 mV, measured at TP10 and TP11
against module #2's rails, or the clamps sit outside module #2's input range under fault.
If it exceeds 100 mV, the only acceptable outcome is to disable module #2's regulators and go
back to case one. **There is no numbered production step for that measurement in
TST-EEG-004 Rev C.** It is taken at first power-up under this section, recorded on the build
record and signed, and the absence of a T-number for a check with a safety consequence is
carried as an open item in section 8 rather than fixed by inventing a step number here.

Signed off by the build engineer on QF-EEG-006-01. AGND_REF (J23.4 and J29.4) stays mated in
every case; it is the reference every electrode is measured against and it is never a decision.

### 7.2 R89 -- electret bias for the boom capsule

R89 is 2 kOhm2 1 % between DVDD3V3 and VOICE_RAW and is **DO NOT POPULATE** by default. It is
fitted only if the boom preamplifier module does not supply its own microphone bias. C90
(10 uF) decouples the 3.3 V feed at that point and is fitted either way.

**Measurement.** Fit the preamplifier module to MP-01 and JMP-21 to J21. Leave J18 unmated, so
the capsule is disconnected. Power the carrier. Measure the DC voltage at J21.4 (VOICE_RAW)
with a meter of >= 10 MOhm input impedance, referred to DGND.

| Reading at J21.4 | Meaning | Decision |
|---|---|---|
| >= 1.0 V DC | the module biases its own microphone input | **leave R89 unpopulated** |
| <= 0.1 V DC | no bias present | **fit R89** |
| between 0.1 and 1.0 V | indeterminate | do not guess: obtain the module schematic and settle it there |

Fitting R89 when the module already biases puts two sources on one node. The capsule's DC
operating point then sits wrong, the FET clips asymmetrically, and the fault shows up as a
distorted VOICE envelope at TST-EEG-004 T12 rather than as anything obviously electrical.
Recording the reading is as important as taking the decision. Because the preamplifier part
itself is not settled (section 2.9), this measurement is repeated for every candidate module.

With R89 fitted, bias current into a standard electret is (3.3 - 1.5) / 2200 = **0.82 mA**
*(calculated)*, which is inside the 0.5 to 1.0 mA that most 6 mm capsules want.

---

## 8. Open points

Six Rev A open points are closed in this revision and are listed first so that nobody carries
them forward: **I2C pull-ups** (R94 and R95, 4k7 each, ECO-EEG-021), **VBUS_DET** (R85 to
150 kOhm, 3.00 V, ECO-EEG-022), **keying** (WH-KEY-01 and the module-end shrouded IDC,
section 6.1), **E-04** (restated at -80 dB on the carrier, ECO-EEG-026), **E-11** (C20/C40/C60
to 10 uF, 1.6 Hz, requirement restated at <= 2 Hz, ECO-EEG-027) and **E-28** (RFQ-EEG-001 Rev E asks for
TP1-TP18 plus the 1x6 header at J26; the 2x5 JTAG header is withdrawn and there is no
deviation to record).

What is still open:

| # | Point | Evidence | What would close it |
|---|---|---|---|
| 1 | **No safety engineer has reviewed this design**, and nothing in it has been built or measured | -- | the safety review. It blocks use on a person; it does not block fabrication or quoting |
| 2 | **J15-J17 have no confirmed part.** Staubli SLB1,5-F / LB-I1,5 is a class of touch-proof socket, not a qualified PCB part, on a Class A patient-contact position | section 1; AVL-EEG-017 | source a touch-proof 1.5 mm socket with a PCB signal pin and two 1.5 mm posts, and first-article it before Phase 2. AVL carries a 12-week lead-time risk |
| 3 | **The boom preamplifier part is not settled.** The MAX9814 is not approved because its AGC cannot be assumed disablable; the module is specified by interface only | section 2.9; AVL-EEG-017 | buy and measure a fixed-gain candidate (MAX4466 class), then add it to AVL-EEG-017 through section 6 |
| 4 | **The isolator's host connector is USB-B where E-24 asks for USB-C.** Live non-conformance with an interim answer (WH-09 pigtail), not a settled interface | section 2.4 | qualify an isolator module with a USB-C host receptacle, or amend E-24 |
| 5 | **Nothing in this design measures cell temperature.** There is no NTC net and no thermistor way on J12 or J13, so **S-04's thermistor-monitored charging is not met and E-23's 45 C inhibit is not met and cannot be tested**. What the module supplies is the charger IC's own thermal regulation, which regulates its die and not the cell | `design.py` netlist; TST-EEG-004 T4 and section 10; RFQ-EEG-001 Rev E E-23 and S-04 | a carrier change at Rev C, or an accepted deviation. No module fitted to J12 can close it |
| 6 | **Corrected 2026-09-02: S-02 single-fault DC is 36.8 uA against a 50 uA limit, and the limit is met on the calculation.** This item read "53.2 uA … not met at the fitted 47 kOhm, and it is the one open item of the production simulation SIM-EEG-018". What is still open is the sign-off: **SR-01 is closed in the design and has not been reviewed**, which is how SIM-EEG-018 Rev A now carries it among its six open items, and nothing has been measured | RISK-EEG-011 section 4, which still prints the 47 kOhm arithmetic as live; SIM-EEG-018 Rev A | ECO-EEG-024 is **applied**: R1-R16 are 68 kOhm. **E-10 is on its +/-1.0 dB branch**, which the requirement provides for this case. The safety reviewer's disposition of SR-01, and the T23 measurement on a unit that does not yet exist, close it |
| 7 | **ECO-EEG-023 (ENV_CMP re-reference) is not yet in `design.py`** and touches an analogue-to-digital crossing in the patient-connected part | section 5.2 | the safety and layout reviewer signs it, then it is cut into `design.py` at Rev C |
| 8 | **The DevKit 3V3 rail is assumed, not measured.** 288 mA calculated against an assumed 350 mA, about 0.5 W in the LDO inside a closed pod | section 5.3 | TST-EEG-004 T3 at full load: TP12 >= 3.20 V and the LDO case temperature reported. Above 85 C, a carrier regulator is an ECO against Rev C |
| 9 | **The R92/R93 case-three consequence has no numbered test step.** A build-time decision with a safety consequence, taken under section 7.1 | section 7.1 | a step in TST-EEG-004, which owns the step numbers. This document does not number one |
| 10 | **The EOG panel sockets are a Phase 2 option with no part number.** J22 and both channels exist and are protected; the panel sockets, their cable and their drawing do not | section 1; PARTS-EEG-019 | a part, a cable and a drawing, if the option is taken |
| 11 | **Corrected 2026-09-02: the contact-light bicolour phase driver is written**, and this item read "not implemented in firmware … `lights_write()` and `lights_task()` are on/off only". The carrier interface was and is complete. Two things are still open: **T11 has not been run**, because no unit exists, and the impedance boundaries between green, amber and red are not established. *Corrected again the same day (FW-D17): this item read that the build enabled `LOFF_SENSP` only so the red state could not appear, and asked for `LOFF_SENSN` to be enabled. Red is reachable now, and `LOFF_SENSN` was never the answer -- the montage is single-ended, so the N half has no per-site electrode. The driver sweeps the positive-side comparator threshold instead, and what is unknown is where the two trip points actually fall* | section 2.11; FW-EEG-001 | a unit to run T11 on, and the two `COMP_TH` values characterised so the colour boundaries are known |
| 12 | **Stack margin is 6.4 mm, calculated.** Comfortable, but every figure in it is a drawing dimension and not a measurement | section 4 | measure the real stack on the first article before any quantity of MP-01 is printed |
| 13 | **The rail budgets of sections 2.7 and 5.3 and TST-EEG-004 T3's current limit disagree.** About 300 mA on V5V typical implies about 440 mA at J13 while recording; T3 limits the recording current at J13 to 150 mA | sections 2.7 and 5.3, both calculated; TST-EEG-004 T3 | the first article: measure idle and recording current at J13 and the five rails, then TST-EEG-004, which owns the step and its limit, sets a limit that matches the measurement. This document does not restate T3 |
| 15 | **J28 is counted twice across the package.** Section 3.3 lists it as JMP-28 and WH-EEG-008 section 3.5 lists the same socket as WH-05's carrier end. They are one connector on one socket, and only WH-05 is built, because the room-microphone module is bonded to the pod wall and not fitted to MP-01. The schedule above still says seventeen jumpers and 134 carrier ways | section 3.3; WH-EEG-008 section 3.5 and section 3.9; AVL-EEG-017 section 1.6.1, which counts the housing once | an ECO that deletes JMP-28 from this schedule and restates the count as sixteen jumpers and 130 ways, together with the labour figures ASM-EEG-007 section 8 and DSN-EEG-003 section 2.1 derive from it |
| 14 | **The routing has not been reviewed by a human layout engineer.** The DRC is clean -- zero violations, all 145 nets connected, both inner planes continuous -- but it was produced by the programme's own tools, and it closes at minimum geometry: 169 connections were relaxed, 36 below the 0.25 mm preferred width and 133 at full width with a reduced gap, all at or above the 0.20 mm minimum | `kicad/EEG-CAR-01_RevB_DRC_report.txt` | the layout review under RFQ-EEG-002A. Until it happens the data is released for review only, not for fabrication |

---

## 9. Verification and sign-off

| Interface | Verified by | When | Signed |
|---|---|---|---|
| Every jumper way, carrier to module | continuity to the tables of sections 1 and 3, 100 % | after jumper build, before first power-up | build operator, checked by a second operator |
| WH-KEY-01 shroud fitted and correct | visual, against the section 6.1 table | at final assembly | build operator |
| J6/J7 to GPIO map | `firmware/main/board_pins.h` generated from section 5 and diffed against it at every build | at every firmware build | automatic; failure breaks the build |
| Module identity and pinout | QF-EEG-006-01, section 6 | before a new module type is fitted | build engineer (Phases 1-2), CM engineer countersigned (Phase 3) |
| R92 / R93 | section 7.1 measurement recorded on the build record | at first power-up of each unit | build engineer |
| R89 | section 7.2 measurement recorded on the build record | at first power-up of each unit | build engineer |
| DVDD3V3 budget | TST-EEG-004 T3: TP12 at full load, >= 3.20 V, with the LDO case temperature reported | first article of each phase | build engineer |
| Isolation keep-out and jumper routing | visual, against section 2.4 and DSN-EEG-003 section 3.3, on all four layers | at every unit's final assembly | build operator; safety review at the outstanding gate |

Nothing in this document has been manufactured or measured, and no safety engineer has
reviewed this design. Every figure marked *calculated* is exactly that, and the first article
is where they stop being calculations.
