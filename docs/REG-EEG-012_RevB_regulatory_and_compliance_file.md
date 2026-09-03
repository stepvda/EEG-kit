# REGULATORY AND COMPLIANCE FILE -- EEG FIELD KIT

**Document:** REG-EEG-012  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this
document and design.py disagree, design.py governs.

**Rev B in one line:** the carrier is now 150.0 x 130.0 mm on **four** layers and POD-P1 has
grown with it, so the RoHS scope, the EUT description and the creepage clause are restated;
every production-test citation is taken from TST-EEG-004 Rev C rather than invented; the
HM-07 / HM-08 / HM-10 part names are corrected; there are **fourteen** patient terminations,
not thirteen; the lithium section keeps the obligation and hands the procedure to
PKG-EEG-015 section 7; and S-02, E-29, F-06, A-04 and the serial-number format are brought
into line with the package rulings of 2026-09-01. **The findings of the second
cross-document audit of 1 September 2026 are closed in this issue**: clause 8.5.2's creepage
argument now cites the DRC report as its evidence instead of asserting the premise, S-04 and
E-23 are separated and each stated at its true status, and every document cited here carries
its current revision letter. **Corrections within Rev B, after the verification review of
package v2.1 of 1 September 2026**: section 3.1 now says which documents actually match the
no-spare-cell decision and which one does not, section 3.4 carries the CASE-00 Rev C
seven-layer foam insert in place of the withdrawn two-sheet one, section 3.8 hands the whole
cell-replacement policy to SVC-EEG-013 section 2 R9 instead of stating a second and
different one, and section 6.1's reuse figure is restated from SVC-EEG-013 section 3.5 and
RISK-EEG-011 section 1.4. **Corrections within Rev B, after the routing closed on 2026-09-01**:
the DRC report now records zero violations with all 145 nets connected and both inner planes
continuous, so the introduction, section 4.2, clause 8.5.2, section 8 item 18 and section 9
items 1 and 10 are restated -- the fabrication data is released for review under RFQ-EEG-002A
and is still not released for fabrication, because no human layout engineer has reviewed the
routing, which closed 169 connections at relaxed geometry. S-02, S-04 and E-23 are untouched by
the routing and stay exactly as section 9 records them. **Corrections within Rev B, after the
independent review of package v2.2 of 2026-09-02**: section 3.4 is restated against what
`mech/` now holds -- the seven CASE-00 Rev C layer cut files are shipped and the Rev B pair is
deleted -- while keeping the true half of that row, which is that they are not released for
cutting and no insert has been cut; and section 9's simulation figures are quoted from the run
of `tools/simulate_production.py` of 2 September 2026 rather than from an earlier one.
**Corrections within Rev B, after the design and firmware changes of 2026-09-02**: three
statuses this file carried as not met are now met in the design and are corrected in place,
with their date, wherever they appear -- **S-02** (ECO-EEG-024 applied, R1-R16 are 68 kΩ,
single-fault DC 36.8 µA against 50 µA: clause 4.7, clause 8.4.2, section 8 item 21 and
section 9 item 5), **E-27** (the bicolour contact-light phase driver is written: section 4.3
mode M5, section 8 item 18, clause 14) and **E-11** (the Sallen-Key moved from X7R to C0G).
The firmware has also been **built** for the first time, against ESP-IDF v5.2.5, and has
booted once under QEMU; clause 14 is restated for that. **None of these is a measurement, a
test or an approval**: no unit exists, nothing has run on hardware, no fault-insertion or
emissions testing has been done, and no safety or notified reviewer has looked at any of it.
The revision letter of this file does not change; these are corrections within the same release.

## Why this document exists

The v1 package carried its entire regulatory position in eleven words on a label and two
one-line requirements. "Research instrument -- not a medical device" appeared twice, in
RFQ-EEG-001 Rev C M-03 and in DSN-EEG-002 section 7, with no declaration, no reasoning and
no controlled wording; S-05 asked for ISO 10993 declarations without naming a material, a
supplier or an acceptance criterion; S-06 asked for a CISPR 11 pre-scan with no test plan
and no place in production; S-08 asked for a RoHS and REACH declaration with no template;
and S-04 asked for a UN 38.3 report to be "available" for the cell. Nothing anywhere in the
v1 package mentioned how a box containing a lithium cell gets from a factory to Brussels, to
a stranger's home and back again. The 14-agent audit of v1 raised that as a blocking finding
(`lithium-shipping-dossier`) alongside `not-a-medical-device-declaration`,
`rohs-reach-declarations`, `emc-prescan-plan`, `biocompatibility-dossier`,
`cell-qualification-evidence` and `ethics-dpia-configuration-link`. This file closes all
seven. It states what the programme is legally obliged to do, who does it, what evidence is
kept, and what has not been done.

**Two things changed in the hardware while package v2 was being laid out, and both reach
this file.** The carrier grew from 130 x 124 mm to **150.0 x 130.0 mm**, because thirty
connectors, 211 parts and 156 nets would not close at the smaller size. And the carrier went
from two layers to **four** -- L1 signal, L2 reference plane, L3 reference plane, L4 signal.
Package v1 asserted that a two-layer carrier would be cheap and easy to route; actually doing
the layout showed that it is not, because on two layers the bottom side has to be both the
reference plane and the second routing surface and it cannot be both. Four layers give two
full routing surfaces and a continuous reference under every analogue trace, which is what
the isolation, star-point and reference-plane rules of DSN-EEG-003 section 3.3 require and
what a swiss-cheesed two-layer pour cannot deliver. The enclosure grew to match: POD-P1 base
163.0 x 143.0 x 58.0 mm external, 158.0 x 138.0 x 55.5 mm internal, and the MP-01 module
plate 146.0 x 126.0 x 3.0 mm. Three things in this file follow from that and are marked
where they occur: the RoHS declaration now has to cover a multilayer laminate rather than a
double-sided one (section 2.2 and 2.3), the equipment under test for the EMC pre-scan is a
different physical object (section 4.2), and the isolation keep-out that carries the creepage
argument has to be copper-free on **four** layers rather than two (section 5, clause 8.5.2).
That last one is a fact about the artwork, so it is checked against the DRC report and quoted
from it rather than asserted.

**The routing exists, it closes, and it is released for review and not for fabrication.**
`kicad/EEG-CAR-01_RevB_DRC_report.txt` is the authority for the state of the layout, and this
file quotes it rather than paraphrasing it. It records a four-layer 150.0 x 130.0 mm board with
3 745 track segments and 552 through vias, each reference plane one continuous island per net,
**all 145 nets fully connected** and **zero violations of any rule**. That meets all three
conditions of the fabrication-release gate in ECO-EEG-016 section 3, so the data in `kicad/` is
**released for review under RFQ-EEG-002A**. It is **not released for fabrication**: the routing
was produced by the programme's own tools, no human layout engineer has looked at it, and the
router closed 169 connections at relaxed geometry. Section 9 item 10 carries the full figures.
Nothing in this file may be read as saying that a board has been made or that anything on it
has been measured.

Nothing in this package has been manufactured, shipped, scanned or tested. **No safety
engineer has reviewed this design.** Every limit below is an acceptance criterion, not a
result. Where a figure is derived rather than measured it is labelled *calculated*.

---

## 1. Regulatory status

### 1.1 The declaration

The TI One Voice EEG field kit is a research instrument built by, and for, a single
pre-registered study. It is **not a medical device within the meaning of Regulation (EU)
2017/745 (MDR)**, it is **not placed on the market**, and it bears **no CE mark**.

The instrument is loaned, never sold and never transferred in ownership. It is issued only
to a person who has consented to a specific study protocol, is used only for the recording
sessions that protocol defines, and is returned. It returns no result of any kind to the
participant during or after a session. The study's findings are published as pre-registered
group results.

### 1.2 The reasoning, written out

MDR Article 2(1) defines a medical device by its intended purpose as stated by the
manufacturer. The programme is the manufacturer, and the intended purpose it states is: *to
acquire sixteen channels of electrophysiological signal with co-registered audio for the
purposes of a research study, under a protocol approved by an independent ethics committee*.
That purpose contains no diagnosis, no prevention, no prediction, no prognosis, no
monitoring of a disease or condition in an individual, no treatment and no alleviation.
Nothing the device produces is looked at by a clinician, is entered in anyone's health
record, or is returned to the individual as information about themselves.

Two further points have to be handled explicitly, because a reviewer will ask about both.

**MDR Article 5(5), in-house manufacture.** This is the exemption a health institution uses
when it makes and uses a device on its own patients. It does not apply here and is not
relied upon: the programme is not a health institution, and the participants are not its
patients. The programme's position is that the device falls outside MDR entirely on the
intended-purpose test of Article 2(1), so no exemption is needed. Article 5(5) is named here
only so that the record shows it was considered and set aside.

**Clinical investigation.** MDR Articles 62 and 82 govern clinical investigations of
devices. Article 62 covers investigations run to demonstrate conformity for a CE mark; that
is not what this is, because no CE mark is sought and no conformity claim is made. Article
82 covers other clinical investigations of devices, and its detailed rules are set by
national law. The study is a research study using an instrument, not an investigation of the
instrument. **This determination is the ethics committee's to make, not the programme's**,
and it is submitted to the committee as an explicit question in ETH-EEG-001. If the
committee or the Belgian competent authority classifies the study otherwise, this section is
revised by ECO before any unit is issued to a participant.

### 1.3 Reconciliation with IEC 60601-1

RFQ-EEG-001 Rev E section 8 says the instrument is designed to the applicable principles of
IEC 60601-1 for a type BF applied part, and Annex A lists IEC 60601-1 and IEC 60601-2-26 as
design references. Read carelessly, that looks like a medical claim sitting next to a denial
of one. It is not. The device is connected to a person's scalp, so the programme borrows the
engineering discipline that exists for exactly that situation: series resistance in every
electrode lead, a galvanic barrier to any mains-referenced host, battery-only recording,
touch-proof electrode connectors. Borrowing the design principles of a standard is not a
claim of conformity to it, and conformity to IEC 60601-1 would not by itself make anything a
medical device. Section 5 below sets out, clause by clause, which of those principles the
design actually meets and which it does not.

### 1.4 Controlled wording

These strings are controlled. They change only by ECO under ECO-EEG-016, and any change
re-triggers the label artwork in PKG-EEG-015 and a notification to the ethics committee.

| Where | Exact text | Owner |
|---|---|---|
| Enclosure label, line 4 (ART-LBL-01, per ASM-EEG-007 stage 6 and RFQ M-03) | `RESEARCH INSTRUMENT -- NOT A MEDICAL DEVICE` | PKG-EEG-015 artwork |
| Participant quick-start card (RFQ A-06) | "This is a research instrument, not a medical device. It cannot detect, confirm or rule out anything about your health or your experiences, and nobody will read your recording as a test result." | IFU-EEG-014 |
| Participant information sheet and consent form | "The headset records electrical activity from your scalp and sound from a microphone. It is a research instrument. It is not a medical device, it is not a diagnostic test, and the recording will not tell you or anyone else whether what you experience is real, imagined, or caused by anything in particular. You will not be given an individual result." | ETH-EEG-001, ethics submission |
| Commercial invoice and customs declaration | "Non-medical research instrument, loaned scientific equipment, not for sale, not for clinical use. Value declared for customs purposes only." | Section 1.5 |
| Website, repository README, public posts | "A research EEG instrument built for one pre-registered study. It is not a medical device and gives no individual result." | Programme lead |
| Manufacturer's own material | The bidder may not describe this instrument as medical, clinical, diagnostic or medical-grade in any catalogue, case study, website or tender reference. This clause goes in the purchase order terms | Purchase order |

**Prohibited words** anywhere in participant-facing or public material: *diagnostic,
diagnosis, clinical, medical-grade, therapy, therapeutic, treatment, screening, patient,
monitor* in a clinical sense. Use *participant*, not *patient*. The single retained
exception is the standard's own term "patient auxiliary current" in RFQ S-02 and in section
5 below, where changing it would misname a defined quantity.

### 1.5 Customs

Tariff classification and regulatory status are different questions and must not be
conflated. An EEG amplifier classifies under HS heading 9018 (instruments and appliances used
in medical, surgical, dental or veterinary sciences), most plausibly 9018.19, and that is a
duty and statistics question decided by the declarant and the customs broker. Declaring 9018
does not make the instrument a medical device under MDR, and the invoice text in section 1.4
says so on the same page.

> **Open.** The HS code has not been confirmed with a broker. Getting it wrong risks a
> health-authority hold on arrival in Brussels, which is exactly the delay a Phase 2 build
> cannot absorb. The programme confirms the code with its broker before the first
> international despatch. Owner: programme lead.

---

## 2. RoHS 3 and REACH

### 2.1 What actually applies

RoHS (Directive 2011/65/EU as amended by (EU) 2015/863, commonly "RoHS 3") is triggered by
placing electrical and electronic equipment on the market. The kit is not placed on the
market, so RoHS is not a legal obligation on the programme. The research-and-development
exclusion in Article 2(4)(j) is *not* relied on either, because it is limited to equipment
made available business-to-business and these kits go to private individuals. The programme
therefore requires RoHS 3 conformity **contractually**, through RFQ S-08, and holds the
evidence in the same form the Directive would require. The reason is practical: partner
institutions, university compliance offices and the ethics committee ask for it, and a fleet
that cannot answer is a fleet that stops.

REACH (Regulation (EC) 1907/2006) Article 33 places a communication duty on any supplier of
an article containing a candidate-list substance of very high concern above 0.1 % w/w. The
programme treats loaning a kit to a participant as supply for this purpose, which is the
conservative reading, and therefore holds article-level SVHC information and passes the
required statement to the participant in IFU-EEG-014.

### 2.2 The RoHS declaration the manufacturer completes

One declaration per phase, signed by an officer of the manufacturer, covering every item the
manufacturer buys, builds or packs.

| Substance | Maximum concentration by weight in a homogeneous material |
|---|---|
| Lead (Pb) | 0.1 % |
| Mercury (Hg) | 0.1 % |
| Cadmium (Cd) | 0.01 % |
| Hexavalent chromium (Cr VI) | 0.1 % |
| Polybrominated biphenyls (PBB) | 0.1 % |
| Polybrominated diphenyl ethers (PBDE) | 0.1 % |
| Bis(2-ethylhexyl) phthalate (DEHP) | 0.1 % |
| Benzyl butyl phthalate (BBP) | 0.1 % |
| Dibutyl phthalate (DBP) | 0.1 % |
| Diisobutyl phthalate (DIBP) | 0.1 % |

Required fields: manufacturer legal entity and address; the covered items listed by BOM item
number and by carrier reference designator range; the standard applied (**EN IEC
63000:2018**, technical documentation for the assessment of electrical and electronic
products with respect to the restriction of hazardous substances); the evidence tier per
item; every exemption claimed, by Annex III or Annex IV number and expiry date; date;
signatory name, position and signature.

**The bare board is now a four-layer laminate and the declaration must say so.** EN IEC 63000
tests each *homogeneous material* separately, and a four-layer EEG-CAR-01 has more of them
than the two-layer board of package v1: the two prepreg plies at 0.200 mm, the 1.065 mm core,
the 17 µm inner copper on L2 and L3, the 35 µm outer copper on L1 and L4, the solder mask
both sides, the legend ink and the ENIG finish. The fabricator declares the laminate system
by trade name and grade, states the flame-retardant chemistry (see section 2.3), and confirms
that the declaration covers the inner plies and not only the outer surfaces. A declaration
written against a double-sided board is not evidence for this one.

**Evidence tiers, in descending order of acceptability:** (1) supplier declaration plus
material declaration data to IEC 62474; (2) supplier declaration alone; (3) analytical test
report from an accredited laboratory. The manufacturer states which tier applies to each
item. The programme accepts tier 2 for passives and mechanical parts and requires tier 1 or
3 for anything in section 2.3.

The manufacturer must state, item by item, **which of the twelve purchased module types they
can evidence and which they cannot**. Twelve types are bought; **thirteen module assemblies
go into each unit**, because the ADS1299 breakout is fitted twice, and the declaration is per
type. Consumer breakouts bought from a maker-market vendor frequently carry no RoHS statement
at all. An honest "cannot evidence" against the microSD breakout at J20 is acceptable and is
recorded as a residual; a blanket "all compliant" covering twelve module types with no
supporting documents is not, and is rejected.

### 2.3 Substances of concern actually present in this BOM

| Item | Concern | Position |
|---|---|---|
| EEG-CAR-01 bare board, four-layer FR-4 (mask / 35 µm L1 / prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask, 1.60 mm ± 10 %) | Brominated flame retardant in the laminate and in both prepreg plies | Standard FR-4 uses TBBPA reacted into the epoxy network, which is **not** a PBB or a PBDE and is therefore outside the RoHS list; the fabricator states this explicitly rather than leaving it to be assumed, names the laminate grade, and declares the mask, the legend ink and the ENIG chemistry. A halogen-free build is not required and is not requested |
| J15--J17 DIN 42802 sockets, touch-proof 1.5 mm, Stäubli SLB1,5-F class | Lead in the brass or copper-alloy socket body. Lead is on the REACH candidate list (CAS 7439-92-1, added 27 June 2018) and free-machining brass commonly exceeds 0.1 % w/w in that homogeneous material | RoHS exemption 6(c) (copper alloy containing up to 4 % lead) is expected to be claimed. Must be **declared, not assumed**. **The part itself is open:** `design.py` names Stäubli SLB1,5-F as a class, not a confirmed PCB-mount part, and no catalogue part has been confirmed to fit a PCB-mount signal pin with two 1.5 mm retention posts. AVL-EEG-017 carries a 12-week first-article lead time against it, and the declaration cannot be requested until the part is chosen |
| Harness jacket, headphone cable (item 29), USB cables (item 32), charge pigtail to J24 | Phthalates DEHP, DBP, BBP, DIBP in flexible PVC | Require a phthalate-free jacket, or a declaration with test data. This is the single most likely RoHS 3 failure in the kit |
| Solder in the twelve purchased module types | Lead in solder | Exemptions 7(a) and 7(c)-I may apply to some parts. Modules bought as consumer breakouts are the weak point |
| HM-01, HM-03, HM-04, **HM-07 boom arm**, **HM-08 battery hatch**, MP-01 module plate and POD-P1 in MJF PA12 dyed black | The dye and any surface treatment | Bureau declares the polymer grade, the colourant and the post-process chemistry. Section 6 needs the same declaration for a different reason, for the printed parts that touch skin |
| HM-02 TPU 85A pads and HM-06 chin strap and liner | Plasticiser and colourant in a part held against the forehead and chin for two hours | Tier 1 or 3 evidence required |
| 5 V 2 A EU charger (item 33) and USB cables (item 32), both currently "certified generic" | Nobody knows who made them | See section 2.5. These are the two items in the kit that most need a real CE and RoHS chain and currently have the least |
| Protected 18650 cell (item 11) | Cadmium and lead limits under the EU Battery Regulation | Supplier RoHS and REACH declarations required with the UN 38.3 summary of section 3 |
| ENIG finish on EEG-CAR-01, Au 0.05--0.10 µm over Ni 3.0--6.0 µm | Nickel release is a REACH Annex XVII restriction for prolonged skin contact | Not applicable: the carrier is inside a closed pod and touches nobody. Recorded so the question is not asked twice |

### 2.4 SCIP

If any article in the kit contains a candidate-list SVHC above 0.1 % w/w, a SCIP
notification to ECHA is due from the **EU-established supplier placing the article on the EU
market**, which is the programme as importer, not a manufacturer outside the EU. The
programme's position, to be recorded as a decision by the programme lead once the section 2.3
declarations are back:

- If the DIN 42802 socket bodies exceed 0.1 % w/w lead, they are articles in scope and a
  SCIP notification is prepared, or a lead-free alternate is approved through AVL-EEG-017.
- If no article exceeds the threshold, the decision "no SCIP notification due" is recorded
  with the declarations that support it, and re-checked at each candidate-list update.

The candidate list is revised roughly twice a year. **Every declaration must state the
candidate-list version and date it was checked against.** A declaration that says only "REACH
compliant" is worthless and is rejected.

### 2.5 EU importer position, WEEE, batteries and packaging

At Phase 2 and 3 the programme imports 10 to 50 assembled kits into Belgium from a supplier
that may be outside the EU. That makes the programme the importer of the components it does
not manufacture, and one of them, the 5 V charger, is a mains-connected consumer good;
the USB cables are accessories carried on their own supplier declaration.

| Obligation | Position |
|---|---|
| CE mark on the kit as a whole | **None, and none is applied.** The kit is not placed on the market. See section 1 |
| 5 V 2 A EU charger (item 33) | The programme requires the actual manufacturer's EU Declaration of Conformity to the Low Voltage Directive 2014/35/EU and the EMC Directive 2014/30/EU, the supporting test reports, and a CE mark traceable to a named legal entity. **"Certified generic" is not acceptable.** If the bidder cannot supply this, the item is replaced with a named-brand charger through AVL-EEG-017 |
| USB cables (item 32) | Named part, supplier declaration, RoHS tier 2 minimum. Two cables ship per kit under RFQ A-07 and **one of them is the host lead**, because the host connection is a socket on the ADuM4160 module and not a captive cable |
| WEEE, Directive 2012/19/EU | The fleet reaches end of life as electronic waste in Belgium. The programme registers with, or disposes through, the Belgian scheme (Recupel) at end of programme. No WEEE crossed-bin symbol is applied to the kit, because it is not placed on the market; the disposal obligation is discharged directly |
| Batteries, Regulation (EU) 2023/1542 | Take-back and disposal of the fleet's cells through the Belgian collection scheme (Bebat). A cell is never disposed of by a participant. See section 3.8 |
| Packaging, Directive 94/62/EC | Outer carton and PE foam are recyclable, minimised and declared. PKG-EEG-015 owns the carton specification |

### 2.6 Production line audit, from S-08

The bidder answers these on the quotation, as a form rather than as prose:

| Question | Answer required |
|---|---|
| ISO 9001 certificate | Number, certifying body, expiry |
| ISO 13485 | Held or not held. **Not required and not wanted** -- see QP-EEG-010 section 1.2 |
| IPC-A-610 class 2 operator certification | How many certified operators, certificate references. IPC-6012 class 2 and IPC-A-600 class 2 apply to the bare four-layer board and IPC-A-610 class 2 to the assembly; all three are required |
| Multilayer capability | Four-layer FR-4, 1.60 mm ± 10 %, through vias only at 0.60 mm pad on a 0.30 mm finished hole. No blind, buried, back-drilled, filled or plugged vias are used or accepted |
| ESD control programme | ANSI/ESD S20.20 or IEC 61340-5-1, with the EPA boundary described. This matters directly for the ADS1299 front end, the sixteen input networks -- 68 kΩ since ECO-EEG-024 was applied on 2026-09-02, 47 kΩ before it -- and U1--U3 |
| Any other audited standard | Named |

---

## 3. The lithium cell

This section governs every kit despatch. It is new in package_v2.2; the v1 package never
mentioned lithium transport once.

**Scope of this section, stated once.** REG-EEG-012 section 3 states **the obligation**: what
the article is, how it classifies, what evidence must exist, what conditions the consignment
must satisfy and who must be trained. **The procedure lives in PKG-EEG-015 section 7** -- the
packing steps, the tick sheet, the artwork, the carrier terms, the return-label mechanics and
the depot storage rules -- and is not restated here. Production evidence that the obligation
was actually discharged on the unit that left the building is TST-EEG-004 Rev C step **T29**.
Where this section and PKG-EEG-015 section 7 could drift, this section states the rule and
PKG-EEG-015 states how it is carried out.

### 3.1 The article, classified

| Property | Value |
|---|---|
| Cell | Protected 18650 Li-ion, one per kit, kit BOM Rev B item 11 |
| Reference parts | Panasonic NCR18650B in a protection sleeve, or Samsung INR18650-35E in a protection holder |
| Nominal voltage | 3.6 V |
| Rated capacity | ≥ 3000 mAh required by RFQ E-22; 3400 mAh (NCR18650B) or 3500 mAh (35E) as quoted |
| Watt-hour rating, *calculated* | 3.6 V × 3.4 Ah = **12.24 Wh**; 3.6 V × 3.5 Ah = **12.6 Wh** |
| Article | A single **cell**, not a battery. Under 20 Wh, so section II of the packing instruction applies |
| Cells per kit | 1, installed at J13 in the **HM-10 keyed cell carrier**, behind the **HM-08 quarter-turn battery hatch**. HM-07 is the boom microphone arm and has nothing to do with the cell (PARTS-EEG-019 section 3.1) |
| Spare cells per kit | **None.** See the decision box below |
| Proper shipping name | Lithium ion batteries contained in equipment |
| UN number | **UN3481** |
| Class | 9 (miscellaneous), lithium battery |

> **Decision, recorded.** DSN-EEG-002 Rev E section 7 said "a charged spare travels in the
> case, so a flat cell never ends a session". That spare has been **removed**. A loose
> charged cell in the foam changes the consignment from UN3481 *contained in* equipment
> (PI967) to UN3481 *packed with* equipment (PI966), with different packing, marking and
> quantity rules, and it puts an unprotected Li-ion cell in a stranger's home. The
> compensating controls are RFQ E-22's four hours of recording at 1000 Hz against a session
> of about two hours, and the 5 V 2 A charger of A-07 in the case. **RFQ-EEG-001 Rev E S-09
> matches this box**: it ships every kit as UN3481, cell inside equipment, and names no
> spare. **DSN-EEG-002 Rev E does not.** Its section 7 still carries the sentence quoted
> above, and ECO-EEG-016 section 1.1 records that the file was not reissued in this
> correction round, so it is wrong on the spare exactly as it is wrong on the boom
> preamplifier. Where they disagree this box governs, RISK-EEG-011 section 6.1 rules the
> same way, and DSN-EEG-002 section 7 is corrected at its next issue. The foam bay legended
> `SPARE CELL` stays in the CASE-00 insert -- Rev C keeps it -- and travels **empty** in
> circulation; PKG-EEG-015 sections 2.2 and 7 govern that bay and its tag. Anyone
> reinstating the spare must re-open this section and PKG-EEG-015 section 7.

### 3.2 Cell qualification evidence

Held before the first purchase order is released, and re-checked whenever the cell part
number changes. This closes RFQ S-04 and the audit finding `cell-qualification-evidence`.

| Evidence | Standard or source | Held by | Acceptance |
|---|---|---|---|
| UN 38.3 test summary | UN Manual of Tests and Criteria, sub-section 38.3, summary format of 38.3.5 -- mandatory to make available since 1 January 2020 | Programme, copy to manufacturer | Must name the cell manufacturer and contact, the test laboratory and contact, a unique test report identifier, the date of the summary, a description of the cell (mass, Wh, chemistry), the list of tests **T.1 altitude, T.2 thermal, T.3 vibration, T.4 shock, T.5 external short circuit, T.6 impact or crush, T.7 overcharge, T.8 forced discharge** with results, the revision of the Manual it was tested to, and a signature. A summary missing any of these is rejected |
| Safety certificate | IEC 62133-2:2017 + AMD1:2021 certificate or full test report | Programme | Certificate number, body, scope naming the exact cell model. UL 1642 accepted in addition, not instead |
| Safety data sheet | Cell manufacturer SDS | Programme, carried with each consignment | Current version, in English, with the emergency telephone number |
| Protection circuit specification | Cell or holder supplier datasheet | Programme | Over-charge cut-off, over-discharge cut-off, over-current and short-circuit trip and recovery, all as numbers. The PCM is a protection means, not the only one: the bq24074-class charger and the two independent interlocks of RFQ S-01 are the others |
| RoHS and REACH declarations | Section 2 | Programme | Per section 2.2 |
| Certificate of conformity | Per lot | Manufacturer | Lot code, date code, quantity, recorded per unit in the device history record per RFQ section 10 |
| Incoming inspection | QP-EEG-010 | Manufacturer | Open-circuit voltage at receipt, wrapper and vent inspection, date code, lot |

> **Open, and it is a hardware hole, not a paperwork hole. Two requirements, at two different
> statuses.** RFQ **S-04** requires thermistor-monitored charging. RFQ **E-23**, restored at
> Rev D and carried in **RFQ-EEG-001 Rev E**, requires a charger IC with thermal regulation and
> **no charging above 45 °C**. Cite S-04 for the thermistor and E-23 for the temperature; they
> are two requirements, not one, and the ruling that separates them is RUL-EEG-021 section B.
>
> **S-04 is not met, and it stays not met.** There is **no NTC net in `design.py`**. The eight
> ways of J12 are VBAT, DGND, VBUS_CHG, CHG_CE, SDA, SCL, VSYS and NC_CHG_STAT, and J13 is a
> two-way cell connector carrying VBAT and DGND, so no thermistor way exists on either
> connector in the Rev B netlist. Nothing measures the cell's temperature, and no test can be
> written that would.
>
> **E-23 is met only in part, and the missing part is the part that matters here.** The
> bq24074-class charger module at J12 regulates its own die temperature, so the "charger IC
> with thermal regulation" half of E-23 is met on the module. The 45 °C inhibit rests on that
> same die-temperature regulation alone: it protects the charger, not the cell, and with no NTC
> the charger cannot know the cell's temperature. TST-EEG-004 Rev C step T4 records that the
> 45 °C inhibit is not tested and cannot be. So E-23 is met in part, is not verified, and is
> not closed.
>
> Closure is either a thermistor added to the charger module's temperature-sense pin by ECO,
> or the 45 °C limit met another way with the alternative written down. The open item is
> carried in DSN-EEG-003 section 11 and in RISK-EEG-011. Owner: programme technical lead,
> before Phase 2.

### 3.3 The three shipping configurations

The rules below are stated as understood at **IATA DGR 67th edition (2026)** for air, **ADR
2025** special provision 188 for road, and **IMDG amendment 42-24** for sea. Editions change
every January. The programme's trained dangerous-goods shipper re-verifies this section
against the edition in force before each phase's despatch, and records the check.

| | **A: manufacturer to Brussels** | **B: Brussels to participant** | **C: participant to Brussels** |
|---|---|---|---|
| Contents | 2 to 50 kits in outer cartons, one cell installed per kit | One kit, one carton, one cell installed | Same kit returned |
| Classification | UN3481, PI967 section II | UN3481, PI967 section II | UN3481, PI967 section II |
| Legal shipper | Manufacturer | Programme | **The participant.** This is the hard case |
| Packages per consignment | More than two | One | One |
| Lithium battery mark | **Required** (more than two packages) | Not required by the small-consignment relief; **applied anyway** as programme policy, because couriers' own acceptance conditions vary and an unmarked lithium package gets refused at the counter | Applied at despatch and reused on the return leg |
| Shipper's declaration for dangerous goods | Not required for section II | Not required | Not required |
| Mode | Air, sea or road as quoted. Sea is cheapest and slowest; the DG rules are equivalent | Road courier within the EU | Road courier |

The "applied anyway" policy is one decision, written here as the rule and in PKG-EEG-015
section 7 as the packing step. Neither document may state it differently: the mark goes on
**every** carton on **every** leg, whether or not the relief would allow its omission.

**Configuration C is the one that has to be engineered, not just documented.** The
participant is legally the shipper of a dangerous good and cannot discharge a shipper's
obligations: they are not trained, they cannot classify, and several carriers will not accept
lithium over a retail counter at all. Options considered:

| Option | Verdict |
|---|---|
| (a) Prepaid, pre-classified courier return label in the M-07 carton pocket, on a programme account with a lithium-approved service; carton already carries the lithium battery mark from the outbound leg; participant seals the carton and hands it over | **Adopted.** The participant writes nothing, classifies nothing and declares nothing. The mechanics are in PKG-EEG-015 section 7 |
| (b) Courier collection booked by the programme from the participant's address | **Adopted as the fallback** where the participant cannot reach a drop-off point, and as the default for any kit reported damaged |
| (c) Participant removes the cell through the HM-08 battery hatch and keeps it; kit returns as non-lithium | **Rejected.** It leaves a loose Li-ion cell in a stranger's home with no protective case and no disposal route |
| (d) Postal despatch | **Rejected.** Universal Postal Union and Belgian postal rules restrict lithium in the post, and international post is largely closed to it. The programme uses a courier account, not the post |

### 3.4 Section II conditions the packed kit must meet

Every one of these is a condition of shipping, not an optional good practice. **PKG-EEG-015
section 7 turns the whole of this table into a packing procedure with a tick sheet and a
sign-off, and TST-EEG-004 Rev C step T29 confirms on the closed kit that it was done.**
Neither the procedure nor the tick sheet is repeated here.

| Condition | How this kit meets it |
|---|---|
| Cell passed UN 38.3 | Section 3.2 evidence held; summary made available on request |
| Cell ≤ 20 Wh | 12.24 or 12.6 Wh *calculated* |
| Cell installed in the equipment | At J13, in the HM-10 keyed cell carrier, behind the closed HM-08 battery hatch |
| Equipment protected against short circuit | The HM-10 carrier cannot accept the cell reversed; the PCM is on the cell; the charge input at J24 is behind a 1.1 A PTC (F1) and a transient suppressor (D24) |
| Equipment protected against accidental activation | The instrument starts only on a deliberate button press. There is no auto-start path. SW1--SW3 sit under their caps and silicone boots, inside a closed pod, inside foam, inside a closed IP67 case, inside a sealed carton. There is **no hatch interlock** anywhere in this design and none may be claimed |
| Secured against movement in the outer packaging | The CASE-00 **Rev C** die-cut PE foam insert of PKG-EEG-015 section 2.2 -- seven loose-laid 25 mm layers, 175 mm of stack, nine bays, every bay at least 3 mm larger than its part on every axis -- with the kit inside the case and the case inside the double-wall carton per M-07. RFQ M-05 requires a die-cut or laser-cut closed-cell PE insert and does not fix the layer count. The two-sheet insert this row named at the first issue of this revision is superseded: PKG-EEG-015 section 2.4 shows it cannot hold the helmet, the pod or the headphones at any arrangement. The seven **Rev C cut files are drawn and shipped** in `mech/` -- `CASE-00_foam_layer_1.dxf` to `_7.dxf`, the two Rev B sheets deleted -- and they are **not released for cutting** until the bought shell is measured (PKG-EEG-015 section 3.2), so **no insert has been cut** and this condition is met on the schedule and not yet on an insert |
| Strong rigid outer packaging | Double-wall carton, M-07. **The Nanuk or Peli case is not the shipping container** and M-05 says so |
| 1.2 m drop test on the completed package | **Not yet performed.** See section 3.6 |
| Lithium battery mark | Section 3.5 |
| Net quantity limit per package | One 48 g cell against a limit measured in kilograms. Not approached; the shipper confirms the exact limit in the edition in force |
| Trained shipper | Section 3.7 |

### 3.5 The marks the regulation requires

The obligation is here; the artwork, its dimensions on the printed sheet, its placement on the
carton and the label set it belongs to (ART-LBL-06) are in PKG-EEG-015 sections 4.2 and 7.

| Mark | What the regulation requires |
|---|---|
| Lithium battery mark | Rectangular, hatched border, **120 mm wide × 110 mm high**, reduced to not less than 105 mm × 74 mm only where the package is too small for the full size. Carries the text "UN3481" and a telephone number for additional information |
| Telephone number in the mark | A number that is answered, by someone who can give information about the shipment, during the carrier's operating hours. **Not a voicemail box.** The programme operations number is used |
| Class 9 lithium battery hazard label | **Not applicable** to section II consignments and not applied. Applying it wrongly implies a fully regulated shipment and invites refusal |
| Case marking | Nothing dangerous-goods related goes on the Nanuk or Peli case. The case circulates; the carton is consumed |

Any change to the telephone number is an ECO, because it changes a regulatory mark.

### 3.6 Package qualification

PI967 section II requires the completed package to withstand a 1.2 m drop in the orientation
most likely to result in damage, with no damage to the cell, no shifting of contents that
would allow contact between the equipment and the cell or between packages, and no release of
contents.

This test **has not been performed**. It is a Phase 1 activity, run once on a fully packed
kit in its production carton, and the record (date, drop orientations, mass of the packed
carton, photographs, post-drop inspection of the cell and of the kit) is retained for the
life of the packaging design. It is distinct from the RFQ M-04 1 m drop test of the
instrument itself: M-04 asks whether the kit still works, this asks whether the package is
legal to ship. Both are run in Phase 1 on the same unit, in that order, and both are recorded.
The carton design the test qualifies is PKG-EEG-015 section 6, and it is sized for the
enlarged POD-P1 (163.0 × 143.0 × 58.0 mm external) inside the travel case; a package
qualified against the v1 pod is not evidence for this one.

### 3.7 Documents held and training

Held by the shipper for every consignment: the UN 38.3 test summary for the cell; the cell
safety data sheet; the package drop-test record from section 3.6; the packing tick sheet
signed by the packer; the consignment note or air waybill; and, where the carrier requests
it, a written statement that the consignment is UN3481 in compliance with section II of
PI967. Retention: three years, or the carrier's stated period if longer. PKG-EEG-015 section
7 lists the same set as a per-shipment checklist and is the document the packer works from.

**Who is the trained shipper.** Under IATA the shipper's personnel must be trained under a
competency-based training and assessment programme, with reassessment at intervals not
exceeding 24 months. Under ADR chapter 1.3 the consignor's personnel must have function-
specific awareness training, refreshed periodically.

| Role | Person | Training | Refresher |
|---|---|---|---|
| Manufacturer's shipper, configuration A | Named in the quotation. **RFQ-EEG-001 Rev E asks the bidder to name them** | IATA CBTA or national equivalent | Bidder states |
| Programme shipper, configuration B and the return leg's classification | Named individual at the programme, appointed before the first Phase 2 despatch. **Not yet appointed** | IATA CBTA plus ADR 1.3 | 24 months |
| Participant | None, and none is required. Configuration C is engineered so the participant never classifies, marks or declares anything | -- | -- |

### 3.8 State of charge, storage, damaged cells and end of life

**State of charge.** RFQ S-09 requires kits to be despatched at **≤ 30 % state of charge**.
Stated plainly: PI967 section II does not itself impose a state-of-charge limit; the 30 %
limit in the regulations belongs to UN3480 cells and batteries shipped alone by air under
PI965. The programme adopts ≤ 30 % as an **additional self-imposed control**, because a cell
at low charge in a thermal-runaway event releases less energy and because some carriers apply
the limit to all lithium consignments in their own conditions of carriage. The MAX17048 gauge
reading is taken and recorded at despatch under the PKG-EEG-015 section 7 procedure, and the
participant's first instruction in IFU-EEG-014 is to charge the kit before the first session,
with the helmet never worn while the charge cable is connected (RFQ S-01, whose two
independent interlocks are specified once in that requirement and are not restated here).

| Situation | Rule |
|---|---|
| Despatch, all configurations | ≤ 30 % SoC, gauge reading recorded per serial |
| Storage between participants | Cell at approximately 3.7 to 3.8 V, kit in the case, room temperature, checked every 3 months |
| Cell replacement | **Annually on age, whatever the condition**, and at any refurbishment where the bench capacity check reads below 80 % of rated, the rested open-circuit voltage is below 3.5 V after a full charge, the wrapper is swollen or deformed, the protection module is damaged, the kit has been through a reported drop with the cell in it, or the cell's own date code is five years old -- whichever comes first. That list is **SVC-EEG-013 section 2 R9**, which owns it; this row cites it and no longer states a second policy of its own. The "2 years in the fleet" carried here at the first issue of this revision is withdrawn: SVC-EEG-013 section 3.4 already replaces the cell annually, and one cell cannot have two replacement ages. The 80 % figure is **not a gauge reading** -- the MAX17048 is a voltage-based ModelGauge part and reports state of charge, not capacity -- so it is measured off the unit on a bench cell analyser at the every-fifth-turnaround check of SVC-EEG-013 section 3.2, and it is the only trigger in the list that needs an instrument the turnaround bench does not use every time |
| Swollen, dented, leaking, deeply discharged or heat-damaged cell | **The kit is never posted or couriered.** Damaged or defective lithium cells are forbidden for transport by air and are subject to special provisions by road. The participant is instructed to stop, not to charge it, and to telephone the programme; the programme arranges a compliant collection or disposal locally |
| Disposal | Belgian battery collection scheme (Bebat) under Regulation (EU) 2023/1542. **A participant never disposes of a cell.** End-of-programme fleet disposal is a single documented consignment |

---

## 4. EMC

### 4.1 Scope, honestly stated

RFQ S-06 asks for a **CISPR 11 group 1 class B pre-scan on one Phase 1 unit**. This is a
pre-scan, not a certification: no notified body, no declaration, no CE mark. IEC 60601-1-2 is
the EMC collateral standard a medical device would be tested to, and the programme is
deliberately **not** claiming it. Immunity is not tested at all in Phase 1; section 4.5
records why and what the decision costs.

### 4.2 The equipment under test, defined exactly

One Phase 1 unit, complete: routed **four-layer, 150.0 × 130.0 mm** EEG-CAR-01 Rev B carrier
with **all thirteen module assemblies** of the twelve purchased types fitted -- twelve of them,
including both ADS1299 breakouts, on the MP-01 plate (146.0 × 126.0 × 3.0 mm) on M3 × 18 mm
nylon standoffs, and the ESP32-S3-DevKitC-1 inserted directly into J6/J7 as the thirteenth; POD-P1 closed (163.0 × 143.0 × 58.0 mm external); the 12-way screened electrode
cable at J14 and the 10-way light cable at J30 both connected to a printed HM-01 with
electrodes fitted to a saline head phantom; boom microphone on its pigtail at J18; headphones
in the 3.5 mm jack; microSD card fitted at J20; the host USB socket on the ADuM4160 module,
presented through its gasketed aperture in POD-P1, connected through a 2 m cable to a
mains-powered laptop; battery installed.

Two notes on the EUT that change the result if they change:

- The board is four-layer with continuous AGND_REF and DGND reference planes on L2 and L3.
  A pre-scan on a two-layer board is not evidence for this design, and if the layer count
  ever changes back the pre-scan is repeated.
- **No EUT exists yet.** The Rev B routing meets all three conditions of the ECO-EEG-016
  section 3 gate -- zero design-rule violations, every net one connected copper island, both
  inner planes continuous under the analogue zone -- so the fabrication data is released for
  review; it is not released for
  fabrication until the layout review of RFQ-EEG-002A is done (section 9, item 10), and no
  carrier has been made. If that review moves the plane geometry under the analogue zone or the
  routing of the host-side nets, the pre-scan is run on the routing as finally released and the
  report names the Gerber revision it was run on.
- **The host connector is not settled.** RFQ E-24 asks for USB-C, and the named candidate
  isolator module presents USB-B. The interim answer is the short USB-B-to-USB-C panel
  pigtail WH-09, and this is a **live non-conformance**, not a settled design. The pre-scan
  is run on whichever arrangement is fitted, and the report states which, because a panel
  pigtail is a radiating structure.

Configuration variables fixed and recorded before the first sweep, because changing any of
them changes the result: harness routing and dress, cable lengths, laptop on mains versus
battery, table height, and the three orientations measured.

### 4.3 Operating modes measured

Each mode loads a different set of clocks, and a pre-scan that measures only one of them
proves nothing.

| Mode | What is running |
|---|---|
| M1 Idle | Powered, no session. ESP32-S3 at 240 MHz, ADS1299 clocks running |
| M2 Recording to host and card | 1000 Hz, 16 channels, USB bulk out plus one-bit SDMMC writes. The frame payload is **50.7 kB/s** (1015 bytes every 20 ms); RFQ E-20's ≈70 kB/s is the allowance once STATUS and SIGNATURE frames and filesystem overhead are added, and it is the figure the card must sustain. The worst case |
| M3 Audio stimulus | Recording plus I2S to the ES8388 and the headphone amplifier driving the shipped headphone load. RFQ A-04 is restated as 32 to 64 Ω and the shipped ATH-M20x is **47 Ω**, so the bench load is 47.0 Ω |
| M4 Lead-off excitation | The ADS1299 lead-off current sources active during set-up |
| M5 Contact lights | Shift register clocking, eight bicolour LEDs alternating at **240 Hz** (`LIGHT_PHASE_HZ`) for amber. **Corrected 2026-09-02: the bicolour phase driver is written**, so M5 can be run as specified once a unit exists. Until that date `lights_write()` and `lights_task()` were on/off only and this row said the mode could not be run. The driver alternates a green and a red phase from both halves of the converter's lead-off word; the half-phase quantises to the FreeRTOS tick, so the emitted alternation is **about 250 Hz rather than exactly 240**, which is the figure the EMC engineer should expect to see in the plots. No unit exists, so **M5 has never been run** |
| M6 Charging, no session | VBUS present at J24, buck-boost and charger switching, session refused by both interlocks |

### 4.4 Ranges, detectors and the pass criterion

| Measurement | Range | Detector | Limit |
|---|---|---|---|
| Conducted, on the host USB lead and on the charge lead in M6 | 150 kHz to 30 MHz | Quasi-peak and average | CISPR 11 group 1 class B |
| Radiated | 30 MHz to 1 GHz | Quasi-peak | CISPR 11 group 1 class B |
| Radiated, extended | 1 to 6 GHz | Peak and average | Only if the radio is ever enabled, which it is not. Run once in M2 anyway as evidence for section 4.6 |

**Pass criterion:** worst-case margin of at least **6 dB** below the class B limit in every
mode. A margin is required rather than a bare pass because the pre-scan is on one hand-built
unit and the fleet will differ. A result between 0 and 6 dB of margin is a finding, not a
failure, and goes to the safety reviewer with a remediation proposal. The report states a
number, not a picture.

If it fails, the fallback order is: harness dressing and ferrite on the electrode cable at
J14; a ferrite on the host USB lead; then a shielded or conductively coated POD-P1. Who pays
for the re-scan is settled in the purchase order, not here.

### 4.5 Immunity

Not tested. The decision is recorded rather than left silent, because a device that must not
drop frames during a two-hour session in an arbitrary home is an immunity problem. Items
considered and their disposition:

| Item | Disposition |
|---|---|
| ESD to the J15--J17 DIN 42802 sockets and to the exposed host USB connector | Not tested. Mitigated by design: touch-proof sockets, the D1--D16 **BAV99** clamps (BAT54S is not approved in these positions, because Schottky leakage across the series resistor is an offset error on a 10 µV input), the D23 clamp on the comparator output, and the ADuM4160 barrier. Recorded as a residual risk in RISK-EEG-011 |
| Radiated RF immunity, home Wi-Fi and mobile handsets | Not tested. The signal band is DC to 100 Hz and every electrode lead carries the series-resistor and 10 nF low-pass whose corner, flatness and Johnson-noise arithmetic are computed once in RISK-EEG-011 section 4 and are not recomputed here. That network is the principal defence |
| Mains transients coupled through the host | Not applicable during recording: the isolator is the only path and the instrument is battery powered (RFQ S-01, S-03) |
| Effect of any immunity event on the data | The F-06 ring buffer and the F-07 GAP frame mechanism mean a disturbance shows up as a declared gap rather than as silently corrupted data. F-06 is relaxed to **90 seconds** of ring plus unlimited backfill from the microSD copy (ECO-EEG-025), because the mandated module's 8 MB of PSRAM cannot hold the three minutes the requirement originally asked for. That is the honest mitigation and it belongs in the analysis plan, not only here |

### 4.6 Proving the radio is never initialised

RFQ S-06 says production must confirm the radio is disabled. The v1 package's only evidence
was a comment in `main.c`. The evidence chain is now three links, and all three are required:

1. **Build.** `sdkconfig.defaults` excludes the Wi-Fi and Bluetooth components from the
   image. No call to `esp_wifi_init`, `esp_bt_controller_init` or `nimble_port_init` exists
   in the source, and the release build fails if one appears. The firmware release record
   carries the image SHA-256.
2. **Image identity.** The hash flashed at provisioning (RFQ F-18) is recorded per serial in
   the calibration record, so the image on any unit in the field can be tied back to the
   build that was scanned.
3. **Production test.** A 2.4 GHz receiver or spectrum sweep, 60 s during a recording block,
   accepting only if no carrier above the receiver noise floor, no ESP-prefixed SSID and no
   BLE advertisement is seen from the unit under test. This is the step S-06 demands and
   TST-EEG-004 Rev B did not contain; it is **T24, "Radio silent"**, in TST-EEG-004 Rev C,
   which owns the step numbering, and it runs concurrently with T14 so it costs no line time.
   It records pass or fail, the receiver noise floor and the firmware image hash.

---

## 5. IEC 60601-1 as a design reference

IEC 60601-1:2005 + A1:2012 + A2:2020 is used as a **design reference** for a type BF applied
part. The applied parts are the eight scalp cup electrodes, the two ear-clip references, the
bias electrode and the three EMG snap electrodes: **fourteen patient terminations**
(8 + 2 + 1 + 3), all connected through the 12-way screened electrode cable at J14 --
terminations J14.1 to J14.11 -- or the three DIN 42802 sockets at J15--J17. The two EOG spare
channels are protected on the carrier and brought to J22, but they are **not fitted to panel
sockets in a standard build**, so they are not applied parts of the standard build and are not
counted here.

The table is a gap list, not a conformity claim. "Met by design" means the design does the
thing the clause asks for; it does not mean anyone has measured it. Step numbers are cited
from TST-EEG-004 Rev C, which owns them; none is invented here.

| Clause | What it asks | Status | Evidence, or what is missing |
|---|---|---|---|
| 4.3 Essential performance | Identify it | **Partly.** Essential performance is named in RISK-EEG-011 as: acquire and record the sample stream without undeclared loss, and not exceed the S-02 auxiliary current | Named, never verified against a fault set |
| 4.7 Single fault condition | Safe in single fault | **Met on the calculated budget, corrected 2026-09-02.** The architecture is unchanged -- BAV99 clamps to AVDD/AVSS, battery-only recording, the isolator -- and the series resistance is now **68 kΩ per lead**, which puts the single-fault DC figure at **36.8 µA against S-02's 50 µA limit**. Until that date this row read "not met on the calculated budget … 53.2 µA against S-02's 50 µA limit, a calculated failure, not a pass", with 47 kΩ fitted | ECO-EEG-024 is **applied** in `design.py`; RISK-EEG-011 section 4 owns the arithmetic and **has not been re-issued for 68 kΩ, so it still prints 53.2 µA as the live state**. A met calculation is not a safe device: **no fault-insertion testing has been done**, nothing has been measured, and the electrical safety reviewer has not seen it |
| 7.2, 7.4 Marking and identification | Legible, durable marking | **Met by design.** ART-LBL-01, 50 × 25 mm matt polyester, IPA-resistant, per ASM-EEG-007 stage 6 | No IEC 60601-1 symbol set is applied. A certified device would carry the type BF symbol; this one deliberately does not, because carrying it would imply conformity |
| 8.4.2 Patient auxiliary current | ≤ 10 µA DC, ≤ 100 µA AC normal; ≤ 50 µA DC single fault | **Calculated only, and the single-fault limit is now calculated as met** -- 36.8 µA against 50 µA at the 68 kΩ of ECO-EEG-024, which is applied; see clause 4.7. Corrected 2026-09-02: this cell read "calculated as exceeded (53.2 µA against 50 µA)". RFQ S-02, budget in RISK-EEG-011 section 4, which still prints the 47 kΩ figure | Never measured. **TST-EEG-004 Rev C step T23** is the routine per-unit measurement, at all **fourteen** terminations -- J14.1 to J14.11 and J15, J16, J17 -- recording 14 DC and 14 AC values normal, host connected and disconnected, plus 14 single-fault DC values. T23 is explicitly a **stand-in**: a 100 kΩ measuring resistor, not the IEC figure-12 measuring device, and one single-fault condition only |
| 8.5.1 Means of protection | Two means of patient protection to mains | **Met by design.** During recording the instrument is battery-only and the only path to a mains-referenced host is the ADuM4160 module, rated ≥ 2.5 kV RMS for one minute | RFQ S-03, E-24. The 2.5 kV RMS figure is the **module supplier's type-test certificate**, collected once at incoming inspection (TST-EEG-004 Rev C step T00) and never repeated per unit |
| 8.5.2, 8.9 Creepage and clearance | 8 mm creepage / 5 mm clearance for 2 MOPP at 250 V working | **Met by design, and the keep-out is evidenced rather than asserted.** The barrier is entirely inside the module. The carrier has no copper on the host side: the isolation keep-out defined in DSN-EEG-003 section 3.3 -- the strip x ≥ 141 mm, y = 2 to 22 mm, which is 9 mm wide at the board edge -- has to be free of copper on **all four layers**, L1, L2, L3 and L4, not merely on the two outer ones. Both inner layers carry reference planes, so the keep-out has to be cut in the planes as well, and that is the change the four-layer decision forces on this clause. It is the one thing in this row that is a fact about the artwork rather than an intention, so it is not asserted here; it is read off the DRC report | **The DRC report is the evidence.** `kicad/EEG-CAR-01_RevB_DRC_report.txt` tests the strip separately on F.Cu, In1.Cu, In2.Cu and B.Cu and reports **zero isolation keep-out violations**, so the strip is clean on all four copper layers as at the Rev B routing. That is stated here because the report says it. Two qualifications travel with it: that report is an automatic check on a routing no layout engineer has reviewed, so the artwork is released for review and not for fabrication and can still move (section 9, item 10); and nothing has been measured on a fabricated board. The FAI in QP-EEG-010 measures it, and TST-EEG-004 Rev C verifies the keep-out from the artwork once per routed Gerber revision, not per unit |
| 8.5.2 continued | No second path across the barrier | **Residual risk, controlled by assembly.** The ESP32-S3-DevKitC-1's own two USB-C sockets sit on the non-isolated side and bypass the barrier entirely if reached. The DevKit's UART USB-C port is also the end-of-line flashing port, so it must be reachable on the line and unreachable in the field | ASM-EEG-007 stage 6 requires the assembler to confirm they are not reachable from outside a closed pod, and stage 6 records it. This is a **procedural** control on a safety-critical property, which is weaker than a physical one, and the safety reviewer is asked to rule on it |
| 8.7 Leakage currents | Measured | **Partly, by a stand-in.** TST-EEG-004 Rev C step T23 gives routine per-unit leakage evidence at all fourteen terminations | It is not the IEC 60601-1 patient-auxiliary-current measurement and does not claim to be. The real verification is owed by the electrical safety review, which has not happened |
| 8.8 Dielectric strength | Type-tested | **Not type-tested by the programme.** The 2.5 kV RMS figure is the module vendor's rating | Per-unit evidence is **TST-EEG-004 Rev C step T20**, a **500 V DC insulation-resistance measurement** across the barrier with a 60 s dwell and a ≥ 1 GΩ limit. **There is no routine per-unit hipot and none is permitted:** a 2.5 kV AC station on an assembled unit stresses a barrier that was already type-tested by its maker and risks damaging it. Any fixture design that specifies a per-unit 2500 V AC test is superseded by T20 |
| 8.10 Components and wiring | Components suited to their application | **Partly.** The isolator and both ADS1299 modules are consumer breakouts with no controlled revision and no vendor commitment, and the J15--J17 touch-proof sockets have no confirmed catalogue part at all | AVL-EEG-017 pins the vendors and requires change notification. Today the strongest statement possible is "not substitutable" |
| 8.11 Mains parts | -- | **Not applicable.** No mains part. The 5 V charger is a separate CE-marked appliance and is never connected during a session (RFQ S-01) | -- |
| 9.2, 9.8 Mechanical hazards | No hazardous moving or sharp parts, adequate retention | **Met by design.** Printed frame, no moving parts other than the ratchet and the HM-08 hatch. 1 m drop per RFQ M-04 | M-04 drop test not yet run |
| 10.1 Radiation | Ionising and non-ionising | **Not applicable** for radiation. Acoustic output is the real hazard here and now has its own requirement: **RFQ E-29, ≤ 100 dB SPL at any commanded level**, measured on an artificial ear, with the firmware clamping the codec volume register to the value measured at calibration. Calculated full-scale output is about **110 dB SPL**, which is why the requirement exists | **TST-EEG-004 Rev C step T28** measures it as a type test, listed in TST-EEG-004 section 14, **once per lot, not per unit**, and publishes the clamp register value that T17 reads back on every unit. Not yet performed |
| 11.1 Excessive temperatures | Applied-part and touchable-surface temperature limits | **Not tested.** RFQ 9.2's three-hour thermal run is the first measurement, and no limit is written for the TPU pads against the forehead until then. The DevKit's own 3V3 regulator is a second unmeasured thermal item: the carrier draws a *calculated* 288 mA worst case from it, about 0.5 W inside a closed pod, and TST-EEG-004 Rev C step T3 reports the case temperature | Gap: the applied-part limit must be set before the thermal run, not after. If the regulator case exceeds 85 °C, a 3.3 V regulator on the carrier fed from V5V is an ECO against Rev C |
| 11.6 Ingress of liquids | Suited to the environment | **Met by design.** All pod openings gasketed or recessed (RFQ M-02); gel and saline cannot reach the carrier; IP67 travel case (M-05) | No IP test is claimed for the pod itself |
| 11.8 Interruption of the supply | Safe on power loss | **Met by design.** Loss of power ends the session; the microSD holds the authoritative copy and the ring buffer backfills on re-enumeration | The ring is 90 s, not three minutes (F-06 as relaxed by ECO-EEG-025), with unlimited backfill from the card. TST-EEG-004 Rev C step T15 is the backfill test |
| 12.2 Usability | IEC 62366-1 process | **Not done.** No usability engineering file exists. The device is used unsupervised, at home, by a distressed cohort, which is precisely the case the standard exists for | IFU-EEG-014 is written in its place. This is a stated shortfall |
| 13.1 Hazardous situations | Enumerated and controlled | **Partly.** RISK-EEG-011 is a risk analysis. It is not a full ISO 14971 risk management file with a plan, a management review and a production-and-post-production feedback loop | Named as a shortfall in RISK-EEG-011 itself |
| 14 PEMS | IEC 62304 software lifecycle | **Not done.** The firmware is developed under version control with a released image hash, and that is all. A lifecycle is a process, and building an image is not one | Corrected 2026-09-02. The firmware **is built** -- ESP-IDF v5.2.5, esp32s3, four images and their SHA-256 in `firmware/release/manifest.json` -- and has **booted once under QEMU**, which emulates none of this design's peripherals. **It has never run on hardware.** The contact-light phase driver **is written**, so T11 is no longer blocked by missing code; it has not been run, because no unit exists. Until that date this cell read "firmware has never been compiled or run on hardware" and "the phase driver is specified and not coded, so T11 cannot pass today" |
| 15.3 Mechanical strength | Drop, impact | **Not tested.** RFQ M-04, Phase 1 | -- |
| 16 ME systems | Host computer forms a system | **Handled by isolation.** The participant's laptop is a mains-referenced non-medical device separated by the ADuM4160 | RFQ F-17 |
| 17 / IEC 60601-1-2 | EMC collateral | **Not claimed.** CISPR 11 class B pre-scan only, section 4 | -- |
| IEC 60601-1-11 | Home healthcare environment | **Not claimed, and it is the collateral that fits best.** Its requirements on mechanical robustness, environmental range, mains interruption and lay-user instructions are exactly this device's operating case | Recorded as the most significant unaddressed collateral |
| IEC 60601-2-26, EEG particular | Input impedance, noise, electrode-lead safety, defibrillation | **Partly by design.** Touch-proof 1.5 mm DIN 42802 connectors satisfy the requirement that an electrode lead cannot be inserted into a mains socket. Noise floor *calculated* at **0.31 µV RMS with the 68 kΩ resistors of ECO-EEG-024, which are what is fitted since 2026-09-02** (it was 0.27 µV at the 47 kΩ this row used to name as fitted), against RFQ E-03's 1.0 µV limit; the arithmetic is in RISK-EEG-011 section 4. **Defibrillation protection is not provided and is not claimed** | Never measured. TST-EEG-004 Rev C steps T7 (gain), T8 (noise floor) and T22 (frequency response) |

**What would have to change if the device were ever certified.** All of the following, at
minimum: a full ISO 14971 risk management file with production and post-production feedback;
an IEC 62366-1 usability engineering file with formative and summative evaluation; an IEC
62304 software lifecycle for the firmware and for the browser session runner; type testing
for dielectric strength, leakage, temperature and mechanical strength by an accredited
laboratory; IEC 60601-1-2 immunity and emissions testing rather than a pre-scan; controlled
vendors with change notification for every safety-relevant component, which the consumer
breakouts at J1--J4 and J10 cannot supply today; a sourced and first-articled touch-proof
socket at J15--J17; a physical rather than procedural control on the DevKit's own USB
sockets; the type BF symbol and the full IEC 60601-1 marking set; a quality system to ISO
13485; and a manufacturer legal entity that takes on the obligations. The programme has no
intention of doing any of it, and says so here so that nobody later mistakes the design
references for a certification path.

---

## 6. Biocompatibility

### 6.1 Categorisation

Under ISO 10993-1:2018 the instrument is a **surface-contacting device, intact skin**. Per
participant, contact is two or three sessions of about two hours, which is *limited* contact
(≤ 24 h). The programme adopts the more conservative **prolonged** category (> 24 h to 30 d)
because participants may run additional sessions, because the same physical parts pass
through a sequence of participants -- about twenty a year on one kit, at the twenty
turnarounds per kit per year SVC-EEG-013 section 3.5 costs, and more over the life of a
fleet built at 25 to 50 kits (RISK-EEG-011 section 1.4) -- and because the abrasive scalp
preparation the protocol uses means the skin is not always intact by the end of the
session. Required endpoints:

| Endpoint | Standard |
|---|---|
| Cytotoxicity | ISO 10993-5:2009 |
| Skin sensitisation | ISO 10993-10:2021 |
| Irritation | **ISO 10993-23:2021.** Irritation testing moved out of ISO 10993-10 in the 2021 revision. A declaration citing "ISO 10993-10 irritation" against the 2021 edition is wrong on its face |

RFQ S-05 names three items. The actual skin-contact set is larger, and section 6.2 is that
list.

### 6.2 Skin-contact material list

**Eight rows.** RFQ A-03's separate headband or cap is **withdrawn as a kit item**: the eight
electrodes are fixed to the HM-01 frame at manufacture, so a headband carrying fixed holders
at the same eight sites would duplicate them. A-03 is rewritten to cover the parts the kit
actually needs and already has on the frame -- the **HM-06 chin strap** and the **HM-03
occipital yoke** -- and both are covered by the rows below. RISK-EEG-011 section 2
(Chemical) and its section 7.3 item 4.6 count the same eight materials.

| Part | Material or product | Reference supplier | Contact site and duration | Evidence route |
|---|---|---|---|---|
| Sintered Ag/AgCl cup electrodes, 8 fitted + 2 spare (item 25) | Sintered Ag/AgCl in an HM-04 body | Wuhan Greentek; FRI or Spes Medica | Scalp, 2 h, through paste | Supplier declaration, -5 and -10/-23 |
| Ag/AgCl ear-clip references ×2 (item 26) | Ag/AgCl and clip body | Greentek | Earlobe, 2 h | Supplier declaration |
| EMG snap leads (item 27) and disposable snap electrodes ×30 (item 28) | Hydrogel snap electrodes | Ambu BlueSensor N or Kendall | Cheek, submental, laryngeal, 2 h, single use | Existing manufacturer declarations. The easiest row in the table |
| HM-02 TPU comfort pads ×4 and HM-06 chin strap and liner (item 19) | TPU 85A, printed or cast | To be named | **Forehead, occiput, crown, chin. The parts most continuously against skin.** Consumable, replaced each turnaround | Material supplier declaration plus the print bureau's process declaration |
| HM-01 halo and arches, HM-03 occipital yoke, HM-04 bodies (items 15, 16) | MJF PA12, dyed black | Print bureau, to be named | Scalp, forehead and occiput through the pads, and directly where the pads do not cover | **The hardest row.** See section 6.4 |
| HM-07 boom arm and its cheek sleeve, HM-08 battery hatch (items 17, 22) | MJF PA12, gooseneck sleeve | Print bureau; gooseneck supplier | Boom sleeve at the cheek, incidental. The HM-08 hatch is handled rather than worn, and is included because it is the same printed, dyed material | Declaration |
| Conductive EEG paste ×2 100 g, abrasive prep gel 100 g, saline wipes ×30 (item 31) | Greentek GT20/GT5 or Ten20/NuPrep | Greentek or Weaver | **Applied by the participant, and not all to the same site.** Conductive paste into the eight scalp ports and onto the two ear clips, 2 h; abrasive prep gel on the face, the neck and the earlobes only and never on the scalp; saline wipes at those same three EMG sites. See IFU-EEG-014 section 13.2 | SDS plus the manufacturer's existing skin-contact evidence. See section 6.5 |
| ATH-M20x ear cushions (item 29) | Protein leather over foam | Audio-Technica | Circumaural, 2 h, both ears. **Never mentioned in S-05** | Supplier declaration or documented history of safe use |

### 6.3 What a valid declaration looks like

The programme sends one page per supplier, and accepts a returned declaration only if it
carries all of the following:

1. The supplier's legal entity, address and the signatory's name and position.
2. The **exact material grade or product part number**, matching the AVL-EEG-017 entry.
3. The contact category assumed: surface device, intact skin, prolonged contact.
4. The endpoints addressed, each named with its **standard number and edition year**.
5. The basis: a test report (with laboratory name, report number and date), or a documented
   history of safe use in the same contact category with the reference given, or a
   toxicological risk assessment by a named assessor.
6. Any conditions or limits on the declaration -- post-processing, colourants, sterilisation
   method, cleaning agents.
7. A statement that the declaration covers the material **as supplied to this programme**,
   not a different grade from the same family.
8. Date, and an expiry or recheck date.
9. A named contact for questions.

**Reject a declaration that:** says only "biocompatible" or "medical grade" with no standard
cited; cites ISO 10993-1 alone, which is a categorisation standard and contains no test;
cites "ISO 10993-10 irritation" against the 2021 edition (see section 6.1); covers a
different grade, colour or supplier from the one on the AVL; is a marketing page rather than
a signed document; is undated; carries no signatory; or is silent about colourant and
post-processing for a printed part.

### 6.4 MJF PA12, treated separately

MJF PA12 is not biocompatible by default. The variables that decide it are the black dye, the
post-process chemistry and the residual unfused powder, none of which the base polymer's
datasheet addresses. The bureau must supply, in addition to the section 6.3 declaration:

- The polymer grade and its supplier, and the fusing and detailing agent chemistry.
- The dyeing process and the colourant, with its own declaration.
- The depowdering method, and a statement on **residual free powder in the HM-01 internal
  wiring channels**, which is the part nobody looks at and which SVC-EEG-013 flushes with
  warm water at every refurbishment.
- Any sealing or coating applied, and whether it changes the answer.
- Confirmation that the declaration still holds after **25 cycles of the SVC-EEG-013
  reprocessing protocol**, including 70 % IPA wiping. A declaration that is true only
  as-printed is not sufficient for a part that circulates for years.

If the bureau cannot supply this, the alternative is programme-commissioned ISO 10993-5 and
-23 testing on printed, dyed, depowdered coupons from the same build, which is a cost and a
lead time the Phase 2 schedule has to carry.

### 6.5 Consumables applied by the participant

The participant applies the paste, the abrasive prep gel and the saline wipes to themselves,
without supervision, and the two gels do not go to the same place: the conductive paste is
introduced into the eight scalp ports and onto the two ear clips, while the abrasive prep gel
is used on the face, the neck and the earlobes only and never on the scalp, which is what
IFU-EEG-014 section 13.2 prints for the participant. The programme holds the SDS for each,
retains the manufacturer's skin-contact evidence, and puts the following in IFU-EEG-014 and
the participant information sheet:

- Do not use the abrasive gel on broken skin, a skin condition or a recent wound at the face,
  neck and earlobe prep sites, and do not use it on the scalp at all. Do not use the
  conductive paste on broken skin or an active scalp condition.
- Stop and remove the headset if the skin stings, burns or itches.
- Contraindication list: known allergy to any listed constituent, active scalp condition,
  broken skin at any electrode site.
- A support contact that is answered, and that is **not** the research team (ETH-EEG-001).

### 6.6 Evidence register

One row per material in section 6.2 -- eight rows: part, material grade, supplier,
declaration reference, revision, date received, endpoints covered, standard editions cited,
recheck date, and the reviewer who accepted it. The register feeds hazard H-19 in
RISK-EEG-011 and is checked before each phase's purchase order. **The register is empty
today.** Not one declaration in section 6.2 has been requested.

---

## 7. Ethics and data protection

### 7.1 Link to the study

The instrument may not be issued to any participant before an independent ethics committee
has approved the protocol. ETH-EEG-001 is the device annex to that submission, written in
committee language, and it carries the **configuration freeze record**: the exact revision of
every controlled document, the routed Gerber revision, the firmware image hash, the BOM
revision and the serial range of units covered by the approval. That freeze record is
produced by ECO-EEG-016 from the as-built record.

The study is pre-registered. The pre-registration identifier, the registry and the date go in
ETH-EEG-001 section 1 and are quoted on the participant information sheet, so a participant
can read the analysis plan that existed before their data were collected. **The identifier is
not yet allocated** and is a placeholder until the registration is filed.

**Amendment rule.** Any Class 1 change under ECO-EEG-016 -- a risk control component, an
applied-part material, the isolation architecture, the acoustic ceiling, or the cell -- is a
protocol amendment and requires re-notification to the committee before any affected unit is
issued. The ECO form carries the question "does this require re-notifying the ethics
committee?" precisely so that this cannot be forgotten. The four-layer carrier and the
enlarged POD-P1 are recorded as ECOs in the ECO-EEG-016 register; they change the isolation
keep-out's realisation on the two new inner layers, so they are re-notifiable if a freeze
record has already been submitted.

### 7.2 GDPR position of the recorded data

| Question | Position |
|---|---|
| Controller | The TI One Voice research programme, Brussels |
| Data | Sixteen channels of EEG, the participant's recorded voice from the boom microphone, room audio from the room microphone during scripted windows only, button responses, and session metadata |
| Category | **Special category data** under Article 9(1): data concerning health, and biometric-adjacent voice data |
| Legal basis | Article 6(1)(a) consent, together with Article 9(2)(j) scientific research subject to Article 89(1) safeguards and the Belgian Law of 30 July 2018 |
| DPIA | **Required** under Article 35. Large-scale special-category processing of a vulnerable cohort, with recording equipment operating inside participants' homes. ETH-EEG-001 section 4 is the device part of it |
| Where the data physically live | The authoritative copy is written to the microSD card at J20 (RFQ E-20) inside a kit that **travels back through the post**. The host copy reaches the programme over TLS during the session |
| Room microphone | Hardware-mutable on MIC_MUTE (GPIO21) and captured only during scripted windows. This is a control the DPIA relies on, and TST-EEG-004 Rev C step T17 verifies the mute depth |
| At rest on the card | **Open decision.** The card is not encrypted today. Either encrypt at rest with a key that is not on the device, or record the decision not to and justify it against the loss-in-post scenario. Owner: programme technical lead, before Phase 2 |
| Erasure | Secure erase of the microSD at refurbishment, after ingest is confirmed, recorded on the SVC-EEG-013 refurbishment record. A kit never carries one participant's data into another participant's home |
| Kit lost in the post | Treated as a personal data breach: assessed within 72 h, notified to the Belgian DPA if the risk threshold is met, and the affected participant told. The mitigation is the encryption decision above |
| Retention | Per the approved protocol, in ETH-EEG-001 |
| Pseudonymisation boundary | The unit serial identifies an instrument. The format is **`TIOV-B-nnnn`** -- programme prefix, hardware revision letter, four digits, with Phase 1 using 0001--0009, Phase 2 0010--0099 and Phase 3 0100--0999 -- **defined once in PKG-EEG-015 section 5** and quoted here only so this row reads on its own. It appears identically on the label, in the Data Matrix, in the USB `iSerialNumber`, in the calibration record and on the packing list. The participant identifier is separate, and the mapping between them is held apart from the recordings, by a named person. **Analysis files carry the unit serial, never the participant identifier and never a name** |

### 7.3 The per-device key: what it proves and what it does not

Each unit holds an ATECC608B secure element at J11. Its P-256 private key is generated
on-chip and never leaves it. At provisioning (RFQ F-18) the public key is exported and the
fingerprint is computed to the single definition in **FW-EEG-001 section 7**, which every
other document cites and none restates. The fingerprint is on the label and in the
calibration record; the **unit serial `TIOV-B-nnnn`** becomes the USB `iSerialNumber` (F-04, and RUL-EEG-021 section B rules it); the ATECC608B's own nine-byte factory serial is a second identifier, printed and carried in the Data Matrix, and is **not** the descriptor string; the firmware
signs each block of the frame stream (F-08).

**What a valid signature proves.** That the signed block was produced by a unit holding the
private key matching a registered public key, and that the block's bytes have not been altered
since signing. It ties a stream to a specific physical instrument, and it means a recording
cannot be silently edited, spliced or fabricated after the fact by anyone who does not hold
that key.

**What it does not prove, stated plainly because the temptation to over-claim is real.**

- Not who wore the device, or that anyone wore it. The key signs whatever the converters
  produced.
- Not that the electrodes were on a head. A signed recording of a saline phantom, or of an
  open input, is exactly as valid a signature as a signed recording of a person.
- Not that the analogue signal is genuine. Anything injected ahead of the ADS1299 is signed
  along with everything else.
- Not that the recording happened when the timestamps say, unless the timestamp chain is
  anchored to something outside the device. It is not, today.
- Not that the unit was not opened. There is no tamper detection on POD-P1, and a unit that is
  lost or stolen keeps signing.
- Not a legal chain of custody, and it must never be described as one in a paper.

The key is an integrity control against post-hoc alteration of study data. It is not an
anti-fraud control against a participant, it is not evidence about anyone's experience, and
nothing in a publication may imply otherwise. On the Phase 1 prototypes the eFuses are **not
burned**: secure boot and flash encryption are enabled from Phase 2, so the two prototypes run
unsigned images and the signature chain above is the only integrity control on them.

---

## 8. Compliance matrix

| # | Obligation | Applicable document | Responsible | Evidence retained | Status |
|---|---|---|---|---|---|
| 1 | Not a medical device under MDR 2017/745 | MDR Art. 2(1); section 1 | Programme lead | This section 1, signed and dated; ethics committee determination | **Drafted.** Committee determination outstanding |
| 2 | Controlled label and participant wording | RFQ M-03; section 1.4; PKG-EEG-015 | Programme lead; manufacturer applies | ART-LBL-01 artwork; IFU-EEG-014 | **Wording released.** Artwork in PKG-EEG-015 |
| 3 | Customs description and HS code | Section 1.5 | Programme lead with broker | Commercial invoice template | **Open.** Code unconfirmed |
| 4 | RoHS 3 conformity, contractual, covering the four-layer laminate ply by ply | 2011/65/EU + 2015/863; EN IEC 63000; RFQ S-08; sections 2.2, 2.3 | Manufacturer declares; programme accepts | Signed declaration per phase; supplier declarations; fabricator laminate declaration; exemption list | **Not started.** No declaration received |
| 5 | REACH SVHC article-level statement | 1907/2006 Art. 33; section 2.3 | Manufacturer declares; programme communicates to participant | Declarations with candidate-list version and date; Article 33 statement in IFU-EEG-014 | **Not started** |
| 6 | SCIP notification decision | ECHA; section 2.4 | Programme lead | Recorded decision plus the declarations behind it | **Not started.** Cannot be closed until the J15--J17 socket part is chosen |
| 7 | EU DoC for the 5 V charger and cables | LVD 2014/35/EU, EMC 2014/30/EU; section 2.5 | Manufacturer supplies; programme accepts | Vendor DoC, test reports, CE traceable to a legal entity | **Not started.** "Certified generic" is not acceptable |
| 8 | WEEE and battery take-back | 2012/19/EU; (EU) 2023/1542; section 2.5, 3.8 | Programme lead | Registration or disposal consignment records | **Not started.** Due at end of programme |
| 9 | Cell UN 38.3 test summary | UN Manual of Tests and Criteria 38.3.5; RFQ S-04; section 3.2 | Cell supplier via manufacturer; programme holds | Test summary, all ten required fields, T.1--T.8 | **Not started** |
| 10 | Cell IEC 62133-2 certificate | IEC 62133-2:2017+A1:2021; section 3.2 | Cell supplier; programme holds | Certificate or full report naming the exact model | **Not started** |
| 11 | Thermistor-monitored charging (S-04) and no charging above 45 °C (E-23) | RFQ S-04, E-23; section 3.2 box; RUL-EEG-021 section B | Programme technical lead | ECO adding the NTC net, or a written alternative | **S-04 not met, and it stays not met:** no NTC net exists in the Rev B netlist and no thermistor way exists on J12 or J13. **E-23 met only in part:** the bq24074-class module's own die thermal regulation is the whole of what stands behind the 45 °C inhibit, nothing measures the cell, and TST-EEG-004 Rev C T4 records that the inhibit is not tested and cannot be. Hardware hole, open |
| 12 | UN3481 / PI967 section II compliance, configurations A and B | IATA DGR, ADR SP188, IMDG; RFQ S-09; sections 3.3--3.5; PKG-EEG-015 §7 | Manufacturer (A); programme (B) | Packing tick sheet per consignment, marks applied, documents per section 3.7 | **Obligation released here; procedure in PKG-EEG-015 §7; per-unit evidence is TST-EEG-004 Rev C T29.** Not yet exercised |
| 13 | Return leg engineered so the participant never classifies or declares | Section 3.3, option (a) | Programme operations | Prepaid pre-classified label; carrier account terms; collection fallback | **Decided, not yet contracted** with a carrier |
| 14 | 1.2 m package drop test | PI967 §II; section 3.6 | Programme, Phase 1 | Drop record, orientations, photographs, post-drop inspection | **Not performed** |
| 15 | Trained dangerous-goods shipper | IATA CBTA; ADR 1.3; section 3.7 | Manufacturer names theirs; programme appoints its own | Training certificates, 24-month refresher log | **Not appointed** at the programme |
| 16 | State of charge ≤ 30 % at despatch | RFQ S-09; section 3.8 | Whoever despatches | Gauge reading per serial on the PKG-EEG-015 §7 tick sheet | **Rule released** |
| 17 | Damaged cell never transported | Section 3.8 | Participant instructed; programme acts | IFU-EEG-014 wording; collection record | **Wording released** |
| 18 | CISPR 11 class B pre-scan, one Phase 1 unit, on the four-layer carrier in the enlarged POD-P1 | RFQ S-06; section 4 | Manufacturer arranges lab; programme accepts report | Lab report, EUT photographs, plots per mode M1--M6, worst-case margin | **Not performed.** Plan released here. The EUT cannot be built until the layout review of RFQ-EEG-002A is done and the artwork is released for fabrication. Corrected 2026-09-02: this cell also said M5 could not be run until the contact-light phase driver existed. **The driver exists**, and M5 will emit its alternation at about 250 Hz rather than the specified 240 Hz, because the half-phase quantises to the FreeRTOS tick |
| 19 | Radio never initialised, proven in production | RFQ S-06; section 4.6 | Programme (build evidence); manufacturer (T24) | sdkconfig, image hash per serial, T24 result per unit | **Not implemented.** T24 "Radio silent" is the step in TST-EEG-004 Rev C |
| 20 | IEC 60601-1 design-reference gap list | Section 5 | Programme technical lead; safety reviewer signs | This section 5, reviewed and signed | **Drafted.** No safety engineer engaged |
| 21 | Patient auxiliary current measured at the fourteen terminations | RFQ S-02; section 5 | Manufacturer, TST-EEG-004 Rev C T23 | 14 DC and 14 AC values normal, host connected and disconnected, plus 14 single-fault DC values, per serial | **Calculated only, and the calculation now passes:** **36.8 µA** single-fault DC against the 50 µA limit, at the 68 kΩ that ECO-EEG-024 fitted on 2026-09-02. Corrected on that date: this cell read "the calculation fails: 53.2 µA … ECO-EEG-024 is the proposed fix". The ECO is applied; **the measurement is still owed and the safety reviewer has still not seen it** |
| 22 | Isolation barrier routine-tested per unit | RFQ S-03; section 5 | Manufacturer, TST-EEG-004 Rev C T20 | Applied voltage, insulation resistance, dwell, RH, module type and lot, per serial | **Specified, not performed.** 500 V DC insulation resistance, ≥ 1 GΩ. No per-unit hipot is used |
| 23 | DevKit USB sockets unreachable in the field | Section 5; ASM-EEG-007 stage 6 | Manufacturer | Stage 6 tick | **Procedural control.** Safety reviewer to rule |
| 24 | ISO 10993-5 / -10 / -23 declarations, all eight material rows | RFQ S-05; section 6 | Suppliers declare; programme accepts | Evidence register, section 6.6 | **Not started.** Register empty |
| 25 | MJF PA12 dye, powder and post-process declaration | Section 6.4 | Print bureau | Bureau declaration plus 25-cycle statement | **Not started** |
| 26 | Consumable SDS and contraindications | Section 6.5 | Programme | SDS on file; IFU-EEG-014 wording | **Not started** |
| 27 | Maximum acoustic output ≤ 100 dB SPL, with a firmware clamp | RFQ E-29; section 5, clause 10.1 | Manufacturer, TST-EEG-004 Rev C T28, once per lot | Two dB SPL values, headphone model and impedance, clamp register value | **Not performed.** Calculated full-scale output is about 110 dB SPL, so the clamp is load-bearing |
| 28 | Ethics approval before any unit is issued | Section 7.1; ETH-EEG-001 | Programme lead | Approval letter, configuration freeze record | **Not submitted** |
| 29 | DPIA | GDPR Art. 35; section 7.2 | Programme lead | DPIA document, device section from ETH-EEG-001 | **Not started** |
| 30 | Encryption-at-rest decision for the microSD | Section 7.2 | Programme technical lead | Recorded decision with justification | **Open** |
| 31 | Secure erase at refurbishment | Section 7.2; SVC-EEG-013 | Programme operations | Refurbishment record per turnaround | **Procedure to be written** in SVC-EEG-013 |
| 32 | Per-device key claims kept accurate in publications | Section 7.3 | Programme lead | This section quoted in the analysis plan | **Released** |

---

## 9. What is not known

> 1. **No safety engineer has reviewed this design.** Section 5 is a self-assessment. It
>    blocks use on a person; it does not block quoting. Fabrication is blocked too, but by
>    the layout review still owed under RFQ-EEG-002A (item 10), not by this section.
> 2. **No hardware has been built, manufactured, shipped, scanned, tested or declared.** Every
>    row of section 8 marked "not started" or "not performed" is exactly that. This file is
>    the list of obligations, not a record of their discharge. **Corrected 2026-09-02:** this
>    item read "nothing has been built". The firmware image is now the one exception -- it is
>    built and it has booted in an emulator (clause 14) -- and it changes nothing here,
>    because no unit exists to run it on and no obligation in section 8 is discharged by it.
> 3. **The dangerous-goods rules in section 3 are stated as understood at IATA DGR 67th
>    edition, ADR 2025 and IMDG 42-24.** They are re-verified against the edition in force
>    before each despatch by the trained shipper, who is not yet appointed.
> 4. **RFQ S-04 and RFQ E-23 are two requirements at two different statuses, and neither is
>    closed.** The thermistor required by S-04 does not exist in the Rev B netlist and there
>    is no thermistor way on J12 or J13, so **S-04 is not met and it stays not met**. **E-23
>    is met only in part**: the bq24074-class charger module regulates its own die
>    temperature, which is the "charger IC with thermal regulation" half of the requirement,
>    but the 45 °C inhibit rests on that alone, nothing measures the cell, and TST-EEG-004
>    Rev C step T4 records that the inhibit is not tested and cannot be. Until a thermistor is
>    added by ECO, or an alternative is written down, S-04 stays not met and E-23 stays met in
>    part only.
> 5. **S-02's single-fault limit is calculated as met -- 36.8 µA against 50 µA -- and has
>    never been measured. Corrected 2026-09-02**: this item read "calculated as exceeded --
>    53.2 µA against 50 µA … nothing in this file may be read as a claim that S-02 is met",
>    with 47 kΩ fitted. ECO-EEG-024 is **applied**: R1-R16 are 68 kΩ on the same footprints,
>    and E-10 moves to the ±1.0 dB branch it already states for this case. What may still not
>    be read into this file is that S-02 has been *demonstrated*: nothing has been measured,
>    the measurement is owed before Phase 2, and **SR-01 is closed in the design and not
>    signed off**. The production simulation SIM-EEG-018 Rev A, re-run on 2 September 2026
>    after these changes, reports **193 checks passed, 0 failed and 6 known open items**, and
>    the S-02 entry among them is now "SR-01 is closed in the design and not yet signed off".
>    The other five are the linked image's static IRAM reporting full with one byte free, the
>    v1 HM-01 mesh being two disconnected bodies, the unreviewed routing, E-27 never having
>    been seen to light, and the two irreconcilable board-current figures. E-11's low-pass
>    half and E-27's missing driver, which this item used to list as open, are met.
> 6. **No maximum acoustic output has ever been measured.** E-29 is new, the calculated
>    full-scale figure is about 110 dB SPL, and the firmware clamp that enforces the 100 dB
>    limit is specified and not yet coded.
> 7. **No biocompatibility declaration has been requested from any supplier.** The register in
>    section 6.6 has no rows.
> 8. **The touch-proof sockets at J15--J17 have no confirmed catalogue part.** They are a
>    Class A patient-safety part on every unit, they carry a 12-week first-article lead time,
>    and neither the RoHS nor the biocompatibility question about them can be asked until the
>    part exists.
> 9. **The pre-registration identifier and the ethics approval reference are placeholders.**
>    They are filled in by ECO before the first unit is issued.
> 10. **The routing exists and closes; it is released for review, not for fabrication, and it
>    has not been reviewed by a human layout engineer.** It was produced by the programme's own
>    constraint-aware autorouter on the four-layer stack-up, and
>    `kicad/EEG-CAR-01_RevB_DRC_report.txt` is the authority for its state. The report records
>    EEG-CAR-01 Rev B routed on four layers, 150.0 x 130.0 mm, with 3 745 track segments and
>    552 through vias, and one continuous plane island per net on both In1.Cu and In2.Cu.
>    **All 145 nets are fully connected**: none unclosed, none without copper. Every geometric
>    rule passes: the smallest measured clearance is 0.260 mm on F.Cu, 0.275 mm on B.Cu and
>    0.285 mm on the planes against a 0.20 mm rule; the narrowest conductor is 0.20 mm; the
>    smallest plated hole is 0.30 mm; copper stands 2.00 mm from every non-plated hole; there
>    are no zone crossings; no digital net enters the analogue zone; and there is exactly one
>    AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND bridge. The report's own line is
>    "VIOLATIONS: 0 -- none.  The board passes every rule listed above", which is why clause
>    8.5.2 above is able to cite the report for the isolation strip rather than assert it.
>    That meets all three conditions of the gate in ECO-EEG-016 section 3 -- zero violations,
>    every net one connected copper island, both inner planes continuous under the analogue
>    zone -- so the data in `kicad/` is **RELEASED FOR REVIEW under RFQ-EEG-002A**. It is
>    **NOT RELEASED FOR FABRICATION** and no board may be ordered from it, because no human
>    layout engineer has read the routing; that review is what fabrication release waits on.
>    Two things belong beside the zero. The router **relaxed 169 connections** to close the
>    board -- 36 took a conductor narrower than the 0.25 mm preferred width, 133 kept full
>    width and took a reduced gap, every one at or above the 0.20 mm minimum conductor and gap
>    -- and a board that closes at minimum geometry is not the same board as one that closes at
>    preferred geometry, even when every rule passes. And nothing has been fabricated or
>    measured. The creepage argument of section 5, clause 8.5.2 depends on the keep-out being
>    honoured on all four layers: the report says it is, and it is re-verified from the artwork
>    once per routed Gerber revision -- including whichever revision the layout review finally
>    releases -- before it is relied upon.
