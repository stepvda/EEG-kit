#!/usr/bin/env python3
"""
emit_revc.py -- write the EEG-CAR-01 Rev C layout-input set from design.py.

Rev C has no routing of its own.  It is the same circuit as Rev B at corrected
footprints and part numbers, prepared so that an external layout contractor can place
and route it (ECO-EEG-030).  Everything this module writes carries `RevC` in its file
stem, computed by `design.stem()` and never typed.

What it writes into package/kicad:

    EEG-CAR-01_RevC_BOM.csv                    grouped BOM, with the substitution column
    EEG-CAR-01_RevC_CPL_SMT_top.csv            provisional placement, CAM convention
    EEG-CAR-01_RevC_CPL_THT_top.csv            provisional placement, CAM convention
    EEG-CAR-01_RevC-IPC-D-356A.ipc             netlist: 156 nets, from the pads alone

The two CPL files are PROVISIONAL and say so in the file: outside the thirty connectors,
Rev C placement is what the contractor is being paid to decide, and the coordinates in
them are Rev B's.  The netlist needs no routing -- it is a list of pads by net -- so it
is final.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import gerber               # noqa: E402
import pcbgen               # noqa: E402

KDIR = os.path.join(PKG, "kicad")


def _provisional_banner(path, what):
    """Prepend a comment line to a CSV that a machine reads as a row and a person reads
    as a warning.  CPL loaders skip a leading '#' line; the warning is not optional,
    because a contractor who treats these coordinates as fixed has been misled."""
    with open(path) as f:
        body = f.read()
    head = (f"# PROVISIONAL. {what}  EEG-CAR-01 Rev {D.REV_C} is UNROUTED and its "
            f"placement, outside the thirty connectors J1-J30, is what the layout "
            f"contractor decides. These coordinates are Rev B's and are a starting "
            f"point, not a specification. Coordinate convention: bottom-left origin, "
            f"Y up. See LAY-EEG-034 and kicad/RevC_layout_inputs/"
            f"README_layout_inputs.md.\n")
    with open(path, "w") as f:
        f.write(head + body)
    return path


def emit_bom_cpl_netlist(board=None, verbose=True):
    board = board or pcbgen.BoardV2()
    errs, warns = board.validate()
    if errs:
        raise SystemExit("design.py does not validate:\n  " + "\n  ".join(errs))
    os.makedirs(KDIR, exist_ok=True)
    stem = D.stem(D.REV_C)
    made = []

    made.append(gerber.bom(os.path.join(KDIR, f"{stem}_BOM.csv"), board))
    made.append(_provisional_banner(
        gerber.cpl(os.path.join(KDIR, f"{stem}_CPL_SMT_top.csv"), board),
        "Surface-mount placement."))
    made.append(_provisional_banner(
        gerber.cpl_tht(os.path.join(KDIR, f"{stem}_CPL_THT_top.csv"), board),
        "Through-hole placement."))

    # the netlist is derived from pads only: no track, no via, nothing routed
    netid = {n: i + 1 for i, n in enumerate(sorted(board.nets()))}
    made.append(gerber.ipc356(os.path.join(KDIR, f"{stem}-IPC-D-356A.ipc"),
                              board, [], netid, rev=D.REV_C))
    if verbose:
        for m in made:
            print("   ", os.path.relpath(m, PKG))
    return made


def main(verbose=True):
    board = pcbgen.BoardV2()
    board.validate()
    if verbose:
        print(f"== EEG-CAR-01 Rev {D.REV_C} layout inputs ==")
        print(f"   {len(board.parts)} designators, "
              f"{sum(1 for _ in board.pads())} pads, {len(board.nets())} nets")
    made = emit_bom_cpl_netlist(board, verbose)
    return made


if __name__ == "__main__":
    main()
