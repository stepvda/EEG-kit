# SERVICE AND REFURBISHMENT MANUAL

**Document:** SVC-EEG-013  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E, then ICD-EEG-006 Rev B,
then PARTS-EEG-019 Rev B. Where this document and `tools/design.py` disagree,
`tools/design.py` governs. The rulings this document is written against are collected in
RUL-EEG-021 Rev A, which is a controlled document in `docs/` and may be cited by section
letter.

**Cross-references.** Every other document is cited here at the revision current at this
issue: FW-EEG-001 Rev C, DSN-EEG-002 Rev E, DSN-EEG-003 Rev C, TST-EEG-004 Rev C,
SCH-EEG-005 Rev B, ICD-EEG-006 Rev B, ASM-EEG-007 Rev B, WH-EEG-008 Rev B, JIG-EEG-009
Rev B, QP-EEG-010 Rev B, RISK-EEG-011 Rev B, REG-EEG-012 Rev B, IFU-EEG-014 Rev B,
PKG-EEG-015 Rev B, ECO-EEG-016 Rev B, AVL-EEG-017 Rev B, SIM-EEG-018 Rev A, PARTS-EEG-019
Rev B, MECH-EEG-020 Rev A, RUL-EEG-021 Rev A and RFQ-EEG-001 Rev E. ECO-EEG-016 Rev B
section 1 is the register of record for those letters; where this list and that register
disagree, the register governs.

**Revision note, Rev A to Rev B:** corrected to the package v2 rulings of 2026-09-01 -- the
carrier is 150.0 x 130.0 mm and four-layer, the enclosure grew with it, the host link is a
socket on the isolator module and not a captive cable through a gland, the A-03 headband is
withdrawn as a kit item and its wash schedule with it, the module counts are twelve types
and thirteen assemblies, the headphone load is 47.0 Ω, the serial format is `TIOV-B-nnnn`,
and every requirement this document touches that is not met now says so where it is stated.
**The findings of the second cross-document audit of 2026-09-01 are closed in this issue at
the same revision letter:** the microSD card layout is now cited from FW-EEG-001 Rev C
instead of being restated here, the serial-number scheme is cited from PKG-EEG-015 Rev B
section 5 instead of being redefined here, and every cross-reference carries the revision
letter current at this issue. **Corrections within Rev B, after the verification review of
package v2.1 of 1 September 2026:** section 2 R9 step 6 is now the single cell-replacement
policy for the package, age and condition in one list, with the 80 % capacity trigger tied
to the bench analyser of section 3.2 that can actually measure it, and REG-EEG-012 section
3.8 cites it instead of carrying a different one; and every place this manual described the
insert as two layers with pockets -- R12, sections 3.2, 3.4, 6 and 9 -- is restated against
the CASE-00 Rev C seven-layer bay schedule of PKG-EEG-015 section 2.2, whose cut file has
still not been issued. **Corrections within Rev B, after the routing closed on 2026-09-01:**
section 5.7 is restated from the DRC report as it now stands -- zero violations, all 145 nets
connected -- so the fabrication data is released for review under RFQ-EEG-002A and is still not
released for fabrication, because no human layout engineer has reviewed the routing; the 169
connections the router closed at relaxed geometry are stated there and carried as open item 15.
No carrier has been fabricated, so nothing else in this manual changes.
**Corrections within Rev B, after the mechanical and firmware changes of 2 September 2026:**
**the cup bayonet is a real quarter turn for the first time.** Until that date HM-04 cut two
straight axial pockets and no circumferential run, and the HM-05B lug sat at an outer radius of
5.40 mm against a 5.30 mm slot -- so the carrier could not enter, and if it had it could not
have rotated. Every "turn the key" in this manual described a motion the released geometry
could not make. Section 4.1 now states the joint as it is: 1.70 mm entry slots at an outer
radius of 5.55 mm cut 3.60 mm deep, a 100° circumferential run at z 1.10 to 3.80 mm, a 1.10 mm
retaining lip below it, and a 5.20 mm outer-radius lug on the carrier, with the key engaging the
carrier's drive notches through the slots rather than engaging HM-04. R4 and R10 are rewritten
as enter, turn a quarter, and let the lip retain it, with the direction of turn referred to the
cup face. The **spring seat was deepened from 4.50 to 6.60 mm** in the same change, which takes
the free height above the spigot from 1.40 to 3.50 mm and is why AVL-EEG-017 K12's "3-6 N
stainless 302 compression spring" could not have been bought before it; K12 is still open, and
every 3 to 6 N in this manual is now labelled as K12's target rather than a measured force
(open item 16). **Nothing has been printed**: the joint is measured on the model by
`tools/simulate_production.py` and the FIT-01 coupon, which must first be re-cut to carry the
slot, the run and a lug, is the acceptance (open item 17). Separately, the **E-27 contact-light
phase driver was written on the same date**, so open item 8 is restated: T11 is specified
against a driver that exists, and the alternation runs at about 250 Hz because the half-phase
quantises to the FreeRTOS tick. **Corrected again on the same date (FW-D17):** this sentence
went on to say the red state could not be produced because `LOFF_SENSN` was never enabled.
The driver no longer depends on it -- the montage is single-ended, so the N half carried no
per-site information -- and red is now a site that trips both settings of a swept positive-side
comparator threshold. All three colours are reachable; what is not yet known is the resistance
each corresponds to, because the thresholds are datasheet endpoints rather than measured ones.
The R10 release rule is restated with it.

---

## Why this document exists

One kit serves about twenty participants a year in sequence, and more over the fleet's life
(the arithmetic is section 2 below). Between each of them the kit is received, its data recovered, stripped, cleaned, disinfected, re-consumabled, re-tested and
re-packed, and the whole of that procedure existed in v1 as five prose rows in DSN-EEG-002 Rev E section 4.1 and one paragraph about an ultrasonic bath. The v1 audit raised six service
findings against those rows -- `refurbishment-service-manual`, `disinfection-validation`,
`consumables-and-wear-schedule`, `service-key-control`, `spares-and-field-replaceable-units`
and `rma-and-returns-form`, plus the quality-side `reprocessing-validation` -- and their
common complaint is that the fleet business model has no procedure behind it. This document
is that procedure. It is written for a trained operator at a bench in Brussels, it states
times so the operator load can be costed rather than hoped for, and it states what is not
known as plainly as what is: **nothing in this package has been manufactured, cleaned or
measured, no safety engineer has reviewed this design, and every time, force and cycle figure
below is calculated or estimated.**

---

## 1. Scope, roles and competence

Three roles, and the boundaries between them are the whole safety argument of the reuse path.

| Role | Who | May do | May never do |
|---|---|---|---|
| Participant | The loan holder | Add gel through the port, wipe the outside of the frame, plug and unplug the USB-C leads, charge the kit between sessions, repack to the foam schedule | Open anything, remove a cup, hold an HM-09 key, read or erase the microSD |
| Operator | Trained programme staff, holds an HM-09 key, works to this document | Sections 2 to 4 of the turnaround, cup release and refit, cleaning, consumables, RTS-1 re-test, release | Open the POD-P1 lid, lift a cover strip, re-provision an ATECC |
| Service | Bench technician, ESD-controlled workstation | All of the above plus section 5 repairs, module swaps, provisioning, carrier replacement | Sign their own release for a unit whose identity they changed (section 5.8) |

Competence is demonstrated once, on a scrap frame, before an operator turns a key on a
fleet unit: eight release-and-refit cycles with no cup dropped and no bayonet marked, one
full turnaround shadowed, one turnaround observed. Recorded in the operator register.

**Safety gate.** No safety engineer has yet reviewed this design (DESIGN_FACTS section 8
item 1). This document describes the reuse path so that a reviewer has something to review.
It does not authorise use on a person.

---

## 2. The turnaround procedure

One pass, twelve steps, from a courier delivery to a sealed outbound carton. Hands-on
minutes are the operator's own time; elapsed minutes include unattended waits. Steps R5 to
R8 run while the cell charges in R9, so the bench critical path is shorter than the column
sum.

| Step | What happens | Hands-on (min) | Elapsed (min) | Records |
|---|---|---|---|---|
| R1 | Receipt, seal check, damage check, quarantine | 12 | 12 | F1 §1, RMA Part A |
| R2 | Download and verify the microSD copy | 10 | 20 | F1 §2 |
| R3 | Wipe and re-provision the card | 6 | 14 | F1 §2 |
| R4 | Strip: cups, ear clips, boom, pads, liner | 10 | 10 | F1 §3 |
| R5 | Ultrasonic clean and disinfect | 8 | 45 | F1 §4 |
| R6 | Gel-port flush | 8 | 20 | F1 §4 |
| R7 | Frame, case and headphone wipe, 70 % IPA | 6 | 8 | F1 §4 |
| R8 | TPU pads and chin-strap liner replacement | 6 | 6 | F1 §5 |
| R9 | Cell check and charge to despatch state | 5 | 90 | F1 §6 |
| R10 | Refit cups, RTS-1 functional re-test | 15 | 50 | F1 §7 |
| R11 | Consumable replenishment | 8 | 8 | F1 §5 |
| R12 | Repack, photograph, seal | 12 | 12 | F1 §8 |
| | **Totals** | **106 (1 h 46)** | **216 (3 h 36) critical path** | |

Add a 24 h quarantine between R1 and R2. Target dwell is two working days per kit.

**Fleet arithmetic, calculated.** A kit spends fourteen days with a participant and serves
about twenty people a year (experiment design v4.2, figure 19). Twenty kits therefore
generate 400 turnarounds a year; at 106 min hands-on that is 707 operator hours, or **0.42
FTE at 1,680 productive hours a year**. That is the number the programme budgets against,
and it is the reason this procedure is timed rather than described.

### R1 -- receipt and damage check (12 min)

1. Photograph the closed carton and its one numbered carton security seal (PKG-EEG-015
   Rev B section 6) before cutting anything. After opening the carton, photograph the two
   ART-LBL-07 case hasp seals before releasing the hasps. Compare all three seal numbers
   with the dispatch record, which carries a field for each; a broken or mismatched seal is
   fault code **FC-30** and the kit is quarantined unopened until the programme rules on it.
2. Open the case and photograph it closed-foam-up against the laminated packing photograph
   in the lid (RFQ M-06). Deviations are photographed, not corrected.
3. Tick the outbound kit packing list line by line in the return column (PKG-EEG-015 Rev B
   §1.1, which owns the list). Missing lines are priced from the section 7 damage schedule;
   they are not written off at the bench.
4. Inspect for: cracked case or hasp, crushed foam, a frame cracked at a node, a cup missing
   or hanging, a boom bent past its gooseneck travel, a cut or crushed USB-C lead, a torn or
   displaced gasket in the POD-P1 host aperture, a swollen or hot cell, visible soiling,
   blood, or any note from the participant.
5. **Quarantine 24 h** in a labelled bay. Escalate immediately and do not wait out the
   quarantine for: a swollen or warm cell (**FC-21**), visible blood or bodily fluid
   (**FC-19**), or a participant report of a skin reaction under an electrode (**FC-19**). A
   kit in either of the last two categories has its eight cups, two ear clips, TPU pads and
   chin-strap liner **scrapped, not cleaned**, and its frame service-inspected before release.

### R2 -- download and verification of the microSD copy (10 min hands-on, 20 elapsed)

The card is the study's evidence of record. It is read by the programme and by nobody else.

1. Remove the card from J20 with the case open on the bench, not with the pod open.
2. Copy the unit's session directory to the ingest store with a verifying copy. **The card
   layout is not restated here.** The firmware is what writes the card, so FW-EEG-001 Rev C
   owns the path, the extension, the filesystem and the sidecar, and the bench works from
   that document and from nothing else. The competing `/SESSIONS/...` path and the 512-byte
   plain-text header carried in Rev A of this manual are withdrawn. FW-EEG-001 Rev C section
   10 item 11 gives the layout in outline only and carries it as that document's own open
   item, so **this step is not to be turned into a work instruction with a fixed path
   written into it until that item is closed**; until then the operator copies the whole of
   the unit's directory rather than named files. Whatever the layout turns out to be, the
   payload is the byte-identical COBS frame stream that went to USB.
3. Verify before erasing anything: the recorded unit serial matches the label; SHA-256 of
   each file matches the copy; the signature chain verifies against the unit's exported
   public key; the frame sequence has no gaps that the host copy does not also have.
4. **Calculated data volume.** The frame payload at 1000 Hz is **50.7 kB/s** -- 1015 bytes
   every 20 ms, fifty frames a second, derived once in FW-EEG-001 Rev C §5.8. RFQ E-20's
   "≈70 kB/s" and F-12's "≈64 kB/s" are not different measurements of the same thing; they
   are allowances that add STATUS and SIGNATURE frames and filesystem overhead on top of the
   payload, and neither requirement changes. At 50.7 kB/s a recording hour is 182.5 MB, a
   two-hour session is 365 MB and a three-session loan is about **1.10 GB**. A 32 GB card
   holds roughly 175 recording hours, so it never fills within a loan; the card-full policy
   is stop-and-flag in STATUS, never overwrite.
5. A card that will not read, or whose recorded serial does not match the unit, is **FC-17**.
   Do not erase it. It goes to service with the unit.

### R3 -- wipe and re-provision the card (6 min hands-on, 14 elapsed)

1. Only after step R2's verification has passed and the ingest store has acknowledged.
2. Secure-erase the card (full overwrite, not a quick format). A quick format leaves the
   previous participant's recordings recoverable, and the kit is about to go to a stranger.
3. Re-format to the filesystem FW-EEG-001 Rev C specifies, which is exFAT, with a 128 kB
   cluster and the unit serial as the volume label.
4. Create the empty session directory that FW-EEG-001 Rev C names for that serial, and write
   `PROVISIONED.txt` into it with the erase date, the operator and the card serial.
5. Re-seat the card and confirm the slot latch. The card stays with the unit; it is not
   pooled between units, because the volume label is part of the evidence chain.
6. **The card is not encrypted at rest, and that decision is open** (REG-EEG-012 Rev B §7.2,
   owner the programme technical lead, before Phase 2). Until it is closed, the card leaves
   the building in a participant's post carrying plain recordings, and the erase step above
   is the only control on the previous participant's data.

### R4 -- strip with the service key (10 min)

1. Support the helmet on the halo in the bench cradle. Nothing may bear on a cup.
2. Insert the **HM-09** key into an HM-04 body from the cup face -- from below, with the
   helmet on the cradle -- and seat it fully. Its two 2.00 x 1.20 x 2.20 mm drive lugs at
   4.20 mm radius pass through HM-04's two entry slots and engage the **drive notches in the
   HM-05B carrier's underside rim**. Those notches are cut at **90° to the carrier's own
   bayonet lugs**, so they lie under the entry slots only when the carrier is seated, and that
   is the whole of the service interlock: with the cup fitted, the only thing under the slots
   is the notch, and nothing a finger can reach turns it.
3. Turn **90° anticlockwise** -- anticlockwise seen from the cup face, the reverse of the
   direction the run is cut. The carrier's two lugs travel back round the 100° circumferential
   run and come out through the entry slots. Nothing has to be lifted while it turns: the run
   is 2.70 mm tall for a 2.10 mm lug, and the 1.10 mm lip beneath it is what was stopping the
   carrier from dropping out, not what was gripping it. The cup releases
   against the compression spring; catch it, do not let it drop on its lead. **The 3 to 6 N
   this manual used to quote here is AVL-EEG-017 K12's stated target and is neither measured
   nor purchased**: the spring seat was too shallow for any such spring until 2026-09-02 and
   K12 is still an open line (section 10 item 16). Expect a spring; do not expect a number.
4. Repeat for all eight sites. Release the two ear clips and detach the boom at the temple.
5. Remove the four HM-02 TPU pads and the HM-06 chin-strap liner and **discard them** -- they
   are consumable and are never cleaned for reuse.
6. Remove the consumables pouch and discard whatever remains in it.
7. Count out: 8 cups, 2 ear clips, 1 boom capsule with windscreen, 4 pads, 1 liner. Count
   them back in at R10. A cup that cannot be released with the key is **FC-15** and goes to
   section 5.4.

### R5 -- ultrasonic clean and disinfection (8 min hands-on, 45 elapsed)

Agents, concentrations and contact times are stated so that they are auditable. Efficacy is
**not** validated by this programme: the agents are chosen on supplier data and on material
compatibility, and the 25-cycle compatibility protocol that DSN-EEG-002 Rev E section 12
finding 8 asked for and never got has not been run and is a Phase 1 deliverable. It is
carried as an open item in section 10 rather than against a document number, because the
disinfection validation protocol is not yet a registered document and the number used for it
in Rev A collided with RFQ-EEG-001 (section 10 item 9).

| Item | Method | Agent | Concentration | Temp | Contact | Rinse | Dry |
|---|---|---|---|---|---|---|---|
| 8 cups, 2 ear clips | Ultrasonic, 40 kHz | Neutral enzymatic instrument detergent | 0.5 % v/v in demineralised water | 35 ± 5 °C | 10 min | Demineralised water, 2 changes, 1 min each | Lint-free wipe, then 30 min at ≤ 40 °C |
| 8 cups, 2 ear clips | Immersion | Isopropanol | 70 % v/v | ambient | **2 min wet** | none | Air, 10 min |
| Boom capsule | Wipe only, **never immersed** | Isopropanol | 70 % v/v | ambient | 2 min wet | none | Air, 10 min |
| Boom windscreen | Discard and replace | -- | -- | -- | -- | -- | -- |
| HM-01 frame, HM-03 occipital yoke, HM-06 chin strap | Wipe, **never immersed** | Isopropanol | 70 % v/v | ambient | 2 min wet | none | Air, 10 min |
| Case interior and exterior | Wipe | Quaternary-ammonium surface wipe **or** 70 % IPA | as supplied | ambient | per label, min 1 min | none | Air |
| Headphone ear cushions | Wipe | 70 % IPA | 70 % v/v | ambient | 1 min | none | Air |

There is no wash schedule for a headband, because **the A-03 headband is withdrawn as a kit
item**. The eight electrodes are fixed to the HM-01 frame at manufacture, so a headband
carrying fixed holders at the same eight sites would duplicate them; RFQ A-03 is rewritten to
cover the chin strap (HM-06) and the occipital yoke (HM-03), both of which are on the frame
and are wiped in the row above. The machine-wash row of Rev A is deleted.

**Prohibited, with the reason:**

| Prohibited | Why |
|---|---|
| Autoclave, any part | MJF PA12 and TPU 85A distort; the +0.15 / −0.05 mm bayonet fit is lost |
| Immersion of HM-01 | The frame contains the harness, the LEDs and, in Phase 2, the electronics |
| Ultrasonic on the boom capsule | The electret capsule is not sealed |
| Bleach or any hypochlorite on Ag/AgCl | Destroys the sintered surface, and with it the lead-off calibration T10 depends on |
| Acetone, MEK, any ketone | Crazes PA12 and attacks the PTFE-jacketed harness terminations |
| Abrasives or wire wool on a cup face | Removes sintered material; the cup is no longer sintered, it is plated |
| Dishwasher | Alkaline detergent attacks Ag/AgCl and the TPU |

Record the agent, its lot and its expiry on F1 §4. An expired agent invalidates the
turnaround and the cleaning is repeated.

### R6 -- gel-port flush (8 min hands-on, 20 elapsed)

Each HM-04 carries a 2.5 mm gel port through the top, coaxial with the cup. Flush each of
the eight with warm (≤ 40 °C) potable water using **the same blunt-tip syringe the
participant used to fill it**, two full 10 ml passes per port, until the return runs clear.
Follow with one pass of demineralised water. Blow through with dry compressed air at ≤ 1 bar
held 20 mm clear of the port. Hardened paste that will not clear is **FC-18**; soak that
assembly's port with demineralised water for 15 min and repeat once before escalating.

### R7 -- frame, case and panel wipe (6 min hands-on, 8 elapsed)

Wipe every external surface of the frame, the yoke and ratchet, the chin cup shell, the
POD-P1 shell, the panel legend, the host and charge USB-C apertures and the label with 70 %
IPA, kept visibly wet for two minutes. The label is matt polyester with permanent acrylic
adhesive and is specified IPA-resistant (ASM-EEG-007 Rev B section 7); check its legibility at
every turnaround and record the count of wipes it has now seen, because 25 wipes is the
figure it was specified against and **nobody has tested it**.

### R8 -- TPU pad and chin-strap liner replacement (6 min)

Fit four new HM-02 pads (brow 85 x 22 x 8 mm, occiput x 2, crown) and one new HM-06
chin-strap liner. They snap into the frame's pad mounts; no adhesive is used, so nothing has
to be scraped off next time. Confirm each pad is fully seated and that no pad bridges a gel
port.

### R9 -- cell check and charge (5 min hands-on, 90 elapsed)

1. Read the MAX17048 state of charge and the open-circuit voltage after a 30 min rest.
2. **Honest limit.** The MAX17048 is a voltage-based ModelGauge part. It reports SoC but not
   a cycle count and not true capacity, so cell health here is inferred from rested OCV and
   from the SoC drop over a timed load, not measured. A true capacity check is done off the
   unit on a bench cell analyser at every fifth turnaround (section 3).
3. Load check: record at 1000 Hz for 20 min (≈150 mA per T3) and record the SoC drop.
   Calculated expectation on a healthy 3,000 mAh cell is ≈1.7 percentage points; a drop above
   4 points is **FC-07** and the cell is replaced.
4. Charge to the **despatch state of charge of 25 to 30 %**, not to full. **PI967 section II
   imposes no state-of-charge limit of its own**; the 30 % ceiling in the regulations belongs
   to cells shipped alone by air under PI965. The ≤ 30 % here is a self-imposed programme
   control adopted under REG-EEG-012 Rev B §3.8 and required by RFQ S-09. This overrides the
   "40 to 60 %" figure in the v1 audit outline, which predates S-09. The participant charges the kit on arrival, and the quick-start card says so.
5. **Charging above 45 °C is inhibited by RFQ E-23, and the thermistor that RFQ S-04 asks
   for is not fitted and stays not fitted:** there is no NTC net in `design.py` and no
   thermistor way on J12 or J13, so S-04 is not met, the charge inhibit rests on the charger
   module's own thermal regulation alone, and the bench cannot test it. It is an open
   hardware item (section 10 item 10, DSN-EEG-003 Rev C §11, RISK-EEG-011).
6. **Cell replacement policy. This list is the only one in the package.** Replace the cell
   outright **annually on age, whatever its condition**, and at any of: measured capacity
   below **80 % of rated** at the bench check of section 3.2, OCV below 3.5 V after a full
   charge and rest, a swollen or deformed wrapper, a damaged protection module, a reported
   drop with the cell in the kit, or five years from the cell's own date code -- whichever
   comes first. The 80 % trigger is measurable only off the unit: step 2 above says why the
   MAX17048 cannot produce a capacity figure, so 80 % is read from the bench cell analyser
   every fifth turnaround and not from the gauge every turnaround. REG-EEG-012 Rev B section
   3.8 cites this list; the "2 years in the fleet, or the gauge below 80 %" it carried at the
   first issue of that revision is withdrawn, because it was a second policy for the same
   cell and its gauge trigger could not be read. The cell lives in the HM-10 keyed carrier
   behind the HM-08 quarter-turn hatch and is changed without opening the POD-P1 lid.

### R10 -- refit and functional re-test (15 min hands-on, 50 elapsed)

1. Refit eight cups, and the sequence is the bayonet's own. **Enter** with the carrier's two
   lugs aligned to HM-04's two entry slots -- the lugs stand 0.65 mm proud of the Ø9.10 mm
   carrier body at an outer radius of 5.20 mm, the slots are 1.70 mm wide at an outer radius
   of 5.55 mm, so there is 0.35 mm of clearance and the carrier drops in without being forced.
   **Turn a quarter**, 90° clockwise seen from the cup face, with the key: the lugs run round
   the 100° circumferential run, which is 90° of travel and 10° of over-run, and the end of
   the run is a positive angular stop. **The lip retains it**: 1.10 mm of printed PA12 below
   the run, on which the lugs come to rest with the spring pressing them down. There is no
   snap and no detent -- one was drawn and removed, because a 0.35 mm interference in a
   material printed to ±0.15 mm is asking the tolerance to be half the feature. Then confirm
   retention by hand: a light straight pull of about **10 N** must not release it. There is no
   torque figure, because the joint is a bayonet held by a spring against a lip and not a
   threaded fastener; the acceptance is **release-with-the-key and retention-without-it**, and
   turning it back out needs the HM-09 key, which is the point.
2. Refit the ear clips and the boom. Confirm the boom detaches and re-seats at the temple.
3. Run the **RTS-1 return-to-service subset** of TST-EEG-004 Rev C. TST-EEG-004 owns every
   step number used here; this document invents none.

| RTS-1 step | Test | Limit | Why it is in the subset |
|---|---|---|---|
| T2 | Module seating and continuity: thirteen module assemblies, twelve on MP-01 plus the DevKitC-1 in J6 and J7 | All present, every jumper seated | The kit has been in a courier network twice |
| T5 | USB enumeration through the host socket, `iSerialNumber` = the unit serial `TIOV-B-nnnn` | Pass, serial matches label | Proves identity is unchanged since dispatch |
| T8 | Noise floor, inputs shorted to AGND_REF, 60 s, 0.5-70 Hz | ≤ 1.0 µV RMS on EEG channels | The single most sensitive indicator of a damaged input network |
| T10 | Lead-off against the 4k99, 10k0 and 49k9 references of FIX-01/A | Within 15 % | Catches a worn cup, a cracked conductor and a poor bayonet seat |
| T11 | Contact-light mapping, all dark on block start, read with the FIX-01/E colorimeter head. **The bicolour phase driver was written on 2026-09-02 and TST-EEG-004 T11 is now specified against it**; the states are produced at the electrode inputs, because the colour is computed from the converter's lead-off status and cannot be commanded. All three states can be produced as of 2026-09-02 (FW-D17): the colour comes from a positive-side comparator swept between two thresholds, not from a second detector this single-ended montage does not have. What is not yet established is the impedance at each boundary, because the thresholds are datasheet endpoints (TST-EEG-004 T11 Note 3) | Correct mapping, green, amber, red and both dark states; the reference resistances are provisional until a unit is characterised | Eight lights, eight sites, and a swap is invisible in the data |
| T13 | Timing self-test, 40 tones | Median ≤ 1 sample, p95 ≤ 2 | The timing chain is what the study rests on |
| T17 | Buttons, mic mute, headphone level into the **47.0 Ω** FIX-02/D load | Aux bits correct; mute ≥ 60 dB; level within 1 dB of `hp_level_db` | The three most-handled controls |

The T17 load is 47.0 Ω because RFQ A-04 is restated as **32 to 64 Ω** and the shipped
headphone, the ATH-M20x, is a 47 Ω model; the output level is measured per model at
calibration, not assumed. The 32.0 Ω load of Rev A is withdrawn.

Steps deliberately **not** in RTS-1: T7 and T9 need the FIX-01/F 1000:1 divider built by
JIG-EEG-009 Rev B and a signal generator, and the gain and CMRR constants cannot drift
unless the front end has been opened -- they are re-run whenever section 5 says so. T14 runs
for 30 min and is run every fifth turnaround rather than every one. T6 and T16 are re-run
only when identity changes.

4. **Release rule.** A kit fails release, and does not go back into circulation, if any T8
   channel exceeds 1.0 µV RMS, any T10 value falls outside 15 %, any cup is loose, the label
   and the record disagree, or any structural damage is unrepaired. **T11 mapping is a release
   criterion from the first image that carries the contact-light driver onwards.** That driver
   now exists in source (2026-09-02), so the weakening this manual carried is on its way out;
   it is not out yet, because no image has been built for the target and no unit exists to run
   one on. Until a unit is running such an image the operator records that T11 could not be
   run and the kit is released on the remaining criteria, which stays a deliberate and stated
   weakening of the release gate. When it can be run, the **red state alone** is recorded
   DEFERRED for the reason in TST-EEG-004 T11 Note 3, and mapping, green, amber and the two
   dark states are release criteria.

### R11 -- consumable replenishment (8 min)

Refill to the section 3 per-turnaround table, checking every expiry date as it goes into the
pouch. An item that expires before the loan period ends does not ship.

### R12 -- repack, photograph and seal (12 min)

Pack to the CASE-00 **Rev C** foam schedule -- seven loose-laid 25 mm layers, nine bays,
no card bay, all the printed matter in the lid. **The bay schedule is not restated here: PKG-EEG-015
Rev B section 2.2 owns it and is cut from the DXF, and a second copy at the bench is a
second chance to drift.** Work from the laminated photograph in the lid and from PKG-EEG-015
Rev B §2.2. The helmet travels assembled and upright, supported at the halo, so nothing
bears on the cups -- the same condition as in service, deliberately. The bay legended
SPARE CELL ships **empty**: REG-EEG-012 Rev B §3.1, RISK-EEG-011 Rev B §6.1 and the
QP-EEG-010 audit row all rule that no spare cell travels with a kit in circulation. **The bay
itself stays in the foam.** It carries a spare only on depot-to-depot moves handled by the
programme's trained shipper, and its tag reads `SPARE CELL -- DEPOT ONLY, EMPTY IN
CIRCULATION`; PKG-EEG-015 Rev B section 7 governs the bay and its tag. Photograph
the packed case open and file the photograph against the kit ID. Fit two new numbered tamper
seals and record their numbers. Confirm, initialled, that **no HM-09 key is in the case**
(section 4).

---

## 3. Consumable and wear schedule

Quantities are per kit unless stated. **What the consumable lines are is owned by
PKG-EEG-015 Rev B section 1.1 group 5, the kit packing list, derived in turn from RFQ A-05;
the tables below give only the service-side replenishment quantity and trigger.** Session
counts come from the per-session signed records rolled up per unit serial in the asset
register, so "every 25 sessions" is a queryable trigger and not a memory. A loan is two to
three sessions, so 25 sessions is about ten turnarounds, or roughly half a year per kit.

### 3.1 Every turnaround

| Line (per PKG-EEG-015 Rev B §1.1 group 5) | Qty | Trigger |
|---|---|---|
| HM-02 TPU pads (brow, occiput x 2, crown) | 4 | Every turnaround, discarded at R4 |
| HM-06 chin-strap liner | 1 | Every turnaround, discarded at R4 |
| Conductive EEG paste, 100 g | 2 | Every turnaround, expiry checked |
| Abrasive skin-prep gel, 100 g | 1 | Every turnaround, expiry checked |
| Saline wipes | 30 | Every turnaround |
| Cotton buds, gauze | 1 set | Every turnaround |
| Blunt-tip syringes | 4 | Every turnaround |
| Disposable EMG snap pads | 30 (1 pack) | Every turnaround, expiry checked |
| Boom windscreen | 1 | Discarded at R5 |
| Consumables pouch, labelled | 1 | Every turnaround |
| Tamper seals | 2 | Fitted at R12, numbers recorded |
| Outer double-wall carton and return-label pocket | 1 | Every turnaround |
| Quick-start card | as needed | Replaced when marked |
| Disinfectant and detergent working solution | 1 batch | Made up at R5, lot and expiry recorded |

### 3.2 Every 5 turnarounds

| Line | Action |
|---|---|
| Headphone ear cushions (ATH-M20x, 47 Ω) | Replace, not wipe |
| Cell | Full capacity check on a bench analyser, off the unit; record measured mAh. Below **80 % of rated** the cell is replaced -- this is the only measurement in the programme that can produce that number, and section 2 R9 is the policy it feeds |
| TST-EEG-004 Rev C T14 | 30 min microSD frame-count run, added to RTS-1 |
| HM-09 key | Inspect lugs for wear and rounding; measure the 2.0 x 1.2 mm lug across flats |
| Case foam | Inspect for compression set; replace any layer whose bay no longer retains its item |

There is no headband row. A-03 is withdrawn as a kit item (section 2 R5) and the chin strap
and occipital yoke it is rewritten to cover are wiped at every turnaround, not laundered at
every fifth.

### 3.3 Every 25 sessions on a given helmet

| Line | Qty | Note |
|---|---|---|
| Sintered Ag/AgCl cups | 8 fitted + 2 spare | RFQ A-01. Replaced outright, not re-plated |
| Ag/AgCl ear-clip references | 2 | Same wear mode |
| EMG snap-to-DIN leads (WH-06) | 3 | The lead is the wear item, not the pad |

Replacement is triggered by **either** the 25-session count **or** a T10 drift trend: three
consecutive turnarounds in which any channel's reading at the FIX-01/A **10k0** reference
moves monotonically by more than 5 % replaces that helmet's cups early, whatever the count
says. The three references are the E96 parts 4k99, 10k0 and 49k9 (TST-EEG-004 section 14
T10); "5 k / 10 k / 50 k" was the rounding of them.

### 3.4 Annually, per kit

| Line | Note |
|---|---|
| Protected 18650 cell | Replaced on age at twelve months regardless of condition. Section 2 R9 holds the whole replacement list, age and condition together, and REG-EEG-012 section 3.8 cites it rather than restating it |
| POD-P1 lid gasket | Compression set; replaced with the lid open for any other reason |
| POD-P1 host-aperture gasket | The gasket around the isolator module's USB-C receptacle; inspected at every turnaround, replaced annually or on damage (section 5.5) |
| Foam insert, all seven layers | Replaced if any bay has lost retention |
| Case hasps and pressure valve | Function check; replace the case on a failed hasp |
| Golden-unit comparison | The kit's T8 and T10 values compared against unit **TIOV-B-0001**, held by the programme and re-measured annually (QP-EEG-010 Rev B §11) |
| Label legibility | Against the wipe count of section 2 R7 |

There is no gland or captive-cable line. The host link is a socket (section 5.5).

### 3.5 Fleet stock model, calculated at 20 kits and 400 turnarounds a year

**Two fleet sizes appear in this manual, on purpose, and they are different bases.** This
consumables model is calculated on a 20-kit operating fleet at 20 turnarounds per kit per
year, which is 400 turnarounds. Section 6 sizes spares on the RFQ pricing template's 25-unit
break, which is 500 turnarounds a year. Neither number is a forecast of the other, and a
fleet actually built at 25 kits scales this table by 1.25.

| Line | Annual demand | Arithmetic | Reorder point |
|---|---|---|---|
| TPU pads | 1,600 | 400 turnarounds x 4 | 300 |
| Chin-strap liners | 400 | 400 x 1 | 80 |
| EEG paste, 100 g | 800 | 400 x 2 | 160 |
| Prep gel, 100 g | 400 | 400 x 1 | 80 |
| Saline wipes | 12,000 | 400 x 30 | 2,400 |
| EMG pad packs of 30 | 400 | 400 x 1 | 80 |
| Sintered cups | 400 | 20 kits x 2 changes x (8 + 2) | 120 |
| Ear clips | 80 pairs | 20 x 2 x 2 | 20 |
| EMG lead sets | 120 leads | 20 x 2 x 3 | 30 |
| Cells | 22 | 20 kits + 10 % attrition | 6 |
| USB-C leads (RFQ A-07, two per kit: host and charge) | 16 | 40 in service, loss or damage at 40 % a year *assumed* | 8 |

The cup line is the one that stalls a fleet: the Greentek MOQ is 200 pieces, about 16 kits'
worth, so the 400-piece annual demand is two MOQ orders and an unplanned reorder is a
multi-week gap. The reorder point of 120 is set at three months of demand against a stated
four-to-six week lead time. Paste and adhesive pads carry expiry dates and are managed FIFO
with lot and expiry recorded per kit at packing.

**Ownership.** The manufacturer supplies the **first fill** of every consumable line as part
of the kit price (RFQ section 10, "Consumables pack (per kit)"). Every fill thereafter is
bought by the programme. This was ambiguous in v1 and is settled here.

---

## 4. Service-key control (HM-09)

The service key is the only means of releasing a cup, and it is deliberately absent from the
participant's kit. In v1 that sentence was the entire control: no register, no count, no
marking, no packing check, and no key file in `mech/`. All five are closed here.

### 4.1 The part

`mech/stl/HM-09_service_key.stl` and `mech/step/HM-09_service_key.step`, generated by
`tools/mech_gen.py:hm09()`, MJF PA12. Knurled grip disc ⌀18.0 x 6.0 mm with eight 1.6 mm
flats, shaft ⌀10.0 x 28.0 mm, tip spigot ⌀8.8 x 4.0 mm, and two drive lugs 2.00 x 1.20 x
2.20 mm high on a 4.20 mm radius. Overall length 40.2 mm, envelope 17.9 x 17.9 x 40.2 mm,
3.9 cm³.

**The joint the key turns, restated on 2026-09-02 against the geometry that now assembles.**
Rev B described the key's lugs as engaging "the two HM-04 bayonet slots (2.2 x 1.4 mm, 2.4 mm
deep, 4.2 mm radius) that `mech_gen.py:hm04_body()` cuts". **That sentence is superseded**, on
two counts: the function is `mech_gen.py:hm04()`, and the key does not engage HM-04 at all --
it passes *through* HM-04's entry slots and engages the **HM-05B carrier's** two drive notches,
1.50 mm wide by 2.60 mm deep in the underside rim and cut at 90° to the carrier's own bayonet
lugs. The dimensions that matter to a service technician, all read off the released generator:

| Feature | Value |
|---|---|
| HM-04 entry slots, two at 180° | 2.30 mm radial x **1.70 mm** wide, outer radius **5.55 mm**, **3.60 mm** deep from the cup face |
| HM-04 circumferential run | **100°** -- 90° of travel and 10° of over-run -- radius 4.30 to 5.55 mm, **z 1.10 to 3.80 mm** above the cup face |
| HM-04 retaining lip | the **1.10 mm** of solid PA12 below the run, which is what carries a seated carrier in an inverted helmet |
| HM-05B bayonet lugs, two at 180° | **1.40 mm** wide, 2.10 mm tall, standing **0.65 mm** proud of the Ø9.10 mm body, outer radius **5.20 mm**, z 1.20 to 3.30 mm |
| HM-05B drive notches, two at 90° to the lugs | **1.50 mm** wide x 2.60 mm deep in the underside rim -- what the key's lugs engage |
| Carrier in bore | Ø9.10 x 8.60 mm body in a Ø9.20 x 9.00 mm bore: 0.10 mm diametral clearance and **0.40 mm of axial float**, which is the travel the cup makes when it is pressed against the scalp and the spring takes up, not slack |

Two of those numbers were wrong until 2026-09-02 and the joint did not work: the lug sat at an
outer radius of 5.40 mm against a 5.30 mm slot, because 0.40 mm of union overlap had been added
to the lug box's width without being taken off its centre, and the slot was 1.40 mm wide for a
1.40 mm lug -- zero tangential clearance in a material printed to ±0.15 mm. **There was also no
circumferential run at all**: two straight axial pockets, so the carrier went in and could not
rotate. It was a plug fit, not a bayonet, and every procedure in this manual that says "turn the
key" described something the released geometry could not do. `tools/simulate_production.py` now
measures the boolean at four rotations and three axial positions on every run: **0.000 mm³ of
interference through the quarter turn, 0.000 mm³ through the 0.40 mm of spring travel, and
1.557 mm³ of lip engagement when the seated carrier is pulled down**. Those are measurements on
the model, not on a part.

**The acceptance is the FIT-01 coupon, and the coupon does not yet carry the joint.** Bayonet
bore nominal ⌀9.20 mm at +0.15 / −0.05 mm is checked on FIT-01 (60.0 x 24.0 x 10.0 mm, bores
9.20 / 9.35 / 9.15 mm) at every print batch, QP-EEG-010 Rev B IP-9 -- but three plain bores gate
the **bore diameter only**. `fit01()`'s docstring says the coupon "carries the cup bayonet" and
its geometry does not: no entry slot, no run, no lug. **FIT-01 must be re-cut to carry the entry
slot, the run and a lug, printed in the batch and pulled, before the run is called released**,
and the retention this manual asks for -- section 5.4's 10 N and WH-EEG-008 H6's 15 N -- must be
demonstrated on that coupon. Nothing in this package has been printed, so the first coupon is
the first physical evidence that any of the above turns. Section 10 item 17.

### 4.2 Quantity and register

| Holder | Keys | Numbers |
|---|---|---|
| Operator 1 | 2 | K01, K02 |
| Operator 2 | 2 | K03, K04 |
| Brussels bench spares, in the service cabinet | 2 | K05, K06 |
| Manufacturer's own service kit, for T2 and T18 rework | 1 | K07 |
| Sealed master, document safe | 1 | K08 |
| **Circulating kits** | **0** | -- |

**Eight keys are manufactured for the Phase 2 fleet.** The kit BOM carries no HM-09 line, so
as things stood zero keys would have been made and no kit could have been refurbished; the
keys are added to the service-stock line of the BOM, not to the per-kit line, so the kit
price stays comparable across bidders. **RFQ section 10's pricing template still has no line
for them**, nor for the section 6 spares, the WH-KEY-01 keying shrouds or the foam insert of PKG-EEG-015 §2.2
tooling, and that is an open commercial question (section 10 item 11), not a settled one.

Each key is engraved in the model with `HM-09 SERVICE KEY -- NOT FOR PARTICIPANT USE` and
its number. The register records: key number, holder, issue date, return date, and the
signature of the person who issued it. A key is signed out and signed back in; it does not
live in a drawer.

### 4.3 Packing enforcement

The negative check exists in two places and both must be initialled: ASM-EEG-007 Rev B
section 9 stage 6 line "HM-09 service key **not** in the kit", and the PKG-EEG-015 packing
list. Goods-in triage at R1 also searches the returned case for a key.

### 4.4 If a key travels by mistake

1. Quarantine the kit on arrival; do not release it on the normal path.
2. Recover the key, check its number against the register, and record who packed it.
3. Inspect all eight cup seatings for signs of removal: a cup out of rotational alignment
   with its light window, paste inside the bayonet, or a marked lug slot.
4. Run RTS-1 in full and additionally re-run T7 if any cup shows evidence of removal, because
   an incorrectly refitted cup changes the source impedance the gain figures were taken at.
5. Record the event in the device history record and in the risk file's post-production loop.

### 4.5 The honest limit of this control

The design files are published under CC BY-SA 4.0. The key geometry is public and anyone
with a printer can make one. **The control is procedural, not physical.** Its purpose is to
stop casual and accidental cup removal by a participant who is trying to help, and it does
that well. It is not a barrier against a determined person, it is not claimed to be one, and
the reuse-path safety argument must not rest on it.

---

## 5. Repair procedures

Each procedure states its tools, its estimated time, the re-test required, and -- the
question that decides whether a repaired unit can go back into a study -- whether the unit's
calibration record survives.

### 5.1 What the calibration record is made of

| Constant group | Owned by | Regenerated when |
|---|---|---|
| Per-channel gain (T7), noise floor (T8), crosstalk and CMRR (T9) | The carrier's R1-R16 / D1-D16 / C1-C16 network and the two ADS1299 modules | Any repair touching J2, J4, J14, an input network or an ADS module |
| Lead-off constants (T10) | The above plus the cup, the conductor and the bayonet seat | Any cup, conductor or ADS module change |
| `hp_level_db` and the E-29 volume-register clamp (T17, E-13) | The ES8388 codec and the specific 47 Ω ATH-M20x headphones | Codec swap or headphone replacement |
| Timing constants (T13, F-21) | The ESP32-S3 module and the codec | Either module swapped |
| Identity: ATECC serial, public key, fingerprint | The ATECC608B at J11 | ATECC or carrier replacement -- see 5.8 |

**Corrected 2026-09-02.** The input network's series resistors are **68 kΩ**: ECO-EEG-024 is
applied, and the calculated single-fault DC worst case is **36.8 µA against S-02's 50 µA
limit, so the requirement is met on the calculation**. Until that date this paragraph read
"47 kΩ on the Phase 1 prototypes and the single-fault DC leakage requirement S-02 is not met
with them fitted … 53.2 µA against a 50 µA limit", with ECO-EEG-024 carried as a proposal.
The flatness requirement moves with the resistor and only one branch is now in force:
**E-10 is ±1.0 dB at 68 kΩ**, which is the branch the requirement states for this case; the
±0.5 dB branch belonged to the 47 kΩ that is no longer fitted. What has not changed: nothing
has been measured, T23 is still owed on a unit that does not exist, and **SR-01 is closed in
the design and not signed off**. Two rules for the bench, and the first is new. **Fit 68 kΩ**:
any input network rebuilt from here takes the ECO-EEG-024 value. And **record which value the
unit in front of you carries**, because an early board may still be stuffed with 47 kΩ; a
mixed board is not released.

### 5.2 Replace a broken conductor through the channel cover

| | |
|---|---|
| **Tools** | Plastic pick, fine tweezers, temperature-controlled iron, crimp receptacles, continuity meter, HM-09 key, ESD mat |
| **Time** | 75 min per conductor, estimated |
| **Procedure** | Release the cup at the affected site. Lift the snap-in cover strip on the skull-facing side of the affected section with the plastic pick. Cut the failed conductor at both ends, leaving the old wire in place as a draw wire. Tie the new conductor to it at the pod end and draw it through. Terminate at the HM-04 bayonet tag and at the J14 or J30 receptacle per WH-EEG-008 Rev B section 3, re-coil the 40 mm site service loop and the 120 mm pod service loop, and close the strip with no conductor trapped. |
| **Re-test** | T2, T8, T10, T11 on all channels; T7 on the repaired channel and its two neighbours. T11 is runnable from the first image carrying the contact-light driver, with the red state recorded DEFERRED (section 2 R10) |
| **Calibration record** | **Regenerated** for the affected channel's gain, noise and lead-off entries. Previous values are retained in the history, not overwritten |
| **Escalation** | If the draw fails and the channel cannot be re-run, the frame is scrapped and replaced from the spare-frame float. This is the risk DSN-EEG-002 Rev E section 12 finding 1 accepted deliberately |

### 5.3 Replace the boom

| | |
|---|---|
| **Tools** | 2 mm hex key, continuity meter |
| **Time** | 20 min |
| **Procedure** | Detach HM-07, the boom arm, at the temple; unplug WH-03B at the panel connector; fit the replacement; dress the 1700 mm lead; confirm the detach force is at least 30 N (WH-EEG-008 Rev B H6). The boom carries the **bare electret capsule and its screen only**, on the J18 pigtail; the preamplifier is on the MP-01 module plate at J21 and is not disturbed by this repair |
| **Re-test** | T12 envelope onset on the voice channel, T17 microphone gain |
| **Calibration record** | **Survives**, except the voice-microphone gain reported by the E-16 reference-tone path, which is re-measured and re-recorded |

### 5.4 Replace a cup or a seized bayonet

| | |
|---|---|
| **Tools** | HM-09 key, 10 N spring gauge, FIT-01 coupon |
| **Time** | 10 min for a cup; 90 min if the HM-04 body itself is damaged |
| **Procedure (cup)** | Release with the key as R4 steps 2 and 3: the key's lugs through the entry slots into the carrier's drive notches, a quarter turn anticlockwise seen from the cup face, the lugs off the lip and out through the slots. Discard the old cup. Fit the new one as R10 step 1: enter with the lugs in the slots, turn a quarter clockwise to the end of the 100° run, and let the spring seat the lugs on the 1.10 mm retaining lip. Verify **release-with-key and retention-without-key** against the 10 N pull. **The field-replaceable item is the carrier assembly, not the cup alone** -- HM-05A, HM-05B and HM-05C are joined once in the shop, which is what keeps a soldering iron out of this procedure and the joint out of the R5 ultrasonic bath |
| **Procedure (seized bayonet)** | A bayonet that will not turn is **not** forced. The HM-04 body is bonded into the frame at manufacture and cannot be replaced in the field, so the decision is: soak the joint with demineralised water for 30 min and retry once; if it still will not turn, the frame goes to service and, if the joint is damaged, the frame is scrapped. **Do not lever a stuck carrier axially**: the retaining lip is 1.10 mm of printed PA12 and it is the only thing holding a seated carrier, so a lip broken in the field turns a cup change into a scrapped frame |
| **Re-test** | T10 and T11 on the affected channel |
| **Calibration record** | **Survives**, with the T10 entry for that channel re-measured |
| **Open item** | Whether a bayonet still releases after 25 disinfection cycles is unknown. DSN-EEG-002 Rev E section 12 finding 8 asked for a 25-cycle release-and-refit test with disinfectant exposure on three assemblies, measuring release torque and retention force each cycle. It has not been run. Until it has, seizure is an unquantified risk to the whole fleet model |
| **Open item, added 2026-09-02** | **Nothing has been printed.** The bayonet turns in the model and is measured there -- 0.000 mm³ of interference through the quarter turn and through the 0.40 mm of travel, 1.557 mm³ of lip engagement (section 4.1) -- and it has never turned in PA12. **The FIT-01 coupon is the acceptance**, and it must first be re-cut to carry the entry slot, the run and a lug, because as released it is three plain bores. Until a coupon is printed and pulled, both figures in this procedure -- the 10 N here and WH-EEG-008 H6's 15 N -- are requirements and not results (section 10 item 17) |

### 5.5 Replace a host or charge lead, and the host-aperture gasket

**The host link is a socket, not a captive cable.** The host connector is the USB-C
receptacle on the ADuM4160 isolator module, presented through a gasketed aperture in the
POD-P1 right-hand wall; the participant plugs one of the two RFQ A-07 cables into it, and the
other into the separate charge-only USB-C receptacle. WH-08, the captive 2 m lead, its P-clip
and the SKINTOP ST-M12x1.5 gland are **deleted from the Phase 1 build** and the gland repair
procedure of Rev A is deleted with them; a captive lead through a gland is a Phase 2 item for
the helmet shell, and POD-P1 carries no gland feature.

| | |
|---|---|
| **Tools** | None for a lead; 2.5 mm hex key and a torque driver for the gasket |
| **Time** | 2 min for a lead; 25 min for the gasket, which needs the lid open |
| **Procedure (lead)** | Discard the damaged lead and issue a replacement from the A-07 stock. No tool, no disassembly, no re-torque. Record the replacement on F1 §5 |
| **Procedure (gasket)** | Open the POD-P1 lid, lift the moulded gasket from the host aperture, clean the seat, fit the replacement, close the lid and torque it to 0.60 N·m in two passes. The isolator module itself is not disturbed |
| **Re-test** | T5 enumeration, T15 ring-buffer backfill |
| **Calibration record** | **Survives** |
| **Live non-conformance** | The only isolator module named as a candidate presents a **USB-B** receptacle while RFQ E-24 asks for USB-C, and this is not settled. The interim answer is a short USB-B-to-USB-C panel pigtail, **WH-09**, fitted inside the aperture, until an isolator module with a USB-C host connector is qualified. A unit built with WH-09 has the pigtail replaced as a wear item on the same trigger as the gasket |

### 5.6 Swap a module on the carrier

Field-replaceable units, one row per module type. Swap difficulty is bench minutes for a
technician at an ESD workstation. **There are twelve purchased module types and thirteen
module assemblies per unit, because the ADS1299 breakout is fitted twice.** ICD-EEG-006 Rev
B section 1 owns the module-to-connector table; the sockets below are repeated only so the
technician can find the jumper.

| FRU (module type) | Socket | Time | Re-test | Calibration record |
|---|---|---|---|---|
| ADS1299 breakout, assembly #1 | J1, J2, J23 | 30 | T7, T8, T9, T10 | **Regenerated** (all 16 gain and noise values) |
| ADS1299 breakout, assembly #2 | J3, J4, J29 | 30 | T7, T8, T9, T10 | **Regenerated** |
| ESP32-S3-DevKitC-1-N16R8 | J6, J7 | 20 | T5, T13, T14 | Survives; timing constants re-measured |
| ES8388 codec | J8, J9 | 20 | T12, T17 | `hp_level_db` and the E-29 clamp **regenerated** |
| ADuM4160 isolator | J10 | 15 | T5, T15 | Survives |
| **ATECC608B** | **J11** | **20** | **T5, T6, T16** | **Identity changes -- see 5.8** |
| bq24074-class charger | J12 | 20 | T3, T4, T21 | Survives |
| MAX17048 fuel gauge | J12 (Y jumper) | 20 | T3 | Survives |
| TPS63020-class buck-boost | J25 | 20 | T3, T21 | Survives. **Omitted from the Rev A table in error; without it the board has no V5V rail and does not power up at all** |
| microSD breakout | J20 | 15 | T14 | Survives |
| 74HC595 shift register | J19 | 15 | T11 | Survives |
| Boom microphone preamplifier | J21, with the boom capsule on the J18 pigtail | 20 | T12, T17 | Voice gain re-measured |
| Room microphone module | J28 | 15 | T17 | Room gain re-measured |

Two notes on that table, both of which the bench needs before it orders a part.

**Which preamplifier is not settled.** The MAX9814 named in package v1 has automatic gain
control, which RFQ E-14 forbids, and disabling it is a module-dependent modification, so the
MAX9814 is **not approved** and the module is specified by interface in ICD-EEG-006 Rev B.
The preferred route is a fixed-gain part of the MAX4466 class. A swap therefore also
re-checks R89, which is do-not-populate by default and is fitted only if the module fitted
does not supply its own electret bias.

**Charger and gauge.** One combined charger-plus-gauge assembly on a single J12 jumper is
the baseline; where a combined assembly is fitted, the two rows above are one
field-replaceable unit. **That baseline changes neither count.** There are twelve module
types and thirteen module assemblies per unit however J12 is populated, because what makes
the thirteenth assembly is the second ADS1299 breakout and not the charger. Where two
separate breakouts are supplied, the gauge mounts on MP-01 and its VBAT and I²C taps are
made at the MP-01 end of a Y jumper drawn in ICD-EEG-006 Rev B section 3.3 -- a drawn part,
not a hand-built variation.

Modules sit on the **MP-01 module plate, 146.0 x 126.0 x 3.0 mm**, above the carrier on four
M3 x 18 mm nylon female-female hex standoffs with eight M3 x 6 nylon pan screws, and are
joined to the carrier by keyed 2.54 mm ribbon jumpers per ICD-EEG-006 Rev B. The 18 mm
standoff is load-bearing for safety, not just for packaging: it makes the slant path from
carrier copper, over the edge of the isolation keep-out and up to any host-side conductor on
MP-01, at least 18 mm, against the 8 mm the safety case asks for. Only the DevKitC-1 inserts
directly into J6 and J7, and it is reachable for flashing through the MP-01 opening. Every
jumper is labelled at both ends and every carrier socket that takes one wears the printed
keying shroud **WH-KEY-01**, so a swap is a plug operation and not a wiring operation. Note
also the module-header caveat in DESIGN_FACTS section 8 item 5: header geometry is not
fixed, so a replacement module of the same class may need a new jumper made by hand.

### 5.7 Replace the carrier itself

The carrier the technician meets is **EEG-CAR-01, 150.0 x 130.0 mm, four layers**: L1
signal, L2 reference plane, L3 reference plane, L4 signal, in a stack of mask / 35 µm L1 /
prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask, 1.60 mm
± 10 % finished, with through vias only at 0.60 mm pad on a 0.30 mm finished hole. Both inner
layers carry AGND_REF left of x = 62 mm and DGND right of it, stitched together only at the
star point. Package v1 said a two-layer carrier would be enough; doing the layout showed it is
not, because on two layers the bottom side has to be both the reference plane and the second
routing surface and it cannot be both. The bench consequence is small but real: **there is no
bottom-side plane to probe or to scrape back to, the inner planes are inaccessible, and a
carrier with a suspected plane fault is replaced, not repaired.**

No carrier has been fabricated. The Rev B fabrication data is **released for review under
RFQ-EEG-002A and not released for fabrication**: the routing was produced by the programme's
own tools, no human layout engineer has read it, and that review is what fabrication release
waits on. Nothing in this manual describes a board that a technician can hold today. What the
DRC report `kicad/EEG-CAR-01_RevB_DRC_report.txt` records is load-bearing for the service
argument of 5.6, so it is stated from the report rather than assumed: **all 145 nets are fully
connected and the report closes with "VIOLATIONS: 0"**; there is no copper inside the isolation
strip on any of the four layers; each reference plane is one continuous island per net on both
inner layers; no digital net crosses into the analogue zone; and there is exactly one
AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND bridge. The measured minima are 0.260 mm of
clearance on L1, 0.285 mm on the planes and 0.275 mm on L4 against a 0.20 mm rule, a narrowest
conductor of 0.20 mm, and a smallest plated hole of 0.30 mm.

Two things travel with that zero and both matter on a bench. The router **relaxed 169
connections** to close the board -- 36 took a conductor narrower than the 0.25 mm preferred
width, 133 kept full width and took a reduced gap, every one at or above the 0.20 mm minimum
conductor and gap -- so parts of this artwork sit at minimum geometry rather than preferred,
and that is where a lifted track or a rework bridge is likeliest. And the routing can still
change under the layout review, so a technician works to the revision marked on the board in
front of them and not to this description.

| | |
|---|---|
| **Tools** | Full bench, ESD workstation, provisioning station |
| **Time** | 180 min, plus TST-EEG-004 Rev C in full |
| **Procedure** | Transfer all thirteen module assemblies to the new carrier, or fit a spare assembled carrier and transfer only the ATECC608B if identity is to be preserved. Re-check R89 absent unless the fitted preamplifier needs it, R90 and R91 fitted as single links, R92 and R93 fitted, R94 and R95 (the 4.7 kΩ I²C pull-ups added to the carrier) present, and R85 at 150 kΩ (ASM-EEG-007 Rev B section 9) |
| **Re-test** | TST-EEG-004 Rev C **in full**, all steps, as a new unit |
| **Calibration record** | **Regenerated in full.** The old record is retained as a superseded revision in the device history record, never deleted |

The pod the carrier goes back into is **POD-P1, 163.0 x 143.0 x 58.0 mm external and 158.0 x
138.0 x 55.5 mm internal**, with a 163.0 x 143.0 x 6.0 mm lid on a 2.0 mm spigot. The stack
inside it is floor 2.5 + boss 6.0 + carrier 1.6 + standoff 18.0 + plate 3.0 + modules ≤ 18.0
= 49.1 mm against 55.5 mm internal, a margin of 6.4 mm. A technician who finds the lid will
not close has a module taller than 18.0 mm on MP-01, not a warped enclosure.

### 5.8 The identity rule

**Replacing the ATECC608B module at J11 changes the device identity.** The ATECC's 9-byte
factory serial is printed on the label and carried in the Data Matrix so a swapped secure element is detectable -- it is **not** the USB `iSerialNumber`, which is the unit serial `TIOV-B-nnnn` (F-04; RUL-EEG-021 section B). Its P-256 key pair signs every block,
and its fingerprint is on the label (M-03). A replacement module therefore:

1. must be re-provisioned per F-18 -- key generation, serial export, VID/PID, hardware
   revision, calibration constants, configuration-zone lock;
2. must be **re-labelled** with the new fingerprint -- the first 8 bytes of SHA-256 over the
   64-byte uncompressed public key, printed as 16 uppercase hex characters in four groups of
   four, defined once in FW-EEG-001 Rev C section 7 -- and the Data Matrix re-verified
   against the record;
3. must have the platform's device registration updated, and the participant's browser will
   be asked to re-authorise the device once, because the persistent WebUSB grant is bound to
   the old identity;
4. keeps its **programme serial** in the form `TIOV-B-nnnn` -- the serial belongs to the unit,
   not to the ATECC, so that the device history record remains continuous across the repair;
5. has its **old public key retired, not deleted**, so that every block signed before the
   repair stays verifiable for as long as the study data does.

Nothing in v1 said any of this, and a repaired unit could have re-entered the fleet with a
changed serial that the platform would treat as an unregistered instrument. That is a silent
data-integrity failure, which is why this rule is stated in bold and why 5.7 requires a
separate signature from the operator who performed the change.

---

## 6. Spares provisioning per 25 kits

Every quantity has arithmetic behind it. Failure rates marked *assumed* have no measured
basis; they are first estimates to be replaced by fleet data after one year.

| Line | Qty per 25 kits | Arithmetic |
|---|---|---|
| HM-01 frames, printed and harnessed | 2 | 25 kits x 20 turnarounds = 500 turnarounds a year; one unrecoverable conductor or bond failure per 250 turnarounds *assumed* = 2 a year (DSN-EEG-002 Rev E §4.1) |
| WH-01 / WH-02 harness sets | 2 | One replaced conductor per 250 turnarounds, plus one set held against a frame rebuild (WH-EEG-008 Rev B §10) |
| Boom assemblies (HM-07 + WH-03B) | 2 | The most-handled detachable part; one failure per 250 turnarounds *assumed* |
| Assembled carriers | 2 | 8 % of fleet, sized to keep two units in service while two are in RMA at a stated 4-week repair lead time |
| Bare EEG-CAR-01 boards | 7 | 25 % spare bare boards at the 25-unit break, per the RFQ pricing template; 6.25 rounds up |
| ADS1299 breakouts | 4 | 2 per unit x 25 = 50 fitted; 2 % annual module failure *assumed* = 1; held at 4 because this class has had long lead times |
| Each other module class (**ten classes**) | 2 each = **20** | Twelve module types less the ADS1299 breakout and the ATECC608B, which have their own lines, leaves ten: the ESP32-S3-DevKitC-1, the ES8388 codec, the ADuM4160 isolator, the bq24074-class charger, the MAX17048 gauge, the TPS63020-class buck-boost, the microSD breakout, the 74HC595, the boom preamplifier and the room microphone. 2 % annual failure on 25 fitted = 0.5; held at 2 so a swap never waits on a purchase order. The combined charger-plus-gauge assembly is the baseline, and one part number then serves both the charger class and the gauge class, so the ten classes are held as eighteen pieces. The class count does not change with it, and neither does the twelve-type, thirteen-assembly count of 5.6 |
| ATECC608B modules | 2 | Same rate, but every swap costs a re-provisioning and a relabel, so the stock is deliberately small |
| Sintered cups | 200 (1 Greentek MOQ) | 25 kits x 2 changes x 10 cups = 500 a year; rolling stock of 200 with a reorder point of 120 |
| Ear clips | 20 pairs | 25 x 2 changes = 50 pairs a year; 20 is about five months |
| EMG lead sets (WH-06) | 12 sets | 25 x 3 leads, one lead in four replaced a year *assumed* = 19 leads; 12 sets covers it with margin |
| USB-C leads, RFQ A-07 pattern | 20 | 2 per kit x 25 = 50 in service; loss or damage at 40 % a year *assumed*. There is no captive host cable and no gland insert to spare |
| POD-P1 host-aperture gaskets | 10 | One per kit replaced annually, less those replaced with the lid gasket |
| WH-09 USB-B to USB-C panel pigtails | 3 | Only where the fitted isolator module presents USB-B; quantity provisional because the isolator is not settled (5.5) |
| ATH-M20x headphones (47 Ω) | 2 | Loss and damage at 8 % a year *assumed* |
| Protected 18650 cells | 6 | 25 replaced annually on age, ordered in two batches; 6 covers early failures between batches |
| microSD cards | 4 | Card loss or unreadability at 15 % a year *assumed* |
| Travel cases | 2 | Hasp or shell damage at 8 % a year *assumed* |
| Foam insert sets, seven layers each | 6 | Compression set at 25 % a year *assumed* |
| HM-04 electrode bodies | 20 | Not a field spare -- HM-04 is bonded into the frame at manufacture. Held only to rebuild the 2 spare frames, 10 each |
| HM-02 pads / HM-06 chin-strap liners | see §3.5 | Consumable, ordered against the annual demand table, not held as spares |
| HM-09 service keys | see §4.2 | Service stock, never a per-kit line |

**Consignment question for the RFQ.** Which of these the manufacturer holds and which sit in
Brussels is a commercial decision the RFQ has not put to bidders, and RFQ section 10's
pricing template carries no line for any of it. The programme's position: modules, cups and
consumables in Brussels; bare boards and assembled carriers with the manufacturer,
replenished to the stated repair lead time.

---

## 7. RMA and fault reporting

### 7.1 Fault codes

One list, used by the participant's tick sheet, the goods-in triage, the RMA form and the
device history record, so that the same fault has the same name everywhere.

| Code | Fault | Usual route |
|---|---|---|
| FC-01 | A light never went green at one site | Operator: cup, conductor, T10 |
| FC-02 | All lights dark | Service: 74HC595 at J19, LED_V. **Corrected 2026-09-02:** this row said the bicolour driver was unimplemented and "all dark" was the expected state. The driver is written, so all-dark outside a recording block is a fault again -- but no unit has ever lit a light, so treat the first one as bring-up, not as service |
| FC-03 | A light stuck on or showing the wrong colour | Operator: T11. **Corrected 2026-09-02:** this row read "T11, when the driver exists"; the driver was written on that date. Two limits on what T11 can tell you: it has never been run, and this image never enables `LOFF_SENSN`, so a site with no contact shows amber rather than red and that is the image, not the light (section 4.1, T11 Note 3) |
| FC-04 | No sound in the headphones | Operator: headphones; else service, codec |
| FC-05 | The device was not recognised by the browser | Service: T5, isolator module, host lead, host socket |
| FC-06 | The session dropped or disconnected | Service: T15, host lead, host socket and its gasket |
| FC-07 | Battery flat before the end of a session | Operator: cell replacement |
| FC-08 | Would not charge | Service: charge receptacle, PTC F1, charger module |
| FC-09 | The boom microphone was not heard | Operator: boom capsule and pigtail; else service, the J21 preamplifier module |
| FC-10 | The room microphone was not heard, or mute stuck | Service: J28, MIC_MUTE |
| FC-11 | A button did not respond | Service: T17, RC debounce |
| FC-12 | The frame is cracked or broken | Service: assess, likely scrap |
| FC-13 | The boom is broken | Operator: 5.3 |
| FC-14 | A supplied USB-C lead is damaged | Operator: replace from A-07 stock, 5.5 |
| FC-15 | A cup is loose or missing | Operator: 5.4 |
| FC-16 | The case or foam is damaged | Operator: replace |
| FC-17 | The microSD is missing or unreadable | Service, and a data-loss report |
| FC-18 | A gel port is blocked | Operator: 2 R6 |
| FC-19 | Skin reaction, blood, or visible soiling | **Quarantine; scrap cups, clips, pads, liner** |
| FC-21 | The cell is swollen, hot or leaking | **Quarantine; do not charge; cell disposal route** |
| FC-30 | Seal broken or missing on arrival | Quarantine unopened, programme ruling |
| FC-40 | Kit not returned | Section 7.4 |
| FC-99 | Anything else, described in free text | Triage decides |

### 7.2 The form

**Part A, participant return** (travels in the case, prepaid): kit ID, dates out and in,
sessions completed, the FC tick list above in plain words, and a free-text box. No technical
vocabulary is asked of the participant.

**Part B, goods-in triage at Brussels**, completed at R1 and R10: seal numbers against
dispatch; packing photograph comparison; packing list ticked with missing lines priced; damage
photographed; battery SoC at receipt; microSD present and readable; RTS-1 values recorded.

**Part C, escalation to the manufacturer's RMA**: programme serial in the form
`TIOV-B-nnnn`, ATECC serial, hardware revision `EEG-CAR-01-B`, firmware image hash, the
failing TST-EEG-004 Rev C step numbers **with their measured values**, the suspected FRU,
whether the ATECC was disturbed, the return address and Incoterm for the repair leg, and a
field for the manufacturer's own findings and root cause. A board arriving without Part C is
a board arriving with no failure description, which is what v1 would have produced.

### 7.3 Repair or scrap

The decision is made at triage and recorded, not left to the bench.

1. Is the unit safe to power? A swollen cell (FC-21), water ingress, or exposed conductor
   goes no further until the cell is removed and the unit is dried and inspected.
2. Is the fault in a plug-in module? If yes, swap it per 5.6 and re-test. Cost is a module.
3. Is the fault in the frame? A cracked node, a delaminated HM-04 bond, or a conductor that
   cannot be re-drawn scraps the frame. A frame is €14 to €22 of print plus 180 min of
   Stage 3 labour; two frames per 25 kits exist for exactly this.
4. Is the fault on the carrier? Two rework cycles per pad and per barrel are permitted
   (ASM-EEG-007 Rev B section 10); beyond that the carrier is scrap and 5.7 applies. A
   suspected inner-plane fault is scrap on the first occurrence, because the planes cannot
   be probed.
5. Does the repair change identity? If yes, 5.8 applies before the unit is released.
6. Is the cumulative repair cost above 60 % of the current per-kit build cost? The figures in
   circulation are €523.32 at the 25 break and €474.95 at 50, and they are **provisional**:
   they come from `EEG_kit_BOM_for_bidders`, a workbook that is not in `package_v2.4/` and
   whose revision two documents give differently (section 10 item 12). If yes, the unit is
   retired and its modules harvested.

### 7.4 The participant side

A €150 refundable deposit is held while the kit is out and returned when a working unit comes
back. **"Working" is defined here so the decision is not discretionary:** every packing-list
line present except consumables; T8 at or below 1.0 µV RMS on all EEG channels; T10 within
15 % on all eight; case and helmet free of structural damage. T11 mapping joins that list
when the contact-light driver is implemented and not before. Anything else goes to the damage
schedule.

| Loss or damage | Charge | Basis |
|---|---|---|
| Headphones missing | €40 | Internal costed BOM Rev C line 39 at the 25 break *provisional, see 7.3 item 6* |
| Charger missing | €5 | Line 49 *provisional* |
| USB-C lead missing | €2 each | Lines 47, 48 *provisional*. Two travel with the kit: one is the host lead, one the charge lead |
| microSD missing | €8 | Line 18 *provisional* |
| Cell missing | €7 | Line 24 *provisional* |
| Boom broken beyond gooseneck wear | €9 | Line 14 *provisional* |
| Case cracked or hasp broken | €45 *provisional* | Line 50 prices the superseded smaller case; re-price against the RFQ M-05 case |
| Foam insert damaged | €14 | Line 51 *provisional* |
| Frame cracked | €100 capped | Print plus Stage 3 labour, capped at the deposit |
| Kit not returned (FC-40) | €150 | The whole deposit |

Every charge is capped at €150 in total. A waiver route exists and is used: the hardship
fund covers deposits and damage for participants who cannot meet them, and a waiver is a
programme decision recorded against the loan, not a bench decision.

Non-return workflow: reminder at day 14, day 21 and day 28; deposit retained at day 35; the
kit ID marked lost in the asset register; police and insurance notification above a €400
aggregate. Turnaround targets: triage within **2 working days** of receipt and refund within
**5**, so that the deposit does not become a barrier to taking part.

---

## 8. The refurbishment record

One record per unit per cycle, form **SVC-EEG-013-F1**, signed. It is the evidence that a kit
handed to participant twelve was processed the same way as the kit handed to participant one.

| Section | Fields |
|---|---|
| §1 Receipt | Kit ID; programme serial `TIOV-B-nnnn`; inbound seal numbers; loan number; participant assignment period (pseudonymous); date and time received; carton and case condition; packing-list return column; FC codes raised; quarantine start |
| §2 Data | Session files recovered with names and SHA-256; signature-chain verification result; ingest acknowledgement; secure-erase date and operator; card serial; new volume label |
| §3 Strip | Items out: 8 cups, 2 ear clips, boom, 4 pads, chin-strap liner; anything missing; sessions on this helmet since the last cup change |
| §4 Clean | Detergent lot and expiry; disinfectant lot and expiry; bath temperature and time; contact times achieved; frame wipe count to date; deviations |
| §5 Replace | Every part fitted with its lot number and expiry; consumables to the §3.1 table; leads and gaskets replaced; firmware version before and after any update |
| §6 Cell | Rested OCV; SoC at receipt; load-test SoC drop; despatch SoC; capacity if a fifth-turnaround check was due; cell lot and date code |
| §7 Re-test | RTS-1 numeric values -- T8 sixteen values, T10 eight by three, T13 median and p95, T17 mute depth and level into 47.0 Ω, and T11 recorded as run or as not runnable -- against the previous cycle's values, with the drift |
| §8 Release | Bayonet release-and-refit cycle count per site; consumables verified; foam schedule verified against PKG-EEG-015 Rev B §2.2; **HM-09 not packed** (initialled); outbound seal numbers; packed photograph reference; releaser's name and signature; date |

The completed F1 joins the device history record at QP-EEG-010 Rev B section 9.2, which
reserves exactly this slot: "Refurbishment record per SVC-EEG-013; parts replaced with their
lots; cell cycle count and OCV; disinfection record; re-test results if any; the participant
assignment period." The master copy is held by the programme for the life of the fleet plus
ten years. The delivery copy -- the printed calibration record that travels in the **case
lid pocket** beside the quick-start card -- is **reissued at every refurbishment**, so the
numbers in the case always match the numbers in the unit.

**The serial format is settled, and it is defined once and not here.** `TIOV-B-nnnn` is
defined in **PKG-EEG-015 Rev B section 5**, and this document cites it. What the service
bench takes from it is the rule that follows: the same serial appears in the label text, the
Data Matrix, the USB `iSerialNumber`, the calibration record and the packing list, and if
any two of those five disagree the unit is quarantined and does not go back into
circulation. The `OV-EEG-<phase><nnn>` and `TIOV-EEG-<phase>-<nnn>` forms of package v1, and
the modulo-23 check-character form, are all withdrawn; ASM-EEG-007 Rev B, QP-EEG-010 Rev B
and PKG-EEG-015 Rev B now carry `TIOV-B-nnnn` and nothing else.

---

## 9. What the participant is asked to do, and what they must never do

This section is the source text for the participant-facing card; IFU-EEG-014 carries the
illustrated version, and the disinfection guide in the pouch is the extract of section 2 R5.

**Please do:**

| | |
|---|---|
| On arrival | Charge the kit fully before the first session. It arrives deliberately part-charged because that is how a lithium cell is allowed to travel |
| To connect it | Take the USB-C cable that fits your computer, plug one end into the computer and the other into the socket marked DATA on the grey box. The cable is not attached to the box; it is meant to come out |
| Before a session | Put the helmet on, tighten the ratchet until it is firm and not tight, and add gel through the port at any site whose light is not green |
| During a session | Follow the runner on screen. If a light goes red, add a little more gel at that site |
| After a session | Wipe the outside of the frame with a supplied wipe. Nothing is taken apart |
| Between sessions | Charge the kit through the second socket, marked CHARGE. The helmet is never worn while the charge cable is connected |
| At the end of the loan | Repack to the labelled foam bays and the photograph in the lid, put the case in the outer carton, and use the prepaid label |
| If something breaks | Tick the box on the return form and tell us. Nothing that breaks is charged to you if it broke in normal use |

**Please never:**

| | |
|---|---|
| Never | Remove, turn or lever a cup. They are released with a tool you do not have, and by design |
| Never | Open the pod, the HM-08 battery hatch or any cover strip |
| Never | Wear the helmet while the charge cable is plugged in (RFQ S-01) |
| Never | Immerse the helmet, put it in water, or clean it with anything but the supplied wipes |
| Never | Use bleach, acetone, nail-varnish remover, or a dishwasher on any part of the kit |
| Never | Remove, read, copy or erase the memory card. Your recordings are on it and they are your evidence |
| Never | Lend the kit to anyone else, or let anyone else wear it |
| Never | Charge the kit from anything but the supplied charger |
| Never | Continue a session if any part becomes hot, smells, or the battery case looks swollen. Unplug it, put it down, and contact us |

---

## 10. Open items

| # | Item | Who closes it |
|---|---|---|
| 1 | **No safety engineer has reviewed the reuse path.** This document exists so that there is something to review. It does not authorise use on a person | RISK-EEG-011 Rev B safety review |
| 2 | The 25-cycle bayonet release-and-refit validation with disinfectant exposure (DSN-EEG-002 Rev E §12 finding 8) has not been run. Seizure remains an unquantified risk to the whole circulation model | Phase 1 test plan |
| 3 | Material compatibility of MJF PA12, TPU 85A and the sintered cups against 25 IPA and ultrasonic cycles is asserted from supplier data, not measured. The S-05 biocompatibility declarations are for virgin material and have not been re-checked after reprocessing | The disinfection validation protocol, then REG-EEG-012 Rev B |
| 4 | Label legibility after 25 IPA wipes is a specification, not a test result | Phase 1 first article |
| 5 | Every failure rate in section 6 marked *assumed* has no measured basis and is a first estimate | One year of fleet data |
| 6 | **Closed at this issue.** The serial format is `TIOV-B-nnnn`, defined once in PKG-EEG-015 Rev B section 5 and cited in section 8. ASM-EEG-007 Rev B, QP-EEG-010 Rev B and PKG-EEG-015 Rev B all carry that form, and the three package v1 forms are withdrawn. The row is kept rather than renumbered so that references to the item numbers below it do not move | Closed |
| 7 | **Closed at this issue.** The CASE-00 SPARE CELL bay stays in the foam and travels empty in circulation; it carries a spare only on depot-to-depot moves handled by the programme's trained shipper, and its tag reads `SPARE CELL -- DEPOT ONLY, EMPTY IN CIRCULATION`. PKG-EEG-015 Rev B section 7 rules the bay and its tag, and this manual's earlier plan to delete the legend at the next foam revision is withdrawn. The row is kept rather than renumbered so that references to the item numbers below it do not move | Closed |
| 8 | **The contact-light driver is written as of 2026-09-02**, so the item as Rev B stated it is closed: `firmware/main/main.c` reads the converter's positive-side lead-off comparator at two thresholds and lights a site green when it trips neither, amber when it trips only the sensitive one and red when it trips both, alternating with green in phase A and red in phase B. Two things replace it. The alternation quantises to the FreeRTOS tick, so it runs at about **250 Hz** rather than the compiled 240, which is inside E-27's "above 100 Hz" and is stated rather than hidden. And **the two thresholds are the ADS1299's documented endpoints, not measured trip points**, so the impedance at which a site turns amber, and the one at which it turns red, are not yet established -- a participant could be told to re-gel a site that was fine, or told nothing about one that was not. *Corrected again 2026-09-02 (FW-D17): this second point read "`LOFF_SENSN` is never enabled, so the red term can never be set". Red is reachable now, and enabling `LOFF_SENSN` was never the fix -- the montage is single-ended, so the N half has no per-site electrode to report on.* The release gate of section 2 R10 stays weak until an image is built and run, which is the general firmware gate and not this item | FW-EEG-001 Rev C for the register, with E-27's owner in DSN-EEG-003 §11 for the threshold values |
| 9 | The microSD file layout is FW-EEG-001 Rev C's and is no longer restated here (section 2 R2), so the two incompatible definitions of the same card are down to one. That one is still an outline: FW-EEG-001 Rev C section 10 item 11 carries it as an open item, so the card path is not yet fixed and R2 cannot become a work instruction until it is. Separately, the disinfection validation protocol and the OTA procedure are cited by numbers that are not registered and that collide with registered documents | FW-EEG-001 for the card layout; ECO-EEG-016 Rev B, which owns the document namespace, for the two unregistered procedures |
| 10 | **RFQ S-04's thermistor-monitored charging is not met and stays not met** (no NTC net, no thermistor way on J12 or J13), so the 45 °C inhibit of E-23 rests on the charger module alone and the bench cannot verify it | DSN-EEG-003 Rev C §11, RISK-EEG-011 |
| 11 | RFQ section 10's pricing template has no line for the section 6 spares, the eight HM-09 service keys, the WH-KEY-01 shrouds or the foam tooling, so the consignment split of section 6 cannot be quoted | RFQ-EEG-001, next revision |
| 12 | The per-kit costs and BOM line numbers used in sections 7.3 and 7.4 come from `EEG_kit_BOM_for_bidders`, which is not in `package_v2.4/` and whose revision is cited as both Rev B and Rev C | ECO-EEG-016 Rev B |
| 13 | The isolator module's host connector is USB-B where RFQ E-24 asks for USB-C. The interim answer is the WH-09 pigtail (5.5); it is a live non-conformance, not a settled design | Programme, before the Phase 2 order |
| 14 | **Nothing in this package has been manufactured, cleaned, refurbished or measured.** Every time, force, volume and cycle figure above is calculated or estimated | Phase 1 |
| 15 | **The carrier routing has not been reviewed by a human layout engineer.** It passes its design rule check with zero violations and all 145 nets connected, so the fabrication data is released for review; fabrication release awaits that review, and 169 of the connections were closed at relaxed geometry (5.7). Until it is done no board is made and there is nothing to service | RFQ-EEG-002A layout review |
| 16 | **AVL-EEG-017 K12, the "3-6 N stainless 302 compression spring", could not have been bought as the geometry stood, and is still not closed.** The HM-05B spigot top is at z 12.10 mm and the HM-04 spring seat's roof was at z 13.50, which left **1.40 mm** of free height; the seat is only 0.10 mm larger than the spigot on the radius, so no coil fits around it and the spring must sit on the spigot top, making that free height the whole budget. The seat was deepened on 2026-09-02 from 4.50 to 6.60 mm, roof z 13.50 -> 15.60, which gives **3.50 mm** of free height and still leaves 2.40 mm of material above it carrying only the Ø2.50 mm gel port. That makes the line buyable; it does not make it bought. The form, the free length, the rate and the material are not settled here and are not invented here, and every "3 to 6 N" in this manual is K12's stated target rather than a measured or purchased figure | AVL-EEG-017 owner with the mechanical reviewer; the safety reviewer sees it, because it is a preload member inside a patient-applied part |
| 17 | **The cup bayonet turns in the model and has never turned in PA12, and the coupon that would prove it does not carry the joint.** `tools/simulate_production.py` measures 0.000 mm³ of interference through the quarter turn, 0.000 mm³ through the 0.40 mm of spring travel and 1.557 mm³ of lip engagement on every run (section 4.1); those are booleans on a mesh. `fit01()` is three plain bores at 9.20 / 9.35 / 9.15 mm despite a docstring claiming it "carries the cup bayonet", so today it gates the bore diameter and nothing else. **FIT-01 must be re-cut to carry the entry slot, the run and a lug, printed in the batch and pulled, and that coupon is the acceptance for this manual's 10 N retention and WH-EEG-008 H6's 15 N** before the joint is called released | Mechanical reviewer on MECH-EEG-020 sheet 8, with QP-EEG-010's owner for the batch acceptance |

---

## 11. Audit findings closed by this document

| gaps.md id | Where it is closed |
|---|---|
| `refurbishment-service-manual` | Sections 1, 2 and 8: twelve numbered steps with times, the RTS-1 re-test subset, release criteria and form F1 |
| `disinfection-validation` | Section 2 R5: named agents, concentrations, contact times, rinse and dry, the prohibition table with reasons, the FC-19 escalation, and the honest statement that efficacy is not validated |
| `consumables-and-wear-schedule` | Section 3: per-turnaround, per-5, per-25-session and annual tables against the PKG-EEG-015 Rev B §1.1 consumable lines, the session-counter definition, the fleet stock model and the first-fill ownership ruling |
| `service-key-control` | Section 4: the HM-09 STEP and STL now exist, eight keys are counted and numbered, the register and the two packing negative checks are defined, and the CC BY-SA limit of the control is stated |
| `spares-and-field-replaceable-units` | Sections 5 and 6: the FRU table over twelve module types and thirteen assemblies including the J25 buck-boost, the identity rule in 5.8, and spares per 25 kits with arithmetic |
| `rma-and-returns-form` | Section 7: fault codes, the three-part form, the repair-or-scrap tree, the "working unit" definition and the damage schedule |
| `reprocessing-validation` (quality) | Sections 2 R5, 5.4 and 10 item 2: item-by-item reprocessing table, release criteria, and the unresolved bayonet-seizure finding carried forward as a named open item rather than silently dropped |
| session-file handling (service half) | Section 2 R2 and R3: the card is read, verified, archived and securely erased by the programme, never by the participant. The file layout itself is FW-EEG-001 Rev C's, cited here and not restated, and remains open in that document (section 10 item 9) |
| firmware-update path (service half) | Firmware updates are applied at refurbishment by the programme with the `eegtest` host tool, refused below 40 % SoC and during a session, and recorded in F1 §5. The OTA procedure is not yet a registered document (section 10 item 9) |
