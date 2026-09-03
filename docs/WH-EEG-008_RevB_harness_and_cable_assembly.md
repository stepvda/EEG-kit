# HARNESS AND CABLE ASSEMBLY SPECIFICATION

**Document:** WH-EEG-008  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs.

**Revision note, Rev A to Rev B.** Re-issued against the 150.0 x 130.0 mm four-layer
carrier and the enlarged POD-P1; WH-08, the captive host cable and its gland, is withdrawn
and replaced by WH-09, the USB-B to USB-C panel pigtail; the boom preamplifier is moved to
MP-01 and its part is stated as unsettled; the harness electrical limits are declared the
single home for JIG-EEG-009 to cite; WH-BUS-01 is specified as a fabricable board in
the new section 3.2.1 rather than as a line in a register; and the requirements this
document cannot claim as met are now stated where the requirement is stated.
**WH-KEY-01 and the five WH-ADP adapters are specified at this revision.** Rev A named all
six in its wire lists, its build order and its test record and drew none of them, so five of
the eight assemblies terminated on a part number with nothing behind it and the only
mitigation against the one safety-relevant mis-mate in the kit had no geometry. The shroud
and three of the adapters are modelled in `tools/mech_gen.py` and released as STEP and STL;
the other two are bought parts and are specified by class. What each one still needs before
it can be bought or printed is stated with it.

**Corrections within Rev B, after the verification review of package v2.2 of 2 September
2026: the EMG lead colours are re-issued to the ruling.** Section 3.6, its WH-06 lead table,
the conductor-identification paragraph of section 10 and open item 7 of section 11 now carry
**RD red / YE yellow / GN green**. Rev B as first issued bought those three leads as white,
brown and grey and reported the difference with IFU-EEG-014 as undecided, which by then it
was not: **IFU-EEG-014 Rev B section 13.2 rules the code red / yellow / green**, states the
reasoning in its control note and records the ruling in its section 16 item 11, and
PKG-EEG-015 Rev B section 4.2 already labels the sockets to it. A harness shop building to
the earlier text would have fitted, in a code no other document uses, the three leads the
participant is told to match by colour. The revision letter does not change; this is a
correction within the same release, and it is not yet entered in the ECO-EEG-016 register,
which is where the change record belongs.

**Also within Rev B, 2026-09-02, after the completeness audit of package v2.3: the helmet-end
and boom-end terminations are specified.** New section 3.1.1 specifies the electrical joint at
the eight HM-04 electrode assemblies, which Rev B named as an "HM-04 bayonet tag" and which
exists as no part, no feature and no method; new section 3.1.2 resolves the two ear-reference
terminations, which this document, AVL-EEG-017 K2 and SVC-EEG-013 R4 described as three
mutually incompatible joints. Section 4 gains a WH-03B column, so the 1700 mm boom lead has a
construction for the first time. Section 6 states **one** crimped 2.54 mm connector system for
the whole kit and says why it is that one. Section 8 gains steps 14a and 14b. AVL-EEG-017
section 4 now carries the purchasing lines that the materials, connectors and tooling of
sections 4 and 6 never had. **Sections 3.1.1 and 3.1.2 are PROPOSALS and are marked as such
in their own headings**: they need a mechanical reviewer, a safety reviewer and a vendor, and
none of the three has answered. The revision letter does not change; this is a correction
within the same release, and it is not yet entered in the ECO-EEG-016 register.

**Also within Rev B, 2026-09-02, after the decision review of package v2.3: the three helmet
terminations and the electrode preload spring are ruled.** Rulings D2-EAR-REFERENCE-COUPLER,
D3-BIAS-FPZ-TERMINATION and D5-K12-SPRING-ENVELOPE are written into sections 1, 3.1, 3.1.1 to
3.1.4, 4, 6, 7, 8, 9, 10, 11 and 12 at this issue. Section 3.1.2 keeps the free-hanging
touch-proof coupler and gains the provisions the ruling attaches to it, of which the
load-bearing one is a **packing rule this document does not own**: the ear clips travel mated
and captive, or the participant mates and unmates two of them every session out of a bay of
five identical 1.5 mm DIN plugs, and the safety argument that section rests on is not true.
New section 3.1.3 terminates conductor 11 at a free-hanging touch-proof socket on the halo
front and **deletes the "Fpz bias pad" as a helmet feature**, which was open item 26. New
section 3.1.4 **issues** the K12 spring specification, which ruling D5 declined to issue
against the 4.50 mm spring seat it was written on and which is derivable now that
`tools/mech_gen.py hm04()` has deepened that seat to 6.60 mm. **None of the three is a
signature.** Each names who must sign it and section 11 carries those names.

**And the released HM-04 and HM-05B changed under this document on the same day**, which is
why sections 3.1.1, 6, 7 and 9 are corrected against them rather than left standing: the
bayonet now turns (entry slots 1.70 mm wide at outer radius 5.55 mm cut 3.60 mm deep, a 100
degree circumferential run at z 1.10 to 3.80 and a 1.10 mm retaining lip below it, with the
HM-05B lug corrected from r 5.40 to the r 5.20 its own docstring always claimed); the single
through-window is now **two** pockets with 1.60 mm of PA12 between them, so an LED lead and an
electrode conductor no longer share one cavity, which was RISK-EEG-011 SF-9; and the spring
seat roof moved from z 13.50 to z 15.60. The revision letter does not change; this is a
correction within the same release, and it is not yet entered in the ECO-EEG-016 register.

## Why this document exists

In package v1 the helmet harness existed only as a prose paragraph in DSN-EEG-002 Rev E
section 6 and as unpublished net names inside a KiCad board file. Four documents gave four
different conductor counts for the same cable -- 20-way, 21-way plus shield, 22 positions,
and a 27-conductor bundle in a 20-way FFC -- and none of them added up. No harness shop can
cut wire from that, no contract manufacturer can quote it, and no goods-inwards inspector
can check what arrives. ECO-EEG-014 has since split the harness into two cables so that
eight switched digital lines no longer cross the analogue zone of the carrier, which changes
the arithmetic again. This document is the single from-to authority for every cable in the
kit: eight assemblies, every conductor, every pin, the materials, the connectors and the
tooling, the routes inside HM-01, the build order, the tests and the record. Nothing in it
has been built or measured, and no safety engineer has reviewed this design. Every
dimension, resistance and fill figure below is **calculated** from `tools/design.py`, from
the HM-01 and POD-P1 geometry, and from supplier catalogue data, and is labelled as such.

---

## 1. Cable register

**Nine controlled assemblies at this issue** *(was eight; WH-10 is added on 2026-09-02 by
section 3.1.3, and like WH-06 it is bought in rather than built)*. Part numbers are WH-EEG-008-nn; the short form WH-nn is used
throughout this document and on the labels. Carrier connector coordinates are given in the
`design.py` convention (top-left origin, Y down) and in the fabrication convention
(bottom-left origin, Y up, `y_out = 130.0 - y_design`), because the two appear on different
drawings and confusing them puts a connector on the wrong edge of the board.

| Ref | Assembly | Ways | Carrier connector | Position, design (mm) | Position, fab (mm) | Screened | Qty/kit |
|---|---|---|---|---|---|---|---|
| WH-01 | Helmet electrode cable | 12 | J14, 1x12 socket strip | 5.0, 12.0 | 5.0, 118.0 | yes, overall foil + drain | 1 |
| WH-02 | Helmet contact-light cable | 10 | J30, 1x10 socket strip | 66.0, 90.0 | 66.0, 40.0 | no -- see section 5.4 | 1 |
| WH-03 | Boom microphone pigtail | 4 | J18, 1x4 socket strip | 122.0, 90.0 | 122.0, 40.0 | yes, overall foil + drain | 1 |
| WH-04 | Headphone panel pigtail | 4 | J27, 1x4 socket strip | 128.0, 72.0 | 128.0, 58.0 | yes, overall foil + drain | 1 |
| WH-05 | Room microphone cable | 4 | J28, 1x4 socket strip | 122.0, 102.0 | 122.0, 28.0 | yes, overall foil + drain | 1 |
| WH-06 | EMG DIN lead set | 1 each | J15, J16, J17 (DIN 42802) | 8.0, 76/88/100 | 8.0, 54/42/30 | no -- see section 3.6 | 3 |
| WH-07 | Charge-port pigtail | 2 | J24, JST PH 1x02 | 143.0, 80.0 | 143.0, 50.0 | no | 1 |
| WH-09 | Isolator host pigtail, USB-B to USB-C panel receptacle | 4 + shell | none -- module to panel | (module at J10: 136.0, 6.0) | (136.0, 124.0) | cable's own braid | 1 |
| WH-10 | Fpz bias lead, snap to DIN 42802 touch-proof plug, 150 mm | 1 | none -- mates the WH-01 conductor 11 coupler on the helmet | -- | -- | no -- see section 3.1.3 | 1 |

**WH-08 is withdrawn and its number is not reused.** Rev A specified WH-08 as a captive 2 m
host USB-C cable leaving the pod through a Lapp SKINTOP gland. The host connection is a
socket, not a captive cable: the host connector is the USB receptacle on the ADuM4160
isolator module, presented through a gasketed aperture in POD-P1, and the participant plugs
one of the two A-07 cables into it. There is no gland in the Phase 1 build and no gland
feature exists in POD-P1-01. A captive lead through a gland remains a Phase 2 candidate for
the helmet shell and is not specified here. Section 3.8 specifies what replaced it.

Two sub-assemblies are called out because they carry conductors and would otherwise fall
between documents:

| Ref | Assembly | What it is |
|---|---|---|
| WH-BUS-01 | Contact-light bus board | 14.0 x 10.0 x 0.80 mm FR-4, ten 1.60 mm plated pads on a 2.70 x 4.80 mm grid, no components. Sits at frame node N1 immediately inside the occipital entry. Splits LED_V into eight tails without a single crimp splice. Fabrication data is `kicad/wh-bus-01/`, generated by `tools/wh_bus.py`; section 3.2.1 specifies it. **Two copper layers, not one**, for the reason in 3.2.1; PARTS-EEG-019 is corrected to it at its 2026-09-02 issue. |
| WH-03B | Boom lead | Capsule to a 4-pole 3.5 mm plug, 1700 mm. Two 7/0.1 mm PTFE conductors, overall foil and 30 AWG drain, TPU jacket OD 2.2 mm maximum. Part of the boom assembly. **Its construction is section 4, which gains a WH-03B column at this issue**; its wire list is section 3.3; AVL-EEG-017 K41 buys it. The "TRRS plug" of the first issue is the same 4-pole part and the word is dropped, because the fourth contact here is a screen return and not a microphone ring. |
| WH-KEY-01 | Keying shroud | Printed PA12 tube that drops over a carrier socket strip and takes the harness housing in one orientation only. Three forms, for J14, J30 and J22. Dimensioned in section 6.1; geometry in `tools/mech_gen.py wh_key01()`. |
| WH-ADP-01, -01B, -02, -03, -04 | Panel adapters | The five parts the panel-going pigtails terminate on. Two are bought jacks, three are printed. Specified in section 3.9. |

**No cable in this register lands on J22.** J22 is the 1x3 socket carrying the two spare
protected electrode channels EOGIN1 and EOGIN2 and their AGND_REF screen. The EOG panel
sockets, their cable and their drawing are a Phase 2 option, listed as such in
PARTS-EEG-019 with no part number yet, so in a standard build channels 15 and 16 are
protected and reach no panel socket. That is a stated omission, not an oversight.

**Phase note.** Phase 1 puts the electronics in the POD-P1 bench enclosure (163.0 x 143.0 x
58.0 mm external, 158.0 x 138.0 x 55.5 mm internal, with the 163.0 x 143.0 x 6.0 mm lid), so
WH-01 and WH-02 are 1500 mm umbilicals from the helmet to the pod, and the boom plugs
directly into the POD-P1 panel rather than running through the frame. In Phase 2 the
electronics move into the occipital shell of HM-01 and both umbilicals shorten to 180 mm;
WH-03 then routes through the left temple channel as DSN-EEG-002 section 6 describes. The
Phase 2 shell is sized in RFQ M-01 for a carrier that no longer exists at that size, so the
-H2 variants cannot be dimensioned yet. The two variants are WH-01-P1 / WH-01-H2 and are not
interchangeable. Only the -P1 variants are being built.

### 1.1 What changed on the carrier, and why this document had to be re-issued

Two findings came out of actually laying the board out rather than asserting that it would
lay out, and both reach this document through the connector coordinates and the keep-out.

**The carrier grew from 130 x 124 mm to 150.0 x 130.0 mm.** Thirty connectors, 211 parts and
156 nets would not close at the smaller size. At kit quantities the extra bare board costs a
few euro per unit against a real risk of an unroutable design. Every carrier coordinate in
this document, and the `y_out = 130.0 - y_design` conversion, follows from that: a harness
built to the Rev A coordinates would be cut to the wrong service lengths and the fabrication
drawing would put J14 on the wrong edge.

**The carrier went from two layers to four.** Package v1 argued that a two-layer carrier is
cheap and easy to route. Doing the layout showed that it is not: on two layers the bottom
side has to be both the reference plane and the second routing surface, and it cannot be
both. The stack is now L1 signal, L2 reference plane, L3 reference plane, L4 signal, mask /
35 um L1 / prepreg 0.200 / 17 um L2 / core 1.065 / 17 um L3 / prepreg 0.200 / 35 um L4 /
mask, 1.60 mm +/- 10 %, with through vias only, 0.60 mm pad on a 0.30 mm finished hole. The
reference planes are AGND_REF left of x = 62 mm and DGND right of it, on **both** inner
layers, stitched together only at the star points. That matters to the harness in three
places: every electrode conductor now lands on a socket with a continuous reference plane
under it rather than a swiss-cheesed pour, which is the condition section 5 assumes when it
allows the in-frame runs to be unscreened; the isolation keep-out at section 3.8 is a
keep-out on four layers, not two; and the two star points of section 5.1 are the only ties
between two planes that now exist twice over.

---

## 2. Conductor arithmetic

The v1 statements and what Rev B actually implements:

| Source | Claim | Status |
|---|---|---|
| DSN-EEG-002 Rev E s6, table W1 | 8 x screened pair + 2 x screened + 1 x screened + 8 LED = 27 conductors | Superseded. "Pair" meant signal plus its own screen, never signal plus return. |
| RFQ-EEG-001 Rev C, E-09 | "J14, 20-way plus shield" | Superseded by ECO-EEG-014; E-09 is re-issued in RFQ-EEG-001 Rev E as two cables. |
| EEG-CAR-01_BOM.csv, J14 | "Helmet harness (20-way + shield)" on a 1x22 footprint | Superseded. J14 is 1x12 in Rev B. |
| Kit BOM Rev B, row 24 | "20-way FFC to carrier" | Wrong construction. An FFC has no per-conductor screen, no drain and cannot mate a 2.54 mm socket strip. Delete "FFC". |
| ECO-EEG-016, ECO-EEG-014 "Was" text | "eleven electrode conductors and **eleven** contact-light conductors" in one 22-way socket | Wrong on the light side. The light group is ten conductors, not eleven: eight LEDn plus LED_V plus LED_GND. The budget below is the one that adds up and ECO-EEG-016 is corrected to it. |

Rev B budget, which does add up:

| Group | Conductors | Cable | Connector |
|---|---|---|---|
| Eight scalp electrodes | 8 | WH-01 | J14.1 to J14.8 |
| Two ear references | 2 | WH-01 | J14.9, J14.10 |
| Bias drive to Fpz | 1 | WH-01 | J14.11 |
| Commoned screen drain | 1 | WH-01 | J14.12 |
| Eight contact-light lines | 8 | WH-02 | J30.1 to J30.8 |
| Light common and guard | 2 | WH-02 | J30.9, J30.10 |
| **Total into the helmet** | **22** | two cables | two connectors |

The count is unchanged at 22. What changed is that the eleven high-impedance electrode
conductors and the eight switched 3.3 V lines are now in separate jackets, entering the
carrier 61 mm apart on opposite sides of the zone split at x = 62 mm, instead of sharing one
socket at x = 5 mm in the middle of the analogue zone.

The kit terminates on **fourteen** places on a person: eight scalp cups, two ear references,
one bias pad and three EMG studs. **The bias pad is a disposable pre-gelled snap electrode off
the K4 pack from 2026-09-02**, placed on prepped forehead skin below the HM-02A brow pad and
replaced every session, not a feature of the helmet -- section 3.1.3. The count is unchanged;
what changed is that the fourteenth termination now exists as a part. The two EOG spares are protected on the carrier and are
not fitted in a standard build.

---

## 3. From-to wire lists

Colour names are IEC 60757 two-letter codes. **Solid** colours belong to WH-01 (electrode);
the same colour **with a black tracer** belongs to WH-02 (light) for the same site, so a
technician with the crown cover strip off can tell a Cz electrode conductor from a Cz light
conductor by eye. Black is used only for 0 V conductors, and never in WH-01, because the bias
lead is a driven common-mode return and not an earth.

### 3.1 WH-01 -- helmet electrode cable, 12-way screened, to J14

Insulation PTFE throughout. Gauge 7/0.1 mm tinned copper for all eleven signal conductors.
Cut lengths are calculated for the -P1 variant: 1500 mm umbilical + 120 mm pod service loop
+ 20 mm pod termination allowance + the in-frame routed length + 40 mm site service loop
+ 15 mm site termination allowance. Tolerance +10 / -0 mm.

**Conductor 11 is the one conductor that does not follow that formula**, from 2026-09-02. Its
site is a free-hanging coupler at the halo front and not a body the harness is dressed into,
so there is nowhere to coil a 40 mm site service loop; the loop is deleted and a stated free
tail **F** takes its place, giving 1500 + 120 + 20 + 285 + 15 + F = **1940 + F mm**. F is a
fitting dimension and is set at the first fitting trial -- open item 30. *The 1980 mm this row
carried before that date is superseded: the arithmetic was right for a conductor soldered to a
fixed pad, and it contains no free tail at all, so it cannot also be a free-hanging coupler.*

| Cond | Colour | Gauge | Insul. | From (site / terminal) | To (pin) | Net | Carrier path | In-frame (mm) | Cut (mm) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WH white | 28 AWG eq. | PTFE | Fz cup, HM-04 termination (3.1.1) | J14.1 | E_Fz | R1 47k -> D1 -> C1 -> IN1 (J2.1) | 315 | 2010 |
| 2 | RD red | 28 AWG eq. | PTFE | Cz cup, HM-04 termination (3.1.1) | J14.2 | E_Cz | R2 -> D2 -> C2 -> IN2 (J2.2) | 205 | 1900 |
| 3 | BU blue | 28 AWG eq. | PTFE | Pz cup, HM-04 termination (3.1.1) | J14.3 | E_Pz | R3 -> D3 -> C3 -> IN3 (J2.3) | 130 | 1825 |
| 4 | GN green | 28 AWG eq. | PTFE | C3 cup, HM-04 termination (3.1.1) | J14.4 | E_C3 | R4 -> D4 -> C4 -> IN4 (J2.4) | 285 | 1980 |
| 5 | YE yellow | 28 AWG eq. | PTFE | C4 cup, HM-04 termination (3.1.1) | J14.5 | E_C4 | R5 -> D5 -> C5 -> IN5 (J2.5) | 285 | 1980 |
| 6 | BN brown | 28 AWG eq. | PTFE | T7 cup, HM-04 termination (3.1.1) | J14.6 | E_T7 | R6 -> D6 -> C6 -> IN6 (J2.6) | 175 | 1870 |
| 7 | OG orange | 28 AWG eq. | PTFE | T8 cup, HM-04 termination (3.1.1) | J14.7 | E_T8 | R7 -> D7 -> C7 -> IN7 (J2.7) | 175 | 1870 |
| 8 | VT violet | 28 AWG eq. | PTFE | F7 cup, HM-04 termination (3.1.1) | J14.8 | E_F7 | R8 -> D8 -> C8 -> IN8 (J2.8) | 250 | 1945 |
| 9 | GY grey | 28 AWG eq. | PTFE | Left ear clip, A1 coupler: free-hanging 1.5 mm DIN 42802-1 socket, GY body (3.1.2) | J14.9 | REF_L | R9 -> D9 -> C9 -> SRB1 (J2.9) | 195 + 250 free | 2140 |
| 10 | PK pink | 28 AWG eq. | PTFE | Right ear clip, A2 coupler: free-hanging 1.5 mm DIN 42802-1 socket, PK body (3.1.2) | J14.10 | REF_R | R10 -> D10 -> C10 -> SRB1 (J2.9) | 195 + 250 free | 2140 |
| 11 | TQ turquoise | 28 AWG eq. | PTFE | Fpz, A3 coupler: free-hanging 1.5 mm DIN 42802-1 socket at the halo front, TQ body (3.1.3) | J14.11 | BIAS_EL | R11 from BIASOUT (J2.10); **D11, C11 on BIASOUT** | 285 | **1940 + F** (3.1.3) |
| 12 | bare, clear sleeve | 30 AWG drain | -- | commoned screen, pod end only | J14.12 | HARN_SHIELD | **R91 (0R) to DGND -- the only connection** | none | 1660 |

D1 to D16 are **BAV99**, not BAT54S. Schottky leakage across a 47 kOhm series resistor is an
offset error on a 10 uV input; BAT54S is used only at the envelope rectifiers D20, D40 and
D60. This is stated here because the harness operator sees the clamp designators on the
board and may otherwise assume they are all the same part.

Two facts a builder must be told, because neither is visible in the cable:

* **REF_L and REF_R are hard-paralleled on the carrier.** R9 and R10 both land on net SRB1
  (J2.9, J4.9), so the two ear clips sit in parallel through 2 x 47 kOhm = 23.5 kOhm to the
  shared reference. There is no separate ear channel and one clip falling off is
  electrically almost invisible. The harness carries two conductors, not one, and both must
  be present and continuous.
* **The bias path runs outward.** BIASOUT leaves the module at J2.10, passes through R11,
  and only then becomes BIAS_EL on the cable. Conductor 11 is therefore a driven output, not
  an input, and the resistor is upstream of the person exactly as it is on every other lead
  (RFQ E-07). **Corrected 2026-09-02:** the clamp and the capacitor are upstream of the person
  now as well. `tools/design.py` lost the channel-11 override at this issue, so the row is
  generated by the same loop as the other fifteen and D11.3 and C11.1 land on BIASOUT, behind
  the 47 kOhm. *Was: "D11, C11 on BIAS_EL", which put both on the patient side of R11 and made
  this the one lead of sixteen whose single-fault current its own series resistor did not
  bound.* What that changes, and what it does not, is stated in section 3.1.3 beside the
  current numbers; where this document and `design.py` disagree, `design.py` governs.

#### 3.1.1 The termination at HM-04 -- a PROPOSAL, not a released design

**Nothing in this section is released.** It specifies a joint that does not exist, asks for
geometry that two released models do not have, and names two parts that have no vendor. It is
written here because the alternative is what Rev B shipped: eight conductors landing on an
"HM-04 bayonet tag" that is on no drawing and in no model, and a build step (section 8, step
14) that defers to an ASM-EEG-007 step which does not exist.

**What is actually missing.** Conductors 1 to 8 of WH-01 and both leads of all eight contact
lights end inside an HM-04 body: eight electrode conductors and sixteen LED leads,
**twenty-four joints per helmet, none of which has a terminal, a method or a wire entry.**
ASM-EEG-007 Rev B stage 3 bonds the bodies (4.2), fits the LEDs (4.3), threads the
harness (4.4) and fits the yoke, strap, boom and pads (4.5); it has no termination step, no
step that fits the cups, the bayonet carriers or the springs, and no stage-3 sign-off line for
either. MECH-EEG-020 sheet 8 shows a cup bore, two bayonet slots, a gel port and a side
window, and no terminal, no tag, no wire entry and no LED seat. So the site end of both helmet
cables cannot be made, and test H6's "HM-04 termination, 15 N minimum" has no joint to pull.

**Three released files already say three different things**, which is the reason this is a
decision and not a drafting job:

| Source | What it says |
|---|---|
| This document, section 3.1 as first issued | "Fz cup, **HM-04 bayonet tag**" -- a feature of HM-04 |
| `tools/mech_gen.py hm05b()` | "a 1.60 x 0.80 mm slot in the flank for the **WH-01 conductor's solder tag**, which WH-EEG-008 H6 pull-tests at 15 N" -- a feature of **HM-05B**, the part that turns and comes out |
| ASM-EEG-007 Rev B stage 3 | nothing at all |

The second is real geometry: the released `mech/stl/HM-05B_cup_bayonet_carrier.stl` carries a
blind pocket 1.60 mm wide, 1.20 mm deep into the flank and 0.80 mm tall at z = 5.60 to 6.40,
at 90 degrees to the bayonet lugs *(read from the mesh)*. It is the only feature anywhere in
the package that was drawn for this joint, and **it cannot be the answer**, for two reasons
that no drawing note can fix.

* **Nothing can reach it.** HM-05B's body is 9.10 mm in HM-04's 9.20 mm bore. The pocket sits
  at z = 5.60, mid-bore, enclosed by 0.05 mm of radial clearance for its whole circumference.
  A conductor soldered into it has no route out of the assembly.
* **It is on the part that leaves.** SVC-EEG-013 section 3 R4 releases all eight cups with the
  HM-09 key at every turnaround, R5 puts them in a 40 kHz ultrasonic bath, and R10 refits
  them. A conductor soldered to the carrier is either unsoldered eight times per turnaround or
  taken into the bath with the frame, the harness and 1500 mm of umbilical attached to it.

**What the released HM-04 has.** Read from `mech/stl/HM-04_electrode_assembly_body.stl` and
`tools/mech_gen.py hm04()`, cup face at z = 0, gel-port face at z = 18.00. *(model figures; no
HM-04 has been printed)*

| Feature | Geometry |
|---|---|
| Body | 12.40 x 12.40 x 18.00 mm square prism, 1.90 cm3, top edges filleted 1.20 mm |
| Cup bore | 9.20 dia, z 0 to 9.00, open at the cup face |
| Spring seat | 6.80 dia, z 9.00 to **15.60** *(was z 9.00 to 13.50; deepened 2026-09-02, section 3.1.4)* |
| Gel port | 2.50 dia on the axis, through the top face into the cup bore |
| Bayonet entry slots | two, 2.30 radial x **1.70** tangential, **3.60 mm** deep from the cup face, outer radius **5.55 mm**, 180 degrees apart *(was 2.20 x 1.40 mm, 2.40 mm deep at 4.20 mm radius -- a 1.40 mm slot for a 1.40 mm lug, in a material printed to +/-0.15 mm)* |
| Circumferential bayonet run | **100 degrees**, r 4.30 to 5.55, z 1.10 to 3.80, both slots, with a **1.10 mm retaining lip** below it. *New on 2026-09-02. Before that date there was no run and the carrier was a plug fit* |
| Two side pockets | each 3.20 mm wide x 2.60 mm tall, z 11.70 to 14.30, 5.40 mm deep from opposite faces, **separated by 1.60 mm of PA12 on the axis**: outboard is the LED seat, inboard is the electrode conductor's run. *(Was one 3.20 mm box cut right through the body. The correction is dated 2026-09-02 and its reason is RISK-EEG-011 SF-9 -- see below)* |
| Anything else | none. The rest is solid PA12 |

Two properties of that geometry decide what follows.

**The window is now two pockets, and that is a safety correction and not a drafting one.**
*Superseded 2026-09-02. Was: "The side slot is a through-slot, not a blind window. `hm04()`
cuts a 3.20 x 14.40 x 2.60 mm box through a 12.40 mm body, so the part has two openings of
3.20 x 2.60 mm at 180 degrees... The outboard opening is the light window the LED of ASM
section 4.3 sits behind. The inboard opening is unused, and it is the only way into the
assembly the part has."* That reading was correct against the model of the day, and the model
of the day was the fault: one cavity through the body put a switched LED lead and a
high-impedance electrode conductor about 3 mm apart, in shared open volume, at all eight
sites, which is RISK-EEG-011 SF-9 written as geometry. `hm04()` now cuts **two** pockets of
3.20 x 2.60 mm, 5.40 mm deep from opposite faces, with 1.60 mm of printed PA12 between them:
**the outboard pocket is the LED seat and the inboard pocket is the conductor run**, and they
are no longer two ends of one hole. **ASM-EEG-007 section 4.2's fitting note, "the window is
on one side of the body only", still does not match the released model** -- there are two
openings, they are simply no longer connected -- and that correction remains ASM-EEG-007's.

**There is no other route in.** HM-05B's body is 9.10 mm in the 9.20 mm bore and its spigot
6.60 mm in the 6.80 mm seat -- 0.05 and 0.10 mm on the radius -- so nothing passes either
annulus, and the 2.50 mm gel port is committed to gel. The free volume inside a seated
assembly is the **3.50 mm** the seat now has above the spigot: HM-05B is 12.10 mm tall
(`hm05b()`, and `mech/MANIFEST.json` bounding box 10.80 x 9.10 x 12.10 mm) and the seat roof
is at **15.60**. *Was 1.40 mm against a seat roof at 13.50, until `hm04()` deepened the seat
on 2026-09-02.* The inboard pocket, at z 11.70 to 14.30, opens into the lower 2.60 mm of that
band, and section 3.1.4 spends 2.10 mm of it on the spring at solid height.

**What the joint has to do.** Five things, and between them they rule out every simple answer.

1. **Part at every turnaround, without a tool.** SVC-EEG-013 section 3 R4, R5 and R10, eight
   times each way, for the life of the kit.
2. **Not become a second half-cell.** The measurement is microvolts from a sintered Ag/AgCl
   surface. A junction of two different metals in the wetted path is an electrochemical cell
   with its own drift; a junction of two different metals anywhere is a thermocouple in a
   10 uV measurement. So: the same plating on both mating faces, and out of the gel.
3. **Survive 15 N** (test H6).
4. **Be re-makeable in the field.** SVC-EEG-013 section 5.3 replaces one conductor by drawing
   a new one through the channel and terminating it at the HM-04, with a soldering iron and
   hand tools, without disturbing the other seven sites.
5. **Not be a connector handled eight times per turnaround with wet gloves.** Whatever parts
   at the bath, the operator's hands are already busy with the bayonet and a released cup.

**The proposal: the bayonet is the disconnect.**

Make the electrical interface an **annular contact at the top of the spring seat**, so that
the quarter-turn that already releases the cup is also what parts the circuit, and no operator
ever plugs or unplugs anything at a site.

| Element | Part | What it is |
|---|---|---|
| Rotating half | **HM-05C**, cup contact crown | An annulus let into the top face of HM-05B's spigot, flush at z = 12.10, clear of the 2.40 mm gel passage, gold over nickel on its upper face. Its tail runs to the cup down a dry groove in the carrier wall |
| Fixed half | **HM-04A**, electrode termination contact | A sprung leaf anchored in HM-04, reaching into the 1.40 mm band above the spigot and bearing axially on the crown, gold over nickel on its bearing face. Its tail leaves through the **inboard** side-slot opening and is soldered to the WH-01 conductor 8 mm outside the body |
| Spring | K12, **specified at section 3.1.4 from 2026-09-02** | Stays purely mechanical and carries no signal. *The words "it bears on the crown" are superseded on 2026-09-02: the spring bears on the PA12 spigot rim outboard of the crown and on the PA12 seat roof, and touching the gold crown is the thing section 3.1.4's no-gold relation exists to prevent. At the crown outside diameter this document proposes today, that relation does not close -- see 3.1.4* |

Being an annulus, the crown is **rotation-invariant**: the carrier turns 90 degrees to lock and
the contact does not move on it, so nothing twists and no conductor follows the bayonet. Being
axial, the contact is closed by the same 3 to 6 N the spring already applies to hold the cup
against the scalp, so **a cup that is seated is by construction a cup that is connected**, and
the failure this design must not have -- a cup that looks fitted and is open -- becomes a cup
that is visibly not locked.

Two figures a contact supplier has to meet, and only one of them can be derived here.

* **Contact force at the crown: 0.5 N minimum.** *This is stated as a requirement. It is not
  derived from a measurement and no contact has been tested.* A gold-to-gold interface on a
  high-impedance input behind a 47 kOhm resistor has no fritting current available to break a
  surface film, so the normal force is the only thing that makes the contact.
* **Contact resistance is not the specification, and saying so matters.** The source impedance
  at this node is 5 to 20 kOhm of skin contact plus the 47 kOhm series resistor. A whole ohm
  of contact resistance is 14 parts per million of it, exactly as section 4 says of the
  conductor. What matters is that the contact is closed and stays closed. H1's 1.0 Ohm limit
  is there to catch an open joint, not to protect the measurement.

**What the released models have to gain. None of it is this document's to draw.**

| Part | Feature the proposal needs |
|---|---|
| HM-04 | an anchorage for HM-04A that takes 15 N, reachable from the inboard face. **Re-stated 2026-09-02:** the material it was to be cut in is no longer a full section. The spring seat now runs to z 15.60, so between the pocket roof at z = 14.30 and the top fillet at z = 16.80 the part is an annulus outside r 3.40 and not 2.50 mm of solid PA12. The anchorage and the deepened seat have to be drawn against each other |
| HM-04 | a dressed exit at the inboard pocket -- a radius, not a printed edge, against a 0.70 mm OD PTFE conductor |
| HM-04 | ~~a seat and two lead passages for the contact-light LED at the outboard opening~~ **-- the seat is cut. Closed 2026-09-02:** `hm04()` cuts the outboard pocket as the LED seat, separated from the inboard conductor run by 1.60 mm of PA12. The **two lead passages out of that pocket are still owed**, and until they exist ASM section 4.3 threads two LED leads through a blind pocket |
| HM-04 | ~~the circumferential bayonet run~~ **-- cut. Closed 2026-09-02:** 100 degrees at r 4.30 to 5.55, z 1.10 to 3.80, over a 1.10 mm retaining lip, against an HM-05B lug corrected to outer radius 5.20 at z 1.20 to 3.30. `tools/simulate_production.py` measures 0.000 mm3 of interference through the quarter turn and through the carrier's 0.40 mm of axial travel, and 1.557 mm3 of lip engagement on a straight pull. That is a boolean measurement on the released solids, not a print: no HM-04 has been printed |
| HM-05B | a 0.50 mm recess in the spigot top for HM-05C and a dry groove down the carrier wall for its tail. **The 1.60 x 1.20 x 0.80 mm flank pocket is deleted or re-cut as that groove's anchorage**, and `hm05b()`'s docstring reference to a WH-01 solder tag is withdrawn with it |
| HM-05A | a defined tail. The cup as bought carries a 1.5 m lead (AVL-EEG-017 K1) and this joint wants tens of millimetres -- see the note on K1 in that document |
| MECH-EEG-020 | a sheet 8 that dimensions all of the above |

**What was considered and rejected.**

| Considered | Rejected because |
|---|---|
| The spring is the conductor | It is 302 stainless (AVL K12) sitting in a seat on the gel path. Stainless against Ag/AgCl in saline is a drifting half-cell in series with the measurement, and making the preload member the contact means every hair under a cup is an electrical fault as well as a mechanical one |
| A wiping contact in the cup bore | The bore is the gel volume: the port delivers into it and SVC R6 flushes it. A contact there is wetted by design |
| The `hm05b()` flank solder tag, as drawn | No route out of the assembly, and it is on the part that goes in the ultrasonic bath. Both are stated above |
| A miniature plug and socket at the site | 3.20 x 2.60 mm of opening, eight sites, mated and unmated with wet gloves at every turnaround, with a released cup hanging off the connector while it is done |
| Solder the conductor to the cup and put the frame in the bath | R5's bath is 40 kHz with an enzymatic cleaner and SVC-EEG-013 does not immerse the frame. It also turns SVC section 5.4's ten-minute cup change into a harness repair |
| Buy the cup as a complete leaded electrode and put the joint in the frame channel | **This is the fallback and it is not a straw man.** It needs a passage out of HM-04 that the part does not have, a connector small enough to live under a 3.80 mm channel cover, and a way to get a 1.5 m factory lead down to a tail. The mechanical reviewer should weigh it against the crown |

**Who has to decide.** The **mechanical reviewer**, because every row of the "must gain" table
is a change to a released model and to MECH-EEG-020 sheet 8. The **safety reviewer**, because
this is a joint in the patient-applied path and RFQ S-02's single-fault case already does not
close (section 5.5). **AVL-EEG-017**, because neither HM-04A nor HM-05C has a vendor: both are
carried there as OPEN WITH CRITERIA, on lines K25 and K26, with the criteria above. Until all
three have answered, the site end of both helmet cables cannot be built. That is open item 22,
and the missing ASM-EEG-007 steps are open item 28.

**Conductor 11 is not solved here.** BIAS_EL lands on an "Fpz bias pad, solder tag" which is
not an HM-04, is on no drawing and has no part number. It has exactly the defect this section
opened with and this section does not close it -- open item 26.

#### 3.1.2 The two ear-reference terminations -- also a PROPOSAL

Three documents describe three incompatible joints for the same two terminations, and a
builder cannot choose between them.

| Source | What it says | What it implies |
|---|---|---|
| Section 3.1 as first issued | "Left ear clip, **A1 crimp**", on 250 mm of free conductor out of the temple | the harness conductor is crimped onto a **bare clip**: a permanent joint, onto a part that is not a catalogue item |
| AVL-EEG-017 K2 | "Ag/AgCl ear-clip reference electrode, **DIN 42802 plug**", two per kit | a **finished leaded electrode** with a touch-proof plug -- and there is nowhere to plug it in. J15, J16 and J17 are the three EMG channels and carry EMGIN1 to EMGIN3 |
| SVC-EEG-013 section 3 R4 and R5 | "Release the two ear clips", then the ultrasonic bath | the joint must part **without a tool**, twice per turnaround, for the life of the kit |

A permanent crimp cannot satisfy the third. A plug with no socket cannot satisfy the second.

**The proposal: a free-hanging touch-proof socket at each temple.** Conductors 9 and 10 leave
the left and right temple as the 250 mm free tails section 3.1 already gives them, and each is
terminated in a **free-hanging 1.5 mm touch-proof socket to DIN 42802**. The ear clip is
bought exactly as AVL-EEG-017 K2 already buys it -- complete, leaded, with its own touch-proof
plug -- and plugs into that socket.

* **It parts by hand, twice per turnaround, with no tool**, which is what SVC-EEG-013 requires
  and what neither of the other two readings can do.
* **It does not change what is bought.** K2 stands as written; what changes is that its plug
  finally has something to enter. *That last clause is superseded on 2026-09-02. The K2 part
  does not change, but its purchase order gains two fields it never had -- a stated
  plug-to-jaw lead length and a plug colour -- for the reasons in 3.1.2.1 provisions 2 and 7.
  AVL-EEG-017 K1 already carries the identical correction one line above K2.*
* **It is touch-proof.** These two conductors reach a person's ears through 47 kOhm from a
  +/-2.5 V rail. A bare crimped clip on 250 mm of free conductor is an accessible conductive
  part on a patient-applied lead, which is the thing DIN 42802 exists to prevent.
* **It is the one form of this part that is actually catalogued.** AVL-EEG-017 section 1.4.1's
  whole difficulty with J15 to J17 is that the Staubli parts `design.py` names are "cable and
  panel parts, not PCB parts". Here a cable part is exactly what is wanted, so this line does
  not carry the 12-week first-article risk the PCB socket line does.
* **And the guard.** The kit then has five 1.5 mm touch-proof interfaces -- three EMG sockets
  on the pod panel and two ear sockets on the helmet temples -- and an EMG lead will
  physically mate an ear socket. That is **not** a safety fault: all five sit behind their own
  47 kOhm series resistor on the same +/-2.5 V rails, so the current bound of section 5.5 is
  unchanged. It is a measurement fault, and a silent one: an EMG lead in an ear socket puts a
  cheek electrode on the linked reference and the whole montage moves with it. **Test T10's
  lead-off check does not catch it**, because a mis-plugged electrode is still an electrode.
  The three defences are physical separation -- panel against temple, 1500 mm apart -- the
  colour code of section 10, and the placement guide of IFU-EEG-014. That is stated, not
  mitigated, and it is open item 24. **Corrected 2026-09-02: it is six interfaces, not five**,
  because section 3.1.3 adds the bias coupler at the halo front, and **all six are sockets**,
  so the count of ways to get it wrong is six plugs into six sockets in both directions. The
  count that matters is not how many but which half: with the instrument side all sockets, no
  helmet-mounted plug exists that could be carried into anything.

**What changes in the wire list, and what does not.** Conductors 9 and 10 keep their colours,
their nets, their carrier paths, their "195 + 250 free" in-frame figure and their 2140 mm cut
length: the socket replaces the crimp at the same place on the same tail, so no arithmetic in
section 3.1 moves. What changes is the last row group of section 6 and the last 15 mm of the
build.

**Who has to decide.** The **safety reviewer**, because this is a patient-applied touch-proof
interface that is specified and not measured; **AVL-EEG-017**, because the coupler has no
vendor and is carried there as OPEN WITH CRITERIA on line K27; and the **programme**, because
the alternative -- buying the clip bare and crimping it, which is what section 3.1 used to say
-- is a decision to accept a permanent joint and to rewrite SVC-EEG-013 R4, R5 and R10 around
it. Until that is settled the two ear references cannot be built. That is open item 23.

#### 3.1.2.1 The ruling of 2026-09-02, and the provisions that come with it

Ruling **D2-EAR-REFERENCE-COUPLER** keeps the clip and the coupler above and replaces the
supporting provisions the proposal carried with the nine below, which have values. The clip is
unchanged: **AVL-EEG-017 K2 exactly as written** -- a Wuhan Greentek Ag/AgCl ear clip,
finished, leaded, carrying its own DIN 42802 touch-proof plug. The coupler is unchanged: a
free-hanging 1.5 mm touch-proof cable **socket to DIN 42802-1**, AVL-EEG-017 **K27**, crimped
or soldered onto the 250 mm temple tail at the point the crimp used to be. **K27 is placed on
the same purchase order as K2**, so that retention and finger-safety when the two are mated
are one supplier's responsibility and not an argument between two of them; the Staubli LB-I1,5
cable-socket family is the approved alternate, and the exact order code, colour suffix
included, is read off the catalogue on the day the order is raised and is not constructed
here. **No cut length moves**: 2140 mm stands, as 1500 + 120 + 20 + 195 + 40 + 15 + 250.

**1. The packing rule. This is the load-bearing provision and this document does not own the
files it changes.** The ear clips travel **mated and captive**, dressed inside the helmet bay.
PKG-EEG-015 section 1.1 line 2.1 becomes `2 fitted | HELMET HM-01`; the (408, 162) 94 x 100 mm
bay becomes EMG LEADS only; IFU-EEG-014 section 1's table and section 9 step 1 are re-issued;
and SVC-EEG-013 R12 gains an explicit line that the ear clips are left mated and dressed
inside the helmet bay, which closes the gap between its R10 and R12.

*Why it is load-bearing.* The proposal above argued that the mis-mate is an operator error,
countable at R10. It is not, as the package stands. PKG-EEG-015 section 1.1 line 2.1 reads
`Ag/AgCl ear-clip references | 2 | EAR CLIPS + EMG LEADS` -- a bare "2", where every fitted
line on that list reads "N fitted" -- and section 2.2 puts HELMET HM-01 at (14, 14) in a
197 x 236 mm bay and EAR CLIPS + EMG LEADS at (408, 162) in a 94 x 100 mm one, with the three
EMG DIN leads in the same hollow. IFU-EEG-014 section 1 renders that to the participant as
"Two ear clips on a lead, and three coloured leads for the face pads", section 2 step 3 has
the participant clipping them on, and section 9 step 1 sends them back to the same hollow. So
without this provision the participant mates and unmates both couplers **every session,
unsupervised, out of one 94 x 100 mm hollow holding five identical 1.5 mm DIN 42802 male
plugs** -- which is the exact fault the proposal claims to have removed -- and IFU-EEG-014
section 8's "You dismantle nothing" is not true. With it, RISK-EEG-011 H-20's stated mitigation
("Participant touches nothing removable") becomes true rather than aspirational. **The
programme lead signs this one**, because PKG-EEG-015 sections 1.1 and 2.2, IFU-EEG-014
sections 1 and 9, SVC-EEG-013 R12 and the RISK-EEG-011 H-20 and H-30 mitigations move
together. It is open item 34, and it requires provision 2, or the clip cannot travel dressed
inside the helmet bay.

**2. The K2 lead length, and the deviation it extends.** Apply the K1 correction verbatim to
K2: the purchase order states the lead length and the termination. **Plug-to-jaw 150 to
200 mm** -- a stated number, not the catalogue 1.0 to 1.5 m. The consequence has to be written
down rather than absorbed: the unscreened reference run becomes the 250 mm temple tail plus at
most 200 mm of clip lead, so **450 mm maximum, and it is recorded as an extension of
DEV-WH-01 to REF_L and REF_R**. Section 3.6 accepts DEV-WH-01 for the three EMG channels only;
section 4 argues at length why WH-01 is screened, and these two conductors are WH-01. **T8 --
input-referred noise, 1.0 uV RMS maximum, an RTS-1 release criterion -- is re-measured on a
built unit carrying the real K2 lead before that extension is accepted.** If it fails, the
clip lead is screened or the coupler moves to the earlobe end; length alone does not settle
it.

**3. Insulation of the free tail.** A materials row in section 4, not a label citation:
extruded PTFE or FEP sleeve, or 3:1 heat-shrink supplied at 1.5 mm or more and **recovered to
0.70 mm or less**, over the whole 250 mm free length, resisting 70 % IPA and the 40 kHz bath.
*The Brady PS-187-2-WT class of section 10 is not an alternate here and no version of this
section may cite it: it is a white thermal-transfer wire-marker sleeve at 1.6 mm recovered,
which is more than twice the 0.70 mm OD of the conductor it would have to grip. A marker
sleeve is identification, not insulation.*

**4. Strain relief -- NOT specified at this issue, and carried open.** The proposal's 2.0 mm
adhesive-lined bulb at a temple channel mouth, captured behind the cover strip, **is deleted**,
because the released HM-01 has no temple channel mouth to put it in. `tools/mech_gen.py`
defines exactly three mouths and all three are occipital: `HM01_N1_MOUTH` at (0.00, -95.38) in
the shell roof, and `HM01_HALO_MOUTH` at (+/-45.41, -82.41, -11.25). `CH_BORE` is a constant
3.80 mm everywhere, so a 2.0 mm bulb has no shoulder to react against in any case.
**Consequently test H6's 15 N leg is not applied to the ear couplers**, and the anchorage is
carried open beside the identical OE-1 / OE-2 entry gap that KNOWN_ISSUES.txt already holds.
That is open item 29. Until a temple wire exit exists in `tools/mech_gen.py` -- a mouth stepped
below 2.0 mm, or a moulded-in anchor -- and is registered, there is nothing to pull against and
nothing is tested.

**5. Tests.** Three changes, and one of them is a test the package has nowhere.

* **H3 is not extended to the couplers.** A DIN 42802 socket is single-pole and has no screen
  terminal (section 3.6 records the same fact as DEV-WH-01), step 6 cuts the WH-01 screen back
  at the helmet end so the tails are outside the screen, and H3's existing drain-to-every-
  conductor leg already covers what a coupler leg would have measured.
* **H4 gains them**: 500 V DC for 60 s, conductor bundle to any exposed metal **with the plug
  withdrawn**, with the socket body and its shroud counted as exposed metal, 100 MOhm minimum.
* **H8 gains them at 100 cycles minimum**, run as-built after step 15 with H1 repeated. The
  per-unit leg needs no new step: it lives in step 19's existing as-built repeat.
* **New H11, first article only**: an **IEC 60601-1 / IEC 61032 test-probe B** check on the
  unmated socket, recorded in the FAI pack. H4 cannot give this. H4 is a 500 V DC
  insulation-resistance measurement; finger-safety to the standard test finger is a gauge
  check, and until this issue the package substituted a supplier declaration for it.

**6. The retention window, which K27 did not have.** **Separation force 5 to 15 N, stated and
repeatable**, added to K27 beside its existing mating-force and 500-cycle line. High enough
that a snag does not part it -- this is the one net whose partial loss section 3.1 itself calls
"electrically almost invisible" -- and low enough for SVC-EEG-013 R4's tool-free release. Every
other separable interface in the kit already has a window (the bayonet at 3 to 6 N seating and
about 10 N retention, H8's 0.15 N per contact, the boom at 30 N); this one had none.

**7. Colour.** **GY on the left coupler and PK on the right stands**, because it meets K27's
actual criterion, "a colour distinct from the three EMG sockets". *The justification given as
"the section 10 one-table rule" is withdrawn: that rule is about conductor identification, not
about connector bodies.* Because K2 is bought unchanged, **the K2 purchase order gains a plug
colour**: matched to the socket, or a printed GY / PK marker sleeve on the clip lead within
25 mm of the plug.

**8. Life, and what it depends on.** With provision 1 adopted, the couplers see roughly **100
operator mate cycles over five years** -- 20 turnarounds per kit-year for five years -- against
K27's 500, a 5x margin, so the cycle count is not the binding criterion. If provision 1 is
refused, the participant adds about **250** more (SVC-EEG-013 section 3: 25 sessions is about
10 turnarounds is about half a year, so roughly 50 sessions per kit-year), for about **350 --
a 1.4x margin, not 5x**. Then three things change together and this ruling must be re-opened:
K27's cycle criterion goes to **1000 minimum**; the colour code stops being an adequate defence
against a participant choosing one of five identical plugs in one 94 x 100 mm bay, so the
mis-mate has to be killed **mechanically**, by gender reversal or keying; and open item 24's
residual is re-scored in RISK-EEG-011 as a per-session participant error rather than an
operator error at R10. Gender reversal is not cost-neutral and is the second choice, not the
first: the temple-tail plug form is a catalogue cable part, while a socket-ended ear clip is
not a Greentek catalogue line and would be a bespoke Class A patient-contact electrode.

**9. Open item 24, restated in both directions.** An EMG lead will mate an ear socket, **and**
the K2 clip's own plug will mate J15 to J17. With provision 1 both are operator errors at R10
and both are caught by R4's existing count-out of 8 cups and 2 ear clips. Without it, neither
is.

**Who signs this ruling.** The **safety reviewer**, for the patient-applied touch-proof
interface itself -- K27 against its criteria including the new 5 to 15 N separation window, the
H4 leg and the first-article H11 test-probe-B check on the unmated socket -- and for accepting
the extension of DEV-WH-01 to REF_L and REF_R **after** T8 has been re-measured on a built unit.
The **programme lead**, for provision 1, because it is the change the whole safety argument
rests on and it moves four other documents. The **mechanical reviewer with the PARTS / MECH
owner**, for the temple wire exit, because a released model has to gain a feature and be
re-cut before the H6 leg can be written at all. The **AVL-EEG-017 owner**, to place K27 on the
same purchase order as K2 and to add the lead-length and plug-colour fields to K2.
**ECO-EEG-016** carries the change record for all of it. **None of those signatures exists
today.**

**What would change it.** A submitted K27 sample that is not finger-safe to IEC 61032 probe B
with the plug withdrawn, or whose separation force is not repeatably inside 5 to 15 N over 500
cycles, kills the vendor and not the ruling -- go to the Staubli LB-I1,5 alternate. If no maker
supplies a cable socket that mates the K2 clip's plug with a stated retention force, the
fallback is to buy clip and coupler as one assembled leaded pair, which makes the temple tail a
permanent joint and forces SVC-EEG-013 R4, R5 and R10 to be rewritten around releasing at the
clip jaw. A T8 above 1.0 uV RMS on a built unit means the unscreened reference run is not
acceptable at any length.

### 3.1.3 WH-01 conductor 11 at Fpz, and WH-10 -- the ruling of 2026-09-02

**The bias pad is deleted as a helmet feature.** *Superseded on 2026-09-02: the "Fpz bias pad,
solder tag" of section 3.1's first issue, which was on no drawing, had no part number and
appeared on no model. It was open item 26 and this section narrows that item rather than
inventing the part.* Ruling **D3-BIAS-FPZ-TERMINATION** puts the electrode outside the helmet
and the joint on the harness, for three reasons that stand without any of them being decisive
alone: **there is no ninth cup, carrier, crown, spring, gel port or contact light anywhere in
the package** for a ninth HM-04 to be made of; a disposable pad needs no retention feature and
no reprocessing argument at all; and SVC-EEG-013 R5's 25-cycle disinfection compatibility
protocol **has never been run**, so nothing reusable at that site can be qualified. *The
0.62 mm of section thickness that an earlier draft argued from -- 12.55 mm needed against
11.93 mm available at Fpz -- is withdrawn as a reason. It is real, but it is the smallest
geometric deficit in the package: `mech_gen.py` records the same frame at 10.91 mm across the
temple against the 12.20 mm this document's own channel section needs. An argument that would
condemn the whole frame condemns nothing.*

**What conductor 11 lands on.** A **free-hanging 1.5 mm touch-proof socket to DIN 42802-1**, of
the same **K27 class** as the two ear couplers -- Staubli LB-I1,5 family or the Wuhan Greentek
DIN 42802 cable range, both of which AVL-EEG-017 K27 already records as catalogued cable parts
-- in **TQ turquoise**, conductor 11's own colour and distinct from the GY and PK ear couplers
and from the red / yellow / green EMG set. It hangs at the **HM-01 halo-front channel mouth**.

**What mates it.** **WH-10 / WH-EEG-008-10**, a new bought-in lead: **150 mm +/- 10 mm**, 4 mm
female snap stud to a 1.5 mm DIN 42802 touch-proof **plug**, TQ turquoise, of the **K3 class**
the three EMG leads are already bought in -- reference Staubli SLS425-SEK/N, Greentek equivalent
approved. AVL-EEG-017 **K47** buys it. This is the form suppliers actually build; a
snap-to-socket lead is not a catalogue form, which is why the socket is on the harness and the
plug is on the lead and not the other way round.

**Gender, stated once.** After this change **no plug exists anywhere on the instrument side**:
three EMG sockets on the pod panel, two ear sockets on the temples, one bias socket at the halo
front, and every mating half is a lead or a leaded electrode. A socket cannot be inserted into
anything, so the driven output cannot be carried into another interface by hand.

**The electrode.** A fourth disposable pre-gelled Ag/AgCl snap pad off the existing K4 pack
(Ambu BlueSensor N, 30 per pack), placed on prepped forehead skin **below the HM-02A brow pad**,
one per session. **The kit therefore consumes four pads per session, not three**, so a 30-pack
is seven full sessions with two pads left over. IFU-EEG-014 section 13.2's "Thirty are supplied,
which is ten sessions' worth" is arithmetically wrong at four pads and is that document's to
re-issue, together with its title "The three face pads", its "These are the only electrodes you
position yourself" and its "Match colour to colour and you cannot get them the wrong way round".
Whether a second pack is kitted is a programme decision and this document does not make it.

**Cut length: 1940 + F, and F is not invented here.** A free-hanging coupler needs a free tail;
1980 = 1500 + 120 + 20 + 285 + 40 + 15 has none, and its 40 mm site service loop has no site
left to be coiled at. The cut is **1500 + 120 + 20 + 285 + 15 + F**, tolerance +10 / -0 mm on
the fixed part. **F is stated explicitly on the wire list and is set at the first fitting
trial**: bounded below by the clearance a hand needs to mate the coupler clear of the HM-02A
brow pad, and above by the 250 mm the ear tails already carry. **Conductor 11's 1980 mm must
not be carried forward into any cut schedule** -- conductors 4 and 5 cut at 1980 mm for
unrelated reasons and are unaffected. Open item 30.

**Pull test: not H6's 15 N.** H6's 15 N is defined as acting on HM-04A's anchorage in the body
and on the solder joint; a free-hanging coupler has no body to anchor in, and 15 N is above the
**13 N** minimum at which H5 qualifies a 28 AWG crimp. Either HM-01 gains a drawn anchorage
that takes 15 N -- which returns this to the mechanical reviewer with open items 22 and 26 -- or
**the coupler retention is set at or below H5's 13 N** and carries K27's mating-force and
500-cycle criteria instead. Open item 31. Nothing is pulled at 15 N here until the anchorage
exists.

**The cross-mate is stated, not designed out.** Open item 24 grows from five interfaces to six
sockets and six plugs, and it gains a consequence RISK-EEG-011 has not analysed: **a K2 ear clip
or a K3 EMG lead will enter the bias socket**, putting an electrode on BIAS_EL, which is a
driven output and not an input, at a site RISK-EEG-011 works only at Fpz. The reach is real and
needs no lead: the halo ellipse is a = 81.10 mm lateral by b = 96.80 mm fore-aft
(`mech_gen.py`), so temple to halo front is about 126 mm straight, and the ear tails are 250 mm
free. If genuine non-interchangeability of the driven output is wanted, the answer is a
different connector **class** or a keyed shroud, not gender -- it is costable and it is referred
to the safety reviewer, who is the only person who can decide that a colour is not enough.

**This does not leave HM-01 untouched.** A dressed channel mouth against 0.70 mm OD PTFE and a
strain relief at the halo front are **new features on the carried-over HM-01 STL that no source
file generates** (PARTS-EEG-019 OA-1: STL only, no STEP, no parametric source). The released
frame has three channel mouths and all three are occipital, so the halo-front mouth this section
needs does not exist any more than the temple mouths of 3.1.2.1 provision 4 do. **Three wire
exits are now owed on one frame that cannot be regenerated from source.** Open item 26 is
narrowed to that, and is not closed.

**SR-12 stays open, and this change does not close it.** Touch-proofing an interface does not
alter what flows out through the electrode into the person. The number has moved and it has to
be stated correctly rather than quoted from memory: with `tools/design.py`'s channel-11
override deleted on 2026-09-02, D11 and C11 sit on BIASOUT behind the full 47 kOhm like the
other fifteen channels, so the shorted-clamp case collapses into the ordinary single-fault case
of section 5.5 -- **53.2 uA on bound A (2.5 V / 47 kOhm) and 41.2 uA on bound B (2.5 V /
60.615 kOhm) today, and 36.8 uA once ECO-EEG-024 raises the series resistors to 68 kOhm.**
*The 183.6 uA that KNOWN_ISSUES and RISK-EEG-011 SR-12 record for this node, and the unbounded
bound A beside it, are superseded by that change on 2026-09-02 and must not be re-quoted.*
What is **not** superseded is that 53.2 uA is still over S-02's 50 uA single-fault limit and
that **SR-12's disposition is the safety reviewer's to record**. RISK-EEG-011 offers three ways
to close it -- move D11 and C11 to the module side, add a second series element, or accept the
topology with a written justification -- and the first of those has now been done in the source.
**None of the three is a connector.** No reviewer should read this section as closing SR-12.

**Who signs.** The **safety reviewer** first, on three things together: that a K27-class
touch-proof socket is the correct patient-side form for the driven output; that the residual
cross-mate above is **accepted and stated** rather than mitigated; and that SR-12 remains open.
Then the **mechanical reviewer**, with open items 22 and 26, for the halo-front mouth, the
dressed exit and the strain relief, and because the coupler retention value depends on whether
an anchorage is drawn. Then **PARTS-EEG-019 and ECO-EEG-016**, to issue WH-10 / WH-EEG-008-10
-- WH-01 to -07 and -09 are in use and WH-08 is withdrawn and not reused, so -10 is the next
free number. Then **AVL-EEG-017**, to open K47 for the lead and to carry the bias socket as a
third unit against K27's existing criteria. Then **IFU-EEG-014's owner**, for section 13.2.
**None of those signatures exists today.**

### 3.1.4 The K12 preload spring -- issued 2026-09-02, and why it can be issued now

**Ruling D5-K12-SPRING-ENVELOPE declined to issue a dimensioned envelope**, and it was right to,
because the two things a vendor quotes against did not exist: the carrier had no rest position,
since `hm04()` cut no circumferential bayonet run, and the only free volume above the spigot was
1.40 mm, which is a washer band and not a spring band. **Both facts changed on 2026-09-02 and
both are measured, not asserted.** The run is cut -- 100 degrees at r 4.30 to 5.55, z 1.10 to
3.80, over a 1.10 mm retaining lip -- and `tools/simulate_production.py` measures 0.000 mm3 of
interference through the quarter turn and through the carrier's 0.40 mm of axial travel. The
seat roof moved from z 13.50 to **z 15.60**, so the free height above the spigot went from
1.40 mm to **3.50 mm**. The specification below is therefore derivable, and it is issued.

*Superseded with it, on the same date and for the same reason: D5's provision that the part
must be a multi-turn crest-to-crest wave spring, and its finding that a coil cannot be used.
That finding was correct against a 1.40 mm band -- the seat/spigot annulus is 0.10 mm on the
radius, so no coil fits around the spigot and the spring must sit ON the spigot top, which
made the free height the entire budget. With 3.50 mm of budget a coil fits, and a coil is what
AVL-EEG-017 K12 has always said it was buying.*

**The geometry, read from `tools/mech_gen.py` at this issue** *(model figures; no HM-04 and no
HM-05B has been printed)*:

| Datum | Value |
|---|---|
| HM-04 spring seat | 6.80 dia, z 9.00 to 15.60 |
| HM-04 gel port | 2.50 dia through the seat roof, on the axis |
| HM-05B body / spigot | 9.10 dia x 8.60 mm body in a 9.20 x 9.00 mm bore; 6.60 dia x 3.50 mm spigot; 2.40 dia passage on the axis |
| Spigot top, carrier fully down | z 12.10 |
| Working height at rest | **3.50 mm** = 15.60 - 12.10 |
| Working height at the hard stop | **3.10 mm**: the carrier body top meets the seat shoulder at z 9.00 after 0.40 mm of travel |
| Working stroke | **0.40 mm** -- the travel the cup makes when it is pressed against the scalp, not slack |

**One discrepancy is reported and not resolved here.** The lug sits at z 1.20 to 3.30 and the
retaining lip roof is at z 1.10, so a carrier resting on its lip stands 0.10 mm proud of the
cup face and its spigot top is at z 12.00, which makes the rest height **3.60 mm** and the
stroke **0.50 mm**. The 3.50 / 0.40 figures above are the ones `mech_gen.py` states, taken from
the 9.00 mm bore against the 8.60 mm body. The two readings differ by one printed layer and the
difference belongs to `tools/mech_gen.py`, which this document does not own -- open item 33.
**The spring below is specified so that it does not matter**: it holds the force window over
every installed height from 3.10 to 3.60 mm, and over the tolerance band around both.

**The tolerance band the spring must work over.** MJF is +0.15 / -0.05 mm and the package gates
that fit at 9.20 / 9.35 / 9.15 mm on FIT-01. The installed height is a stack of two printed
dimensions -- the HM-04 seat depth and the HM-05B body-plus-spigot height -- so **+/- 0.25 mm**
is allowed on it (+/- 0.30 worst case, +/- 0.21 root-sum-square, rounded up). The spring must
therefore hold its window over installed heights of **2.85 to 3.85 mm**.

**The specification, and the arithmetic behind every number.** Force target 3 to 6 N is
AVL-EEG-017 K12's own stated target and is **not** derived here; everything else is derived
from it and from the geometry above.

| Characteristic | Value | Where it comes from |
|---|---|---|
| Form | helical compression, **closed and ground both ends** | the 3.50 mm band now takes a coil; a ground end is required so the load spreads over a full turn of PA12 rim rather than a short arc |
| Material | **stainless AISI 302 spring temper to ASTM A313**, as K12 says | K12; see the open material question below |
| Wire diameter d | **0.50 mm** | the largest wire that reaches 1.20 N/mm inside the 6.50 / 5.40 mm envelope and still stacks short: at 0.55 mm the same rate needs 3.1 active coils and a solid height of 2.82 mm, over the 2.60 mm limit below |
| Outside diameter | **6.40 mm nominal, 6.50 mm maximum** free and at every point of the stroke | the seat bore is 6.80 mm at +0.15 / -0.05, so 6.75 mm worst case: 0.25 mm of diametral clearance at the tight end. Calculated coil growth at solid is 6.46 mm, so the 6.50 ceiling holds through the stroke |
| Inside diameter | **5.40 mm minimum** | so the coil bears on the PA12 spigot rim between r 2.70 and r 3.20, inside the rim's r 1.20 to 3.30 and clear of the 2.40 mm passage; at the top it bears between the 2.50 mm gel port (r 1.25) and the bore wall (r 3.40). **Neither end covers the gel port** |
| Mean coil diameter | 5.90 mm; spring index 11.8 | 6.40 - 0.50 |
| Active coils | **2.2** | k = G d^4 / (8 D^3 n) with G = 69 000 MPa for 302: 69 000 x 0.50^4 = 4 312.5, 8 x 5.90^3 = 1 643.0, so k = 2.625 / n and n = 2.19 for 1.20 N/mm |
| Rate k | **1.20 N/mm +/- 10 %** | chosen low on purpose: the whole 3 to 6 N window is 3 N wide, and 0.50 mm of stroke plus +/- 0.25 mm of build tolerance is 1.00 mm of height variation, which at 1.20 N/mm is 1.20 N of it |
| Free length | **6.90 mm +/- 0.20 mm** | set so the worst-case low still preloads: 1.08 N/mm x (6.70 - 3.85) = **3.08 N**, above the 3 N floor |
| Solid height | **2.10 mm calculated; 2.60 mm maximum** | 4.2 total coils x 0.50 mm. The maximum is the ruling's own relation, solid height at least 0.25 mm below the minimum working height of 2.85 mm |
| Squareness | 3 degrees maximum | it is unguided at both ends |
| Ends | ground square, deburred | PA12 bearing |

**The forces that result, calculated:**

| Condition | Installed height | Force |
|---|---|---|
| At rest, nominal build | 3.50 mm | 1.20 x (6.90 - 3.50) = **4.08 N** |
| At rest, on the lip reading | 3.60 mm | **3.96 N** |
| At the hard stop, nominal | 3.10 mm | **4.56 N** |
| Worst case low, k and L0 both low, build tall | 3.85 mm | 1.08 x (6.70 - 3.85) = **3.08 N** |
| Worst case high, k and L0 both high, build short | 2.85 mm | 1.32 x (7.10 - 2.85) = **5.61 N** |
| If it were stacked solid anyway | 2.10 mm | 1.20 x 4.80 = **5.76 N**, and about 6.7 N at the worst case of rate, free length and wire tolerance together |

**Three consequences worth stating, because they are what the low rate buys.**

* **The force is bounded by the spring and not by the assembler.** The carrier reaches its
  mechanical stop -- body shoulder on seat shoulder -- with 1.00 mm of spring travel still in
  hand at nominal and 0.75 mm at worst case, so the spring cannot stack solid inside the
  stroke. And even if it did, it delivers under 6.7 N. The failure the ruling was most
  concerned by -- a rigid metal stack handing the scalp whatever the helmet presses with, for a
  two-hour session, on a patient-applied part -- cannot happen at this rate.
* **The PA12 rim is not overloaded.** A ground end bears over about one full turn, pi x 5.90 x
  0.50 = 9.3 mm2, so 4.56 N is **0.49 MPa** against PA12's compressive strength of tens of MPa.
  An unground end would land on a short arc and multiply that by roughly three, which is why
  the ground end is a requirement and not a preference.
* **The steel is not near its limit.** Wahl factor 1.12 at index 11.8; shear stress
  8 F D Kw / (pi d^3) is **615 MPa** at the 4.56 N working maximum, 809 MPa at the 6 N ceiling
  and about 900 MPa if it were stacked solid at worst case, against a minimum tensile of about
  2 000 MPa for 0.50 mm 302 spring wire -- 31 %, 40 % and 45 %. Helix angle 8.2 degrees, under
  the 12 degrees at which the rate formula stops holding. Free length over mean diameter is
  1.17, well under the 2.6 at which a squared-and-ground spring buckles between parallel faces.

**The no-gold relation, and it does not close at the crown diameter this document proposes.**
The spring must not touch HM-05C: not because a stainless ring bearing on gold is a second
metal junction in parallel with the measurement -- seated on PA12 at one end, it is a dead-end
stub -- but because of **galling of the gold-over-nickel plating K25 and K26 require, under the
90-degree turn SVC-EEG-013 R4 performs at eight sites every turnaround**. The rule has to be a
relation and not two independent limits, because float is what defeats it:

> (ID minimum - crown OD maximum) / 2 >= (seat bore maximum - spring OD minimum) / 2 + 0.05 mm

With ID 5.40 minimum, spring OD 6.30 minimum and a seat bore of 6.95 mm at the loose end of MJF,
the right-hand side is 0.375 mm and the relation requires a **crown outside diameter of 4.65 mm
or less**. Section 3.1.1's crown is proposed at **5.20 mm**, which fails it by 0.55 mm on the
diameter: at the extreme of its float the coil reaches the gold. Three ways out, and the choice
is the **mechanical reviewer's on MECH-EEG-020 sheet 8**, not this document's and not a
purchase specification's:

1. bring the crown outside diameter down to 4.65 mm or less;
2. recess the crown's upper face **0.15 mm below the spigot rim** -- equivalently, stand the rim
   0.15 mm proud of the crown -- so that an overhanging coil cannot reach it. HM-04A's leaf then
   travels 0.15 mm further, which it is sprung to do;
3. locate the spring radially to +/- 0.10 mm with a feature on the rim or in the seat.

**The spring is not part of the electrical joint, and that is a measurement and not a claim.**
It bears on printed PA12 at both ends. The first-article check below measures it.

**Qualification regime.** 25 cycles of **SVC-EEG-013 R6** -- two 10 ml warm-water passes,
demineralised rinse, 1 bar air or less -- plus a 70 % IPA wipe and a conductive-paste dwell:
the same regime K25 carries. **Not the cups' 40 kHz R5 bath.** ASM-EEG-007 section 4.2 bonds
HM-04 into HM-01 and SVC-EEG-013 R5 lists HM-01 as wipe, never immersed, so this spring never
sees the bath even though the cup it sits above does.

**What must be measured on the first five, before any fleet order.** K12 already requires five
pieces; these are what is measured on them, **on a printed HM-04 / HM-05B pair and not only on
the bench**:

| # | Measurement | Accept |
|---|---|---|
| 1 | Free length, each piece | 6.90 +/- 0.20 mm |
| 2 | Solid height, each piece | 2.60 mm maximum |
| 3 | Rate, from force at 3.60 mm and at 3.10 mm | 1.20 N/mm +/- 10 % |
| 4 | Force at 3.60 mm and at 3.10 mm | inside 3.0 to 6.0 N at every height from 2.85 to 3.85 mm |
| 5 | Outside diameter free and compressed to 2.85 mm; squareness | 6.50 mm maximum; 3 degrees maximum |
| 6 | Seating in the printed pair, spring pushed to one side of the seat | the coil bears wholly on the spigot rim and **does not touch HM-05C** -- the go / no-go against the no-gold relation |
| 7 | Gap between the carrier's mechanical stop and the spring's solid height | 0.25 mm minimum, measured, not calculated |
| 8 | Resistance, spring to HM-05C and spring to HM-04A, dry; and H1 site-to-connector with the spring removed | 10 MOhm minimum; H1 unchanged. **This is the check that the preload member is not the conductor** |
| 9 | After 25 cycles of the R6 + IPA + paste regime: free length, force at 3.60 mm, and a 20x inspection under the coil ends | free-length loss 5 % (0.35 mm) maximum; force still 3.0 N minimum; no crevice pitting |
| 10 | With the spring fitted: the bayonet still turns with the HM-09 key, and SVC-EEG-013 R10's 10 N straight pull still does not release the carrier | as R10 |

**The material question the ruling raised and this specification does not settle.** K12 says
302 and 302 is what is specified above, because that is the line the programme is buying
against. The ruling's finding stands beside it and is not dismissed: **the seat is a chloride
crevice under the coil ends that is never immersed, never scrubbed and never fully dried**, and
on that argument 316 spring temper would be mandatory rather than an alternate. Measurement 9 is
what decides it. If it shows pitting or relaxation, the line goes to **316**, and beyond that to
Elgiloy; the change costs a purchase-order line and no geometry, which is why it is safe to
resolve it on evidence rather than on argument.

**Still absent, and named so that nobody reads this section as more finished than it is.** The
spring has **no retention or capture feature**: nothing holds it if a carrier is drawn without
one. **ASM-EEG-007 has no step that fits it and SVC-EEG-013 has no step that handles it**
(KNOWN_ISSUES.txt records that no assembly step fits the cups, the carriers or the springs at
all). Section 8 step 14a of this document is the harness half of that and it is not enough on
its own. Open item 32.

**Who signs, and the order matters.** (1) The **mechanical reviewer on MECH-EEG-020 sheet 8**:
the crown dimension, so the no-gold relation becomes a pair of limits rather than a failure; a
capture feature for the spring; the one-time allocation of the z 11.70 to 14.30 band across
HM-04A's anchorage, the LED seat and its two lead passages and the dressed conductor exit; and
the 0.10 mm rest-datum question of open item 33. (2) The **safety reviewer**: this is a
patient-applied part, the solid-height bound is what keeps the force bounded, and a stainless
preload member inside a gel-flushed volume is signed as an accepted open item or designed out.
(3) **AVL-EEG-017 with a spring maker** -- K12 names Lee Spring, Century Spring and Gutekunst --
against the five measured samples above, and only after (1). (4) **ECO-EEG-016**, to carry the
change to this section and to AVL-EEG-017 K12, K25 and K26, because this contradicts a live
proposal rather than silently overwriting it. **SAMPLE ONLY until all ten measurements pass.
No fleet order.**

### 3.2 WH-02 -- helmet contact-light cable, 10-way, to J30

Insulation PVC. Same 7/0.1 mm tinned-copper conductor. Cut lengths use the same
1640 mm pre-frame allowance as WH-01, then the channel-B routed length + 55 mm.

| Cond | Colour | Gauge | Insul. | From (helmet terminal) | To (pin) | Net | Carrier path | In-frame (mm) | Cut (mm) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WH/BK | 28 AWG eq. | PVC | Fz LED, lead A | J30.1 | LED1 | R70 1k -> SR_Q0 (J19.8) | 330 | 2025 |
| 2 | RD/BK | 28 AWG eq. | PVC | Cz LED, lead A | J30.2 | LED2 | R71 -> SR_Q1 (J19.9) | 220 | 1915 |
| 3 | BU/BK | 28 AWG eq. | PVC | Pz LED, lead A | J30.3 | LED3 | R72 -> SR_Q2 (J19.10) | 145 | 1840 |
| 4 | GN/BK | 28 AWG eq. | PVC | C3 LED, lead A | J30.4 | LED4 | R73 -> SR_Q3 (J19.11) | 300 | 1995 |
| 5 | YE/BK | 28 AWG eq. | PVC | C4 LED, lead A | J30.5 | LED5 | R74 -> SR_Q4 (J19.12) | 300 | 1995 |
| 6 | BN/BK | 28 AWG eq. | PVC | T7 LED, lead A | J30.6 | LED6 | R75 -> SR_Q5 (J19.13) | 190 | 1885 |
| 7 | OG/BK | 28 AWG eq. | PVC | T8 LED, lead A | J30.7 | LED7 | R76 -> SR_Q6 (J19.14) | 190 | 1885 |
| 8 | VT/BK | 28 AWG eq. | PVC | F7 LED, lead A | J30.8 | LED8 | R77 -> SR_Q7 (J19.15) | 265 | 1960 |
| 9 | GY/BK | 28 AWG eq. | PVC | WH-BUS-01 pad 9 | J30.9 | LED_V | R78 (0R) from LED_PWM, GPIO48 | 30 | 1725 |
| 10 | BK black | 28 AWG eq. | PVC | WH-BUS-01 pad 10 (isolated) | J30.10 | LED_GND | R79 (0R) to DGND | 30 | 1725 |

Eight LED_V tails leave WH-BUS-01 and run beside their matching LEDn conductor to the second
lead of each site LED:

| Tail | Colour | From | To | Length |
|---|---|---|---|---|
| WH-02T-1 to -8 | GY/BK | WH-BUS-01 pads 1 to 8 | Fz, Cz, Pz, C3, C4, T7, T8, F7 LED lead B | matching LEDn in-frame length less 30 mm |

**LED_GND carries no LED current in either drive phase.** The contact lights are two-lead
bicolour devices between LEDn and the LED_V common: phase A drives LED_V high and Qn low
(green), phase B drives LED_V low and Qn high (red), and alternating fast enough reads as
amber. The requirement is that the alternation is above 100 Hz; the fitted value is
**240 Hz**, `LIGHT_PHASE_HZ` in `board_pins.h`. The return in both phases is LED_V. LED_GND
is a 0 V guard conductor, held at DGND through R79, laid in the geometric centre of the
WH-02 bundle so that the eight switched lines always have a 0 V neighbour and their
displacement current returns beside its source rather than through the wearer. It is landed
on an isolated pad of WH-BUS-01 and connected to nothing else. It exists so the return
topology can be changed by ECO without a new cable.

**The bicolour phase scheme is specified and not yet coded.** `lights_write()` and
`lights_task()` in the firmware are on and off only, per FW-EEG-001 section 1.1, so the
amber state that TST-EEG-004 T11 tests cannot pass until the driver is written. The cable is
built for the scheme regardless, because the wiring is the same either way.

Drive current is (3.3 - 2.0) / 1000 = **1.3 mA per site**, so **10.4 mA total** sourced or
sunk by GPIO48 with all eight lit. LED_V is GPIO48, an input at reset, so nothing on the
head can light at boot whatever the shift register happens to contain, and all eight lights
are forced dark during recording blocks (RFQ E-27).

#### 3.2.1 WH-BUS-01 -- the contact-light bus board

WH-BUS-01 is what makes the sentence "there are no splices anywhere in the kit" true. LED_V
arrives at N1 as one conductor and has to become nine -- the incoming conductor plus eight
tails -- and the alternative to a board is eight crimp splices buried under a cover strip
inside a helmet that a participant puts on and takes off. PARTS-EEG-019 Rev B registered the
part, gave it a size and a pad count, and recorded that no Gerber set existed for it. That
set now exists: `kicad/wh-bus-01/`, written by `tools/wh_bus.py`, with a README beside it
that carries the stack-up, the finish and the panel.

| Property | Value |
|---|---|
| Size | **14.0 x 10.0 mm**, rectangular, no cut-outs, no slots, no mounting hole |
| Layers | **two**, both signal. No plane and no pour: there are two nets on this board |
| Stack-up | mask / 35 um L1 / FR-4 core 0.71 / 35 um L2 / mask = **0.80 mm +/- 10 %** finished |
| Material | FR-4, Tg >= 150 C, 1 oz (35 um) copper both sides -- the carrier's material, so one qualification covers both boards |
| Finish | ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um, as EEG-CAR-01. Lead-free HASL is acceptable on notice |
| Mask / legend | green LPI both sides; white legend both sides. The bottom legend is mirrored in the data |
| Pads | ten, 1.60 mm, on a 2.70 x 4.80 mm grid, two rows of five. Pad 9 is square |
| Plated holes | ten, **0.80 mm finished**, one drill tool, 0.40 mm annular ring |
| Minimum clearance used | 1.10 mm, LED_V to the LED_GND island. Nothing here is near a fabricator's limit |
| Panel | 5 x 4 V-scored array, 20 up, step 14.0 x 10.0 mm, 5 mm rails: an 80.0 x 50.0 mm panel |
| Electrical test | 100 % to the supplied IPC-D-356A netlist |

**Two layers, where the register says one.** The pads are plated through holes, and plating
needs two layers. A 28 AWG 7/0.1 mm conductor soldered to a surface-only pad is held by the
pad's peel strength alone; through the board and soldered on both sides it is held by the
barrel. The board sits in a helmet under a cover strip and is handled every time a
conductor is replaced, so that difference is the whole argument. The second layer also
doubles the bus copper and costs nothing at these quantities. **PARTS-EEG-019 Rev B's
"single-layer FR-4" wording and its "no Gerber set has been generated for it" status were both
superseded by this data set, and PARTS-EEG-019 is corrected on both counts at its 2026-09-02
issue**; that closes open item 15.

**The hole size is derived, not measured.** 1.60 mm is the registered pad. 0.80 mm is the
hole that pad wants for the conductor it takes: the WH-02 conductor is 7/0.1 mm tinned
copper, about 0.30 mm across the strand bundle (section 4), and 0.80 mm leaves 0.25 mm all
round for tinning and for solder to wick. It is not the carrier's 1.00 mm socket-strip
hole; the two boards share no drill programme, and 1.00 mm would only mean more solder in
each joint. No joint has been made yet, so this is arithmetic, not experience.

**No resistor goes on this board.** The eight series resistors are R70 to R77 on the
carrier, 1 kOhm each, between the 74HC595 outputs at J19.8-15 and the cable, and the common
reaches the cable through R78, 0 ohm. The 1.3 mA per site is already set there. A resistor
here would be a second limit in the same loop and would change a current that this
document, ICD-EEG-006 and TST-EEG-004 all quote. Ten pads, one copper bar, nothing fitted --
so there is no CPL file, no paste layer and no stencil for this part, and their absence is
the design rather than an omission.

**Pad map.** Fabrication coordinates, origin at the bottom-left corner with Y up, the same
convention as the Gerbers, the drill file and the netlist.

| Pad | Net | x, y (mm) | Shape | What lands on it |
|---|---|---|---|---|
| 1 | LED_V | 4.50, 7.40 | round | tail WH-02T-1, to the Fz LED lead B |
| 2 | LED_V | 7.20, 7.40 | round | tail WH-02T-2, to the Cz LED lead B |
| 3 | LED_V | 9.90, 7.40 | round | tail WH-02T-3, to the Pz LED lead B |
| 4 | LED_V | 12.60, 7.40 | round | tail WH-02T-4, to the C3 LED lead B |
| 5 | LED_V | 4.50, 2.60 | round | tail WH-02T-5, to the C4 LED lead B |
| 6 | LED_V | 7.20, 2.60 | round | tail WH-02T-6, to the T7 LED lead B |
| 7 | LED_V | 9.90, 2.60 | round | tail WH-02T-7, to the T8 LED lead B |
| 8 | LED_V | 12.60, 2.60 | round | tail WH-02T-8, to the F7 LED lead B |
| 9 | LED_V | 1.80, 7.40 | **square** | WH-02 conductor 9, GY/BK, LED_V from J30.9 |
| 10 | LED_GND | 1.80, 2.60 | round | WH-02 conductor 10, BK, LED_GND from J30.10 |

Pad 9 is square, and that is the only orientation feature the board has: the square pad and
the "9" on the legend mark the input end, which faces OE-2. Fitted the other way round the
eight tails still reach their LEDs, but the input pair has to cross the whole board and the
N1 cover strip will not close over the crossing conductors.

Pad 10 is an island. It is 1.10 mm from the nearest LED_V copper on both layers and it is
connected to nothing, which is the point: LED_GND is a 0 V guard conductor and must not
become a return path (open item 9). That isolation is also the one property of this board
that a visual inspection will not catch, which is why the IPC-D-356A netlist ships with the
Gerbers and why the electrical test is not optional. If an ECO ever ties LED_GND to
something, the tie is a wire link off pad 10, not a new board.

**What is still unknown.** No WH-BUS-01 has been fabricated, soldered or measured; the
clearances, the annular ring and the copper-to-edge figures above are computed by
`tools/wh_bus.py --check` from the geometry that produced the Gerbers, and nothing else
about the board has been verified. V-scoring 0.80 mm material is at or near the lower limit
at several fabrication houses, so the panel line is the one most likely to come back as a
question; the README states the tab-routed alternative. And **HM-01 has no pocket, no boss
and no location feature for this board at N1** -- it is retained by the cover strip and by
its own ten solder joints, and no drawing says where within N1 it beds. That is open item
16.

### 3.3 WH-03 -- boom microphone pigtail, 4-way, to J18

From J18 on the carrier to the 4-conductor 3.5 mm panel jack on adapter WH-ADP-01, which is
specified in section 3.9. Length 220 mm. Rev A put that jack "3 mm behind a recessed 7.0 mm
opening in the POD-P1 underside"; `tools/mech_gen.py` cuts a **6.5 mm opening in the
right-hand wall** at design (122.0, 90.0) and cuts nothing in the underside, so the jack face
finishes 2.5 mm behind the outer face -- the wall thickness -- and the Rev A sentence is
withdrawn.

| Cond | Colour | Gauge | Insul. | From | To | Net | Note |
|---|---|---|---|---|---|---|---|
| 1 | RD red | 28 AWG eq. | PTFE | J18.1 | jack tip (T) | VOICE_RAW | high-impedance electret line, on to J21.4, the preamplifier input on MP-01 |
| 2 | BK black | 28 AWG eq. | PTFE | J18.2 | jack ring 1 (R1) | DGND | capsule return |
| 3 | BK black | 28 AWG eq. | PTFE | J18.3 | jack ring 2 (R2) | DGND | screen return at the jack |
| 4 | BK black | 28 AWG eq. | PTFE | J18.4 | jack sleeve (S) | DGND | shell |
| -- | bare drain | 30 AWG | -- | J18.2 (pod end only) | cut back at the jack | DGND | see section 5.3 |

**The preamplifier is on MP-01, not on the boom and not on the carrier.** The boom carries
the bare electret capsule and its screen, and nothing else. VOICE_RAW arrives on this
pigtail at J18.1, crosses to J21.4, and the amplified VOICE_PRE returns on J21.3 for the
codec at J9.1 and for envelope channel 2. `design.py` governs: J21 is a carrier socket, and
purchased modules sit on MP-01 and connect through keyed jumpers, so the module in the J21
jumper is physically on the plate. This settles the v1 conflict in which DESIGN_FACTS
section 2, RFQ section 2, RFQ E-14 and DSN-EEG-003 section 2 all put the preamplifier on the
boom, and Rev A of this document put it on the carrier. All of those are corrected to MP-01.
Keeping the amplifier off the head keeps 3.3 V off the head, keeps the boom immersible in
the ultrasonic refurbishment bath, and costs a high-impedance run that section 4 handles by
screening it and keeping it short.

**Which preamplifier is not settled, and this document does not settle it.** The MAX9814
named throughout package v1 is an automatic-gain-control part, and RFQ E-14 requires AGC
off; disabling it is a module-dependent modification. The preferred route is a fixed-gain
part of the MAX4466 class, such as Adafruit 1063. Until a part is bought and measured the
module is specified **by interface only**, in ICD-EEG-006, and AVL-EEG-017 carries the
MAX9814 as **not approved**. Nothing on this pigtail changes with the choice; what changes
is R89 (2k2, DO NOT POPULATE), the electret bias, which is fitted only if the module finally
chosen does not supply its own, per ICD-EEG-006 section 7.2.

**MIC_MUTE does not reach the boom in Rev B.** The mute line exists only at J9.4 and J28.4,
both inside the pod. No logic edge travels to the head.

WH-03B, the boom lead itself, is 1700 mm: capsule + to tip, capsule - to ring 1, screen to
ring 2 and sleeve, terminated in a moulded 3.5 mm 4-conductor plug.

### 3.4 WH-04 -- headphone panel pigtail, 4-way, to J27

From J27 to a second 4-conductor panel jack of the same part on adapter WH-ADP-01B, which is
specified with WH-ADP-01 in section 3.9. Length 190 mm. Using the 4-pole part for a stereo
output is deliberate: the fourth contact becomes
the insertion detect that J27.4 reserves, and the kit then carries one jack part number, not
two.

| Cond | Colour | Gauge | Insul. | From | To | Net |
|---|---|---|---|---|---|---|
| 1 | WH white | 28 AWG eq. | PTFE | J27.1 | jack tip | HP_L |
| 2 | RD red | 28 AWG eq. | PTFE | J27.2 | jack ring 1 | HP_R |
| 3 | BK black | 28 AWG eq. | PTFE | J27.3 | jack sleeve | HP_GND |
| 4 | GY grey | 28 AWG eq. | PTFE | J27.4 | jack detect contact | NC_HP_DET |

HP_TAP, the stimulus envelope source, is taken on the codec module at J8.10 and never
appears on this cable, which satisfies RFQ E-16's requirement that the tap sit before any
user-adjustable control.

The headphones this pigtail drives are specified in RFQ A-04 as **32 to 64 Ohm**, and the
calibrated output level is measured per model; the shipped ATH-M20x is 47 Ohm. The
harness is indifferent to the impedance, but the acoustic limit is not: RFQ E-29 caps the
output at **100 dB SPL** at any commanded level, against a calculated full-scale output of
about 110 dB SPL, and that clamp lives in the firmware volume register, not in this cable.
The requirement is therefore **not met by hardware here** and cannot be, and this pigtail
does nothing to enforce it.

### 3.5 WH-05 -- room microphone cable, 4-way, to J28

From J28 to the room-microphone module mounted behind the meshed acoustic port in the POD-P1
wall. Length 180 mm.

| Cond | Colour | Gauge | Insul. | From | To | Net |
|---|---|---|---|---|---|---|
| 1 | RD red | 28 AWG eq. | PTFE | J28.1 | module VDD | DVDD3V3 |
| 2 | BK black | 28 AWG eq. | PTFE | J28.2 | module GND | DGND |
| 3 | WH white | 28 AWG eq. | PTFE | J28.3 | module OUT | ROOM_PRE |
| 4 | YE yellow | 28 AWG eq. | PTFE | J28.4 | module MUTE | MIC_MUTE |
| -- | bare drain | 30 AWG | -- | J28.2, pod end only | cut back at the module | DGND |

The mute must be a hardware gate in the module's signal path, driven by GPIO21, and not a
firmware-only mute, which is what RFQ E-15 asks for. **No room-microphone module is known
to meet E-15**, so the interface above is specified against a candidate and not a qualified
part: a Knowles SPU0414HR5H-SB class analogue MEMS capsule with a TI TS5A3159 analogue
switch in the output path, carried on adapter WH-ADP-02, which is specified in section 3.9,
with the module interface governed by ICD-EEG-006. If no catalogue module qualifies, the
fallback is that same capsule and
switch as a programme-designed sub-assembly, which needs a drawing, a part number and an
AVL line that none of them has today. This wire list does not change in either case.

### 3.6 WH-06 -- EMG DIN lead set, 3 off

Bought-in, not built: 1000 mm lead, 4 mm female snap stud to a touch-proof 1.5 mm DIN 42802
plug. Reference part Staubli SLS425-SEK/N, 1.0 m; approved alternate Greentek equivalent.

| Lead | Colour | Site | Socket | Net | Carrier path |
|---|---|---|---|---|---|
| WH-06-1 | RD red | cheek | J15 | EMGIN1 | R12 -> D12 -> C12 -> EMG1 (J4.1) |
| WH-06-2 | YE yellow | submental (chin) | J16 | EMGIN2 | R13 -> D13 -> C13 -> EMG2 (J4.2) |
| WH-06-3 | GN green | laryngeal (neck) | J17 | EMGIN3 | R14 -> D14 -> C14 -> EMG3 (J4.3) |

**The lead colours are red, yellow and green because that is the ruling, not because this
document prefers them.** Rev B as first issued bought these three leads as white, brown and
grey while IFU-EEG-014 section 13.2 and PKG-EEG-015 section 4.2 named red, yellow and green
for the same three sites, and this section reported that as undecided. It is decided.
**IFU-EEG-014 Rev B section 13.2 rules the code red / yellow / green**, in its control note,
and carries the ruling in its section 16 item 11; the reasoning recorded there is that the
person who has to resolve a colour difference is the participant, matching a lead in the
hand against a coloured socket legend under a desk lamp, and white against grey is not a
distinction to ask of anyone in a mirror. The code the participant reads is the code that
governs, so this document is re-issued to it rather than the other way round.

Nothing in this document depended on the white / brown / grey names: the three leads are
distinguished by socket and by net everywhere else, and WH-06 is bought in rather than
built. IFU-EEG-014 records that the lead set is a catalogue item stocked in either code, so
the ruling costs nothing at the harness and nothing in lead time. What it does do is make
the colour a controlled characteristic: the Staubli SLS425-SEK/N line and any approved
alternate must name red, yellow and green on the order, and goods-in checks the three
colours against this table before the set is kitted. Former
open item 7 of section 11 is closed by this correction and its number is not reused.

The **carrier sockets at J15 to J17 have no confirmed part.** `design.py` names Staubli
SLB1,5-F / LB-I1,5, but those are cable and panel parts, not PCB parts, and no catalogue
part has been confirmed to fit the footprint: a touch-proof 1.5 mm socket with a PCB-mount
signal pin and two 1.5 mm retention posts. It must be sourced and first-articled before
Phase 2 and AVL-EEG-017 carries a 12-week lead-time risk against it. What the footprint
requires is fixed: a 1.70 mm plated hole for the signal pin with six 1.50 mm non-plated
retention posts that carry no copper and no mask (ECO-EEG-012). This is a Class A
patient-contact part on every unit and it has no vendor.

**Deviation DEV-WH-01.** DSN-EEG-002 Rev E section 6 calls the EMG runs "3 x screened". A
DIN 42802 touch-proof socket is single-pole and has no screen terminal, so there is nowhere
for a screen to land. The EMG leads are unscreened. This is recorded as a deliberate
deviation rather than a defect; the alternative -- a ground stud beside the panel wired to
AGND_REF -- was rejected because it puts an exposed conductor referenced to the analogue
mid-rail on the outside of the pod. DSN-EEG-002 is corrected at its next revision.

### 3.7 WH-07 -- charge-port pigtail, 2-way, to J24

From J24 (JST B2B-PH-K, 2.00 mm pitch) to the charge-only USB-C receptacle on adapter
WH-ADP-03, which is specified in section 3.9. Length 150 mm.

| Cond | Colour | Gauge | Insul. | From | To | Net |
|---|---|---|---|---|---|---|
| 1 | RD red | 24 AWG | PVC | J24.1 | receptacle VBUS (A4, A9, B4, B9 commoned) | VBUS_IN |
| 2 | BK black | 24 AWG | PVC | J24.2 | receptacle GND (A1, A12, B1, B12 commoned) | DGND |

24 AWG here, not 28, because this pair carries the full charge current: F1 is a 1.1 A hold /
2.2 A trip PTC and the conductor must not be the fuse. Calculated loop resistance at 0.079
Ohm/m for 24 AWG over 0.3 m is 0.024 Ohm; at 1.1 A that is 26 mV, which is inside the
charger's input tolerance.

The receptacle carries two 5.1 kOhm CC pull-downs so a Type-C source presents 5 V. **No data
conductor enters this cable.** D+, D-, SBU and the CC lines terminate on the adapter. The
receptacle shell is isolated from DGND -- see the open item in section 11.

Charging and recording are mutually exclusive by the two independent mechanisms of RFQ S-01,
which are written out once in DESIGN_FACTS section 4 and are not restated here. The
consequence for the harness builder is the one that matters: **the helmet is never worn
while this cable is connected**, so WH-07 and WH-01 are never live at the same time.

The temperature half of that interlock is **not met**. RFQ E-23 asks for a charger with
thermal regulation and no charging above 45 C, and RFQ S-04 asks for a thermistor; there is
no NTC net in `design.py` and no thermistor way on J12 or J13, so no conductor in this
document carries a cell temperature and none can be added without a board change. It is an
open hardware item listed in DSN-EEG-003 section 11 and RISK-EEG-011.

### 3.8 WH-09 -- isolator host pigtail, USB-B to USB-C panel receptacle

This assembly replaces the withdrawn WH-08 and exists to resolve a connector mismatch, so
the mismatch is stated first.

**RFQ E-24 asks for a USB-C host connector. The only named candidate isolator module, the
Olimex USB-ISO class ADuM4160 board, presents a USB-B host receptacle. That is a live
non-conformance and it is not closed.** The interim resolution, which is what is built for
Phase 1, is this short pigtail: a moulded USB-B plug at the module, a panel-mount USB-C
receptacle at the POD-P1 aperture. If and when an isolator module with a USB-C host
receptacle is qualified, that module's own receptacle is presented directly through the
aperture, WH-09 is deleted, and E-24 is met by the module rather than by a pigtail. Until
then the kit meets E-24 at the panel and not at the module, which is a difference a safety
and EMC reviewer must see rather than have hidden by a cable.

Length 150 mm. Reference construction: a shielded USB 2.0 cable assembly, 28 AWG data pair,
24 AWG power pair, OD 4.0 to 4.5 mm, with the panel receptacle on adapter WH-ADP-04, which is
specified in section 3.9.

| Conductor | From | To | Note |
|---|---|---|---|
| VBUS | panel receptacle A4/A9/B4/B9 | module USB-B pin 1 | powers the host side of the isolator only; no path to the battery rail |
| D+ | panel receptacle A6/B6 | module USB-B pin 3 | |
| D- | panel receptacle A7/B7 | module USB-B pin 2 | |
| GND | panel receptacle A1/A12/B1/B12 | module USB-B pin 4 | host-side 0 V, not DGND |
| braid | panel receptacle shell | module USB-B shell | bonded at both ends of this cable and **to nothing else**; not bonded to DGND anywhere in the pod |

The panel receptacle carries two 5.1 kOhm CC pull-downs, so a Type-C host enumerates the pod
as a device and supplies 5 V. Every conductor in this assembly is on the **host** side of the
isolation barrier. Nothing in it may be commoned with DGND, with the WH-07 charge return, or
with any harness drain, because that is the one bond the ADuM4160 exists to prevent.

No carrier copper crosses the isolation barrier (RFQ E-24, S-03). The keep-out that
guarantees it is specified once, in DSN-EEG-003 section 3.3, and this document does not
restate its coordinates; what the harness builder must know is that it is a keep-out on
**all four layers**, not two, and that nothing in this assembly, including a cable tie, a
P-clip screw or a stray drain, may be routed across it.

**Retention and sealing.** The panel receptacle is fixed to the POD-P1 wall on adapter
WH-ADP-04 with a gasket behind its flange; the aperture is a gasketed panel aperture and
**not** a gland. The module-end USB-B plug is retained by a printed P-clip screwed to a
POD-P1 boss 40 mm behind the connector so the plug cannot back out inside a closed
enclosure. At service the whole pigtail is a replaceable item: undo the P-clip, undo the two
receptacle screws, fit a new one. That is the replaceable element the DSN-EEG-002 section 9
risk 9 mitigation depends on, and it replaces the gland insert of Rev A.

**The participant's cable is not part of this document.** RFQ A-07 ships two 1.0 m cables
with every kit, one USB-C to USB-A and one USB-C to USB-C, plus a 5 V 2 A EU charger. **One
of those two is the host lead** and plugs into the panel receptacle above; the other serves
the charge port at WH-07. Which of the two is which depends on the participant's computer,
which is exactly why two are shipped. Rev A of this document said both A-07 cables served
the charge port and that the host link was captive; that is corrected.

**The DevKit's own USB-C receptacles.** The two USB-C receptacles on the
ESP32-S3-DevKitC-1 sit on the patient-applied side of the barrier and are brought to no
panel aperture. They are reachable only with the lid off, through the 31 x 61 mm opening in
MP-01 over the DevKit, which is where end-of-line flashing is done: the DevKit's UART USB-C
port carries the auto-reset circuit and the carrier's J26 header is console and recovery
only, because GPIO0 is committed to LED_SR_LATCH. This is an assembly requirement in
ASM-EEG-007, repeated here because the harness builder is the last person who sees those
receptacles before the plate goes on.

### 3.9 The five panel adapters

Rev A named WH-ADP-01, -01B, -02, -03 and -04 in five wire lists and specified none of them,
so five of the eight assemblies terminated on a part number with nothing behind it. Each is
settled here: what it mates at each end, what it is made of, its own wire list, and what has
to be confirmed before it can be bought or printed. Two are bought parts and three are
printed, and the printed three are modelled in `tools/mech_gen.py` and released as STEP and
STL with the rest of the print set. **None of the five has been made or measured.**

| Adapter | Cable | POD-P1 opening, design (mm) | What it is |
|---|---|---|---|
| WH-ADP-01 | WH-03, boom microphone | 6.5 dia at 122.0, 90.0 | a bought jack; no printed part |
| WH-ADP-01B | WH-04, headphones | 6.5 dia at 128.0, 72.0 | the same bought jack |
| WH-ADP-02 | WH-05, room microphone | 4.0 dia at 122.0, 102.0 | a printed carrier and an unqualified module |
| WH-ADP-03 | WH-07, charge port | 10.0 x 4.0 at 143.0, 80.0 | a printed clamp plate and a bought receptacle |
| WH-ADP-04 | WH-09, host port | 10.0 x 4.0 at 146.0, 12.0 | a printed clamp plate and a bought receptacle |

Those are the openings `tools/mech_gen.py` cuts, and they are all on the **right-hand wall**
at 45 % of the enclosure height. **Four of the five overlap a button opening.** The three
response buttons are 13.0 mm openings on the same wall at the same height, at design y = 76,
90 and 104 mm, so BTN_B is concentric with the boom opening, BTN_STOP contains the
room-microphone port, BTN_A overlaps the headphone opening, and the charge opening runs into
both BTN_A and BTN_B. That is a fault in `pod_base()`, not in these adapters -- they are
dimensioned to the openings as they are specified -- and no adapter here can be fitted until
it is corrected. It is open item 20.

#### WH-ADP-01 and WH-ADP-01B -- the 3.5 mm panel jacks. Bought.

**What it mates.** Outside: the moulded 3.5 mm 4-conductor plug of WH-03B on WH-ADP-01, the
participant's headphone plug on WH-ADP-01B. Inside: the four flying leads of WH-03 or WH-04,
soldered to the jack's own lugs. Nothing else.

**What it is made from.** A 4-conductor 3.5 mm panel-mount jack with a threaded barrel,
M6 x 0.75, for a 6.5 mm panel hole and a panel up to 2.5 mm thick, with solder lugs -- the CUI
SJ-435xx and Lumberg KLBR classes are both of that form. It is fitted with its own nut and a
10 mm outside diameter, 0.8 mm silicone washer behind the flange. **There is no printed
part**: POD-P1's wall is 2.5 mm and the jack's own thread and nut hold it, so a bracket would
add a part without adding a function.

**Wire list.** Sections 3.3 and 3.4, one conductor to each of tip, ring 1, ring 2 and sleeve,
with the WH-03 drain cut back 10 mm at the jack and insulated. It is not repeated here.

**What has to be confirmed, and none of it is.** Which lug is which contact on the part
actually bought, because the tip / ring 1 / ring 2 / sleeve lug order is not common across the
class and getting it wrong puts DGND on VOICE_RAW; that the barrel is at least 4.5 mm long, so
that it passes a 2.5 mm wall and still takes its nut; that the part tolerates POD-P1's
**printed** 6.5 mm hole, which an MJF part holds to about +/-0.3 mm and which is not a
machined panel hole; and the plug retention, against the 30 N boom-detach limit of test H6.
On WH-ADP-01B there is one more: section 3.4 uses the fourth contact as the insertion detect
that J27.4 reserves, and **a switched detect contact is not a feature every jack in this class
carries**. If the part bought has none, J27.4 stays a no-connect, the detect of section 3.4 is
not implemented, and this document does not pretend otherwise.

#### WH-ADP-02 -- the room-microphone carrier. Printed, and it carries a module that does not exist.

**What it mates.** Outside: bonded to the inside of the POD-P1 wall over the 4.0 mm acoustic
port, with a silicone washer in the 10 mm recess on its wall face. Inside: the capsule and
switch module, on M2.5 standoffs, sealed to the plate by a second washer in the recess on the
module face. Cable: the four conductors of WH-05 and its drain, at the module.

**What it is made from.** `tools/mech_gen.py wh_adp02()`, MJF PA12, **32.0 x 24.0 x 3.4 mm,
1.96 cm3** *(model figures, read from the released mesh; the 3.0 mm of the first issue was the
plate thickness without the gasket-recess boss)*: a 4.0 mm acoustic port, a 10 mm gasket recess on each face, six
M2.5 clearance holes on an 8 mm grid and two 6.0 x 2.5 mm tie slots. The grid is deliberate,
and it is the answer MP-01 gives for the same reason: **no room-microphone module is
qualified** (section 3.5 and open item 5), so no hole pattern is known, and a plate drilled to
a guessed pattern is worse than a grid that a small breakout picks up two holes of and a tie
holds the rest of the way.

**Wire list.** Section 3.5 gives the four conductors at J28. On the adapter itself:

| Node | From | To |
|---|---|---|
| supply | WH-05 conductor 1, DVDD3V3 | capsule V+ and the analogue switch V+ |
| return | WH-05 conductor 2, DGND | capsule ground, switch ground, and the WH-05 drain |
| audio | capsule output | the switch's signal input |
| audio out | switch common | WH-05 conductor 3, ROOM_PRE |
| mute | WH-05 conductor 4, MIC_MUTE | the switch's control pin, with a 100 kOhm resistor holding it in the **muted** state |

That 100 kOhm sits on the adapter and not on the carrier, and it is there so the room
microphone is muted whenever GPIO21 is an input -- which it is at reset, before any firmware
runs, which is when a microphone in a participant's home is least supervised. **Which logic
level mutes is not fixed by this document**: it follows from which throw of the switch the
sub-assembly uses, and the sub-assembly has no drawing.

**What has to be confirmed.** Everything about the module. RFQ E-15 asks for a mute that is a
hardware gate in the signal path and no catalogue part is known to meet it. The candidate is a
Knowles SPU0414HR5H-SB class analogue MEMS capsule with a TI TS5A3159 analogue switch in the
output path; the fallback is that same pair as a programme-designed sub-assembly, which needs
a drawing, a part number and an AVL line and has none of the three. This carrier is
dimensioned so that either of them lands on the same plate, which is the most this document
can do while the part is open.

#### WH-ADP-03 and WH-ADP-04 -- the USB-C panel plates. Printed, plus a bought receptacle.

**What they mate.** Outside: one of the two A-07 cables the kit ships. Inside: WH-07's two
conductors on WH-ADP-03, WH-09's four conductors and its braid on WH-ADP-04.

**What they are made from.** `tools/mech_gen.py wh_adp_usb()`, MJF PA12. WH-ADP-03 is
**34.0 x 20.0 x 5.0 mm, 2.18 cm3**; WH-ADP-04 is **34.0 x 20.0 x 7.4 mm, 2.65 cm3** *(model
figures)*. A USB-C receptacle nose fills the 10.0 x 4.0 mm opening, so no part of the plate
can sit in it and the plate works from behind: a picture-frame rim lands on the inside of the
wall, the receptacle's mounting flange is trapped inside that rim, and a 14.0 x 8.0 mm window
passes the receptacle body and its wires. The rim takes **any** flange up to
24.0 x 14.0 x 1.6 mm rather than being cut to one receptacle, because no receptacle has been
bought and a pocket cut to a guessed flange is a plate that fits nothing.

WH-ADP-04 differs in two ways and both of them are the isolation barrier: its rim is 0.8 mm
deeper, for the flange gasket section 3.8 calls for, and a 2.0 mm skirt around the window adds
4.0 mm to the surface path from the receptacle's own terminals to anything bonded to the pod
wall. PA12 is not conductive and neither plate carries a metal insert, so nothing in either
of them can become the bond the ADuM4160 exists to prevent.

**The receptacle.** A panel-mount USB-C 2.0 receptacle with a two-hole flange and solder cups
or a short pigtail, carrying **two 5.1 kOhm CC pull-downs** so that a Type-C source or host
sees a device. The pull-downs are fitted on the adapter, at the receptacle's own CC cups,
under heat-shrink; they are not on the carrier and no carrier net reaches them.

**Wire list, WH-ADP-03**, the charge port. WH-07 is section 3.7.

| Receptacle | To | Note |
|---|---|---|
| A4, A9, B4, B9 commoned | WH-07 conductor 1, VBUS_IN, to J24.1 | |
| A1, A12, B1, B12 commoned | WH-07 conductor 2, DGND, to J24.2 | |
| CC1 (A5) | 5.1 kOhm to the commoned ground | on the adapter |
| CC2 (B5) | 5.1 kOhm to the commoned ground | on the adapter |
| D+, D-, SBU1, SBU2 | no connection | **no data conductor enters WH-07** |
| shell | no connection | isolated from DGND; that ruling is open item 8 |

**Wire list, WH-ADP-04**, the host port. WH-09 is section 3.8.

| Receptacle | To | Note |
|---|---|---|
| A4, A9, B4, B9 commoned | WH-09 VBUS, to the module's USB-B pin 1 | host side only; no path to the battery rail |
| A6, B6 | WH-09 D+, to USB-B pin 3 | |
| A7, B7 | WH-09 D-, to USB-B pin 2 | |
| A1, A12, B1, B12 commoned | WH-09 GND, to USB-B pin 4 | host-side 0 V, **not DGND** |
| CC1 (A5), CC2 (B5) | 5.1 kOhm each, to that host-side 0 V | **not to DGND** |
| shell | WH-09 braid, to the USB-B shell | bonded at both ends of WH-09 and to nothing else |

Every node in the WH-ADP-04 table is on the host side of the barrier, the two pull-downs and
the shell included, and test H10 is what measures that, at 500 V DC, with WH-09 unplugged.

**What has to be confirmed.** That the receptacle's nose stands at least 2.5 mm proud of its
flange -- 3.3 mm on WH-ADP-04, which has a gasket in front of the flange -- so that it reaches
through the wall; that the flange is inside 24.0 x 14.0 x 1.6 mm; and that its CC cups are
reachable for the pull-downs once it is in the rim.

**And how the plates are held on.** All three are bonded to the inside of the wall, because
`pod_base()` carries no boss for WH-ADP-02, WH-ADP-03 or WH-ADP-04. Both USB plates carry two
M2.5 clearance holes for the screws that would replace the bond, and there is nothing in
POD-P1 for those screws to go into. Test H6 pulls the panel receptacle at 50 N: that is then a
pull on a bonded joint which has not been made and has not been tested. The section 3.8
P-clip has the same gap -- it is specified as screwed to "a POD-P1 boss 40 mm behind the
connector" and WH-09 has no such boss. Open item 21.

---

## 4. Materials

| Property | WH-01 | WH-02 | WH-03, WH-04, WH-05 | WH-03B | WH-07 |
|---|---|---|---|---|---|
| Conductors | 11 signal + drain | 10 | 4 | **2 signal + drain** | 2 |
| Conductor | 7/0.1 mm tinned copper | 7/0.1 mm tinned copper | 7/0.1 mm tinned copper | **7/0.1 mm tinned copper** | 7/0.2 mm tinned copper |
| Nominal CSA (calculated) | 0.055 mm2 | 0.055 mm2 | 0.055 mm2 | **0.055 mm2** | 0.22 mm2 |
| DC resistance (calculated, 0.0172 Ohm.mm2/m) | 0.313 Ohm/m | 0.313 Ohm/m | 0.313 Ohm/m | **0.313 Ohm/m** | 0.079 Ohm/m |
| Primary insulation | PTFE, 0.15 mm wall, OD 0.70 mm | PVC, 0.18 mm wall, OD 0.75 mm | PTFE, OD 0.70 mm | **PTFE, 0.15 mm wall, OD 0.70 mm** | PVC, OD 1.15 mm |
| Colours | section 3.1 | section 3.2 | sections 3.3 to 3.5 | **RD capsule +, BK capsule -** | section 3.7 |
| Screen | overall Al/PET foil, 100 % coverage, + 30 AWG tinned drain | none | overall Al/PET foil + 30 AWG drain | **overall Al/PET foil, 100 % coverage, + 30 AWG tinned drain** | none |
| Jacket | TPU, 0.55 mm wall, OD 4.3 mm nom / 4.6 mm max | TPU, 0.50 mm wall, OD 4.5 mm nom | TPU, OD 2.2 mm max | **TPU, OD 2.2 mm max** | PVC, OD 3.0 mm |
| Min bend radius | 26 mm dynamic, 13 mm static (6x / 3x OD) | 27 mm / 14 mm | 14 mm / 7 mm | **14 mm / 7 mm** | 18 mm / 9 mm |
| Single conductor min bend radius | 5 mm | 5 mm | 5 mm | **5 mm** | 8 mm |
| Temperature | -20 to +200 C (PTFE) | -20 to +80 C | -20 to +200 C | **-20 to +200 C (PTFE)** | -20 to +80 C |
| Chemical | resists 70 % IPA and conductive EEG paste | as WH-01 | as WH-01 | **as WH-01, and repeated 40 kHz ultrasonic immersion** | as WH-01 |
| Flex life target | 50 000 cycles at the crown transition | 50 000 cycles | not flexed in use | **a duty, not a cycle count -- see below** | not flexed in use |
| Cut length | section 3.1 | section 3.2 | 220 / 190 / 180 mm | **1700 mm, +10 / -0** | 150 mm |

WH-09 is a bought-in shielded USB 2.0 assembly and is specified by its USB conformance, not
by the table above. **WH-10 is a bought-in lead of the same class as the three WH-06 EMG leads
and is specified in section 3.1.3, not here.**

**Insulation of the three free tails, new on 2026-09-02.** Conductors 9, 10 and 11 leave the
jacket and the screen at the helmet end and run free -- 250 mm at each temple and F mm at the
halo front. Over that whole free length each carries a **secondary sleeve over its PTFE
primary**: extruded PTFE or FEP, or 3:1 heat-shrink supplied at 1.5 mm or more and **recovered
to 0.70 mm or less** so that it grips the conductor rather than tenting over it, resistant to
70 % IPA and to the 40 kHz ultrasonic bath the clips go into. It is a materials requirement and
it is written here for that reason. *A printed marker sleeve is not insulation and must not be
cited as this part: the Brady PS-187-2-WT class of section 10 recovers to 1.6 mm, more than
twice the 0.70 mm OD of the conductor it would have to insulate.* AVL-EEG-017 K34 buys it.

**WH-03B, and why it now has a column.** Rev B registered the boom lead in section 1, gave its
four connections in section 3.3, and left it out of this table. The one cable in the kit that a
participant bends by hand at the start of every session therefore had no conductor
construction, no gauge, no insulation, no colour code, no screen, no jacket, no OD, no bend
radius and no temperature or chemical rating -- and a harness shop could neither cut it, buy
it, nor lay it up. It is specified above as the two-conductor member of the WH-03 / WH-04 /
WH-05 family rather than as a new construction, because electrically it **is** the continuation
of WH-03: the same 7/0.1 mm conductor, the same PTFE primary, the same foil-and-drain screen
and the same TPU jacket, so it adds no new raw material to the kit and no new qualification.
Three things follow from where it goes, and they are stated rather than assumed.

* **Its screen is terminated at both ends**, which no other screened cable in this document
  does. Section 3.3 lands the screen on ring 2 and the sleeve of the 3.5 mm plug, and the
  capsule end bonds it to the capsule can. That is deliberate and it is not a breach of the
  single-point rule of section 5.1: both ends of this cable are at DGND through the jack
  anyway, the lead is outside the frame and outside the pod for its whole length, and it is
  **not part of the helmet screen system** and never reaches R91.
* **It is immersed.** SVC-EEG-013 section 3 R5 puts the boom in the 40 kHz ultrasonic bath at
  every turnaround. The PTFE primary and the TPU jacket are chosen for that; **a PVC jacket is
  not acceptable on this assembly and no deviation may substitute one.**
* **Its plug is assembled, not moulded.** Section 3.3 called for "a moulded 3.5 mm
  4-conductor plug". An over-moulded plug cannot be fitted in a harness shop and cannot be
  replaced at service, and this is a lead that test H6 pulls to 30 N at the participant-facing
  detach point. The word is corrected here: the plug is a **4-pole 3.5 mm plug with solder
  buckets and a screwed or crimped strain-relief barrel**, so the assembly can be built, pull
  tested, and repaired. AVL-EEG-017 K41 carries it.

**Its flex duty is a duty, not a cycle count.** WH-01 and WH-02 carry a 50 000-cycle target at
the crown transition. No equivalent number is stated for WH-03B, because nothing in the package
says how many times a boom is set in a unit's life, and a cycle count invented to fill the cell
would be worse than the empty cell it replaced. What is stated instead is the duty: the lead is
worked at the gooseneck root every time the boom is positioned, and it must survive the
gooseneck's full articulation with no continuity change. **Test H7 is run at the gooseneck root
rather than at the crown for the WH-03B first article.** The number belongs to that first
article -- open item 25.

**On the gauge designation.** 7/0.1 mm has a calculated cross-section of 0.055 mm2, which is
30 AWG by area and is catalogued as "28 AWG equivalent" by several European cable houses
because its overall diameter matches 28 AWG. Where a supplier's 28 AWG is 7/0.127 mm
(0.0887 mm2, 0.194 Ohm/m) that construction is the preferred alternate and needs no
deviation: it is lower resistance and the same OD class. No other substitution is permitted
without a written deviation, because the OD drives the channel fill in section 7.

**Why the resistance does not matter, and where it does.** The longest WH-01 run is REF_L at
2140 mm: 0.67 Ohm calculated, against a 47 kOhm series resistor and a 5 to 20 kOhm contact
impedance. It contributes 14 parts per million of the source impedance and is not a signal
consideration; the 1.0 Ohm continuity limit in section 9 exists to catch a bad crimp, not to
protect the measurement. On WH-02 the LED current of 1.3 mA drops 0.9 mV in the longest run
and cannot shift a colour boundary.

**Why WH-01 is screened and WH-02 is not.** The eleven electrode conductors are
high-impedance nodes referenced to AGND_REF, the analogue mid-rail, carrying microvolts in a
0.5 to 70 Hz band against the input-referred noise budget of RFQ E-03. The arithmetic of
that budget -- the Johnson noise of the series resistors, the converter contribution and the
flatness at 100 Hz -- is worked once, in RISK-EEG-011 section 4, and is not recomputed here;
what it leaves is very little room for pickup. These conductors run beside a person for two
hours in a domestic room full of mains field. They are screened. The eight light conductors
are driven from a 74HC595 through 1 kOhm into a 2 V LED: source impedance under 1.1 kOhm, no
high-impedance node anywhere, and the lights are forced dark for the whole of every recording
block.

**Corrected 2026-09-02: that last clause used to read "so the cable carries no switching
current at any moment when an electrode channel is live", and it is not true.** RFQ-EEG-001
E-27 drives the contact lights *from the converter's own lead-off measurement*, so a lit
light means a live measurement on the same electrode by definition. What the recording
interlock gives is narrower and still worth having: no switching current during a **recording
block**. The concurrent case is electrode preparation -- the participant gelling a site and
watching its light change -- and that is not an edge case, it is the state the lights exist
for. It is also the case in which the LED and the electrode conductor are closest together,
because at the site they share the HM-04 body and the frame's 6 mm channel separation does
not apply there; the 47 kOhm series resistors are on the carrier, so the electrode conductor
runs at full electrode impedance the whole way from the cup to J14.

The controls below are real and are unchanged. What was missing was a limit and a
measurement: nothing in the package stated how much noise the lights were allowed to add,
and no test measured it -- TST-EEG-004 T9a measures channel-to-channel crosstalk on the
carrier through a fixture, with no harness and no lights. **RFQ-EEG-001 E-30 now states the
limit and TST-EEG-004 T9c measures it, through the fitted harness in an assembled helmet.**
Until T9c has been run on a built unit, the decision to leave WH-02 unscreened rests on the
argument in this section and not on evidence. A screen would earn nothing and would cost a second drain, for which there is exactly
one shield pin on the whole carrier. The separation that matters for WH-02 was made
physically by ECO-EEG-014, which moved it to J30 in the digital zone across the x = 62 mm
split, and by the two-channel routing of section 7.

---

## 5. Screen and drain

### 5.1 The single-point rule

The star-point rule itself is stated once, in DSN-EEG-003 section 3.3, and this document
cites it rather than restating it. Its consequences for the harness are these, and they are
what the builder is signing for:

`HARN_SHIELD` reaches DGND at **R91 only**, a 0 Ohm 0603 at design coordinate (56.0, 62.0),
fab (56.0, 68.0). AGND_REF reaches DGND at **R90 only**, at design (56.0, 58.0), fab
(56.0, 72.0). Fit exactly one of each. Never bridge either with a wire link or a solder blob,
and never fit a second drain anywhere in the kit that reaches DGND by another route. Two star
points in parallel is a ground loop around the whole helmet, and its signature -- 50 Hz
pickup that appears on every channel at once -- will be blamed on the electrodes. On the
four-layer carrier there are now two reference planes on each side of the split rather than
one, and R90 and R91 remain the only ties between the AGND_REF planes and the DGND planes;
the stitching vias tie L2 to L3 within one reference, never across the split.

### 5.2 WH-01 construction

* **Screen:** aluminium/polyester foil, 100 % coverage, applied over the eleven conductors
  with a 25 % overlap, foil side inward against the drain.
* **Drain:** one 30 AWG tinned-copper conductor laid in continuous contact with the foil, in
  the interstice, running the full length.
* **Pod end:** foil and drain terminated together. The drain is sleeved in clear 2:1
  heat-shrink from the jacket cut to within 6 mm of the crimp, crimped into a single contact,
  and inserted in position 12 of the WH-01 housing. One drain, one pin. There is no splice.
* **Helmet end:** foil and drain cut back 10 mm inside the jacket, folded back on themselves
  and covered with 15 mm of 2:1 adhesive-lined heat-shrink. **The screen is not connected to
  the cup, to the spring, to the HM-04 body, to any LED, to WH-BUS-01 or to the frame.** This
  is a "do not connect" instruction, and section 9 test H3 exists to prove it was followed.
* Inside the frame each conductor continues unscreened. That is a deliberate ruling: the
  frame is a closed PA12 monocoque with no conductive part, the in-frame runs are 130 to 315
  mm, and an individually screened run cannot be drawn through a 3.8 mm channel and replaced
  through a cover strip, which is the service story DSN-EEG-002 section 4.1 depends on. The
  residual risk is mains pickup on the unscreened section and it is verified, not assumed, at
  the input-referred noise step of TST-EEG-004 (inputs shorted, 60 s at 1 kHz, 1.0 uV RMS
  maximum in 0.5 to 70 Hz).

### 5.3 WH-03, WH-04, WH-05

Each carries its own overall foil and 30 AWG drain, terminated at the **carrier end only**: the
WH-03 and WH-05 drains on the **DGND pin** of their connectors (J18.2, J28.2), and the WH-04 drain
on **J27.3 = HP_GND**, the headphone return, which is referenced to DGND inside the codec module
and, since the routing closed on 2 September 2026, **reaches DGND through the carrier copper**;
`kicad/EEG-CAR-01_RevB_DRC_report.txt` records all 145 nets fully connected with none
unclosed and none without copper, HP_GND (J8.13 to J27.3) among them, so the WH-04 drain no
longer floats and this harness needs no change. At the far end the drain
is cut back 10 mm and insulated. The WH-03 and WH-05 drains reach DGND directly and do not pass
through R91; all three are entirely inside the pod, in the digital zone, and are not part of the
helmet screen system. The WH-09 braid is not part of either system and is bonded only within
WH-09 itself, per section 3.8.

### 5.4 WH-02

No screen, no drain. LED_GND is the guard conductor and is described in section 3.2. The
justification for carrying no screen is in section 4, together with the correction of
2026-09-02 to the sentence that used to justify it, the E-30 limit that now bounds it and
the T9c measurement that will decide it.

### 5.5 Leakage

RFQ S-02 allows a maximum of 10 uA DC and 100 uA AC through any electrode in normal
condition and 50 uA DC in single fault. In normal condition the screen path contributes
nothing: it is tied to DGND, the electrode conductors are separated from it by PTFE tested
to at least 100 MOhm at 500 V DC, and the working voltage across that insulation never
exceeds the +/-2.5 V analogue rails. The calculated worst-case leakage through the insulation
at 2.5 V across 100 MOhm is 25 nA per conductor, three orders of magnitude below the
normal-condition limit.

**The single-fault limit of S-02 is not met, and this document does not claim it is.** With
one conductor shorted to the drain the 47 kOhm series resistor is still in circuit and the
fault current is bounded by the rails at 2.5 V / 47 kOhm = **53.2 uA against the 50 uA limit
of S-02**. The fix is ECO-EEG-024, which raises R1 to R16 from 47 kOhm to 68 kOhm and gives
2.5 V / 68 kOhm = 36.8 uA; that keeps the input corner at 234 Hz, which is -0.75 dB at
100 Hz and therefore requires RFQ E-10 to widen to +/-1.0 dB, and raises the resistor noise
to 0.28 uV for a total of 0.31 uV, still well inside E-03. **The Phase 1 prototypes are
built with 47 kOhm fitted**, the measurement is made on them, and the change is made before
Phase 2. Until then S-02 single fault is a stated non-conformance carried for the safety
reviewer, not a compliance. The primary means of compliance remain R1 to R16 and the
ADuM4160 isolator, per E-07 and E-24.

---

## 6. Connectors, contacts and tooling

J14 and J30 are 2.54 mm **socket** strips on the carrier (Samtec SSW-112-01-G-S and
SSW-110-01-G-S or equivalent), 1.00 mm finished plated holes. The harness therefore
terminates in male crimp contacts. Pin 1 of every socket strip is the square pad and is
marked on the top silkscreen.

| Item | Board side | Harness side | Contact | Tool | Notes |
|---|---|---|---|---|---|
| WH-01 to J14 | 1x12 socket strip, 2.54 mm | Harwin M20 12-way male crimp housing, polarised | Harwin M20-118 male crimp, gold flash, 24-30 AWG | Harwin Z20-320 hand tool; Z20-431 extraction | confirm the current Harwin ordering suffix at IQC and record it in AVL-EEG-017 |
| WH-02 to J30 | 1x10 socket strip | Harwin M20 10-way male crimp housing | as above | as above | |
| WH-03 to J18 | 1x4 socket strip | Harwin M20 4-way male crimp housing | as above | as above | |
| WH-04 to J27 | 1x4 socket strip | as above | as above | as above | |
| WH-05 to J28 | 1x4 socket strip | as above | as above | as above | |
| WH-06 to J15-J17 | touch-proof 1.5 mm socket, **no confirmed part** (section 3.6) | Staubli SLS425-SEK/N touch-proof plug | moulded, bought-in | none | 1.70 mm plated hole, 1.50 mm NPTH retention posts |
| WH-07 to J24 | JST B2B-PH-K-S(LF)(SN) | JST PHR-2 housing | JST SPH-002T-P0.5S | JST WC-160 / YC-160R | 2.00 mm pitch, 0.90 mm plated holes |
| WH-09 | none -- module USB-B receptacle to panel | moulded USB-B plug; panel USB-C receptacle on WH-ADP-04 | -- | -- | plug retained by printed P-clip; receptacle gasketed to the panel |

The **helmet-end and boom-end** terminations, which Rev B named and did not specify:

| Item | Fixed side | Removable side | Contact | Tool | Notes |
|---|---|---|---|---|---|
| WH-01 conductors 1-8, at the eight sites | **HM-04A** termination contact, anchored in the HM-04 body, conductor soldered to its tail 8 mm outside the body | **HM-05C** contact crown on the HM-05B spigot; parts with the bayonet | axial, gold on gold, 0.5 N minimum | soldering iron; HM-09 service key | **PROPOSAL, section 3.1.1.** No part, no vendor and no geometry today. AVL-EEG-017 K25 and K26 |
| WH-01 conductors 9 and 10, at the ears | free-hanging 1.5 mm touch-proof socket to **DIN 42802-1**, GY and PK bodies, on the 250 mm temple tail | the K2 ear clip's own DIN 42802 touch-proof plug, colour matched or sleeved within 25 mm of the plug | crimp or solder bucket for 28 AWG; **separation force 5 to 15 N**, mating force stated, 500 cycles minimum | per the coupler maker | **RULED 2026-09-02, section 3.1.2.1; not signed.** AVL-EEG-017 K27, ordered on the same purchase order as K2 |
| WH-01 conductor 11, at Fpz | free-hanging 1.5 mm touch-proof socket to **DIN 42802-1**, TQ body, at the HM-01 halo-front mouth on a stated free tail F | **WH-10**: 150 mm +/- 10 mm snap-to-DIN-plug lead, TQ, onto a K4 disposable pad | crimp or solder bucket for 28 AWG; retention **13 N maximum** until HM-01 gains an anchorage, not H6's 15 N | per the coupler maker | **RULED 2026-09-02, section 3.1.3; not signed.** AVL-EEG-017 K27 third unit and K47. *Was: "bias pad, solder tag" -- no part and no drawn feature* |
| WH-02, both leads at each of the eight site LEDs | two-lead bicolour LED, ASM-EEG-007 section 4.3 | -- | soldered and sleeved | soldering iron | the LED has no seat and no lead passage in HM-04 -- section 3.1.1 |
| WH-03B, at the capsule and at the panel | electret capsule solder tags | 4-pole 3.5 mm plug, solder buckets, screwed or crimped barrel | -- | soldering iron | **not over-moulded** -- section 4. AVL-EEG-017 K41 |

**One connector system, and which one it is.** Every crimped 2.54 mm connector in this kit --
the five harness housings above and the seventeen module jumpers of ICD-EEG-006 section 3 --
is the **Harwin M20 crimp system**. That has to be said in one place because until this issue
the package said it in three, incompatibly: this section's M20 rows, AVL-EEG-017 section 1.6's
"Harwin M20-106 series or 3M 89 series", and ICD-EEG-006 section 3.1's "a Molex KK 254 crimp
build: female housings 22-01-30nn with 08-50-0114 terminals at the module end, free-hanging
male housings with 08-52-0072 terminals at the carrier end". The choice is settled by geometry
and not by preference: `tools/mech_gen.py` cuts the WH-KEY-01 cavity at
`KEY_CAV_W = M20_HSG_W + 0.30 = 4.50 mm` and asserts both that the housing enters with 0.30 mm
of clearance and that a reversed housing is stopped by
`M20_HSG_W + M20_KEY_MIN - KEY_CAV_W = 0.40 mm` of interference. **A housing outside
4.20 +0.10 / -0.20 mm across the flats either will not enter the shroud or will not be keyed by
it**, so adopting a different family would have made every printed shroud in the kit the wrong
size, silently, and the only mitigation against the one safety-relevant mis-mate in the kit
would have been a dust cover. **ICD-EEG-006 section 3.1 is corrected to the M20 system at this
issue, and AVL-EEG-017 section 1.6.1 now carries the per-way-count housing and contact table
that both documents used to point at and neither contained.** The 4.20 mm itself is still
UNCONFIRMED and is measured at IQC before a shroud is printed -- open item 11.

**Polarisation and mis-mating.** ECO-EEG-014 removed some of the risk by construction: J14 is
12-way and J30 is 10-way, so WH-01's housing cannot enter J30. It removed less than Rev A
claimed, because a 10-way housing does fit a 12-way socket and WH-02 can therefore reach J14.
What is left is that, offset and reversal on a bare socket strip, and the mating housings
alone prevent none of it. The anti-reversal feature is the printed shroud **WH-KEY-01**, part
of the MP-01 print set, which surrounds J14 and J30 and takes the housing's polarising rib in
one orientation only; it is dimensioned in section 6.1, which also states the one of these
four mis-mates it does not stop. A third form of WH-KEY-01 exists for J22; it is fitted only
when the Phase 2 EOG panel
option is taken, since no cable in this register lands on J22 (section 2). This is the same
keying decision ICD-EEG-006 section 6 records for the module jumpers:
a shrouded polarised header at the module end where the module has one, and the printed
carrier-end shroud over every socket that takes a jumper. The shroud names SHR-14-A,
SHR-30-A and SHR-22-A of JIG-EEG-009 Rev A are withdrawn: JIG-EEG-009 Rev B section 1.10 calls
all three WH-KEY-01, and PARTS-EEG-019 records the old names as legacy. The consequences if the
shroud is omitted:

| Mis-mate | Result |
|---|---|
| WH-01 offset +1 | E_Fz onto the Cz channel, every site reported one place out, HARN_SHIELD floating and the screen open |
| WH-01 offset -1 | BIAS_EL onto REF_R; the driven common-mode return lands on the reference node |
| WH-01 reversed | E_Fz onto HARN_SHIELD, BIAS_EL onto E_Cz; a driven output onto a protected scalp input |
| WH-02 reversed | LED_GND onto LED1 and LED_V onto LED2; lights wrong, no safety consequence |

Only WH-01 has a safety-relevant mis-mate, and in every case the 47 kOhm series resistors and
the +/-2.5 V rails still bound the current -- to the 53.2 uA of section 5.5, which is over
the single-fault limit. That is a mitigation with a stated shortfall, not a licence:
WH-KEY-01 is mandatory.

**Insertion force.** Supplier data for 2.54 mm gold-flash contacts is 0.6 N typical and 1.5 N
maximum per contact. Calculated totals: 12-way 7.2 N typical, 18 N maximum; 10-way 6.0 N /
15 N; 4-way 2.4 N / 6.0 N. Withdrawal force after 25 mating cycles must remain at or above
0.15 N per contact. Nothing here has been measured.

**Strain relief and service loop.** Each helmet cable is clipped to a POD-P1 boss with a
printed P-clip 40 mm behind its housing, so that any pull is taken by the enclosure and not
by the crimps. Behind the clip, **120 mm of service loop** is coiled at 30 mm diameter and
tied with a hook-and-loop strap, not a cable tie -- it must be undone by hand at service. The
loop exists so that a replacement conductor can be drawn through a channel and terminated
without dismantling the far end, which is the requirement in DSN-EEG-002 section 6 and the
mitigation in section 4.1. A further **40 mm service loop** is coiled at each HM-04 assembly
for the same reason at the other end. **Conductor 11 carries no site service loop from
2026-09-02**: its site is a coupler on a free tail and there is nothing to coil it at, which
is why its cut length is 1940 + F and not 1980 mm (section 3.1.3). Conductors 9 and 10 keep
theirs -- the 40 mm is inside their 2140 mm and is coiled at the temple before the tail runs
free. The enlarged POD-P1 internal volume of 158.0 x 138.0 x
55.5 mm is what these loops are coiled into, and the carrier now stands on M3 x 18 mm nylon
standoffs above the floor, so the loops sit under the plate and not against the carrier edge.

### 6.1 WH-KEY-01, dimensioned

Rev A named the shroud, made it mandatory, and drew nothing. It is now modelled, in
`tools/mech_gen.py wh_key01()`, in the three forms JIG-EEG-009 Rev B section 1.10 asks for,
and it is released as STEP and STL with the rest of the MP-01 print set. MJF PA12.
Coordinates are the design convention of section 1. **Every figure here is from the model;
nothing has been printed and no housing has been in a shroud.**

| Form | Socket | Ways | Outside (mm) | Volume | Keyway side | Footprint on the carrier |
|---|---|---|---|---|---|---|
| WH-KEY-01/J14 | J14 | 12 | 8.30 x 33.68 x 12.50 | 1.57 cm3 | +X | x 1.15 to 9.45, y 9.33 to 42.61 |
| WH-KEY-01/J30 | J30 | 10 | 8.30 x 28.60 x 12.50 | 1.36 cm3 | -X | x 61.55 to 69.85, y 87.33 to 115.53 |
| WH-KEY-01/J22 | J22 | 3 | 8.30 x 10.82 x 12.50 | 0.57 cm3 | +X, which is board +Y at J22 | x 22.25 to 32.67, y 112.15 to 120.45 |

It is a rectangular tube, open top and bottom, that drops over a socket strip already
soldered to the carrier and stands 4.00 mm proud of it. Walls are 1.20 mm, and 2.20 mm on the
wall that carries the keyway. Everything that could be derived was: the cavity is 4.50 mm wide
by N x 2.54 + 0.40 mm long because `fplib.pinsocket_1xn` makes the socket body 2.54 mm wide on
a 2.54 mm pitch, and the 12.50 mm overall height is the **8.50 mm of socket mating height that
ICD-EEG-006 section 4 budgets** plus 4.00 mm of lead-in, so that the shroud has hold of the
housing before the male contacts reach the socket. One pair of internal ribs on the J22 form
and two on the others close to 2.50 mm on the socket's 2.54 mm body, below the mating face
where they can never touch the housing, and locate the shroud; a bead of adhesive at the rim
holds it. MJF holds about +/-0.30 mm on a feature this size, so the ribs
are a location and the adhesive is the retention, and neither has been tested.

**Which side the keyway is on is a board-clearance decision, not a preference,** and it is
recorded per form because the housing has to match it. At J14 the fiducial FID1 sits at
x = 10.0 mm and the board edge at x = 0, so the keyway goes on +X. At J30, R70's pad starts at
x = 70.53 mm, so it goes on -X. Calculated clearances, from `design.py` and the model, to the
KiCad footprint envelopes in `tools/fplib.py`, which include the courtyard: the J14 form is
0.55 mm from FID1's and 1.33 mm from MH1's; the J30 form is 0.68 mm from R70's, which is
0.91 mm to R70's copper, and reaches y = 87.33, which is **0.44 mm from J9's socket body**. J9
is one of the seventeen module sockets ICD-EEG-006 section 6.1 also puts a WH-KEY-01 on, and
0.44 mm will not hold a second end wall, so either the 1x4 module form is open-ended on that
side or J9 moves. The module forms are not modelled here and that is open item 19.

**What it blocks, and what it does not.**

| Mis-mate | Blocked | By what |
|---|---|---|
| WH-01 reversed end for end | yes | the keyway is a 2.60 x 1.00 mm slot in one long wall, over way 1 only. The right way round, the housing's polarising rib slides down it; turned end for end the rib meets a flat wall and the housing then needs 4.90 mm of a 4.50 mm cavity |
| WH-01 or WH-02 offset by one way | yes | the cavity is the housing length plus 0.40 mm and is closed at both ends. A pitch is 2.54 mm |
| WH-01's 12-way housing into J30 | yes | 30.5 mm of housing into a 25.8 mm cavity |
| WH-02's 10-way housing into J14 | **no** | 25.4 mm of housing enters a 30.9 mm cavity, either way round. Way count does not stop it either: a 10-way housing fits a 12-way socket, so this section's claim that the two helmet cables "physically cannot be swapped" holds in one direction only. What catches this one is the pin-by-pin read-back at step 8 and test H9, not this part |

**The two dimensions this part does not have.** The shroud is cut for a Harwin M20 male crimp
housing **4.20 mm wide across the flats** whose **male contacts stand 4.00 mm proud of the
mating face**, and neither figure is in this package and neither has been measured. They are
`M20_HSG_W` and `M20_PIN_PROUD` in `mech_gen.py` and the part regenerates from them. A cavity
0.30 mm narrower than the housing will not take the cable at all, and one 0.50 mm wider stops
keying it, so **the housing is measured and the shroud reprinted before a build**, and the IQC
step this section already requires for the Harwin ordering suffix records the housing envelope
with it.

**And one dimension it imposes.** The shroud keys nothing unless the housing carries a
**polarising rib at least 0.70 mm proud of its body, within the first way from the way-1
end**. Section 6 specifies a polarised housing; where that housing's rib actually is has not
been confirmed. If the part bought has no rib, or carries it elsewhere, WH-KEY-01 is a dust
cover, the reversed WH-01 of the table above is stopped only by the read-back at step 8 --
which is exactly where Rev A stood -- and that is why it is written here rather than in a
drawing note.

**The shroud clears MP-01. The cable does not.** At 12.50 mm the shroud leaves 5.50 mm of the
18.00 mm carrier-to-plate gap of ICD-EEG-006 section 4. The mated cable does not fit what is
left:
8.50 mm of that gap is the socket, which leaves 9.50 mm for the housing and for the cable to
turn, and **WH-01's jacket is 4.30 mm OD with a 13 mm static bend radius**, so a 90-degree
turn out of J14 needs 15.15 mm of height before the housing itself is counted. **MP-01 has no
relief over either socket**: J14 runs x = 3.73 to 6.27 mm and the nearest slot edge in the
plate is at x = 8.0 mm, so nothing over it is open at all, and over J30 there are four
12 x 3 mm jumper slots which give 3 mm of opening every 7 mm and no continuous exit. With the
plate fitted the helmet cables cannot leave their sockets. MP-01 needs a relief over both; it
is not cut in this revision and it is open item 18.

---

## 7. Routing inside the helmet

HM-01 is a monocoque with wiring channels subtracted at 1.9 mm radius, giving a 3.80 mm bore
and 11.34 mm2 of channel area. Each section carries **two** parallel channels: **channel A**
on the outer wall for WH-01, and **channel B** on the skull-facing inner wall for WH-02,
separated by the section's central web, minimum 6 mm centre to centre. That separation is
the physical form of the ECO-EEG-014 rule that the light group stays away from the electrode
group. Both channels are closed by snap-in cover strips on the skull-facing side, so
conductors are laid in, not pulled; the fill limit is therefore set at **50 %**, and only a
single replacement conductor is ever drawn through.

Two occipital entries, not one: **OE-1** for WH-01 (left of the midline) and **OE-2** for
WH-02 (right of it). WH-BUS-01 sits at node **N1** immediately inside OE-2 under its own
cover strip.

| Segment | Channel | Conductors carried | Area (mm2) | Fill |
|---|---|---|---|---|
| OE-1 to N1, trunk | A | all 11 WH-01 signal conductors | 4.24 | 37 % |
| OE-2 to N1, trunk | B | all 10 WH-02 conductors | 4.42 | 39 % |
| N1 to crown NC, rear sagittal arch | A | Fz, Cz, Pz, C3, C4 | 1.93 | 17 % |
| N1 to crown NC, rear sagittal arch | B | LED1-5 + 5 LED_V tails | 4.42 | 39 % |
| NC to Fz, forward sagittal arch | A / B | E_Fz / LED1 + tail | 0.39 / 0.88 | 3 % / 8 % |
| NC to C3, coronal left | A / B | E_C3 / LED4 + tail | 0.39 / 0.88 | 3 % / 8 % |
| NC to C4, coronal right | A / B | E_C4 / LED5 + tail | 0.39 / 0.88 | 3 % / 8 % |
| N1 round the left halo | A | T7, F7, REF_L, BIAS_EL | 1.54 | 14 % |
| N1 round the left halo | B | LED6, LED8 + 2 tails | 1.77 | 16 % |
| N1 round the right halo | A | T8, REF_R | 0.77 | 7 % |
| N1 round the right halo | B | LED7 + tail | 0.88 | 8 % |

Sites and where each conductor leaves its channel, per DSN-EEG-002 section 2:

| 10-20 site | Carried on | Assembly | WH-01 pin | WH-02 pin |
|---|---|---|---|---|
| Fz | sagittal arch, forward of the crown | HM-04 #1 | J14.1 | J30.1 |
| Cz | crown junction of both arches | HM-04 #2 | J14.2 | J30.2 |
| Pz | sagittal arch, aft of the crown | HM-04 #3 | J14.3 | J30.3 |
| C3 | coronal arch, left | HM-04 #4 | J14.4 | J30.4 |
| C4 | coronal arch, right | HM-04 #5 | J14.5 | J30.5 |
| T7 | halo stub above the left ear | HM-04 #6 | J14.6 | J30.6 |
| T8 | halo stub above the right ear | HM-04 #7 | J14.7 | J30.7 |
| F7 | halo stub, left front | HM-04 #8 | J14.8 | J30.8 |
| Left ear | left temple exit, free lead | ear clip | J14.9 | -- |
| Right ear | right temple exit, free lead | ear clip | J14.10 | -- |
| Fpz | halo front, free lead to a coupler | disposable K4 pad on WH-10 | J14.11 | -- |

**Three wire exits the released frame does not have.** Conductors 9, 10 and 11 leave the
channels at the two temples and at the halo front, and none of those is a channel mouth.
`tools/mech_gen.py` defines exactly three mouths and all three are occipital: `HM01_N1_MOUTH`
at (0.00, -95.38) in the shell roof and `HM01_HALO_MOUTH` at (+/-45.41, -82.41, -11.25).
`CH_BORE` is a constant 3.80 mm, so there is no stepped mouth anywhere for a strain relief to
react against either. HM-01 is carried over as an STL with no STEP and no parametric source
(PARTS-EEG-019 OA-1), so these are three features that have to be added to a model nobody can
regenerate. Sections 3.1.2.1 provision 4 and 3.1.3 state the consequence: no pull test is
written against an anchorage that does not exist. Open items 26 and 29.

**Where the boom detaches.** In Phase 1 the boom does not route through the frame. The boom
assembly clamps to the left temple mount and its own 1700 mm lead (WH-03B) runs outside the
frame to the 3.5 mm jack on the POD-P1 panel; the participant-facing detach point is that
plug. In Phase 2 the boom lead enters the left temple channel and the detach point becomes a
temple-mounted jack. Either way the boom, the eight cups and the two ear clips are the parts
that go into the ultrasonic bath at refurbishment; the frame is wiped and never immersed.

**Cover strips.** Every channel is closed by a snap-in strip on the skull-facing side,
released with a plastic pick. The strips over N1 (WH-BUS-01), over the crown node NC and over
each HM-04 base are separately removable so that a single conductor can be replaced without
opening a whole arch.

---

## 8. Assembly sequence

Workmanship to **IPC/WHMA-A-620 class 2** for the cable assemblies, with **IPC-A-610 class 2**
governing the carrier-end assembly they mate to. There are no splices anywhere in the kit:
the drain is crimped directly into position 12, and WH-BUS-01 replaces what would otherwise
have been eight LED_V splices.

| # | Step | Tooling | Check before proceeding |
|---|---|---|---|
| 1 | Cut all conductors to the section 3 schedule, +10/-0 mm | calibrated tape, flush cutters | 100 % length check on the first article, then 1 in 5 |
| 2 | Strip 3.0 mm at the connector end, 4.0 mm at the site end | thermal or precision die stripper set for PTFE | no nicked, cut or missing strands; PTFE not drawn back |
| 3 | Crimp male contacts on the connector ends | Harwin Z20-320 | visual to A-620 class 2: insulation crimp on insulation, conductor crimp on conductor, bell-mouth present, brush visible |
| 4 | Lay up WH-01: eleven conductors, binder tape, foil 25 % overlap, drain in contact with the foil, TPU jacket | jacketing die or heat-shrink jacket | OD 4.3 mm nominal, 4.6 mm maximum, measured on 3 points |
| 5 | Terminate the WH-01 drain: sleeve, crimp, insert in position 12 | Z20-320, 2:1 clear heat-shrink | one drain, one contact, no stray strand outside the sleeve |
| 6 | Cut back and insulate the WH-01 screen at the helmet end, 10 mm, adhesive-lined shrink | hot-air, 120 C | screen not touching any conductor or any metal part |
| 7 | Lay up WH-02, ten conductors with LED_GND at the centre, TPU jacket | as step 4 | OD 4.5 mm nominal |
| 8 | Insert contacts into the housings in the section 3 order | -- | 100 % pin-by-pin read-back against the wire list, by a second person |
| 9 | Build WH-03, WH-04, WH-05, WH-07 pigtails and the adapters WH-ADP-01/-01B/-02/-03 to section 3.9 | as above | drains landed at the carrier end only; on WH-ADP-01 and -01B the lug-to-contact order proved against the jack in hand, not against the catalogue |
| 10 | Build WH-09: fit the panel receptacle and its gasket to WH-ADP-04, terminate the USB-B end, bond the braid at both ends of this cable only | as above | continuity of all four conductors and the braid; **no continuity from any WH-09 conductor or the braid to DGND, to any harness drain or to the WH-07 return** |
| 11 | **Electrical test of every loose assembly per section 9, before anything is fitted** | test set of section 9 | full record; a failed harness is scrapped, not reworked at the crimp |
| 12 | Fit WH-BUS-01 at N1, square pad 9 facing OE-2; solder LED_V to pad 9, LED_GND to pad 10 and the eight tails to pads 1 to 8 in WH-02 conductor order (section 3.2.1) | temperature-controlled iron, 320 C, no-clean; strip 4.0 mm, tin, feed through from the legend side and solder both sides | LED_GND on its isolated pad and connected to nothing else; board the right way round |
| 13 | Lay WH-01 into channel A and WH-02 into channel B, site by site, from N1 outward | plastic pick | no conductor under tension with the frame opened to 62 cm; min bend radius respected at every node |
| 14 | Terminate at each HM-04 **per section 3.1.1**: solder the conductor to the HM-04A contact tail 8 mm outside the body, sleeve the joint in adhesive-lined shrink, dress it through the inboard slot opening, solder LED leads A and B with the marked lead to LEDn, and coil the 40 mm site service loop. **Not buildable at this issue: HM-04A, HM-05C, the LED seat and the bayonet run do not exist (open item 22)** | iron, adhesive-lined 2:1 shrink | continuity site to connector re-checked per site; the joint dry, clear of the gel port and clear of the spring |
| 14a | Fit the eight electrode assemblies: HM-05C crown into the HM-05B spigot, cup into the carrier, K12 spring into the HM-04 seat, carrier into the bore with its lugs in the two entry slots, then the HM-09 key a quarter turn clockwise. Repeat for all eight | HM-09 service key | retention by hand -- a straight pull of about 10 N does not release it (SVC-EEG-013 section 3 R10); the crown seated; the light window clear. **ASM-EEG-007 Rev B stage 3 has no such step and no stage-3 sign-off line for it. This document does not number an ASM step; the gap is open item 28** |
| 14b | Fit the two ear-reference couplers to the temple tails per sections 3.1.2 and 3.1.2.1: sleeve the free tail over its whole 250 mm per section 4, crimp or solder the GY socket to conductor 9 and the PK socket to conductor 10, then **mate the K2 clips and leave them mated** | crimp or solder per the coupler maker | both clips part by hand without a tool and re-mate fully home; sleeve continuous from the screen cut-back to the coupler body; **the clips leave the bench mated** -- PKG-EEG-015 and IFU-EEG-014 carry the packing rule and it is open item 34. **RULED, not signed, open item 23** |
| 14c | Fit the bias coupler to conductor 11 per section 3.1.3: cut the tail to the F recorded at the fitting trial, sleeve it, crimp or solder the TQ socket, dress it at the halo front and leave WH-10 mated | as 14b | F recorded on the build record for this unit, not assumed from the drawing; the coupler mates and parts by hand; **no 15 N pull is applied to this joint** (section 3.1.3). **RULED, not signed, open items 26, 30 and 31** |
| 15 | Close all cover strips | -- | no conductor trapped in a strip; strips flush |
| 16 | Fit the pod-end P-clips, coil the 120 mm service loops, bond the WH-KEY-01 shrouds over J14 and J30, mate J14 and J30 | -- | shroud seated on the socket and square; **the housing enters one way round only, checked by trying it the other way**; housings fully seated |
| 17 | Fit WH-ADP-04 to the POD-P1 aperture and plug WH-09 into the isolator module; fit its P-clip | -- | gasket seated square; plug fully home; P-clip 40 mm behind the plug |
| 18 | Label every cable at both ends per section 10 | thermal transfer printer | labels legible and correctly oriented |
| 19 | Repeat continuity and screen isolation as an as-built check, **and the H1 leg through each of the three mated couplers** | test set | matches the step 11 record; each coupler mated and re-read |

---

## 9. Test

**These limits are the single home for the harness electrical test.** JIG-EEG-009 section 4.2
cites this table and does not restate it. Where JIG-EEG-009 Rev B gave different figures --
a 500 V all-pairs sweep, a 1000 V AC 1 s dielectric withstand, a 10 N termination pull on 1
in 10 terminations -- those are superseded by the table below. **There is no AC
dielectric-withstand test on any harness assembly.** The only high-voltage tests in this
document are the 500 V DC insulation-resistance measurements of H4 and H10, and both are
insulation-resistance measurements, not hipots.

Every harness is tested as a loose assembly **before it is fitted to a carrier and before the
helmet-end terminations to the contact-light LEDs are made**. This is not a preference. The
500 V DC insulation test would destroy the LEDs and would put 500 V on the ADS1299 module
inputs through the 47 kOhm resistors. The order is: build the cable, test the cable, then
terminate the ends that carry semiconductors.

| ID | Test | Method | Limit | Applies to | Signed by |
|---|---|---|---|---|---|
| H1 | Continuity, every conductor | 4-wire milliohm meter, site terminal to its connector pin | 1.0 Ohm maximum (WH-01, WH-02); 0.5 Ohm maximum (WH-07, WH-09) | all | harness operator |
| H2 | Conductor-to-conductor isolation, all pairs | 100 V DC insulation tester, every conductor against every other | 100 MOhm minimum | WH-01 (66 pairs), WH-02 (45 pairs) | harness operator |
| H3 | Screen continuity and screen isolation | drain to J14.12; drain to every conductor; drain to each cup terminal (HM-04A and HM-05C, section 3.1.1) and to each HM-04 body. **The three touch-proof couplers are deliberately not in this test**: a DIN 42802 socket is single-pole and has no screen terminal, step 6 cuts the WH-01 screen back at the helmet end so all three tails are outside the screen, and the drain-to-every-conductor leg already covers them (section 3.1.2.1 provision 5) | drain to J14.12 2.0 Ohm maximum; all others 100 MOhm minimum | WH-01, WH-03, WH-04, WH-05 | harness operator |
| H4 | Insulation resistance | **500 V DC, 60 s**, conductor bundle to drain where a drain exists, and bundle to any exposed metal; **WH-02 has no screen or drain, so on WH-02 only the bundle-to-exposed-metal leg is run**. **New leg 2026-09-02: the three touch-proof couplers, plug withdrawn**, bundle to any exposed metal with the socket body and its shroud counted as exposed metal | 100 MOhm minimum, no breakdown, no flashover | WH-01, WH-02, WH-03, WH-04, WH-05 | QC inspector |
| H5 | Crimp pull-out | tensile tester, 10 s hold, on **3 sample crimps per batch** | **13 N minimum** for 28 AWG per IPC/WHMA-A-620 class 2 | all crimped ends | QC inspector |
| H6 | Assembly pull test | 60 s hold | panel receptacle in its POD-P1 aperture 50 N minimum; boom detach 30 N minimum; HM-04 termination **15 N minimum** -- which acts on HM-04A's anchorage in the body and on the solder joint to the conductor, **not** on the separable crown interface, which is designed to part at 3 to 6 N with the bayonet (section 3.1.1). **The three free-hanging couplers are excluded from the 15 N leg from 2026-09-02**: 15 N is defined against a body anchorage they do not have and sits above the 13 N at which H5 qualifies a 28 AWG crimp. They are not pulled at all until HM-01 gains a drawn anchorage -- sections 3.1.2.1 provision 4 and 3.1.3, open items 29 and 31 | WH-09, WH-03B, WH-01/-02 site ends | QC inspector |
| H7 | Flex | 1000 cycles, +/-90 deg, at the crown transition | no continuity change; H1 repeated after | first article only | programme engineer |
| H8 | Mate and de-mate | 25 cycles on J14 and J30, then repeat H1. **New leg 2026-09-02: 100 cycles minimum on each of the three touch-proof couplers**, run as-built after step 15 with H1 repeated; the per-unit leg is step 19's as-built repeat and needs no new step | H1 limits still met; withdrawal 0.15 N minimum per contact; **coupler separation force inside 5 to 15 N at cycle 1 and at cycle 100** | first article only | programme engineer |
| H11 | Finger-safety of the unmated couplers | **IEC 60601-1 / IEC 61032 test probe B** applied to each unmated touch-proof socket, all approach angles | no contact with any live part; recorded in the FAI pack | first article only, all three couplers | programme engineer, countersigned by the safety reviewer |
| H9 | Wire-list verification | pin-by-pin read-back against section 3 by a second person | 100 % match | all | second operator |
| H10 | WH-09 barrier isolation | 500 V DC, 60 s, every WH-09 conductor and its braid against DGND, against every harness drain and against the WH-07 return, with WH-09 unplugged from the module | 100 MOhm minimum | WH-09 | QC inspector |

**The 500 V figure and why it is that number.** No insulation-test value existed anywhere in
package v1. 500 V DC is the standard insulation-resistance test voltage for equipment working
below 50 V and is 200 times the +/-2.5 V that the electrode conductors actually see. A
conductor that passes 100 MOhm at 500 V has, by the same insulation, a calculated leakage of
25 nA at the working voltage, 400 times below the 10 uA normal-condition limit of RFQ S-02.
The test is a screen for damaged insulation and trapped strands, not a proof of the safety
case; the safety case rests on R1 to R16 (E-07) and the ADuM4160 (E-24), and its single-fault
arithmetic does not close today (section 5.5).

The same 500 V DC insulation-resistance measurement, made across the isolation barrier on the
assembled unit, is the per-unit isolation test for the kit. The 2.5 kV RMS type test is the
isolator supplier's certificate and is checked once at incoming inspection; there is no
per-unit AC hipot station anywhere in this programme.

**Record.** Every measurement is recorded against the harness serial in the per-unit test
record that ships with the kit, in the format of QP-EEG-010: harness part number and
revision, serial, operator, date, instrument and its calibration due date, and every value in
H1 to H6 and H10 as a number, not a pass mark. H7, H8 and H11 are first-article only and are
recorded in the FAI pack. The record is signed by the harness operator, countersigned by the
QC inspector, and the FAI pack is accepted by the programme engineer before the second unit
is built.

**TST-EEG-004 has no step that checks the harness record, and this document does not invent
one.** TST-EEG-004 Rev C owns the step numbers; what is needed is a document check on the
pack -- "harness record present and within limits" -- not a repeat of the measurements. It is
raised as open item 6 in section 11 against TST-EEG-004's next revision. Rev A of this
document numbered it T2a, which it had no authority to do.

Estimated test time, calculated from the step count and not measured: 14 minutes per harness
set, of which 6 are the all-pairs isolation sweep. This is additional to the per-unit test
time of TST-EEG-004 section 10 and belongs in the RFQ pricing line for provisioning and
functional test. The "25 minutes per unit" figure quoted in Rev A is withdrawn: it was
arithmetically impossible against TST-EEG-004's own step durations, and TST-EEG-004 now
carries the real figure.

Fixture: a 12-way and a 10-way mating adapter built from the same Harwin housings and
contacts as the harness, so the jig proves the real mate and not a laboratory approximation.
These adapters are fixture sub-assemblies and are numbered in JIG-EEG-009 under the FIX-01 to
FIX-04 naming; this document does not number them.

---

## 10. Labelling

Every cable carries one label at each end, applied before the assembly leaves the bench.

| Field | Format | Example |
|---|---|---|
| Part number and revision | `WH-EEG-008-nn RvB` | `WH-EEG-008-01 RvB` |
| Variant | `-P1` or `-H2` | `-P1` |
| Unit serial | `TIOV-B-nnnn`, as issued by PKG-EEG-015 | `TIOV-B-0007` |
| End identifier | `A` = carrier end, `B` = helmet or panel end | `A` |

The unit serial is programme prefix, hardware revision letter and four digits, and it is the
same string on the label, in the Data Matrix, in the USB `iSerialNumber`, in the calibration
record and on the packing list. Phase 1 uses 0001 to 0009.

Label material: printable heat-shrink polyolefin sleeve, Brady PermaSleeve PS-187-2-WT class
or equivalent, thermal-transfer printed, 3.2 mm recovered diameter for the jacketed cables
and 1.6 mm for the pigtails. Wrap-around adhesive labels are not accepted: the whole kit is
wiped with 70 % IPA at every refurbishment and adhesive labels curl. The sleeve is positioned
25 mm behind the connector so it is readable with the connector mated.

Individual conductors are identified by colour, not by a printed number. The colour table of
section 3 is the same table used for the HM-04 site labels, the POD-P1 panel legend required
by RFQ A-06, and the runner's on-screen placement guide, so that the head, the panel and the
screen cannot disagree about which site is which. That statement held for WH-01 and WH-02
only until this issue: **it now holds for the three EMG leads as well**, because section 3.6
is re-issued to the red / yellow / green ruling of IFU-EEG-014 Rev B section 13.2, so the
lead in the participant's hand, the panel legend and the placement guide name one code.

Packing: each helmet ships with its harness already fitted inside HM-01, not loose. Spare
harnesses ship coiled at 120 mm diameter, tied with two hook-and-loop straps, in an
antistatic bag with the label visible through the bag.

Spares policy, to be costed in AVL-EEG-017 and the internal BOM, where the harness currently
carries no cost at all: one spare WH-10 bias lead and two spare ear-reference couplers per ten
kits, two spare WH-01/WH-02 sets and two spare boom assemblies per
twenty-five kits, alongside the existing two spare frames, plus one spare EMG lead set and
one spare WH-09 pigtail per ten kits. The participant's host and charge leads are the A-07
cables and are replaced from stock, not from this line.

---

## 11. Open items

An item that closes keeps its number and stays in this table with the text it carried, so
that a reader who saw the earlier issue can tell a closed item from a deleted one. **Items 7
and 15 are the closed rows at this issue; items 22 to 28 were new at it and items 29 to 34 are
new on 2026-09-02 with the rulings of sections 3.1.2.1, 3.1.3 and 3.1.4.**

| # | Item | Who closes it |
|---|---|---|
| 1 | **No safety engineer has reviewed this design.** The single-fault case of section 5.5 -- one electrode conductor shorted to the drain giving a calculated 53.2 uA against the 50 uA limit of S-02 -- is a specific question for that review, together with ECO-EEG-024's 68 kOhm answer and the E-10 widening it forces. It does not block fabrication or quoting; it blocks use on a person. | RISK-EEG-011 safety review |
| 2 | **The isolator module presents USB-B where RFQ E-24 asks for USB-C.** WH-09 is the interim answer and is built for Phase 1; the non-conformance is open until a module with a USB-C host receptacle is qualified. | AVL-EEG-017, then an ECO |
| 3 | **J15 to J17 have no confirmed carrier part** (section 3.6). A touch-proof 1.5 mm socket with a PCB-mount signal pin and two 1.5 mm retention posts must be sourced and first-articled before Phase 2; AVL-EEG-017 carries a 12-week lead-time risk against it. | AVL-EEG-017, before Phase 2 |
| 4 | **The boom preamplifier part is not chosen** (section 3.3). MAX9814 is AGC and is not approved; a MAX4466-class fixed-gain module is preferred; the interface in ICD-EEG-006 is what is specified until one is bought and measured. | AVL-EEG-017, before Phase 2 |
| 5 | **No room-microphone module is known to meet E-15's hardware mute** (section 3.5). The fallback is a programme-designed capsule-plus-switch sub-assembly that has no drawing and no part number. | AVL-EEG-017, then a new drawing |
| 6 | TST-EEG-004 has no step that checks the harness test record is present and within limits. This document will not number one. | TST-EEG-004 next revision |
| 7 | **Closed on 2026-09-02. The EMG lead colours are ruled red, yellow and green** by IFU-EEG-014 Rev B section 13.2, and section 3.6, the WH-06 table and section 10 of this document are re-issued to that code at this issue. *Was: "The EMG lead colours are not agreed. This document says white, brown and grey; IFU-EEG-014 section 13.2 and PKG-EEG-015 say red, yellow and green for the same three leads. The participant matches lead colour to site, so the two cannot both stand."* The number is not reused. **What is still open is the change record, not the colour:** this correction has no entry in the ECO-EEG-016 register | Closed against IFU-EEG-014 Rev B section 13.2. The register entry is still owed by ECO-EEG-016 |
| 8 | The charge-receptacle shell is specified isolated from DGND, which trades ESD and EMC robustness for leakage margin. Bonding it through an RC network was considered and rejected without measurement. | RISK-EEG-011, then an ECO if the ruling changes |
| 9 | LED_GND's function as a guard conductor is a ruling, not a measurement. If the contact lights are changed to a common-return part, LED_GND becomes the return and this document is re-issued. | ECO-EEG-016 |
| 10 | The contact-light bicolour phase driver is not implemented in firmware, so nothing yet exercises this cable as designed. | FW-EEG-001 |
| 11 | Harwin ordering suffixes are given to the family and way-count. Confirm the current suffixes at IQC, and **with them the two housing dimensions WH-KEY-01 is cut for and the one it imposes**: body width across the flats, taken as 4.20 mm; male contact protrusion, taken as 4.00 mm; and a polarising rib at least 0.70 mm proud within the first way, without which the shroud keys nothing (section 6.1). | AVL-EEG-017 |
| 12 | WH-KEY-01, WH-BUS-01 and the adapters WH-ADP-01, -01B, -02, -03 and -04 have no line in the RFQ pricing template, so nobody is quoting them. All seven now have something to quote from -- WH-BUS-01 fabrication data (section 3.2.1) and AVL-EEG-017 K42, WH-KEY-01 and WH-ADP-02/-03/-04 STEP and STL (sections 3.9 and 6.1) and AVL-EEG-017 K24, WH-ADP-01 and -01B a bought-part class and AVL-EEG-017 K37 -- and the pricing template still has no line for any of them. **The same is now true of the harness itself**: AVL-EEG-017 K25 to K45 and section 1.6.1 price every material, connector, contact and tool in this document, and the pricing template has no line for those either. | RFQ-EEG-001 next revision |
| 13 | The Phase 2 in-frame boom route and the -H2 umbilical lengths are not dimensioned, because the occipital shell is a Phase 2 routing task and the shell in RFQ M-01 is sized for a carrier that no longer has those dimensions. | Phase 2 |
| 14 | **Nothing in this package has been manufactured or measured, and no safety engineer has reviewed it.** Every length, OD, fill percentage, resistance, force and leakage figure above is calculated. | Phase 1 first article |
| 15 | **Closed on 2026-09-02.** PARTS-EEG-019 now records WH-BUS-01 as a two-layer board with the fabrication data set in `kicad/wh-bus-01/`, and AVL-EEG-017 K42 buys the bare board. *Was: "PARTS-EEG-019 Rev B's WH-BUS-01 entry is out of date in two places. It says single-layer, and the board is two layers because the pads are plated through holes; and it says 'specified, not built. No Gerber set has been generated for it', which section 3.2.1 and `kicad/wh-bus-01/` now answer."* The number is not reused. What is still true and is not an open item, because it is the state of the whole package: **no WH-BUS-01 has been fabricated.** | Closed against PARTS-EEG-019, 2026-09-02 issue |
| 16 | **HM-01 has no geometry for WH-BUS-01 at node N1** -- no pocket, no boss, no location dimension. The board is retained by the cover strip and its own solder joints, which is probably enough for a 14 x 10 x 0.8 mm part, but nothing says where within N1 it sits and no drawing can be checked against. | the mechanical package, before the first article |
| 17 | The IPC-D-356A netlist `tools/gerber.py` writes for EEG-CAR-01 states hole diameters in micrometres while its coordinates are in 0.0001 inch, so a tester reading the file to the standard sees every hole ten times too big. `tools/wh_bus.py` writes both fields in 0.0001 inch and says so in the file; the carrier's netlist is not corrected here. | DSN-EEG-003, then `tools/gerber.py` |
| 18 | **MP-01 has no opening over J14 or J30, so with the plate fitted the helmet cables cannot leave their sockets.** J14 is under the 8 mm solid border and J30 under four 12 x 3 mm jumper slots; 9.50 mm of the 18.00 mm carrier-to-plate gap is left above the socket, and WH-01's 13 mm static bend radius needs 15.15 mm for a 90-degree turn before the housing is counted (section 6.1). A relief over both sockets is not cut in this revision. | `tools/mech_gen.py mp01()`, then ICD-EEG-006 section 4 |
| 19 | The J30 shroud reaches to y = 87.33 mm, **0.44 mm from J9's socket body**, which will not hold the end wall of the 1x4 module form of WH-KEY-01 that ICD-EEG-006 section 6.1 puts on J9. Either that form is open-ended on one side or J9 moves. The seventeen module-socket forms are not modelled. | ICD-EEG-006 section 6.1, then `tools/mech_gen.py` |
| 20 | **Four of the five panel adapters sit in an opening that overlaps a button opening** (section 3.9): BTN_B is concentric with the boom opening, BTN_STOP contains the room-microphone port, BTN_A overlaps the headphone opening, and the charge opening runs into both. The adapters are dimensioned to the openings as specified; none can be fitted until `pod_base()` is corrected. | `tools/mech_gen.py pod_base()`, then RFQ M-02 |
| 21 | **`pod_base()` carries no boss for WH-ADP-02, WH-ADP-03, WH-ADP-04 or the WH-09 P-clip**, so all three adapters are bonded to the wall and the section 3.8 P-clip has nothing to screw into. Test H6 pulls the panel receptacle at 50 N, which is then a pull on a bonded joint that has not been made or tested. Both USB plates carry M2.5 clearance holes for the screws that would replace the bond. | `tools/mech_gen.py pod_base()` |
| 22 | **The HM-04 termination is a proposal and not a design.** Section 3.1.1 specifies the joint, and HM-04A, HM-05C, the HM-04 anchorage, the LED seat, the dressed conductor exit and the circumferential bayonet run all have to be drawn and approved before the site end of either helmet cable can be built. `mech_gen.py hm05b()`'s flank solder-tag pocket is superseded by it and is withdrawn. **Narrowed on 2026-09-02: two of those six are cut.** The circumferential bayonet run exists and measures 0.000 mm3 of interference through the quarter turn and through the 0.40 mm of travel, and the LED seat exists as the outboard of two separated pockets, which also closes RISK-EEG-011 SF-9's shared cavity. **Still owed: HM-04A, HM-05C, the 15 N anchorage against a seat that now runs to z 15.60, the dressed inboard exit, and the LED's two lead passages out of its new blind pocket.** | The mechanical reviewer, then the safety reviewer, then AVL-EEG-017 K25 and K26 |
| 23 | **The two ear-reference terminations are a proposal.** Section 3.1.2 resolves the three-way disagreement between this document, AVL-EEG-017 K2 and SVC-EEG-013 R4 in favour of a free-hanging touch-proof coupler on the temple tail. The coupler has no vendor and the decision has no signature. **Ruled on 2026-09-02 (section 3.1.2.1) and still unsigned**: the coupler and the clip are unchanged; what is added is the packing rule (item 34), a stated 150 to 200 mm K2 lead with T8 re-measured, a sleeved free tail, a withdrawn strain relief (item 29), the H4 / H8 / H11 test legs and a 5 to 15 N separation window on K27. | The safety reviewer, then the programme lead for the packing rule, then AVL-EEG-017 K27 on the same purchase order as K2 |
| 24 | **If item 23 is taken, the kit carries five 1.5 mm touch-proof interfaces and an EMG lead will mate an ear socket.** Not a safety fault -- every one of them sits behind its own 47 kOhm resistor on the same rails -- but a silent measurement fault that T10's lead-off check does not catch. Stated, not mitigated. **Grown on 2026-09-02 to six sockets and six plugs**, and it now runs in both directions: a K2 clip's plug will enter J15 to J17, and a K2 clip or a K3 EMG lead will enter the **bias** socket, putting an electrode on the driven output at a site RISK-EEG-011 works only at Fpz. Bounded by the same 47 kOhm as everything else since `design.py` lost its channel-11 override, and still a measurement fault. If the safety reviewer wants genuine non-interchangeability of the driven output, the answer is a connector class or a keyed shroud, not gender or colour. | RISK-EEG-011, then IFU-EEG-014's placement guide; the safety reviewer on the driven-output residual |
| 25 | **WH-03B has a flex duty and no cycle count**, because nothing in the package says how many times a boom is set in a unit's life. Test H7 is run at the gooseneck root for the WH-03B first article and the number comes from there. | Phase 1 first article |
| 26 | **Conductor 11 lands on an "Fpz bias pad, solder tag" that has no part number, no drawing and no feature on any model.** It is the same defect as item 22 at a different site and section 3.1.1 does not close it. **Narrowed on 2026-09-02 by section 3.1.3, not closed**: the pad is deleted as a helmet feature and becomes a disposable K4 pad on the new WH-10 lead, and conductor 11 terminates in a TQ touch-proof socket of the K27 class. What is still owed on the frame is a **halo-front channel mouth and a dressed exit**, on a carried-over STL with no parametric source (PARTS-EEG-019 OA-1) -- one of the three wire exits of section 7. | The mechanical reviewer, with item 22; then the safety reviewer, PARTS-EEG-019 and AVL-EEG-017 K47 |
| 27 | **WH-03, WH-04, WH-05, WH-07 and WH-09 still have no row in `EEG_kit_BOM_for_bidders_RevC.xlsx`**, which is the sheet a contract manufacturer quotes from; WH-01 and WH-02 have rows that read "custom assembly / none". AVL-EEG-017 section 4 now carries the material, connector, contact and tooling lines behind all eight, so the rows can be written; this document cannot write them. | The kit BOM, at its next issue |
| 28 | **ASM-EEG-007 Rev B stage 3 has no step that terminates at HM-04 and no step that fits the cups, the bayonet carriers or the springs**, and its section 9 stage-3 sign-off table has no line for either. Steps 14, 14a, 14b and 14c of section 8 above are the harness half; the ASM steps and their sign-off lines are not this document's to number. ASM section 4.2's "the window is on one side of the body only" is also wrong against the released HM-04 model -- there are two openings and, since 2026-09-02, they are two separate pockets. | ASM-EEG-007, next revision |
| 29 | **The ear couplers have no strain relief and no anchorage, and the H6 15 N leg is withdrawn from them.** The proposal's 2.0 mm adhesive-lined bulb at a temple channel mouth is deleted because the released HM-01 has no temple mouth -- three mouths, all occipital -- and `CH_BORE` is a constant 3.80 mm, so nothing reacts a bulb anywhere. Carried open beside the identical OE-1 / OE-2 anchor entry in KNOWN_ISSUES.txt. Nothing is pull-tested here until a temple wire exit is added to `tools/mech_gen.py` and registered. | The mechanical reviewer with the PARTS / MECH owner, then this document's section 9 |
| 30 | **The free tail F on conductor 11 is not a number yet**, and its cut length is 1940 + F. It is a fitting dimension: bounded below by the clearance a hand needs to mate the coupler clear of the HM-02A brow pad, above by the 250 mm the ear tails carry. **Conductor 11's 1980 mm must not be carried forward** -- it contains no free tail. Conductors 4 and 5 cut at the same figure for unrelated reasons and do not move. | The first fitting trial; recorded per unit on the build record at step 14c |
| 31 | **The bias coupler's retention value depends on a frame feature that does not exist.** With a drawn HM-01 anchorage it aligns with H6 at 15 N; without one it is capped at H5's 13 N minimum for a 28 AWG crimp, and 15 N must not be written against it. | The mechanical reviewer, with items 26 and 29 |
| 32 | **The K12 spring has no retention or capture feature, no ASM fitting step and no SVC handling step.** Section 3.1.4 issues the spring itself; nothing holds it if a carrier is drawn without one, and a lost or mis-seated ring is a silent open electrode under a cup that still looks fitted. KNOWN_ISSUES.txt already records that no assembly step fits the cups, the carriers or the springs at all. | The mechanical reviewer for the capture feature; ASM-EEG-007 and SVC-EEG-013 for the steps, with item 28 |
| 33 | **The HM-04 / HM-05B rest datum is ambiguous by 0.10 mm, and it is the datum a spring is quoted against.** `mech_gen.py` states 0.40 mm of axial float from a 9.00 mm bore against an 8.60 mm body, which puts the spring's rest height at 3.50 mm; but the lug at z 1.20 comes to rest on a lip whose roof is at z 1.10, which stands the carrier 0.10 mm proud and makes the rest height 3.60 mm and the stroke 0.50 mm. Section 3.1.4's spring is specified to be indifferent to which is true; the models should not stay ambiguous. | `tools/mech_gen.py`, then MECH-EEG-020 sheet 8 |
| 34 | **The packing rule that section 3.1.2.1's safety argument rests on belongs to four documents this one does not own.** The ear clips must travel mated and captive: PKG-EEG-015 section 1.1 line 2.1 to read "2 fitted, HELMET HM-01" and its (408, 162) 94 x 100 mm bay to become EMG LEADS only; IFU-EEG-014 section 1's table and section 9 step 1 re-issued; SVC-EEG-013 R12 to say the clips are left mated and dressed inside the helmet bay; RISK-EEG-011 H-20 and H-30 re-checked against the result. Without it the participant mates two of five identical DIN plugs every session, K27's life margin falls from 5x to 1.4x, and open item 24 becomes a per-session participant error. | The programme lead, across PKG-EEG-015, IFU-EEG-014, SVC-EEG-013 and RISK-EEG-011 together |

---

## 12. Gaps closed by this document

| Gap id | Closed by |
|---|---|
| harness-wire-list-absent | sections 3.1 to 3.8, one row per conductor with site, pin, net and colour |
| conductor-count-contradiction | section 2, with the v1 statements, the ECO-EEG-016 error and the Rev B budget that adds up |
| led-lines-have-no-driver | section 3.2 -- J19 is 1x16 in Rev B and Q0 to Q7 reach LED1 to LED8 through R70 to R77 (ECO-EEG-001); the firmware driver is still open, item 10 |
| contact-light-colour-vs-conductors | section 3.2, two-lead bicolour on LEDn / LED_V at 240 Hz with WH-BUS-01 splitting the common eight ways |
| screen-and-drain-termination | section 5, including the pod-end-only rule at R91 and the do-not-connect instruction at the head |
| cable-datasheet-missing | section 4 |
| cut-length-schedule | sections 3.1 and 3.2, with the 1500 mm -P1 umbilical fixed |
| j14-mating-connector-and-tooling | section 6, including the mis-mate table and WH-KEY-01 |
| emg-lead-assembly-and-din-screen | section 3.6, with deviation DEV-WH-01 recorded, the socket part still open, and the lead colour ruled red / yellow / green by IFU-EEG-014 Rev B section 13.2 and carried here |
| boom-cable-and-trrs-pinout | section 3.3 |
| max9814-location-conflict | section 3.3 -- the preamplifier is on MP-01, connected at J21, and which part it is remains open |
| panel-flylead-schedule | sections 3.4 and 3.5 |
| host-cable-and-gland | **superseded.** The host connector is a socket on the isolator module presented through a gasketed POD-P1 aperture; WH-08 and the gland are withdrawn; section 3.8 specifies WH-09 and reconciles A-07 |
| isolator-connector-mismatch | section 3.8 and open item 2 -- stated as a live non-conformance with WH-09 as the interim answer |
| harness-test-specification | section 9, which is the single home for the limits that JIG-EEG-009 section 4.2 cites |
| harness-assembly-drawing-and-identity | part numbers WH-EEG-008-01 to -07 and -09, section 8 build order, section 10 labelling and spares |
| wh-key-01-has-no-geometry | section 6.1 and `tools/mech_gen.py wh_key01()` -- three forms, released as STEP and STL, with the two housing dimensions it is cut for and the one it imposes named in the same section, and the one mis-mate it does not stop stated in the table |
| wh-adp-adapters-to-be-created | section 3.9 -- five adapters, each with what it mates at both ends, what it is made from, its wire list and what has to be confirmed; WH-ADP-02, -03 and -04 modelled in `tools/mech_gen.py`, WH-ADP-01 and -01B specified as a bought jack class with no printed part |
| hm04-termination-does-not-exist | **not closed; specified.** Section 3.1.1 states what is missing, what the released HM-04 and HM-05B actually carry, what the joint has to do, a proposed method with its reasoning, the geometry the models must gain, the four alternatives rejected and who has to decide. It is a proposal and it is marked as one, and open item 22 carries it |
| ear-reference-termination-unbuildable | **not closed; specified, then ruled.** Section 3.1.2 sets out the three incompatible joints the package described and proposes the free-hanging touch-proof coupler that satisfies all three constraints, with the mis-mate it creates stated as open item 24. Section 3.1.2.1 rules it on 2026-09-02 and attaches nine provisions with values -- the packing rule, a stated K2 lead length with T8 re-measured, a sleeved tail, a withdrawn strain relief, the H4 / H8 / H11 legs, a 5 to 15 N separation window, the colour, the life margin and the two-way mis-mate. It is not signed |
| bias-termination-does-not-exist | **not closed; specified.** Section 3.1.3 deletes the "Fpz bias pad" as a helmet feature, terminates conductor 11 in a TQ touch-proof socket of the K27 class at the halo front, adds WH-10 and a fourth K4 disposable pad, replaces the 1980 mm cut with 1940 + F, caps the pull test at H5's 13 N, states the cross-mate residual, and says in the same paragraph as the current numbers that **SR-12 is not closed by any of it**. It is not signed |
| k12-spring-cannot-be-bought | **closed as a specification, open as a purchase.** Section 3.1.4 issues the spring against the deepened seat: 0.50 mm wire, 6.40 / 5.40 mm diameters, 2.2 active coils, 1.20 N/mm, 6.90 mm free length, 2.10 mm solid, 3.96 to 4.56 N over the working stroke and inside 3 to 6 N over the whole tolerance band, with the arithmetic, the no-gold relation, the R6 qualification regime and ten measurements on the first five. Five samples only; no fleet order; not signed |
| wh-03b-has-no-cable-specification | section 4, as a fifth column of the materials table, with the both-ends screen termination, the ultrasonic-immersion requirement, the corrected plug type and the flex duty stated in place of an invented cycle count |
| harness-has-no-purchasing-lines | AVL-EEG-017 section 4 lines K25 to K45 -- raw cable, screen, drain, jacket, sleeving, connectors, contacts, tooling, panel jacks, receptacles and the WH-BUS-01 bare board -- and section 1.6.1 for the per-way-count connector table. The bidders' BOM rows are still owed and are open item 27 |
| harness-connector-system-decided-three-ways | section 6: one system, Harwin M20, chosen because `mech_gen.py` cuts the WH-KEY-01 cavity to it; ICD-EEG-006 section 3.1's Molex KK 254 wording is corrected and AVL-EEG-017 section 1.6.1 carries the per-way-count table |
| wh-bus-01-has-no-fabrication-data | section 3.2.1 and `kicad/wh-bus-01/` -- two-layer Gerber X2, one Excellon drill file, an IPC-D-356A netlist, a placement and BOM note and a README, all written by `tools/wh_bus.py`. Nothing has been fabricated |
