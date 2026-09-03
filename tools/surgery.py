#!/usr/bin/env python3
"""
surgery.py -- targeted, declared repairs applied after routing.

The autorouter is not iterated further (user instruction, 2026-09-02).  What
remains is two named connections, each with a specified fix.  The fixes are
DATA in design.py (TARGETED_REPAIRS) so that design.py stays the single
source of truth and a full build reproduces them; this module carries them
out on the finished route, after the late repair and before the final via
push, and ONLY where the named connection is still open -- a fix whose need
has already gone is skipped and said so.

Two kinds:

  stub_via   -- a short F.Cu stub from a pad outward from its package, ending
                in a through-via to the reference planes.  Segments of the
                nets named in `rip` that sit in the way are removed first and
                those nets re-routed afterwards with the stub and via locked
                in as obstacles.  Nothing else is touched: if copper of any
                other net blocks every candidate site, the repair reports
                that and does nothing.
  corridor   -- rip the segments of the nets named in `rip` that cross a
                declared box, route the named connection through the freed
                space FIRST at its full class geometry (no relaxation), then
                re-route the ripped nets around the new copper.

Every step is measured with the router's own distance transforms and the
result verified by netcheck in build_board; this module never claims a
connection it did not make.  Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math

import numpy as np
from shapely.geometry import LineString, Point, box as sbox

import design as D
import pours
import netcheck
import router as R


def _padmap(board):
    return {f"{p.ref}.{p.num}": p for p in board.pads()}


def _open_pads(board, rt, pour_geo, net):
    """Pads of `net` not on its main island, per netcheck."""
    conn = netcheck.check(board, rt.tracks, rt.vias, pour_geo)
    ok, _, stray = conn.get(net, (True, 1, []))
    return set() if ok else {s[4:] for s in stray}


def _repair(rt, board, pour_geo, net, verbose):
    """Re-join `net` after its copper was cut: strays -> nearest pads, honest ladder."""
    from build_board import _place_ground_via
    padmap = _padmap(board)
    cls = D.netclass_of(net)
    w, c = D.NETCLASS[cls]
    fixed, still = 0, []
    for _pass in range(3):
        stray = _open_pads(board, rt, pour_geo, net)
        if not stray:
            break
        targets = [p for p in board.nets()[net] if f"{p.ref}.{p.num}" not in stray]
        still = []
        for tag in sorted(stray):
            src = padmap[tag]
            done = False
            if targets:
                targets.sort(key=lambda p: (p.x - src.x) ** 2 + (p.y - src.y) ** 2)
                for tgt in targets[:8]:
                    if rt.try_ladder(net, src, tgt, w, c, cls == "ELECTRODE"):
                        done = True
                        break
            if not done and net in ("DGND", "AGND_REF") and not src.tht:
                done = _place_ground_via(rt, src, dists=(1.15, 1.4, 1.7, 2.0, 2.4,
                                                         2.8, 3.2, 3.8))
            if done:
                fixed += 1
            else:
                still.append(tag)
        if not fixed:
            break
    if verbose:
        print(f"    re-route {net}: {fixed} joined, still open: {still or 'none'}")
    return still


# --------------------------------------------------------------------- stub_via
def _stub_via(rt, board, pour_geo, spec, verbose):
    padmap = _padmap(board)
    pad = padmap[spec["pad"]]
    net = pad.net
    netv = rt.netid[net]
    part = board.part(pad.ref)
    note = dict(kind="stub_via", pad=spec["pad"], net=net)
    if spec["pad"] not in _open_pads(board, rt, pour_geo, net):
        note["result"] = "skipped: pad already on the net's main island"
        if verbose:
            print(f"  stub_via {spec['pad']}: {note['result']}")
        return note
    # outward from the package: SOIC / SOT pins leave the body along +-x
    dirx = -1.0 if pad.x < part.x else 1.0
    via_w, via_d = spec.get("via", (R.VIA_PAD, R.VIA_DRILL))
    lo, hi = spec.get("length", (1.0, 1.5))
    rip_nets = set(spec.get("rip", ()))
    lengths = [round(lo + 0.1 * k, 2) for k in range(int(round((hi - lo) / 0.1)) + 1)]
    for length in lengths:
        vx, vy = pad.x + dirx * length, pad.y
        zone = Point(vx, vy).buffer(via_w / 2).union(
            LineString([(pad.x, pad.y), (vx, vy)]).buffer(0.15))
        rip_t, rip_v, others = [], [], set()
        for i, t in enumerate(rt.tracks):
            if t.net == net:
                continue
            clr = 0.35 if t.net in D.ELECTRODE_NETS else 0.20
            if pours.track_poly(t).distance(zone) < clr + 0.03:
                (rip_t.append(i) if t.net in rip_nets else others.add(t.net))
        for i, v in enumerate(rt.vias):
            if v.net == net:
                continue
            if pours.via_poly(v).distance(zone) < 0.23:
                (rip_v.append(i) if v.net in rip_nets else others.add(v.net))
        for p in board.pads():
            if p.net == net or not p.net:
                continue
            clr = 0.35 if p.net in D.ELECTRODE_NETS else 0.20
            if pours.pad_poly(p).distance(zone) < clr + 0.03:
                others.add(p.net)
        if others:
            if verbose:
                print(f"  stub_via {spec['pad']}: length {length} blocked by "
                      f"{sorted(others)} (not in rip list)")
            continue
        if rt.no_via[R.mm2c(vy), R.mm2c(vx)]:
            continue
        # rip, then measure with the router's own transforms
        saved_t, saved_v = list(rt.tracks), list(rt.vias)
        rt.tracks = [t for i, t in enumerate(rt.tracks) if i not in set(rip_t)]
        rt.vias = [v for i, v in enumerate(rt.vias) if i not in set(rip_v)]
        rt.rebuild()
        cx, cy = R.mm2c(vx), R.mm2c(vy)
        need = via_w / 2 + 0.20 + 0.05
        ok = all(rt._dist(L, netv)[cy, cx] >= need for L in range(len(R.LAYERS)))
        ok = ok and all(rt._dist_elec(L)[cy, cx] >= via_w / 2 + 0.35 + 0.05
                        for L in range(len(R.LAYERS)))
        free = rt._free_mask(0, netv, 0.15, 0.20)
        n = 12
        for k in range(n + 1):
            px, py = pad.x + (vx - pad.x) * k / n, pad.y + (vy - pad.y) * k / n
            inside_pad = abs(px - pad.x) <= 0.5 and abs(py - pad.y) <= 0.25
            if not inside_pad and not free[R.mm2c(py), R.mm2c(px)]:
                ok = False
                break
        if not ok:
            rt.tracks, rt.vias = saved_t, saved_v
            rt.rebuild()
            if verbose:
                print(f"  stub_via {spec['pad']}: length {length} -- site not legal after "
                      f"ripping {len(rip_t)} segment(s)")
            continue
        # commit: stub + via, locked in as obstacles for everything that follows
        rt.tracks.append(R.Track("F.Cu", pad.x, pad.y, vx, vy, 0.30, net))
        rt.r.stamp_seg(0, pad.x, pad.y, vx, vy, 0.15, netv)
        rt.vias.append(R.Via(vx, vy, via_w, via_d, net))
        for L in range(len(R.LAYERS)):
            rt.r.stamp_disk(L, vx, vy, via_w / 2, netv)
        note.update(result="placed", via=(round(vx, 2), round(vy, 2), via_w, via_d),
                    stub_mm=length, ripped={n_: 0 for n_ in rip_nets})
        for i in rip_t:
            note["ripped"][saved_t[i].net] += 1
        if verbose:
            print(f"  stub_via {spec['pad']}: via {via_w}/{via_d} at ({vx:.2f},{vy:.2f}), "
                  f"stub {length} mm, ripped {note['ripped']}")
        for rn in sorted(rip_nets):
            still = _repair(rt, board, pour_geo, rn, verbose)
            note.setdefault("rip_net_open", {})[rn] = still
        return note
    note["result"] = "FAILED: no candidate site 1.0-1.5 mm outward is legal touching only " \
                     + ", ".join(sorted(rip_nets))
    if verbose:
        print(f"  stub_via {spec['pad']}: {note['result']}")
    return note


# --------------------------------------------------------------------- corridor
def _corridor(rt, board, pour_geo, spec, verbose):
    padmap = _padmap(board)
    a, b = padmap[spec["a"]], padmap[spec["b"]]
    net = a.net
    netv = rt.netid[net]
    note = dict(kind="corridor", net=net, a=spec["a"], b=spec["b"])
    if spec["a"] not in _open_pads(board, rt, pour_geo, net) \
            and spec["b"] not in _open_pads(board, rt, pour_geo, net):
        note["result"] = "skipped: both pads already on the net's main island"
        if verbose:
            print(f"  corridor {net}: {note['result']}")
        return note
    x0, y0, x1, y1 = spec["box"]
    bx = sbox(x0, y0, x1, y1)
    rip_nets = set(spec["rip"])
    rip_t = [i for i, t in enumerate(rt.tracks)
             if t.net in rip_nets and pours.track_poly(t).intersects(bx)]
    rip_v = [i for i, v in enumerate(rt.vias)
             if v.net in rip_nets and bx.contains(Point(v.x, v.y))]
    ripped = {}
    for i in rip_t:
        ripped[rt.tracks[i].net] = ripped.get(rt.tracks[i].net, 0) + 1
    rt.tracks = [t for i, t in enumerate(rt.tracks) if i not in set(rip_t)]
    rt.vias = [v for i, v in enumerate(rt.vias) if i not in set(rip_v)]
    rt.rebuild()
    note["ripped"] = ripped
    if verbose:
        print(f"  corridor {net}: ripped {ripped} segments and {len(rip_v)} via(s) in "
              f"box {spec['box']}")
    w, c = spec.get("width", 0.30), spec.get("clearance", 0.40)
    ok = (rt.route_pair(net, a, b, w, c, top_only=True, margin=30.0)
          or rt.route_pair(net, a, b, w, c, top_only=False, margin=30.0)
          or rt.route_pair(net, a, b, w, c, top_only=False, margin=200.0))
    note["routed"] = bool(ok)
    if not ok:
        # say what still crosses the straight corridor, at what distance
        line = LineString([(a.x, a.y), (b.x, b.y)]).buffer(w / 2)
        crossers = {}
        for t in rt.tracks:
            if t.net == net:
                continue
            dd = pours.track_poly(t).distance(line)
            if dd < c:
                crossers[(t.net, t.layer)] = round(min(dd, crossers.get((t.net, t.layer), 9)), 3)
        note["still_crossing"] = sorted(crossers.items())
        if verbose:
            print(f"  corridor {net}: {spec['a']} -> {spec['b']} NOT routed at {w}/{c}; "
                  f"still crossing: {note['still_crossing']}")
    # No fence beyond the routed copper itself.  A box-wide keep-out was tried
    # first and it strands every foreign pad INSIDE the box (D16.1/D16.2 and
    # C16.2 sit there): the ripped nets must be able to reach their own pads.
    # The SPARE2 copper is already stamped, and every non-electrode net keeps
    # 0.35 mm from it by the electrode rule in _free_mask, which is the
    # corridor the instruction reserves.
    for rn in sorted(rip_nets):
        still = _repair(rt, board, pour_geo, rn, verbose)
        note.setdefault("rip_net_open", {})[rn] = still
    rt.rebuild()
    if verbose:
        print(f"  corridor {net}: {'routed' if ok else 'OPEN'}; "
              f"ripped nets re-joined except {note.get('rip_net_open')}")
    return note


def rotation_facts(board, ref):
    """What a 180-degree turn of `ref` does to its pads -- a report, never applied."""
    p = board.part(ref)
    out = []
    for pd in p.pads:
        nx = 2 * p.x - pd.x
        ny = 2 * p.y - pd.y
        out.append((f"{ref}.{pd.num}", pd.net, (round(pd.x, 2), round(pd.y, 2)),
                    (round(nx, 2), round(ny, 2))))
    return out


def apply(rt, board, pour_geo, verbose=True):
    notes = []
    for spec in getattr(D, "TARGETED_REPAIRS", []):
        if spec["kind"] == "stub_via":
            notes.append(_stub_via(rt, board, pour_geo, spec, verbose))
        elif spec["kind"] == "corridor":
            notes.append(_corridor(rt, board, pour_geo, spec, verbose))
    return notes
