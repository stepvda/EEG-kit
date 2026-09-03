#!/usr/bin/env python3
"""
drawings.py -- fabrication, assembly, drill and stack-up drawings for EEG-CAR-01 Rev B.

All drawn from the same geometry as the Gerbers, at 1:1 on A3, so a CAM operator and an
assembler are looking at the data they are given rather than at a picture of it.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import collections
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Circle, Polygon as MplPoly
import numpy as np

import design as D
import pours
import sym as S

A3 = (420.0, 297.0)
DRILL_SYMBOLS = ["o", "s", "^", "D", "v", "P", "X", "*", "h", "<", ">", "p"]


def _sheet(title, subtitle, sheet_no, scale=1.0):
    fig, ax = S.sheet(A3[0], A3[1], title, subtitle, sheet_no, D.REV, D.DATE)
    return fig, ax


def _board_axes(ax, ox, oy, sc=1.0, mirror=False):
    """Return a transform from board mm to sheet mm.

    mirror=True flips X so the board is drawn AS SEEN FROM UNDERNEATH -- the view an
    operator has when soldering the through-hole joints, which ASM-EEG-007 section 2.7
    does from the bottom.  Package v1 shipped a separate mirrored placement_bottom.pdf;
    without the flip a "bottom" sheet is just the top view with a different title, and
    every left-right instruction on it is wrong.
    """
    def T(x, y):
        xx = (D.BOARD_W - x) if mirror else x
        return (ox + xx * sc, oy + (D.BOARD_H - y) * sc)
    return T


def _outline(ax, T, lw=1.2):
    pts = [T(0, 0), T(D.BOARD_W, 0), T(D.BOARD_W, D.BOARD_H), T(0, D.BOARD_H), T(0, 0)]
    S.wire(ax, pts, lw=lw)


def _dim(ax, p1, p2, text, off=6.0, horiz=True):
    if horiz:
        y = min(p1[1], p2[1]) - off
        S.wire(ax, [(p1[0], p1[1]), (p1[0], y - 1.5)], lw=0.4, color="#8fa0ad")
        S.wire(ax, [(p2[0], p2[1]), (p2[0], y - 1.5)], lw=0.4, color="#8fa0ad")
        S.wire(ax, [(p1[0], y), (p2[0], y)], lw=0.6)
        S.label(ax, (p1[0] + p2[0]) / 2, y + 1.2, text, 5.4, ha="center", va="bottom")
    else:
        x = max(p1[0], p2[0]) + off
        S.wire(ax, [(p1[0], p1[1]), (x + 1.5, p1[1])], lw=0.4, color="#8fa0ad")
        S.wire(ax, [(p2[0], p2[1]), (x + 1.5, p2[1])], lw=0.4, color="#8fa0ad")
        S.wire(ax, [(x, p1[1]), (x, p2[1])], lw=0.6)
        S.label(ax, x + 1.2, (p1[1] + p2[1]) / 2, text, 5.4, ha="left", va="center", rot=90)


# --------------------------------------------------------------------------- fab drawing
def fabrication(pdf, board, vias, png_dir=None):
    fig, ax = _sheet("EEG-CAR-01 -- fabrication drawing",
                     f"4 layers, {D.BOARD_W:.1f} x {D.BOARD_H:.1f} mm, 1.60 mm FR-4, ENIG.  Scale 1:1 on A3.",
                     "FAB 1 of 2")
    T = _board_axes(ax, 22, 156)
    _outline(ax, T)
    # drill map
    tools = collections.defaultdict(list)
    for pd in board.pads():
        if pd.kind == "thru_hole":
            tools[round(pd.drill, 2)].append((pd.x, pd.y, True))
        elif pd.kind == "np_thru_hole":
            tools[round(pd.drill, 2)].append((pd.x, pd.y, False))
    for v in vias:
        tools[round(v.drill, 2)].append((v.x, v.y, True))
    order = sorted(tools)
    for i, dia in enumerate(order):
        m = DRILL_SYMBOLS[i % len(DRILL_SYMBOLS)]
        xs = [T(x, y)[0] for x, y, _ in tools[dia]]
        ys = [T(x, y)[1] for x, y, _ in tools[dia]]
        ax.plot(xs, ys, m, ms=1.9, mfc="none", mec="#12212e", mew=0.35, ls="none",
                zorder=4)
    S.wire(ax, [T(D.ZONE_SPLIT_X, 0), T(D.ZONE_SPLIT_X, D.BOARD_H)], lw=0.5, ls="--",
           color="#b23b2e")
    S.label(ax, *T(D.ZONE_SPLIT_X - 1, 6), "ANALOGUE", 5.0, ha="right", color="#b23b2e")
    S.label(ax, *T(D.ZONE_SPLIT_X + 1, 6), "DIGITAL", 5.0, ha="left", color="#b23b2e")
    ib = (141.0, 2.0, D.BOARD_W, 22.0)
    ax.add_patch(Rectangle(T(ib[0], ib[3]), (ib[2] - ib[0]), (ib[3] - ib[1]),
                           fc="#fdeaea", ec="#c0392b", lw=0.6, ls="--", zorder=1))
    S.label(ax, *T(142.0, 12.0), "ISOLATION\nKEEP-OUT\nNO COPPER", 4.4, color="#c0392b",
            va="center")
    for i, (x, y) in enumerate([(5.0, 5.0), (D.BOARD_W - 5, 5.0), (5.0, D.BOARD_H - 5),
                               (D.BOARD_W - 5, D.BOARD_H - 5)]):
        cx, cy = T(x, y)
        ax.add_patch(Circle((cx, cy), 3.0, fc="none", ec="#12212e", lw=0.6, zorder=5))
        ax.add_patch(Circle((cx, cy), 1.6, fc="none", ec="#12212e", lw=0.5, zorder=5))
        S.label(ax, cx + 4, cy + 4, f"MH{i+1}", 4.6)
    _dim(ax, T(0, D.BOARD_H), T(D.BOARD_W, D.BOARD_H), f"{D.BOARD_W:.2f} +/- 0.10", 8)
    _dim(ax, T(D.BOARD_W, 0), T(D.BOARD_W, D.BOARD_H), f"{D.BOARD_H:.2f} +/- 0.10", 8,
         horiz=False)
    _dim(ax, T(0, 5), T(5, 5), "5.00", 4)
    _dim(ax, T(D.BOARD_W - 5, D.BOARD_H), T(D.BOARD_W, D.BOARD_H), "5.00", 22)

    # drill table
    tx, ty = 22, 130
    S.label(ax, tx, ty, "DRILL SCHEDULE  (finished hole sizes)", 6.4, weight="bold")
    S.wire(ax, [(tx - 2, ty - 3), (tx + 150, ty - 3)], lw=0.8)
    S.label(ax, tx, ty - 7, "sym", 5.4, weight="bold")
    S.label(ax, tx + 14, ty - 7, "dia mm", 5.4, weight="bold")
    S.label(ax, tx + 38, ty - 7, "qty", 5.4, weight="bold")
    S.label(ax, tx + 54, ty - 7, "plated", 5.4, weight="bold")
    S.label(ax, tx + 76, ty - 7, "used for", 5.4, weight="bold")
    use = {0.3: "through vias", 0.9: "J13 / J24 JST PH", 1.0: "2.54 mm socket strips",
           1.2: "SW1-SW3 tactile switches", 1.5: "DIN 42802 retention posts (NPTH)",
           1.7: "J15-J17 DIN 42802 signal pin", 3.2: "M3 mounting holes (NPTH)"}
    for i, dia in enumerate(order):
        yy = ty - 12 - i * 5.4
        m = DRILL_SYMBOLS[i % len(DRILL_SYMBOLS)]
        ax.plot([tx + 2], [yy], m, ms=2.6, mfc="none", mec="#12212e", mew=0.5)
        plated = tools[dia][0][2]
        S.label(ax, tx + 14, yy, f"{dia:.2f}", 5.4)
        S.label(ax, tx + 38, yy, f"{len(tools[dia])}", 5.4)
        S.label(ax, tx + 54, yy, "PTH" if plated else "NPTH", 5.4,
                color="#12212e" if plated else "#c0392b")
        S.label(ax, tx + 76, yy, use.get(dia, ""), 5.4, color="#4a5c68")
    total = sum(len(v) for v in tools.values())
    S.label(ax, tx, ty - 12 - len(order) * 5.4 - 4,
            f"{total} holes in total.  Tolerance +/-0.08 mm on plated, "
            f"+/-0.05 mm on non-plated.", 5.4, color="#4a5c68")

    nx, ny = 200, 130
    S.label(ax, nx, ny, "FABRICATION NOTES", 6.6, weight="bold")
    for i, ln in enumerate(D.NOTES["fabrication"]):
        S.label(ax, nx, ny - 6 - i * 4.6, ln, 5.2)
    S.label(ax, nx, ny - 6 - len(D.NOTES["fabrication"]) * 4.6 - 6, "STACK-UP", 6.6,
            weight="bold")
    sy = ny - 6 - len(D.NOTES["fabrication"]) * 4.6 - 14
    layers = [("solder mask, LPI green", 1.0, "#1b7a4b"),
              ("L1  F.Cu   signal, 1 oz (35 um) + ENIG", 2.0, "#c98b2e"),
              ("prepreg 0.200 mm", 3.0, "#e6dcc8"),
              ("L2  In1.Cu reference plane, 0.5 oz (17 um)", 1.4, "#c98b2e"),
              ("core 1.065 mm, FR-4 Tg >= 150 C", 9.0, "#ddd0b4"),
              ("L3  In2.Cu reference plane, 0.5 oz (17 um)", 1.4, "#c98b2e"),
              ("prepreg 0.200 mm", 3.0, "#e6dcc8"),
              ("L4  B.Cu   signal, 1 oz (35 um) + ENIG", 2.0, "#c98b2e"),
              ("solder mask, LPI green", 1.0, "#1b7a4b")]
    yy = sy
    for name, th, col in layers:
        ax.add_patch(Rectangle((nx, yy - th), 70, th, fc=col, ec="#12212e", lw=0.4))
        S.label(ax, nx + 74, yy - th / 2, name, 5.2, va="center")
        yy -= th
    S.label(ax, nx, yy - 5, "Total 1.60 mm +/- 10 %.  Symmetric stack, so the board "
                            "should not bow.  Through vias only:\nno blind or buried vias, "
                            "no back-drill, no via-in-pad, no filled or plugged vias.", 5.2,
            color="#4a5c68")
    _out(pdf, png_dir, fig, "fab_drawing")


def drill_map(pdf, board, vias, png_dir=None):
    fig, ax = _sheet("EEG-CAR-01 -- drill map and hole detail",
                     "Plated and non-plated holes shown separately", "FAB 2 of 2")
    for k, (title, plated, ox) in enumerate([("PLATED (PTH)", True, 22),
                                             ("NON-PLATED (NPTH)", False, 224)]):
        T = _board_axes(ax, ox, 138, 1.25)
        _outline(ax, T, lw=0.9)
        S.label(ax, ox, 288, title, 7.0, weight="bold")
        tools = collections.defaultdict(list)
        for pd in board.pads():
            if plated and pd.kind == "thru_hole":
                tools[round(pd.drill, 2)].append((pd.x, pd.y))
            if not plated and pd.kind == "np_thru_hole":
                tools[round(pd.drill, 2)].append((pd.x, pd.y))
        if plated:
            for v in vias:
                tools[round(v.drill, 2)].append((v.x, v.y))
        for i, dia in enumerate(sorted(tools)):
            m = DRILL_SYMBOLS[i % len(DRILL_SYMBOLS)]
            xs = [T(x, y)[0] for x, y in tools[dia]]
            ys = [T(x, y)[1] for x, y in tools[dia]]
            ax.plot(xs, ys, m, ms=2.4, mfc="none", mec="#12212e", mew=0.4, ls="none")
            S.label(ax, ox, 282 - i * 5.2 - 6, f"{m}   {dia:.2f} mm   x{len(tools[dia])}",
                    5.4)
        if not plated:
            for pd in board.pads():
                if pd.kind != "np_thru_hole":
                    continue
                cx, cy = T(pd.x, pd.y)
                ax.add_patch(Circle((cx, cy), 2.0 * 1.35 if pd.drill > 2.5 else 1.0 * 1.35,
                                    fc="none", ec="#c0392b", lw=0.5, ls="--"))
    S.label(ax, 22, 46,
            "NON-PLATED HOLES CARRY NO COPPER AND NO SOLDER-MASK OPENING.\n"
            "The four 3.2 mm holes are M3 mounting holes with a 6.0 mm diameter copper "
            "keep-out on both layers.\n"
            "The six 1.5 mm holes are the retention posts of the DIN 42802 sockets "
            "J15-J17 and need only a 1.10 mm copper gap.\n"
            "Both sets are supplied in EEG-CAR-01-NPTH.drl and must NOT be merged into "
            "the plated file.", 6.0, color="#c0392b")
    _out(pdf, png_dir, fig, "drill_map")


# --------------------------------------------------------------------------- assembly
def assembly(pdf, board, png_dir=None, side="top"):
    bottom = (side == "bottom")
    fig, ax = _sheet(
        f"EEG-CAR-01 -- assembly drawing, {side} side",
        ("Reference designators and orientation.  Scale 1:1 on A3.  "
         "MIRRORED -- drawn as seen from underneath, the soldering view."
         if bottom else
         "Reference designators and orientation.  Scale 1:1 on A3.  "
         "Component side, as seen from above."),
        "ASM 1 of 2" if side == "top" else "ASM 2 of 2")
    T = _board_axes(ax, 22, 156, mirror=bottom)
    _outline(ax, T)
    for p in board.parts:
        b = board.courtyard_box(p)
        x0, y0 = T(b[0], b[3])
        ax.add_patch(Rectangle((x0, y0), b[2] - b[0], b[3] - b[1], fc="#f2f5f8",
                               ec="#7d92a3", lw=0.35, zorder=2))
        for pd in p.pads:
            w, h = pd.size_rot()
            px, py = T(pd.x, pd.y)
            if pd.shape == "circle" or pd.kind == "np_thru_hole":
                ax.add_patch(Circle((px, py), w / 2, fc="#c9d4dd", ec="none", zorder=3))
            else:
                ax.add_patch(Rectangle((px - w / 2, py - h / 2), w, h, fc="#c9d4dd",
                                       ec="none", zorder=3))
            if pd.drill:
                ax.add_patch(Circle((px, py), pd.drill / 2, fc="white", ec="none", zorder=4))
            if str(pd.num) == "1":
                ax.add_patch(Circle((px, py), 1.1, fc="none", ec="#c0392b", lw=0.5,
                                    zorder=5))
        cx, cy = T((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        dnp = "DNP" in p.value
        S.label(ax, cx, cy, p.ref, 3.6, ha="center", va="center",
                color="#c0392b" if dnp else "#12212e")
    S.label(ax, 22, 140, "ASSEMBLY NOTES", 6.6, weight="bold")
    for i, ln in enumerate(D.NOTES["assembly"]):
        S.label(ax, 22, 134 - i * 4.6, ln, 5.2)
    y = 134 - len(D.NOTES["assembly"]) * 4.6 - 6
    S.label(ax, 22, y, "PIN 1 IS RINGED IN RED ON EVERY POLARISED PART.", 5.6,
            color="#c0392b")
    dnps = [p.ref for p in board.parts if "DNP" in p.value]
    S.label(ax, 22, y - 6, f"DO NOT POPULATE: {', '.join(dnps) if dnps else 'none'}",
            5.6, color="#c0392b")
    if bottom:
        S.label(ax, 22, y - 12, "THIS SHEET IS MIRRORED. It is the view from UNDER the "
                                "board, which is how the through-hole joints are "
                                "soldered (ASM-EEG-007 section 2.7). Left and right are "
                                "reversed against the top sheet. NO PART IS FITTED ON "
                                "THIS SIDE -- the designators are shown so that a joint "
                                "can be found from underneath.", 5.4, color="#c0392b")
    else:
        S.label(ax, 22, y - 12, "PROCESS: SMT reflow on the top side, then through-hole "
                                "inserted from the top and soldered from the bottom. "
                                "All parts are on the top side; the bottom side carries "
                                "copper and legend only. The solder-side view is ASM 2 "
                                "of 2 and it is MIRRORED.", 5.4)
    S.label(ax, 230, 140, "GPIO AND MODULE NOTES", 6.6, weight="bold")
    for i, ln in enumerate(D.NOTES["gpio"]):
        S.label(ax, 230, 134 - i * 4.6, ln, 5.2)
    S.label(ax, 230, 134 - len(D.NOTES["gpio"]) * 4.6 - 6, "SAFETY NOTES", 6.6,
            weight="bold")
    for i, ln in enumerate(D.NOTES["safety"]):
        S.label(ax, 230, 134 - len(D.NOTES["gpio"]) * 4.6 - 12 - i * 4.6, ln, 5.2,
                color="#c0392b")
    _out(pdf, png_dir, fig, f"assembly_{side}")


# --------------------------------------------------------------------------- copper views
LAYER_ORDER = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")
LAYER_ROLE = {"F.Cu": "L1, signal, component side",
              "In1.Cu": "L2, reference plane (AGND_REF left of x = 62, DGND right)",
              "In2.Cu": "L3, reference plane (AGND_REF left of x = 62, DGND right)",
              "B.Cu": "L4, signal, solder side"}


def copper_view(pdf, board, tracks, vias, pour_geo, layer, png_dir=None):
    side = LAYER_ROLE[layer]
    fig, ax = _sheet(f"EEG-CAR-01 -- {layer} copper",
                     f"{side}.  Viewed from the top.  Scale 1:1 on A3.",
                     f"CU {LAYER_ORDER.index(layer) + 1} of 4")
    T = _board_axes(ax, 22, 156)
    ax.add_patch(Rectangle(T(0, D.BOARD_H), D.BOARD_W, D.BOARD_H, fc="#0f2a1c",
                           ec="#12212e", lw=1.0, zorder=1))
    for (lay, net), g in pour_geo.items():
        if lay != layer:
            continue
        for poly in pours.polys(g):
            ax.add_patch(MplPoly([T(x, y) for x, y in poly.exterior.coords], closed=True,
                                 fc="#1f7a4e", ec="none", zorder=2))
            for ring in poly.interiors:
                ax.add_patch(MplPoly([T(x, y) for x, y in ring.coords], closed=True,
                                     fc="#0f2a1c", ec="none", zorder=3))
    for t in tracks:
        if t.layer != layer:
            continue
        a, b = T(t.x1, t.y1), T(t.x2, t.y2)
        ax.plot([a[0], b[0]], [a[1], b[1]], c="#e0b64a", lw=t.width * 2.2,
                solid_capstyle="round", zorder=4)
    for v in vias:
        cx, cy = T(v.x, v.y)
        ax.add_patch(Circle((cx, cy), v.pad / 2, fc="#dfe6ea", ec="none", zorder=5))
        ax.add_patch(Circle((cx, cy), v.drill / 2, fc="#0f2a1c", ec="none", zorder=6))
    for pd in board.pads():
        if pd.kind == "np_thru_hole":
            continue
        if not pd.tht and not pd.on(layer):
            continue
        w, h = pd.size_rot()
        cx, cy = T(pd.x, pd.y)
        if pd.shape == "circle":
            ax.add_patch(Circle((cx, cy), w / 2, fc="#f0e2b6", ec="none", zorder=7))
        else:
            ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fc="#f0e2b6",
                                   ec="none", zorder=7))
        if pd.drill:
            ax.add_patch(Circle((cx, cy), pd.drill / 2, fc="#0f2a1c", ec="none", zorder=8))
    tl = sum(math.hypot(t.x2 - t.x1, t.y2 - t.y1) for t in tracks if t.layer == layer)
    S.label(ax, 22, 140, f"{sum(1 for t in tracks if t.layer == layer)} segments, "
                         f"{tl/1000:.2f} m of conductor on this layer.  "
                         f"{len(vias)} vias on the board.", 6.0)
    S.label(ax, 22, 133, "Green: the reference pour (AGND_REF left of x = 58 mm, "
                         "DGND right of it).  Gold: routed conductors.  "
                         "Cream: pads.", 5.6, color="#4a5c68")
    _out(pdf, png_dir, fig, f"copper_{side}")


def _out(pdf, png_dir, fig, name):
    fig.tight_layout(pad=0.2)
    if pdf:
        pdf.savefig(fig)
    if png_dir:
        fig.savefig(os.path.join(png_dir, name + ".png"), dpi=160)
    plt.close(fig)


def build(outdir, board, tracks, vias, pour_geo, png_dir=None):
    os.makedirs(outdir, exist_ok=True)
    if png_dir:
        os.makedirs(png_dir, exist_ok=True)
    made = []
    p = os.path.join(outdir, "EEG-CAR-01_RevB_fabrication_drawing.pdf")
    with PdfPages(p) as pdf:
        fabrication(pdf, board, vias, png_dir)
        drill_map(pdf, board, vias, png_dir)
    made.append(p)
    p = os.path.join(outdir, "EEG-CAR-01_RevB_assembly_drawing.pdf")
    with PdfPages(p) as pdf:
        assembly(pdf, board, png_dir, "top")
        assembly(pdf, board, png_dir, "bottom")
    made.append(p)
    p = os.path.join(outdir, "EEG-CAR-01_RevB_copper_layers.pdf")
    with PdfPages(p) as pdf:
        for lay in ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu"):
            copper_view(pdf, board, tracks, vias, pour_geo, lay, png_dir)
    made.append(p)
    return made
