#!/usr/bin/env python3
"""
emit_all.py -- build every generated artifact of package_v2.3 from design.py.

    python3 emit_all.py            route, check and write everything
    python3 emit_all.py --cached   reuse routed.pkl instead of routing again

Writes into package_v2.4/kicad, package_v2.4/schematic and package_v2.4/graphics.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import hashlib
import os
import pickle
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import pcbgen               # noqa: E402
import drc                  # noqa: E402
import gerber               # noqa: E402
import drawings             # noqa: E402
import kicad_write          # noqa: E402
import schematic            # noqa: E402
import build_board as BB    # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main(cached=False):
    kdir = os.path.join(PKG, "kicad")
    gdir = os.path.join(kdir, "gerber")
    sdir = os.path.join(PKG, "schematic")
    grdir = os.path.join(PKG, "graphics")
    for d in (kdir, gdir, sdir, grdir):
        os.makedirs(d, exist_ok=True)

    if cached and os.path.exists(os.path.join(HERE, "routed.pkl")):
        res = pickle.load(open(os.path.join(HERE, "routed.pkl"), "rb"))
        res["board"] = pcbgen.BoardV2()
        res["board"].validate()
    else:
        res = BB.build(verbose=True, plot=os.path.join(grdir, "EEG-CAR-01_RevB_routed.png"))
        pickle.dump({k: v for k, v in res.items() if k != "board"},
                    open(os.path.join(HERE, "routed.pkl"), "wb"))

    board, tracks, vias, pour = res["board"], res["tracks"], res["vias"], res["pours"]

    print("== DRC ==")
    v, stats = drc.write_report(
        os.path.join(kdir, "EEG-CAR-01_RevB_DRC_report.txt"),
        board, tracks, vias, pour, res["iso_box"], res.get("narrowed", []))
    print(f"   {len(v)} violations")
    for k, val in stats.items():
        print(f"   {k}: {val}")

    print("== Gerbers, drill, netlist ==")
    netid = {n: i + 1 for i, n in enumerate(sorted(board.nets()))}
    made, pth, npth = gerber.write_all(gdir, board, tracks, vias, pour, netid)
    gerber.cpl(os.path.join(kdir, "EEG-CAR-01_RevB_CPL_SMT_top.csv"), board)
    gerber.cpl_tht(os.path.join(kdir, "EEG-CAR-01_RevB_CPL_THT_top.csv"), board)
    gerber.bom(os.path.join(kdir, "EEG-CAR-01_RevB_BOM.csv"), board)
    print(f"   {len(made)} fabrication files; PTH tools {pth}; NPTH tools {npth}")

    print("== KiCad board ==")
    kicad_write.write(os.path.join(kdir, "EEG-CAR-01_RevB_routed.kicad_pcb"),
                      board, tracks, vias, pour)

    print("== Drawings ==")
    drawings.build(kdir, board, tracks, vias, pour, png_dir=grdir)

    print("== Schematic ==")
    schematic.build(os.path.join(sdir, "SCH-EEG-005_RevB_schematic_set.pdf"),
                    os.path.join(sdir, "png"))

    print("== Zip and manifest ==")
    zpath = os.path.join(gdir, "EEG-CAR-01_RevB_gerber_X2.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(gdir)):
            if f.endswith((".gbr", ".drl", ".ipc")):
                z.write(os.path.join(gdir, f), f)
    # the copper rows come from gerber.LAYER_FUNC, the same table that writes the
    # %TF.FileFunction of each file, so a layer cannot be omitted or mis-numbered here
    copper = []
    for lay, func in gerber.LAYER_FUNC.items():
        num, pos = func.split(",")
        desc = {"Top": "top copper", "Bot": "bottom copper"}.get(pos, f"inner copper {num}")
        fname = f"{D.BOARD_NAME}-{lay.replace('.', '_')}.gbr"
        copper.append(f"  {fname:<30s}{desc:<20s}Copper,{func},Signal")
    lines = ["EEG-CAR-01 Rev B -- fabrication data manifest",
             f"generated {D.DATE} from package_v2.4/tools/design.py",
             "",
             "LAYER MAP",
             *copper,
             "  EEG-CAR-01-F_Mask.gbr         top solder mask     Soldermask,Top",
             "  EEG-CAR-01-B_Mask.gbr         bottom solder mask  Soldermask,Bot",
             "  EEG-CAR-01-F_Silkscreen.gbr   top legend          Legend,Top",
             "  EEG-CAR-01-B_Silkscreen.gbr   bottom legend       Legend,Bot",
             "  EEG-CAR-01-F_Paste.gbr        stencil (top only)  Paste,Top",
             "  EEG-CAR-01-Edge_Cuts.gbr      board profile       Profile,NP",
             "  EEG-CAR-01-User_Drawings.gbr  reference only, do not image",
             "  EEG-CAR-01-PTH.drl            plated holes, Excellon 2, metric",
             "  EEG-CAR-01-NPTH.drl           non-plated holes, Excellon 2, metric",
             "  EEG-CAR-01-IPC-D-356A.ipc     netlist for bare-board electrical test",
             "",
             "FORMAT",
             "  Gerber X2 (RS-274X with file attributes), 4.6 absolute, metric,",
             "  leading zeros omitted.  Origin is the BOTTOM-LEFT board corner with Y up,",
             "  which is also the origin of both drill files and of the CPL files.",
             "  The design source uses a top-left origin with Y down; the conversion is",
             f"  y_gerber = {D.BOARD_H:.1f} - y_design, applied once, in "
             f"package_v2.4/tools/gerber.py.",
             "",
             "SHA-256"]
    for f in sorted(os.listdir(gdir)):
        p = os.path.join(gdir, f)
        if os.path.isfile(p) and not f.endswith(".txt"):
            lines.append(f"  {sha256(p)}  {f}")
    open(os.path.join(gdir, "README_layer_map_and_checksums.txt"), "w").write(
        "\n".join(lines) + "\n")
    print("   ", zpath)
    print("done")


if __name__ == "__main__":
    main(cached="--cached" in sys.argv)
