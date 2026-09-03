# PARTICIPANT QUICK-START AND PLACEMENT GUIDE

**Document:** IFU-EEG-014  **Revision:** B  **Date:** 2026-09-01
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E, and TST-EEG-004 Rev C for every test-step number cited here. Where this document and `tools/design.py` or `tools/mech_gen.py` disagree, the source files govern.

**Revision note (Rev B).** Carries the 150.0 × 130.0 mm four-layer carrier and the enlarged POD-P1 enclosure; corrects the button and socket geometry on the pod panel, the ring-buffer recovery figure, the E-27 verification step and the host-USB description; hands the foam pocket schedule back to PKG-EEG-015 section 2.2; and adds six open items that were being carried silently. **Corrections within Rev B, after the verification review of package v2.1 of 1 September 2026:** sections 1, 9 and 14 are re-rendered against the CASE-00 **Rev C** seven-layer bay schedule in place of the withdrawn two-sheet Rev B one, with all five printed items in the lid pocket; and section 13.2 **rules the EMG lead colours red / yellow / green** rather than reporting the conflict. **Corrections within Rev B, after the independent review of package v2.2 of 2 September 2026:** sections 1 and 16 are restated against the seven CASE-00 Rev C layer cut files that `mech/` now holds, which this document had recorded as unissued, and which remain not released for cutting until the bought shell is measured. **Corrections within Rev B, after the firmware and design changes of 2 September 2026:** the **contact-light phase driver is written**, so the control notes in sections 3 and 14 and open item 3 in section 16, which said the amber state could not be produced at all, are corrected in place with their date; the firmware itself has been **built** for the first time and has booted once in an emulator, and it has still never run on hardware, so this card is still not printed until T11 has been observed on a real unit. The revision letter does not change; these are corrections within the same release.

## Why this document exists

RFQ-EEG-001 Rev E A-06 requires a laminated quick-start card in the case lid and a printed placement guide that matches the on-screen guide. Until package v2 neither existed anywhere: three documents named the card, two BOM lines priced it, and there was no text to print. The audit of package v1 records this as `quick-start-card`, and this document closes it. Sections 1 to 12 are the words that go on the card and in the case, written for the person who opens the case, not for an engineer. Section 13 is the placement guide. Sections 14 to 16 are control data for the programme and the manufacturer, and are not printed on the card.

Two things are true of every page below. Nothing in this package has been manufactured or measured, so every figure marked *calculated* is a calculation and not a result. And no safety engineer has yet reviewed this design, which is why no kit may be placed on a person's head until RISK-EEG-011 is signed.

---

## 0. How to read this document

| Sections | Audience | Where it appears |
|---|---|---|
| 1 to 12 | The participant | Laminated A5 card, both sides, in the case lid pocket; the same text in the session runner's help panel |
| 13 | The participant | Printed placement guide, A5, in the same lid pocket as the card; the same eight sites on screen during the contact check |
| 14 to 16 | Programme and manufacturer | Not printed |

Short control notes appear in italics at the end of some participant sections. They are not printed on the card either. They exist so that a reviewer can see which requirement each sentence answers, and so that the places where a requirement is not yet met are visible next to the sentence that depends on them.

---

## 0.1 Two design changes this revision carries

These are engineering findings and not preferences, and they reach the participant only as a slightly larger grey box. They are recorded here because this document describes that box.

**The carrier grew from 130 × 124 mm to 150 × 130 mm.** Thirty connectors, 211 parts and 156 nets would not close at the smaller size. Package v1 asserted that they would; doing the layout showed that they would not.

**The carrier went from two layers to four:** L1 signal, L2 reference plane, L3 reference plane, L4 signal, through vias only, 0.60 mm pad on a 0.30 mm finished hole, stack-up mask / 35 µm L1 / prepreg 0.200 / 17 µm L2 / core 1.065 / 17 µm L3 / prepreg 0.200 / 35 µm L4 / mask = 1.60 mm ± 10 %. Package v1's argument was that a two-layer carrier is cheap and easy to route. It is not: on two layers the bottom side has to be both the reference plane and the second routing surface, and it cannot be both. Four layers give two full routing surfaces and a continuous reference under every analogue trace. The reference planes are AGND_REF left of x = 62 mm and DGND right of it, on both inner layers. The cost is about €35 in total at two units and about €3 a board at fifty.

**The enclosure grew with the board.** POD-P1 base is now 163.0 × 143.0 × 58.0 mm external and 158.0 × 138.0 × 55.5 mm internal, and the MP-01 module plate is 146.0 × 126.0 × 3.0 mm. Two things in this document follow from that. The foam was re-cut round the larger box: the CASE-00 Rev B pocket was 152 × 90 mm and 25 mm deep and could not take it, and CASE-00 Rev C gives POD-P1 a 169 × 149 mm bay 65 mm deep over a 10 mm packer, which can. The seven Rev C layer cut files are now drawn and shipped -- `mech/CASE-00_foam_layer_1.dxf` through `mech/CASE-00_foam_layer_7.dxf`, with the Rev B pair deleted from `mech/` -- and they are still **not released for cutting** until the bought shell is measured (section 16 item 8). And the panel openings of sections 4, 5 and 7 are placed by their carrier y-coordinate alone and overlap each other in the current model (section 16 item 9).

---

# PART ONE -- FOR THE PARTICIPANT

## 1. What is in the case

The case opens like a book. Put it flat on a table with the hinge away from you.

Inside is one block of grey foam, about 52 cm across and 39 cm deep. It is built from seven loose sheets stacked on each other, each 25 mm thick -- but you never take it apart. Every item has its own hollow, cut to its own depth, and lifts straight out. Each hollow has its name printed beside it, and all of them except the helmet's have a round finger hole so you can lift the item out without digging.

**Lid.** A pocket inside the lid holds all the paper: this card, the printed placement guide, the full instruction booklet, the printed calibration certificate for your unit, and a photograph of the packed case. The photograph is the one that shows you where everything goes when you pack up. Nothing made of paper travels in the foam.

**The nine hollows.**

| Hollow | Where it sits | What is in it |
|---|---|---|
| HELMET HM-01 | The deep opening filling one long side, from the front edge to about two thirds of the way back | The helmet, standing upright. It hangs by the wide band that goes round your head, which rests on a ledge cut in the top sheet. The eight silver cups hang free in the space underneath and touch nothing. This is the one hollow with no finger hole: you lift the helmet by that same band |
| HEADPHONES | The middle strip, at the front | The headphones, folded |
| POD-P1 ENCLOSURE | The middle strip, behind the headphones | The grey box with the three buttons. This is the recorder. It stays on the desk |
| BOOM MICROPHONE | Across the back, behind the helmet | The microphone arm, if it has been detached for cleaning |
| SPARE CUPS + KEYLESS SPARES | Back corner, on the helmet side | Spare parts for the programme. You do not need them |
| SPARE CELL | Back edge, beside the spares | Empty, on every kit and every leg. Your kit has one battery and it is already inside the box. Nothing here is missing |
| CONSUMABLES | The narrow column down the far edge, at the front | A zipped pouch: two tubes of gel, one tube of prep gel, saline wipes, cotton buds and blunt syringes |
| EAR CLIPS + EMG LEADS | The same column, in the middle | Two ear clips on a lead, and three coloured leads for the face pads |
| CABLES + CHARGER | The same column, at the back | Two USB-C cables and the charger. One of the two cables is the one you plug into your computer |

If a hollow is empty and it is not the SPARE CELL one, tell us before you start.

*Control note: this table renders the **CASE-00 Rev C** bay schedule of PKG-EEG-015 section 2.2, which is the only authoritative foam schedule in the package: one 516 × 390 mm sheet, seven loose-laid 25 mm PE layers, 175 mm of stack, nine bays, and both Rev B card pockets deleted because the paper travels in the lid wallet. It replaces the CASE-00 Rev B schedule this section rendered at the first issue of this revision -- two 340 × 250 mm sheets and eleven pockets -- which PKG-EEG-015 section 2.4 shows cannot hold the helmet, the pod or the headphones at any arrangement, and against which no foam is cut. "Where it sits" is the plan position of each bay read from the section 2.2 table with the sheet datum at its bottom-left corner; which case edge that datum falls against is fixed at the trial pack of PKG-EEG-015 section 2.4, and the lid photograph of M-06 is what the participant actually navigates by. Two things behind this table are still open and neither is hidden from the participant by it: the seven Rev C cut files are drawn and shipped -- `mech/CASE-00_foam_layer_1.dxf` through `mech/CASE-00_foam_layer_7.dxf`, with the Rev B pair deleted from `mech/` -- but they are **not released for cutting**, because their 516 × 390 mm sheet is drawn to the Peli 1560's published internal footprint and no shell has yet been measured (PKG-EEG-015 section 3.2); and six of the nine bays hold parts that are not dimensioned anywhere in package v2, so their plan sizes are confirmed or corrected at that trial pack: section 16 item 14. The SPARE CELL bay travels empty on every leg -- REG-EEG-012 section 3.1, RISK-EEG-011 section 6.1, QP-EEG-010 audit row A-22 and PKG-EEG-015 line 4.2 all record zero spare cells in circulation -- because RFQ S-09 ships every kit as UN3481, cell inside equipment only. The bay exists in the schedule and is never filled.*

## 2. Fitting, in three steps

It takes two to three minutes once you have done it once. Sit in front of a mirror.

**Step 1 -- gel.** With the helmet on the table, take a blunt syringe of gel. There are eight small ports on the top of the helmet, one above each silver cup. Put gel into each of the eight ports. Then put a little gel on the two ear clips. The lights will show amber while the cups are dry. That is expected.

**Step 2 -- put it on.** Put the helmet on front to back, so the soft pad meets your forehead first. Let the back cradle settle onto the back of your skull. Fasten the chin strap if you are using one -- see section 6, you may leave it off. Then turn the dial at the back two clicks past the point where you first feel it grip. That is all the tightening there is.

**Step 3 -- clips, boom, cable.** Clip the two ear references onto your earlobes. Swing the microphone arm round until it sits about three centimetres from the corner of your mouth. Plug the helmet's cables into the grey box, and plug the box into your computer.

Now watch the lights in the mirror.

> **If a light is red, adjust that site. Do not tighten anything.**
>
> This is the one instruction that feels wrong and is right. Slide that one electrode a few millimetres, side to side, to part the hair under it. Then add a little more gel through its port. The pressure on your scalp comes from a small spring inside each electrode. Tightening the dial or the strap does not press the electrodes harder -- it only bends the frame and lifts the electrodes on the other side of your head. Tightening makes it worse. Every time.

*Control note: three steps as DSN-EEG-002 Rev E section 9. The counter-intuitive instruction is the one DSN-EEG-002 section 3 says the design exists to make sayable. The chin strap is HM-06 and the back cradle is the occipital yoke HM-03, both fixed to the HM-01 frame; the separate headband of RFQ A-03 is withdrawn as a kit item, so there is nothing else for the participant to fit. The boom arm carries only the electret capsule and its screen, on the pigtail at J18; its preamplifier is on the MP-01 module plate at J21, inside the pod, so detaching the arm for cleaning disturbs no electronics.*

## 3. What the lights mean

There are eight lights, one on top of each electrode, facing up and outward so you can read them in a mirror.

| Light | What it means | What you do |
|---|---|---|
| Green | Good contact | Nothing |
| Amber | Usable but marginal | Add gel through that port and wait a few seconds |
| Red | Not usable, or the electrode is not touching you | Slide that site a few millimetres to part the hair, then add gel. Do not tighten |
| Slow pulse | The check is running | Wait, and keep still |
| Off, during recording | Deliberately dark | Nothing. This is on purpose |
| Off, at power-on | Deliberately dark | Nothing. They light when the check starts |

**These lights show electrical contact and nothing else.** A green light does not mean anything about you. A red light does not mean anything about you. It means gel and hair.

The screen shows the same eight numbers the lights are made from, so the helmet and the screen cannot disagree. You are never asked to judge whether contact is good enough. The runner will not let you continue until it is.

*Control note: thresholds green below 10 kΩ, amber 10--20 kΩ, red above 20 kΩ or lead-off, per DSN-EEG-002 section 5, calibrated at TST-EEG-004 T10. Dark at power-on and during recording blocks per RFQ E-27; the power-on dark state is guaranteed in hardware because LED_V is GPIO48, an input at reset, so no current can flow whatever the shift register holds. Each site is driven through a 1 kΩ resistor (R70 to R77) at (3.3 − 2.0) / 1000 = 1.3 mA, 10.4 mA total from GPIO48. Amber is made by alternating the red and green phases, specified at LIGHT_PHASE_HZ = 240 Hz against E-27's requirement of "above 100 Hz". **Corrected 2 September 2026: the contact-light phase driver is written.** Until that date `lights_write()` and `lights_task()` were on/off only and this note said the firmware could not show amber at all. `lights_task()` now reads both halves of the converter's lead-off word -- neither detector gone is green, exactly one is amber, both are red -- and the half-phase quantises to the FreeRTOS tick, so the real alternation is **about 250 Hz rather than exactly 240**, which still satisfies "above 100 Hz". Two things are still true and hold the card back: **no unit exists, so no light has ever been lit and TST-EEG-004 T11 has not been run**; and only `LOFF_SENSP` is enabled in this build, so a site that has lost contact shows **amber where the table above says red** until the N-side excitation is enabled (FW-EEG-001 section 1.1, DSN-EEG-003 section 5). The colour rows above therefore still describe intended behaviour, and this card is not printed until T11 passes: section 16 item 3.*

## 4. Connecting

1. Take the USB-C cable that fits your computer. Plug one end into the computer.
2. Plug the other end into the socket on the grey box marked DATA. It is on the same end panel as the three buttons, at the far end of that panel, as far from the buttons as it gets. The other USB-C socket on that panel is in among the buttons, level with the top two, and it is for charging only. It will do nothing here.
3. Open the session runner in Chrome or Edge, on Windows, macOS, Linux or Android. Firefox, Safari and iPhones will not work for this study, and that is a limitation of the browsers, not of you.
4. The browser shows a small window listing devices. Your unit appears there by its serial number, which is printed on the box. Click it once and click Connect.

That is the one-click authorisation, and you do it once. After that, on that computer and that browser profile, the runner reconnects on its own every time. If you later use a different computer, you do it once more there.

*Control note: WebSerial on desktop, WebUSB on desktop and Android, per RFQ F-13. The chooser entry is keyed to VID/PID and the `iSerialNumber` string, which F-04 populates with the unit serial `TIOV-B-nnnn` (format defined once, in PKG-EEG-015 section 5, and nowhere else -- FW-EEG-001 section 7 defines the public-key fingerprint, not the serial); the same string appears on the label, in the Data Matrix, in the calibration record and on the packing list. The host connection is a panel socket and not a captive cable: the host connector is the USB-C receptacle on the ADuM4160 isolator module, presented through a gasketed aperture in POD-P1. WH-08 and the cable gland are deleted from the Phase 1 build, and one of the two A-07 cables is the host lead. **This is not fully settled:** the named isolator module presents USB-B where RFQ E-24 asks for USB-C, and the interim answer is a short USB-B-to-USB-C panel pigtail, WH-09, until an isolator module with a USB-C host connector is qualified. It is a live non-conformance, recorded at section 16 item 10.*

## 5. During the session

**Two response buttons and a stop button, all on the grey box.** They sit in a row along the end panel, 14 mm apart from centre to centre: Button A is green, Button B is blue, Stop is red, with Stop at the end of the row furthest from the DATA socket. The caps are 12 mm across, so they are big enough to find without looking and there is a clear 2 mm gap between them. The runner tells you which one to press and when.

**The lights go out when recording starts.** All eight of them, every time. This is deliberate and it is a design decision, not a fault. While data is being taken there is nothing on your head to watch and nothing to react to. They come back on between blocks, for the next contact check.

**Stop.** Press the red button at any time, for any reason, and you do not have to give one. The recording block you are in ends at that moment and a marker is written at that point. Everything already recorded is kept. The runner shows you that the session is stopped and offers to end or to carry on. If you would rather just take the helmet off, take it off -- pressing Stop first is tidier, but nothing bad happens if you do not.

You may also stop by closing the laptop or unplugging the cable. That is a rougher stop and it will show as a gap in the record, but it is not damage and it is not a mistake.

*Control note: SW1 BTN_A, SW2 BTN_B, SW3 BTN_STOP on GPIO4/5/6, hardware RC debounce R50--R52 and C50--C52. RFQ E-26 is restated as a 6 mm tactile switch with a 12 mm coloured cap on an extender; the Rev C wording "≥ 12 mm actuator" described the cap and not the switch. **Corrected 2026-09-02:** the buttons are now on the **POD-P1 LID**, not the right end wall, as 12.4 mm circles on the same 14 mm pitch at y = 76, 90 and 104 mm (`mech_gen.py` PANEL and POD_LID_MOUNTED). A 12 mm cap through a 12.4 mm opening has 0.2 mm of radial clearance and leaves a 1.60 mm web between neighbours. They were 13.0 mm circles cut into the right END WALL, chosen by carrier x-coordinate alone -- 48 mm inboard of that wall, so they lined up with nothing -- and at 13.0 mm on a 14 mm pitch they left 1.0 mm of material and swallowed the headphone jack, the charge USB-C, the boom-microphone connector and the room-microphone port. A button is pressed from above; it belongs in the lid, which had no openings at all. Section 16 item 9 is closed.*

## 6. The chin strap

The chin strap is removable, and you may run the whole study without it.

It is offered because it stops the helmet from rotating when you look down, when you talk for twenty minutes, or when you reach for a button. Without it the electrode positions drift a little over two hours, and the repeat check at the end of the session may not agree with the one at the start. The session report records whether the strap was fitted, so if it turns out to have mattered, the analysis can say so.

It is removable because a strap under the chin is not a neutral object for everyone, and this study is with people who have good reason to dislike being fastened into things. If you would rather not wear it, take it off and run without it. You do not need to explain, and nobody will ask. The cost is a stability note in your session report. That is the whole cost.

## 7. Charging

Charge overnight, with the kit in its case and the lid open.

1. Put the helmet and the grey box back in their hollows in the foam.
2. Plug the charger into the wall and into the socket marked CHARGE on the box -- the small USB-C socket in among the three buttons, level with the top two. It is not the one at the far end of the panel; that one is DATA.
3. Leave it. It will take several hours. The runner shows you the battery level when you next connect.

**Never wear the helmet while the charge cable is connected.** Not for a moment, not to top it up, not while you set up. The instrument refuses to start a session while the charger is plugged in, and a second circuit holds the charger switched off for the whole of a session, so it will not let you do it by accident. Do not try to work around it.

A full battery gives more than four hours of recording. A session is about two hours. You should never run out mid-session, and there is no spare battery in the case because there does not need to be one. Do not open the hatch on the box.

*Control note: the four-hour figure is calculated from RFQ E-22, not measured. Two interlocks per RFQ S-01: firmware refuses CMD_START_SESSION while VBUS_DET is high, and CHG_CE holds the charger disabled for the session. There are two mechanisms and no others; S-01 is written out in full in RFQ-EEG-001 S-01 and E-23 and this document only cites it. Both are verified at TST-EEG-004 T4 and T21. RFQ E-23 requires a charger IC with thermal regulation and no charging above 45 °C, which the charger module provides; **S-04's thermistor-monitored charging is not met and stays not met**, because there is no NTC net in `design.py` and no thermistor way on J12 or J13. It is an open hardware item in DSN-EEG-003 section 11 and RISK-EEG-011, and section 16 item 13 here. Charge time is not yet measured; the input is limited by a 1.1 A PTC (F1).*

## 8. Cleaning between your own sessions

You dismantle nothing. There is nothing in this kit that you take apart.

- Wipe the outside of the helmet with one of the supplied wipes. The outside only.
- Wipe the ear clips.
- Do not put the helmet in water, and do not run water over it. It has electronics in it.
- Do not try to take the silver cups out. They are held by a bayonet that needs a key you have not been given, and they are cleaned properly at our end between participants.
- Leftover gel in a port is fine. It is flushed out here.

If gel gets into your hair, warm water and normal shampoo will deal with it. It is a salt gel, not an adhesive.

## 9. Packing it back up

Use the photograph in the lid. It shows the packed case, and each hollow in the foam has its name printed beside it.

1. Everything except the helmet goes straight back into the hollow with its name on it. The order does not matter. The foam is one block, nothing is stacked on anything, and nothing should sit proud of the surface.
2. The helmet goes in upright and it is the only one that needs care. Lower it into its deep opening until the wide band that goes round your head rests on the ledge. The eight silver cups must hang free underneath and touch nothing. If it will not settle, turn it round rather than pressing it down.
3. All the paper -- this card, the placement guide, the booklet, your calibration certificate and the packing photograph -- goes back in the lid pocket. None of it goes in the foam.
4. Close the case and both catches.

**The case is not the parcel.** It travels inside the cardboard carton it arrived in, with the same foam blocks in the corners. The prepaid return label is in the clear plastic wallet on the outside of that carton, together with a one-page return sheet. Put the case in the carton, tape it, take the label out of the wallet, stick it on over the old one, and either book a collection or drop it at the point named on the return sheet.

Keep the carton. It is used twice, out and back. If it has been damaged or thrown away, tell us and we will send another one -- do not improvise a box, because there is a lithium battery inside the equipment and the carton carries the markings the courier needs.

*Control note: M-07 carton and label wallet, S-09 lithium markings. The shipping procedure itself lives in PKG-EEG-015 section 7 and is not restated here; it governs the return leg and is verified at TST-EEG-004 T29.*

## 10. If something goes wrong

| What you see | What to do |
|---|---|
| No lights at all when everything is plugged in | Check the two cables from the helmet to the grey box are both home. There are two: one wide screened cable for the electrodes and one thinner one for the lights. The lights are on the thinner one |
| Nothing on the screen when you plug into the computer | You are probably in the CHARGE socket, the one in among the buttons. Move the cable to the DATA socket at the far end of the same panel, then reload the page |
| The browser never offers your device in the chooser window | Try the other USB-C cable. Then try the other USB port on your computer. Then reload the page. If it still does not appear, stop and contact us -- do not install any driver, and do not accept any download that offers you one |
| One site stays red after two goes of gel | Slide that electrode a few millimetres to part the hair, then gel it again. If it is still red after the third try, leave it and carry on. The runner records which site it was. Do not tighten anything |
| Every light is amber and none go green | Check the two ear clips. They are the reference for all eight sites, so a dry or loose ear clip makes everything look bad at once. Gel them again and reseat them |
| The runner will not start and says the charger is connected | Unplug the charging cable from the box and from the wall. Wait a few seconds. It will then let you start. This is the interlock doing its job |
| The cable came out in the middle of a session | Plug it back in. The instrument keeps the last minute and a half in its own memory and hands that back, and it has been writing a full copy to the card inside it the whole time, so nothing is lost even if you were away for longer. You have not lost the session |
| The battery warning appears mid-session | Finish the block you are in, then stop. Charge overnight and do the rest tomorrow. Do not plug the charger in while wearing the helmet |
| The sound is too loud, distorted, or only in one ear | Press Stop. Check the headphone plug is fully in. If it is still wrong, do not turn anything up -- stop the session and contact us |

*Control note: the recovery figure is RFQ F-06 as relaxed by ECO-EEG-025. Twelve megabytes of ring buffer in eight megabytes of PSRAM is impossible; the fitted ring is 6 MiB, which is 126 seconds of raw samples at 1000 Hz (124 s framed), so F-06 is relaxed to **90 seconds of ring plus unlimited backfill from the microSD copy**, and the card copy is what covers a longer disconnect. Frame payload is 50.7 kB/s at 1000 Hz, 1015 bytes every 20 ms. Verified at TST-EEG-004 T15 and T14; both are calculated capacities, untested on hardware. The DATA/CHARGE confusion is a real risk of the POD-P1 panel: the two USB-C openings are on the same wall, about 68 mm apart at y = 12 mm and y = 80 mm, with the charge opening sitting between the first two button openings, and PKG-EEG-015 must engrave both legends. The maximum acoustic output requirement behind the last row is RFQ E-29, 100 dB SPL on an artificial ear, verified as a type test at TST-EEG-004 T28.*

## 11. When to stop and contact the programme

Stop the session and contact us if any of these happen. None of them is your fault and none of them wastes the session.

- Anything hurts, anywhere, at any point.
- The sound is uncomfortable, however quiet the runner says it is.
- Your skin itches, reddens or reacts under an electrode, an ear clip or a face pad.
- The helmet or the grey box feels hot.
- You smell anything burning, or you see damage to a cable or a case.
- The battery hatch has come loose.
- You feel distressed, and continuing does not feel right.

The last one counts as much as the others. You can end a session for that reason alone and it is recorded as a completed decision, not a failure.

There are two ways to reach us and they are separate on purpose. The technical contact on the return sheet deals with the equipment. The support contact on the same sheet is not part of the research team, does not see your data, and is there if you want to talk to somebody who is not us. You may use either, or both, or neither.

## 12. What this instrument is, and what it is not

Plainly, because you are entitled to it.

- **This is a research instrument. It is not a medical device.** It is not approved, licensed or certified for medical use, and it is not being sold. It is lent to you and comes back.
- **It does not diagnose anything.** Not a condition, not a cause, not an implant, not a signal. It cannot, and nobody will tell you that it has.
- **Nothing it shows on your head means anything except electrical contact.** The eight lights are made from one measurement: how well the gel is bridging the gap between a silver cup and your scalp. That is all they are. They are called contact lights for that reason.
- **You will not be given an individual verdict**, and no one on the programme will offer you one. The study compares groups. A single person's recording cannot answer a single person's question, and saying otherwise would be a lie that is easy to tell.
- **It has no radio.** The wireless parts of the controller are switched off in the firmware and stay off. The only thing that leaves the instrument is data down the cable to your own computer.
- **The room microphone is muted on a dedicated hardware line** except during the specific windows the runner tells you about in advance. MIC_MUTE is a wire to a gate on the microphone module, not a volume setting in software.
- **It runs on its own battery** and there is no electrical path from the mains to you. The one link to your computer passes data across an isolation barrier and does not pass current.
- **Nothing in this design has been built or measured yet.** The numbers in our documents are calculations, and no safety engineer has yet reviewed this design. When we have measurements we will publish those instead.

*Control note: "no radio" is verified at TST-EEG-004 T24 and the isolation barrier at T20, a 500 V DC insulation-resistance measurement; there is no per-unit hipot. The room-microphone module with a hardware mute is specified by interface at J28 (DVDD3V3, DGND, ROOM_PRE, MIC_MUTE) and has not been bought or measured.*

---

## 13. Placement guide

### 13.1 The eight scalp sites

You do not place these. They are fixed to the frame at manufacture and cannot be moved more than a few millimetres, which is exactly the point: an electrode two centimetres from where the protocol says it is can still show a perfect green light, and nobody would ever know. This page tells you what each one is, because being told is better than not being told.

The names are the international 10-20 system, the standard map used for putting electrodes on heads. F is front, C is the middle band across the crown, P is behind that, T is the side above the ear. Odd numbers are on the left, even numbers on the right, z means it is on the centre line.

| Site | Where it sits on your head | What it is for |
|---|---|---|
| Fz | Centre line, forehead, above the hairline | Front-to-back gradient of the hearing response, and the frontal activity that separates the two possible outcomes of the study |
| Cz | Centre line, top of the head, where the two arches cross | The main one. The response the whole study rests on is largest here, so it sits on the most stable point of the frame |
| Pz | Centre line, behind Cz, towards the back of the crown | The other end of that front-to-back gradient |
| C3 | Left side, on the band across the crown, above the left ear | Left-right symmetry check, and the movement activity that appears just before a silently intended reply |
| C4 | Right side, mirror of C3 | The same, on the right |
| T7 | Left side, on a short stub above the left ear | Nearest scalp site to the left hearing cortex. Whether the temporal sites or the frontal sites respond first is measured here |
| T8 | Right side, mirror of T7 | The same, on the right |
| F7 | Left front, on a stub above and forward of the left ear | Speech-related site. It is expected to be messy while you are speaking, and it is used as a monitor for that mess rather than as a signal |

Two more contacts complete the set and are not on the list above because they are not measurement sites:

- **The two ear clips**, one on each earlobe, linked together. Every one of the eight sites is measured against these. This is why a loose ear clip turns every light amber at once.
- **The bias pad** at the middle of your forehead, just above the brow. It is an active return path, not an earth connection. There is no earth connection anywhere in this instrument.

That is fourteen patient terminations in a standard build: eight scalp, two ear references, one bias and the three face pads of section 13.2. The two spare channels exist on the board and are not brought out to a socket in a standard build.

### 13.2 The three face pads -- the one placement you do make

Three small sticky pads go on your face and neck. These are the only electrodes you position yourself. Each has a coloured lead that matches a coloured socket on the left end of the grey box. Match colour to colour and you cannot get them the wrong way round.

| Lead colour | Socket | Where the pad goes | What it is for |
|---|---|---|---|
| Red | EMG1 | On the cheek, beside the corner of the mouth | Picks up the small muscle activity around the lips, including movements too small to feel |
| Yellow | EMG2 | Under the chin, in the soft area behind the jawbone | Picks up tongue and floor-of-mouth muscle |
| Green | EMG3 | Front of the throat, beside the voice box, to one side of the midline | Picks up voice-box muscle |

How to place them:

1. Wipe each spot with a saline wipe and let it dry.
2. If the runner asks you to, rub the spot gently with a little prep gel on a cotton bud, then wipe it off. Gently, once. This gel is mildly abrasive. **Use it on the face, the neck and the earlobes only. Never put it through the eight ports on the helmet, and never rub it on your scalp.**
3. Peel one fresh pad, press it on, and press round the edge with a finger for a few seconds.
4. Clip the matching coloured lead to the stud on the pad.
5. One fresh pad per site per session. Thirty are supplied, which is ten sessions' worth.

If a pad will not stick because of stubble or moisturiser, wipe the spot again and use a new pad. Do not tape it down.

These three channels exist because the study is about the difference between speaking, intending to speak and hearing. Muscle activity at the mouth, tongue and voice box is how we can tell those apart in the recording rather than having to take anyone's word for it, including our own.

*Control note: EMG channels are ADS1299 #2 channels 1--3 on carrier channels 12--14, cheek / submental / laryngeal, on touch-proof DIN 42802 sockets J15--J17, whose panel openings are 8.2 mm circles on the POD-P1 left end wall at y = 76, 88 and 100 mm (`mech_gen.py` PANEL). **The carrier-side socket part is open:** `design.py` names Stäubli SLB1,5-F as a class and not a confirmed PCB part, and a touch-proof 1.5 mm socket with a PCB-mount signal pin and two 1.5 mm retention posts must be sourced and first-articled before Phase 2, against a 12-week lead-time risk in AVL-EEG-017. **The lead colour code is ruled here, and it is red / yellow / green.** Three documents named two codes: this section and PKG-EEG-015 section 4.2 say red / yellow / green, WH-EEG-008 section 3.6 buys the same three WH-06 leads as white / brown / grey. The code the participant matches by hand, under a desk lamp, against a coloured socket legend is the code that governs, and white against grey is not a distinction to ask of a person in a mirror. WH-06 is a bought-in catalogue lead set stocked in either code, so the ruling costs nothing at the harness and nothing in lead time, and nothing else in the package depends on the white / brown / grey names. WH-EEG-008 section 3.6, its WH-06 table and its open item 7 must be re-issued to red / yellow / green under an ECO-EEG-016 change, and until they are, the two documents still disagree on paper: section 16 item 11. This section is the placement guide of RFQ A-06 and closes audit item `quick-start-card`.*

---

# PART TWO -- CONTROL DATA (NOT PRINTED ON THE CARD)

## 14. Print specification and where each piece lives

| Item | Content | Format | Where it travels |
|---|---|---|---|
| QSC-EEG-001 quick-start card | Sections 2, 3, 5, 7, 10 and 12 of this document, condensed to two sides | A5, 300 gsm, double-sided, 125 µm matt encapsulation, rounded corners | Lid pocket of the case, per A-06 |
| PLG-EEG-001 placement guide | Section 13 entire, with a head diagram and a face diagram | A5, 300 gsm, single sheet, matt encapsulation | Lid pocket of the case, beside the quick-start card. CASE-00 **Rev C** has no card bay in the foam (PKG-EEG-015 section 2.2) |
| Packing photograph | The packed case, both layers, pockets legible | A5, laminated | Lid, per M-06 |
| Per-unit calibration and test record | One printed A4 page per unit, from TST-EEG-004 section 12 | A4, plain | Lid pocket, beside the quick-start card |
| Full IFU | This document, sections 1 to 13 | A5 booklet or the runner's help panel | Lid pocket, with the card and the placement guide. CASE-00 **Rev C** deletes the QUICK-START CARD pocket as well; no foam bay carries paper |

Matt encapsulation is specified rather than gloss because the card is read under a desk lamp beside a mirror, and a gloss card put in front of a lamp becomes the lamp.

All five printed items travel in the lid pocket: the quick-start card, the placement guide, the full IFU, the per-unit calibration record and the packing photograph. CASE-00 Rev C has no paper bay in the foam at all, which is the reason, and section 9 tells the participant to put all five back there. PKG-EEG-015 section 2.2 names three of the five when it says why the card pockets are deleted -- card, photograph, certificate -- and must be extended to all five so the two documents count the same wallet: section 16 item 14.

**Language.** English for Phase 1. French and Dutch versions are required before any kit reaches a Belgian participant, and the translation must be done by a translator who has read section 12, because the honesty sentences are the ones a loose translation damages first.

**Foam label wording.** CASE-00 Rev B cut a pocket legended CASE LID CARD in the top layer and one legended QUICK-START CARD in the bottom, which never matched A-06's single card in the lid. Rev C deletes both, so that legend conflict is closed by deletion rather than reconciled, and the ECO that would have renamed the top-layer pocket to DOCUMENTS is overtaken by it. PKG-EEG-015 section 2.2 owns the cut file and the foam legend text; this document does not restate the bay schedule and does not change it.

**Artwork identifiers.** QSC-EEG-001 and PLG-EEG-001 are used above because three documents already cite them, but neither is registered in ECO-EEG-016 and both collide numerically with RFQ-EEG-001. They must be renumbered before the artwork is released: section 16 item 12.

## 15. Requirement traceability, verification and sign-off

| Requirement | Where satisfied here | How it is verified | Who signs |
|---|---|---|---|
| A-06 laminated card and printed placement guide | Sections 2--12, 13; print spec 14 | TST-EEG-004 T18, kit closure against KPL-EEG-001: one card and one guide present, legible, encapsulated | Kit packer, countersigned at goods-out |
| S-01 charging warning in the participant text | Section 7, sentence in bold | Word-for-word check against S-01 at each revision of this document; the interlocks themselves at T4 and T21 | Programme lead |
| E-27 lights dark during recording, explained not hidden | Sections 3 and 5 | TST-EEG-004 **T11**, contact lights, colorimeter head FIX-01/E; the card text is checked against observed behaviour. Corrected 2 September 2026: this row said T11 could not pass until the phase driver existed. **The driver exists**; T11 is now waiting on a unit to run it on, and on the red state, which this build cannot produce because only `LOFF_SENSP` is enabled | Test engineer |
| E-26 three buttons, colours and function | Section 5 | TST-EEG-004 T17, buttons, mute and headphone level, against the printed colours; panel openings at T18 | Test engineer |
| E-29 maximum acoustic output, 100 dB SPL | Section 10, last row; section 11 | TST-EEG-004 T28, artificial ear, type test once per lot | Test engineer |
| F-13 browser scope stated plainly | Section 4 | Reviewed at each firmware release; if browser support changes, this document is reissued | Firmware owner |
| M-06 repack without instructions | Section 9 and the lid photograph | Timed repack trial by a person who has not seen the kit before: correct repack in under five minutes with the photograph only | Programme lead |
| S-09 no loose cell on participant legs | Sections 1 and 7 | TST-EEG-004 T29 and the packing check: SPARE CELL bay empty, carton markings present | Kit packer |
| Not-a-medical-device statement | Section 12, first bullet | Wording taken verbatim from the enclosure label of M-03; the two are compared at each revision | Programme lead, and the safety reviewer once appointed |

Every T-number above is taken from TST-EEG-004 Rev C, which owns the step numbers. This document invents none, and where it needs a step that does not exist it says so as an open item instead.

**Readability verification.** Before the first participant kit ships, this document is read aloud in full by two people who are not part of the programme and have not seen the kit. Every sentence they stop at, re-read or query is rewritten. The record of that session is filed with the document. A guide that a reviewer can follow and a participant cannot is a guide that has not been verified.

**Fit-trial verification.** One person who has never fitted the helmet follows sections 2 and 4 unaided, timed. The design claims two to three minutes. If the trial exceeds five minutes, the instructions are wrong, not the person, and this document is revised before the fleet ships.

## 16. What is not settled

| # | Open item | Effect on this document |
|---|---|---|
| 1 | No safety engineer has reviewed the design | No kit may go on a person's head. This document may be printed and proofed, but not issued with a kit |
| 2 | USB VID and PID are placeholders pending a pid.codes allocation | The name the browser chooser shows in section 4 is not final. The card must not print a device name until it is |
| 3 | **Corrected 2 September 2026.** This item read "the firmware has never been compiled or run on hardware, and the contact-light phase driver in particular does not exist". The firmware **is built** (ESP-IDF v5.2.5) and has **booted once under QEMU**, which emulates none of this kit's peripherals; the **phase driver is written**. What has not changed: **the firmware has never run on hardware**, no light has ever been lit, and TST-EEG-004 T11 has not been run | Sections 3, 5 and 10 still describe intended behaviour, and section 3's red row in particular cannot be produced by this build, which enables only `LOFF_SENSP`, so a lost site shows amber. Each sentence is re-verified against the first working prototype before the card is printed |
| 4 | Nothing has been manufactured or measured | Battery life, charge time, fit time and recovery behaviour are calculated. Section 12 says so to the participant, and it stays there until they are measured |
| 5 | French and Dutch versions do not exist | Belgian participants cannot be enrolled with an English-only card |
| 6 | The support pathway contact is named on the return sheet, which PKG-EEG-015 owns | This document must not be printed with a blank contact. If PKG-EEG-015 is not issued, the card is not issued |
| 7 | The head diagram for section 13.1 and the face diagram for section 13.2 have not been drawn | The placement guide is text-only until they exist. A text-only placement guide is a deficiency against A-06, not a substitute |
| 8 | The CASE-00 **Rev C** schedule gives POD-P1 a 169 × 149 mm bay, 65 mm deep over a 10 mm packer, which takes the 163 × 143 × 62 mm pod. The seven Rev C layer cut files are now shipped -- `mech/CASE-00_foam_layer_1.dxf` through `mech/CASE-00_foam_layer_7.dxf`, and the Rev B pair that held the 152 × 90 mm through-cut is deleted from `mech/` -- but they are **not released for cutting**: their sheet is drawn to the Peli 1560's published internal footprint, and six of the nine bays hold parts that are dimensioned nowhere in package v2 | Sections 1 and 9 describe the Rev C bays, and no foam is cut until PKG-EEG-015 section 3.2's shell measurement is in. PKG-EEG-015 section 2.4 gates the cut on a trial pack with the first printed HM-01 and the first bought shell, and this document is re-checked against the cut files if that trial pack moves a bay |
| 9 | ~~The POD-P1 right-wall openings are placed by carrier y-coordinate alone and overlap.~~ **CLOSED 2026-09-02.** The three buttons moved to the LID at 12.4 mm on the 14 mm pitch; the four right-wall connector openings were re-spaced to leave at least 2.0 mm of wall between every pair. `tools/simulate_production.py` now measures the gap between every pair of openings on each face on every run, so a merged panel cannot ship again | -- |
| 10 | The isolator module presents USB-B where RFQ E-24 asks for USB-C. The interim answer is the WH-09 USB-B-to-USB-C panel pigtail | Section 4 tells the participant to plug a USB-C cable into a USB-C socket. That stays true only while WH-09 is fitted, and it is a live non-conformance until an isolator with a USB-C host connector is qualified |
| 11 | **Ruled: the EMG leads are red, yellow and green** (section 13.2, with the reasoning). PKG-EEG-015 section 4.2 already carries that code. WH-EEG-008 section 3.6, its WH-06 lead table and its own open item 7 still say white / brown / grey and have not been re-issued | The ruling is not in doubt; the re-issue is the open work and belongs in ECO-EEG-016. The card is not printed while WH-EEG-008 still buys a different code, because the lead the participant is handed is bought to that document's WH-06 line -- section 13.2, the A-06 panel legend and the runner's on-screen guide have to name the colours that arrive in the box |
| 12 | QSC-EEG-001 and PLG-EEG-001 are unregistered document numbers that collide with RFQ-EEG-001 | The artwork in section 14 cannot be released under those identifiers. ECO-EEG-016 must issue numbers first |
| 13 | S-04's thermistor-monitored charging is not met: there is no NTC net in `design.py` and no thermistor way on J12 or J13 | Section 7 tells the participant the charger will not run hot. That rests on the charger module's own thermal regulation (E-23) alone, with no battery temperature measurement behind it, and the safety reviewer must be told so explicitly |
| 14 | Sections 1, 9 and 14 now render the **CASE-00 Rev C** schedule of PKG-EEG-015 section 2.2 -- one 516 × 390 mm sheet, seven loose-laid 25 mm layers, nine bays, both card pockets deleted, all the paper in the lid. Two things behind it are open: six of the nine bays hold parts that are not dimensioned anywhere in package v2 and are sized at the trial pack of PKG-EEG-015 section 2.4, and PKG-EEG-015 section 2.2 names three items in the lid wallet -- card, photograph, certificate -- where section 14 here puts five, adding the placement guide and the full IFU | The bay names and the paper allocation are settled; the bay dimensions are provisional and the cut files, though drawn and shipped, are not released for cutting. PKG-EEG-015 section 2.2 must extend its lid-wallet sentence to all five printed items, and this document is re-checked against the Rev C cut files if the trial pack moves a bay, before the card is printed |

Nothing in this package has been manufactured or measured, and no safety engineer has reviewed this design.
