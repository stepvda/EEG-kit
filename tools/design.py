#!/usr/bin/env python3
"""
design.py -- EEG-CAR-01 Rev B, the single source of truth.

Every other artifact in package_v2.4/kicad, package_v2.4/schematic and the carrier sub-BOM is
generated from this file: the board, the Gerbers, the drill, the CPL, the IPC-D-356 netlist,
the schematic sheets, the assembly drawings and the DRC report.

Revision B closes the electrical defects found in Rev A; each one is logged as an ECO in
docs/ECO-EEG-016_change_control_and_document_register.md.  Anything a builder needs to know
that is not geometry lives in the NOTES dictionary at the bottom, and is printed onto the
fabrication and assembly drawings.

Coordinates: millimetres, origin at the top-left board corner, X right, Y down (KiCad).
Gerber, drill and CPL output flip Y so that their origin is the bottom-left board corner.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

BOARD_W = 150.0
BOARD_H = 130.0
ZONE_SPLIT_X = 62.0          # analogue zone x < 62 mm, digital zone x > 62 mm
REV = "B"
DATE = "2026-09-02"
BOARD_NAME = "EEG-CAR-01"

# ---------------------------------------------------------------------------
# 1. Components
# ---------------------------------------------------------------------------
C = {}


def add(ref, fp, val, x, y, rot=0.0, mpn="", descr="", zone="A", dnp=False):
    assert ref not in C, f"duplicate refdes {ref}"
    C[ref] = dict(ref=ref, fp=fp, val=val, x=x, y=y, rot=rot, mpn=mpn,
                  descr=descr, zone=zone, dnp=dnp)


PS = "PinSocket_1x{:02d}_P2.54mm_Vertical".format
PS2 = "PinSocket_2x10_P2.54mm_Vertical"
R06, C06, L06 = "R_0603_1608Metric", "C_0603_1608Metric", "L_0603_1608Metric"
SKT = "Samtec SSW-1{:02d}-01-G-S or equivalent 2.54 mm socket strip".format

# ===========================================================================
# ANALOGUE ZONE  (x < 58 mm)
# ===========================================================================
# ECO-EEG-014: Rev A ran eight digital contact-light lines through the same 22-way
# harness socket as the electrodes, at x = 5 mm, which forced them to cross the whole
# analogue zone.  The harness is now two cables and two sockets: a screened 12-way
# electrode bundle here, and a 10-way light ribbon at J30 in the digital zone.
add("J14", PS(12), "Helmet harness -- electrodes (12-way screened)", 5.0, 12.0, 0, SKT(12),
    "1x12 socket: eight scalp electrodes, two ear references, the bias lead and the "
    "cable screen.  Nothing digital enters this connector.", "A")

# 16 electrode protection networks: source -> R -> node -> clamp D + filter C -> module
PROT = [
    (1, "E_Fz", "IN1", "Fz scalp"), (2, "E_Cz", "IN2", "Cz scalp"),
    (3, "E_Pz", "IN3", "Pz scalp"), (4, "E_C3", "IN4", "C3 scalp"),
    (5, "E_C4", "IN5", "C4 scalp"), (6, "E_T7", "IN6", "T7 scalp"),
    (7, "E_T8", "IN7", "T8 scalp"), (8, "E_F7", "IN8", "F7 scalp"),
    (9, "REF_L", "SRB1", "left ear reference"), (10, "REF_R", "SRB1", "right ear reference"),
    (11, "BIAS_EL", "BIASOUT", "bias drive to Fpz"),
    (12, "EMGIN1", "EMG1", "EMG cheek"), (13, "EMGIN2", "EMG2", "EMG submental"),
    (14, "EMGIN3", "EMG3", "EMG laryngeal"),
    (15, "EOGIN1", "SPARE1", "EOG / spare 1"), (16, "EOGIN2", "SPARE2", "EOG / spare 2"),
]
for i, (n, src, dst, lbl) in enumerate(PROT):
    y = 5.0 + i * 4.3
    # ECO-EEG-024 APPLIED 2026-09-02: 47 kOhm -> 68 kOhm.
    #
    # S-02 asks that single-fault DC current into a patient connection stay inside 50 uA.
    # At 47 kOhm it was 53.2 uA on this programme's bare-resistor bound A -- a 6.4 %
    # overshoot on a SAFETY limit, carried as not-met through three revisions.  At 68 kOhm
    # it is 36.8 uA (bound A) and 30.0 uA (bound B).  The limit is met.
    #
    # What it costs is already written into the requirement it costs: E-10 states BOTH
    # branches, "+/-0.5 dB with the 47 kOhm fitted (-0.36 dB at 100 Hz), and +/-1.0 dB if
    # ECO-EEG-024 raises them to 68 kOhm (-0.75 dB at 100 Hz)".  Taking the ECO moves the
    # front end to the second branch, which E-10 permits; it does not breach it.
    #
    # Same 0603 footprint, same nets, same pad count, so the board does not move.
    #
    # THIS DOES NOT DISCHARGE SR-01.  The safety reviewer owns the disposition and that
    # review has not started.  What changes is that the reviewer is now handed a design
    # that MEETS the limit and is asked to confirm it, rather than one that does not and
    # is asked to accept it.
    add(f"R{n}", R06, "68k 0.1% 25ppm", 16.0, y, 0, "Vishay TNPW060368K0BEEA",
        f"series protection resistor, {lbl}", "A")
    # ECO-EEG-028: D moved 22 -> 23 and C 28 -> 29.  The AVSS/AVDD rails that feed
    # every clamp run vertically between the R and D columns, and at a 6 mm pitch
    # the rails, their vias and the sixteen row signals (each owed 0.35 mm) did
    # not all fit -- rows 12-16 shipped with their R-to-D hop open.  One extra
    # millimetre is a rail lane; the C-to-module runs shorten by the same amount.
    add(f"D{n}", "SOT-23", "BAV99", 23.0, y, 0, "Nexperia BAV99,215",
        f"clamp to AVDD/AVSS, {lbl}", "A")
    add(f"C{n}", C06, "10n C0G 50V", 29.0, y, 0, "Murata GCM1885C1H103JA16D",
        f"RF filter to AGND_REF, {lbl}", "A")

# ECO-EEG-013: the Rev A 2x10 analogue connectors could not be escaped on two layers --
# the inner row had no route out.  Split into a 1x10 signal socket and a 1x6 rail socket
# per module: every analogue signal pin now escapes sideways on the top layer.
add("J2", PS(10), "ADS1299 module #1 analogue signals", 41.0, 5.0, 0, SKT(10),
    "1x10 socket: eight EEG inputs, the SRB1 reference and the bias drive", "A")
add("J23", PS(6), "ADS1299 module #1 analogue rails", 47.0, 5.0, 0, SKT(6),
    "1x6 socket: AVDD, AVSS, BIASIN, AGND_REF and a second rail pair", "A")
# ECO-EEG-028: J4 sat at y = 36 while the protection rows that feed its pins 1-3 and
# 7-8 sit at y = 52 to 70, so five electrode-class signals fanned 16 mm diagonally
# through the same window and sealed each other in (the Rev B route left EMG2, SPARE1
# and SPARE2 stranded at these pins).  At y = 50 the pins face their rows almost
# straight on: row 15 to pin 7 is now dead level.  SRB1 (pin 9) is reached around the
# south end of the socket; the envelope outputs enter pins 4-6 from the east.  What
# is uncertain: the SRB1 descent and the three envelope climbs now share the corridor
# east of the socket, which the router must arbitrate.
add("J4", PS(10), "ADS1299 module #2 analogue signals", 41.0, 50.0, 0, SKT(10),
    "1x10 socket: three EMG inputs, three envelope channels, two spares, SRB1", "A")
add("J29", PS(6), "ADS1299 module #2 analogue rails", 47.0, 24.0, 0, SKT(6),
    "1x6 socket: AVDD2, AVSS2, BIASIN, AGND_REF and a second rail pair", "A")

# analogue rails, links and star points -- one tidy column at x = 45
add("C100", C06, "10u X5R 16V", 54.0, 5.0, 0, "Murata GRM188R61C106MA73D",
    "AVDD bulk decoupling at the carrier", "A")
add("C101", C06, "10u X5R 16V", 54.0, 9.0, 0, "Murata GRM188R61C106MA73D",
    "AVSS bulk decoupling at the carrier", "A")
add("C102", C06, "100n X7R 50V", 54.0, 13.0, 0, "Murata GCM188R71H104KA57D",
    "AVDD high-frequency decoupling", "A")
add("C103", C06, "100n X7R 50V", 54.0, 17.0, 0, "Murata GCM188R71H104KA57D",
    "AVSS high-frequency decoupling", "A")
# ECO-EEG-028: the rail links sat at x = 54 with the AVDD/AVSS trunk descending at
# x = 52-55 BETWEEN them and J29, so the AVSS2 side could not be reached at all -- the
# Rev B route shipped AVSS2 with zero copper.  At x = 50.8 the links sit between the
# socket and the trunk, with pad 1 facing J29 and pad 2 dead level with the TP10/TP11
# trunk taps.  Uncertain: pin 2 of J29 still has to reach pad 1 around the socket's
# own foreign pins, which is tight but no longer walled.
# Second refinement, same ECO: at (50.8, 31/35) the AVDD2 tree still dropped the
# whole J29 column from pin 1 to pin 5, and that drop walled pin 2 (AVSS2) in.  At
# the MID-LATITUDE of its two pins each link pulls both pins to itself directly --
# the minimum spanning tree prefers two short diagonals over the 10.2 mm column
# drop -- so no rail net runs the length of the socket any more.  R93 sits 2 mm
# east of R92 so the AVSS2 diagonals pass north and south of R92's body.
add("R92", R06, "0R", 50.5, 29.0, 90, "Vishay CRCW06030000Z0EA",
    "link AVDD2 (module #2) to AVDD -- remove if module #2 regulates its own rails", "A")
add("R93", R06, "0R", 52.5, 31.5, 90, "Vishay CRCW06030000Z0EA",
    "link AVSS2 (module #2) to AVSS -- remove if module #2 regulates its own rails", "A")
# ECO-EEG-028: TP10/TP11 moved from x = 54 -- the rail links now live there, and a
# test point is the one part on this board that can go anywhere.
add("TP10", "TestPoint_Pad_D1.5mm", "AVDD", 56.0, 28.0, 0, "-", "test point AVDD", "A")
add("TP11", "TestPoint_Pad_D1.5mm", "AVSS", 56.0, 32.0, 0, "-", "test point AVSS", "A")
add("TP13", "TestPoint_Pad_D1.5mm", "AGND_REF", 54.0, 39.0, 0, "-", "test point AGND_REF", "A")

# star grounds and the stimulus comparator -- column at x = 54
add("R90", R06, "0R", 56.0, 58.0, 0, "Vishay CRCW06030000Z0EA",
    "SINGLE STAR POINT: AGND_REF to DGND. Fit exactly one; never bridge with a wire.", "A")
add("R91", R06, "0R", 56.0, 62.0, 0, "Vishay CRCW06030000Z0EA",
    "harness shield to DGND, pod end only", "A")
add("R80", R06, "470k 1%", 56.0, 66.0, 0, "Vishay CRCW0603470KFKEA",
    "comparator threshold divider, top (trips at about 52 mV)", "A")
add("R81", R06, "10k 1%", 56.0, 70.0, 0, "Vishay CRCW060310K0FKEA",
    "comparator threshold divider, bottom", "A")
add("R82", R06, "1M 1%", 56.0, 74.0, 0, "Vishay CRCW06031M00FKEA",
    "comparator hysteresis, about 5 mV", "A")
add("TP7", "TestPoint_Pad_D1.5mm", "ENV_STIM", 56.0, 80.0, 0, "-",
    "test point, stimulus envelope", "A")
add("U7", "SOT-23-5", "TLV3201AIDBV", 56.0, 85.0, 0, "TI TLV3201AIDBVR",
    "stimulus-envelope comparator (RFQ E-12); its output is latched on DRDY in firmware", "A")
add("TP8", "TestPoint_Pad_D1.5mm", "ENV_VOICE", 56.0, 92.0, 0, "-",
    "test point, voice envelope", "A")
add("TP9", "TestPoint_Pad_D1.5mm", "ENV_ROOM", 56.0, 104.0, 0, "-",
    "test point, room envelope", "A")

# three envelope detectors -- three bands, five passive columns plus the quad op-amp
ENV = [(1, 20, "HP_TAP", "ENV_STIM", 76.0, "stimulus, from the headphone tap"),
       (2, 40, "VOICE_PRE", "ENV_VOICE", 88.0, "voice microphone preamp"),
       (3, 60, "ROOM_PRE", "ENV_ROOM", 100.0, "room microphone preamp")]
ECOL = [16.0, 22.0, 28.0, 34.0, 40.0]
for k, b, src, out, ybase, lbl in ENV:
    r0, r1, r2 = ybase + 1.0, ybase + 5.0, ybase + 9.0
    add(f"U{k}", "SOIC-14_3.9x8.7mm_P1.27mm", "OPA4376AID", 47.0, r1, 0, "TI OPA4376AIDR",
        f"quad precision op-amp: rectifier, absolute-value summer, 50 Hz filter and output "
        f"buffer for envelope channel {k} ({lbl})", "A")
    add(f"C{b}", C06, "10u X5R 16V", ECOL[0], r0, 0, "Murata GRM188R61C106MA73D",
        f"input AC coupling into 10 kOhm: 1.6 Hz corner, envelope channel {k}. "
        f"ECO-EEG-027: 1 uF gave 15.9 Hz, which removes the envelope it is meant to "
        f"pass.", "A")
    add(f"R{b}", R06, "10k 0.1%", ECOL[1], r0, 0, "Vishay TNPW060310K0BEEA",
        f"rectifier input resistor, envelope channel {k}", "A")
    add(f"R{b+1}", R06, "10k 0.1%", ECOL[2], r0, 0, "Vishay TNPW060310K0BEEA",
        f"rectifier feedback resistor, envelope channel {k}", "A")
    add(f"D{b}", "SOT-23", "BAT54S", ECOL[3], r0, 0, "Nexperia BAT54S,215",
        f"precision-rectifier Schottky pair (pin 3 at the op-amp output), channel {k}", "A")
    add(f"C{b+3}", C06, "100n X7R 25V", ECOL[4], r0, 0, "Murata GCM188R71E104KA57D",
        f"AVDD decoupling at U{k}", "A")
    add(f"R{b+2}", R06, "4k99 0.1%", ECOL[0], r1, 0, "Vishay TNPW06034K99BEEA",
        f"half-wave summing resistor (R/2) into the absolute-value stage, channel {k}", "A")
    add(f"R{b+3}", R06, "10k 0.1%", ECOL[1], r1, 0, "Vishay TNPW060310K0BEEA",
        f"direct summing resistor into the absolute-value stage, channel {k}", "A")
    add(f"R{b+4}", R06, "10k 0.1%", ECOL[2], r1, 0, "Vishay TNPW060310K0BEEA",
        f"absolute-value stage feedback resistor, channel {k}", "A")
    # E-11's low-pass half, rescaled to C0G on 2 September 2026.
    #
    # It was 22 k with 100 nF and 220 nF X7R, and it could not meet its own requirement.
    # X7R is +/-15 % over temperature, f0 goes as 1/sqrt(C1.C2), so the corner moved over
    # 42.4 to 57.4 Hz against E-11's 50 Hz +/-10 %, i.e. 45 to 55: NO build with those
    # parts could be held inside the band, wherever the centre sat.  The BOM note said as
    # much and pointed at a tolerance in TST-EEG-004 that had never been written.
    #
    # C0G is +/-5 % and does not move with temperature, which puts the same topology at
    # 47.6 to 52.6 Hz -- inside the band with margin.  The obstacle was that 100 nF C0G is
    # not a stocked 0603 part, and the answer is to stop asking for 100 nF: scale the
    # capacitors down by ten and the resistors up by ten, which leaves f0 and Q where they
    # were and lands on 10 nF, a C0G part this board ALREADY BUYS SIXTEEN OF as the
    # electrode RF filter C1-C16.
    #
    #   f0 = 1/(2.pi.R.sqrt(C1.C2)) = 1/(2.pi.215k.sqrt(10n x 22n)) = 49.9 Hz
    #   Q  = 0.5.sqrt(C2/C1) = 0.5.sqrt(2.2) = 0.742, unchanged
    #
    # Same 0603 footprints, same nets, same pad count: this is a BOM change and the board
    # does not move.  The 215 k raises the resistors' own thermal noise to about 60 nV per
    # root hertz, which is nothing against a stage whose output is scaled to +/-100 mV,
    # and the OPA4376's 0.2 pA of input bias current develops 43 nV across it.
    add(f"R{b+5}", R06, "215k 0.1%", ECOL[3], r1, 0, "Vishay TNPW0603215KBEEA",
        f"Sallen-Key R1, channel {k}", "A")
    add(f"R{b+6}", R06, "215k 0.1%", ECOL[4], r1, 0, "Vishay TNPW0603215KBEEA",
        f"Sallen-Key R2, channel {k}", "A")
    add(f"C{b+1}", C06, "10n C0G 50V", ECOL[0], r2, 0,
        "Murata GCM1885C1H103JA16D",
        f"Sallen-Key C to AGND_REF, channel {k}.  C0G, and the SAME part as the sixteen "
        f"electrode filters C1-C16, so it adds no line to the purchase.", "A")
    add(f"C{b+2}", C06, "22n C0G 50V", ECOL[1], r2, 0, "Murata GCM1885C1H223JA16D",
        f"Sallen-Key feedback C, sets Q = 0.74, channel {k}.  C0G for the same reason as "
        f"C{b+1}; the ratio 22/10 is what holds Q at 0.742.", "A")
    add(f"R{b+7}", R06, "22k 0.1%", ECOL[2], r2, 0, "Vishay TNPW060322K0BEEA",
        f"output divider, top, channel {k}", "A")
    add(f"R{b+8}", R06, "2k2 0.1%", ECOL[3], r2, 0, "Vishay TNPW06032K20BEEA",
        f"output divider, bottom -- scales to +/-100 mV, channel {k}", "A")
    add(f"C{b+4}", C06, "100n X7R 25V", ECOL[4], r2, 0, "Murata GCM188R71E104KA57D",
        f"AVSS decoupling at U{k}", "A")

# touch-proof electrode panel, left edge of the board = underside of the pod
for i, (ref, lbl) in enumerate([("J15", "EMG1 cheek"), ("J16", "EMG2 submental"),
                                ("J17", "EMG3 laryngeal")]):
    add(ref, "DIN42802_1p5mm_Socket", f"DIN 42802 {lbl}", 8.0, 76.0 + 12.0 * i, 0,
        "Staubli SLB1,5-F / LB-I1,5",
        f"touch-proof 1.5 mm safety socket, {lbl}, colour-coded", "A")
# ECO-EEG-028: J22 sat at (30, 116), which made EOGIN1/EOGIN2 climb 50 mm through the
# ladder's own escape lane at 0.35 mm electrode clearance -- two of the four vertical
# electrode runs that sealed rows 15 and 16 in.  Here, directly under the bottom of
# the ladder, both runs are under 9 mm and stay clear of that lane.  Uncertain: the
# jumpers from the panel DIN sockets now terminate mid-board rather than at its edge,
# which WH-EEG-008's EOG option loom must tolerate (it is a hand-built loom either way).
add("J22", PS(3), "EOG / spare electrode header", 15.7, 73.5, 270,
    SKT(3), "1x3 socket: two spare protected electrode channels and their screen. "
            "Wired to panel DIN sockets only when the EOG option is used (RFQ 3.1).", "A")

# ===========================================================================
# DIGITAL ZONE  (x > 58 mm)
# ===========================================================================
add("J1", PS(12), "ADS1299 module #1 digital", 66.0, 6.0, 0, SKT(12),
    "1x12 socket: SPI, control lines, shared clock, 3V3 and 5 V feed to module #1", "D")
add("J3", PS(12), "ADS1299 module #2 digital", 66.0, 42.0, 0, SKT(12),
    "1x12 socket: SPI, control lines, shared clock, 3V3 and 5 V feed to module #2", "D")
add("J5", PS(4), "ADS #1 DAISY_IN / CLKOUT stub", 72.0, 6.0, 0, SKT(4),
    "1x4 stub: module #2 DOUT into module #1 DAISY_IN and the shared 2.048 MHz clock", "D")
add("J6", PS(22), "ESP32-S3-DevKitC-1 row A", 82.0, 8.0, 0, SKT(22),
    "1x22 socket, DevKitC-1 left header. Row spacing to J7 is 22.86 mm (0.900 in).", "D")
add("J7", PS(22), "ESP32-S3-DevKitC-1 row B", 104.86, 8.0, 0, SKT(22),
    "1x22 socket, DevKitC-1 right header", "D")
add("J10", PS(4), "ADuM4160 USB isolator, device side", 136.0, 6.0, 0, SKT(4),
    "1x4: isolated USB D+/D-, isolated 3V3 and DGND. No carrier copper crosses the "
    "barrier. The module's host receptacle is USB-B on the qualified part, not USB-C; "
    "WH-09 adapts it. See RUL-EEG-021 section B.", "D")
add("J11", PS(4), "ATECC608B breakout", 136.0, 20.0, 0, SKT(4),
    "1x4: secure element on the shared I2C bus", "D")
add("J12", PS(8), "Charger + fuel gauge module", 136.0, 34.0, 0, SKT(8),
    "1x8: bq24074-class charger with power path, and the MAX17048 gauge on I2C", "D")
add("J13", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "18650 protected cell", 136.0, 60.0, 0,
    "JST B2B-PH-K-S(LF)(SN)", "battery input from the keyed cell carrier", "D")
add("J20", PS(8), "microSD breakout, SDMMC 1-bit", 136.0, 72.0, 0, SKT(8),
    "1x8: microSD card breakout wired for one-bit SDMMC (70 kB/s needed, 2 MB/s available)",
    "D")

# --- lower digital zone, in columns so every bundle has its own channel ----------------
# ECO-EEG-028: J9 sat at (66, 78), the far west of the digital zone, while every net
# on it terminates in the east -- J21 and J28 at x = 122, MIC_MUTE at J7.18 -- so three
# signals crossed the whole lower digital belt and pin 2 (ROOM_PRE) was sealed in by
# the shift-register feed bundle.  At (114, 62) it faces its partners across open
# board.  The ROOM_PRE and VOICE_PRE taps toward the envelope detectors still cross to
# the analogue zone; that is inherent in RFQ E-12/E-11, not in this placement.
add("J9", PS(4), "Codec microphone feeds", 114.0, 62.0, 0, SKT(4),
    "1x4: voice and room preamp outputs into the codec ADC, and the room-mic mute line", "D")
add("J30", PS(10), "Helmet harness -- contact lights (10-way)", 66.0, 90.0, 0, SKT(10),
    "1x10 socket: eight contact-light lines, the light common and its return. This is the "
    "second helmet cable; it carries no electrode signal.", "D")
add("C84", C06, "100n X7R 25V", 66.0, 120.0, 0, "Murata GCM188R71E104KA57D",
    "local supply decoupling at J19", "D")
# R70-R77 sit between J30 (the light harness) and J19 (the shift register) at the same
# pitch as both, so all sixteen connections are short horizontal runs at their own y and
# nothing has to queue in a vertical channel.
for i in range(8):
    add(f"R{70+i}", R06, "1k 1%", 72.0, 89.9 + i * 2.54, 0, "Vishay CRCW06031K00FKEA",
        f"contact-light series resistor, helmet site {i+1}", "D")
add("R78", R06, "0R", 72.0, 111.0, 0, "Vishay CRCW06030000Z0EA",
    "LED_V common drive link from GPIO48. 0R fitted; 47R is the approved alternate.", "D")
add("R79", R06, "0R", 72.0, 114.0, 0, "Vishay CRCW06030000Z0EA",
    "contact-light common return to DGND", "D")
add("R87", R06, "0R", 72.0, 117.0, 0, "Vishay CRCW06030000Z0EA",
    "74HC595 output enable tied active (OE low)", "D")
add("R88", R06, "10k 1%", 72.0, 120.0, 0, "Vishay CRCW060310K0FKEA",
    "74HC595 master-reset pull-up", "D")
add("C88", C06, "100n X7R 25V", 72.0, 123.0, 0, "Murata GCM188R71E104KA57D",
    "74HC595 power-on reset. Dark-at-boot is guaranteed by LED_V (GPIO48) floating.", "D")
add("J19", PS(16), "74HC595 contact-light driver", 78.0, 72.0, 0, SKT(16),
    "1x16: shift-register module. Q0..Q7 drive the eight helmet contact lights.", "D")
add("J8", PS(14), "ES8388 codec module", 90.0, 72.0, 0, SKT(14),
    "1x14: I2S, I2C, headphone amplifier output, the stimulus envelope tap and 5 V", "D")
add("C82", C06, "100n X7R 25V", 94.0, 110.0, 0, "Murata GCM188R71E104KA57D",
    "local supply decoupling at J8", "D")
add("SW1", "SW_PUSH_6mm_H5mm", "BTN_A response (green)", 102.0, 76.0, 0, "Omron B3F-4055",
    "response button A, 12 mm green cap on an extender", "D")
add("SW2", "SW_PUSH_6mm_H5mm", "BTN_B response (blue)", 102.0, 90.0, 0, "Omron B3F-4055",
    "response button B, 12 mm blue cap on an extender", "D")
add("SW3", "SW_PUSH_6mm_H5mm", "BTN_STOP (red)", 102.0, 104.0, 0, "Omron B3F-4055",
    "session stop button, 12 mm red cap, distinct tactile feel", "D")
for rr, cc, net, ry in (("R50", "C50", "BTN_A", 76.0), ("R51", "C51", "BTN_B", 90.0),
                        ("R52", "C52", "BTN_STOP", 104.0)):
    add(rr, R06, "10k 1%", 110.0, ry, 0, "Vishay CRCW060310K0FKEA", f"pull-up for {net}", "D")
    add(cc, C06, "100n X7R 25V", 115.0, ry, 0, "Murata GCM188R71E104KA57D",
        f"hardware debounce for {net}, with the firmware debounce in FW-EEG-001", "D")
add("J21", PS(6), "Boom-mic preamp module (part not settled, E-14)", 122.0, 72.0, 0,
    SKT(6),
    "1x6: fixed-gain boom microphone preamp module. RFQ E-14 forbids automatic gain "
    "control, so the MAX9814 of package v1 is NOT APPROVED (AVL-EEG-017); a "
    "MAX4466-class fixed-gain board is the reference. The part is an open item and "
    "this socket is specified by its interface, not by a chosen module.", "D")
add("J18", PS(4), "Boom microphone pigtail (TRRS)", 122.0, 90.0, 0, SKT(4),
    "1x4: to the panel TRRS jack at the left temple", "D")
add("J28", PS(4), "Room microphone module", 122.0, 102.0, 0, SKT(4),
    "1x4: outward-facing room microphone module with hardware mute", "D")
add("R89", R06, "2k2 1% -- DNP", 122.0, 114.0, 0, "Vishay CRCW06032K20FKEA",
    "electret bias for the boom capsule. DO NOT POPULATE unless the preamp module lacks "
    "its own microphone bias; see ICD-EEG-006 section 7.2.", "D", dnp=True)
add("C90", C06, "10u X5R 16V", 122.0, 117.0, 0, "Murata GRM188R61C106MA73D",
    "electret bias decoupling", "D")
# ECO-EEG-021: the I2C bus had no pull-up anywhere on the carrier and depended entirely
# on whatever the modules happened to carry.  That is not a design.
# ECO-EEG-028: moved from (132, 26/30), the most congested corner of the bottom copper,
# where the Rev B route could not reach their DVDD3V3 pads at all.  Here they tap the
# bus 7 mm from where it leaves J7 pins 4/5; electrically a pull-up works anywhere on
# a bus this short.
add("R94", R06, "4k7 1%", 112.0, 20.0, 0, "Vishay CRCW06034K70FKEA",
    "I2C SDA pull-up to DVDD3V3", "D")
add("R95", R06, "4k7 1%", 112.0, 24.0, 0, "Vishay CRCW06034K70FKEA",
    "I2C SCL pull-up to DVDD3V3", "D")
# ECO-EEG-020: three global fiducials so the placement machine does not need a vision
# teach on test-point pads.
for _i, (_fx, _fy) in enumerate([(12.0, 10.0), (144.0, 100.0), (12.0, 120.0)]):
    add(f"FID{_i+1}", "Fiducial_1mm_Mask3mm", "global fiducial", _fx, _fy, 0, "-",
        "1 mm copper, 3 mm mask opening, no net", "D" if _fx > ZONE_SPLIT_X else "A")
add("J27", PS(4), "Headphone jack pigtail", 128.0, 72.0, 0, SKT(4),
    "1x4: to the panel 3.5 mm headphone jack", "D")
add("J25", PS(6), "Buck-boost module, TPS63020 class", 128.0, 86.0, 0, SKT(6),
    "1x6: VSYS to a regulated 5.0 V rail for the DevKit and both ADS1299 modules", "D")
# ECO-EEG-028: J26 sat at (128, 104), so UART0 ran 100 mm from the top of J7 down the
# board's most congested corner (the Rev B route shipped UART_TX and UART_RX with zero
# copper) and RESET_EN squeezed at minimum width.  Here, 12 mm east of J7 pins 2/3, in
# a block that carried almost no copper, all three are short runs; the move also
# vacates the x = 118-128 lane that HP_GND and ROOM_PRE need.  A bench cable still
# reaches it: the header is at the board's top-right, clear of the DevKit and 24 mm
# from the isolation strip.
add("J26", PS(6), "Debug / programming header", 117.0, 8.0, 0, SKT(6),
    "1x6: 3V3, GND, UART0 TX and RX, EN and NC_GPIO0 -- console and recovery flashing. "
    "Way 6 is the spare NC_GPIO0, not GPIO0: GPIO0 is committed to LED_SR_LATCH.", "D")
add("C86", C06, "100n X7R 25V", 128.0, 120.0, 0, "Murata GCM188R71E104KA57D",
    "local supply decoupling at J21", "D")
add("R83", R06, "10k 1%", 102.0, 118.0, 0, "Vishay CRCW060310K0FKEA",
    "series limiter between the comparator output and the 3V3 GPIO", "D")
add("D23", "SOT-23", "BAV99", 107.0, 118.0, 0, "Nexperia BAV99,215",
    "clamp of ENV_CMP to DGND and DVDD3V3", "D")

# --- power column at the right-hand edge ---------------------------------------------
add("R85", R06, "150k 1%", 145.0, 32.0, 0, "Vishay CRCW0603150KFKEA",
    "VBUS-present divider, bottom. ECO-EEG-022: 3.00 V at VBUS = 5 V, above the 2.48 V "
    "input-high threshold. The 56 kOhm of the first cut gave 1.79 V and would not have "
    "asserted reliably.", "D")
add("R84", R06, "100k 1%", 145.0, 36.0, 0, "Vishay CRCW0603100KFKEA",
    "VBUS-present divider, top", "D")
add("D24", "SOT-23", "PESD5V0S2BT", 145.0, 41.0, 0, "Nexperia PESD5V0S2BT,215",
    "transient suppressor on the charge input", "D")
add("F1", "R_1206_3216Metric", "PTC 1.1 A hold / 2.2 A trip", 145.0, 46.0, 90,
    "Bourns MF-MSMF110-2", "resettable fuse in the charge input", "D")
add("C70", C06, "10u X5R 16V", 145.0, 51.0, 0, "Murata GRM188R61C106MA73D",
    "VSYS bulk at the buck-boost input", "D")
add("C71", C06, "10u X5R 16V", 145.0, 55.0, 0, "Murata GRM188R61C106MA73D",
    "VSYS bulk at the buck-boost input", "D")
add("C72", C06, "10u X5R 16V", 145.0, 59.0, 0, "Murata GRM188R61C106MA73D",
    "V5V bulk at the buck-boost output", "D")
add("C73", C06, "10u X5R 16V", 145.0, 63.0, 0, "Murata GRM188R61C106MA73D",
    "V5V bulk feeding the DevKit and both ADS1299 modules", "D")
add("C74", C06, "10u X5R 16V", 145.0, 67.0, 0, "Murata GRM188R61C106MA73D",
    "DVDD3V3 bulk", "D")
add("R86", R06, "100k 1%", 145.0, 71.0, 0, "Vishay CRCW0603100KFKEA",
    "buck-boost enable pull-up to VSYS, so the rail starts before DVDD3V3 exists", "D")
add("J24", "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "Charge input from the panel USB-C",
    143.0, 80.0, 0, "JST B2B-PH-K-S(LF)(SN)",
    "charge-only USB-C receptacle pigtail; no data conductor enters here", "D")
add("L1", L06, "600R at 100 MHz, 1.5 A", 130.0, 16.0, 90, "Murata BLM18PG601SN1D",
    "ferrite between DVDD3V3 and the isolator device-side supply", "D")
add("C89", C06, "10u X5R 16V", 130.0, 12.0, 0, "Murata GRM188R61C106MA73D",
    "isolator device-side bulk", "D")
# ECO-EEG-028: C80 sat at (70, 32) -- 26 mm from the J1.1 pin it decouples and exactly
# in the escape mouth of J1 pins 9-11, where its pads, its ground via and the DVDD3V3
# trunk that had to reach it walled RESET, CLK_ADS and V5V in (all three shipped
# stranded there in Rev B).  C81 did the same to J3 pins 9-11 from (70, 68).  Both now
# sit in line with the socket column, next to the pin 1 they serve; the DVDD3V3 trunk
# follows the west strip instead of crossing the SPI fan twice.
DEC3V3 = [("C80", "J1", 66.0, 3.3), ("C81", "J3", 66.0, 38.0),
          ("C83", "J11", 130.0, 20.0), ("C85", "J20", 140.0, 96.0),
          ("C87", "J10", 130.0, 8.0)]
for cref, near, cx, cy in DEC3V3:
    add(cref, C06, "100n X7R 25V", cx, cy, 0, "Murata GCM188R71E104KA57D",
        f"local supply decoupling at {near}", "D")
DEC3V3 += [("C82", "J8", 94.0, 110.0), ("C84", "J19", 66.0, 120.0),
           ("C86", "J21", 128.0, 120.0)]

# The four M3 mounting holes, and the copper keep-out they carry on EVERY layer.  Named
# constants because three generators need them: pours.py voids the planes here, drc.py
# measures against them, and kicad_write.py writes them out as explicit keepout zones so a
# reader who refills the zones in KiCad gets the same answer as the Gerbers.
MOUNTING_HOLES = [(5.0, 5.0), (145.0, 5.0), (5.0, 125.0), (145.0, 125.0)]
MOUNTING_KEEPOUT_D = 6.0

for i, (x, y) in enumerate(MOUNTING_HOLES):
    add(f"MH{i+1}", "MountingHole_3.2mm_M3", "M3 x 3.2 mm NPTH", x, y, 0, "-",
        "board mounting hole, non-plated, 6 mm diameter keep-out on all four layers",
        "D" if x > ZONE_SPLIT_X else "A")

# The test points sit along the bottom edge, clear of the band between the DevKit sockets
# and the lower digital zone, which is the only channel between the two.
TESTPOINTS_D = [("TP1", "SCLK", 66.0, 126.5), ("TP2", "MOSI", 71.0, 126.5),
                ("TP3", "MISO", 76.0, 126.5), ("TP4", "DRDY", 81.0, 126.5),
                ("TP5", "I2S_BCLK", 86.0, 126.5), ("TP6", "I2S_LRCK", 91.0, 126.5),
                ("TP12", "DVDD3V3", 96.0, 126.5), ("TP14", "DGND", 101.0, 126.5),
                ("TP15", "VSYS", 106.0, 126.5), ("TP16", "V5V", 111.0, 126.5),
                ("TP17", "NC_DRDY2", 116.0, 126.5), ("TP18", "CLK_ADS", 121.0, 126.5)]
for ref, net, x, y in TESTPOINTS_D:
    add(ref, "TestPoint_Pad_D1.5mm", net, x, y, 0, "-", f"test point, {net}", "D")
TESTPOINTS = TESTPOINTS_D + [("TP7", "ENV_STIM", 56.0, 80.0), ("TP8", "ENV_VOICE", 56.0, 92.0),
                             ("TP9", "ENV_ROOM", 56.0, 104.0), ("TP10", "AVDD", 56.0, 28.0),
                             ("TP11", "AVSS", 56.0, 32.0), ("TP13", "AGND_REF", 54.0, 39.0)]

# ---------------------------------------------------------------------------
# 2. Netlist
# ---------------------------------------------------------------------------
N = {}


def conn(ref, pins):
    for i, net in enumerate(pins, start=1):
        if net:
            N[f"{ref}.{i}"] = net


def wire(*pairs):
    for pin, net in pairs:
        N[pin] = net


conn("J1", ["DVDD3V3", "DGND", "SCLK", "MOSI", "MISO", "DRDY",
            "CS", "START", "RESET", "CLK_ADS", "V5V", "DGND"])
conn("J2", ["IN1", "IN2", "IN3", "IN4", "IN5", "IN6", "IN7", "IN8",
            "SRB1", "BIASOUT"])
conn("J23", ["AVDD", "AVSS", "BIASIN", "AGND_REF", "AVDD", "AVSS"])
conn("J3", ["DVDD3V3", "DGND", "SCLK", "MOSI", "DAISY", "NC_DRDY2",
            "CS", "START", "RESET", "CLK_ADS", "V5V", "DGND"])
conn("J4", ["EMG1", "EMG2", "EMG3", "ENV_STIM", "ENV_VOICE", "ENV_ROOM",
            "SPARE1", "SPARE2", "SRB1", "NC_BIASOUT2"])
conn("J29", ["AVDD2", "AVSS2", "BIASIN", "AGND_REF", "AVDD2", "AVSS2"])
conn("J5", ["DAISY", "CLK_ADS", "DGND", "DGND"])

# ESP32-S3-DevKitC-1: header POSITIONS, not GPIO numbers. See NOTES['gpio'].
conn("J6", ["DVDD3V3", "DVDD3V3", "RESET_EN", "BTN_A", "BTN_B", "BTN_STOP",
            "I2S_DIN", "START", "RESET", "I2S_MCLK", "I2S_BCLK", "I2S_LRCK",
            "ENV_CMP", "VBUS_DET", "I2S_DOUT", "CS", "MOSI", "SCLK",
            "MISO", "DRDY", "V5V", "DGND"])
conn("J7", ["DGND", "UART_TX", "UART_RX", "SDA", "SCL", "LED_SR_CLK",
            "LED_SR_DATA", "SD_D0", "SD_CLK", "SD_CMD",
            "NC_GPIO37", "NC_GPIO36", "NC_GPIO35",
            "LED_SR_LATCH", "NC_GPIO45", "LED_PWM", "CHG_CE", "MIC_MUTE",
            "USB_DP", "USB_DN", "DGND", "DGND"])

conn("J8", ["DVDD3V3", "DGND", "I2S_MCLK", "I2S_BCLK", "I2S_LRCK", "I2S_DIN",
            "I2S_DOUT", "SDA", "SCL", "HP_TAP", "HP_L", "HP_R", "HP_GND", "V5V"])
conn("J9", ["VOICE_PRE", "ROOM_PRE", "DGND", "MIC_MUTE"])
conn("J18", ["VOICE_RAW", "DGND", "DGND", "DGND"])
conn("J21", ["DVDD3V3", "DGND", "VOICE_PRE", "VOICE_RAW", "NC_MIC_GAIN", "DGND"])
conn("J28", ["DVDD3V3", "DGND", "ROOM_PRE", "MIC_MUTE"])
conn("J27", ["HP_L", "HP_R", "HP_GND", "NC_HP_DET"])
conn("J10", ["VDD_ISO", "USB_DN", "USB_DP", "DGND"])
conn("J11", ["DVDD3V3", "DGND", "SDA", "SCL"])
conn("J20", ["DVDD3V3", "DGND", "SD_CLK", "SD_CMD", "SD_D0", "DGND", "DGND", "DGND"])
conn("J13", ["VBAT", "DGND"])
conn("J12", ["VBAT", "DGND", "VBUS_CHG", "CHG_CE", "SDA", "SCL", "VSYS", "NC_CHG_STAT"])
conn("J24", ["VBUS_IN", "DGND"])
conn("J25", ["VSYS", "DGND", "V5V", "DGND", "BOOST_EN", "NC_BOOST_PG"])
conn("J26", ["DVDD3V3", "DGND", "UART_TX", "UART_RX", "RESET_EN", "NC_GPIO0"])
conn("J14", ["E_Fz", "E_Cz", "E_Pz", "E_C3", "E_C4", "E_T7", "E_T8", "E_F7",
             "REF_L", "REF_R", "BIAS_EL", "HARN_SHIELD"])
conn("J30", ["LED1", "LED2", "LED3", "LED4", "LED5", "LED6", "LED7", "LED8",
             "LED_V", "LED_GND"])
conn("J19", ["DVDD3V3", "DGND", "LED_SR_DATA", "LED_SR_CLK", "LED_SR_LATCH",
             "LED_OE", "LED_MR", "SR_Q0", "SR_Q1", "SR_Q2", "SR_Q3",
             "SR_Q4", "SR_Q5", "SR_Q6", "SR_Q7", "NC_SR_Q7S"])
conn("J22", ["EOGIN1", "AGND_REF", "EOGIN2"])
for ref, net in [("J15", "EMGIN1"), ("J16", "EMGIN2"), ("J17", "EMGIN3")]:
    wire((f"{ref}.1", net))

wire(("F1.1", "VBUS_IN"), ("F1.2", "VBUS_CHG"),
     ("D24.1", "VBUS_CHG"), ("D24.2", "DGND"), ("D24.3", "DGND"),
     ("R84.1", "VBUS_CHG"), ("R84.2", "VBUS_DET"),
     ("R85.1", "VBUS_DET"), ("R85.2", "DGND"),
     ("R86.1", "VSYS"), ("R86.2", "BOOST_EN"),
     ("C70.1", "VSYS"), ("C70.2", "DGND"), ("C71.1", "VSYS"), ("C71.2", "DGND"),
     ("C72.1", "V5V"), ("C72.2", "DGND"), ("C73.1", "V5V"), ("C73.2", "DGND"),
     ("C74.1", "DVDD3V3"), ("C74.2", "DGND"),
     ("L1.1", "DVDD3V3"), ("L1.2", "VDD_ISO"),
     ("C89.1", "VDD_ISO"), ("C89.2", "DGND"))
for cref, near, _x, _y in DEC3V3:
    wire((f"{cref}.1", "VDD_ISO" if cref == "C87" else "DVDD3V3"), (f"{cref}.2", "DGND"))

for i in range(8):
    wire((f"R{70+i}.1", f"SR_Q{i}"), (f"R{70+i}.2", f"LED{i+1}"))
wire(("R78.1", "LED_PWM"), ("R78.2", "LED_V"),
     ("R79.1", "LED_GND"), ("R79.2", "DGND"),
     ("R87.1", "LED_OE"), ("R87.2", "DGND"),
     ("R88.1", "LED_MR"), ("R88.2", "DVDD3V3"),
     ("C88.1", "LED_MR"), ("C88.2", "DGND"))

for n, src, dst, lbl in PROT:
    wire((f"R{n}.1", src), (f"R{n}.2", dst),
         (f"D{n}.1", "AVSS"), (f"D{n}.2", "AVDD"), (f"D{n}.3", dst),
         (f"C{n}.1", dst), (f"C{n}.2", "AGND_REF"))
# CHANNEL 11 IS NO LONGER AN EXCEPTION.
#
# This used to override the generic PROT loop above and reverse the row: R11.1 = BIASOUT,
# R11.2 = BIAS_EL, with D11.3 and C11.1 on BIAS_EL -- the PATIENT side of the resistor.
# It was the only one of the sixteen protection networks whose clamp and filter a fault
# could reach with no series resistance in the path, and the consequence was a
# single-fault current on the Fpz forehead electrode of 183.6 uA against S-02's 50 uA
# limit on this programme's own bound B, and unbounded on bound A, where every other
# channel gives 41.2 uA.  RISK-EEG-011 recorded it as SF-1a, SF-6a and SR-12.
#
# The row is now generated by the loop like the other fifteen: src BIAS_EL (patient),
# dst BIASOUT (module), with D11.3 and C11.1 on BIASOUT behind the 47 kOhm.  Nothing is
# added and no value changes; an exception is removed.  SF-1a collapses into the ordinary
# SF-1 and SF-6a into SF-6, both of which are rows that already exist.
#
# The bias signal still runs outward from the module to the electrode -- that is what the
# net names say and a resistor is symmetric, so reversing which pad is called .1 changes
# the netlist and not the circuit.
#
# THIS DOES NOT DISCHARGE SR-12.  The electrical safety reviewer of RISK-EEG-011 section 7
# owns that item and that review has not started.  Applying the fix the analysis points to
# is not the same as having it approved.


# OPA4376 TSSOP-14: 1 OUTA 2 -INA 3 +INA 4 V+ 5 +INB 6 -INB 7 OUTB
#                   8 OUTC 9 -INC 10 +INC 11 V- 12 +IND 13 -IND 14 OUTD
for k, b, src, out, _yb, _lbl in ENV:
    AC, HW, SUM_, MID, INP, FLT, DIV = (f"ENV{k}_AC", f"ENV{k}_HW", f"ENV{k}_SUM",
                                        f"ENV{k}_MID", f"ENV{k}_INP", f"ENV{k}_FLT",
                                        f"ENV{k}_DIV")
    INM, ROUT, ABS_ = f"ENV{k}_INM", f"ENV{k}_ROUT", f"ENV{k}_ABS"
    wire((f"C{b}.1", src), (f"C{b}.2", AC),
         (f"R{b}.1", AC), (f"R{b}.2", INM),
         (f"R{b+1}.1", HW), (f"R{b+1}.2", INM),
         (f"D{b}.3", ROUT), (f"D{b}.1", HW), (f"D{b}.2", INM),
         (f"U{k}.1", ROUT), (f"U{k}.2", INM), (f"U{k}.3", "AGND_REF"), (f"U{k}.4", "AVDD"),
         (f"R{b+2}.1", HW), (f"R{b+2}.2", SUM_),
         (f"R{b+3}.1", AC), (f"R{b+3}.2", SUM_),
         (f"R{b+4}.1", SUM_), (f"R{b+4}.2", ABS_),
         (f"U{k}.5", "AGND_REF"), (f"U{k}.6", SUM_), (f"U{k}.7", ABS_),
         (f"R{b+5}.1", ABS_), (f"R{b+5}.2", MID),
         (f"R{b+6}.1", MID), (f"R{b+6}.2", INP),
         (f"C{b+1}.1", INP), (f"C{b+1}.2", "AGND_REF"),
         (f"C{b+2}.1", MID), (f"C{b+2}.2", FLT),
         (f"U{k}.8", FLT), (f"U{k}.9", FLT), (f"U{k}.10", INP), (f"U{k}.11", "AVSS"),
         (f"R{b+7}.1", FLT), (f"R{b+7}.2", DIV),
         (f"R{b+8}.1", DIV), (f"R{b+8}.2", "AGND_REF"),
         (f"U{k}.12", DIV), (f"U{k}.13", out), (f"U{k}.14", out),
         (f"C{b+3}.1", "AVDD"), (f"C{b+3}.2", "AGND_REF"),
         (f"C{b+4}.1", "AVSS"), (f"C{b+4}.2", "AGND_REF"))

# TLV3201 SOT-23-5: 1 OUT, 2 V-, 3 +IN, 4 -IN, 5 V+
wire(("R80.1", "AVDD"), ("R80.2", "ENV_THR"),
     ("R81.1", "ENV_THR"), ("R81.2", "AGND_REF"),
     ("U7.1", "CMP_RAW"), ("U7.2", "AVSS"), ("U7.3", "ENV_STIM"),
     ("U7.4", "ENV_THR"), ("U7.5", "AVDD"),
     ("R82.1", "CMP_RAW"), ("R82.2", "ENV_STIM"),
     ("R83.1", "CMP_RAW"), ("R83.2", "ENV_CMP"),
     ("D23.1", "DGND"), ("D23.2", "DVDD3V3"), ("D23.3", "ENV_CMP"))

for sw, rr, cc, net in [("SW1", "R50", "C50", "BTN_A"), ("SW2", "R51", "C51", "BTN_B"),
                        ("SW3", "R52", "C52", "BTN_STOP")]:
    wire((f"{sw}.1", net), (f"{sw}.2", "DGND"),
         (f"{rr}.1", net), (f"{rr}.2", "DVDD3V3"),
         (f"{cc}.1", net), (f"{cc}.2", "DGND"))

wire(("R94.1", "SDA"), ("R94.2", "DVDD3V3"),
     ("R95.1", "SCL"), ("R95.2", "DVDD3V3"),
     ("C100.1", "AVDD"), ("C100.2", "AGND_REF"), ("C101.1", "AVSS"), ("C101.2", "AGND_REF"),
     ("C102.1", "AVDD"), ("C102.2", "AGND_REF"), ("C103.1", "AVSS"), ("C103.2", "AGND_REF"),
     ("R90.1", "AGND_REF"), ("R90.2", "DGND"),
     ("R91.1", "HARN_SHIELD"), ("R91.2", "DGND"),
     ("R92.1", "AVDD2"), ("R92.2", "AVDD"),
     ("R93.1", "AVSS2"), ("R93.2", "AVSS"),
     ("R89.1", "DVDD3V3"), ("R89.2", "VOICE_RAW"),
     ("C90.1", "DVDD3V3"), ("C90.2", "DGND"))

for ref, net, _x, _y in TESTPOINTS:
    wire((f"{ref}.1", net))

# ---------------------------------------------------------------------------
# 3. Net classes -- these drive the router and the DRC
# ---------------------------------------------------------------------------
ELECTRODE_NETS = {"E_Fz", "E_Cz", "E_Pz", "E_C3", "E_C4", "E_T7", "E_T8", "E_F7",
                  "REF_L", "REF_R", "BIAS_EL", "EMGIN1", "EMGIN2", "EMGIN3",
                  "EOGIN1", "EOGIN2", "IN1", "IN2", "IN3", "IN4", "IN5", "IN6",
                  "IN7", "IN8", "SRB1", "BIASOUT", "BIASIN", "EMG1", "EMG2",
                  "EMG3", "SPARE1", "SPARE2"}
ANALOG_NETS = {"HP_TAP", "VOICE_PRE", "VOICE_RAW", "ROOM_PRE",
               "ENV_STIM", "ENV_VOICE", "ENV_ROOM", "ENV_THR", "CMP_RAW",
               "HP_L", "HP_R", "HP_GND"}
for _k in (1, 2, 3):
    ANALOG_NETS |= {f"ENV{_k}_{s}" for s in
                    ("AC", "HW", "INM", "SUM", "MID", "INP", "FLT", "DIV", "ABS", "ROUT")}
POWER_A_NETS = {"AVDD", "AVSS", "AVDD2", "AVSS2", "AGND_REF"}
POWER_D_NETS = {"DVDD3V3", "DGND", "VBAT", "VSYS", "V5V", "VBUS_CHG", "VBUS_IN", "VDD_ISO"}
USB_NETS = {"USB_DP", "USB_DN"}

NETCLASS = {   # name: (track width mm, clearance mm)
    "ELECTRODE": (0.30, 0.40),
    "ANALOG":    (0.25, 0.30),
    "POWER_A":   (0.40, 0.30),
    "POWER_D":   (0.80, 0.30),
    "USB":       (0.30, 0.35),
    "DEFAULT":   (0.25, 0.25),
}

POURS = [("AGND_REF", "B.Cu", (0.0, ZONE_SPLIT_X)),
         ("DGND", "B.Cu", (ZONE_SPLIT_X, BOARD_W))]

ANALOG_ZONE_NETS = ELECTRODE_NETS | POWER_A_NETS | {
    f"ENV{k}_{s}" for k in (1, 2, 3)
    for s in ("AC", "HW", "INM", "SUM", "MID", "INP", "FLT", "DIV", "ABS", "ROUT")
} | {"ENV_THR"}
# CMP_RAW deliberately crosses the zone line: it is the one analogue-referenced signal
# that must reach a 3V3 GPIO, and it does so through R83 and the D23 clamp.

# nets that must never be routed inside the analogue zone
DIGITAL_ONLY_NETS = {"SCLK", "MOSI", "MISO", "DRDY", "CS", "START", "RESET", "CLK_ADS",
                     "DAISY", "SD_CLK", "SD_CMD", "SD_D0", "I2S_MCLK", "I2S_BCLK",
                     "I2S_LRCK", "I2S_DIN", "I2S_DOUT", "SDA", "SCL", "USB_DP", "USB_DN",
                     "LED_SR_DATA", "LED_SR_CLK", "LED_SR_LATCH", "UART_TX", "UART_RX",
                     "DVDD3V3", "V5V", "VSYS", "VBAT", "VBUS_CHG", "VBUS_IN", "VDD_ISO"}

# Targeted repairs, specified by the programme on 2026-09-02 after the router had
# been taken as far as it goes (143 of 145 nets).  tools/surgery.py applies these
# after routing, only where the named connection is still open, so a full build
# reproduces them and they are never hand-edits of the cache.
#   U1.3  -- the op-amp's AGND_REF input sits directly over the AGND_REF planes; a
#            1.0-1.5 mm F.Cu stub outward from the package (west) to a 0.60/0.30
#            through-via is all it needs.  Only AVDD copper may be ripped to make
#            the site; anything else blocking is reported, not touched.
#   SPARE2 -- R16.2 to D16.3 across the ladder column: every segment of the listed
#            nets that crosses the box is ripped, SPARE2 is routed first at its full
#            electrode geometry (0.30 / 0.40, never relaxed), then the ripped nets
#            re-join at their own full class, crossing the ladder anywhere the new
#            copper leaves free.  The rip list was AVDD/AVSS; measured, that left
#            AGND_REF, EMGIN3 and EOGIN1 crossing at 0.000 mm, so on 2026-09-02 the
#            programme approved widening it.  On the route it applies to, the cost
#            is 6 AVDD, 1 EMGIN3 and 1 EOGIN1 segments; AVSS and AGND_REF no longer
#            cross and stay listed only so the repair holds if the route shifts.
#            If any listed net fails to re-close, the build is worse than before
#            and is reverted -- one open net is not traded for another.
TARGETED_REPAIRS = [
    dict(kind="stub_via", pad="U1.3", length=(1.0, 1.5), rip=("AVDD",),
         via=(0.60, 0.30)),
    dict(kind="corridor", net="SPARE2", a="R16.2", b="D16.3",
         box=(17.0, 68.0, 30.0, 71.0),
         rip=("AVDD", "AVSS", "AGND_REF", "EMGIN3", "EOGIN1"),
         width=0.30, clearance=0.40),
]

# do not place a via or copper under these module outlines (rule DSN-EEG-003 3.1.3)
NO_VIA_ZONES = [("J2", 1.0), ("J4", 1.0), ("J23", 1.0), ("J29", 1.0)]


def netclass_of(net):
    if net in ELECTRODE_NETS:
        return "ELECTRODE"
    if net in USB_NETS:
        return "USB"
    if net in POWER_A_NETS:
        return "POWER_A"
    if net in POWER_D_NETS:
        return "POWER_D"
    if net in ANALOG_NETS:
        return "ANALOG"
    return "DEFAULT"


# ---------------------------------------------------------------------------
# 4. Notes printed onto the fabrication and assembly drawings
# ---------------------------------------------------------------------------
NOTES = {
    "fabrication": [
        "1.  Board outline 150.0 x 130.0 mm, rectangular, no cut-outs, no slots.",
        "2.  FOUR layers, FR-4, Tg >= 150 C, 1.60 mm +/- 10 % finished.",
        "    L1 signal, L2 reference plane, L3 reference plane, L4 signal.",
        "    Outer copper 1 oz (35 um) finished; inner copper 0.5 oz (17 um).",
        "    Stack: 0.035 / prepreg 0.2 / 0.017 / core 1.065 / 0.017 / prepreg 0.2 / 0.035.",
        "3.  Surface finish ENIG: Au 0.05-0.10 um over Ni 3.0-6.0 um.",
        "4.  Solder mask green LPI both sides; silkscreen white, both sides.",
        "5.  Minimum track 0.20 mm, minimum clearance 0.20 mm (8 mil / 8 mil).  Most",
        "    conductors are 0.25 mm or wider; the exceptions are listed in the DRC report.",
        "6.  Vias 0.60 mm pad / 0.30 mm finished hole, tented on both sides.",
        "7.  Smallest plated hole 0.30 mm (vias); largest 1.70 mm (J15-J17).",
        "8.  Four non-plated 3.2 mm holes at (5,5) (145,5) (5,125) (145,125); keep",
        "    6.0 mm clear of copper on both layers.",
        "9.  IPC-6012 class 2, IPC-A-600 class 2.  100 % electrical test to the supplied",
        "    IPC-D-356A netlist.",
        "10. No controlled impedance is required.  USB_DP and USB_DN are a 0.30 mm pair on",
        "    0.35 mm spacing over the bottom-layer DGND pour: about 95 ohm differential on",
        "    this stack-up.  No IMPEDANCE coupon and no impedance report are required.",
        "    A microsection coupon IS required -- see note 13.",
        "11. Mark the board with the fabricator's date code and UL mark inside the outline",
        "    on the bottom silkscreen, clear of all pads.",
        "12. Panelisation is the fabricator's choice.  V-score or tab-route, 5 mm rails.",
        "13. LOT COUPON.  Include ONE four-layer microsection coupon per fabrication lot,",
        "    in the panel rails, carrying at least one plated through-hole of each drill",
        "    size and one via.  It is sectioned at incoming inspection to verify layer",
        "    order and internal annular ring.  QP-EEG-010 row IQC-B11 REJECTS THE WHOLE LOT",
        "    on wrong layer order or an internal annular ring below 0.025 mm, so a lot that",
        "    arrives without a coupon cannot be accepted at all.",
        "14. LOT DOCUMENTS.  Supply with every lot, referenced to the lot number:",
        "    (a) certificate of conformance naming this drawing and revision  (IQC-B1);",
        "    (b) 100 % electrical test report against the supplied IPC-D-356A  (IQC-B2);",
        "    (c) ENIG thickness report, XRF, gold and nickel, min 3 points     (IQC-B5);",
        "    (d) layer-to-layer registration report                            (IQC-B12);",
        "    (e) the microsection report from the note 13 coupon               (IQC-B11).",
        "    These are conditions of acceptance, not extras.  Each is an incoming-inspection",
        "    row in QP-EEG-010 section 2.1 and each rejects the lot if it is absent.",
    ],
    "gpio": [
        "J6 and J7 are ESP32-S3-DevKitC-1 header POSITIONS, not GPIO numbers.",
        "GPIO35, 36 and 37 carry the octal PSRAM on the -N16R8 variant and are NOT",
        "CONNECTED on the carrier (J7 positions 11, 12, 13).  GPIO45 (J7 position 15) is",
        "the VDD_SPI strapping pin and is also left open.",
        "Row spacing J6 to J7 is 22.86 mm (0.900 in), the DevKitC-1 header dimension.",
        "The microSD interface is one-bit SDMMC.  70 kB/s is needed and about 2 MB/s is",
        "available, so the three data lines released by dropping four-bit mode are spent",
        "on the contact-light shift register instead.",
    ],
    "safety": [
        "Every conductor that can reach a person passes through a 47 kOhm 0.1 % series",
        "resistor (R1-R16) and a BAV99 clamp to AVDD/AVSS before it reaches a module.",
        "AGND_REF is the analogue 0 V mid-rail.  AVDD = +2.5 V and AVSS = -2.5 V are",
        "generated on ADS1299 module #1 and brought onto the carrier at J2 pins 11-14.",
        "AGND_REF joins DGND at R90 ONLY.  HARN_SHIELD joins DGND at R91 ONLY.",
        "No copper crosses the isolation barrier.  The ADuM4160 module at J10 is the only",
        "path between the host and the battery-powered side.  Keep 8.0 mm clear of the J10",
        "module outline on both layers -- the strip x >= 141 mm, y = 2 to 22 mm.",
        "The charge input (J24) is a separate, charge-only USB-C receptacle.  A session",
        "cannot start while VBUS is present (VBUS_DET) and the charger enable is held off",
        "by CHG_CE while a session is active.  The helmet is never worn while charging.",
    ],
    "assembly": [
        "SMT on the top side only.  All through-hole parts on the top side.",
        "Purchased modules do NOT plug directly into these sockets.  They mount on the",
        "printed module plate MP-01 above the carrier and connect with keyed 2.54 mm",
        "ribbon jumpers per ICD-EEG-006.  The one exception is the ESP32-S3-DevKitC-1,",
        "which is inserted directly into J6 and J7.",
        "R90 and R91 are the single star points.  Fit exactly one of each.  Never bridge",
        "either with a wire link or a solder blob.",
        "R92 and R93 are fitted by default.  Remove both if ADS1299 module #2 regulates",
        "its own analogue rails; see ICD-EEG-006 section 4.",
        "R89 is DO NOT POPULATE by default.  Fit only if the boom preamp module does not",
        "supply its own electret bias.",
        "Pin 1 of every socket strip is the square pad and is marked on the silkscreen.",
    ],
}

DNP = [ref for ref, c in C.items() if c["dnp"]]
