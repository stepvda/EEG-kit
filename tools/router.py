#!/usr/bin/env python3
"""
router.py -- constraint-aware two-layer autorouter for EEG-CAR-01 Rev B.

It is a raster maze router (Dijkstra on a 0.1 mm grid, two layers, via cost) with the
layout rules of DSN-EEG-003 section 3.1 encoded as costs and hard keep-outs:

  * the board is split at x = 58 mm.  Digital nets may not enter the analogue zone and
    analogue nets may not enter the digital zone (one declared exception, CMP_RAW).
  * electrode nets are routed on the top layer only, with the AGND_REF pour either side.
  * no via inside the ADS1299 module outlines or within 8 mm of the isolator module.
  * USB_DP and USB_DN are routed as a length-matched pair, short, with no stubs.
  * SPI is length-matched within 10 mm; DRDY gets no crossing trace beneath it.
  * AGND_REF joins DGND only at R90; HARN_SHIELD only at R91.

Ground and the analogue reference are not routed: they are copper pours on both layers,
built with shapely and connected through vias.

The router is deterministic: same input, same board.  Its output is checked by drc.py,
which measures real clearances on the finished geometry rather than trusting the grid.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass

from scipy import ndimage
from skimage.graph import MCP_Geometric

import design as D
import pcbgen

GRID = 0.1                      # mm per cell
VIA_PAD = 0.6          # 0.60 mm pad on a 0.30 mm finished hole: 0.15 mm annular
VIA_DRILL = 0.3        # ring, which every fabricator in the contact list does at
                       # standard price, and small enough to fit between the pads
LAYERS = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")
SIGNAL_LAYERS = (0, 3)          # L1 and L4 route; L2 and L3 are reference planes
PLANE_COST = 40.0               # a path may pass THROUGH a plane layer in a via, but
                                # travelling laterally on one costs 25x, so it does not


@dataclass
class Track:
    layer: str
    x1: float
    y1: float
    x2: float
    y2: float
    width: float
    net: str


@dataclass
class Via:
    x: float
    y: float
    pad: float
    drill: float
    net: str


# --------------------------------------------------------------------------- raster
def mm2c(v):
    return int(round(v / GRID))


class Raster:
    """Per-layer int32 map: 0 free, -1 hard keep-out, else the index of the owning net."""

    def __init__(self, w, h):
        self.nx = mm2c(w) + 1
        self.ny = mm2c(h) + 1
        self.epoch = 0
        self.occ = [np.zeros((self.ny, self.nx), np.int32) for _ in LAYERS]

    def snapshot(self):
        """Cheap copy of the occupancy maps.  Four array copies, a few milliseconds."""
        return (self.epoch, [a.copy() for a in self.occ])

    def restore(self, snap):
        self.epoch, occ = snap
        self.occ = [a.copy() for a in occ]

    def _disk(self, cx, cy, r):
        rc = int(math.ceil(r / GRID))
        x0, x1 = max(0, cx - rc), min(self.nx - 1, cx + rc)
        y0, y1 = max(0, cy - rc), min(self.ny - 1, cy + rc)
        if x1 < x0 or y1 < y0:
            return None
        yy, xx = np.ogrid[y0:y1 + 1, x0:x1 + 1]
        m = ((xx - cx) ** 2 + (yy - cy) ** 2) * GRID * GRID <= r * r
        return (slice(y0, y1 + 1), slice(x0, x1 + 1)), m

    def stamp_disk(self, layer, x, y, r, val):
        self.epoch += 1
        got = self._disk(mm2c(x), mm2c(y), r + GRID / 2)
        if not got:
            return
        sl, m = got
        tgt = self.occ[layer][sl]
        tgt[m & (tgt == 0)] = val
        if val == -1:
            tgt[m] = -1

    def stamp_rect(self, layer, x, y, w, h, val, grow=0.0):
        self.epoch += 1
        x0 = int(math.floor((x - w / 2 - grow) / GRID))
        x1 = int(math.ceil((x + w / 2 + grow) / GRID))
        y0 = int(math.floor((y - h / 2 - grow) / GRID))
        y1 = int(math.ceil((y + h / 2 + grow) / GRID))
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(self.nx - 1, x1), min(self.ny - 1, y1)
        if x1 < x0 or y1 < y0:
            return
        tgt = self.occ[layer][y0:y1 + 1, x0:x1 + 1]
        if val == -1:
            tgt[:] = -1
        else:
            tgt[tgt == 0] = val

    def stamp_seg(self, layer, x1, y1, x2, y2, r, val):
        self.epoch += 1
        n = max(2, int(math.hypot(x2 - x1, y2 - y1) / (GRID * 0.7)) + 1)
        for i in range(n + 1):
            t = i / n
            self.stamp_disk(layer, x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, r, val)


# --------------------------------------------------------------------------- router
class Router:
    def __init__(self, board: pcbgen.BoardV2, verbose=True):
        self.b = board
        self.verbose = verbose
        self.tracks: list[Track] = []
        self.vias: list[Via] = []
        self.failed: list[tuple] = []
        self.narrowed: list[tuple] = []
        self.dirty_vias = 0
        self.netid = {}
        for i, n in enumerate(sorted(board.nets()), start=1):
            self.netid[n] = i
        # net ids of the electrode class: every OTHER net owes their copper the
        # 0.35 mm electrode clearance, which is a DRC rule (drc.py measures it)
        # and was not encoded in the costs -- the former 0.328 mm electrode-net
        # violations of the first Rev B release, and five more on the first
        # rebuild, were vias legalised against the general 0.20 mm clearance
        # only.  All are gone; this cost term is why they cannot come back.
        self._elec_ids = frozenset(self.netid[n] for n in D.ELECTRODE_NETS
                                   if n in self.netid)
        self.r = Raster(board.width, board.height)
        self._distcache = {}
        self._seed()

    def log(self, *a):
        if self.verbose:
            print(*a, flush=True)

    # ------------------------------------------------------------------ obstacles
    def _seed(self):
        b = self.b
        # board edge keep-out: enough that even a via pad stays 0.3 mm inside
        eg = mm2c(0.75)
        for L in range(len(LAYERS)):
            self.r.occ[L][:eg, :] = -1
            self.r.occ[L][-eg:, :] = -1
            self.r.occ[L][:, :eg] = -1
            self.r.occ[L][:, -eg:] = -1

        # fiducials keep 2 mm of clear copper around them, on the top layer only
        for p in b.parts:
            if p.ref.startswith("FID"):
                self.r.stamp_disk(0, p.x, p.y, 2.0, -1)

        # pads
        for pd in b.pads():
            if pd.ref.startswith("FID"):
                continue
            val = self.netid.get(pd.net, -1) if pd.net else -1
            w, h = pd.size_rot()
            for L in range(len(LAYERS)):
                if not pd.tht and not pd.on(LAYERS[L]):
                    continue
                if pd.shape == "circle" or pd.kind == "np_thru_hole":
                    self.r.stamp_disk(L, pd.x, pd.y, w / 2, val)
                else:
                    self.r.stamp_rect(L, pd.x, pd.y, w, h, val)

        # non-plated holes: an M3 mounting hole gets a 3.0 mm copper keep-out radius,
        # a DIN retention post gets drill/2 + 0.45 mm.  Hard keep-out on both layers.
        for pd in b.pads():
            if pd.kind != "np_thru_hole":
                continue
            r = 3.0 if pd.drill > 2.5 else pd.drill / 2 + 0.45
            for L in range(len(LAYERS)):
                self.r.stamp_disk(L, pd.x, pd.y, r, -1)

        # via keep-out under the ADS module outlines and around the isolator
        self.no_via = np.zeros((self.r.ny, self.r.nx), bool)
        for ref, clr in D.NO_VIA_ZONES:
            part = self.b.part(ref)
            if not part:
                continue
            bx = self.b.courtyard_box(part)
            x0, y0 = mm2c(bx[0] - clr), mm2c(bx[1] - clr)
            x1, y1 = mm2c(bx[2] + clr), mm2c(bx[3] + clr)
            self.no_via[max(0, y0):y1 + 1, max(0, x0):x1 + 1] = True

        # the isolation barrier: nothing but the J10 module may come within 8 mm
        # The ADuM4160 module carries the barrier.  What the carrier must guarantee is
        # that no carrier copper sits under the module's HOST half: a 9 mm strip from the
        # J10 socket to the board edge.  Everything on the device side is at battery
        # potential and needs no separation.  See RISK-EEG-011 and DSN-EEG-003 3.1.4.
        self.iso_box = (141.0, 2.0, D.BOARD_W, 22.0)

        # zone masks
        self.x_mm = np.arange(self.r.nx) * GRID
        self.analog_col = self.x_mm < D.ZONE_SPLIT_X
        self.digital_col = self.x_mm > D.ZONE_SPLIT_X

    # ------------------------------------------------------------------ helpers
    def _dist(self, layer, netv):
        """Distance in mm from every cell to the nearest copper that is NOT this net.

        One Euclidean distance transform per (layer, net) answers the clearance question
        for every track width at once, which is what makes the width ladder affordable.
        The cache is dropped whenever anything is stamped into the raster.
        """
        key = (layer, netv, self.r.epoch)
        d = self._distcache.get(key)
        if d is None:
            occ = self.r.occ[layer]
            free = (occ == 0) | (occ == netv)
            d = ndimage.distance_transform_edt(free) * GRID
            if len(self._distcache) > 16:
                self._distcache.clear()
            self._distcache[key] = d
        return d

    def _dist_elec(self, layer):
        """Distance in mm from every cell to the nearest ELECTRODE-net copper.

        Net-independent (a non-electrode net is never electrode copper), so one
        transform per (layer, epoch) serves every net; the sentinel id -1 keys
        it into the same cache as the per-net transforms.
        """
        key = (layer, -1, self.r.epoch)
        d = self._distcache.get(key)
        if d is None:
            occ = self.r.occ[layer]
            free = ~np.isin(occ, list(self._elec_ids))
            d = ndimage.distance_transform_edt(free) * GRID
            if len(self._distcache) > 16:
                self._distcache.clear()
            self._distcache[key] = d
        return d

    def _free_mask(self, layer, netv, half_w, clearance):
        """Cells whose centre can carry a track of half-width half_w for net netv."""
        m = self._dist(layer, netv) >= (half_w + clearance + 0.09)
        if netv not in self._elec_ids:
            # electrode copper keeps 0.35 mm to EVERYTHING (drc.py rule), not
            # just to what the electrode net itself was routed with
            m &= self._dist_elec(layer) >= (half_w + 0.35 + 0.09)
        return m

    def _cost(self, net, half_w, clearance, top_only=False):
        """Cost per cell, four layers.

        L1 and L4 carry signals.  L2 and L3 are reference planes: a through-via crosses
        them, so the cell has to be traversable, but only where a via would clear the
        plane's anti-pad, and travelling laterally there is priced out of existence.
        """
        cost = np.full((len(LAYERS), self.r.ny, self.r.nx), np.inf, np.float64)
        netv = self.netid[net]
        for L in range(len(LAYERS)):
            if L in SIGNAL_LAYERS:
                free = self._free_mask(L, netv, half_w, clearance)
                c = np.where(free, 1.0, np.inf)
                if L == 3:
                    c = c * 1.15          # a mild preference for the top layer
            else:
                # A plane layer is not a routing surface: the only legal way to
                # occupy a cell here is a through-via drilled at it.  Gate these
                # cells on the via actually fitting -- pad clear of foreign
                # copper on ALL FOUR layers, the same test _legalise_vias
                # applies -- so the maze can only change layers where a via is
                # buildable.  The old gate (clearance on this plane layer alone,
                # need = pad/2 + 0.25) let the search dive where no via could
                # ever be legalised, and worse, let it travel SIDEWAYS along
                # the plane at PLANE_COST: _commit lays no copper on a plane,
                # so such a "route" was two vias joined by nothing, counted as
                # routed while the net stayed open.  Measured on the Rev B
                # route: V5V J1.11->J6.21 "closed" through 1.5 mm of lateral
                # In2.Cu travel.  route_pair now also rejects any residual
                # lateral plane move after traceback.
                clr_via = 0.35 if net in D.ELECTRODE_NETS else 0.20
                need = VIA_PAD / 2 + clr_via + 0.10
                need_e = VIA_PAD / 2 + 0.35 + 0.10
                ok = np.ones((self.r.ny, self.r.nx), bool)
                for LL in range(len(LAYERS)):
                    ok &= self._dist(LL, netv) >= need
                    if netv not in self._elec_ids:
                        ok &= self._dist_elec(LL) >= need_e
                c = np.where(ok, PLANE_COST, np.inf)
            if net in D.DIGITAL_ONLY_NETS:
                c[:, self.analog_col] = np.inf
            elif net in D.ANALOG_ZONE_NETS:
                c[:, self.digital_col] = np.inf
            if top_only and L != 0:
                c[:] = np.inf
            cost[L] = c
        x0, y0, x1, y1 = self.iso_box
        # Hard keep-out for EVERY net.  An older revision exempted the USB
        # pair, VDD_ISO and DGND so they could reach a J10 that sat further
        # right; J10's pad column is at x = 136 and the strip starts at 141,
        # so nothing needs it -- and drc.py forbids copper there for all nets,
        # which is how one exempted DGND track became a violation.
        #
        # The blank is inflated by what the cell would CARRY: drc.py measures
        # finished copper, and a 0.56 mm track whose centreline passes 0.2 mm
        # outside the box still overhangs into it -- three DGND segments did
        # exactly that at the box's south-west corner on the Rev B rebuild.
        # Plane cells are via sites, so they inflate by the via pad radius.
        for L in range(len(LAYERS)):
            grow = (half_w if L in SIGNAL_LAYERS else VIA_PAD / 2) + 0.05
            cost[L,
                 max(0, mm2c(y0 - grow)):mm2c(y1 + grow) + 1,
                 max(0, mm2c(x0 - grow)):mm2c(x1 + grow) + 1] = np.inf
        return cost

    def _pad_nodes(self, pad):
        """Grid nodes that lie strictly inside this pad's copper, per layer.

        The shape matters: a round pad's bounding box has corners outside the copper,
        and a track that starts there is not electrically connected to anything.
        """
        out = []
        w, h = pad.size_rot()
        cx, cy = mm2c(pad.x), mm2c(pad.y)
        margin = 0.12                      # stay this far inside the pad edge
        round_pad = pad.shape == "circle" or pad.kind == "np_thru_hole"
        rx = max(1, mm2c(w / 2 - margin))
        ry = max(1, mm2c(h / 2 - margin))
        rr = (w / 2 - margin) ** 2
        for L in range(len(LAYERS)):
            if not pad.tht and not pad.on(LAYERS[L]):
                continue
            for dx in range(-rx, rx + 1):
                for dy in range(-ry, ry + 1):
                    if round_pad and (dx * GRID) ** 2 + (dy * GRID) ** 2 > rr:
                        continue
                    x, y = cx + dx, cy + dy
                    if 0 <= x < self.r.nx and 0 <= y < self.r.ny:
                        out.append((L, y, x))
        return out

    # ------------------------------------------------------------------ MST
    @staticmethod
    def _mst(points):
        n = len(points)
        if n < 2:
            return []
        used = [0]
        rest = list(range(1, n))
        edges = []
        while rest:
            best = None
            for a in used:
                for bi in rest:
                    d = ((points[a][0] - points[bi][0]) ** 2
                         + (points[a][1] - points[bi][1]) ** 2)
                    if best is None or d < best[0]:
                        best = (d, a, bi)
            _, a, bi = best
            edges.append((a, bi))
            used.append(bi)
            rest.remove(bi)
        return edges

    # ------------------------------------------------------------------ one connection
    def route_pair(self, net, pa, pb, width, clearance, top_only=False, margin=25.0):
        cost = self._cost(net, width / 2, clearance, top_only)
        # Signal-layer nodes only.  A THT pad reaches both signal layers by its
        # own barrel; letting the path begin or end ON a plane-layer node
        # invites a lateral first or last step there, which the check below
        # would then reject.
        starts = [n for n in self._pad_nodes(pa) if n[0] in SIGNAL_LAYERS]
        ends = [n for n in self._pad_nodes(pb) if n[0] in SIGNAL_LAYERS]
        if not starts or not ends:
            return False
        # restrict the search to a window
        xs = [pa.x, pb.x]
        ys = [pa.y, pb.y]
        x0, x1 = mm2c(min(xs) - margin), mm2c(max(xs) + margin)
        y0, y1 = mm2c(min(ys) - margin), mm2c(max(ys) + margin)
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(self.r.nx - 1, x1), min(self.r.ny - 1, y1)
        sub = cost[:, y0:y1 + 1, x0:x1 + 1].copy()
        # allow the two pads themselves
        for L, y, x in starts + ends:
            if y0 <= y <= y1 and x0 <= x <= x1:
                sub[L, y - y0, x - x0] = 1.0
        # Forbid VIAS where they are not allowed: the two plane layers are the
        # only cells a via can occupy, so blanking them inside the box is the
        # whole rule (DSN-EEG-003 3.1.3 as drc.py checks it -- a via keep-out).
        # Until iteration 5 this also blanked B.Cu, forbidding TRAVEL under the
        # module outlines, which the rule never asked for; that over-reach was
        # the last wall around AVSS2 J29.2, SPARE1 J4.7 and AVSS J23.6, all of
        # which need a bottom-layer pass beneath J29/J4/J23 with the vias
        # outside the box.  Iteration 5 (reports/drc_05_FULL.txt): the three
        # closed, plus AVSS U7.2 -- 143 of 145 nets, zero clearance violations.
        nv = self.no_via[y0:y1 + 1, x0:x1 + 1]
        for _L in (1, 2):
            sub[_L][nv] = np.inf
        sampling = (VIA_COST_MM, GRID, GRID)
        try:
            mcp = MCP_Geometric(sub, sampling=sampling, fully_connected=True)
            s = [(L, y - y0, x - x0) for L, y, x in starts if y0 <= y <= y1 and x0 <= x <= x1]
            e = [(L, y - y0, x - x0) for L, y, x in ends if y0 <= y <= y1 and x0 <= x <= x1]
            if not s or not e:
                return False
            costs, _ = mcp.find_costs(s, e, find_all_ends=False)
            finite = [(costs[t], t) for t in e if np.isfinite(costs[t])]
            if not finite:
                return False
            _, tgt = min(finite)
            path = mcp.traceback(tgt)
        except Exception:
            return False
        path = [(L, y + y0, x + x0) for (L, y, x) in path]
        path = self._legalise_vias(net, path, width, clearance)
        if path is None:
            return False
        # No move that involves a plane layer may change position: a through-
        # via is a vertical stack of cells, and anything else -- a lateral run
        # on the plane, or a diagonal staircase across it -- commits vias with
        # no conductor between them and reports a connection that is not there.
        for (L1, y1, x1), (L2, y2, x2) in zip(path, path[1:]):
            if ((y1, x1) != (y2, x2)
                    and (L1 not in SIGNAL_LAYERS or L2 not in SIGNAL_LAYERS)):
                return False
        # The path must still LAND on both pads.  _legalise_vias slides layer
        # changes along the path, and sliding one over either end leaves the
        # final approach on a layer the pad has no copper on.  Measured on the
        # Rev B repair passes: EMG3 D14.3 -> C14.1 ended on B.Cu underneath an
        # F.Cu-only pad, the net counted as repaired, and the repair loop
        # oscillated for eight passes re-committing the same dead copper.
        for pd, (L, _, _) in ((pa, path[0]), (pb, path[-1])):
            if pd.tht:
                if L not in SIGNAL_LAYERS:
                    return False
            elif not pd.on(LAYERS[L]):
                return False
        self._commit(net, path, width, clearance)
        return True

    @staticmethod
    def _compress(path):
        """Collapse a through-via (three layer changes at one cell) into one transition."""
        out = [path[0]]
        i = 1
        while i < len(path):
            L, y, x = path[i]
            pL, py, px = out[-1]
            if y == py and x == px:
                out[-1] = (L, y, x)          # same cell, later layer wins
            else:
                out.append((L, y, x))
            i += 1
        return out

    def _legalise_vias(self, net, path, width, clearance, window=90):
        """Move every layer change to a point where a via actually fits.

        The maze search only knows the track width, but a via pad is 0.8 mm across, so a
        layer change the search thought was legal can leave the via inside another net's
        clearance.  Rather than fix that afterwards, the transition is slid along the path
        to the nearest point where a via clears foreign copper on BOTH layers.  If there is
        no such point within `window` cells, the route is rejected and the caller tries a
        narrower or a different one.
        """
        path = self._compress(path)
        netv = self.netid[net]
        need = VIA_PAD / 2 + (0.35 if net in D.ELECTRODE_NETS else 0.2) + 0.10
        need_e = VIA_PAD / 2 + 0.35 + 0.10
        dists = [self._dist(L, netv) for L in range(len(LAYERS))]
        edists = (None if netv in self._elec_ids
                  else [self._dist_elec(L) for L in range(len(LAYERS))])
        half = width / 2

        def via_ok(i):
            _, y, x = path[i]
            if self.no_via[y, x]:
                return False
            if not all(d[y, x] >= need for d in dists):
                return False
            return edists is None or all(d[y, x] >= need_e for d in edists)

        def usable(i, layer):
            _, y, x = path[i]
            if layer not in SIGNAL_LAYERS:
                return via_ok(i)
            if dists[layer][y, x] < half + clearance:
                return False
            return edists is None or edists[layer][y, x] >= half + 0.35

        out = list(path)
        n = len(out)
        for i in range(n - 1):
            if out[i][0] == out[i + 1][0]:
                continue
            if via_ok(i):
                continue
            src, dst = out[i][0], out[i + 1][0]
            best = None
            for j in range(max(0, i - window), min(n, i + window + 1)):
                if not via_ok(j):
                    continue
                lo, hi = (j, i) if j < i else (i + 1, j)
                layer = dst if j < i else src
                if all(usable(k, layer) for k in range(lo, hi + 1)):
                    if best is None or abs(j - i) < abs(best - i):
                        best = j
            if best is None:
                self.dirty_vias += 1
                return None

            if best < i:
                for k in range(best + 1, i + 1):
                    out[k] = (dst, out[k][1], out[k][2])
            else:
                for k in range(i + 1, best + 1):
                    out[k] = (src, out[k][1], out[k][2])
        return out

    def _commit(self, net, path, width, clearance):
        netv = self.netid[net]
        pts = [(L, x * GRID, y * GRID) for (L, y, x) in path]
        norm = [pts[0]]
        for (L1, x1, y1), (L2, x2, y2) in zip(pts, pts[1:]):
            if L1 != L2 and (abs(x1 - x2) > 1e-9 or abs(y1 - y2) > 1e-9):
                norm.append((L2, x1, y1))
            norm.append((L2, x2, y2))
        simple = _simplify(norm)
        for (L1, x1, y1), (L2, x2, y2) in zip(simple, simple[1:]):
            if L1 != L2:
                # one through-via, all four layers, placed once however many layer
                # boundaries the path crosses at this point
                if not (self.vias and abs(self.vias[-1].x - x1) < 1e-9
                        and abs(self.vias[-1].y - y1) < 1e-9
                        and self.vias[-1].net == net):
                    self.vias.append(Via(x1, y1, VIA_PAD, VIA_DRILL, net))
                    for L in range(len(LAYERS)):
                        self.r.stamp_disk(L, x1, y1, VIA_PAD / 2, netv)
                continue
            if L1 not in SIGNAL_LAYERS:
                continue
            if abs(x1 - x2) < 1e-9 and abs(y1 - y2) < 1e-9:
                continue
            self.tracks.append(Track(LAYERS[L1], x1, y1, x2, y2, width, net))
            self.r.stamp_seg(L1, x1, y1, x2, y2, width / 2, netv)

    def try_ladder(self, net, pa, pb, width, clearance, top_only):
        """Preferred geometry first; then narrower, down to the board minimum.

        The clearance floor is the net's own: an electrode net keeps its 0.35 mm to
        everything else however tight the route gets, because that number is a safety
        margin and not a routing preference.
        """
        floor = 0.35 if net in D.ELECTRODE_NETS else 0.20
        for w, c, top, marg in ((width, clearance, top_only, 30.0),
                                (width, clearance, False, 200.0),
                                (max(0.25, width * 0.7), max(0.25, floor), False, 200.0),
                                (0.20, floor, False, 200.0),
                                (0.20, floor, True, 200.0)):
            if self.route_pair(net, pa, pb, w, c, top_only=top, margin=marg):
                if w < width or c < clearance:
                    self.narrowed.append((net, f"{pa.ref}.{pa.num}", f"{pb.ref}.{pb.num}",
                                          w, c))
                return True
        return False

    # ------------------------------------------------------------------ rip-up
    def rebuild(self):
        """Re-seed the obstacle raster and re-stamp every surviving track and via."""
        self.r = Raster(self.b.width, self.b.height)
        self._distcache = {}
        self._seed()
        for t in self.tracks:
            L = LAYERS.index(t.layer)
            self.r.stamp_seg(L, t.x1, t.y1, t.x2, t.y2, t.width / 2,
                             self.netid.get(t.net, -1))
        for v in self.vias:
            for L in range(len(LAYERS)):
                self.r.stamp_disk(L, v.x, v.y, v.pad / 2, self.netid.get(v.net, -1))

    # MEASURED, not guessed.  A rip-up costs about 4 s at max_nets 2-4 and can reach a
    # minute on a congested corridor at max_nets 8, and it usually FAILS -- the corridor is
    # blocked by geometry, not by a couple of tracks that happen to be in the way.  Plain
    # try_ladder, at 0.4 s, closes most of what is closeable.  A budget of 240 was set
    # without measuring and cost about four hours per repair pass; 30 bounds the work to a
    # couple of minutes and gives up nothing that was actually being won.
    MAX_RIPUPS = 30

    def ripup_retry(self, net, pa, pb, width, clearance, max_nets=5):
        """Tear up the nets that block a corridor, route through it, then put them back."""
        from shapely.geometry import LineString
        if len(getattr(self, "ripped", [])) >= self.MAX_RIPUPS:
            return False
        corridor = LineString([(pa.x, pa.y), (pb.x, pb.y)]).buffer(3.0)
        blockers = {}
        for t in self.tracks:
            if t.net in (net, "DGND", "AGND_REF"):
                continue
            seg = LineString([(t.x1, t.y1), (t.x2, t.y2)])
            if seg.intersects(corridor):
                blockers[t.net] = blockers.get(t.net, 0) + 1
        if not blockers:
            return False
        victims = [n for n, _ in sorted(blockers.items(), key=lambda kv: -kv[1])][:max_nets]
        kept_t = [t for t in self.tracks if t.net not in victims]
        kept_v = [v for v in self.vias if v.net not in victims]
        saved_t, saved_v = self.tracks, self.vias
        saved_raster = self.r.snapshot()          # see the rollbacks below
        saved_cache = self._distcache
        self.tracks, self.vias = kept_t, kept_v
        self.rebuild()
        if not self.try_ladder(net, pa, pb, width, clearance, False):
            self.tracks, self.vias = saved_t, saved_v
            self.r.restore(saved_raster)
            self._distcache = saved_cache
            return False
        # Put the victims back -- and this has to be ALL OR NOTHING.
        #
        # An earlier version recorded whatever it could not restore and returned True
        # anyway, so a rip-up that closed one connection and broke four counted as a
        # success.  The repair loop then oscillated: 26 broken nets became 33, became 31,
        # and never converged, because every pass traded working copper for a net it wanted
        # more.  A rip-up is only worth taking if the board afterwards is strictly better,
        # so if any victim cannot be restored the whole thing is rolled back.
        lost = []
        nets = self.b.nets()
        for vnet in victims:
            pads = nets[vnet]
            cls = D.netclass_of(vnet)
            w, c = D.NETCLASS[cls]
            for a, bi in self._mst([(p.x, p.y) for p in pads]):
                if not self.try_ladder(vnet, pads[a], pads[bi], w, c, False):
                    lost.append((vnet, f"{pads[a].ref}.{pads[a].num}",
                                 f"{pads[bi].ref}.{pads[bi].num}"))
        if lost:
            self.tracks, self.vias = saved_t, saved_v
            self.r.restore(saved_raster)
            self._distcache = saved_cache
            return False
        self.ripped = getattr(self, "ripped", [])
        self.ripped.append((net, victims, 0))
        return True

    # ------------------------------------------------------------------ drive
    def route_all(self, order, checkpoint_every=25, checkpoint_path="route_partial.pkl"):
        """Route every net in `order`.

        Checkpoints every `checkpoint_every` nets.  This environment kills a build somewhere
        past ten minutes and the routing phase takes about twelve, so six consecutive runs
        were lost mid-route with nothing to show.  A partial checkpoint turns that from
        "start again" into "carry on", and resume_route() below picks it up.  Writing it
        costs a fraction of a second against the minutes it saves.
        """
        import pickle
        nets = self.b.nets()
        done = 0
        for net in order:
            pads = nets.get(net, [])
            if len(pads) < 2:
                continue
            cls = D.netclass_of(net)
            width, clearance = D.NETCLASS[cls]
            top_only = cls == "ELECTRODE"
            pts = [(p.x, p.y) for p in pads]
            ok = 0
            for a, bi in self._mst(pts):
                if self.try_ladder(net, pads[a], pads[bi], width, clearance, top_only):
                    ok += 1
                else:
                    self.failed.append((net, pads[a].ref + "." + pads[a].num,
                                        pads[bi].ref + "." + pads[bi].num))
            self.log(f"  {net:14s} {len(pads):3d} pads  {ok} connections")
            done += 1
            if checkpoint_every and done % checkpoint_every == 0:
                try:
                    with open(checkpoint_path, "wb") as f:
                        pickle.dump({"tracks": self.tracks, "vias": self.vias,
                                     "failed": self.failed, "narrowed": self.narrowed,
                                     "iso_box": self.iso_box, "netid": self.netid,
                                     "routed_nets": done, "order": list(order)}, f)
                    self.log(f"  ... partial checkpoint after {done} nets "
                             f"({len(self.tracks)} segments)")
                except Exception as e:          # never let a checkpoint kill a build
                    self.log(f"  ... checkpoint failed ({e}); continuing")


VIA_COST_MM = 0.06     # spacing of the layer axis.  A through-via crosses three
                       # boundaries at PLANE_COST, so it costs about 9.7 units, which is
                       # the same as 97 mm of straight track -- expensive enough that the
                       # router prefers to stay on a layer, cheap enough that it will
                       # change when it has to.  Travelling laterally on a plane costs
                       # 40x a signal layer, so it never does.    # a layer change costs the same as 4 mm of track


def _simplify(pts, tol=1e-9):
    """Collapse collinear runs of grid steps into straight segments."""
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        L0, x0, y0 = out[-1]
        L1, x1, y1 = pts[i]
        L2, x2, y2 = pts[i + 1]
        if L0 != L1 or L1 != L2:
            out.append(pts[i])
            continue
        cross = (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)
        if abs(cross) > 1e-9:
            out.append(pts[i])
    out.append(pts[-1])
    return out
