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
    EEG-CAR-01_RevC.kicad_dru                  custom design rules, from tools/rules.py
    EEG-CAR-01_RevC*.kicad_sch                 the native hierarchical schematic
    EEG-CAR-01.kicad_sym                       the symbol library it is drawn from
    EEG-CAR-01_RevC_schematic_netlist_check.txt  the gate on the schematic
    EEG-CAR-01_RevC_unrouted.kicad_pcb         the board: placed, netted, NO copper
    EEG-CAR-01_RevC.kicad_pro                  net classes, rules and severities
    EEG-CAR-01_RevC_outline_and_fixed_connectors.dxf   the mechanical inputs

and into package/mech:

    step/footprints/*.step                     one body per footprint class, bound
                                               into the board's 3D view
    step/EEG-CAR-01_RevC_carrier_envelopes.step
    step/MP-01_RevC_plate_and_standoffs.step
    step/EEG-CAR-01_RevC_module_envelopes.step
    EEG-CAR-01_RevC_collision_check.txt

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
import collision_check      # noqa: E402
import dxf_out              # noqa: E402
import emit_kicad_sch       # noqa: E402
import kicad_pcb8           # noqa: E402
import mech_bodies          # noqa: E402
import pcbgen               # noqa: E402
import rules                # noqa: E402
import sch_netlist          # noqa: E402

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


def emit_rules(verbose=True):
    """The KiCad custom-rules file.  One source of truth with the in-house DRC: both
    sides read tools/rules.py, and neither is maintained by hand (ECO-EEG-032)."""
    os.makedirs(KDIR, exist_ok=True)
    path = os.path.join(KDIR, f"{D.stem(D.REV_C)}.kicad_dru")
    with open(path, "w") as f:
        f.write(rules.kicad_dru())
    if verbose:
        print("   ", os.path.relpath(path, PKG))
    return [path]


def verify_board(pcb, board, nfixed):
    """Read the board back and check it against design.py.

    The board file is the thing the contractor routes.  A footprint dropped, a net lost
    or a stray track left in it is not a cosmetic defect: it is a board routed to the
    wrong netlist.  So it is parsed back rather than trusted.
    """
    import json
    import kicad_parse
    text = open(pcb).read()
    for token in ("(segment ", "(via ", "(arc "):
        if token in text:
            raise SystemExit(f"{os.path.basename(pcb)} contains {token.strip()} -- "
                             f"Rev C is unrouted and this file must carry no copper")
    got = kicad_parse.load(pcb)
    if len(got.footprints) != len(board.parts):
        raise SystemExit(f"{len(got.footprints)} footprints written, "
                         f"{len(board.parts)} expected")
    want_nets, got_nets = {}, {}
    for pd in board.pads():
        if pd.net:
            want_nets.setdefault(pd.net, set()).add(f"{pd.ref}.{pd.num}")
    for pd in got.pads():
        if pd.netname:
            got_nets.setdefault(pd.netname, set()).add(f"{pd.ref}.{pd.num}")
    if want_nets != got_nets:
        bad = [k for k in set(want_nets) | set(got_nets)
               if want_nets.get(k) != got_nets.get(k)]
        raise SystemExit(f"the board's netlist differs from design.py on {len(bad)} "
                         f"net(s): {sorted(bad)[:8]}")
    n_locked = text.count("(locked yes)")
    if n_locked != len(kicad_pcb8.LOCKED):
        raise SystemExit(f"{n_locked} footprints locked, "
                         f"{len(kicad_pcb8.LOCKED)} expected")
    for name, _lay, _pts, _why in rules.AREAS:
        if f'(name "{name}")' not in text:
            raise SystemExit(f"rule area {name} is missing from the board; the "
                             f".kicad_dru refers to it by that name")
    pro = os.path.join(KDIR, f"{D.stem(D.REV_C)}.kicad_pro")
    cfg = json.load(open(pro))
    names = {c["name"] for c in cfg["net_settings"]["classes"]}
    want = {("Default" if c.name == "DEFAULT" else c.name) for c in rules.CLASSES}
    if names != want:
        raise SystemExit(f"the project file's net classes are {sorted(names)}, "
                         f"not {sorted(want)}")
    if len(cfg["net_settings"]["netclass_patterns"]) != len(set(D.N.values())):
        raise SystemExit("the project file does not assign every net to a class")
    if cfg["board"]["design_settings"]["rule_severities"]["track_dangling"] != "error":
        raise SystemExit("track_dangling is not an error in the project file")
    return dict(footprints=len(got.footprints), pads=sum(1 for _ in got.pads()),
                nets=len(got_nets), locked=n_locked, segments=len(got.segments),
                vias=len(got.vias))


def emit_board(board, verbose=True):
    """The unrouted board, the project file and the DXF."""
    os.makedirs(KDIR, exist_ok=True)
    stem = D.stem(D.REV_C)
    made = []
    # The board is `<project>.kicad_pcb` and NOT `<project>_unrouted.kicad_pcb`.
    #
    # A KiCad project expects its board and its schematic to share the project's stem.
    # A board named `..._unrouted.kicad_pcb` opens standalone, and standalone means
    # WITHOUT `EEG-CAR-01_RevC.kicad_pro` -- so the eight net classes, the 156 net
    # assignments and the rule severities that make track_dangling an error would all be
    # silently absent for the contractor, which is the opposite of the point.  That the
    # board is unrouted is said in its own title block, in comment 1, in the file's
    # first four lines and in LAY-EEG-034, none of which a file name has to repeat.
    models = mech_bodies.write_footprint_models(
        os.path.join(PKG, "mech", "step", "footprints"))
    kicad_pcb8.set_models(models)
    pcb = os.path.join(KDIR, f"{stem}.kicad_pcb")
    made.append(kicad_pcb8.write_pcb(pcb, board))
    made.append(kicad_pcb8.write_pro(os.path.join(KDIR, f"{stem}.kicad_pro"), board,
                                     os.path.basename(pcb)))
    dxf, nfixed = dxf_out.write(
        os.path.join(KDIR, f"{stem}_outline_and_fixed_connectors.dxf"), board)
    made.append(dxf)
    st = verify_board(pcb, board, nfixed)
    if verbose:
        print(f"    {len(models)} footprint 3D bodies bound")
        print(f"    board reads back: {st['footprints']} footprints, {st['pads']} pads, "
              f"{st['nets']} nets, {st['segments']} segments, {st['vias']} vias, "
              f"{st['locked']} locked")
        for m in made:
            print("   ", os.path.relpath(m, PKG))
    return made


def emit_mech(verbose=True):
    """The 3D bodies and the collision check (ECO-EEG-033, finding 6)."""
    made = mech_bodies.write_step(os.path.join(PKG, "mech", "step"))
    n, report = collision_check.main(verbose=False)
    made.append(report)
    if verbose:
        for m in made:
            print("   ", os.path.relpath(m, PKG))
        print(f"    collision check: {n} finding(s) -- see the report; they are NOT "
              f"all closed")
    return made


def main(verbose=True):
    board = pcbgen.BoardV2()
    board.validate()
    if verbose:
        print(f"== EEG-CAR-01 Rev {D.REV_C} layout inputs ==")
        print(f"   {len(board.parts)} designators, "
              f"{sum(1 for _ in board.pads())} pads, {len(board.nets())} nets")
    made = emit_bom_cpl_netlist(board, verbose)
    made += emit_rules(verbose)
    made += emit_board(board, verbose)
    made += emit_mech(verbose)
    made += emit_kicad_sch.main(verbose)
    ndiff, nprob, report = sch_netlist.main(write=True)
    made.append(report)
    if ndiff or nprob:
        raise SystemExit(f"the schematic does not match design.py: {ndiff} netlist "
                         f"difference(s), {nprob} structural finding(s). "
                         f"See {os.path.relpath(report, PKG)}")
    if verbose:
        print("   schematic netlist matches design.py: 0 differences")
    return made


if __name__ == "__main__":
    main()
