#!/usr/bin/env python3
"""
rules.py -- the layout rule set for EEG-CAR-01, as data, in one place.

Every rule here exists in two places and is written down once.  It is checked on real
geometry by `tools/drc.py`, so a board that comes back from a layout contractor can be
graded; and it is exported as KiCad constraints by `kicad_dru()` and
`kicad_pro_settings()`, so the contractor's engineer works under it while drawing.
Neither side is maintained by hand.

Where the rules come from:

  * DSN-EEG-003 section 3.2 -- board, stack-up, vias, minimum track and clearance,
    electrode-net clearance, mounting holes.
  * DSN-EEG-003 section 3.3 -- zoning at x = 62 mm, the star points, electrode nets on
    L1 with the plane continuous beneath, the isolation keep-out, the USB pair, no via
    inside the analogue module connector outlines.
  * ECO-EEG-032 -- the seven findings of the external layout review (ECO-EEG-030), six
    of which are geometry rules this programme's router was never given.

**Three of the rules below are new constraints and not transcriptions**: the per-class
minimum widths, the pad-entry rule and the angle rule.  `NetClass.confirm` names the
COLUMNS of a row that are proposals rather than figures read out of a governing
document, and LAY-EEG-034 section 5 prints them per column.

The electrode layer and via restriction was carried here as a proposal until 9 September
2026 and is not one: DSN-EEG-003 section 3.3 rule 3 puts these nets on L1 with the plane
continuous beneath them, in those words.  It is reclassified as a requirement under
ECO-EEG-034, with `ELECTRODE.cites` naming the source.  What remains a proposal in that
row is the width pair alone -- no governing document fixes a width for the electrode
class, which was checked against the whole document set before the reclassification.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import sys
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import design as D          # noqa: E402

COPPER_LAYERS = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")
SIGNAL_LAYERS = ("F.Cu", "B.Cu")
PLANE_LAYERS = ("In1.Cu", "In2.Cu")

# --------------------------------------------------------------------------- board floor
# DSN-EEG-003 section 3.2.  These are the absolute floors: no net class may go below
# them, and a class may be stricter.
MIN_TRACK = 0.20
MIN_CLEARANCE = 0.20
PREFERRED_TRACK = 0.25
EDGE_CLEARANCE = 0.25
NPTH_CLEARANCE = 2.00
MIN_ANNULAR = 0.15
MIN_HOLE = 0.30

VIA = dict(pad=0.60, drill=0.30, through_only=True, tented=True)


# --------------------------------------------------------------------------- net classes
@dataclass
class NetClass:
    name: str
    min_width: float
    pref_width: float
    min_clearance: float
    pref_clearance: float
    layers: tuple = COPPER_LAYERS      # layers a track of this class may use
    vias_allowed: bool = True
    why: str = ""
    # Which COLUMNS of this row are proposals of this programme rather than figures
    # transcribed from a governing document.  A tuple and not a flag, because a row can
    # be part transcription and part proposal: ELECTRODE's clearance, layer and via
    # restriction are DSN-EEG-003 section 3.3 rule 3, and only its widths are ours.
    # Valid members: "width", "clearance", "layers", "vias".
    confirm: tuple = ()
    cites: str = ""                    # the governing document for the rest of the row
    nets: set = field(default_factory=set)

    def __post_init__(self):
        bad = set(self.confirm) - {"width", "clearance", "layers", "vias"}
        if bad:
            raise ValueError(f"{self.name}: unknown confirm column(s) {sorted(bad)}")


def _led_nets():
    return {f"LED{i}" for i in range(1, 9)} | {
        "LED_V", "LED_PWM", "LED_SR_DATA", "LED_SR_CLK", "LED_SR_LATCH",
        "LED_MR", "LED_OE", "SR_Q7"}


LED_DRIVE_NETS = _led_nets()
ANALOGUE_REF_NETS = set(D.POWER_A_NETS)          # AGND_REF, AVDD, AVSS, AVDD2, AVSS2
POWER_NETS = set(D.POWER_D_NETS)                 # DVDD3V3, DGND, VBAT, VSYS, V5V, VBUS_*
DIGITAL_NETS = (set(D.DIGITAL_ONLY_NETS) - POWER_NETS - set(D.USB_NETS)
                - LED_DRIVE_NETS)

CLASSES = [
    NetClass(
        "ELECTRODE", 0.25, 0.30, 0.35, 0.40,
        layers=("F.Cu",), vias_allowed=False, confirm=("width",),
        cites="DSN-EEG-003 section 3.3 rule 3",
        nets=set(D.ELECTRODE_NETS),
        why="Patient-connected. **The clearance, the layer and the via restriction are "
            "requirements, not proposals.** DSN-EEG-003 section 3.3 rule 3 reads: every "
            "electrode net is routed on L1 with the reference plane continuous beneath "
            "it, at 0.35 mm clearance to any other net rather than 0.20 mm. The 0.35 mm "
            "is transcribed from that sentence and from the electrode-net clearance row "
            "of section 3.2; L1-only is transcribed from it word for word; and the via "
            "prohibition follows from both halves of it, because a net routed wholly on "
            "L1 has no via to place and a via would break the plane it is routed over. "
            "It is achievable -- the harness socket J14, the R/D/C protection rows and "
            "the module sockets J2/J4/J23/J29 are all on the top side. **What IS a "
            "proposal is the width pair**, and only that: no governing document fixes a "
            "width for these nets. Section 3.2 gives the board a 0.20 mm floor and a "
            "0.25 mm preferred width and says nothing about the electrode class. The "
            "0.25 mm minimum is set above the board floor because Rev B only reached "
            "0.20 mm on these nets by relaxing, and a patient-connected conductor is the "
            "last place to spend the last 0.05 mm. Current is not the constraint: these "
            "carry microamperes."),
    NetClass(
        "ANALOGUE_REF", 0.30, 0.40, 0.20, 0.30,
        confirm=("width",), nets=ANALOGUE_REF_NETS,
        why="AGND_REF, AVDD, AVSS and the module-2 pair. About 10 mA per rail "
            "(ICD-EEG-006 section 2.1), so 0.20 mm would carry it four times over: the "
            "width is for source impedance and for the mid-rail's noise, not for current. "
            "0.40 mm preferred is what the Rev B router already aimed at."),
    NetClass(
        "POWER", 0.40, 0.80, 0.20, 0.30,
        nets=POWER_NETS,
        why="VSYS, VBAT, V5V, VBUS_CHG, VBUS_IN, DVDD3V3, VDD_ISO, DGND. The worst case "
            "is about 610 mA at J13 (ICD-EEG-006 section 2.7, calculated). On 35 um outer "
            "copper at a 10 C rise, IPC-2221 gives about 1.29 A for 0.40 mm and about "
            "0.89 A for 0.25 mm, so 0.40 mm is the floor with margin and 0.80 mm is the "
            "preferred width the Rev B router already used."),
    NetClass(
        "USB", 0.30, 0.30, 0.35, 0.35,
        layers=("F.Cu",), vias_allowed=False,
        nets=set(D.USB_NETS),
        why="DSN-EEG-003 section 3.3 rule 5, transcribed and not proposed: a 0.30 mm pair "
            "on 0.35 mm spacing on L1 directly over the DGND plane on L2, about 95 ohm "
            "differential. The width is the impedance, so it is a fixed value and not a "
            "minimum; a via would move the reference and is not permitted."),
    NetClass(
        "ANALOGUE", 0.25, 0.25, 0.20, 0.30,
        nets=set(D.ANALOG_NETS),
        why="Envelope-detector nodes, the microphone and headphone paths, the comparator. "
            "Signal nets at high impedance; 0.25 mm is the board's preferred width and "
            "there is no reason for these to be narrower than that."),
    NetClass(
        "LED_DRIVE", 0.25, 0.30, 0.20, 0.25,
        nets=LED_DRIVE_NETS,
        why="1.3 mA per site and 10.4 mA on the LED_V common (ICD-EEG-006 section 2.11, "
            "calculated), so current is nowhere near the constraint. These run to a "
            "harness connector and out of the box, which is the reason not to route them "
            "at the 0.20 mm floor."),
    NetClass(
        "DIGITAL", 0.20, 0.25, 0.20, 0.25,
        nets=DIGITAL_NETS,
        why="SPI, I2S, I2C, SDMMC, UART and the control lines. Logic-level, "
            "milliamperes."),
    NetClass(
        "DEFAULT", 0.20, 0.25, 0.20, 0.25,
        nets=set(),
        why="Everything the classes above do not name: test points, spare ways, "
            "no-connects, the harness screen, the button and reset lines."),
]

BY_NAME = {c.name: c for c in CLASSES}
_ORDER = ("ELECTRODE", "USB", "ANALOGUE_REF", "POWER", "LED_DRIVE", "ANALOGUE", "DIGITAL")


def netclass_of(net):
    """The one mapping from a net name to a class name.  Order matters: a net that is
    in two sets takes the first class in _ORDER, and ELECTRODE wins over everything."""
    for name in _ORDER:
        if net in BY_NAME[name].nets:
            return name
    return "DEFAULT"


def rule_for(net):
    return BY_NAME[netclass_of(net)]


def width_clearance(net):
    """(preferred width, preferred clearance) -- what a router aims for."""
    c = rule_for(net)
    return c.pref_width, c.pref_clearance


def floor(net):
    """(minimum width, minimum clearance) -- what a DRC grades against."""
    c = rule_for(net)
    return c.min_width, c.min_clearance


def class_membership():
    """{class name: [net names]} across every net design.py declares."""
    out = {c.name: [] for c in CLASSES}
    for net in sorted(set(D.N.values())):
        out[netclass_of(net)].append(net)
    return out


# --------------------------------------------------------------------------- areas
# Rule areas.  Each is (name, layers, polygon) with the polygon in design coordinates
# (top-left origin, Y down).  WP5's board writer places these as KiCad rule areas under
# these exact names, and the .kicad_dru rules below refer to them by name.
def _rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


ISOLATION_KEEPOUT = (141.0, 2.0, 150.0, 22.0)     # DSN-EEG-003 section 3.3 rule 4

AREAS = [
    ("ISOLATION_KEEPOUT", COPPER_LAYERS, _rect(*ISOLATION_KEEPOUT),
     "No copper on any layer. The ADuM4160 module's host half sits over this strip; "
     "DSN-EEG-003 section 3.3 rule 4. Enforced against copper EDGES, not centrelines."),
    ("ANALOGUE_ZONE", COPPER_LAYERS, _rect(0.0, 0.0, D.ZONE_SPLIT_X, D.BOARD_H),
     "Analogue side of the x = 62 mm split, DSN-EEG-003 section 3.3 rule 1. No digital "
     "net may enter it. CMP_RAW crosses by design, through R83 and the D23 clamp."),
    ("DIGITAL_ZONE", COPPER_LAYERS, _rect(D.ZONE_SPLIT_X, 0.0, D.BOARD_W, D.BOARD_H),
     "Digital side of the x = 62 mm split. No analogue-zone net may leave the analogue "
     "zone into it."),
]

MOUNTING_KEEPOUTS = [(x, y, D.MOUNTING_KEEPOUT_D / 2.0) for x, y in D.MOUNTING_HOLES]

# DSN-EEG-003 section 3.3 rule 7: no via inside the analogue module connector outlines.
NO_VIA_ZONES = list(D.NO_VIA_ZONES)


# --------------------------------------------------------------------------- geometry
# The seven findings of ECO-EEG-030, as checkable numbers.  Finding 5 is the net-class
# table above; finding 6 is tools/collision_check.py; finding 7 is the native schematic.
GEOMETRY = dict(
    # 1  no via inside an SMD pad
    via_in_pad=True,
    via_to_smd_pad_min=0.15,      # mm, edge of the drill to the edge of the pad
    # 2a  no dangling track end
    dangling_ends=True,
    dangling_tol=0.002,           # mm, how close counts as touching
    # 2b  no second copper path between the same two pads, outside a plane
    redundant_paths=True,
    # 3  45-degree routing, and no angle below 90 degrees between two segments
    min_segment_angle_deg=90.0,
    allowed_axes_deg=(0.0, 45.0, 90.0, 135.0),
    axis_tol_deg=0.5,
    # 4  a track enters a pad through its centre, along the pad's major axis
    pad_entry=True,
    pad_entry_frac=0.25,          # perpendicular miss allowed, as a fraction of the
                                  # pad's MINOR dimension
    # 5  per-class widths: the table above
    # extra, from DSN-EEG-003 section 3.3 rule 3
    electrode_layer_restriction=True,
)

CONFIRM_NOTES = [
    ("ELECTRODE minimum width 0.25 mm", "the board floor is 0.20 mm; this class is held "
     "above it because these are patient-connected conductors"),
    ("ELECTRODE on L1 only, no vias", "DSN-EEG-003 section 3.3 rule 3 read literally. It "
     "constrains the contractor and it is achievable on the present placement"),
    ("ANALOGUE_REF minimum width 0.30 mm", "impedance, not current; 0.20 mm would carry "
     "the 10 mA four times over"),
    ("segment angle floor 90 degrees", "finding 3 as stated. It forbids an acute inside "
     "corner and permits 45- and 90-degree turns"),
    ("pad entry within 25 % of the pad's minor dimension", "finding 4 turned into a "
     "number. There is no number in the finding"),
]


# --------------------------------------------------------------------------- KiCad export
def _mm(v):
    return f"{v:g}mm"


def kicad_dru():
    """The custom design rules file.  One text, loaded by KiCad 8 and KiCad 10 alike.

    **Comments here are `#`, and that is not a style choice.**  Until 9 September 2026
    this function wrote `;;`, and KiCad discards the WHOLE file the moment it meets a
    semicolon comment -- no error, no warning, DRC carrying on as though the file were
    absent.  Measured on KiCad 10.0.6: with `;;` a probe rule that must fire produced
    nothing, and deleting the file changed no result; with `#` the same probe fired.
    So the released Rev C set shipped 37 rules of which KiCad applied none.  That is
    finding 1 of the KiCad 10 re-emission, ECO-EEG-034.  `check_dru()` now refuses a
    semicolon so the defect cannot come back.

    Angle and pad-entry are NOT expressible here.  KiCad has no constraint for either,
    so they are checked by tools/drc.py on the geometry that comes back, and LAY-EEG-034
    section 6 says so against each of them rather than implying KiCad will catch them.
    """
    L = []
    a = L.append
    a("(version 1)")
    a("")
    a("# EEG-CAR-01 Rev C -- custom design rules")
    a("# GENERATED by tools/rules.py from tools/design.py. Do not edit.")
    a(f"# Board {D.BOARD_W:g} x {D.BOARD_H:g} mm, four layers, through vias only.")
    a("# The rule sheet these implement is LAY-EEG-034. Where the two disagree,")
    a("# tools/rules.py governs and both are wrong until regenerated.")
    a("")
    a("# ---------------------------------------------------------------- vias")
    a('(rule "through_vias_only"')
    a("  (constraint disallow buried_via micro_via))")
    a("")
    a('(rule "via_size_fixed"')
    a(f"  (constraint via_diameter (min {_mm(VIA['pad'])}) (opt {_mm(VIA['pad'])}) "
      f"(max {_mm(VIA['pad'])}))")
    a('  (condition "A.Type == \'Via\'"))')
    a("")
    a('(rule "via_hole_fixed"')
    a(f"  (constraint hole_size (min {_mm(VIA['drill'])}) (opt {_mm(VIA['drill'])}) "
      f"(max {_mm(VIA['drill'])}))")
    a('  (condition "A.Type == \'Via\'"))')
    a("")
    a("# finding 1 -- no drill inside a pad.  physical_hole_clearance is used rather")
    a("# than hole_clearance because a via in its own net's pad is the case that has to")
    a("# be caught, and net-aware clearance rules skip it.")
    a('(rule "no_via_in_smd_pad"')
    a(f"  (constraint physical_hole_clearance (min {_mm(GEOMETRY['via_to_smd_pad_min'])}))")
    a('  (condition "A.Type == \'Via\' && B.Type == \'Pad\' && B.Pad_Type == \'SMD\'"))')
    a("")
    a("# ---------------------------------------------------------------- net classes")
    import textwrap
    for c in CLASSES:
        a(f"# {c.name}")
        for line in textwrap.wrap(" ".join(c.why.split()), 74):
            a(f"#   {line}")
        a(f'(rule "width_{c.name}"')
        a(f"  (constraint track_width (min {_mm(c.min_width)}) (opt {_mm(c.pref_width)}))")
        a(f'  (condition "A.NetClass == \'{c.name}\'"))')
        a("")
        a(f'(rule "clearance_{c.name}"')
        a(f"  (constraint clearance (min {_mm(c.min_clearance)}) "
          f"(opt {_mm(c.pref_clearance)}))")
        a(f'  (condition "A.NetClass == \'{c.name}\'"))')
        a("")
        if c.layers != COPPER_LAYERS:
            allowed = " || ".join(f"A.Layer == '{ly}'" for ly in c.layers)
            a(f'(rule "layers_{c.name}"')
            a("  (constraint disallow track)")
            a(f"  (condition \"A.NetClass == '{c.name}' && !({allowed})\"))")
            a("")
        if not c.vias_allowed:
            a(f'(rule "no_vias_{c.name}"')
            a("  (constraint disallow via)")
            a(f'  (condition "A.NetClass == \'{c.name}\'"))')
            a("")
    a("# ---------------------------------------------------------------- areas")
    a("# finding: DSN-EEG-003 section 3.3 rule 4.  Nothing at all inside the strip,")
    a("# on any of the four copper layers.")
    a('(rule "isolation_keepout"')
    a("  (constraint disallow track via zone pad graphic hole footprint)")
    a("  (condition \"A.insideArea('ISOLATION_KEEPOUT')\"))")
    a("")
    a("# DSN-EEG-003 section 3.3 rule 1.  The zone split is a routing rule and not a")
    a("# placement rule: a class may have pads on both sides where the circuit demands")
    a("# it, and CMP_RAW crosses by design through R83 and D23.")
    for cls in ("DIGITAL", "POWER", "LED_DRIVE", "USB"):
        a(f'(rule "zoning_{cls}_out_of_analogue"')
        a("  (constraint disallow track via)")
        a(f"  (condition \"A.NetClass == '{cls}' && A.insideArea('ANALOGUE_ZONE')\"))")
        a("")
    for cls in ("ELECTRODE", "ANALOGUE_REF"):
        a(f'(rule "zoning_{cls}_out_of_digital"')
        a("  (constraint disallow track via)")
        a(f"  (condition \"A.NetClass == '{cls}' && A.insideArea('DIGITAL_ZONE')\"))")
        a("")
    a("# DSN-EEG-003 section 3.3 rule 7: no via under an analogue module connector.")
    for ref, clr in NO_VIA_ZONES:
        a(f'(rule "no_via_under_{ref}"')
        a("  (constraint disallow via)")
        a(f"  (condition \"A.insideArea('NO_VIA_{ref}')\"))")
        a("")
    a("# ---------------------------------------------------------------- board floor")
    a('(rule "edge_clearance"')
    a(f"  (constraint edge_clearance (min {_mm(EDGE_CLEARANCE)}))")
    a("  (condition \"A.Type != 'Zone'\"))")
    a("")
    a('(rule "annular_ring"')
    a(f"  (constraint annular_width (min {_mm(MIN_ANNULAR)})))")
    a("")
    a("# ---------------------------------------------------------------- NOT CHECKED HERE")
    a("# KiCad has no constraint for either of these and neither is expressible above.")
    a("# They are checked by tools/drc.py on the board that comes back, and LAY-EEG-034")
    a("# section 6 says so against each of them:")
    a(f"#   finding 3  no angle below {GEOMETRY['min_segment_angle_deg']:g} degrees "
      f"between two segments of one track,")
    a("#              and every segment on a 0, 45, 90 or 135 degree axis;")
    a(f"#   finding 4  a track enters a pad within "
      f"{GEOMETRY['pad_entry_frac'] * 100:.0f} % of the pad's minor dimension")
    a("#              of the pad centre, measured on the track's centreline.")
    a("# Findings 2a and 2b -- dangling ends and redundant copper loops -- are KiCad")
    a("# BUILT-IN checks and are raised to errors in the .kicad_pro, not here.")
    text = "\n".join(L) + "\n"
    check_dru(text)
    return text


def check_dru(text):
    """Balance the parentheses and count the rules.

    A .kicad_dru with one missing bracket loads as far as the error and silently drops
    every rule after it, which is the failure mode this whole module exists to avoid: a
    contractor working under a rule set that is half there and says nothing.  This is
    called on every emit, so a bracket cannot be lost between here and the file.
    """
    depth, in_str, n_rules = 0, False, 0
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith(";"):
            raise ValueError(
                f"a semicolon comment survives in the .kicad_dru: {line!r}. KiCad "
                f"discards the WHOLE file when it meets one, silently -- see "
                f"ECO-EEG-034, finding 1 of the KiCad 10 re-emission. Comments in "
                f"this file are '#'")
        if line.lstrip().startswith("(rule "):
            if depth != 0:
                raise ValueError(f"a rule opens while {depth} brackets are still open: "
                                 f"{line!r}")
            n_rules += 1
        for ch in line:
            if ch == '"':
                in_str = not in_str
            elif not in_str and ch == "(":
                depth += 1
            elif not in_str and ch == ")":
                depth -= 1
                if depth < 0:
                    raise ValueError(f"unbalanced closing bracket at {line!r}")
    if depth != 0:
        raise ValueError(f".kicad_dru ends with {depth} bracket(s) unclosed")
    if in_str:
        raise ValueError(".kicad_dru ends inside a quoted string")
    if n_rules < 20:
        raise ValueError(f"only {n_rules} rules emitted; the rule set has more than that")
    return n_rules


def kicad_pro_netclasses():
    """The net-class block of a .kicad_pro, as plain data."""
    classes = []
    for c in CLASSES:
        classes.append({
            "name": "Default" if c.name == "DEFAULT" else c.name,
            "clearance": c.pref_clearance,
            "track_width": c.pref_width,
            "via_diameter": VIA["pad"],
            "via_drill": VIA["drill"],
            "microvia_diameter": VIA["pad"],
            "microvia_drill": VIA["drill"],
            "diff_pair_width": 0.30,
            "diff_pair_gap": 0.35,
            "diff_pair_via_gap": 0.35,
            "line_style": 0,
            "pcb_color": "rgba(0, 0, 0, 0.000)",
            "schematic_color": "rgba(0, 0, 0, 0.000)",
            "wire_width": 6,
            "bus_width": 12,
        })
    assignments = {}
    for net in sorted(set(D.N.values())):
        cls = netclass_of(net)
        assignments[net] = "Default" if cls == "DEFAULT" else cls
    return classes, assignments


def summary_table():
    """Rows for LAY-EEG-034 section 5 and for the DRC report header."""
    rows = []
    counts = class_membership()
    for c in CLASSES:
        rows.append(dict(
            name=c.name,
            nets=len(counts[c.name]),
            min_width=c.min_width, pref_width=c.pref_width,
            min_clearance=c.min_clearance, pref_clearance=c.pref_clearance,
            layers=("any" if c.layers == COPPER_LAYERS else "/".join(c.layers)),
            vias="yes" if c.vias_allowed else "NO",
            confirm=c.confirm,
            cites=c.cites,
            why=c.why))
    return rows


if __name__ == "__main__":
    counts = class_membership()
    total = 0
    print(f"{'class':14s} {'nets':>5s} {'w min/pref':>12s} {'clr min/pref':>13s} "
          f"{'layers':>16s} {'vias':>5s}")
    for c in CLASSES:
        n = len(counts[c.name])
        total += n
        lay = "any" if c.layers == COPPER_LAYERS else "/".join(c.layers)
        print(f"{c.name:14s} {n:5d} {c.min_width:5.2f}/{c.pref_width:<6.2f} "
              f"{c.min_clearance:6.2f}/{c.pref_clearance:<6.2f} {lay:>16s} "
              f"{'yes' if c.vias_allowed else 'NO':>5s}"
              + (f"   CONFIRM: {','.join(c.confirm)}" if c.confirm else ""))
    print(f"{'total':14s} {total:5d}")
    if "--dru" in sys.argv:
        print()
        print(kicad_dru())
