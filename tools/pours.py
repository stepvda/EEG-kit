#!/usr/bin/env python3
"""
pours.py -- copper pour construction for EEG-CAR-01 Rev B.

Two reference pours per layer:
    x < 58 mm   AGND_REF   the analogue 0 V mid-rail and the guard for every input net
    x > 58 mm   DGND       the digital return

They are built as real polygons with shapely (not as a raster), so the Gerber output is
vector and a fabricator sees exactly what the DRC measured.  Through-hole pads of the
pour net get four-spoke thermal reliefs so the sockets can still be hand-soldered;
surface-mount pads are connected solid, which is better electrically and is what reflow
wants.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
from shapely.geometry import box, Point, Polygon, MultiPolygon, LineString
from shapely.ops import unary_union

import design as D

POUR_EDGE_INSET = 0.4       # keep the pour this far inside the board outline
ZONE_GAP = 0.5              # gap between the analogue and the digital pour
THERMAL_GAP = 0.4           # annulus width around a same-net through-hole pad
SPOKE_W = 0.6               # thermal spoke width
MIN_ISLAND_AREA = 2.0       # mm^2, anything smaller is dropped


def pad_poly(pd, grow=0.0):
    w, h = pd.size_rot()
    if pd.shape == "circle" or pd.kind == "np_thru_hole":
        return Point(pd.x, pd.y).buffer(w / 2 + grow, 24)
    # fplib gives every through-hole header pin but pin 1 the shape "oval", which at
    # equal width and height is a CIRCLE -- that is the KiCad convention and what
    # kicad_write.py emits.  This function used to box it, and gerber.py used to
    # aperture it as R,wXh, so the connectivity model and the fabricated copper both
    # had a square where the design has a round pad.  The corners are 27 % of the
    # area, and 83 nets' tracks ended in them: real on the Gerber, absent in KiCad.
    if pd.shape == "oval" and abs(w - h) < 1e-9:
        return Point(pd.x, pd.y).buffer(w / 2 + grow, 24)
    if pd.shape == "oval":
        return LineString([(pd.x - (w - h) / 2, pd.y), (pd.x + (w - h) / 2, pd.y)]
                          ).buffer(h / 2 + grow, 16) if w > h else \
               LineString([(pd.x, pd.y - (h - w) / 2), (pd.x, pd.y + (h - w) / 2)]
                          ).buffer(w / 2 + grow, 16)
    return box(pd.x - w / 2 - grow, pd.y - h / 2 - grow,
               pd.x + w / 2 + grow, pd.y + h / 2 + grow)


def track_poly(t, grow=0.0):
    return LineString([(t.x1, t.y1), (t.x2, t.y2)]).buffer(t.width / 2 + grow, 16,
                                                           cap_style=1, join_style=1)


def via_poly(v, grow=0.0):
    return Point(v.x, v.y).buffer(v.pad / 2 + grow, 20)


def build(board, tracks, vias, layer, pour_net, x_lo, x_hi,
          clearance=0.35, iso_box=None):
    """Return a MultiPolygon of the finished pour for one net on one layer."""
    zone = box(max(x_lo, POUR_EDGE_INSET), POUR_EDGE_INSET,
               min(x_hi, D.BOARD_W - POUR_EDGE_INSET), D.BOARD_H - POUR_EDGE_INSET)

    blockers, own_tht, own_smd = [], [], []
    for pd in board.pads():
        if not pd.tht and not pd.on(layer):
            continue
        if pd.net == pour_net:
            (own_tht if pd.tht else own_smd).append(pd)
            continue
        clr = clearance
        if pd.net in D.ELECTRODE_NETS:
            clr = max(clearance, 0.4)
        blockers.append(pad_poly(pd, clr))
        if pd.kind == "np_thru_hole":
            # a 3.2 mm hole is an M3 mounting hole and gets a 6 mm copper keep-out;
            # the 1.5 mm holes are the DIN socket retention posts and need only a gap
            blockers.append(Point(pd.x, pd.y)
                            .buffer(3.0 if pd.drill > 2.5 else pd.drill / 2 + 0.4, 24))

    for t in tracks:
        if t.layer != layer or t.net == pour_net:
            continue
        clr = 0.4 if t.net in D.ELECTRODE_NETS else clearance
        blockers.append(track_poly(t, clr))
    for v in vias:
        if v.net == pour_net:
            continue
        blockers.append(via_poly(v, 0.45 if v.net in D.ELECTRODE_NETS else clearance))
    if iso_box:
        # the isolation strip is a hard keep-out, and a plane must be cut back from it by
        # the same clearance as anything else
        blockers.append(box(iso_box[0] - clearance, iso_box[1] - clearance,
                            iso_box[2] + clearance, iso_box[3] + clearance))

    pour = zone.difference(unary_union(blockers)) if blockers else zone

    # thermal reliefs on same-net through-hole pads
    reliefs = []
    for pd in own_tht:
        w, _ = pd.size_rot()
        r = w / 2
        ring = Point(pd.x, pd.y).buffer(r + THERMAL_GAP, 24).difference(
            Point(pd.x, pd.y).buffer(r, 24))
        spokes = unary_union([
            box(pd.x - SPOKE_W / 2, pd.y - r - THERMAL_GAP - 0.1,
                pd.x + SPOKE_W / 2, pd.y + r + THERMAL_GAP + 0.1),
            box(pd.x - r - THERMAL_GAP - 0.1, pd.y - SPOKE_W / 2,
                pd.x + r + THERMAL_GAP + 0.1, pd.y + SPOKE_W / 2)])
        reliefs.append(ring.difference(spokes))
    if reliefs:
        pour = pour.difference(unary_union(reliefs))

    pour = _clean(pour)

    # keep only islands that actually touch a pad of this net
    anchors = [pad_poly(p, 0.02) for p in own_tht + own_smd]
    anchors += [via_poly(v, 0.02) for v in vias if v.net == pour_net]
    anchors += [track_poly(t, 0.02) for t in tracks
                if t.net == pour_net and t.layer == layer]
    keep = []
    for poly in _polys(pour):
        if poly.area < MIN_ISLAND_AREA:
            continue
        if any(poly.intersects(a) for a in anchors):
            keep.append(poly)
    return MultiPolygon(keep) if keep else MultiPolygon()


def _clean(g):
    if g.is_empty:
        return g
    g = g.buffer(0)
    return g


def _polys(g):
    if g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    return [p for p in g.geoms if isinstance(p, Polygon)]


def polys(g):
    return _polys(g)
