#!/usr/bin/env python3
"""
viafix.py -- push vias clear of their neighbours after routing.

A via pad is 0.8 mm across while most tracks are 0.25 mm, so a layer change that the
maze router thought was legal can still leave the via inside another net's clearance.
Rather than constrain the router (which costs routability everywhere for a problem that
happens in a few dozen places), the vias are moved afterwards: each offending via is
slid to the nearest position where it and its incident tracks are all legal, and the
tracks are re-endpointed to follow it.  A via that cannot be moved is deleted together
with its layer change, and the connection is handed back to the router.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math

from shapely.geometry import Point
from shapely.strtree import STRtree

import design as D
import pours

LAYERS = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")

EPS = 1e-6


def _foreign_index(board, tracks, vias, pour_geo, layer, skip_via_ids=()):
    items = []
    for pd in board.pads():
        if not pd.net:
            continue
        if not pd.tht and not pd.on(layer):
            continue
        items.append((pd.net, pours.pad_poly(pd)))
    for t in tracks:
        if t.layer == layer:
            items.append((t.net, pours.track_poly(t)))
    for i, v in enumerate(vias):
        if i in skip_via_ids:
            continue
        items.append((v.net, pours.via_poly(v)))
    for (lay, net), g in pour_geo.items():
        if lay != layer:
            continue
        for poly in pours.polys(g):
            items.append((net, poly))
    return items


def _need(n1, n2):
    e = D.ELECTRODE_NETS
    return 0.35 if (n1 in e or n2 in e) else 0.20


class Checker:
    def __init__(self, board, tracks, vias, pour_geo):
        self.layers = {}
        for layer in ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu"):
            items = _foreign_index(board, tracks, vias, pour_geo, layer)
            self.layers[layer] = (items, STRtree([g for _, g in items]))

    def clear(self, net, geom, layer, ignore_bounds=()):
        """ignore_bounds: bounding boxes of the features being replaced."""
        items, tree = self.layers[layer]
        for j in tree.query(geom.buffer(0.36)):
            n2, g2 = items[j]
            if n2 == net:
                continue
            if ignore_bounds:
                b2 = g2.bounds
                if any(abs(b2[0] - b[0]) < 1e-6 and abs(b2[1] - b[1]) < 1e-6
                       and abs(b2[2] - b[2]) < 1e-6 and abs(b2[3] - b[3]) < 1e-6
                       for b in ignore_bounds):
                    continue
            if geom.distance(g2) < _need(net, n2) - EPS:
                return False
        return True


def push(board, tracks, vias, pour_geo, max_shift=2.5, step=0.25, verbose=True):
    """Returns (n_moved, n_deleted, list of vias that could not be fixed)."""
    chk = Checker(board, tracks, vias, pour_geo)
    by_pos = {}
    for i, t in enumerate(tracks):
        by_pos.setdefault((round(t.x1, 4), round(t.y1, 4)), []).append((i, "start"))
        by_pos.setdefault((round(t.x2, 4), round(t.y2, 4)), []).append((i, "end"))

    moved = deleted = 0
    stuck = []
    for vi, v in enumerate(vias):
        g = pours.via_poly(v)
        own = [pours.via_poly(v).bounds]
        bad = any(not chk.clear(v.net, g, L, own) for L in LAYERS)
        if not bad:
            continue
        inc = by_pos.get((round(v.x, 4), round(v.y, 4)), [])
        best = None
        r = step
        while r <= max_shift and best is None:
            nk = max(8, int(2 * math.pi * r / step))
            for k in range(nk):
                a = 2 * math.pi * k / nk
                nx, ny = v.x + r * math.cos(a), v.y + r * math.sin(a)
                if not (1.5 < nx < D.BOARD_W - 1.5 and 1.5 < ny < D.BOARD_H - 1.5):
                    continue
                ng = Point(nx, ny).buffer(v.pad / 2, 20)
                if any(not chk.clear(v.net, ng, L, own) for L in LAYERS):
                    continue
                # the incident tracks must remain legal when re-endpointed
                ok = True
                trial = []
                for ti, which in inc:
                    t = tracks[ti]
                    x1, y1, x2, y2 = t.x1, t.y1, t.x2, t.y2
                    if which == "start":
                        x1, y1 = nx, ny
                    else:
                        x2, y2 = nx, ny
                    from router import Track
                    nt = Track(t.layer, x1, y1, x2, y2, t.width, t.net)
                    if not chk.clear(t.net, pours.track_poly(nt), t.layer,
                                     [pours.track_poly(t).bounds] + own):
                        ok = False
                        break
                    trial.append((ti, nt))
                if ok:
                    best = (nx, ny, trial)
                    break
            r += step
        if best is None:
            stuck.append(vi)
            continue
        nx, ny, trial = best
        old = (round(v.x, 4), round(v.y, 4))
        v.x, v.y = nx, ny
        for ti, nt in trial:
            tracks[ti] = nt
        by_pos.pop(old, None)
        by_pos.setdefault((round(nx, 4), round(ny, 4)), []).extend(inc)
        moved += 1
        if moved % 20 == 0:
            chk = Checker(board, tracks, vias, pour_geo)
    if verbose:
        print(f"  via push: {moved} vias moved, {len(stuck)} could not be moved")
    return moved, deleted, stuck
