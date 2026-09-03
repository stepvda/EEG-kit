#!/usr/bin/env python3
"""
fixture_gen.py -- released data for the FIX-01 to FIX-04 test fixtures of JIG-EEG-009.

JIG-EEG-009 Rev B designs four fixtures, prices them and schedules them.  Three things it
called for had no files at all, and this generator writes them:

  * **the fixture printed circuit boards.**  Section 6.1 prices "Fixture PCB, 5-off
    minimum order" for FIX-01 and FIX-04 and section 6.3 allows ten working days to
    fabricate and assemble them, against no schematic, no netlist and no artwork.
  * **the printed fixture parts.**  Section 1.8 calls for a light-tight FIX-01/E manifold
    "printed from the FIX-01 STL set", section 2.4 for couplers "printed from the FIX-02
    STL set" and section 3.3 for a PA12 nest.  None of those sets existed.
  * **the manifest** that ties both of the above, and the fixture firmware beside them, to
    a checksum, so a fixture can be told from another fixture built from other files.

WHAT IS RELEASED HERE AND WHAT IS NOT, STATED BEFORE ANYTHING ELSE

The printed parts are a complete release: STEP and STL from one parametric model, the same
treatment tools/mech_gen.py gives the product's own printed parts, and the cavity volumes
that FIX-02/A and FIX-02/B are specified by are computed from the model rather than
asserted beside it.

**The fixture PCBs are NOT a fabrication release, and this file does not pretend one.**
There is no copper layer here, no via, no paste and no assembly drawing.  What is released
is everything that does not need a layout engineer -- the outline, the mounting holes, the
zoning and keep-out artwork, the panel legend, the drill programme for the non-plated
holes, the complete netlist and the constraint set -- because those are derivable from
JIG-EEG-009 and the netlist is the thing a layout house cannot start without.  Copper is
not derivable: laying out 83 relays and 144 precision resistors on two layers with a driven
guard pour is a person's job, and the one dimension it turns on -- the land pattern of the
Omron G6K-2F-Y -- is a datasheet this package does not carry.  `--check` computes the area
budget against a stated land-pattern envelope and says what that envelope has to be for the
160.0 x 100.0 mm outline of section 1.9 to be feasible at all.  Inventing a copper layer
against a footprint nobody has measured would produce a file a fabricator would build and a
board nobody could assemble.

Usage:  python3 tools/fixture_gen.py                emit everything, then self-check
        python3 tools/fixture_gen.py --pcb          the two PCB data sets only
        python3 tools/fixture_gen.py --mech         the printed parts only (needs cadquery)
        python3 tools/fixture_gen.py --check        self-check and area budget, emit nothing
        python3 tools/fixture_gen.py --quiet        emit, print only failures

Nothing here has been fabricated, printed or measured.  No fixture has been built
(JIG-EEG-009 section 7).

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
OUT = os.path.join(PKG, "fixtures")
sys.path.insert(0, HERE)

import strokefont as SF          # noqa: E402  -- read-only use of the package's own font

DATE = "2026-09-02"
GEN = "package_v2.4/tools/fixture_gen.py"


# =======================================================================================
# Section 1.  The two fixture boards, as descriptions.
# =======================================================================================
# Everything below that carries a JIG-EEG-009 section number is transcribed from the
# document.  Everything that does not is a choice made here, and each one says so on the
# line it is made.

FIX01 = dict(
    name="FIX-01",
    rev="A",
    title="front-end injection, lead-off and contact-light fixture",
    # JIG-EEG-009 section 1.9, verbatim.
    w=160.0, h=100.0, layers=2, thickness=1.60,
    mount=[(5.0, 5.0), (155.0, 5.0), (5.0, 95.0), (155.0, 95.0)],
    mount_d=3.2, mount_keepout_d=6.0,
    min_track=0.20, min_gap=0.20,
    finish="ENIG", mask="green", legend="white both sides",
    source="JIG-EEG-009 section 1.9",
    # Section 1.9's x bands, as rectangles.  The y extents are this file's: the document
    # gives bands in x only, and a zoning layer needs both.
    zones=[
        (0.0, 0.0, 40.0, 100.0, "GUARDED COMPARTMENT",
         "U3, K101-K103, A1, U1, A2, U2, inside the soldered can"),
        (40.0, 0.0, 150.0, 100.0, "RELAY MATRIX + REFERENCE FIELD",
         "5 columns of 16 relays and the RA/RB/RC/RS resistor field"),
        (150.0, 0.0, 160.0, 100.0, "LOGIC",
         "TPIC6B595 chain, M1, U20, 5 V input, FIX-01/E I2C header"),
    ],
    # Tinplate can, JIG-EEG-009 section 1.8: 60 x 40 x 15 mm, soldered on four sides.  The
    # 60 mm side is placed along Y so the can fits the 40 mm-wide x band of section 1.9;
    # that orientation is this file's and is stated on the zoning layer.
    can=(1.0, 20.0, 41.0, 80.0),
)

FIX04 = dict(
    name="FIX-04",
    rev="A",
    title="harness continuity and isolation scanner card",
    # NOT in JIG-EEG-009: the document prices a FIX-04 PCB at EUR 40 and never gives it an
    # outline.  120.0 x 80.0 mm is chosen here against the area budget of --check, which
    # puts the bill of materials at about a third of the board.  It is deliberately loose
    # rather than minimal: this is the card that carries 500 V DC, the 3.0 mm creepage
    # rule of the constraints file costs area, and a scanner squeezed onto the smallest
    # panel that would hold the parts is the wrong trade on the one fixture where a
    # flashover reaches an operator.
    w=120.0, h=80.0, layers=2, thickness=1.60,
    mount=[(5.0, 5.0), (115.0, 5.0), (5.0, 75.0), (115.0, 75.0)],
    mount_d=3.2, mount_keepout_d=6.0,
    min_track=0.20, min_gap=0.20,
    finish="ENIG", mask="green", legend="white both sides",
    source="this file; JIG-EEG-009 section 4.1 gives the card no outline",
    zones=[
        (0.0, 0.0, 85.0, 80.0, "SCANNER MATRIX",
         "24 DPDT relays, four rows of six, instrument bus and common bus"),
        (85.0, 0.0, 120.0, 80.0, "LOGIC AND ENTRY",
         "U30-U32, M3, 5 V input, lid interlock, instrument leads"),
    ],
    can=None,
)

BOARDS = [FIX01, FIX04]

# The land-pattern envelope used by the area budget.  It is NOT a datasheet figure: the
# Omron G6K-2F-Y datasheet is not in this package (AVL-EEG-017 names the part, not its
# footprint).  10.0 x 7.0 mm is the envelope a two-pole signal relay of that class is
# ASSUMED to need including its courtyard, and --check reports the largest envelope the
# section 1.9 outline can carry, so the assumption can be replaced by a measurement in one
# line when somebody opens the datasheet.
RELAY_ENV_MM2 = 10.0 * 7.0
IC_SOIC20W_MM2 = 13.0 * 8.0     # SOIC-20 wide body plus courtyard, IPC-7351 nominal
IC_SOIC24W_MM2 = 16.0 * 8.0
R0603_MM2 = 2.0 * 3.0           # 0603 land pair plus the spacing a resistor field needs
PICO_MM2 = 51.0 * 21.0          # Raspberry Pi Pico module outline
HDR_PER_WAY_MM2 = 2.54 * 6.0    # a 2.54 mm header way plus its keep-out


# ---------------------------------------------------------------------------------------
# The FIX-01 netlist, generated from the section 1.2 text schematic.
# ---------------------------------------------------------------------------------------
# Pins are named by FUNCTION and not by number.  No pinout in this package is a released
# fact -- the OPA189, the ADR4550, the TPIC6B595 and the CD74HC4067 are all named by MPN in
# section 1.8 and by nothing else -- so a netlist with pin numbers in it would be inventing
# eleven datasheets.  Schematic capture assigns the numbers; the connectivity below is what
# JIG-EEG-009 actually specifies and it is complete.

def fix01_netlist():
    """Return {net: [pin, ...]} for FIX-01, built from JIG-EEG-009 sections 1.2 and 1.5."""
    n = {}

    def add(net, *pins):
        n.setdefault(net, []).extend(pins)

    # --- the divider, section 1.3.  No switch contact appears in either ratio leg. -----
    add("SRC_HI",  "R101.1", "K103.C1", "J102H.1")
    add("SRC_MID", "R101.2", "R102.1", "U1.IN+")
    add("FIX_COM", "R102.2", "R104.2", "U1.VS-", "U2.VS-", "U3.GND")
    add("GRD_DRV", "U1.OUT", "U1.IN-", "R103.1", "U2.IN+")
    add("GUARD",   "U2.OUT", "U2.IN-")
    add("SRC_LO",  "R103.2", "R104.1")
    add("V5",      "U1.VS+", "U2.VS+", "U3.VIN", "J107.1")

    # --- source select and the polarity commutator, section 1.2 -----------------------
    # K103 is the SIN / CAL changeover: common to SRC_HI, normally-open to the generator,
    # normally-closed to the commutated reference.  That much is section 1.2.
    #
    # K101 and K102 are given there as "DPDT polarity reversal, 5 s dwell each polarity"
    # and no contact assignment.  What is modelled here is the four-changeover reversal
    # two DPDT relays give: the reference pair enters on the two commons and leaves as
    # CAL_HI / CAL_LO with the sense swapped when both relays are energised.  It is the
    # only assignment that produces the polarity differencing the section 1.3 uncertainty
    # budget takes credit for, and it is THIS FILE'S reading -- see the note in the
    # constraints file, and JIG-EEG-009 section 8.9, which records the one question it
    # raises: a reference that is reversed against the fixture common has to float, and
    # section 1.2 does not say whether U3 is on an isolated rail.
    add("REF_HI",  "U3.VOUT", "K101.C1", "K102.NC1")
    add("REF_LO",  "U3.GND_SENSE", "K102.C1", "K101.NC1")
    add("CAL_HI",  "K101.NO1", "K102.NO2", "K103.NC1")
    add("FIX_COM", "K102.NO1", "K101.NO2")
    add("REF_HI",  "K101.C2")
    add("REF_LO",  "K102.C2")
    add("GEN_IN",  "J101H.1", "K103.NO1")
    add("GEN_SCR", "J101H.2", "LK1.1")
    add("FIX_COM", "LK1.2", "J102H.2")

    # --- sixteen channel networks, section 1.2 ---------------------------------------
    for c in range(1, 17):
        k_src, k_ra, k_rb, k_rc, k_sh = (5 * c - 4, 5 * c - 3, 5 * c - 2,
                                         5 * c - 1, 5 * c)
        node = f"NODE{c}"
        add("SRC_LO", f"K{k_src}.NO1")
        add(node, f"K{k_src}.C1", f"K{k_ra}.C1", f"K{k_rb}.C1",
                  f"K{k_rc}.C1", f"K{k_sh}.C1", f"RS{c}.1", f"U20.I{c - 1}")
        add(f"RA{c}_SW", f"K{k_ra}.NO1", f"RA{c}.1")
        add(f"RB{c}_SW", f"K{k_rb}.NO1", f"RB{c}.1")
        add(f"RC{c}_SW", f"K{k_rc}.NO1", f"RC{c}.1")
        add("FIX_COM", f"RA{c}.2", f"RB{c}.2", f"RC{c}.2", f"K{k_sh}.NO1")
        add(f"CH{c}", f"RS{c}.2")

    # --- the readback network, section 8.4 -------------------------------------------
    add("MUX_COM", "U20.COM", "RP1.2", "M1.ADC0")
    add("MUX_PULL", "RP1.1", "M1.GP11")
    add("V5", "U20.VCC")
    add("FIX_COM", "U20.GND")
    # The mux enable is DRIVEN, not strapped low.  A multiplexer permanently enabled has
    # one of sixteen channel nodes connected to the readback network at all times, and the
    # readback network is the thing section 8.4 keeps away from a mated unit.
    add("MUX_EN", "U20.E", "M1.GP10")
    for i, gp in enumerate(("GP6", "GP7", "GP8", "GP9")):
        add(f"MUX_A{i}", f"U20.S{i}", f"M1.{gp}")

    # --- the shift-register chain, eleven devices, section 8.4 ------------------------
    # Section 1.8 Rev B listed ten TPIC6B595, which is 80 outputs for 83 relays.  The
    # eleventh is U22 and it carries K101, K102 and K103 with five outputs spare.
    regs = [f"U{i}" for i in range(10, 20)] + ["U22"]
    add("SR_SER", "M1.GP3", f"{regs[0]}.SERIN")
    for a, b in zip(regs, regs[1:]):
        add(f"SR_LINK_{a}_{b}", f"{a}.SEROUT", f"{b}.SERIN")
    for r in regs:
        add("SR_SRCK", f"{r}.SRCK", "M1.GP2")
        add("SR_RCK", f"{r}.RCK", "M1.GP4")
        add("SR_G", f"{r}.G", "M1.GP5")
        add("SR_CLR", f"{r}.SRCLR")
        add("V5", f"{r}.VCC")
        add("FIX_COM", f"{r}.GND")
    # Relay coils: high side to V5, low side to a shift-register drain.
    order = list(range(1, 81)) + [101, 102, 103]
    for idx, k in enumerate(order):
        reg = regs[idx // 8] if k <= 80 else regs[10]
        drain = (idx % 8) if k <= 80 else (k - 101)
        add("V5", f"K{k}.A1")
        add(f"COIL_K{k}", f"K{k}.A2", f"{reg}.DRAIN{drain}")

    # --- connectors, sections 1.2 and 1.8 --------------------------------------------
    for c in range(1, 12):                        # J103, 1x12 into J14  [FIX-01/A]
        add(f"CH{c}", f"J103.{c}")
    add("SHIELD_SENSE", "J103.12")                # J14 way 12 is HARN_SHIELD, section 1.11
    for i, c in enumerate((12, 13, 14), start=1):  # J105 header to the DIN bar [FIX-01/B]
        add(f"CH{c}", f"J105.{i}")
    add("FIX_COM", "J105.4")
    add("CH15", "J106.1")                         # J22.1 SPARE1                [FIX-01/G]
    add("FIX_COM", "J106.2")                      # J22.2 AGND_REF              [FIX-01/C]
    add("CH16", "J106.3")                         # J22.3 SPARE2                [FIX-01/G]
    # J104, 1x10 into J30, FIX-01/E.  The eight LEDs are the helmet part in the helmet's
    # polarity; the current limit is R70-R77 ON THE CARRIER and there is none here.
    for i in range(1, 9):
        add(f"LED{i}", f"J104.{i}", f"RL{i}.1")
        add(f"LED{i}_A", f"RL{i}.2", f"D20{i}.K")
        add("LED_V", f"D20{i}.A")
    add("LED_V", "J104.9")
    add("LED_GND", "J104.10")
    add("V5", "U21.VIN")
    add("FIX_COM", "U21.GND")
    add("I2C_SDA", "U21.SDA", "M1.GP16")
    add("I2C_SCL", "U21.SCL", "M1.GP17")
    add("V5", "M1.VSYS")
    add("FIX_COM", "M1.GND", "J107.2")
    return {k: sorted(set(v)) for k, v in n.items()}


def fix04_netlist():
    """Return {net: [pin, ...]} for the FIX-04 scanner card, JIG-EEG-009 section 4.1."""
    n = {}

    def add(net, *pins):
        n.setdefault(net, []).extend(pins)

    # Each conductor arrives on one way of a head connector and leaves on one relay's
    # common.  Released, the conductor sits on the common bus; energised, it goes to the
    # instrument.  That is what makes the all-pairs isolation matrix of WH-EEG-008 H2 one
    # mask write: one conductor to the instrument, twenty-three to the common bus.
    # Twenty-four channels for twenty-five conductors.  The three heads of section 4.1
    # carry 12 + 10 + 3 = 25 between them and the card has 24 relays, so one pairing has
    # to share.  The EMG head is paralleled onto channels 1 to 3 and the rule that goes
    # with it is on the board legend: THE ELECTRODE HEAD AND THE EMG HEAD ARE NEVER MATED
    # AT THE SAME TIME.  They never need to be -- WH-EEG-008 section 9 tests one cable at
    # a time -- and the alternative is a fourth shift register and eight more relays for
    # a case that does not arise.  Channels 23 and 24 are spare on a two-way header, so a
    # conductor that needs its own path during a diagnosis has one.
    for i in range(1, 13):
        add(f"COND{i}_E{i}", f"J401.{i}", f"K{i}.C1")
    for i in range(1, 11):
        add(f"COND{i + 12}_L{i}", f"J402.{i}", f"K{i + 12}.C1")
    for i in range(1, 4):
        add(f"COND{i}_E{i}", f"J403.{i}")          # paralleled onto channels 1 to 3
    for i in (23, 24):
        add(f"COND{i}_SPARE", f"J407.{i - 22}", f"K{i}.C1")
    for i in range(1, 25):
        add("INSTR_BUS", f"K{i}.NO1")
        add("COMMON_BUS", f"K{i}.NC1")
    add("INSTR_BUS", "J404.1")          # to the DMM / insulation tester, guarded lead
    add("COMMON_BUS", "J404.2")
    add("EARTH_LEAD", "J404.3")         # FIX-04/C protective-earth lead, section 4.3

    regs = ["U30", "U31", "U32"]
    add("SR_SER", "M3.GP3", "U30.SERIN")
    add("SR_LINK_U30_U31", "U30.SEROUT", "U31.SERIN")
    add("SR_LINK_U31_U32", "U31.SEROUT", "U32.SERIN")
    for r in regs:
        add("SR_SRCK", f"{r}.SRCK", "M3.GP2")
        add("SR_RCK", f"{r}.RCK", "M3.GP4")
        add("SR_G", f"{r}.G", "M3.GP5")
        add("SR_CLR", f"{r}.SRCLR")
        add("V5", f"{r}.VCC")
        add("DGND", f"{r}.GND")
    for c in range(1, 25):
        # U30 receives SER and is byte 2 of the chain (fix_m3.c ch_byte()), so channels
        # 1 to 8 are on U30 and channels 17 to 24 on U32.
        reg = regs[(c - 1) // 8]
        add("V5", f"K{c}.A1")
        add(f"COIL_K{c}", f"K{c}.A2", f"{reg}.DRAIN{(c - 1) % 8}")
    add("LID_SW", "J405.1", "M3.GP20")
    add("DGND", "J405.2", "M3.GND", "J406.2")
    add("V5", "M3.VSYS", "J406.1")
    return {k: sorted(set(v)) for k, v in n.items()}


NETLISTS = {"FIX-01": fix01_netlist, "FIX-04": fix04_netlist}

# Nets with one pin, and the reason each is one.  A net of one is normally a wire to
# nowhere and --check treats it as a fault; these five are deliberate, so they are listed
# with their reasons rather than tolerated silently, and the netlist prints the reasons.
SINGLE_PIN_NETS = {
    "SR_CLR": "TPIC6B595 SRCLR.  It is tied to the controller's reset rail and not to a "
              "GPIO, so that a controller in reset opens every relay with no code "
              "running.  That is the safe state and it must not depend on firmware.",
    "SHIELD_SENSE": "J14 way 12, HARN_SHIELD.  A sense lead only: section 1.11 records "
                    "the resistance from FIX_COM to it during T9b and nothing on the "
                    "fixture drives it.",
    "EARTH_LEAD": "FIX-04/C's protective-earth lead.  It leaves on J404 way 3 and "
                  "reaches nothing else on the board, which is the point: the earth is "
                  "the measurement's other terminal, not a fixture rail.",
    "LED_GND": "J30 way 10.  Left unconnected in FIX-01/E on purpose.  FIX_COM reaches "
               "the DUT at exactly one point, J106 way 2 (section 1.11), and a second "
               "ground path from the unit into the fixture through the light connector "
               "would break that rule for no gain -- the head sinks its LED current "
               "through the eight LEDn lines the carrier drives.",
}

# Front-edge and panel connectors, for the legend and for the enclosure.  x, y are the
# position of way 1 on the board; the pitch is 2.54 mm along +x unless stated.  These are
# this file's positions -- section 1.9 says only "front edge" -- and they are what the
# WH-KEY-01 shrouds and the FIX-01 enclosure cut-outs have to line up with.
CONNECTORS = {
    "FIX-01": [
        ("J103", 46.0, 6.0, 12, "1x12 into J14   FIX-01/A   WH-KEY-01 J14 form"),
        ("J104", 80.0, 6.0, 10, "1x10 into J30   FIX-01/E   WH-KEY-01 J30 form"),
        ("J106", 110.0, 6.0, 3, "1x3 into J22    FIX-01/C + /G"),
        ("J105", 124.0, 6.0, 4, "to the DIN 42802 bar   FIX-01/B"),
        ("J101H", 20.0, 84.0, 2, "BNC generator input, left end panel"),
        ("J102H", 20.0, 16.0, 2, "BNC DMM monitor, left end panel"),
        ("J107", 152.0, 90.0, 2, "5 V 2 A isolated supply or USB power bank"),
    ],
    "FIX-04": [
        ("J401", 8.0, 6.0, 12, "12-way electrode head   FIX-04/D"),
        ("J402", 42.0, 6.0, 10, "10-way light head       FIX-04/D"),
        ("J403", 70.0, 6.0, 3, "EMG head  NEVER WITH J401  FIX-04/D"),
        ("J407", 82.0, 6.0, 2, "channels 23 and 24, spare"),
        ("J404", 92.0, 6.0, 3, "instrument, common, protective earth"),
        ("J405", 96.0, 72.0, 2, "lid interlock switch"),
        ("J406", 108.0, 72.0, 2, "5 V input"),
    ],
}


# =======================================================================================
# Section 2.  Gerber X2 emission.
# =======================================================================================
# Format 4.6 absolute metric, bottom-left origin, Y up -- the same %FSLAX46Y46*% / %MOMM*%
# pair EEG-CAR-01 and WH-BUS-01 use, so one CAM import setting covers every board in the
# package.

def _c(v: float) -> int:
    return int(round(v * 1e6))


def header(project, rev, function, polarity, comment):
    pid = hashlib.md5(project.encode()).hexdigest()
    return [
        f"%TF.GenerationSoftware,TI One Voice,{GEN},1.0*%",
        f"%TF.CreationDate,{DATE}T00:00:00+01:00*%",
        f"%TF.ProjectId,{project},{pid},{rev}*%",
        f"%TF.FileFunction,{function}*%",
        f"%TF.FilePolarity,{polarity}*%",
        "%TF.SameCoordinates,Original*%",
        "%FSLAX46Y46*%",
        "%MOMM*%",
        f"G04 {comment}*",
        f"G04 {project} Rev {rev} -- TI One Voice research programme*",
        "G04 NOT A FABRICATION SET -- no copper layer exists for this board*",
        "G04 Licence CC BY-SA 4.0*",
        "G01*",
        "G75*",
        "%LPD*%",
    ]


def apertures(specs):
    lines, codes, d = [], {}, 10
    for func, shape in specs:
        if shape in codes:
            continue
        if func:
            lines.append(f"%TA.AperFunction,{func}*%")
        lines.append(f"%ADD{d}{shape}*%")
        if func:
            lines.append("%TD*%")
        codes[shape] = d
        d += 1
    return lines, codes


def draw(pts):
    out = [f"X{_c(pts[0][0])}Y{_c(pts[0][1])}D02*"]
    out += [f"X{_c(x)}Y{_c(y)}D01*" for x, y in pts[1:]]
    return out


def rect_path(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def circle_path(cx, cy, r, n=64):
    return [(cx + r * math.cos(2 * math.pi * i / n),
             cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def edge_cuts(b):
    lines = header(b["name"], b["rev"], "Profile,NP", "Positive",
                   "Board outline (profile is the centre line)")
    alines, codes = apertures([("Profile", "C,0.100000")])
    lines += alines + [f"D{codes['C,0.100000']}*"]
    lines += draw(rect_path(0.0, 0.0, b["w"], b["h"]))
    lines.append("M02*")
    return "\n".join(lines) + "\n"


def text(lines, codes, ap, s, x, y, h, limit=None):
    """One legend string, clipped to the board.

    Legend that runs off the profile is legend the fabricator drops or the CAM operator
    queries, so it is truncated here rather than emitted and caught later; --check reads
    the file back and fails if anything is outside the outline, which is how the clipping
    got written in the first place.
    """
    if limit is not None:
        while s and x + SF.text_width(s, h) > limit:
            s = s[:-1]
        if not s:
            return
    lines.append(f"D{codes[ap]}*")
    for poly, _th in SF.text_strokes(s, x, y, height=h):
        lines += draw(poly)


def silkscreen(b):
    """The panel legend.  It carries what an operator has to read on the bench and the two
    warnings that section 1.11 makes load-bearing: the fixture common is not DGND, and the
    guard pour is not a screen."""
    lines = header(b["name"], b["rev"], "Legend,Top", "Positive",
                   "Silkscreen Top -- panel legend and zone captions")
    alines, codes = apertures([("Material", "C,0.150000")])
    lines += alines
    ap = "C,0.150000"
    edge = b["w"] - 2.0
    text(lines, codes, ap, f"{b['name']} REV {b['rev']}", 4.0, b["h"] - 8.0, 3.0, edge)
    text(lines, codes, ap, b["title"].upper(), 4.0, b["h"] - 13.0, 2.0, edge)
    text(lines, codes, ap, "TI ONE VOICE  CC BY-SA 4.0  JIG-EEG-009 SECTION 8",
         4.0, b["h"] - 17.0, 1.6, edge)
    for (x0, y0, x1, y1, cap, _note) in b["zones"]:
        text(lines, codes, ap, cap, x0 + 2.0, (y0 + y1) / 2.0, 2.2, min(x1 - 1.0, edge))
    ends = sorted(x for (_r, x, _y, _w, _n) in CONNECTORS[b["name"]])
    for (ref, x, y, ways, note) in CONNECTORS[b["name"]]:
        # a caption may run as far as the next connector along the same row, or the edge
        nxt = min([e for e in ends if e > x] or [edge + 2.0]) - 2.0
        text(lines, codes, ap, ref, x, y + 3.2, 2.0, min(nxt, edge))
        text(lines, codes, ap, "1", x - 2.4, y - 0.9, 1.6, edge)
        text(lines, codes, ap, note, x, y - 4.6, 1.2, min(nxt, edge))
    if b["name"] == "FIX-01":
        text(lines, codes, ap, "FIX_COM IS ANALOGUE REFERENCE - NOT DGND",
             44.0, 92.0, 2.2, edge)
        text(lines, codes, ap, "GUARD IS DRIVEN - NOT A SCREEN",
             44.0, 88.0, 1.8, edge)
        text(lines, codes, ap, "GUARD STOPS 2MM SHORT OF EVERY SHROUD",
             44.0, 84.5, 1.6, edge)
    else:
        text(lines, codes, ap, "500 V DC - DO NOT SWITCH WHILE ENERGISED",
             4.0, 62.0, 2.2, edge)
        text(lines, codes, ap, "LID INTERLOCK MUST BE CLOSED TO ARM",
             4.0, 58.0, 1.8, edge)
        text(lines, codes, ap, "J403 EMG HEAD IS NEVER MATED WITH J401",
             4.0, 54.5, 1.8, edge)
    lines.append("M02*")
    return "\n".join(lines) + "\n"


def zoning(b):
    """A mechanical layer carrying the zone boundaries, the mounting-hole keep-outs, the
    screening-can outline and the connector footprints' way-1 marks.  It is what a layout
    engineer imports first: it says where things may not go before anything is placed."""
    lines = header(b["name"], b["rev"], "Other,Zoning", "Positive",
                   "Zoning, keep-outs and the screening can -- not a copper layer")
    alines, codes = apertures([(None, "C,0.200000"), (None, "C,0.100000")])
    lines += alines
    ap = "C,0.200000"
    lines.append(f"D{codes[ap]}*")
    for (x0, y0, x1, y1, _cap, _note) in b["zones"]:
        lines += draw(rect_path(x0, y0, x1, y1))
    if b["can"]:
        lines += draw(rect_path(*b["can"]))
    lines.append(f"D{codes['C,0.100000']}*")
    for (x, y) in b["mount"]:
        lines += draw(circle_path(x, y, b["mount_keepout_d"] / 2.0))
    for (_ref, x, y, ways, _note) in CONNECTORS[b["name"]]:
        lines += draw(rect_path(x - 1.6, y - 1.6, x + (ways - 1) * 2.54 + 1.6, y + 1.6))
    lines.append("M02*")
    return "\n".join(lines) + "\n"


def drill_npth(b):
    """Excellon 2, metric, trailing zeros suppressed -- as EEG-CAR-01-NPTH.drl.

    Four holes and no plated ones, because there is no copper: this file releases the
    mechanical drill programme and the plated programme comes with the layout."""
    lines = [
        "M48",
        f"; {b['name']} Rev {b['rev']} -- non-plated holes",
        "; TI One Voice research programme, CC BY-SA 4.0",
        f"; generated {DATE} from {GEN}",
        "; sizes are FINISHED hole diameters",
        "; NON-PLATED ONLY.  There is no plated drill programme for this board because",
        "; there is no copper layer -- see the README in this directory.",
        "FMAT,2",
        "METRIC,TZ",
        "; #@! TF.FileFunction,NonPlated,1,2,NPTH",
        f"T01C{b['mount_d']:.3f}",
        "%",
        "G90",
        "G05",
        "T01",
    ]
    for (x, y) in b["mount"]:
        lines.append(f"X{x:.3f}Y{y:.3f}")
    lines.append("M30")
    return "\n".join(lines) + "\n"


# =======================================================================================
# Section 3.  The notes that travel with the data.
# =======================================================================================
def _para(t, indent="  ", width=88):
    return textwrap.fill(" ".join(t.split()), width=width,
                         initial_indent=indent, subsequent_indent=indent)


def netlist_text(b, nets):
    # Pins per designator, not nets per designator: it is the number a schematic capture
    # can check its symbol against, and it is what says at a glance that a relay has four
    # pins used and a shift register twelve.
    parts = {}
    for _net, pins in nets.items():
        for p in pins:
            parts.setdefault(p.split(".")[0], set()).add(p.split(".", 1)[1])
    out = [
        f"{b['name']} Rev {b['rev']} -- netlist",
        f"TI One Voice research programme -- CC BY-SA 4.0 -- generated {DATE} by {GEN}",
        "",
        _para("Pins are named by FUNCTION and not by number. No pinout in this package is "
              "a released fact: JIG-EEG-009 section 1.8 names every semiconductor by "
              "manufacturer part number and by nothing else, so a netlist carrying pin "
              "numbers would be inventing eleven datasheets. Schematic capture assigns "
              "the numbers against the datasheets; the connectivity below is what "
              "JIG-EEG-009 specifies and it is complete.", indent=""),
        "",
        f"{len(nets)} nets, {sum(len(v) for v in nets.values())} pins, "
        f"{len(parts)} reference designators.",
        "",
        "NET                    PINS",
        "-" * 88,
    ]
    for net in sorted(nets):
        pins = nets[net]
        out.append(f"{net:<22} {pins[0]}")
        for p in pins[1:]:
            out.append(f"{'':<22} {p}")
    singles = [n for n in sorted(nets) if len(nets[n]) == 1]
    if singles:
        out += ["", "NETS WITH ONE PIN, AND WHY", "-" * 88]
        for n in singles:
            out.append(f"  {n}")
            out.append(_para(SINGLE_PIN_NETS.get(n, "no reason on file"), indent="    "))
    out += ["", "REFERENCE DESIGNATORS", "-" * 88]
    for ref in sorted(parts, key=lambda s: (s.rstrip("0123456789"), len(s), s)):
        out.append(f"  {ref:<10} {len(parts[ref]):>3} pins used")
    return "\n".join(out) + "\n"


def constraint_note(b, nets, budget):
    n = b["name"]
    out = [
        f"{n} Rev {b['rev']} -- board constraints, zoning and area budget",
        f"TI One Voice research programme -- CC BY-SA 4.0 -- generated {DATE} by {GEN}",
        "",
        "1.  WHAT THIS DIRECTORY IS",
        "",
        _para("It is the part of the fixture board that does not need a layout engineer: "
              "outline, mounting holes, zoning and keep-out artwork, panel legend, the "
              "non-plated drill programme, and the complete netlist. It is NOT a "
              "fabrication set. There is no copper, no via, no plated drill, no paste and "
              "no assembly drawing, and none of those can be derived from JIG-EEG-009."),
        "",
        _para("The reason is stated rather than left to be discovered: laying out "
              f"{budget['relays']} relays and {budget['resistors']} precision resistors on "
              "two layers with a driven guard pour under the low-level tracks is a "
              "person's job, and the one dimension the placement turns on -- the land "
              "pattern of the Omron G6K-2F-Y -- is a datasheet this package does not "
              "carry. Section 4 below computes what that land pattern has to be for the "
              "outline to be feasible at all."),
        "",
        "2.  STACK-UP AND RULES",
        "",
        f"  Outline           {b['w']:.1f} x {b['h']:.1f} mm     ({b['source']})",
        f"  Layers            {b['layers']} (this is the FIXTURE's board and has nothing to do",
        "                    with the carrier's four-layer stack-up -- section 1.9)",
        f"  Base material     FR-4 Tg >= 150 C, {b['thickness']:.2f} mm, 1 oz copper",
        f"  Finish            {b['finish']}, {b['mask']} mask, {b['legend']}",
        "  Class             IPC-6012 class 2, IPC-A-600 class 2",
        f"  Minimum track     {b['min_track']:.2f} mm",
        f"  Minimum clearance {b['min_gap']:.2f} mm",
        f"  Mounting          4 x M3, {b['mount_d']:.1f} mm non-plated, "
        f"{b['mount_keepout_d']:.1f} mm keep-out, at "
        + ", ".join(f"({x:.0f}, {y:.0f})" for x, y in b["mount"]),
        "  Origin            bottom-left, Y up, matching tools/gerber.py",
        "",
        "3.  ZONES",
        "",
    ]
    for (x0, y0, x1, y1, cap, note) in b["zones"]:
        out.append(f"  x {x0:6.1f} .. {x1:6.1f}   y {y0:5.1f} .. {y1:5.1f}   {cap}")
        out.append(f"{'':>32}{note}")
    if b["can"]:
        x0, y0, x1, y1 = b["can"]
        out += ["",
                f"  Screening can     {x1 - x0:.1f} x {y1 - y0:.1f} mm tinplate, soldered on "
                "four sides, over",
                f"                    x {x0:.1f}..{x1:.1f}, y {y0:.1f}..{y1:.1f}. "
                "JIG-EEG-009 section 1.8 gives the can as",
                "                    60 x 40 x 15 mm; the 60 mm side is placed along Y here so "
                "that it",
                "                    fits the 40 mm-wide x band section 1.9 allots it."]
    out += ["", "4.  AREA BUDGET", "",
            _para("Computed, not asserted. The question it answers is whether the outline "
                  "can hold the bill of materials at all, because a board that cannot is a "
                  "board nobody should be asked to lay out."),
            ""]
    for row in budget["rows"]:
        out.append(f"  {row}")
    out += ["", _para(budget["verdict"]), "",
            "5.  RULES THE LAYOUT MUST MEET", ""]
    if n == "FIX-01":
        out += [
            _para("a. No switch contact in either leg of either ratio network "
                  "(section 1.3). A relay contact of 100 mOhm in the 20.0 Ohm bottom leg "
                  "is a 0.5 % ratio error; the same contact in a channel network sits "
                  "against 1.59 MOhm and is invisible."),
            "",
            _para("b. The SRC bus and the sixteen channel tracks are top-layer only, each "
                  "inside a 0.5 mm gap from the GUARD pour, with the bottom layer beneath "
                  "them being GUARD and not FIX_COM (section 1.9)."),
            "",
            _para("c. GUARD stops 2 mm short of every shroud, so the guard never leaves "
                  "the box on a cable (section 1.9)."),
            "",
            _para("d. FIX_COM reaches the DUT at exactly one point, J106 way 2 "
                  "(section 1.11). It is not bonded to the enclosure anywhere on the "
                  "board; the single box bond is an M3 stud at the cable-entry corner."),
            "",
            _para("e. RP1, the readback pull-up of section 8.4, is a 10.0 kOhm 0.1 % part "
                  "from M1.GP11 to the CD74HC4067 common. It is inside the logic zone and "
                  "its track must not run beside a channel track: it is switched, and a "
                  "capacitive path from it into a channel node injects the switching edge "
                  "into a protected input."),
        ]
    else:
        out += [
            _para("a. 500 V DC creepage. Every conductor that can carry the insulation "
                  "tester's output -- the instrument bus, the twenty-four relay common "
                  "and normally-open contacts and J404 way 1 -- keeps at least 3.0 mm of "
                  "creepage and clearance to every other conductor and to the mounting "
                  "holes. That is this file's rule, taken as the pollution-degree-2 "
                  "figure for 500 V DC on FR-4, and it must be checked against the "
                  "clearance table of the standard the programme's safety review adopts. "
                  "WH-EEG-008 H4 and H10 are what put 500 V on this card."),
            "",
            _para("b. The common bus is a bus and not a plane: every relay's "
                  "normally-closed contact reaches it, and it leaves the board on J404 "
                  "way 2 only. It is not bonded to DGND anywhere on the board, because "
                  "the insulation measurement is between two floating groups and a bond "
                  "to the controller's ground would put the controller inside the "
                  "measurement."),
            "",
            _para("c. The lid interlock switch reaches M3 directly and does not pass "
                  "through the relay matrix. An interlock routed through the thing it "
                  "protects is not an interlock."),
        ]
    out += ["", "6.  WHAT A LAYOUT CONTRACTOR IS BEING ASKED FOR", "",
            _para("Schematic capture from the netlist in this directory, land patterns "
                  "from the manufacturers' datasheets, placement inside the zones of "
                  "section 3, two-layer routing to the rules of section 5, and a "
                  "fabrication set in the house style of kicad/gerber/ -- Gerber X2, 4.6 "
                  "metric, bottom-left origin, plus an Excellon drill programme and an "
                  "IPC-D-356A netlist for bare-board test. JIG-EEG-009 section 6.1 "
                  "carries the labour line and section 6.3 the days."),
            ""]
    return "\n".join(out) + "\n"


def pcb_readme(b, files, budget):
    n = b["name"]
    lines = [
        f"{n} Rev {b['rev']} -- fixture board data",
        f"TI One Voice research programme -- CC BY-SA 4.0",
        f"Generated {DATE} by {GEN}.  Regenerate with: python3 tools/fixture_gen.py --pcb",
        "",
        "READ THIS FIRST",
        "",
        _para("THIS IS NOT A FABRICATION SET.  There is no copper layer, no plated drill "
              "programme, no solder-paste layer and no assembly drawing in this "
              "directory, and a board fabricated from what is here would be a bare piece "
              "of FR-4 with four holes in it.  What is here is everything about the board "
              "that JIG-EEG-009 determines: the outline, the mounting pattern, the "
              "zoning, the panel legend, the non-plated drill and the complete netlist.  "
              "The copper is a layout engineer's work and is priced in JIG-EEG-009 "
              "section 6.1 and scheduled in section 6.3."),
        "",
        "FILES",
        "",
    ]
    for f in files:
        p = os.path.join(OUT, "pcb", n, f)
        lines.append(f"  {f:<38} {os.path.getsize(p):>7} bytes  "
                     f"{sha256(p)}")
    lines += [
        "",
        "LAYER MAP",
        "",
        f"  {n}-Edge_Cuts.gbr        board outline, profile on the centre line",
        f"  {n}-F_Silkscreen.gbr     panel legend, zone captions, the two bench warnings",
        f"  {n}-Zoning.gbr           zone boundaries, keep-outs, screening can, connector",
        "                              way-1 marks.  A mechanical layer, not copper.",
        f"  {n}-NPTH.drl             four M3 mounting holes.  No plated programme exists.",
        f"  {n}_netlist.txt          the connectivity, human-readable",
        f"  {n}_netlist.json         the same connectivity, machine-readable",
        f"  {n}_constraints.txt      stack-up, rules, zoning and the area budget",
        "",
        "GERBER CONVENTIONS",
        "",
        _para("Gerber X2, format 4.6 absolute, metric, leading zeros omitted, bottom-left "
              "origin with Y up -- the same %FSLAX46Y46*% / %MOMM*% pair EEG-CAR-01 and "
              "WH-BUS-01 use, so one CAM import setting covers every board in this "
              "package.  Every file carries a TF.FileFunction attribute and a G04 line "
              "saying it is not a fabrication set."),
        "",
        "AREA BUDGET",
        "",
    ]
    for row in budget["rows"]:
        lines.append(f"  {row}")
    lines += ["", _para(budget["verdict"]), ""]
    return "\n".join(lines) + "\n"


# =======================================================================================
# Section 4.  The area budget, computed.
# =======================================================================================
def area_budget(b, nets, relay_env=RELAY_ENV_MM2):
    refs = set()
    for pins in nets.values():
        for p in pins:
            refs.add(p.split(".")[0])
    relays = len([r for r in refs if r.startswith("K") and r[1:].isdigit()])
    resistors = len([r for r in refs if r[0] == "R" and r != "RP1"]) + \
        (1 if "RP1" in refs else 0)
    socs = len([r for r in refs if r.startswith("U")])
    hdr_ways = sum(w for (_r, _x, _y, w, _n) in CONNECTORS[b["name"]])

    board = b["w"] * b["h"]
    a_relay = relays * relay_env
    a_res = resistors * R0603_MM2
    a_soc = socs * IC_SOIC20W_MM2
    a_pico = PICO_MM2
    a_hdr = hdr_ways * HDR_PER_WAY_MM2
    a_can = ((b["can"][2] - b["can"][0]) * (b["can"][3] - b["can"][1])) if b["can"] else 0.0
    used = a_relay + a_res + a_soc + a_pico + a_hdr
    free = board - used
    # A two-layer board with the SRC bus and sixteen channel tracks on the top layer only
    # needs routing channel, not just free area.  60 % occupancy is the working figure this
    # file uses for a two-layer board of this density; it is a rule of thumb and is stated
    # as one, not as a standard.
    limit = 0.60 * board
    feasible = used <= limit
    max_env = (limit - (a_res + a_soc + a_pico + a_hdr)) / relays if relays else 0.0

    rows = [
        f"board area                      {board:9.0f} mm2  "
        f"({b['w']:.1f} x {b['h']:.1f})",
        f"{relays:3d} relays at {relay_env:5.1f} mm2 each  {a_relay:9.0f} mm2  "
        "ASSUMED envelope, not a datasheet figure",
        f"{resistors:3d} resistors, 0603            {a_res:9.0f} mm2",
        f"{socs:3d} integrated circuits        {a_soc:9.0f} mm2  SOIC-20W nominal",
        f"  1 controller module          {a_pico:9.0f} mm2  Raspberry Pi Pico outline",
        f"{hdr_ways:3d} connector ways            {a_hdr:9.0f} mm2",
        f"    total occupied              {used:9.0f} mm2  "
        f"{100.0 * used / board:.0f} % of the board",
        f"    free                        {free:9.0f} mm2",
    ]
    if a_can:
        rows.append(f"    of which inside the can     {a_can:9.0f} mm2  "
                    "shared with the relay and resistor counts above")
    if feasible:
        verdict = (
            f"VERDICT: feasible at the assumed envelope. The outline carries the bill of "
            f"materials at {100.0 * used / board:.0f} % occupancy against a 60 % working "
            f"limit for a two-layer board of this density. The largest relay land-pattern "
            f"envelope the outline can carry is {max_env:.1f} mm2, so the fitted relay's "
            f"land pattern must be at or under that -- roughly "
            f"{math.sqrt(max_env * 10.0 / 7.0):.1f} x "
            f"{math.sqrt(max_env * 7.0 / 10.0):.1f} mm at the aspect ratio assumed here. "
            f"That is the number to check against the Omron G6K-2F-Y datasheet before any "
            f"layout is commissioned, and it is the only datasheet figure the outline "
            f"depends on.")
        margin = 100.0 * (max_env - relay_env) / relay_env
        if margin < 10.0:
            verdict += (
                f"  THE MARGIN IS {margin:.1f} %.  A board that closes only if the relay "
                f"is at or under the size assumed for it is a board that does not close "
                f"if the assumption is 2 mm out on one axis, so this outline is "
                f"provisional until the datasheet is opened -- and FIX-01's enclosure, "
                f"the Hammond 1590D at 188 x 119 mm, has room for a larger board if it "
                f"needs one.")
    else:
        verdict = (
            f"VERDICT: NOT feasible at the assumed envelope. The bill of materials needs "
            f"{used:.0f} mm2 against a {limit:.0f} mm2 working limit, so the outline in "
            f"JIG-EEG-009 section 1.9 cannot carry it and either the outline or the "
            f"relay has to change. The largest relay land-pattern envelope that would fit "
            f"is {max_env:.1f} mm2.")
    return dict(rows=rows, verdict=verdict, feasible=feasible, relays=relays,
                resistors=resistors, used=used, board=board, max_env=max_env)


# =======================================================================================
# Section 5.  The printed fixture parts.
# =======================================================================================
# cadquery is imported inside build_mech() so that --pcb and --check run on a machine that
# does not have it.  The pattern -- one parametric model exported as both STEP and STL,
# with the identity stamped into both headers -- is tools/mech_gen.py's, and the reasons
# for it are in that file's docstring.

# FIX-01/E manifold.  The eight sites are the fixture's own: the LEDs are IN the manifold
# (section 1.7), so nothing about the helmet's geometry reaches it and the pitch is chosen
# for the indexed slide rather than copied from anywhere.
E_PITCH = 20.0          # site pitch along the slide
E_SITES = 8
E_CAL = 1               # one further index position, the reference-card position
E_CHAN_W = 24.0         # light chamber width
E_CHAN_D = 12.0         # light chamber depth
E_WALL = 3.0
E_LED_D = 5.2           # 5 mm through-hole LED body, 0.2 mm clearance
E_LED_FLANGE_D = 6.4    # the moulded flange under a 5 mm LED
E_APERTURE_D = 4.0      # what the chamber sees of each site
E_RAIL = 4.0            # slide rail thickness

# FIX-02 couplers.  The cavity volumes are JIG-EEG-009 section 2.2's; the diameters are
# chosen and the depths are DERIVED from them, so the volume is arithmetic and not a claim.
A_CAV_CM3 = 2.0
A_CAV_D = 16.0
B_CAV_CM3 = 3.5
B_CAV_D = 20.0
DRIVER_D = 13.0         # "13 mm mylar driver", section 2.2
MIC_PORT_D = 10.0       # the reference electret bore; see the note in fix02a()

# FIX-03/A nest.  Every dimension here is JIG-EEG-009 section 3.3's or design.py's.
NEST_MARGIN = 15.0
NEST_T = 12.0
NEST_RECESS = 2.5
CARRIER_MH = [(5.0, 5.0), (145.0, 5.0), (5.0, 125.0), (145.0, 125.0)]

ENGRAVE_FONT = "DejaVu Sans"
ENGRAVE_DEPTH = 0.4


def _cav_depth(vol_cm3, d):
    """Depth of a cylindrical cavity of the required volume.  Rounded to 0.01 mm, and the
    caller checks the rounded volume against the requirement."""
    return round(vol_cm3 * 1000.0 / (math.pi * (d / 2.0) ** 2), 2)


def build_mech(outdir, verbose=True):
    """Model, export and measure the seven printed fixture parts."""
    import cadquery as cq

    def engrave(part, txt, plane, size=4.0):
        g = cq.Workplane(plane).text(txt, size, -ENGRAVE_DEPTH, combine=False,
                                     font=ENGRAVE_FONT, kind="bold")
        return part.cut(g)

    def face(origin, normal=(0, 0, 1), xdir=(1, 0, 0)):
        return cq.Plane(origin=cq.Vector(*origin), xDir=cq.Vector(*xdir),
                        normal=cq.Vector(*normal))

    # ----------------------------------------------------------------- FIX-01/E body --
    def fix01e_manifold():
        """The light-tight manifold, JIG-EEG-009 sections 1.7 and 1.8.

        A closed channel with one LED per site in its floor and a rebate along the top for
        the sensor carrier.  Light-tightness is a fit and an overlap, not a seal: the
        carrier sits 0.2 mm proud inside a 1.5 mm-deep rebate whose walls stand above the
        chamber, so there is no straight path from outside the manifold to the sensor
        window.  The dark reading of section 1.12 step 5 is what proves it, and the
        acceptance for that reading is already in the document.

        Nine index positions, not eight: the ninth holds the printed reference card of
        section 1.7, so the shift-start check is made without taking the carrier off its
        rail and losing the sensor-to-site geometry that the R/G ratio depends on.
        """
        n = E_SITES + E_CAL
        span = (n - 1) * E_PITCH
        L = span + 2 * (E_CHAN_W / 2.0)
        W = E_CHAN_W + 2 * E_WALL
        H = E_CHAN_D + E_WALL + E_RAIL
        p = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))
        p = p.edges("|Z").fillet(3.0)
        # the chamber
        p = p.cut(cq.Workplane("XY", origin=(0, 0, E_WALL))
                  .rect(span + E_CHAN_W - 2 * E_WALL, E_CHAN_W).extrude(E_CHAN_D))
        # the carrier rebate, 1.5 mm deep and 0.4 mm wider than the carrier
        p = p.cut(cq.Workplane("XY", origin=(0, 0, H - 1.5))
                  .rect(L - 2 * E_WALL, E_CHAN_W + 0.4).extrude(2.0))
        # per-site LED bore and aperture, and a partition between sites
        x0 = -span / 2.0
        for i in range(n):
            x = x0 + i * E_PITCH
            if i < E_SITES:
                p = p.cut(cq.Workplane("XY", origin=(x, 0, -1.0))
                          .circle(E_LED_D / 2.0).extrude(E_WALL + 2.0))
                p = p.cut(cq.Workplane("XY", origin=(x, 0, -1.0))
                          .circle(E_LED_FLANGE_D / 2.0).extrude(1.0 + 1.6))
            else:
                # the reference-card slot, through the end wall into the chamber
                p = p.cut(cq.Workplane("XY", origin=(x, 0, E_WALL + 1.0))
                          .rect(1.2, E_CHAN_W - 2.0).extrude(E_CHAN_D))
            # index notch in the rail top: 2.2 mm below the rebate floor, so the peg
            # bottoms in the rail and never breaks through into the light chamber
            p = p.cut(cq.Workplane("XY", origin=(x, (E_CHAN_W + E_WALL) / 2.0, H - 3.7))
                      .rect(5.0, E_WALL + 0.4).extrude(4.2))
        p = engrave(p, "FIX-01E", face((-span / 2.0 + 6.0, -(W / 2.0), H / 2.0),
                                       normal=(0, -1, 0), xdir=(1, 0, 0)), 4.0)
        return p

    # -------------------------------------------------------------- FIX-01/E carrier --
    def fix01e_carrier():
        """The indexed sensor carrier.

        It holds a TCS34725 breakout over a 6.0 mm window and drops an index peg into one
        of the manifold's nine notches.  The breakout is held the way MP-01 and WH-ADP-02
        hold their modules -- a generous pocket and a grid of M2 clearance holes -- because
        JIG-EEG-009 section 1.8 buys the sensor "on a breakout" and names no breakout, so
        there is no hole pattern to cut.
        """
        L, W, T = 30.0, E_CHAN_W, 6.0
        p = cq.Workplane("XY").box(L, W, T, centered=(True, True, False))
        p = p.edges("|Z").fillet(2.0)
        # sensor window through to the chamber
        p = p.cut(cq.Workplane("XY", origin=(0, 0, -1)).circle(3.0).extrude(T + 2))
        # breakout pocket on top, 24 x 20 x 2.0, taking any breakout up to that size
        p = p.cut(cq.Workplane("XY", origin=(0, 0, T - 2.0)).rect(24.0, 20.0).extrude(3.0))
        for x, y in ((-9.0, -7.0), (-9.0, 7.0), (0.0, 7.0), (9.0, -7.0), (9.0, 7.0)):
            p = p.cut(cq.Workplane("XY", origin=(x, y, -1)).circle(1.1).extrude(T + 2))
        # The index peg.  It OVERLAPS the body in both axes rather than touching it: two
        # solids that meet on a face union into a shell that reports watertight and is
        # not, which is the failure mode tools/mech_gen.py's _one_solid() exists to catch.
        peg = (cq.Workplane("XY", origin=(0, W / 2.0, -2.0))
               .rect(4.8, E_WALL + 3.0).extrude(3.0))
        p = p.union(peg)
        # a finger grip on each end wall, so the carrier is lifted and not levered
        for gx in (-(L / 2.0 - 1.5), (L / 2.0 - 1.5)):
            p = p.cut(cq.Workplane("XY", origin=(gx, 0, T - 1.0))
                      .rect(3.0, 12.0).extrude(2.0))
        return p

    # ------------------------------------------------------------------- FIX-02/A ----
    def fix02a():
        """The voice coupler body, JIG-EEG-009 section 2.2: 2.0 cm3 cavity.

        The cavity is a plain cylinder so that its volume is arithmetic: at a bore of
        16.0 mm the depth for 2.0 cm3 is 2000 / (pi x 8.0^2) = 9.95 mm, and build() prints
        the volume the model actually encloses so the two can be compared.

        The mouth is 10.0 mm and takes the TPU 85A lip, which is where the seal is made.
        It is stated as a PROPOSAL rather than a fit: the boom capsule is AVL-EEG-017 K10,
        "Primo EM272Z1, alternate any 6 mm electret", and the boom nose that carries it
        (HM-07A/B) has no released geometry, so the diameter the lip has to seal on is not
        a known number.  The lip is compliant and covers a range; which range is the
        programme's decision and is recorded in JIG-EEG-009 section 8.9.
        """
        depth = _cav_depth(A_CAV_CM3, A_CAV_D)
        wall = 4.0
        L = depth + wall + 4.0
        p = (cq.Workplane("XY").circle(A_CAV_D / 2.0 + wall).extrude(L)
             .faces(">Z").workplane().hole(A_CAV_D, depth))
        # driver recess in the closed end, from outside
        p = p.faces("<Z").workplane().hole(DRIVER_D + 0.4, 3.0)
        # a 4.0 mm port from the driver recess into the cavity
        p = p.faces("<Z").workplane().hole(4.0, L)
        # the mouth, at 10.0 mm, opening into the cavity
        p = p.faces(">Z").workplane().hole(10.0, 3.0)
        # reference microphone port at 90 degrees to the driver axis, section 2.2
        p = p.cut(cq.Workplane("YZ", origin=(0, 0, wall + depth / 2.0))
                  .circle(MIC_PORT_D / 2.0).extrude(A_CAV_D / 2.0 + wall + 1.0))
        p = engrave(p, "FIX-02A", face((0.0, -(A_CAV_D / 2.0 + wall), 3.0),
                                       normal=(0, -1, 0)), 3.0)
        return p

    def fix02b():
        depth = _cav_depth(B_CAV_CM3, B_CAV_D)
        wall = 4.0
        L = depth + wall + 3.0
        p = (cq.Workplane("XY").circle(B_CAV_D / 2.0 + wall).extrude(L)
             .faces(">Z").workplane().hole(B_CAV_D, depth))
        p = p.faces("<Z").workplane().hole(DRIVER_D + 0.4, 3.0)
        p = p.faces("<Z").workplane().hole(4.0, L)
        p = p.cut(cq.Workplane("YZ", origin=(0, 0, wall + depth / 2.0))
                  .circle(MIC_PORT_D / 2.0).extrude(B_CAV_D / 2.0 + wall + 1.0))
        # gasket seat: an annular recess 1.5 mm deep on the sealing face
        seat = (cq.Workplane("XY", origin=(0, 0, L - 1.5))
                .circle(B_CAV_D / 2.0 + wall).circle(B_CAV_D / 2.0 + 0.5).extrude(2.0))
        p = p.cut(seat)
        p = engrave(p, "FIX-02B", face((0.0, -(B_CAV_D / 2.0 + wall), 3.0),
                                       normal=(0, -1, 0)), 3.0)
        return p

    def lip(inner_d, outer_d, thick=2.5, lip_h=2.0):
        """A TPU 85A sealing lip.  Two of these, one per coupler.

        It is a separate part because it is a separate material: JIG-EEG-009 section 2.4
        specifies "MJF PA12 + TPU 85A lip", and MJF prints one material per build.
        """
        p = (cq.Workplane("XY").circle(outer_d / 2.0).circle(inner_d / 2.0).extrude(thick))
        tip = (cq.Workplane("XY", origin=(0, 0, thick))
               .circle(inner_d / 2.0 + 1.6).circle(inner_d / 2.0).extrude(lip_h))
        return p.union(tip)

    # ------------------------------------------------------------------- FIX-03/A ----
    def fix03a_nest():
        """The flashing and provisioning nest, JIG-EEG-009 section 3.3.

        It holds the 150.0 x 130.0 mm carrier on its four M3 holes.  Section 0.2 item 1
        says a nest cut for the package v1 outline will not accept a Rev B carrier, so the
        outline and the hole pattern come from tools/design.py's BOARD_W and BOARD_H rather
        than from a number typed here.

        The carrier is supported on its edges and on four posts and nowhere else: the
        underside carries through-hole socket tails over most of its area, and a nest that
        touches them presses them while a technician leans on the board to seat a USB
        plug.
        """
        import design as D
        bw, bh = D.BOARD_W, D.BOARD_H
        L, W = bw + 2 * NEST_MARGIN, bh + 2 * NEST_MARGIN
        p = cq.Workplane("XY").box(L, W, NEST_T, centered=(True, True, False))
        p = p.edges("|Z").fillet(5.0)
        # the recess the board drops into, 0.6 mm larger than the board on each axis
        p = p.cut(cq.Workplane("XY", origin=(0, 0, NEST_T - NEST_RECESS))
                  .rect(bw + 0.6, bh + 0.6).extrude(NEST_RECESS + 1.0))
        # the relief pocket under the board: everything but a 10 mm ledge
        p = p.cut(cq.Workplane("XY", origin=(0, 0, NEST_T - NEST_RECESS - 6.0))
                  .rect(bw - 20.0, bh - 20.0).extrude(6.0))
        # four locating posts on the carrier's own M3 pattern
        for x, y in CARRIER_MH:
            px, py = x - bw / 2.0, bh / 2.0 - y
            p = p.union(cq.Workplane("XY", origin=(px, py, NEST_T - NEST_RECESS))
                        .circle(2.9 / 2.0).extrude(NEST_RECESS + 3.5))
        # cable and pigtail reliefs on all four edges, so nothing is trapped under a lead
        for sx in (-1, 1):
            p = p.cut(cq.Workplane("XY", origin=(sx * (L / 2.0 - 4.0), 0, NEST_T - 6.0))
                      .rect(10.0, 40.0).extrude(8.0))
        for sy in (-1, 1):
            p = p.cut(cq.Workplane("XY", origin=(0, sy * (W / 2.0 - 4.0), NEST_T - 6.0))
                      .rect(60.0, 10.0).extrude(8.0))
        # two M3 clearance holes for the sprung USB-C arm of section 3.3.  The arm itself
        # is fabricated, not printed, and is not modelled.
        for x in (-30.0, 30.0):
            p = p.cut(cq.Workplane("XY", origin=(x, W / 2.0 - 8.0, -1))
                      .circle(1.7).extrude(NEST_T + 2))
        p = engrave(p, "FIX-03A", face((0.0, -(W / 2.0), NEST_T / 2.0),
                                       normal=(0, -1, 0)), 5.0)
        return p

    PARTS = [
        ("FIX-01E_colorimeter_manifold", fix01e_manifold),
        ("FIX-01E_sensor_carrier", fix01e_carrier),
        ("FIX-02A_voice_coupler_body", fix02a),
        ("FIX-02A_sealing_lip", lambda: lip(10.0, A_CAV_D + 8.0)),
        ("FIX-02B_room_coupler_body", fix02b),
        ("FIX-02B_sealing_lip", lambda: lip(B_CAV_D, B_CAV_D + 8.0)),
        ("FIX-03A_carrier_nest", fix03a_nest),
    ]

    stl = os.path.join(outdir, "stl")
    step = os.path.join(outdir, "step")
    os.makedirs(stl, exist_ok=True)
    os.makedirs(step, exist_ok=True)
    made = []
    for name, fn in PARTS:
        obj = fn()
        n_solids = len(obj.val().Solids())
        assert n_solids == 1, f"{name} came out as {n_solids} solids, not one"
        solid = obj.val()
        bb = solid.BoundingBox()
        sp = os.path.join(stl, f"{name}.stl")
        tp = os.path.join(step, f"{name}.step")
        cq.exporters.export(obj, sp)
        cq.exporters.export(obj, tp, cq.exporters.ExportTypes.STEP)
        ident = f"{REGISTER[name]['part_id']} {REGISTER[name]['name']} " \
                f"Rev {REGISTER[name]['revision']} -- EEG field kit fixture -- CC BY-SA 4.0"
        _stamp_step(tp, ident)
        _stamp_stl(sp, ident)
        made.append(name)
        if verbose:
            print(f"  {name:34s} {bb.xlen:7.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f} mm "
                  f"{solid.Volume() / 1000.0:8.2f} cm3")
    return made


REGISTER = {
    "FIX-01E_colorimeter_manifold": dict(
        part_id="FIX-01/E", name="light-tight colorimeter manifold", revision="A",
        material="PA12", process="MJF, dyed black -- the inside must not be reflective",
        description="light-tight manifold, eight LED sites at 20.0 mm pitch plus a "
                    "reference-card position, rebate and nine index notches for the "
                    "sensor carrier",
        source="tools/fixture_gen.py fix01e_manifold()"),
    "FIX-01E_sensor_carrier": dict(
        part_id="FIX-01/E", name="indexed sensor carrier", revision="A",
        material="PA12", process="MJF, dyed black",
        description="sliding carrier, 6.0 mm sensor window, pocket for a TCS34725 "
                    "breakout up to 24 x 20 x 2.0 mm, index peg",
        source="tools/fixture_gen.py fix01e_carrier()"),
    "FIX-02A_voice_coupler_body": dict(
        part_id="FIX-02/A", name="voice coupler body", revision="A",
        material="PA12", process="MJF, bead-blast",
        description="2.0 cm3 coupler for the boom capsule, 16.0 mm bore, 13 mm driver "
                    "recess, reference-microphone port at 90 degrees",
        source="tools/fixture_gen.py fix02a()"),
    "FIX-02A_sealing_lip": dict(
        part_id="FIX-02/A", name="voice coupler sealing lip", revision="A",
        material="TPU 85A", process="MJF",
        description="compliant sealing lip, 10.0 mm mouth. The diameter it has to seal "
                    "on is not a known number -- see JIG-EEG-009 section 8.9",
        source="tools/fixture_gen.py lip()"),
    "FIX-02B_room_coupler_body": dict(
        part_id="FIX-02/B", name="room coupler body", revision="A",
        material="PA12", process="MJF, bead-blast",
        description="3.5 cm3 coupler sealing over the POD-P1 4.0 mm acoustic port, "
                    "20.0 mm bore, annular gasket seat",
        source="tools/fixture_gen.py fix02b()"),
    "FIX-02B_sealing_lip": dict(
        part_id="FIX-02/B", name="room coupler gasket ring", revision="A",
        material="TPU 85A", process="MJF",
        description="flat gasket ring with a raised bead, sealing on the pod wall",
        source="tools/fixture_gen.py lip()"),
    "FIX-03A_carrier_nest": dict(
        part_id="FIX-03/A", name="carrier nest", revision="A",
        material="PA12", process="MJF, bead-blast",
        description="flashing and provisioning nest for the 150.0 x 130.0 mm carrier on "
                    "its four M3 holes, edge-supported with a relief pocket",
        source="tools/fixture_gen.py fix03a_nest()"),
}


def _stamp_step(path, ident):
    import re
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    txt, n1 = re.subn(r"FILE_NAME\('[^']*'", f"FILE_NAME('{ident}'", txt, count=1)
    txt, n2 = re.subn(r"PRODUCT\('[^']*',\s*'[^']*'",
                      f"PRODUCT('{ident}',\n  '{ident}'", txt, count=1)
    assert n1 == 1 and n2 == 1, f"STEP header not recognised in {path}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)


def _stamp_stl(path, ident):
    with open(path, "rb") as f:
        head = f.read(84)
    if len(head) < 84:
        return False
    ntri = int.from_bytes(head[80:84], "little")
    if os.path.getsize(path) != 84 + 50 * ntri:
        return False
    stamp = ident.encode("ascii", "replace")[:80].ljust(80, b" ")
    assert not stamp.lower().startswith(b"solid"), ident
    with open(path, "r+b") as f:
        f.write(stamp)
    return True


# =======================================================================================
# Section 6.  Manifest and self-check.
# =======================================================================================
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(outdir):
    """`fixtures/MANIFEST.json`, the same schema mech/MANIFEST.json uses, extended with the
    firmware sources so that a fixture's software can be tied to a build."""
    try:
        import trimesh
    except ImportError:
        trimesh = None
    files = {}
    for root, _dirs, names in os.walk(outdir):
        for fn in sorted(names):
            if fn in ("MANIFEST.json", ".DS_Store") or fn.endswith((".o", ".pyc")):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, outdir)
            if os.sep + "build" + os.sep in os.sep + rel:
                continue
            stem = fn.rsplit(".", 1)[0]
            r = REGISTER.get(stem, {})
            row = {
                "part_id": r.get("part_id", "--"),
                "revision": r.get("revision", "--"),
                "description": r.get("description", "--"),
                "material": r.get("material", "--"),
                "process": r.get("process", "--"),
                "units": "mm/cm3",
                "bytes": os.path.getsize(path),
                "sha256": sha256(path),
                "source": r.get("source", GEN if rel.startswith(("pcb", "stl", "step"))
                                else "hand-written source"),
            }
            if fn.endswith(".stl") and trimesh is not None:
                m = trimesh.load(path)
                row.update({
                    "watertight": bool(m.is_watertight),
                    "bbox_mm": [round(float(v), 2) for v in m.extents],
                    "volume_cm3": round(float(m.volume) / 1000.0, 2),
                    "surface_cm2": round(float(m.area) / 100.0, 1),
                    "triangles": int(len(m.faces)),
                    "step": os.path.exists(os.path.join(outdir, "step", stem + ".step")),
                })
            files[rel] = row
    return {
        "document": "fixtures/MANIFEST.json",
        "generated_by": f"{GEN} manifest()",
        "schema": "PARTS-EEG-019 Rev B OA-2, as mech/MANIFEST.json",
        "units": "mm/cm3",
        "note": "Model figures. No fixture part has been printed and no fixture board has "
                "been fabricated, so no figure here has been verified against hardware. "
                "The pcb/ directories are NOT fabrication sets: they carry no copper "
                "layer. The firmware/ sources are hand-written and are listed here for "
                "their checksums only.",
        "licence": "CC BY-SA 4.0",
        "files": files,
    }


def index_readme(m, budgets):
    lines = [
        "fixtures/ -- test fixture data for JIG-EEG-009 Rev B",
        "TI One Voice research programme (one.witysk.org), Brussels, Belgium",
        "Licence: CC BY-SA 4.0",
        f"Generated {DATE} by {GEN}, except firmware/, which is hand-written source.",
        "",
        "WHAT IS HERE",
        "",
        _para("JIG-EEG-009 Rev B designs four fixtures and prices them. Three things it "
              "called for had no files: the fixture printed circuit boards, the printed "
              "fixture parts, and the controller firmware. This directory is those three."),
        "",
        "  firmware/        M1, M2 and M3 controller firmware, and the FIXPROTO v1 host",
        "                   protocol of JIG-EEG-009 section 8. Hand-written C, built for",
        "                   the RP2040 and tested natively -- see firmware/README.md.",
        "  pcb/FIX-01/      board data for the injection fixture.  NOT A FABRICATION SET.",
        "  pcb/FIX-04/      board data for the harness scanner.   NOT A FABRICATION SET.",
        "  step/, stl/      the seven printed fixture parts, one parametric model each.",
        "  MANIFEST.json    every file above with its SHA-256, in the schema",
        "                   mech/MANIFEST.json uses.",
        "",
        "WHAT IS NOT HERE, AND WHY",
        "",
        _para("There is no copper layer for either fixture board. The outline, the "
              "mounting pattern, the zoning, the legend, the non-plated drill and the "
              "complete netlist are released because JIG-EEG-009 determines them; the "
              "copper is not derivable from any document in this package and depends on "
              "one datasheet the package does not carry, the land pattern of the Omron "
              "G6K-2F-Y. Each board's constraints file computes what that land pattern "
              "has to be for its outline to be feasible."),
        "",
        _para("There is no I2S driver in the M2 firmware. The specification the block has "
              "to meet is in the source where the code will go, and the command layer "
              "refuses the tone verbs rather than reporting a start time for a tone "
              "nobody played."),
        "",
        "NOTHING HERE HAS BEEN BUILT",
        "",
        _para("No fixture has been fabricated, printed, assembled or measured, and no "
              "safety engineer has reviewed any of it (JIG-EEG-009 section 7). Every "
              "dimension is a model figure and every constant marked as stated is stated, "
              "not measured."),
        "",
        "AREA BUDGET SUMMARY",
        "",
    ]
    for name, b in budgets.items():
        lines.append(f"  {name}  {b['used']:.0f} of {b['board']:.0f} mm2 "
                     f"({100.0 * b['used'] / b['board']:.0f} %), "
                     f"largest relay land pattern {b['max_env']:.1f} mm2 -- "
                     f"{'feasible' if b['feasible'] else 'NOT FEASIBLE'}")
    lines += ["", "FILES", ""]
    for rel in sorted(m["files"]):
        row = m["files"][rel]
        lines.append(f"  {rel:<52} {row['bytes']:>8}  {row['sha256'][:16]}")
    return "\n".join(lines) + "\n"


def check(verbose=True):
    """Measure what this file describes and report.  Returns (ok, info)."""
    fails, info = [], {}
    for b in BOARDS:
        nets = NETLISTS[b["name"]]()
        bud = area_budget(b, nets)
        info[b["name"]] = bud
        if verbose:
            print(f"\n{b['name']} Rev {b['rev']} -- {b['w']:.1f} x {b['h']:.1f} mm, "
                  f"{b['layers']} layers")
            for row in bud["rows"]:
                print(f"  {row}")
            print(_para(bud["verdict"], indent="  "))
        if not bud["feasible"]:
            fails.append(f"{b['name']}: the bill of materials does not fit the outline")

        # 1. every pin belongs to exactly one net
        seen = {}
        for net, pins in nets.items():
            for p in pins:
                if p in seen:
                    fails.append(f"{b['name']}: {p} is on both {seen[p]} and {net}")
                seen[p] = net
        # 2. no net with a single pin -- a net of one is a wire to nowhere
        singles = [n for n, p in nets.items() if len(p) < 2]
        for s in singles:
            if s not in SINGLE_PIN_NETS:
                fails.append(f"{b['name']}: net {s} has one pin and no reason on file")
        # 3. every relay has a coil net and a driver
        relays = sorted({p.split(".")[0] for pins in nets.values() for p in pins
                         if p.split(".")[0].startswith("K")
                         and p.split(".")[0][1:].isdigit()})
        for k in relays:
            if f"COIL_{k}" not in nets:
                fails.append(f"{b['name']}: {k} has no coil net")
            elif len(nets[f"COIL_{k}"]) != 2:
                fails.append(f"{b['name']}: {k} coil is not a two-pin net")
        # 4. no shift-register drain drives two coils
        drains = [p for n, pins in nets.items() if n.startswith("COIL_")
                  for p in pins if ".DRAIN" in p]
        if len(drains) != len(set(drains)):
            dup = sorted({d for d in drains if drains.count(d) > 1})
            fails.append(f"{b['name']}: shift-register drains drive two coils: {dup}")
        if len(drains) != len(relays):
            fails.append(f"{b['name']}: {len(relays)} relays but {len(drains)} drains")
        # 5. every connector way named in CONNECTORS appears in the netlist
        for (ref, _x, _y, ways, _note) in CONNECTORS[b["name"]]:
            for w in range(1, ways + 1):
                if f"{ref}.{w}" not in seen:
                    fails.append(f"{b['name']}: {ref}.{w} is on the board and on no net")
        # 6. connectors and the can stay inside the outline
        for (ref, x, y, ways, _note) in CONNECTORS[b["name"]]:
            x1 = x + (ways - 1) * 2.54
            if x < 2.0 or x1 > b["w"] - 2.0 or y < 2.0 or y > b["h"] - 2.0:
                fails.append(f"{b['name']}: {ref} runs off the board "
                             f"({x:.1f}..{x1:.1f}, {y:.1f})")
        if b["can"]:
            cx0, cy0, cx1, cy1 = b["can"]
            for (mx, my) in b["mount"]:
                if cx0 - 1 <= mx <= cx1 + 1 and cy0 - 1 <= my <= cy1 + 1:
                    fails.append(f"{b['name']}: the screening can covers the mounting "
                                 f"hole at ({mx}, {my})")

    # 7. the cavity volumes the couplers are specified by
    for label, cm3, d in (("FIX-02/A", A_CAV_CM3, A_CAV_D), ("FIX-02/B", B_CAV_CM3, B_CAV_D)):
        depth = _cav_depth(cm3, d)
        got = math.pi * (d / 2.0) ** 2 * depth / 1000.0
        info[label] = dict(depth=depth, volume=got)
        if verbose:
            print(f"\n  {label} cavity  bore {d:.1f} mm, depth {depth:.2f} mm "
                  f"-> {got:.4f} cm3 against {cm3:.1f} cm3 required")
        if abs(got - cm3) > 0.01:
            fails.append(f"{label}: cavity is {got:.3f} cm3, not {cm3:.1f}")

    # 8. read the emitted Gerbers back and confirm they describe the board we think.
    #    A deliberately independent pass, as tools/wh_bus.py verify_emitted(): the failure
    #    this guards against is artwork that exists as a file and is the wrong shape.
    for b in BOARDS:
        d = os.path.join(PKG, "fixtures", "pcb", b["name"])
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".gbr"):
                continue
            txt = open(os.path.join(d, fn), encoding="utf-8").read()
            for must in ("%FSLAX46Y46*%", "%MOMM*%", "%TF.FileFunction,",
                         "NOT A FABRICATION SET", "M02*"):
                if must not in txt:
                    fails.append(f"{fn}: missing {must}")
            xs, ys = [], []
            for line in txt.splitlines():
                if line.startswith("X") and line.endswith(("D01*", "D02*", "D03*")):
                    body = line.split("D")[0]
                    xp, yp = body[1:].split("Y")
                    xs.append(int(xp) / 1e6)
                    ys.append(int(yp) / 1e6)
            if not xs:
                fails.append(f"{fn}: no coordinates")
                continue
            bb = (min(xs), max(xs), min(ys), max(ys))
            if fn.endswith("Edge_Cuts.gbr"):
                if (round(bb[0], 3), round(bb[1], 3), round(bb[2], 3), round(bb[3], 3)) != \
                        (0.0, b["w"], 0.0, b["h"]):
                    fails.append(f"{fn}: profile {bb} is not the "
                                 f"{b['w']} x {b['h']} board")
            elif bb[0] < -0.01 or bb[1] > b["w"] + 0.01 or \
                    bb[2] < -0.01 or bb[3] > b["h"] + 0.01:
                fails.append(f"{fn}: features at {bb} run outside the profile")
            if verbose:
                print(f"  {fn:<32} x {bb[0]:6.2f}..{bb[1]:6.2f}  "
                      f"y {bb[2]:6.2f}..{bb[3]:6.2f}  {len(xs):5d} coords")
        drl = os.path.join(d, f"{b['name']}-NPTH.drl")
        if os.path.exists(drl):
            hits = [l for l in open(drl, encoding="utf-8").read().splitlines()
                    if l.startswith("X") and "Y" in l]
            if len(hits) != len(b["mount"]):
                fails.append(f"{b['name']}-NPTH.drl has {len(hits)} hits, "
                             f"expected {len(b['mount'])}")

    # 9. every exported mesh is one closed body.  A raised or dropped feature that only
    #    TOUCHES the part unions into a shell that reports watertight in some readers and
    #    not in others, and prints as a loose lump; it is checked here on the released
    #    file rather than trusted from the model.
    stl_dir = os.path.join(PKG, "fixtures", "stl")
    if os.path.isdir(stl_dir):
        try:
            import trimesh
            for fn in sorted(os.listdir(stl_dir)):
                if not fn.endswith(".stl"):
                    continue
                m = trimesh.load(os.path.join(stl_dir, fn))
                if not m.is_watertight:
                    fails.append(f"{fn} is not watertight")
                if verbose:
                    print(f"  {fn:<38} watertight, {m.volume / 1000.0:7.2f} cm3, "
                          f"{len(m.faces):6d} triangles")
        except ImportError:
            if verbose:
                print("  trimesh not installed; mesh check skipped")

    # 10. the RP2040 pin map and this netlist agree, pin by pin.  hal_rp2040.c chooses the
    #     numbers against a board that has not been laid out, so the two are checked
    #     against each other rather than left to drift.
    hal = os.path.join(PKG, "fixtures", "firmware", "src", "hal_rp2040.c")
    if os.path.exists(hal):
        import re as _re
        txt = open(hal, encoding="utf-8").read()
        pins = {m.group(1): int(m.group(2))
                for m in _re.finditer(r"#define\s+(PIN_\w+)\s+(\d+)", txt)}
        expect = {
            "FIX-01": ("M1", {"PIN_SR_SRCK": "SR_SRCK", "PIN_SR_SER": "SR_SER",
                              "PIN_SR_RCK": "SR_RCK", "PIN_SR_G": "SR_G",
                              "PIN_MUX_A0": "MUX_A0", "PIN_MUX_A1": "MUX_A1",
                              "PIN_MUX_A2": "MUX_A2", "PIN_MUX_A3": "MUX_A3",
                              "PIN_MUX_EN": "MUX_EN", "PIN_MUX_PULL": "MUX_PULL",
                              "PIN_I2C_SDA": "I2C_SDA", "PIN_I2C_SCL": "I2C_SCL"}),
            "FIX-04": ("M3", {"PIN_SR_SRCK": "SR_SRCK", "PIN_SR_SER": "SR_SER",
                              "PIN_SR_RCK": "SR_RCK", "PIN_SR_G": "SR_G",
                              "PIN_LID_INTERLOCK": "LID_SW"}),
        }
        for board, (ctrl, want) in expect.items():
            nets = NETLISTS[board]()
            for define, net in want.items():
                if define not in pins:
                    fails.append(f"hal_rp2040.c has no {define}")
                    continue
                pin = f"{ctrl}.GP{pins[define]}"
                if net not in nets or pin not in nets[net]:
                    fails.append(f"{board}: hal_rp2040.c puts {define} on GP{pins[define]} "
                                 f"but the netlist does not have {pin} on {net}")
            if verbose:
                print(f"  {board} pin map: {len(want)} controller pins agree with "
                      f"hal_rp2040.c")
    else:
        fails.append("fixtures/firmware/src/hal_rp2040.c is missing")

    # 11. the firmware's relay map and this file's netlist agree on the chain
    fw = os.path.join(PKG, "fixtures", "firmware", "src", "fix_m1.c")
    if os.path.exists(fw):
        src = open(fw, encoding="utf-8").read()
        if "10 - (k - 1) / 8" not in src:
            fails.append("fix_m1.c relay_byte() no longer matches the chain map used here")
        if "#define CHAIN_BYTES   11" not in src:
            fails.append("fix_m1.c does not use an eleven-device chain")
    else:
        fails.append("fixtures/firmware/src/fix_m1.c is missing")
    fw3 = os.path.join(PKG, "fixtures", "firmware", "src", "fix_m3.c")
    if os.path.exists(fw3):
        src3 = open(fw3, encoding="utf-8").read()
        if "2 - (c - 1) / 8" not in src3:
            fails.append("fix_m3.c ch_byte() no longer matches the chain map used here")
        if "#define CHAIN_BYTES     3" not in src3:
            fails.append("fix_m3.c does not use a three-device chain")
    else:
        fails.append("fixtures/firmware/src/fix_m3.c is missing")

    if verbose:
        print()
        for f in fails:
            print(f"  FAIL: {f}")
        print(f"  {'PASS' if not fails else str(len(fails)) + ' FAILURES'}")
    return (not fails), info


# =======================================================================================
# Section 7.  Emit.
# =======================================================================================
def emit_pcb(quiet=False):
    budgets = {}
    for b in BOARDS:
        n = b["name"]
        d = os.path.join(OUT, "pcb", n)
        os.makedirs(d, exist_ok=True)
        nets = NETLISTS[n]()
        bud = area_budget(b, nets)
        budgets[n] = bud
        files = {
            f"{n}-Edge_Cuts.gbr": edge_cuts(b),
            f"{n}-F_Silkscreen.gbr": silkscreen(b),
            f"{n}-Zoning.gbr": zoning(b),
            f"{n}-NPTH.drl": drill_npth(b),
            f"{n}_netlist.txt": netlist_text(b, nets),
            f"{n}_netlist.json": json.dumps(
                {"board": n, "revision": b["rev"], "generated_by": GEN,
                 "note": "Pins are named by function. This is connectivity only: there is "
                         "no copper layer for this board.",
                 "licence": "CC BY-SA 4.0", "nets": nets}, indent=1) + "\n",
            f"{n}_constraints.txt": constraint_note(b, nets, bud),
        }
        for name, txt in files.items():
            with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
                fh.write(txt)
        with open(os.path.join(d, "README_fixture_pcb_data.txt"), "w",
                  encoding="utf-8") as fh:
            fh.write(pcb_readme(b, sorted(files), bud))
        if not quiet:
            print(f"  {n}: {len(files) + 1} files, {len(nets)} nets, "
                  f"{sum(len(v) for v in nets.values())} pins -> "
                  f"{os.path.relpath(d, PKG)}/")
    return budgets


def main(argv):
    quiet = "--quiet" in argv
    want_pcb = "--pcb" in argv or not any(a in argv for a in ("--pcb", "--mech", "--check"))
    want_mech = "--mech" in argv or not any(a in argv for a in ("--pcb", "--mech", "--check"))

    if "--check" in argv:
        ok, _ = check(verbose=not quiet)
        return 0 if ok else 1

    if want_pcb:
        if not quiet:
            print("PCB data")
        budgets = emit_pcb(quiet)
    else:
        budgets = {b["name"]: area_budget(b, NETLISTS[b["name"]]()) for b in BOARDS}

    if want_mech:
        if not quiet:
            print("Printed parts")
        build_mech(OUT, verbose=not quiet)

    ok, _info = check(verbose=not quiet)
    if not ok:
        print("self-check failed; the data above is written but is not consistent",
              file=sys.stderr)

    m = manifest(OUT)
    with open(os.path.join(OUT, "MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, indent=1)
        f.write("\n")
    with open(os.path.join(OUT, "README_fixture_data_index.txt"), "w",
              encoding="utf-8") as f:
        f.write(index_readme(m, budgets))
    if not quiet:
        print(f"\n  {len(m['files'])} files listed in fixtures/MANIFEST.json")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
