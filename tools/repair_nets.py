#!/usr/bin/env python3
"""
repair_nets.py -- re-route the nets a SMALL netlist change broke, and persist the result.

WHY THIS EXISTS, AND WHY IT IS NOT rerun_subset.py

`rerun_subset.py` is the fast inner loop for asking "would this close?", and it
deliberately never writes `routed.pkl`, so that the shipped artefact has exactly one
producer and cannot drift from `design.py`.  That is the right rule for an experiment.

It is the wrong rule for a two-net change to a finished board.  On 2 September 2026
`design.py` moved D11 and C11 from `BIAS_EL` to `BIASOUT` -- the fix that takes a
single-fault current on the forehead electrode from 183.6 uA to 41.2 uA -- and that
changed four pad-to-net assignments and nothing else.  Two nets went open; 143 of 145
were untouched.  A full `build_board.py` run on that input took 30 minutes and came back
with **63 of 145 connected**: the router re-solved the whole board from scratch, made
different global choices, and finished far worse than the board it started from.  The
result was discarded.

So this tool exists to do the small thing: load the finished board, route ONLY the
connections that the netlist change opened, rebuild the reference pours against the new
copper, run the full design-rule check, and write `routed.pkl` **only if the board came
out at least as good as it went in**.  It refuses to write otherwise, which is the whole
point -- the failure mode being guarded against is a repair that silently makes the board
worse, and that is exactly what the full rebuild did.

    python3 repair_nets.py              report what it would do
    python3 repair_nets.py --apply      write routed.pkl if, and only if, it improves

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import os
import pickle
import sys
import time

import design as D
import drc
import netcheck
import pcbgen
import pours
import router as R
from build_board import PLANE_LAYERS, POUR_NETS

HERE = os.path.dirname(os.path.abspath(__file__))
PKL = os.path.join(HERE, "routed.pkl")


def grade(board, tracks, vias, pour_geo, iso_box):
    """(connected, total, violations) -- the three numbers that decide everything."""
    conn = netcheck.check(board, tracks, vias, pour_geo)
    ok = sum(1 for v in conn.values() if v[0])
    viol, _stats = drc.run(board, tracks, vias, pour_geo, iso_box)
    return ok, len(conn), len(viol), conn


def main(apply=False):
    d = pickle.load(open(PKL, "rb"))
    board = pcbgen.BoardV2()

    before_ok, total, before_viol, conn = grade(
        board, d["tracks"], d["vias"], d["pours"], d["iso_box"])
    broken = sorted(n for n, v in conn.items() if not v[0])
    print(f"before:  {before_ok}/{total} connected, {before_viol} violations")
    print(f"         open: {', '.join(broken) if broken else 'none'}\n")
    if not broken:
        print("nothing to repair")
        return 0

    # RIP UP THE AFFECTED NETS FIRST.
    #
    # A netlist change does not move copper -- it re-labels it.  The tracks that used to
    # be BIAS_EL are still lying there, now carrying the name BIASOUT, at spacings that
    # were legal when they were the same net and are not now.  Routing the open
    # connections without clearing that leaves the stale geometry in place: the first
    # attempt did exactly this and came back with 16 violations against the 12 it started
    # with, having closed a net.  Clear the affected nets to bare pads, then route them.
    ripped_t = [t for t in d["tracks"] if t.net in broken]
    ripped_v = [v for v in d["vias"] if v.net in broken]
    print(f"  ripping up {len(ripped_t)} segments and {len(ripped_v)} vias on "
          f"{', '.join(broken)}")
    rt = R.Router(board, verbose=False)
    rt.tracks = [t for t in d["tracks"] if t.net not in broken]
    rt.vias = [v for v in d["vias"] if v.net not in broken]
    rt.rebuild()

    # After a rip-up every pad of those nets is stray, so re-read the connectivity that
    # drives the routing loop rather than using the pre-rip-up picture.
    conn = netcheck.check(board, rt.tracks, rt.vias, d["pours"])
    padmap = {f"{p.ref}.{p.num}": p for p in board.pads()}

    for net in broken:
        ok, _ncomp, stray = conn[net]
        cls = D.netclass_of(net)
        w, c = D.NETCLASS[cls]
        targets = [p for p in board.nets()[net]
                   if f"pad {p.ref}.{p.num}" not in stray]
        for tag in stray:
            src = padmap[tag[4:]]
            targets.sort(key=lambda p: (p.x - src.x) ** 2 + (p.y - src.y) ** 2)
            t0 = time.time()
            got = None
            for tgt in targets[:8]:
                if rt.try_ladder(net, src, tgt, w, c, cls == "ELECTRODE"):
                    got = f"{tgt.ref}.{tgt.num}"
                    break
            # A pad that has just been joined is itself a landing site for the next one.
            # Routing every stray pad to ONE chosen pad makes a star, and the far pad of a
            # star can fail on a board this full while a hop to its nearer neighbour would
            # have succeeded -- which is what J2.10 did, reporting a closed ladder whose
            # copper netcheck still read as a separate island.
            if got:
                targets.append(src)
            # try_ladder's own success is not the connectivity check's.  Confirm against
            # netcheck rather than trusting the return value, and say so when they differ.
            live = netcheck.check(board, rt.tracks, rt.vias, d["pours"])[net]
            print(f"  {net} {tag}: "
                  f"{'closed -> ' + got if got else 'STILL OPEN'}"
                  f"  ({time.time()-t0:.1f}s, net now {live[1]} island(s))")

    # Land the new track ends IN their pads.
    #
    # The router reaches a pad by getting to a grid point inside it, and netcheck asks
    # whether the copper polygons actually overlap.  Those are not the same question on a
    # 0.1 mm grid against a round pad, which is why pad_snap.py exists and why the shipped
    # board needed 184 entry stubs.  Tracks laid by a repair need the same treatment, and
    # without it try_ladder reports a closed ladder whose copper netcheck reads as two
    # islands -- which is exactly what happened here, four times, before this call existed.
    # ONLY the nets that were repaired.  pad_snap.snap() adds a stub for every track end
    # that sits outside its pad, and the shipped board already carries 184 of them -- so
    # running it over the whole board adds a SECOND stub beside each existing one, because
    # an existing stub's own outer end is, by construction, outside the pad.  That measured
    # as 182 duplicate-copper violations.  Snap the repaired nets and nothing else.
    import pad_snap
    subset = [t for t in rt.tracks if t.net in broken]
    n_before = len(subset)
    pad_snap.snap(subset, [p for p in pad_snap.round_pads(board) if p.net in broken])
    new_stubs = subset[n_before:]
    rt.tracks.extend(new_stubs)
    print(f"  {len(new_stubs)} entry stub(s) added, on the repaired nets only")

    # The pours have to be rebuilt against the new copper or the planes still void around
    # tracks that have moved, which shows up as a connectivity failure that is an artefact
    # of a stale pour rather than a real break.
    print("\n  ... rebuilding the reference planes against the new copper")
    pour_geo = {}
    for layer in PLANE_LAYERS:
        for net, lo, hi in POUR_NETS:
            pour_geo[(layer, net)] = pours.build(
                board, rt.tracks, rt.vias, layer, net, lo, hi,
                clearance=0.35, iso_box=d["iso_box"])

    after_ok, total, after_viol, conn2 = grade(
        board, rt.tracks, rt.vias, pour_geo, d["iso_box"])
    still = sorted(n for n, v in conn2.items() if not v[0])
    print(f"\nafter:   {after_ok}/{total} connected, {after_viol} violations")
    print(f"         open: {', '.join(still) if still else 'none'}")

    better = after_ok >= before_ok and after_viol <= before_viol
    if not better:
        print("\nREFUSED: the repair did not improve the board, so routed.pkl is untouched.")
        print("A repair that makes the board worse is worse than no repair, and this is")
        print("the check that stops one being shipped by accident.")
        return 1
    if not apply:
        print("\n(dry run -- pass --apply to write routed.pkl)")
        return 0

    d["tracks"], d["vias"], d["pours"] = rt.tracks, rt.vias, pour_geo
    pickle.dump(d, open(PKL, "wb"))
    print(f"\nwrote {PKL}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
