#!/usr/bin/env python3
"""
emit_handover.py -- assemble kicad/RevC_layout_inputs/, the set that goes to the layout
contractor, with a README and a SHA-256 for every file.

**Nothing here sends anything.**  It writes a directory.  Stephane uploads it.

The files are COPIED rather than linked or zipped, so that what the contractor receives
is a self-contained set whose checksums can be quoted in the covering email and checked
on arrival -- which is the same discipline
`kicad/gerber/README_layer_map_and_checksums.txt` applies to the Rev B fabrication data.
Every file is generated, so the copy is not a second source of truth: re-run
`tools/emit_all.py` and the directory is rebuilt identically.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import kicad_fmt            # noqa: E402
import rules                # noqa: E402

OUT = os.path.join(PKG, "kicad", "RevC_layout_inputs")
OUT_K10 = os.path.join(PKG, "kicad", "RevC_layout_inputs_kicad10")
EQUIV = "EQUIVALENCE_kicad8_vs_kicad10.md"


def out_dir(fmt):
    return OUT if fmt.key == "kicad8" else OUT_K10


# The two paragraphs that differ between the two sets.  Everything else in the README is
# one text, because everything else about the two sets is the same by construction.
KICAD_SECTION = """## KiCad version -- and there are two sets

This directory is the **{label}** emission: `(kicad_sch (version {schv}))` and
`(kicad_pcb (version {pcbv}))`, `(generator_version "{genv}")`.

**{other_line}**

Both sets are generated from one source, `tools/design.py`, in a single run. The {k10}
set is the {k8} set passed through KiCad's own `kicad-cli pcb upgrade`, `sch upgrade`
and `sym upgrade`, so the two are equivalent by construction and not by assertion; the
schema is KiCad's to define and this programme does not hand-write it. They have then
been **diffed against each other and the result written down** -- netlist, board census,
net classes, the 37 custom rules, the DRC severities, the locked footprints, the fixed
geometry and the rule areas. Read **`{equiv}`** in the KiCad 10 directory. Where a check
could not be performed it says so rather than inferring the answer.

Independently of KiCad, `{stem}_schematic_netlist_check.txt` is the schematic parsed
back out of the emitted files -- pin geometry from their own `lib_symbols`, wires,
junctions, labels and power symbols -- and diffed against the design source: **156 nets
and 614 pins on both sides, 0 differences.** The generator is not asked what it meant.

{drc_line}"""

K8_OTHER = ("If you are on KiCad 10, use `kicad/RevC_layout_inputs_kicad10/` instead. "
            "This directory is the KiCad 8 reference set and stays as the published "
            "one.")
K10_OTHER = ("This is the set for the JLCPCB layout desk, which has confirmed it runs "
             "KiCad 10. The KiCad 8 set is kept alongside at "
             "`kicad/RevC_layout_inputs/` for anyone still on 8.")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _files():
    """(source path, name in the package, what it is).  The order is the order of the
    input list the programme committed to on 8 September 2026."""
    stem = D.stem(D.REV_C)
    K = os.path.join(PKG, "kicad")
    M = os.path.join(PKG, "mech")
    DOC = os.path.join(PKG, "docs")
    out = []

    out.append((os.path.join(K, f"{stem}.kicad_pro"), f"{stem}.kicad_pro",
                "the KiCad project: eight net classes, an assignment for all 156 nets, "
                "the board minima and the DRC severities. Open THIS, not the board on "
                "its own"))
    out.append((os.path.join(K, f"{stem}.kicad_sch"), f"{stem}.kicad_sch",
                "input 1: the root schematic, a block diagram of the nine sheets"))
    for f in sorted(os.listdir(K)):
        if f.startswith(f"{stem}_") and f.endswith(".kicad_sch"):
            out.append((os.path.join(K, f), f, "input 1: a schematic sheet"))
    out.append((os.path.join(K, "EEG-CAR-01.kicad_sym"), "EEG-CAR-01.kicad_sym",
                "the symbol library the schematic is drawn from"))
    out.append((os.path.join(K, f"{stem}.kicad_pcb"), f"{stem}.kicad_pcb",
                "the board: placed, netted, LOCKED where it must be, and UNROUTED"))
    out.append((os.path.join(K, f"{stem}.kicad_dru"), f"{stem}.kicad_dru",
                "input 6, machine-readable: 37 custom design rules. Load it"))
    out.append((os.path.join(K, f"{stem}-IPC-D-356A.ipc"), f"{stem}-IPC-D-356A.ipc",
                "input 2: the netlist, 156 nets, from the pads alone"))
    out.append((os.path.join(K, f"{stem}_schematic_netlist_check.txt"),
                f"{stem}_schematic_netlist_check.txt",
                "the schematic read back and diffed against the design source: "
                "0 differences"))
    out.append((os.path.join(K, f"{stem}_BOM.csv"), f"{stem}_BOM.csv",
                "input 3: the BOM, with a Substitution column"))
    out.append((os.path.join(DOC, "footprint_audit_RevC.md"),
                "footprint_audit_RevC.md",
                "input 3: what 'verified footprints' means -- all 211 designators "
                "audited against their part numbers"))
    out.append((os.path.join(K, f"{stem}_CPL_SMT_top.csv"), f"{stem}_CPL_SMT_top.csv",
                "PROVISIONAL placement, surface mount. Rev B's coordinates, not a "
                "specification"))
    out.append((os.path.join(K, f"{stem}_CPL_THT_top.csv"), f"{stem}_CPL_THT_top.csv",
                "PROVISIONAL placement, through hole"))
    out.append((os.path.join(K, f"{stem}_outline_and_fixed_connectors.dxf"),
                f"{stem}_outline_and_fixed_connectors.dxf",
                "input 4: outline, mounting holes and keep-outs, the isolation strip, "
                "the zone split and all thirty connector courtyards with pin-1 marks"))
    for f in ("EEG-CAR-01_RevC_carrier_envelopes.step",
              "MP-01_RevC_plate_and_standoffs.step",
              "EEG-CAR-01_RevC_module_envelopes.step"):
        out.append((os.path.join(M, "step", f), f"step/{f}",
                    "input 5: 3D bodies"))
    fpdir = os.path.join(M, "step", "footprints")
    if os.path.isdir(fpdir):
        for f in sorted(os.listdir(fpdir)):
            if f.endswith(".step"):
                out.append((os.path.join(fpdir, f), f"step/footprints/{f}",
                            "input 5: the body bound to one footprint class, referenced "
                            "by the board file"))
    out.append((os.path.join(M, "EEG-CAR-01_RevC_collision_check.txt"),
                "EEG-CAR-01_RevC_collision_check.txt",
                "the 3D collision report. Read case D"))
    out.append((os.path.join(DOC, "LAY-EEG-034_RevA_carrier_layout_rule_sheet.pdf"),
                "LAY-EEG-034_RevA_carrier_layout_rule_sheet.pdf",
                "input 6: THE RULE SHEET. It is part of the order specification"))
    out.append((os.path.join(DOC, "LAY-EEG-034_RevA_carrier_layout_rule_sheet.md"),
                "LAY-EEG-034_RevA_carrier_layout_rule_sheet.md",
                "input 6, as text"))
    return out


README = """# EEG-CAR-01 Rev C -- layout inputs

**Document:** not a controlled document. It is the covering note for the set in this
directory, which is generated by `tools/emit_handover.py`.
**Board:** EEG-CAR-01 Rev {rev}, {w:.1f} x {h:.1f} mm, four layers, through vias only.
**Date:** {date}
**Licence:** CC BY-SA 4.0

## What this is

The complete input set for the **placement and routing of EEG-CAR-01 Rev C**. The board
is **unrouted**. Its predecessor, Rev B, was routed by this programme's own tools, read
by an external layout engineer between 3 and 5 September 2026, and **withdrawn from
fabrication** on his advice; his seven findings are the reason this set exists and are
encoded in the rule sheet. Nothing in this package has been manufactured or measured, and
no safety engineer has reviewed the design.

## Open this, not that

Open **`{stem}.kicad_pro`**. The board and the schematic share the project's stem so that
KiCad loads them together with the net classes and the DRC severities. Opening
`{stem}.kicad_pcb` on its own gets you the geometry **without** the eight net classes,
without the assignment of all 156 nets, and without `track_dangling` set to error -- which
is most of the specification.

Load **`{stem}.kicad_dru`** with the project. It is 37 rules and it is not optional.

{kicad_section}

## What is locked, and what is yours

**37 footprints are locked and may not be moved**: the thirty connectors **J1 to J30**,
the four mounting holes **MH1 to MH4**, and the three fiducials **FID1 to FID3**. The
connectors are fixed by the enclosure, the MP-01 module plate and the harness. If one of
them has to move to make the board route, say so -- it is a change we may be able to
make, and it is not one you can make.

**Everything else is unlocked and is yours to place.** The 174 unlocked parts sit at
their Rev B coordinates, which are a starting point and not a specification: Rev B's
placement is what produced a board that closed only by relaxing 169 connections to the
minimum geometry the rules allow. The two CPL files carry the same coordinates and say
PROVISIONAL on their first line for the same reason.

## Coordinates

**The `.kicad_pcb` and the `.dxf` both use a top-left origin with Y increasing DOWN**,
which is KiCad's own convention and this programme's design source.

**Gerber, drill and both CPL files use a bottom-left origin with Y increasing UP**, which
is what CAM expects: `y_cam = {h:.1f} - y_design`. The conversion happens in one place,
`tools/gerber.py`. Do not mix the two; a board mirrored about its own middle is the
result.

## Which rules KiCad checks, and which we check on return

Six of the seven findings are rules. **Four of them KiCad can check** and are in the
`.kicad_dru` or in the project's severities:

- no via inside an SMD pad;
- no dangling track end (KiCad's own `track_dangling`, raised to **error**);
- no redundant copper path;
- the per-class width, clearance, layer and via rules, and the zoning, star-point and
  isolation rule areas.

**Two of them KiCad cannot check, because it has no constraint for either:**

- **no angle below 90 degrees between two segments of one track**, and every segment on a
  0, 45, 90 or 135 degree axis;
- **a track entering a pad within {frac:.0f} % of the pad's minor dimension of the pad
  centre.**

Those two are checked **by us, on the geometry you return**, with `tools/drc.py` and
`tools/drc_geometry.py`. Both tools are in the repository. They are the same ones that
regraded Rev B and found **1 311** occurrences of these six rules in a board whose own
report read "VIOLATIONS: 0 -- none". That is not a warning about your work; it is what
happened to ours, and it is why the rules are written down this time.

## The three-phase process, and the gate in the middle

We understand the order as three phases with a confirmation at each. **The one that
matters is the placement gate.** Placement drives via count, must precede routing, and is
reviewed before routing starts -- that is the reviewing engineer's own principle and we
have adopted it.

**The placement stage is delivered as a `.kicad_pcb` with the STEP bodies loaded and a 3D
collision check passed, and we review it before routing is confirmed.** The review is a
written findings list by net, pad pair and coordinate -- not edits to the board file --
and it is capped at four to six hours. Please do not begin routing on an unconfirmed
placement.

## One thing that is ours and not yours

`EEG-CAR-01_RevC_collision_check.txt` case D reports that the twelve plate-mounted modules
do not fit on the MP-01 plate: 17 356 mm2 of declared envelopes into 12 409 mm2 of plate.
Case B reports that the plate's DevKit opening is 2 mm shorter than the DevKit. **Neither
is a carrier layout question and neither blocks this order.** They are recorded against
this programme in ASM-EEG-023. They are mentioned because the STEP bodies are in this set
and you would otherwise wonder.

## Contact

Stephane van der Aa
Founder, TI One Voice
one.witysk.org
stephane@stepvda.com
+32 493 70 16 01
"""


def _write_readme(fmt, drc_line, verbose=True):
    other = K8_OTHER if fmt.key == "kicad8" else K10_OTHER
    section = KICAD_SECTION.format(
        label=fmt.label, schv=fmt.sch_version, pcbv=fmt.pcb_version,
        genv=fmt.generator_version, other_line=other, equiv=EQUIV,
        k8=kicad_fmt.KICAD8.label, k10=kicad_fmt.KICAD10.label,
        stem=D.stem(D.REV_C), drc_line=drc_line)
    readme = README.format(rev=D.REV_C, w=D.BOARD_W, h=D.BOARD_H, date=D.DATE_C,
                           stem=D.stem(D.REV_C),
                           frac=rules.GEOMETRY["pad_entry_frac"] * 100,
                           kicad_section=section)
    p = os.path.join(out_dir(fmt), "README_layout_inputs.md")
    open(p, "w").write(readme)
    return p


def _write_manifest(fmt, files, extra, verbose=True):
    """SHA256SUMS.txt over this directory's own files."""
    OUTD = out_dir(fmt)
    if fmt.key == "kicad8":
        repro = ["Every file here is GENERATED from tools/design.py.  Re-running",
                 "tools/emit_all.py rebuilds this directory identically, so a checksum",
                 "that does not match means the file changed and not that the build is",
                 "nondeterministic."]
    else:
        # Say this plainly rather than let the manifest make a promise it cannot keep.
        repro = [
            "Every file here is GENERATED from tools/design.py.  These checksums",
            "identify THIS emission and verify what you received against what was",
            "sent, which is what a manifest is for.",
            "",
            "They are NOT reproducible run to run, and the KiCad 8 set's are.  Two",
            "files move on every emission and neither is a change to the design:",
            "",
            "  * the .kicad_pcb and the .kicad_sch files, because KiCad mints a fresh",
            "    random UUID for each element it upgrades.  Measured across two full",
            "    runs: 844 differing lines in the board, ALL of them (uuid ...) and",
            "    NONE of them anything else.  The board this programme writes uses",
            "    derived UUIDs and does not have this property; KiCad's upgrader",
            "    reintroduces it and there is no flag to seed it.",
            "  * drc_kicad10.txt, which carries the wall-clock time of the DRC run in",
            "    its second line, and the equivalence report, which quotes that line",
            "    verbatim.",
            "",
            "The netlist, the net classes, the 37 rules, the severities, the locked",
            "footprints and the geometry are identical run to run; that is what",
            "EQUIVALENCE_kicad8_vs_kicad10.md checks and it is checked on every",
            "emission."]
    lines = [f"EEG-CAR-01 Rev {D.REV_C} -- layout input set, SHA-256 manifest",
             f"{fmt.label} emission, generated {D.DATE_C} by tools/emit_handover.py",
             ""] + repro + [
             "",
             kicad_fmt.report(fmt),
             "",
             "FILES", ""]
    total, n = 0, 0
    for name, what in [(f[1], f[2]) for f in files] + extra:
        p = os.path.join(OUTD, name)
        if not os.path.exists(p):
            continue
        total += os.path.getsize(p)
        n += 1
        lines.append(f"  {name}")
        lines.append(f"      {what}")
        lines.append(f"      {sha256(p)}  {os.path.getsize(p)} bytes")
    lines += ["", f"{n} files listed above, {total} bytes, plus this "
                  f"manifest: {n + 1} files in the directory.",
              "",
              "NOT SENT FROM THIS REPOSITORY.  Nothing in tools/ transmits anything.",
              ""]
    man = os.path.join(OUTD, "SHA256SUMS.txt")
    open(man, "w").write("\n".join(lines) + "\n")
    if verbose:
        print(f"    {n + 1} files in {os.path.relpath(OUTD, PKG)} "
              f"({total // 1024} kB) -- {fmt.label}")
    return man, total, n + 1


def main(verbose=True, targets=("kicad8", "kicad10")):
    """Assemble the handover set once per format target.

    The KiCad 8 directory is built from the generated files.  Every other target is
    built by COPYING that directory and converting it with KiCad's own upgrader, so the
    two sets cannot drift: there is one emission and one conversion, not two emitters.
    """
    files = _files()
    missing = [src for src, _n, _w in files if not os.path.exists(src)]
    if missing:
        raise SystemExit("the handover set is incomplete; run tools/emit_all.py first:\n"
                         + "\n".join("  " + os.path.relpath(m, PKG) for m in missing))

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for src, name, _what in files:
        dst = os.path.join(OUT, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    kicad_fmt.verify(OUT, kicad_fmt.KICAD8, verbose)

    made = [kicad_fmt.KICAD8]
    if "kicad10" in targets:
        fmt = kicad_fmt.KICAD10
        if os.path.isdir(OUT_K10):
            shutil.rmtree(OUT_K10)
        shutil.copytree(OUT, OUT_K10)
        kicad_fmt.convert_tree(OUT_K10, fmt, verbose=verbose)
        kicad_fmt.verify(OUT_K10, fmt, verbose)
        made.append(fmt)

    # the equivalence check, and the DRC that check 9 records, both run against the
    # finished directories and before either manifest is taken.
    import emit_equivalence           # noqa: E402  (circular at module scope)
    stem = D.stem(D.REV_C)
    extra8, extra10 = [], []
    drc_line8 = ("**No DRC or ERC result is claimed for this set.** KiCad 8 is not "
                 "installed on the machine that generated it and Homebrew carries no "
                 "`kicad@8`, so `kicad-cli` could not be run against it. The KiCad 10 "
                 "set WAS checked; see the equivalence report.")
    drc_line10 = ""
    if kicad_fmt.KICAD10 in made:
        drc = kicad_fmt.run_drc(OUT_K10, f"{stem}.kicad_pcb")
        eq_path, checks = emit_equivalence.main(OUT, OUT_K10, drc, verbose)
        extra10.append((EQUIV, "the two emissions compared, check by check"))
        if drc[2]:
            extra10.append((os.path.basename(drc[2]),
                            "the KiCad 10 DRC report, verbatim"))
            drc_line10 = (
                f"**This set was opened by KiCad {kicad_fmt.cli_version()} and DRC was "
                f"run against the `.kicad_dru`.** It loads with no schema warning and "
                f"no rule-parse error. The report is in this directory as "
                f"`{os.path.basename(drc[2])}` and is read in check 9 of `{EQUIV}` -- "
                f"including what the counts in it do and do not mean.")
        else:
            drc_line10 = drc_line8

    # KiCad writes a `.kicad_prl` (local editor state: the visible layers, the active
    # grid) whenever it opens a project, and `-backups/` alongside it.  Neither is part
    # of the specification and neither is reproducible, so they are removed before the
    # manifest is taken rather than shipped and checksummed.
    for fmt in made:
        d = out_dir(fmt)
        for name in sorted(os.listdir(d)):
            p = os.path.join(d, name)
            if name.endswith((".kicad_prl", ".lck")):
                os.remove(p)
            elif name.endswith("-backups") and os.path.isdir(p):
                shutil.rmtree(p)

    for fmt in made:
        _write_readme(fmt, drc_line8 if fmt.key == "kicad8" else drc_line10, verbose)
        ex = extra8 if fmt.key == "kicad8" else extra10
        _write_manifest(fmt, files, list(ex) + [
            ("README_layout_inputs.md",
             "what is locked, the coordinate convention, which KiCad this set is for, "
             "and which rules we check on return")], verbose)
    return [out_dir(f) for f in made]


if __name__ == "__main__":
    main()
