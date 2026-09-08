#!/usr/bin/env python3
"""
schlib.py -- the schematic symbol library for EEG-CAR-01, generated.

Two rules run through it.

**No symbol is rotated on a sheet.**  KiCad stores library graphics with Y increasing
UP and schematic sheets with Y increasing DOWN, and a rotation composes the two flips in
a way that is easy to get wrong and, without KiCad here to open the file, impossible to
see wrong.  So where a part is needed both ways there are two symbols -- `R_H` and `R_V`
-- and `emit_kicad_sch.py` places everything at rotation 0.  The cost is a dozen extra
symbols.  The benefit is that a pin's position on the sheet is `(x + lx, y - ly)` with
no cases in it, and the wires land on the pins.

**The connector symbols are generated from the netlist.**  One symbol per reference
designator, its way count and its pin names taken from the `conn()` calls in `design.py`
that ICD-EEG-006 section 1.1 is transcribed from.  A connector symbol whose pin count
disagrees with the ICD is therefore not possible.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import design as D          # noqa: E402
from kicad_sch import LibSymbol   # noqa: E402

# --------------------------------------------------------------------------- passives
def _r(name, horizontal):
    s = LibSymbol(name, "R", "Resistor", hide_pin_names=True)
    if horizontal:
        s.rect(0, -2.54, -1.016, 2.54, 1.016)
        s.pin(1, "1", "~", -5.08, 0, 0)
        s.pin(1, "2", "~", 5.08, 0, 180)
        s.ref_at, s.val_at = (0, 2.2, 0), (0, -3.6, 0)
    else:
        s.rect(0, -1.016, -2.54, 1.016, 2.54)
        s.pin(1, "1", "~", 0, 5.08, 270)
        s.pin(1, "2", "~", 0, -5.08, 90)
        s.ref_at, s.val_at = (2.0, 1.2, 0), (2.0, -1.2, 0)
    return s


def _c(name, horizontal):
    s = LibSymbol(name, "C", "Unpolarised capacitor", hide_pin_names=True)
    if horizontal:
        s.poly(0, [(-0.635, -2.032), (-0.635, 2.032)], 0.508)
        s.poly(0, [(0.635, -2.032), (0.635, 2.032)], 0.508)
        s.pin(1, "1", "~", -5.08, 0, 0, length=4.445)
        s.pin(1, "2", "~", 5.08, 0, 180, length=4.445)
        s.ref_at, s.val_at = (0, 2.8, 0), (0, -3.8, 0)
    else:
        s.poly(0, [(-2.032, 0.635), (2.032, 0.635)], 0.508)
        s.poly(0, [(-2.032, -0.635), (2.032, -0.635)], 0.508)
        s.pin(1, "1", "~", 0, 5.08, 270, length=4.445)
        s.pin(1, "2", "~", 0, -5.08, 90, length=4.445)
        s.ref_at, s.val_at = (2.2, 1.2, 0), (2.2, -1.2, 0)
    return s


def _l():
    s = LibSymbol("FB_H", "L", "Ferrite bead", hide_pin_names=True)
    s.rect(0, -2.54, -1.016, 2.54, 1.016)
    s.poly(0, [(-2.54, 1.016), (2.54, -1.016)], 0.15)
    s.pin(1, "1", "~", -5.08, 0, 0)
    s.pin(1, "2", "~", 5.08, 0, 180)
    s.ref_at, s.val_at = (0, 2.2, 0), (0, -3.6, 0)
    return s


def _fuse():
    s = LibSymbol("PTC_H", "F", "Resettable PTC fuse", hide_pin_names=True)
    s.rect(0, -2.54, -1.016, 2.54, 1.016)
    s.poly(0, [(-2.54, 0), (2.54, 0)], 0.2)
    s.poly(0, [(-1.0, 1.016), (1.0, -1.016)], 0.15)
    s.pin(1, "1", "~", -5.08, 0, 0)
    s.pin(1, "2", "~", 5.08, 0, 180)
    s.ref_at, s.val_at = (0, 2.2, 0), (0, -3.6, 0)
    return s


def _dual_series_v(name, descr):
    """Two diodes in series, common point at pin 3, drawn as a rail clamp.

    BAV99 and PESD5V0S2BT are both used this way: pin 1 to the lower rail, pin 2 to the
    upper rail, pin 3 the signal between them, so the pair clamps the signal into the
    rails.  Drawing it vertically is the point -- the clamp reads as a clamp.
    """
    s = LibSymbol(name, "D", descr)
    s.pin(1, "2", "K2", 0, 7.62, 270)          # upper rail
    s.pin(1, "1", "A1", 0, -7.62, 90)          # lower rail
    s.pin(1, "3", "COM", -6.35, 0, 0)          # signal
    # lower diode: anode at the bottom, cathode at the common node
    s.poly(1, [(-1.27, -3.81), (1.27, -3.81), (0, -1.27), (-1.27, -3.81)], 0.2, "outline")
    s.poly(1, [(-1.27, -1.27), (1.27, -1.27)], 0.3)
    s.poly(1, [(0, -7.62), (0, -3.81)], 0.15)
    # upper diode: anode at the common node, cathode at the top
    s.poly(1, [(-1.27, 1.27), (1.27, 1.27), (0, 3.81), (-1.27, 1.27)], 0.2, "outline")
    s.poly(1, [(-1.27, 3.81), (1.27, 3.81)], 0.3)
    s.poly(1, [(0, 7.62), (0, 3.81)], 0.15)
    s.poly(1, [(0, -1.27), (0, 1.27)], 0.15)
    s.poly(1, [(-6.35, 0), (0, 0)], 0.15)
    s.ref_at, s.val_at = (2.2, 5.0, 0), (2.2, 2.8, 0)
    return s


def _dual_series_h(name, descr):
    """The same pair drawn along the signal path, for the precision rectifier where the
    two diodes are in the path and not across it."""
    s = LibSymbol(name, "D", descr)
    s.pin(1, "1", "A1", -8.89, 0, 0)
    s.pin(1, "2", "K2", 8.89, 0, 180)
    s.pin(1, "3", "COM", 0, -6.35, 90)
    s.poly(1, [(-3.81, -1.27), (-3.81, 1.27), (-1.27, 0), (-3.81, -1.27)], 0.2, "outline")
    s.poly(1, [(-1.27, -1.27), (-1.27, 1.27)], 0.3)
    s.poly(1, [(-8.89, 0), (-3.81, 0)], 0.15)
    s.poly(1, [(3.81, -1.27), (3.81, 1.27), (1.27, 0), (3.81, -1.27)], 0.2, "outline")
    s.poly(1, [(1.27, -1.27), (1.27, 1.27)], 0.3)
    s.poly(1, [(8.89, 0), (3.81, 0)], 0.15)
    s.poly(1, [(-1.27, 0), (1.27, 0)], 0.15)
    s.poly(1, [(0, -6.35), (0, 0)], 0.15)
    s.ref_at, s.val_at = (0, 2.6, 0), (0, -8.4, 0)
    return s


def _opamp_quad():
    """OPA4376, TSSOP-14: four amplifiers and a power unit.

    1 OUTA  2 -INA  3 +INA  4 V+  5 +INB  6 -INB  7 OUTB
    8 OUTC  9 -INC 10 +INC 11 V- 12 +IND 13 -IND 14 OUTD

    Drawn as five units rather than as a fourteen-pin box, because finding 7 of
    ECO-EEG-030 is about a schematic being READABLE and a box is not a circuit.  The
    inverting input is on top, which is what the eight-sheet PDF set drew and what the
    envelope-detector topology reads best as.
    """
    s = LibSymbol("OPA4376", "U", "Quad precision CMOS op-amp, rail-to-rail I/O",
                  keywords="opamp quad")
    units = [(1, "2", "3", "1"), (2, "6", "5", "7"),
             (3, "9", "10", "8"), (4, "13", "12", "14")]
    for u, inv, non, out in units:
        s.poly(u, [(-5.08, 5.08), (-5.08, -5.08), (5.08, 0), (-5.08, 5.08)],
               0.254, "background")
        s.pin(u, inv, "-", -8.89, 2.54, 0)
        s.pin(u, non, "+", -8.89, -2.54, 0)
        s.pin(u, out, "~", 8.89, 0, 180, etype="output")
        s.text(u, -3.6, 2.54, "-", 1.6)
        s.text(u, -3.6, -2.54, "+", 1.6)
    s.rect(5, -3.81, -3.81, 3.81, 3.81)
    s.pin(5, "4", "V+", 0, 6.35, 270, etype="power_in")
    s.pin(5, "11", "V-", 0, -6.35, 90, etype="power_in")
    s.ref_at, s.val_at = (0, 6.6, 0), (0, -6.6, 0)
    return s


def _comparator():
    """TLV3201, SOT-23-5: 1 OUT, 2 V-, 3 +IN, 4 -IN, 5 V+.  One unit, power included,
    because a five-pin part split into two units reads worse than it reads whole."""
    s = LibSymbol("TLV3201", "U", "Push-pull comparator, SOT-23-5")
    s.poly(1, [(-5.08, 5.08), (-5.08, -5.08), (5.08, 0), (-5.08, 5.08)],
           0.254, "background")
    s.pin(1, "4", "-", -8.89, 2.54, 0)
    s.pin(1, "3", "+", -8.89, -2.54, 0)
    s.pin(1, "1", "OUT", 8.89, 0, 180, etype="output")
    s.pin(1, "5", "V+", 0, 8.89, 270, etype="power_in")
    s.pin(1, "2", "V-", 0, -8.89, 90, etype="power_in")
    s.text(1, -3.6, 2.54, "-", 1.6)
    s.text(1, -3.6, -2.54, "+", 1.6)
    s.ref_at, s.val_at = (6.0, 6.6, 0), (6.0, 4.4, 0)
    return s


def _switch():
    s = LibSymbol("SW_PUSH_H", "SW", "Momentary push switch, normally open")
    s.pin(1, "1", "1", -6.35, 0, 0)
    s.pin(1, "2", "2", 6.35, 0, 180)
    s.poly(1, [(-6.35, 0), (-2.54, 0)], 0.15)
    s.poly(1, [(2.54, 0), (6.35, 0)], 0.15)
    s.poly(1, [(-2.54, 1.27), (2.54, 2.54)], 0.2)
    s.poly(1, [(0, 2.54), (0, 4.06)], 0.15)
    s.poly(1, [(-1.9, 4.06), (1.9, 4.06)], 0.3)
    s.circle(1, -2.54, 0, 0.4, "outline")
    s.circle(1, 2.54, 0, 0.4, "outline")
    s.ref_at, s.val_at = (0, 5.6, 0), (0, -2.6, 0)
    return s


def _testpoint():
    s = LibSymbol("TESTPOINT", "TP", "Bare probe pad", hide_pin_names=True)
    s.pin(1, "1", "~", 0, -2.54, 90)
    s.circle(1, 0, 0.9, 0.9, "none")
    s.poly(1, [(0, -2.54), (0, 0)], 0.15)
    s.ref_at, s.val_at = (1.6, 2.4, 0), (1.6, 0.4, 0)
    return s


def _mech(name, descr):
    s = LibSymbol(name, "MH" if "hole" in descr.lower() else "FID", descr)
    s.circle(1, 0, 0, 1.27, "none")
    s.circle(1, 0, 0, 0.5, "outline")
    s.ref_at, s.val_at = (0, 2.6, 0), (0, -2.6, 0)
    return s


# --------------------------------------------------------------------------- power
GROUNDS = {"AGND_REF", "DGND", "HARN_SHIELD", "HP_GND"}


def power_symbol(net):
    s = LibSymbol(f"PWR_{net}", "#PWR", f"Power flag: {net}", power=True,
                  hide_pin_numbers=True)
    if net in GROUNDS:
        s.pin(1, "1", net, 0, 0, 270, length=0, etype="power_in")
        s.poly(1, [(0, 0), (0, -1.27)], 0.15)
        s.poly(1, [(-2.54, -1.27), (2.54, -1.27)], 0.25)
        s.poly(1, [(-1.6, -2.03), (1.6, -2.03)], 0.25)
        s.poly(1, [(-0.7, -2.79), (0.7, -2.79)], 0.25)
        s.ref_at, s.val_at = (0, -4.4, 0), (0, -6.0, 0)
    else:
        s.pin(1, "1", net, 0, 0, 90, length=0, etype="power_in")
        s.poly(1, [(0, 0), (0, 1.27)], 0.15)
        s.poly(1, [(-1.27, 1.27), (1.27, 1.27)], 0.25)
        s.poly(1, [(0, 1.27), (0, 2.54)], 0.15)
        s.circle(1, 0, 2.9, 0.36, "outline")
        s.ref_at, s.val_at = (0, 5.2, 0), (0, 3.6, 0)
    return s


# --------------------------------------------------------------------------- connectors
def _pins_of(ref):
    """{pin number: net name} for one reference designator, from design.py's netlist."""
    out = {}
    for key, net in D.N.items():
        r, _, num = key.rpartition(".")
        if r == ref:
            out[num] = net
    return out


def connector_symbol(ref, side="r"):
    """One symbol per connector, its ways and pin names taken from the netlist.

    `side` says which edge the pins leave from, so a connector drawn at the left of a
    sheet has its pins on the right and one at the right of a sheet has them on the
    left.  Nothing is ever rotated.
    """
    pins = _pins_of(ref)
    ways = D.C[ref]["fp"]
    nums = sorted(pins, key=lambda k: int(k) if k.isdigit() else 0)
    n = len(nums)
    name = f"CONN_{ref}_{side.upper()}"
    s = LibSymbol(name, "J", f"{D.C[ref]['val']} ({ways})")
    half = (n - 1) * 2.54 / 2.0
    w = 6.35
    if side == "r":
        s.rect(1, -w, half + 2.54, 0.0, -half - 2.54)
        for i, num in enumerate(nums):
            y = half - i * 2.54
            s.pin(1, num, pins[num], 5.08, y, 180, length=5.08)
            s.poly(1, [(0.0, y), (-0.9, y)], 0.15)
    else:
        s.rect(1, 0.0, half + 2.54, w, -half - 2.54)
        for i, num in enumerate(nums):
            y = half - i * 2.54
            s.pin(1, num, pins[num], -5.08, y, 0, length=5.08)
            s.poly(1, [(0.0, y), (0.9, y)], 0.15)
    s.ref_at = (0 if side == "r" else 0, half + 4.4, 0)
    s.val_at = (0, -half - 4.4, 0)
    return s


# --------------------------------------------------------------------------- registry
def build():
    """-> {name: LibSymbol} for every symbol the schematic can use."""
    lib = {}

    def add(s):
        lib[s.name] = s
        return s

    add(_r("R_H", True))
    add(_r("R_V", False))
    add(_c("C_H", True))
    add(_c("C_V", False))
    add(_l())
    add(_fuse())
    add(_dual_series_v("D_CLAMP_V", "Dual series diode used as a rail clamp"))
    add(_dual_series_h("D_SERIES_H", "Dual series diode in the signal path"))
    add(_opamp_quad())
    add(_comparator())
    add(_switch())
    add(_testpoint())
    add(_mech("MOUNTING_HOLE", "M3 mounting hole, non-plated"))
    add(_mech("FIDUCIAL", "Global fiducial, 1 mm copper"))
    for net in sorted(set(D.N.values())):
        if net in GROUNDS or net in D.POWER_A_NETS or net in D.POWER_D_NETS:
            add(power_symbol(net))
    for ref in sorted(D.C):
        if not ref.startswith("J"):
            continue
        for side in ("r", "l"):
            add(connector_symbol(ref, side))
    return lib


def pin_xy(libsym, number, x, y, unit=None):
    """Where a pin's connection point lands on the sheet, for a symbol placed at
    (x, y) with NO rotation.  Library Y is up, sheet Y is down."""
    for u, d in libsym.units.items():
        if unit is not None and u != unit:
            continue
        for p in d["pins"]:
            if p.number == str(number):
                return (x + p.x, y - p.y)
    raise KeyError(f"{libsym.name} has no pin {number} in unit {unit}")


if __name__ == "__main__":
    lib = build()
    print(f"{len(lib)} symbols")
    for k in sorted(lib):
        s = lib[k]
        npins = sum(len(d["pins"]) for d in s.units.values())
        print(f"  {k:28s} units={s.n_units()} pins={npins}")
