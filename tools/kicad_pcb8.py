#!/usr/bin/env python3
"""
kicad_pcb8.py -- write the UNROUTED EEG-CAR-01 Rev C as a KiCad 8 board and project.

`tools/kicad_write.py` writes the Rev B routed board in the KiCad 5 dialect (version
20171130), which KiCad 6 to 9 all import.  That was the right choice for a fabrication
set going to houses on older tools.  It is the wrong choice here: the contractor is being
asked to work IN KiCad, under a rule set that uses net classes, rule areas and custom
rules, and none of those survive a KiCad 5 file.  So this is a separate writer at
`(kicad_pcb (version 20240108))`, and Rev B's writer is untouched.

What it writes:

  * the board outline on Edge.Cuts and the four-layer stack-up in `(setup)`;
  * every one of the 211 footprints with its pads and its nets, and **no tracks and no
    vias** -- Rev C is unrouted and the routing is bought;
  * the thirty connectors J1 to J30 **locked**, because the pod, the plate and the
    harness fix them, and everything else unlocked;
  * AGND_REF and DGND zones on In1.Cu and In2.Cu, split at x = 62 mm;
  * rule areas by the names `tools/rules.py` writes into the `.kicad_dru`:
    ISOLATION_KEEPOUT, ANALOGUE_ZONE, DIGITAL_ZONE, NO_VIA_J2/J4/J23/J29 and the four
    mounting keep-outs;
  * a `.kicad_pro` carrying the net classes, the assignments and the severities that
    turn the two KiCad BUILT-IN checks of finding 2 -- dangling ends and redundant
    copper -- into errors.

Coordinates are `design.py`'s: top-left origin, Y down, which is also KiCad's.  Nothing
is flipped here; `tools/gerber.py` is the one place that flips, and only for CAM.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import json
import math
import os
import sys
import uuid as _uuid

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import fplib                # noqa: E402
import rules                # noqa: E402
from kicad_sch import NS, uid, esc, n   # noqa: E402

LAYERS = [(0, "F.Cu", "signal"), (1, "In1.Cu", "power"), (2, "In2.Cu", "power"),
          (31, "B.Cu", "signal"), (32, "B.Adhes", "user"), (33, "F.Adhes", "user"),
          (34, "B.Paste", "user"), (35, "F.Paste", "user"),
          (36, "B.SilkS", "user", "B.Silkscreen"), (37, "F.SilkS", "user", "F.Silkscreen"),
          (38, "B.Mask", "user"), (39, "F.Mask", "user"),
          (40, "Dwgs.User", "user", "User.Drawings"),
          (41, "Cmts.User", "user", "User.Comments"),
          (44, "Edge.Cuts", "user"), (45, "Margin", "user"),
          (46, "B.CrtYd", "user", "B.Courtyard"), (47, "F.CrtYd", "user", "F.Courtyard"),
          (48, "B.Fab", "user"), (49, "F.Fab", "user")]

# ECO-EEG-030: the thirty connectors are fixed by the pod, the module plate and the
# harness, so the contractor may not move them.  Everything else is theirs to place.
LOCKED = {ref for ref in D.C if ref.startswith("J")} | {
    f"MH{i}" for i in range(1, 5)} | {f"FID{i}" for i in range(1, 4)}


def _u(*k):
    return str(_uuid.uuid5(NS, "pcb|" + "|".join(str(x) for x in k)))


def _stackup():
    """DSN-EEG-003 section 3.2, transcribed once."""
    L = ["    (stackup",
         '      (layer "F.SilkS" (type "Top Silk Screen"))',
         '      (layer "F.Paste" (type "Top Solder Paste"))',
         '      (layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))',
         '      (layer "F.Cu" (type "copper") (thickness 0.035))',
         '      (layer "dielectric 1" (type "prepreg") (thickness 0.2) '
         '(material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))',
         '      (layer "In1.Cu" (type "copper") (thickness 0.017))',
         '      (layer "dielectric 2" (type "core") (thickness 1.065) '
         '(material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))',
         '      (layer "In2.Cu" (type "copper") (thickness 0.017))',
         '      (layer "dielectric 3" (type "prepreg") (thickness 0.2) '
         '(material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))',
         '      (layer "B.Cu" (type "copper") (thickness 0.035))',
         '      (layer "B.Mask" (type "Top Solder Mask") (thickness 0.01))',
         '      (layer "B.Paste" (type "Bottom Solder Paste"))',
         '      (layer "B.SilkS" (type "Bottom Silk Screen"))',
         '      (copper_finish "ENIG")',
         "      (dielectric_constraints no)",
         "    )"]
    return L


def _pad_sexp(pd, part, netid, indent="    "):
    lx, ly = pd.x - part.x, pd.y - part.y
    if part.rot:
        a = -math.radians(part.rot)
        lx, ly = lx * math.cos(a) - ly * math.sin(a), lx * math.sin(a) + ly * math.cos(a)
    layers = " ".join(f'"{ly_}"' for ly_ in pd.layers if ly_) or '"*.Cu"'
    shape = {"roundrect": "roundrect", "rect": "rect", "oval": "oval",
             "circle": "circle"}.get(pd.shape, "rect")
    num = pd.num if pd.num else ""
    out = [f'{indent}(pad "{esc(num)}" {pd.kind} {shape} '
           f"(at {n(lx)} {n(ly)}) (size {n(pd.w)} {n(pd.h)})"]
    if pd.drill:
        out.append(f"{indent}  (drill {n(pd.drill)})")
    out.append(f"{indent}  (layers {layers})")
    if shape == "roundrect":
        out.append(f"{indent}  (roundrect_rratio 0.25)")
    if pd.net:
        out.append(f'{indent}  (net {netid[pd.net]} "{esc(pd.net)}")')
    out.append(f'{indent}  (uuid "{_u("pad", pd.ref, pd.num, lx, ly)}")')
    out.append(f"{indent})")
    return out


def _rule_area(name, layers, pts, tracks="not_allowed", vias="not_allowed",
               pours="not_allowed", note=""):
    lay = " ".join(f'"{ly}"' for ly in layers)
    p = " ".join(f"(xy {n(x)} {n(y)})" for x, y in pts)
    return ["  (zone (net 0) (net_name \"\") (layers " + lay + ")",
            f'    (uuid "{_u("area", name)}")',
            f'    (name "{esc(name)}")',
            "    (hatch edge 0.5)",
            "    (connect_pads (clearance 0))",
            "    (min_thickness 0.2)",
            "    (filled_areas_thickness no)",
            f"    (keepout (tracks {tracks}) (vias {vias}) (pads not_allowed) "
            f"(copperpour {pours}) (footprints not_allowed))",
            "    (placement (enabled no) (sheetname \"\"))",
            f"    (polygon (pts {p}))",
            "  )"]


def write_pcb(path, board, revision=None):
    rev = revision or D.REV_C
    nets = sorted(board.nets())
    netid = {name: i + 1 for i, name in enumerate(nets)}
    W, H = D.BOARD_W, D.BOARD_H
    o = ["(kicad_pcb",
         "  (version 20240108)",
         '  (generator "eeg-car-01-generator")',
         '  (generator_version "8.0")',
         "  (general",
         "    (thickness 1.6)",
         "    (legacy_teardrops no)",
         "  )",
         '  (paper "A3")',
         "  (title_block",
         f'    (title "EEG-CAR-01 carrier board -- Rev {rev}, UNROUTED")',
         f'    (date "{D.DATE_C}")',
         f'    (rev "{rev}")',
         '    (company "TI One Voice research programme")',
         '    (comment 1 "UNROUTED. Placement and routing are bought; this file is the '
         'input set (ECO-EEG-030).")',
         '    (comment 2 "J1-J30, MH1-MH4 and FID1-FID3 are LOCKED and may not be '
         'moved. Everything else is unlocked.")',
         '    (comment 3 "Rules: kicad/EEG-CAR-01_RevC.kicad_dru and LAY-EEG-034. '
         'Angle and pad-entry are checked on return, not by KiCad.")',
         '    (comment 4 "Generated from tools/design.py. Not edited by hand. '
         'Licence CC BY-SA 4.0.")',
         "  )",
         "  (layers"]
    for row in LAYERS:
        num, name, typ = row[0], row[1], row[2]
        user = f' "{row[3]}"' if len(row) > 3 else ""
        o.append(f'    ({num} "{name}" {typ}{user})')
    o.append("  )")
    o.append("  (setup")
    o += _stackup()
    o.append("    (pad_to_mask_clearance 0)")
    o.append("    (allow_soldermask_bridges_in_footprints no)")
    o.append("    (grid_origin 0 0)")
    o.append("  )")

    o.append('  (net 0 "")')
    for name in nets:
        o.append(f'  (net {netid[name]} "{esc(name)}")')

    # ---- outline, zone split and the legend of what is fixed -----------------
    for a, b in (((0, 0), (W, 0)), ((W, 0), (W, H)), ((W, H), (0, H)), ((0, H), (0, 0))):
        o.append(f"  (gr_line (start {n(a[0])} {n(a[1])}) (end {n(b[0])} {n(b[1])})")
        o.append('    (stroke (width 0.1) (type solid)) (layer "Edge.Cuts")')
        o.append(f'    (uuid "{_u("edge", a, b)}"))')
    o.append(f"  (gr_line (start {n(D.ZONE_SPLIT_X)} 0) "
             f"(end {n(D.ZONE_SPLIT_X)} {n(H)})")
    o.append('    (stroke (width 0.15) (type dash)) (layer "Dwgs.User")')
    o.append(f'    (uuid "{_u("split")}"))')
    for txt, x, y, size in (("ANALOGUE ZONE", 20, 4, 2.0),
                            ("DIGITAL ZONE", 90, 4, 2.0),
                            ("EEG-CAR-01 Rev " + rev + " -- UNROUTED", 20, 127, 2.0),
                            ("J1-J30 LOCKED", 90, 127, 2.0)):
        o.append(f'  (gr_text "{esc(txt)}" (at {n(x)} {n(y)}) (layer "Dwgs.User")')
        o.append(f'    (uuid "{_u("txt", txt)}")')
        o.append(f"    (effects (font (size {n(size)} {n(size)}) (thickness 0.3))))")

    # ---- footprints ---------------------------------------------------------
    for part in board.parts:
        fp = fplib.get(part.fpname)
        lock = " (locked yes)" if part.ref in LOCKED else ""
        o.append(f'  (footprint "EEG-CAR-01:{esc(part.fpname)}"{lock}')
        o.append(f'    (layer "F.Cu")')
        o.append(f'    (uuid "{_u("fp", part.ref)}")')
        o.append(f"    (at {n(part.x)} {n(part.y)} {n(part.rot)})")
        o.append(f'    (descr "{esc(fp.descr)}")')
        o.append('    (attr through_hole)' if part.is_tht else '    (attr smd)')
        o.append(f'    (property "Reference" "{esc(part.ref)}" (at 0 -2.4 0) '
                 f'(layer "F.SilkS")')
        o.append(f'      (uuid "{_u("ref", part.ref)}")')
        o.append("      (effects (font (size 1 1) (thickness 0.15))))")
        o.append(f'    (property "Value" "{esc(part.value)}" (at 0 2.4 0) '
                 f'(layer "F.Fab")')
        o.append(f'      (uuid "{_u("val", part.ref)}")')
        o.append("      (effects (font (size 1 1) (thickness 0.15))))")
        if part.mpn:
            o.append(f'    (property "MPN" "{esc(part.mpn)}" (at 0 0 0) '
                     f'(layer "F.Fab") (hide yes)')
            o.append(f'      (uuid "{_u("mpn", part.ref)}")')
            o.append("      (effects (font (size 1 1) (thickness 0.15))))")
        for segs, lay in ((fp.silk, "F.SilkS"), (fp.fab, "F.Fab"), (fp.crtyd, "F.CrtYd")):
            for k, (x1, y1, x2, y2, w) in enumerate(segs):
                o.append(f"    (fp_line (start {n(x1)} {n(y1)}) (end {n(x2)} {n(y2)})")
                o.append(f'      (stroke (width {n(w)}) (type solid)) (layer "{lay}")')
                o.append(f'      (uuid "{_u("fpl", part.ref, lay, k)}"))')
        for pd in part.pads:
            o += _pad_sexp(pd, part, netid)
        o.append("  )")

    # ---- reference planes ---------------------------------------------------
    for layer in ("In1.Cu", "In2.Cu"):
        for net, x_lo, x_hi in (("AGND_REF", 0.0, D.ZONE_SPLIT_X),
                                ("DGND", D.ZONE_SPLIT_X, D.BOARD_W)):
            pts = [(x_lo + 0.4, 0.4), (x_hi - 0.4, 0.4),
                   (x_hi - 0.4, H - 0.4), (x_lo + 0.4, H - 0.4)]
            p = " ".join(f"(xy {n(x)} {n(y)})" for x, y in pts)
            o.append(f'  (zone (net {netid[net]}) (net_name "{net}") '
                     f'(layers "{layer}")')
            o.append(f'    (uuid "{_u("zone", layer, net)}")')
            o.append(f'    (name "{net}_{layer.replace(".", "_")}")')
            o.append("    (hatch edge 0.5)")
            o.append("    (connect_pads (clearance 0.35))")
            o.append("    (min_thickness 0.2)")
            o.append("    (filled_areas_thickness no)")
            o.append("    (fill yes (thermal_gap 0.4) (thermal_bridge_width 0.6) "
                     "(smoothing none) (island_removal_mode 1) "
                     "(island_area_min 2))")
            o.append(f"    (polygon (pts {p}))")
            o.append("  )")

    # ---- rule areas ---------------------------------------------------------
    for name, layers, pts, _why in rules.AREAS:
        if name == "ISOLATION_KEEPOUT":
            o += _rule_area(name, layers, pts)
        else:
            # the zoning areas are conditions for the .kicad_dru rules and must not
            # themselves forbid anything: the rules say which class may be inside them.
            o += _rule_area(name, layers, pts, tracks="allowed", vias="allowed",
                            pours="allowed")
    for i, (mx, my, r) in enumerate(rules.MOUNTING_KEEPOUTS, start=1):
        pts = [(mx + r * math.cos(2 * math.pi * k / 24),
                my + r * math.sin(2 * math.pi * k / 24)) for k in range(24)]
        o += _rule_area(f"MOUNT_KEEPOUT_MH{i}", rules.COPPER_LAYERS, pts)
    for ref, clr in rules.NO_VIA_ZONES:
        part = board.part(ref)
        if not part:
            continue
        b = board.courtyard_box(part)
        pts = [(b[0] - clr, b[1] - clr), (b[2] + clr, b[1] - clr),
               (b[2] + clr, b[3] + clr), (b[0] - clr, b[3] + clr)]
        o += _rule_area(f"NO_VIA_{ref}", rules.COPPER_LAYERS, pts,
                        tracks="allowed", vias="not_allowed", pours="allowed")

    o.append(")")
    text = "\n".join(o) + "\n"
    open(path, "w").write(text)
    return path


# --------------------------------------------------------------------------- project
def write_pro(path, board, pcb_name):
    classes, assignments = rules.kicad_pro_netclasses()
    # KiCad 8 stores the net-class assignment as a list of [pattern, class] pairs
    patterns = [[net, cls] for net, cls in sorted(assignments.items())]
    pro = {
        "board": {"3dviewports": [], "design_settings": {
            "defaults": {
                "board_outline_line_width": 0.1,
                "copper_line_width": 0.2,
                "copper_text_size_h": 1.5, "copper_text_size_v": 1.5,
                "copper_text_thickness": 0.3,
                "silk_line_width": 0.12,
                "silk_text_size_h": 1.0, "silk_text_size_v": 1.0,
                "silk_text_thickness": 0.15,
            },
            "diff_pair_dimensions": [{"gap": 0.35, "via_gap": 0.35, "width": 0.3}],
            "drc_exclusions": [],
            "rules": {
                "max_error": 0.005,
                "min_clearance": rules.MIN_CLEARANCE,
                "min_copper_edge_clearance": rules.EDGE_CLEARANCE,
                "min_hole_clearance": 0.25,
                "min_hole_to_hole": 0.25,
                "min_microvia_diameter": 0.6,
                "min_microvia_drill": 0.3,
                "min_resolved_spokes": 2,
                "min_silk_clearance": 0.0,
                "min_through_hole_diameter": rules.MIN_HOLE,
                "min_track_width": rules.MIN_TRACK,
                "min_via_annular_width": rules.MIN_ANNULAR,
                "min_via_diameter": rules.VIA["pad"],
                "solder_mask_to_copper_clearance": 0.0,
                "use_height_for_length_calcs": True,
            },
            # ECO-EEG-032, finding 2: KiCad checks dangling ends and redundant copper
            # ITSELF.  They are errors here rather than restated as custom rules.
            "rule_severities": {
                "annular_width": "error",
                "clearance": "error",
                "copper_edge_clearance": "error",
                "copper_sliver": "warning",
                "courtyards_overlap": "error",
                "diff_pair_gap_out_of_range": "error",
                "drill_out_of_range": "error",
                "duplicate_footprints": "error",
                "extra_footprint": "error",
                "footprint_type_mismatch": "error",
                "hole_clearance": "error",
                "hole_near_hole": "error",
                "invalid_outline": "error",
                "isolated_copper": "error",
                "item_on_disabled_layer": "error",
                "items_not_allowed": "error",
                "length_out_of_range": "error",
                "lib_footprint_issues": "warning",
                "lib_footprint_mismatch": "warning",
                "malformed_courtyard": "error",
                "microvia_drill_out_of_range": "error",
                "missing_courtyard": "error",
                "missing_footprint": "error",
                "net_conflict": "error",
                "npth_inside_courtyard": "error",
                "padstack": "error",
                "pth_inside_courtyard": "error",
                "shorting_items": "error",
                "silk_edge_clearance": "warning",
                "silk_over_copper": "warning",
                "silk_overlap": "warning",
                "skew_out_of_range": "error",
                "solder_mask_bridge": "error",
                "starved_thermal": "error",
                "text_height": "error",
                "text_thickness": "error",
                "through_hole_pad_without_hole": "error",
                "too_many_vias": "error",
                "track_dangling": "error",
                "track_width": "error",
                "tracks_crossing": "error",
                "unconnected_items": "error",
                "unresolved_variable": "error",
                "via_dangling": "error",
                "zones_intersect": "error",
            },
            "track_widths": sorted({c.min_width for c in rules.CLASSES}
                                   | {c.pref_width for c in rules.CLASSES}),
            "via_dimensions": [{"diameter": rules.VIA["pad"],
                                "drill": rules.VIA["drill"]}],
            "zones_allow_external_fillets": False,
        }},
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": os.path.basename(path), "version": 3},
        "net_settings": {
            "classes": classes,
            "meta": {"version": 4},
            "net_colors": None,
            "netclass_assignments": None,
            "netclass_patterns": patterns,
        },
        "pcbnew": {
            "last_paths": {"gencad": "", "idf": "", "netlist": "",
                           "plot": "", "pos_files": "", "specctra_dsn": "",
                           "step": "", "svg": "", "vrml": ""},
            "page_layout_descr_file": "",
        },
        "schematic": {
            "legacy_lib_dir": "", "legacy_lib_list": [],
            "meta": {"version": 1},
        },
        "sheets": [],
        "text_variables": {
            "BOARD_REV": D.REV_C,
            "RULE_SHEET": "LAY-EEG-034",
        },
    }
    with open(path, "w") as f:
        json.dump(pro, f, indent=2)
        f.write("\n")
    return path
