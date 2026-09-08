#!/usr/bin/env python3
"""
emit_kicad_sch.py -- the native KiCad schematic for EEG-CAR-01 Rev C.

Finding 7 of ECO-EEG-030 is that no native schematic exists: `schematic/SCH-EEG-005_
RevB_schematic_set.pdf` is eight matplotlib drawings and carries no netlist, so no
reviewer can import it, check it, or route from it.  This module is the answer.  It
writes a hierarchical set --

    kicad/EEG-CAR-01_RevC.kicad_sch                 root: block diagram
    kicad/EEG-CAR-01_RevC_10_power.kicad_sch        charger, gauge, cell, buck-boost
    kicad/EEG-CAR-01_RevC_20_isolation_usb.kicad_sch  isolator module interface
    kicad/EEG-CAR-01_RevC_30_controller.kicad_sch   DevKit, storage, secure element
    kicad/EEG-CAR-01_RevC_40_afe_1.kicad_sch        ADS1299 module 1
    kicad/EEG-CAR-01_RevC_41_afe_2.kicad_sch        ADS1299 module 2
    kicad/EEG-CAR-01_RevC_50_harness_input.kicad_sch  harness and 16 protection networks
    kicad/EEG-CAR-01_RevC_60_audio.kicad_sch        codec, envelopes, comparator
    kicad/EEG-CAR-01_RevC_70_contact_lights.kicad_sch  74HC595 and the light harness
    kicad/EEG-CAR-01_RevC_80_star_points_test.kicad_sch  R90, TP1-TP18, mechanical

-- from the same `design.py` data the eight-sheet PDF is drawn from, so the two cannot
drift apart.

**How connectivity is expressed, and why.**  Power and ground nets use power symbols and
are global; nothing else about them appears on the root.  Every OTHER net that has pads
on more than one sheet becomes a hierarchical label on each sheet that uses it and a
sheet pin on the root, joined on the root by a local label of the same name.  Nets whose
pads all sit on one sheet are drawn with wires and local labels and never leave it.

**Every symbol is placed at rotation 0.**  See tools/schlib.py for why.

The gate on this file is not that it looks right.  It is `tools/sch_netlist.py`, which
reads the emitted files back -- wires, junctions, labels, power symbols and pin
positions computed from the embedded `lib_symbols` -- and diffs the netlist it finds
against `design.py`.  Zero differences, or this is not done.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import schlib               # noqa: E402
from kicad_sch import Sheet, balanced   # noqa: E402

KDIR = os.path.join(PKG, "kicad")
COMPANY = "TI One Voice research programme"
GRID = 1.27

POWER_NETS = set(D.POWER_A_NETS) | set(D.POWER_D_NETS) | {"HARN_SHIELD"}

# --------------------------------------------------------------------------- sheets
PAPER_OF = {"60_audio": "A1"}          # everything else fits A2

SHEETS = [
    ("10_power", "10 power", "Charger, fuel gauge, cell, buck-boost and the rails",
     ["J12", "J13", "J24", "J25", "F1", "D24", "R84", "R85", "R86",
      "C70", "C71", "C72", "C73", "C74"]),
    ("20_isolation_usb", "20 isolation and USB",
     "USB isolator module interface -- the barrier is ON THE MODULE",
     ["J10", "L1", "C87", "C89"]),
    ("30_controller", "30 controller",
     "ESP32-S3-DevKitC-1-N16R8, storage, secure element, debug and the buttons",
     ["J6", "J7", "J11", "J20", "J26", "SW1", "SW2", "SW3",
      "R50", "R51", "R52", "C50", "C51", "C52", "R94", "R95", "C83", "C85"]),
    ("40_afe_1", "40 AFE 1", "ADS1299 module 1: digital, analogue signals, analogue rails",
     ["J1", "J2", "J23", "J5", "C80", "C100", "C101", "C102", "C103", "R92", "R93"]),
    ("41_afe_2", "41 AFE 2", "ADS1299 module 2: digital, analogue signals, analogue rails",
     ["J3", "J4", "J29", "C81"]),
    ("50_harness_input", "50 harness and protection",
     "The electrode harness and the sixteen protection networks",
     ["J14", "J15", "J16", "J17", "J22", "R91"]
     + [f"R{i}" for i in range(1, 17)]
     + [f"D{i}" for i in range(1, 17)]
     + [f"C{i}" for i in range(1, 17)]),
    ("60_audio", "60 audio and envelopes",
     "Codec, microphones, headphone tap, three envelope detectors and the comparator",
     ["J8", "J9", "J18", "J21", "J27", "J28", "C82", "C86", "C90", "R89",
      "U1", "U2", "U3", "U7", "R80", "R81", "R82", "R83", "D23"]
     + [f"C{b + k}" for b in (20, 40, 60) for k in (0, 1, 2, 3, 4)]
     + [f"R{b + k}" for b in (20, 40, 60) for k in range(9)]
     + ["D20", "D40", "D60"]),
    ("70_contact_lights", "70 contact lights",
     "74HC595 shift-register module and the ten-way light harness",
     [f"R{i}" for i in range(70, 80)] + ["R87", "R88", "J19", "J30", "C84", "C88"]),
    ("80_star_points_test", "80 star points and test",
     "R90, the eighteen test points and the mechanical features",
     ["R90"] + [t[0] for t in D.TESTPOINTS]
     + [f"MH{i}" for i in range(1, 5)] + [f"FID{i}" for i in range(1, 4)]),
]

SHEET_OF = {}
for _stem, _name, _title, _refs in SHEETS:
    for _r in _refs:
        assert _r not in SHEET_OF, f"{_r} is on two sheets"
        SHEET_OF[_r] = _stem


def check_assignment():
    missing = sorted(set(D.C) - set(SHEET_OF))
    extra = sorted(set(SHEET_OF) - set(D.C))
    if missing or extra:
        raise SystemExit(f"sheet assignment is not a partition of design.C:\n"
                         f"  not on any sheet: {missing}\n"
                         f"  not in design.C: {extra}")
    return len(SHEET_OF)


def inter_sheet_nets():
    """Nets with pads on more than one sheet, excluding the power nets, which are
    global through power symbols and carry no sheet pin."""
    where = {}
    for key, net in D.N.items():
        ref = key.rpartition(".")[0]
        where.setdefault(net, set()).add(SHEET_OF[ref])
    return {net: sorted(s) for net, s in where.items()
            if len(s) > 1 and net not in POWER_NETS}


# --------------------------------------------------------------------------- helpers
class Page:
    """One sheet under construction, with the placement helpers the blocks use."""

    def __init__(self, sh, lib, stem):
        self.sh = sh
        self.lib = lib
        self.stem = stem
        self.placed = set()
        self.hier = set()

    # -- primitives ----------------------------------------------------------
    def sym(self, ref, libname, x, y, unit=1, value=None, hide_value=False):
        s = self.lib[libname]
        self.sh.use(s)
        c = D.C.get(ref)
        self.sh.place(ref, libname, x, y, unit=unit,
                      value=value if value is not None else (c["val"] if c else ""),
                      footprint=("EEG-CAR-01:" + c["fp"]) if c else "",
                      extra_props=([("MPN", c["mpn"])] if c and c["mpn"] else []),
                      hide_value=hide_value, dnp=bool(c and c["dnp"]))
        self.placed.add((ref, unit))
        return s

    def pin(self, ref, libname, x, y, number, unit=1):
        return schlib.pin_xy(self.lib[libname], number, x, y, unit)

    def power(self, net, x, y):
        """A power symbol at (x, y).  Its own pin sits exactly there."""
        name = f"PWR_{net}"
        self.sh.use(self.lib[name])
        idx = len([1 for r, _ in self.placed if r.startswith("#PWR")])
        self.sh.place(f"#PWR{idx:03d}", name, x, y, value=net, hide_value=True)
        self.placed.add((f"#PWR{idx:03d}", 1))

    def net_at(self, net, x, y, rot=0, justify="left bottom"):
        """Terminate a stub: a power symbol for a rail, a hierarchical label for a net
        that leaves this sheet, a plain label otherwise."""
        if net in POWER_NETS:
            self.power(net, x, y)
        elif net in INTER:
            self.sh.hier_label(net, x, y, rot,
                               justify="right" if rot == 180 else "left")
            self.hier.add(net)
        else:
            self.sh.label(net, x, y, rot, justify=justify)

    def stub(self, net, x, y, dx=0.0, dy=0.0, rot=0):
        """A wire from (x, y) by (dx, dy), terminated by net_at."""
        if dx or dy:
            self.sh.wire(x, y, x + dx, y + dy)
        self.net_at(net, x + dx, y + dy, rot)

    # -- blocks --------------------------------------------------------------
    def connector(self, ref, x, y, side="r", stub_len=10.16):
        """A connector with a stub and a terminator on every way."""
        name = f"CONN_{ref}_{side.upper()}"
        s = self.sym(ref, name, x, y, value=D.C[ref]["val"], hide_value=True)
        pins = schlib._pins_of(ref)
        for num, net in pins.items():
            px, py = schlib.pin_xy(s, num, x, y, 1)
            dx = stub_len if side == "r" else -stub_len
            self.stub(net, px, py, dx=dx, rot=0 if side == "r" else 180)
        return s

    def decouple(self, ref, x, y, rail, gnd):
        """A capacitor standing between a rail above and a ground below."""
        s = self.sym(ref, "C_V", x, y)
        p1 = schlib.pin_xy(s, "1", x, y, 1)
        p2 = schlib.pin_xy(s, "2", x, y, 1)
        top, bot = (p1, p2) if p1[1] < p2[1] else (p2, p1)
        top_net = rail if p1[1] < p2[1] else gnd
        bot_net = gnd if p1[1] < p2[1] else rail
        self.sh.wire(top[0], top[1], top[0], top[1] - 3.81)
        self.net_at(top_net, top[0], top[1] - 3.81)
        self.sh.wire(bot[0], bot[1], bot[0], bot[1] + 3.81)
        self.net_at(bot_net, bot[0], bot[1] + 3.81)

    def series_h(self, ref, x, y, left_net, right_net, kind="R_H",
                 left_len=7.62, right_len=7.62, left_rot=180, right_rot=0):
        """A two-pin part lying horizontally, terminated at both ends."""
        s = self.sym(ref, kind, x, y)
        p1 = schlib.pin_xy(s, "1", x, y, 1)
        p2 = schlib.pin_xy(s, "2", x, y, 1)
        if left_net is not None:
            self.stub(left_net, p1[0], p1[1], dx=-left_len, rot=left_rot)
        if right_net is not None:
            self.stub(right_net, p2[0], p2[1], dx=right_len, rot=right_rot)
        return s, p1, p2

    def divider(self, top_ref, bot_ref, x, y, top_net, mid_net, bot_net, gap=20.32):
        """Two resistors in a column with the tap between them, drawn as a divider."""
        st = self.sym(top_ref, "R_V", x, y)
        sb = self.sym(bot_ref, "R_V", x, y + gap)
        t1 = schlib.pin_xy(st, "1", x, y, 1)
        t2 = schlib.pin_xy(st, "2", x, y, 1)
        b1 = schlib.pin_xy(sb, "1", x, y + gap, 1)
        b2 = schlib.pin_xy(sb, "2", x, y + gap, 1)
        top = t1 if t1[1] < t2[1] else t2
        tmid = t2 if t1[1] < t2[1] else t1
        bmid = b1 if b1[1] < b2[1] else b2
        bot = b2 if b1[1] < b2[1] else b1
        self.sh.wire(top[0], top[1], top[0], top[1] - 3.81)
        self.net_at(top_net, top[0], top[1] - 3.81)
        self.sh.wire(tmid[0], tmid[1], bmid[0], bmid[1])
        my = (tmid[1] + bmid[1]) / 2
        self.sh.wire(tmid[0], my, tmid[0] + 8.89, my)
        self.sh.junction(tmid[0], my)
        self.net_at(mid_net, tmid[0] + 8.89, my)
        self.sh.wire(bot[0], bot[1], bot[0], bot[1] + 3.81)
        self.net_at(bot_net, bot[0], bot[1] + 3.81)

    def two_pin_v(self, ref, x, y, net1, net2, kind="R_V", lead=5.08):
        """A vertical two-pin part wired BY PIN NUMBER and not by which end is higher.

        The first version of this drawing wired the pull-ups by geometry -- "the lower
        end goes to the button" -- and put pin 2 where design.py has pin 1 on all four
        of them.  A resistor is symmetric so the circuit was right and the NETLIST was
        wrong, which is exactly the class of error tools/sch_netlist.py exists to catch
        and did.
        """
        sym = self.sym(ref, kind, x, y)
        p1 = schlib.pin_xy(sym, "1", x, y, 1)
        p2 = schlib.pin_xy(sym, "2", x, y, 1)
        for (px, py), net in ((p1, net1), (p2, net2)):
            dy = -lead if py < y else lead
            self.sh.wire(px, py, px, py + dy)
            self.net_at(net, px, py + dy)
        return sym, p1, p2

    def testpoint(self, ref, net, x, y):
        s = self.sym(ref, "TESTPOINT", x, y, value=net)
        p = schlib.pin_xy(s, "1", x, y, 1)
        self.stub(net, p[0], p[1], dy=5.08)

    def title(self, s, x, y, size=2.5):
        self.sh.text(s, x, y, size)

    def note(self, s, x, y, size=1.2, width=96):
        """Notes wrap.  KiCad renders a text item as one line however long it is, so an
        unwrapped 300-character note runs off the sheet and out of the PDF."""
        import textwrap
        for i, line in enumerate(textwrap.wrap(" ".join(s.split()), width)):
            self.sh.text(line, x, y + i * (size * 1.6 + 1.2), size)


INTER = {}          # filled by main(), read by Page.net_at


# --------------------------------------------------------------------------- blocks
def sheet_power(p):
    p.title("10  POWER -- charge in, cell, power path, rails", 20, 18)
    p.note("Charge input and cell on the left; the power path and the rails to the "
           "right.  The 45 C charge inhibit of RFQ E-23 is NOT MET and cannot be: no "
           "NTC net exists (ICD-EEG-006 section 2.6).", 20, 24)
    p.connector("J24", 40, 60, "r")
    p.note("charge-only USB-C pigtail", 22, 44)
    p.series_h("F1", 90, 55, "VBUS_IN", "VBUS_CHG", kind="PTC_H")
    p.sym("D24", "D_CLAMP_V", 120, 60)
    d = p.lib["D_CLAMP_V"]
    for num, net in (("2", "DGND"), ("1", "VBUS_CHG"), ("3", "DGND")):
        px, py = schlib.pin_xy(d, num, 120, 60, 1)
        if num == "3":
            p.stub(net, px, py, dx=-7.62, rot=180)
        else:
            p.stub(net, px, py, dy=(-5.08 if num == "2" else 5.08))
    p.divider("R84", "R85", 160, 48, "VBUS_CHG", "VBUS_DET", "DGND")
    p.note("VBUS_DET divider: 100k/150k gives 3.0 V from a 5.0 V VBUS "
           "(ECO-EEG-022)", 150, 92)

    p.connector("J13", 40, 150, "r")
    p.note("protected 18650 cell", 24, 132)
    p.connector("J12", 250, 70, "l")
    p.note("charger + fuel gauge on MP-01", 240, 40)
    p.connector("J25", 250, 165, "l")
    p.note("buck-boost, 5.00 V", 240, 138)
    p.series_h("R86", 320, 165, "VSYS", "BOOST_EN")
    p.note("R86 pulls BOOST_EN to VSYS so that V5V comes up before DVDD3V3 exists "
           "(ECO-EEG-002).  Measure BOOST_EN with the module fitted: >= 1.2 V.",
           300, 178)

    for i, (ref, rail) in enumerate([("C70", "VSYS"), ("C71", "VSYS"), ("C72", "V5V"),
                                     ("C73", "V5V"), ("C74", "DVDD3V3")]):
        p.decouple(ref, 380 + i * 25.4, 240, rail, "DGND")
    p.note("bulk decoupling: VSYS at the buck-boost input, V5V at its output and "
           "feeding the DevKit and both ADS1299 modules, DVDD3V3 from the DevKit's "
           "own regulator", 370, 262)


def sheet_isolation(p):
    p.title("20  ISOLATION AND USB", 20, 18)
    p.note("The 2.5 kV barrier is ON THE ADuM4160 MODULE at J10 and not on this board. "
           "What the carrier owes it is the copper keep-out of DSN-EEG-003 section 3.3 "
           "rule 4: x >= 141.0 mm, y = 2.0 to 22.0 mm, no copper on any of the four "
           "layers.  Nothing on the carrier is on the host side.", 20, 24)
    p.connector("J10", 90, 90, "r")
    p.note("USB isolator module, device side", 70, 68)
    p.series_h("L1", 220, 60, "DVDD3V3", "VDD_ISO", kind="FB_H")
    p.note("600 R at 100 MHz, 500 mA (ECO-EEG-031)", 200, 72)
    p.decouple("C87", 210, 110, "VDD_ISO", "DGND")
    p.decouple("C89", 245, 110, "VDD_ISO", "DGND")
    p.note("device-side supply decoupling and bulk", 200, 134)
    p.sh.box(60, 40, 300, 150, "isolation")
    p.note("USB_DP and USB_DN are a 0.30 mm pair on 0.35 mm spacing on L1 over the "
           "L2 DGND plane, about 95 ohm differential.  No coupon and no impedance "
           "report are required (DSN-EEG-003 section 3.3 rule 5).", 20, 165)


def sheet_controller(p):
    p.title("30  CONTROLLER -- ESP32-S3-DevKitC-1-N16R8, storage, identity, debug",
            20, 18)
    p.note("J6 and J7 are DevKit header POSITIONS, not GPIO numbers.  GPIO35/36/37 "
           "carry the octal PSRAM on the -N16R8 and are NOT CONNECTED (J7 positions "
           "11, 12, 13); GPIO45 (J7 position 15) is the VDD_SPI strapping pin and is "
           "left open.  Row spacing is 22.86 mm.", 20, 24)
    p.connector("J6", 80, 120, "r")
    p.note("DevKit row A", 62, 55)
    p.connector("J7", 250, 120, "r")
    p.note("DevKit row B", 232, 55)

    p.connector("J20", 420, 60, "l")
    p.note("microSD, one-bit SDMMC", 400, 38)
    p.connector("J11", 420, 130, "l")
    p.note("ATECC608B secure element", 400, 112)
    p.connector("J26", 420, 200, "l")
    p.note("console and recovery header", 400, 178)

    for i, (sw, r, c, net) in enumerate([("SW1", "R50", "C50", "BTN_A"),
                                         ("SW2", "R51", "C51", "BTN_B"),
                                         ("SW3", "R52", "C52", "BTN_STOP")]):
        y = 270 + i * 38.1
        s = p.sym(sw, "SW_PUSH_H", 90, y)
        a = schlib.pin_xy(s, "1", 90, y, 1)
        b = schlib.pin_xy(s, "2", 90, y, 1)
        p.sh.wire(a[0], a[1], a[0] - 10.16, a[1])
        p.sh.junction(a[0] - 10.16, a[1])
        p.net_at(net, a[0] - 20.32, a[1], 180)
        p.sh.wire(a[0] - 20.32, a[1], a[0] - 10.16, a[1])
        p.sh.wire(b[0], b[1], b[0] + 7.62, b[1])
        p.net_at("DGND", b[0] + 7.62, b[1])
        # R.1 is the button node and R.2 is DVDD3V3, which is design.py's order and
        # not the order the geometry suggests.
        p.two_pin_v(r, a[0] - 10.16, a[1] - 20.32, net, "DVDD3V3")
        p.decouple(c, a[0] - 25.4, a[1] + 15.24, net, "DGND")
    p.note("Hardware RC debounce, R50-R52 with C50-C52, and firmware debounce on top "
           "(RFQ E-26).", 20, 262)

    p.two_pin_v("R94", 520, 280, "SDA", "DVDD3V3")
    p.two_pin_v("R95", 555, 280, "SCL", "DVDD3V3")
    p.note("R94 and R95 are the I2C pull-ups ECO-EEG-021 added: 4k7 from SDA and from "
           "SCL to DVDD3V3.  Two separate pull-ups, not a divider.", 470, 305)
    p.decouple("C83", 500, 130, "DVDD3V3", "DGND")
    p.decouple("C85", 530, 130, "DVDD3V3", "DGND")
    p.note("local decoupling at J11 and J20", 490, 152)


def sheet_afe1(p):
    p.title("40  ANALOGUE FRONT END 1 -- ADS1299 module #1", 20, 18)
    p.note("Module #1 is the clock source and generates AVDD = +2.5 V and "
           "AVSS = -2.5 V, which reach the carrier at J23.  AGND_REF is the analogue "
           "0 V mid-rail and is NOT ground.", 20, 24)
    p.connector("J1", 90, 110, "r")
    p.note("module #1, digital", 70, 55)
    p.connector("J2", 300, 100, "l")
    p.note("module #1, analogue signals", 280, 45)
    p.connector("J23", 300, 200, "l")
    p.note("module #1, analogue rails", 280, 172)
    p.connector("J5", 90, 260, "r")
    p.note("DAISY_IN / CLKOUT stub", 70, 242)

    p.decouple("C80", 420, 70, "DVDD3V3", "DGND")
    p.note("local supply decoupling at J1", 400, 92)
    for i, (ref, rail) in enumerate([("C100", "AVDD"), ("C102", "AVDD"),
                                     ("C101", "AVSS"), ("C103", "AVSS")]):
        p.decouple(ref, 420 + (i % 2) * 30.48, 160 + (i // 2) * 45.72,
                   rail, "AGND_REF")
    p.note("AVDD and AVSS bulk and high-frequency decoupling to AGND_REF", 400, 262)

    p.series_h("R92", 480, 300, "AVDD2", "AVDD")
    p.series_h("R93", 480, 320, "AVSS2", "AVSS")
    p.note("R92 and R93 are fitted by default and link module #2's analogue rails to "
           "module #1's.  REMOVE BOTH if module #2 regulates its own rails "
           "(ICD-EEG-006 section 7.1).", 420, 336)


def sheet_afe2(p):
    p.title("41  ANALOGUE FRONT END 2 -- ADS1299 module #2", 20, 18)
    p.note("Module #2 takes DAISY and the shared 2.048 MHz CLK_ADS from module #1.  "
           "Its analogue inputs are the three EMG channels, the three envelope "
           "outputs and the two spares.", 20, 24)
    p.connector("J3", 90, 110, "r")
    p.note("module #2, digital", 70, 55)
    p.connector("J4", 300, 100, "l")
    p.note("module #2, analogue signals", 280, 45)
    p.connector("J29", 300, 200, "l")
    p.note("module #2, analogue rails", 280, 172)
    p.decouple("C81", 420, 70, "DVDD3V3", "DGND")
    p.note("local supply decoupling at J3", 400, 92)
    p.note("Module #1 and module #2 are not interchangeable once fitted: label both at "
           "incoming inspection and keep the pair together (AVL-EEG-017 section 2).",
           20, 300)


def sheet_harness(p):
    p.title("50  HARNESS AND THE SIXTEEN PROTECTION NETWORKS", 20, 18)
    p.note("Every conductor that can reach a person passes through a 68 kOhm 0.1 % "
           "series resistor and a BAV99 clamp to AVDD/AVSS before it reaches a "
           "module (ECO-EEG-024).  Each network is drawn as the straight line "
           "DSN-EEG-003 section 3.3 rule 3 asks the layout to place it in: "
           "resistor, then clamp, then filter capacitor, from the harness towards "
           "the module.", 20, 24)
    p.connector("J14", 60, 120, "r")
    p.note("electrode harness, 12-way screened", 34, 52)
    p.connector("J15", 60, 250, "r")
    p.connector("J16", 60, 275, "r")
    p.connector("J17", 60, 300, "r")
    p.note("touch-proof DIN 42802 panel sockets", 34, 232)
    p.connector("J22", 60, 340, "r")
    p.note("EOG / spare header, Phase 2 option", 34, 322)

    p.series_h("R91", 60, 380, "HARN_SHIELD", "DGND")
    p.note("R91 is the ONLY HARN_SHIELD-to-DGND path (DSN-EEG-003 section 3.3 rule 2).  "
           "A 0 R 0603 part, never a copper bridge: it lifts for a leakage "
           "measurement and refits.", 20, 394)

    x0 = 200.0
    for i, (n_, src, dst, lbl) in enumerate(D.PROT):
        y = 46 + i * 21.0
        # R : source -> node
        rs = p.sym(f"R{n_}", "R_H", x0, y)
        r1 = schlib.pin_xy(rs, "1", x0, y, 1)
        r2 = schlib.pin_xy(rs, "2", x0, y, 1)
        p.stub(src, r1[0], r1[1], dx=-12.7, rot=180)
        # node between R and the clamp
        node_x = r2[0] + 25.4
        p.sh.wire(r2[0], r2[1], node_x, r2[1])
        # D : clamp to the rails, common pin 3 on the node
        ds = p.sym(f"D{n_}", "D_CLAMP_V", node_x + 12.7, y)
        d3 = schlib.pin_xy(ds, "3", node_x + 12.7, y, 1)
        d1 = schlib.pin_xy(ds, "1", node_x + 12.7, y, 1)
        d2 = schlib.pin_xy(ds, "2", node_x + 12.7, y, 1)
        p.sh.wire(node_x, r2[1], d3[0], d3[1])
        p.sh.junction(node_x, r2[1])
        p.sh.wire(d2[0], d2[1], d2[0], d2[1] - 2.54)
        p.net_at("AVDD", d2[0], d2[1] - 2.54)
        p.sh.wire(d1[0], d1[1], d1[0], d1[1] + 2.54)
        p.net_at("AVSS", d1[0], d1[1] + 2.54)
        # C : filter from the node to AGND_REF
        cx = node_x + 40.64
        cs = p.sym(f"C{n_}", "C_V", cx, y + 6.35)
        c1 = schlib.pin_xy(cs, "1", cx, y + 6.35, 1)
        c2 = schlib.pin_xy(cs, "2", cx, y + 6.35, 1)
        top, bot = (c1, c2) if c1[1] < c2[1] else (c2, c1)
        p.sh.wire(node_x, r2[1], cx, r2[1])
        p.sh.wire(cx, r2[1], top[0], top[1])
        p.sh.wire(cx, r2[1], cx + 22.86, r2[1])
        p.sh.junction(cx, r2[1])
        p.stub(dst, cx + 22.86, r2[1], dx=0)
        p.sh.wire(bot[0], bot[1], bot[0], bot[1] + 3.81)
        p.net_at("AGND_REF", bot[0], bot[1] + 3.81)
        p.note(f"{lbl}", x0 - 12.7, y - 7.0, 1.0)
    p.sh.box(180, 30, 500, 30 + 16 * 21.0 + 6, "protection")


def _env_channel(p, k, b, src, out, x0, y0):
    """One envelope channel, drawn as the signal path it is: AC couple, precision
    half-wave rectifier, absolute-value summer, 50 Hz Sallen-Key, output divider."""
    p.note(f"envelope channel {k}: {src} -> {out}", x0, y0 - 8.0, 1.4)
    # AC coupling and the rectifier input
    p.series_h(f"C{b}", x0 + 25, y0, src, f"ENV{k}_AC", kind="C_H")
    p.series_h(f"R{b}", x0 + 75, y0, f"ENV{k}_AC", f"ENV{k}_INM")
    p.series_h(f"R{b + 1}", x0 + 75, y0 + 15, f"ENV{k}_HW", f"ENV{k}_INM")
    ds = p.sym(f"D{b}", "D_SERIES_H", x0 + 140, y0 + 8)
    for num, net in (("1", f"ENV{k}_HW"), ("2", f"ENV{k}_INM"), ("3", f"ENV{k}_ROUT")):
        px, py = schlib.pin_xy(ds, num, x0 + 140, y0 + 8, 1)
        if num == "3":
            p.stub(net, px, py, dy=6.35)
        else:
            p.stub(net, px, py, dx=(-6.35 if num == "1" else 6.35),
                   rot=180 if num == "1" else 0)
    # unit A: the rectifier
    ua = p.sym(f"U{k}", "OPA4376", x0 + 200, y0 + 8, unit=1)
    for num, net in (("2", f"ENV{k}_INM"), ("3", "AGND_REF"), ("1", f"ENV{k}_ROUT")):
        px, py = schlib.pin_xy(ua, num, x0 + 200, y0 + 8, 1)
        p.stub(net, px, py, dx=(7.62 if num == "1" else -7.62),
               rot=0 if num == "1" else 180)
    # the absolute-value summer
    p.series_h(f"R{b + 2}", x0 + 25, y0 + 40, f"ENV{k}_HW", f"ENV{k}_SUM")
    p.series_h(f"R{b + 3}", x0 + 25, y0 + 55, f"ENV{k}_AC", f"ENV{k}_SUM")
    p.series_h(f"R{b + 4}", x0 + 110, y0 + 47, f"ENV{k}_SUM", f"ENV{k}_ABS")
    ub = p.sym(f"U{k}", "OPA4376", x0 + 200, y0 + 47, unit=2)
    for num, net in (("6", f"ENV{k}_SUM"), ("5", "AGND_REF"), ("7", f"ENV{k}_ABS")):
        px, py = schlib.pin_xy(ub, num, x0 + 200, y0 + 47, 2)
        p.stub(net, px, py, dx=(7.62 if num == "7" else -7.62),
               rot=0 if num == "7" else 180)
    # the 50 Hz Sallen-Key
    p.series_h(f"R{b + 5}", x0 + 25, y0 + 85, f"ENV{k}_ABS", f"ENV{k}_MID")
    p.series_h(f"R{b + 6}", x0 + 85, y0 + 85, f"ENV{k}_MID", f"ENV{k}_INP")
    p.series_h(f"C{b + 2}", x0 + 145, y0 + 85, f"ENV{k}_MID", f"ENV{k}_FLT",
               kind="C_H")
    p.decouple(f"C{b + 1}", x0 + 85, y0 + 105, f"ENV{k}_INP", "AGND_REF")
    uc = p.sym(f"U{k}", "OPA4376", x0 + 210, y0 + 92, unit=3)
    for num, net in (("9", f"ENV{k}_FLT"), ("10", f"ENV{k}_INP"), ("8", f"ENV{k}_FLT")):
        px, py = schlib.pin_xy(uc, num, x0 + 210, y0 + 92, 3)
        p.stub(net, px, py, dx=(7.62 if num == "8" else -7.62),
               rot=0 if num == "8" else 180)
    p.note("f0 = 49.9 Hz, Q = 0.742, C0G (ECO-EEG-019)", x0 + 25, y0 + 122, 1.0)
    # the output divider and the buffer
    p.series_h(f"R{b + 7}", x0 + 25, y0 + 135, f"ENV{k}_FLT", f"ENV{k}_DIV")
    p.series_h(f"R{b + 8}", x0 + 85, y0 + 135, f"ENV{k}_DIV", "AGND_REF")
    ud = p.sym(f"U{k}", "OPA4376", x0 + 210, y0 + 135, unit=4)
    for num, net in (("13", out), ("12", f"ENV{k}_DIV"), ("14", out)):
        px, py = schlib.pin_xy(ud, num, x0 + 210, y0 + 135, 4)
        p.stub(net, px, py, dx=(7.62 if num == "14" else -7.62),
               rot=0 if num == "14" else 180)
    p.note("unity-gain buffer: pin 13 and pin 14 are the same node", x0 + 150,
           y0 + 152, 1.0)
    # the power unit
    up = p.sym(f"U{k}", "OPA4376", x0 + 285, y0 + 60, unit=5)
    for num, net in (("4", "AVDD"), ("11", "AVSS")):
        px, py = schlib.pin_xy(up, num, x0 + 285, y0 + 60, 5)
        p.stub(net, px, py, dy=(-5.08 if num == "4" else 5.08))
    p.decouple(f"C{b + 3}", x0 + 315, y0 + 40, "AVDD", "AGND_REF")
    p.decouple(f"C{b + 4}", x0 + 315, y0 + 85, "AVSS", "AGND_REF")
    p.sh.box(x0 + 5, y0 - 12, x0 + 345, y0 + 160, f"env{k}")


def sheet_audio(p):
    p.title("60  AUDIO, ENVELOPES AND THE COMPARATOR", 20, 16)
    p.note("Signal flow is left to right: the codec headphone tap and the two "
           "microphone preamplifiers enter on the left, three envelope detectors "
           "scale them to +/-100 mV for the converter, and the stimulus envelope also "
           "drives the comparator.  CMP_RAW is the one signal that crosses the zone "
           "split by design, through R83 and the D23 clamp.", 20, 21)
    p.connector("J8", 55, 90, "r")
    p.note("audio codec module", 36, 34, 1.2, 30)
    p.connector("J9", 55, 190, "r")
    p.note("codec microphone feeds", 36, 172, 1.2, 30)
    p.connector("J21", 55, 250, "r")
    p.note("boom preamplifier on MP-01", 36, 232, 1.2, 30)
    p.connector("J18", 55, 310, "r")
    p.note("boom pigtail (bare capsule)", 36, 292, 1.2, 30)
    p.connector("J28", 55, 380, "r")
    p.note("room microphone module", 36, 362, 1.2, 30)
    p.connector("J27", 55, 450, "r")
    p.note("3.5 mm headphone pigtail", 36, 432, 1.2, 30)

    p.decouple("C82", 145, 100, "DVDD3V3", "DGND")
    p.decouple("C86", 145, 260, "DVDD3V3", "DGND")
    p.series_h("R89", 150, 340, "DVDD3V3", "VOICE_RAW")
    p.decouple("C90", 145, 400, "DVDD3V3", "DGND")
    p.note("R89 is DO NOT POPULATE by default: fit only if the boom preamplifier "
           "module does not supply its own electret bias (ICD-EEG-006 section 7.2).",
           110, 352, 1.0, 46)

    for i, (k, b, src, out, _yb, _lbl) in enumerate(D.ENV):
        _env_channel(p, k, b, src, out, 215, 55 + i * 180)

    # the comparator
    cx, cy = 610.0, 60.0
    p.title("comparator -- RFQ E-12", cx, cy - 14, 1.8)
    p.divider("R80", "R81", cx + 10, cy + 20, "AVDD", "ENV_THR", "AGND_REF")
    u7x, u7y = cx + 120, cy + 40
    u7 = p.sym("U7", "TLV3201", u7x, u7y)
    for num, net in (("3", "ENV_STIM"), ("4", "ENV_THR"), ("1", "CMP_RAW"),
                     ("5", "AVDD"), ("2", "AVSS")):
        px, py = schlib.pin_xy(u7, num, u7x, u7y, 1)
        if num in ("3", "4"):
            p.stub(net, px, py, dx=-7.62, rot=180)
        elif num == "1":
            p.stub(net, px, py, dx=7.62)
        else:
            p.stub(net, px, py, dy=(-5.08 if num == "5" else 5.08))
    p.series_h("R82", u7x, cy, "CMP_RAW", "ENV_STIM")
    p.note("R82 is the 1 M hysteresis, about 5 mV", cx + 60, cy + 88, 1.0, 60)
    p.series_h("R83", u7x - 20, cy + 110, "CMP_RAW", "ENV_CMP")
    p.sym("D23", "D_CLAMP_V", u7x + 60, cy + 110)
    dc = p.lib["D_CLAMP_V"]
    for num, net in (("2", "DVDD3V3"), ("1", "DGND"), ("3", "ENV_CMP")):
        px, py = schlib.pin_xy(dc, num, u7x + 60, cy + 110, 1)
        if num == "3":
            p.stub(net, px, py, dx=-7.62, rot=180)
        else:
            p.stub(net, px, py, dy=(-5.08 if num == "2" else 5.08))
    p.note("ECO-EEG-023, OPEN: U7's output swings +/-2.5 V into a 3.3 V GPIO.  R83 and "
           "the D23 clamp are the fix in the design and the ECO is NOT IMPLEMENTED -- "
           "the safety reviewer holds it.", cx, cy + 140, 1.1, 46)


def sheet_lights(p):
    p.title("70  CONTACT LIGHTS -- 74HC595 and the light harness", 20, 18)
    p.note("Eight bicolour contact lights in the helmet, driven from the converter's "
           "own lead-off measurement.  ECO-EEG-014 moved the eight light lines out of "
           "the electrode harness into their own ten-way ribbon at J30, so nothing "
           "digital enters J14.", 20, 24)
    p.connector("J19", 90, 130, "r")
    p.note("74HC595 shift-register module", 66, 42)
    p.connector("J30", 470, 100, "l")
    p.note("contact-light harness, 10-way", 450, 42)
    for i in range(8):
        p.series_h(f"R{70 + i}", 300, 60 + i * 20.32, f"SR_Q{i}", f"LED{i + 1}")
    p.note("1 k per site: (3.3 - 2.0) / 1000 = 1.3 mA, and 10.4 mA on the LED_V "
           "common -- inside the 74HC595's 35 mA per output and 70 mA per package.",
           260, 232, 1.1)
    p.series_h("R78", 300, 250, "LED_PWM", "LED_V")
    p.series_h("R79", 300, 275, "LED_GND", "DGND")
    p.series_h("R87", 300, 300, "LED_OE", "DGND")
    p.note("R87 ties the output enable active", 260, 312, 1.0)
    p.series_h("R88", 300, 325, "LED_MR", "DVDD3V3")
    p.decouple("C88", 400, 320, "LED_MR", "DGND")
    p.note("R88 and C88 are the 74HC595 power-on reset.  Dark-at-boot is guaranteed "
           "in hardware by LED_V being GPIO48, an input at reset, so no current can "
           "flow through any light whatever the register holds (RFQ E-27).",
           260, 350, 1.1)
    p.decouple("C84", 470, 250, "DVDD3V3", "DGND")
    p.note("local decoupling at J19", 450, 272)


def sheet_star(p):
    p.title("80  STAR POINTS, TEST POINTS AND MECHANICAL", 20, 18)
    p.note("R90 is the ONLY AGND_REF-to-DGND path and R91, on sheet 50, is the only "
           "HARN_SHIELD-to-DGND path (DSN-EEG-003 section 3.3 rule 2).  Both are 0 R "
           "0603 parts and never copper bridges, so either can be lifted for a "
           "leakage measurement and refitted.  FIT EXACTLY ONE OF EACH.", 20, 24)
    p.series_h("R90", 120, 60, "AGND_REF", "DGND", left_len=15.24, right_len=15.24)
    p.sh.box(80, 44, 190, 76, "star")

    p.title("TP1-TP18 -- assigned in TST-EEG-004 section 6.2, which owns the table",
            20, 110, 1.6)
    for i, (ref, net, _x, _y) in enumerate(D.TESTPOINTS):
        col, row = i % 6, i // 6
        p.testpoint(ref, net, 40 + col * 76.2, 140 + row * 40.64)

    p.title("Mechanical features -- fabricated, not purchased", 20, 290, 1.6)
    for i in range(4):
        p.sym(f"MH{i + 1}", "MOUNTING_HOLE", 50 + i * 30.48, 320,
              value="M3 3.2 mm NPTH")
    for i in range(3):
        p.sym(f"FID{i + 1}", "FIDUCIAL", 220 + i * 30.48, 320,
              value="1 mm / 3 mm mask")
    p.note("MH1-MH4 at (5,5), (145,5), (5,125) and (145,125), 6 mm copper keep-out on "
           "all four layers.  FID1-FID3 at (12,10), (144,100) and (12,120).  They "
           "carry no net and appear here so the schematic's designator set is the "
           "board's (ECO-EEG-020, ECO-EEG-007).", 20, 345, 1.1)


BUILDERS = {"10_power": sheet_power, "20_isolation_usb": sheet_isolation,
            "30_controller": sheet_controller, "40_afe_1": sheet_afe1,
            "41_afe_2": sheet_afe2, "50_harness_input": sheet_harness,
            "60_audio": sheet_audio, "70_contact_lights": sheet_lights,
            "80_star_points_test": sheet_star}


# --------------------------------------------------------------------------- root
def build_root(children, lib, inter):
    root = Sheet(f"{D.stem(D.REV_C)}.kicad_sch", "root",
                 f"EEG-CAR-01 Rev {D.REV_C} -- carrier board", 1, D.REV_C, D.DATE_C,
                 COMPANY,
                 ["UNROUTED. Placement and routing are external (ECO-EEG-030).",
                  "Generated from tools/design.py by tools/emit_kicad_sch.py. "
                  "Not edited by hand.",
                  "Rules: LAY-EEG-034 and kicad/EEG-CAR-01_RevC.kicad_dru.",
                  "Licence CC BY-SA 4.0."],
                 root=True, paper="A1")
    root.text(f"EEG-CAR-01 Rev {D.REV_C} -- block diagram", 20, 18, 3.0)
    root.text("Signal flow is left to right and top to bottom.  Power and ground are "
              "global through power symbols and carry no sheet pin; every other net "
              "that crosses a sheet boundary is a hierarchical pin here.", 20, 26, 1.4)
    root.text("Nothing in this package has been manufactured or measured, and no "
              "safety engineer has reviewed this design.", 20, 32, 1.4)

    cols = [(30.0, 60.0), (290.0, 60.0), (550.0, 60.0)]
    W, H = 180.0, 130.0
    for i, ch in enumerate(children):
        cx, cy = cols[i % 3]
        y = cy + (i // 3) * 150.0
        nets = sorted(n for n in inter if ch.stem in inter[n])
        pins = []
        left = [n for n in nets if n in ch.hier_in]
        right = [n for n in nets if n not in ch.hier_in]
        for j, nname in enumerate(left):
            pins.append((nname, "input", "l", 8.0 + j * 3.0))
        for j, nname in enumerate(right):
            pins.append((nname, "output", "r", 8.0 + j * 3.0))
        root.add_child(ch, cx, y, W, H, pins)
        for nname, _shape, side, off in pins:
            px = cx if side == "l" else cx + W
            py = y + off
            dx = -6.0 if side == "l" else 6.0
            root.wire(px, py, px + dx, py)
            root.label(nname, px + dx, py, 0,
                       justify="right bottom" if side == "l" else "left bottom")
    return root


# --------------------------------------------------------------------------- library
def write_symbol_library(lib, path):
    """kicad/EEG-CAR-01.kicad_sym -- the symbols as a KiCad library.

    ICD-EEG-006 Rev B said, correctly for Rev B, that no such file exists and that Rev A
    was wrong to claim one.  It exists from Rev C and it is generated, and the ICD is
    corrected in the same change (ECO-EEG-033) rather than left contradicting the tree.
    The contractor needs it: a .kicad_sch whose symbols live only inside itself opens,
    but nobody can edit it without the library the symbols came from.
    """
    L = ['(kicad_symbol_lib', "  (version 20231120)",
         '  (generator "eeg-car-01-generator")', '  (generator_version "8.0")']
    for name in sorted(lib):
        L.append(lib[name].sexp())
    L.append(")")
    text = "\n".join(L) + "\n"
    ok, why = balanced(text)
    if not ok:
        raise SystemExit(f"EEG-CAR-01.kicad_sym is not balanced: {why}")
    open(path, "w").write(text)
    return path


# --------------------------------------------------------------------------- driver
def main(verbose=True):
    global INTER
    n_assigned = check_assignment()
    INTER = inter_sheet_nets()
    lib = schlib.build()
    os.makedirs(KDIR, exist_ok=True)

    children, pages = [], []
    for page, (stem, name, title, refs) in enumerate(SHEETS, start=2):
        fname = f"{D.stem(D.REV_C)}_{stem}.kicad_sch"
        sh = Sheet(fname, name, title, page, D.REV_C, D.DATE_C, COMPANY,
                   ["UNROUTED. Placement and routing are external (ECO-EEG-030).",
                    "Generated from tools/design.py by tools/emit_kicad_sch.py.",
                    "Licence CC BY-SA 4.0."],
                   root_uuid=None, paper=PAPER_OF.get(stem, "A2"))
        sh.stem = stem
        p = Page(sh, lib, stem)
        BUILDERS[stem](p)
        sh.hier_in = set()          # filled below, used by the root for pin direction
        children.append(sh)
        pages.append(p)

    root = build_root_prepare(children, pages, lib)

    made = []
    for sh in children:
        sh.root_uuid = root.uuid
        sh._instance_path = f"/{root.uuid}"
        made.append(sh.write(os.path.join(KDIR, sh.filename)))
    made.append(root.write(os.path.join(KDIR, root.filename)))
    made.append(write_symbol_library(lib, os.path.join(KDIR, "EEG-CAR-01.kicad_sym")))

    for path in made:
        if not path.endswith((".kicad_sch", ".kicad_sym")):
            continue
        ok, why = balanced(open(path).read())
        if not ok:
            raise SystemExit(f"{os.path.basename(path)} is not balanced: {why}")

    if verbose:
        print(f"== EEG-CAR-01 Rev {D.REV_C} schematic ==")
        print(f"   {n_assigned} designators over {len(SHEETS)} sheets plus the root")
        print(f"   {len(INTER)} nets cross a sheet boundary and carry a hierarchical "
              f"pin")
        print(f"   {len(set(D.N.values())) - len(INTER)} nets are local to one sheet "
              f"or global through a power symbol")
        for m in made:
            print("   ", os.path.relpath(m, PKG))
    return made


def build_root_prepare(children, pages, lib):
    """Work out which side of each sheet symbol a net's pin belongs on, then build the
    root.  A net is an INPUT to the sheet that does not drive it; with no direction
    information in design.py, the first sheet in SHEETS order owns the output and the
    rest take inputs, which is a convention and is stated as one on the sheet."""
    owner = {}
    for sh, p in zip(children, pages):
        for net in sorted(p.hier):
            owner.setdefault(net, sh.stem)
    for sh, p in zip(children, pages):
        sh.hier_in = {net for net in p.hier if owner.get(net) != sh.stem}
        sh.stem_nets = set(p.hier)
    return build_root(children, lib, INTER)


if __name__ == "__main__":
    main()
