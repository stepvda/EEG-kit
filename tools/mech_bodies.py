#!/usr/bin/env python3
"""
mech_bodies.py -- the 3D bodies the collision check of ECO-EEG-033 needs.

Finding 6 of ECO-EEG-030: there are no module outlines, so no placement can be shown to
be free of interference.  This module is the geometry; `tools/collision_check.py` is the
test.  Everything is in `design.py` coordinates -- top-left origin of the carrier, X
right, Y down -- with **Z measured upward from the carrier's top copper**, so the
carrier's own components occupy positive Z and MP-01's underside is at the standoff
height.

Three groups of bodies, and they are not equally well founded:

  1  **Carrier component envelopes**, one per footprint class, from the package
     datasheets.  These are heights above the board.  They are the only group taken
     from a datasheet rather than assumed.
  2  **MP-01, the four standoffs and the DevKit.**  MP-01's outline, thickness, DevKit
     opening and slot field are `tools/mech_gen.py`'s numbers, transcribed here because
     mech_gen cannot be imported without cadquery; ICD-EEG-006 section 4 carries the
     same set and is the document home.  The DevKit's PCB outline is Espressif's
     published 63.0 x 25.5 mm and its height above the carrier is ICD-EEG-006 section 4's
     13.6 mm, which that document marks *calculated*.
  3  **The twelve plate-mounted module assemblies.**  **NO VENDOR DRAWING WAS CONSULTED
     FOR ANY OF THEM.**  What is modelled is a DECLARED MAXIMUM ENVELOPE per module: the
     box the bought module must fit inside.  That turns twelve unknowns into twelve
     acceptance criteria -- ICD-EEG-006 section 6 step 9 already checks module height at
     qualification, and these give it a footprint to check as well.  Every one is
     registered in ASM-EEG-023 under MECH-D6-MODULE-ENVELOPES.  Two are better founded
     than the rest and say so: the PiEEG-8 is a Raspberry Pi shield, so its outline is
     the HAT mechanical standard, and the Pololu S13V15F5 is a catalogue 0.5 x 0.8 inch
     board.

Nothing here has been measured against a real part.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import fplib                # noqa: E402
import step_write as SW     # noqa: E402

# --------------------------------------------------------------------------- 1
# Height above the top copper, per footprint class, from the package datasheets.
COMPONENT_HEIGHT = {
    "R_0603_1608Metric": (0.95, "0603 chip, 0.80 mm body plus solder"),
    "C_0603_1608Metric": (0.95, "0603 chip, 0.80 mm body plus solder"),
    "L_0603_1608Metric": (0.95, "0603 chip, 0.80 mm body plus solder"),
    "R_1206_3216Metric": (1.20, "1206 PTC, 1.10 mm body plus solder"),
    "SOT-23": (1.45, "SOT-23 maximum seated height"),
    "SOT-23-5": (1.45, "SOT-23-5 maximum seated height"),
    "TSSOP-14_4.4x5mm_P0.65mm": (1.20, "TI PW package, 1.20 mm maximum"),
    "SOIC-14_3.9x8.7mm_P1.27mm": (1.75, "not used from Rev C; kept for Rev B"),
    "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical": (6.00, "JST PH vertical header"),
    "DIN42802_1p5mm_Socket": (10.00, "ASSUMED: no qualified part exists "
                                     "(AVL-EEG-017 section 1.4.1)"),
    "SW_PUSH_6mm_H7.3mm": (7.30, "Omron B3F-1052, projected plunger"),
    "TestPoint_Pad_D1.5mm": (0.00, "bare copper"),
    "Fiducial_1mm_Mask3mm": (0.00, "bare copper"),
    "MountingHole_3.2mm_M3": (0.00, "a hole"),
}
SOCKET_HEIGHT = (8.50, "2.54 mm socket strip, mating height (ICD-EEG-006 section 4)")

# --------------------------------------------------------------------------- 2
# MP-01, from tools/mech_gen.py and ICD-EEG-006 section 4.
PLATE_W, PLATE_H, PLATE_T = 146.0, 126.0, 3.0
PLATE_INSET = 2.0                    # 2 mm inside the carrier outline on every edge
STANDOFF_H = 18.0                    # M3 x 18 nylon, carrier top to plate underside
STANDOFF_AF = 5.5                    # hex across flats
DEVKIT_OPENING = (78.0, 4.0, 109.0, 65.0)      # carrier coordinates
SLOT_ORIGIN = (14.0, 12.0)
SLOT_PITCH = (16.0, 7.0)
SLOT_SIZE = (12.0, 3.0)
PLATE_BORDER = 8.0
MODULE_H_LIMIT = 18.0                # ICD-EEG-006 section 4 stack budget
MODULE_GAP = 1.0                     # clearance between two modules

DEVKIT = dict(w=63.0, h=25.5, z_top=13.6,
              why="Espressif ESP32-S3-DevKitC-1 published PCB outline; the 13.6 mm is "
                  "ICD-EEG-006 section 4's calculated stack of 8.5 mm socket mating, "
                  "1.6 mm PCB and about 3.5 mm of components")

# --------------------------------------------------------------------------- 3
# DECLARED MAXIMUM ENVELOPES.  Every one is a requirement on the bought module and not a
# measurement of one.  w x h is the plan footprint; z is the height above MP-01's top
# face, PCB and tallest component together.
MODULES = [
    # ref, connector, w, h, z, confidence, why
    ("M1a", "ADS1299 breakout #1", "J1/J2/J23", 65.0, 56.5, 15.0, "form factor",
     "PiEEG-8 is a Raspberry Pi shield, so the outline is the HAT mechanical "
     "standard 65.0 x 56.5 mm. The height is assumed."),
    ("M1b", "ADS1299 breakout #2", "J3/J4/J29", 65.0, 56.5, 15.0, "form factor",
     "as M1a; the type is specified once and fitted twice."),
    ("M3", "audio codec", "J8/J9", 40.0, 30.0, 12.0, "assumed",
     "OPEN WITH CRITERIA in AVL-EEG-017 section 2: no part is chosen, so this is the "
     "envelope a candidate must fit."),
    ("M4", "USB isolator", "J10", 65.0, 45.0, 15.0, "assumed",
     "Olimex USB-ISO presents a USB-B receptacle, which is the tallest thing on it. "
     "OPEN WITH CRITERIA and a live non-conformance (E-24 asks for USB-C)."),
    ("M5", "secure element", "J11", 30.0, 22.0, 8.0, "assumed",
     "Adafruit 4314 class STEMMA QT breakout."),
    ("M6", "charger", "J12", 40.0, 30.0, 10.0, "assumed",
     "Adafruit 4755 class. The baseline is ONE combined charger-plus-gauge assembly, "
     "in which case M6 and M7 are one body and this envelope covers both."),
    ("M7", "fuel gauge", "J12", 30.0, 22.0, 8.0, "assumed",
     "Adafruit 5580 class. Not fitted separately in the baseline; see M6."),
    ("M8", "buck-boost", "J25", 20.4, 12.8, 10.0, "form factor",
     "Pololu S13V15F5 is a catalogue 0.5 x 0.8 inch board. The height is assumed and "
     "is set by the inductor."),
    ("M9", "microSD breakout", "J20", 30.0, 22.0, 8.0, "assumed",
     "Adafruit 4682 class, 3 V only."),
    ("M10", "boom preamplifier", "J21", 30.0, 22.0, 10.0, "assumed",
     "OPEN WITH CRITERIA: the MAX9814 is NOT approved (AGC), and no fixed-gain part "
     "has been bought."),
    ("M11", "room microphone", "J28", 30.0, 22.0, 10.0, "assumed",
     "OPEN WITH CRITERIA: no catalogue part is known to meet E-15's hardware mute."),
    ("M12", "74HC595 shift register", "J19", 45.0, 25.0, 10.0, "assumed",
     "OPEN WITH CRITERIA. The controlled fallback is a 74HC595D on a SOIC-16-to-DIP "
     "adapter, which is smaller than this."),
]


# --------------------------------------------------------------------------- placement
def module_positions():
    """Where each module sits on MP-01, in carrier coordinates.

    MP-01 is deliberately not drilled to a pattern -- ICD-EEG-006 section 4 says so, and
    says a per-unit fitting decision is taken instead.  So there IS no module placement
    to transcribe, and one has to be proposed before anything can be checked for
    interference.  This is that proposal, and it is an assumption
    (ASM-EEG-023 MECH-D6-MODULE-ENVELOPES), not a transcription.

    The rule is simple and stated so a reviewer can disagree with it: take the modules
    largest first; for each, walk the M2.5 fixing grid; keep the free position whose
    centre is nearest the module's own carrier connector, so the jumper is short; skip
    any position that would overlap the DevKit opening, a standoff keep-out, the 8 mm
    solid border or a module already placed.
    """
    conn_xy = {}
    for _ref, _name, conns, *_rest in MODULES:
        first = conns.split("/")[0]
        c = D.C.get(first)
        conn_xy[_ref] = (c["x"], c["y"]) if c else (D.BOARD_W / 2, D.BOARD_H / 2)

    x0, y0 = SLOT_ORIGIN
    px, py = SLOT_PITCH
    cand = []
    for gy in range(0, 22):
        for gx in range(0, 14):
            cx = x0 + gx * px + 8.0
            cy = y0 + gy * py + 3.5
            cand.append((cx, cy))

    placed = {}
    taken = []
    for ref, name, conns, w, h, z, conf, why in sorted(
            MODULES, key=lambda m: -(m[3] * m[4])):
        tx, ty = conn_xy[ref]
        best = None
        for ww, hh in ((w, h), (h, w)):          # a module may be turned 90 degrees
            for cx, cy in sorted(cand,
                                 key=lambda p: (p[0] - tx) ** 2 + (p[1] - ty) ** 2):
                b = (cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2)
                if not _inside_plate(b):
                    continue
                if _overlaps(b, DEVKIT_OPENING, 2.0):
                    continue
                if any(_overlaps(b, (mx - 4.0, my - 4.0, mx + 4.0, my + 4.0), 0.0)
                       for mx, my in D.MOUNTING_HOLES):
                    continue
                if any(_overlaps(b, t, MODULE_GAP) for t in taken):
                    continue
                best = b
                break
            if best:
                break
        placed[ref] = best
        if best is not None:
            taken.append(best)
    return placed


def plate_area_budget():
    """Plan area, which nothing in the package has ever checked.

    ICD-EEG-006 section 4 budgets the module stack in HEIGHT and finds 6.4 mm of margin.
    It says nothing about area, and area is the binding constraint: the plate is
    146 x 126 mm, the slot field sits inside an 8 mm border, and the DevKit opening
    takes 31 x 61 mm out of the middle of it.
    """
    usable_w = PLATE_W - 2 * PLATE_BORDER
    usable_h = PLATE_H - 2 * PLATE_BORDER
    gross = usable_w * usable_h
    ox0, oy0, ox1, oy1 = DEVKIT_OPENING
    opening = (ox1 - ox0) * (oy1 - oy0)
    modules = sum(m[3] * m[4] for m in MODULES)
    return dict(usable=gross, opening=opening, net=gross - opening, modules=modules,
                fill=modules / (gross - opening))


def _inside_plate(b):
    px0 = PLATE_INSET + PLATE_BORDER
    py0 = PLATE_INSET + PLATE_BORDER
    px1 = D.BOARD_W - PLATE_INSET - PLATE_BORDER
    py1 = D.BOARD_H - PLATE_INSET - PLATE_BORDER
    return b[0] >= px0 and b[1] >= py0 and b[2] <= px1 and b[3] <= py1


def _overlaps(a, b, gap=0.0):
    return (a[0] < b[2] + gap and b[0] < a[2] + gap
            and a[1] < b[3] + gap and b[1] < a[3] + gap)


# --------------------------------------------------------------------------- bodies
def carrier_component_bodies(board):
    """[(ref, (x0, y0, x1, y1), z0, z1, why)] for every placed carrier part."""
    out = []
    for part in board.parts:
        fp = fplib.get(part.fpname)
        if part.fpname.startswith("PinSocket"):
            hz, why = SOCKET_HEIGHT
        else:
            hz, why = COMPONENT_HEIGHT.get(part.fpname, (2.0, "ASSUMED: no entry"))
        if hz <= 0.0:
            continue
        b = _fp_box(part, fp)
        out.append((part.ref, b, 0.0, hz, why))
    return out


def _fp_box(part, fp):
    xs, ys = [], []
    for seg in part.crtyd:
        xs += [seg[0], seg[2]]
        ys += [seg[1], seg[3]]
    if not xs:
        for pd in part.pads:
            w, h = pd.size_rot()
            xs += [pd.x - w / 2, pd.x + w / 2]
            ys += [pd.y - h / 2, pd.y + h / 2]
    return (min(xs), min(ys), max(xs), max(ys))


def plate_parts():
    """MP-01 as four rectangles around the DevKit opening, so that the solid needs no
    hole in a face -- see tools/step_write.py."""
    x0, y0 = PLATE_INSET, PLATE_INSET
    x1, y1 = D.BOARD_W - PLATE_INSET, D.BOARD_H - PLATE_INSET
    ox0, oy0, ox1, oy1 = DEVKIT_OPENING
    z0, z1 = STANDOFF_H, STANDOFF_H + PLATE_T
    return [(SW.box(x0, y0, x1, oy0), z0, z1),
            (SW.box(x0, oy1, x1, y1), z0, z1),
            (SW.box(x0, oy0, ox0, oy1), z0, z1),
            (SW.box(ox1, oy0, x1, oy1), z0, z1)]


def standoff_parts():
    out = []
    for mx, my in D.MOUNTING_HOLES:
        r = STANDOFF_AF / 2.0 / math.cos(math.pi / 6)     # across corners
        out.append((SW.ngon(mx, my, r, 6, math.pi / 6), 0.0, STANDOFF_H))
    return out


def devkit_body():
    ox0, oy0, ox1, oy1 = DEVKIT_OPENING
    cx = (D.C["J6"]["x"] + D.C["J7"]["x"]) / 2.0
    # J6 and J7 are 1x22 sockets running down the board from their origin
    cy = D.C["J6"]["y"] + 21 * 2.54 / 2.0
    w, h = DEVKIT["w"], DEVKIT["h"]
    # the DevKit's long axis runs along the sockets, which run in Y
    return (cx - h / 2.0, cy - w / 2.0, cx + h / 2.0, cy + w / 2.0), 0.0, DEVKIT["z_top"]


def module_bodies():
    """[(ref, name, box, z0, z1, confidence, why)] above MP-01."""
    pos = module_positions()
    z0 = STANDOFF_H + PLATE_T
    out = []
    for ref, name, conns, w, h, z, conf, why in MODULES:
        b = pos[ref]
        if b is None:
            out.append((ref, name, None, z0, z0 + z, conf, why))
        else:
            out.append((ref, name, b, z0, z0 + z, conf, why))
    return out


def write_footprint_models(outdir):
    """One STEP body per FOOTPRINT CLASS, for the board's 3D view.

    Bound into the `.kicad_pcb` so the contractor sees the board with bodies on it
    without importing anything.  Two conventions matter and are handled here rather than
    in an offset: a footprint's coordinates are X right and **Y DOWN**, and KiCad's 3D
    scene is **Y UP**, so the body is written with Y negated and the model is bound at
    offset (0, 0, 0).  A body is the footprint's own `body` extent extruded to the height
    in COMPONENT_HEIGHT, so it is the package outline and not the courtyard.
    """
    os.makedirs(outdir, exist_ok=True)
    made = {}
    for name in sorted(fplib.LIB):
        fp = fplib.get(name)
        if name.startswith("PinSocket"):
            hz, why = SOCKET_HEIGHT
        else:
            hz, why = COMPONENT_HEIGHT.get(name, (0.0, ""))
        if hz <= 0.0:
            continue
        x0, y0, x1, y1 = fp.body
        if x1 - x0 <= 0 or y1 - y0 <= 0:
            continue
        poly = SW.box(x0, -y1, x1, -y0)          # Y down -> Y up
        f = SW.StepFile(name, f"{fp.descr} -- body envelope {hz:.2f} mm tall ({why})",
                        date=D.DATE_C)
        safe = name.replace("/", "_")
        path = os.path.join(outdir, f"{safe}.step")
        f.write(path, [(safe, [(poly, 0.0, hz)])])
        ok, why2 = SW.check(path)
        if not ok:
            raise SystemExit(f"{safe}.step: {why2}")
        made[name] = path
    return made


def write_step(outdir):
    """Write the body set as STEP.  One file per group."""
    import pcbgen
    board = pcbgen.BoardV2()
    os.makedirs(outdir, exist_ok=True)
    made = []

    # the carrier as one solid plus its component envelopes
    solids = [("EEG-CAR-01_RevC_board",
               [(SW.box(0, 0, D.BOARD_W, D.BOARD_H), -1.6, 0.0)])]
    for ref, b, z0, z1, _why in carrier_component_bodies(board):
        solids.append((f"carrier_{ref}", [(SW.box(*b), z0, z1)]))
    f = SW.StepFile("EEG-CAR-01_RevC_carrier_with_component_envelopes",
                    "Carrier board and the height envelope of every placed part",
                    date=D.DATE_C)
    p = os.path.join(outdir, "EEG-CAR-01_RevC_carrier_envelopes.step")
    f.write(p, solids)
    made.append(p)

    f = SW.StepFile("MP-01_module_plate_and_standoffs",
                    "MP-01 plate with the DevKit opening, and the four M3 x 18 standoffs",
                    date=D.DATE_C)
    p = os.path.join(outdir, "MP-01_RevC_plate_and_standoffs.step")
    f.write(p, [("MP-01_module_plate", plate_parts()),
                ("standoffs_M3x18", standoff_parts())])
    made.append(p)

    b, z0, z1 = devkit_body()
    mods = [("ESP32-S3-DevKitC-1_body", [(SW.box(*b), z0, z1)])]
    for ref, name, mb, mz0, mz1, conf, why in module_bodies():
        if mb is None:
            continue
        mods.append((f"{ref}_{name.replace(' ', '_')}", [(SW.box(*mb), mz0, mz1)]))
    f = SW.StepFile("EEG-CAR-01_RevC_module_envelopes",
                    "DECLARED MAXIMUM envelopes of the thirteen module assemblies. "
                    "No vendor drawing was consulted. ASM-EEG-023 MECH-D6.",
                    date=D.DATE_C)
    p = os.path.join(outdir, "EEG-CAR-01_RevC_module_envelopes.step")
    f.write(p, mods)
    made.append(p)

    for path in made:
        ok, why = SW.check(path)
        if not ok:
            raise SystemExit(f"{os.path.basename(path)}: {why}")
    return made
