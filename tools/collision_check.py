#!/usr/bin/env python3
"""
collision_check.py -- does the stack fit?  Finding 6 of ECO-EEG-030.

Three cases, which is how the problem actually decomposes on this design, because the
modules do not plug into the carrier: twelve of the thirteen sit on the MP-01 plate on
four M3 x 18 standoffs and reach the carrier through ribbon jumpers, and the thirteenth,
the ESP32-S3-DevKitC-1, is inserted directly into J6 and J7 and stands up through an
opening in the plate.

  A  carrier parts against the plate underside -- is anything on the board taller than
     the standoff?
  B  the DevKit against the plate opening and against its neighbours on the carrier.
  C  the modules on top of the plate against each other, against the standoffs, and
     against the reach of their own jumpers.

  D  and one the brief did not ask for and the geometry insists on: PLAN AREA.  Nothing
     in this package has ever checked whether twelve modules fit on the plate at all.
     ICD-EEG-006 section 4 budgets the stack in HEIGHT and finds 6.4 mm of margin.

Bounding boxes, not meshes.  `trimesh` is installed here and would give mesh-accurate
interference, but every body in `tools/mech_bodies.py` IS a box or a prism, so a
box test is exact for them and a mesh test would only be slower and less legible.  What
would need a mesh is a real module with a connector overhanging its own PCB edge, and
there is no such model to test.

Writes mech/EEG-CAR-01_RevC_collision_check.txt.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import mech_bodies as MB    # noqa: E402
import pcbgen               # noqa: E402

OUT = os.path.join(PKG, "mech", "EEG-CAR-01_RevC_collision_check.txt")
JUMPER_LEN = 60.0            # ICD-EEG-006 section 3.2, "why 60 mm"


def _overlap(a, b):
    dx = min(a[2], b[2]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[1], b[1])
    return (dx, dy) if dx > 0 and dy > 0 else None


def case_a(board):
    """Carrier parts against the underside of MP-01."""
    findings, tallest = [], (None, 0.0, "")
    for ref, b, z0, z1, why in MB.carrier_component_bodies(board):
        if z1 > tallest[1]:
            tallest = (ref, z1, why)
        if z1 > MB.STANDOFF_H:
            findings.append(f"{ref} stands {z1:.2f} mm above the top copper and the "
                            f"plate underside is at {MB.STANDOFF_H:.1f} mm ({why})")
    return findings, tallest


def case_b(board):
    """The DevKit against the plate opening, and against its carrier neighbours."""
    findings = []
    box, z0, z1 = MB.devkit_body()
    ox0, oy0, ox1, oy1 = MB.DEVKIT_OPENING
    if not (box[0] >= ox0 and box[1] >= oy0 and box[2] <= ox1 and box[3] <= oy1):
        findings.append(
            f"the DevKit body ({box[0]:.1f}, {box[1]:.1f})-({box[2]:.1f}, {box[3]:.1f}) "
            f"is not inside the plate opening ({ox0:.1f}, {oy0:.1f})-({ox1:.1f}, "
            f"{oy1:.1f}); it would foul the plate")
    for ref, b, cz0, cz1, why in MB.carrier_component_bodies(board):
        if ref in ("J6", "J7"):
            continue
        ov = _overlap(box, b)
        if ov and cz1 > z0 + 1.6:
            findings.append(f"the DevKit body overlaps {ref} by {ov[0]:.2f} x "
                            f"{ov[1]:.2f} mm, and {ref} stands {cz1:.2f} mm")
        elif ov:
            findings.append(f"the DevKit body overlaps {ref} by {ov[0]:.2f} x "
                            f"{ov[1]:.2f} mm in plan (below the DevKit PCB, so it may "
                            f"be a clearance question rather than a collision)")
    clear = MB.DEVKIT["z_top"]
    if clear > MB.STANDOFF_H + MB.PLATE_T:
        findings.append(f"the DevKit stands {clear:.1f} mm and the plate's top face is "
                        f"at {MB.STANDOFF_H + MB.PLATE_T:.1f} mm, so it protrudes "
                        f"{clear - MB.STANDOFF_H - MB.PLATE_T:.1f} mm above the plate "
                        f"-- intended, its ports must be reachable")
    return findings, box, z1


def case_c():
    """Modules on the plate: against each other, the standoffs, and the jumper reach."""
    findings = []
    bodies = MB.module_bodies()
    pos = {r: b for r, _n, b, _z0, _z1, _c, _w in bodies}
    unplaced = [r for r, b in pos.items() if b is None]
    for r in unplaced:
        findings.append(f"{r} could not be placed on MP-01 at all")
    names = {m[0]: m[1] for m in MB.MODULES}
    refs = [r for r, b in pos.items() if b is not None]
    for i, ra in enumerate(refs):
        for rb in refs[i + 1:]:
            ov = _overlap(pos[ra], pos[rb])
            if ov:
                findings.append(f"{ra} ({names[ra]}) and {rb} ({names[rb]}) overlap by "
                                f"{ov[0]:.2f} x {ov[1]:.2f} mm")
        for k, (mx, my) in enumerate(D.MOUNTING_HOLES, start=1):
            so = (mx - MB.STANDOFF_AF / 2, my - MB.STANDOFF_AF / 2,
                  mx + MB.STANDOFF_AF / 2, my + MB.STANDOFF_AF / 2)
            if _overlap(pos[ra], so):
                findings.append(f"{ra} sits over the MH{k} standoff")
        if pos[ra][2] - pos[ra][0] > 0 and not MB._inside_plate(pos[ra]):
            findings.append(f"{ra} is outside the plate's 8 mm solid border")

    # Jumper reach.  The 60 mm of ICD-EEG-006 section 3.2 is a CROSSTALK limit and not
    # a mechanical one: coupling scales linearly with length and 120 mm puts a
    # neighbouring electrode artefact 6 dB above the front end's own noise floor.  It is
    # applied to every jumper so the assembler has one number.
    #
    # The model: from the nearest edge of the module to the carrier connector, Manhattan
    # because a ribbon runs in X and then in Y, plus the rise from the carrier's top
    # copper to the plate's top face.  Slack for the bend at each end is not added, so
    # this is a floor and not an estimate.
    rise = MB.STANDOFF_H + MB.PLATE_T
    reach = []
    for ref, name, conns, w, h, z, conf, why in MB.MODULES:
        first = conns.split("/")[0]
        c = D.C.get(first)
        if not c:
            continue
        b = pos.get(ref)
        run = _run(b, c, rise) if b else None
        best = _best_case_run(w, h, c, rise)
        reach.append((ref, first, run, best))
        if best is None:
            findings.append(
                f"{ref} has NO position on the plate at all: no grid position leaves a "
                f"{w:.0f} x {h:.0f} mm module inside the 8 mm border and clear of the "
                f"DevKit opening, with the plate otherwise empty. This does not depend "
                f"on the proposed placement.")
        elif best > JUMPER_LEN:
            findings.append(
                f"{ref} cannot reach {first} in {JUMPER_LEN:.0f} mm from ANY position "
                f"on the plate: the best case is about {best:.0f} mm. This does not "
                f"depend on the proposed placement.")
        elif run is not None and run > JUMPER_LEN:
            findings.append(
                f"{ref} to {first} is about {run:.0f} mm of jumper run against the "
                f"{JUMPER_LEN:.0f} mm of ICD-EEG-006 section 3.2, at the proposed "
                f"placement; {best:.0f} mm is reachable if the plate were free")
    return findings, bodies, reach


def _run(b, c, rise):
    dx = max(0.0, max(b[0] - c["x"], c["x"] - b[2]))
    dy = max(0.0, max(b[1] - c["y"], c["y"] - b[3]))
    return dx + dy + rise


def _best_case_run(w, h, c, rise):
    """The shortest jumper this module could have if the plate were empty."""
    best = None
    x0, y0 = MB.SLOT_ORIGIN
    px, py = MB.SLOT_PITCH
    for ww, hh in ((w, h), (h, w)):
        for gy in range(0, 22):
            for gx in range(0, 14):
                cx = x0 + gx * px + 8.0
                cy = y0 + gy * py + 3.5
                b = (cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2)
                if not MB._inside_plate(b):
                    continue
                if MB._overlaps(b, MB.DEVKIT_OPENING, 2.0):
                    continue
                r = _run(b, c, rise)
                best = r if best is None else min(best, r)
    return best


def case_d():
    """Plan area.  Nothing has ever checked it."""
    b = MB.plate_area_budget()
    findings = []
    if b["modules"] > b["net"]:
        findings.append(
            f"the twelve declared module envelopes need {b['modules']:.0f} mm2 and the "
            f"plate offers {b['net']:.0f} mm2 inside its 8 mm border and clear of the "
            f"DevKit opening: {b['fill'] * 100:.0f} % fill. No arrangement fits.")
    return findings, b


def main(verbose=True):
    board = pcbgen.BoardV2()
    fa, tallest = case_a(board)
    fb, dk_box, dk_z = case_b(board)
    fc, bodies, reach = case_c()
    fd, area = case_d()
    total = len(fa) + len(fb) + len(fc) + len(fd)

    L = ["EEG-CAR-01 Rev C -- 3D collision check",
         f"Generated {D.DATE_C} by tools/collision_check.py.", "=" * 78, "",
         "WHAT THIS IS",
         "  Finding 6 of ECO-EEG-030: no module outlines exist, so no placement could",
         "  be shown to be free of interference.  These are bounding-box tests over the",
         "  bodies of tools/mech_bodies.py.  Coordinates are design.py's -- top-left",
         "  origin, Y down -- with Z measured upward from the carrier's top copper.",
         "",
         "  **The twelve module envelopes are DECLARED MAXIMA and not measurements.**",
         "  No vendor drawing was consulted for any of them.  They are the boxes a",
         "  bought module must fit inside, registered in ASM-EEG-023 under",
         "  MECH-D6-MODULE-ENVELOPES.  Two are better founded than the rest: the",
         "  PiEEG-8 is a Raspberry Pi shield, so 65.0 x 56.5 mm is the HAT mechanical",
         "  standard, and the Pololu S13V15F5 is a catalogue 0.5 x 0.8 inch board.",
         "",
         "  The module placement on MP-01 is also a proposal.  ICD-EEG-006 section 4",
         "  deliberately does not drill the plate to a pattern and takes a per-unit",
         "  fitting decision instead, so there is no placement to transcribe.",
         "",
         f"FINDINGS: {total}", "",
         "A  CARRIER PARTS AGAINST THE PLATE UNDERSIDE",
         f"   plate underside at {MB.STANDOFF_H:.1f} mm on M3 x 18 nylon standoffs",
         f"   tallest carrier part: {tallest[0]} at {tallest[1]:.2f} mm ({tallest[2]})",
         f"   clearance to the plate: {MB.STANDOFF_H - tallest[1]:.2f} mm",
         f"   findings: {len(fa)}"]
    L += [f"     {x}" for x in fa] or ["     none"]
    L += ["",
          "B  THE DEVKIT AGAINST THE PLATE OPENING AND ITS NEIGHBOURS",
          f"   DevKit body ({dk_box[0]:.1f}, {dk_box[1]:.1f})-({dk_box[2]:.1f}, "
          f"{dk_box[3]:.1f}), {dk_z:.1f} mm tall",
          f"   plate opening {MB.DEVKIT_OPENING}",
          f"   findings: {len(fb)}"]
    L += [f"     {x}" for x in fb] or ["     none"]
    L += ["",
          "C  MODULES ON THE PLATE",
          f"   {sum(1 for _r, _n, b, *_ in bodies if b is not None)} of "
          f"{len(bodies)} placed",
          f"   findings: {len(fc)}"]
    L += [f"     {x}" for x in fc] or ["     none"]
    if reach:
        L += ["", "   Jumper run: nearest module edge to the carrier connector,",
              "   Manhattan, plus the 21.0 mm rise to the plate's top face. No bend",
              "   slack is added, so these are floors.  'best' is the shortest that",
              "   module could have with the plate to itself, which does not depend on",
              "   the proposed placement.",
              "",
              f"     {'module':6s} {'connector':10s} {'proposed':>9s} {'best':>7s}"]
        for ref, conn, run, best in sorted(reach,
                                           key=lambda r: -(r[3] if r[3] else 1e9)):
            rs = f"{run:5.0f} mm" if run is not None else "not placed"
            bs = f"{best:5.0f} mm" if best is not None else " no position"
            L.append(f"     {ref:6s} {conn:10s} {rs:>10s} {bs:>12s}"
                     + ("   OVER" if best is None or best > JUMPER_LEN else ""))
    L += ["",
          "D  PLAN AREA -- NOT ASKED FOR, AND IT IS THE BINDING CONSTRAINT",
          f"   plate {MB.PLATE_W:.0f} x {MB.PLATE_H:.0f} mm, "
          f"{MB.PLATE_BORDER:.0f} mm solid border",
          f"   usable inside the border          {area['usable']:8.0f} mm2",
          f"   less the DevKit opening           {area['opening']:8.0f} mm2",
          f"   net usable                        {area['net']:8.0f} mm2",
          f"   twelve declared module envelopes  {area['modules']:8.0f} mm2",
          f"   fill                              {area['fill'] * 100:8.0f} %",
          f"   findings: {len(fd)}"]
    L += [f"     {x}" for x in fd] or ["     none"]
    L += ["",
          "   Sensitivity, because the envelopes are assumptions and the conclusion",
          "   must not rest on them: the two ADS1299 boards alone are "
          f"{2 * 65.0 * 56.5:.0f} mm2,",
          f"   which is {2 * 65.0 * 56.5 / area['net'] * 100:.0f} % of the net usable "
          f"plate, and that figure is the",
          "   Raspberry Pi HAT standard rather than an assumption.  Halving every",
          "   OTHER envelope still leaves "
          f"{(area['modules'] - 2 * 65.0 * 56.5) / 2 + 2 * 65.0 * 56.5:.0f} mm2 against "
          f"{area['net']:.0f} mm2.",
          "",
          "WHAT IS NOT CHECKED HERE",
          "  Anything needing a real module: a connector overhanging a PCB edge, a",
          "  heatsink, a cable bend radius, or the pod lid.  Nothing in this package",
          "  has been manufactured or measured.",
          ""]
    text = "\n".join(L) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(text)
    if verbose:
        print(text)
    return total, OUT


if __name__ == "__main__":
    n, _ = main()
    sys.exit(0)
