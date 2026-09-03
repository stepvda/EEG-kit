#!/usr/bin/env python3
"""
schematic.py -- draw the EEG-CAR-01 Rev B schematic set.

Rev A of the package had no schematic at all; the only machine-readable description of
the circuit was net names attached to pads in an unrouted board file.  These sheets are
generated from design.py, so every wire on them is a net that exists on the board.

Output: schematic/SCH-EEG-005_RevB_schematic_set.pdf and one PNG per sheet.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import design as D
import sym as S

W, H = 420.0, 297.0
DATE = D.DATE
REV = D.REV


# --------------------------------------------------------------------------- sheet 1
def sheet_block(pdf, png_dir):
    fig, ax = S.sheet(W, H, "EEG-CAR-01 -- system block diagram",
                      "16-channel research EEG carrier, module-on-carrier architecture",
                      "1 of 8", REV, DATE)
    S.block(ax, 20, 190, 78, 70, "HELMET HM-01",
            ["8 scalp electrodes", "2 ear references (SRB1)", "1 bias electrode (Fpz)",
             "8 bicolour contact lights", "boom microphone"], fc="#f4efe6")
    S.block(ax, 20, 120, 78, 46, "EMG / EOG PANEL",
            ["3 x DIN 42802 touch-proof", "2 spare protected channels"], fc="#f4efe6")
    S.block(ax, 118, 190, 74, 70, "PROTECTION x16",
            ["47 k 0.1 % series (R1-R16)", "BAV99 clamp to AVDD/AVSS",
             "10 n C0G to AGND_REF", "R1-R16 / D1-D16 / C1-C16"])
    S.block(ax, 118, 108, 74, 62, "ENVELOPE x3",
            ["OPA4376 quad, U1-U3", "precision full-wave rectifier",
             "50 Hz Butterworth 2nd order", "x0.0909 output buffer",
             "TLV3201 comparator U7"])
    S.block(ax, 212, 200, 76, 60, "ADS1299 #1",
            ["8 EEG channels, gain 24", "SRB1 reference, bias drive",
             "lead-off 6 nA AC", "CLKOUT -> module #2"], fc="#e8f1ea")
    S.block(ax, 212, 128, 76, 60, "ADS1299 #2",
            ["3 EMG, gain 12", "3 envelopes, gain 1", "2 spare, gain 24",
             "DAISY_IN <- CLK shared"], fc="#e8f1ea")
    S.block(ax, 306, 172, 82, 88, "ESP32-S3-DevKitC-1",
            ["N16R8, radio never started", "DRDY ISR owns the sample", "counter (E-19)",
             "12 MB PSRAM ring buffer", "COBS frames, CRC-32",
             "TinyUSB composite device"], fc="#e6eef6")
    S.block(ax, 306, 108, 82, 52, "ES8388 CODEC",
            ["I2S stereo DAC (stimulus)", "2 ADC (voice, room)",
             "headphone amp, 32 ohm", "HP_TAP -> envelope 1"], fc="#e6eef6")
    S.block(ax, 306, 46, 82, 52, "ADuM4160 ISOLATOR",
            ["2.5 kV RMS, full speed", "host USB-C on the module",
             "no carrier copper crosses", "the barrier"], fc="#fdeaea")
    S.block(ax, 212, 46, 76, 52, "POWER",
            ["18650 protected cell", "bq24074 power path", "TPS63020 -> 5.0 V",
             "MAX17048 gauge", "charge inhibit CHG_CE"], fc="#fff6e0")
    S.block(ax, 118, 46, 74, 52, "STORAGE / ID",
            ["microSD, 1-bit SDMMC", "ATECC608B P-256", "signed block chain",
             "iSerial = unit serial TIOV-B-nnnn"], fc="#e6eef6")
    S.block(ax, 20, 46, 78, 52, "CONTACT LIGHTS",
            ["74HC595, Q0..Q7", "1 k series R70-R77", "LED_V phase from GPIO48",
             "dark at boot and while", "recording (E-27)"], fc="#e6eef6")

    for a, b in [((98, 225), (118, 225)), ((98, 143), (118, 200)),
                 ((192, 230), (212, 230)), ((192, 210), (212, 158)),
                 ((192, 139), (212, 150)), ((288, 230), (306, 220)),
                 ((288, 158), (306, 200)), ((288, 134), (306, 134)),
                 ((347, 172), (347, 160)), ((347, 108), (347, 98)),
                 ((288, 72), (306, 72)), ((212, 72), (192, 72)),
                 ((118, 72), (98, 72))]:
        S.wire(ax, [a, b], color="#6b7f8d", lw=0.9)

    S.label(ax, 214, 268, "Everything left of the isolator is battery powered and floats. "
                          "The only route to a mains-referenced host is the USB isolator, "
                          "and it passes data, not current.", 6.4, ha="center",
            color="#4a5c68")
    S.wire(ax, [(12, 30), (300, 30), (300, 276), (12, 276), (12, 30)], color="#c0392b",
           lw=0.9, ls="--")
    S.label(ax, 16, 33, "ISOLATED / BATTERY-POWERED / PATIENT SIDE", 6.0, color="#c0392b")
    _finish(pdf, png_dir, fig, "sheet1_block")


# --------------------------------------------------------------------------- sheet 2
def sheet_protection(pdf, png_dir):
    fig, ax = S.sheet(W, H, "EEG-CAR-01 -- electrode input protection",
                      "One of sixteen identical paths; the table below assigns them",
                      "2 of 8", REV, DATE)
    x0, y = 60, 235
    S.netlabel(ax, x0 - 34, y, "E_Fz  (J14.1)", direction="right")
    S.wire(ax, [(x0 - 18, y), (x0 - 8, y)])
    (ra, rb) = S.resistor(ax, x0, y, 14, 4.4, ref="R1", val="47k 0.1% 25ppm")
    S.wire(ax, [(x0 - 8, y), ra])
    node = (x0 + 30, y)
    S.wire(ax, [rb, node])
    S.junction(ax, *node)
    # clamp
    S.wire(ax, [node, (x0 + 30, y + 24)])
    S.diode(ax, x0 + 30, y + 30, 3.0, rot=90, ref="D1a", val="", lead=3.0)
    S.wire(ax, [(x0 + 30, y + 36), (x0 + 30, y + 42)])
    S.rail(ax, x0 + 30, y + 42, "AVDD  +2.5 V")
    S.wire(ax, [node, (x0 + 30, y - 24)])
    S.diode(ax, x0 + 30, y - 18, 3.0, rot=90, ref="D1b", val="", lead=3.0)
    S.wire(ax, [(x0 + 30, y - 24), (x0 + 30, y - 34)])
    S.rail(ax, x0 + 30, y - 34, "AVSS  -2.5 V", up=False)
    S.label(ax, x0 + 36, y + 30, "BAV99 (D1)\npin 3 = input\npin 2 = AVDD\npin 1 = AVSS",
            5.0, color="#4a5c68", va="center")
    # filter
    n2 = (x0 + 62, y)
    S.wire(ax, [node, n2])
    S.junction(ax, *n2)
    S.wire(ax, [n2, (x0 + 62, y - 10)])
    S.capacitor(ax, x0 + 62, y - 16, rot=90, ref="C1", val="10n C0G", lead=3.0)
    S.wire(ax, [(x0 + 62, y - 22), (x0 + 62, y - 28)])
    S.gnd(ax, x0 + 62, y - 28, "agnd", text="AGND_REF")
    S.wire(ax, [n2, (x0 + 96, y)])
    S.netlabel(ax, x0 + 96, y, "IN1  (J2.1)", direction="right")

    S.label(ax, 40, 200,
            "Corner frequency 1 / (2*pi*47k*10n) = 339 Hz.  At 100 Hz the loss is 0.36 dB, "
            "inside the +/-0.5 dB of RFQ E-10.\n"
            "Johnson noise of 47 k over 0.5-70 Hz is 0.233 uV RMS; with the ADS1299's "
            "0.14 uV that is 0.27 uV RMS total,\n"
            "against the 1.0 uV limit of E-03.  4n7 is the approved alternate if the "
            "safety review asks for a wider band.", 6.0, color="#2c3e50")

    rows = [("R1  D1  C1", "E_Fz", "IN1", "scalp Fz"), ("R2  D2  C2", "E_Cz", "IN2", "scalp Cz"),
            ("R3  D3  C3", "E_Pz", "IN3", "scalp Pz"), ("R4  D4  C4", "E_C3", "IN4", "scalp C3"),
            ("R5  D5  C5", "E_C4", "IN5", "scalp C4"), ("R6  D6  C6", "E_T7", "IN6", "scalp T7"),
            ("R7  D7  C7", "E_T8", "IN7", "scalp T8"), ("R8  D8  C8", "E_F7", "IN8", "scalp F7"),
            ("R9  D9  C9", "REF_L", "SRB1", "left ear reference"),
            ("R10 D10 C10", "REF_R", "SRB1", "right ear reference"),
            ("R11 D11 C11", "BIASOUT", "BIAS_EL", "bias drive OUT to Fpz"),
            ("R12 D12 C12", "EMGIN1", "EMG1", "EMG cheek, J15"),
            ("R13 D13 C13", "EMGIN2", "EMG2", "EMG submental, J16"),
            ("R14 D14 C14", "EMGIN3", "EMG3", "EMG laryngeal, J17"),
            ("R15 D15 C15", "EOGIN1", "SPARE1", "EOG / spare, J22.1"),
            ("R16 D16 C16", "EOGIN2", "SPARE2", "EOG / spare, J22.3")]
    ty = 176
    S.label(ax, 40, ty, "designators", 6.0, weight="bold")
    S.label(ax, 92, ty, "from (patient side)", 6.0, weight="bold")
    S.label(ax, 140, ty, "to (module side)", 6.0, weight="bold")
    S.label(ax, 186, ty, "signal", 6.0, weight="bold")
    S.wire(ax, [(38, ty - 2.6), (300, ty - 2.6)], lw=0.8)
    for i, (r, a, b, c) in enumerate(rows):
        yy = ty - 7 - i * 6.2
        S.label(ax, 40, yy, r, 5.6)
        S.label(ax, 92, yy, a, 5.6)
        S.label(ax, 140, yy, b, 5.6)
        S.label(ax, 186, yy, c, 5.6, color="#4a5c68")
    S.label(ax, 40, 60,
            "R11 runs the other way: BIASOUT leaves ADS1299 module #1 at J2.10, passes "
            "through R11 and reaches the Fpz\nbias electrode at J14.11.  It is a driven "
            "common-mode return, not an earth.  D11 and C11 sit on the electrode side.",
            6.0, color="#2c3e50")
    # This note used to read "every conductor that can reach a person passes through
    # exactly one 47 k resistor and one clamp" -- two sentences after saying D11 and C11
    # sit on the electrode side, which is the one case where that is not true.
    S.label(ax, 40, 44, "SAFETY: on channels 1-10 and 12-16 the 47 k resistor stands "
                        "between the person and the clamp.\nCHANNEL 11 IS THE EXCEPTION: "
                        "D11 and C11 are on BIAS_EL, the patient side of R11, so a shorted "
                        "D11\nor C11 is not limited by it.  See RISK-EEG-011 SF-1a, SF-6a "
                        "and SR-12; patient auxiliary\ncurrent is budgeted in "
                        "RISK-EEG-011 section 4.", 6.2, color="#c0392b")
    _finish(pdf, png_dir, fig, "sheet2_protection")


# --------------------------------------------------------------------------- sheet 3
def sheet_envelope(pdf, png_dir):
    fig, ax = S.sheet(W, H, "EEG-CAR-01 -- envelope detector (one of three)",
                      "Precision full-wave rectifier, 50 Hz Butterworth low-pass, "
                      "scaled buffer", "3 of 8", REV, DATE)
    y = 215
    S.netlabel(ax, 26, y, "HP_TAP", direction="right")
    S.wire(ax, [(42, y), (48, y)])
    ca, cb = S.capacitor(ax, 54, y, ref="C20", val="1u", lead=4.0)
    S.wire(ax, [(48, y), ca])
    nAC = (68, y)
    S.wire(ax, [cb, nAC])
    S.junction(ax, *nAC)
    ra, rb = S.resistor(ax, 82, y, 12, 4.0, ref="R20", val="10k")
    S.wire(ax, [nAC, ra])
    nINM = (100, y)
    S.wire(ax, [rb, nINM])
    S.junction(ax, *nINM)
    it, ib, out, _, _ = S.opamp(ax, 122, y - 4, 13, 12, "U1A", "OPA4376 1/4")
    S.wire(ax, [nINM, (nINM[0], it[1]), it])
    S.gnd(ax, ib[0] - 4, ib[1], "agnd", text="AGND_REF")
    S.wire(ax, [(ib[0] - 4, ib[1]), ib])
    # rectifier diodes: BAT54S pin3 at the output
    S.wire(ax, [out, (out[0] + 6, out[1])])
    S.junction(ax, out[0] + 6, out[1])
    S.diode(ax, out[0] + 6, out[1] + 14, 2.6, rot=90, ref="D20 (2)", schottky=True, lead=4.0)
    S.wire(ax, [(out[0] + 6, out[1]), (out[0] + 6, out[1] + 9.7)])
    S.wire(ax, [(out[0] + 6, out[1] + 18.3), (out[0] + 6, out[1] + 24), (nINM[0], out[1] + 24),
                nINM])
    S.diode(ax, out[0] + 6, out[1] - 14, 2.6, rot=270, ref="D20 (1)", schottky=True, lead=4.0)
    S.wire(ax, [(out[0] + 6, out[1]), (out[0] + 6, out[1] - 9.7)])
    nHW = (out[0] + 6, out[1] - 26)
    S.wire(ax, [(out[0] + 6, out[1] - 18.3), nHW])
    S.junction(ax, *nHW)
    S.label(ax, out[0] + 12, out[1] - 26, "ENV1_HW  = -Vin for Vin > 0, 0 otherwise",
            5.4, color="#4a5c68")
    # feedback resistor HW -> INM
    ra2, rb2 = S.resistor(ax, 100, y - 44, 12, 4.0, ref="R21", val="10k")
    S.wire(ax, [nHW, (nHW[0], y - 44), rb2])
    S.wire(ax, [ra2, (86, y - 44), (86, y - 12), (nINM[0] - 0.0, y - 12), nINM])

    # summing stage
    y2 = 150
    ra3, rb3 = S.resistor(ax, 178, y2 + 10, 12, 4.0, ref="R22", val="4k99")
    S.wire(ax, [nHW, (162, nHW[1]), (162, y2 + 10), ra3])
    ra4, rb4 = S.resistor(ax, 178, y2 - 6, 12, 4.0, ref="R23", val="10k")
    S.wire(ax, [nAC, (nAC[0], y2 - 6 - 40), (162, y2 - 46), (162, y2 - 6), ra4])
    nSUM = (198, y2 + 2)
    S.wire(ax, [rb3, (198, y2 + 10), nSUM])
    S.wire(ax, [rb4, (198, y2 - 6), nSUM])
    S.junction(ax, *nSUM)
    it2, ib2, out2, _, _ = S.opamp(ax, 222, y2 - 2, 13, 12, "U1B", "absolute value")
    S.wire(ax, [nSUM, (nSUM[0], it2[1]), it2])
    S.gnd(ax, ib2[0] - 4, ib2[1], "agnd", text="AGND_REF")
    S.wire(ax, [(ib2[0] - 4, ib2[1]), ib2])
    ra5, rb5 = S.resistor(ax, 222, y2 + 22, 12, 4.0, ref="R24", val="10k")
    S.wire(ax, [nSUM, (nSUM[0], y2 + 22), ra5])
    nABS = (out2[0] + 4, out2[1])
    S.wire(ax, [rb5, (240, y2 + 22), (240, out2[1]), nABS])
    S.wire(ax, [out2, nABS])
    S.junction(ax, *nABS)
    S.label(ax, nABS[0] + 2, nABS[1] + 6, "ENV1_ABS = |Vin|", 5.4, color="#4a5c68")

    # Sallen-Key
    y3 = 92
    ra6, rb6 = S.resistor(ax, 60, y3, 12, 4.0, ref="R25", val="22k")
    S.wire(ax, [nABS, (nABS[0], 118), (44, 118), (44, y3), ra6])
    nMID = (78, y3)
    S.wire(ax, [rb6, nMID])
    S.junction(ax, *nMID)
    ra7, rb7 = S.resistor(ax, 94, y3, 12, 4.0, ref="R26", val="22k")
    S.wire(ax, [nMID, ra7])
    nINP = (112, y3)
    S.wire(ax, [rb7, nINP])
    S.junction(ax, *nINP)
    S.wire(ax, [nINP, (112, y3 - 10)])
    S.capacitor(ax, 112, y3 - 16, rot=90, ref="", val="", lead=3.0)
    S.label(ax, 116, y3 - 16, "C21  100n C0G", 5.0, color="#4a5c68")
    S.wire(ax, [(112, y3 - 22), (112, y3 - 28)])
    S.gnd(ax, 112, y3 - 28, "agnd", text="AGND_REF")
    it3, ib3, out3, _, _ = S.opamp(ax, 140, y3 - 4, 13, 12, "U1C", "Sallen-Key, Q = 0.74",
                                   inv_top=False)
    S.wire(ax, [nINP, (nINP[0], it3[1]), it3])
    nFLT = (out3[0] + 6, out3[1])
    S.wire(ax, [out3, nFLT])
    S.junction(ax, *nFLT)
    S.wire(ax, [ib3, (ib3[0] - 6, ib3[1]), (ib3[0] - 6, out3[1] - 22), (nFLT[0], out3[1] - 22),
                nFLT])
    S.capacitor(ax, 100, y3 + 20, ref="C22", val="220n", lead=4.0)
    S.wire(ax, [nMID, (78, y3 + 20), (92, y3 + 20)])
    S.wire(ax, [(108, y3 + 20), (nFLT[0], y3 + 20), nFLT])
    S.label(ax, 44, 66, "f0 = 1 / (2*pi*22k*sqrt(100n*220n)) = 48.8 Hz,  Q = 0.5*sqrt(220/100)"
                        " = 0.74  ->  -3 dB at 50 Hz, inside E-11's +/-10 %.",
            5.8, color="#2c3e50")

    # output divider and buffer
    ra8, rb8 = S.resistor(ax, 208, y3, 12, 4.0, ref="R27", val="22k")
    S.wire(ax, [nFLT, (190, y3), ra8])
    nDIV = (226, y3)
    S.wire(ax, [rb8, nDIV])
    S.junction(ax, *nDIV)
    S.wire(ax, [nDIV, (226, y3 - 10)])
    S.resistor(ax, 226, y3 - 18, 10, 4.0, rot=90, ref="", val="")
    S.label(ax, 230, y3 - 18, "R28  2k2", 5.0, color="#4a5c68")
    S.wire(ax, [(226, y3 - 23), (226, y3 - 30)])
    S.gnd(ax, 226, y3 - 30, "agnd", text="AGND_REF")
    it4, ib4, out4, _, _ = S.opamp(ax, 258, y3 - 4, 13, 12, "U1D", "x1 buffer", inv_top=False)
    S.wire(ax, [nDIV, (nDIV[0], it4[1]), it4])
    S.wire(ax, [ib4, (ib4[0] - 6, ib4[1]), (ib4[0] - 6, out4[1] - 20),
                (out4[0] + 6, out4[1] - 20), (out4[0] + 6, out4[1]), out4])
    S.wire(ax, [out4, (out4[0] + 14, out4[1])])
    S.netlabel(ax, out4[0] + 14, out4[1], "ENV_STIM -> J4.4", direction="right")
    S.label(ax, 196, 66, "divider 2k2/(22k+2k2) = 0.0909; a 1.1 V peak envelope becomes "
                         "100 mV at the ADS1299 input at gain 1.", 5.8, color="#2c3e50")

    S.label(ax, 300, 210, "CHANNELS", 6.6, weight="bold")
    for i, (ch, src, out_, refs) in enumerate([
            ("1  stimulus", "HP_TAP (J8.10)", "ENV_STIM -> J4.4", "U1, D20, C20-C24, R20-R28"),
            ("2  voice", "VOICE_PRE (J21.3)", "ENV_VOICE -> J4.5", "U2, D40, C40-C44, R40-R48"),
            ("3  room", "ROOM_PRE (J28.3)", "ENV_ROOM -> J4.6", "U3, D60, C60-C64, R60-R68")]):
        yy = 200 - i * 24
        S.label(ax, 300, yy, ch, 6.0, weight="bold")
        S.label(ax, 300, yy - 5, f"in  {src}", 5.4)
        S.label(ax, 300, yy - 9.5, f"out {out_}", 5.4)
        S.label(ax, 300, yy - 14, refs, 5.2, color="#4a5c68")
    S.label(ax, 300, 122, "Each OPA4376 gets 100 n on AVDD (C23/C43/C63) and\n"
                          "100 n on AVSS (C24/C44/C64), within 3 mm of pins 4 and 11.",
            5.4, color="#4a5c68")
    S.label(ax, 300, 100, "ECO-EEG-004: in Rev A the second amplifier of the dual\n"
                          "OPA2376 had its inverting input unconnected and its\n"
                          "non-inverting input tied to AGND_REF, so the filter was\n"
                          "not in circuit at all.  Rev B uses a quad and closes both\n"
                          "loops.  ECO-EEG-005 corrects the BAT54S orientation:\n"
                          "pin 3 is the op-amp output, not the rectified node.",
            5.4, color="#c0392b")
    _finish(pdf, png_dir, fig, "sheet3_envelope")


# --------------------------------------------------------------------------- sheet 4
def sheet_rails(pdf, png_dir):
    fig, ax = S.sheet(W, H, "EEG-CAR-01 -- analogue rails, star grounds and the "
                            "stimulus comparator",
                      "Where the analogue reference is made, and the one place it meets "
                      "digital ground", "4 of 8", REV, DATE)
    S.block(ax, 30, 200, 90, 56, "ADS1299 MODULE #1",
            ["generates AVDD = +2.5 V", "and AVSS = -2.5 V", "brought out on J23"],
            fc="#e8f1ea")
    pins = S.connector(ax, 140, 250, ["AVDD", "AVSS", "BIASIN", "AGND_REF", "AVDD", "AVSS"],
                       "J23", "module #1 analogue rails", pitch=7)
    S.wire(ax, [(120, 236), (134, 236)])
    for i, (nm, col) in enumerate([("AVDD", "#c0392b"), ("AVSS", "#1f6fb2")]):
        S.wire(ax, [pins[i], (pins[i][0] + 20, pins[i][1])])
        S.netlabel(ax, pins[i][0] + 20, pins[i][1], nm)
    S.wire(ax, [pins[2], (pins[2][0] + 20, pins[2][1])])
    S.netlabel(ax, pins[2][0] + 20, pins[2][1], "BIASIN -> J29.3")
    S.gnd(ax, pins[3][0] + 8, pins[3][1], "agnd", text="AGND_REF pour")
    S.wire(ax, [pins[3], (pins[3][0] + 8, pins[3][1])])

    y = 190
    for ref, val, net, dy in (("C100", "10u", "AVDD", 0), ("C102", "100n C0G", "AVDD", -16),
                              ("C101", "10u", "AVSS", -32), ("C103", "100n C0G", "AVSS", -48)):
        S.rail(ax, 60, y + dy + 6, net, color="#c0392b" if net == "AVDD" else "#1f6fb2")
        S.wire(ax, [(60, y + dy + 6), (60, y + dy)])
        S.capacitor(ax, 60, y + dy - 6, rot=90, ref=ref, val=val, lead=3.0)
        S.wire(ax, [(60, y + dy - 12), (60, y + dy - 16)])
        S.gnd(ax, 60, y + dy - 16, "agnd")

    S.label(ax, 150, 190, "MODULE #2 RAIL LINKS", 6.4, weight="bold")
    S.resistor(ax, 180, 180, 12, 4.0, ref="R92", val="0R")
    S.netlabel(ax, 150, 180, "AVDD2", "right")
    S.netlabel(ax, 196, 180, "AVDD", "right")
    S.resistor(ax, 180, 166, 12, 4.0, ref="R93", val="0R")
    S.netlabel(ax, 150, 166, "AVSS2", "right")
    S.netlabel(ax, 196, 166, "AVSS", "right")
    S.label(ax, 150, 154, "Fitted by default.  Remove BOTH if ADS1299 module #2 regulates\n"
                          "its own analogue rails, so two regulators are never paralleled.\n"
                          "ICD-EEG-006 section 4 tells the builder how to decide.",
            5.4, color="#4a5c68")

    S.label(ax, 30, 118, "THE SINGLE STAR POINT", 7.0, weight="bold", color="#c0392b")
    S.gnd(ax, 50, 100, "agnd", text="AGND_REF")
    S.wire(ax, [(50, 100), (50, 108), (66, 108)])
    S.resistor(ax, 78, 108, 14, 4.4, ref="R90", val="0R")
    S.wire(ax, [(85, 108), (100, 108), (100, 100)])
    S.gnd(ax, 100, 100, "earth", text="DGND")
    S.label(ax, 30, 86, "R90 is the ONLY connection between the analogue reference and\n"
                        "digital ground.  It is a 0 ohm 0603 part, not a copper bridge,\n"
                        "so it can be lifted for a leakage measurement and refitted.",
            5.6, color="#2c3e50")
    S.gnd(ax, 150, 100, "agnd", text="HARN_SHIELD")
    S.wire(ax, [(150, 100), (150, 108), (166, 108)])
    S.resistor(ax, 178, 108, 14, 4.4, ref="R91", val="0R")
    S.wire(ax, [(185, 108), (200, 108), (200, 100)])
    S.gnd(ax, 200, 100, "earth", text="DGND")
    S.label(ax, 150, 86, "R91 grounds the helmet cable screen at the pod end only, so the\n"
                         "screen carries no loop current.  The far end of the screen is\n"
                         "left open at the electrode assemblies (WH-EEG-008 section 3).",
            5.6, color="#2c3e50")

    S.label(ax, 250, 190, "STIMULUS COMPARATOR (RFQ E-12)", 6.6, weight="bold")
    it, ib, out, _, _ = S.opamp(ax, 300, 160, 13, 12, "U7", "TLV3201", inv_top=True,
                                comparator=True)
    S.netlabel(ax, 260, it[1] + 0, "ENV_THR", "right")
    S.wire(ax, [(276, it[1]), it])
    S.netlabel(ax, 260, ib[1], "ENV_STIM", "right")
    S.wire(ax, [(276, ib[1]), ib])
    S.wire(ax, [out, (out[0] + 8, out[1])])
    S.junction(ax, out[0] + 8, out[1])
    S.resistor(ax, out[0] + 20, out[1], 12, 4.0, ref="R83", val="10k")
    nC = (out[0] + 34, out[1])
    S.wire(ax, [(out[0] + 26, out[1]), nC])
    S.junction(ax, *nC)
    S.netlabel(ax, nC[0], nC[1], "ENV_CMP -> J6.13", "right")
    S.wire(ax, [nC, (nC[0], nC[1] - 12)])
    S.diode(ax, nC[0], nC[1] - 18, 2.4, rot=270, ref="D23b", lead=3.0)
    S.gnd(ax, nC[0], nC[1] - 26, "earth", text="DGND")
    S.wire(ax, [nC, (nC[0], nC[1] + 12)])
    S.diode(ax, nC[0], nC[1] + 18, 2.4, rot=90, ref="D23a", lead=3.0)
    S.rail(ax, nC[0], nC[1] + 24, "DVDD3V3")
    S.resistor(ax, out[0] + 20, out[1] + 22, 12, 4.0, ref="R82", val="1M")
    S.wire(ax, [(out[0] + 8, out[1]), (out[0] + 8, out[1] + 22), (out[0] + 14, out[1] + 22)])
    S.wire(ax, [(out[0] + 26, out[1] + 22), (out[0] + 44, out[1] + 22),
                (out[0] + 44, ib[1] - 26), (272, ib[1] - 26), (272, ib[1]), (276, ib[1])])
    S.rail(ax, 268, 200, "AVDD")
    S.wire(ax, [(268, 200), (268, 196)])
    S.resistor(ax, 268, 188, 10, 4.0, rot=90, ref="R80", val="470k")
    nT = (268, 178)
    S.wire(ax, [(268, 183), nT])
    S.junction(ax, *nT)
    S.wire(ax, [nT, (276, 178), (276, it[1])])
    S.resistor(ax, 268, 170, 10, 4.0, rot=90, ref="R81", val="10k")
    S.wire(ax, [(268, 165), (268, 158)])
    S.gnd(ax, 268, 158, "agnd", text="AGND_REF")
    S.label(ax, 250, 130, "Threshold = 2.5 V x 10k / 480k = 52 mV, about half of the "
                          "100 mV full-scale\nenvelope.  R82 gives roughly 5 mV of "
                          "hysteresis.  R83 and the D23 clamp keep\nthe +/-2.5 V "
                          "comparator swing out of the 3.3 V GPIO.  The firmware latches\n"
                          "ENV_CMP in the DRDY interrupt, which is what makes it a "
                          "sub-sample onset flag.", 5.6, color="#2c3e50")
    S.label(ax, 30, 58, "AGND_REF IS NOT GROUND.  With AVDD = +2.5 V and AVSS = -2.5 V, "
                        "AGND_REF is the analogue mid-rail and the\nreference every "
                        "electrode, clamp and op-amp input is measured against.  "
                        "It is poured on both layers over the\nwhole analogue zone and "
                        "is the guard either side of every input trace.", 6.2,
            color="#c0392b")
    _finish(pdf, png_dir, fig, "sheet4_rails")


# --------------------------------------------------------------------------- sheet 5-8
def _conn_table(ax, x, y, ref, title, pins, pitch=5.2, width=64):
    n = len(pins)
    h = pitch * n + 8
    S.wire(ax, [(x, y), (x + width, y), (x + width, y - h), (x, y - h), (x, y)], lw=0.9)
    S.wire(ax, [(x, y - 7), (x + width, y - 7)], lw=0.7)
    S.label(ax, x + 2, y - 3.5, ref, 6.6, weight="bold", va="center")
    S.label(ax, x + 13, y - 3.5, title, 5.0, va="center", color="#4a5c68")
    for i, p in enumerate(pins):
        yy = y - 11 - i * pitch
        S.label(ax, x + 2, yy, f"{i+1}", 4.8, color="#4a5c68")
        S.label(ax, x + 9, yy, p, 5.2)
    return h


def sheet_connectors(pdf, png_dir, page, groups, sheet_no, title, note=""):
    fig, ax = S.sheet(W, H, title, "Pin-by-pin assignment, generated from the netlist",
                      sheet_no, REV, DATE)
    x, y = 20, 262
    colw = 72
    for ref, ttl, pins in groups:
        h = _conn_table(ax, x, y, ref, ttl, pins)
        y -= h + 8
        if y < 44:
            x += colw
            y = 262
    if note:
        S.label(ax, 20, 26, note, 5.8, color="#2c3e50")
    _finish(pdf, png_dir, fig, f"sheet{page}_connectors")


def _pins_of(ref, n):
    return [D.N.get(f"{ref}.{i}", "-") for i in range(1, n + 1)]


def sheet_power(pdf, png_dir):
    fig, ax = S.sheet(W, H, "EEG-CAR-01 -- power tree and the charge interlock",
                      "Battery only while recording; charging is inhibited in hardware",
                      "7 of 8", REV, DATE)
    S.block(ax, 24, 200, 62, 40, "18650 CELL", ["protected, >= 3000 mAh",
                                                "UN 38.3 report on file", "J13"],
            fc="#fff6e0")
    S.block(ax, 108, 196, 74, 52, "bq24074 MODULE",
            ["charger + power path", "CE from GPIO47", "thermal regulation",
             "J12"], fc="#fff6e0")
    S.block(ax, 204, 196, 70, 52, "TPS63020 MODULE",
            ["buck-boost 3.0-4.2 V in", "5.00 V +/- 2 % out, 1 A", "EN pulled to VSYS by R86",
             "J25"], fc="#fff6e0")
    S.block(ax, 296, 214, 84, 34, "ESP32-S3-DevKitC-1",
            ["5 V in at J6.21, on-board", "LDO makes DVDD3V3"], fc="#e6eef6")
    S.block(ax, 296, 168, 84, 34, "ADS1299 MODULES",
            ["5 V in at J1.11 and J3.11", "own regulators make", "AVDD / AVSS"],
            fc="#e8f1ea")
    S.block(ax, 24, 128, 62, 40, "PANEL USB-C", ["CHARGE ONLY", "no data conductor",
                                                 "J24 pigtail"], fc="#fdeaea")
    for a, b in [((86, 220), (108, 220)), ((182, 222), (204, 222)),
                 ((274, 230), (296, 230)), ((274, 210), (296, 185))]:
        S.wire(ax, [a, b], lw=1.1)
    S.wire(ax, [(86, 148), (96, 148), (96, 205), (108, 205)], lw=1.1)
    S.label(ax, 92, 226, "VBAT", 5.4, color="#4a5c68")
    S.label(ax, 186, 228, "VSYS", 5.4, color="#4a5c68")
    S.label(ax, 278, 236, "V5V", 5.4, color="#4a5c68")
    S.label(ax, 98, 176, "VBUS_IN", 5.4, color="#4a5c68", rot=90)

    S.resistor(ax, 100, 150, 12, 4.0, ref="F1", val="PTC 1.1 A")
    S.diode(ax, 118, 140, 2.4, rot=270, ref="D24", val="PESD5V0")
    S.label(ax, 24, 108, "VBUS_DET divider R84 100k / R85 56k -> 1.79 V at GPIO46.\n"
                         "The firmware refuses CMD_START_SESSION while VBUS_DET is high,\n"
                         "and the charger enable CHG_CE is driven low for the whole of a\n"
                         "session, so charging cannot start while recording either.\n"
                         "Two independent mechanisms, one requirement: RFQ S-01.",
            6.0, color="#2c3e50")
    S.block(ax, 204, 120, 176, 56, "THE RULE THAT MATTERS",
            ["The helmet is never worn while the charge cable is connected.",
             "The charge port is a separate receptacle from the data port, and the",
             "data port is isolated at 2.5 kV RMS by the ADuM4160 module.",
             "A CE-marked 5 V USB supply can leak up to 250 uA of touch current,",
             "which is far above the 100 uA of RFQ S-02 -- hence the interlock,",
             "the label on the pod and the line in the quick-start card."],
            fc="#fdeaea")
    rails = [("VBAT", "3.0 - 4.2 V", "cell terminal, J13.1 -> J12.1"),
             ("VSYS", "3.2 - 4.4 V", "charger power-path output, J12.7"),
             ("V5V", "5.00 V, 1 A", "buck-boost output; DevKit and both ADS modules"),
             ("DVDD3V3", "3.30 V, 0.5 A", "DevKit on-board LDO; all 3.3 V logic"),
             ("VDD_ISO", "3.30 V", "isolator device side, through ferrite L1"),
             ("AVDD", "+2.50 V", "from ADS1299 module #1, analogue only"),
             ("AVSS", "-2.50 V", "from ADS1299 module #1, analogue only"),
             ("AGND_REF", "0 V", "analogue mid-rail; joins DGND at R90 only"),
             ("DGND", "0 V", "digital return")]
    S.label(ax, 24, 92, "RAIL", 6.0, weight="bold")
    S.label(ax, 66, 92, "VALUE", 6.0, weight="bold")
    S.label(ax, 110, 92, "SOURCE", 6.0, weight="bold")
    S.wire(ax, [(22, 89), (300, 89)], lw=0.8)
    for i, (r, v, s) in enumerate(rails):
        yy = 84 - i * 6.0
        S.label(ax, 24, yy, r, 5.6)
        S.label(ax, 66, yy, v, 5.6)
        S.label(ax, 110, yy, s, 5.6, color="#4a5c68")
    S.label(ax, 24, 22, "ECO-EEG-002: Rev A had no source for DVDD3V3 at all -- the "
                        "charger's SYS output, the DevKit's 5 V pin and the ADS module\n"
                        "supplies were all unconnected nets.  The board could not have "
                        "powered up.  Rev B adds J25, F1, D24, R84-R86 and C70-C74.",
            5.8, color="#c0392b")
    _finish(pdf, png_dir, fig, "sheet7_power")


def sheet_lights(pdf, png_dir):
    fig, ax = S.sheet(W, H, "EEG-CAR-01 -- contact lights",
                      "Eight two-lead bicolour LEDs on eight lines and one phase common",
                      "8 of 8", REV, DATE)
    pins = S.connector(ax, 40, 264, _pins_of("J19", 16), "J19",
                       "74HC595 shift-register module", pitch=6.4, width=34)
    for i in range(8):
        p = pins[7 + i]
        S.wire(ax, [p, (p[0] + 10, p[1])])
        ra, rb = S.resistor(ax, p[0] + 22, p[1], 12, 3.6, ref=f"R{70+i}",
                            val="1k" if i == 0 else "")
        S.wire(ax, [(p[0] + 10, p[1]), ra])
        S.wire(ax, [rb, (p[0] + 44, p[1])])
        S.netlabel(ax, p[0] + 44, p[1], f"LED{i+1} -> J30.{i+1}")
    S.wire(ax, [pins[5], (pins[5][0] + 10, pins[5][1]), (pins[5][0] + 10, pins[5][1] - 6)])
    S.gnd(ax, pins[5][0] + 10, pins[5][1] - 6, "earth", text="R87 0R to DGND")
    S.wire(ax, [pins[6], (pins[6][0] + 10, pins[6][1])])
    S.label(ax, pins[6][0] + 12, pins[6][1], "R88 10k to DVDD3V3, C88 100n to DGND "
                                             "(power-on reset)", 5.0, color="#4a5c68")

    S.block(ax, 236, 196, 150, 66, "HOW THREE COLOURS COME OUT OF EIGHT LINES",
            ["Each site carries one two-lead bicolour LED: red and green dice in",
             "inverse parallel between its LEDn line and the LED_V common.",
             "Phase A: LED_V driven high, Qn low  ->  that site shows green.",
             "Phase B: LED_V driven low,  Qn high ->  that site shows red.",
             "Alternating the two phases above 100 Hz shows amber.",
             "A site that is off in both phases is dark.  All eight are",
             "independent, and no extra conductor is needed."], fc="#eef3f7")
    S.block(ax, 236, 120, 150, 64, "DARK AT BOOT, DARK WHILE RECORDING",
            ["LED_V is GPIO48.  At reset it is an input, so it floats and no",
             "current can flow through any LED whatever the shift register",
             "happens to contain.  That is the power-on guarantee.",
             "During a recording block the firmware holds LED_V low and clears",
             "the register (RFQ E-27), so nothing on the head can be watched",
             "or reacted to while data is being taken."], fc="#eef3f7")
    S.block(ax, 236, 44, 150, 64, "WHAT THE LIGHTS MEAN",
            ["green   below 10 kohm      ready, do nothing",
             "amber   10 - 20 kohm       add gel through that site's port",
             "red     above 20 kohm      slide the assembly a few mm, then gel",
             "pulse   measurement running, keep still",
             "off     recording, or the instrument is not powered",
             "Driven from the ADS1299's own lead-off measurement, so the head",
             "and the screen can never disagree."], fc="#eef3f7")
    S.label(ax, 40, 40, "ECO-EEG-001: in Rev A the eight LEDn nets existed on the harness "
                        "connector with nothing driving them -- the 74HC595 module's\n"
                        "outputs were not brought to the carrier at all, so the contact "
                        "lights could not work.  Rev B widens J19 to 1x16, adds R70-R77\n"
                        "and defines the phase scheme above.  ECO-EEG-014 moves the light "
                        "lines out of the electrode harness into their own cable (J30).",
            5.8, color="#c0392b")
    _finish(pdf, png_dir, fig, "sheet8_lights")


def _finish(pdf, png_dir, fig, name):
    fig.tight_layout(pad=0.2)
    pdf.savefig(fig)
    if png_dir:
        fig.savefig(os.path.join(png_dir, name + ".png"), dpi=150)
    plt.close(fig)


def build(out_pdf, png_dir=None):
    if png_dir:
        os.makedirs(png_dir, exist_ok=True)
    with PdfPages(out_pdf) as pdf:
        sheet_block(pdf, png_dir)
        sheet_protection(pdf, png_dir)
        sheet_envelope(pdf, png_dir)
        sheet_rails(pdf, png_dir)
        sheet_connectors(pdf, png_dir, 5, [
            ("J1", "ADS1299 module #1 digital", _pins_of("J1", 12)),
            ("J2", "ADS1299 module #1 analogue signals", _pins_of("J2", 10)),
            ("J23", "ADS1299 module #1 analogue rails", _pins_of("J23", 6)),
            ("J3", "ADS1299 module #2 digital", _pins_of("J3", 12)),
            ("J4", "ADS1299 module #2 analogue signals", _pins_of("J4", 10)),
            ("J29", "ADS1299 module #2 analogue rails", _pins_of("J29", 6)),
            ("J5", "DAISY / clock stub", _pins_of("J5", 4)),
            ("J14", "helmet harness, electrodes", _pins_of("J14", 12)),
            ("J30", "helmet harness, contact lights", _pins_of("J30", 10)),
            ("J22", "EOG / spare header", _pins_of("J22", 3)),
        ], "5 of 8", "EEG-CAR-01 -- analogue and module connectors",
            "Module connectors are NOT direct plug-in sockets. The purchased modules sit on "
            "the printed module plate MP-01 above the carrier and are joined with keyed "
            "2.54 mm ribbon jumpers per ICD-EEG-006.\n"
            "The one exception is the ESP32-S3-DevKitC-1, which is inserted directly into "
            "J6 and J7 (row spacing 22.86 mm).")
        sheet_connectors(pdf, png_dir, 6, [
            ("J6", "ESP32-S3-DevKitC-1 row A", _pins_of("J6", 22)),
            ("J7", "ESP32-S3-DevKitC-1 row B", _pins_of("J7", 22)),
            ("J8", "ES8388 codec module", _pins_of("J8", 14)),
            ("J9", "codec microphone feeds", _pins_of("J9", 4)),
            ("J10", "ADuM4160 isolator, device side", _pins_of("J10", 4)),
            ("J11", "ATECC608B breakout", _pins_of("J11", 4)),
            ("J12", "charger + gauge module", _pins_of("J12", 8)),
            ("J20", "microSD breakout", _pins_of("J20", 8)),
            ("J21", "boom preamp (part open, E-14)", _pins_of("J21", 6)),
            ("J18", "boom microphone pigtail", _pins_of("J18", 4)),
            ("J28", "room microphone module", _pins_of("J28", 4)),
            ("J27", "headphone jack pigtail", _pins_of("J27", 4)),
            ("J25", "buck-boost module", _pins_of("J25", 6)),
            ("J26", "debug / programming", _pins_of("J26", 6)),
            ("J24", "charge input pigtail", _pins_of("J24", 2)),
            ("J13", "battery", _pins_of("J13", 2)),
        ], "6 of 8", "EEG-CAR-01 -- digital and power connectors",
            "J7 positions 11, 12 and 13 are GPIO37, 36 and 35. They carry the octal PSRAM "
            "on the -N16R8 variant and MUST be left unconnected; position 15 is GPIO45, the "
            "VDD_SPI strapping pin, also open.\n"
            "The microSD interface is one-bit SDMMC. 70 kB/s is needed and about 2 MB/s is "
            "available; the three data lines that four-bit mode would have used are spent "
            "on the contact-light shift register instead.")
        sheet_power(pdf, png_dir)
        sheet_lights(pdf, png_dir)
    return out_pdf


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "SCH-EEG-005_RevB_schematic_set.pdf"
    png = sys.argv[2] if len(sys.argv) > 2 else None
    print(build(out, png))
