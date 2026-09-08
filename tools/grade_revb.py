#!/usr/bin/env python3
"""
grade_revb.py -- run the ECO-EEG-032 rule set over the RELEASED Rev B routing.

The point is evidence.  ECO-EEG-030 records seven findings from an external layout
engineer who read `kicad/EEG-CAR-01_RevB_routed.kicad_pcb`, declined the review and
advised a redesign, while the programme's own DRC report on that same geometry said
"VIOLATIONS: 0 -- none.  The board passes every rule listed above."  Both statements
were true, because the rule set the report was written against did not contain six of
his seven findings.  This tool measures how many times each of those six occurs in the
released geometry.  A number here is not a regression; it is the reason the rules exist.

**What it grades, and why it is not `design.py`.**  `design.py` has moved on to Rev C:
U1-U3 are TSSOP-14 and four part numbers changed (ECO-EEG-031), so its pads are not the
pads the Rev B copper was routed to.  This tool therefore takes the pads and the copper
from the released artefacts themselves --

    kicad/EEG-CAR-01_RevB_routed.kicad_pcb   footprints, pads, nets, tracks, vias
    tools/routed.pkl                         the reference-plane polygons

-- and grades those.  The two agree on the census by construction and the tool checks
that they do before grading: 3 745 track segments, 552 through vias, four pour islands.

Writes kicad/EEG-CAR-01_RevB_regraded_ECO-EEG-032.txt.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import drc_geometry         # noqa: E402
import kicad_parse          # noqa: E402
import rules                # noqa: E402

PCB = os.path.join(PKG, "kicad", "EEG-CAR-01_RevB_routed.kicad_pcb")
PKL = os.path.join(HERE, "routed.pkl")
OUT = os.path.join(PKG, "kicad", "EEG-CAR-01_RevB_regraded_ECO-EEG-032.txt")


# --------------------------------------------------------------------------- adapters
class _Pad:
    """A kicad_parse.Pad wearing the interface pcbgen.Pad presents, so that
    drc_geometry and pours can read a parsed board without knowing the difference."""

    __slots__ = ("ref", "num", "kind", "shape", "x", "y", "w", "h", "rot", "drill",
                 "layers", "net")

    def __init__(self, p):
        self.ref, self.num, self.kind, self.shape = p.ref, p.num, p.kind, p.shape
        self.x, self.y, self.w, self.h = p.x, p.y, p.w, p.h
        self.rot, self.drill = p.rot, p.drill
        self.layers = tuple(p.layers)
        self.net = p.netname or ""

    @property
    def tht(self):
        return self.kind in ("thru_hole", "np_thru_hole")

    @property
    def plated(self):
        return self.kind == "thru_hole"

    def on(self, layer):
        if self.tht:
            return True
        return any(ly == layer or ly == "*.Cu" for ly in self.layers)

    def size_rot(self):
        q = int(round(self.rot / 90.0)) % 2
        return (self.h, self.w) if q else (self.w, self.h)


class _Part:
    __slots__ = ("ref", "fpname", "pads", "crtyd")

    def __init__(self, fp, pads):
        self.ref, self.fpname, self.pads = fp.ref, fp.lib, pads
        self.crtyd = [(g.pts[0][0], g.pts[0][1], g.pts[1][0], g.pts[1][1], g.width)
                      for g in fp.graphics
                      if g.layer in ("F.CrtYd", "B.CrtYd") and g.kind == "line"
                      and len(g.pts) >= 2]


class _Board:
    def __init__(self, parsed):
        self.parts = []
        for fp in parsed.footprints:
            pads = [_Pad(p) for p in fp.pads]
            self.parts.append(_Part(fp, pads))
        self.width, self.height = D.BOARD_W, D.BOARD_H

    def pads(self):
        for p in self.parts:
            for pd in p.pads:
                yield pd

    def nets(self):
        d = {}
        for pd in self.pads():
            if pd.net:
                d.setdefault(pd.net, []).append(pd)
        return d

    def part(self, ref):
        for p in self.parts:
            if p.ref == ref:
                return p
        return None

    def courtyard_box(self, part):
        xs, ys = [], []
        for seg in part.crtyd:
            xs += [seg[0], seg[2]]
            ys += [seg[1], seg[3]]
        if not xs:
            for pd in part.pads:
                w, h = pd.size_rot()
                xs += [pd.x - w / 2 - 0.2, pd.x + w / 2 + 0.2]
                ys += [pd.y - h / 2 - 0.2, pd.y + h / 2 + 0.2]
        return (min(xs), min(ys), max(xs), max(ys))


def load():
    parsed = kicad_parse.load(PCB)
    board = _Board(parsed)
    d = pickle.load(open(PKL, "rb"))
    tracks, vias, pours = d["tracks"], d["vias"], d["pours"]
    # the released census, from DSN-EEG-003 section 3.4
    assert len(tracks) == 3745, f"routed.pkl has {len(tracks)} segments, not 3745"
    assert len(vias) == 552, f"routed.pkl has {len(vias)} vias, not 552"
    assert len(parsed.segments) == 3745, \
        f"the board file has {len(parsed.segments)} segments, not 3745"
    assert len(parsed.vias) == 552, f"the board file has {len(parsed.vias)} vias, not 552"
    return board, tracks, vias, pours


def main():
    board, tracks, vias, pours = load()
    npads = sum(1 for _ in board.pads())
    nets = board.nets()
    print(f"Rev B as released: {len(board.parts)} designators, {npads} pads, "
          f"{len(nets)} nets, {len(tracks)} segments, {len(vias)} vias")

    v, stats = drc_geometry.run_all(board, tracks, vias, pours, max_report=25)

    order = ["vias inside an SMD pad",
             "dangling track ends",
             "redundant copper loops",
             "sharp inside corners (< 90 deg)",
             "segments off the 45-degree grid",
             "off-centre pad entries",
             "conductors under their class minimum",
             "net classes on a forbidden layer",
             "vias on a class that forbids them"]
    finding = {"vias inside an SMD pad": "1  drills in pads",
               "dangling track ends": "2a net stubs -- antennas",
               "redundant copper loops": "2b redundant copper loops",
               "sharp inside corners (< 90 deg)": "3  sharp inside corners",
               "segments off the 45-degree grid": "3  45-degree routing",
               "off-centre pad entries": "4  off-centre pad entry",
               "conductors under their class minimum": "5  under-width critical nets",
               "net classes on a forbidden layer": "5  net class layer restriction",
               "vias on a class that forbids them": "5  net class via restriction"}

    by_kind = {}
    for kind, msg in v:
        by_kind.setdefault(kind, []).append(msg)

    with open(OUT, "w") as f:
        f.write("EEG-CAR-01 Rev B -- REGRADED against the ECO-EEG-032 rule set\n")
        f.write(f"Generated {D.DATE_C} by tools/grade_revb.py.\n")
        f.write("=" * 78 + "\n\n")
        f.write("WHAT THIS IS\n")
        f.write("  The released Rev B routing, measured against the six geometry rules\n")
        f.write("  the external layout review of ECO-EEG-030 asked for and the rule set\n")
        f.write("  behind kicad/EEG-CAR-01_RevB_DRC_report.txt did not contain.  That\n")
        f.write("  report says VIOLATIONS: 0 and it is not withdrawn: it is correct\n")
        f.write("  about the rules it was given.  The counts below are what those rules\n")
        f.write("  did not look for.\n\n")
        f.write("  Geometry graded:\n")
        f.write(f"    kicad/EEG-CAR-01_RevB_routed.kicad_pcb   "
                f"{len(board.parts)} designators, {npads} pads, {len(nets)} nets\n")
        f.write(f"    tools/routed.pkl                         "
                f"{len(tracks)} segments, {len(vias)} vias, {len(pours)} pour islands\n\n")
        f.write("  Rev C is unrouted, so there is nothing of Rev C's to grade here.\n")
        f.write("  These rules apply to the geometry the layout contractor returns.\n\n")
        f.write("COUNTS\n")
        f.write(f"  {'finding':34s} {'rule':44s} {'count':>7s}\n")
        total = 0
        for k in order:
            n = stats.get(k, 0)
            total += n
            f.write(f"  {finding[k]:34s} {k:44s} {n:7d}\n")
        f.write(f"  {'':34s} {'TOTAL':44s} {total:7d}\n\n")
        f.write("  The redundant-loop line counts LOOPS and the detail below lists one\n")
        f.write("  line per net, so those two numbers differ on purpose. Every other\n")
        f.write("  line counts one occurrence per detail line.\n\n")

        f.write("PER-CLASS RULES IN FORCE (tools/rules.py)\n")
        f.write(f"  {'class':14s} {'nets':>5s} {'w min/pref':>12s} {'clr min/pref':>13s} "
                f"{'layers':>10s} {'vias':>5s}\n")
        for r in rules.summary_table():
            f.write(f"  {r['name']:14s} {r['nets']:5d} "
                    f"{r['min_width']:5.2f}/{r['pref_width']:<6.2f} "
                    f"{r['min_clearance']:6.2f}/{r['pref_clearance']:<6.2f} "
                    f"{r['layers']:>10s} {r['vias']:>5s}\n")
        f.write("\n  Net membership is Rev C's, because the net names did not change:\n")
        f.write("  ECO-EEG-031 moved footprints and part numbers and the netlist is\n")
        f.write("  byte-identical to Rev B's.\n\n")

        f.write("DETAIL\n")
        for kind in sorted(by_kind):
            msgs = by_kind[kind]
            f.write(f"\n  {kind}  ({stats.get(kind, len(msgs))})\n")
            for m in msgs:
                f.write(f"    {m}\n")
            shown = len(msgs)
            got = stats.get(kind, shown)
            if got > shown:
                f.write(f"    ... and {got - shown} more, not listed\n")
        f.write("\nNothing in this package has been manufactured or measured.\n")

    print(f"\n{'finding':34s} {'count':>7s}")
    for k in order:
        print(f"  {finding[k]:32s} {stats.get(k, 0):7d}")
    print(f"  {'TOTAL':32s} {sum(stats.get(k, 0) for k in order):7d}")
    print("\nwrote", os.path.relpath(OUT, PKG))
    return stats


if __name__ == "__main__":
    main()
