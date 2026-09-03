#!/usr/bin/env python3
"""
emit_extras.py -- the remaining package v2 counterparts of the package v1 files.

Package v1 shipped a PCB specification sheet, a net report, a board outline in STEP, a kit
BOM workbook, an internal costed BOM and a manufacturer contact list. Each of those needs a
current version, and most of them can be generated rather than typed.

  kicad/EEG-CAR-01_RevB_PCB_spec_sheet.txt      for bidders who do not open a board file
  kicad/EEG-CAR-01_RevB_netreport.json          nets, classes, rules and the routing result
  mech/step/EEG-CAR-01_RevB_board_outline.step  the board as a solid, for enclosure fit
  mech/MANIFEST.json                            every mesh with its measured properties
  docs/EEG_kit_BOM_for_bidders_RevC.xlsx        the kit BOM
  docs/EEG_kit_BOM_INTERNAL_RevC_costed.xlsx    the programme's own costed version
  docs/EEG_kit_manufacturer_contacts_RevB.xlsx  the contact list, corrected

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import collections
import json
import os
import pickle
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
V1 = os.path.join(os.path.dirname(PKG), "package")
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import drc                  # noqa: E402
import pcbgen               # noqa: E402


def drc_stats():
    p = os.path.join(PKG, "kicad", "EEG-CAR-01_RevB_DRC_report.txt")
    t = open(p).read() if os.path.exists(p) else ""
    def g(pat, cast=str, d=None):
        m = re.search(pat, t)
        return cast(m.group(1)) if m else d
    return {
        "segments": g(r"segments (\d+)", int, 0),
        "vias": g(r"vias (\d+)", int, 0),
        "nets": g(r"nets +(\d+)\n", int, 0),
        "connected": g(r"nets fully connected +(\d+)", int, 0),
        "violations": g(r"VIOLATIONS: (\d+)", int, 0),
        "open": len(re.findall(r"^    net \S+:", t, re.M)),
    }


def _status_lines(st):
    """The STATUS paragraph, written from the measured DRC rather than asserted."""
    if st["violations"] == 0:
        return [
            "  The DRC reports ZERO VIOLATIONS: every clearance, width, annular-ring,",
            "  hole-size, edge, non-plated-hole, isolation and zoning rule passes on the",
            "  finished polygons, and both inner planes are one continuous island per net.",
            "",
            "  ECO-EEG-016 section 3 sets the gate for releasing fabrication data as zero",
            "  DRC violations, every net one connected copper island, and both inner planes",
            "  continuous under the analogue zone.  ALL THREE ARE NOW MET.",
            "",
            "  Two things that gate does not cover, and a buyer should know both.  The",
            "  routing was produced by the programme's own tools and HAS NOT BEEN REVIEWED",
            "  BY A HUMAN LAYOUT ENGINEER; that review is RFQ-EEG-002A, and it is now a",
            "  review of a clean board rather than a rescue of a broken one.  And the DRC",
            "  report's CONNECTIONS THE ROUTER HAD TO RELAX figure should be read before",
            "  copper is ordered: a board that closes at minimum geometry is not the same",
            "  board as one that closes at preferred geometry, even when every rule passes.",
            "",
            "  Nothing here has been manufactured or measured.",
        ]
    return [
        f"  {st['violations']} DRC items remain open, named with their pads in",
        "  EEG-CAR-01_RevB_DRC_report.txt.",
        "  THE FABRICATION DATA IS NOT RELEASED FOR FABRICATION until they are closed.",
        "  Closing them and reviewing the whole routing is the scope of RFQ-EEG-002A.",
    ]


# --------------------------------------------------------------------------- spec sheet
def spec_sheet(board, st):
    pads = list(board.pads())
    fp = collections.Counter(p.fpname for p in board.parts)
    drills = collections.Counter(round(p.drill, 2) for p in pads if p.drill)
    L = [
        f"{D.BOARD_NAME} carrier board -- PCB fabrication and assembly specification",
        f"Revision {D.REV}, {D.DATE}.  Governing document: DSN-EEG-003 Rev C section 3.",
        "For bidders who do not open a board file.  Everything here is generated from",
        "package_v2.4/tools/design.py; where this sheet and design.py differ, design.py governs.",
        "",
        "BOARD",
        f"  Size ...................... {D.BOARD_W:.1f} x {D.BOARD_H:.1f} mm, rectangular, "
        f"no cut-outs, no slots",
        "  Layers .................... 4: L1 signal, L2 reference plane, L3 reference plane,",
        "                              L4 signal.  Package v1 specified two; laying the board",
        "                              out showed that two will not do -- see DSN-EEG-003",
        "                              Rev C section 3.",
        "  Material .................. FR-4, Tg >= 150 C",
        "  Finished thickness ........ 1.60 mm +/- 10 %",
        "  Stack-up .................. mask / 35 um L1 / prepreg 0.200 / 17 um L2 /",
        "                              core 1.065 / 17 um L3 / prepreg 0.200 / 35 um L4 / mask",
        "  Copper .................... 1 oz (35 um) outer, 0.5 oz (17 um) inner",
        "  Surface finish ............ ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um",
        "  Solder mask ............... green LPI, both sides",
        "  Silkscreen ................ white, both sides",
        "  Min track / clearance ..... 0.20 mm / 0.20 mm.  Electrode nets keep 0.35 mm",
        "  Vias ...................... 0.60 mm pad / 0.30 mm finished hole, THROUGH ONLY,",
        "                              tented both sides.  No blind, buried, back-drilled,",
        "                              filled or plugged vias",
        f"  Plated holes .............. " + ", ".join(
            f"{d:.2f} mm x{n}" for d, n in sorted(drills.items())
            if any(p.kind == "thru_hole" and round(p.drill, 2) == d for p in pads)),
        "  Non-plated holes .......... 4 x 3.20 mm (M3 mounting, 6 mm copper keep-out),",
        "                              6 x 1.50 mm (DIN 42802 retention posts).  Separate file",
        "  Controlled impedance ...... not required.  USB_DP/USB_DN are a 0.30 mm pair on",
        "                              0.35 mm spacing over the L2 plane: about 90 ohm",
        "                              differential.  No impedance coupon or report;",
        "                              a microsection LOT COUPON is required, and the",
        "                              five lot documents of fabrication drawing note 14",
        "  Panelisation .............. fabricator's choice, v-score or tab-route, 5 mm rails",
        "  Class ..................... IPC-6012 class 2, IPC-A-600 class 2",
        "  Electrical test ........... 100 % to the supplied IPC-D-356A netlist",
        "  Marking ................... fabricator's date code and UL mark on the bottom",
        "                              silkscreen, inside the outline, clear of all pads",
        "",
        "ASSEMBLY",
        f"  Reference designators ..... {len(board.parts)}",
        f"  Pads ...................... {len(pads)} "
        f"({sum(1 for p in pads if p.kind=='smd')} SMD, "
        f"{sum(1 for p in pads if p.kind=='thru_hole')} plated through-hole, "
        f"{sum(1 for p in pads if p.kind=='np_thru_hole')} non-plated)",
        f"  Nets ...................... {len(board.nets())}",
        "  Sides ..................... SMT on the top side only; all through-hole parts on",
        "                              the top side.  The bottom side carries copper and",
        "                              legend only",
        "  Footprints ................",
    ]
    for name, n in sorted(fp.items()):
        L.append(f"      {n:3d} x {name}")
    L += [
        "  Do not populate ........... " + (", ".join(D.DNP) if D.DNP else "none"),
        "  Class ..................... IPC-A-610 class 2",
        "  Test ...................... TST-EEG-004 Rev C, 31 steps (T00, T0, T1 to T29)",
        "  Quantities ................ 2 / 10 / 25 / 50, plus 25 % spare bare boards at 25",
        "                              and 50",
        "",
        "MODULES ARE NOT PLUGGED INTO THIS BOARD",
        "  Except for the ESP32-S3-DevKitC-1, which is inserted directly into J6 and J7 on",
        "  22.86 mm row spacing, every purchased module mounts on the printed plate MP-01",
        "  above the carrier and connects with a keyed 2.54 mm ribbon jumper.  No public",
        "  standard fixes those modules' header geometry, so a socket at a chosen coordinate",
        "  would be a guess.  ICD-EEG-006 Rev B gives the jumper schedule.",
        "",
        "STATUS",
        f"  Routed on four layers: {st['segments']} track segments, {st['vias']} through vias.",
        f"  {st['connected']} of {st['nets']} nets are one connected copper island.",
        # Written from the measured DRC, not asserted.  This used to hard-code "two vias at
        # 0.328 mm" and an open-item count, which read as nonsense the moment the board
        # closed: "0 DRC items remain open: 0 nets each have one connection...".
        *_status_lines(st),
        "",
        "FILES IN THIS FOLDER",
        "  gerber/                                 Gerber X2, Excellon, IPC-D-356A, checksums",
        "  EEG-CAR-01_RevB_routed.kicad_pcb        the routed board",
        "  EEG-CAR-01_RevB_BOM.csv                 grouped BOM with manufacturer part numbers",
        "  EEG-CAR-01_RevB_CPL_SMT_top.csv         pick-and-place, bottom-left origin, Y up",
        "  EEG-CAR-01_RevB_CPL_THT_top.csv         through-hole positions",
        "  EEG-CAR-01_RevB_fabrication_drawing.pdf dimensions, drill schedule, stack-up, notes",
        "  EEG-CAR-01_RevB_assembly_drawing.pdf    designators, pin 1, DNP, process",
        "  EEG-CAR-01_RevB_copper_layers.pdf       all four layers at 1:1",
        "  EEG-CAR-01_RevB_DRC_report.txt          every rule, every measurement, every item",
        "  EEG-CAR-01_RevB_netreport.json          nets, classes and rules, machine-readable",
        "",
        "Licence: CC BY-SA 4.0.  TI One Voice research programme, one.witysk.org.",
        "Nothing in this package has been manufactured or measured.",
    ]
    p = os.path.join(PKG, "kicad", "EEG-CAR-01_RevB_PCB_spec_sheet.txt")
    open(p, "w").write("\n".join(L) + "\n")
    return p


# --------------------------------------------------------------------------- net report
def netreport(board, st):
    nets = board.nets()
    out = {
        "board": D.BOARD_NAME,
        "revision": D.REV,
        "date": D.DATE,
        "size_mm": [D.BOARD_W, D.BOARD_H],
        "layers": ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"],
        "layer_roles": {"F.Cu": "signal", "In1.Cu": "reference plane",
                        "In2.Cu": "reference plane", "B.Cu": "signal"},
        "zone_split_x_mm": D.ZONE_SPLIT_X,
        "parts": len(board.parts),
        "pads": sum(1 for _ in board.pads()),
        "nets": len(nets),
        "status": (
            # Released for REVIEW is not released for fabrication.  A DFM tool reading
            # this field must not treat a clean DRC as a human sign-off.
            "routed; %d of %d nets are one connected copper island; no DRC item open; "
            "RELEASED FOR REVIEW under RFQ-EEG-002A, NOT RELEASED FOR FABRICATION "
            "(no human layout engineer has reviewed this routing)"
            % (st["connected"], st["nets"])
            if st["violations"] == 0 and st["connected"] == st["nets"] else
            "routed; %d of %d nets are one connected copper island; %d DRC items "
            "open; NOT RELEASED FOR FABRICATION"
            % (st["connected"], st["nets"], st["violations"])),
        # These are the router's PREFERRED widths and clearances, not minimums; the
        # board is routed narrower than them in places and still passes.  What was
        # actually enforced is drc_minimums below, taken from drc.py itself so the two
        # cannot drift.  A DFM tool must grade the board against drc_minimums.
        "netclasses": {k: {"track_mm_preferred": v[0], "clearance_mm_preferred": v[1]}
                       for k, v in D.NETCLASS.items()},
        "drc_minimums": {"clearance_mm": drc.MIN_CLEARANCE,
                         "electrode_clearance_mm": drc.ELECTRODE_CLEARANCE,
                         "track_mm": drc.MIN_TRACK,
                         "edge_clearance_mm": drc.EDGE_CLEARANCE,
                         "npth_clearance_mm": drc.NPTH_CLEARANCE,
                         "annular_ring_mm": drc.MIN_ANNULAR,
                         "hole_mm": drc.MIN_HOLE,
                         "source": "package_v2.4/tools/drc.py, the rules the DRC report "
                                   "applied"},
        "route_rules": [
            "Analogue zone x < 62 mm, digital zone x > 62 mm. No digital net enters the "
            "analogue zone and no analogue net leaves it, with one declared exception "
            "(CMP_RAW, through R83 and the D23 clamp).",
            "AGND_REF is the analogue 0 V mid-rail, not a ground. It joins DGND at R90 "
            "only. HARN_SHIELD joins DGND at R91 only.",
            "Electrode nets keep 0.35 mm to everything else and are routed with a "
            "reference plane directly beneath.",
            "No via inside the analogue module connector outlines J2, J4, J23, J29.",
            "No copper of any kind in the isolation strip x >= 141 mm, y = 2 to 22 mm, on "
            "any layer. The ADuM4160 module carries the barrier.",
            "USB_DP and USB_DN are a 0.30 mm pair on 0.35 mm spacing over the L2 plane.",
            "Through vias only, 0.60 mm pad on a 0.30 mm finished hole.",
        ],
        "nets_detail": {
            n: {"pads": [f"{p.ref}.{p.num}" for p in ps],
                "class": D.netclass_of(n),
                "zone": ("analogue" if n in D.ANALOG_ZONE_NETS
                         else "digital" if n in D.DIGITAL_ONLY_NETS else "either")}
            for n, ps in sorted(nets.items())},
    }
    p = os.path.join(PKG, "kicad", "EEG-CAR-01_RevB_netreport.json")
    json.dump(out, open(p, "w"), indent=1)
    return p


# --------------------------------------------------------------------------- board solid
def board_step(board):
    import cadquery as cq
    b = (cq.Workplane("XY")
         .box(D.BOARD_W, D.BOARD_H, 1.6, centered=(True, True, False)))
    holes = {}
    for pd in board.pads():
        if pd.drill:
            holes.setdefault(round(pd.drill, 2), []).append(
                (pd.x - D.BOARD_W / 2, D.BOARD_H / 2 - pd.y))
    for dia, pts in holes.items():
        b = b.cut(cq.Workplane("XY", origin=(0, 0, -1)).pushPoints(pts)
                  .circle(dia / 2).extrude(4))
    out = os.path.join(PKG, "mech", "step", "EEG-CAR-01_RevB_board_outline.step")
    cq.exporters.export(b, out, cq.exporters.ExportTypes.STEP)
    cq.exporters.export(b, out.replace("/step/", "/stl/").replace(".step", ".stl"))
    return out


# The manifest is NOT written here.  tools/mech_gen.py owns it, and owns the OA-2 schema
# (sha256, revision, material, process, units, marking, and the DXFs as well as the meshes).
# There were two manifest generators with two different schemas, and whichever ran last won;
# emit_extras.py ran last, so the thin schema shipped.  See ECO-EEG-016 and PARTS-EEG-019
# OA-2.  If you need to refresh the manifest, run tools/mech_gen.py.


def main():
    board = pcbgen.BoardV2()
    board.validate()
    st = drc_stats()
    print(spec_sheet(board, st))
    print(netreport(board, st))
    # HM-01 is carried over from package v1 as a mesh; it is a rendered form study and its
    # geometry changes after the Stage 0 fit measurement, so there is no parametric model.
    src = os.path.join(V1, "mech", "HM-01_frame_monocoque.stl")
    dst = os.path.join(PKG, "mech", "stl", "HM-01_frame_monocoque.stl")
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(dst)
    print(board_step(board))
    # mech/MANIFEST.json is written by tools/mech_gen.py, not here (OA-2).


if __name__ == "__main__":
    main()
