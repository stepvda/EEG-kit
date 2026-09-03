# TEST FIXTURE DESIGN

**Document:** JIG-EEG-009  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs. Step numbers are owned by
TST-EEG-004 Rev C and are never invented here.

## Why this document exists

DSN-EEG-003 Rev A.2 described the whole production test fixture in one sentence: "a
16-channel resistor-divider and reference-resistor fixture on a 1x22 socket mating J14, a
3-way DIN plug set for EMG, and a host PC running the open test tool." Nine of the eighteen
steps of the package v1 test flow depended on that sentence, RFQ-EEG-001 section 10 asks bidders to
price "Stencil, fixtures, test jig (one-off)" against it, and the fourteen-agent audit of
package v1 recorded it as blocking three separate ways: the fixture had no design, the 1000:1
divider had no accuracy budget, and the analogue reference the noise test is measured against
was not on the connector the fixture mates with. TST-EEG-004 Rev C now has thirty-one steps,
T00, T0 and T1 to T29; fourteen of them name a lettered fixture sub-assembly and three more --
T19, T20 and T25 -- name fixture hardware that carries no letter. This document designs the
four fixtures that test flow needs, states the arithmetic behind the one limit that matters
most, and prices and schedules one set so a manufacturer can fill in that line.

**No hardware in this package has been built or measured, and no safety engineer has reviewed
this design** (DESIGN_FACTS section 8, item 1). Every figure marked *calculated* is
calculated. *Corrected 2026-09-02 from "Nothing in this package has been built or measured":
the ESP32-S3 firmware is now built -- ESP-IDF v5.2.5, images and SHA-256 manifest in
`firmware/release/` -- and has run only under QEMU emulation. **No fixture has been built**,
and no RP2040 image for M1 or M2 exists (section 7).*

---

## 0. Scope and fixture register

| Fixture | Name | TST-EEG-004 Rev C steps served | Mates with |
|---|---|---|---|
| FIX-01 | Front-end injection, lead-off and contact-light fixture | T7a/b/c, T8, T9a, T9b, T10, T11, T22, T23 | J14, J30, J15-J17, J22 |
| FIX-02 | Audio loopback and onset fixture | T12a, T12b, T12c, T12d, T13, T17, and T28 once per lot | 3.5 mm jack at J27, boom capsule, room port, J22 |
| FIX-03 | Flashing and provisioning fixture | the flashing and provisioning operation that precedes T5b, then T6, T16 and T25 | DevKitC-1 UART USB-C port, J26 |
| FIX-04 | Harness, current-shunt and isolation-barrier fixture | T00 (module bench currents), T3, T4, T20, T21, T23, and the WH-EEG-008 section 9 harness acceptance | 12-way and 10-way harness ends, J13 and J24, ADuM4160 host USB-C, the applied-part group |

Instruments are not fixtures and are not designed here. The set assumes a 6.5-digit DMM with
4-wire ohms, a function generator, a 100 MHz oscilloscope, a 500 V DC insulation tester, a
bench supply with 0.1 mA current resolution and a host PC. It also assumes three instruments
that TST-EEG-004 section 5 requires and that no fixture in this document replaces: an **audio
analyser or calibrated interface** (level +/- 0.1 dB, residual THD+N <= 0.01 %, used at T17
and T28), a **contact thermometer or thermal camera** (+/- 2 degC, used at T3) and a **2.4 GHz
receiver or SDR with a near-field probe** (noise floor <= -90 dBm, used at T24). Section 6 says
which instruments must be bought specifically. The v1 audit's FXT-EEG-005 and FIX-EEG-010 are
superseded by FIX-01 and FIX-03 and recorded in ECO-EEG-016.

### 0.1 Fixture naming, and the mapping onto TST-EEG-004's part letters

Package v1 left two naming systems running side by side: TST-EEG-004 Rev B lettered the
fixture parts A to G, and this document numbered whole fixtures FIX-01 to FIX-04 while using
the word "Part" for something else entirely. A contract manufacturer reading both would have
built the wrong hardware. The naming is now **FIX-01 to FIX-04 with lettered sub-assemblies**,
**the table in TST-EEG-004 Rev C section 6.1 owns the letters**, and this document uses those
letters and no others. Where a piece of fixture hardware carries no letter there, it carries
none here either, and it is named by what it mates instead of being given a letter this
document invented.

This is the sub-assembly register. It is a **transcription of all seventeen rows of
TST-EEG-004 Rev C section 6.1** for the reader who has only this document in front of them,
not a second definition; where the two differ, TST-EEG-004 section 6.1 governs. An earlier
draft of this revision carried only twelve of the seventeen and moved three of the letters
onto different hardware; that is corrected here. The last column says where each row is built
in this document, or says plainly that it is not built here.

| Sub-assembly | Mates | Contents | Built in this document at |
|---|---|---|---|
| **FIX-01/A** | J14, 1x12, keyed, pin 1 marked E_Fz | eleven channel networks: 1000:1 tap, selectable **4k99 / 10k0 / 49k9** 0.1 % thin-film reference, short-to-common, open. Relay-switched, state readable by the host tool | J103; sections 1.2, 1.5 and 1.8 |
| **FIX-01/B** | J15, J16, J17 DIN 42802 1.5 mm, 12 mm pitch | three identical channel networks for EMG1 cheek, EMG2 submental, EMG3 laryngeal | J105; sections 1.2 and 1.8 |
| **FIX-01/C** | J22.2 (AGND_REF), second position TP13 | analogue reference lead, marked "ANALOGUE REFERENCE -- NOT DGND" | J106 pin 2; sections 1.2 and 1.8 |
| **FIX-01/D** | all eleven J14 analogue pins and SRB1 | common-mode injection network, one source into all inputs through matched 100 Ohm | section 1.11: LK1 opened, the fixture common driven 1 V RMS at 50 Hz from an isolated source, reaching the inputs through the matched RS1-RS16 100 Ω series resistors of section 1.8. It is a state of FIX-01, not a separate head, and section 1.11 is where it is specified |
| **FIX-01/E** | J30, 1x10 | TCS34725-class colorimeter head over the eight contact-light positions, reading the R/G ratio at each site | J104; sections 1.7 and 1.8 |
| **FIX-01/F** | the FIX-01 injection input, with a DMM tap | the 1000:1 ratio divider, two cascaded stages, 100:1 then 10:1, feeding FIX-01/A, FIX-01/B and FIX-01/G | section 1.3 and its accuracy budget; R101-R104, U1, U2 and the J102 monitor in section 1.8 |
| **FIX-01/G** | J22, 1x3 | spare-channel injection for EOGIN1 (J22.1) and EOGIN2 (J22.3) | J106; sections 1.2 and 1.8. An earlier draft of this revision called this head FIX-01/D |
| **FIX-02/A** | the boom capsule, windscreen removed | voice coupler, 2.0 cm3, delivering 70.0 dB SPL at 1 kHz at the capsule | section 2.2; BOM at 2.4 |
| **FIX-02/B** | the room-microphone port and its mesh | room coupler, 3.5 cm3, sealed over the port | section 2.2; BOM at 2.4 |
| **FIX-02/C** | the shipped headphone model | IEC 60318-1 artificial ear and the class 1 sound level meter mount | **Not built here.** It is in neither the section 2.4 bill of materials nor the section 6 cost tables, so the one-off price in section 6 is short by that coupler and that meter. Stated as an open item in section 7 (section 2.1) |
| **FIX-02/D** | J27 headphone pigtail, and a scope tap | 47.0 Ohm load and the electrical-onset marker | sections 2.1 and 2.3; RL201, RL202, U201, R201, R202 and the TRS plug in the 2.4 BOM. An earlier draft of this revision lettered it "FIX-02" |
| **FIX-03/A** | DevKitC-1 UART USB-C port, card reader, host PC | flashing and provisioning nest | section 3.3: the PA12 nest, the sprung right-angle USB-C pigtail, the barcode scanner and the powered hub |
| **FIX-03/B** | J26, 1x6 | console and recovery lead. **It cannot enter download mode**, because GPIO0 is LED_SR_LATCH | section 3.3: the six-pin P75-B1 pogo block on J26, used for console capture with the UART pigtail unplugged. Section 3.2 rule 1 governs -- the pigtail and the pogo block are never connected at the same time |
| **FIX-04/A** | J13 and J24 JST PH pigtails | two 1.000 Ohm 0.1 % shunts, one in the battery line and one in the charge line | section 4.1, and read at the FIX-01 shift start (section 1.12) |
| **FIX-04/B** | host-side USB shell, VBUS, D+ and D- on the ADuM4160 | insulation head that reaches the module without touching the carrier | sections 4.1 and 4.2 |
| **FIX-04/C** | applied-part group and protective earth | 100 kOhm 0.1 % measuring resistor, screened, and the earth lead | sections 4.1 and 4.3 |
| **FIX-04/D** | 12-way electrode end, 10-way light end, three EMG snap leads | harness continuity and pull heads | section 4.1: the 12-way electrode head, the 10-way light head and the EMG head, with the 24-channel scanner card that switches them. The limits are WH-EEG-008 section 9, steps H1 to H10 |

TST-EEG-004 Rev B's "Part A" to "Part G" map onto that register as follows, so that every
older step reference still resolves. This is TST-EEG-004 section 6.1's own mapping and is
copied, not derived.

| TST-EEG-004 Rev B part | Now |
|---|---|
| A | FIX-01/A |
| B | FIX-01/B |
| C | FIX-01/C |
| D | FIX-02/D |
| E | FIX-01/E |
| F | FIX-04/A |
| G | FIX-01/G |

Identifiers this document has used and now **withdraws**, listed so that a reader holding an
earlier draft can find where each thing went:

| Withdrawn | Replaced by |
|---|---|
| FIX-04/H-D, the barrier insulation head | **FIX-04/B** |
| H-A, H-B and H-C, the harness heads of section 4.1 | **FIX-04/D**, which TST-EEG-004 section 6.1 calls the harness continuity and pull heads. An earlier draft of this revision said that table gave the heads no letter; it gives them FIX-04/D, and the three heads keep their descriptive names inside it |
| CPL-V and CPL-R, the acoustic couplers | **FIX-02/A** and **FIX-02/B** |

Three designators an earlier draft of this revision moved are **reassigned, not withdrawn**,
because TST-EEG-004 section 6.1 carries all three: **FIX-01/F** is the 1000:1 divider of
section 1.3, and the 1.000 Ω shunt pigtails that draft lettered FIX-01/F are **FIX-04/A**
(section 4.1); **FIX-01/G** is the spare-channel head into J22, which that draft renamed
FIX-01/D; and **FIX-02/D** is the 47.0 Ω load and electrical-onset marker of section 2.1,
which that draft lettered plain "FIX-02". A reader holding the intermediate draft should read
its FIX-01/D as FIX-01/G throughout: in TST-EEG-004 section 6.1, FIX-01/D is the common-mode
injection network for T9b.

The SHR-14-A, SHR-30-A and SHR-22-A shroud identifiers used in Rev A of this document are
**withdrawn**; PARTS-EEG-019 records them as legacy. The keying part is now WH-KEY-01, and
section 1.10 says how the fixture uses it. The 100 kΩ measuring resistor of T23 was called an
instrument rather than a fixture in an earlier draft of this revision; TST-EEG-004
section 6.1 makes it
FIX-04/C, and section 4.3 now builds it as one.

### 0.2 What changed in the carrier, and what it means for the fixtures

Two carrier changes happened during layout, after package v1 was written, and both are
engineering findings rather than preferences. They reach this document through the FIX-03
nest, the FIX-01 head coordinates and the checks that depend on the reference planes.

**The carrier is 150.0 x 130.0 mm**, not the 130 x 124 mm of package v1. Thirty connectors,
211 parts and 156 nets would not close at the smaller size, and the extra 33.8 cm² of bare board
costs a few euro per unit against a real risk of an unroutable design.

**The carrier is a four-layer board:** L1 signal, L2 reference plane, L3 reference plane, L4
signal. Package v1 asserted that two layers would be enough and would be cheap and easy to
route. Actually doing the layout showed it is not: on two layers the bottom side has to be
both the reference plane and the second routing surface, and it cannot be both. Four layers
give two full routing surfaces and a continuous reference under every analogue trace, which is
what DSN-EEG-003's layout rules require and which a swiss-cheesed two-layer pour cannot
deliver. At two units the four-layer board costs about €35 more in total; at fifty units it is
about €3 per board.

| Property | Value |
|---|---|
| Outline | 150.0 x 130.0 mm, rectangular, no cut-outs |
| Layers | four: L1 signal, L2 reference plane, L3 reference plane, L4 signal |
| Stack-up | mask / 35 µm L1 / prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask = 1.60 mm ± 10 % |
| Reference planes | AGND_REF left of x = 62 mm, DGND right of it, on **both** L2 and L3, tied together by stitching vias |
| Vias | through vias only -- no blind, buried, back-drilled, filled or plugged -- 0.60 mm pad on a 0.30 mm finished hole |
| Mounting holes | M3, 3.2 mm NPTH at (5,5), (145,5), (5,125), (145,125), 6 mm copper keep-out |

The routing statistics for the four-layer board come from the DRC report at
`kicad/EEG-CAR-01_RevB_DRC_report.txt` and not from this document. EEG-CAR-01 Rev B is routed
on four layers with **3 745 track segments and 552 through vias**, and each reference plane is
one continuous island per net. **All 145 nets are fully connected**, none unclosed and none
without copper. Every rule passes: the smallest measured clearance is 0.260 mm on L1, 0.285 mm
on the planes and 0.275 mm on L4 against a 0.20 mm rule; the narrowest conductor is 0.20 mm and
the smallest plated hole is 0.30 mm; no copper comes within 2.00 mm of a non-plated hole; there
are no zone crossings; no digital net enters the analogue zone; and there is exactly one
AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND bridge. The report lists no isolation
keep-out violation and no via keep-out violation, so the isolation strip is copper-free on all
four layers, which is what item 4 below relies on and the reason it is stated as a checked
result rather than an assumption.

**The board closes: zero DRC violations.** The report's own line is "VIOLATIONS: 0 -- none.
The board passes every rule listed above." Zero violations, every net one connected copper
island and both inner planes continuous under the analogue zone are the three conditions
ECO-EEG-016 section 3 sets for releasing fabrication data, and all three are met, so **the data
is RELEASED FOR REVIEW under RFQ-EEG-002A**. It is **not released for fabrication**: that
awaits the review, because the routing was produced by the programme's own tools and **has not
been reviewed by a human layout engineer** (DESIGN_FACTS section 8, item 4). Nor does it close
comfortably. **169 connections are relaxed** -- 36 take a conductor narrower than the 0.25 mm
preferred width, and 133 keep full width and take a reduced gap -- all at or above the 0.20 mm
minimum conductor and the 0.20 mm minimum gap. A board that closes at minimum geometry is not
the same board as one that closes at preferred geometry, even when every rule passes, and the
fixtures are designed against a board nobody has yet fabricated or measured.

Consequences for the fixtures, and they are the reason this section is here rather than in an
annex:

1. The FIX-03 nest is dimensioned to 150.0 x 130.0 mm on the four M3 holes above. A nest cut
   for the v1 outline will not accept a Rev B carrier.
2. Every head coordinate in section 1.10 is taken from `tools/design.py` at the new outline.
3. The T19 star-point check and the T0 bare-board isolation now have to hold across **four**
   copper layers, not two. The star-point rule itself -- AGND_REF to DGND at R90 only,
   HARN_SHIELD to DGND at R91 only -- lives in DSN-EEG-003 section 3.3 and is not restated
   here.
4. The isolation keep-out is copper-free on **all four layers**, and that is a result read
   from the DRC report rather than an assumption: the report lists no isolation keep-out
   violation. Its coordinates and the star-point rule live in DSN-EEG-003 section 3.3;
   FIX-04 works to that section.

The fixtures' own printed circuit boards are unaffected: they stay two-layer, and section 1.9
says so explicitly so that nobody reads the carrier's stack-up onto them.

### 0.3 Programming and debug access -- no deviation remains

RFQ-EEG-001 Rev E E-28 asks for TP1 to TP18 on the carrier plus a 1x6 UART debug header at
J26 carrying DVDD3V3, DGND, UART_TX, UART_RX, RESET_EN and NC_GPIO0. EEG-CAR-01 Rev B carries
exactly that. The 2x5 1.27 mm JTAG/SWD header of RFQ Rev C is **withdrawn**: the ESP32-S3 is
programmed over UART0 and its native USB, and no JTAG connector is fitted. J26 way 6 is a
spare way named `NC_GPIO0` because GPIO0 is committed to LED_SR_LATCH (ECO-EEG-009) and does
not reach J26. FIX-03 is designed to that board, and the "E-28 deviation" open item carried in
Rev A of this document is deleted rather than answered.

---

## 1. FIX-01 -- front-end injection, lead-off and contact-light fixture

### 1.1 What it has to do

One function generator drives all sixteen protected inputs at once. That is not a convenience:
E-04's gain limit is *channel-to-channel matching within 0.5 %*, which is a ratio, and a ratio
measured against a source common to every channel at the same instant is free of the
generator's amplitude error entirely. Driving channels one at a time would put the generator's
+/-1 to 2 % amplitude accuracy straight into a 0.5 % limit, and would turn T7 into a 48-minute
sequential test instead of a 6-minute parallel one.

Absolute gain is a different quantity: the per-channel constant F-18 writes into NVS, recorded
rather than judged. FIX-01 produces it from an internal DC substitution source traceable to the
volt, not from the generator.

### 1.2 Architecture, in text-schematic form

```
J101 BNC  ---LK1--- [generator screen to FIX_COM; OPEN for T9b]
   centre --o K103.A (SIN)
                          +-------------------- J102 BNC monitor (DMM at the
                          |                     divider INPUT -- this node is
                          |                     measured, never commanded)
U3 ADR4550 5.0000 V --o K103.B (CAL)
   via K101/K102 DPDT polarity reversal, 5 s dwell each polarity
                          |
                     SRC_HI node
                          |
                    R101 9k90  (A1, ratio network, 99:1)
                          |
                    +-----+----- SRC_MID  (10 mV from 1 V; 5.0000 mV from 5.0000 V)
                    |     |
                  R102 100R    U1 OPA189 unity buffer, out = GRD_DRV
                    |            |
                 FIX_COM         +--> U2 OPA189 unity buffer --> GUARD pour
                                 |
                            R103 180R  (A2, ratio network, 9:1)
                                 |
                          +------+----- SRC_LO  (1/1000 of SRC_HI, Zo = 18 R)
                          |      |
                       R104 20R0 |
                          |      |
                       FIX_COM   +---- SRC bus, guarded, to 16 channel networks

per channel n (n = 1..16), all five relays open = OPEN:
   SRC bus --K(5n-4)--+
   RA(n) 4k99 --K(5n-3)--+
   RB(n) 10k0 --K(5n-2)--+---- RS(n) 100R 0.1% ---- channel pin n
   RC(n) 49k9 --K(5n-1)--+
   FIX_COM --K(5n)-------+      [SHORT position]
   (RA/RB/RC return to FIX_COM)

channel pins 1..11  -> J103, 12-way plug, into J14        [FIX-01/A]
channel pins 12..14 -> J105, 3-way DIN plug bar, J15/J16/J17  [FIX-01/B]
channel pins 15,16  -> J106, 3-way plug, into J22 pins 1 and 3 [FIX-01/G]
FIX_COM             -> J106 pin 2 = J22.2 = AGND_REF      [FIX-01/C]
lights              -> J104, 10-way plug, into J30        [FIX-01/E]
1.000 R shunts      -> J108/J109, JST PH pigtails, J13 and J24  [FIX-04/A]
```

FIX_COM is the fixture common. It reaches the DUT at exactly one point, J22 pin 2, which is
AGND_REF in the Rev B netlist. This closes the v1 audit finding that T8's "inputs shorted to
AGND_REF" had no defined return: on Rev A the reference was not on the harness connector at
all. On Rev B it is on J22, and the FIX-01/C lead is marked **ANALOGUE REFERENCE -- NOT
DGND**. TST-EEG-004 section 6.1 gives FIX-01/C two positions, TP13 and J22 pin 2; both are
built, and the J22 position is the one used for T8 because it is inside the protection
network rather than behind it.

The short for T8 is taken **at the connector pins**, so R1-R16 and C1-C16 stay in circuit.
That is the chain a participant is connected to, and its Johnson noise is part of the 1.0 µV
budget of E-03, not something to be engineered out of the measurement. The 68 kΩ noise and
flatness arithmetic lives in RISK-EEG-011 section 4 and is not repeated here; **RISK-EEG-011
still runs it at 47 kΩ and is owed the same correction**.

**R1-R16 are 68 kΩ.** *Corrected 2026-09-02: this paragraph read "R1-R16 are 47 kΩ on the
Phase 1 prototypes and do not stay that way. ECO-EEG-024 raises them to 68 kΩ before Phase 2
... when that ECO is cut, every lead-off expectation in section 1.6 and every calculated value
in TST-EEG-004 T10 must be recomputed at 68 kΩ."* The ECO is cut: `tools/design.py` fits
68 kΩ, and the recomputation it called for is done -- section 1.6's expectations and
TST-EEG-004 T10's calculated values are now the 68 kΩ set, and the T8 noise expectation is
0.31 µV RMS. E-10 sits at its +/-1.0 dB branch at the fitted 68 kΩ and was +/-0.5 dB at
47 kΩ; both states are stated together everywhere they appear. **The fixture hardware does not
change**, which is why this is a correction to wording and arithmetic and not to a design.

### 1.3 The divider, and its accuracy budget

Two cascaded ratio networks with a buffer between them, 99:1 then 9:1, total 1000:1.

| Stage | Top | Bottom | Nominal ratio | Output impedance |
|---|---|---|---|---|
| A1 | R101 9.90 kΩ | R102 100 Ω | 100:1 | 99.0 Ω into U1 (1 TΩ) |
| U1 | -- | -- | 1:1 | < 1 Ω |
| A2 | R103 180 Ω | R104 20.0 Ω | 10:1 | 18.0 Ω |

The buffer is there so that A2 does not load A1: without it, A2's 200 Ω across A1's 100 Ω
bottom leg gives 66.7 Ω, A1 attenuates by (9900 + 66.7) / 66.7 = 149.5 instead of 100, and
1000:1 becomes **1495:1, a 49.5 % ratio error**. An earlier draft of this revision printed
1099:1 and 9 %, which is the arithmetic for a 1000 Ω load and not for the 200 Ω the table
above specifies.

**The ratio is calibrated, not assumed.** Each stage is measured in DC at a high level where a
6.5-digit DMM is at its best, and the composite ratio is the product. Resistor tolerance is
therefore not the dominant term; it only has to keep the ratio still between calibrations.

Worked budget, using the published 1-year DC accuracy of a 34465A-class 6.5-digit DMM at
18-28 °C, as +/-(% of reading + % of range): 10 V range 0.0035 + 0.0005; 1 V range
0.0035 + 0.0007; 100 mV range 0.0040 + 0.0035. **A manufacturer using a different DMM must
substitute its figures and redo this table.**

| Term | Arithmetic | 1σ |
|---|---|---|
| A1 input, 5.0000 V on 10 V range | 0.0035 % x 5 V = 175 µV; 0.0005 % x 10 V = 50 µV; 225 µV / 5 V | 0.0045 % |
| A1 output, 50.00 mV on 100 mV range | 0.0040 % x 50 mV = 2.0 µV; 0.0035 % x 100 mV = 3.5 µV; 5.5 µV / 50 mV | 0.0110 % |
| A1 ratio, RSS of the two | √(0.0045² + 0.0110²) | 0.0119 % |
| U1 gain, 1 V in and out on the 1 V range | √(0.0042² + 0.0042²) | 0.0059 % |
| A2 input 5.0000 V, output 500.0 mV on 1 V range | √(0.0045² + 0.0049²) | 0.0066 % |
| Reference U3 value, 5.0000 V on 10 V range | as A1 input | 0.0045 % |
| Reference drift, 2 ppm/°C over 18-25 °C plus 6-month load life | √(0.0007² + 0.0025²) | 0.0026 % |
| Ratio drift, 2 ppm/°C tracking plus 6-month load life | as above | 0.0026 % |
| Residual thermal EMF after +/- polarity differencing | 1 µV site mismatch, cancelled to 10 % | 0.0020 % |
| Guard leakage, 1 TΩ against an 18 Ω source | calculated | 0.0020 % |
| Channel-to-channel inequality (relay contact, RS spread, bias current) | calculated | 0.0020 % |
| Output loading at DC by 16 channels (68 k into > 1 GΩ ADS input) | 18 Ω / > 1 GΩ | 0.0001 % |
| **Combined, RSS** | √(sum of squares) = √(2.558 x 10⁻⁴) | **0.0160 %** |
| **Expanded, k = 2** | | **0.0320 %** |

The rule the programme set is that the fixture's own uncertainty must be five times better than
the 0.5 % limit it verifies, that is 0.100 % or better. 0.0320 % beats it by a factor of 3.1,
and the test uncertainty ratio against the 0.5 % limit is 0.5 / 0.0320 = **15.6:1**.

Two supporting calculations, both of which are counter-intuitive and should not be
"improved" away by a manufacturer:

*Loading in AC mode.* At 10 Hz each DUT input presents 47.1 kΩ in series with
1/(2π x 10 x 10 nF) = 1.5915 MΩ of reactance. Sixteen in parallel is 2.94 kΩ - j99.47 kΩ.
Against the divider's 18 Ω real output impedance the attenuation error is
18 x 2944 / (99514)² = 5.4 x 10⁻⁶, that is **0.0005 %**. The load is almost purely reactive and
therefore almost orthogonal to a resistive source impedance. Do not lower the divider
impedance to "fix" this; a lower bottom leg costs ratio accuracy and buys nothing.

*DC-to-10 Hz difference.* The only reactance in the divider is stray capacitance, of order
50 pF, which is 318 MΩ at 10 Hz against a 100 Ω bottom leg: 3 x 10⁻⁷. The DC-calibrated ratio
is valid at 10 Hz to better than **0.001 %**.

**Design rule: no switch contact may appear in either leg of either ratio network.** Relay
contact resistance of 100 mΩ in a 20 Ω bottom leg is a 0.5 % error. In the channel networks
the same 100 mΩ sits against 1.59 MΩ and is invisible.

### 1.4 The estimator, and what the 10 µV point can and cannot support

Amplitudes in TST-EEG-004 are **RMS**. The package never said, and a factor of √2 or 2√2 in a
0.5 % limit is not a detail.

For a coherent single-bin estimate at the test frequency, with one-sided noise density S at
that frequency and record length T, the 1σ uncertainty of the estimated RMS amplitude is
S / √(2T). With E-03's limit of 1.0 µV RMS over 0.5-70 Hz, S = 1.0 / √69.5 =
0.1200 µV/√Hz, calculated.

| Level | T = 60 s, 1σ | T = 60 s, k = 2 | T = 240 s, k = 2 | T = 600 s, k = 2 |
|---|---|---|---|---|
| 1 mV RMS | 0.0011 % | 0.0022 % | 0.0011 % | 0.0007 % |
| 100 µV RMS | 0.011 % | 0.022 % | 0.011 % | 0.007 % |
| 10 µV RMS | 0.110 % | 0.219 % | 0.110 % | 0.069 % |

At 60 s the 10 µV point consumes 44 % of a 0.5 % limit before the fixture contributes
anything, which is why **the 0.5 % gain-matching limit of E-04 applies at the 100 µV and 1 mV
points only. The 10 µV point is a linearity check with a +/-5 % limit.** That is the
programme's ruling and it settles the disagreement the audit found: TST-EEG-004 T7's
"+/-2 %" is corrected to +/-5 %, and QP-EEG-010's "1σ" label on the 0.219 % figure is
corrected -- the derivation above puts it at k = 2 for a 60 s record, which the ruling rounds
to 0.22 %.

Against the +/-5 % limit a 60 s record already gives a test uncertainty ratio of
5 / 0.219 = **22.8:1**. TST-EEG-004 Rev C T7 nevertheless records **240 s** at the 10 µV
point; that costs three minutes and buys a further factor of two, and the record length is
TST-EEG-004's to set. This document supplies the arithmetic and does not set the step.

Estimator: rectangular window, integer number of cycles, bin width 1/T, amplitude and phase
and residual all reported, together with the in-band noise used to compute the uncertainty.

### 1.5 Channel and injection map

Rev B has sixteen protected input networks R1-R16 and sixteen converter channels. They are not
the same sixteen, and the v1 audit's "T7 demands 16 values and the jig can reach 8" is closed
by saying so explicitly.

| Fixture ch | Protection | Carrier net | Converter | Gain | Physical access | Mode |
|---|---|---|---|---|---|---|
| 1-8 | R1-R8 / D1-D8 / C1-C8 | IN1-IN8 (Fz Cz Pz C3 C4 T7 T8 F7) | module #1 ch 1-8 | 24 | J14 pins 1-8 via FIX-01/A | SIN, CAL, 4k99/10k0/49k9, SHORT |
| 9 | R9 | REF_L into SRB1 | reference node | -- | J14 pin 9 | SHORT during T10 (lead-off return) |
| 10 | R10 | REF_R into SRB1 | reference node | -- | J14 pin 10 | SHORT during T10 |
| 11 | R11 | BIASOUT out to BIAS_EL | bias driver, an output | -- | J14 pin 11 | OPEN or SHORT only; never driven |
| 12-14 | R12-R14 | EMG1-EMG3 | module #2 ch 1-3 | 12 | J15/J16/J17 via FIX-01/B | SIN, CAL, references, SHORT |
| 15-16 | R15-R16 | SPARE1, SPARE2 | module #2 ch 7-8 | 1 for T12b, 24 otherwise | J22 pins 1 and 3 via FIX-01/G | SIN, CAL, SHORT; the FIX-02/D onset marker |
| -- | none | ENV_STIM, ENV_VOICE, ENV_ROOM | module #2 ch 4-6 | 1 | internal, from U1-U3 | FIX-02 only |

D1-D16 are **BAV99**, not BAT54S: Schottky leakage across a 68 kΩ series resistor is an offset
error on a 10 µV input. BAT54S appears only at D20, D40 and D60, the envelope rectifiers.
TST-EEG-004 T1's visual check is corrected to match.

Channel 11 is a bias **output**. Driving it from the divider would fight the ADS1299's BIAS
amplifier. FIX-01 leaves it open except during T8, where SHORT loads it the way a scalp does.

Channels 9 and 10 must be in SHORT during T10, because the ADS1299 lead-off excitation leaves
the input under test and returns through SRB1. Without that return the impedance reading is
meaningless. Nothing in v1 said so.

Two numbering warnings, because three numbering systems are live in this package. The fixture
channel numbers in this table are the **R1-R16 protection-network** numbers. TST-EEG-004 T7
and T27 use the **stream** numbering, in which fixture channel 12 is stream channel 9. The
daisy-chain order check is the same check under either name: fixture channel 12, stream
channel 9, must read gain 12 while fixture channel 1 reads gain 24. If they are swapped,
module #2 is not first on the chain, which is TST-EEG-004 T27. Second, the spare channels
default to gain 24 in RFQ-EEG-001 section 3.1 and FW-EEG-001 section 5.2; the host tool must
set **gain 1** on module #2 channel 7 for the T12b marker, or the +/-1.0 V marker of section
2.3 saturates a gain-24 input.

### 1.6 Reference resistors and the lead-off test

Nominal values are E96, because 0.1 % thin film is not made in E24: **4.99 kΩ, 10.0 kΩ,
49.9 kΩ**, Vishay TNPW0603 series, 0.1 %, 25 ppm/°C, the same family as R1-R16. TST-EEG-004
Rev C now names the same three parts by the same E96 values, written **4k99 / 10k0 / 49k9** in
its T10 and its section 6.1; the rounded naming survives in **RFQ-EEG-001 Rev E section 9.1
item 7 and RISK-EEG-011 H-24**, which still call them "5 kΩ, 10 kΩ and 50 kΩ". Those are
names, not a second set of parts: 5.00 kΩ and 50.0 kΩ do not exist as 0.1 % thin film, and no
fixture will ever be built with them. The 15 % limit is applied against each resistor's
**measured, recorded** value, not against a round number, so the naming difference cannot
reach a pass or fail decision.

The series resistors sit inside the measurement. A 4.99 kΩ reference reads as about 73 kΩ,
which is a 1,360 % error against a 15 % limit -- the v1 audit's point, and the reason every
unit would have failed T10 on the first attempt. The fixture makes T10 a **two-point
calibration** instead of a check: record the residual in OPEN, record Z at each of the three
references, least-squares fit for a per-channel offset R_off and slope k. Pass criteria:
R_off within **68 kΩ +/-5 %** (a cold joint on R1-R8 shows here and nowhere else), and after
correction the three references reported within 15 %. *Corrected 2026-09-02: this passage was
written with 47 kΩ fitted -- a 4.99 kΩ reference reading about 52 kΩ, a 940 % error, and an
R_off band of 47 kΩ +/-5 % -- and held the 68 kΩ case out as conditional. ECO-EEG-024 is
applied in `tools/design.py`, so 68 kΩ is the fitted value; TST-EEG-004 T10's three
calculated raw expectations are recomputed with it and are now 70.5, 75.1 and 111.5 kΩ.*

Excitation must be fixed at **LOFF_FREQ 7.8 Hz, LOFF_MAG 6 nA** (E-06). At 7.8 Hz the 10 nF
shunt is 2.04 MΩ; the worst case, 49.9 k + 68 k = 117.9 kΩ in parallel with 2.04 MΩ, reads
**111.5 kΩ**, that is 5.5 % low -- inside the limit and identical for a reference resistor and
for a scalp electrode, so it largely cancels in the fit. **TST-EEG-004 T10 prints the same
111.5 kΩ.** *Corrected 2026-09-02: this paragraph ran the arithmetic at 47 kΩ and printed
92.5 kΩ at 4.5 % low. That figure is the superseded one; it is still the right contrast against
the rounded 50 kΩ name, which gives 92.6 kΩ, and that is why the E96 values are used.* At
31.2 Hz the shunt is 510 kΩ, the same point reads far lower still and T10 fails on physics --
at 47 kΩ that reading was 81.4 kΩ, 16 % low, and the 68 kΩ figure has not been recomputed here
because the conclusion does not turn on it. All figures calculated from the fitted 49.9 kΩ, not
from the rounded name.

C1-C16 are **10 nF C0G**, part `GCM1885C1H103JA16D`. The `GCM188R71H103KA37D` of package v1 is
an X7R part and is wrong; an X7R at its legal +20 % moves the corner far enough to fail T22, so
the fixture's lead-off model and the frequency-response step both depend on the C0G part
actually being fitted. That correction is ECO-EEG-019 in ECO-EEG-016.

### 1.7 FIX-01/E -- the contact-light colorimeter head, into J30

T11 needs the eight bicolour lights verified per site and proven dark during a recording block
(E-27). Watching lamps is not a record, and neither is a current measurement: a sense resistor
cannot tell a lit LED from a shorted one, and it cannot tell green from red at all. **The
measurement is colorimetric.** The LED current-sense scheme of Rev A of this document is
dropped.

FIX-01/E is a light-tight MJF PA12 manifold on the 1x10 plug into J30. It carries the eight
two-lead bicolour LEDs of the helmet part in the helmet's polarity, each in series with a 1 kΩ
resistor position that is fitted with a **0 Ω link**, so each site draws the 1.3 mA the
carrier actually drives (ICD-EEG-006 section 2.11 owns that arithmetic). Over the sites sits
one **TCS34725-class RGB colorimeter**, on an indexed carrier with a detent per site, read
over I²C by the fixture controller M1.

**The 0 Ω link is a correction, and the arithmetic is why.** Rev B of this document put a
1.0 kΩ resistor at each site "the same value as R70-R77, so each site draws the 1.3 mA the
carrier actually drives". Those two halves contradict each other. R70 to R77 are **on the
carrier**, one per LEDn line between the 74HC595 outputs and the cable (WH-EEG-008 section
3.2), and it is those resistors that set (3.3 - 2.0) / 1000 = 1.3 mA. A second 1.0 kΩ in the
fixture head puts 2.0 kΩ in the same loop and the site draws (3.3 - 2.0) / 2000 = **0.65 mA,
half the current the product uses**. The R/G ratio recorded at calibration would then be the
ratio at a current no carrier ever drives, on a fixture whose only job is to prove the sites
at the current the carrier does drive. The positions RL1 to RL8 are kept and fitted with 0 Ω
links rather than deleted, so that a current-sense resistor can be dropped in at one site
during a fault-finding session without cutting a track.

One head and not eight, for a reason worth stating: the TCS34725 has a fixed I²C address, so
eight would need a bus multiplexer and eight separate calibrations, and TST-EEG-004 T11 drives
one site at a time in any case. One head on a mechanical index is simpler, and it is the one
item that has to be calibrated.

| Quantity | Setting or limit | Source |
|---|---|---|
| Integration time | **300 ms** = 125 TCS34725 integration steps of 2.4 ms | this document |
| Gain | fixed, recorded at calibration, the same for all states | this document |
| Reported value | red-to-green channel ratio R/G, plus the clear channel for the dark states | TST-EEG-004 T11 |
| Green state | R/G <= 0.30 | TST-EEG-004 T11 |
| Red state | R/G >= 3.0 | TST-EEG-004 T11 |
| Amber state | 0.6 <= R/G <= 1.7 | TST-EEG-004 T11 |
| Dark at boot and dark during a recording block | below 2 % of the green-state clear reading | TST-EEG-004 T11 |
| Repeatability | <= 2 % on the ratio | TST-EEG-004 section 4 |

The 300 ms integration is chosen and not inherited, and it survives the driver that has since
been written. `LIGHT_PHASE_HZ` is **240**, the fitted value against E-27's "above 100 Hz", so a
half-phase is 2.083 ms and a period 4.1667 ms; 300 ms is 125 TCS34725 integration steps and 72
whole phase periods, so the ratio does not depend on where the integration window starts. **The
firmware delays with the FreeRTOS tick, so the half-phase quantises to 2 ms on a 1 kHz tick and
the unit alternates at about 250 Hz rather than 240** (TST-EEG-004 T11 Note 2). That is stated
rather than smoothed over, and it changes nothing here: 300 ms at 250 Hz is **75 whole
periods**, still exact, the two half-phases stay equal so the duty stays 50/50 and no colour
shifts, and a ratio is blind to 4 % of frequency in any case. The same 300 ms is used for the
static states so that one calibration covers all three.

Because the ratio is a ratio, absolute illuminance drops out and the head needs no photometric
traceability; the light-tight manifold is what removes ambient light, and it replaces the
TEMT6000 ambient sensor of Rev A. Shift-start verification is against a printed reference card
with a green and a red patch, held in the manifold's calibration position (section 1.12).

**The driver exists as of 2026-09-02, and Rev B's "T11 cannot pass yet, and the fixture is not
the reason" is superseded on that date.** `firmware/main/main.c` implements E-27's bicolour
phase scheme: the converter's positive-side lead-off comparator is read at two thresholds, a
site that trips neither is green, one that trips only the sensitive threshold is amber, one
that trips both is red, and the two phases alternate with green in phase A, red in phase B and
amber in both. *As first written on that date the driver used both halves of the lead-off
status and red was unreachable; FW-D17, the same day, replaced it -- see below.* **The colour is computed
from lead-off and cannot be written to the shift register by a host command**, so FIX-01/E is
only half the fixture T11 now needs: the states are produced at the electrode inputs with
FIX-01/A's reference resistors and the relay matrix of section 1.5, on this same board, and
FIX-01/E reads the result. TST-EEG-004 T11 carries the procedure.

**Corrected 2026-09-02 (FW-D17): all three states can now be produced, and the fixture needs
no change to produce them.** This paragraph read that red was unreachable because `LOFF_SENSN`
was never written, and proposed enabling it. That would not have worked: **the montage is
single-ended**, so there is no per-site negative electrode, and with `SRB1` closed all eight
N bits would have reported the one shared reference. The firmware now sweeps the positive-side
comparator threshold `COMP_TH` between a sensitive and an insensitive setting, so red is a
site that trips both and amber is a site that trips only the sensitive one.

**What this means for the fixture:** FIX-01/A's reference resistors and the relay matrix of
section 1.5 are exactly the right instrument for it, because the three states are now three
impedance bands rather than two independent detectors. T11 must present a resistance below
the sensitive trip point for green, one between the two trip points for amber, and one above
the insensitive trip point for red. **The two `COMP_TH` values in the firmware are the
datasheet's endpoints, not measured ones**, so the resistor values T11 needs cannot be fixed
until the first unit is characterised -- that is T11 Note 3 and it belongs to the firmware
owner with E-27's owner in DSN-EEG-003 section 11. It is in section 7 below.

J30 carries no electrode signal (ECO-EEG-014) and FIX-01/E is on the far side of the box from
the guarded compartment.

### 1.8 Bill of materials, FIX-01

| Ref | Qty | Description | Reference part |
|---|---|---|---|
| A1 | 1 | Ratio network 9.90 kΩ / 100 Ω, 0.01 % ratio, 2 ppm/°C tracking | Vishay VHD200 series, custom ratio. **Alternate, and the schedule-safe choice:** 2 x Vishay VSMP0603 Z-foil, 9k90 and 100R, 0.01 %, 0.2 ppm/°C |
| A2 | 1 | Ratio network 180 Ω / 20.0 Ω, 0.01 % | as A1 |
| U1, U2 | 2 | Zero-drift precision op-amp, unity buffer and guard driver | TI OPA189IDBVR |
| U3 | 1 | 5.0000 V reference, 0.02 %, 2 ppm/°C | ADI ADR4550BRZ |
| K101, K102 | 2 | DPDT polarity commutator, CAL mode | Omron G6K-2F-Y DC5 |
| K103 | 1 | SIN / CAL source select | Omron G6K-2F-Y DC5 |
| K1-K80 | 80 | Channel matrix, 5 per channel x 16 channels | Omron G6K-2F-Y DC5 |
| U10-U19, U22 | **11** | 8-bit power shift register, 150 mA open-drain, clamped. **Eleven, not the ten of Rev B**: 80 channel relays plus K101, K102 and K103 is 83 loads and ten devices are 80 outputs. U22 carries the three source relays and has five outputs spare | TI TPIC6B595DW |
| M1 | 1 | Fixture controller, USB CDC, no radio. Firmware and host protocol in section 8; source at `fixtures/firmware/` | Raspberry Pi Pico (RP2040) |
| RS1-RS16 | 16 | 100 Ω 0.1 % 25 ppm, per-channel series and common-mode injection | Vishay TNPW0603100RBEEA |
| RA1-RA16 | 16 | 4.99 kΩ 0.1 % 25 ppm lead-off reference | Vishay TNPW06034K99BEEA |
| RB1-RB16 | 16 | 10.0 kΩ 0.1 % 25 ppm lead-off reference | Vishay TNPW060310K0BEEA |
| RC1-RC16 | 16 | 49.9 kΩ 0.1 % 25 ppm lead-off reference | Vishay TNPW060349K9BEEA |
| D201-D208 | 8 | Two-lead bicolour LED, helmet part, in FIX-01/E | per DSN-EEG-002 Rev E (Kingbright WP59EGW class) |
| RL1-RL8 | 8 | **0 Ω link** at each FIX-01/E site. The current limit is R70-R77 on the carrier; see the correction in section 1.7 | Vishay CRCW06030000Z0EA class jumper |
| **U21** | **1** | **RGB colour sensor with IR filter, I²C, FIX-01/E** | **AMS TCS34725 on a breakout, ams TCS34725FN** |
| U20 | 1 | 16:1 analogue multiplexer for the relay self-test reads | TI CD74HC4067M |
| **RP1** | **1** | **10.0 kΩ 0.1 % 25 ppm readback pull-up**, from M1 GP11 to the U20 common. It is what makes the section 1.12 step 2 relay readback a measurement rather than a continuity check; the arithmetic is in section 8.4 | Vishay TNPW060310K0BEEA |
| J101, J102 | 2 | BNC, generator in and DMM monitor | Amphenol 031-6572 |
| J103 | 1 | 1x12 pin plug, 2.54 mm, FIX-01/A, in a WH-KEY-01 shroud | Samtec TSW-112-08-G-S |
| J104 | 1 | 1x10 pin plug, 2.54 mm, FIX-01/E, in a WH-KEY-01 shroud | Samtec TSW-110-08-G-S |
| J105 | 1 | 3 x touch-proof 1.5 mm DIN 42802 plug on a 12 mm-pitch bar, FIX-01/B | Staubli LM-I1,5, colour-coded |
| J106 | 1 | 1x3 pin plug, 2.54 mm, FIX-01/C and FIX-01/G | Samtec TSW-103-08-G-S |
| J107 | 1 | 5 V 2 A input, isolated supply or USB power bank | -- |
| LK1 | 1 | Generator screen to FIX_COM link, opened for T9b | 2.54 mm jumper, captive |
| -- | 1 | Die-cast aluminium enclosure | Hammond 1590D, 188 x 119 x 37 mm |
| -- | 1 | Tinplate screening can over the divider compartment | 60 x 40 x 15 mm, soldered on four sides |
| -- | 1 | Light-tight FIX-01/E manifold | MJF PA12, dyed black, `fixtures/stl/FIX-01E_colorimeter_manifold.stl` (section 8.9) |
| -- | 1 | FIX-01/E indexed sensor carrier | MJF PA12, dyed black, `fixtures/stl/FIX-01E_sensor_carrier.stl` (section 8.9) |
| -- | 1 | Colorimeter reference card, green and red patch | printed, matt, replaced annually |
| -- | 3 | WH-KEY-01 keying shrouds, J14, J30 and J22 forms | MJF PA12, from the MP-01 / POD-P1 print set |
| -- | 2 | Screened multicore, 1.0 m, 16 cores plus overall braid | Alpha 5478C class |

The 1.000 Ω shunt pigtails that an earlier draft of this revision listed here as FIX-01/F --
a letter TST-EEG-004 section 6.1 gives to the 1000:1 divider of section 1.3 -- are **FIX-04/A**
and are in the FIX-04 bill of materials at section 4.1. They are read at the
FIX-01 shift start (section 1.12) because T3 and T4 use them alongside FIX-01, but they
belong to FIX-04.

### 1.9 Fixture board outline and layout rules

**This is the fixture's own board and it has nothing to do with the carrier's stack-up.**
160.0 x 100.0 mm, **two-layer** FR-4 Tg >= 150 °C, 1.6 mm, 1 oz copper, ENIG, green mask, white
legend both sides, IPC-6012 class 2 and IPC-A-600 class 2. Four M3 non-plated holes at (5, 5),
(155, 5), (5, 95), (155, 95), 6 mm keep-out. Minimum track and clearance 0.20 mm / 0.20 mm.
Origin bottom-left, Y up, matching the Gerber convention of `tools/gerber.py`; note that
design.py itself uses a top-left origin with Y down and converts once, as
`y_out = 130.0 - y_design`, and that FIX-01 does not inherit that convention.

| x band | Contents |
|---|---|
| 0-40 mm | Guarded compartment: U3, K101-K103, A1, U1, A2, U2, inside the soldered can |
| 40-150 mm | Relay matrix, 5 columns of 16, and the reference resistor field |
| 150-160 mm | TPIC6B595 chain, M1, U20, the 5 V input and the FIX-01/E I²C header |
| front edge | J103, J104, J105, J106 shrouds; J101, J102 on the left end panel |

The SRC bus and the sixteen channel tracks are top-layer only, each inside a 0.5 mm gap from
the GUARD pour, with the bottom layer beneath them being GUARD and not common. GUARD stops
2 mm short of every shroud, so the guard never leaves the box on a cable.

**The board data is released at `fixtures/pcb/FIX-01/`, and it is not a fabrication set.**
`tools/fixture_gen.py` writes the outline, the four M3 mounting holes, the zoning and
keep-out artwork, the panel legend and the non-plated drill programme as Gerber X2 and
Excellon in the house style of `kicad/gerber/`, together with the **complete netlist** --
217 nets and 772 pins, generated from the section 1.2 text schematic rather than typed --
and a constraints file carrying everything in this section plus the rules a layout has to
meet. There is no copper layer, no via, no plated drill and no paste layer, and section 8.8
says plainly why not and what a layout contractor is being asked for. Section 6.1 now
carries the labour and section 6.3 the days.

**One result of that work belongs in this section, because it is about this outline.** The
area budget in `fixtures/pcb/FIX-01/FIX-01_constraints.txt` is computed by the generator and
puts the bill of materials at **60 % of the 160.0 x 100.0 mm board** against a 60 % working
occupancy for a two-layer board of this density -- that is, exactly at the limit. The
largest relay land pattern the outline can carry is **70.7 mm²**, about 10.1 x 7.0 mm, and
the Omron G6K-2F-Y datasheet is not in this package, so whether the outline closes at all
turns on one number nobody here has looked up. **Treat 160.0 x 100.0 mm as provisional until
that datasheet is opened.** The Hammond 1590D enclosure is 188 x 119 mm inside and has room
for a larger board, so the remedy is cheap if the number goes the wrong way; what would not
be cheap is discovering it after a five-off minimum order. This is listed in section 7.

### 1.10 Mating, keying and the mis-mate hazard

Coordinates below are design-source coordinates from `tools/design.py`, top-left origin with Y
down, on the 150.0 x 130.0 mm outline: J14 (1x12 socket, 5.0, 12.0), J30 (1x10 socket, 66.0,
90.0), J22 (1x3 socket, 30.0, 116.0, rotated 90°), and J15, J16, J17 (DIN 42802 sockets at
8.0, 76.0 / 8.0, 88.0 / 8.0, 100.0, a 12 mm pitch). J14, J30 and J22 are plain 2.54 mm socket
strips. A plain socket strip is not keyed, and the v1 audit is right that an unkeyed strip has
three plausible mis-mates, two of which put a driven rail onto a high-impedance protected
input. The key is therefore mechanical and lives in the shroud.

**The fixture uses the product's own keying part, WH-KEY-01, and does not define its own.**
That is the whole point: a fixture that mates through a shroud the product never uses proves a
mate the product never makes. WH-KEY-01 is the printed keying shroud that is part of the
MP-01 / POD-P1 print set; WH-EEG-008 section 6 fits it around J14 and J30 on the harness ends,
and ICD-EEG-006 section 6 lists which sockets carry one. FIX-01/A and FIX-01/E carry the
identical J14 and J30 shrouds, printed from the same STLs.

- The J14 shroud accepts the housing's polarising ramp in one orientation only and physically
  cannot enter J30 or J22.
- The J30 shroud is 10-position and indexes on the same feature the harness uses.
- FIX-01/C and FIX-01/G share a 3-position body that will not enter a 10- or 12-position
  socket; where a WH-KEY-01 form is fitted to J22 on the product, the fixture head carries it
  too.
- Each shroud carries a moulded pin-1 chamfer aligned with the square pad marked on the
  carrier silkscreen, and a printed legend naming its socket.

If WH-EEG-008 and this document ever diverge on the shroud again, WH-EEG-008 governs, because
the harness is the thing the participant plugs in.

### 1.11 Shield, guard and the common -- the three are different things

| Net | What it is | Where it is bonded |
|---|---|---|
| SRC / channel nets | The signal | -- |
| GUARD | A unity-gain copy of SRC_MID, driven by U2 | Nowhere else. Surrounds the low-level tracks and forms the pour beneath them |
| FIX_COM | Fixture common, the reference every measurement is against | To the DUT at **J22 pin 2 (AGND_REF) only** |
| Box | Die-cast aluminium, and the cable braids | To FIX_COM at **one** M3 stud at the cable-entry corner |
| Protective earth | -- | **Not connected.** The fixture is powered from an isolated supply or a USB power bank |

The only accidental earth is the function generator's BNC outer, which is why LK1 exists. For
T9b (CMRR) LK1 is opened, the DUT runs on battery with USB disconnected, and the fixture common
is driven 1 V RMS at 50 Hz against earth from a battery-powered source or through a 1:1
isolating transformer, reaching all eleven analogue pins and SRB1 through the matched RS1-RS16.
CMRR per channel is 20 log10(1 V / measured differential). Record the resistance from FIX_COM to
J14 pin 12 (HARN_SHIELD) and to DGND at the same time, which is the fixture's contribution to
the star-point evidence TST-EEG-004 T19 gathers with Kelvin probes at TP13, TP14 and J14.12.

### 1.12 Fixture self-test, run at every shift start

1. Continuity of all 12 + 10 + 3 + 3 mating pins, 4-wire, <= 0.5 Ω each.
2. All 80 relays exercised, each verified through U20 against its own reference resistor,
   +/-1 % of the recorded value. The measurement this step needs did not exist in Rev B:
   a multiplexer with nothing driving it reads whatever the channel node happens to sit
   at. **Section 8.4 adds RP1**, a 10.0 kΩ readback pull-up switched by M1, and gives
   the five node voltages it produces and the resolution each is measured to. The
   sweep is one command, `SELFTEST RELAYS`, and it refuses to run until the operator
   has confirmed the fixture is unmated.
3. A1, U1 and A2 ratios re-measured in DC against the shift's DMM, +/-0.02 % of the calibrated
   value or the fixture is out of service.
4. U3 reference re-measured, +/-0.005 % of the calibrated value.
5. FIX-01/E read against the green and the red patch of the reference card in the calibration
   position: both ratios within 2 % of their recorded values, and the manifold's dark reading
   below 1 % of the green-state clear reading.
6. FIX-04/A shunts read 4-wire, +/-0.05 % of the recorded value. They belong to FIX-04 and
   are read at this shift start because T3 and T4 use them with FIX-01 on the same bench.
7. Golden unit measured on T7, T8 and T10. Gain drift > 0.2 % or noise drift > 0.15 µV halts
   the line. The golden unit is serial **TIOV-B-0001**, in the `TIOV-B-nnnn` format that the
   label, the Data Matrix, the USB `iSerialNumber`, the calibration record and the packing list
   all carry.

The result is a signed FIX-01 self-test record, one per shift, filed with that shift's unit
records.

---

## 2. FIX-02 -- audio loopback and onset fixture

### 2.1 FIX-02/D -- the 47 Ω load and the electrical-onset marker

Two non-inductive **47.0 Ω** 1 % 1 W resistors, one per channel, on a 3.5 mm TRS plug that
mates the panel jack at J27, with a BNC monitor across the left channel for the audio analyser
or the oscilloscope. Bourns PWR221T-30-47R0F or Vishay RCH25 class; wirewound is not acceptable
because its inductance colours the level measurement of T17.

47.0 Ω and not 32 Ω, because the load must be the headphones that actually ship.
Audio-Technica publishes 47 Ω for the ATH-M20x. RFQ A-04 is restated as **32 to 64 Ω**, the
calibrated output level is measured per model, and the test load is 47.0 Ω to match the shipped
part. TST-EEG-004 T17's "32.0 Ohm" is corrected with it. The load resistance is measured 4-wire
and recorded, and T17's "within 1 dB of target" is applied against the measured value.

**Maximum acoustic output is TST-EEG-004 step T28.** It is a type test rather than a per-unit
step -- it runs once per lot on one unit -- but it carries a step number, and this document
cites that number rather than asserting there is none. RFQ-EEG-001 Rev E gains E-29: the
headphone output must not exceed **100 dB SPL** at any commanded level, measured on an
artificial ear, and the firmware must clamp the codec volume register to the value measured at
calibration. The calculated full-scale output is about 110 dB SPL, which is why the requirement
exists. T28 is listed among the type tests in **TST-EEG-004 section 14** and specified in
section 8 with every other step; FIX-02 provides the electrical level that T28 correlates
against, so every per-unit record holds an electrical proxy for the acoustic ceiling. An
earlier draft of this revision cited "T22" for this and then said no T-number existed; both
statements were wrong. T22 in TST-EEG-004 Rev C is the frequency response step.

T28 needs an IEC 60318-1 artificial ear and a class 1 sound level meter. TST-EEG-004
section 6.1 puts the artificial-ear coupler inside FIX-02 and section 5 lists the sound level
meter as an instrument bought for T28 only. **Neither is in this document's FIX-02 bill of
materials at section 2.4 or in the cost tables at section 6**, and that gap is stated as an
open item in section 7 rather than papered over with a price this document cannot estimate
honestly.

### 2.2 Acoustic injection for the voice and room paths

Two couplers, each an MJF PA12 cup with a TPU 85A sealing lip, a 13 mm mylar driver, and a
reference microphone port at 90 degrees to the driver axis:

| Coupler | Fits | Cavity | Reference level |
|---|---|---|---|
| **FIX-02/A** | The boom capsule with the windscreen removed | 2.0 cm³ | 70.0 dB SPL at 1 kHz, the reference voice level of E-17 |
| **FIX-02/B** | Seals over the room-microphone port and its mesh | 3.5 cm³ | 70.0 dB SPL at 1 kHz |

The names CPL-V and CPL-R used in an earlier draft of this revision are withdrawn. PARTS-EEG-019 already
carries these two as FIX-02 sub-assemblies to be renumbered FIX-02/A and FIX-02/B, and that
renumbering is done here.

The boom carries the bare electret capsule and its screen on the pigtail at J18; the voice
**preamplifier is on the MP-01 module plate and connects at J21**, not on the boom. FIX-02/A
therefore drives a capsule, and every gain the fixture measures on the voice path is the
capsule plus the MP-01 module, not the capsule alone. Which preamplifier module that is has
**not been settled**: the MAX9814 has automatic gain control, which RFQ E-14 forbids, and
disabling it is a module-dependent modification, so the module is specified by interface in
ICD-EEG-006 and a fixed-gain part of the MAX4466 class is the preferred route. AVL-EEG-017
carries it as not approved.

Drive chain: fixture controller M2 (Raspberry Pi Pico) -> PCM5102A I2S DAC module -> TPA6132
amplifier -> coupler driver. Reference microphones are electret capsules with their own
preamps, read by M2's ADC.

Calibration chain, and it is the whole point of the word "calibrated": a Class 2 acoustic
calibrator at 94.0 dB / 1 kHz is applied to the reference microphone through an adaptor, the
reference microphone's sensitivity is recorded, the coupler is closed with a blank in place of
the DUT capsule, and the drive level is set to give 70.0 dB SPL at the reference microphone.
That drive level is the coupler's recorded constant. The Class 2 calibrator is itself
calibrated every 24 months by an ISO/IEC 17025 laboratory.

E-17 -- headphone bleed into the boom at maximum stimulus level, <= -40 dB relative to a
70 dB SPL voice -- has a reference level here and **no per-unit method anywhere**. It is a
type test on one Phase 1 unit, listed in TST-EEG-004 section 14 with no step number and no
method, and "maximum stimulus level" is not yet defined in any document. That is an open
item, not a solved one.

### 2.3 The electrical-onset reference

This is the part of T12 that v1 never defined, and without it T12 fails every unit by more than
twice its own limit.

The envelope chain has a real, calculated delay. The Sallen-Key stage of U1-U3 has
f0 = 48.77 Hz and Q = 0.7416 (ECO-EEG-006), so its group delay at DC is
1 / (Q x 2π x f0) = 1 / 227.2 = **4.40 ms = 4.40 samples at 1000 Hz**. The rectifier and the
output buffer add a little more. A literal reading of "onset within 2 samples of electrical
onset" therefore cannot pass, and never could.

**4.40 ms is the governing figure.** TST-EEG-004 T12's 4.61 ms comes from √2 / (2π f0), which
is the DC group delay of a two-pole low-pass only at Q = 0.7071; the fitted stage is
Q = 0.7416 and the correct expression is 1 / (Q · 2π · f0). TST-EEG-004's 4.61 ms is corrected
to 4.40 ms.

FIX-02 solves the comparison by putting the electrical onset **on the same converter, on the
same sample clock**:

```
47 Ω load / coupler drive  --> U201 TLV3201 comparator, threshold at 50 % of the
                               commanded burst amplitude
                           --> R201/R202 attenuator to +/-1.0 V
                           --> J106 pin 1 -> J22.1 -> R15 (47 k) -> C15 (10 nF)
                           --> SPARE1 = module #2 channel 7, gain 1
```

SPARE1 and SPARE2 were single-pad nets with no source in Rev A, which the audit recorded as
"two channels have no source at all". Rev B protects them like every other electrode lead, and
FIX-02 gives them a job: channel 7 of module #2 carries the electrical onset, channel 4 carries
ENV_STIM, and the difference between them is read directly in samples out of one data stream
with no external instrument and no cross-clock comparison. The host tool must set gain 1 on
that channel for the duration of the step (section 1.5).

**The marker attenuator, R201 and R202.** Rev B named the two parts, gave them a tolerance
and a series, and gave them no resistance. They are derived here, and the arithmetic is
short enough to print in full so that a manufacturer can check it rather than trust it.

The requirement is the +/-1.0 V above: a **2.000 V peak-to-peak** step at SPARE1. That
figure is not arbitrary and it is worth saying where it comes from, because it is the
number the divider is designed to. E-05 fixes the converters' internal reference at 4.5 V,
so an ADS1299 channel at **gain 1** has a full-scale differential range of
+/- 4.5 / 1 = **+/- 4.5 V** and a 2.000 V step sits at 44 % of positive full scale --
comfortably inside it, and far enough above the channel's own noise that the onset sample
is unambiguous. At gain 24 the range is +/- 4.5 / 24 = +/- 187.5 mV and the same step is
**10.7 times full scale**, which is the saturation section 1.5 warns about, now with a
number against it.

The source is U201's output. **The comparator is powered from the 3.300 V rail of M2**,
which is a decision made here and not inherited: it is the only regulated rail FIX-02 is
specified to have, and the alternative -- USB VBUS -- is specified over 4.75 to 5.25 V, so
a marker taken off it would change amplitude with the cable. The marker needs a **push-pull
rail-to-rail output**, so that the swing is the rail; that is a requirement on the fitted
comparator and not an assertion about the part section 2.4 names. *The fitted part's supply range must be confirmed to cover 3.3 V,
and its output drop at the 1.000 mA computed below must be confirmed to be small against
that rail; this package carries no datasheets and states both numbers so that confirming
them is one line of work.*

The load is R15 in series with C15 and then a converter input of more than 1 GOhm
(section 1.3), so at DC the divider is effectively unloaded and its ratio is its own. What
the load does constrain is the divider's **impedance level**, because the divider's Thevenin
resistance adds to R15 in the marker-path time constant of the table below.

| Step | Arithmetic | Result |
|---|---|---|
| Required ratio | 2.000 V wanted / 3.300 V available | 0.60606 |
| Required R201 : R202 | (3.300 - 2.000) / 2.000 | 0.650 |
| E96 pair | **R201 = 1.30 kΩ**, **R202 = 2.00 kΩ**; both values are in E96 and in E24 | 1.30 / 2.00 = 0.650 |
| Ratio delivered | 2.00 / (1.30 + 2.00) | 0.606060... |
| Marker amplitude | 3.300 V x 0.60606 | **2.0000 V**, exactly |
| Current from U201 | 3.300 V / 3.300 kΩ | **1.000 mA** |
| Dissipation | 1.000 mA² x 1.30 kΩ and x 2.00 kΩ | 1.30 mW and 2.00 mW, against a 0.10 W 0603 rating |
| Thevenin resistance | 1.30 kΩ in parallel with 2.00 kΩ = 2.60 / 3.30 | **787.9 Ω** |
| Effect on the marker path | (787.9 + 47 000) x 10 nF = 477.9 µs, x ln 2 | 0.331 ms against 0.326 ms for R15 alone |

The pair is exact because 1.30 + 2.00 = 3.30 and the tap is at 2.00: the divider is
3.30 kΩ across a 3.300 V rail drawing one milliamp per volt, and no rounding enters
anywhere. That is worth having, but it is not what makes the choice right -- what makes it
right is the last row. The divider's 787.9 Ω adds 1.7 % to the marker-path time constant,
which moves the 50 % delay from 0.326 ms to 0.331 ms, and **both round to the 0.33 ms this
document already publishes**, so the fixture constant in the table below is unchanged by
fitting the divider. At the 68 kΩ of ECO-EEG-024 the same arithmetic gives 0.48 ms rather
than the 0.47 ms of R15 alone; that constant is re-measured at calibration in any case, so
it is a recalibration and not a change to a limit.

*Why 0.1 % parts for a ratio that does not need them.* The marker is a timing signal. Its
amplitude has no limit tighter than "inside the gain-1 full scale and well above the
channel noise", and the rail and the comparator's output drop enter it directly, so nobody
should read the 0.1 % as a calibrated amplitude. TNPW0603 at 0.1 % and 25 ppm/°C is kept
because it is the series already on this fixture's bill of materials at four other values
and costs nothing extra, and because 25 ppm/°C keeps the marker level from wandering
between calibrations. The reason is stated so that the tolerance is not mistaken for a
requirement.

*The single-fault case, stated because the divider is DC-coupled to a protected input.*
With U201's output stuck high, SPARE1 sees +2.000 V through 787.9 Ω plus R15: 2.000 /
68.8 kΩ = **29.1 µA** into the unit. *Corrected 2026-09-02: this read 2.000 / 47.8 kΩ =
41.8 µA, computed with R15 at 47 kΩ. ECO-EEG-024 raised R1-R16 to 68 kΩ, so the fault current
falls with them.* No person is connected during T12b -- section 4.3
records that the two EOG spares are not among the fourteen patient terminations and are not
fitted in a standard build -- so this is an instrument fault and not a patient current, but
it is the same order as the S-02 limit and is recorded here rather than found later.

**The comparator threshold, closed on 2026-09-02, and the paragraph that left it open is
superseded.** Rev B ended this subsection with "The comparator threshold is a separate item
and it is NOT closed here", recommended a commanded threshold without dimensioning one, and
gave its acceptance criteria as "ripple at the comparator input below 1 % of the threshold
voltage at the lowest burst frequency TST-EEG-004 T12b uses, settling to within 1 % in under
10 ms, and a commanded range covering 10 % to 90 % of the 3.300 V rail". That paragraph is
superseded on 2026-09-02. Its *reasoning* is kept, because it is what forces the answer: the
commanded burst amplitude is a level in tenths of a decibel below digital full scale, what
that is in volts across the 47.0 Ω load is a property of the codec and the headphone
amplifier of the unit under test, no document in this package states it, and it will not be
the same on two amplifier models. **A fixed divider is therefore not specifiable, and the
threshold is commanded.** Two of its three criteria are re-checked below and met; the third,
the 10 % to 90 % range, is **superseded with the paragraph**: it is written as a fraction of
the fixture's own rail rather than as a threshold at the load, which is the wrong quantity to
size a range in, and the decision of 2026-09-02 records that it reaches none of the
thresholds T12b actually needs. The range is stated in volts at the load instead.

**The PWM.** An RP2040 PWM slice on **GP15**, sysclk 125.0 MHz, `pwm_set_wrap(slice, 999)`.
TOP = 999 and not 1000: the RP2040 counter runs 0 to TOP inclusive, so the period is TOP + 1
counts. That gives a 1000-count period, **f = 125.000 kHz exactly**, duty = CC / 1000 and
CC = 1000 at full scale. GP15 is named here because a builder cannot infer it: the free pins
are 0, 1, 12, 13, 14 and 15, GP12 to GP14 are reserved for the section 8.8 I²S transmitter and
GP0/GP1 for the UART, which leaves GP15.

**The network.** R203 = 10.0 kΩ from GP15 to the threshold node; R204 = 10.0 kΩ from the node
to M2 ground; C201 = 220 nF 50 V X7R 0603 across R204; the node goes to U201's **inverting**
input. R205 = 10.0 kΩ from **RL201 hot** -- the left channel, the same node as the section 2.1
BNC monitor -- to U201's **non-inverting** input. All three resistors are
**TNPW060310K0BEEA**, which is already approved in this package at AVL-EEG-017 row 126 and is
already on this fixture at RB1-RB16 and RP1, so this decision closes a constructed order code
rather than adding one. Section 2.4's BOM gains **four** lines, not the "one resistor and one
capacitor" the superseded paragraph estimated.

**J27.3 HP_GND is bonded to M2 ground.** Stated because both the single-supply comparator and
a ground-referenced threshold require it, and because it is a bond between the unit's audio
ground and the fixture and host side; it sits alongside the marker's existing DC path into
SPARE1 and its 41.8 µA single-fault case above.

| Step | Arithmetic | Result |
|---|---|---|
| Full-scale threshold | 3.300 V x 10.0 / (10.0 + 10.0) | **1.6500 V** |
| Setting granularity | 1.6500 V / 1000 counts | **1.650 mV per count** |
| Settling, τ | (10.0 kΩ ‖ 10.0 kΩ) x 220 nF = 5.00 kΩ x 220 nF | 1.100 ms |
| Settling to 1 % | 4.605 τ | **5.07 ms** against the 10 ms criterion, 1.97x |
| Ripple, peak to peak | 3.3 x D(1-D) / (f R203 C201) = 3.3 D(1-D) / 275 | 12.0 D(1-D) mV |
| Ripple against 1 % of a 1650 D mV threshold | 12.0 D(1-D) / (1650 D) | **0.727 %(1-D)**, worst 0.727 % as D goes to zero |
| PWM frequency against T12b's 1 kHz burst | 125.0 kHz / 1 kHz | 125x, that is **2.10 decades** |

The ripple worst case is stated as D going to zero because that is where the relative figure
peaks; it is inside the 1 % criterion at every setting with 27 % of margin. 2.10 decades is
not three, and it is stated as what it is: far enough above the burst that nothing aliases
into the marker.

**Range: 0 to 1.650 V, which is 50 % of a burst up to 3.30 V peak at the 47.0 Ω load.** That
bounds every case this package permits, and a range is the one thing here that should be
sized to the worst permitted case rather than a typical one, because being short is
uncommissionable and being long only costs resolution the measurement does not need. A
headphone amplifier fed from the 5.0 V V5V rail of J8.14 cannot put more than about 2.5 V
peak across the load. The ICD's fallback tap -- a 10 k / 1 k divider from HP_L to HP_GND
inside the JMP-08 module-end assembly, a divide-by-11 -- with HP_L at 2.4 V peak needs a
1.2 V threshold and fits with 27 % to spare. The package's own ~110 dB SPL full scale into
the 47 Ω ATH-M20x (FW-EEG-001) is about 1.5 V peak, a threshold near 770 mV, and fits. Note
what this replaces: **HP_TAP's "0.1 to 1.1 V peak" never bounded the 47.0 Ω load at all**,
because the ICD itself permits that tap to be a divide-by-11, and the 10 dB E-29 acoustic
derating does not apply at T12 because T6 writes the clamp constants after the
characterisation steps and the clamp is not implemented.

**1.650 mV per count is setting granularity and not accuracy.** The 3.3 V rail's tolerance and
the GPIO's output resistance set the accuracy: 330 µA into about 100 Ω is about 33 mV, some
2 % of full scale, and 2 % of threshold on a 1 kHz burst is about **2 µs** of onset error
against T12b's 1 ms sample grid.

**Operationally.** At first article for **each headphone-amplifier model**, measure the burst
amplitude across RL201 with the oscilloscope **at the resistor body** -- not "4-wire", which
is section 2.1's resistance method for the 47.0 Ω value itself -- at the level T12b actually
commands and with the E-29 clamp in whatever state it is in at T12, which today is unset. Set
THR to 50 % of the measured value, record it per model, and re-measure it at the six-monthly
FIX-02 calibration of section 5.2.

**Not closed, and deliberately left open rather than filled with a number: the coupler-drive
electrical onset for the VOICE_PRE and ROOM_PRE channels.** The source list above feeds "47 Ω
load / coupler drive" into one comparator and TST-EEG-004 T12b reports per envelope channel,
but no document in this package states the coupler drive in volts -- it is a per-coupler
constant set at calibration to give 70.0 dB SPL, and no coupler has been built or calibrated.
A second range cannot be dimensioned without that number, and an attempt to fit one produced
a network 2.4x outside the ripple criterion, so **no second range is fitted and no fitted
values are stated**. It is measured when a FIX-02/A or /B coupler is first calibrated, and it
stays in section 7.

**Who signs.** The FIX-02 fixture designer **jointly with TST-EEG-004's owner**, because
T12b's burst level is theirs to define and this threshold sets a per-unit group-delay constant
that ships inside the device and is subtracted from the study's latency data. The schematic
and safety reviewer signs the J27.3 HP_GND-to-M2-ground bond. The owner of this document signs
the FIXPROTO verb change, because the old verb is struck in the same change (section 8.6).
**This is a decision, not an approval: none of it is released until those signatures exist.**

**What would change it.** A measured burst above 3.30 V peak at the 47.0 Ω load -- which needs
a headphone amplifier on more than the 5.0 V of J8.14 -- pushes past the 1.650 V full scale;
R204 then goes to 20.0 kΩ for a 2.200 V span and C201 to 100 nF to hold the ripple criterion.
A TLV3201 datasheet showing the fitted part's supply range does not cover 3.3 V, or an output
drop at the 1.000 mA above that is not small against the rail, changes the marker rail and
this divider with it -- that is the confirmation this subsection already asks for. A T12b
burst level fixed by TST-EEG-004's owner materially below full scale would narrow the required
range and permit a finer span.

Two fixture constants are subtracted, both calculated and both re-measured at fixture
calibration:

| Constant | Value | Origin |
|---|---|---|
| Marker-path 50 % delay | 0.33 ms | R15/C15 single pole at 338.6 Hz, delay = τ ln 2 = 0.470 ms x 0.693 |
| FIX-02/A / FIX-02/B acoustic transit | 0.029 ms | 10 mm at 343 m/s |

When ECO-EEG-024 raises R15 to 68 kΩ the marker-path constant moves to 0.47 ms and is
re-measured; it is a fixture constant and not a limit, so the change is a recalibration rather
than an ECO against this document.

The step numbers are TST-EEG-004 Rev C's. **T12a** is the scaling check. **T12b** measures the
group delay as its own quantity: 40 bursts, report the median and inter-quartile range of
(envelope onset sample − marker onset sample) per envelope channel. The acceptance is that the
**spread** is <= 2 samples; the median is expected near 4.4 samples and is written per unit as
an envelope group-delay calibration constant, alongside "envelope scaling" in F-18, and
subtracted by the session runner. **T12c** confirms the U7 comparator trips. **T12d** records
the AC-coupling corner and **T12e** the Sallen-Key low-pass corner f0. **T13** is the F-21
forty-tone self-test, reported against the T12b constant.

**E-11's AC-coupling half is met by the fitted values, and T12d confirms it rather than
recording an exception. Its 50 Hz +/- 10 % low-pass half is not met with the approved parts**,
because a 100 nF C0G in 0603 / 50 V is not stocked and the fitted X7R at +/- 15 % over
temperature puts f0 between 42.4 and 57.4 Hz against a 45 to 55 Hz band; TST-EEG-004 T12e
records f0 per unit against 42 to 58 Hz and carries the conflict as its section 16 item 16.
`design.py` fits C20, C40 and C60 as **10 µF** with R20/R40/R60 unchanged at 10 kΩ, which gives
a corner of **1.6 Hz** into 10 kΩ against the restated E-11 limit of **<= 2 Hz**. That is
ECO-EEG-027 and it is implemented. The 1 µF part and its 15.9 Hz corner are the superseded
Rev A value and appear here only as history: 15.9 Hz would have removed the envelope of a
speech signal, which is why the change was cut. T12d records the as-built corner, expected
near 1.6 Hz.

Without the marker path, every latency in the study's dataset carries a 4.4 ms bias -- the same
order as the 2 ms N100 tolerance RFQ section 9.2 sets for the OpenBCI Cyton comparison.

### 2.4 BOM, FIX-02

| Ref | Qty | Description | Reference part |
|---|---|---|---|
| RL201, RL202 | 2 | **47.0 Ω** 1 % 1 W non-inductive | Bourns PWR221T-30-47R0F |
| U201 | 1 | Onset comparator | TI TLV3201AIDBVR |
| R201 | 1 | Marker attenuator top leg, **1.30 kΩ** 0.1 % 25 ppm (derived, section 2.3) | Vishay TNPW0603 series, expected order code **TNPW06031K30BEEA** |
| R202 | 1 | Marker attenuator bottom leg, **2.00 kΩ** 0.1 % 25 ppm (derived, section 2.3) | Vishay TNPW0603 series, expected order code **TNPW06032K00BEEA** |
| R203 | 1 | Threshold PWM top leg, GP15 to the threshold node, **10.0 kΩ** 0.1 % 25 ppm (derived, section 2.3) | Vishay **TNPW060310K0BEEA** (AVL-EEG-017 row 126) |
| R204 | 1 | Threshold bottom leg, node to M2 ground, **10.0 kΩ** 0.1 % 25 ppm (derived, section 2.3) | Vishay **TNPW060310K0BEEA** (AVL-EEG-017 row 126) |
| R205 | 1 | Comparator input series resistor, RL201 hot to U201 non-inverting, **10.0 kΩ** 0.1 % 25 ppm (derived, section 2.3) | Vishay **TNPW060310K0BEEA** (AVL-EEG-017 row 126) |
| C201 | 1 | Threshold low-pass, across R204, **220 nF 50 V X7R 0603** (derived, section 2.3) | any qualified X7R; the capacitor sets τ only, and its tolerance does not enter the threshold |
| M2 | 1 | Fixture controller | Raspberry Pi Pico |
| -- | 1 | I2S DAC module | PCM5102A breakout |
| -- | 1 | Headphone amplifier module | TPA6132 breakout |
| -- | 2 | Coupler driver, 13 mm mylar | generic 8 Ω 0.5 W |
| -- | 2 | Reference electret with preamp | PUI Audio POM-2735P-R class |
| -- | 1 | Class 2 acoustic calibrator, 94.0 / 114.0 dB at 1 kHz | Reed R8090 or Extech 407744 class |
| -- | 2 | Couplers **FIX-02/A** and **FIX-02/B** | MJF PA12 + TPU 85A lip, printed from the FIX-02 STL set |
| -- | 1 | 3.5 mm TRS plug, gold, moulded | Neutrik NYS231BG |
| -- | 1 | Enclosure | Hammond 1590B |

**Four lines were added on 2026-09-02 with the comparator threshold**: R203, R204, R205 and
C201. Section 2.3's superseded paragraph estimated the commanded route at "one resistor and
one capacitor"; it is four parts, and the count is corrected here rather than left to be
discovered when the box is built. All three resistors are the same **TNPW060310K0BEEA** that
this fixture already buys sixteen of at RB1-RB16 and one of at RP1, so the threshold network
adds no new part number at all -- which is the opposite of what a 20.0 kΩ pair would have
done, since **TNPW060320K0BEEA** is a constructed code nobody has confirmed. C201 is an
unqualified X7R on purpose: it sets the time constant and it is not in the ratio, so its
tolerance cannot reach the threshold.

The two attenuator resistances are **derived** in section 2.3 from the +/-1.0 V the
marker has to deliver and the 3.300 V rail it is delivered from, and they are not open.
The two order codes are **constructed** from the value-coding rule the four TNPW0603
part numbers already in this document follow -- `TNPW0603` plus a four-character value
code plus `B` for 0.1 % plus `EEA` for the reel -- and `1K30` and `2K00` are the
standard codes for those two values. *They have not been checked against a
distributor's stock list.* They are stated as the expected order codes so that a buyer
can raise the line and confirm it in one step; if the code is wrong the resistance is
still right, which is the opposite way round from an invented part number.

The couplers are printed from `fixtures/stl/FIX-02A_voice_coupler_body.stl` and
`FIX-02B_room_coupler_body.stl`, with their TPU 85A lips as separate parts --
`FIX-02A_sealing_lip` and `FIX-02B_sealing_lip` -- because MJF prints one material per
build. Section 8.9 dimensions them and states the one thing about FIX-02/A that is not
a fit but a proposal.

---

## 3. FIX-03 -- flashing and provisioning fixture

### 3.1 The decision, stated

**Modules are flashed and provisioned in situ, on the assembled carrier, before the POD-P1 lid
goes on.** Flashing loose DevKitC-1 modules on a tray is cheaper per module and wrong: it
breaks the binding between the eFuse state, the ATECC608B serial, the calibration constants and
the board serial, which is the whole point of RFQ section 9's opening sentence about device
identity not becoming a confound.

### 3.2 The USB path, and the one that must not be used

The ESP32-S3-DevKitC-1 has two USB-C connectors. They are not interchangeable here.

| Connector | On the module | On the carrier | Use at end of line |
|---|---|---|---|
| **UART** port, via the on-board USB-to-UART bridge on GPIO43/44 | yes | GPIO43/44 also reach J26 pins 3 and 4 | **This is the flashing port.** esptool at 921600 baud, `--before default_reset`. It carries the auto-reset circuit, DTR and RTS to EN and IO0, on the DevKit itself |
| **USB** port, native OTG on GPIO19/20 | yes | GPIO19/20 are J7 positions 19 and 20 and run to J10, the ADuM4160 device side | **Do not use.** Plugging it parallels the isolator's device-side D+/D- with a second host |

The module is reached through the MP-01 opening with the lid off.

Rules the manufacturer must be given, because both are non-obvious:

1. The fixture's UART-port pigtail and the J26 pogo block must never be connected at the same
   time. Both drive GPIO43/44, and two drivers on one pair is a diagnostic that takes an
   afternoon to find.
2. The isolator module's host USB-C must be unconnected during flashing.
3. The DevKitC-1's own USB-C connectors are on the **non-isolated** side of the barrier. They
   are factory-only. T18 checks that the closed POD-P1 gives a participant access to neither
   (E-23, S-03).

**The carrier's J26 is console and recovery only and cannot enter download mode**, because
GPIO0 is LED_SR_LATCH (ECO-EEG-009) and J26 way 6 is the spare way NC_GPIO0. Boot-mode entry is
the DevKit's own auto-reset sequence over the UART bridge. Any procedure that describes a relay
sequence on GPIO0 and EN at J26 is describing hardware that does not exist; ASM-EEG-007 section
6.1 is corrected to match. The DevKitC-1's own BOOT and EN buttons remain the manual fallback
and are reachable with the lid off.

### 3.3 Fixture build

A printed PA12 nest holding the **150.0 x 130.0 mm** carrier on its four M3 holes at (5, 5),
(145, 5), (5, 125) and (145, 125). The nest is released as
`fixtures/stl/FIX-03A_carrier_nest.stl` and its STEP twin (section 8.9); its outline and its
hole pattern are taken from `tools/design.py`'s `BOARD_W` and `BOARD_H` rather than typed
here, which is what section 0.2 item 1 asks for. It carries:

- a right-angle USB-C pigtail on a sprung arm reaching the DevKitC-1 UART port;
- a six-pin pogo block (P75-B1 pins) on J26 for DVDD3V3 sense, DGND, UART_TX, UART_RX,
  RESET_EN and the NC_GPIO0 spare way, used for the console capture when the pigtail is
  unplugged;
- a barcode scanner reading the board serial from the carrier label;
- a powered USB hub so one host PC can run several nests;
- no keys, no secrets, and no ability to sign anything.

Measured budget, calculated from a 16 MB flash at 921600 baud: about 40 s to write the image,
about 30 s for the provisioning steps, about 2 minutes per unit including handling. One station
covers 50 units only if flashing overlaps the unattended part of the test flow; the station plan
lives in TST-EEG-004 section 11, not here.

### 3.4 How the signing key stays away from the manufacturer

F-19 says the manufacturer never holds the signing key. That is achievable, and it is worth
setting out the sequence because it is easy to get wrong in a way nobody notices until a fleet
is unrecoverable.

| Step | What crosses to the manufacturer | What never does |
|---|---|---|
| Release build | Application, bootloader and partition images **already signed** in Brussels, plus a SHA-256 manifest and a detached signature | The ECDSA/RSA secure-boot **private** key |
| eFuse burn (Phase 2 onward) | The **public key digest** for SECURE_BOOT_DIGEST0 | anything secret -- a digest is public by construction |
| Flash encryption (Phase 2 onward) | Nothing. The key is generated **on the device** at first boot in Release mode and is never readable | The flash encryption key, which does not exist off-chip |
| ATECC608B provisioning | The programme's provisioning script, which contains no secrets | The device P-256 private key, generated inside the ATECC by GenKey and never exported |
| Output | Public key PEM, ATECC serial, key fingerprint, calibration constants, flash log | -- |

The public-key fingerprint is defined once, in FW-EEG-001 section 7 -- the first 8 bytes of
SHA-256 over the 64-byte uncompressed public key, printed as 16 uppercase hex characters in
four groups of four -- and this document cites it rather than restating the rule.

**On the two Phase 1 prototypes no eFuses are burned.** Secure boot and flash encryption are
enabled from Phase 2. The prototypes run unsigned images so the firmware volunteer can iterate,
TST-EEG-004 T25 is marked "Phase 2 onward" and is not a Phase 1 gate, and FIX-03 in Phase 1
therefore flashes, provisions and logs but burns nothing.

From Phase 2 the order matters. The secure-boot digest burn is irreversible and is done **after
T5 to T17 have passed and before T18**, so that a unit failing a functional test is still
reflashable. Until that point the unit runs a programme-supplied TEST-MODE image with the
security eFuses not yet burned; that image's SHA-256 is recorded in the unit's record so a
deferred security step is a tracked state and not a blank field.

Burn SECURE_BOOT_EN, SPI_BOOT_CRYPT_CNT and DIS_DOWNLOAD_MANUAL_ENCRYPT. Leave UART download
mode enabled but in secure download mode, so F-20's field update and a Brussels recovery remain
possible while flash readback does not. Read the eFuse summary back and file it: that readback
is the only evidence F-19 is actually satisfied.

A manufacturer can reflash any image the programme has signed. They cannot produce a new image
that boots. That is the whole security property, and it costs them nothing.

---

## 4. FIX-04 -- harness and isolation-barrier fixture

Rev B splits the helmet cable in two (ECO-EEG-014), removing the worst hazard the v1 risk work
found: eight 74HC595 drive lines sharing a bundle with eight screened electrode pairs. The
harness is still built by hand, twice per kit, and nothing in v1 tested it at all.

### 4.1 Heads

The three harness heads are **FIX-04/D** in TST-EEG-004 section 6.1, which calls them the
harness continuity and pull heads and points them at WH-EEG-008 section 9, steps H1 to H10.
An earlier draft of this revision said that table gave them no letter; it does. Inside
FIX-04/D the three heads keep their descriptive names, because they are named by the cable
they mate. The bare letters H-A, H-B and H-C used in that draft are withdrawn (section 0.1).

| Head | Mates | Conductors |
|---|---|---|
| 12-way electrode head | Electrode cable, both ends | 12: E_Fz, E_Cz, E_Pz, E_C3, E_C4, E_T7, E_T8, E_F7, REF_L, REF_R, BIAS_EL, HARN_SHIELD |
| 10-way light head | Light cable, both ends | 10: LED1-LED8, LED_V, LED_GND |
| EMG head | EMG snap lead to DIN 42802 plug | 1 each, 3 leads |

The lettered sub-assemblies of FIX-04 are TST-EEG-004 section 6.1's:

| Sub-assembly | What it is | Steps |
|---|---|---|
| **FIX-04/A** | 1.000 Ω 0.1 % 0.5 W shunt pigtails, RSH1 and RSH2, on JST PHR-2 bodies with SPH-002T-P0.5S contacts, in the J13 and J24 lines. Vishay Y0785 class | T00, T3, T4, T21 |
| **FIX-04/B** | Isolation-barrier insulation head: a USB-C plug bunching shell, VBUS, D+ and D- on the ADuM4160 host connector, against the applied-part group | T20 |
| **FIX-04/C** | 100 kΩ 0.1 % screened measuring resistor and the protective-earth lead | T23 |
| **FIX-04/D** | The three harness heads above -- 12-way electrode, 10-way light and EMG -- with the 24-channel relay scanner card that switches them | WH-EEG-008 section 9, steps H1 to H10 |

The 12-way and 10-way heads are built from the same Harwin housings and contacts as the harness
itself, so the jig proves the real mate and not a laboratory approximation. A 24-channel relay
scanner card, controller M3, switches every conductor to the DMM in turn for the continuity and
insulation matrix, and to the insulation tester for FIX-04/B. Its firmware and its host
protocol are section 8; its board data is released at `fixtures/pcb/FIX-04/` on the same terms
as FIX-01's, and section 8.8 says what is and is not in it.

**The scanner card's outline, ratified on 2026-09-02.** Section 1.9 gives FIX-01 a full
outline with its stack-up, its holes and its zones, and this section gave FIX-04 a pointer to
a directory. That asymmetry is closed here. Every value below is **read back from the released
`fixtures/pcb/FIX-04/FIX-04-Edge_Cuts.gbr` and `FIX-04-NPTH.drl`**: nothing is invented, no
geometry moves and no board is re-cut.

**120.0 x 80.0 mm, two-layer FR-4 Tg >= 150 °C, 1.60 mm, 1 oz copper, ENIG, green mask, white
legend both sides, IPC-6012 class 2 and IPC-A-600 class 2, minimum track and clearance
0.20 / 0.20 mm. Four M3 non-plated holes, 3.2 mm finished, at (5, 5), (115, 5), (5, 75),
(115, 75), 6.0 mm keep-out. Origin bottom-left, Y up. Zones: scanner matrix x 0.0-85.0, logic
and entry x 85.0-120.0, y 0.0-80.0 both.**

**Writing it here is half the edit, and the other half is not this document's to make.**
`tools/fixture_gen.py` carries `source="this file; JIG-EEG-009 section 4.1 gives the card no
outline"` at line 119 and prints that string verbatim into `FIX-04_constraints.txt` line 20,
which is the file a layout contractor is handed; it also carries a "NOT in JIG-EEG-009"
comment at line 107. Until those are changed to name this section, `--pcb` is re-run, and
`fixtures/MANIFEST.json` has its bytes and sha256 updated for `FIX-04_constraints.txt` and
`README_fixture_pcb_data.txt`, the document and the released data flatly contradict each other
rather than merely differing. **The four artwork and drill files do not change and must not be
listed as changing**: only `cap` reaches silkscreen and the zone note is a constraints-file
string, so neither `FIX-04-Zoning.gbr` nor `FIX-04-F_Silkscreen.gbr` moves. The generator and
the released fixture data are the tools owner's; this document states what has to happen to
them and does not reach into them. The `.docx` and `.pdf` renditions of this document are
regenerated in the same change, because those are what a manufacturer is issued.

**The relay grid is NOT mandated, and the reason is the same one this document gives
everywhere else: the datasheet is not open.** `fixture_gen.py`'s zone note says "24 DPDT
relays, four rows of six"; it should say "24 DPDT relays, grid set at layout (constraints
section 5 d), instrument bus and common bus", and the constraints file should carry the four
bullets below **as its rule 5(d)**. What is stated is the constraint and not the answer, with
the arithmetic anyone can re-run when the datasheet arrives:

- **Creepage is charged on BOTH axes.** Rule 5(a) binds every 500 V conductor pair, and the NO
  pads of two vertically adjacent relays are such a pair, so the column pitch is land width
  + 3.0 mm **and** the row pitch is land height + 3.0 mm. An earlier form of this ruling
  charged 3.0 mm on the column pitch and nothing on the row pitch; charged consistently, the
  four-columns-of-six grid it prescribed needs 6 x 13.6 = 81.6 mm of height on an 80.0 mm
  board and fails by 1.6 mm.
- **The usable relay band is x 0.0-85.0 by y 10.6-80.0, that is 69.4 mm and not the full
  zone.** J401, J402, J403 and J407 sit at y = 6.0 with footprints spanning x 6.4-86.14,
  y 4.4-7.6 -- J407's footprint crosses into the logic zone -- and 3.0 mm of creepage must
  stand off them. The M3 keep-outs at (5, 5) and (5, 75) take both left-column corners.
- **At the assumed 10.0 x 7.0 mm envelope every candidate grid closes.** Six across by four up
  needs 6 x 13.0 = 78.0 mm by 4 x 10.0 = 40.0 mm, leaving 7.0 mm and 29.4 mm to spare.
- **The land each grid can carry**, at the 10:7 aspect assumed here: six columns of four, up
  to 11.2 x 7.8 mm; four columns of six, up to 12.2 x 8.6 mm; five columns of five, up to
  14.0 x 9.8 mm. Five of five carries the largest part and is the grid to reach for if the
  datasheet is big. **It is not fixed here.** The grid is chosen when the Omron G6K-2F-Y
  datasheet is opened, which is the same datasheet section 1.9 says FIX-01's outline turns on.

**The acceptance number is 137 mm², and 160.8 mm² is superseded on this board.** The area
budget in `fixture_gen.py` computes max_env = (5760 - 1901.16) / 24 = **160.8 mm²** against the
70.0 mm² assumed envelope, and that figure is real but it is **area only: it charges no
creepage**. On the one card in this package with a 3.0 mm rule the binding constraint is grid
fit, not area, and the best grid caps the land at about **137 mm² (14.0 x 9.8 mm)**. A layout
contractor handed 160.8 mm² as an acceptance limit would go looking for a part 17 % too big.
160.8 mm² stands as the area-only figure and is not the number the datasheet is checked
against here.

**Logged, not settled, and it is a safety question rather than a layout one.** A G6K-class
signal relay's own COM-to-NO pin spacing is well under 3.0 mm, so rule 5(a) as written cannot
be met inside the relay package. Either 5(a) is a board-level rule about inter-device
conductors, or the fitted relay is not rated for the 500 V duty. This is the one fixture where
a flashover reaches an operator, so it belongs to the programme safety review that owns
RISK-EEG-011 and adopted the pollution-degree-2 clearance table, and not to this section. **If
the ruling is part-level, the relay selection in AVL-EEG-017 changes and the section 6.1 relay
line changes with it, and the rule-5(d) placement text must not be released to a layout
contractor ahead of that ruling.** It is carried in section 7.

**Who signs.** The outline block above and the section 6.1 price and totals are this
document's owner's to apply -- they are read back from released data and derived from a rate
already in section 6.1, no geometry changes and no signature is needed. **What needs a
signature is the rule-5(a) ruling above**, from the programme safety review.

**Twenty-four channels for twenty-five conductors, and how that is resolved.** The three
heads above carry 12 + 10 + 3 = **25** conductors between them and the card has 24 relays.
Nothing in Rev B noticed. The resolution taken here is that the **EMG head is paralleled onto
channels 1 to 3**, with the rule that **the electrode head and the EMG head are never mated at
the same time** -- which they never need to be, because WH-EEG-008 section 9 tests one cable
at a time. The rule is on the board legend, not only in this paragraph. Channels 23 and 24 are
left spare on a two-way header so that a conductor needing its own path during a diagnosis has
one. The alternative, a fourth shift register and eight more relays, buys a case that does not
arise. If a future step does need all three heads live together, that is where to spend.

### 4.2 Tests and limits

**The harness electrical tests are WH-EEG-008's, not this document's.** Package v1 specified
them twice with different limits, which is how a 1000 V AC dielectric test that exists in no
other document ended up in Rev A of this file. The limits, the sequence and the record format
for continuity, all-pairs isolation, 500 V DC insulation resistance, crimp pull-out, assembly
pull and the WH-09 barrier isolation are **WH-EEG-008 section 9, steps H1 to H10**; FIX-04
supplies the 12-way and 10-way mating heads, the EMG head and the scanner that make those steps
executable, and adds nothing to them. H10 is inside that range and not outside it: it is the
only 500 V DC test on the WH-09 pigtail that crosses the barrier, and FIX-04's insulation-test
lead set is what executes it. The order of WH-EEG-008 section 9 is load-bearing: the cable is
tested before the LED terminations are made, because 500 V DC would destroy the LEDs and would
put 500 V onto the ADS1299 inputs through the series resistors.

The one test FIX-04 owns is the barrier measurement on the assembled unit:

| Test | Method | Limit | Record |
|---|---|---|---|
| **T20** isolation-barrier insulation resistance, assembled unit, battery disconnected | **500 V DC, 60 s** from the host-side group (shell, VBUS, D+, D- shorted together at FIX-04/B) to the applied-part group (J14.1 to J14.11 and J15, J16, J17 shorted together) | >= 1 GΩ, or the value recorded for that module type at T00 where the module carries a cross-barrier Y-capacitor | applied voltage, measured resistance, dwell, RH, module type and lot |

**There is no per-unit hipot, and Rev A of this document was wrong to specify one.** The
2500 V AC station it described would have been built, would have cost about €900 in tester
alone, and would have stressed a certified barrier on every unit for no evidential gain. The
2.5 kV RMS type test is the **module supplier's certificate**, collected once at incoming
inspection (TST-EEG-004 T00) and never repeated per unit; the per-unit routine evidence is the
500 V DC insulation-resistance measurement above. On failure the unit is quarantined: do not
repeat the test and do not increase the voltage.

The barrier requirement of S-03 -- at least 2.5 kV RMS with creepage at least 8 mm -- lives
entirely on the ADuM4160 module and on the carrier's isolation keep-out, whose coordinates and
copper rule are stated once in DSN-EEG-003 section 3.3 and are not restated here. The keep-out
is verified from the artwork once per routed Gerber revision, not per unit. The purchased
isolator module's own creepage must be inspected and its isolation certificate filed at
incoming inspection -- the fixture cannot make an uncertified breakout compliant, and no safety
engineer has yet reviewed any of it.

One live non-conformance belongs with this fixture because it is the head that mates the
connector. The named isolator module presents **USB-B** and RFQ E-24 asks for USB-C. The
interim answer is a short USB-B-to-USB-C panel pigtail, **WH-09**, until an isolator module
with a USB-C host connector is qualified; FIX-04/B mates whichever connector the fitted
module actually presents and the unit record states which. This is stated as unresolved, not as
settled.

### 4.3 Leakage current, and a calculated figure the programme must act on

FIX-01/A in the open position, FIX-01/B and a lead to protective earth present the **fourteen**
patient terminations for TST-EEG-004 **T23** (leakage current at the applied parts, S-02):
eight scalp electrodes, two ear references, one bias lead and three EMG leads. The two EOG
spares are not fitted in a standard build and are not among them. The measuring network -- a
100 kΩ 0.1 % screened resistor and the protective-earth lead -- is **FIX-04/C** in TST-EEG-004
section 6.1, and this document builds it as a FIX-04 sub-assembly (section 4.1). An earlier
draft of this revision called it an instrument and declined to build it; that was wrong. The DMM that reads
the resistor is an instrument and is not designed here.

One number belongs here because the fixture is where it would be discovered, and it must be
read as a failure and not as a margin. In single fault, with one BAV99 clamp shorted, AVDD
(+2.5 V) reaches an electrode through the series resistor. At the **68 kΩ** now fitted that is
2.5 V / 68 kΩ = **36.8 µA**, calculated, against the S-02 single-fault limit of 50 µA DC:
**the limit is met in the design**. *Corrected 2026-09-02. This passage read "2.5 V / 47 kΩ =
53.2 µA ... S-02 is not met", with ECO-EEG-024 named as an unapplied fix and the prototypes
said to be built at 47 kΩ. ECO-EEG-024 is applied in `tools/design.py`; the resistor changed in
the design before any prototype was built, so the 53.2 µA figure is the superseded one.* The
change moves the corner to 234 Hz so that the loss at 100 Hz becomes 0.75 dB, which is why
**E-10 sits at its +/-1.0 dB branch at the fitted 68 kΩ and was +/-0.5 dB at 47 kΩ**; both
states are stated together every time either is quoted. It also raises Johnson noise to
0.28 µV for a total of 0.31 µV, still well inside E-03. The arithmetic behind those figures
lives in RISK-EEG-011 section 4, **which has not yet been restated against the applied ECO**.

**Met in the design is not met on a unit, and it is not signed off.** 36.8 µA is calculated;
no board exists and no measurement has been made, and this fixture is what will make it. The
disposition belongs to RISK-EEG-011's SR-01 and the safety review of RFQ 9.2, not to a fixture
document, and **no safety engineer has reviewed it** (DESIGN_FACTS section 8, item 1). It is
stated here so that a T23 result at or above the limit is understood on the line rather than
argued about -- and so that a unit found with 47 kΩ fitted is recognised as the
non-conformance it would be.

---

## 5. Calibration of the fixtures themselves

A fixture that is not calibrated produces numbers, not measurements. RFQ section 9's argument
-- that device identity must not become a confound -- collapses if fixture drift cannot be told
apart from unit-to-unit difference.

### 5.1 Traceability chain

```
SI volt and SI ohm
  -> national metrology institute
  -> ISO/IEC 17025 accredited calibration laboratory (12-month interval)
       -> 6.5-digit DMM  [asset number recorded in every unit record]
            -> FIX-01 U3 reference value          (6-month interval)
            -> FIX-01 A1, U1, A2 ratios           (6-month interval)
            -> FIX-01 RA/RB/RC/RS resistor values (12-month interval)
            -> FIX-04/A 1.000 R shunts            (12-month interval)
            -> FIX-02 47.0 R load values          (12-month interval)
                 -> per-unit channel gain, noise, lead-off and level constants

SI pascal
  -> 17025 laboratory (24-month interval)
       -> Class 2 acoustic calibrator, 94.0 dB at 1 kHz
            -> FIX-02 reference microphones       (12-month interval)
                 -> FIX-02/A and FIX-02/B drive constants
                      -> per-unit microphone gain and E-17 bleed figures

no SI chain
  -> FIX-01/E colorimeter: the reported quantity is a ratio of two channels of one
     sensor, so it needs repeatability and not traceability.  Verified against the
     printed reference card at every shift start; the card is replaced annually.
     T11 is an attribute test with a numeric trail and is described as one.
```

### 5.2 Schedule

| Item | Quantity calibrated | To what | Interval | Signed by |
|---|---|---|---|---|
| 6.5-digit DMM, function generator, current shunt, 500 V DC insulation tester, oscilloscope | full manufacturer spec | 17025 laboratory certificate | 12 months | CM quality manager; certificate copied to the programme |
| Acoustic calibrator | 94.0 / 114.0 dB at 1 kHz | 17025 laboratory certificate | 24 months | CM quality manager |
| FIX-01 A1, U1, A2 ratios | DC ratio at 5.0000 V | shift DMM, recorded value +/-0.02 % | 6 months | CM test engineer |
| FIX-01 U3 reference | 5.0000 V DC | shift DMM, +/-0.005 % | 6 months | CM test engineer |
| FIX-01 RA/RB/RC (48) and RS (16) | 4-wire resistance | recorded value, +/-0.05 % | 12 months | CM test engineer |
| FIX-04/A shunts | 4-wire resistance | recorded value, +/-0.05 % | 12 months | CM test engineer |
| FIX-01/E colorimeter head | R/G ratio on the green and red patches, and the dark reading | recorded values +/-2 % | 12 months, and verified every shift | CM test engineer |
| FIX-01 mating pins and 80 relays | continuity and per-relay reference read | self-test section 1.12 | every shift | operator |
| FIX-02 47.0 Ω loads | 4-wire resistance | +/-0.5 % of recorded value | 12 months | CM test engineer |
| FIX-02 coupler drive constants | 70.0 dB SPL at 1 kHz | reference microphone against the calibrator | 12 months | CM test engineer |
| FIX-02 marker delay constants | 0.33 ms and 0.029 ms | 100 MHz oscilloscope | 6 months | CM test engineer |
| FIX-03 | no metrology; software version, image SHA-256 and, from Phase 2, the eFuse readback pinned and logged | manifest match | every build lot | CM test engineer |
| FIX-04 relay scanner | contact resistance of all 24 paths | <= 0.1 Ω | 6 months | CM test engineer |
| FIX-04 open-circuit leakage | with no DUT fitted | below tester threshold | every shift | operator |
| Golden unit TIOV-B-0001 | T7 gain, T8 noise, T10 offsets | control chart; halt on gain drift > 0.2 % or noise drift > 0.15 µV | every build lot, and every shift start for FIX-01 | programme, unit retained by the programme |

Every calibration produces a dated record carrying the asset number of the instrument used,
and those asset numbers appear in each unit's calibration record. A fixture failing a scheduled
calibration puts every unit tested since its last good calibration into review, which is why
the divider is on a 6-month interval rather than 12.

---

## 6. Build cost and lead time for one fixture set

Indicative EUR, ex VAT, from distributor list prices at single-set quantity as at 2026-09-01.
**These are calculated estimates for the purpose of making RFQ-EEG-001 section 10's one-off
line quotable and comparable between bidders. They are not quotations, and no fixture has been
built.** Labour at EUR 55 per hour.

### 6.1 Materials and labour

| Item | FIX-01 | FIX-02 | FIX-03 | FIX-04 |
|---|---|---|---|---|
| Fixture PCB, 5-off minimum order | 120 | -- | -- | **72** |
| Relays (80 + 3 / 24) | 191 | -- | -- | 55 |
| Shift registers, controller, mux, colorimeter head | 38 | 25 | -- | 12 |
| Ratio networks, reference, op-amps (discrete Z-foil alternate) | 65 | -- | -- | -- |
| Precision resistors (48 reference + 16 series / loads) | 36 | 8 | -- | -- |
| Current shunts and JST pigtails (FIX-04/A) | -- | -- | -- | 40 |
| Audio modules, drivers, reference microphones | -- | 48 | -- | -- |
| Connectors, WH-KEY-01 shrouds, DIN plug set, screened multicore | 87 | 25 | 55 | 45 |
| Printed parts (MJF PA12 and TPU) | 60 | 90 | 70 | 20 |
| Enclosure, screening can, hardware, labels | 55 | 15 | -- | 20 |
| Barcode scanner, powered hub, USB-C pigtail | -- | -- | 85 | -- |
| Guarded insulation-test lead set, interlocked lid switch, FIX-04/B head, FIX-04/C measuring resistor | -- | -- | -- | 140 |
| **Materials subtotal** | **652** | **211** | **210** | **404** |
| Build labour | 6 h = 330 | 5 h = 275 | 3 h = 165 | 4 h = 220 |
| Verification and first calibration | 4 h = 220 | 3 h = 165 | 2 h = 110 | 3 h = 165 |
| **Fixture total** | **1 202** | **651** | **485** | **789** |

| Line | EUR |
|---|---|
| FIX-01 + FIX-02 + FIX-03 + FIX-04 | 3 127 |
| Common: cables, labelling, fixture manual, calibration record forms | 150 |
| Documentation and hand-over, 4 h | 220 |
| **One fixture set, materials and labour** | **3 497** |
| Instruments to be bought specifically: Class 2 acoustic calibrator | 280 |
| Instruments to be bought specifically: 500 V DC insulation tester, range to 100 GΩ, +/-5 % (Megger MIT525 class) | 1 400 |
| **One fixture set including programme-specific instruments** | **5 177** |

The three euro against Rev B are the eleventh TPIC6B595 of section 1.8 and the RP1 readback
resistor of section 8.4. They are in the table because a bill of materials that quietly does
not add up is worse than one that is three euro out.

**The FIX-04 board line moves from EUR 40 to EUR 72 on 2026-09-02, and all five dependent
totals move in the same edit.** EUR 40 was inconsistent with this section's only rate. FIX-01's
five-off line is EUR 120 for a 160.0 x 100.0 mm board, which is **EUR 0.15 per cm² of finished
board** over the five; 120.0 x 80.0 mm at the same rate is **EUR 72**. A five-off ENIG order is
setup-dominated, so 72 is the floor if the board is ordered alone and FIX-01's 120 is the
practical ceiling -- but section 6.3 already runs both boards through one 15-day layout leg and
one 10-day fabrication leg, so they go out on **one setup**, and on one setup the incremental
cost of the smaller board is area-proportional. That is why 72 and not a figure in between.
EUR 40 was below the floor. The five dependents are the FIX-04 materials subtotal 372 -> 404,
the FIX-04 fixture total 757 -> 789, "FIX-01 + FIX-02 + FIX-03 + FIX-04" 3 095 -> 3 127, "One
fixture set, materials and labour" 3 465 -> 3 497, and "One fixture set including
programme-specific instruments" 5 145 -> 5 177. A corrected cell without its totals is exactly
the defect the paragraph above names, so they move together or the edit does not happen. **It
is still a calculated estimate and not a quotation**; a real five-off quotation for both boards
from one fabricator replaces 120, 72 and all five totals at once, and it should be sought for
both boards together because the assumption EUR 72 rests on is that the setup is paid once.

**One-off engineering, which is not part of a fixture set and is not repeated.** Rev B priced
no design labour at all, which left the FIX-01 and FIX-04 boards as line items a bidder could
not quote: a five-off PCB order cannot be placed against a board that does not exist as data.
`fixtures/pcb/` now carries everything about both boards that this document determines --
outline, zoning, legend, drill and the full netlist -- and section 8.8 states what remains.
This is what remains, priced at the same EUR 55 per hour and on the same footing as every
other figure in section 6: **calculated estimates, not quotations, and nothing has been
built.**

| One-off item | Hours | EUR |
|---|---|---|
| FIX-01 schematic capture from `fixtures/pcb/FIX-01/FIX-01_netlist.txt`, 217 nets, 772 pins | 8 | 440 |
| FIX-01 land patterns for six part types, from the manufacturers' datasheets | 4 | 220 |
| FIX-01 placement, 83 relays and 77 precision resistors inside the section 1.9 zones | 8 | 440 |
| FIX-01 two-layer routing with the driven GUARD pour and the section 1.3 ratio-leg rule | 20 | 1 100 |
| FIX-01 DRC, fabrication outputs, IPC-D-356A netlist and review | 6 | 330 |
| FIX-04 schematic capture, land patterns, placement and routing, 61 nets, 208 pins | 13 | 715 |
| FIX-04 outputs and review, including the 3.0 mm 500 V DC creepage check | 2 | 110 |
| Controller firmware bring-up on the first boards: three roles, the pin map against the built board, and the M2 I2S block that section 8.6 leaves unwritten | 24 | 1 320 |
| **One-off engineering, first set only** | **85** | **4 675** |

The firmware itself is written and is in `fixtures/firmware/`, so it carries no design line;
what is priced above is bring-up on hardware that does not yet exist, and the I2S block, which
section 8.6 explains was deliberately not written against an unbuilt board. A second and third
fixture set repeat none of the 4 675.

The 5 kV hipot tester priced in Rev A of this document is **removed**: with the per-unit
2500 V AC station deleted (section 4.2) nothing in the flow needs one.

Assumed already owned by the manufacturer and **not** in the figure above: 6.5-digit DMM,
function generator, 100 MHz oscilloscope, bench supply with 0.1 mA resolution, host PC, EPA
workstation, and the three instruments TST-EEG-004 section 5 requires that no fixture here
replaces -- the audio analyser or calibrated interface of T17 and T28, the contact thermometer
or thermal camera of T3, and the 2.4 GHz receiver or SDR with near-field probe of T24. A bidder
who does not own a 6.5-digit DMM must say so, because the divider budget in section 1.3 is
built on one; a bidder who does not own the thermal camera or the SDR must price them, because
the figures above do not carry them and neither does the class 2 acoustic calibrator line.

### 6.2 How many sets

| Phase | Units | Recommended | Reason |
|---|---|---|---|
| 1 | 2 | 1 set | Single bench, sequential |
| 2 | 10 | 1 set + 2 parking stations | T14's 30-minute record and T9a's long record are unattended |
| 3 | 10 to 40 further kits, 25 to 50 in total | 2 sets + 6 parking stations | Attended time on FIX-01 becomes the constraint |

A parking station is power and USB only, about EUR 60 each, and is not a fixture.

### 6.3 Lead time, one set, from purchase order

| Activity | Working days | Note |
|---|---|---|
| Purchase of relays, precision resistors, semiconductors, colorimeter head | 5 | All stock lines |
| **Ratio networks** | **5 or 30-40** | 5 days for the discrete Vishay VSMP0603 Z-foil alternate; **30 to 40 days for a custom-ratio VHD200**. This is the only long-lead item in the set and it is the schedule driver -- build the first set with the discrete alternate |
| **FIX-01 and FIX-04 schematic capture, layout and review** | **15** | **One-off, first set only.** It has to finish before anything can be fabricated, so on the first set it is in series with the row below rather than in parallel with purchasing. Section 6.1 prices it |
| FIX-01 and FIX-04 PCB fabrication and assembly | 10 | Runs in parallel with purchasing on a second set; on the first set it follows the layout above |
| MJF PA12 and TPU printed parts | 7 | WH-KEY-01 shrouds, and the seven fixture parts of section 8.9 -- FIX-01/E manifold and carrier, both couplers with their TPU lips, and the FIX-03/A nest. All seven have STL and STEP files; the shrouds come from the MP-01 / POD-P1 print set |
| Acoustic calibrator | 10 | Stock item, calibrated |
| 500 V DC insulation tester | 10-15 | Stock item, calibrated |
| Build and wire all four fixtures | 3 | |
| Verification, first calibration, self-test records | 2 | |
| **Total, discrete Z-foil alternate, FIRST set** | **about 35 working days (7 weeks)** | The layout-then-fabricate leg is now the longest one at 25 days |
| **Total, discrete Z-foil alternate, second and later sets** | **about 25 working days (5 weeks)** | The 15 layout days are not repeated |
| **Total, custom ratio networks** | **about 45 working days (9 weeks)** | Unchanged: at 30 to 40 days the networks are still the driver, and the 25-day layout-and-fabricate leg finishes inside them |

The fixture set is on the critical path for the first article, not for fabrication. A
manufacturer can fabricate and assemble carriers while the set is being built, but no unit can
be released without it.

---

## 7. What this document closes, and what it does not

| Audit item | Status |
|---|---|
| Test jig is one sentence; no schematic, BOM, drawing or build instruction | Closed by sections 1 to 4 |
| 1000:1 divider has no design and no accuracy budget | Closed by section 1.3; fixture uncertainty 0.0320 % at k = 2, TUR 15.6:1 against the 0.5 % limit |
| The 10 µV point cannot meet 0.5 % in 60 s | Closed by section 1.4; the 0.5 % limit applies at 100 µV and 1 mV, the 10 µV point is a +/-5 % linearity check, and its uncertainty is 0.219 % at k = 2 for a 60 s record |
| Envelope group delay quoted two ways | Closed by section 2.3; 4.40 ms from 1/(Q·2π·f0) governs, and the √2/(2π f0) form is only valid at Q = 0.7071 |
| AGND_REF is not on the fixture's connector | Closed by section 1.2; J22 pin 2 in Rev B, dedicated lead FIX-01/C, dedicated label |
| T7 asks for 16 values, the jig reaches 8 | Closed by the map in section 1.5 |
| Two channels (SPARE1/2) have no source at all | Closed: Rev B protects them; FIX-02 drives SPARE1 with the onset marker |
| T10 cannot pass with the series protection resistor in circuit | Closed by section 1.6; two-point calibration, R_off extracted, 7.8 Hz mandated. *The resistor was 47 kΩ when this row was written and is 68 kΩ since ECO-EEG-024 (2026-09-02); the closure does not depend on the value, only on R_off being fitted rather than assumed* |
| Envelope onset compared against an undefined electrical onset | Closed by section 2.3; marker on SPARE1, group delay 4.40 ms calculated, spread is the acceptance |
| No flashing fixture or EOL flashing procedure | Closed by section 3; in-situ, the DevKit's own UART USB-C port, sequence stated |
| Signing key handling undefined | Closed by section 3.4 |
| No harness continuity or insulation test | Closed by section 4.2, which supplies the heads and defers the limits to WH-EEG-008 section 9 |
| Fixture naming incompatible between TST-EEG-004 and this document | Closed by section 0.1, which now transcribes **all seventeen** sub-assembly rows of TST-EEG-004 section 6.1, FIX-02/C, FIX-03/A, FIX-03/B and FIX-04/D included. An earlier draft of this revision carried twelve rows and had moved three letters onto other hardware; FIX-01/D is the common-mode network of section 1.11, the spare-channel head is FIX-01/G, FIX-01/F is the 1000:1 divider and FIX-02/D is the 47.0 Ω load and onset marker. FIX-04/H-D, H-A, H-B, H-C, CPL-V and CPL-R remain withdrawn. What is still open is hardware, not naming: **FIX-02/C is not built, priced or on the calibration schedule** (section 7) |
| E-11's AC-coupling corner was said here to be unmet | Closed by section 2.3; `design.py` fits 10 µF at C20, C40 and C60, the corner is 1.6 Hz into 10 kΩ, E-11 is restated as <= 2 Hz and is met. ECO-EEG-027 is implemented |
| Maximum acoustic output said here to have no T-number | Closed by section 2.1; it is TST-EEG-004 **T28**, a type test listed in TST-EEG-004 section 14 |
| The 100 kΩ leakage measuring resistor called an instrument here and a fixture in TST-EEG-004 | Closed by sections 4.1 and 4.3; it is **FIX-04/C** and this document builds it |
| This document renumbered TST-EEG-004's steps | Closed; every T-number here is TST-EEG-004 Rev C's, and where no step exists the fact is stated instead of a number being invented |
| A per-unit 2500 V AC hipot that TST-EEG-004 forbids | Closed by section 4.2; deleted, replaced by the 500 V DC T20 measurement, and the hipot tester removed from section 6 |
| T11 measured by LED current sense in one document and by colorimeter in another | Closed by section 1.7; TCS34725-class colorimeter head FIX-01/E, in the BOM at section 1.8, current sense dropped |
| Fixture keying invented its own shrouds | Closed by section 1.10; the fixture uses WH-KEY-01, and the SHR-xx-A identifiers are withdrawn |
| Nothing to price against in RFQ section 10 | Closed by section 6 |
| E-28 programming-header deviation | Closed by section 0.3; RFQ-EEG-001 Rev E E-28 is TP1-TP18 plus the J26 1x6 header, the 2x5 JTAG header is withdrawn, and no deviation remains |
| Three fixture controllers named and never specified: M1, M2 and M3 had no source, no command set, no framing and no host contract | Closed by **section 8**. FIXPROTO v1 is defined line by line, the firmware is written and is at `fixtures/firmware/`, and 154 host checks drive the real firmware against a model of the fixture. Two parts of it stay open and are below |
| The FIX-01 and FIX-04 boards were priced and scheduled and did not exist as data | **Closed except for the copper.** `fixtures/pcb/` carries the outline, zoning, legend, non-plated drill, the complete netlist (217 nets on FIX-01, 61 on FIX-04) and a constraints file. Section 6.1 now prices the layout and section 6.3 gives it 15 working days. What is not closed is the copper itself, and section 8.8 says why |
| Every printed fixture part was called for and none had geometry | Closed by **section 8.9**: seven parts, STEP and STL from one parametric model, at `fixtures/step/` and `fixtures/stl/`. The two coupler cavities are computed to 2.0006 and 3.4997 cm³ against the 2.0 and 3.5 cm³ of section 2.2 |
| The FIX-02/D onset-marker attenuator had a tolerance and a series and no resistance | Closed by **section 2.3**: R201 = 1.30 kΩ and R202 = 2.00 kΩ, derived from the +/-1.0 V required and the 3.300 V rail, exact in E96, 1.000 mA, and a Thevenin resistance that leaves the published 0.33 ms marker-path constant unchanged |
| **Ten shift registers driving 83 relays.** Rev B's section 1.8 listed ten TPIC6B595, which is 80 outputs, against 80 channel relays plus K101, K102 and K103 | Closed by arithmetic: eleven devices, U22 added, five outputs spare. Section 1.8 and the chain map in section 8.4 |
| **The FIX-01/E head put a second 1.0 kΩ in a loop that already had one.** Rev B's section 1.7 asked for a 1 kΩ per site "so each site draws the 1.3 mA the carrier actually drives"; R70-R77 are on the carrier and already set that current | Closed by section 1.7: the positions are kept and fitted with 0 Ω links. With the resistor fitted each site would have drawn 0.65 mA and the recorded R/G ratio would have been the ratio at a current no carrier drives |
| **Section 1.12 step 2 asked for a measurement nothing could make.** A multiplexer with nothing driving it reads whatever the node happens to sit at | Closed by **section 8.4**: RP1, a 10.0 kΩ 0.1 % switched readback pull-up, with the five node voltages calculated and the resolution of each stated |
| **Twenty-four scanner channels for twenty-five harness conductors** | Closed by section 4.1: the EMG head is paralleled onto channels 1 to 3 and never mated with the electrode head, a rule the board legend carries; channels 23 and 24 are spare |
| **The FIX-02/D comparator threshold had acceptance criteria and no network** | Closed by **section 2.3** on 2026-09-02: a PWM on GP15 at 125.000 kHz through R203 = R204 = 10.0 kΩ with C201 = 220 nF across the lower leg, full scale 3.300 x 10.0 / 20.0 = **1.6500 V** at 1.650 mV per count, commanded as `THR MV`. Settling 5.07 ms against 10 ms, ripple 0.727 % against 1 %, and no new part number: all three resistors are the TNPW060310K0BEEA this fixture already buys. The coupler-drive half is **not** closed and is below |
| **The FIX-04 scanner card was priced and never dimensioned** | Closed by **section 4.1** on 2026-09-02, which ratifies the released outline -- 120.0 x 80.0 mm, four M3 at (5, 5), (115, 5), (5, 75), (115, 75), the two zones -- read back from `FIX-04-Edge_Cuts.gbr` and `FIX-04-NPTH.drl`, and by **section 6.1**, which moves the board line from EUR 40 to EUR 72 with all five dependent totals. The relay grid is deliberately not mandated and the acceptance land is 137 mm² rather than the area-only 160.8 mm². What is not closed is the generator and the released constraints file, which still say the card has no outline, and the rule-5(a) ruling below |

Not closed, and deliberately so:

- **The host test tool does not exist.** Eleven of the thirty-one steps of TST-EEG-004 Rev C
  produce numbers only a decoder can read -- T7, T8, T9, T10, T12, T13, T14, T15, T16, T26 and
  T27 (TST-EEG-004 section 16, item 10). FIX-01 and FIX-02 present signals and read fixture
  state; they cannot produce a gain figure without the tool.
  That is a separate deliverable and it blocks T12 to T17. T6 is no longer blocked with it:
  the provisioning script exists as `firmware/tools/provision.py` and its ten steps are
  documented in FW-EEG-001 section 7.
- **S-02 is met in the design and is not signed off, and this fixture is still what measures
  it.** *Corrected 2026-09-02: this item read "S-02 is not met. Single-fault patient auxiliary
  current is calculated at 53.2 µA against a 50 µA limit", with ECO-EEG-024 held out as
  pending.* ECO-EEG-024 is applied: R1-R16 are 68 kΩ, the calculated single-fault current is
  **36.8 µA** against 50 µA, and E-10 moves from the +/-0.5 dB of the 47 kΩ build to the
  +/-1.0 dB branch. What stays open is what always was: the figure is calculated, no unit
  exists, and SR-01 is the electrical safety reviewer's, who has not started. The fixture can
  measure it; it cannot resolve it.
- **T11's three states are reachable; what is open is the resistance values that reach them.**
  This item read "T11's red state cannot be produced". It can, as of 2026-09-02: FW-D17
  replaced the unreachable `LOFF_STATP & LOFF_STATN` red term with a sweep of the positive-side
  comparator threshold, which is what a single-ended montage supports. The three colours are
  now three impedance bands, and FIX-01/A's reference resistors and relay matrix produce them
  directly. **What is still open is which resistances:** the two `COMP_TH` settings are the
  datasheet's endpoints rather than measured trip points, so T11's resistor values cannot be
  fixed until a unit is characterised. **Firmware owner, with E-27's owner in DSN-EEG-003
  section 11** (TST-EEG-004 T11 Note 3).
- **E-17 has a reference level and no method.** Section 2.2 states it; "maximum stimulus level"
  is undefined in every document in this package. It is listed as a type test in TST-EEG-004
  section 14 with no step number.
- **T28's artificial ear and class 1 sound level meter are not in this document.** TST-EEG-004
  section 6.1 puts the artificial-ear coupler inside FIX-02 and section 5 lists the sound level
  meter as an instrument for T28 only. Neither is in the FIX-02 bill of materials at section
  2.4 nor in the cost tables at section 6, so the one-off price quoted in section 6 is short by
  that coupler and that meter (section 2.1).
- **The isolator's host connector is USB-B where E-24 asks for USB-C.** The WH-09 pigtail is an
  interim answer, not a resolution (section 4.2).
- **The voice preamplifier module is not chosen.** It is specified by interface only
  (section 2.2).
- **The FIX-01 outline is provisional, and it is provisional on one datasheet.** The area
  budget computed by `tools/fixture_gen.py` puts the bill of materials at 60 % of the
  160.0 x 100.0 mm board of section 1.9, exactly at the working occupancy for a two-layer
  board of this density, and the largest relay land pattern the outline can carry is
  70.7 mm². The Omron G6K-2F-Y datasheet is not in this package. Whether this board closes
  at all turns on a number nobody here has looked up, and the margin is 1 %. The Hammond
  1590D has room for a larger board (section 1.9).
- **The fixture boards have no copper.** Everything else about them is released
  (section 8.8). Schematic capture, land patterns, placement and routing are a layout
  engineer's work, priced at 61 hours in section 6.1 and given 15 working days in section
  6.3. This is a scope statement, not a gap: it says who does the work and what it costs.
- **The coupler-drive electrical onset is not dimensioned, and is deliberately not guessed
  at.** The FIX-02/D threshold network itself is closed (section 2.3, and the table above),
  but section 2.3's source list feeds "47 Ω load / coupler drive" into one comparator and
  TST-EEG-004 T12b reports per envelope channel. No document in this package states the
  coupler drive in volts: it is a per-coupler constant set at calibration to give 70.0 dB SPL,
  and no coupler has been built or calibrated. **No second range is fitted**, because one
  cannot be dimensioned without that number and an attempt to fit one lands 2.4x outside the
  ripple criterion the main range is checked against. It is measured when a FIX-02/A or /B
  coupler is first calibrated. The closed half still needs its signatures: **the FIX-02
  fixture designer with TST-EEG-004's owner, the schematic and safety reviewer for the
  J27.3 HP_GND-to-M2-ground bond, and this document's owner for the `THR MV` verb.**
- **Rule 5(a)'s 3.0 mm is not ruled part-level or board-level, and the FIX-04 relay grid waits
  on it.** A G6K-class signal relay's own COM-to-NO pin spacing is well under 3.0 mm, so the
  rule as written cannot be met inside the relay package: either it is a board-level rule about
  inter-device conductors, or the fitted relay is not rated for the 500 V duty. FIX-04 is the
  one fixture where a flashover reaches an operator. **The programme safety review that owns
  RISK-EEG-011 and adopted the pollution-degree-2 clearance table rules on it**; if the ruling
  is part-level, the relay selection in AVL-EEG-017 changes and the section 6.1 relay line
  changes with it, and section 4.1's placement text must not go to a layout contractor first.
- **The FIX-04 outline is ratified in this document and not yet in the released data.**
  Section 4.1 now carries the outline, but `tools/fixture_gen.py` line 119 still sources it to
  "this file; JIG-EEG-009 section 4.1 gives the card no outline" and prints that sentence into
  `FIX-04_constraints.txt` line 20, and the zone note still names a grid. Until the generator
  is corrected, `--pcb` re-run and `fixtures/MANIFEST.json` re-hashed for the two text files,
  the document and the data a contractor is handed contradict each other. **Tools owner**, in
  the same change as this issue.
- **The M2 I2S transmitter is not written** (section 8.6, section 8.8). The command layer
  refuses the tone verbs with `UNSUPPORTED` rather than reporting a start time for a tone
  nobody played. It is priced as bring-up in section 6.1.
- **Whether U3 floats is not settled.** Section 1.2 gives K101 and K102 as "DPDT polarity
  reversal" with no contact assignment; the released netlist implements the four-changeover
  reversal the section 1.3 uncertainty budget takes credit for, and that requires the
  reference and its supply to float against the fixture common. Section 1.2 does not say
  whether U3 is on an isolated rail. **This is the one thing in the FIX-01 netlist a
  schematic reviewer must settle before capture** (section 8.8).
- **FIX-02/A's mouth diameter is a proposal.** The coupler is modelled with a 10.0 mm mouth
  and a compliant TPU lip. What the lip seals against is the boom capsule with its
  windscreen removed, and neither the capsule (AVL-EEG-017 K10 buys a class, not a part) nor
  the boom nose that carries it (HM-07A/B, no released geometry) fixes a diameter. **The
  programme decides once the boom is drawn and the capsule is chosen** (section 8.9).
- **No fixture has been built or measured, and no safety engineer has reviewed this design.**
  Every figure in sections 1.3, 1.4, 1.6, 2.3, 4.3, 6, 8.4 and 8.9 is calculated, modelled or
  estimated and is labelled as such. No firmware image has been built for an RP2040 and none
  has been run on one; what has been run is 154 host-side checks against a model of the
  fixture (section 8.8).

---

## 8. Fixture controller firmware, the host protocol, and the released fixture data

**Why this is section 8 and not section 5.** Other documents in this package cite this one
by section number -- TST-EEG-004, ASM-EEG-007 and RFQ-EEG-001 all quote "JIG-EEG-009 section
6.1" or "section 1.12" -- so renumbering to put new material in the middle would break every
one of those citations to gain nothing. New sections go at the end.

### 8.1 What was missing

Section 1.8 lists "M1 | 1 | Fixture controller, USB CDC, no radio | Raspberry Pi Pico
(RP2040)". Section 2.4 lists M2 the same way, and section 4.1 names "a 24-channel relay
scanner card, controller M3". Rev B said nothing else about any of them: no source, no
command set, no framing, no host-side contract, and no line in the section 6.1 cost table.

That is a bigger hole than it looks. Section 0.1 requires FIX-01/A to be "relay-switched,
state readable by the host tool"; T7's fourteen unattended minutes depend on driving all
sixteen channels through the matrix at once; section 1.12 step 2 requires all eighty relays
to be read back through U20 against their own reference resistors; T11 needs the TCS34725
read over I²C. None of that can be built from a part number.

This section is the contract. The firmware that implements it is in `fixtures/firmware/`,
it is hand-written C for the RP2040, and section 8.8 says exactly what has and has not been
run.

### 8.2 FIXPROTO v1

**One request line, one response line, always, in order, with no unsolicited traffic after
the boot banner.** ASCII, terminated by LF, CR ignored, at most 160 characters in and 240
out. The link is USB CDC and the baud rate is ignored.

The DUT's own protocol is binary and framed (FW-EEG-001 section 6) because it carries a
50.7 kB/s sample stream. A fixture carries a few relay commands a second and has nothing to
gain from the same machinery, and two things to lose: an operator with a terminal emulator
cannot drive it, and a test engineer reading a log six months later cannot see what
happened. The status codes are deliberately the same shape as FW-EEG-001 section 6.2's --
one number, one keyword, one free-text tail -- so that moving between a unit log and a
fixture log is not moving between two vocabularies.

| Direction | Form |
|---|---|
| Request | `VERB [arg ...]` -- verbs and keyword arguments are case-insensitive, integers accept `0x` |
| Success | `OK VERB key=value key=value ...` |
| Failure | `ERR VERB <code> <KEYWORD> <free text>` |
| Informational | `# ...` -- **never** a response. Boot banner, `HELP`, `STATE` detail, the readback sweep and the one watchdog notice all use it |

The `#` rule is what lets a host match replies by arrival order without a sequence number,
and it is why the watchdog notice -- the only unsolicited line the firmware ever emits -- is
prefixed with it. A line beginning `#` sent *to* the fixture is a comment and is ignored, so
a command script can carry its own annotations.

| Code | Keyword | Meaning |
|---|---|---|
| 0 | `OK` | -- |
| 1 | `UNKNOWN_VERB` | not a verb in this role |
| 2 | `SYNTAX` | malformed, wrong argument count, or a line over 160 characters |
| 3 | `RANGE` | a value outside its stated range |
| 4 | `STATE` | right verb, wrong moment -- no coupler selected, colorimeter not initialised |
| 5 | `INTERLOCK` | refused for safety: HV armed, lid open, or inside the discharge dwell |
| 7 | `HARDWARE` | a bus did not acknowledge, or a sensor reported the wrong identity |
| 10 | `TIMEOUT` | an expected edge did not arrive |
| 11 | `UNSUPPORTED` | the verb exists in this protocol and not in this build -- the honest answer from a part that is not written |

An over-long line is refused **whole**: the firmware keeps discarding to the next newline, so
a truncated command can never be executed as a short one. A host that gets no response
within 2 s retries once and then reports, which is FW-EEG-001 section 6.2's rule and is
reused rather than reinvented.

**The comms watchdog is OFF at boot, and that is a decision.** T7 leaves the relay matrix
driving all sixteen channels for fourteen unattended minutes (section 1.1). A fixture that
dropped its relays because the host went quiet would abort the step it exists to serve. A
host that wants fail-safe behaviour for a particular step arms it for that step with
`WDT <seconds>`; when it expires the fixture returns to its safe state and says so on a `#`
line.

### 8.3 The verbs every fixture has

| Verb | What it does |
|---|---|
| `ID` | role, fixture, protocol version, firmware version, build hash, uptime |
| `ECHO ...` | echoes its arguments -- the link check, for the reason FW-EEG-001 gives `LOOPBACK` an opcode |
| `RESET` | returns the fixture to its safe state: every relay open, no source connected |
| `STATE` | the whole commanded state, as `#` lines then one `OK` |
| `WDT [s\|OFF]` | the comms watchdog above |
| `ERRS` | protocol errors counted since boot |
| `HELP` | every verb in this role with one line each |

**The safe state does not depend on firmware.** SRCLR on the TPIC6B595 chain is tied to the
controller's reset rail rather than to a GPIO, so a controller held in reset, unprogrammed
or crashed opens every relay with no code running. That is the one property of these
fixtures that must not be a software promise.

### 8.4 M1 -- the relay matrix, and the readback that section 1.12 needs

**The relay map is section 1.2's and no other.** Channel *n* owns K(5n-4) SRC, K(5n-3) RA,
K(5n-2) RB, K(5n-1) RC and K(5n) SHORT for n = 1 to 16; K101 and K102 are the polarity
commutator and K103 the SIN/CAL select.

**The chain.** Eleven TPIC6B595 devices, 88 outputs, 83 used and five spare (section 1.8).
U10 receives SER from M1, then U11 to U19, and U22 is last. Data shifted out first travels
furthest, so the firmware's first byte lands in U22:

| Chain byte | Device | Relays, bit 0 to bit 7 |
|---|---|---|
| 0 | U22 | K101, K102, K103, then five spare outputs that must be written zero |
| 1 | U19 | K73 to K80 |
| ... | ... | eight relays per device, descending |
| 10 | U10 | K1 to K8 |

One rising edge on RCK latches the whole chain, so `CHALL` is one relay event and not
sixteen -- which is what T7's simultaneous drive requires.

**Every mode change is break-before-make.** The five relays of a channel share one node.
Closing RB before SRC has opened would put the 5.0000 V reference across a 10.0 kΩ leg
through the divider for the operate time of one relay, and section 1.3's rule is that no
switch contact ever appears in a ratio leg. The firmware writes the all-open pattern, waits,
then writes the target: two latch events per change, and the host test counts them rather
than trusting a comment.

| Verb | What it does |
|---|---|
| `CH <1-16> [mode]` | one channel. Modes `OPEN SRC RA RB RC SHORT`, and the document's own names `SIN CAL 4K99 10K0 49K9` are accepted and mean the same relays. `SIN` and `CAL` also command K103, and the reply says so. Channel 11 accepts `OPEN` and `SHORT` only, because it is the BIAS output (section 1.5) |
| `CHALL <mode>` | all sixteen on one latch edge. Channel 11 is left open and the reply reports it |
| `SRC [OFF\|SIN\|CAL]` | K103 |
| `POL [A\|B]` | K101 and K102 together -- they are one commutator, and driving them separately reverses one side of the pair only. The 5 s dwell is the host's |
| `RLY <k> [0\|1]` | one raw relay, for fault-finding. It invalidates the cached channel mode rather than leaving it to be read back as a fact |
| `RLYMASK [22 hex]` | the raw chain. The five spare outputs must be zero |
| `SELFTEST ARM\|RELAYS\|DISARM` | the readback sweep below |

**The readback, and the part Rev B was missing.** Section 1.12 step 2 requires every relay
to be "verified through U20 against its own reference resistor, +/-1 % of the recorded
value". A multiplexer with nothing driving it reads whatever the channel node happens to sit
at, so as specified the step could not be performed. **RP1** closes it: one 10.0 kΩ 0.1 %
resistor from an M1 GPIO to the CD74HC4067 common, driven high only while a readback is
running and left high-impedance otherwise. The mux reads the relay-common node, so RS(n)'s
100 Ω is outside the measurement.

| Channel state | Node voltage against the 3.300 V rail | 1 % of the resistor, in millivolts and in ADC counts |
|---|---|---|
| OPEN | 3300.0 mV | -- |
| SHORT | 0.0 mV | -- |
| SRC, source OFF | 3300 x 18 / 10018 = **5.9 mV** | a contact check, not a measurement |
| RA 4.99 kΩ | 3300 x 4990 / 14990 = **1098.5 mV** | 7.33 mV, 9.1 counts |
| RB 10.0 kΩ | 3300 x 10000 / 20000 = **1650.0 mV** | 8.25 mV, 10.2 counts |
| RC 49.9 kΩ | 3300 x 49900 / 59900 = **2749.1 mV** | 4.59 mV, 5.7 counts |

The RP2040's ADC is 12 bits over 3.3 V, that is 0.806 mV per count, and the firmware
averages 64 conversions, so the +/-1 % band is six to ten counts wide at the worst position
and is comfortably resolved. *All six figures are calculated.* They are nominal, and they
include RP1's own tolerance and the 3.3 V rail, which is exactly why section 1.12 step 2
measures against the value **recorded at calibration** and not against the numbers above.
The firmware applies no limit at all: it reports the measured millivolts and the nominal
beside it, and the host tool owns the pass and fail.

**The sweep is interlocked, and the interlock is an admission.** `SELFTEST RELAYS` refuses
to run until `SELFTEST ARM` has been sent, and `ARM` prints a warning: with a unit fitted,
RP1 drives 3.3 V through 10 kΩ into a protected input. The controller cannot tell whether
the fixture is mated -- nothing on this fixture senses that -- so the interlock is a
procedural one made explicit rather than a claim that the hardware is safe in every state.
It disarms itself after 300 s.

### 8.5 M1 -- FIX-01/E

| Verb | What it does |
|---|---|
| `COL INIT` | reads the ID register, refuses unless it is 0x44, then sets 300 ms integration (ATIME 131 = 256 - 125 steps of 2.4 ms, section 1.7) and enables the ADC |
| `COL READ` | clear, red, green and blue counts, and R/G as an integer per mille |
| `COL GAIN [0-3]` | the gain, with a reply that says the head must be recalibrated after a change |

Two things the firmware deliberately does not do. It applies **no limit**: T11's 0.30, 3.0
and 0.6-to-1.7 bands are TST-EEG-004's and are applied by the host against values recorded
at calibration. And it refuses rather than guesses: a wrong address or a different sensor on
the breakout produces `ERR COL 7 HARDWARE` and not a column of plausible numbers.

### 8.6 M2 -- acoustic injection and the onset marker

| Verb | What it does |
|---|---|
| `DRV [OFF\|A\|B]` | one coupler driver, never both -- the two have different cavity volumes and different recorded drive constants, so a state with both driven has no calibrated meaning |
| `TONE <hz> <tenths_db> <ms>` / `TONE STOP` | a tone at a level in tenths of a decibel below digital full scale, the same unit as the DUT's own `SET_HP_LEVEL` |
| `BURST <hz> <tenths_db> <ms>` | a tone, then the fixture's own timestamp of the comparator's first edge |
| `MIC <A\|B> [navg]` | a reference electret, in millivolts |
| `MARK` | the U201 comparator output now |
| `THR MV <millivolts, 0..1650>` | set the commanded comparator threshold, 1.650 mV per count on the 1000-count PWM of section 2.3; replies `OK THR mv=NNNN permille=NNN`. **Power-on default `THR MV 165`, not zero**, so that `fix_m2.c`'s "marker is already high" path does not refuse every burst on a freshly booted fixture |

**`BURST` does not replace T12b and must not be read as if it did.** T12b measures the delay
between the DUT's envelope onset and the marker onset **on the DUT's own converter**, which
is the whole point of the marker: the comparison never crosses a clock boundary. `BURST`
reports the delay from the fixture's own t0 -- the first sample handed to the I2S peripheral
-- to the comparator's first edge, which is the fixture's own contribution and is what
section 5.2 calibrates every six months on a 100 MHz oscilloscope. Two independent numbers,
and a disagreement between them says which side moved. The edge is found by polling, so its
resolution is the loop period and not the microsecond it is printed in; the reply carries
`polled=1` so nobody mistakes it for a captured timestamp.

**What the marker does after its first edge, stated because it looks like a defect and is
not.** U201 compares the burst against a threshold, so during a tone burst its output
follows the tone and the R15/C15 pole averages the result to roughly the duty cycle. Only
the **first** rising edge is used -- T12b's quantity is (envelope onset sample - marker onset
sample) -- and the behaviour after it carries no meaning. A retriggerable one-shot would
make the marker a clean gate rather than a chattering one; it would also add parts to a
fixture whose burst waveform TST-EEG-004 has not yet fixed. It is left out and said out
loud.

**One open item lives here, and it is the I²S transmitter of section 8.8.** The other, the
comparator threshold, is **closed on 2026-09-02** in section 2.3: the threshold is commanded
from a PWM on GP15 through a 10.0 kΩ / 10.0 kΩ divider with 220 nF across the lower leg, full
scale 1.6500 V, and the verb is the `THR MV` row above.

**`THR <per mille of the 3.300 V rail>` is struck**, here and at its other statement in
section 2.3, in the same change and for one reason: the unit now names itself on the wire, and
a verb left in two places with two meanings is a host tool written to the wrong one. There is
no per-mille form of this verb. The reply carries the per-mille value as well as the
millivolts so that an operator reading a log can still see where in the range the fixture is
sitting, but **millivolts is what is commanded** and it is the only thing the fixture parses.
The firmware gains one HAL function for the PWM; nothing else in this section changes.

### 8.7 M3 -- the harness scanner and the 500 V gate

| Verb | What it does |
|---|---|
| `SCAN [1-24\|OFF]` | one conductor to the instrument, the rest on the common bus. Break-before-make |
| `SCANMASK [6 hex]` | a 24-bit pattern -- one write per row of the WH-EEG-008 H2 all-pairs isolation matrix |
| `HV [ARM\|SAFE]` | the 500 V DC gate |
| `LID` | the interlock switch |

This is the only fixture in the set that switches a voltage that can kill. WH-EEG-008 H4 and
H10 apply 500 V DC through this card, and a relay changing state under that voltage arcs its
contacts and can carry the test voltage somewhere the operator did not intend. Three rules,
enforced in firmware:

1. **While HV is armed, every switching command is refused** with `ERR ... 5 INTERLOCK`.
2. **HV will not arm with the lid open**, and if the lid opens while armed the firmware
   drops every channel to the common bus, disarms, and says so. It cannot open the tester's
   own contactor, so it does the two things it can.
3. **Switching is refused for a discharge dwell after `HV SAFE`.** The firmware enforces
   5000 ms. *That is a stated constant and not a measurement*: it has to be at least the
   time the fitted tester takes to discharge the cable capacitance it has just charged, and
   the Megger MIT525-class tester of section 6.1 is not in this package. It is one line in
   `fix_m3.c` and it is the number to check before the first H4.

None of that is a substitute for the interlock being wired. The firmware can only refuse a
command it is sent, and it cannot open a relay a stuck driver is holding closed.

### 8.8 What is released, what was run, and what was not

**Firmware, at `fixtures/firmware/`.** One source tree, three images -- `fix_m1`, `fix_m2`,
`fix_m3` -- with the role fixed at build time and not by a strap or a stored setting, because
a fixture that can be talked into being another fixture will one day drive FIX-04's 500 V
relay map with FIX-01's channel numbers. The whole hardware surface is seventeen functions in
`include/fixhal.h`, so nothing above that header touches a register.

`sh fixtures/firmware/test/run.sh` does two different things and it matters which is which.

* It compiles each of the three roles against `test/hal_sim.c` -- a model of the fixture:
  the relay chain, the readback divider of section 8.4, the colour sensor and the marker
  comparator -- and drives the **real firmware** with **154 checks**. That is what proves
  the two behaviours a reviewer cannot see by reading: that a channel mode change breaks
  before it makes, counted in latch events, and that a switching command is refused while HV
  is armed. It is the same arrangement `webtest/tests/interop` uses for the product
  firmware, and it catches the same class of defect.
* It then compiles `src/hal_rp2040.c` against five stub Pico SDK headers and checks that all
  seventeen `fixhal.h` functions are defined. That proves the C is valid and the contract is
  met. **It proves nothing whatever about the peripherals.**

`CMakeLists.txt` builds the real images on a machine with the Raspberry Pi Pico SDK. **No
image has been built and none has been run**: this package vendors no SDK and there is no
board. Every pin number in `hal_rp2040.c` is that file's own choice against a board that has
not been laid out, and `tools/fixture_gen.py --check` compares the two rather than leaving
them to drift.

**The M2 I2S transmitter is not written.** `hal_tone_start()` on the RP2040 returns zero,
`fix_m2.c` turns that into `ERR ... 11 UNSUPPORTED`, and the specification the block has to
meet sits in the source where the code will go. A PIO program written against no hardware
and never run is a guess with a comment on it; T12a, T12b and T13 are in any case blocked on
the host test tool that section 7 records as not existing, so writing one now would buy
nothing and would look like progress. It is priced as bring-up in section 6.1.

**Board data, at `fixtures/pcb/FIX-01/` and `fixtures/pcb/FIX-04/`.** Written by
`tools/fixture_gen.py --pcb`. Each directory carries the outline, the panel legend, the
zoning and keep-out artwork, the non-plated drill programme, the complete netlist in
human-readable and machine-readable form, and a constraints file with the stack-up, the
rules and the area budget. Gerber X2, 4.6 metric, bottom-left origin -- the same CAM import
setting as `kicad/gerber/` and `kicad/wh-bus-01/`.

**They are not fabrication sets and each file says so in its own header.** There is no
copper, no via, no plated drill and no paste layer. The reason is stated rather than left to
be discovered: laying out 83 relays and 77 precision resistors on two layers with a driven
guard pour is a person's job, and the one dimension the placement turns on -- the land
pattern of the Omron G6K-2F-Y -- is a datasheet this package does not carry. Section 1.9
carries what the area budget computes about that, and it is not comfortable reading.

Pins in both netlists are named by **function** and not by number. Every semiconductor in
sections 1.8 and 2.4 is named by manufacturer part number and by nothing else, so a netlist
with pin numbers in it would be inventing eleven datasheets. Schematic capture assigns the
numbers; the connectivity is complete without them.

**One topology question the FIX-01 netlist raises and does not answer.** Section 1.2 gives
K101 and K102 as "DPDT polarity reversal" and no contact assignment. The netlist implements
the four-changeover reversal two DPDT relays give, which is the only assignment that produces
the polarity differencing the section 1.3 uncertainty budget takes credit for. It has a
consequence: **a reference that is reversed against the fixture common has to float**, and
section 1.2 does not say whether U3 is on an isolated rail. This is an engineering decision
for the fixture designer, it is the one thing in the FIX-01 netlist a schematic reviewer must
settle before capture, and it is listed in section 7.

### 8.9 The printed fixture parts

Seven parts, from `tools/fixture_gen.py --mech`, each exported as **STEP** for dimensioning
and inspection and as **STL** for MJF from one parametric model, so the two cannot disagree.
This is the treatment `tools/mech_gen.py` gives the product's own printed parts, and the
reasons are that file's. Each mesh is checked closed on the released file, not on the model.

| File stem | Part | Material | Model figures |
|---|---|---|---|
| `FIX-01E_colorimeter_manifold` | light-tight manifold, eight LED sites at 20.0 mm pitch plus a ninth index position for the reference card | PA12, **dyed black** | 184.0 x 30.0 x 19.0 mm, 45.8 cm³ |
| `FIX-01E_sensor_carrier` | indexed sliding carrier, 6.0 mm sensor window, pocket for a breakout up to 24 x 20 x 2.0 mm | PA12, dyed black | 30.0 x 27.0 x 8.0 mm, 3.2 cm³ |
| `FIX-02A_voice_coupler_body` | voice coupler, **2.0 cm³** cavity | PA12 | 24.0 x 24.0 x 17.95 mm, 5.1 cm³ |
| `FIX-02A_sealing_lip` | its compliant lip | **TPU 85A** | 24.0 x 24.0 x 4.5 mm, 1.1 cm³ |
| `FIX-02B_room_coupler_body` | room coupler, **3.5 cm³** cavity | PA12 | 28.0 x 28.0 x 18.1 mm, 6.3 cm³ |
| `FIX-02B_sealing_lip` | its gasket ring | **TPU 85A** | 28.0 x 28.0 x 4.5 mm, 1.0 cm³ |
| `FIX-03A_carrier_nest` | flashing and provisioning nest, section 3.3 | PA12 | 180.0 x 160.0 x 15.5 mm, 199.6 cm³ |

The lips are separate parts because they are a separate material: section 2.4 specifies
"MJF PA12 + TPU 85A lip", and MJF prints one material per build.

**The cavity volumes are arithmetic, not assertions.** Each cavity is a plain cylinder so
that its volume can be computed and checked: FIX-02/A is a 16.0 mm bore, and 2000 mm³ /
(π x 8.0²) gives a depth of **9.95 mm**; FIX-02/B is a 20.0 mm bore and 3500 / (π x 10.0²)
gives **11.14 mm**. `--check` recomputes both from the rounded depths and requires them
within 0.01 cm³ of the 2.0 and 3.5 cm³ section 2.2 specifies; they come out at 2.0006 and
3.4997 cm³.

**The manifold has nine index positions and not eight.** The ninth holds the printed
reference card of section 1.7, so the shift-start check of section 1.12 step 5 is made
without lifting the carrier off its rail and losing the sensor-to-site geometry the R/G ratio
depends on. Indexing is a peg and nine notches rather than a sprung detent: it is positive,
it is printable, and it needs no bought part. Light-tightness is a fit and an overlap and not
a seal -- the carrier sits in a 1.5 mm rebate whose walls stand above the chamber -- and the
thing that proves it is the dark reading section 1.12 step 5 already requires.

**One dimension in this set is a PROPOSAL and not a fit.** FIX-02/A's mouth is 10.0 mm and
the TPU lip seals on it. What the lip has to seal *against* is the boom capsule with its
windscreen removed, and that diameter is not a known number in this package: AVL-EEG-017 K10
buys a "Primo EM272Z1, alternate any 6 mm electret", and the boom nose that carries it,
HM-07A/B, has no released geometry at all. The lip is compliant and covers a range; **which
range, and therefore the mouth diameter, is a decision for the programme once the boom is
drawn and the capsule is chosen.** It is listed in section 7. Nothing else in the set depends
on it -- FIX-02/B seals on a flat pod wall around the 4.0 mm acoustic port `mech_gen.py` cuts
at carrier (122.0, 102.0), and the nest works to `design.py`'s own board outline.

**None of the seven has been printed or measured.** Every figure in the table is a model
figure, and the manifest at `fixtures/MANIFEST.json` records them as such in the schema
`mech/MANIFEST.json` uses, with the SHA-256 of each STEP and STL beside it. All seven meshes
are checked closed on the released file rather than on the model, because a raised or dropped
feature that only *touches* a part unions into a shell that reports watertight in some readers
and not in others and prints as a loose lump -- which is what the FIX-01/E sensor carrier's
index peg did on its first pass.

---

## Revision history

| Rev | Date | Change |
|---|---|---|
| A | 2026-09-01 | First issue. Supersedes the single-sentence jig description in DSN-EEG-003 Rev A.2 section 6, and the FXT-EEG-005 and FIX-EEG-010 identifiers used in the package v1 audit. |
| B | 2026-09-01 | Corrected against the package v2 rulings: carrier restated as 150.0 x 130.0 mm and four layers; fixture naming aligned to FIX-01 to FIX-04 with TST-EEG-004's part letters; every step number re-cited to TST-EEG-004 Rev C; the per-unit 2500 V AC hipot deleted in favour of the 500 V DC T20 measurement and the hipot tester removed from the cost; T11 rebuilt around a TCS34725 colorimeter head FIX-01/E; harness limits deferred to WH-EEG-008 section 9; the 10 µV limit restated as +/-5 %; the headphone load restated as 47.0 Ω; the 1.000 Ω current shunts added (now FIX-04/A); keying moved to WH-KEY-01; the E-28 deviation deleted; S-02, E-17 and T11 stated as not met where they are not met. |
| B | 2026-09-01 | The findings of the second cross-document audit that name this document were closed within this release, without a revision letter change: all seventeen sub-assembly rows of TST-EEG-004 section 6.1 transcribed into section 0.1, including FIX-02/C, FIX-03/A, FIX-03/B and FIX-04/D, which an intermediate draft of this revision had omitted or said did not exist; FIX-01/D restored to the common-mode injection network of section 1.11 with the spare-channel head returned to FIX-01/G, FIX-01/F restored to the 1000:1 divider and FIX-02/D to the 47.0 Ω load and onset marker; FIX-04/H-D, H-A, H-B, H-C, CPL-V and CPL-R withdrawn; maximum acoustic output restated as TST-EEG-004 T28, listed in TST-EEG-004 section 14; the claim that E-11 is not met deleted, because `design.py` fits 10 µF at C20, C40 and C60 for a 1.6 Hz corner against the restated <= 2 Hz; the lead-off reference resistors reconciled with TST-EEG-004 T10, which now names them by the E96 values 4k99 / 10k0 / 49k9 and calculates 92.5 kΩ at 7.8 Hz, so section 1.6 no longer attributes a 5 k / 10 k / 50 k naming or a 92.6 kΩ figure to it -- the rounded naming is left standing only where it still is, in RFQ-EEG-001 section 9.1 item 7 and RISK-EEG-011 H-24 -- and the 31.2 Hz reading recomputed from 49.9 kΩ as 81.4 kΩ; the fixture table cited as TST-EEG-004 section 6.1 rather than section 5; the station plan cited as section 11; the host-tool count corrected to eleven of thirty-one steps at TST-EEG-004 section 16 item 10; the harness step range corrected to WH-EEG-008 H1 to H10; FIX-04/C added as a built sub-assembly; and E-10's two states stated together everywhere. |
| B | 2026-09-02 | **The routing closes.** Section 0.2 is restated against the Rev B DRC report as it now stands: zero violations, all 145 nets fully connected, no net without copper, both inner planes continuous, 3 745 track segments and 552 through vias, and the measured clearances corrected to 0.260 mm on L1, 0.285 mm on the planes and 0.275 mm on L4. The twenty-five open items and the two 0.328 mm electrode-clearance vias are gone. The fabrication data is **released for review under RFQ-EEG-002A** and **not released for fabrication** -- no human layout engineer has looked at routing produced by the programme's own tools -- and the **169 relaxed connections** are stated, because a board that closes at minimum geometry is not the board that closes at preferred geometry. No fixture has been built or measured, S-02 stays not met at 53.2 uA, and the section 7 list of what this document does not close is unchanged. |

| B | 2026-09-02 | **The three things this document called for and never supplied are supplied.** A new **section 8** defines FIXPROTO v1, the host-to-fixture line protocol, and the command sets of M1, M2 and M3; the firmware that implements it is written and is at `fixtures/firmware/`, with 154 host checks driving the real firmware against a model of the fixture. Board data for FIX-01 and FIX-04 is released at `fixtures/pcb/` -- outline, zoning, legend, non-plated drill, the complete netlist and a constraints file -- with the copper stated as a layout engineer's work, priced at 61 hours in section 6.1 and given 15 working days in section 6.3. Seven printed fixture parts are released at `fixtures/step/` and `fixtures/stl/` and dimensioned in section 8.9, with both coupler cavities computed against the volumes section 2.2 specifies. **R201 and R202 are derived** in section 2.3 -- 1.30 kΩ and 2.00 kΩ, exact in E96 -- and the comparator threshold is stated as an open decision with its criteria rather than guessed. Four arithmetic errors found while doing the above are corrected in place and are listed in section 7: ten shift registers for 83 relays (now eleven), a second 1.0 kΩ in the FIX-01/E LED loop (now a 0 Ω link), a section 1.12 relay readback with nothing driving it (now RP1, with the arithmetic in section 8.4), and twenty-four scanner channels for twenty-five harness conductors. Six items move to the section 7 "not closed" list, the largest being that the 160.0 x 100.0 mm outline of section 1.9 closes with a 1 % margin against a relay land pattern nobody in this package has looked up. Nothing has been built, printed, fabricated or measured. |
| B | 2026-09-02 | **Two open items close, one open item is corrected, and the contact-light driver arrives.** **The FIX-02/D comparator threshold is designed** (section 2.3): an RP2040 PWM slice on GP15, `pwm_set_wrap(999)` for a 1000-count period at 125.000 kHz, R203 = R204 = 10.0 kΩ with C201 = 220 nF across the lower leg into U201's inverting input and R205 = 10.0 kΩ from RL201 hot into its non-inverting input, full scale 3.300 x 10.0 / 20.0 = **1.6500 V** at 1.650 mV per count. Settling 5.07 ms against 10 ms and ripple 0.727 % against 1 %, both re-checked; the third Rev B criterion, a range of 10 % to 90 % of the rail, is **superseded** by a range stated at the load, 0 to 1.650 V, which covers the 5.0 V V5V ceiling, the ICD's divide-by-11 fallback tap and the package's own ~110 dB SPL figure. All three resistors are the **TNPW060310K0BEEA** already approved at AVL-EEG-017 row 126, so the decision closes a constructed order code instead of adding one; section 2.4 gains **four** BOM lines and not two. FIXPROTO gains `THR MV <millivolts, 0..1650>` with a power-on default of 165, and **`THR <per mille of the rail>` is struck at both of its statements** so no host tool can be written to the old meaning. The coupler-drive onset for VOICE_PRE and ROOM_PRE is **left open on purpose** and is in section 7. **The FIX-04 scanner card is dimensioned** (section 4.1): 120.0 x 80.0 mm with four M3 at (5, 5), (115, 5), (5, 75), (115, 75) and the two zones, every value read back from the released Edge_Cuts and NPTH files, so no geometry moves. The relay grid is **not** mandated -- creepage is charged on both axes, the usable band is y 10.6-80.0 once the front-edge connectors and their 3.0 mm stand-off are taken out, and the land each candidate grid can carry is stated so the arithmetic can be re-run when the Omron G6K-2F-Y datasheet is opened. The acceptance land is **137 mm² (14.0 x 9.8 mm)**; the area budget's **160.8 mm² is area-only and is superseded on this board**, because it charges no creepage and would have sent a contractor after a part 17 % too big. Section 6.1's FIX-04 board line moves **EUR 40 -> 72** at FIX-01's own EUR 0.15 per cm² of finished board, with all five dependent totals. **Section 1.7 is restated against the E-27 phase driver, which was written on 2026-09-02**: the colour is computed from the converter's lead-off status and cannot be commanded, so T11's states are produced with FIX-01/A and the relay matrix and read by FIX-01/E; the alternation quantises to the FreeRTOS tick at about 250 Hz, and 300 ms is 75 whole periods of it. Three things stay open and are in section 7: the coupler-drive onset, whether rule 5(a)'s 3.0 mm is a board-level or a part-level rule -- a safety-review question on the one fixture where a flashover reaches an operator -- and the fact that `tools/fixture_gen.py` and the released `FIX-04_constraints.txt` still say the card has no outline. Nothing has been built, printed, fabricated or measured, and none of the above is released until the signatures named in sections 2.3, 4.1 and 7 exist. |
| B | 2026-09-02 | **ECO-EEG-024 is applied, and every figure in this document that was computed through the 47 kΩ series resistor is recomputed.** `tools/design.py` fits **68 kΩ** at R1-R16 (Vishay TNPW060368K0BEEA). Section 1.2's "R1-R16 are 47 kΩ on the Phase 1 prototypes and do not stay that way" is superseded and the recomputation it asked for is done here: section 1.6's lead-off arithmetic is run at 68 kΩ, so a 4.99 kΩ reference reads about 73 kΩ, the R_off pass band becomes **68 kΩ +/-5 %**, and the 7.8 Hz worst case 49.9 k + 68 k = 117.9 kΩ shunted by 2.04 MΩ reads **111.5 kΩ**, 5.5 % low, which is the figure TST-EEG-004 T10 now prints. The 92.5 kΩ / 4.5 % pair is kept beside it as the superseded 47 kΩ case, because it is still the contrast that justifies naming the references 4k99 / 10k0 / 49k9 rather than 5 k / 10 k / 50 k. Section 2.3's FIX-02/D single-fault current falls from 41.8 µA to **29.1 µA** with R15. Section 4.3 and the section 7 open item are restated: the single-fault patient auxiliary current is **36.8 µA calculated against 50 µA and S-02 is met in the design**, where both said "53.2 µA, S-02 is not met"; E-10 sits at its **+/-1.0 dB** branch and was +/-0.5 dB at 47 kΩ. **Nothing here is signed off and nothing is measured**: 36.8 µA is a calculation, no board and no fixture exist to measure it on, and SR-01 stays with the electrical safety reviewer of RISK-EEG-011 section 7, who has not started. RISK-EEG-011 section 4, which this document points at for the noise and flatness arithmetic, still runs it at 47 kΩ and is owed the same correction. Separately, the preamble's "nothing in this package has been built or measured" is narrowed to **no hardware**: the ESP32-S3 firmware is built (ESP-IDF v5.2.5, `firmware/release/`) and has run only under QEMU emulation, while **no fixture has been built and no RP2040 image for M1 or M2 exists**, which section 7 already says and this revision does not soften. No fixture geometry, part number, cost or calibration interval changes. |

Changes to any limit or calibration interval in this document require a change note against
DSN-EEG-003 Rev C and an entry in ECO-EEG-016.
