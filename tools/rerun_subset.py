#!/usr/bin/env python3
"""
rerun_subset.py -- the fast inner loop: retry chosen nets on the FINISHED board.

A full build is ~40 minutes; this loads routed.pkl, rebuilds the router's
obstacle raster from the finished tracks and vias, and re-attempts only the
connections you name -- seconds per connection.  Use it to test whether a
placement or rule change WOULD close a net before paying for a full build.

    python3 rerun_subset.py AVSS2 SPARE2        # retry these nets' strays
    python3 rerun_subset.py --all-broken        # retry everything netcheck flags

It never writes routed.pkl: the full build remains the only producer of the
shipped artefact, so the cache cannot drift from design.py.
Licence: CC BY-SA 4.0.
"""
import pickle
import sys
import time

import design as D
import pcbgen
import router as R
import netcheck

def main():
    d = pickle.load(open("routed.pkl", "rb"))
    board = pcbgen.BoardV2()
    rt = R.Router(board, verbose=False)
    rt.tracks = list(d["tracks"])
    rt.vias = list(d["vias"])
    rt.rebuild()
    pour_geo = dict(d["pours"])
    padmap = {f"{p.ref}.{p.num}": p for p in board.pads()}
    conn = netcheck.check(board, rt.tracks, rt.vias, pour_geo)
    if "--all-broken" in sys.argv:
        wanted = sorted(n for n, v in conn.items() if not v[0])
    else:
        wanted = [a for a in sys.argv[1:] if not a.startswith("-")]
    for net in wanted:
        ok, ncomp, stray = conn.get(net, (True, 1, []))
        if ok:
            print(f"{net}: already connected")
            continue
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
            print(f"{net} {tag}: {'closed -> ' + got if got else 'STILL OPEN'}"
                  f"  ({time.time() - t0:.1f}s)")
    conn2 = netcheck.check(board, rt.tracks, rt.vias, pour_geo)
    print("broken now (pours NOT rebuilt):",
          sorted(n for n, v in conn2.items() if not v[0]))

if __name__ == "__main__":
    main()
