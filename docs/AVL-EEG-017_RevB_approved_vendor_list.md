# APPROVED VENDOR LIST AND SOURCING FILE

**Document:** AVL-EEG-017  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this document and
design.py disagree, design.py governs.

**Revision note (Rev A to Rev B):** the carrier grew to 150.0 x 130.0 mm and became a
four-layer board, so the bare-board line, its price basis and the purchase-order checklist all
change; the C1-C16 part number is corrected to a real C0G part and the Sallen-Key 100 nF
capacitors are labelled X7R; R85 becomes 150 kOhm; C20/C40/C60 become 10 uF; R94/R95 and three
fiducials are added; the headphone line is settled at 32 to 64 ohm; and the duplicated board
specification, keep-out, star-point and noise arithmetic are replaced by cross-references.
**Also within Rev B, 2026-09-02, after the completeness audit of package v2.3: the harness is
purchasable.** New §1.6.1 settles the 2.54 mm crimp connector system on **one** family --
Harwin M20, because that is the envelope `tools/mech_gen.py` cuts the WH-KEY-01 shroud to --
and carries the per-way-count housing and contact table that this document and ICD-EEG-006
§3.1 both pointed at and neither contained; ICD-EEG-006 §3.1's contradictory Molex KK 254
wording is corrected in that document at the same issue. §4 gains **K25 to K45**: the two
halves of the HM-04 electrode termination, the ear-reference coupler, all four raw cable
materials, the screen tape and drain, the jacket, the sleeving and label stock, the JST mating
set, the 3.5 mm panel jack, the USB-C panel receptacles and their CC pull-downs, the WH-09 base
assembly, the WH-03B boom lead, the WH-BUS-01 bare board and the harness adhesive -- none of
which had a purchasing line anywhere in the package -- plus **K46**, the printed fixture set
released in `fixtures/`. K1 and K2 gain notes reconciling what they
buy with what the harness terminates on, and **K24 now names the twelve printed parts that
gained released geometry** and, separately, the four that have not, so a print bureau's quote
says which parts it covers. Five of the new lines are **OPEN WITH CRITERIA** because they wait
on a design decision or on a datasheet the programme has not read; §10 items 13 to 16 carry
them. The revision letter does not change; this is a correction within the same release.

**Also within Rev B, 2026-09-02, after the decision review of package v2.3: three of those
open lines gain values and a fourth line is opened.** Rulings D2-EAR-REFERENCE-COUPLER,
D3-BIAS-FPZ-TERMINATION and D5-K12-SPRING-ENVELOPE are written into §4 at this issue. **K27
becomes three units, not two**, and gains a separation-force window of 5 to 15 N — it was the
only separable interface in the kit with no force window at all — and a first-article
finger-safety check with a real test probe rather than a supplier declaration. **K2 gains two
purchase-order fields**, a stated plug-to-jaw lead length and a plug colour, exactly the
correction K1 already carries one line above it, and is ordered on the same purchase order as
K27. **K12 becomes a specification a buyer can shop**: the ruling declined to issue one against
a 4.50 mm spring seat, `tools/mech_gen.py hm04()` deepened that seat to 6.60 mm on the same
day, and WH-EEG-008 §3.1.4 now derives the spring from the released solids. **New K47** buys
the WH-10 bias lead that WH-EEG-008 §3.1.3 creates when it deletes the Fpz bias pad as a helmet
feature. **None of the four rulings is a signature**; §10 items 13, 14, 17 and 18 say who has
to sign, and no sample has been submitted against any of them. The revision letter does not
change; this is a correction within the same release.

The findings of the second cross-document audit of 1 September 2026 are closed in this same
issue, without a further revision letter: the routing result and the release status are stated
from `kicad/EEG-CAR-01_RevB_DRC_report.txt` -- zero violations, all 145 nets connected, 169
connections relaxed to get there, and the data released for review and not for fabrication --
and the fiducial ruling is cited as RUL-EEG-021 Rev A rather than as the uncontrolled worksheet
`tools/RULINGS.md`.

## Why this document exists

Package v1 asked a contract manufacturer to buy "any 2.54 mm socket strip", "Murata C0G/X7R",
"Nexperia BAV99 / BAT54S", "generic microSD SDMMC breakout", "Chinese equivalent" and
"certified generic" -- and then told the same manufacturer, in RFQ section 10, that
substitutions need written approval. Those two instructions cannot both be followed, because
nothing said what the parts actually were. The audit of v1 recorded it in four findings:
`carrier-bom-avl-mpn`, `approved-alternates-matrix`, `module-male-headers-missing` and
`supplier-quality-and-avl`. This file closes them. It gives one row per purchasable line with
a manufacturer, a manufacturer part number, a distributor order code, packaging, RoHS and
lifecycle status, the approved alternates and the rule that decides when an alternate may be
used; it names the interface each purchased module must meet so a substitute can be qualified
rather than guessed at; and it states, plainly, which lines have no qualified vendor yet.

---

## 0. How to read this file

**Four sourcing states.** Every line carries one.

| State | Meaning |
|---|---|
| **PREFERRED** | The part the design was calculated against. Buy this unless an ECO says otherwise. |
| **APPROVED ALTERNATE** | Qualified equivalent. May be bought without a new request, subject to the line's substitution rule. |
| **OPEN WITH CRITERIA** | No vendor is qualified yet. The criteria are stated; a sample must be submitted to the programme and approved before the fleet order. |
| **PROHIBITED** | Named because a buyer would otherwise reach for it. Do not buy. |

**Distributor codes.** The order codes below follow Mouser Electronics' manufacturer-prefix
convention (Vishay `71-`, Murata `81-`, Nexperia `771-`, Texas Instruments `595-`, Omron
`653-`, Bourns `652-`, JST `538-`, Adafruit `485-`). They are given so a buyer can paste a
line straight into a basket. **No code in this file has been checked against a live
distributor catalogue by the programme.** Confirm every one against the MPN on the day the
purchase order is raised; where a code and an MPN disagree, the MPN governs. Digi-Key,
Farnell and RS Components are approved second sources for the same MPNs.

**Lifecycle.** Every active line below is shown as Active because that is the manufacturer's
published status at the time of writing. The programme runs no obsolescence monitoring
service. Section 6.4 makes re-checking lifecycle a purchase-order step, and any line that is
not Active at PO requires written approval before purchase.

**MSL.** Moisture sensitivity applies to the plastic-packaged semiconductors only. Ceramic
chip resistors and capacitors carry no MSL. The stated levels are the manufacturers'
declarations; the reel or tube label is the record, and IQC checks it (QP-EEG-010 §2.3).

**Attrition and build quantity.** The phase quantities are RFQ-EEG-001 Rev E section 1's and
are not restated here as a requirement: Phase 1 is 2 prototypes, Phase 2 is 10 kits and
Phase 3 is 10 to 40 further kits, 25 to 50 in total. Purchase quantities in section 5 are
computed as `ceil(qty per board x boards to build x 1.05)` for surface-mount parts and
`x 1.02` for through-hole parts, on this build plan:

| Phase | Kits | Spare assembled boards (25 %) | Boards to build |
|---|---|---|---|
| 1 | 2 | 0 | **2** |
| 2 | 10 | 3 | **13** |
| 3 lower | 25 | 7 | **32** |
| 3 upper | 50 | 13 | **63** |

**Nothing in this package has been manufactured or measured, and no safety engineer has
reviewed this design.** Every figure marked *calculated* is exactly that; no vendor named here
has yet supplied a part to the programme; and until an electrical safety reviewer is appointed
no Class A substitution can be approved and no unit may be used on a person (§6.3, §10 item 8).

---

## 1. Carrier sub-BOM -- EEG-CAR-01 Rev B

The carrier is **150.0 x 130.0 mm** and **four layers** as of this revision. Both changes came
out of doing the layout rather than asserting it, and both change what is bought: see §1.5.

`tools/design.py` carries **211 reference designators**, 614 pads and 156 nets. Twenty-five of
those designators are fabricated features and are not purchased: TP1-TP18 (test pads),
MH1-MH4 (mounting holes) and FID1-FID3 (fiducials, new at this revision, ECO-EEG-020).
**186 purchased placements per board: 153 surface-mount, of which 152 are fitted because R89
is DNP, plus 33 through-hole, plus one bare board.** Extracted from `tools/design.py` and
grouped by value, footprint and MPN.

This is the count a buyer works from. QP-EEG-010 §3 IP-3's "24 through-hole parts, 201 plated
holes" and ASM-EEG-007 §2.1's "33 parts, 236 plated" disagree with each other; the designator
census above is the one taken from the source file, and the plated-hole count belongs to the
drill file, not to this document.

### 1.1 Resistors -- all 0603 (1608 metric)

| Designators | Qty | Value / description | Manufacturer + MPN | Mouser code | State | Approved alternate | Substitution rule |
|---|---|---|---|---|---|---|---|
| R1–R16 | 16 | 47 kΩ 0.1 % 25 ppm/K thin film, ≥ 50 V -- electrode series protection (E-07). **Fitted at 47 kΩ on the Phase 1 prototypes only: at 47 kΩ the single-fault DC leakage of RFQ S-02 is 53.2 µA against a 50 µA limit and S-02 is NOT met.** ECO-EEG-024 raises the value to 68 kΩ. | Vishay TNPW060347K0BEEA | 71-TNPW060347K0BEEA | PREFERRED **for Phase 1 only** | Panasonic ERA-3AEB473V; KOA RN73H1JTTD4702B. **68 kΩ (Vishay TNPW060368K0BEEA) becomes the preferred value if ECO-EEG-024 is confirmed.** | **Thin film only.** Thick film of any tolerance is PROHIBITED: excess noise and tempco land directly on a 10 µV input. All sixteen on one board from one manufacturing lot. **Do not buy the fleet reel until ECO-EEG-024 is decided** -- see §3 and §5. The noise and flatness arithmetic for both values lives in RISK-EEG-011 §4 and is not repeated here. |
| R20, R21, R23, R24, R40, R41, R43, R44, R60, R61, R63, R64 | 12 | 10 kΩ 0.1 % thin film -- rectifier and absolute-value stages, and the load the envelope AC coupling works into | Vishay TNPW060310K0BEEA | 71-TNPW060310K0BEEA | PREFERRED | Panasonic ERA-3AEB103V | 0.1 % required: the R/2 : R ratio sets the full-wave transfer. R20, R40 and R60 also set the AC-coupling corner with C20/C40/C60 (§1.2, ECO-EEG-027); do not change either half alone. |
| R25, R26, R27, R45, R46, R47, R65, R66, R67 | 9 | 22 kΩ 0.1 % thin film -- Sallen-Key R1/R2 and divider top | Vishay TNPW060322K0BEEA | 71-TNPW060322K0BEEA | PREFERRED | Panasonic ERA-3AEB223V | Value fixed by ECO-EEG-006. Changing it moves f₀ = 48.8 Hz outside the E-11 filter band. |
| R22, R42, R62 | 3 | 4.99 kΩ 0.1 % thin film -- half-wave summing R/2 | Vishay TNPW06034K99BEEA | 71-TNPW06034K99BEEA | PREFERRED | Panasonic ERA-3AEB4991V | Must be half of the 10 kΩ line to within 0.1 %; buy both from the same manufacturer. |
| R28, R48, R68 | 3 | 2.2 kΩ 0.1 % thin film -- output divider bottom (×0.0909) | Vishay TNPW06032K20BEEA | 71-TNPW06032K20BEEA | PREFERRED | Panasonic ERA-3AEB222V | Sets the ±100 mV envelope scaling. |
| R70–R77 | 8 | 1 kΩ 1 % thick film -- contact-light series | Vishay CRCW06031K00FKEA | 71-CRCW06031K00FKEA | PREFERRED | Yageo RC0603FR-071KL; Panasonic ERJ-3EKF1001V | Free. Digital zone. With Vf = 2.0 V the drive is (3.3 − 2.0) / 1000 = **1.3 mA per site and 10.4 mA total from GPIO48** *(calculated)*. Every document in the package uses these two figures. |
| R50, R51, R52, R81, R83, R88 | 6 | 10 kΩ 1 % thick film -- button pull-ups, comparator divider bottom, GPIO limiter, 74HC595 MR pull-up | Vishay CRCW060310K0FKEA | 71-CRCW060310K0FKEA | PREFERRED | Yageo RC0603FR-0710KL | Free. R81 and R83 are affected by ECO-EEG-023 -- see §1.3. |
| R84, R86 | 2 | 100 kΩ 1 % -- VBUS divider top, buck-boost enable pull-up | Vishay CRCW0603100KFKEA | 71-CRCW0603100KFKEA | PREFERRED | Yageo RC0603FR-07100KL | R86 is a rail-sequencing part (ECO-EEG-002). Do not raise its value. |
| R85 | 1 | **150 kΩ** 1 % -- VBUS divider bottom, **3.00 V at VBUS = 5 V** | Vishay CRCW0603150KFKEA | 71-CRCW0603150KFKEA | PREFERRED | Yageo RC0603FR-07150KL | **Changed from 56 kΩ by ECO-EEG-022.** 5 × 150/250 = 3.00 V, above the 2.48 V V_IH of a 3.3 V ESP32-S3 input. The 56 kΩ of Rev A gave 1.79 V and would not reliably have asserted the first of the two S-01 charge interlocks. Ratio with R84 is a safety interlock input: it is not a tuning choice. |
| R94, R95 | 2 | **4.7 kΩ 1 % -- I²C pull-ups on SDA and SCL to DVDD3V3** | Vishay CRCW06034K70FKEA | 71-CRCW06034K70FKEA | PREFERRED | Yageo RC0603FR-074K7L | **New at this revision, ECO-EEG-021.** Rev A had no pull-up anywhere on the carrier and the bus depended on whatever the modules happened to carry, which is not a design. If a fitted module also carries pull-ups the parallel value must be checked against the bus capacitance before the fleet build; that check has not been done. |
| R80 | 1 | 470 kΩ 1 % -- comparator threshold top | Vishay CRCW0603470KFKEA | 71-CRCW0603470KFKEA | PREFERRED | Yageo RC0603FR-07470KL | With R81 sets the 52 mV trip of E-12. Value may change under ECO-EEG-023 (§1.3). |
| R82 | 1 | 1 MΩ 1 % -- comparator hysteresis, ≈ 5 mV | Vishay CRCW06031M00FKEA | 71-CRCW06031M00FKEA | PREFERRED | Yageo RC0603FR-071ML | -- |
| R78, R79, R87, R90, R91, R92, R93 | 7 | 0 Ω jumper, ≥ 1 A | Vishay CRCW06030000Z0EA | 71-CRCW06030000Z0EA | PREFERRED | Yageo RC0603JR-070RL | **A real 0 Ω part, never a solder bridge or a wire link.** R90 and R91 are the single star points; the rule that governs them is DSN-EEG-003 Rev C §3.3 and is not restated here. R78's approved alternate is 47 Ω where light current needs trimming. |
| R89 | 1 (**DNP**) | 2.2 kΩ 1 % -- electret bias, do not populate | Vishay CRCW06032K20FKEA | 71-CRCW06032K20FKEA | PREFERRED | Yageo RC0603FR-072K2L | Buy the line, do not fit it. Fitted only if the preamplifier module on MP-01 supplies no microphone bias (ICD-EEG-006 §7.2). |

Seventy-two resistor placements, one of them DNP. Packaging for every line above: cut tape
(7 in reel) or a full reel. Vishay TNPW 0603 full reel is 5000 pieces; CRCW 0603 full reel is
5000. **MSL: not applicable.** RoHS 3 compliant, REACH SVHC-free per the manufacturers'
declarations, lead-free terminations. **Lifecycle: Active.**

### 1.2 Capacitors, ferrite and fuse

| Designators | Qty | Value / description | Manufacturer + MPN | Mouser code | State | Approved alternate | Substitution rule |
|---|---|---|---|---|---|---|---|
| C1–C16 | 16 | 10 nF **C0G/NP0** 50 V ±5 %, 0603 -- electrode RF filter to AGND_REF | **Murata GCM1885C1H103JA16D** | 81-GCM1885C1H103JA16D | PREFERRED | 4.7 nF C0G, same series, **only on a written ECO** | **X7R, X5R and Y5V are PROHIBITED here.** The `C1` in the part number is the C0G dielectric code and the `J` is the ±5 % tolerance; check both on the reel label. **The Rev A part number `GCM188R71H103KA37D` was wrong -- its `R7` code is X7R, not C0G -- and is withdrawn (ECO-EEG-019.)** The sixteen RC time constants set the corner, the 100 Hz flatness of E-10 and the common-mode match behind E-04; the arithmetic lives in RISK-EEG-011 §4. Note that if ECO-EEG-024 raises R1-R16 to 68 kΩ the corner moves with it, and this line is re-checked against E-10 at the same time. |
| C21, C41, C61 | 3 | 100 nF **X7R** 25 V, 0603, **±15 % over the operating temperature range** -- Sallen-Key C to AGND_REF | Murata GCM188R71E104KA57D | 81-GCM188R71E104KA57D | PREFERRED | TDK CGA3E2X7R1E104K080AA | **These are X7R and are labelled X7R deliberately. A 100 nF C0G in 0603 at 50 V is not a stocked part, so the design accepts a class 2 dielectric here (ECO-EEG-019).** *This line carried ECO-EEG-019's wording that "TST-EEG-004's filter-corner tolerance is widened to match". That sentence is **withdrawn: no widened corner tolerance was ever written into TST-EEG-004**, and section 16 item 16 of that document records that it was not.* What TST-EEG-004 has is **T12e, which measures and records f₀ per unit against 42 to 58 Hz**, the band these parts can hold. ±15 % over temperature moves f₀ between 42.4 and 57.4 Hz, which does not fit inside the 45 to 55 Hz of RFQ E-11's 50 Hz ±10 %, so **buying this line correctly does not make E-11 met: its low-pass half is a stated non-conformance** until E-11 is restated to 42 to 58 Hz or a stocked C0G part is qualified. Rev A called this line C0G and quoted an X7R part number, which a buyer could not act on. The ratio to the 220 nF part sets Q = 0.74; keep both from one manufacturer so the two dielectrics track. |
| C22, C42, C62 | 3 | 220 nF X7R 25 V, 0603 -- Sallen-Key feedback | Murata GCM188R71E224KA64D | 81-GCM188R71E224KA64D | PREFERRED | TDK CGA3E3X7R1E224K080AB | Ratio to the 100 nF part sets Q. Keep both from one manufacturer. |
| C23, C24, C43, C44, C50, C51, C52, C63, C64, C80–C88 | 18 | 100 nF X7R 25 V, 0603 -- local decoupling and button debounce | Murata GCM188R71E104KA57D | 81-GCM188R71E104KA57D | PREFERRED | Samsung CL10B104KB8NNNC; Yageo CC0603KRX7R9BB104 | Free. Decoupling and debounce only. Same MPN as C21/C41/C61: one reel covers both lines. |
| C102, C103 | 2 | 100 nF 50 V, 0603 -- AVDD and AVSS HF decoupling at the module rail entry | Murata GCM188R71H104KA57D | 81-GCM188R71H104KA57D | PREFERRED | TDK CGA3E2X7R1H104K080AA | `design.py`'s descriptive text calls this line C0G; **the `R7` code makes it an X7R part and it is bought as X7R.** In an HF decoupling position the dielectric is not load-bearing, which is why the mislabel is corrected rather than the part changed. The 50 V rating is kept for margin on the ±2.5 V rails. |
| C20, C40, C60 | 3 | **10 µF X5R 16 V ±20 %**, 0603 -- envelope input AC coupling into R20/R40/R60 (10 kΩ), **1.6 Hz corner** | Murata GRM188R61C106MA73D | 81-GRM188R61C106MA73D | PREFERRED | Samsung CL10A106MA8NRNC; TDK C1608X5R1C106M080AC | **Changed from 1 µF by ECO-EEG-027.** The fitted 1 µF gave 15.9 Hz, which removes the speech envelope it is meant to pass; E-11 is restated as **≤ 2 Hz** and 10 µF into 10 kΩ gives 1.59 Hz. **The margin is thin and it is a purchasing constraint: at the −20 % end of the M tolerance the corner is 1.99 Hz, just inside the limit, so a 10 µF part with a wider tolerance or a heavier DC-bias derating than this one is PROHIBITED on this line.** Do not order this line as "same as the bulk 10 µF" without checking the tolerance letter. |
| C70–C74, C89, C90, C100, C101 | 9 | 10 µF X5R 16 V, 0603 -- rail bulk | Murata GRM188R61C106MA73D | 81-GRM188R61C106MA73D | PREFERRED | Samsung CL10A106MA8NRNC; TDK C1608X5R1C106M080AC | **16 V minimum.** At 5 V a 16 V X5R 0603 loses roughly half its capacitance to DC bias; the bulk figure is already sized for that. A 6.3 V part is PROHIBITED. |
| L1 | 1 | Ferrite bead 600 Ω at 100 MHz, 1.5 A, 0603 | Murata BLM18PG601SN1D | 81-BLM18PG601SN1D | PREFERRED | TDK MPZ1608S601A | DC resistance ≤ 0.10 Ω. Feeds VDD_ISO; a lossier bead drops the isolator's device-side supply. |
| F1 | 1 | PTC resettable fuse, 1.1 A hold / 2.2 A trip, 6 V, 1206 | Bourns MF-MSMF110-2 | 652-MF-MSMF110-2 | PREFERRED | Littelfuse 1206L110/6WR; Bel Fuse 0ZCJ0110FF2E | Safety-relevant: it is the only current limit on the charge input (E-23). Hold current must not exceed 1.1 A. |

Fifty-four capacitor placements, of which twelve are the 10 µF X5R part across two lines with
different rules. Packaging: Murata GCM/GRM 0603 in 4000-piece paper tape reels, cut tape
available; MF-MSMF in 2000-piece reels. **MSL: not applicable to the ceramics.** RoHS 3
compliant. **Lifecycle: Active.** The GCM series is Murata's automotive-grade line and is
chosen for its longer declared availability, not for AEC qualification, which this instrument
does not need.

### 1.3 Semiconductors

| Designators | Qty | Description | Manufacturer + MPN | Mouser code | Package | MSL | State | Alternate | Rule |
|---|---|---|---|---|---|---|---|---|---|
| D1–D16, D23 | 17 | Dual switching diode, series pair, common centre pin -- electrode clamp to AVDD/AVSS (D1–D16) and ENV_CMP clamp (D23) | Nexperia BAV99,215 | 771-BAV99215 | SOT-23, 3000/reel | 1 | PREFERRED | none for D1–D16 | **BAT54S is NOT approved for D1–D16.** Schottky leakage across a 47 kΩ series resistor is an offset error on a 10 µV input. Pinout is locked: pin 1 → AVSS, pin 2 → AVDD, pin 3 → the node between R(n) and C(n). Any proposed substitute must be a series pair with the common node on pin 3 and must be checked against that diagram before build. The v1 string "BAV99 / PESD" is withdrawn. D23's role changes under ECO-EEG-023 from the only thing between ±2.5 V and a 3.3 V pin to a belt-and-braces clamp; the part does not change. |
| D20, D40, D60 | 3 | Dual Schottky, series pair -- precision half-wave rectifier | Nexperia BAT54S,215 | 771-BAT54S215 | SOT-23, 3000/reel | 1 | PREFERRED | onsemi BAT54SLT1G | Approved **only** in the envelope rectifier positions. Pin 3 sits at the op-amp output (ECO-EEG-005); a part with a different internal arrangement inverts the rectifier. |
| D24 | 1 | Bidirectional TVS array, 5 V working -- charge-input transient suppressor | Nexperia PESD5V0S2BT,215 | 771-PESD5V0S2BT215 | SOT-23, 3000/reel | 1 | PREFERRED | Littelfuse SP0503BAHT | Safety-relevant (E-23). Working voltage must not exceed 5.5 V. |
| U1, U2, U3 | 3 | Quad precision CMOS op-amp, rail-to-rail I/O, 5.5 V absolute maximum -- rectifier, absolute-value summer, 50 Hz filter, output buffer | Texas Instruments **OPA4376AIDR** | 595-OPA4376AIDR | **SOIC-14 (D)**, 2500/reel | 1 | PREFERRED | none | **No alternate.** `design.py` places `SOIC-14_3.9x8.7mm_P1.27mm`; Rev A of this file quoted the TSSOP part OPA4376AIPWR, which does not fit that land pattern, and it is withdrawn. The part runs from the ADS1299 module's ±2.5 V rails -- 5.0 V total -- and must be rail-to-rail on both input and output with an absolute maximum at or above 5.5 V. Rev A's dual OPA2376 is superseded by ECO-EEG-004 and must not be re-introduced. Quiescent current 760 µA per amplifier, 3.04 mA per package *(calculated)*, inside the ICD-EEG-006 §2.1 rail budget. |
| U7 | 1 | Push-pull comparator, 40 ns, 5.5 V maximum -- stimulus onset (E-12) | Texas Instruments TLV3201AIDBVR | 595-TLV3201AIDBVR | SOT-23-5, 3000/reel | 1 | PREFERRED | none | Open-drain variants (TLV3202-class open-drain, LMV7239) are PROHIBITED: the carrier fits no pull-up on CMP_RAW. **ECO-EEG-023 re-powers U7 from DVDD3V3 and DGND instead of AVDD and AVSS and re-references its inputs to a DVDD3V3/2 divider with the envelope AC-coupled into it. That change is ruled but is NOT yet in `design.py`, which still wires U7.2 to AVSS and U7.5 to AVDD, and the divider and coupling capacitor therefore have no designators and no part numbers in this file.** Two or three passive lines will appear here when it is drawn, and the safety and layout reviewer must check the change before it is built. Do not order U7's surrounding passives as final until then. |

Twenty-one diodes and four amplifier packages. RoHS 3 compliant, lead-free terminations,
halogen-free. **Lifecycle: Active** for all five lines. Tape-and-reel is the standard
packaging; tube or cut-tape quantities are available for Phase 1 and are the sensible buy at
two boards.

### 1.4 Connectors, switches and mechanical

| Designators | Qty | Description | Manufacturer + MPN | Order code | State | Alternate | Rule |
|---|---|---|---|---|---|---|---|
| J22 (1×3), J5, J9, J10, J11, J18, J27, J28 (1×4 ×7), J21, J23, J25, J26, J29 (1×6 ×5), J12, J20 (1×8 ×2), J2, J4, J30 (1×10 ×3), J1, J3, J14 (1×12 ×3), J8 (1×14), J19 (1×16), J6, J7 (1×22 ×2) | 25 strips | 2.54 mm single-row female socket strip, vertical through-hole, **gold over nickel on the contact**, dual-wipe | Samtec SSW-1nn-01-G-S (nn = way count: 03, 04, 06, 08, 10, 12, 14, 16, 22) | Samtec direct (samtec.com) or Mouser/Digi-Key by MPN | PREFERRED | Harwin M20-782xx45 series; Preci-Dip 801-87-0nn-10-001101 | **Tin-plated strips are PROHIBITED on J2, J4, J14, J22, J23 and J29.** Those sockets carry IN1–IN8, SRB1, BIASOUT, the electrode harness, the spare channels and the analogue rails; a tin contact against the board's ENIG gold is a bimetallic junction and a thermocouple inside a 10 µV measurement. Gold ≥ 0.76 µm on the contact area. Insertion force, mating height and current rating to be stated on the CoC. Board holes are 1.00 mm. **J21 is a 1×6, not a 1×4**; ASM-EEG-007 §3.4's socket-family list has it wrong and is corrected against this table and ICD-EEG-006 §1. |
| J13, J24 | 2 | 2.00 mm PH-series through-hole header, 2-way, vertical -- cell input and charge pigtail | JST B2B-PH-K-S(LF)(SN) | 538-B2B-PH-K-S | PREFERRED | none | Mating parts are a separate line: JST **PHR-2** housing (538-PHR-2) and **SPH-002T-P0.5S** crimps (538-SPH-002T-P0.5S), two of each per board, with the WC-160 hand tool or equivalent. Board holes are 0.90 mm. |
| J15, J16, J17 | 3 | Touch-proof 1.5 mm safety socket to DIN 42802, **PCB-mount**, colour-coded (EMG1 cheek / EMG2 submental / EMG3 laryngeal) | -- see below -- | -- | **OPEN WITH CRITERIA** | -- | See §1.4.1. |
| SW1, SW2, SW3 | 3 | Tactile push switch, 6.0 × 6.0 mm body, **5.0 mm actuator**, ≥ 100 000 cycles, 160 gf ±50 | Omron B3F-4055 | 653-B3F-4055 | PREFERRED | C&K PTS645SM50SMTR92; E-Switch TL1105AF160Q | RFQ E-26 is a **6 mm tactile switch with a 12 mm coloured cap on an extender**; the "≥ 12 mm actuator" wording of Rev C described the cap, not the switch, and the two were read as one part. The panel openings are **13.0 mm on a 14 mm pitch at y = 76, 90 and 104 mm** on the POD-P1 right wall. The 12 mm caps (A green, B blue, stop red) and their extenders are a separate kit line. A substitute with a different actuator height needs a lid change, not a BOM change. Board holes are 1.20 mm. |
| MH1–MH4 | 4 | M3 non-plated mounting holes, Ø3.2 mm at (5,5), (145,5), (5,125) and (145,125), 6 mm copper keep-out | -- | -- | not purchased | -- | Fabricated feature (ECO-EEG-007). Coordinates moved with the board outline at this revision. Fixing hardware is in §1.6. |
| FID1–FID3 | 3 | Ø1.0 mm round copper fiducials with Ø3.0 mm mask openings, at (12, 10), (144, 100) and (12, 120) | -- | -- | not purchased | -- | **New at this revision, ECO-EEG-020.** Fabricated feature. They exist so the placement machine has three global fiducials of its own; the v1 workaround of teaching vision on test-point pads is withdrawn. **RUL-EEG-021 Rev A section A** transcribes them as (8, 8), (142, 8) and (8, 122); `design.py` governs, and the coordinates above -- (12, 10), (144, 100) and (12, 120) -- are the ones in the source file, confirmed against `tools/design.py` at this correction. |
| TP1–TP18 | 18 | Ø1.5 mm test pads | -- | -- | not purchased | -- | Bare copper, mask-relieved. |

#### 1.4.1 The DIN 42802 sockets -- the one line with no qualified vendor

`design.py` names *Stäubli SLB1,5-F / LB-I1,5*. **That is a class of part, not a confirmed PCB
part: those are cable and panel parts.** The carrier footprint `DIN42802_1p5mm_Socket` is a
single Ø1.7 mm plated signal pin on a 2.6 mm pad with two Ø1.50 mm non-plated retention posts
at ±3.5 mm, inside a 9.8 × 7.8 mm body. No catalogue part has been confirmed to fit it. This
was audit finding `specsheet-file-contradictions` and it is **not closed by this document** --
it is stated, and WH-EEG-008 §6's flat assertion that "mating sockets on the carrier are
Stäubli SLB1,5-F / LB-I1,5" is corrected to match.

The criteria a submitted sample must meet, per QP-EEG-010 §11.2:

| Criterion | Requirement |
|---|---|
| Standard | Touch-proof 1.5 mm socket to DIN 42802-1 |
| Finger safety | Finger-safe to IEC 60601-1 for a type BF applied part; no accessible conductive part with the plug withdrawn |
| Termination | One Ø1.7 mm PCB pin on the footprint centre, two Ø1.5 mm retention posts at ±3.5 mm, or a documented deviation with a drawing |
| Colour coding | Three distinct colours, recorded per site in WH-EEG-008 |
| Current rating | ≥ 1 A stated on the datasheet |
| Mating force | Stated, and repeatable over ≥ 500 cycles |
| Evidence | Dimensioned drawing, RoHS/REACH declaration, ISO 10993-5 and -10 declarations if any part of the socket can be touched (S-05), CoC per lot |
| Approval | Physical sample submitted to the programme; approved in writing before the fleet order |

Candidate vendors to approach: Stäubli Electrical Connectors (Allschwil, Switzerland) for a
PCB-terminated variant of the LB-I1,5 family; Wuhan Greentek (an existing programme supplier
for electrodes) for its DIN 42802 socket range; Plastics One / Bio-Medical Instruments.
**Class A supplier** in QP-EEG-010 §11.1 -- this is a patient-safety part and the v1 language
"or Chinese equivalent" is withdrawn. **The programme carries a 12-week first-article
lead-time risk against this line** (§3), and it must be sourced and first-articled before
Phase 2.

### 1.5 Bare board

**The board specification table is not restated here.** It lives in **DSN-EEG-003 Rev C §3.2**
and the fabricator is quoted against that table plus the Gerber, drill and IPC-D-356A set.
That set is **released for review, not for fabrication** -- see the routing result at the end
of this section -- so it supports a quotation and a layout review, and not yet an order. The
review is RFQ-EEG-002A; a bare-board order follows it. The isolation keep-out and the
star-point rule live in **DSN-EEG-003 Rev C §3.3**. What this section carries is only what a buyer needs in order to raise the order.

| Item | Purchasing summary | State |
|---|---|---|
| EEG-CAR-01 Rev B bare PCB | **150.0 × 130.0 mm**, rectangular, no cut-outs or slots. **FOUR layers: L1 signal, L2 reference plane, L3 reference plane, L4 signal.** FR-4, Tg ≥ 150 °C, **1.60 mm ± 10 %** finished. **Outer copper 1 oz (35 µm) finished; inner copper 0.5 oz (17 µm).** Stack-up: mask / 35 µm L1 / prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask. ENIG, Au 0.05–0.10 µm over Ni 3.0–6.0 µm. Green LPI mask both sides, white legend both sides. Minimum track 0.20 mm, minimum clearance 0.20 mm. **Through vias only -- 0.60 mm pad / 0.30 mm finished hole, tented both sides. No blind, buried, back-drilled, filled or plugged vias: do not quote them and do not offer them.** Plated holes 0.30 / 0.90 / 1.00 / 1.20 / 1.70 mm. Non-plated: 4 × 3.2 mm, 6 × 1.50 mm, **no copper and no mask** (ECO-EEG-012). IPC-6012 class 2 and IPC-A-600 class 2 (IPC-A-610 class 2 applies to the assembly, §6.2 evidence line 9). 100 % electrical test to the supplied IPC-D-356A netlist, 156 nets. Full specification: DSN-EEG-003 Rev C §3.2. | PREFERRED: any fabricator meeting the above with a lot-specific CoC |

**Why the board changed, and what it costs.** Package v1 asserted that a two-layer carrier
would be cheap and easy to route. Actually laying it out showed that it is not: on two layers
the bottom side has to be both the reference plane and the second routing surface, and it
cannot be both. Four layers give two full routing surfaces **and** a continuous reference under
every analogue trace, which is what DSN-EEG-002 §13's layout rules ask for and which a
swiss-cheesed two-layer pour cannot deliver. The board also grew from 130 × 124 mm to
150 × 130 mm because thirty connectors, 211 parts and 156 nets would not close at the smaller
size. Priced: **at 2 units the four-layer board is about €35 more in total; at 50 units it is
about €3 per board**, and the extra 33.8 cm² of bare board is a few euro per unit. That is the
right trade for a sixteen-channel EEG front end, and it is the single most important thing
package v2 learned by doing the work instead of asserting it. **Every quotation held against
the Rev A two-layer 130 × 124 mm outline is void and must be re-requested.**

Approved fabricators, none yet used by the programme: Eurocircuits (Mechelen, BE), Leiton
(Berlin, DE), Newbury Electronics / PCB Train (UK), PCBWay, JLCPCB, Elecrow (all Shenzhen,
CN). All six quote four-layer FR-4 with ENIG as a standard process; none of them needs a
non-standard stack-up for this board. The two mandatory hard-reject checks at goods-in are
IQC-B6 (the six DIN retention holes and the four M3 holes carry no plating and no mask) and
IQC-B7 (the isolation keep-out defined in DSN-EEG-003 Rev C §3.3 is free of copper on **all
four** layers, inner planes included -- the plane cut-out is new work for the fabricator and is
the check most likely to be missed on a first article). Both are safety characteristics under
S-03. Buy 25 % spare bare boards at Phase 2 and Phase 3.

**The routing result. Every figure below is quoted from
`kicad/EEG-CAR-01_RevB_DRC_report.txt` and not from this document.** EEG-CAR-01 Rev B is routed
on four layers, 150.0 x 130.0 mm, with 3 745 track segments and 552 through vias. **All 145 nets
are fully connected**, none unclosed and none without copper, and each reference plane is one
continuous island per net on both inner layers. The smallest measured clearance is 0.260 mm on
F.Cu, 0.275 mm on B.Cu and 0.285 mm on the planes, against a 0.20 mm rule. The narrowest
conductor is 0.200 mm and the smallest plated hole is 0.300 mm. Copper stands 2.00 mm clear of
every non-plated hole, no digital net enters the analogue zone, there are no duplicate segments
and no duplicate via positions, and there is exactly one AGND_REF-to-DGND bridge and one
HARN_SHIELD-to-DGND bridge. **The report raises no violation of any kind** -- its own line is
"VIOLATIONS: 0 -- none.  The board passes every rule listed above" -- so the keep-out of
DSN-EEG-003 Rev C §3.3 is free of copper on all four layers in the layout as routed, stated here
because the report says it, and IQC-B7 above is still what confirms it on the fabricated article.

**The layout passes the programme's own DRC, at minimum geometry.** Closing the board cost the
router **169 relaxed connections**: 36 took a conductor narrower than the 0.25 mm preferred
width, and 133 kept full width and took a reduced gap instead. All 169 sit at or above the
0.20 mm minimum conductor and the 0.20 mm minimum gap, which is why they pass. The fabricator
should read the bare-board line above with that in mind: the 0.20 mm minimum track quoted there is
really used -- the narrowest conductor on the board is 0.200 mm -- and this is not a layout with
room to spare against its own minima.

**The fabrication data is RELEASED FOR REVIEW under RFQ-EEG-002A, not for fabrication.** The
release gate of ECO-EEG-016 §3 -- zero DRC violations, every net one connected copper island,
both inner planes continuous under the analogue zone -- is met on all three counts. What has not
happened is a human layout review: the routing came from the programme's own tools and no layout
engineer has looked at it. **This document therefore supports a quotation against the bare-board
line above, and the data may be issued for that review; a bare-board order follows the review,
not this page.**

### 1.6 Module interface hardware

Package v1 had no line for any of this. The carrier presents 25 female sockets and the
purchased breakouts arrive with their header strips loose in the bag; without these lines the
manufacturer receives a bag of modules and a board full of sockets and cannot connect them.
Six soldering operations per unit, and at 50 units 300 header strips, were neither bought nor
priced. This closes audit finding `module-male-headers-missing`.

| Item | Qty per unit | Description | Manufacturer + MPN | Order code | Rule |
|---|---|---|---|---|---|
| Male header stock | 6 strips | 2.54 mm break-away male header, 1×40, **gold flash over nickel**, 6.0 mm mating pin length | Samtec TSW-140-07-G-S | Samtec direct or Mouser by MPN | Cut to the lengths of ICD-EEG-006 §3.4: 1×12, 1×10 and 1×6 per ADS module; 1×14 codec; 1×4 isolator; 1×5 ATECC; 1×6 charger; 1×4 gauge; 1×8 microSD; 1×6 preamp; 1×16 shift register; 1×4 room mic. Fitted from the component side, soldered underside, body flush, perpendicular within 2°, using the carrier's own socket as the alignment fixture. |
| Ribbon jumper cable | ≈ 1.5 m | Flat ribbon, 28 AWG (7/0.127) stranded tinned copper, PVC, 1.27 mm pitch, grey with a red stripe on conductor 1 -- used at 2.54 mm by discarding alternate conductors | 3M 3365/34 (34-way, cut down) | Mouser 517-3365/34 | 17 jumpers, 134 carrier ways, ≤ 60 mm each (ICD-EEG-006 §3). Way 1 is the red stripe, both ends, always. IPC/WHMA-A-620 class 2. |
| Screened ribbon | ≈ 0.3 m | As above with a foil or braid screen and a drain wire -- JMP-02, JMP-04, JMP-23, JMP-29 only | 3M 3517/10 or equivalent screened flat cable | Mouser by MPN | Drain terminated **at the carrier end only**, into the AGND_REF crimp of JMP-23.4 / JMP-29.4. Module end floating. |
| Crimp connector housings and contacts | 38 housings, 298 contacts | 2.54 mm single-row crimp housings and contacts, **female at the module end and male at the carrier end**, way counts per ICD-EEG-006 §3.3 and WH-EEG-008 §1 | **Harwin M20 crimp system** -- see §1.6.1, which is the single home for these lines | see §1.6.1 | §1.6.1 carries the per-way-count table, the selection criteria and the quantities, and it also covers the five crimped harness housings so that the kit buys one connector system and one crimp tool. Printed heat-shrink sleeve at each end naming the jumper and the connector. **Module end: a shrouded polarised IDC header wherever the module has one; otherwise pin 1 is marked and the jumper is labelled.** |
| Keying shroud **WH-KEY-01** | 1 print set | Printed 2.54 mm keying shroud fitted over every carrier socket that takes a jumper | part of the MP-01 print set (§4, MJF line) | -- | **Jumper keying is decided at this revision.** The carrier end is keyed by WH-KEY-01, not by a nylon rod in an NC way; ICD-EEG-006 §6 lists which sockets take one. Rev A's Ø0.6 mm nylon monofilament line is withdrawn. |
| Carrier-to-plate standoff | 4 | M3 × 18 mm nylon hex, female-female | Würth 970200321 | Mouser 710-970200321 | With **8 × M3 × 6 mm nylon screws** (Würth 709030300 class), four into the standoff at the carrier end and four at the plate end. ASM-EEG-007 §3.3's "12 mm standoff, four screws" is wrong and is corrected against this line and ICD-EEG-006 §4. The 18 mm length is load-bearing for the safety case: it puts the slant path from carrier copper to any host-side conductor on MP-01 at ≥ 18 mm, which closes RISK-EEG-011 SR-08 against an 8 mm requirement. |
| Module standoff | ≈ 20 | M2.5 × 6 mm nylon female-female, with M2.5 × 5 mm nylon screws | Würth 970250321 class | Mouser by MPN | MP-01 is **146.0 × 126.0 × 3.0 mm** with an 8 mm solid border, twelve 3 mm jumper slots on a 16 × 7 mm grid and Ø2.7 mm M2.5 fixing holes between the slot rows. A module picking up fewer than two fixing holes is held with a tie mount and foam tape and that is recorded on the build record. |
| Adhesive cable-tie mount | 24 | 19 × 19 mm, acrylic adhesive, ≥ 70 °C | Panduit ABMM-A-C | Mouser 649-ABMM-A-C | Two per module group. |


#### 1.6.1 The 2.54 mm crimp connector system, per way count

Package v1 had no line for these at all. Rev B as first issued named a family and a way count
and no order code; **ICD-EEG-006 §3.1 named a different and incompatible family** -- "a Molex
KK 254 crimp build: female housings 22-01-30nn with 08-50-0114 terminals at the module end,
free-hanging male housings with 08-52-0072 terminals at the carrier end, with the exact housing
part numbers per way count fixed at kitting and listed in AVL-EEG-017" -- and pointed here for
the per-way-count numbers, which were not here. So thirty-eight connector bodies and about
three hundred contacts per unit could not be put on a purchase order, and an EMS could not tell
which of two systems to quote.

**The system is Harwin M20, and the reason is geometric rather than commercial.**
`tools/mech_gen.py` cuts the WH-KEY-01 keying shroud -- the part that stops the one
safety-relevant mis-mate in the kit (WH-EEG-008 §6) -- at `KEY_CAV_W = M20_HSG_W + 0.30
= 4.50 mm`, and its own assertions require both that the housing enter with 0.30 mm of
clearance and that a reversed housing be stopped by `M20_HSG_W + M20_KEY_MIN - KEY_CAV_W =
0.40 mm` of interference. **A housing outside 4.20 +0.10 / −0.20 mm across the flats either
does not enter the shroud or is not keyed by it.** A Molex KK 254 body is not that envelope, so
taking the ICD's wording would have made every printed shroud in the kit the wrong size,
silently, and left the reversed-WH-01 mis-mate with nothing but a dust cover in front of it.
**ICD-EEG-006 §3.1 is corrected to this table at this issue**; WH-EEG-008 §6 already specified
M20 for the five crimped harness housings, so one system now serves the harness and the jumpers
and the kit carries one crimp tool and one extraction tool instead of two of each.

**No order code below is confirmed, and none is invented.** Harwin's M20 ordering codes carry a
way-count element and a plating suffix that cannot be constructed by guesswork from the family
root, and the programme has not had a current Harwin catalogue in front of it. Every line is
therefore **OPEN WITH CRITERIA** with the criteria stated, which is what that state exists for.
The buyer resolves each code against Harwin's current catalogue on the day the order is raised
and **writes the resolved code back into this table** (§8 checklist; WH-EEG-008 open item 11).
An empty order code gets asked about; a guessed one gets bought.

**Common criteria, every line in this sub-section.** 2.54 mm pitch, single row, **crimp and not
IDC**, gold flash over nickel on the contact, rated for 24 to 30 AWG stranded, and:

| # | Criterion | Requirement | Why it is there |
|---|---|---|---|
| C1 | Housing body width | **4.20 mm +0.10 / −0.20 across the flats** | WH-KEY-01's 4.50 mm cavity, `mech_gen.py KEY_CAV_W` |
| C2 | Polarising rib | **≥ 0.70 mm proud of the body, within the first way from the way-1 end** | without it the shroud keys nothing and is a dust cover (WH-EEG-008 §6.1) |
| C3 | Male contact protrusion | **4.00 mm proud of the mating face** | the shroud's 12.50 mm height is 8.50 mm of socket mating height plus 4.00 mm of lead-in, so it has hold of the housing before the contacts touch |
| C4 | Contact resistance | **≤ 50 mΩ after 20 insertion cycles** | ICD-EEG-006 §3.1's qualification, unchanged |
| C5 | Mating height | consistent with ICD-EEG-006 §4's 8.50 mm socket budget | the carrier-to-plate stack |
| C6 | Retention in the housing | contact latches; extractable with the Z20-431 without damage | a jumper is re-worked at IQC, not scrapped |
| C7 | Evidence | a dimensioned drawing carrying the body width, the rib position and the contact protrusion, plus a CoC per lot | **C1, C2 and C3 are the three figures `mech_gen.py` carries as UNCONFIRMED.** One drawing closes all three and releases WH-KEY-01 for printing |

**Housings, per unit.** Way counts are the union of ICD-EEG-006 §3.3's seventeen jumpers and
WH-EEG-008 §1's five crimped harness assemblies. The **carrier end is male** because every
carrier connector is a female socket strip (§1.4); the **module end is female** because the
module headers are male (§1.6, ICD-EEG-006 §3.4).

| Way count | Male, carrier end | Female, module end | Where they go |
|---|---|---|---|
| 3 | 0 | 0 | J22 takes a WH-KEY-01 shroud but no cable and no jumper lands on it in a standard build (WH-EEG-008 §2). One male 3-way if the Phase 2 EOG option is taken |
| 4 | **7** | **4** | carrier: J5, J9, J10, J11, J18 (WH-03), J27 (WH-04), J28. Module: JMP-05, -09, -10, -28. Add one female 4-way if the charger and the gauge are two boards (JMP-12's gauge branch) |
| 5 | 0 | **1** | JMP-11's module end. ICD-EEG-006 §3.3 makes it a four-way carrier socket serving a five-way module in a different pin order, so the housing is five ways wide with four contacts loaded. **Whether the unloaded position is at an end -- in which case a 4-way serves -- depends on the module's header order, which no document records. Buy the 5-way and confirm at IQC** |
| 6 | **4** | **4** | J21, J23, J25, J29. Add one female 6-way for JMP-12's charger branch in the two-board case |
| 8 | **2** | **2** | J12, J20. One female 8-way in the two-board case, because JMP-12's module end becomes 6 + 4 |
| 10 | **3** | **2** | carrier: J2, J4 and **J30 (WH-02)**. Module: the two ADS analogue headers |
| 12 | **3** | **2** | carrier: J1, J3 and **J14 (WH-01)**. Module: the two ADS digital headers |
| 14 | **1** | **1** | J8, the codec module |
| 16 | **1** | **1** | J19, the shift-register module |
| **Total** | **21** | **17** | **38 housings per unit** |

**J28 is one connector, not two.** ICD-EEG-006 §3.3 lists it as JMP-28, a 60 mm jumper to the
room-microphone module, and WH-EEG-008 §3.5 lists the same socket as the carrier end of WH-05,
a 180 mm cable to the module on WH-ADP-02 bonded to the pod wall. They are the same
connector on the same socket; the module is not on MP-01, so WH-05 is what is actually built
and there is no separate jumper. It is counted **once** in the table above. The seventeen-jumper
and 134-carrier-way figures that ASM-EEG-007 §8, ICD-EEG-006 §3.3 and DSN-EEG-003 §2.1 all
quote are left standing so that a correction which is not an ECO does not move a labour
estimate under three documents, and ICD-EEG-006 §3.3 now carries the note. **Do not buy two.**

**Contacts, per unit.** One contact per loaded way.

| Line | Qty/unit | Note |
|---|---|---|
| Male crimp contact, carrier end | **164** | 134 jumper ways (ICD-EEG-006 §3.3) + 30 harness ways: WH-01 12, WH-02 10, WH-03 4, WH-04 4. WH-05's four are inside the 134 |
| Female crimp contact, module end | **134** | 136 if the charger and the gauge are two boards |
| **Total** | **298** | Buy at **× 1.10**; crimps are made by hand and mis-crimps happen. The NC ways of ICD-EEG-006 §6.1 note 3 are not crimped at the carrier end, so real usage is a little lower and the difference is absorbed in the same allowance. *The 1.10 is a stated allowance, not a measured yield* |

| Item | Qty | Description | Manufacturer + MPN | Order code | State | Rule |
|---|---|---|---|---|---|---|
| Male crimp contact, carrier end | 164/unit | 2.54 mm male crimp, gold flash over nickel, 24–30 AWG | Harwin **M20-118** series -- the family root WH-EEG-008 §6 has quoted since Rev A | **not resolved -- see the rule** | OPEN WITH CRITERIA | Criteria C3, C4, C6, C7. Resolve the current ordering suffix at IQC and write it here |
| Female crimp contact, module end | 134/unit | 2.54 mm female crimp, gold flash over nickel, 24–30 AWG | Harwin M20 female crimp, family not yet quoted by the programme | **not resolved -- see the rule** | OPEN WITH CRITERIA | Criteria C4, C6, C7. **This line has never been named anywhere in the package**, not even by family: the module end needs female contacts and only the male part was ever written down |
| Male housing, per way count | 21/unit | polarised single-row crimp housing, way counts in the table above | Harwin **M20-106** series -- the family root §1.6 has quoted since Rev A | **not resolved -- see the rule** | OPEN WITH CRITERIA | Criteria C1, C2, C5, C7. **C1 and C2 are the two that decide whether WH-KEY-01 works** |
| Female housing, per way count | 17/unit | polarised single-row crimp housing | Harwin M20 female housing family | **not resolved -- see the rule** | OPEN WITH CRITERIA | Criteria C5, C7. Not shroud-constrained: the module end is keyed by the module's own shrouded header where it has one |
| Crimp hand tool | 1 per bench | ratchet crimp tool for the M20 contact | Harwin **Z20-320** | by MPN | OPEN WITH CRITERIA | Named in WH-EEG-008 §6. Confirm it covers **both** the male and the female contact before ordering one tool; if it does not, this is two tools and the harness build time of ASM-EEG-007 §8 moves |
| Extraction tool | 1 per bench | contact extractor | Harwin **Z20-431** | by MPN | OPEN WITH CRITERIA | Named in WH-EEG-008 §6 |

**Spares.** Two crimped harness sets and two boom assemblies per twenty-five kits, one EMG lead
set and one WH-09 pigtail per ten kits (WH-EEG-008 §10). Housings and contacts for those sets
are inside the × 1.10 above only at the unit level; the spare-set quantity is added on top when
the fleet order is placed.

---

## 2. Purchased modules

Modules do not plug into the carrier. They sit on the MP-01 plate and connect through keyed
2.54 mm ribbon jumpers; the ESP32-S3-DevKitC-1 is the one exception and is inserted directly
into J6 and J7. **Twelve module types are purchased and thirteen module assemblies are fitted
per unit**, because the ADS1299 breakout is fitted twice; twelve of the thirteen mount on
MP-01 and the DevKit does not. Each row states the ICD-EEG-006 section that defines the
interface, so a substitute is qualified against a written requirement rather than a brand name.

| # | Block | Carrier | Qty/unit | Manufacturer + part | Distributor | ICD interface | State | Alternate |
|---|---|---|---|---|---|---|---|---|
| M1 | ADS1299 8-channel front end | J1/J2/J23 and J3/J4/J29 | 2 | PiEEG **PiEEG-8** ADS1299 board, or an ADS1299 breakout meeting §2.1 | PiEEG direct (pieeg.com), Crowd Supply | **§2.1** | PREFERRED | OpenBCI Cyton (Phase 1 bench reference only, not a fitted alternate) |
| M2 | Controller | J6, J7 | 1 | Espressif **ESP32-S3-DevKitC-1-N16R8** | Mouser (356- prefix), Digi-Key (1965- prefix), Espressif official store | **§5** | PREFERRED, **not substitutable (E-18)** | none |
| M3 | Audio codec + headphone amplifier | J8, J9 | 1 | ES8388-class I²S codec module with a headphone amplifier and an HP_TAP node | -- | **§2.3** | **OPEN WITH CRITERIA** | WM8960 module, with a firmware change |
| M4 | USB isolator | J10 | 1 | Olimex **USB-ISO** (ADuM4160, open hardware, Plovdiv, BG) | Olimex direct, Mouser, Farnell | **§2.4** | **OPEN WITH CRITERIA** -- device not substitutable (E-24), module not yet qualified | none |
| M5 | Secure element | J11 | 1 | Adafruit **4314** ATECC608 breakout | Adafruit direct; Mouser 485-4314; Digi-Key 1528-4314-ND | **§2.5** | PREFERRED, **not substitutable (E-21)** | none |
| M6 | Li-ion charger with power path | J12 | 1 | Adafruit **4755** bq24074 charger | Adafruit direct; Mouser 485-4755 | **§2.6** | PREFERRED | MCP73871-based module, subject to §6 qualification |
| M7 | Fuel gauge | J12 (gauge branch of the Y jumper) | 1 | Adafruit **5580** MAX17048 | Adafruit direct; Mouser 485-5580 | **§2.6** | PREFERRED | BQ27441 module, firmware change |
| M8 | Buck-boost 5.00 V | J25 | 1 | Pololu **S13V15F5** 5 V step-up/step-down regulator (or TPS63020-class module) | Pololu direct, Mouser | **§2.7** | **OPEN WITH CRITERIA** | any module meeting §2.7 with the enable measurement passed |
| M9 | microSD, one-bit SDMMC | J20 | 1 | Adafruit **4682** microSD SPI-or-SDIO breakout, **3 V only** | Adafruit direct; Mouser 485-4682 | **§2.8** | PREFERRED | none confirmed |
| M10 | **Boom-microphone preamplifier, mounted on MP-01** | J21 | 1 | Fixed-gain electret preamplifier -- see below | -- | **§2.9** | **OPEN WITH CRITERIA** | -- |
| M11 | Room microphone with hardware mute | J28 | 1 | Analogue microphone module with an analogue-domain mute input | -- | **§2.10** | **OPEN WITH CRITERIA** | -- |
| M12 | 8-bit shift register | J19 | 1 | 74HC595 breakout at 3.3 V with SER, SRCLK, RCLK, OE, MR and QA–QH all brought out | -- | **§2.11** | **OPEN WITH CRITERIA** | Nexperia 74HC595D on a SOIC-16-to-DIP adapter, as a controlled fallback |

**M1, the ADS1299 modules -- a contradiction resolved.** RFQ-EEG-001 Rev E section 10 lists
"the ADS1299 modules" as not substitutable; ICD-EEG-006 §2 says every module except the
DevKit and the isolator is specified by interface. Both are correct once the level is stated.
**The device is not substitutable: E-01 requires the full eight-channel TI ADS1299; the -4 and
-6 variants are not acceptable.** The *breakout board carrying it* may be changed, but only
through the ten-step qualification of ICD-EEG-006 §6 and an ECO. The module must generate
AVDD = +2.50 V and AVSS = −2.50 V on board and expose both, because the carrier's sixteen
clamps, three envelope detectors and comparator all run from those rails; must have ≥ 25 mA
spare on each rail against a carrier analogue load of about 10 mA per rail *(calculated)*;
must expose DAISY_IN and CLKOUT; and must have module #1 as the clock source. Module #1 and
module #2 are not interchangeable once fitted -- label both at incoming inspection and keep
the pair together.

**M2, the DevKit -- one measurement stands between this line and a new BOM item.** The carrier
draws a **calculated 288 mA worst case** from the DevKit's own 3.3 V regulator. That is inside
its rating but dissipates about 0.5 W inside a closed pod. Phase 1 measures it at TST T3 and
reports the case temperature; **if it exceeds 85 °C, a 3.3 V regulator on the carrier fed from
V5V becomes an ECO against Rev C and this file gains a regulator line.** It is not solved, and
a buyer planning the Phase 2 order should know the BOM may grow by one part.

**M4, the isolator -- the single most safety-critical purchased part.** The ADuM4160 device is
mandated by E-24 and S-03 and cannot be changed. No module has been qualified. The Olimex
USB-ISO is the leading candidate because it is open hardware, so its layout can be published
and the creepage across the barrier verified rather than assumed, and because it is made in
the EU. **It presents a USB-B host receptacle, not the USB-C that E-24 asks for. That is a
live non-conformance and it is not settled; the interim answer is a short USB-B-to-USB-C panel
pigtail, WH-09, carried until an isolator module with a USB-C host connector is qualified.**
The host connection is a **socket, not a captive cable**: the receptacle is presented through
a gasketed aperture in POD-P1, the WH-08 captive lead and its cable gland are deleted from the
Phase 1 build and become a Phase 2 item for the helmet shell, and one of the two A-07 cables
is the host lead. Whatever module is bought must arrive with an isolation certificate stating
≥ 2.5 kV RMS for one minute -- that certificate is the type test, checked once at incoming
inspection, and the per-unit test is a **500 V DC insulation-resistance measurement across the
barrier, not a hipot**. The module must be strapped for full speed with the device-side pull-up
disabled, and is inspected 100 % at goods-in for anything -- component, track or label --
bridging the barrier (QP-EEG-010 §2.2).

**M6 and M7, the charger and the gauge.** **One combined charger-plus-gauge assembly on a
single J12 jumper is the baseline.** The two Adafruit boards named above are the fallback: if
two separate breakouts are supplied, the gauge mounts on MP-01 and its VBAT and I²C taps are
made at the MP-01 end of the J12 jumper as the **Y jumper drawn in ICD-EEG-006 §3.3**, not as
a hand-built variation. Buy against the drawing, not against the improvisation.

**M10, the boom preamplifier -- where it is, and why the MAX9814 is not approved.** The
preamplifier is **on the MP-01 module plate, connected at J21**. The boom carries the bare
electret capsule and its screen on the pigtail at J18. `design.py` governs: J21 is a carrier
socket. Package v1, DESIGN_FACTS §2, RFQ §2, RFQ E-14 and DSN-EEG-003 §2 all put the
preamplifier on the boom and are corrected; WH-EEG-008's "on the carrier" is also corrected,
because MP-01 is not the carrier. **Which preamplifier is not settled, and it must be stated as
not settled.** ICD-EEG-006 §2.9 requires a **fixed** gain, because E-16 reports a
reference-tone gain in the session metadata and a gain that moves is not a gain. The MAX9814
named in package v1 has automatic gain control, which RFQ E-14 forbids ("AGC off"); disabling
it is a module-dependent modification, so **the MAX9814 is not approved and is named here only
as the package-v1 candidate.** The preferred route is a fixed-gain part of the MAX4466 class --
Adafruit **1063**, adjustable gain, with the trimmer set at build and locked with varnish and
its position recorded on the build record. Until a part is bought and measured the module is
specified by interface in ICD-EEG-006 §2.9 and nothing else. Either way the part is qualified
under §6 step 4 and the strap or trimmer position is written into the device history record.

**M11, the room microphone -- no catalogue part is known to meet E-15.** The requirement is a
**hardware** mute that gates the audio in the analogue domain; a register-controlled mute does
not meet it. MIC_MUTE is defined mute-not: high = live, low or open = muted, and GPIO21 floats
at reset, so the muted state must be the module's default with the line open. Verification is
ICD-EEG-006 §2.10: with JMP-28 way 4 unmated and the module powered, the audio path must be
attenuated by ≥ 60 dB. **If no module does this -- and none is known to -- the fallback is an
electret capsule with an analogue switch (Nexperia NX3L1G66GW or TI TS5A3159) in the
module-end connector of JMP-28, which becomes a programme-designed sub-assembly and a new
drawing.** WH-EEG-008 §3.5 already names one such implementation on an adapter "WH-ADP-02";
that adapter has no drawing, no part number and no line in this file, and it cannot be bought
until it has all three.

---

## 3. Long-lead and single-source risk

Exposure is stated as the number of units that cannot ship if the line is unavailable, at each
build break. **No lead time in this table has been quoted to the programme.** They are the
figures a buyer should assume when planning and must replace with the vendor's written
quotation at PO -- RFQ-EEG-001 Rev E section 10 asks every bidder to state module lead times
at the time of quoting, and that answer supersedes this table.

| Line | Sources | Assumed lead time | Exposure @2 / @10 / @25 / @50 | Mitigation |
|---|---|---|---|---|
| **ADS1299 modules (M1)** | Effectively one: PiEEG. The TI ADS1299IPAG behind it has a documented history of 20+ week lead times. | 4–8 weeks for the module; 20+ weeks if the module vendor is themselves waiting on TI | 4 / 26 / 64 / 126 modules -- **every unit** | Buy the full Phase 2 and Phase 3 module quantity in one purchase order at Phase 2, one lot, and hold it. Qualify a second breakout under ICD-EEG-006 §6 **before** it is needed, not after. Record the TI date code and lot per unit (RFQ §10). A 20-week reorder inside a build is a schedule failure, not a purchasing problem. |
| **ADuM4160 module (M4)** | The device has one manufacturer (Analog Devices) and no approved second source; no module vendor is qualified. | 8–16 weeks for the device; module unknown | 2 / 13 / 32 / 63 -- **every unit** | Not substitutable, so the only mitigations are stock and qualification. Buy Phase 2 and Phase 3 together. Qualify the Olimex USB-ISO now and resolve the USB-B non-conformance -- WH-09 pigtail as the interim -- before the Phase 2 order. Hold two spare modules per ten units: the isolator is also the part most likely to be destroyed by a host-side fault in the field. |
| **ESP32-S3-DevKitC-1-N16R8 (M2)** | One manufacturer, several authorised distributors. Not substitutable (E-18). | 2–6 weeks from an authorised distributor | 2 / 13 / 32 / 63 -- **every unit** | Widely stocked, so the risk is not scarcity but **variant substitution**: an N8R2 or N16R2 board in an N16R8 bag. `esptool flash_id` on 100 % of arrivals, accept only 16 MB flash **and** 8 MB PSRAM (QP-EEG-010 §2.2). Buy only from Mouser, Digi-Key, Farnell, RS or the Espressif official store. Marketplace sellers are PROHIBITED (§7). |
| **DIN 42802 sockets (J15–J17)** | **None qualified.** | unknown; **assume a 12-week first-article lead time** | 6 / 39 / 96 / 189 sockets -- **every unit** | This is the highest-risk line in the file because it has no vendor at all and it is a patient-safety part. Approach the three candidates of §1.4.1 now; a bespoke PCB-mount variant may carry tooling on top of the 12 weeks. The fallback, which needs an ECO, is a panel-mount socket on a flying lead into a 1×3 header, which moves the part off the carrier footprint entirely. |
| **Four-layer bare board** | Six approved fabricators, all quoting a standard process | 5–15 working days standard, 2–3 days on an expedited service | 2 / 13 / 32 / 63 | New at this revision and **not a risk line**: four layers on this stack-up is stock work at every named fabricator. It is listed here only so nobody re-quotes the Rev A two-layer outline by habit. |
| Sintered Ag/AgCl cups and ear clips | Wuhan Greentek preferred; Florida Research Instruments and Spes Medica are approved alternates | 4–6 weeks, plus MOQ (§5) | 20 / 130 / 320 / 630 cups | Sintered, not plated (A-01). Order against the MOQ break, not against the build. |
| Protected 18650 cell assembly | Pack-builder assembly, not a catalogue part | 6–10 weeks including UN 38.3 paperwork | 2 / 13 / 32 / 63 | See §4. The UN 38.3 report is a prerequisite for shipping (S-09), so a late cell delays despatch even if every kit is built. |
| Travel case | One baseline shell and one paper alternate (§4 K21) | 2–4 weeks ex-stock; longer for custom foam | 2 / 10 / 25 / 50 kits | The foam die or laser programme is a one-off; order it once, against the seven CASE-00 Rev C layer files and **after** the first shell has been measured. Five distinct profiles at one thickness, so five dies. |
| OPA4376AIDR, TLV3201AIDBVR | TI single-source, no approved alternate | 8–12 weeks in a constrained market | 6 / 39 / 96 / 189 op-amps | Small parts, low value: buy a full 2500-piece reel of the OPA4376 at Phase 2 and the fleet is covered for the life of the programme. Hold the U7 order until ECO-EEG-023 is drawn, because its surrounding passives change. |
| 47 kΩ 0.1 % 25 ppm thin film | Vishay preferred, two approved alternates | 4–10 weeks | 32 / 208 / 512 / 1008 | **Do not buy the fleet reel yet.** ECO-EEG-024 may raise this line to 68 kΩ because S-02 fails at 47 kΩ, and a 5000-piece reel of the wrong value is the most expensive small mistake available in this BOM. Buy cut tape for Phase 1, decide ECO-EEG-024 on the Phase 1 measurement, then buy one reel of the settled value. |

**The pattern.** At these volumes the money is not in unit price, it is in the four lines --
ADS1299 module, isolator module, DIN socket, cell assembly -- where a single source can stop
the whole build. Every one of them should be bought once, in full, for Phases 2 and 3
together, and held. The passives, the sockets and the semiconductors are cheap enough that
buying a full reel to cover fifty units costs less than the administration of buying twice --
with the one exception of R1-R16, where the value itself is not yet settled.

---

## 4. Mechanical, electrode and kit items

Package v1 named a class where a part was needed. This section names parts. Quantities are per
kit; A-nn and M-nn references are to RFQ-EEG-001 Rev E.

| # | Group | Item | Qty/kit | Manufacturer + part | State | Notes and rule |
|---|---|---|---|---|---|---|
| K1 | Electrodes | Sintered Ag/AgCl cup electrode, 10 mm, on service bayonet, 1.5 m lead, colour-coded (A-01) | 10 (8 fitted + 2 spare) | Wuhan Greentek sintered Ag/AgCl cup electrode lead | PREFERRED | **Sintered, not plated.** Plated cups drift and are PROHIBITED. Approved alternates: Florida Research Instruments, Spes Medica. Class A supplier: CoC per lot, ISO 10993-5 and -10 declarations (S-05). Contact: greentek@gtsensor.com. **The "1.5 m lead" in this line is a catalogue description and is not what the kit needs.** WH-EEG-008 §3.1.1 terminates the cup on a tail of tens of millimetres inside the HM-04 assembly, and a 1.5 m factory lead cut back to 60 mm is a lead whose terminated end has been thrown away. The purchase order must state the **tail length and its termination**, and until WH-EEG-008 §3.1.1 is approved that length is not known -- which is the same open item, WH-EEG-008 item 22. HM-05A is in any case a cup "modified for the service bayonet" (PARTS-EEG-019 §2.1) and the modification has never been drawn. |
| K2 | Electrodes | Ag/AgCl ear-clip reference electrode, DIN 42802 plug | 2 | Wuhan Greentek Ag/AgCl ear clip | PREFERRED | Linked-earlobe reference, REF_L and REF_R. Class A. Two of the **fourteen patient terminations** in a standard build: eight scalp, two ear references, one bias, three EMG. **The touch-proof plug on this electrode had nowhere to plug in.** J15--J17 are the three EMG channels; there is no DIN socket for an ear reference anywhere in the kit, and WH-EEG-008 §3.1 crimped the harness conductor straight onto the clip instead, which SVC-EEG-013 R4 then had to release without a tool at every turnaround. **WH-EEG-008 §3.1.2 resolves it in favour of this line**: the clip is bought exactly as written here and the mating half becomes a free-hanging touch-proof socket on the temple tail, K27 below. That is a proposal, not a decision -- WH-EEG-008 open item 23 -- and this line does not change either way. **Two purchase-order fields added 2026-09-02, and the "does not change either way" above is superseded to that extent.** The part does not change; the order does. **(1) Lead length.** Apply the K1 correction on this line verbatim: the catalogue 1.0–1.5 m is a description, not a requirement, and the order must state **plug-to-jaw 150–200 mm** and the termination. Two things follow and both are stated in WH-EEG-008 §3.1.2.1 provision 2: the total unscreened reference run becomes 250 mm of temple tail plus at most 200 mm of clip lead, **≤ 450 mm**, which is recorded as an extension of DEV-WH-01 from the three EMG channels to REF_L and REF_R; and **T8 (input-referred noise, ≤ 1.0 µV RMS, an RTS-1 release criterion) is re-measured on a built unit carrying the real lead before that extension is accepted**. A short lead is also what lets the clip travel dressed inside the helmet bay, which is the packing rule the whole ear-coupler safety argument rests on. **(2) Plug colour.** Matched to the K27 socket it mates — GY left, PK right — or a printed GY / PK marker sleeve on the clip lead within 25 mm of the plug. **Order this line and K27 on the same purchase order**, so that retention and finger-safety when the pair is mated are one supplier's responsibility. |
| K3 | Electrodes | EMG lead, snap to DIN 42802 touch-proof plug, 1.0 m, three colours | 3 | Wuhan Greentek snap-to-DIN lead | PREFERRED | Colour and site assignment (cheek / submental / laryngeal) fixed in WH-EEG-008. Must mate with whatever socket §1.4.1 approves -- **order the leads and the sockets together, from the same decision.** **K47 is the same class of part at a fourth site** (WH-10, the Fpz bias lead, TQ turquoise, 150 mm) and is bought against these criteria plus a stated length; it mates a K27 socket on the helmet and not a carrier socket, so it does not wait on §1.4.1. |
| K4 | Electrodes | Disposable EMG snap electrode, pre-gelled, pack of 30 (A-02) | 1 pack | Ambu BlueSensor N (N-00-S/25) | PREFERRED | Alternate: Cardinal Health / Kendall H124SG. Consumable, replaced at refurbishment. Check the expiry date at kitting and at each turnaround. **Consumption corrected 2026-09-02: four pads per session, not three.** WH-EEG-008 §3.1.3 puts the Fpz bias electrode on a fourth pad off this pack, on prepped forehead skin below the HM-02A brow pad, one per session. A 30-pack is therefore **seven full sessions with two pads left over**, and IFU-EEG-014 §13.2's "Thirty are supplied, which is ten sessions' worth" is wrong at four pads and is that document's to re-issue. Whether a second pack is kitted is a programme decision and is not made here; the quantity in this row is unchanged until it is. |
| K5 | Consumables | Conductive EEG paste, 100 g | 2 | Weaver and Company **Ten20**, or Greentek GT20 | PREFERRED | Alternate: Nihon Kohden Elefix Z-401CE. |
| K6 | Consumables | Abrasive skin-prep gel, 100 g | 1 | Weaver and Company **NuPrep**, or Greentek GT5 | PREFERRED | -- |
| K7 | Consumables | Consumables pouch (A-05) | 1 set | assorted, CE-marked | APPROVED ALTERNATE, buyer's choice | **The contents are listed once, in PKG-EEG-015 §1.1 group 5**, and are not repeated here. The purchasing rule is the only thing this line adds: the blunt-tip 5 mL syringe with a 1.2 mm cannula is the gel-port tool of DSN-EEG-002 §3 and is not optional, whatever else the pouch is filled with. |
| K8 | Wearables | -- | -- | -- | **WITHDRAWN** | **RFQ A-03's headband is withdrawn as a kit item.** The eight electrodes are fixed to the HM-01 frame at manufacture, so a headband with fixed holders at the same eight sites would duplicate them. What the kit needs and did not have is the **chin strap (HM-06) and the occipital yoke (HM-03)**, both of which are on the frame and are covered by K13 and K14. The packing list drops the headband line and SVC-EEG-013 drops its wash schedule. |
| K9 | Wearables | Closed-back over-ear headphones, 3.5 mm, ≥ 1.2 m cable, **same model in every kit** (A-04) | 1 | Audio-Technica **ATH-M20x** (47 Ω) | PREFERRED | **A-04 is restated as 32 to 64 Ω** and the calibrated output level is measured per model, so the published 47 Ω of the ATH-M20x is inside the requirement and this line is no longer open. **The test load in TST T17 and JIG-EEG-009 becomes 47.0 Ω to match the shipped part**, not the 32.0 Ω of Rev A. Superlux HD-681 (32 Ω) is the approved alternate but a kit fleet must be one model, because the calibrated E-13 level is transferable only then. **RFQ E-29 applies to this line: the headphone output must not exceed 100 dB SPL at any commanded level, measured on an artificial ear, and the firmware clamps the codec volume register to the value measured at calibration. Calculated full-scale output is about 110 dB SPL, which is why the requirement exists and why the model cannot be changed in the field.** |
| K10 | Audio | Boom microphone capsule: electret, omnidirectional, with windscreen | 1 | Primo **EM272Z1** | PREFERRED | Distributor: FEL Communications / Micbooster (UK). **The boom carries the bare capsule and its screen only; the preamplifier is on MP-01 at J21 (ICD-EEG-006 §2.9, §2 M10 above), which reverses what package v1 said.** Alternate: any 6 mm electret with ≥ 60 dB(A) signal-to-noise. |
| K11 | Mechanical | Boom gooseneck, 120 mm, M4 threaded both ends, holds position | 1 | -- | **OPEN WITH CRITERIA** | Must hold the capsule at 3 cm from the mouth corner without creep over a two-hour session, and survive detach/reattach at the temple (E-14). Submit a sample. |
| K12 | Mechanical | **Electrode assembly compression spring: helical, closed and ground both ends, stainless 302, wire 0.50 mm, OD 6.40 / ID 5.40 mm, free length 6.90 mm, rate 1.20 N/mm, 3–6 N across the working stroke** | 10 | -- ; approach Lee Spring, Century Spring, Gutekunst | **OPEN WITH CRITERIA** — now a full specification with no vendor, rather than a description that could not be bought | **Specified on 2026-09-02. It could not be bought before that date, and the reason was geometry and not sourcing.** *Was: "3–6 N at working length, stainless 302", selected against the HM-04 drawing envelope of 12.4 × 12.4 × 18.0 mm in MECH-EEG-020 — which is the envelope of the whole electrode body, not of the seat the spring sits in.* `hm04()` cut that seat Ø6.80 × 4.50 mm deep with its roof at z 13.50, against an HM-05B spigot top at z 12.10: **1.40 mm of free height**, with the seat only 0.10 mm larger than the spigot **on the radius**, so no coil fits around the spigot and the spring must sit **on** the spigot top. A 3–6 N spring does not exist in 1.40 mm, which is why ruling D5-K12-SPRING-ENVELOPE declined to issue an envelope at all. `tools/mech_gen.py hm04()` deepened the seat to 6.60 mm on 2026-09-02 — roof z 15.60, **3.50 mm** of free height — and cut the circumferential bayonet run that gives the carrier a rest position to be measured from. Both blockers are gone, so the envelope is issued. **WH-EEG-008 §3.1.4 carries the specification and every line of the arithmetic; this row is the shopping list and does not restate it.** What a buyer orders: helical compression, **closed and ground both ends** (an unground end lands on a short arc of printed PA12 and triples the bearing stress), **stainless AISI 302 spring temper to ASTM A313**, wire **0.50 mm**, **OD 6.40 mm nominal, 6.50 mm maximum** free and compressed, **ID 5.40 mm minimum**, **2.2 active coils**, **free length 6.90 ± 0.20 mm**, **rate 1.20 N/mm ± 10 %**, **solid height 2.60 mm maximum** (2.10 mm calculated), squareness ≤ 3°. Calculated forces: **3.96 N** at the 3.60 mm rest height, **4.56 N** at the 3.10 mm hard stop, and inside 3–6 N at every installed height from 2.85 to 3.85 mm, which is the ± 0.25 mm the two printed parts stack up to. The rate is deliberately low: at 1.20 N/mm the spring cannot deliver more than 6.7 N even if it were stacked solid, so the force on a scalp is bounded by the spring and not by the assembler. **Stainless only** — the spring is inside the electrode body and is exposed to gel and saline. **316 is neither offered as an alternate nor excluded**: WH-EEG-008 §3.1.4 records the finding that the seat is a chloride crevice under the coil ends that is never immersed, never scrubbed and never fully dried, and the 25-cycle result below decides between 302, 316 and Elgiloy on evidence rather than on argument. **Qualification is the K25 regime and not the cups' bath**: 25 cycles of SVC-EEG-013 R6 (two 10 ml warm-water passes, demineralised rinse, ≤ 1 bar air) plus a 70 % IPA wipe and a conductive-paste dwell. ASM-EEG-007 §4.2 bonds HM-04 into HM-01 and SVC-EEG-013 R5 lists HM-01 as wipe, never immersed, so this spring never sees the 40 kHz bath even though the cup below it does. **Five pieces, measured on a printed HM-04 / HM-05B pair against WH-EEG-008 §3.1.4's ten-row table, before any fleet order**: free length, solid height, rate, force at both working heights, OD and squareness, seating clear of the HM-05C crown, the measured gap between the carrier's mechanical stop and the spring's solid height, **≥ 10 MΩ from the spring to both halves of the contact with H1 unchanged when the spring is removed** — which is the check that the preload member is not the conductor — relaxation and 20× pitting inspection after the 25 cycles, and the bayonet still turning with the HM-09 key under load. **Two things this line still waits on and cannot buy round**: HM-05C's outside diameter, because §3.1.4's no-gold relation requires **≤ 4.65 mm** against the 5.20 mm §3.1.1 proposes, or a 0.15 mm step; and a **capture feature**, because nothing retains the ring today and a lost one is a silent open electrode under a cup that still looks fitted (§10 item 17). Contact force is the one thing the participant cannot adjust and it is the reason the design works. **Class A** — it is in the gel-wetted patient-applied path. |
| K13 | Mechanical | Occipital yoke (HM-03) ratchet dial with POM pawl, 2 mm per click, 52–62 cm | 1 | Hard-hat suspension ratchet -- candidate: MSA Fas-Trac III replacement ratchet | **OPEN WITH CRITERIA** | Bought in, not printed (DSN-EEG-002 §14). Must accept the HM-03 yoke interface, which is not yet defined -- an open mechanical item, not a sourcing one. Now also carries the sizing function that RFQ A-03's headband used to claim. |
| K14 | Mechanical | Chin strap (HM-06) webbing, chin cup and anchors | 1 set | generic 20 mm polyester webbing with a side-release buckle | APPROVED ALTERNATE, buyer's choice | Removable; the liner is a consumable replaced each turnaround. RFQ A-03 is rewritten to cover this line and K13. |
| K15 | Mechanical | TPU comfort pads ×4 and chin-cup liner | 1 set (+4 spare) | printed TPU 85A, or cast | PREFERRED | HM-02. Skin contact: ISO 10993-5 and -10 declarations required (S-05). |
| K16 | Power | Protected 18650 Li-ion cell assembly, ≥ 3000 mAh, with PCM and a tab-welded JST PHR-2 lead | 1 | **Not a catalogue part.** Cell: Panasonic NCR18650B or Samsung INR18650-35E. PCM: a Seiko S-8261-class protection board. Assembly by a pack builder. | **OPEN WITH CRITERIA** | Evidence required **before** first article: UN 38.3 test summary (T.1–T.8) for the cell **and** for the assembled pack; IEC 62133-2:2017 report; safety data sheet; RoHS and REACH declarations; CoC per lot. PCM trip thresholds stated numerically. **RFQ E-23's "no charging above 45 °C" is met only in part: the charger module supplies the thermal-regulation half; the 45 °C inhibit itself is not met and cannot be tested, because nothing reads the cell. RFQ S-04's battery thermistor is NOT met and stays not met, because there is no NTC net in `design.py` and no thermistor way on J12 or J13.** That is an open hardware item against S-04, listed in DSN-EEG-003 §11 and RISK-EEG-011, and it is not solved by anything bought on this line. 100 % goods-in: OCV 3.4–3.9 V, internal resistance, wrap and PCM intact, lot recorded per unit. Class A supplier. |
| K17 | Storage | microSD card, 32 GB, industrial or high-endurance | 1 | SanDisk **SDSDQAF3-032G-I** (Industrial) | PREFERRED | Alternate: Kingston **SDCIT2/32GB**. Consumer cards are PROHIBITED: the card takes a continuous write for three hours per session for the life of the fleet. The frame payload is **50.7 kB/s at 1000 Hz** (1015 bytes every 20 ms); E-20's ≈70 kB/s is an allowance that includes STATUS and SIGNATURE frames and filesystem overhead, and the allowance, not the payload, is what the card is sized against. Full-card write-read verify on the sample at goods-in. |
| K18 | Cables | USB-C to USB-A, 1.0 m, USB 2.0 data-capable, USB-IF certified (A-07) | 1 | StarTech.com or Delock, current catalogue number | APPROVED ALTERNATE, buyer's choice against the criteria | Charge-only cables are PROHIBITED on this line: it is the data path, and one of the two A-07 cables is the host lead into the isolator's panel receptacle. |
| K19 | Cables | USB-C to USB-C, 1.0 m, USB 2.0 data-capable, USB-IF certified (A-07) | 1 | StarTech.com or Delock | APPROVED ALTERNATE | -- |
| K20 | Power | USB charger, ≥ 5 V 2 A, EU CEE 7/16 plug, CE marked, Ecodesign 2019/1782 | 1 | Raspberry Pi 15 W USB-C PSU (EU variant), Delock, or Mean Well GST-class | APPROVED ALTERNATE against the criteria | Class A supplier: it is a mains-connected part in a participant's home. CE Declaration of Conformity on file. The kit draws ≤ 1.1 A through F1, so 2 A is ample. |
| K21 | Case | Hard-shell watertight travel case, IP67 class, pressure-equalisation valve, lockable hasps, internal envelope per **PKG-EEG-015 §3.2**, which is its single home | 1 | Peli **1560**, **unwheeled variant** (published internal 518 × 392 × 229 mm). Nanuk **960** (552 × 358 × 226 mm) is the alternate | **PREFERRED** -- the model is settled, the shell is not yet measured | The 1560 is the baseline **because PKG-EEG-015 §3.2 settles it there**, and this line does not restate the envelope, it points at it. **Measure the first shell received, in the base and in the lid separately, before a single sheet of foam is bought or cut** (PKG-EEG-015 §2.1 and §3.2). Two figures are read and not measured, and both can still sink this shell: Peli publishes one interior depth and does not split base from lid, against a **≥ 185 mm in the base** requirement; and the plan margin is 2 mm on each axis, which is inside the tolerance of a moulded case, so a shell that measures short does not make the foam tight, it makes it scrap. The purchase order must name the **unwheeled** variant -- the case has to sit inside a carton (M-07). Published empty mass about 5.1 kg; the ≤ 4.0 kg target of Rev A is withdrawn in PKG-EEG-015 §3.2, not met here. **No case in the Peli, Nanuk or Explorer ranges reaches 210 mm internal depth below this size class.** M-05's 210 mm depth exists so an assembled helmet can stand upright, which is the point of the design; the cost of that decision is a case much larger in plan than the kit needs, and postage is already the largest line in the fleet budget. The Nanuk 960 clears the depth but is 32 mm short of the 390 mm second axis, so **the CASE-00 Rev C bay layout does not fit it as drawn** and choosing it is a Rev D of the seven cut files: it is an alternate on paper only, which is §10 item 8 and PKG-EEG-015 §9 item 10. |
| K22 | Case | **Seven-layer** closed-cell PE foam insert, CASE-00 **Rev C**: seven loose-laid 25 mm layers, 175 mm of stack, one 516.0 × 390.0 mm sheet per layer, nine bays, die-cut or laser-cut, bay legends as printed tags ART-LBL-04 and not engraved (M-05, M-06) | 1 set of 7 sheets | cut to `mech/CASE-00_foam_layer_1.dxf` through `mech/CASE-00_foam_layer_7.dxf` (CASE-00-01 to CASE-00-07, all **Rev C**) | **PREFERRED** -- the cut is held until the K21 shell is measured | **The two Rev B files `CASE-00_foam_top_layer.dxf` and `CASE-00_foam_bottom_layer.dxf` are withdrawn and deleted from the package. Any quotation held against them is void**: they are two 25 mm sheets on 340 × 250 mm and PKG-EEG-015 §2.4 records that they cannot pack this kit, on footprint and on depth. The pocket schedule lives in PKG-EEG-015 §2.2, which is its single home, and nothing is copied here. The seven files are **not interchangeable** -- a bay is cut in a layer only where the schedule cuts it -- and each names its own layer number in its TEXT layer; layers 5, 6 and 7 are the same cut and are supplied as three files so that a sheet cannot be laid in at the wrong height. The sheet is the case internal footprint minus 2 mm on each axis and **516.0 × 390.0 mm is the published K21 figure, not a measured one**: measure the shell first, then release the cut. The POD-P1 bay is drawn to the enclosure as it now is -- base 163.0 × 143.0 × 58.0 mm external with a 163.0 × 143.0 × 6.0 mm lid, 62.0 mm closed -- at 169 × 149 mm. Phase 3 die tooling is a one-off but it is **five dies, not one**: layers 1, 2, 3, 4 and 5-7 are five distinct profiles at one thickness. Pluck foam is the Phase 1 alternate only. **The calibration certificate travels in the case lid wallet beside the quick-start card**, so no foam layer carries a card pocket -- Rev C deletes both of them. |
| K23 | Case | Laminated quick-start and packing card (A-06, IFU-EEG-014); double-wall outer carton with a return-label pocket (M-07) | 1 each | print; generic double-wall carton | PREFERRED | The case is not the shipping container. The carton carries the UN3481 lithium-battery mark (S-09); the shipping procedure lives in PKG-EEG-015 §7. |
| K24 | Printed parts | MJF nylon print set. **Files released, and the line a bureau is quoted against:** HM-02A brow pad, HM-02B occiput pad ×2, HM-02C crown pad, HM-03A occipital yoke, HM-04 electrode bodies ×10, **HM-05B cup bayonet carriers ×10**, HM-08 battery hatch, HM-09 service key, **HM-10 keyed cell carrier**, **HM-11A/B/C channel cover strips**, **MP-01 module plate (146.0 × 126.0 × 3.0 mm)**, **POD-P1 base (163.0 × 143.0 × 58.0 mm external, 158.0 × 138.0 × 55.5 mm internal), lid (163.0 × 143.0 × 6.0 mm) and POD-P1-04 P-clips**, **WH-ADP-02 room-microphone carrier, WH-ADP-03 and WH-ADP-04 USB-C panel plates**, WH-KEY-01 keying shrouds ×3 forms, FIT-01 coupon. **Files not yet released, and therefore not quotable:** HM-01 frame (STL only, no STEP, OA-1), HM-03B ratchet housing, HM-06A/B chin cup and liner, HM-07A boom temple mount. HM-02 pads and HM-06B liner are TPU 85A, not PA12 | 1 set | MJF PA12 print bureau; TPU 85A for the pads and the liner | PREFERRED | **The enclosure grew with the board at this revision and every earlier POD-P1 and MP-01 dimension in the package is superseded.** The internal stack budget is floor 2.5 + boss 6.0 + carrier 1.6 + standoff 18.0 + plate 3.0 + modules ≤ 18.0 = 49.1 mm against 55.5 mm internal, **margin 6.4 mm**. Print a whole phase in one build (§5). Geometry is governed by `tools/mech_gen.py`, and every released file above is in `mech/stl/` and `mech/step/` with a `mech/MANIFEST.json` entry carrying its SHA-256. **Twelve of the parts named above were listed in the previous issue of this line as having no geometry and could not be quoted; they now have STL, STEP and a MECH-EEG-020 sheet, and they are inside this line for the first time.** The four still unreleased are named rather than omitted, so that a bureau's quotation says which parts it covers. **The printed fixture parts are not in this line and are not kit items**: they are K46, and they are printed once per fixture set rather than once per kit. Nothing has been printed. |
| K25 | Harness | **HM-04A electrode termination contact** -- the fixed half of the joint at each of the eight sites: a sprung leaf anchored in the HM-04 body, bearing axially on K26, tail soldered to the WH-01 conductor | 8 fitted + 2 spare | -- | **OPEN WITH CRITERIA** | **Neither this part nor its anchorage exists.** WH-EEG-008 §3.1.1 is a proposal, not a released design; its open item 22 carries it. Criteria: normal force **≥ 0.5 N** at the crown across the whole 3--6 N spring travel; **gold over nickel on the bearing face, the same finish as K26**, so the junction is gold-to-gold and adds no thermal EMF to a 10 µV measurement; an anchorage in printed PA12 that holds **15 N** (WH-EEG-008 test H6); a solderable tail for 7/0.1 mm; the whole part through a 3.2 × 2.6 mm slot; 25 cycles of 70 % IPA and conductive paste with no change; ISO 10993-5 and -10 declarations if any part of it can be touched (S-05). **Class A supplier** -- it is in the patient-applied path. Sample and a dimensioned drawing before the fleet order. |
| K26 | Harness | **HM-05C cup contact crown** -- the rotating half: an annulus let into the top face of the HM-05B spigot, flush at 12.10 mm, clear of the Ø2.40 mm gel passage, with a tail to the cup | 8 + 2 spare | -- | **OPEN WITH CRITERIA** | Same proposal, same open item. Criteria: outside diameter to suit the Ø6.60 mm spigot; centre clear of Ø2.40 mm; **gold over nickel on the upper face, matching K25**; 0.50 mm nominal thickness; joinable to the K1 cup's tail by solder or weld; **rotation-invariant, because the carrier turns 90° at every service**; and the same IPA, paste and 40 kHz ultrasonic exposure as the cup, because it goes into the bath with it. Class A. **A second constraint on the outside diameter, added 2026-09-02, and it does not close today.** WH-EEG-008 §3.1.4's no-gold relation — (ID minimum − crown OD maximum) / 2 ≥ (seat bore maximum − spring OD minimum) / 2 + 0.05 mm — gives a **crown OD of 4.65 mm or less** against the K12 spring specified there, and WH-EEG-008 §3.1.1 proposes **5.20 mm**, which fails it by 0.55 mm on the diameter: at the extreme of its float in a Ø6.80 seat the coil reaches the gold. The hazard is not a parallel electrical path — a ring seated on PA12 at one end is a dead-end stub — it is **galling of the gold-over-nickel plating under the 90° turn SVC-EEG-013 R4 performs at eight sites every turnaround**. Three ways out and the choice is the **mechanical reviewer's on MECH-EEG-020 sheet 8**, not a purchase specification's: bring the crown to ≤ 4.65 mm; recess its upper face 0.15 mm below the spigot rim, which HM-04A's leaf is sprung to follow; or locate the spring radially to ± 0.10 mm. **This line cannot be dimensioned until one of the three is chosen** (§10 item 17). |
| K27 | Harness | **Helmet-side in-line coupler** -- free-hanging 1.5 mm touch-proof socket to DIN 42802-1, on the temple tails of WH-01 conductors 9 and 10 **and on the halo-front tail of conductor 11** | **3 fitted** *(was 2; the third is the Fpz bias coupler, added 2026-09-02)*, plus 2 spare per 10 kits | -- | **OPEN WITH CRITERIA** | WH-EEG-008 §3.1.2, §3.1.2.1 and §3.1.3, and its open items 23 and 26. **This is the cable form of the part §1.4.1 cannot find as a PCB part**, so it does not carry that line's 12-week first-article risk: Stäubli's LB-I1,5 family and Wuhan Greentek's DIN 42802 range are both catalogued as cable parts. **The exact order code, colour suffix included, is read off the catalogue on the day the order is raised and is not constructed in this file.** Criteria: touch-proof to DIN 42802-1; finger-safe to IEC 60601-1 for a type BF applied part with the plug withdrawn, **demonstrated on the first article with an IEC 61032 test probe B on the unmated socket and recorded in the FAI pack** — a supplier declaration is not this evidence and a 500 V insulation-resistance measurement is not either (WH-EEG-008 test H11); crimp or solder bucket for 7/0.1 mm; ≥ 1 A; mating force stated and repeatable over ≥ 500 cycles; **separation force 5 to 15 N, stated and repeatable** *(new 2026-09-02: high enough that a snag does not part the one net WH-EEG-008 §3.1 itself calls "electrically almost invisible" when it partly fails, low enough for SVC-EEG-013 R4's tool-free release. Every other separable interface in the kit already had a window; this one had none)*; **colours GY, PK and TQ**, each distinct from the three EMG sockets (WH-EEG-008 open item 24); ISO 10993-5 and -10 (S-05). **The 500-cycle criterion depends on a packing rule this file does not own.** With the ear clips travelling mated and captive the couplers see about 100 operator cycles in five years, a 5× margin; if they travel loose the participant adds about 250 more and the margin falls to 1.4×, in which case **this line goes to ≥ 1000 cycles and the mis-mate has to be killed mechanically by gender reversal or keying rather than by a colour** — accepting that a socket-ended ear clip is a bespoke Class A patient-contact electrode and not a Greentek catalogue line. **Class A. Order this line and K2 together, from the same decision**, the way K3 and §1.4.1 have to be ordered together. |
| K28 | Harness | Hook-up wire, **7/0.1 mm tinned copper, PTFE primary, OD 0.70 mm** -- WH-01's eleven signal conductors, WH-03, WH-04, WH-05 and WH-03B | **27.4 m calculated; buy 30 m** | -- | **OPEN WITH CRITERIA** | Construction, colours and ratings: WH-EEG-008 §4. *Calculated from the §3 cut schedule: WH-01 21.64 m + WH-03 0.88 + WH-04 0.76 + WH-05 0.72 + WH-03B 3.40.* Eleven IEC 60757 colours for WH-01 plus the pigtail colours. **A supplier's 28 AWG at 7/0.127 mm (0.0887 mm², 0.194 Ω/m) is the preferred alternate and needs no deviation** -- lower resistance, same OD class. No other substitution without a written deviation, because the OD drives the channel fill of WH-EEG-008 §7. Criteria: ≥ 100 MΩ at 500 V DC (test H4); −20 to +200 °C; resists 70 % IPA and conductive EEG paste; RoHS and REACH. Class C. |
| K29 | Harness | Hook-up wire, **7/0.1 mm tinned copper, PVC primary, OD 0.75 mm** -- WH-02's ten conductors and the eight WH-02T bus tails | **20.7 m calculated; buy 23 m** | -- | **OPEN WITH CRITERIA** | *Calculated: WH-02 18.95 m + the eight tails 1.70 m.* Eight colours with a black tracer, plus GY/BK and BK (WH-EEG-008 §3.2). The tracer is not cosmetic: it is what lets a technician with the crown cover off tell a Cz electrode conductor from a Cz light conductor. Criteria as K28 but −20 to +80 °C. Class C. |
| K30 | Harness | Hook-up wire, **7/0.2 mm tinned copper, PVC, 24 AWG, OD 1.15 mm** -- WH-07's two charge conductors | **0.3 m** | -- | **OPEN WITH CRITERIA** | 24 AWG and not 28, because this pair carries the full charge current and **the conductor must not be the fuse**: F1 is a 1.1 A hold / 2.2 A trip PTC (WH-EEG-008 §3.7). Class C. |
| K31 | Harness | **Aluminium/polyester foil screen tape**, 100 % coverage, applied with 25 % overlap, foil side inward against the drain | **3.93 m of screened cable per kit**; tape bought by the roll | -- | **OPEN WITH CRITERIA** | *Calculated: WH-01 1640 mm + WH-03 220 + WH-04 190 + WH-05 180 + WH-03B 1700.* Width to suit each cable's lay-up circumference. Criteria: the foil face must be the face the drain lies against, or the drain contacts polyester and the screen is open at DC. Class C. |
| K32 | Harness | **30 AWG tinned-copper drain wire**, laid in continuous contact with the foil, running the full length | **3.95 m** | -- | **OPEN WITH CRITERIA** | *Calculated: WH-01 conductor 12 at 1660 mm + WH-03 220 + WH-04 190 + WH-05 180 + WH-03B 1700.* One drain per cable, one contact, **no splice anywhere** (WH-EEG-008 §5.2). Class C. |
| K33 | Harness | **TPU jacket**, extruded or heat-shrink jacketing: 0.55 mm wall to OD 4.3 mm nominal / 4.6 mm maximum for WH-01, 0.50 mm wall to OD 4.5 mm nominal for WH-02, OD ≤ 2.2 mm for WH-03, WH-04, WH-05 and WH-03B | ≈ 5.6 m | -- | **OPEN WITH CRITERIA** | The OD is a controlled characteristic, measured at three points on every cable (WH-EEG-008 §8 step 4), because it sets the channel fill of §7 and the bend radius of §4. **PVC is not acceptable on WH-03B**, which is immersed at every turnaround. Class C. |
| K34 | Harness | **Heat-shrink sleeving**: clear 2:1 for the drain sleeve, adhesive-lined 2:1 for the screen cut-back at the helmet end and for the HM-04 joints | 1 assortment | -- | APPROVED ALTERNATE, buyer's choice against the criteria | WH-EEG-008 §5.2 and §8 steps 5, 6 and 14. Criteria: ≥ 90 °C continuous, halogen-free, and the adhesive-lined grade must wet PTFE-jacketed conductors. Class C. |
| K35 | Harness | **Printable heat-shrink label sleeve**, thermal-transfer printed, 3.2 mm recovered diameter for the jacketed cables and 1.6 mm for the pigtails | **16 labels/kit** | Brady PermaSleeve PS-187-2-WT class | APPROVED ALTERNATE against the criteria | WH-EEG-008 §10: one label at each end of the eight built assemblies, WH-03B included. **Wrap-around adhesive labels are PROHIBITED on this line** -- the whole kit is wiped with 70 % IPA at every refurbishment and adhesive labels curl. The printer is the manufacturer's; the sleeve stock is this line. |
| K36 | Harness | **JST PH mating set for J24**: PHR-2 housing and SPH-002T-P0.5S crimp contacts, with the WC-160 / YC-160R hand tool | 1 housing + 2 contacts; 1 tool per bench | JST **PHR-2** and **SPH-002T-P0.5S** | PREFERRED | §1.4 carried these only as a sentence inside the J13/J24 header row, so nothing on any bill of materials bought them. This is that line. **J13 takes a second PHR-2 on the cell assembly's tab-welded lead**, which the K16 pack builder fits, so the harness buys one and the pack builder one. Board holes 0.90 mm. Class C. |
| K37 | Harness | **3.5 mm 4-conductor panel-mount jack**, threaded M6 × 0.75 barrel for a 6.5 mm panel hole in a wall up to 2.5 mm, solder lugs, with nut | 2 -- WH-ADP-01 and WH-ADP-01B | CUI SJ-435xx or Lumberg KLBR class | **OPEN WITH CRITERIA** | WH-EEG-008 §3.9. Criteria: **the tip / ring 1 / ring 2 / sleeve lug order stated on a drawing**, because it is not common across the class and getting it wrong puts DGND on VOICE_RAW; barrel ≥ 4.5 mm so it passes a 2.5 mm wall and still takes its nut; tolerant of a **printed** 6.5 mm hole, which MJF holds to about ±0.3 mm and which is not a machined panel hole; plug retention ≥ 30 N (test H6). On WH-ADP-01B additionally a **switched insertion-detect contact**; not every jack in this class has one, and if the part bought has none then J27.4 stays a no-connect and WH-EEG-008 §3.4's detect is not implemented. One part number serves both positions, which is why a 4-pole part is used for a stereo output. |
| K38 | Harness | **Panel-mount USB-C 2.0 receptacle**, two-hole flange, solder cups or a short pigtail | 2 -- WH-ADP-03 charge and WH-ADP-04 host | -- | **OPEN WITH CRITERIA** | WH-EEG-008 §3.9. Criteria: flange inside **24.0 × 14.0 × 1.6 mm**, because the printed rim takes any flange up to that and a pocket cut to a guessed flange fits nothing; nose ≥ 2.5 mm proud of the flange, and ≥ 3.3 mm on WH-ADP-04 which has a gasket in front of it; CC cups reachable for the K39 pull-downs once it is seated in the rim; **USB 2.0 only**. **On WH-ADP-03 no data conductor is fitted at all**, and **on WH-ADP-04 every node including the shell and both pull-downs is on the host side of the isolation barrier and may be commoned with nothing** -- that is what test H10 measures at 500 V DC. |
| K39 | Harness | **5.1 kΩ ±1 % resistor** -- the CC pull-downs at both USB-C receptacles, fitted on the adapter at the receptacle's own CC cups, under heat-shrink | 4 | any 5.1 kΩ 1 %, 0603 or leaded | PREFERRED | WH-EEG-008 §3.9. They are not on the carrier and no carrier net reaches them. **The two on WH-ADP-04 return to the host-side 0 V and not to DGND**, which is the one bond the ADuM4160 exists to prevent. Class C. |
| K40 | Harness | **Shielded USB 2.0 cable assembly**, re-terminated into WH-09: 28 AWG data pair, 24 AWG power pair, OD 4.0--4.5 mm, with a moulded USB-B plug at one end | 1 | -- | **OPEN WITH CRITERIA** | WH-EEG-008 §3.8. Criteria: USB-IF conformant construction; a moulded **USB-B** plug, because that is what the named isolator module presents; braid continuous and bondable at both ends of the finished pigtail **and to nothing else**; enough length to finish at 150 mm after re-termination. **This line is the interim answer to the live RFQ E-24 non-conformance of §10 item 2 and is deleted if an isolator with a USB-C host receptacle is qualified.** |
| K41 | Harness | **WH-03B boom lead**, 1700 mm: two 7/0.1 mm PTFE conductors, overall foil and drain, TPU jacket, terminated in a **4-pole 3.5 mm plug with solder buckets and a screwed or crimped strain-relief barrel** | 1 | built from K28, K31, K32 and K33 plus the plug | **OPEN WITH CRITERIA** | The construction is WH-EEG-008 §4, which gains a WH-03B column at this issue; before that this assembly had no cable specification, no AVL line and no BOM row anywhere. Criteria for the plug: **not over-moulded**, so the lead can be built in a harness shop, pull-tested to 30 N (test H6) and repaired at service; four poles; mates K37; and survives 40 kHz ultrasonic immersion at every turnaround, which is what rules out a moulded strain relief with a PVC boot. |
| K42 | Harness | **WH-BUS-01 bare board**: 14.0 × 10.0 × 0.80 mm, **two layers**, ten 1.60 mm pads on 0.80 mm plated holes, ENIG, green mask, white legend both sides, 5 × 4 V-scored panel | 1 per kit; the panel is 20 up | any fabricator meeting `kicad/wh-bus-01/README_layer_map_and_checksums.txt` | **PREFERRED** -- the fabrication data exists; no board has been fabricated | WH-EEG-008 §3.2.1. FR-4, Tg ≥ 150 °C and ENIG as EEG-CAR-01, so **one material qualification covers both boards**. **100 % electrical test to the supplied IPC-D-356A netlist is not optional**: pad 10's isolation is the one property of this board that a visual inspection will not catch. V-scoring 0.80 mm material is at or near the lower limit at several houses and the README states the tab-routed alternative. One panel covers twenty kits, so this is a Phase-2 order, not a per-kit one. |
| K43 | Harness | **Hook-and-loop strap**, 10 mm, for the two 120 mm pod service loops | 2 | generic | APPROVED ALTERNATE, buyer's choice | WH-EEG-008 §6. **A cable tie is not acceptable on this line**: the loop has to be undone by hand at service, which is the whole reason the loop exists. |
| K44 | Harness | **Silicone gasket washer**, 10 mm OD × 0.8 mm, behind the two 3.5 mm jack flanges and in the two WH-ADP-02 recesses | 4 | generic 60 Shore A silicone | APPROVED ALTERNATE | WH-EEG-008 §3.9. The WH-ADP-04 flange gasket is a different profile and is cut to that plate's 0.8 mm deeper rim; it is not this washer. |
| K45 | Harness | **Structural adhesive** for the three WH-KEY-01 shrouds and the three bonded WH-ADP plates | 1 cartridge per build | two-part methacrylate for unprimed PA12: 3M **DP8010NS** blue, or Loctite **AA 3038** | PREFERRED | The same adhesive ASM-EEG-007 §4.2 specifies for the eight HM-04 bonds, so the kit qualifies one adhesive and one surface preparation. Neither product has been tested on this programme's dyed MJF surface. **Test H6 pulls a bonded WH-ADP plate at 50 N and that joint has never been made** -- WH-EEG-008 open item 21. |
| K46 | Fixtures | **MJF print set for the production test fixtures**, seven released solids: FIX-01/E light-tight colorimeter manifold (184.00 × 30.00 × 19.00 mm, 46.08 cm³) and its sliding sensor carrier (30.00 × 27.00 × 9.00 mm, 3.16 cm³), both **dyed black because the inside must not be reflective**; FIX-02/A voice-coupler body (24.00 × 24.00 × 17.95 mm, 5.10 cm³) and its **TPU 85A** sealing lip (24.00 × 23.99 × 4.50 mm, 1.05 cm³); FIX-02/B room-coupler body (28.00 × 28.00 × 18.14 mm, 6.34 cm³) and its **TPU 85A** gasket ring (28.00 × 27.99 × 4.50 mm, 0.97 cm³); FIX-03/A carrier nest (180.00 × 160.00 × 15.50 mm, 199.55 cm³) | **not a kit item** -- one set per fixture set | MJF PA12 print bureau; TPU 85A for the two lips | PREFERRED -- files released, nothing printed | Geometry from `tools/fixture_gen.py`, released in `fixtures/stl/` and `fixtures/step/` and listed with SHA-256 in `fixtures/MANIFEST.json`; identifiers in PARTS-EEG-019 §2.4. **This is a fixture cost and belongs in JIG-EEG-009 §6.1, not in the kit price** -- it is here so that the print bureau quotes one order covering K24 and K46 together, which is where the nesting break of §5 actually comes from. Two things to know before the order: the **two lips are TPU 85A and the five bodies are PA12**, so this is two materials and possibly two builds; and **`FIX-01E_sensor_carrier.stl` is not watertight** as released and must be repaired before it is sent (PARTS-EEG-019 OA-17). |
| K47 | Electrodes | **WH-10 Fpz bias lead** -- 4 mm female snap stud to a 1.5 mm DIN 42802 touch-proof **plug**, **150 mm ± 10 mm**, TQ turquoise | 1, plus 1 spare per 10 kits | Stäubli SLS425-SEK/N class; Wuhan Greentek snap-to-DIN lead approved as an equivalent | **OPEN WITH CRITERIA** | **New on 2026-09-02.** WH-EEG-008 §3.1.3 deletes the "Fpz bias pad, solder tag" as a helmet feature and terminates WH-01 conductor 11 in a TQ touch-proof **socket** of the K27 class at the halo front; this line is the lead that mates it and carries the fourth K4 disposable pad on prepped forehead skin below the HM-02A brow pad, one per session. It is the **same class of part as K3** and is bought against K3's criteria, plus three of its own. **(1) The length is a stated number, not a catalogue description.** K3's reference part is 1.0 m; 150 mm is not a catalogue length and must be on the order, or this line repeats the defect K1 and K2 both carry. **(2) Colour TQ turquoise**, distinct from the three EMG leads (RD / YE / GN) and from the two ear couplers (GY / PK) — WH-EEG-008 open item 24. **(3) It mates a helmet-side K27 socket and not a carrier socket**, so unlike K3 it does not wait on §1.4.1 and does not carry that line's 12-week first-article risk. **Class A** — it is a patient-applied lead carrying the module's driven output. **This line is opened, not approved**: WH-EEG-008 §3.1.3 is a ruling without a signature, the halo-front channel mouth it hangs from does not exist on the released HM-01 STL, and the residual cross-mate — a K2 ear clip or a K3 EMG lead entering the bias socket — has to be accepted in writing by the safety reviewer before a sample is judged (§10 item 18). |

**Why this group exists.** Before this issue, **nothing in the harness could be ordered or
priced.** Kit BOM Rev C carried WH-01 and WH-02 as "custom assembly / reference part: none" and
had no row at all for WH-03, WH-04, WH-05, WH-07 or WH-09; §4's K1 to K24 contained no harness
line of any kind -- no crimp housing, no contact, no crimp tool, no extractor, no JST mating
set, no 3.5 mm panel jack, no USB-C panel receptacle, no CC pull-down, no USB assembly for
WH-09, and none of the four raw materials that WH-EEG-008 §4 calls up. Eight controlled cable
assemblies rested on a bill of materials that bought none of their parts. K25 to K45 and
§1.6.1 are those parts, and K46 does the same for the printed fixture set. **The rows in `EEG_kit_BOM_for_bidders_RevC.xlsx` are still owed** --
that sheet is what a contract manufacturer quotes from, and this document cannot write in it;
it is WH-EEG-008 open item 27.

**Six of these twenty-two lines have no vendor and cannot get one from a catalogue**
*(was five of twenty-one, before K47 was opened on 2026-09-02)*. K25, K26, K27 and K47 depend
on design decisions that WH-EEG-008 §3.1.1, §3.1.2, §3.1.2.1 and §3.1.3 propose or rule and
that nobody has yet signed — and K12, though it is now a full specification rather than a
description, still waits on HM-05C's outside diameter and on a capture feature before a sample
can be judged; K37, K38, K40 and K41 depend on datasheet facts -- a lug order, a flange
envelope, a receptacle nose length, a plug that is not over-moulded -- that the programme has
not had in front of it. Each is **OPEN WITH CRITERIA** with the criteria written out, and the
criteria are what a sample is judged against. That is the honest state of them: an empty order
code gets asked about at the purchase order, and a guessed manufacturer part number gets
bought, fitted and found out at the first article.

**Spares, which the harness has never carried a cost for.** WH-EEG-008 §10 sets the policy:
two spare WH-01 / WH-02 sets and two spare boom assemblies per twenty-five kits, one spare EMG
lead set and one spare WH-09 pigtail per ten kits, on top of the two spare frames. Those spare
sets consume K25 to K45 at their own rate and are added when the fleet order is placed; the
per-kit quantities above are per kit.


---

## 5. Minimum order quantities and the price breaks that matter

Most lines here are cheap enough that the buying decision is set by packaging, not by price.
The table lists only the breaks that change a decision at 2, 10, 25 or 50 units. Quantities
are `ceil(qty per board x boards x 1.05)` against the 2 / 13 / 32 / 63 board plan of §0.

| Line | MOQ | Break that matters | Quantity needed @2 / @13 / @32 / @63 boards | Recommendation |
|---|---|---|---|---|
| 47 kΩ 0.1 % thin film (R1–R16) | cut tape from 1 | Full reel 5000 | 34 / 219 / 538 / 1059 | **Do not buy the reel yet.** ECO-EEG-024 may change this line to 68 kΩ (§1.1, §3). Cut tape for Phase 1; one 5000-piece reel of the settled value at Phase 2, which covers the whole fleet from one lot and satisfies the QP-EEG-010 §2.3 same-lot rule at no extra cost. |
| 10 nF C0G `GCM1885C1H103JA16D` (C1–C16) | cut tape | Full reel 4000 | 34 / 219 / 538 / 1059 | One reel, Phase 2. **Check the `C1` dielectric code on the reel label, not the description on the order acknowledgement.** |
| 100 nF X7R 25 V `GCM188R71E104KA57D` (**21/board**: 18 decoupling + C21/C41/C61) | cut tape | Full reel 4000 | 45 / 287 / 706 / 1390 | One reel covers 180+ boards. Buy the reel. Both lines take the same part; the difference is the tolerance statement required on the CoC for C21/C41/C61. |
| 100 nF 50 V `GCM188R71H104KA57D` (C102, C103) | cut tape | -- | 5 / 28 / 68 / 133 | Cut tape at every phase. Two per board does not justify a reel. |
| 10 µF X5R 16 V (**12/board**: 9 bulk + C20/C40/C60) | cut tape | Full reel 4000 | 26 / 164 / 404 / 794 | One reel. The three AC-coupling positions take the same MPN but a tighter rule (§1.2): do not let a substitution on the bulk line silently reach them. |
| 4.7 kΩ 1 % (R94, R95) | cut tape | -- | 5 / 28 / 68 / 133 | Cut tape. New line at this revision. |
| BAV99 (17/board) | cut tape | Full reel 3000 | 36 / 233 / 572 / 1125 | One reel at Phase 2. |
| OPA4376AIDR | tube or cut tape at Phase 1 | Full reel 2500 | 7 / 41 / 101 / 199 | Cut tape at Phase 1, one reel at Phase 2. Single-source part (§3). |
| Socket strips, all lengths | Samtec sells singly, no MOQ | -- | 25 strips/board | Samtec direct is the sensible route at Phase 1: no MOQ, and the gold specification is on the part number rather than in a note. |
| Male header stock TSW-140-07-G-S | none | -- | 13 / 82 / 202 / 397 strips | Includes the 1.05 attrition; strips are cut and mis-cuts happen. Rev A's figures omitted the attrition. |
| **Sintered Ag/AgCl cups (Greentek)** | **200 pieces** | 200 | 20 / 130 / 320 / 630 | **The MOQ, not the build, sets the order.** At Phase 2 (10 kits, 100 cups) you are below MOQ: either buy 200 and carry 100 into Phase 3, or buy from a distributor at a materially higher unit price. Buying 200 at Phase 2 is the cheaper of the two and de-risks §3. |
| Ear clips, EMG leads (Greentek) | typically 50–100 per line | -- | 4/20/50/100 and 6/30/75/150 | Order on the same purchase order as the cups to reach the vendor's freight and MOQ break once. |
| ADS1299 modules | 1 | vendor-stated volume break | 4 / 26 / 64 / 126 | Buy Phase 2 + Phase 3 in one PO (§3). Ask the vendor in writing for the break at 64 and 126 pieces. |
| Travel case | 1 | vendor-stated, usually 10 or 25 | 2 / 10 / 25 / 50 | RFQ-EEG-001 Rev E section 10 already asks every bidder to state the case supplier's minimum order. |
| Foam insert | 1 | tooling amortisation | 2 / 10 / 25 / 50 | One-off die or laser programme; the per-piece price falls sharply after the first ten. |
| MJF printed parts (K24 set) | 1 | build-chamber nesting | per DSN-EEG-002 §10 | The break is nesting, not quantity: print a whole phase in one build. Ten kits in one chamber is materially cheaper than ten chambers of one. **The POD-P1 and MP-01 volumes grew at this revision, so an earlier nesting quotation is stale.** |
| Protected 18650 assembly | pack builders typically 100 | 100 | 2 / 13 / 32 / 63 | Below MOQ at every phase except the 50-kit upper bound. Expect to pay a setup charge, or buy 100 and hold -- but cells age on the shelf, so hold no more than one phase ahead. |
| Bare boards, **four-layer** | fabricator minimum, usually 5 | 5 / 10 / 25 | 2 / 13 / 32 / 63 | Includes the 25 % spares. At Phase 1 the fabricator minimum will exceed the need; take the spares. The four-layer premium is about **€35 in total at 2 boards and about €3 per board at 50**, so it does not change where the order goes. |

---

## 6. The substitution procedure

This is the mechanism RFQ-EEG-001 Rev E section 10 assumes and package v1 never provided.

### 6.1 Who proposes

Anyone who buys or builds: the manufacturer's purchasing or process engineer, or the
programme's build engineer. A substitution is proposed **before** purchase, never after
receipt. A part fitted without an approved request is a non-conformance under QP-EEG-010 §7,
and the disposition is removal, not concession.

### 6.2 What evidence is required

Form **QF-EEG-006-01**, one page, with:

| # | Evidence | Applies to |
|---|---|---|
| 1 | The line, the preferred part, the proposed alternate, and the reason (cost, lead time, obsolescence) | all |
| 2 | Side-by-side datasheet comparison against **every** affected requirement, cited by number (E-nn, F-nn, A-nn, M-nn, S-nn) | all |
| 3 | The ten qualification steps of ICD-EEG-006 §6, completed on one sample, with measured numbers | purchased modules |
| 4 | Measured leakage from any input pin to any supply at 2.5 V bias, ≤ 10 nA | any part on an electrode net |
| 5 | Measured V_OH ≥ 2.48 V and V_OL ≤ 0.83 V under real load | any module output reaching an ESP32-S3 GPIO |
| 6 | Tolerance, temperature coefficient and dielectric stated, not implied | R1–R16, C1–C16, C20/C40/C60, the envelope thin films |
| 7 | Impact on RISK-EEG-011, stated even when the answer is "none" | all |
| 8 | A full pass of TST-EEG-004 Rev C on one unit built with the alternate | purchased modules, and any change to R1–R16, C1–C16 or D1–D16 |
| 9 | CoC, RoHS and REACH declarations; ISO 10993-5 and -10 declarations for skin-contact items; isolation certificate for the isolator; IPC-A-610 class 2 workmanship declaration for any assembled sub-assembly | Class A lines |

### 6.3 Who approves

| Case | Approver | Countersignature |
|---|---|---|
| Class C commodity (passives, sockets, fasteners, consumables) within the stated alternates | Manufacturer QA manager | none |
| Any new alternate on a Class B line | Programme technical lead | -- |
| Any Class A line: isolator, ADS1299 modules, cell, cups and ear clips, DIN sockets, EU charger | Programme technical lead | **Electrical safety reviewer** -- an external appointment that has **not yet been made**. Until it is, a Class A substitution cannot be approved. |
| Phase 3 builds | Manufacturer's engineer signs QF-EEG-006-01 | Programme countersigns |

Approved substitutions are issued as an **ECO** against the change register **ECO-EEG-016** and
added to this file as a new revision. The individual changes carried by this revision are
ECO-EEG-019 (capacitor dielectrics and part numbers), ECO-EEG-020 (fiducials), ECO-EEG-021
(I²C pull-ups), ECO-EEG-022 (R85), ECO-EEG-023 (ENV_CMP re-referencing, **not yet drawn**),
ECO-EEG-024 (47 kΩ to 68 kΩ, **not yet decided**) and ECO-EEG-027 (C20/C40/C60). The programme
acknowledges a request within **2 working days** and decides within **10 working days** where
the decision needs bench work. A request that arrives without section 6.2 evidence is
returned, not queued.

### 6.4 Parts that are not substitutable at all

| Part | Reason |
|---|---|
| **ESP32-S3-DevKitC-1-N16R8** (M2) | E-18. The J6/J7 pin map, the GPIO35/36/37/45 prohibition, the 22.86 mm row spacing and the whole firmware pin map are written to this exact variant. An N8R2 or N16R2 board is not a smaller version of it. F-06's ring buffer is **6 MB inside the 8 MB PSRAM, which is 126 seconds at 1000 Hz**, and F-06 is relaxed to 90 seconds of ring plus unlimited backfill from the microSD copy (ECO-EEG-025); Rev A's "12 MB ring buffer" was never possible in 8 MB and is withdrawn. On a smaller-PSRAM variant even 90 seconds does not fit. |
| **ADuM4160 device** (M4) | E-24 and S-03. It is the only barrier between a participant's head and a mains-referenced host. There is no second source and no second barrier. |
| **TI ADS1299, eight-channel part** (M1) | E-01. The -4 and -6 variants cannot carry sixteen channels; the daisy-chain, the shared 2.048 MHz clock and the simultaneity of E-01 are properties of this device. The breakout carrying it may change under §6.2; the device may not. |
| **Microchip ATECC608B** (M5) | E-21 and F-04. The device identity, the block signatures of F-08 and the USB serial string all derive from it, and swapping the module after provisioning destroys the identity the browser is bound to. |
| **R1–R16 thin film, 0.1 %, 25 ppm** | E-03 and E-07. Thick film is prohibited: its excess noise and tempco appear directly in the 1.0 µV RMS budget. **The value is 47 kΩ on the Phase 1 prototypes and is not yet settled -- S-02 is not met at 47 kΩ and ECO-EEG-024 proposes 68 kΩ (§1.1).** The construction is fixed; the value is open. |
| **C1–C16, 10 nF C0G `GCM1885C1H103JA16D`** | E-10. X7R is prohibited **on this line**. The sixteen time constants set the 100 Hz flatness and the common-mode match; X7R moves with voltage and temperature and the failure appears at T8 and T9, after the batch is built. Note that C21/C41/C61 **are** X7R by decision (§1.2), so "no X7R" is a rule about C1–C16 and not about the board. |
| **D1–D16, BAV99** | E-07. Pinout locked, pin 3 on the input node. BAT54S is explicitly not approved here: Schottky leakage across the series resistor is a measurable offset. |
| **R90 and R91, 0 Ω** | DSN-EEG-003 Rev C §3.3. They are the single star points. Fit exactly one of each, as a real 0 Ω part. Never bridge with a wire or a solder blob, and never fit a second path. |
| **DIN 42802 touch-proof sockets** (J15–J17) | E-09, S-02. A patient-safety part. No "or equivalent": a sample is approved in writing or it is not bought (§1.4.1). |
| **Protected 18650 cell** (K16) | S-04, S-09. Protection, retention and the UN 38.3 report are requirements, not features -- and S-04's thermistor is not met by any of them. |
| **Sintered Ag/AgCl cups** (K1) | A-01. Sintered, not plated. |

---

## 7. Counterfeit avoidance

Two lines attract counterfeits for the same reason: a part with a long lead time and a high
price, bought in small quantities, is exactly the condition that pulls remarked and cloned
stock into a supply chain.

### 7.1 ADS1299

| # | Rule | Verified by |
|---|---|---|
| 1 | Purchase only from the module vendor directly, or from an authorised Texas Instruments distributor with a documented chain of custody. **No brokers, no open-market purchases, no marketplace sellers.** | The purchase invoice is filed in the device history record. |
| 2 | Photograph the TI package marking of every converter on every module. Record the date code and the lot. | QP-EEG-010 §2.2, 100 % at Phases 1 and 2. RFQ §10 already requires date code and lot per unit; this is how. |
| 3 | Reject any package with a sanded or re-blacked top, an inconsistent or off-axis laser mark, a mismatched pin-1 dimple, or a date code newer than the module's own build date. | Goods-in visual at ×10. |
| 4 | Bench power-up and read the ADS1299 ID register before the module is fitted. Measure the on-module AVDD and AVSS. | Reject on an ID mismatch or rails outside +2.50/−2.50 V ±5 %. |
| 5 | X-ray of the **converter packages** for Phase 1 units. This is a different check from RFQ §9.1 item 2's X-ray of the **module connectors**, and neither is a numbered step in TST-EEG-004 Rev C. Extending either to the whole fleet, or justifying a sampling plan, is an **open item** in QP-EEG-010 §14. | -- |
| 6 | Treat a **T7 gain outlier or a T8 noise outlier as a counterfeit indicator.** Quarantine the unit; do not rework it and do not re-test it into a pass. | TST-EEG-004 Rev C; NCR under QP-EEG-010 §7. |
| 7 | Price sanity: a module offered materially below the cost of the TI device inside it is a red flag, and the buyer records the query and the vendor's answer. | Purchase file. |

### 7.2 ESP32-S3-DevKitC-1-N16R8

| # | Rule | Verified by |
|---|---|---|
| 1 | Buy from Mouser, Digi-Key, Farnell, RS Components or the Espressif official store. **AliExpress, Amazon Marketplace, eBay and Taobao are PROHIBITED sources for this line**, whatever the price. | Purchase invoice in the DHR. |
| 2 | The failure mode here is not a fake chip, it is a **mislabelled variant**. Run `esptool flash_id` on **100 %** of arrivals and accept only 16 MB flash **and** 8 MB PSRAM. | QP-EEG-010 §2.2. Reject the whole lot on any mismatch and raise a supplier NCR. |
| 3 | Confirm the module fitted is an ESP32-S3-WROOM-1 with the correct N16R8 marking and an intact Espressif label; photograph the shield marking and the label. | Goods-in visual. |
| 4 | Reject boards with re-soldered or reworked shields, missing or duplicated label serials, or a silkscreen revision that does not match the ordered variant. | Goods-in visual. |
| 5 | Record the module label serial or lot per unit alongside the ATECC608B serial and the unit serial number, which is formatted **`TIOV-B-nnnn`**. | DHR, QP-EEG-010 §10. |
| 6 | A DevKit that fails re-enumeration within 2 s (F-05) at first test, or whose PSRAM fails a full write-read, is quarantined as a suspect part, not swapped silently. | TST-EEG-004 Rev C. |

Note for the buyer, because it changes nothing about the order but everything about what the
line is for: end-of-line flashing goes through the **DevKitC-1's own UART USB-C port**, which
carries the auto-reset circuit on the DevKit itself and is reachable through the MP-01 opening.
The carrier's J26 is a 1×6 console and recovery header and **cannot** enter download mode,
because GPIO0 is LED_SR_LATCH. No JTAG connector is fitted and none is bought.

The same posture applies in weaker form to the ATECC608B and the ADuM4160: buy from the
breakout vendor or an authorised distributor, photograph the marking, and for the isolator
insist on the isolation certificate before the lot is accepted.

---

## 8. Purchase-order checklist

Run this before every purchase order. One tick per line, signed by the buyer, filed with the
order.

| # | Check | |
|---|---|---|
| 1 | The BOM revision on the order is **AVL-EEG-017 Rev B** and the board revision is **EEG-CAR-01 Rev B**. | ☐ |
| 2 | Every line is quoted by **manufacturer part number**, not by description or by distributor code alone. | ☐ |
| 3 | Every distributor code has been re-checked against the MPN in the live catalogue **today**. | ☐ |
| 4 | Lifecycle status re-checked. Any line not **Active** has written programme approval attached. | ☐ |
| 5 | No line reads "equivalent", "generic", "or similar" or "Chinese equivalent". Every OPEN WITH CRITERIA line has an approved sample on file. | ☐ |
| 6 | The four **non-substitutable** module lines are ordered as specified: ESP32-S3-DevKitC-1-**N16R8**, ADuM4160 isolator module, TI ADS1299 eight-channel modules, ATECC608B breakout. | ☐ |
| 7 | Socket strips are the **gold** part number, not the tin one, for every one of the 25 strips. | ☐ |
| 8 | C1–C16 are ordered as **`GCM1885C1H103JA16D`, C0G**, and the order does not contain the word X7R against that line. **This check applies to C1–C16 only: C21/C41/C61 are X7R by decision and must carry a stated ±15 % over-temperature tolerance on the CoC.** | ☐ |
| 9 | R1–R16 are **thin film, 0.1 %, 25 ppm/K**. **The value on the order matches the current ECO-EEG-024 position, and no fleet reel has been bought while that ECO is open.** | ☐ |
| 10 | D1–D16 are **BAV99**. No BAT54S appears against those designators. | ☐ |
| 11 | The bare board is ordered as **150.0 × 130.0 mm, four layers, 35 µm outer / 17 µm inner copper, through vias only at 0.60 / 0.30 mm**. No quotation held against the Rev A two-layer 130 × 124 mm outline is used. | ☐ |
| 12 | **R85 is 150 kΩ** and **R94/R95 (4.7 kΩ) are on the order**; the three fiducials are on the fabrication drawing. | ☐ |
| 13 | **C20/C40/C60 are 10 µF**, not 1 µF, and the tolerance letter has been checked (§1.2). | ☐ |
| 14 | Quantities include the attrition and the spare-board allowance of §0 for the phase being built. | ☐ |
| 15 | **Certificates of conformity** requested per lot for every Class A and Class B line (QP-EEG-010 §11.1). | ☐ |
| 16 | **Change notification** clause on the order for every Class A line: 90 days' written notice before any board revision, process change or site move. | ☐ |
| 17 | Cell order carries the **UN 38.3** summary, IEC 62133-2 report and SDS as deliverables, for the cell **and** the assembled pack. | ☐ |
| 18 | Skin-contact items carry **ISO 10993-5 and -10** declarations (S-05). | ☐ |
| 19 | The ADS1299 and ESP32 lines are ordered from an **authorised source** per §7, and the invoice will be filed in the DHR. | ☐ |
| 20 | Module lead times are **stated in writing** on the acknowledgement, and the long-lead lines of §3 are ordered for Phases 2 and 3 together. | ☐ |
| 21 | **ESD packaging** specified for bare boards, ADS1299 modules and the OPA4376 line (QP-EEG-010 §6). | ☐ |
| 22 | MSL parts arrive in **sealed dry-pack with an indicator card**; the seal date is recorded at goods-in. | ☐ |
| 23 | Delivery address, Incoterms, HS code and country of origin stated (PKG-EEG-015). | ☐ |
| 24 | Every line has an **IQC route**: the QP-EEG-010 §2 row that will accept or reject it is identified. | ☐ |
| 25 | **The travel case is the unwheeled Peli 1560 (K21), and no foam order is placed against the CASE-00 Rev C files until the first shell has been measured in the base and in the lid** (PKG-EEG-015 §2.1, §3.2). | ☐ |
| 26 | **K2, K27 and K47 are on one purchase order**, and K2 carries a stated plug-to-jaw lead length of 150–200 mm, a stated termination and a plug colour; K47 carries a stated 150 mm length and TQ colour. No line reads "1.5 m lead" or "1.0 m". | ☐ |
| 27 | **No spring is ordered against K12 beyond five sample pieces**, and no sample is judged before HM-05C's outside diameter is settled against WH-EEG-008 §3.1.4's no-gold relation. | ☐ |
| 28 | Buyer's name, date and signature. | ☐ |

---

## 9. Supplier identity register, and three corrections to the record

QP-EEG-010 §1.2 records that three corrections to the manufacturer contact list were logged as
complete in DSN-EEG-003 Rev A.2 and never applied to the file. They are applied here, and this
file is now the single source for supplier identity and certification status.

| # | Was recorded as | Correct entry |
|---|---|---|
| 1 | Regulus Electronics (New Taipei, Taiwan) -- "ISO 13485 capable" | Regulus Electronics holds **ISO 9001**. It does **not** hold ISO 13485. The claim is withdrawn from every programme document. |
| 2 | RayPCB / RayMing PCB & Assembly (sales@raypcb.com) | The intended contact is **PCBSync**, **stan@pcbsync.com**. |
| 3 | NextPCB (support@nextpcb.com), listed twice | Dropped from the bidder mailing. Both entries removed. |

**No certification claim about any supplier is to be restated in a programme document without
a copy of the certificate on file.** This applies to every "ISO 13485" annotation carried
forward from the v1 contact list: none of them has been verified by the programme, and
QP-EEG-010 §1.2 explains why ISO 13485 is not asked for in any case.

Supplier classes are defined in QP-EEG-010 §11.1 and are repeated here only as the buying
rule: **Class A** -- ADuM4160 module, ADS1299 modules, protected cell, sintered cups and ear
clips, DIN 42802 sockets, EU charger: named vendor, controlled revision, drawing or schematic,
CoC per lot, 90-day change notification. **Class B** -- the remaining module types, the print
bureau, the case and foam, the headphones: CoC per lot, change notification, part number
pinned. **Class C** -- passives, socket strips, fasteners, consumables: CoC, and traceable lot
codes for R1–R16, C1–C16 and D1–D16.

---

## 10. What this document does not settle

Stated as plainly as the rest.

| # | Open item | Consequence | Gate |
|---|---|---|---|
| 1 | **No qualified vendor for the DIN 42802 PCB sockets.** The part named in `design.py` is a class of cable and panel parts and does not fit the carrier footprint. | J15–J17 cannot be bought. Every unit is affected, at an assumed 12-week first-article lead time. | §1.4.1 sample approval, before the Phase 1 order |
| 2 | **No qualified isolator module**, and the leading candidate presents USB-B where E-24 asks for USB-C. The interim answer is the WH-09 USB-B-to-USB-C panel pigtail; it is not a resolution. | Blocks the Phase 2 order and the safety case. | Qualification under ICD-EEG-006 §6, plus a USB-C isolator module or an ECO |
| 3 | **No room-microphone module is known to meet the hardware-mute requirement** of E-15, and WH-EEG-008's WH-ADP-02 fallback has no drawing and no part number. | E-15 unmet, or a programme-designed sub-assembly appears in the BOM. | Sample submission, or a new drawing |
| 4 | **The boom preamplifier is not chosen.** The MAX9814 is not approved because its AGC contradicts E-14; the MAX4466-class route is preferred but unmeasured. | Blocks E-16's reference-tone calibration. | §6 step 4 measurement on a purchased sample |
| 5 | **R1–R16 value is open.** S-02's single-fault DC leakage is 53.2 µA against a 50 µA limit at 47 kΩ, so **S-02 is not met**; ECO-EEG-024 proposes 68 kΩ, which also widens E-10 to ±1.0 dB. | No fleet reel can be bought, and E-10's limit moves with the decision. | Phase 1 measurement, then the safety reviewer |
| 6 | **ECO-EEG-023 is ruled but not drawn.** U7's supply and input reference change, and `design.py` still wires U7 to AVDD and AVSS. | Two or three passive lines will appear in §1.3 and cannot be ordered yet. | Schematic change, then safety and layout review |
| 7 | **RFQ S-04's battery thermistor is not met and stays not met.** There is no NTC net in `design.py` and no thermistor way on J12 or J13. E-23's thermal-regulation half is met on the charger module; its 45 °C inhibit is not met and cannot be tested, for the same missing hardware. | An open hardware item, not a purchasing one, but it must not be described as met on any CoC or in any compliance table. | DSN-EEG-003 §11, RISK-EEG-011 |
| 8 | **Travel case depth, and a single source.** No case below the Peli 1560 / Nanuk 960 class reaches M-05's 210 mm internal depth. The 1560 is settled as the baseline in PKG-EEG-015 §3.2, but the Nanuk 960 is 32 mm short of the second plan axis, so the CASE-00 Rev C layout does not fit it and the programme is on one shell with no drawn alternate. Its base-to-lid depth split is not published. | A materially larger and more expensive case, higher postage on every leg, and no second source until a second shell is laid out. | Measure the first shell, base and lid separately, **before any foam is cut**; then a programme decision on the alternate |
| 9 | **The cell assembly is not a catalogue part** and its UN 38.3 evidence for the assembled pack does not exist yet. | Blocks despatch under S-09 even if the kits are built. | Pack builder's first article |
| 10 | **No electrical safety reviewer has been appointed.** | No Class A substitution can be approved, and no unit may be used on a person. | DESIGN_FACTS §8 item 1 |
| 11 | **No lead time, price or lifecycle status in this file has been quoted or verified by the programme**, including the four-layer premium of §1.5. | Every figure in §3 and §5 is a planning assumption. | The bidders' answers to RFQ-EEG-001 Rev E section 10 |
| 12 | **The layout has not been reviewed by a human layout engineer.** It now passes the programme's own DRC -- `kicad/EEG-CAR-01_RevB_DRC_report.txt` records zero violations, all 145 nets connected and both inner planes continuous -- but it was produced by the programme's own tools, and it closes at minimum geometry: **169 connections were relaxed**, 36 below the 0.25 mm preferred width and 133 at full width with a reduced gap, all at or above the 0.20 mm minimum. The routing statistics quoted in §1.5 are taken from that report. | The data is **released for review, not for fabrication**: quoting against the §1.5 bare-board line is not blocked, and a bare-board order waits on the review. The safety case is separately blocked by item 10. | RFQ-EEG-002A: a human layout review and sign-off |
| 13 | **The two halves of the HM-04 electrode termination, K25 and K26, are not a sourcing problem yet -- they are a design decision nobody has taken.** WH-EEG-008 §3.1.1 specifies the joint as a proposal: an annular crown on the HM-05B spigot and a sprung leaf anchored in HM-04, so that the bayonet is the disconnect. Until a mechanical reviewer accepts it, HM-04 and HM-05B gain the features it needs, and a safety reviewer signs the patient-applied path, no sample can be judged and no order can be raised. | **The site end of both helmet cables cannot be built.** Twenty-four joints per helmet -- eight electrode conductors and sixteen contact-light LED leads -- have no terminal, no method and no wire entry. | The mechanical reviewer on MECH-EEG-020 sheet 8, then the safety reviewer, then a sample against the K25 and K26 criteria. **Narrowed 2026-09-02**: two of the features that row waits on are cut in `tools/mech_gen.py` — the circumferential bayonet run (measured at 0.000 mm³ of interference through the quarter turn and the 0.40 mm of travel) and the LED seat, now an outboard pocket separated from the conductor run by 1.60 mm of PA12, which is RISK-EEG-011 SF-9 designed out rather than argued away. HM-04A, HM-05C, the 15 N anchorage, the dressed exit and the LED's two lead passages are still owed |
| 14 | **The ear-reference coupler, K27, waits on the same kind of decision.** WH-EEG-008 §3.1.2 proposes a free-hanging touch-proof socket on the temple tail, which is the only reading that satisfies K2's leaded electrode, SVC-EEG-013 R4's tool-free release and IEC 60601-1's touch-proof expectation at once. **Ruled on 2026-09-02 and still unsigned** (WH-EEG-008 §3.1.2.1): the coupler and the clip do not change, and what is added is a 5–15 N separation window, the first-article probe-B check, a stated K2 lead length with T8 re-measured, and a **packing rule** — the clips travel mated and captive — that this file does not own and that K27's 500-cycle criterion depends on. | Two of the fourteen patient terminations cannot be built, and if the packing rule is refused the cycle criterion doubles and the mis-mate has to be designed out mechanically. | The safety reviewer on the interface, **the programme lead on the packing rule across PKG-EEG-015, IFU-EEG-014, SVC-EEG-013 and RISK-EEG-011**, then a sample against the K27 criteria; ordered on the same purchase order as K2 |
| 15 | **Four purchased harness lines are open on datasheet facts, not on availability**: K37's lug order and detect contact, K38's flange envelope and nose length, K40's USB-B plug and braid, K41's non-moulded 3.5 mm plug. All four are in current catalogues; none has been read by the programme. | Each becomes buildable the moment one drawing is obtained. Getting K37's lug order wrong puts DGND on VOICE_RAW. | Obtain the four drawings before the Phase 1 order; §6.2 evidence line 1 |
| 16 | **The 4.20 mm Harwin M20 housing width and the 4.00 mm contact protrusion that §1.6.1 selects against are still UNCONFIRMED**, and `tools/mech_gen.py` says so in its own source. WH-KEY-01 is printed to them. | A shroud printed before the housing is measured either will not take the cable or will not key it. | IQC on the first Harwin delivery, recorded back into §1.6.1; WH-EEG-008 open item 11 |
| 17 | **K12 is now a specification and still cannot be sampled, for two reasons that are not about springs.** HM-05C has no outside diameter, and WH-EEG-008 §3.1.4's no-gold relation needs one: at the 5.20 mm §3.1.1 proposes the coil reaches the gold at the extreme of its float and galls the plating under the 90° service turn, and the relation wants ≤ 4.65 mm or a 0.15 mm step. And nothing retains the spring — there is no capture feature, no ASM fitting step and no SVC handling step anywhere in the package. | A sample cannot be judged against criterion 6 of the ten measurements, and a lost or mis-seated ring is a silent open electrode under a cup that still looks fitted. | The mechanical reviewer on MECH-EEG-020 sheet 8 for the crown dimension and the capture feature; the safety reviewer on a stainless preload member inside a gel-flushed volume; then five samples measured on a printed HM-04 / HM-05B pair |
| 18 | **K47 and the third K27 unit are opened on a ruling that has no signature.** WH-EEG-008 §3.1.3 deletes the Fpz bias pad as a helmet feature and terminates conductor 11 in a TQ touch-proof socket mated by the new WH-10 lead. Three things have to happen before a sample means anything: the safety reviewer accepts the residual cross-mate in writing (a K2 clip or a K3 lead will enter the bias socket, putting an electrode on the module's driven output), the mechanical reviewer adds a halo-front channel mouth and a dressed exit to an HM-01 that exists as an STL with no parametric source (OA-1), and the free tail length F is fixed at a fitting trial. | The fourteenth patient termination cannot be built, and IFU-EEG-014 §13.2 is wrong in four places until it is re-issued at four pads per session. | The safety reviewer, then the mechanical reviewer with WH-EEG-008 open items 26, 30 and 31, then PARTS-EEG-019 and ECO-EEG-016 to issue WH-10 |

Settled since Rev A, and no longer open items: the headphone impedance (A-04 restated as 32 to
64 Ω, the ATH-M20x kept, the test load moved to 47.0 Ω) and the location of the boom
preamplifier (MP-01 at J21).

---

## 11. Verification and sign-off

| What | How verified | Who signs |
|---|---|---|
| Every carrier line matches `tools/design.py` | Regenerate the grouped sub-BOM from `design.py` and diff against §1 | Programme build engineer |
| Every purchase order matches this revision | §8 checklist, filed with the order | Buyer, and manufacturer QA manager |
| Received material matches this AVL | QP-EEG-010 §2 incoming inspection; no lot enters SMT until its IQC record is closed | Manufacturer QA manager; programme quality lead countersigns the Phase 1 pack |
| A substitution is approved before it is bought | QF-EEG-006-01, ICD-EEG-006 §6, and an ECO under ECO-EEG-016 | Programme technical lead; safety reviewer for Class A |
| This document stays current | Reissued at any ECO that changes a part; lifecycle re-checked at every PO | Programme technical lead |

**Audit findings closed by this document:** `carrier-bom-avl-mpn`, `approved-alternates-matrix`,
`module-male-headers-missing`, `supplier-quality-and-avl`. **Findings stated but not closed:**
`specsheet-file-contradictions` (the DIN socket, §1.4.1 and §10 item 1) and
`cell-qualification-evidence` (§4 K16 and §10 item 9), both of which need a vendor before they
can be closed.

**Nothing in this package has been manufactured or measured, and no safety engineer has
reviewed this design.** No vendor named here has yet supplied a part to the programme, no price
or lead time has been quoted, and every figure marked *calculated* is exactly that.
