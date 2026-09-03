#!/usr/bin/env python3
"""
netcheck.py -- exact connectivity verification for EEG-CAR-01 Rev B.

Builds a graph over the real copper primitives (pads, track segments, vias, pour
polygons) with shapely.  Two primitives on the same layer are joined if their
geometries touch.  The two layers are joined only through a via barrel or a
plated through-hole pad -- never by copper that merely overlaps.  A net passes
if all of its pads land in one connected component.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
from shapely.prepared import prep
from shapely.strtree import STRtree

import pours

LAYERS = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def check(board, tracks, vias, pour_geo):
    """Return {net: (ok, n_components, [pad names not on the main component])}."""
    by_net = {}

    def prim(net, layer, geom, tag):
        by_net.setdefault(net, []).append((layer, geom, tag))

    for pd in board.pads():
        if not pd.net:
            continue
        g = pours.pad_poly(pd, 0.001)
        if pd.tht:
            prim(pd.net, "BOTH", g, f"pad {pd.ref}.{pd.num}")
        else:
            prim(pd.net, "F.Cu" if pd.on("F.Cu") else "B.Cu", g, f"pad {pd.ref}.{pd.num}")
    for i, t in enumerate(tracks):
        prim(t.net, t.layer, pours.track_poly(t, 0.001), f"trk{i}")
    for i, v in enumerate(vias):
        prim(v.net, "BOTH", pours.via_poly(v, 0.001), f"via{i}")
    for (layer, net), g in pour_geo.items():
        for j, poly in enumerate(pours.polys(g)):
            prim(net, layer, poly, f"pour {layer} #{j}")

    out = {}
    nets = board.nets()
    for net, items in by_net.items():
        if len(nets.get(net, [])) < 2:
            continue
        uf = UF(len(items))
        # pads that share a reference designator AND a pin number are the same node of
        # the component (a 6 mm tact switch has two pads per terminal)
        same = {}
        for i, (_, _, tag) in enumerate(items):
            if tag.startswith("pad "):
                same.setdefault(tag, []).append(i)
        for group in same.values():
            for i in group[1:]:
                uf.union(group[0], i)
        for layer in LAYERS:
            idx = [i for i, (L, _, _) in enumerate(items) if L in (layer, "BOTH")]
            if len(idx) < 2:
                continue
            geoms = [items[i][1] for i in idx]
            tree = STRtree(geoms)
            prepared = {}
            for k, g in enumerate(geoms):
                for m in tree.query(g):
                    if m == k:
                        continue
                    pg = prepared.get(m)
                    if pg is None:
                        pg = prepared[m] = prep(geoms[m])
                    if pg.intersects(g):
                        uf.union(idx[k], idx[m])
        comps = {}
        for i, (_, _, tag) in enumerate(items):
            comps.setdefault(uf.find(i), []).append(tag)
        pad_tags = {f"pad {p.ref}.{p.num}" for p in nets[net]}
        pad_comps = {r for r, tags in comps.items() if pad_tags & set(tags)}
        ok = len(pad_comps) == 1
        stray = []
        if not ok:
            biggest = max(pad_comps, key=lambda r: len(set(comps[r]) & pad_tags))
            for r in pad_comps:
                if r != biggest:
                    stray += sorted(set(comps[r]) & pad_tags)
        out[net] = (ok, len(pad_comps), stray)
    return out


def report(res, verbose=True):
    bad = {n: v for n, v in res.items() if not v[0]}
    if verbose:
        for n, (_, k, stray) in sorted(bad.items()):
            print(f"  BROKEN {n:14s} {k} islands: " + ", ".join(stray[:8]))
    return len(res) - len(bad), len(bad)
