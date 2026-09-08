#!/usr/bin/env python3
"""
drc_geometry.py -- the six geometry checks the external layout review asked for.

ECO-EEG-030 recorded seven findings against the Rev B routing.  Six of them are rules a
design-rule check can enforce and this programme's DRC was never given, which is why a
report at zero violations was a report against an incomplete rule set.  This module is
those six, measured on real geometry; `tools/drc.py` calls it and prints each one as its
own counted line, and `tools/rules.py` holds the numbers.

  1   via inside an SMD pad                          `via_in_pad`
  2a  dangling track end -- an "antenna"             `dangling_ends`
  2b  redundant copper path between two pads         `redundant_paths`
  3   an angle below 90 degrees between two          `segment_angles`
      segments of one track, and any segment not
      on a 0/45/90/135 degree axis
  4   a track entering a pad off its centre          `pad_entry`
  5   a conductor below its net class's minimum      `class_widths`
      width, or on a layer the class forbids, or
      a via on a class that may not have one

Each returns a list of (kind, message) in the same shape as `drc.run` builds, plus a
count.  `max_report` truncates the LIST and never the COUNT: a caller that wants a short
listing still gets the true total, because a truncated total is how a report comes to
understate what it measured.

**What these do NOT check.**  None of them looks at whether the routing is any good.
They are geometric hygiene: a board can pass all six and still have a return path that
goes round three sides of the analogue zone.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
import os
import sys
from collections import defaultdict

from shapely.geometry import LineString, Point
from shapely.strtree import STRtree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import pours                # noqa: E402
import rules                # noqa: E402

LAYERS = rules.COPPER_LAYERS


def _key(x, y, q=3):
    return (round(x, q), round(y, q))


# --------------------------------------------------------------------------- 1
def via_in_pad(board, vias, max_report=None):
    """Finding 1: drills in pads.

    A via whose hole falls inside, or within `via_to_smd_pad_min` of, an SMD pad is a
    via-in-pad.  It is checked against the pad's own net as well as any other net,
    because via-in-pad on the same net is exactly the construction the finding is about:
    the solder wicks down the barrel and the joint starves.

    Through-hole pads are drilled by definition and are not in scope; a via that lands
    inside a THT pad is caught by the hole-to-hole rule in drc.py instead.
    """
    v = []
    smd = [pd for pd in board.pads() if pd.kind == "smd" and not pd.ref.startswith("FID")]
    if not smd or not vias:
        return v, 0
    geoms = [pours.pad_poly(pd) for pd in smd]
    tree = STRtree(geoms)
    clr = rules.GEOMETRY["via_to_smd_pad_min"]
    for i, vv in enumerate(vias):
        hole = Point(vv.x, vv.y).buffer(vv.drill / 2 + clr, 20)
        for j in tree.query(hole):
            if not hole.intersects(geoms[j]):
                continue
            pd = smd[j]
            same = " (same net)" if pd.net == vv.net else f" (pad net {pd.net})"
            v.append(("via in pad",
                      f"via {vv.net} at ({vv.x:.3f}, {vv.y:.3f}) drill {vv.drill:.2f} mm "
                      f"is inside pad {pd.ref}.{pd.num}{same}, or within "
                      f"{clr:.2f} mm of it"))
    return v[:max_report], len(v)


# --------------------------------------------------------------------------- 2a
def dangling_ends(board, tracks, vias, pour_geo, max_report=None):
    """Finding 2, first half: net stubs -- "antennas".

    A track endpoint is dangling when nothing else on the same net touches it: no other
    track on that layer, no pad, no via, no pour polygon.  A stub is copper that carries
    no current and radiates and receives; on this board an electrode-net stub is also a
    patient-connected antenna.
    """
    v = []
    tol = rules.GEOMETRY["dangling_tol"]
    if not tracks:
        return v, 0

    # what a track end may legitimately land on, per net
    by_net_layer = defaultdict(list)
    for i, t in enumerate(tracks):
        by_net_layer[(t.net, t.layer)].append(("trk", i, pours.track_poly(t, tol)))
    for pd in board.pads():
        if not pd.net:
            continue
        g = pours.pad_poly(pd, tol)
        lays = LAYERS if pd.tht else tuple(ly for ly in LAYERS if pd.on(ly))
        for ly in lays:
            by_net_layer[(pd.net, ly)].append(("pad", f"{pd.ref}.{pd.num}", g))
    for i, vv in enumerate(vias):
        g = pours.via_poly(vv, tol)
        for ly in LAYERS:
            by_net_layer[(vv.net, ly)].append(("via", i, g))
    for (ly, net), g in pour_geo.items():
        for j, poly in enumerate(pours.polys(g)):
            by_net_layer[(net, ly)].append(("pour", j, poly))

    trees = {}
    for k, items in by_net_layer.items():
        trees[k] = (items, STRtree([it[2] for it in items]))

    for i, t in enumerate(tracks):
        items, tree = trees[(t.net, t.layer)]
        for (ex, ey), which in (((t.x1, t.y1), "start"), ((t.x2, t.y2), "end")):
            p = Point(ex, ey).buffer(tol, 8)
            touched = False
            for j in tree.query(p):
                kind, ident, g = items[j]
                if kind == "trk" and ident == i:
                    continue
                if g.intersects(p):
                    touched = True
                    break
            if not touched:
                v.append(("dangling track end",
                          f"{t.net} on {t.layer}: the {which} of the segment "
                          f"({t.x1:.3f}, {t.y1:.3f})-({t.x2:.3f}, {t.y2:.3f}) touches "
                          f"nothing else on its net"))
    return v[:max_report], len(v)


# --------------------------------------------------------------------------- 2b
def redundant_paths(board, tracks, vias, pour_geo, max_report=None):
    """Finding 2, second half: loops -- more than one copper path between two pads.

    This is a TOPOLOGICAL count and not a geometric one, and the difference matters.
    An earlier draft built a graph whose nodes were copper polygons and whose edges were
    "these two polygons touch", and counted its cycles.  That over-reports by an order of
    magnitude: wherever two consecutive segments meet on top of their own pad, the three
    polygons touch each other pairwise and the count sees a triangle where the copper has
    no loop at all.  It reported 3 356 loops on a board that has far fewer.

    The model here is the one a router actually has.  Nodes are JUNCTIONS -- segment
    endpoints, via centres, pad centres -- merged when they coincide, when an endpoint
    lands inside a pad, or when an endpoint lands inside a via.  Edges are SEGMENTS.  A
    segment through whose interior another junction passes is split there, so a T is a T
    and not a chord.  The number of independent loops is then E - V + C, and every one of
    them is a second copper path between two points that already had one.

    Pour polygons are excluded deliberately: a plane is a sheet and every pair of points
    on it has infinitely many paths.  The finding is about redundant ROUTED copper.
    """
    v = []
    if not tracks:
        return v, 0

    # ---- nodes -------------------------------------------------------------
    # A node key is (net, layer_or_BOTH, x, y).  Vias and through-hole pads are BOTH.
    parent = {}

    def find(a):
        parent.setdefault(a, a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    def node(net, layer, x, y):
        k = (net, layer, round(x, 3), round(y, 3))
        find(k)
        return k

    # pads and vias, as anchors that swallow any endpoint landing on them
    anchors = defaultdict(list)          # net -> [(geom, layers, key)]
    for pd in board.pads():
        if not pd.net:
            continue
        lays = LAYERS if pd.tht else tuple(ly for ly in LAYERS if pd.on(ly))
        key = (pd.net, "PAD", pd.ref, pd.num)
        find(key)
        anchors[pd.net].append((pours.pad_poly(pd, 0.002), lays, key))
    for i, vv in enumerate(vias):
        key = (vv.net, "VIA", i, 0)
        find(key)
        anchors[vv.net].append((pours.via_poly(vv, 0.002), LAYERS, key))

    trees = {}
    for net, items in anchors.items():
        trees[net] = (items, STRtree([it[0] for it in items]))

    def anchor_of(net, layer, x, y):
        if net not in trees:
            return None
        items, tree = trees[net]
        p = Point(x, y)
        for j in tree.query(p):
            geom, lays, key = items[j]
            if layer in lays and geom.intersects(p):
                return key
        return None

    # ---- edges -------------------------------------------------------------
    # Every segment is an edge.  Its ends are anchored where they land on a pad or a
    # via, and merged with any other endpoint at the same coordinate on the same layer.
    seg_nodes = []
    for t in tracks:
        ends = []
        for x, y in ((t.x1, t.y1), (t.x2, t.y2)):
            a = anchor_of(t.net, t.layer, x, y)
            n = node(t.net, t.layer, x, y)
            if a is not None:
                union(a, n)
            ends.append(n)
        seg_nodes.append(ends)

    # T junctions: a node lying strictly inside another segment splits it.
    lines = [LineString([(t.x1, t.y1), (t.x2, t.y2)]) for t in tracks]
    ltree = STRtree(lines)
    extra_splits = defaultdict(set)
    for si, (a, b) in enumerate(seg_nodes):
        for key in (a, b):
            _, layer, x, y = key
            p = Point(x, y)
            for j in ltree.query(p.buffer(0.002)):
                if j == si or tracks[j].net != tracks[si].net:
                    continue
                if tracks[j].layer != layer:
                    continue
                t2 = tracks[j]
                if (abs(t2.x1 - x) < 0.003 and abs(t2.y1 - y) < 0.003) or \
                   (abs(t2.x2 - x) < 0.003 and abs(t2.y2 - y) < 0.003):
                    continue
                if lines[j].distance(p) <= 0.002:
                    extra_splits[j].add(key)

    # A segment whose two ends resolve to the SAME junction is a degenerate edge, not a
    # loop.  It happens constantly and harmlessly: the first 0.1 mm hop out of a via sits
    # entirely inside the via's own 0.60 mm pad, so both of its ends anchor to the via.
    # Counting those as loops reported two on ENV1_ABS, which has none.
    per_net_nodes = defaultdict(set)
    per_net_edges = defaultdict(int)
    real_edges = defaultdict(list)
    for si, (a, b) in enumerate(seg_nodes):
        net = tracks[si].net
        pts = [a] + sorted(extra_splits.get(si, ()),
                           key=lambda k: (k[2] - a[2]) ** 2 + (k[3] - a[3]) ** 2) + [b]
        for u, w in zip(pts, pts[1:]):
            ru, rw = find(u), find(w)
            if ru == rw:
                continue
            per_net_nodes[net].add(ru)
            per_net_nodes[net].add(rw)
            per_net_edges[net] += 1
            real_edges[net].append((ru, rw))

    # vias join the layers: the via node is one node, already unioned with every
    # endpoint that landed on it, so no extra edge is needed.
    total = 0
    for net in sorted(per_net_edges):
        nodes = {find(k) for k in per_net_nodes[net]}
        E = per_net_edges[net]
        V = len(nodes)
        # components, over the nodes this net actually uses
        roots = {}
        for k in nodes:
            roots.setdefault(k, 0)
        C = len(roots)
        # count components properly: walk the edges again
        seen = {}
        for ra, rb in real_edges[net]:
            seen.setdefault(ra, set()).add(rb)
            seen.setdefault(rb, set()).add(ra)
        comp, visited = 0, set()
        for k in nodes:
            if k in visited:
                continue
            comp += 1
            stack = [k]
            visited.add(k)
            while stack:
                cur = stack.pop()
                for nb in seen.get(cur, ()):
                    if nb not in visited:
                        visited.add(nb)
                        stack.append(nb)
        C = comp
        loops = E - V + C
        if loops > 0:
            total += loops
            v.append(("redundant copper path",
                      f"net {net}: {loops} independent copper loop"
                      f"{'s' if loops != 1 else ''} outside the planes "
                      f"({E} segments over {V} junctions in {C} "
                      f"component{'s' if C != 1 else ''})"))
    return v[:max_report], total


# --------------------------------------------------------------------------- 3
def segment_angles(tracks, max_report=None):
    """Finding 3: sharp inside corners, and 45-degree routing.

    Two checks, counted separately by the caller because they fail for different
    reasons.  The first is the finding as stated: where two segments of one net meet at
    a point, the angle between them, measured between the two directions leading AWAY
    from the joint, must be at least 90 degrees.  An acute inside corner traps etchant
    and concentrates current.

    The second is the other half of "45-degree routing": every segment must lie on a 0,
    45, 90 or 135 degree axis.  A segment at 63 degrees cannot make an acute corner on
    its own and is still not 45-degree routing.
    """
    v_angle, v_axis = [], []
    axes = rules.GEOMETRY["allowed_axes_deg"]
    tol = rules.GEOMETRY["axis_tol_deg"]
    floor_deg = rules.GEOMETRY["min_segment_angle_deg"]

    joints = defaultdict(list)          # (layer, net, point) -> [direction away]
    for i, t in enumerate(tracks):
        dx, dy = t.x2 - t.x1, t.y2 - t.y1
        if abs(dx) < 1e-9 and abs(dy) < 1e-9:
            continue
        ang = math.degrees(math.atan2(dy, dx)) % 180.0
        if min(abs(ang - a) for a in axes) > tol:
            v_axis.append(("segment off the 45-degree grid",
                           f"{t.net} on {t.layer}: segment "
                           f"({t.x1:.3f}, {t.y1:.3f})-({t.x2:.3f}, {t.y2:.3f}) lies at "
                           f"{ang:.2f} degrees"))
        joints[(t.layer, t.net, _key(t.x1, t.y1))].append(
            (math.degrees(math.atan2(dy, dx)) % 360.0, i))
        joints[(t.layer, t.net, _key(t.x2, t.y2))].append(
            (math.degrees(math.atan2(-dy, -dx)) % 360.0, i))

    for (layer, net, pt), dirs in joints.items():
        if len(dirs) < 2:
            continue
        for a in range(len(dirs)):
            for b in range(a + 1, len(dirs)):
                if dirs[a][1] == dirs[b][1]:
                    continue
                d = abs(dirs[a][0] - dirs[b][0]) % 360.0
                if d > 180.0:
                    d = 360.0 - d
                if d < floor_deg - 1e-6:
                    v_angle.append(("sharp inside corner",
                                    f"{net} on {layer} at ({pt[0]:.3f}, {pt[1]:.3f}): "
                                    f"two segments meet at {d:.1f} degrees, below the "
                                    f"{floor_deg:.0f} degree floor"))
    return (v_angle[:max_report], len(v_angle)), (v_axis[:max_report], len(v_axis))


# --------------------------------------------------------------------------- 4
def pad_entry(board, tracks, max_report=None):
    """Finding 4: off-centre pad entry.

    A track that ends on a pad must have its centreline pass through the pad centre.
    "Through" is given a number here because the finding does not have one: the
    perpendicular distance from the pad centre to the infinite line of the entering
    segment must be no more than `pad_entry_frac` of the pad's MINOR dimension --
    25 per cent, so on a 0.45 mm-wide TSSOP land the centreline may miss by 0.11 mm.

    A track that merely crosses a pad is not an entry and is not checked here; that is a
    clearance question and drc.py owns it.
    """
    v = []
    frac = rules.GEOMETRY["pad_entry_frac"]
    pads = [pd for pd in board.pads() if pd.net and not pd.ref.startswith("FID")]
    if not pads or not tracks:
        return v, 0
    geoms = [pours.pad_poly(pd, 0.002) for pd in pads]
    tree = STRtree(geoms)
    for t in tracks:
        for (ex, ey), which in (((t.x1, t.y1), "start"), ((t.x2, t.y2), "end")):
            p = Point(ex, ey)
            for j in tree.query(p):
                pd = pads[j]
                if pd.net != t.net:
                    continue
                if not pd.tht and not pd.on(t.layer):
                    continue
                if not geoms[j].intersects(p):
                    continue
                w, h = pd.size_rot()
                minor = min(w, h)
                allow = frac * minor
                dx, dy = t.x2 - t.x1, t.y2 - t.y1
                L = math.hypot(dx, dy)
                if L < 1e-9:
                    continue
                # perpendicular distance from the pad centre to the segment's own line
                miss = abs(dy * (pd.x - t.x1) - dx * (pd.y - t.y1)) / L
                if miss > allow + 1e-6:
                    v.append(("off-centre pad entry",
                              f"{t.net} on {t.layer}: the {which} of segment "
                              f"({t.x1:.3f}, {t.y1:.3f})-({t.x2:.3f}, {t.y2:.3f}) "
                              f"enters pad {pd.ref}.{pd.num} with its centreline "
                              f"{miss:.3f} mm off the pad centre, against "
                              f"{allow:.3f} mm allowed on a {minor:.2f} mm pad"))
    return v[:max_report], len(v)


# --------------------------------------------------------------------------- 5
def class_widths(tracks, vias, max_report=None):
    """Finding 5: no net classes.

    Three counts, because a class says three things: how wide its conductor must be, on
    which layers it may run, and whether it may have a via at all.  Rev B routed every
    net at the board floor when it had to, which is how 169 connections came to be
    relaxed with nothing to say that some of them were the wrong nets to relax.
    """
    v_w, v_l, v_v = [], [], []
    for t in tracks:
        c = rules.rule_for(t.net)
        if t.width < c.min_width - 1e-9:
            v_w.append(("under-width for its class",
                        f"{t.net} ({c.name}) on {t.layer}: {t.width:.3f} mm against a "
                        f"class minimum of {c.min_width:.2f} mm "
                        f"({c.pref_width:.2f} mm preferred)"))
        if t.layer not in c.layers:
            v_l.append(("net class on a forbidden layer",
                        f"{t.net} ({c.name}) has a segment on {t.layer}; the class is "
                        f"restricted to {'/'.join(c.layers)}"))
    for i, vv in enumerate(vias):
        c = rules.rule_for(vv.net)
        if not c.vias_allowed:
            v_v.append(("via on a class that may not have one",
                        f"{vv.net} ({c.name}) has a via at "
                        f"({vv.x:.3f}, {vv.y:.3f}); the class forbids vias"))
    return ((v_w[:max_report], len(v_w)), (v_l[:max_report], len(v_l)),
            (v_v[:max_report], len(v_v)))


# --------------------------------------------------------------------------- driver
def run_all(board, tracks, vias, pour_geo, max_report=None):
    """-> (violations, stats).  Violations are (kind, message) like drc.run's."""
    v = []
    stats = {}

    got, n = via_in_pad(board, vias, max_report)
    v += got
    stats["vias inside an SMD pad"] = n

    got, n = dangling_ends(board, tracks, vias, pour_geo, max_report)
    v += got
    stats["dangling track ends"] = n

    got, n = redundant_paths(board, tracks, vias, pour_geo, max_report)
    v += got
    stats["redundant copper loops"] = n

    (ga, na), (gx, nx) = segment_angles(tracks, max_report)
    v += ga + gx
    stats["sharp inside corners (< 90 deg)"] = na
    stats["segments off the 45-degree grid"] = nx

    got, n = pad_entry(board, tracks, max_report)
    v += got
    stats["off-centre pad entries"] = n

    (gw, nw), (gl, nl), (gv, nv) = class_widths(tracks, vias, max_report)
    v += gw + gl + gv
    stats["conductors under their class minimum"] = nw
    stats["net classes on a forbidden layer"] = nl
    stats["vias on a class that forbids them"] = nv

    return v, stats
