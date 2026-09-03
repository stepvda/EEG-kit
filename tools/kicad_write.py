#!/usr/bin/env python3
"""
kicad_write.py -- write the routed EEG-CAR-01 Rev B as a .kicad_pcb.

The file is emitted in the KiCad 5 s-expression dialect (version 20171130), the same
dialect the Rev A file used, because KiCad 6, 7, 8 and 9 all import it without loss and
several of the manufacturers who answered the RFQ are on older tools.  Tracks, vias and
both filled reference pours are included, so the board opens routed.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import design as D
import fplib
import pours

LAYER_ID = {"F.Cu": 0, "In1.Cu": 1, "In2.Cu": 2, "B.Cu": 31, "B.Paste": 34, "F.Paste": 35, "B.SilkS": 36,
            "F.SilkS": 37, "B.Mask": 38, "F.Mask": 39, "Dwgs.User": 40,
            "Edge.Cuts": 44, "F.CrtYd": 46, "B.CrtYd": 47, "F.Fab": 48, "B.Fab": 49}


def write(path, board, tracks, vias, pour_geo, unrouted=0):
    nets = sorted(board.nets())
    netid = {n: i + 1 for i, n in enumerate(nets)}
    o = []
    o.append('(kicad_pcb (version 20171130) (host eeg-car-01-generator "package_v2.4/tools")')
    o.append("  (general (thickness 1.6))")
    o.append("  (page A3)")
    o.append(f'  (title_block (title "EEG-CAR-01 carrier board") (date {D.DATE}) '
             f'(rev {D.REV}) (company "TI One Voice research programme")')
    o.append('    (comment 1 "ROUTED. Generated from package_v2.4/tools/design.py; '
             'DRC report in kicad/EEG-CAR-01_RevB_DRC_report.txt")')
    o.append('    (comment 2 "4 layers (L1 signal, L2 and L3 reference planes, L4 '
             'signal), 1.60 mm FR-4, ENIG, min track 0.20 mm / clearance 0.20 mm, '
             'through vias 0.60/0.30 mm")')
    o.append(f'    (comment 3 "Analogue zone x < {D.ZONE_SPLIT_X:.0f} mm; digital zone beyond; '
             'AGND_REF joins DGND at R90 only")')
    o.append('    (comment 4 "Licence CC BY-SA 4.0"))')
    o.append("  (layers (0 F.Cu signal) (1 In1.Cu power) (2 In2.Cu power) "
             "(31 B.Cu signal) (34 B.Paste user) "
             "(35 F.Paste user) (36 B.SilkS user) (37 F.SilkS user)")
    o.append("    (38 B.Mask user) (39 F.Mask user) (40 Dwgs.User user) "
             "(44 Edge.Cuts user) (46 F.CrtYd user) (47 B.CrtYd user) "
             "(48 F.Fab user) (49 B.Fab user))")
    o.append("  (setup (last_trace_width 0.25) (trace_clearance 0.2) (zone_clearance 0.35) "
             "(zone_45_only no) (trace_min 0.2)")
    o.append("    (via_size 0.6) (via_drill 0.3) (via_min_size 0.6) (via_min_drill 0.3) "
             "(edge_width 0.1) (grid_origin 0 0))")
    o.append('  (net 0 "")')
    for n in nets:
        o.append(f'  (net {netid[n]} "{n}")')
    o.append('  (net_class Default "carrier default"')
    o.append("    (clearance 0.2) (trace_width 0.25) (via_dia 0.6) (via_drill 0.3)")
    for n in nets:
        o.append(f'    (add_net "{n}")')
    o.append("  )")

    # board outline
    W, H = D.BOARD_W, D.BOARD_H
    for a, b in [((0, 0), (W, 0)), ((W, 0), (W, H)), ((W, H), (0, H)), ((0, H), (0, 0))]:
        o.append(f"  (gr_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) "
                 f"(layer Edge.Cuts) (width 0.1))")
    o.append(f"  (gr_line (start {D.ZONE_SPLIT_X} 0) (end {D.ZONE_SPLIT_X} {H}) "
             f"(layer Dwgs.User) (width 0.15))")
    o.append(f'  (gr_text "ANALOGUE ZONE" (at 30 3) (layer Dwgs.User) '
             f'(effects (font (size 2 2) (thickness 0.3))))')
    o.append(f'  (gr_text "DIGITAL ZONE" (at 90 3) (layer Dwgs.User) '
             f'(effects (font (size 2 2) (thickness 0.3))))')
    o.append('  (gr_text "ISOLATION KEEP-OUT - NO COPPER" (at 145 12 90) '
             '(layer Dwgs.User) (effects (font (size 1.4 1.4) (thickness 0.25))))')

    # footprints
    for p in board.parts:
        fp = fplib.get(p.fpname)
        o.append(f'  (module {p.fpname} (layer F.Cu) (at {p.x} {p.y} {p.rot})')
        o.append(f'    (descr "{fp.descr}")')
        o.append(f'    (fp_text reference {p.ref} (at 0 -2.4) (layer F.SilkS)')
        o.append("      (effects (font (size 1 1) (thickness 0.15))))")
        val = p.value.replace('"', "'")
        o.append(f'    (fp_text value "{val}" (at 0 2.4) (layer F.Fab)')
        o.append("      (effects (font (size 1 1) (thickness 0.15))))")
        for seg, lay in ((fp.silk, "F.SilkS"), (fp.fab, "F.Fab"), (fp.crtyd, "F.CrtYd")):
            for x1, y1, x2, y2, w in seg:
                o.append(f"    (fp_line (start {x1} {y1}) (end {x2} {y2}) "
                         f"(layer {lay}) (width {w}))")
        for pd in p.pads:
            lx = pd.x - p.x
            ly = pd.y - p.y
            if p.rot:
                import math
                a = -math.radians(p.rot)
                lx, ly = lx * math.cos(a) - ly * math.sin(a), lx * math.sin(a) + ly * math.cos(a)
            layers = " ".join(l for l in pd.layers if l)
            if not layers:
                layers = "*.Cu"
            drill = f" (drill {pd.drill})" if pd.drill else ""
            net = ""
            if pd.net:
                net = f' (net {netid[pd.net]} "{pd.net}")'
            shape = {"roundrect": "roundrect", "rect": "rect", "oval": "oval",
                     "circle": "circle"}.get(pd.shape, "rect")
            rr = " (roundrect_rratio 0.25)" if shape == "roundrect" else ""
            num = pd.num if pd.num else '""'
            o.append(f'    (pad {num} {pd.kind} {shape} (at {lx:.4f} {ly:.4f}) '
                     f"(size {pd.w} {pd.h}){drill} (layers {layers}){rr}{net})")
        o.append("  )")

    # tracks and vias
    for t in tracks:
        o.append(f"  (segment (start {t.x1:.4f} {t.y1:.4f}) (end {t.x2:.4f} {t.y2:.4f}) "
                 f"(width {t.width}) (layer {t.layer}) (net {netid[t.net]}))")
    for v in vias:
        o.append(f"  (via (at {v.x:.4f} {v.y:.4f}) (size {v.pad}) (drill {v.drill}) "
                 f"(layers F.Cu B.Cu) (net {netid[v.net]}))")

    # zones
    for (layer, net), g in sorted(pour_geo.items()):
        polys = pours.polys(g)
        if not polys:
            continue
        x_lo = 0.0 if net == "AGND_REF" else D.ZONE_SPLIT_X
        x_hi = D.ZONE_SPLIT_X if net == "AGND_REF" else D.BOARD_W
        o.append(f'  (zone (net {netid[net]}) (net_name "{net}") (layer {layer}) '
                 f"(hatch edge 0.508)")
        o.append("    (connect_pads (clearance 0.35))")
        o.append("    (min_thickness 0.2)")
        o.append("    (fill yes (arc_segments 32) (thermal_gap 0.4) "
                 "(thermal_bridge_width 0.6))")
        o.append("    (polygon (pts " + " ".join(
            f"(xy {x:.3f} {y:.3f})" for x, y in
            [(x_lo + 0.4, 0.4), (x_hi - 0.4, 0.4), (x_hi - 0.4, D.BOARD_H - 0.4),
             (x_lo + 0.4, D.BOARD_H - 0.4)]) + "))")
        # NO (filled_polygon) IS WRITTEN, DELIBERATELY.
        #
        # In the KiCad format a filled_polygon is a CACHE of the last fill, and each one is
        # a simple ring that cannot express a hole.  These planes have 226 and 407 voids
        # apiece -- every antipad, thermal relief and mounting-hole keep-out -- so writing
        # the exterior ring alone produced a SOLID RECTANGLE, which is what an earlier
        # revision of this writer shipped.  A reader opening the board then saw planes with
        # no antipads at all, covering the M3 mounting holes, and had no way to tell that
        # the Gerbers (which use LPD/LPC polarity and are correct) disagreed.
        #
        # A wrong cache is worse than no cache: KiCad rebuilds it from the outline and the
        # clearance rules the moment the zones are filled, so leaving it out costs a
        # keypress and removes the chance of believing something false.  The authority for
        # copper is kicad/gerber/, and the keep-outs below are written explicitly so that
        # KiCad's own fill honours them.
        o.append("  )")
    # ---- mounting-hole keep-outs, all four layers
    # design.py voids these in the pours it computes, and the Gerbers carry the voids, but
    # KiCad refilling from the outline would only clear the zone clearance (0.35 mm) around
    # an NPTH pad, not the 6.0 mm this design requires.  Stating them as keepout zones makes
    # the board file agree with the Gerbers whoever refills it.
    for mx, my in D.MOUNTING_HOLES:
        r = D.MOUNTING_KEEPOUT_D / 2.0
        pts = []
        for k in range(24):
            import math
            a_ = 2 * math.pi * k / 24
            pts.append((mx + r * math.cos(a_), my + r * math.sin(a_)))
        o.append('  (zone (net 0) (net_name "") '
                 "(layers F.Cu In1.Cu In2.Cu B.Cu) (hatch edge 0.508)")
        o.append("    (connect_pads (clearance 0))")
        o.append("    (min_thickness 0.2)")
        o.append("    (keepout (tracks not_allowed) (vias not_allowed) "
                 "(copperpour not_allowed))")
        o.append("    (polygon (pts " + " ".join(
            f"(xy {x:.3f} {y:.3f})" for x, y in pts) + "))")
        o.append("  )")

    o.append(")")
    with open(path, "w") as f:
        f.write("\n".join(o) + "\n")
    return path
