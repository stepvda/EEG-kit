#!/usr/bin/env python3
"""
build_board.py -- route EEG-CAR-01 Rev B, pour the reference planes, stitch, verify.

Run:  python3 build_board.py            (writes routed.pkl next to the tools)
      python3 build_board.py --plot     (also writes a routed-board picture)

The result object is consumed by gerber.py, drawings.py, drc.py and kicad_write.py.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
import pickle
import sys
import time

import numpy as np
from shapely.geometry import Point
from shapely.ops import unary_union

import design as D
import pcbgen
import pours
import router as R

POUR_NETS = [("AGND_REF", 0.0, D.ZONE_SPLIT_X - pours.ZONE_GAP / 2),
             ("DGND", D.ZONE_SPLIT_X + pours.ZONE_GAP / 2, D.BOARD_W)]
# L2 and L3 are solid reference planes.  L1 and L4 carry signals and are not poured, so
# both routing surfaces are fully available and every trace has a continuous plane
# 0.2 mm beneath or above it.
PLANE_LAYERS = ("In1.Cu", "In2.Cu")

# routing priority: the most constrained and the most sensitive first
PRIORITY = (
    # Signals first, power last.  A supply rail tolerates a detour and a narrow track;
    # a signal that has to reach one pin of a 2.54 mm socket does not.  Routing the
    # thirty-pad AVDD, AVSS and DVDD3V3 trees early filled the board and starved the
    # I2S, button and UART nets that only had one way in.
    ["USB_DP", "USB_DN"]
    + [f"E_{s}" for s in ("Fz", "Cz", "Pz", "C3", "C4", "T7", "T8", "F7")]
    + ["REF_L", "REF_R", "BIAS_EL", "EMGIN1", "EMGIN2", "EMGIN3", "EOGIN1", "EOGIN2"]
    + [f"IN{i}" for i in range(1, 9)]
    + ["SRB1", "BIASOUT", "BIASIN", "EMG1", "EMG2", "EMG3", "SPARE1", "SPARE2"]
    + ["ENV_STIM", "ENV_VOICE", "ENV_ROOM"]
    + [f"ENV{k}_{s}" for k in (1, 2, 3)
       for s in ("AC", "INM", "ROUT", "HW", "SUM", "ABS", "MID", "INP", "FLT", "DIV")]
    + ["ENV_THR", "CMP_RAW", "ENV_CMP"]
    # the contact-light bus is electrically trivial and geometrically the most
    # constrained thing on the board: eleven conductors crossing the whole digital zone
    + ["LED_SR_DATA", "LED_SR_CLK", "LED_SR_LATCH", "LED_PWM", "LED_V", "LED_GND",
       "LED_OE", "LED_MR"]
    + [f"SR_Q{i}" for i in range(8)] + [f"LED{i}" for i in range(1, 9)]
    + ["I2S_MCLK", "I2S_BCLK", "I2S_LRCK", "I2S_DIN", "I2S_DOUT"]
    + ["DRDY", "SCLK", "MOSI", "MISO", "CS", "START", "RESET", "CLK_ADS", "DAISY"]
    + ["SDA", "SCL", "SD_CLK", "SD_CMD", "SD_D0"]
    + ["HP_TAP", "VOICE_PRE", "VOICE_RAW", "ROOM_PRE", "HP_L", "HP_R", "HP_GND"]
    + ["BTN_A", "BTN_B", "BTN_STOP", "MIC_MUTE", "CHG_CE", "VBUS_DET", "BOOST_EN",
       "RESET_EN", "UART_TX", "UART_RX", "HARN_SHIELD"]
    # power rails last
    + ["VBAT", "VBUS_IN", "VBUS_CHG", "VSYS", "V5V", "VDD_ISO", "DVDD3V3"]
    + ["AVDD2", "AVSS2", "AVDD", "AVSS"]
)


def _place_ground_via(rt, pd, dists=(1.15, 1.4, 1.7, 2.0, 2.4), n_ang=16):
    """Drop a via next to a surface-mount reference pad and link it with a short track."""
    netv = rt.netid[pd.net]
    need = R.VIA_PAD / 2 + 0.3
    # electrode copper keeps 0.35 mm to everything; the occ-disk test below
    # only guarantees 0.30 mm from the via pad edge, which drc.py would flag
    need_e = R.VIA_PAD / 2 + 0.35 + 0.05
    for dist in dists:
        for k in range(n_ang):
            a = 2 * math.pi * k / n_ang
            x, y = pd.x + dist * math.cos(a), pd.y + dist * math.sin(a)
            if not (1.5 < x < D.BOARD_W - 1.5 and 1.5 < y < D.BOARD_H - 1.5):
                continue
            cx, cy = R.mm2c(x), R.mm2c(y)
            if rt.no_via[cy, cx]:
                continue
            if any(rt._dist_elec(L)[cy, cx] < need_e for L in (0, 3)):
                continue
            # the isolation strip takes no copper at all, and the via PAD is
            # copper -- reject candidates whose pad would overhang the box
            ix0, iy0, ix1, iy1 = rt.iso_box
            pr = R.VIA_PAD / 2 + 0.05
            if (x + pr > ix0 and x - pr < ix1
                    and y + pr > iy0 and y - pr < iy1):
                continue
            ok = True
            for L in range(len(R.LAYERS)):
                got = rt.r._disk(cx, cy, need)
                if not got:
                    ok = False
                    break
                sl, m = got
                sub = rt.r.occ[L][sl][m]
                if np.any((sub != 0) & (sub != netv)):
                    ok = False
                    break
            if not ok:
                continue
            # the short link from the pad to the via must also be clear
            r_link = 0.15 + 0.3
            n = 12
            clash = False
            for i in range(n + 1):
                t = i / n
                px, py = pd.x + (x - pd.x) * t, pd.y + (y - pd.y) * t
                got = rt.r._disk(R.mm2c(px), R.mm2c(py), r_link)
                sl, m = got
                sub = rt.r.occ[0][sl][m]
                if np.any((sub != 0) & (sub != netv)):
                    clash = True
                    break
            if clash:
                continue
            rt.vias.append(R.Via(x, y, R.VIA_PAD, R.VIA_DRILL, pd.net))
            # ALL four layers.  This stamped layers 0 and 1 only, and build()
            # goes straight from here into route_all() without a rebuild, so
            # for the whole main routing pass the 69 reference vias had no
            # footprint on In2.Cu or B.Cu: bottom-layer tracks were laid across
            # their pads and viafix then had to move the vias out from under
            # them ("via push: 20 vias moved" every build), deleting the ones
            # it could not move -- which is how AGND_REF U1.3 lost its via.
            for L in range(len(R.LAYERS)):
                rt.r.stamp_disk(L, x, y, R.VIA_PAD / 2, netv)
            rt.tracks.append(R.Track("F.Cu", pd.x, pd.y, x, y, 0.3, pd.net))
            rt.r.stamp_seg(0, pd.x, pd.y, x, y, 0.15, netv)
            return True
    return False


def _tht_anchor(board, poly, net):
    for pd in board.pads():
        if pd.net == net and pd.tht and poly.intersects(pours.pad_poly(pd, 0.01)):
            return True
    return False


def _dedupe(rt, verbose=False):
    """Drop exact duplicate segments and vias.

    The segment key is the ORDERED endpoint pair, normalised so that a segment and its
    reverse compare equal.  An earlier version keyed on the bounding box, which is not the
    same thing: two different diagonals across the same box would have been treated as
    duplicates and one of them silently deleted.
    """
    seen_t, uniq_t = set(), []
    for t in rt.tracks:
        a = (round(t.x1, 3), round(t.y1, 3))
        b = (round(t.x2, 3), round(t.y2, 3))
        k = (t.layer, t.net, min(a, b), max(a, b), round(t.width, 3))
        if k in seen_t:
            continue
        seen_t.add(k)
        uniq_t.append(t)
    seen_v, uniq_v = set(), []
    for v in rt.vias:
        k = (round(v.x, 3), round(v.y, 3))      # a hole is a hole, whatever net claims it
        if k in seen_v:
            continue
        seen_v.add(k)
        uniq_v.append(v)
    if verbose and (len(rt.tracks) != len(uniq_t) or len(rt.vias) != len(uniq_v)):
        print(f"  deduplicated: {len(rt.tracks)-len(uniq_t)} segments and "
              f"{len(rt.vias)-len(uniq_v)} vias removed")
    rt.tracks, rt.vias = uniq_t, uniq_v


def build(verbose=True, plot=None):
    t0 = time.time()
    board = pcbgen.BoardV2()
    errs, warns = board.validate()
    if errs:
        for e in errs:
            print("PLACEMENT ERROR", e)
        raise SystemExit("placement is not clean; fix design.py first")

    rt = R.Router(board, verbose=verbose)
    nets = board.nets()

    # Every surface-mount pad on a reference net gets its own via down to the plane
    # before signal routing starts, so the router treats them as fixed obstacles and
    # no decoupling capacitor is left stranded on a top-layer island.
    gnd_vias = 0
    for pd in sorted(board.pads(), key=lambda p: (p.ref, p.num)):
        if pd.net not in ("DGND", "AGND_REF") or pd.tht or pd.ref.startswith("FID"):
            continue
        if not _place_ground_via(rt, pd):
            print(f"   no room for a plane via at {pd.ref}.{pd.num} ({pd.net})")
        else:
            gnd_vias += 1
    if verbose:
        print(f"{gnd_vias} plane vias placed at surface-mount reference pads")

    order = [n for n in PRIORITY if n in nets]
    order += [n for n in sorted(nets)
              if n not in order and n not in ("DGND", "AGND_REF")
              and len(nets[n]) > 1]
    if verbose:
        print(f"routing {len(order)} nets ({sum(len(nets[n]) for n in order)} pads)")
    rt.route_all(order)

    if rt.failed:
        retry, rt.failed = rt.failed, []
        if verbose:
            print(f"second pass over {len(retry)} unrouted connections "
                  f"(constraints relaxed one step at a time)")
        padmap = {f"{p.ref}.{p.num}": p for p in board.pads()}
        for net, a, b in retry:
            pa, pb = padmap[a], padmap[b]
            cls = D.netclass_of(net)
            w, c = D.NETCLASS[cls]
            if rt.try_ladder(net, pa, pb, w, c, False):
                if verbose:
                    print(f"   recovered {net} {a} -> {b}")
            else:
                rt.failed.append((net, a, b))

    # ---------------------------------------------------------------- pours
    if verbose:
        print(f"routing done in {time.time()-t0:.0f}s; "
              f"{len(rt.tracks)} segments, {len(rt.vias)} vias, "
              f"{len(rt.failed)} unrouted connections")
    if verbose:
        print("  ... building the reference planes", flush=True)
    pour_geo = {}
    for layer in PLANE_LAYERS:
        for net, x_lo, x_hi in POUR_NETS:
            pour_geo[(layer, net)] = pours.build(
                board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                clearance=0.35, iso_box=rt.iso_box)
    if verbose:
        for k, g in pour_geo.items():
            print(f"  pour {k[0]:5s} {k[1]:9s} {len(pours.polys(g)):3d} islands, "
                  f"{g.area:7.1f} mm2")

    if verbose:
        print("  ... stitching the planes", flush=True)
    # With planes on L2 and L3, every through-hole pad of a reference net reaches both
    # of them by its own barrel and every surface-mount pad reaches them through the via
    # placed beside it, so no separate stitching pass is needed.  What is worth doing is
    # tying the two planes together away from the pads.
    stitch = []
    for net, x_lo, x_hi in POUR_NETS:
        g1 = pour_geo[("In1.Cu", net)]
        g2 = pour_geo[("In2.Cu", net)]
        both = g1.intersection(g2)
        if both.is_empty:
            continue
        obstacles = unary_union(
            [pours.pad_poly(p, 0.35) for p in board.pads() if p.net != net]
            + [pours.track_poly(t, 0.35) for t in rt.tracks if t.net != net]
            + [pours.via_poly(v, 0.35) for v in rt.vias if v.net != net])
        step = 12.0
        x = x_lo + step / 2
        while x < x_hi:
            y = 6.0
            while y < D.BOARD_H - 6.0:
                p = Point(x, y)
                if (both.contains(p.buffer(0.6, 12))
                        and not obstacles.intersects(p.buffer(0.55))
                        and not rt.no_via[R.mm2c(y), R.mm2c(x)]):
                    stitch.append(R.Via(x, y, R.VIA_PAD, R.VIA_DRILL, net))
                y += step
            x += step
    rt.vias.extend(stitch)
    if verbose:
        print(f"  {len(stitch)} plane stitching vias")

    if verbose:
        print("  ... repairing broken nets", flush=True)

    # CHECKPOINT.  The routing phase takes about twelve minutes and this environment kills
    # long-running builds somewhere past that, which lost six consecutive runs -- every one
    # of them AFTER the routing had succeeded and during the repair.  Dumping here means a
    # kill costs the repair, which is minutes, instead of the route, which is not.
    # resume_from_checkpoint() in this module picks it up.
    try:
        import pickle as _pk
        with open("route_checkpoint.pkl", "wb") as _f:
            _pk.dump({"tracks": rt.tracks, "vias": rt.vias, "failed": rt.failed,
                      "narrowed": rt.narrowed, "iso_box": rt.iso_box,
                      "netid": rt.netid, "pours": pour_geo}, _f)
        if verbose:
            print(f"  checkpoint written: {len(rt.tracks)} segments, {len(rt.vias)} vias",
                  flush=True)
    except Exception as _e:                      # a checkpoint failure must not kill a build
        if verbose:
            print(f"  checkpoint failed ({_e}); continuing", flush=True)

    # -------------------------------------------------- repair broken nets
    import netcheck
    for attempt in range(8):
        conn = netcheck.check(board, rt.tracks, rt.vias, pour_geo)
        broken = {n: v for n, v in conn.items() if not v[0]}
        if not broken:
            break
        if verbose:
            print(f"repair pass {attempt + 1}: {len(broken)} broken nets")
        fixed = 0
        padmap = {f"{p.ref}.{p.num}": p for p in board.pads()}
        for net, (_, _, stray) in broken.items():
            cls = D.netclass_of(net)
            w, c = D.NETCLASS[cls]
            targets = [p for p in board.nets()[net]
                       if f"pad {p.ref}.{p.num}" not in stray]
            for tag in stray:
                src = padmap.get(tag[4:])
                if src is None or not targets:
                    continue
                targets.sort(key=lambda p: (p.x - src.x) ** 2 + (p.y - src.y) ** 2)
                done = False
                for tgt in targets[:8]:
                    if rt.try_ladder(net, src, tgt, w, c, False):
                        done = True
                        break
                if not done:
                    # Escalate.  The ladder only tries to squeeze through what is already
                    # there; rip-up tears out the nets blocking the corridor, routes
                    # through it, and puts them back.  Duplicate copper used to make this
                    # unsafe, which is why it was not used here -- the de-duplication now
                    # runs after everything, so it is safe.
                    for tgt in targets[:4]:
                        # max_nets 4, not 8: measured at about 4 s against up to a minute,
                        # for the same success rate.  Tearing out eight nets to place one is
                        # a trade this board almost never wins.
                        if rt.ripup_retry(net, src, tgt, w, c, max_nets=4):
                            done = True
                            break
                if done:
                    fixed += 1
                elif net in ("DGND", "AGND_REF"):
                    _place_ground_via(rt, src, dists=(1.15, 1.4, 1.7, 2.0, 2.4,
                                                      2.8, 3.2, 3.8))
        if verbose:
            print(f"   {fixed} repaired")
        if not fixed:
            break

        for layer in PLANE_LAYERS:
            for net, x_lo, x_hi in POUR_NETS:
                pour_geo[(layer, net)] = pours.build(
                    board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                    clearance=0.35, iso_box=rt.iso_box)

    if verbose:
        print("  ... removing duplicate copper", flush=True)
    _dedupe(rt, verbose)
    for layer in PLANE_LAYERS:
        for net, x_lo, x_hi in POUR_NETS:
            pour_geo[(layer, net)] = pours.build(
                board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                clearance=0.35, iso_box=rt.iso_box)

    if verbose:
        print("  ... pushing vias clear", flush=True)
    # -------------------------------------------------- push vias clear
    import viafix
    for _ in range(3):
        moved, _d, stuck = viafix.push(board, rt.tracks, rt.vias, pour_geo, verbose=verbose)
        if not moved:
            break
    if stuck:
        # a via that cannot be moved has its connection re-routed on the top layer only
        if verbose:
            print(f"  {len(stuck)} vias could not be pushed clear; deleting and re-routing")
        drop = set(stuck)
        killed_nets = {rt.vias[i].net for i in drop}
        rt.vias = [v for i, v in enumerate(rt.vias) if i not in drop]
        rt.rebuild()
        for net in sorted(killed_nets):
            pads = board.nets()[net]
            cls = D.netclass_of(net)
            w, c = D.NETCLASS[cls]
            for a, bi in rt._mst([(p.x, p.y) for p in pads]):
                rt.try_ladder(net, pads[a], pads[bi], w, c, False)
        for layer in PLANE_LAYERS:
            for net, x_lo, x_hi in POUR_NETS:
                pour_geo[(layer, net)] = pours.build(
                    board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                    clearance=0.35, iso_box=rt.iso_box)
        viafix.push(board, rt.tracks, rt.vias, pour_geo, verbose=verbose)

    # Deduplicate again.  The first pass runs before viafix, and viafix moves vias and
    # re-routes the connections of any it cannot move, which puts fresh duplicates back.
    # Twenty-eight duplicate segments and four doubly-drilled via positions reached the
    # released data that way, and a fabricator's CAM review flags a doubly-drilled hole.
    _dedupe(rt, verbose)

    # final pour after everything has settled
    for layer in PLANE_LAYERS:
        for net, x_lo, x_hi in POUR_NETS:
            pour_geo[(layer, net)] = pours.build(
                board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                clearance=0.35, iso_box=rt.iso_box)

    # -------------------------------------------------- late repair
    # The main repair loop runs BEFORE viafix and the de-duplication, so the
    # geometry it repaired is not the geometry that ships: viafix moves vias
    # and re-routes what it cannot move.  Anything still broken gets one more
    # bounded try_ladder pass on the final landscape (no rip-up here -- at
    # this stage it almost never wins and can only trade working copper away),
    # then vias are pushed clear and the pours rebuilt so the DRC sees exactly
    # what was committed.
    for _late in range(3):
        conn = netcheck.check(board, rt.tracks, rt.vias, pour_geo)
        broken = {n: v for n, v in conn.items() if not v[0]}
        if not broken:
            break
        if verbose:
            print(f"late repair pass {_late + 1}: {len(broken)} broken nets")
        fixed = 0
        padmap = {f"{p.ref}.{p.num}": p for p in board.pads()}
        for net, (_, _, stray) in broken.items():
            cls = D.netclass_of(net)
            w, c = D.NETCLASS[cls]
            targets = [p for p in board.nets()[net]
                       if f"pad {p.ref}.{p.num}" not in stray]
            for tag in stray:
                src = padmap.get(tag[4:])
                if src is None:
                    continue
                done = False
                if targets:
                    targets.sort(key=lambda p: (p.x - src.x) ** 2
                                 + (p.y - src.y) ** 2)
                    for tgt in targets[:8]:
                        if rt.try_ladder(net, src, tgt, w, c, False):
                            done = True
                            break
                if not done and net in ("DGND", "AGND_REF") and not src.tht:
                    # a reference pad's connection is the plane, not another
                    # pad: viafix may have deleted its plane via, so put one
                    # back rather than chase a surface route that cannot fit
                    done = _place_ground_via(rt, src,
                                             dists=(1.15, 1.4, 1.7, 2.0, 2.4,
                                                    2.8, 3.2, 3.8))
                if done:
                    fixed += 1
        if verbose:
            print(f"   {fixed} repaired late")
        if not fixed:
            break
        for layer in PLANE_LAYERS:
            for net, x_lo, x_hi in POUR_NETS:
                pour_geo[(layer, net)] = pours.build(
                    board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                    clearance=0.35, iso_box=rt.iso_box)
        viafix.push(board, rt.tracks, rt.vias, pour_geo, verbose=verbose)
        _dedupe(rt, verbose)
        for layer in PLANE_LAYERS:
            for net, x_lo, x_hi in POUR_NETS:
                pour_geo[(layer, net)] = pours.build(
                    board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                    clearance=0.35, iso_box=rt.iso_box)

    # -------------------------------------------------- targeted repairs
    # Declared in design.TARGETED_REPAIRS, carried out by tools/surgery.py on
    # the settled route, only where the named connection is still open.  The
    # router is not iterated further (programme instruction, 2026-09-02).
    # Then the same tail as the late repair: pours, via push, de-dup, pours.
    surgery_notes = []
    if getattr(D, "TARGETED_REPAIRS", None):
        import surgery
        if verbose:
            print("  ... targeted repairs", flush=True)
        surgery_notes = surgery.apply(rt, board, pour_geo, verbose=verbose)
        for layer in PLANE_LAYERS:
            for net, x_lo, x_hi in POUR_NETS:
                pour_geo[(layer, net)] = pours.build(
                    board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                    clearance=0.35, iso_box=rt.iso_box)
        viafix.push(board, rt.tracks, rt.vias, pour_geo, verbose=verbose)
        _dedupe(rt, verbose)
        for layer in PLANE_LAYERS:
            for net, x_lo, x_hi in POUR_NETS:
                pour_geo[(layer, net)] = pours.build(
                    board, rt.tracks, rt.vias, layer, net, x_lo, x_hi,
                    clearance=0.35, iso_box=rt.iso_box)

    result = dict(board=board, tracks=rt.tracks, vias=rt.vias, pours=pour_geo,
                  failed=rt.failed, narrowed=rt.narrowed, iso_box=rt.iso_box,
                  netid=rt.netid, elapsed=time.time() - t0,
                  surgery=surgery_notes)

    # ---------------------------------------------------------------- connectivity
    result["connectivity"] = netcheck.check(board, rt.tracks, rt.vias, pour_geo)
    good, bad = netcheck.report(result["connectivity"], verbose)
    if verbose:
        print(f"connectivity: {good} nets fully connected, {bad} broken")
        if rt.failed:
            print("unrouted connections:")
            for net, a, b in rt.failed:
                print(f"   {net:14s} {a} -> {b}")

    if plot:
        plot_board(result, plot)
    return result


# ---------------------------------------------------------------- connectivity check
def check_connectivity(board, tracks, vias, pour_geo, grid=0.1):
    """Rasterise every net's copper on both layers and count connected components."""
    from scipy import ndimage
    nx = int(D.BOARD_W / grid) + 1
    ny = int(D.BOARD_H / grid) + 1
    yy, xx = np.mgrid[0:ny, 0:nx]
    xs = xx * grid
    ys = yy * grid
    out = {}
    nets = board.nets()
    for net, pads in nets.items():
        if len(pads) < 2:
            continue
        m = np.zeros((2, ny, nx), bool)
        for pd in pads:
            w, h = pd.size_rot()
            for L, name in enumerate(("F.Cu", "B.Cu")):
                if not pd.tht and not pd.on(name):
                    continue
                if pd.shape == "circle":
                    m[L] |= ((xs - pd.x) ** 2 + (ys - pd.y) ** 2) <= (w / 2) ** 2
                else:
                    m[L] |= ((np.abs(xs - pd.x) <= w / 2) & (np.abs(ys - pd.y) <= h / 2))
        for t in tracks:
            if t.net != net:
                continue
            L = 0 if t.layer == "F.Cu" else 1
            m[L] |= _seg_mask(xs, ys, t.x1, t.y1, t.x2, t.y2, t.width / 2)
        for v in vias:
            if v.net != net:
                continue
            d = (xs - v.x) ** 2 + (ys - v.y) ** 2 <= (v.pad / 2) ** 2
            m[0] |= d
            m[1] |= d
        for (layer, pnet), g in pour_geo.items():
            if pnet != net or g.is_empty:
                continue
            L = 0 if layer == "F.Cu" else 1
            m[L] |= _poly_mask(g, xs, ys)
        lab, n = ndimage.label(m, structure=np.array(
            [[[0, 0, 0], [0, 1, 0], [0, 0, 0]],
             [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
             [[0, 0, 0], [0, 1, 0], [0, 0, 0]]]))
        seen = set()
        for pd in pads:
            L = 0 if (pd.on("F.Cu") or pd.tht) else 1
            v = lab[L, int(round(pd.y / grid)), int(round(pd.x / grid))]
            if v == 0 and pd.tht:
                v = lab[1, int(round(pd.y / grid)), int(round(pd.x / grid))]
            seen.add(int(v))
        out[net] = (len(seen - {0}) == 1 and 0 not in seen)
    return out


def _seg_mask(xs, ys, x1, y1, x2, y2, r):
    dx, dy = x2 - x1, y2 - y1
    L2 = dx * dx + dy * dy
    if L2 < 1e-12:
        return (xs - x1) ** 2 + (ys - y1) ** 2 <= r * r
    t = np.clip(((xs - x1) * dx + (ys - y1) * dy) / L2, 0, 1)
    px, py = x1 + t * dx, y1 + t * dy
    return (xs - px) ** 2 + (ys - py) ** 2 <= r * r


def _poly_mask(geom, xs, ys):
    from matplotlib.path import Path
    m = np.zeros(xs.shape, bool)
    pts = np.column_stack([xs.ravel(), ys.ravel()])
    for poly in pours.polys(geom):
        ext = Path(np.asarray(poly.exterior.coords))
        inside = ext.contains_points(pts).reshape(xs.shape)
        for ring in poly.interiors:
            hole = Path(np.asarray(ring.coords))
            inside &= ~hole.contains_points(pts).reshape(xs.shape)
        m |= inside
    return m


# ---------------------------------------------------------------- picture
def plot_board(res, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle, Polygon as MplPoly

    board = res["board"]
    fig, ax = plt.subplots(figsize=(14, 13.4))
    ax.set_facecolor("#0b1a12")
    ax.add_patch(Rectangle((0, 0), board.width, board.height,
                           fc="#123a26", ec="#8fbf9f", lw=1.6))
    for (layer, net), g in res["pours"].items():
        col = "#1d6b43" if layer == "B.Cu" else "#2c8f5c"
        for poly in pours.polys(g):
            ax.add_patch(MplPoly(np.asarray(poly.exterior.coords), closed=True,
                                 fc=col, ec="none", alpha=0.55 if layer == "B.Cu" else 0.35))
            for ring in poly.interiors:
                ax.add_patch(MplPoly(np.asarray(ring.coords), closed=True,
                                     fc="#123a26", ec="none"))
    for t in res["tracks"]:
        col = "#e8b84b" if t.layer == "F.Cu" else "#5aa9e6"
        ax.plot([t.x1, t.x2], [t.y1, t.y2], c=col, lw=t.width * 3.2,
                solid_capstyle="round", alpha=0.95, zorder=3)
    for v in res["vias"]:
        ax.add_patch(Circle((v.x, v.y), v.pad / 2, fc="#cfd8dc", ec="none", zorder=4))
        ax.add_patch(Circle((v.x, v.y), v.drill / 2, fc="#0b1a12", ec="none", zorder=5))
    for pd in board.pads():
        w, h = pd.size_rot()
        col = "#f2e2b0" if pd.tht else "#d9c07a"
        if pd.shape == "circle" or pd.kind == "np_thru_hole":
            ax.add_patch(Circle((pd.x, pd.y), w / 2, fc=col, ec="none", zorder=6))
        else:
            ax.add_patch(Rectangle((pd.x - w / 2, pd.y - h / 2), w, h,
                                   fc=col, ec="none", zorder=6))
        if pd.drill:
            ax.add_patch(Circle((pd.x, pd.y), pd.drill / 2, fc="#0b1a12",
                                ec="none", zorder=7))
    ax.plot([D.ZONE_SPLIT_X, D.ZONE_SPLIT_X], [0, board.height], "--",
            c="#ff8a80", lw=0.8, zorder=8)
    for p in board.parts:
        b = board.courtyard_box(p)
        ax.text((b[0] + b[2]) / 2, (b[1] + b[3]) / 2, p.ref, ha="center", va="center",
                fontsize=3.6, color="#e6f0ea", zorder=9)
    ax.set_xlim(-3, board.width + 3)
    ax.set_ylim(board.height + 3, -3)
    ax.set_aspect("equal")
    ax.set_title(f"EEG-CAR-01 Rev {D.REV} -- routed, both layers "
                 f"(top gold, bottom blue, pours green)", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=180, facecolor="#0b1a12")
    plt.close(fig)


if __name__ == "__main__":
    res = build(plot=("routed.png" if "--plot" in sys.argv else None))
    with open("routed.pkl", "wb") as f:
        pickle.dump({k: v for k, v in res.items() if k != "board"}, f)
    print("elapsed %.0f s" % res["elapsed"])
