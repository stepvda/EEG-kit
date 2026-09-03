#!/usr/bin/env python3
"""
resume_repair.py -- finish a build from the post-routing checkpoint.

The routing phase costs about twelve minutes and this environment kills long builds a little
past that, always after the routing has succeeded.  build_board.build() therefore writes
route_checkpoint.pkl once the routing is done; this script picks it up and runs everything
after it -- repair, pours, de-duplication, connectivity and the DRC report -- as a short job
that finishes well inside the window.

Usage:  python3 resume_repair.py [iteration_number]
"""
import pickle
import shutil
import sys
import time
import types

import pcbgen
import design as D
import netcheck
import pours
import drc
import build_board as BB

t0 = time.time()
ck = pickle.load(open("route_checkpoint.pkl", "rb"))
board = pcbgen.BoardV2(); board.validate()

rt = types.SimpleNamespace(**ck)
pour_geo = dict(ck["pours"])
print(f"resumed: {len(rt.tracks)} segments, {len(rt.vias)} vias", flush=True)

# The repair loop needs the real Router, not a namespace -- rebuild one around the tracks.
import router as R
real = R.Router(board)
real.tracks, real.vias = list(rt.tracks), list(rt.vias)
real.iso_box, real.netid = rt.iso_box, rt.netid
real.failed, real.narrowed = list(rt.failed), list(rt.narrowed)
real.rebuild()

padmap = {f"{p.ref}.{p.num}": p for p in board.pads()}
nets = board.nets()
for attempt in range(6):
    conn = netcheck.check(board, real.tracks, real.vias, pour_geo)
    broken = {n: v for n, v in conn.items() if not v[0]}
    print(f"repair pass {attempt+1}: {len(broken)} broken  [{time.time()-t0:.0f}s]", flush=True)
    if not broken:
        break
    fixed = 0
    for net, (_, _, stray) in broken.items():
        w, c = D.NETCLASS[D.netclass_of(net)]
        allp = nets[net]
        srcs = [padmap[t[4:]] for t in stray if t[4:] in padmap] or allp[:1]
        for src in srcs:
            tg = sorted((p for p in allp if p is not src),
                        key=lambda p: (p.x-src.x)**2 + (p.y-src.y)**2)
            if any(real.try_ladder(net, src, t, w, c, False) for t in tg[:10]):
                fixed += 1
                break
    print(f"   {fixed} closed  [{time.time()-t0:.0f}s]", flush=True)
    if not fixed:
        break
    for layer in BB.PLANE_LAYERS:
        for n_, lo, hi in BB.POUR_NETS:
            pour_geo[(layer, n_)] = pours.build(board, real.tracks, real.vias, layer, n_,
                                                lo, hi, clearance=0.35, iso_box=real.iso_box)

# --- viafix and the late repair.  THESE ARE NOT OPTIONAL.
#
# An earlier version of this script stopped after the repair loop and wrote a DRC report,
# and that report was WRONG in a way that mattered: it showed sixteen tracks lying on via
# pads at 0.000 mm and nine unclosed nets, and on the strength of it a good iteration was
# judged a failure and reverted.  The full build resolves exactly those shorts in
# viafix.push(), which moves vias out from under tracks, and closes more nets in the late
# repair that runs on the settled geometry.  The same board scored 136/9/28 here and
# 143/2/2 through the real pipeline.
#
# A partial pipeline must never produce a report that looks like a verdict.
import viafix
stuck = []
for _ in range(3):
    moved, _d, stuck = viafix.push(board, real.tracks, real.vias, pour_geo, verbose=True)
    if not moved:
        break
if stuck:
    print(f"  {len(stuck)} vias could not be pushed clear; deleting and re-routing", flush=True)
    drop = set(stuck)
    killed = {real.vias[i].net for i in drop}
    real.vias = [v for i, v in enumerate(real.vias) if i not in drop]
    real.rebuild()
    for net in sorted(killed):
        pads = nets[net]
        w, c = D.NETCLASS[D.netclass_of(net)]
        for a_, b_ in real._mst([(p.x, p.y) for p in pads]):
            real.try_ladder(net, pads[a_], pads[b_], w, c, False)
    for layer in BB.PLANE_LAYERS:
        for n_, lo, hi in BB.POUR_NETS:
            pour_geo[(layer, n_)] = pours.build(board, real.tracks, real.vias, layer, n_,
                                                lo, hi, clearance=0.35, iso_box=real.iso_box)
    viafix.push(board, real.tracks, real.vias, pour_geo, verbose=True)

BB._dedupe(real, verbose=True)
for layer in BB.PLANE_LAYERS:
    for n_, lo, hi in BB.POUR_NETS:
        pour_geo[(layer, n_)] = pours.build(board, real.tracks, real.vias, layer, n_,
                                            lo, hi, clearance=0.35, iso_box=real.iso_box)

# late repair, on the settled landscape -- no rip-up
for attempt in range(3):
    conn = netcheck.check(board, real.tracks, real.vias, pour_geo)
    broken = {n: v for n, v in conn.items() if not v[0]}
    print(f"late repair pass {attempt+1}: {len(broken)} broken  [{time.time()-t0:.0f}s]",
          flush=True)
    if not broken:
        break
    fixed = 0
    for net, (_, _, stray) in broken.items():
        w, c = D.NETCLASS[D.netclass_of(net)]
        allp = nets[net]
        srcs = [padmap[t[4:]] for t in stray if t[4:] in padmap] or allp[:1]
        for src in srcs:
            tg = sorted((p for p in allp if p is not src),
                        key=lambda p: (p.x-src.x)**2 + (p.y-src.y)**2)
            if any(real.try_ladder(net, src, t, w, c, False) for t in tg[:10]):
                fixed += 1
                break
    print(f"   {fixed} repaired late  [{time.time()-t0:.0f}s]", flush=True)
    if not fixed:
        break
    viafix.push(board, real.tracks, real.vias, pour_geo, verbose=False)
    BB._dedupe(real, verbose=False)

BB._dedupe(real, verbose=True)
for layer in BB.PLANE_LAYERS:
    for n_, lo, hi in BB.POUR_NETS:
        pour_geo[(layer, n_)] = pours.build(board, real.tracks, real.vias, layer, n_,
                                            lo, hi, clearance=0.35, iso_box=real.iso_box)

# --- targeted repairs.  ALSO NOT OPTIONAL.
#
# design.TARGETED_REPAIRS is carried out by tools/surgery.py on the settled route, and
# build_board.build() runs it after the late repair.  Omitting it here would report the
# board WITHOUT the surgery and make a working change look like a failure -- which is
# exactly the mistake that cost iteration 5.  Mirror the build's tail exactly.
surgery_notes = []
if getattr(D, "TARGETED_REPAIRS", None):
    import surgery
    print("  ... targeted repairs", flush=True)
    surgery_notes = surgery.apply(real, board, pour_geo, verbose=True)
    for layer in BB.PLANE_LAYERS:
        for n_, lo, hi in BB.POUR_NETS:
            pour_geo[(layer, n_)] = pours.build(board, real.tracks, real.vias, layer, n_,
                                                lo, hi, clearance=0.35, iso_box=real.iso_box)
    viafix.push(board, real.tracks, real.vias, pour_geo, verbose=True)
    BB._dedupe(real, verbose=True)
    for layer in BB.PLANE_LAYERS:
        for n_, lo, hi in BB.POUR_NETS:
            pour_geo[(layer, n_)] = pours.build(board, real.tracks, real.vias, layer, n_,
                                                lo, hi, clearance=0.35, iso_box=real.iso_box)
    for note in surgery_notes:
        print(f"     surgery: {note}", flush=True)

res = {"tracks": real.tracks, "vias": real.vias, "pours": pour_geo,
       "failed": real.failed, "narrowed": real.narrowed, "iso_box": real.iso_box,
       "netid": real.netid}
res["connectivity"] = netcheck.check(board, real.tracks, real.vias, pour_geo)
pickle.dump(res, open("routed.pkl", "wb"))
v, st = drc.write_report("drc_report.txt", board, real.tracks, real.vias, pour_geo,
                         res["iso_box"], res.get("narrowed", []))
print(f"\nDRC violations: {len(v)}   [{time.time()-t0:.0f}s]")
for k in ("nets fully connected", "unclosed nets", "unclosed nets with NO copper at all",
          "unique segments", "unique vias"):
    print(f"   {k}: {st.get(k)}")
if len(sys.argv) > 1:
    shutil.copy("drc_report.txt", f"../reports/drc_{sys.argv[1]}.txt")
    print(f"   saved to reports/drc_{sys.argv[1]}.txt")
