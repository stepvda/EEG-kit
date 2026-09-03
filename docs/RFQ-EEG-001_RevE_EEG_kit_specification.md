# Request for Quotation and Engineering Specification

Sixteen-channel research EEG instrument with co-registered audio, EMG and response channels,
streamed over an isolated USB link to a browser-based session runner.

**Document:** RFQ-EEG-001 **Revision:** E (routed four-layer production package) **Date:** 1 September 2026
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** all design files CC BY-SA 4.0; firmware MIT
**Governing document:** DSN-EEG-003 Rev C. Where this document and DSN-EEG-003 differ,
DSN-EEG-003 governs. Where a number appears here and in `tools/design.py`, `design.py` governs.

**Revision note (Rev E).** Corrected to the carrier as it was actually laid out -- 150.0 × 130.0 mm
on four layers, in the enlarged POD-P1 enclosure -- and to the rulings of the cross-document audit
of 2026-09-01: E-04 restated to −80 dB, E-10 stated as ±0.5 dB with the fitted 47 kΩ and ±1.0 dB only if the
S-02 fix is taken, E-11 to ≤ 2 Hz,
F-06 to 90 s, A-03 rewritten for the chin strap and yoke, A-04 to 32 to 64 Ω, E-23's 45 °C charge
inhibit restored, E-26's button geometry restated, E-28's 2×5 header withdrawn, E-29 (maximum
acoustic output) added, and S-02, S-04, E-23 and E-27 stated plainly as not met where they are not
met.

**Corrections within Rev E (2026-09-01).** The findings of the second cross-document audit that
name this document were closed without a further revision letter: the DevKit regulator fallback
is an ECO against Rev C of the board, E-10 states the 47 kΩ and the 68 kΩ case together
everywhere, E-23 is stated as met in part, the routing result of that date and the **not
released for fabrication** status it carried replaced every claim that the board was DRC-clean
-- both are superseded by the fourth-audit paragraph below -- the ECO numbering is
restated against RUL-EEG-021 section B, and the unreconciled board-current figures are raised as
an open item. The rulings themselves are the controlled document **RUL-EEG-021 Rev A**.

**Further corrections within Rev E (2026-09-01, third audit).** Still without a revision letter: **E-11 is stated as met in part**, because the ±15 % X7R capacitors the design actually fits move the envelope corner outside the ±10 % the requirement asks for, and the note claiming that TST-EEG-004 already allowed for that is withdrawn -- the band TST-EEG-004 T12e sets is 42 to 58 Hz, measured per unit, and it is wider than E-11; **M-05 names the Peli 1560 as the settled baseline shell** on PKG-EEG-015 section 3.2's reconciled figures, so the "the shell is not selected" of the previous issue and the two disagreeing transcriptions behind it are withdrawn; and **section 12 item 14 is restated from ICD-EEG-006 section 2.7's tally** rather than from the superseded per-rail figures. Section 12 item 15 is new and carries the E-11 band.

**Fourth correction within Rev E (2026-09-02).** Still without a revision letter: **EEG-CAR-01
Rev B now closes.** `kicad/EEG-CAR-01_RevB_DRC_report.txt` reports 145 of 145 nets fully
connected, no unclosed net, no net without copper and **zero DRC violations**, and the two
electrode-clearance vias at 0.328 mm are gone with the rest. The twenty-five open items are
withdrawn wherever this document counted them, and the **not released for fabrication** status is
replaced by the status the programme actually decided: **released for review under RFQ-EEG-002A,
with fabrication release awaiting that review.** Nothing else moves. Nothing in this package has
been manufactured or measured, no human layout engineer has read the routing, and 169 of its
connections were relaxed to close. *This paragraph ended, at first issue, "and S-02, S-04, E-23 and
E-27 are exactly as not met as they were". **That sentence is superseded on 2026-09-02** by the
fifth correction below: S-02 and E-27 are met, E-11 is met in both halves, and S-04 and E-23's
45 °C-inhibit half are the two that are still not.*

**Fifth correction within Rev E (2026-09-02, after the design changes of that afternoon).** Still
without a revision letter, and this one moves requirement rows rather than status wording. **S-02
is met.** ECO-EEG-024 is applied in `tools/design.py`: R1--R16 are **68 kΩ**, not 47 kΩ, so the
single-fault DC current is 36.8 µA on the bare-resistor bound and 30.0 µA on the measuring-device
bound against the 50 µA limit, where 47 kΩ gave 53.2 µA and overshot by 6.4 %. E-10 moves onto the
**±1.0 dB** branch it already states for exactly this case, and TST-EEG-004 T22 grades against it.
**E-27 is met**: the bicolour phase driver is written. **E-11 is met in both halves**: the
Sallen-Key moved from X7R to C0G. **The firmware is built**, under ESP-IDF v5.2.5 for esp32s3, and
has been **run once under QEMU** -- and never on hardware. Section 12 is reconciled against all of
it: items 2, 4, 12 and 15 are closed or restated with the date they moved, and items 1, 3, 5 to 11,
13 and 14 are untouched and still open. **What has not changed is the important part**: nothing in
this package has been built, assembled or measured; no human layout engineer has read the routing;
no safety engineer has reviewed the design; and RISK-EEG-011 SR-01 stays **open** for the safety
reviewer's written disposition, because applying the fix an analysis recommends is not the same as
having the reviewer who owns the finding sign it off.

**Scope:** review and sign-off of the supplied carrier routing (RFQ-EEG-002A), then prototype
builds and complete field kits in three phases (RFQ-EEG-002B) -- 2 prototype units, 10 kits,
then 10 to 40 further kits (25 to 50 in total).

---

## Status of this document

This document specifies an instrument that **has not been built**. Nothing in this package has
been manufactured or measured; every figure marked *calculated* is exactly that. **No safety
engineer has reviewed this design.** Passing every test in section 9 does not, by itself, make a
unit fit to wear; the electrical safety review of section 9.2 is what releases Phase 2.

**The fabrication data is RELEASED FOR REVIEW under RFQ-EEG-002A. Fabrication release awaits
that review.** EEG-CAR-01 Rev B is routed and poured on four layers, and
`kicad/EEG-CAR-01_RevB_DRC_report.txt` reports **145 of 145 nets fully connected, no unclosed
net, no net without copper and zero DRC violations** -- in the report's own words, "the board
passes every rule listed above". ECO-EEG-016 section 3 sets the gate for releasing fabrication
data as zero violations, every net one connected copper island, and both inner planes continuous
under the analogue zone; **all three are now met**. What has not happened is the review. The
routing was produced by the programme's own tools, **no human layout engineer has looked at it**,
and 169 of its connections were relaxed to close, so the board closes at minimum geometry in
places (see the routed-result note below). RFQ-EEG-002A is that review, and it is what releases
the data for fabrication. Boards are not ordered against this issue.

Every requirement below is labelled Mandatory (M), Should (S) or Optional (O). Bidders are asked to
state compliance against each M and S requirement and to price O items separately. Where a
requirement is **not met by the design as it stands**, this document says so in the same sentence
as the requirement rather than in an annex.

**What changed in Revision D.** Rev C asked a bidder to route the carrier board. The board is
now routed and poured, and the complete fabrication package -- Gerber X2, both
Excellon drill files, an IPC-D-356A netlist, BOM with manufacturer part numbers, separate SMT
and through-hole pick-and-place files, fabrication and assembly drawings, and an eight-sheet
schematic -- is in the package. RFQ-EEG-002A is therefore re-scoped from *route this board* to
**review this routing and sign the result off**. Regenerating the board from a single machine-readable
source also found fourteen defects in Rev C's design basis, four of which made the board
unbuildable. They are listed in DSN-EEG-003 Rev C section 9 and each is logged in ECO-EEG-016.

**What changed in Revision E.** Two things changed during layout, and both are engineering
findings rather than preferences.

**The carrier grew from 130 × 124 mm to 150.0 × 130.0 mm.** Thirty connectors, 211 reference
designators and 156 nets would not close at the smaller size. At these quantities the extra 33.8 cm²
of bare board costs a few euro per unit against a real risk of an unroutable design.

**The carrier went from two layers to four.** Package v1's architecture argument was that a
two-layer carrier is cheap and easy to route. Actually laying it out showed that it is not: on two
layers the bottom side has to be both the reference plane and the second routing surface, and it
cannot be both. Four layers -- **L1 signal, L2 reference plane, L3 reference plane, L4 signal** --
give two full routing surfaces and a continuous reference under every analogue trace, which is what
DSN-EEG-003 Rev C section 3.3 asks for and which a swiss-cheesed two-layer pour cannot deliver. The
reference planes carry **AGND_REF left of x = 62 mm and DGND right of it, on both L2 and L3**, tied
together by stitching vias. Vias are **through vias only**, 0.60 mm pad on a 0.30 mm finished hole;
no blind, buried, back-drilled, filled or plugged vias are used. The stack-up is mask / 35 µm L1 /
prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask = **1.60 mm
± 10 %**. At 2 units the fourth and third layers cost about €35 in total; at 50 units about €3 per
board. That is the right trade for a sixteen-channel EEG front end, and section 10 now carries a
four-layer fabrication line.

**The routed result, from `kicad/EEG-CAR-01_RevB_DRC_report.txt`.** EEG-CAR-01 Rev B is routed on
four layers, 150.0 × 130.0 mm, with **3 745 track segments and 552 through vias**. **All 145 nets
are fully connected**; none is unclosed and none is without copper; and each inner plane is **one
continuous copper island per net** on both In1.Cu and In2.Cu. Every geometric rule in the report
passes: the smallest measured clearance is 0.260 mm on F.Cu, 0.275 mm on B.Cu and 0.285 mm on
both planes against a 0.20 mm rule; the narrowest conductor is 0.20 mm; the smallest plated hole
is 0.30 mm; copper stands 2.00 mm off every non-plated hole; zero digital nets enter the analogue
zone; and there is exactly one AGND_REF-to-DGND bridge and exactly one HARN_SHIELD-to-DGND
bridge. There are no duplicate track segments and no duplicate via positions. The report records
no clearance, width, annular-ring, hole-size, board-edge, non-plated-hole, isolation-keep-out or
via-keep-out violation, so the isolation strip is clean on all four copper layers -- stated here
because the report says it, not because the rule was asserted. **VIOLATIONS: 0.** The two vias
that sat 0.328 mm from an electrode net in the previous routing are gone.

**What the report does not say is that the routing is good.** It closes, and in places it closes
at minimum geometry: **169 connections were relaxed to make them** -- 36 took a conductor
narrower than the 0.25 mm preferred width, and 133 kept full width and took a reduced gap
instead. All 169 are at or above the 0.20 mm minimum conductor and the 0.20 mm minimum gap, and
0.35 mm on electrode nets, so every one of them passes; they are listed pad to pad in the report
so that a reviewer can see exactly where the router had to squeeze. A board that closes at
minimum geometry is not the same board as one that closes at preferred geometry, even when every
rule passes. That judgement, and the fact that **no human layout engineer has read this
routing**, is what RFQ-EEG-002A buys. **The data is released for review under it; fabrication
release waits on the review.**

The enclosure grew with the board: POD-P1 is now 163.0 × 143.0 × 58.0 mm external and
158.0 × 138.0 × 55.5 mm internal, and the MP-01 module plate is 146.0 × 126.0 × 3.0 mm.

**ECO numbering**, as ruled in RUL-EEG-021 section B. The change *register* is the document
ECO-EEG-016. The individual changes are ECO-EEG-001 to ECO-EEG-015, ECO-EEG-017 and
ECO-EEG-018, so that no change shares a number with the register: the routing-scope change that
once carried the number ECO-EEG-016 is now **ECO-EEG-018**, and both layout findings above -- the
growth to 150.0 × 130.0 mm and the move from two layers to four -- sit inside it. A Rev B
draft of ECO-EEG-016 briefly numbered those two findings separately, as ECO-EEG-028 and
ECO-EEG-029; **both numbers are withdrawn**, and the findings sit inside ECO-EEG-018.

The requirement changes of Rev E are each logged in ECO-EEG-016 as ECO-EEG-019 to ECO-EEG-027.
They are: the C0G part-number correction (019), fiducials (020), I²C pull-ups (021),
the VBUS_DET divider (022), the ENV_CMP re-referencing (023), the 68 kΩ series-resistor fix and the
E-10 widening (024), the F-06 ring relaxation (025), the E-04 crosstalk restatement (026) and the
E-11 corner restatement (027).

---

## 1. Purpose and how to respond

We are seeking a manufacturing partner for a small-batch, open-hardware EEG instrument used in
a pre-registered research study. The instrument is a **loaned, circulating field kit**: it is
shipped to a participant, used for two to three recording sessions at home, returned,
refurbished and shipped to the next participant. Everything about its design follows from that.

| Phase | Quantity | Deliverable | Purpose |
|---|---|---|---|
| 1 -- Prototype | 2 finished units, plus bare and partially populated boards as needed | Layout review and sign-off (RFQ-002A, separate line), DFM review, 2 assembled carriers with modules fitted on the MP-01 plate, in the POD-P1 enclosure, with printed helmet frame HM-01, harness assembled, test report per TST-EEG-004 | Prove the front end, the timing chain, the USB path and the safety design |
| 2 -- Pilot fleet | 10 complete kits | Assembled, tested, enclosed units with electrodes, headphones, microphones, cables, consumables and travel case, each kit serialised | The single-site study and the first remote sessions |
| 3 -- Fleet | 10 to 40 further kits (25 to 50 total) | As Phase 2, in one or two batches, with 25 % spare boards | The circulating fleet for the distributed study |

### 1.1 What we are asking you to quote

**What we want to receive is a finished kit.** Not a board, not a bag of parts, and not a
sub-assembly to be completed here: a working instrument, assembled, provisioned, tested,
packed in its flight case with its consumables and its printed guide, that a researcher in
Brussels can take out of the case, plug into a computer with the supplied USB cable, open a
Chromium browser and see working. Every line in the list below exists to produce that one
thing, and the acceptance in section 9.3 is written against it.

The last step of that sentence is testable by you before you ship, and we require it: every
unit must pass **TOOL-EEG-022**, the browser connectivity test program supplied in `webtest/`,
on your bench, against the same USB cable that ships in the case. It needs no instrument, no
network and no account -- one HTML file, a Chromium browser and the unit. Section 9.1 step
T-CONN records it and the printed result travels in the case lid pocket. A unit that has
not been shown to enumerate, identify itself and pass a data round trip through a browser
has not been tested against the thing it is for.


- **RFQ-EEG-002A -- layout review.** Review the supplied routing of EEG-CAR-01 Rev B against
  the rules in DSN-EEG-003 Rev C section 3.3, correct what is wrong, and sign it off. Deliver
  a corrected board file, corrected Gerbers and a written review note. One correction round.
  Quote as a separate line. **This is a review, not a layout project**; the board file, the
  Gerbers, the drill files and the DRC report are supplied. The board is **four layers**, so the
  review must cover plane splits and the continuity of the reference under every analogue trace,
  not only the two signal surfaces. **The supplied routing is complete and passes our own
  design-rule check.** It is 3 745 track segments and 552 through vias on four layers, all 145
  nets fully connected, one continuous reference island per net per plane, and
  `kicad/EEG-CAR-01_RevB_DRC_report.txt` records **zero violations**. **This is a smaller line
  than earlier issues of this document advertised**: there is no longer a set of open violations
  to close, so a bidder who priced a rescue should requote a review. What is left is judgement.
  The routing was produced by the programme's own tools and **no human layout engineer has looked
  at it**, and **169 connections were relaxed to close** -- 36 below the 0.25 mm preferred
  conductor width, 133 at full width with a reduced gap, all at or above the 0.20 mm minimum.
  Reading what the router did, and saying whether the relaxed connections are acceptable where
  they fall, is what this line buys. **The data is released for review under this line and not
  yet for fabrication**, so the carrier-fabrication line below is priced now and goes to a
  fabricator on the reviewer's sign-off.
- Carrier fabrication (four layers, ENIG) and assembly (SMT and through-hole). **Note 13 and
  note 14 of the fabrication drawing are conditions of acceptance, not extras**: one
  microsection lot coupon in the panel rails, and five lot documents with every lot. Each is
  an incoming-inspection row in QP-EEG-010 section 2.1 and each rejects the lot if it is
  missing, so please price them rather than discover them.
- Procurement of the listed modules, or acceptance of consigned modules -- please state which,
  or quote both. **Twelve module types are purchased and thirteen module assemblies are fitted per
  unit**, because the ADS1299 breakout is fitted twice.
- Manufacture of the ribbon-jumper set, the WH-KEY-01 keying shrouds and the MP-01 module plate
  per ICD-EEG-006.
- Firmware loading and end-of-line provisioning (we supply the image and the script).
- MJF printing of the supplied STL files, mechanical assembly, cable and harness assembly
  per WH-EEG-008.
- Kitting: electrodes, headphones, microphones, consumables, printed guide, travel case.
- Functional test per TST-EEG-004, and a per-unit test record.
- The one-off test fixtures FIX-01 to FIX-04 of JIG-EEG-009, if you prefer to build them rather
  than have them supplied.
- Packaging and shipping to Brussels, Belgium, with Incoterms stated. Note that kits contain a
  lithium cell; see S-09.

### 1.1a If you cannot do all of it

We would rather have an honest partial bid than a complete-looking one that unravels at the
first stage you had not thought about. **Bid on what you actually do**, and for every line you
are not quoting, say so explicitly in the compliance matrix rather than leaving it blank.

For each line you cannot deliver, please tell us:

1. **What you would need from a third party** -- the process, not just the gap. "MJF printing"
   is a gap; "MJF PA12 printing of eleven parts, one build, PA12 to the AVL-EEG-017 K24 row,
   bead-blasted and dyed" is a process we can go and buy.
2. **Who could do it.** Named suppliers you have worked with, or the type of supplier and how
   to qualify one. You are not endorsing them and we will not hold you to their performance.
   This is the most useful thing a specialist bidder can give us and it costs you nothing.
3. **Who integrates, and who tests.** If the kit is assembled in more than one place, name the
   party who does final assembly, runs TST-EEG-004 and TOOL-EEG-022, signs the per-unit record
   and packs the case. Split responsibility for the finished article is the failure mode we are
   trying to avoid; someone has to own the working instrument.
4. **What it costs to hand off.** Any co-ordination, carriage, incoming inspection or rework
   you would charge for parts arriving from elsewhere.

**If you are bidding partially, state your differentiator.** We will also receive bids from
integrators who can deliver the finished, tested kit in its case end to end. A partial bid
costs us the co-ordination those bidders absorb, so tell us plainly what you are better at and
why that is worth the difference -- analogue assembly yield, four-layer capability, harness
craft, test rigour, medical-adjacent quality system, engineering support during bring-up,
whatever it genuinely is. A specific claim we can check beats a general one. We are a small
research programme and a bidder who is candid about their edges is worth more to us than one
who is not.

### 1.2 What we supply

- The complete package v2: routed board file, Gerbers, drill, IPC-D-356A netlist, BOM, CPL,
  drawings, schematic, STL/STEP/DXF, firmware with its build system and provisioning script,
  and every document listed in DSN-EEG-003 Annex A.
- Reference amplifier for the section 9.2 comparison test: one OpenBCI Cyton.
- Firmware, provisioning tooling and the host-side test software.
- Electrical safety review sign-off, by a qualified reviewer we engage, before Phase 2 is
  released. That review has not yet happened.

### 1.3 Response format

Please return, within three weeks of receipt: (a) a compliance matrix against sections 4 to 9,
**marking every line you are not quoting rather than leaving it blank**; (b) itemised pricing
per phase on the template in section 10, **including the section 9.4 correction rates**;
(c) lead times per phase; (d) your certifications (ISO 9001, IPC class); (e) the name of an
engineering contact; (f) **if you are bidding partially, the four answers section 1.1a asks
for, and your differentiator against a bidder who can deliver the finished tested kit end to
end**; (g) **your answer to section 9.4** -- the correction loop, what your price already
includes, and whether you will hold the Phase 1 units at your bench until they pass.
Questions are welcome and will be answered to all bidders.

---

## 2. Design basis (Rev E)

Purchased, proven modules on one custom **four-layer** carrier, EEG-CAR-01 Rev B, 150.0 × 130.0 mm.
**Modules do not plug directly into the carrier**: except for the ESP32-S3-DevKitC-1 they mount on
the printed module plate MP-01 above the board and connect with keyed 2.54 mm ribbon jumpers,
because no public standard fixes their header geometry. That includes the **voice-microphone
preamplifier, which is on MP-01 at J21**; the boom carries only the bare electret capsule and its
screen, on the pigtail at J18. Package v1 put the preamplifier on the boom and was wrong;
`design.py` governs, and J21 is a carrier socket.

**The module-to-connector table is in ICD-EEG-006 section 1** and is not repeated here. The
interface each module must present, including which sockets take a WH-KEY-01 keying shroud, is in
the same document.

The carrier itself carries what no purchased module provides: sixteen input protection networks,
three envelope detectors, the stimulus comparator, the response buttons, the star grounds, the I²C
pull-ups and the two helmet harness sockets. Its full specification -- material, finish, stack-up,
track and clearance minima, hole schedule, zone split and IPC classes -- is in **DSN-EEG-003 Rev C
section 3.2**, and the isolation keep-out and star-point rules are in **DSN-EEG-003 Rev C section
3.3**. Both are cited, not restated, everywhere else in this package.

> **Licence condition.** All design files are published under CC BY-SA 4.0. The manufacturer
> retains no exclusivity and may not apply additional restrictions. Any file generated from
> them -- corrected Gerbers, CAM data, assembly programs -- must be released to us under the same
> licence. Firmware is MIT.

---

## 3. System architecture

The design principle that dictates almost every choice below is that **co-registration happens
where the signals are digitised**. EEG, EMG, three audio envelopes and the button states are
fields of a single sample produced by one converter clock. Nothing downstream -- not the USB
link, the browser or the server -- is used as a timing reference. The instrument has a single
host interface: USB. There is no wireless path.

### 3.1 Channel allocation

| Converter | Channels | Signal | Gain | Notes |
|---|---|---|---|---|
| ADS1299 #1 | 1–8 | EEG: Fz, Cz, Pz, C3, C4, T7, T8, F7 | 24 | Reference: linked earlobes into SRB1. Bias drive to the Fpz electrode. Lead-off enabled |
| ADS1299 #2 | 1–3 | EMG: cheek, submental, laryngeal | 6 or 12 | Separate gain register; same reference |
| ADS1299 #2 | 4 | Envelope: stimulus (headphone tap) | 1 | AC coupled, scaled to ±100 mV |
| ADS1299 #2 | 5 | Envelope: voice microphone | 1 | as above |
| ADS1299 #2 | 6 | Envelope: room microphone | 1 | as above |
| ADS1299 #2 | 7–8 | Spare: EOG electrode, future in-ear probe | 24 | Brought to J22 through their own protection networks (R15/R16). **Not wired to a panel socket in a standard build**; see E-09 |
| Aux bits | -- | Button A, Button B, envelope comparator flag, charger present, SD write OK | -- | Packed into the 16-bit auxiliary field of every sample |

This is the **stream** numbering. It is not the same as the R1–R16 protection-network numbering of
DSN-EEG-003 section 5, and the two must not be conflated.

---

## 4. Electrical requirements

### 4.1 Analogue front end

| Ref | Requirement | Level |
|---|---|---|
| E-01 | Two Texas Instruments ADS1299 (full eight-channel parts; the -4 and -6 variants are not acceptable) cascaded in daisy-chain mode on one SPI bus, sharing one 2.048 MHz clock from the first converter's CLK output, so that all sixteen channels are sampled simultaneously | M |
| E-02 | Sample rate selectable by register write: 250, 500 and 1000 samples per second. Fleet default 500 Hz. The rate in force is carried in every frame header | M |
| E-03 | Input-referred noise of the EEG channels ≤ 1.0 µV RMS in the 0.5–70 Hz band at gain 24 with inputs shorted, measured per unit. *Calculated **0.31 µV RMS** with the 68 kΩ resistors ECO-EEG-024 fitted on 2026-09-02, inside the limit with more than 3× of margin. It was 0.27 µV at the 47 kΩ fitted until that date; that figure is superseded as the live one. The arithmetic lives in RISK-EEG-011 section 4 and is not repeated here* | M |
| E-04 | **Channel-to-channel crosstalk better than −80 dB at 50 Hz, measured on the carrier** (restated by ECO-EEG-026), and gain matching within 0.5 % across the eight EEG channels at the 100 µV and 1 mV points, measured per unit. *The −100 dB of Rev D is withdrawn: it is not achievable through a 60 mm un-interleaved ribbon and it sits some 40 dB below this instrument's own noise floor, so it is not measurable here either. The ribbon's own contribution is characterised once on the first prototype as a type test. The 10 µV point is a ±5 % linearity check, not a 0.5 % matching point* | M |
| E-05 | Internal 4.5 V reference used for both converters; the bias amplifier closed-loop from the average of the EEG channels, routed to a dedicated bias electrode lead through R11. *Partially verified only: the 4.5 V reference itself is not measured in production* | M |
| E-06 | Lead-off detection on the EEG channels using AC excitation (7.8 or 31.2 Hz) at a current not exceeding 6 nA. *Register-set, not measured* | M |
| E-07 | **Sixteen** series protection networks, one per conductor that can reach a person: **68 kΩ** 0.1 % 25 ppm thin film (R1–R16, Vishay TNPW060368K0BEEA — **ECO-EEG-024, applied 2026-09-02**; 47 kΩ until that date, and that value is superseded), a BAV99 clamp to AVDD/AVSS (D1–D16) and a 10 nF **C0G** filter to AGND_REF (C1–C16, Murata GCM1885C1H103JA16D; the GCM188R71H103KA37D of earlier drafts is an X7R part and is wrong, ECO-EEG-019). Footprints allow 10 kΩ to 100 kΩ, which is what made the ECO-EEG-024 change to 68 kΩ a fit change and not a respin: same 0603 footprint, same nets, same pad count, so the board did not move. **BAT54S is not acceptable at D1–D16**: Schottky leakage across a 68 kΩ series resistor is an offset error on a 10 µV input. Value confirmed at safety review | M |
| E-08 | Analogue and digital ground partition, guard pour around all high-impedance inputs, no digital trace inside the analogue zone. The four-layer stack gives a continuous AGND_REF reference under every analogue trace on both inner layers. Met by the zoning rules of DSN-EEG-003 Rev C section 3.3 and verified in the DRC report | M |
| E-09 | Scalp electrodes, references and bias arrive on the **12-way screened electrode harness** at J14. The three EMG face leads use external touch-proof 1.5 mm DIN 42802 sockets (J15–J17) on the pod underside, colour-coded. The two spare channels are brought to J22 and are protected like every other electrode lead, but **the EOG panel sockets are not fitted in a standard build**: they are a Phase 2 option with no cable, no drawing and no part number yet, listed as such in PARTS-EEG-019. *Rev C's M-02 called for thirteen DIN sockets; the correct number is three fitted, plus two optional and unfitted* | M |
| E-10 | No mains-frequency notch in hardware; the front end must pass DC to 100 Hz flat within **±0.5 dB with the 47 kΩ resistors fitted (calculated −0.36 dB at 100 Hz), and within ±1.0 dB if ECO-EEG-024 raises them to 68 kΩ (calculated −0.75 dB at 100 Hz)**. **Both limits are stated together every time E-10 is quoted**, because the resistor value is a safety decision under S-02: the 68 kΩ value is the one the safety fix requires and the widened limit goes with it, and the wider limit is earned by that resistor and by nothing else. **Restated 2026-09-02: ECO-EEG-024 is applied and 68 kΩ is what is fitted, so the ±1.0 dB branch is the one in force**, and TST-EEG-004 T22 grades every unit against it. *Until that date this row read "ECO-EEG-024 is open and 47 kΩ is what is fitted, so the Phase 1 prototypes are graded at ±0.5 dB"; that is superseded.* A unit built with 47 kΩ would still be graded at ±0.5 dB, and none is to be built | M |

### 4.2 Envelope detectors and audio

| Ref | Requirement | Level |
|---|---|---|
| E-11 | Three identical envelope channels: precision **full-wave** rectifier followed by a second-order Butterworth low-pass at 50 Hz ±10 %, **AC coupled at ≤ 2 Hz** (restated by ECO-EEG-027), output scaled to ±100 mV into the ADS1299 input at gain 1. *Implemented with one OPA4376 quad per channel: rectifier, absolute-value summer, Sallen-Key filter and a ×0.0909 buffered divider.* **E-11 IS NOW MET IN BOTH HALVES, as of 2026-09-02.** The AC-coupling half was already met: 1.6 Hz *(calculated)* against ECO-EEG-027's ≤ 2 Hz. **The low-pass half is met by moving the Sallen-Key from X7R to C0G.** It was 22 kΩ with 100 nF and 220 nF X7R, and X7R is ±15 % over temperature: since f₀ goes as 1/√(C₁C₂) the corner ranged over **42.4 to 57.4 Hz** *(calculated)*, so no build with those parts could be held inside 45–55 Hz wherever the centre sat. The obstacle was that 100 nF C0G is not a stocked 0603 part — so the network no longer asks for 100 nF. Scaling the capacitors down by ten and the resistors up by ten leaves f₀ and Q where they were and lands on **10 nF and 22 nF C0G with 215 kΩ**: f₀ = 49.9 Hz, Q = 0.742, and at C0G's ±5 % the corner spans **47.6 to 52.6 Hz** *(calculated)*, inside the band with margin. The 10 nF is the SAME part the board already buys sixteen of as the electrode RF filter C1–C16, so it adds no purchasing line. Same 0603 footprints and same nets, so **the board does not move**: this is a BOM change, not a respin. TST-EEG-004 T12e still measures f₀ per unit and its 42–58 Hz band is now a wide acceptance around a part that holds 47.6–52.6, not a band written to excuse the parts | M |
| E-12 | A comparator on the stimulus envelope driving a GPIO latched on the sample-ready interrupt, giving sub-sample onset resolution as an aux bit. *Implemented as drawn: U7 TLV3201 powered from **AVDD and AVSS**, threshold 52 mV (R80 470 kΩ / R81 10 kΩ from AVDD to AGND_REF), hysteresis ≈5 mV, output into GPIO3 through R83 and the D23 clamp, leaving 20 mV of logic margin. **ECO-EEG-023 — re-power U7 from DVDD3V3 and DGND, re-reference its inputs to a DVDD3V3/2 divider and AC-couple the envelope into it — is OPEN and is NOT in the released `design.py`; the 52 mV threshold changes with it.** The safety and layout reviewer signs it before it is cut in at Rev C (ECO-EEG-016 §2). Raised from S to M in Rev D because it is now fitted* | M |
| E-13 | Audio codec on I²S with at least one stereo DAC output and two ADC inputs. Headphone amplifier capable of driving the 32 to 64 Ω closed-back headphones of A-04 to 85 dB SPL with ≤ 0.1 % THD. Output level set by register, read back and logged. The ceiling of E-29 applies at every commanded level | M |
| E-14 | Voice microphone: electret capsule on a removable boom fixed to the HM-01 frame at about 3 cm from the mouth corner, detachable at a keyed connector so the boom can be replaced between participants. **The preamplifier is on the MP-01 module plate at J21, not on the boom**, which carries the bare capsule and its screen on the J18 pigtail. Automatic gain control must be off. **Which preamplifier is not settled**: the MAX9814 named in package v1 is an AGC part and disabling its AGC is a module-dependent modification, so it is carried as a candidate only and is not approved; the preferred route is a fixed-gain part of the MAX4466 class. Until one is bought and measured the module is specified **by interface** in ICD-EEG-006 | M |
| E-15 | Room microphone: omnidirectional module on the enclosure, facing outward, with an acoustic port; its audio path must be hardware-gatable (MIC_MUTE on GPIO21) so that room audio is captured only during scripted windows. *No catalogue module is yet known to meet the hardware-mute requirement; the fallback is a capsule with an analogue switch in the module-end connector, which would be a programme-designed sub-assembly and a new drawing. Open* | M |
| E-16 | Reference-tone calibration path: the firmware plays a known-level tone and reads both microphone envelopes; the resulting gains are reported in session metadata. The headphone output tap must be before any user-adjustable control | M |
| E-17 | Headphone bleed into the voice microphone at maximum stimulus level ≤ −40 dB relative to a 70 dB SPL voice at the boom, measured on the first prototype and reported. *No method for this measurement exists anywhere in the package and "maximum stimulus level" is not defined; both are owed before the Phase 1 report* | M |
| E-29 | **Maximum acoustic output.** The headphone output must not exceed **100 dB SPL** at any commanded level, measured on an artificial ear, and the firmware must clamp the codec volume register to the value measured at calibration. *New in Rev E. Calculated full-scale output is about 110 dB SPL, which is why the requirement is needed on an instrument that plays stimuli into the ears of distressed participants at home. Type-tested once per lot at **TST-EEG-004 step T28**, which is listed among the type tests in TST-EEG-004 section 14; the clamp value is read back per unit at T17* | M |
| E-30 | **The contact lights must not corrupt the measurement they report.** The lights are driven from the converter's own lead-off measurement (E-27), so whenever a light is lit an electrode channel is being measured: the two are concurrent by design, and only the recording blocks are mutually exclusive with them. With all eight lights driven at the E-27 phase rate, the added noise on any electrode channel referred to the input must be **below 0.5 µV RMS in 0.5–70 Hz**, the band E-03 states, measured through the fitted WH-01 and WH-02 harnesses in an assembled helmet -- not on the carrier through a fixture. *This requirement did not exist before 2026-09-02 and nothing had ever measured the quantity. The design's controls are real and are stated in WH-EEG-008 sections 3.2, 5.4 and 7: two occipital entries, channel A for the electrodes and channel B for the lights at minimum 6 mm centre to centre, an LED_GND guard conductor in the middle of the WH-02 bundle, J30 placed in the digital zone across the x = 62 mm split by ECO-EEG-014, and a source impedance below 1.1 kΩ with no high-impedance node in the light group. What was missing was a limit and a measurement. Note that the separation the frame provides does not exist at the site: the LED sits inside the HM-04 electrode body, millimetres from the cup, and the electrode conductor runs at full electrode impedance the whole way to the carrier because the series resistors — 68 kΩ since ECO-EEG-024 — are on the board. TST-EEG-004 T9c measures this. The limit is set at half the 1.0 µV RMS input-referred noise floor E-03 asks of the channel, in E-03's own band so the two are directly comparable, so that the lights cannot consume more than a small part of the budget* | M |

### 4.3 Digital, storage, identity and power

| Ref | Requirement | Level |
|---|---|---|
| E-18 | ESP32-S3-DevKitC-1-N16R8, socketed at J6/J7 on 22.86 mm row spacing, with Wi-Fi and Bluetooth permanently disabled in firmware. **GPIO35, 36 and 37 carry the octal PSRAM on this variant and must be left unconnected; GPIO45 is the VDD_SPI strapping pin and is also left open.** Not substitutable. *The carrier draws a calculated 288 mA worst case from the DevKit's own 3V3 regulator, which is inside its rating but dissipates about 0.5 W inside a closed pod. Phase 1 measures it and reports the regulator case temperature (TST-EEG-004 T3); if it exceeds 85 °C, **a 3.3 V regulator on the carrier fed from V5V is an ECO against Rev C** of the board. This is not presented as solved. The 288 mA is the calculated worst-case load on the DevKit's 3.3 V output, from the load table in ICD-EEG-006 section 5.3; it is not the cell-side current that TST-EEG-004 T3 measures at J13, and the two figures have not been reconciled -- see section 12 item 14* | M |
| E-19 | SPI to both converters at ≥ 4 MHz with DRDY on an interrupt-capable pin; the sample counter is incremented in the DRDY interrupt and never elsewhere | M |
| E-20 | microSD socket, **one-bit SDMMC**, FAT32/exFAT, written continuously with the identical frame stream that goes to the host, with no dropped frames. **Tested as a split: 30 minutes at 1000 Hz per unit, and a three-hour soak at 1000 Hz on one unit per lot.** *The sustained payload at 1000 Hz is **50.7 kB/s** -- 1015 bytes every 20 ms. The "≈70 kB/s" of earlier revisions and the "≈64 kB/s" of F-12 are allowances that include STATUS and SIGNATURE frames and filesystem overhead; they are not the frame payload and neither figure is a new requirement. About 2 MB/s is available in one-bit mode. One-bit is used because four-bit would consume the three GPIOs the contact-light shift register needs* | M |
| E-21 | Microchip ATECC608B on I²C, provisioned at end of line with a unique P-256 key pair and a serial number; the public key and serial are printed on the unit label and delivered in the per-unit test record | M |
| E-22 | Single protected Li-ion cell (18650, ≥ 3000 mAh) giving ≥ 4 hours recording at 1000 Hz. The isolated side stays battery powered. Fuel gauge readable by firmware; battery percentage carried in the status frame. *The 4 h endurance figure has no per-unit test; it is a type test* | M |
| E-23 | **Two separate USB-C connectors**, and a charger IC with thermal regulation that **does not charge above 45 °C**. Data is the connector on the ADuM4160 isolator module and carries no power to the instrument. Charging is a separate charge-only receptacle wired to J24 through a 1.1 A PTC and a transient suppressor. Charging is inhibited by firmware (VBUS_DET on GPIO46) and by the charger enable line (CHG_CE on GPIO47) while a session is active; the two mechanisms are specified once, at S-01. *R85 is 150 kΩ, giving 3.00 V at VBUS = 5.00 V against the 2.48 V input-high threshold of a 3.3 V ESP32-S3 pin (ECO-EEG-022); the 56 kΩ of the first cut gave 1.79 V and would not have asserted the first interlock reliably.* **E-23 is met in part, and the two halves must always be stated together.** The thermal-regulation half is met: the charger module carries a charger IC whose own thermal regulation folds back the charge current as the die heats, and that is what the requirement asks for. **The 45 °C inhibit is not met and cannot be tested**: it needs a cell temperature, and there is no NTC net in `design.py` and no thermistor way on J12 or J13, so nothing on the carrier can read the cell. **S-04's thermistor-monitored charging is therefore not met either**, and the two hardware holes are the same hole. It is an open hardware item with no closure proposed, carried with S-04 in section 12 item 3 | M |
| E-24 | ADuM4160-based USB isolator module (≥ 2.5 kV RMS) at J10, with the host connector on the module and no carrier copper crossing the barrier; the isolation keep-out is specified in DSN-EEG-003 Rev C section 3.3. The part is not substitutable. **This requirement asks for USB-C and the only named candidate module presents USB-B. That is a live non-conformance.** The interim answer is a short USB-B-to-USB-C panel pigtail, **WH-09**, until an isolator module with a USB-C host connector is qualified; it is not a settled design | M |
| E-25 | Analogue supplies **AVDD = +2.5 V and AVSS = −2.5 V**, generated on ADS1299 module #1 and brought onto the carrier at J23. AGND_REF is the analogue 0 V mid-rail, not a ground; the single star point to DGND is the rule in DSN-EEG-003 Rev C section 3.3. A buck-boost converter supplies the 5 V rail; it is in the digital zone, at least 15 mm from any input net. *Its switching frequency is not measured in production* | M |
| E-26 | Three momentary push buttons, distinct tactile feel and colour (A green, B blue, stop red), with hardware RC debounce (R50–R52, C50–C52) and firmware debounce. **The switch is a 6 mm tactile switch (Omron B3F-4055 class) with a 12 mm coloured cap on an extender; the panel openings are 12.4 mm on a 14.0 mm pitch, in the POD-P1 LID, at x = 102 and y = 76, 90 and 104 mm.** *Corrected 2026-09-02 on `tools/mech_gen.py`, which is where the openings are cut. This row read "13.0 mm on a 14 mm pitch … on the POD-P1 right wall"; both halves were wrong. The buttons sit at x = 102 on the carrier, 48 mm inboard of the right wall, so wall openings lined up with nothing and merged with the connector openings — a button on a pod lying on a table is pressed from above, and it belongs in the lid. And 12.4 mm is the smallest opening that still clears the 12 mm cap this row specifies; at 13.0 mm on a 14.0 mm pitch the openings leave only 1.0 mm of lid between them. The "≥ 12 mm actuator" wording of Rev C described the cap, not the switch, and put 13 mm openings on a 12 mm pitch, which does not fit at all* | M |
| E-27 | Eight bicolour contact lights in the helmet, driven from the converter's own lead-off measurement, alternating at 240 Hz to show amber. They must be dark at power-on and dark during recording blocks. **MET as of 2026-09-02.** *Dark at power-on is met in hardware: LED_V is GPIO48, an input at reset, so no current can flow through any light whatever the shift register contains -- and the driver returns it to an input whenever the lights are dark, so that state is re-entered and not merely left behind. **The bicolour phase driver is now written.** The converter's positive-side lead-off comparator is read at two thresholds. Per site: trips neither = GREEN, trips the sensitive threshold only = AMBER, trips both = RED. *Corrected again 2026-09-02 (FW-D17): the sentence about both halves of the lead-off word is superseded. `ads_init()` enabled `LOFF_SENSP` only, so `LOFF_STATN` was zero for ever and RED WAS UNREACHABLE -- every site that had lost contact showed amber. Enabling `LOFF_SENSN` was not the fix either: the montage is single-ended, J2 carrying IN1-IN8 with one shared SRB1, so the N half has no per-site electrode. The driver now sweeps the positive-side comparator threshold COMP_TH between a sensitive and an insensitive setting: trips neither = GREEN, trips the sensitive one only = AMBER, trips both = RED. The two thresholds are datasheet endpoints, not measured trip points, so the impedance at each boundary is set at first bring-up (TST-EEG-004 T11 Note 3).* Green is lit in phase A, red in phase B, amber in both. The alternation quantises to the FreeRTOS tick: 2 ms half-phases on a 1 kHz tick, so about 250 Hz rather than exactly 240, which meets the "above 100 Hz" this requirement is written against and is stated rather than rounded away. TST-EEG-004 T11 can now pass, and has not been run: no unit exists* | M |
| E-28 | Test points on SPI, DRDY, I²S, the three envelope outputs, all supply rails and the analogue reference, accessible with the enclosure open: **TP1–TP18 on the carrier, assigned in TST-EEG-004 section 6.2**, which is the one home for that table. A **1×6 debug header (J26)** carries 3V3, DGND, UART0 TX and RX, EN and a spare way. *The 2×5 1.27 mm JTAG/SWD header of Rev C is **withdrawn**: the ESP32-S3 is programmed over UART0 and its native USB, and no JTAG connector is fitted, so there is no deviation to record against one. J26 way 6 is **NC_GPIO0**, a spare, because GPIO0 is committed to LED_SR_LATCH (ECO-EEG-009) and does not reach J26; end-of-line flashing therefore uses the DevKitC-1's own UART USB-C port, which carries the auto-reset circuit, reached through the MP-01 opening. **Met in part**: CS, I2S_MCLK, I2S_DIN, I2S_DOUT, VBAT and VBUS_CHG have no test point* | M |

---

## 5. Firmware and host-interface requirements

The session runner is a browser application on the TI One Voice platform, connecting over USB
from a Chromium-based browser using WebSerial on desktop or WebUSB on desktop and Android.
There is no wireless path. The goal is *one click, once, ever*. The firmware is ours; the
requirements below are what the hardware must make possible and what the manufacturer must
provision at end of line. FW-EEG-001 specifies the build and the provisioning. **Restated 2026-09-02: the firmware is
built and has never run on hardware.** It compiles under ESP-IDF v5.2.5 for esp32s3 and
`firmware/release/` holds the four flashable images with a manifest of their SHA-256; it has been
run once under QEMU, which emulates none of this instrument's peripherals. *The "has never been
compiled or run on hardware, and five driver stubs remain" of the previous issue is withdrawn on
both halves: the drivers are written, and two paths — the sample-accurate tone start and the
sub-sample onset interpolation — are marked partial in `firmware/main/drivers.c` and are graded
against what they achieve.* Section 12 item 12 states what the build does and does not prove.

### 5.1 USB device model

| Ref | Requirement | Level |
|---|---|---|
| F-01 | Composite USB 2.0 full-speed device: a CDC-ACM serial interface for the WebSerial path and a vendor-specific bulk interface (one IN, one OUT, 64-byte packets) for WebUSB. Both carry the same frame stream | M |
| F-02 | Descriptors: a Binary Object Store with a WebUSB platform capability descriptor and a Microsoft OS 2.0 platform capability descriptor assigning WinUSB to the vendor interface, so Windows binds a driver with no user action | M |
| F-03 | VID and PID: the programme will obtain a PID under pid.codes; the manufacturer programs the assigned values at end of line. They must be identical across all units of a hardware revision. *The allocation is pending; the values in the package are placeholders* | M |
| F-04 | `iSerialNumber` populated from the unit serial at boot, in the format **`TIOV-B-nnnn`** defined once, in PKG-EEG-015 section 5. The same string appears on the label, in the Data Matrix, in the calibration record and on the packing list | M |
| F-05 | Re-enumeration after host sleep, cable re-seat or browser reload within 2 s, with no reset of the sample counter or the ring buffer | M |

### 5.2 Frame format and stream discipline

The same frame format crosses every boundary: microSD, USB and the browser-to-server
websocket. One parser, one test suite, and the manufacturer's production test must decode it.

| Field | Size | Content |
|---|---|---|
| Delimiter | 1 byte | 0x00, with the body COBS-encoded so 0x00 cannot appear inside it |
| Version / type | 2 bytes | Protocol version; DATA, STATUS, EVENT, GAP, SIGNATURE, CMD_ACK |
| Sequence number | 2 bytes | Increments per frame, wraps; used for gap detection and retransmit |
| First sample index | 4 bytes | Monotonic sample counter of the first sample, assigned in the DRDY interrupt and never recomputed. **This is the only timeline in the system** |
| Rate code / count | 2 bytes | Rate in force; samples in this frame (20 at 1000 Hz, 10 at 500, 5 at 250 -- one frame every 20 ms) |
| Samples | n × 50 bytes | 16 × 24-bit two's-complement channel values (48 bytes) then the 16-bit auxiliary field |
| CRC-32 | 4 bytes | Over the decoded body, before COBS |

A full frame at 1000 Hz is **1015 bytes every 20 ms, which is the 50.7 kB/s of E-20**.

| Ref | Requirement | Level |
|---|---|---|
| F-06 | Ring buffer of at least **90 seconds** at 1000 Hz in PSRAM, from which the host can request retransmission by sequence range, **plus unlimited backfill from the microSD copy beyond that depth** (restated by ECO-EEG-025). *The three minutes of Rev D asked for about 12 MB of ring in the 8 MiB of PSRAM the mandated E-18 module carries, which is impossible. The fitted ring is 6 MB, which is 126 seconds; the device declares its own ring depth in the STATUS frame and the test grades against the declared depth* | M |
| F-07 | On overflow the device drops the oldest frames and emits a GAP frame stating the first and last sample index lost. Silent loss is not permitted. The microSD copy is unaffected | M |
| F-08 | A SIGNATURE frame every 2048 samples carrying an ECDSA P-256 signature computed by the ATECC608B over the SHA-256 of the block, chained to the previous block hash | M |
| F-09 | STATUS frame once per second: battery, temperature, per-channel lead-off state, SD free space, link type, uptime, clock offset estimate, and the ring depth in seconds | M |
| F-10 | A command channel on the same interface: start/stop session, start/stop block with label, set rate, set per-channel gain, run impedance check, load block audio, play at a sample-indexed start time, set headphone level, reference-tone calibration, exchange clock offset, request retransmit, begin signed firmware update, enter provisioning mode. *The full command set is not swept in production* | M |
| F-11 | Audio for a block is pre-loaded before the block begins and started at a commanded sample index, so stimulus onset is fixed on the device clock and the stimulus envelope is the authoritative onset record | M |
| F-12 | Bandwidth: the ≈64 kB/s allowance for 16 channels at 1000 Hz covers the 50.7 kB/s of frame payload plus STATUS and SIGNATURE traffic; the USB path must sustain three times that for backfill | M |

### 5.3 Host and browser requirements (for information)

| Ref | Requirement | Level |
|---|---|---|
| F-13 | The session runner runs in a Chromium-based browser on Windows, macOS, Linux or Android. Safari, Firefox and iOS are out of scope for this revision | Info |
| F-14 | The browser read loop runs in a worker, batches frames into ~20 ms chunks and forwards them over a TLS websocket. The browser is trusted for liveness, not integrity: block signatures are verified server-side | Info |
| F-15 | Backpressure is absorbed by the browser and, if the browser stalls, by the device ring buffer. The microSD copy is complete regardless of link state | Info |
| F-16 | Clock-offset exchange is relayed at 10 s intervals; the estimate is metadata only and is never applied to the sample timeline | Info |
| F-17 | **The host connection is a socket, not a captive cable.** The host connector is the USB-C receptacle on the ADuM4160 module, presented through a gasketed aperture in POD-P1 (with the WH-09 pigtail while the candidate module presents USB-B). The two cables of A-07 are shipped with every kit and one of them is the host lead. The isolator is the only electrical connection between the participant and any mains-powered equipment; bidders must confirm it carries the full session data rate plus backfill without error. *The captive lead through a cable gland is a Phase 2 item for the helmet shell and is not in the Phase 1 build* | M |

### 5.4 Provisioning and firmware update

| Ref | Requirement | Level |
|---|---|---|
| F-18 | End-of-line provisioning using our script: generate the key pair in the ATECC608B, export the public key and serial, program VID/PID and hardware revision, write the calibration constants from the functional test, lock the configuration zone. The script prints a record that is returned with the unit | M |
| F-19 | Secure boot and flash encryption enabled on the ESP32-S3; images signed with the programme's key; the device rejects unsigned images. **The manufacturer never holds the signing key.** No network credentials of any kind are provisioned. *The eFuses are **not burned on the two Phase 1 prototypes**, which run unsigned images so the firmware volunteer can iterate; secure boot and flash encryption are enabled from Phase 2, and TST-EEG-004 T25 is a Phase 2 step, not a Phase 1 gate* | M |
| F-20 | Firmware update over the USB command channel with A/B partitions and automatic rollback on boot failure | M |
| F-21 | A timing self-test mode: the device plays 40 test tones and reports the spread between the commanded onset sample index and the detected stimulus-envelope onset. Median ≤ 1 sample, 95th percentile ≤ 2 samples at 1000 Hz. Run at end of line and before every session | M |

> **Why these details matter to the manufacturer.** The browser cannot enumerate USB devices
> silently; it can only reconnect to a device the participant has authorised once, and that
> authorisation is keyed to the VID/PID and the serial number string. If units in a batch
> differ in either, or if Windows does not bind WinUSB automatically because the OS 2.0
> descriptor is missing, the participant is sent to a driver-installation page -- and for this
> population, that is where the session ends.

---

## 6. Electrodes, sensors and accessories

| Ref | Requirement | Level |
|---|---|---|
| A-01 | Eight sintered Ag/AgCl cup electrodes on service-release bayonets inside the permanently mounted HM-04 assemblies, two spare bodies held as build stock, plus two Ag/AgCl ear-clip references. Sintered, not plated; replaced by the operator every ~25 sessions with the HM-09 service key, never by the participant | M |
| A-02 | Three EMG surface electrodes with snap-to-DIN leads. Disposable snap pads are a consumable; 30 per kit | M |
| A-03 | **Head retention: the chin strap HM-06 and the occipital yoke HM-03**, both fitted to the HM-01 frame. HM-06 is a printed chin cup (HM-06A) with a washable TPU liner (HM-06B, a consumable replaced each turnaround) and a bought-in 20 mm webbing and buckle set (HM-06C). HM-03 is a printed yoke (HM-03A) and dial housing (HM-03B) over a bought-in ratchet (HM-03C) giving 52 to 62 cm of band travel at 2 mm per click. *The separate adjustable headband of Rev D is **withdrawn as a kit item**: the eight electrodes are fixed to the HM-01 frame at manufacture, so a headband with fixed holders at the same eight sites would duplicate them. **No drawing has been issued for HM-03A/B or HM-06A/B and no supplier part is named for HM-03C or HM-06C**; both are Phase 1 make-or-buy work and cannot be firmly quoted today* | M |
| A-04 | Closed-back over-ear headphones, **32 to 64 Ω**, 3.5 mm plug, ≥ 1.2 m cable; the same model in every kit so the calibrated output level is transferable, and the output level measured per model. *The shipped candidate is the Audio-Technica ATH-M20x, which the manufacturer publishes at 47 Ω, so the production test load is 47.0 Ω. The 32 Ω of Rev D matched no shipped part* | M |
| A-05 | Consumables per kit: two 100 g tubes of conductive EEG paste, one 100 g abrasive prep gel, 30 saline wipes, cotton buds, blunt-tip syringes, a disinfection guide | M |
| A-06 | Enclosure-mounted electrode panel labelled with 10–20 names and colours; a laminated quick-start card in the **case lid pocket** (IFU-EEG-014), with the per-unit calibration and test record beside it; a printed placement guide matching the on-screen guide | M |
| A-07 | A 1.0 m USB-C to USB-A cable and a 1.0 m USB-C to USB-C cable, one of which is the host lead of F-17; a 5 V 2 A USB charger with EU plug. No charger of other plug types unless specified per destination | M |

---

## 7. Enclosure and travel case

| Ref | Requirement | Level |
|---|---|---|
| M-01 | Phase 1: **POD-P1 bench enclosure, 163.0 × 143.0 × 58.0 mm external and 158.0 × 138.0 × 55.5 mm internal**, 2.5 mm walls, a 1.6 × 1.2 mm gasket groove and a 163.0 × 143.0 × 6.0 mm lid with a 2.0 mm spigot, connected to the helmet by the two harness cables. The internal stack is floor 2.5 + boss 6.0 + carrier 1.6 + M3 × 18 mm standoff + MP-01 plate 3.0 + modules ≤ 18.0 = 49.1 mm against 55.5 mm internal, a margin of 6.4 mm. **Phases 2–3: the occipital shell of HM-01, sized for the carrier split into two smaller boards -- that split does not exist.** The Rev B carrier is 150 × 130 mm and does not fit the 116 × 46 × 88 mm shell of earlier revisions, no split design has been drawn, and **nothing in the Phase 2 enclosure line can be quoted or built today**; it is a Phase 2 design task and is quoted when the design exists | M |
| M-02 | Openings: the electrode panel (**three DIN 42802 sockets fitted; two further sockets for the EOG option are a Phase 2 item and are not fitted**), 3.5 mm headphone jack, boom-microphone connector, room-microphone port with mesh, data USB-C on the isolator module, **charge USB-C**, microSD, and three button openings of **12.4 mm on a 14.0 mm pitch in the LID**, at x = 102 and y = 76, 90 and 104 mm (*corrected 2026-09-02 from "13.0 mm on a 14 mm pitch … on the right wall"; see E-26*). The right-wall connector openings are re-spaced accordingly. **No indicator opening**: the "LEDs" of Rev D are withdrawn, because all eight contact lights are in the helmet and the pod carries no indicator -- its state is read from the session runner. All openings gasketed or recessed so that gel and saline cannot reach the board | M |
| M-03 | Enclosure label: unit serial in the `TIOV-B-nnnn` format defined in PKG-EEG-015 section 5, hardware revision, ATECC public-key fingerprint as defined in FW-EEG-001 section 7, "research instrument -- not a medical device", the programme URL, and the charging warning of S-01. Laser-etched or a durable polyester label. Artwork in PKG-EEG-015 | M |
| M-04 | Drop test: the unit survives a 1 m drop onto concrete on each face without functional damage (case open, kit packed), tested on one Phase 1 unit | S |
| M-05 | Travel case: hard-shell, watertight and dust-tight (IP67 class), pressure-equalisation valve, lockable hasps, internal size large enough for **an assembled helmet standing upright** and for the enlarged POD-P1. The envelope is **≥ 516 × 390 mm usable footprint with the lid closed and ≥ 210 mm total internal depth, of which ≥ 185 mm in the base**, derived bay by bay from the CASE-00 Rev C schedule. **PKG-EEG-015 section 3.2 is the single home of the travel-case dimensions** and this row is written to it; the approximately 340 × 250 × 210 mm of Rev D is withdrawn, and it was too small for the bay schedule, not merely imprecise. A custom die-cut or laser-cut closed-cell PE foam insert -- CASE-00 Rev C, seven loose-laid 25 mm layers, 175 mm of stack, scheduled in PKG-EEG-015 section 2.2 and no longer the two sheets of Rev B -- holds the enclosure, the electrode set coiled, the headphones, the boom, the cables, the charger, the consumables pouch and the quick-start card. **The baseline shell is the Peli 1560**, published internal 518 × 392 × 229 mm, which clears the footprint by 2 mm on each plan axis and the total depth by 19 mm. The two transcriptions of that shell that used to be in circulation are reconciled: AVL-EEG-017 K21's figures are the adopted ones and PKG-EEG-015's earlier 508 × 330 × 198 mm is withdrawn as a mis-transcription. **What is open is not the choice.** No shell has been bought, measured or weighed, so those figures are published-and-unverified; Peli does not publish the base-to-lid depth split, so the ≥ 185 mm base figure is the one number that can still sink this shell; 2 mm of plan margin is inside the tolerance of a moulded case; and the Rev C cut file is not drawn, because six of its nine bays hold parts that are not dimensioned anywhere in this package. There is also **no drawn alternate**: the Nanuk 960 clears the depth but is 32 mm short of the 390 mm axis, so choosing it means a Rev D of the cut file (PKG-EEG-015 section 9, items 1, 2 and 10; section 12 item 9 here). **No empty-mass limit is set**: PKG-EEG-015 section 3.2 withdrew the ≤ 4.0 kg target of its Rev A because no shell that meets this envelope meets it, and the measured empty mass is recorded instead. Bidders quote the foam tooling against the Peli 1560 and state the cost of a change | M |
| M-06 | Foam cut-outs labelled (engraved or printed) so a participant can repack correctly without instructions; a packing photograph laminated inside the lid | S |
| M-07 | Outer shipping carton for the case, double-wall, with a returnable pre-paid label pocket. The case itself must not be the shipping container | M |

---

## 8. Safety and regulatory requirements

This is a research instrument connected to a person's head. It is not being placed on the
market as a medical device, but it is used on human participants and is designed to the
applicable principles of IEC 60601-1 for a type BF applied part. Certification is not
requested; the test evidence in section 9 must be supplied so that our safety reviewer can sign
the design off. RISK-EEG-011 is the pack the reviewer receives. **That review has not happened,
and no requirement below has been verified on hardware.**

| Ref | Requirement | Level |
|---|---|---|
| S-01 | Battery-only operation during recording. **Two independent interlocks**: firmware refuses to start a session while VBUS_DET is high, and CHG_CE holds the charger disabled for the whole of a session. **The helmet is never worn while the charge cable is connected**, and the label and the participant card say so. No other interlock exists; in particular there is no hatch interlock anywhere in this design | M |
| S-02 | Patient auxiliary current through any electrode ≤ 10 µA DC and ≤ 100 µA AC in normal condition, including the lead-off excitation; single-fault ≤ 50 µA DC. **MET as of 2026-09-02, in the design.** ECO-EEG-024 is applied: R1–R16 are **68 kΩ**, so the single-fault DC current is **36.8 µA** *(calculated)* on the bare-resistor bound and **30.0 µA** *(calculated)* on the measuring-device bound, against the 50 µA limit — a 26 % margin on the worse of the two. The cost is written into E-10, which states both branches and permits the ±1.0 dB one for exactly this case: the input corner moves to 234 Hz, −0.75 dB at 100 Hz. Same 0603 footprint, same nets, so the board does not move. *Superseded on 2026-09-02: this requirement read "This is not met by the board as fitted: the single-fault DC current is calculated at 53.2 µA against the 50 µA limit, with the 47 kΩ resistors in place", that 47 kΩ was fitted on the Phase 1 prototypes, and that S-02 was "carried as a live Phase 1 decision … and is not claimed as met". The 53.2 µA stood through three revisions and is withdrawn as a statement of the design.* **Three things are unchanged and none of them is small.** Nothing has been built or measured, so 36.8 µA is arithmetic on datasheet figures and not a reading. **This does not discharge RISK-EEG-011 SR-01**, which stays open: the electrical safety reviewer owns the disposition, the review has not started, and what has changed is that the reviewer is handed a design that meets the limit and asked to confirm it rather than one that does not and asked to accept it. And S-02 still states no AC single-fault limit, which is its own open point (RISK-EEG-011 SR-06). The arithmetic and the fault bounds are in RISK-EEG-011 section 4 | M |
| S-03 | Isolation from any mains-referenced host: the USB isolator rated ≥ 2.5 kV RMS for one minute, evidenced by the module supplier's type certificate checked once at incoming inspection. The barrier is entirely on the module; the carrier has no copper crossing it, per the keep-out in DSN-EEG-003 Rev C section 3.3. **The per-unit test is a 500 V DC insulation-resistance measurement across the barrier, not a hipot**; no routine 2.5 kV AC test is performed on an assembled unit | M |
| S-04 | Battery: protected cell with over-charge, over-discharge and short-circuit protection; **thermistor-monitored charging**; the cell mechanically retained in the keyed HM-10 carrier so it cannot be inserted reversed; UN 38.3 test report available. **S-04 is not met and stays not met**: there is no NTC net in `design.py` and no thermistor way on J12 or J13, so the cell temperature cannot be read and S-04's thermistor-monitored charging cannot be provided or tested. The same missing hardware is why the 45 °C inhibit half of E-23 is not met, while E-23's thermal-regulation half is met on the charger module. It is an open hardware item with no closure proposed, carried in DSN-EEG-003 section 11 and RISK-EEG-011 | M |
| S-05 | Materials in contact with skin biocompatible per ISO 10993-5 and -10 declarations from their suppliers, for every skin-contact material including the HM-06B chin-cup liner. REG-EEG-012 section 6 states what a valid declaration looks like | M |
| S-06 | EMC: the assembled unit must not emit above CISPR 11 class B limits (report on one Phase 1 unit). No intentional radiator is active; production must confirm the radio is disabled. *The CISPR measurement is a type test; only the radio-silent check is per unit* | S |
| S-07 | Not used. Retained so that requirement numbering stays stable across revisions | M |
| S-08 | Manufacturer to supply a Declaration of Conformity draft for RoHS 3 and REACH, and to state which safety standard, if any, their production line is audited against | S |
| S-09 | **Lithium shipping.** Every kit contains an 18650 cell inside equipment. Despatch must comply with UN3481 / packing instruction PI967 section II: state of charge ≤ 30 %, the lithium-battery mark on the outer carton, the correct carrier documentation, and a return arrangement the participant can actually use. **The procedure lives in PKG-EEG-015 section 7**; this requirement states only the obligation. Verified per unit at kit closure by TST-EEG-004 T29 | M |

---

## 9. Test and acceptance

Every unit is a slightly different instrument, and device identity must not become a confound
in the study. So every unit is characterised, and the numbers travel with it.

**TST-EEG-004 (Rev C is the current issue) is the authoritative production test, and it owns the
step numbers T00 to T29.** No other document invents one. It carries a requirements-to-test
traceability matrix, so any mandatory requirement above with no test is visible. The summary below
is retained for orientation and cites that document's steps; where the two differ, TST-EEG-004
governs.

### 9.1 Per-unit production test (all phases)

1. Incoming inspection of the purchased modules and the carrier passives (T00), including the
   C0G check on C1–C16 and the isolator supplier's 2.5 kV type certificate.
2. Bare-board electrical test to the supplied IPC-D-356A netlist, before assembly (T0). This is
   the 100 % star-point and keep-out evidence.
3. Visual and AOI to IPC-A-610 class 2 (T1), including BAV99 at D1–D16, the DNP of R89, the
   fiducials and the TP1–TP18 set. **X-ray is applied to the two converter packages** on the
   Phase 1 units per QP-EEG-010 section 11.2; it is not a numbered step in TST-EEG-004, and that
   gap is open.
4. Module seating and keying (T2); power-on current at idle and recording, measured at J13, and the
   DevKit regulator case temperature (T3) -- T3's own pass limits govern, and they are not the
   same quantity as the 288 mA calculated 3.3 V load of E-18 (section 12 item 14); charge current with a session active (T4); VBUS detection
   and both S-01 interlocks (T21).
5. Provisioning per F-18 (T6) and USB enumeration on Windows, macOS and Linux with no driver
   installation (T5, before and after provisioning).
6. Front-end gain through the JIG-EEG-009 FIX-01 divider (T7): 100 µV and 1 mV at 10 Hz with
   **matching within 0.5 % across the eight EEG channels**, and the 10 µV point as a **±5 %
   linearity check** -- the measurement uncertainty there is 0.22 % (k = 2) and will not support
   a tighter limit. Noise per E-03 (T8), crosstalk to the restated −80 dB and CMRR (T9). Written
   to the unit's calibration record.
7. Lead-off calibration against 5 kΩ, 10 kΩ and 50 kΩ references on each channel (T10);
   reported within 15 %.
8. Contact lights (T11): colour, site mapping and the two dark states, read with a
   TCS34725-class colorimeter head, FIX-01/E. *Corrected 2026-09-02: this step used to read "cannot
   pass until the bicolour light driver of E-27 is written". **The driver is written**, so T11 can
   pass; it **has not been run**, because no unit exists.*
9. Envelope channels (T12): scaling, group delay, the comparator flag and the AC-coupling
   corner. Onset is graded as a **spread**, not against an absolute two-sample limit; the
   expected constant group delay is 4.40 ms. Timing self-test per F-21 (T13).
10. microSD write test for **30 minutes** at 1000 Hz with frame-count verification and a
    card-versus-host comparison (T14); ring-buffer backfill with a forced 60 s disconnect and a
    300 s disconnect recovered from the card (T15). The three-hour soak is one unit per lot, not
    per unit.
11. Signature chain verified end-to-end by our host test tool against the exported public key
    (T16).
12. Buttons, microphone mute, **headphone output level into 47.0 Ω** and the E-29 clamp
    readback, microphone gains (T17). **The fuel gauge has no per-unit step**: presence is
    confirmed at T00 and the reading is logged only at the per-lot 4 h endurance test of
    TST-EEG-004 section 14; raised as an open item.
13. Star-point continuity (T19); isolation-barrier insulation resistance at 500 V DC (T20);
    leakage measurement at the fourteen applied-part terminations standing in for patient
    auxiliary current (T23) -- a stand-in, not the IEC 60601-1 method. *Corrected 2026-09-02: this
    read "and S-02 is not met at the fitted resistor value". **S-02 is met at the fitted 68 kΩ**,
    at a calculated 36.8 µA. T23 is still a stand-in, the real verification is a type test with an
    MD-2 measuring device that does not exist yet, and RISK-EEG-011 SR-01 is still open.* The AGND_REF-to-DGND measurement with R90 lifted is per lot first
    article and on any unit whose reading is anomalous.
14. Radio silent (T24); re-enumeration timing (T26); converter clock, sample rate and daisy
    order (T27).
15. Final assembly check (T18): enclosure closed, openings gasketed, label applied, kit contents
    ticked against KPL-EEG-001, foam cut-outs correct; and the lithium marking and shipping
    documents (T29).

**Requirements with no per-unit coverage**, and stated as such rather than implied: E-17
(headphone bleed), M-04 (drop), E-22 (4 h endurance), the three-hour half of E-20, the CISPR half
of S-06, S-08, and F-13 to F-16 (host and server software, out of scope). **Partially covered:**
E-05, E-06, E-10 (six frequencies only, and against the ±1.0 dB band that the fitted 68 kΩ earns
-- *corrected 2026-09-02 from "the ±0.5 dB band while 47 kΩ is fitted"*),
E-23 (the charger module's thermal regulation is not measured and the 45 °C inhibit has no
hardware to test), E-25, E-28 (six named nets have no
test point), F-10, S-02 and S-03.

### 9.2 Phase 1 additional tests

- Comparison recording on a human volunteer against the OpenBCI Cyton we provide, same
  electrodes, same session: N100 latency within 2 ms and amplitude within 10 %.
- **Maximum acoustic output into an artificial ear per E-29** (T28), once per lot, with the
  codec clamp value recorded.
- Ribbon-jumper crosstalk contribution, characterised once with and without the 60 mm ribbon in
  circuit, which is the measurement E-04's restatement rests on.
- Headphone bleed per E-17; EMC pre-scan per S-06; drop test per M-04; the closed-pod regulator
  thermal run of TST-EEG-004 T3 (30 minutes, case temperature < 85 °C).
- **Twenty-five cup release-and-refit cycles with disinfectant exposure**, to answer the
  bayonet-seizure objection of DSN-EEG-002 section 12.
- Total worn mass and centre-of-gravity measurement, to answer the counterweight objection.
- Fit measurement on eight heads spanning 52–62 cm and across hair types, with actual electrode
  positions marked against measured 10–20 sites.
- Our electrical safety review of the schematic, the layout and one assembled unit. **Phase 2
  is released only on written sign-off.** *Restated 2026-09-02:* **ECO-EEG-024 is applied**, so
  what is on the reviewer's desk is a design that meets S-02 at a calculated 36.8 µA, to be
  ratified rather than chosen — RISK-EEG-011 SR-01 is open for that written disposition, and the
  measurement of the real single-fault current on a Phase 1 unit is made before Phase 2. The
  **ECO-EEG-023 comparator change is still open** and is on the same desk.

### 9.3 Acceptance and warranty

**Acceptance is against a working instrument, not against a shipment.** A unit is accepted in
Brussels when all four of these are true: the per-unit TST-EEG-004 record is present and
passes; the TOOL-EEG-022 browser connectivity result is present and passes; our own incoming
test (a subset of 9.1, plus TOOL-EEG-022 run here on our own machine) passes; and the case
contains everything PKG-EEG-015 section 2 lists. The printed calibration and test record
travels in the **case lid pocket** beside the quick-start card.

Please state your warranty period, your policy on infant-mortality replacements, and your lead
time for repair of returned boards. We expect to return boards for repair over the life of the
fleet and would prefer a partner who will service the design.

### 9.4 When a unit does not work: the correction process

**We expect the first prototypes to have faults.** Phase 1 is two units of a design that has
never been built, whose firmware has never run on hardware, and whose layout was produced by
software. Nobody should price this work as though it will be right first time, and we would
rather agree now what happens when it is not than negotiate it while a broken unit sits on a
bench.

This section is a **question to bidders**, not a term we are imposing. Answer it in your
response and we will settle the wording in the contract.

**The loop we propose.** One iteration is: we report, you reproduce, we agree the cause, you
correct, you retest, you return.

| Step | Who | What | Target |
|---|---|---|---|
| 1 | us | Written defect report: symptom, the TST-EEG-004 step or TOOL-EEG-022 check that fails, the unit serial, and the raw evidence (log, capture, photograph) | within 5 working days of receipt |
| 2 | you | Acknowledge and reproduce, or state that you cannot reproduce and what you need | 5 working days |
| 3 | both | Agree the **cause class** from the table below. This is the only judgement that decides who pays | 5 working days |
| 4 | you | Correct, retest to the same step, and state what changed | quote your lead time |
| 5 | you | Return with an updated per-unit record | -- |

**Who pays follows the cause, and there are only four causes.**

| Cause | Example | Who bears the cost |
|---|---|---|
| **A. Build fault** | Wrong part fitted, dry joint, harness miswired against WH-EEG-008, missing item in the case, unit fails a TST-EEG-004 step it was signed off as passing | You. Under warranty, at your cost including carriage both ways |
| **B. Design fault** | The design is built exactly as supplied and still does not work -- our schematic, our firmware, our layout | Us. We pay the correction iteration at the rates you quote below |
| **C. Specification defect** | The package is ambiguous, self-contradictory or silent, and you built a defensible reading of it | Us -- and we want to hear about these loudly. This package carries its own open-item lists precisely so that this class is small; every instance is a document defect we will fix and credit you for finding |
| **D. Change of mind** | We change a requirement after you have built to it | Us, at the rates below, and we accept the schedule consequence |

A fault whose cause is genuinely disputed after step 3 goes to the engineering contacts of
both parties before it goes anywhere else. We have not built this instrument either, and we
will not treat an honest disagreement as a warranty claim.

**What we need priced.** Put these in the section 10 template. We are asking for rates, not a
commitment to a number of iterations; nobody can forecast that.

| Rate | What it covers |
|---|---|
| Engineering hour, bring-up and fault-finding | Diagnosing a unit that does not pass, including your time on a call with us |
| Rework of one assembled carrier | Component replacement, rework of one board, retest to the failing step |
| Rebuild of one unit from an existing carrier | Harness, mechanical and kitting rework, full retest |
| One additional carrier fabrication lot, Phase 1 quantity | A board respin during bring-up, priced at the smallest lot you will run |
| Additional layout revision | Already a line in section 10; state whether it changes at Phase 1 quantities |
| Re-provisioning and retest of one unit | Firmware reload, provisioning, TST-EEG-004 and TOOL-EEG-022, updated record |
| Carriage, return to you and back to Brussels | Per unit, both directions, and whether a case must travel with it |
| Minimum charge per correction iteration | If you apply one, say so |

Also please state: **how many correction iterations your Phase 1 price already includes**
(many bidders include one and do not say so), whether cause-B and cause-C work is charged at
the same rate as cause-A rework, and whether you would prefer to hold the two Phase 1 units at
your bench until they pass rather than ship and return them. **We would prefer that**, if you
will do it: a fault found on your bench with the fixture in front of you is worth several
found on ours, and it is the single biggest lever on how long Phase 1 takes.

**Prototype-stage expectation.** For Phase 1 we would rather buy your engineering judgement
than your warranty. If your quote assumes a fixed scope with change control on every
deviation, say so, because that is a poor fit for a first build and we would rather know at
quotation than at iteration three.

---

## 10. Pricing template and commercial terms

Prices in EUR or USD, ex-works and delivered Brussels as separate figures. State the quantity
breaks you actually price at (2 / 10 / 25 / 50).

| Line | Phase 1 (2 units) | Phase 2 (10 kits) | Phase 3 (per kit at 25 / 50) |
|---|---|---|---|
| Layout **review** and sign-off of EEG-CAR-01 Rev B incl. one correction round and DFM (RFQ-002A) | | -- | -- |
| Additional layout revision (per revision) | | -- | -- |
| Carrier fabrication, **four layers**, 150.0 × 130.0 mm, 1.60 mm, ENIG, through vias only (per board) | | | |
| Four-layer premium over an equivalent two-layer board, stated separately (per board and per lot) | | | |
| **Microsection lot coupon and the five lot documents** of fabrication drawing notes 13 and 14 -- CoC, 100 % ET report, ENIG XRF, registration report, microsection report (per lot) | | | |
| Assembly: SMT + through-hole (per board) | | | |
| Carrier components (turnkey, per board) -- or consignment handling fee | | | |
| Purchased modules per unit (twelve types, thirteen assemblies: ADS1299 ×2, DevKit, codec, isolator, ATECC, charger, gauge, buck-boost, SD, boom preamp, room mic, 74HC595) -- or consignment | | | |
| Ribbon-jumper set, WH-KEY-01 keying shrouds and MP-01 plate 146.0 × 126.0 × 3.0 mm (per unit) | | | |
| WH-09 USB-B-to-USB-C panel pigtail, while the isolator module presents USB-B (per unit) | | | |
| Stencil and test fixtures FIX-01 to FIX-04 per JIG-EEG-009 (one-off) | | | |
| MJF prints: POD-P1 base + lid 163.0 × 143.0 mm (Phase 1) / HM-01 shell (Phases 2–3, design not yet issued), per unit | | | |
| MJF prints: HM-01 frame, HM-04 ×10, HM-08 hatch, HM-10 cell carrier, MP-01 (per kit) | | | |
| HM-09 service keys (per operator, not kit content -- eight for the Phase 2 fleet) | | | |
| Harness assembly per WH-EEG-008 (per unit) | | | |
| Boom microphone assembly, panel pigtails, cables (per unit) | | | |
| Electrodes, ear clips, EMG leads (per kit) | | | |
| Chin strap HM-06 and occipital yoke HM-03 sets, printed and bought-in parts (per kit) | | | |
| Headphones, 32 to 64 Ω, one model across the fleet (per kit) | | | |
| Consumables pack, first fill (per kit) | | | |
| Field spares held against SVC-EEG-013 section 6, and whether you hold them on consignment | | | |
| Travel case (Peli 1560 baseline, M-05) with the CASE-00 Rev C custom foam insert (per kit) -- seven loose-laid 25 mm PE layers, 175 mm of stack, scheduled in PKG-EEG-015 section 2.2 -- and the foam tooling as a one-off | | | |
| Provisioning and functional test per TST-EEG-004 (per unit) | | | |
| **TOOL-EEG-022 browser connectivity test on your bench, with the shipped cable, per unit** | | | |
| **Final integration: assemble, kit, pack the case, and sign the unit off as a working instrument (per unit)** -- quote this even if it is included elsewhere, so we can see what integration costs | | | |
| Spare assembled boards (25 % of fleet, per board) | -- | | |
| Packaging and shipping to Brussels, incl. UN3481 compliance (per batch) | | | |
| Lead time (weeks from PO) | | | |
| **Correction iterations already included in the Phase 1 price** (state the number) | | -- | -- |

**Correction rates (section 9.4).** These are rates, not quantities. We are not asking you to
forecast how many iterations a first build needs; we are asking what one costs when it happens.

| Rate | Unit | Phase 1 | Phase 2+ |
|---|---|---|---|
| Engineering hour, bring-up and fault-finding | per hour | | |
| Rework of one assembled carrier, incl. retest to the failing step | per board | | |
| Rebuild of one unit from an existing carrier, incl. full retest | per unit | | |
| Additional carrier fabrication lot at your smallest run | per lot | | |
| Re-provisioning and retest of one unit (TST-EEG-004 + TOOL-EEG-022) | per unit | | |
| Carriage, Brussels to you and back, one unit | per round trip | | |
| Minimum charge per correction iteration, if you apply one | per iteration | | |
| Holding the Phase 1 units at your bench until they pass, rather than ship-and-return | per unit | | -- |

- Please state: payment terms; module lead times at the time of quoting; your minimum order for
  the travel case supplier; any tooling you would retain; and your agreement to release the
  final Gerber, CAM and assembly files to us under CC BY-SA 4.0.
- **Component substitution.** Any substitution against the BOM must be proposed in writing and
  approved by us before build. The ADS1299 devices, the ATECC608B, the ADuM4160 isolator and the
  ESP32-S3-DevKitC-1-N16R8 are **not substitutable**. ICD-EEG-006 section 6 names only the last
  two; this document's wider list governs by the precedence of section 1. The *device* is what is
  fixed -- the breakout board carrying it may be changed only through the AVL-EEG-017 section 6
  procedure and with the evidence that section requires.
- **Traceability.** Date code and lot for the two converters and the cell recorded per unit.

---

## 11. Open decisions this specification has made on the programme's behalf

- **Host interface.** USB only. The wireless topology of the underlying design document is
  dropped: it removes the radio, the network stack, credential provisioning and the associated
  certification questions, at the cost of restricting participants to Chromium browsers on
  desktop or Android. The isolator therefore becomes the single most safety-critical component.
- **Four layers, not two.** Decided by doing the layout rather than by argument; the reasoning
  and the cost are in the Rev E note above. Through vias only, so any fabricator can quote it.
  The layout closes and passes every rule in our own design-rule check, but it is the programme's
  own router's work, no human layout engineer has read it, and 169 of its connections were
  relaxed to close. The data is released for review under RFQ-EEG-002A and is released for
  fabrication on that review.
- **Sample rate.** Fleet default 500 Hz, with 250 and 1000 selectable. The frame format carries
  the rate so no analysis code ever assumes one.
- **Isolation.** Specified on the board from revision A rather than as a later addition.
- **Electrode connector.** Touch-proof 1.5 mm DIN sockets on a panel rather than a single
  multi-pin connector, because electrodes are replaced individually at refurbishment.
- **Two USB connectors** rather than one (E-23), with a separate charge-only port and a hardware
  interlock, and **the host connection is a socket rather than a captive cable** (F-17).
- **Modules on jumpers rather than plugged directly** (section 2). The cost is stated openly in
  DSN-EEG-003 Rev C section 2.1. Jumper keying is decided: a shrouded polarised header at the
  module end where the module has one, and the printed WH-KEY-01 shroud at the carrier end.
- **No conformal coating for Phases 1 and 2.** The decision is taken, not deferred: the board
  lives inside a gasketed enclosure, and coating a board with thirty connectors and a socketed
  DevKit costs more in masking than it buys. Revisited before Phase 3 if a unit returns with
  corrosion.
- **Fiducials on the carrier.** Three 1.0 mm fiducials with 3.0 mm mask openings are placed
  (ECO-EEG-020), so the vision-teach workaround on test-point pads is withdrawn and need not be
  priced.
- **eFuses on the Phase 1 prototypes are not burned** (F-19), so the firmware volunteer can
  iterate; secure boot begins at Phase 2.

## 12. What this specification does not settle

These are open, and a bidder should price around them or ask. **Items that have since closed keep
their number and their row**, marked CLOSED with the date, so that a bidder reading a previous
issue can see what moved and when; nothing is deleted silently.

| # | Open item | What it blocks |
|---|---|---|
| 1 | **No safety engineer has reviewed this design.** | Use on a person. Not fabrication or quoting |
| 2 | **CLOSED 2026-09-02.** S-02's single-fault limit failed at 53.2 µA with 47 kΩ fitted, and the ECO-EEG-024 68 kΩ fix was not fitted. **It is fitted now** (`tools/design.py`): R1–R16 are 68 kΩ, the single-fault DC current is 36.8 µA on the bare-resistor bound and 30.0 µA on the measuring-device bound against the 50 µA limit, and E-10 moves onto the ±1.0 dB branch it already states for this case. The board does not move: same 0603 footprint, same nets. **What is not closed by it** is the safety reviewer's disposition — RISK-EEG-011 SR-01 stays open — and the Phase 1 measurement of the real single-fault current, because the 36.8 µA is calculated and nothing has been measured | Nothing any longer. The design meets S-02; item 1 is what still blocks use on a person |
| 3 | **S-04's thermistor and the 45 °C inhibit half of E-23 have no hardware.** There is no NTC net in `design.py` and no thermistor way on J12 or J13, so nothing can read the cell temperature. E-23's other half, thermal regulation in the charger IC, is met on the module | S-04 entirely, and half of E-23. No closure is proposed, and neither can be tested |
| 4 | **CLOSED 2026-09-02.** E-27's bicolour light driver was not written. **It is written** (`firmware/main/main.c`). The converter's positive-side lead-off comparator is read at two thresholds. Per site: trips neither is green, trips the sensitive threshold only is amber, trips both is red; green is lit in phase A, red in phase B, amber in both. *Corrected again 2026-09-02 (FW-D17): the sentence about both halves of the lead-off word is superseded. `ads_init()` enabled `LOFF_SENSP` only, so `LOFF_STATN` was zero for ever and RED WAS UNREACHABLE -- every site that had lost contact showed amber. Enabling `LOFF_SENSN` was not the fix either: the montage is single-ended, J2 carrying IN1-IN8 with one shared SRB1, so the N half has no per-site electrode. The driver now sweeps the positive-side comparator threshold COMP_TH between a sensitive and an insensitive setting: trips neither = GREEN, trips the sensitive one only = AMBER, trips both = RED. The two thresholds are datasheet endpoints, not measured trip points, so the impedance at each boundary is set at first bring-up (TST-EEG-004 T11 Note 3).* The alternation is a task delay and quantises to the FreeRTOS tick — 2 ms half-phases on a 1 kHz tick — so it runs at **about 250 Hz rather than exactly 240**, which meets the "above 100 Hz" E-27 is written against and is stated rather than rounded away | Nothing any longer. **T11 can now pass and has not been run**: no unit exists, and the light driver has never driven a light |
| 5 | Which boom preamplifier (E-14), and whether its AGC can be disabled | The AVL line and the boom sub-assembly |
| 6 | Whether any room-microphone module meets E-15's hardware mute | A programme-designed sub-assembly and a new drawing |
| 7 | J15–J17: `design.py` names Stäubli SLB1,5-F as a class, not a confirmed PCB part | A Class A patient-safety part on every unit; 12-week first-article risk |
| 8 | The isolator's host connector is USB-B against E-24's USB-C; WH-09 is interim | The panel design and the cable BOM |
| 9 | The travel case (M-05): the Peli 1560 is the named baseline, but **no shell has been bought, measured or weighed**, its published internal figures are unverified, its base-to-lid depth split is not published at all, and the CASE-00 Rev C foam cut file is not drawn because six of its nine bays hold parts that are not dimensioned anywhere in the package. There is no drawn alternate shell (PKG-EEG-015 section 9, items 1, 2 and 10) | Foam tooling, carton, freight and the M-05/M-06 acceptance |
| 10 | The Phase 2 occipital-shell carrier split (M-01) | All Phase 2 enclosure pricing |
| 11 | USB VID/PID allocation (F-03) | The fleet, not the prototypes |
| 12 | **RESTATED 2026-09-02. The firmware is BUILT and has NEVER RUN ON HARDWARE.** *This item read "the firmware has never been compiled or run on hardware; five driver stubs remain". Both halves are withdrawn.* It builds under **ESP-IDF v5.2.5** for **esp32s3**, and `firmware/release/` holds `bootloader.bin`, `partition-table.bin`, `ota_data_initial.bin` and `eeg_field_kit.bin` (405 360 bytes) with a `manifest.json` of their SHA-256. It has been **run once under QEMU** (`qemu_boot.log`, `qemu-system-xtensa -M esp32s3`): the bootloader reads this partition table, the app loads from the factory slot, `app_main()` runs, and the microSD and ES8388 bring-up paths degrade as they were written to. **QEMU emulates none of this instrument's peripherals** — no octal PSRAM, no microSD, no ES8388, no ADS1299 — so the run says nothing about a register value, a daisy-chain order or SPI timing. Three things stay open and are named rather than implied. **The PSRAM path aborts and reboots**: with no external RAM the 6 MiB ring buffer will not allocate, FW-D13 refuses to continue silently, and the image reboot-loops — correct behaviour on a part without PSRAM, and completely untested against the -N16R8 part that has it. **IRAM is 16 383 of 16 384 bytes** (`firmware/release/size.json`), so any further `IRAM_ATTR` code, or growth in the ISR tables, fails to link. And two driver paths are written as **partial** in `firmware/main/drivers.c` — the sample-accurate tone start and the sub-sample onset interpolation — and are graded against what they achieve rather than what E-13 and E-12 ask | A working prototype. The build is real; the bring-up is not, and no line of this firmware has executed on silicon |
| 13 | **The supplied routing has not been read by a human layout engineer.** It was produced by the programme's own tools. It closes -- 145 of 145 nets connected, zero DRC violations, one plane island per net on both inner layers -- but **169 connections were relaxed to make it close**: 36 below the 0.25 mm preferred conductor width and 133 at full width with a reduced gap, all at or above the 0.20 mm minimum. A board that closes at minimum geometry is not a board that closes at preferred geometry | Fabrication release, not quoting. The data is released for review under RFQ-EEG-002A, and that review is what releases it for fabrication |
| 14 | **The board-current figures are not reconciled.** TST-EEG-004 T3 grades idle < 90 mA and recording at 1000 Hz < 150 mA at J13. **ICD-EEG-006 section 2.7 is the tally the package works from**: about **300 mA typical on V5V** while recording and about 420 mA worst case, which at 3.900 V from the cell and an assumed 88 % buck-boost efficiency is **about 440 mA at J13** while recording and **about 610 mA worst case** *(calculated)*. Section 5.3's about 190 mA typical and 288 mA worst case on DVDD3V3 is the same arithmetic seen from the other rail, because the DevKit's LDO is fed from V5V and passes its own output current almost one for one; Rev A's "DevKit about 120 mA on V5V" is withdrawn and the two ICD tables no longer disagree with each other. **They still disagree with T3**: on this arithmetic every unit fails the 150 mA limit, by a factor of about three. Nothing has been measured on either side | The T3 pass limits, the E-22 endurance calculation and the DevKit regulator thermal case. The measurement is made at Phase 1 and the owning documents are corrected against it. ICD-EEG-006 carries the same disagreement as open point 13 of its section 8 |
| 15 | **CLOSED 2026-09-02.** E-11's 50 Hz ±10 % low-pass band could not be met with the approved parts, because a 100 nF C0G in 0603/50 V is not stocked and both Sallen-Key capacitors were therefore X7R at ±15 % over temperature, putting f₀ anywhere between 42.4 and 57.4 Hz. **The network stopped asking for 100 nF.** Capacitors down by ten and resistors up by ten leave f₀ and Q where they were and land on **10 nF and 22 nF C0G with 215 kΩ**: f₀ = 49.9 Hz, Q = 0.742 unchanged, and at C0G's ±5 % the corner spans 47.6 to 52.6 Hz *(calculated)*, inside the 45–55 band with margin. The 10 nF is the same part the board already buys sixteen of at C1–C16, so it adds no purchasing line, and the footprints and nets are unchanged, so the board does not move. TST-EEG-004 T12e's 42–58 Hz band is now a wide acceptance around a part that holds 47.6–52.6, not a band written to excuse the parts | Nothing any longer. **Nothing has been built or measured**: 49.9 Hz is calculated, and T12e measures f₀ per unit when units exist |

**The order these close in. Restated 2026-09-02, because two of the three it used to name have
closed.** None of the remaining items stops a bidder quoting. Item 14 first: T3's idle and
recording limits, the E-22 endurance calculation and the DevKit regulator thermal case are all
written against a board current nobody has measured, and the Phase 1 measurement is what corrects
them. Item 12 next, in its restated form: the firmware is built, so what T3, T21 and the other
firmware-dependent steps now wait on is **hardware**, not code -- the image has never executed on
silicon, and the PSRAM path in particular has only ever been exercised on a machine with no PSRAM.
*Item 2 used to sit third here, on the argument that the 47 kΩ/68 kΩ value was cheaper to settle
before the prototype boards were stuffed than after. It is settled: 68 kΩ, ECO-EEG-024, and the
boards will be stuffed with it.* Items 1 and 3 block use on a person outright, and item 13 stands
between the data and a fabricator; they are not sequencing questions. Item 1 is the one that has
not moved at all, and it is the one that matters most: **no safety engineer has reviewed this
design**, and RISK-EEG-011 SR-01 is open on their desk even though the requirement it was raised
against is now met.

---

## Annex A -- Cover email for the RFQ

*Carried forward from RFQ-EEG-001 Rev C and brought up to Rev E. It is here because a
manufacturer who has never heard of this programme opens the email before the package, and
nothing else in the package is written for a reader who has opened nothing yet. Square
brackets are filled in per recipient.*

> **Subject:** RFQ -- small-batch open-hardware EEG instrument, 2 prototypes then 10-50 field kits
>
> Dear [name / sales team],
>
> I am writing on behalf of a research programme in Brussels, Belgium, to request a
> quotation for the manufacture, assembly and kitting of a sixteen-channel research EEG
> instrument. The design is a derivative of the OpenBCI Cyton and Daisy open-hardware
> boards -- two Texas Instruments ADS1299 converters cascaded -- with an ESP32-S3 DevKit, a
> codec module, a secure element and a USB-isolator module, on a **four-layer carrier board
> that we supply as a fully routed file with Gerber X2, Excellon and IPC-D-356A data**. It
> connects to a browser over USB only, with no wireless, sits in a small enclosure, and is
> delivered as a complete field kit in a hard travel case with electrodes, the
> head-retention set (chin strap and occipital yoke), headphones and consumables.
>
> The work is in three phases: two prototype units, then ten complete kits, then a further
> ten to forty. **The routing already exists and our own design-rule check passes it with zero
> violations**, so what we ask for as a separate line is a *review* of it rather than a layout
> job -- and a smaller review than earlier issues of this package described. What we are buying
> is judgement: no human layout engineer has read the routing yet, and 169 of its connections
> were routed at relaxed geometry in order to close. The data is released for review and goes to
> a fabricator on the reviewer's sign-off.
> The attached RFQ (RFQ-EEG-001 Rev E, within the design package) sets out the electrical,
> firmware-interface, mechanical, safety and test requirements, and a pricing template.
> Every requirement is labelled Mandatory, Should or Optional; we ask for a compliance
> matrix against them.
>
> Two points are worth stating up front. The design files are and will remain open hardware
> under CC BY-SA 4.0, so we are looking for a partner comfortable with that. And the
> instrument is used on human research participants, so the electrical safety requirements
> in section 8 -- battery-only operation while recording, series lead protection, USB
> isolation -- are not negotiable, although certification is not requested.
>
> We would be grateful for a response within three weeks. Technical questions are welcome
> at any time and will be answered to all bidders. Please also let us know whether you
> would prefer to receive the design files as KiCad, as the Gerber set alone, or as PDF
> schematics.
>
> With thanks,
>
> Stephane van der Aa
> TI One Voice research programme -- one.witysk.org
> stephane@stepvda.com -- +32 493 70 16 01
>
> *Attachments: the EEG field kit design package (see Annex B index).*

**What changed from Rev C's version of this letter.** Rev C described a "two-layer carrier
board supplied as a placed and netlisted file" and asked bidders to quote the routing. Both
are now wrong: the carrier is four layers and it is routed. Rev E also drops the separate
headband from the kit list, which A-03 withdraws as a kit item: the eight electrodes are fixed
to the HM-01 frame at manufacture and the head-retention set is the chin strap and the
occipital yoke. The letter says so, and states the review line's real size -- a board that
closes and that no layout engineer has read, not a broken one to rescue -- because a bidder who
discovers the scope after quoting is a bidder lost.

---

## Annex B -- Reference documents

- OpenBCI V3 hardware design files (Cyton and Daisy), CC BY-SA 4.0
- Texas Instruments ADS1299 datasheet and ADS1299EEGFE-PDK reference design
- Texas Instruments OPA4376 and TLV3201 datasheets
- Analog Devices ADuM4160 datasheet
- Microchip ATECC608B datasheet and provisioning guide
- Espressif ESP32-S3 datasheet and ESP32-S3-DevKitC-1 user guide; ESP-IDF USB-OTG device stack
- WebUSB and WebSerial API specifications (WICG)
- IEC 60601-1 (general safety, type BF applied parts) and IEC 60601-2-26 (electroencephalographs),
  as design references only
- IPC-6012 class 2, IPC-A-600 class 2, IPC-A-610 class 2, IPC-D-356A, IPC-7351B
- UN Manual of Tests and Criteria 38.3; IEC 62133-2; IATA DGR packing instruction PI967
- The experiment design document, version 4.2, Parts 7, 13 and 14 -- available on request

---

## Revision history

| Rev | Date | Change |
|---|---|---|
| C | earlier | Bidder asked to route the carrier |
| D | 2026-09-01 | Board supplied routed; RFQ-EEG-002A re-scoped to review and sign-off; fourteen Rev C design defects corrected; S-09 added |
| E | 2026-09-01 | Corrected to the 150.0 × 130.0 mm four-layer carrier and the enlarged POD-P1 and MP-01; preamplifier moved to MP-01 at J21; E-04 restated to −80 dB (ECO-EEG-026), E-10 stated as ±0.5 dB at the fitted 47 kΩ and ±1.0 dB only if ECO-EEG-024 raises them to 68 kΩ, E-11 to ≤ 2 Hz (ECO-EEG-027), E-20 split into a per-unit and a per-lot test with the 50.7 kB/s payload explained, E-23's 45 °C inhibit restored, E-26's button geometry restated, E-28's 2×5 header withdrawn and TP1–TP18 referred to TST-EEG-004 section 6.2, F-06 relaxed to 90 s (ECO-EEG-025); E-29 maximum acoustic output added; A-03 rewritten for the chin strap and yoke, A-04 to 32 to 64 Ω; M-01, M-02 and M-05 corrected; S-02, S-04, E-23 and E-27 stated plainly as not met; duplicated tables replaced by cross-references; section 10 gained a four-layer line and the missing spares, service-key, shroud and tooling lines; section 12 added |
| E | 2026-09-01 | Corrections within Rev E, no revision letter change: the findings of the second cross-document audit naming this document were closed -- the DevKit regulator fallback restated as an ECO against Rev C of the board, E-10's ±0.5 dB and ±1.0 dB cases always stated together, E-23 stated as met in part with S-04, the real DRC result and the **not released for fabrication** status inserted in the Status section, section 1.1 and section 12, the ECO numbering restated against RUL-EEG-021 section B, the `TIOV-B-nnnn` serial format referred to PKG-EEG-015 section 5, and the unreconciled board-current figures raised as section 12 item 14. Third audit, same day: E-11 stated as met in part with its 50 Hz ±10 % half not met by the approved parts and section 12 item 15 opened for it, M-05 rewritten onto PKG-EEG-015 section 3.2's settled Peli 1560 envelope with section 12 item 9 restated, and section 12 item 14 restated from ICD-EEG-006 section 2.7 |
| E | 2026-09-02 | Corrections within Rev E, no revision letter change, fourth audit: EEG-CAR-01 Rev B was re-routed and now closes -- 145 of 145 nets fully connected, no unclosed net, no net without copper, **zero DRC violations**, and the two 0.328 mm electrode-clearance vias gone. The twenty-five open items are withdrawn from the Status section, section 1.1, the Rev D and Rev E notes, section 11, section 12 item 13 and the Annex A letter, and the **not released for fabrication** status is replaced by **released for review under RFQ-EEG-002A, with fabrication release awaiting that review**, the ECO-EEG-016 section 3 gate now being met on all three of its conditions. RFQ-EEG-002A is restated as the smaller line it has become, and the **169 relaxed connections** are stated wherever routing quality is discussed. Unchanged: nothing has been manufactured or measured, no human layout engineer has read the routing, the electrical safety review has not happened, and S-02, S-04, E-23 and E-27 are still not met |
| E | 2026-09-02 | Corrections within Rev E, no revision letter change, fifth pass, against the design changes of the afternoon of 2 September. **S-02 is met**: ECO-EEG-024 is applied, R1--R16 are 68 kΩ, single-fault DC is 36.8 µA (bare-resistor bound) and 30.0 µA (measuring-device bound) against 50 µA, and the 53.2 µA that stood through three revisions is withdrawn. E-10 sits on the ±1.0 dB branch it already states for this case and TST-EEG-004 T22 grades against it; E-03's live noise figure is 0.31 µV; E-07 states 68 kΩ; E-30 and the section 9.1 leakage and partial-coverage entries are restated with it. **E-27 is met**: the bicolour phase driver is written, reading both `LOFF_STATP` and `LOFF_STATN`, and alternating at about 250 Hz because the phase quantises to the FreeRTOS tick. **E-11's low-pass half is met** by the C0G Sallen-Key. **The firmware is built** under ESP-IDF v5.2.5 for esp32s3 and has been run once under QEMU; the "never compiled … five driver stubs" of section 5 and section 12 item 12 is withdrawn on both halves. **E-26 and M-02 are corrected**: the three button openings are 12.4 mm on a 14.0 mm pitch **in the lid**, not 13.0 mm on the right wall, per `tools/mech_gen.py`. **Section 12 is reconciled against the requirement rows**: items 2, 4 and 15 are marked CLOSED with the date and item 12 restated, each keeping its number and its history; items 1, 3, 5 to 11, 13 and 14 are untouched and open; the closing "order these close in" paragraph is rewritten around the two that closed. **Unchanged, and stated again because the rest of this row could be misread**: nothing in this package has been manufactured, assembled or measured, no human layout engineer has read the routing, no safety engineer has reviewed the design, RISK-EEG-011 SR-01 is open for that reviewer's written disposition, and S-04 and E-23's 45 °C-inhibit half are still not met |
