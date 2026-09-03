#!/usr/bin/env python3
"""
gerber.py -- Gerber X2, Excellon and IPC-D-356A output for EEG-CAR-01 Rev B.

Everything is written from the same geometry the DRC measured, so the fabrication data,
the drawings and the check report can never disagree.

Coordinates: Gerber and drill use a bottom-left origin with Y up, which is what every
fabricator's CAM expects.  The design file uses a top-left origin with Y down, so
gy = BOARD_H - y everywhere below.  This is stated in the layer-map README as well.

Format: 4.6 absolute, metric, leading zeros omitted (%FSLAX46Y46*%, %MOMM*%).

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import hashlib
import math
import os

import design as D
import pours
import strokefont

SCALE = 1_000_000          # 4.6 format
MASK_EXPANSION = 0.051     # per side, IPC-7351 nominal
# Stencil apertures, from ASM-EEG-007 section 2.3.  Keyed by the UNROTATED land size in
# the footprint's own frame, because the reductions the process specifies are per-axis in
# that frame and a rotated pad must reduce on the same physical edge.
#
# This table used to be a single scalar, PASTE_SHRINK = 0.0, so the paste layer was cut
# 1:1 with the copper lands and NO reduction was applied anywhere -- while ASM-EEG-007
# section 2.3 published a full aperture table with area ratios computed from it.  A
# stencil cut from the shipped Gerbers would have deposited more paste than the process
# was written for, and the heel-bridging reduction on the 1.27 mm SOIC-14 pitch, which is
# the tightest thing on the board, would not have been there at all.
#
#   land (w, h)   ->  aperture (w, h)          package                  rule
PASTE_APERTURE = {
    (0.800, 0.950): (0.720, 0.950),   # 0603 resistor / ferrite   10 % reduction in X
    (0.875, 0.950): (0.790, 0.950),   # 0603 capacitor            10 % reduction in X
    (1.125, 1.750): (1.030, 1.750),   # 1206 (F1)                  9 % reduction in X
    (1.025, 0.600): (0.950, 0.600),   # SOT-23                     7 % reduction in X
    (1.100, 0.600): (1.000, 0.600),   # SOT-23-5 (U7)              9 % reduction in X
    (1.950, 0.600): (1.850, 0.550),   # SOIC-14 1.27 mm pitch      both axes, heel bridging
}
PASTE_UNKNOWN = []          # lands with no rule; reported rather than silently cut 1:1


def _c(v):
    return int(round(v * SCALE))


def gy(y):
    return D.BOARD_H - y


class GerberFile:
    def __init__(self, path, function, polarity="Positive", title=""):
        self.path = path
        self.function = function
        self.polarity = polarity
        self.title = title
        self.apertures = {}
        self.body = []
        self._next = 10
        self._cur = None

    def aperture(self, spec, func=None):
        key = (spec, func)
        if key not in self.apertures:
            self.apertures[key] = self._next
            self._next += 1
        return self.apertures[key]

    def use(self, d):
        if self._cur != d:
            self.body.append(f"D{d}*")
            self._cur = d

    def flash(self, d, x, y):
        self.use(d)
        self.body.append(f"X{_c(x)}Y{_c(gy(y))}D03*")

    def line(self, d, x1, y1, x2, y2):
        self.use(d)
        self.body.append(f"X{_c(x1)}Y{_c(gy(y1))}D02*")
        self.body.append(f"X{_c(x2)}Y{_c(gy(y2))}D01*")

    def polyline(self, d, pts):
        if len(pts) < 2:
            return
        self.use(d)
        self.body.append(f"X{_c(pts[0][0])}Y{_c(gy(pts[0][1]))}D02*")
        for x, y in pts[1:]:
            self.body.append(f"X{_c(x)}Y{_c(gy(y))}D01*")

    def region(self, rings, clear=False):
        """rings: list of coordinate sequences; clear=True cuts a hole."""
        self.body.append("%LPC*%" if clear else "%LPD*%")
        for ring in rings:
            pts = list(ring)
            if pts[0] != pts[-1]:
                pts.append(pts[0])
            self.body.append("G36*")
            self.body.append(f"X{_c(pts[0][0])}Y{_c(gy(pts[0][1]))}D02*")
            for x, y in pts[1:]:
                self.body.append(f"X{_c(x)}Y{_c(gy(y))}D01*")
            self.body.append("G37*")
        if clear:
            self.body.append("%LPD*%")

    def write(self):
        out = ["%TF.GenerationSoftware,TI One Voice,package_v2.4/tools/gerber.py,1.0*%",
               f"%TF.CreationDate,{D.DATE}T00:00:00+01:00*%",
               f"%TF.ProjectId,{D.BOARD_NAME},"
               f"{hashlib.md5(D.BOARD_NAME.encode()).hexdigest()},{D.REV}*%",
               f"%TF.FileFunction,{self.function}*%",
               f"%TF.FilePolarity,{self.polarity}*%",
               "%TF.SameCoordinates,Original*%",
               "%FSLAX46Y46*%",
               "%MOMM*%",
               f"G04 {self.title}*",
               f"G04 EEG-CAR-01 Rev {D.REV} -- TI One Voice research programme*",
               "G04 Licence CC BY-SA 4.0*",
               "G01*",
               "G75*",
               "%LPD*%"]
        for (spec, func), d in sorted(self.apertures.items(), key=lambda kv: kv[1]):
            if func:
                out.append(f"%TA.AperFunction,{func}*%")
            out.append(f"%ADD{d}{spec}*%")
            if func:
                out.append("%TD*%")
        out += self.body
        out.append("M02*")
        with open(self.path, "w") as f:
            f.write("\n".join(out) + "\n")
        return self.path


# --------------------------------------------------------------------------- apertures
def pad_aperture(gf, pd, grow=0.0, func=None, size=None):
    w, h = pd.size_rot() if size is None else size
    w += 2 * grow
    h += 2 * grow
    if pd.shape == "circle":
        return gf.aperture(f"C,{w:.6f}", func)
    if pd.shape == "oval" and abs(w - h) > 1e-9:
        return gf.aperture(f"O,{w:.6f}X{h:.6f}", func)
    # An "oval" with equal sides is a round pad.  It used to fall through to the
    # rectangle branch below, so every through-hole header pin but pin 1 was
    # FABRICATED SQUARE while the KiCad file and fplib both call it round.
    if pd.shape == "oval":
        return gf.aperture(f"C,{w:.6f}", func)
    if pd.shape in ("rect", "roundrect"):
        return gf.aperture(f"R,{w:.6f}X{h:.6f}", func)
    return gf.aperture(f"C,{max(w, h):.6f}", func)


# --------------------------------------------------------------------------- layers
LAYER_FUNC = {"F.Cu": "L1,Top", "In1.Cu": "L2,Inr", "In2.Cu": "L3,Inr", "B.Cu": "L4,Bot"}


def copper_layer(path, layer, board, tracks, vias, pour_geo, silk_note=""):
    n = LAYER_FUNC[layer]
    gf = GerberFile(path, f"Copper,{n},Signal", title=f"{layer} copper")
    # pours first, so tracks and pads image over them
    for (lay, net), g in sorted(pour_geo.items()):
        if lay != layer:
            continue
        for poly in pours.polys(g):
            gf.region([list(poly.exterior.coords)])
            for ring in poly.interiors:
                gf.region([list(ring.coords)], clear=True)
    for t in tracks:
        if t.layer != layer:
            continue
        d = gf.aperture(f"C,{t.width:.6f}", "Conductor")
        gf.line(d, t.x1, t.y1, t.x2, t.y2)
    for pd in board.pads():
        if pd.kind == "np_thru_hole":
            continue
        if not pd.tht and not pd.on(layer):
            continue
        func = "ComponentPad" if pd.tht else "SMDPad,CuDef"
        gf.flash(pad_aperture(gf, pd, 0.0, func), pd.x, pd.y)
    for v in vias:
        d = gf.aperture(f"C,{v.pad:.6f}", "ViaPad")
        gf.flash(d, v.x, v.y)
    return gf.write()


def mask_layer(path, layer, board):
    side = "Top" if layer == "F.Cu" else "Bot"
    mlay = "F.Mask" if layer == "F.Cu" else "B.Mask"
    gf = GerberFile(path, f"Soldermask,{side}", polarity="Negative",
                    title=f"Solder mask {side} (vias tented, not opened)")
    for pd in board.pads():
        if pd.kind == "np_thru_hole":
            continue
        if not pd.tht and mlay in pd.layers and not pd.on(layer):
            # a mask-defined opening -- the fiducials' 3.0 mm aperture, which carries no
            # copper of its own.  It is drawn at its stated size, with no expansion.
            gf.flash(pad_aperture(gf, pd, 0.0), pd.x, pd.y)
            continue
        if not pd.tht and not pd.on(layer):
            continue
        gf.flash(pad_aperture(gf, pd, MASK_EXPANSION), pd.x, pd.y)
    return gf.write()


def paste_layer(path, layer, board):
    side = "Top" if layer == "F.Cu" else "Bot"
    play = "F.Paste" if layer == "F.Cu" else "B.Paste"
    gf = GerberFile(path, f"Paste,{side}", title=f"Solder paste {side} (stencil)")
    for pd in board.pads():
        if pd.tht or pd.kind == "np_thru_hole":
            continue
        # paste follows the pad's own paste layer, not its copper: a fiducial has copper
        # and mask but no paste, and gating on copper flashed paste onto all three
        if play not in pd.layers:
            continue
        key = (round(pd.w, 3), round(pd.h, 3))
        ap = PASTE_APERTURE.get(key)
        if ap is None:
            if key not in PASTE_UNKNOWN:
                PASTE_UNKNOWN.append(key)
            size = pd.size_rot()                      # no rule: cut 1:1 and report it
        else:
            # reduce in the footprint frame, then apply the pad's own rotation
            rot = getattr(pd, "rot", 0) or 0
            size = (ap[1], ap[0]) if round(rot / 90.0) % 2 else (ap[0], ap[1])
        gf.flash(pad_aperture(gf, pd, 0.0, size=size), pd.x, pd.y)
    return gf.write()


def silk_layer(path, layer, board, extra_text=()):
    side = "Top" if layer == "F.Cu" else "Bot"
    gf = GerberFile(path, f"Legend,{side}", title=f"Silkscreen {side}")
    if layer == "F.Cu":
        for p in board.parts:
            for x1, y1, x2, y2, w in p.silk:
                d = gf.aperture(f"C,{w:.6f}", "Material")
                gf.line(d, x1, y1, x2, y2)
        for p in board.parts:
            if p.fpname.startswith("MountingHole"):
                continue
            b = board.courtyard_box(p)
            h = 0.9 if (b[2] - b[0]) > 4 else 0.7
            tw = strokefont.text_width(p.ref, h)
            # put the reference above the part, or inside it when it is large
            tx = (b[0] + b[2]) / 2 - tw / 2
            ty = b[1] - 0.25
            if ty < 1.0:
                ty = b[3] + h + 0.25
            for pts, th in strokefont.text_strokes(p.ref, tx, D.BOARD_H - ty, h):
                d = gf.aperture(f"C,{th:.6f}", "Material")
                gf.polyline(d, [(x, D.BOARD_H - y) for x, y in pts])
    for (txt, x, y, h, mirror) in extra_text:
        for pts, th in strokefont.text_strokes(txt, x, D.BOARD_H - y, h, mirror=mirror):
            d = gf.aperture(f"C,{th:.6f}", "Material")
            gf.polyline(d, [(px, D.BOARD_H - py) for px, py in pts])
    return gf.write()


def edge_layer(path):
    gf = GerberFile(path, "Profile,NP", title="Board outline (profile is the centre line)")
    d = gf.aperture("C,0.100000", "Profile")
    W, H = D.BOARD_W, D.BOARD_H
    gf.polyline(d, [(0, 0), (W, 0), (W, H), (0, H), (0, 0)])
    return gf.write()


def fab_layer(path, board):
    gf = GerberFile(path, "Other,Fabrication", title="Fabrication drawing data (reference)")
    d = gf.aperture("C,0.100000")
    for p in board.parts:
        for x1, y1, x2, y2, w in p.fab:
            gf.line(d, x1, y1, x2, y2)
    gf.polyline(d, [(D.ZONE_SPLIT_X, 0), (D.ZONE_SPLIT_X, D.BOARD_H)])
    return gf.write()


# --------------------------------------------------------------------------- drill
def excellon(path, board, vias, plated=True):
    tools = {}
    holes = []
    for pd in board.pads():
        if plated and pd.kind != "thru_hole":
            continue
        if not plated and pd.kind != "np_thru_hole":
            continue
        tools.setdefault(round(pd.drill, 3), []).append((pd.x, pd.y))
    if plated:
        for v in vias:
            tools.setdefault(round(v.drill, 3), []).append((v.x, v.y))
    lines = ["M48",
             f"; {D.BOARD_NAME} Rev {D.REV} -- {'plated' if plated else 'non-plated'} holes",
             "; TI One Voice research programme, CC BY-SA 4.0",
             f"; generated {D.DATE} from package_v2.4/tools/design.py",
             "; sizes below are FINISHED hole diameters; add plating allowance for the tool",
             "FMAT,2",
             "METRIC,TZ",
             "; #@! TF.FileFunction,"
             + ("Plated,1,2,PTH" if plated else "NonPlated,1,2,NPTH")]
    for i, dia in enumerate(sorted(tools), start=1):
        lines.append(f"T{i:02d}C{dia:.3f}")
    lines += ["%", "G90", "G05"]
    for i, dia in enumerate(sorted(tools), start=1):
        lines.append(f"T{i:02d}")
        for x, y in sorted(tools[dia]):
            lines.append(f"X{x:.3f}Y{gy(y):.3f}")
    lines.append("M30")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path, {d: len(v) for d, v in sorted(tools.items())}


# --------------------------------------------------------------------------- IPC-D-356A
def ipc356(path, board, vias, netid):
    """Write the bare-board test netlist.

    IPC-D-356A is a FIXED-COLUMN format: a field is identified by where it starts, not by
    what separates it from its neighbour.  Two things were wrong with what this function
    used to emit, and the second is the one that would have silently mis-tested a board.

    1.  Units.  The header declares `P  UNITS CUST 0`, which is 0.0001 inch, and the
        coordinates and pad dimensions were written in those units -- but the drill
        diameter was written in MICROMETRES (`drill * 1000`).  A 0.30 mm hole came out as
        D0300, which a reader in customary units reads as 0.0300 inch = 0.762 mm.  Every
        hole in the file was overstated by a factor of 2.54.

    2.  Field widths.  The feature-dimension fields were written with six digits where the
        format allocates four, so every record ran to 82 or 83 columns instead of 80 and
        each field after the first overflow sat in the wrong place.

    The column map below is written into the file itself, as C-records, so that a CAM
    engineer can see exactly what was generated rather than having to infer it.

    HONESTY NOTE, and it matters for this file more than most: this output has never been
    read by a CAM or bare-board-test system.  The layout follows the format's published
    field allocation and the file is now internally consistent with the map it declares,
    but "internally consistent" is not "accepted by your tester".  The Gerbers and the
    drill files govern fabrication and are independent of this file; if your tool rejects
    this netlist, derive the netlist from those and tell us, because that is a defect here
    and not in the board.
    """
    lines = ["C  IPC-D-356A netlist for " + D.BOARD_NAME + " Rev " + D.REV,
             "C  TI One Voice research programme -- CC BY-SA 4.0",
             "C  units 0.0001 inch, board origin at the bottom-left corner",
             "C  ",
             "C  Column map of the 317/327 records in this file:",
             "C    1-3    record type: 317 through-hole, 327 SMD",
             "C    4-17   net name, 14 characters, left justified",
             "C    18-20  blank",
             "C    21-26  reference designator, 6 characters, left justified",
             "C    27     '-'",
             "C    28-31  pin number, 4 characters, left justified",
             "C    32     blank",
             "C    33-37  'D' + 4-digit drill diameter, 0.0001 inch (317 records only)",
             "C    38     'P' plated or 'U' unplated (317 records only)",
             "C    39-41  'A' + 2-digit access code (317 records only)",
             "C    42-49  'X' + signed 7-digit X coordinate",
             "C    50-57  'Y' + signed 7-digit Y coordinate",
             "C    58-62  'X' + 4-digit feature width",
             "C    63-67  'Y' + 4-digit feature height",
             "C    68-71  'R' + 3-digit rotation",
             "C    72     blank",
             "C    73-74  'S' + access code",
             "C  ",
             "C  A = access: 1 top, 2 bottom, 3 both",
             "P  UNITS CUST 0"]
    MM = 1 / 0.0254 * 10       # mm -> 0.0001 inch

    def xy(x, y):
        return f"X{int(round(x * MM)):+07d}Y{int(round(gy(y) * MM)):+07d}"

    def dim(w, h):
        """Feature size, 4 digits each, clamped to the width the format allows."""
        return f"X{min(9999, int(round(w * MM))):04d}Y{min(9999, int(round(h * MM))):04d}"

    def drill_field(d_mm, access):
        """'D' + 4-digit diameter in 0.0001 inch, plating flag, access code."""
        return f"D{min(9999, int(round(d_mm * MM))):04d}PA{access:02d}"

    def record(code, net, ref, pin, drill, x, y, w, h, access):
        r = (f"{code}{net[:14]:<14s}"                    # 1-17
             f"{'':3s}"                                  # 18-20
             f"{ref[:6]:<6s}-{str(pin)[:4]:<4s}"         # 21-31
             f"{'':1s}"                                  # 32
             f"{drill:<9s}"                              # 33-41
             f"{xy(x, y)}"                               # 42-57
             f"{dim(w, h)}"                              # 58-67
             f"R000"                                     # 68-71
             f" S{access}")                              # 72-74
        return r

    for pd in sorted(board.pads(), key=lambda p: (p.net, p.ref, str(p.num))):
        if not pd.net:
            continue
        w, h = pd.size_rot()
        access = 3 if pd.tht else (1 if pd.on("F.Cu") else 2)
        code = "317" if pd.tht else "327"
        drill = drill_field(pd.drill, access) if pd.tht else ""
        lines.append(record(code, pd.net, pd.ref, pd.num, drill,
                            pd.x, pd.y, w, h, access))
    for i, v in enumerate(vias):
        lines.append(record("317", v.net, "VIA", i, drill_field(v.drill, 3),
                            v.x, v.y, v.pad, v.pad, 3))
    lines.append("999")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


# --------------------------------------------------------------------------- CPL / BOM
def cpl(path, board, side="top"):
    rows = ["Designator,Val,Package,Mid X,Mid Y,Rotation,Layer"]
    for p in sorted(board.parts, key=lambda p: (p.ref[0], _num(p.ref))):
        if p.fpname.startswith("MountingHole") or p.fpname.startswith("TestPoint"):
            continue
        if p.is_tht:
            continue
        rows.append(f'"{p.ref}","{p.value}","{p.fpname}",'
                    f'{p.x:.4f},{gy(p.y):.4f},{p.rot:.1f},"Top"')
    with open(path, "w") as f:
        f.write("\n".join(rows) + "\n")
    return path


def cpl_tht(path, board):
    # Origin X/Y, not Mid X/Y: this is the footprint origin (pin 1 on the pin sockets),
    # Y up from the bottom-left board corner.  On a 1x22 socket it is 26.67 mm from the
    # part midpoint, so calling it a midpoint would misplace the part.
    rows = ["Designator,Val,Package,Origin X,Origin Y,Rotation,Layer,Process"]
    for p in sorted(board.parts, key=lambda p: (p.ref[0], _num(p.ref))):
        if not p.is_tht or p.fpname.startswith("MountingHole"):
            continue
        rows.append(f'"{p.ref}","{p.value}","{p.fpname}",'
                    f'{p.x:.4f},{gy(p.y):.4f},{p.rot:.1f},"Top","hand or selective solder"')
    with open(path, "w") as f:
        f.write("\n".join(rows) + "\n")
    return path


def bom(path, board):
    import collections
    groups = collections.OrderedDict()
    for p in sorted(board.parts, key=lambda p: (p.ref[0], _num(p.ref))):
        if p.fpname.startswith("MountingHole"):
            continue
        key = (p.value, p.fpname, p.mpn)
        groups.setdefault(key, []).append(p.ref)
    rows = ["Item,Qty,Designators,Value,Footprint,Manufacturer part number,"
            "Fit,Notes"]
    for i, ((val, fp, mpn), refs) in enumerate(groups.items(), start=1):
        if fp.startswith("TestPoint"):
            # bare copper: nothing is bought and nothing is placed, so it appears in no CPL
            fit = "fabricated feature -- not purchased, not placed"
        elif fp.startswith("Fiducial"):
            fit = "fabricated feature -- not purchased"
        else:
            fit = "DNP" if "DNP" in val else "fit"
        note = board.part(refs[0]).descr.replace('"', "'")
        rows.append(f'{i},{len(refs)},"{" ".join(refs)}","{val}","{fp}","{mpn}",'
                    f'"{fit}","{note}"')
    with open(path, "w") as f:
        f.write("\n".join(rows) + "\n")
    return path


def _num(ref):
    d = "".join(c for c in ref if c.isdigit())
    return int(d) if d else 0


# --------------------------------------------------------------------------- driver
def write_all(outdir, board, tracks, vias, pour_geo, netid):
    os.makedirs(outdir, exist_ok=True)
    B = D.BOARD_NAME
    made = []
    for lay, fname in (("F.Cu", "F_Cu"), ("In1.Cu", "In1_Cu"),
                       ("In2.Cu", "In2_Cu"), ("B.Cu", "B_Cu")):
        made.append(copper_layer(f"{outdir}/{B}-{fname}.gbr", lay, board, tracks, vias,
                                 pour_geo))
    made.append(mask_layer(f"{outdir}/{B}-F_Mask.gbr", "F.Cu", board))
    made.append(mask_layer(f"{outdir}/{B}-B_Mask.gbr", "B.Cu", board))
    made.append(paste_layer(f"{outdir}/{B}-F_Paste.gbr", "F.Cu", board))
    top_text = [
        (f"{B} REV {D.REV}", 62.0, 121.0, 1.6, False),
        ("TI ONE VOICE - RESEARCH INSTRUMENT", 62.0, 123.0, 1.0, False),
        ("NOT A MEDICAL DEVICE", 96.0, 121.0, 1.0, False),
        ("ANALOGUE", 34.0, 74.0, 1.2, False),
        ("DIGITAL", 90.0, 63.5, 1.2, False),
        ("ISOLATION KEEP-OUT - NO COPPER", 122.5, 3.0, 0.9, False),
        ("CC BY-SA 4.0", 96.0, 123.0, 1.0, False),
    ]
    bot_text = [
        (f"{B} REV {D.REV}", 62.0, 121.0, 1.6, True),
        ("ONE.WITYSK.ORG", 62.0, 123.0, 1.0, True),
        ("SN", 20.0, 121.0, 1.4, True),
    ]
    made.append(silk_layer(f"{outdir}/{B}-F_Silkscreen.gbr", "F.Cu", board, top_text))
    made.append(silk_layer(f"{outdir}/{B}-B_Silkscreen.gbr", "B.Cu", board, bot_text))
    made.append(edge_layer(f"{outdir}/{B}-Edge_Cuts.gbr"))
    made.append(fab_layer(f"{outdir}/{B}-User_Drawings.gbr", board))
    p1, t1 = excellon(f"{outdir}/{B}-PTH.drl", board, vias, plated=True)
    p2, t2 = excellon(f"{outdir}/{B}-NPTH.drl", board, vias, plated=False)
    made += [p1, p2]
    made.append(ipc356(f"{outdir}/{B}-IPC-D-356A.ipc", board, vias, netid))
    return made, t1, t2
