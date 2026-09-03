#!/usr/bin/env python3
"""
wh_bus.py -- fabrication data for WH-BUS-01, the contact-light bus board.

WH-BUS-01 is the 14.0 x 10.0 x 0.80 mm board that sits at frame node N1, immediately
inside occipital entry OE-2, and splits LED_V from WH-02 into the eight tails that reach
the second lead of each site LED.  It is the reason there is no crimp splice anywhere in
the kit.  PARTS-EEG-019 Rev B registered it, gave it a size and a pad count, and recorded
that "no Gerber set has been generated for it".  This file is that Gerber set.

WHAT THIS FILE IS, AND WHAT IT DELIBERATELY IS NOT

It is self-contained on purpose.  It imports nothing from design.py, gerber.py, pcbgen.py
or router.py, and it writes only into kicad/wh-bus-01/.  The carrier EEG-CAR-01 is a
211-part four-layer board that needs a router and a DRC; WH-BUS-01 is ten pads and one
copper bar, and running it through the carrier's toolchain would buy nothing and couple two
things that have no reason to be coupled.  The header conventions, the 4.6 metric format,
the aperture-function attributes and the bottom-left origin are copied from the carrier's
output so that a CAM operator sees one house style across both boards.

WHAT THE DESIGN HAD TO DECIDE, AND ON WHAT EVIDENCE

  No series resistors.  WH-EEG-008 section 3.2 puts R70 to R77, 1 kOhm each, on the
  CARRIER, one per LEDn line, between the 74HC595 outputs at J19.8-15 and the cable; LED_V
  is the common and reaches the cable through R78, 0 ohm.  The drive current of
  (3.3 - 2.0) / 1000 = 1.3 mA per site is already set there.  A resistor on this board
  would be a second limit in the same loop and would change a current that three documents
  already quote.  So: ten pads, one net, no components, exactly as PARTS-EEG-019 registers
  it.  The eight-way split is a copper bar, not eight resistors.

  Ten pads, not ten pad pairs.  The eight tails are single conductors -- WH-EEG-008
  section 3.2, table WH-02T-1 to -8, one GY/BK conductor each, running beside its own LEDn
  conductor in channel B.  Only the input is a pair, and only in the sense that WH-02
  conductors 9 (LED_V) and 10 (LED_GND) both land here.  Pad 10 is an island connected to
  nothing.

  Two copper layers, where the register says single-layer.  The pads are plated through
  holes, and plating needs two layers.  A 28 AWG 7/0.1 mm conductor soldered to a
  surface-only pad on a 0.8 mm board is held by the pad's peel strength alone, inside a
  helmet, under a cover strip, for the service life of the kit; through the board and
  soldered on both sides it is held by the barrel.  The second layer also doubles the bus
  copper for nothing.  PARTS-EEG-019's "single-layer FR-4" wording is superseded by this
  file and needs re-issuing; that is an open item, recorded in WH-EEG-008 section 3.2.1.

  1.60 mm pad, 0.80 mm finished hole.  The pad diameter is PARTS-EEG-019's registered
  figure and is not changed.  The hole is derived from the conductor it takes: the WH-02
  conductor is 7/0.1 mm tinned copper, about 0.30 mm over the strand bundle (WH-EEG-008
  section 4), and 0.80 mm leaves 0.25 mm all round for tinning and solder.  The resulting
  0.40 mm annular ring is well past the 0.15 mm the carrier works to.  It is not the
  carrier's 1.00 mm socket-strip hole, because nothing is shared between the two drill
  programmes and 1.00 mm would only mean more solder.

Nothing here has been fabricated or measured.  The clearances, the annular ring and the
copper-to-edge figures below are computed by this file from its own geometry and printed by
--check; the V-score web thickness, the solderability and the panel yield are the
fabricator's and are unverified.

Usage:  python3 tools/wh_bus.py              emit into kicad/wh-bus-01/ and self-check
        python3 tools/wh_bus.py --check      self-check only, emit nothing
        python3 tools/wh_bus.py --quiet      emit, print only failures

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import hashlib
import math
import os
import sys
import textwrap
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
OUT = os.path.join(PKG, "kicad", "wh-bus-01")

PROJECT = "WH-BUS-01"
REV = "A"
DATE = "2026-09-01"          # same issue date as the rest of package v2.1
PROJECT_ID = hashlib.md5(PROJECT.encode()).hexdigest()   # same scheme as EEG-CAR-01

# --------------------------------------------------------------------------------------
# Geometry.  All coordinates are FABRICATION coordinates: origin at the bottom-left board
# corner, Y up, millimetres.  There is no y_out = 130.0 - y_design conversion here because
# there is no design.py source for this board -- it is laid out directly in the frame the
# Gerber, the drill file and the netlist all use.
# --------------------------------------------------------------------------------------
BOARD_W = 14.0               # PARTS-EEG-019 Rev B, WH-BUS-01 row
BOARD_H = 10.0               # ditto
BOARD_T = 0.80               # ditto

PAD_D = 1.60                 # PARTS-EEG-019: "ten 1.6 mm solder pads"
HOLE_D = 0.80                # derived from the 7/0.1 mm conductor, see the docstring
MASK_EXPAND = 0.051          # per side; the package's mask rule, from EEG-CAR-01-F_Mask
BUS_W = 1.20                 # LED_V bar; 10.4 mA total needs nothing like this, the width
                             # is for the solder joints and for handling, not for current
SILK_W = 0.15                # matches the 0.150 mm legend aperture on the carrier

# Pad grid: two rows of five on a 2.70 x 4.80 mm pitch.  The left column is the WH-02 input
# pair (conductors 9 and 10, which are neighbours in the cable lay-up, so they land as
# neighbours here).  The other eight are the tails, numbered in the WH-02 conductor order.
ROW_HI, ROW_LO = 7.40, 2.60
COL = [1.80, 4.50, 7.20, 9.90, 12.60]

# (pad number, x, y, net, shape, what lands on it)
PADS = [
    (1,  COL[1], ROW_HI, "LED_V",   "round",  "tail WH-02T-1 to the Fz LED, lead B"),
    (2,  COL[2], ROW_HI, "LED_V",   "round",  "tail WH-02T-2 to the Cz LED, lead B"),
    (3,  COL[3], ROW_HI, "LED_V",   "round",  "tail WH-02T-3 to the Pz LED, lead B"),
    (4,  COL[4], ROW_HI, "LED_V",   "round",  "tail WH-02T-4 to the C3 LED, lead B"),
    (5,  COL[1], ROW_LO, "LED_V",   "round",  "tail WH-02T-5 to the C4 LED, lead B"),
    (6,  COL[2], ROW_LO, "LED_V",   "round",  "tail WH-02T-6 to the T7 LED, lead B"),
    (7,  COL[3], ROW_LO, "LED_V",   "round",  "tail WH-02T-7 to the T8 LED, lead B"),
    (8,  COL[4], ROW_LO, "LED_V",   "round",  "tail WH-02T-8 to the F7 LED, lead B"),
    (9,  COL[0], ROW_HI, "LED_V",   "square", "WH-02 conductor 9, GY/BK, LED_V from J30.9"),
    (10, COL[0], ROW_LO, "LED_GND", "round",  "WH-02 conductor 10, BK, LED_GND, J30.10"),
]
PAD = {n: (x, y, net, shape, note) for n, x, y, net, shape, note in PADS}

# The LED_V bar.  Pad 9 feeds the upper row directly; the upper row feeds the lower row
# through the link at x = COL[1].  The link is put at COL[1] rather than at COL[0] so that
# it stays 1.10 mm clear of the isolated LED_GND pad.
TRACKS = [
    ((COL[0], ROW_HI), (COL[4], ROW_HI)),
    ((COL[1], ROW_LO), (COL[4], ROW_LO)),
    ((COL[1], ROW_HI), (COL[1], ROW_LO)),
]

# Legend.  (text, centre x, centre y, cap height).  Bands are the copper-free strips
# between the mask openings: y 8.25-10.0, y 3.45-6.55 and y 0-1.75.
SILK_TOP = [
    ("9",                  COL[0], 8.95, 0.90),
    ("1",                  COL[1], 8.95, 0.90),
    ("2",                  COL[2], 8.95, 0.90),
    ("3",                  COL[3], 8.95, 0.90),
    ("4",                  COL[4], 8.95, 0.90),
    ("WH-BUS-01",             7.00, 5.75, 0.90),
    ("9=LED_V 10=LED_GND",    7.00, 4.35, 0.80),
    ("10",                 COL[0], 0.85, 0.90),
    ("5",                  COL[1], 0.85, 0.90),
    ("6",                  COL[2], 0.85, 0.90),
    ("7",                  COL[3], 0.85, 0.90),
    ("8",                  COL[4], 0.85, 0.90),
]
# Bottom legend is mirrored about x = BOARD_W/2 so that it reads the right way round when
# the board is turned over.  It carries the identity; the top side carries the pad map.
SILK_BOT = [
    ("CC BY-SA 4.0",          7.00, 9.10, 0.80),
    ("WH-BUS-01 REV A",       7.00, 5.75, 0.90),
    ("TI ONE VOICE",          7.00, 4.35, 0.80),
    ("WH-EEG-008 3.2",        7.00, 0.85, 0.80),
]

# Panel.  Phase 1 is 2 units and Phase 2 is 10 kits (RFQ-EEG-001 Rev E section 12), so one
# 20-up array covers both with eight spares and is the whole Phase 1 + Phase 2 buy.
PANEL_COLS, PANEL_ROWS, PANEL_RAIL = 5, 4, 5.0
CORE = 0.71                  # stock FR-4 core; 0.71 + 2 x 35 um copper + mask = 0.80 mm


def _para(text: str, indent: str = "  ", width: int = 90) -> str:
    """Reflow one paragraph.  The notes below are read in a terminal, not a browser."""
    return textwrap.fill(" ".join(text.split()), width=width,
                         initial_indent=indent, subsequent_indent=indent)


def _panel_para(extra: str = "") -> str:
    """The panel sentence, written once, so the README and the note cannot disagree."""
    return _para(
        f"Supplied as a {PANEL_COLS} x {PANEL_ROWS} V-scored array, "
        f"{PANEL_COLS * PANEL_ROWS} up, step {BOARD_W:.1f} x {BOARD_H:.1f} mm, with "
        f"{PANEL_RAIL:.0f} mm rails on all four sides: panel "
        f"{PANEL_COLS * BOARD_W + 2 * PANEL_RAIL:.1f} x "
        f"{PANEL_ROWS * BOARD_H + 2 * PANEL_RAIL:.1f} mm. " + extra)

# --------------------------------------------------------------------------------------
# Stroke font.  Glyphs are polylines on a 0.6 wide x 1.0 tall cell; the advance is 0.8.
# It exists because this file does not import the package's strokefont.py -- see the
# docstring.  It covers only the characters the two legends use, plus the rest of A-Z so
# that a later ECO can change the text without editing a font.
# --------------------------------------------------------------------------------------
_F = {
    " ": [],
    "-": [[(0.05, 0.50), (0.55, 0.50)]],
    "_": [[(0.00, 0.00), (0.60, 0.00)]],
    ".": [[(0.25, 0.00), (0.35, 0.00)]],
    "=": [[(0.05, 0.35), (0.55, 0.35)], [(0.05, 0.65), (0.55, 0.65)]],
    ">": [[(0.05, 0.80), (0.50, 0.50), (0.05, 0.20)]],
    "/": [[(0.00, 0.00), (0.60, 1.00)]],
    ":": [[(0.30, 0.20), (0.30, 0.30)], [(0.30, 0.60), (0.30, 0.70)]],
    "+": [[(0.30, 0.20), (0.30, 0.80)], [(0.00, 0.50), (0.60, 0.50)]],
    "0": [[(0.15, 0.00), (0.45, 0.00), (0.60, 0.15), (0.60, 0.85), (0.45, 1.00),
           (0.15, 1.00), (0.00, 0.85), (0.00, 0.15), (0.15, 0.00)],
          [(0.60, 0.85), (0.00, 0.15)]],
    "1": [[(0.10, 0.80), (0.30, 1.00), (0.30, 0.00)], [(0.05, 0.00), (0.55, 0.00)]],
    "2": [[(0.00, 0.85), (0.15, 1.00), (0.45, 1.00), (0.60, 0.85), (0.60, 0.65),
           (0.00, 0.15), (0.00, 0.00), (0.60, 0.00)]],
    "3": [[(0.00, 1.00), (0.60, 1.00), (0.25, 0.55)],
          [(0.25, 0.55), (0.45, 0.55), (0.60, 0.40), (0.60, 0.15), (0.45, 0.00),
           (0.15, 0.00), (0.00, 0.15)]],
    "4": [[(0.45, 0.00), (0.45, 1.00), (0.00, 0.30), (0.60, 0.30)]],
    "5": [[(0.60, 1.00), (0.00, 1.00), (0.00, 0.55), (0.45, 0.55), (0.60, 0.40),
           (0.60, 0.15), (0.45, 0.00), (0.15, 0.00), (0.00, 0.15)]],
    "6": [[(0.60, 0.85), (0.45, 1.00), (0.15, 1.00), (0.00, 0.85), (0.00, 0.15),
           (0.15, 0.00), (0.45, 0.00), (0.60, 0.15), (0.60, 0.35), (0.45, 0.50),
           (0.15, 0.50), (0.00, 0.35)]],
    "7": [[(0.00, 1.00), (0.60, 1.00), (0.20, 0.00)]],
    "8": [[(0.15, 0.50), (0.00, 0.65), (0.00, 0.85), (0.15, 1.00), (0.45, 1.00),
           (0.60, 0.85), (0.60, 0.65), (0.45, 0.50), (0.15, 0.50), (0.00, 0.35),
           (0.00, 0.15), (0.15, 0.00), (0.45, 0.00), (0.60, 0.15), (0.60, 0.35),
           (0.45, 0.50)]],
    "9": [[(0.00, 0.15), (0.15, 0.00), (0.45, 0.00), (0.60, 0.15), (0.60, 0.85),
           (0.45, 1.00), (0.15, 1.00), (0.00, 0.85), (0.00, 0.65), (0.15, 0.50),
           (0.45, 0.50), (0.60, 0.65)]],
    "A": [[(0.00, 0.00), (0.00, 0.75), (0.30, 1.00), (0.60, 0.75), (0.60, 0.00)],
          [(0.00, 0.40), (0.60, 0.40)]],
    "B": [[(0.00, 0.00), (0.00, 1.00), (0.45, 1.00), (0.60, 0.85), (0.60, 0.65),
           (0.45, 0.50), (0.00, 0.50)],
          [(0.45, 0.50), (0.60, 0.35), (0.60, 0.15), (0.45, 0.00), (0.00, 0.00)]],
    "C": [[(0.60, 0.85), (0.45, 1.00), (0.15, 1.00), (0.00, 0.85), (0.00, 0.15),
           (0.15, 0.00), (0.45, 0.00), (0.60, 0.15)]],
    "D": [[(0.00, 0.00), (0.00, 1.00), (0.40, 1.00), (0.60, 0.80), (0.60, 0.20),
           (0.40, 0.00), (0.00, 0.00)]],
    "E": [[(0.60, 1.00), (0.00, 1.00), (0.00, 0.00), (0.60, 0.00)],
          [(0.00, 0.50), (0.45, 0.50)]],
    "F": [[(0.60, 1.00), (0.00, 1.00), (0.00, 0.00)], [(0.00, 0.50), (0.45, 0.50)]],
    "G": [[(0.60, 0.85), (0.45, 1.00), (0.15, 1.00), (0.00, 0.85), (0.00, 0.15),
           (0.15, 0.00), (0.45, 0.00), (0.60, 0.15), (0.60, 0.45), (0.30, 0.45)]],
    "H": [[(0.00, 0.00), (0.00, 1.00)], [(0.60, 0.00), (0.60, 1.00)],
          [(0.00, 0.50), (0.60, 0.50)]],
    "I": [[(0.00, 1.00), (0.60, 1.00)], [(0.30, 1.00), (0.30, 0.00)],
          [(0.00, 0.00), (0.60, 0.00)]],
    "J": [[(0.60, 1.00), (0.60, 0.15), (0.45, 0.00), (0.15, 0.00), (0.00, 0.15)]],
    "K": [[(0.00, 0.00), (0.00, 1.00)], [(0.60, 1.00), (0.00, 0.45)],
          [(0.20, 0.62), (0.60, 0.00)]],
    "L": [[(0.00, 1.00), (0.00, 0.00), (0.60, 0.00)]],
    "M": [[(0.00, 0.00), (0.00, 1.00), (0.30, 0.60), (0.60, 1.00), (0.60, 0.00)]],
    "N": [[(0.00, 0.00), (0.00, 1.00), (0.60, 0.00), (0.60, 1.00)]],
    "O": [[(0.15, 0.00), (0.45, 0.00), (0.60, 0.15), (0.60, 0.85), (0.45, 1.00),
           (0.15, 1.00), (0.00, 0.85), (0.00, 0.15), (0.15, 0.00)]],
    "P": [[(0.00, 0.00), (0.00, 1.00), (0.45, 1.00), (0.60, 0.85), (0.60, 0.65),
           (0.45, 0.50), (0.00, 0.50)]],
    "Q": [[(0.15, 0.00), (0.45, 0.00), (0.60, 0.15), (0.60, 0.85), (0.45, 1.00),
           (0.15, 1.00), (0.00, 0.85), (0.00, 0.15), (0.15, 0.00)],
          [(0.35, 0.25), (0.60, 0.00)]],
    "R": [[(0.00, 0.00), (0.00, 1.00), (0.45, 1.00), (0.60, 0.85), (0.60, 0.65),
           (0.45, 0.50), (0.00, 0.50)], [(0.30, 0.50), (0.60, 0.00)]],
    "S": [[(0.60, 0.85), (0.45, 1.00), (0.15, 1.00), (0.00, 0.85), (0.00, 0.60),
           (0.15, 0.50), (0.45, 0.50), (0.60, 0.40), (0.60, 0.15), (0.45, 0.00),
           (0.15, 0.00), (0.00, 0.15)]],
    "T": [[(0.00, 1.00), (0.60, 1.00)], [(0.30, 1.00), (0.30, 0.00)]],
    "U": [[(0.00, 1.00), (0.00, 0.15), (0.15, 0.00), (0.45, 0.00), (0.60, 0.15),
           (0.60, 1.00)]],
    "V": [[(0.00, 1.00), (0.30, 0.00), (0.60, 1.00)]],
    "W": [[(0.00, 1.00), (0.15, 0.00), (0.30, 0.60), (0.45, 0.00), (0.60, 1.00)]],
    "X": [[(0.00, 1.00), (0.60, 0.00)], [(0.00, 0.00), (0.60, 1.00)]],
    "Y": [[(0.00, 1.00), (0.30, 0.50), (0.60, 1.00)], [(0.30, 0.50), (0.30, 0.00)]],
    "Z": [[(0.00, 1.00), (0.60, 1.00), (0.00, 0.00), (0.60, 0.00)]],
}


def text_width(s: str, h: float) -> float:
    """Ink width of s at cap height h.  (n-1) advances plus one glyph cell."""
    return (len(s) - 1) * 0.8 * h + 0.6 * h if s else 0.0


def text_strokes(s, cx, cy, h, mirror=False):
    """Polylines for s, centred on (cx, cy).  mirror flips about x = BOARD_W/2."""
    out = []
    x0 = cx - text_width(s, h) / 2.0
    y0 = cy - h / 2.0
    for i, ch in enumerate(s.upper()):
        glyph = _F.get(ch)
        if glyph is None:
            raise KeyError(f"no glyph for {ch!r}; add it to _F")
        ox = x0 + i * 0.8 * h
        for poly in glyph:
            pts = [(ox + px * h, y0 + py * h) for px, py in poly]
            if mirror:
                pts = [(BOARD_W - px, py) for px, py in pts]
            out.append(pts)
    return out


# --------------------------------------------------------------------------------------
# Gerber X2 emission.  Format 4.6 absolute, metric, leading zeros omitted -- the same
# %FSLAX46Y46*% / %MOMM*% pair the carrier uses, so one CAM import setting covers both.
# --------------------------------------------------------------------------------------
def _c(v: float) -> int:
    return int(round(v * 1e6))


def header(function: str, polarity: str, comment: str) -> list:
    return [
        f"%TF.GenerationSoftware,TI One Voice,package_v2.4/tools/wh_bus.py,1.0*%",
        f"%TF.CreationDate,{DATE}T00:00:00+01:00*%",
        f"%TF.ProjectId,{PROJECT},{PROJECT_ID},{REV}*%",
        f"%TF.FileFunction,{function}*%",
        f"%TF.FilePolarity,{polarity}*%",
        "%TF.SameCoordinates,Original*%",
        "%FSLAX46Y46*%",
        "%MOMM*%",
        f"G04 {comment}*",
        f"G04 {PROJECT} Rev {REV} -- TI One Voice research programme*",
        "G04 Licence CC BY-SA 4.0*",
        "G01*",
        "G75*",
        "%LPD*%",
    ]


def apertures(specs: list) -> tuple:
    """specs is [(function, gerber shape string), ...]; returns (lines, {shape: Dcode}).

    func None emits a bare %ADD with no aperture attribute, which is what the package's
    mask layers do -- see EEG-CAR-01-F_Mask.gbr.
    """
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


def flash(x, y):
    return f"X{_c(x)}Y{_c(y)}D03*"


def draw(pts):
    out = [f"X{_c(pts[0][0])}Y{_c(pts[0][1])}D02*"]
    out += [f"X{_c(x)}Y{_c(y)}D01*" for x, y in pts[1:]]
    return out


def pad_shape(shape, d):
    return f"C,{d:.6f}" if shape == "round" else f"R,{d:.6f}X{d:.6f}"


def copper(side: str) -> str:
    fn = "Copper,L1,Top,Signal" if side == "F" else "Copper,L2,Bot,Signal"
    lines = header(fn, "Positive", f"{side}.Cu copper -- LED_V bus and the LED_GND island")
    specs = [("Conductor", f"C,{BUS_W:.6f}"),
             ("ComponentPad", pad_shape("round", PAD_D)),
             ("ComponentPad", pad_shape("square", PAD_D))]
    alines, codes = apertures(specs)
    lines += alines
    lines.append(f"D{codes[f'C,{BUS_W:.6f}']}*")
    for a, b in TRACKS:
        lines += draw([a, b])
    for shape in ("round", "square"):
        hits = [(n, x, y) for n, (x, y, _net, s, _t) in sorted(PAD.items()) if s == shape]
        if not hits:
            continue
        lines.append(f"D{codes[pad_shape(shape, PAD_D)]}*")
        lines += [flash(x, y) for _n, x, y in hits]
    lines.append("M02*")
    return "\n".join(lines) + "\n"


def mask(side: str) -> str:
    fn = "Soldermask,Top" if side == "F" else "Soldermask,Bot"
    d = PAD_D + 2 * MASK_EXPAND
    lines = header(fn, "Negative",
                   f"Solder mask {'Top' if side == 'F' else 'Bot'} "
                   f"({MASK_EXPAND:.3f} mm expansion per side, ten openings, no tenting)")
    alines, codes = apertures([(None, pad_shape("round", d)),
                               (None, pad_shape("square", d))])
    lines += alines
    for shape in ("round", "square"):
        hits = [(x, y) for _n, (x, y, _net, s, _t) in sorted(PAD.items()) if s == shape]
        if not hits:
            continue
        lines.append(f"D{codes[pad_shape(shape, d)]}*")
        lines += [flash(x, y) for x, y in hits]
    lines.append("M02*")
    return "\n".join(lines) + "\n"


def silkscreen(side: str) -> str:
    fn = "Legend,Top" if side == "F" else "Legend,Bot"
    items, mirror = (SILK_TOP, False) if side == "F" else (SILK_BOT, True)
    lines = header(fn, "Positive", f"Silkscreen {'Top' if side == 'F' else 'Bot'}")
    alines, codes = apertures([("Material", f"C,{SILK_W:.6f}")])
    lines += alines
    lines.append(f"D{codes[f'C,{SILK_W:.6f}']}*")
    for s, cx, cy, h in items:
        for poly in text_strokes(s, cx, cy, h, mirror=mirror):
            lines += draw(poly)
    lines.append("M02*")
    return "\n".join(lines) + "\n"


def edge_cuts() -> str:
    lines = header("Profile,NP", "Positive",
                   "Board outline (profile is the centre line)")
    alines, codes = apertures([("Profile", "C,0.100000")])
    lines += alines
    lines.append(f"D{codes['C,0.100000']}*")
    lines += draw([(0.0, 0.0), (BOARD_W, 0.0), (BOARD_W, BOARD_H),
                   (0.0, BOARD_H), (0.0, 0.0)])
    lines.append("M02*")
    return "\n".join(lines) + "\n"


def drill() -> str:
    """Excellon 2, metric, trailing zeros suppressed -- as EEG-CAR-01-PTH.drl."""
    lines = [
        "M48",
        f"; {PROJECT} Rev {REV} -- plated holes",
        "; TI One Voice research programme, CC BY-SA 4.0",
        f"; generated {DATE} from package_v2.4/tools/wh_bus.py",
        "; sizes below are FINISHED hole diameters; add plating allowance for the tool",
        "; one tool, ten hits: the ten harness solder pads.  There are no vias and no",
        "; non-plated holes on this board, so there is no NPTH file.",
        "FMAT,2",
        "METRIC,TZ",
        "; #@! TF.FileFunction,Plated,1,2,PTH",
        f"T01C{HOLE_D:.3f}",
        "%",
        "G90",
        "G05",
        "T01",
    ]
    for n, (x, y, _net, _s, _t) in sorted(PAD.items()):
        lines.append(f"X{x:.3f}Y{y:.3f}")
    lines.append("M30")
    return "\n".join(lines) + "\n"


def ipc356() -> str:
    """IPC-D-356A bare-board netlist.

    Two nets and ten pads, and the whole point of the file is the second net: it is what
    makes a fabricator's flying-probe prove that pad 10 is open to everything else, which
    is the one electrical property of this board that a visual inspection will not catch.
    Coordinates AND hole diameters are in 0.0001 inch.  (EEG-CAR-01's netlist states its
    hole diameters in micrometres while its coordinates are in 0.0001 inch; that mismatch
    is in gerber.py, is not corrected here, and is recorded as an open item.)
    """
    def u(mm):     # 0.0001 inch
        return int(round(mm / 0.00254))

    lines = [
        f"C  IPC-D-356A netlist for {PROJECT} Rev {REV}",
        "C  TI One Voice research programme -- CC BY-SA 4.0",
        "C  units 0.0001 inch, board origin at the bottom-left corner",
        "C  hole diameters are in the same 0.0001 inch units as the coordinates",
        "P  UNITS CUST 0",
        "C  A = access: 1 top, 2 bottom, 3 both.  Every feature here is a plated hole.",
    ]
    for net in ("LED_GND", "LED_V"):
        for n, (x, y, pnet, _s, _t) in sorted(PAD.items()):
            if pnet != net:
                continue
            lines.append(
                "317" + net.ljust(17) + "PAD".ljust(6) + "-" + str(n).ljust(4) + "    "
                + f"D{u(HOLE_D):04d}PA00" + "  "
                + f"X{u(x):+07d}Y{u(y):+07d}"
                + f"X{u(PAD_D):06d}Y{u(PAD_D):06d}R000 S3")
    lines.append("999")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------------------
def placement_note(metrics: dict) -> str:
    rows = []
    for n, (x, y, net, shape, what) in sorted(PAD.items()):
        rows.append(f"  {n:>2}   {net:<8} {x:>6.2f} {y:>6.2f}  {PAD_D:.2f} "
                    f"{'sq' if shape == 'square' else 'rd':<3} {HOLE_D:.2f}   {what}")
    panel_para = _panel_para(
        "One panel is the whole Phase 1 and Phase 2 buy, 2 units plus 10 kits, with eight "
        f"spares. See the README for the alternative if the fabricator will not V-score "
        f"{BOARD_T:.2f} mm material.")
    return f"""{PROJECT} Rev {REV} -- placement and BOM note
generated {DATE} from package_v2.4/tools/wh_bus.py

BOM

  Nothing is fitted to this board.  It carries no resistor, no capacitor, no diode, no
  connector and no fiducial, and there is no CPL file, no paste layer and no stencil,
  because there is no part to place.  The kit BOM line for WH-BUS-01 is the bare board:

    part        qty/kit  description
    ----------- -------- ------------------------------------------------------------
    WH-BUS-01      1     Bare PCB, {BOARD_W:.1f} x {BOARD_H:.1f} x {BOARD_T:.2f} mm, 2 layers, FR-4, ENIG,
                         green mask, white legend both sides, per this data set

  The eight LED series resistors are R70 to R77 on the CARRIER, 1 kOhm each, and the two
  0 ohm links in the common are R78 and R79, also on the carrier (WH-EEG-008 section 3.2).
  Putting a resistor here would add a second limit to the same loop and change the 1.3 mA
  per site that WH-EEG-008, ICD-EEG-006 and TST-EEG-004 all quote.  Do not fit one.

PAD MAP  (fabrication coordinates: origin bottom-left, Y up, millimetres)

  pad  net          x      y   pad  sh hole   what lands on it
  ---- -------- ------ ------ ----- --- ----  --------------------------------------------
{chr(10).join(rows)}

  Pad 9 is square.  That is the only orientation feature on the board: square pad and the
  "9" legend mark the WH-02 input end, which faces occipital entry OE-2.  Fitted the other
  way round the eight tails still reach their LEDs, but the input pair arrives across the
  whole board and the cover strip will not close over the crossing conductors.

  Pad 10 is an island.  It is 1.10 mm from the nearest LED_V copper on both layers and is
  connected to nothing, on either layer, by design: LED_GND is a 0 V guard conductor laid
  in the centre of the WH-02 bundle and it must not become a return path (WH-EEG-008
  section 3.2 and open item 9).  If an ECO ever ties LED_GND to something, the tie is a
  wire link from pad 10, not a new board.

  The eight tails are numbered in WH-02 conductor order, so pad n feeds the second lead of
  the LED whose first lead is WH-02 conductor n.  All eight leave through the same N1 cover
  strip, so the pad order does not constrain the route inside the frame; it exists so that
  a mis-landed tail is visible against the wire list rather than only at the light.

HOW IT IS FITTED

  Hand-soldered, temperature-controlled iron at 320 C, no-clean flux, per WH-EEG-008
  section 8 step 12.  Strip 4.0 mm, tin, feed through from the legend side, solder on both
  sides.  The board is retained by the N1 cover strip and by its own ten solder joints.

  No mounting hole is specified and none is drilled.  There is also no pocket for this
  board in the HM-01 geometry, so where exactly it beds at N1 is not yet defined by any
  drawing -- that is an open item against the mechanical package, not something this data
  set can settle.

PANEL AND DELIVERY

{panel_para}

MEASURED FROM THIS GEOMETRY

  minimum copper to board edge      {metrics['edge']:.2f} mm
  minimum LED_V to LED_GND          {metrics['gnd']:.2f} mm
  annular ring                      {metrics['ring']:.2f} mm
  minimum legend to mask opening    {metrics['silk']:.2f} mm

  These four are computed by wh_bus.py --check from the same numbers that produced the
  Gerbers.  Nothing on this board has been fabricated, soldered or measured.

Licence: CC BY-SA 4.0.
"""


def readme(files: list, metrics: dict) -> str:
    panel_para = _panel_para(
        "The boards abut: the step IS the board size, there is no gap and no rout line "
        "between them. One panel covers Phase 1 (2 units) and Phase 2 (10 kits) with "
        "eight spares, which is the whole current buy.")
    score_para = _para(
        f"V-scoring is possible because the nearest copper is {metrics['edge']:.2f} mm "
        "from the board edge on every side. A fabricator whose rule is 0.80 mm "
        "copper-to-score cannot V-score this layout and should tab-rout instead -- 2.0 mm "
        f"tabs, two per {BOARD_W:.1f} mm edge, five 0.50 mm mouse-bite holes per tab -- "
        "on notice to the programme rather than silently.")
    web_para = _para(
        f"The residual web a V-score leaves in {BOARD_T:.2f} mm material is the "
        f"fabricator's standard and is not specified here. {BOARD_T:.2f} mm is at or near "
        "the lower V-score limit at several houses, so this is the line of the panel spec "
        "most likely to come back as a question. It has not been tried.")
    core = CORE
    digest = []
    for name in sorted(files):
        with open(os.path.join(OUT, name), "rb") as fh:
            digest.append(f"  {hashlib.sha256(fh.read()).hexdigest()}  {name}")
    return f"""{PROJECT} Rev {REV} -- fabrication data manifest
generated {DATE} from package_v2.4/tools/wh_bus.py

WHAT THIS BOARD IS

  The contact-light bus board.  It sits at frame node N1, immediately inside occipital
  entry OE-2 under its own cover strip, and splits LED_V from WH-02 into the eight tails
  that reach the second lead of each site LED.  It replaces what would otherwise have been
  eight crimp splices, and it is the reason WH-EEG-008 can say there is no splice anywhere
  in the kit.  Ten plated pads, one copper bar, no components.

  PARTS-EEG-019 Rev B registered it and recorded that no Gerber set existed.  This is that
  set.  Two things in that register entry are superseded by this data and need re-issuing:
  the board is TWO layers, not single-layer, because the pads are plated through holes; and
  "specified, not built" is now "specified, data released for quotation".

LAYER MAP
  {PROJECT}-F_Cu.gbr           top copper          Copper,L1,Top,Signal
  {PROJECT}-B_Cu.gbr           bottom copper       Copper,L2,Bot,Signal
  {PROJECT}-F_Mask.gbr         top solder mask     Soldermask,Top
  {PROJECT}-B_Mask.gbr         bottom solder mask  Soldermask,Bot
  {PROJECT}-F_Silkscreen.gbr   top legend          Legend,Top
  {PROJECT}-B_Silkscreen.gbr   bottom legend       Legend,Bot
  {PROJECT}-Edge_Cuts.gbr      board profile       Profile,NP
  {PROJECT}-PTH.drl            plated holes, Excellon 2, metric
  {PROJECT}-IPC-D-356A.ipc     netlist for bare-board electrical test

  There is no paste layer, no CPL file and no NPTH file.  Nothing is surface-mounted,
  nothing is placed, and the only holes are the ten plated pads.  Their absence is the
  design, not an omission.

  {PROJECT}_Rev{REV}_gerber_X2.zip holds the nine files above and nothing else, which is
  the same convention EEG-CAR-01 uses.  It is the imaging data only: send this README and
  {PROJECT}_Rev{REV}_placement_and_BOM.txt with it, because the stack-up, the finish and
  the panel are not anywhere in the Gerbers.

FORMAT
  Gerber X2 (RS-274X with file attributes), 4.6 absolute, metric, leading zeros omitted.
  Origin is the BOTTOM-LEFT board corner with Y up, which is also the origin of the drill
  file and of the netlist.  Unlike EEG-CAR-01 there is no top-left design source and so no
  y conversion: this board is laid out directly in fabrication coordinates.

  Both layers are written in board coordinates as seen from the top, as KiCad writes them.
  The bottom legend is mirrored in the data so that it reads correctly on the finished
  board; do not mirror it again.

THE BOARD
  Size                     {BOARD_W:.1f} x {BOARD_H:.1f} mm, rectangular, no cut-outs, no slots
  Layers                   two: L1 signal, L2 signal.  No plane, no pour
  Stack-up                 mask / 35 um L1 / FR-4 core {core:.2f} / 35 um L2 / mask
                           = {BOARD_T:.2f} mm +/- 10 % finished, mask included.  0.71 mm is
                           a stock core; the fabricator may substitute its nearest and hold
                           the finished {BOARD_T:.2f} mm
  Material                 FR-4, Tg >= 150 C, 1 oz (35 um) copper both sides.  Tg 130 would
                           carry this board, but the carrier is already quoted at Tg 150 and
                           one material across both boards is one qualification, not two
  Finish                   ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um, as EEG-CAR-01.
                           Lead-free HASL is acceptable on notice: this is a two-net board
                           with a {metrics['ring']:.2f} mm annular ring and no fine pitch, so
                           coplanarity buys nothing here.  ENIG is specified for shelf life
                           and because the same fabricator is already quoting it
  Mask / legend            green LPI both sides; white legend both sides
  Mask expansion           {MASK_EXPAND:.3f} mm per side, ten openings each side, none tented
  Pads                     ten, {PAD_D:.2f} mm, on a {COL[1] - COL[0]:.2f} x {ROW_HI - ROW_LO:.2f} mm grid.
                           Pad 9 is square and marks the WH-02 input end
  Plated holes             ten, {HOLE_D:.2f} mm finished, one tool.  Aspect ratio {BOARD_T / HOLE_D:.1f}:1
  Annular ring             {metrics['ring']:.2f} mm
  Minimum track            {BUS_W:.2f} mm (the LED_V bar).  Nothing here is near a fabricator's
                           limit; the width is for the solder joints, not for the 10.4 mA
  Minimum clearance        {metrics['gnd']:.2f} mm, LED_V to the LED_GND island
  Copper to board edge     {metrics['edge']:.2f} mm minimum
  Legend to mask opening   {metrics['silk']:.2f} mm minimum
  Class                    IPC-6012 class 2 (fabrication), IPC-A-600 class 2 (bare board)
  Electrical test          100 % to the supplied IPC-D-356A netlist.  This is not optional
                           on this board: the isolation of pad 10 from the LED_V bar is the
                           one property that a visual inspection will not catch
  Conformal coating        none

PANELISATION
{panel_para}

{score_para}

{web_para}

WHAT IS NOT IN THIS DATA SET
  No fabrication drawing.  On a rectangular board with one drill size and no mechanical
  features, this README and the placement note carry everything a drawing would, and a
  drawing that repeats them is one more thing to keep in step.
  No impedance control, no coupon, no cross-section.  Nothing on this board is a
  transmission line; the fastest edge it sees is a 240 Hz phase reversal.
  No pocket, no mounting feature and no location dimension at node N1.  HM-01 has no
  geometry for this board, so where it beds is undefined.  That is an open item against the
  mechanical package.
  No measurement of anything.  Nothing here has been fabricated, soldered or tested.

SHA-256
{chr(10).join(digest)}
"""


# --------------------------------------------------------------------------------------
# Self-check.  Everything below measures the geometry that produced the files above; the
# numbers it prints are the numbers quoted in the README and the placement note.
# --------------------------------------------------------------------------------------
def _seg_pt(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _seg_seg(a, b, c, d):
    return min(_seg_pt(a, c, d), _seg_pt(b, c, d), _seg_pt(c, a, b), _seg_pt(d, a, b))


def _seg_rect(a, b, cx, cy, w, h):
    """Distance from segment ab to the axis-aligned rectangle centred on (cx, cy)."""
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    edges = [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
             ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
    return min(_seg_seg(a, b, e[0], e[1]) for e in edges)


def check(verbose=True):
    """Measure the design and report.  Returns (ok, metrics)."""
    fails, metrics = [], {}

    # copper features as (kind, geometry, net, half-width)
    copper_feats = []
    for n, (x, y, net, shape, _t) in PAD.items():
        copper_feats.append(("pad", (x, y, shape), net))
    for a, b in TRACKS:
        copper_feats.append(("trk", (a, b), "LED_V"))

    def outer(f):
        """Bounding box of one copper feature, outer edge included."""
        kind, g, _net = f
        if kind == "pad":
            x, y, _s = g
            r = PAD_D / 2.0            # square and round share the half-width
            return x - r, x + r, y - r, y + r
        (ax, ay), (bx, by) = g
        r = BUS_W / 2.0
        return min(ax, bx) - r, max(ax, bx) + r, min(ay, by) - r, max(ay, by) + r

    # 1. copper to board edge
    edge = min(min(x0, BOARD_W - x1, y0, BOARD_H - y1)
               for x0, x1, y0, y1 in (outer(f) for f in copper_feats))
    metrics["edge"] = edge
    if edge < 0.30:
        fails.append(f"copper {edge:.3f} mm from the board edge, under 0.30 mm")

    # 2. LED_V to LED_GND, the clearance the whole design turns on
    gx, gy, _n, _s, _t = PAD[10]
    gnd = float("inf")
    for kind, g, net in copper_feats:
        if net != "LED_V":
            continue
        if kind == "pad":
            x, y, _sh = g
            gnd = min(gnd, math.hypot(x - gx, y - gy) - PAD_D)
        else:
            a, b = g
            gnd = min(gnd, _seg_pt((gx, gy), a, b) - PAD_D / 2 - BUS_W / 2)
    metrics["gnd"] = gnd
    if gnd < 0.20:
        fails.append(f"LED_V to LED_GND {gnd:.3f} mm, under the 0.20 mm package minimum")

    # 3. annular ring, and every drill hit inside its pad
    ring = (PAD_D - HOLE_D) / 2.0
    metrics["ring"] = ring
    if ring < 0.15:
        fails.append(f"annular ring {ring:.3f} mm, under the 0.15 mm class 2 minimum")
    if HOLE_D >= PAD_D:
        fails.append("hole is not smaller than the pad")
    if BOARD_T / HOLE_D > 8.0:
        fails.append(f"hole aspect ratio {BOARD_T / HOLE_D:.1f}:1 is beyond 8:1")

    # 4. mask openings do not merge (a sliver of mask between two openings peels)
    mask_d = PAD_D + 2 * MASK_EXPAND
    web = min(math.hypot(PAD[a][0] - PAD[b][0], PAD[a][1] - PAD[b][1]) - mask_d
              for a in PAD for b in PAD if a < b)
    metrics["maskweb"] = web
    if web < 0.10:
        fails.append(f"mask web {web:.3f} mm between openings, under 0.10 mm")

    # 5. legend clear of every mask opening, and inside the board
    silk_min, silk_edge = float("inf"), float("inf")
    for items, mirror in ((SILK_TOP, False), (SILK_BOT, True)):
        for s, cx, cy, h in items:
            for poly in text_strokes(s, cx, cy, h, mirror=mirror):
                for a, b in zip(poly, poly[1:]):
                    for x, y in (a, b):
                        silk_edge = min(silk_edge, x - SILK_W / 2, BOARD_W - x - SILK_W / 2,
                                        y - SILK_W / 2, BOARD_H - y - SILK_W / 2)
                    for _n, (px, py, _net, shape, _t) in PAD.items():
                        if shape == "round":
                            d = _seg_pt((px, py), a, b) - mask_d / 2 - SILK_W / 2
                        else:
                            d = _seg_rect(a, b, px, py, mask_d, mask_d) - SILK_W / 2
                        silk_min = min(silk_min, d)
    metrics["silk"] = silk_min
    metrics["silkedge"] = silk_edge
    if silk_min < 0.15:
        fails.append(f"legend {silk_min:.3f} mm from a mask opening, under 0.15 mm")
    if silk_edge < 0.0:
        fails.append(f"legend runs {-silk_edge:.3f} mm off the board")

    # 6. the net list is what the wire list expects
    if sorted(PAD) != list(range(1, 11)):
        fails.append("pads are not numbered 1 to 10")
    tails = [n for n, (_x, _y, net, _s, _t) in PAD.items() if net == "LED_V" and n <= 8]
    if len(tails) != 8:
        fails.append(f"{len(tails)} LED_V tails, expected 8")
    if PAD[9][2] != "LED_V" or PAD[10][2] != "LED_GND":
        fails.append("pad 9 must be LED_V and pad 10 must be LED_GND (WH-EEG-008 3.2)")

    # 7. every LED_V pad actually reaches pad 9 through copper, walked as a graph
    reach, frontier = {9}, [9]
    while frontier:
        n = frontier.pop()
        nx, ny, _net, _s, _t = PAD[n]
        for a, b in TRACKS:
            if _seg_pt((nx, ny), a, b) > PAD_D / 2 + BUS_W / 2:
                continue
            for m, (mx, my, _net2, _s2, _t2) in PAD.items():
                if m in reach:
                    continue
                if _seg_pt((mx, my), a, b) <= PAD_D / 2 + BUS_W / 2:
                    reach.add(m)
                    frontier.append(m)
    want = {n for n, (_x, _y, net, _s, _t) in PAD.items() if net == "LED_V"}
    if reach != want:
        fails.append(f"LED_V connectivity is {sorted(reach)}, expected {sorted(want)}")

    if verbose:
        print(f"{PROJECT} Rev {REV} -- geometry check")
        print(f"  board                       {BOARD_W:.1f} x {BOARD_H:.1f} x "
              f"{BOARD_T:.2f} mm, 2 layers")
        print(f"  pads                        {len(PAD)} "
              f"({len(want)} on LED_V, 1 isolated on LED_GND)")
        print(f"  copper to board edge        {metrics['edge']:.3f} mm")
        print(f"  LED_V to LED_GND            {metrics['gnd']:.3f} mm")
        print(f"  annular ring                {metrics['ring']:.3f} mm  "
              f"(hole {HOLE_D:.2f}, pad {PAD_D:.2f}, aspect "
              f"{BOARD_T / HOLE_D:.1f}:1)")
        print(f"  mask web between openings   {metrics['maskweb']:.3f} mm")
        print(f"  legend to mask opening      {metrics['silk']:.3f} mm")
        print(f"  legend to board edge        {metrics['silkedge']:.3f} mm")
        print(f"  LED_V connectivity          pad 9 reaches {sorted(reach - {9})}")
        for f in fails:
            print(f"  FAIL: {f}")
        print(f"  {'PASS' if not fails else str(len(fails)) + ' FAILURES'}")
    return (not fails), metrics


def verify_emitted(files, verbose=True):
    """Re-read the files just written and confirm they say what we think.

    This is a deliberately independent pass: it parses the Gerber text back rather than
    trusting the emitter, because the failure this guards against is a board that exists as
    a file and is the wrong shape.
    """
    fails = []
    prof = None
    for name in files:
        if not name.endswith((".gbr",)):
            continue
        txt = open(os.path.join(OUT, name)).read()
        for must in ("%FSLAX46Y46*%", "%MOMM*%", "%TF.FileFunction,",
                     f"%TF.ProjectId,{PROJECT},{PROJECT_ID},{REV}*%", "M02*"):
            if must not in txt:
                fails.append(f"{name}: missing {must}")
        # extents of every coordinate in the file
        xs, ys = [], []
        for line in txt.splitlines():
            if line.startswith("X") and ("D01*" in line or "D02*" in line
                                         or "D03*" in line):
                body = line.split("D")[0]
                xpart, ypart = body[1:].split("Y")
                xs.append(int(xpart) / 1e6)
                ys.append(int(ypart) / 1e6)
        if not xs:
            fails.append(f"{name}: no coordinates")
            continue
        bb = (min(xs), max(xs), min(ys), max(ys))
        if name.endswith("Edge_Cuts.gbr"):
            prof = bb
            if bb != (0.0, BOARD_W, 0.0, BOARD_H):
                fails.append(f"{name}: profile {bb} is not the {BOARD_W} x {BOARD_H} board")
        else:
            if bb[0] < -0.01 or bb[1] > BOARD_W + 0.01 \
               or bb[2] < -0.01 or bb[3] > BOARD_H + 0.01:
                fails.append(f"{name}: features at {bb} run outside the profile")
        if verbose:
            print(f"  {name:<34} x {bb[0]:6.2f}..{bb[1]:6.2f}  "
                  f"y {bb[2]:6.2f}..{bb[3]:6.2f}   {len(xs):4d} coords")

    drl = open(os.path.join(OUT, f"{PROJECT}-PTH.drl")).read()
    hits = [l for l in drl.splitlines() if l.startswith("X") and "Y" in l]
    if len(hits) != len(PAD):
        fails.append(f"drill has {len(hits)} hits, expected {len(PAD)}")
    for l in hits:
        x = float(l[1:l.index("Y")])
        y = float(l[l.index("Y") + 1:])
        if not any(abs(x - px) < 1e-6 and abs(y - py) < 1e-6
                   for px, py, _n, _s, _t in PAD.values()):
            fails.append(f"drill hit {x},{y} is not on a pad")
    ipc = open(os.path.join(OUT, f"{PROJECT}-IPC-D-356A.ipc")).read().splitlines()
    recs = [l for l in ipc if l.startswith("317")]
    if len(recs) != len(PAD):
        fails.append(f"netlist has {len(recs)} records, expected {len(PAD)}")
    if len({l[3:20].strip() for l in recs}) != 2:
        fails.append("netlist does not carry exactly two nets")
    if verbose:
        print(f"  {'drill':<34} {len(hits)} hits, one tool, {HOLE_D:.2f} mm finished")
        print(f"  {'netlist':<34} {len(recs)} records, "
              f"{len({l[3:20].strip() for l in recs})} nets")
        for f in fails:
            print(f"  FAIL: {f}")
    return not fails


def emit(quiet=False):
    os.makedirs(OUT, exist_ok=True)
    ok, metrics = check(verbose=not quiet)
    if not ok:
        print("geometry check failed; nothing written", file=sys.stderr)
        return 1

    files = {
        f"{PROJECT}-F_Cu.gbr": copper("F"),
        f"{PROJECT}-B_Cu.gbr": copper("B"),
        f"{PROJECT}-F_Mask.gbr": mask("F"),
        f"{PROJECT}-B_Mask.gbr": mask("B"),
        f"{PROJECT}-F_Silkscreen.gbr": silkscreen("F"),
        f"{PROJECT}-B_Silkscreen.gbr": silkscreen("B"),
        f"{PROJECT}-Edge_Cuts.gbr": edge_cuts(),
        f"{PROJECT}-PTH.drl": drill(),
        f"{PROJECT}-IPC-D-356A.ipc": ipc356(),
    }
    for name, text in files.items():
        with open(os.path.join(OUT, name), "w") as fh:
            fh.write(text)

    note = f"{PROJECT}_Rev{REV}_placement_and_BOM.txt"
    with open(os.path.join(OUT, note), "w") as fh:
        fh.write(placement_note(metrics))

    if not quiet:
        print(f"\n{PROJECT} Rev {REV} -- emitted files")
    if not verify_emitted(list(files), verbose=not quiet):
        print("emitted data failed its own read-back; do not send it", file=sys.stderr)
        return 1

    zname = f"{PROJECT}_Rev{REV}_gerber_X2.zip"
    with zipfile.ZipFile(os.path.join(OUT, zname), "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(files):
            zi = zipfile.ZipInfo(name, date_time=(2026, 9, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, files[name])

    manifest = sorted(list(files) + [note, zname])
    with open(os.path.join(OUT, "README_layer_map_and_checksums.txt"), "w") as fh:
        fh.write(readme(manifest, metrics))

    if not quiet:
        print(f"\n  wrote {len(manifest) + 1} files to "
              f"{os.path.relpath(OUT, PKG)}/")
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if check()[0] else 1)
    sys.exit(emit(quiet="--quiet" in sys.argv))
