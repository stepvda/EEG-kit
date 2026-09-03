#!/usr/bin/env python3
"""
pad_snap.py -- land every track end inside the pad it is supposed to reach.

WHY THIS EXISTS

fplib gives every through-hole header pin but pin 1 the shape "oval", which at equal
width and height is a CIRCLE -- the KiCad convention, and what kicad_write.py emits.
Two other places disagreed with it:

  pours.py  modelled every non-circular pad as a BOX, so the connectivity check and
            the clearance check both saw a 1.6 mm square where the design has a
            1.6 mm round pad.
  gerber.py apertured it as R,1.6X1.6, so the board would have been FABRICATED with
            square pads.

The corners a square has and a circle does not are 27 % of the pad area, and the
router used them: 373 track ends landed in a corner, outside the round pad.  Under
the square model every net closed (145 of 145); under the round pad that the KiCad
file and the footprint library both describe, 83 nets were open.  The board was
consistent with itself and wrong about its own pads.

With pours.py and gerber.py corrected to the round pad, those track ends no longer
reach.  This pass extends each of them to the pad centre, which is where a track
should end on a through-hole pad anyway.  The copper it adds lies inside the square
that the DRC had already cleared for this net, so it cannot introduce a clearance
violation that the old model would not have caught -- but drc.py is the authority on
that, and it is re-run afterwards rather than trusted here.

Idempotent: an end already inside the pad is left alone.

Usage:  python3 pad_snap.py            report what would move
        python3 pad_snap.py --apply    rewrite routed.pkl
Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import math
import os
import pickle
import sys

import pcbgen
from router import Track

HERE = os.path.dirname(os.path.abspath(__file__))
PKL = os.path.join(HERE, "routed.pkl")


def round_pads(board):
    """The pads fplib calls 'oval' at equal sides -- i.e. the round ones."""
    return [p for p in board.pads()
            if getattr(p, "shape", "") == "oval" and abs(p.w - p.h) < 1e-9]


def snap(tracks, pads, report=None):
    """Add a short entry stub from each stranded track end to its pad centre.

    Returns the number of stubs added.  Only an end that is inside the pad's old
    SQUARE footprint but not fully inside the round pad is served: that is exactly
    the set the model change stranded, and it keeps the pass from dragging in a
    track that merely passes nearby.

    The stub is ADDED, not substituted for the existing end.  Moving the end instead
    rotates the segment it belongs to, and a rotated segment sweeps across whatever
    is beside it: doing that put MISO 0.158 mm from a via of START, against a
    0.20 mm rule, on the first attempt.  An added stub leaves every routed segment
    exactly where the router put it and where the DRC last cleared it.
    """
    by_net = {}
    for pd in pads:
        if pd.net:
            by_net.setdefault(pd.net, []).append(pd)
    stubs = []
    seen = set()
    for t in tracks:
        for pd in by_net.get(t.net, ()):
            half = pd.w / 2.0
            for xa, ya in (("x1", "y1"), ("x2", "y2")):
                ex, ey = getattr(t, xa), getattr(t, ya)
                if abs(ex - pd.x) > half or abs(ey - pd.y) > half:
                    continue
                if math.hypot(ex - pd.x, ey - pd.y) <= half - t.width / 2.0:
                    continue
                key = (round(ex, 4), round(ey, 4), t.layer, t.net)
                if key in seen:
                    continue
                seen.add(key)
                if report is not None:
                    report.append((t.net, f"{pd.ref}.{pd.num}",
                                   math.hypot(ex - pd.x, ey - pd.y) - half))
                stubs.append(Track(t.layer, ex, ey, pd.x, pd.y, t.width, t.net))
    tracks.extend(stubs)
    return len(stubs)


def main(apply=False):
    res = pickle.load(open(PKL, "rb"))
    board = pcbgen.BoardV2()
    pads = round_pads(board)
    report = []
    moved = snap(res["tracks"], pads, report)
    nets = sorted({n for n, _, _ in report})
    print(f"round pads on the board ........ {len(pads)}")
    print(f"track ends short of their pad .. {moved} on {len(nets)} net(s)")
    if report:
        worst = max(d for _, _, d in report)
        print(f"worst shortfall ................ {worst:.3f} mm outside the pad edge")
    if not apply:
        print("\n(dry run -- pass --apply to rewrite routed.pkl)")
        return 0
    pickle.dump(res, open(PKL, "wb"))
    print(f"\nrewrote {PKL}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
