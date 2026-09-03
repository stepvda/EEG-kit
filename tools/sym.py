#!/usr/bin/env python3
"""
sym.py -- a tiny schematic symbol library drawn with matplotlib.

Enough to draw the EEG-CAR-01 schematic sheets from the same netlist the board is built
from, so the schematic and the PCB cannot drift apart.  Units are schematic millimetres
on an A3 sheet; Y is up.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math

LW = 0.55
INK = "#12212e"
WIRE = "#12212e"
HILITE = "#b23b2e"
GHOST = "#8fa0ad"


def wire(ax, pts, color=WIRE, lw=LW, ls="-"):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, c=color, lw=lw, ls=ls, solid_capstyle="round", zorder=3)


def junction(ax, x, y, color=WIRE):
    ax.plot([x], [y], marker="o", ms=2.3, c=color, zorder=5)


def label(ax, x, y, s, size=6.0, ha="left", va="center", color=INK, rot=0, weight=None,
          family="DejaVu Sans"):
    ax.text(x, y, s, fontsize=size, ha=ha, va=va, color=color, rotation=rot,
            fontweight=weight, family=family, zorder=6)


def resistor(ax, x, y, w=7.0, h=2.6, rot=0, ref="", val="", refside=1):
    """IEC box resistor, pins at (x - w/2, y) and (x + w/2, y) before rotation."""
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def T(px, py):
        return (x + px * c - py * s, y + px * s + py * c)
    box = [T(-w / 4, -h / 2), T(w / 4, -h / 2), T(w / 4, h / 2), T(-w / 4, h / 2),
           T(-w / 4, -h / 2)]
    wire(ax, box)
    wire(ax, [T(-w / 2, 0), T(-w / 4, 0)])
    wire(ax, [T(w / 4, 0), T(w / 2, 0)])
    if ref:
        label(ax, *T(0, refside * (h / 2 + 1.4)), ref, 5.2, ha="center",
              va="bottom" if refside > 0 else "top")
    if val:
        label(ax, *T(0, -refside * (h / 2 + 1.4)), val, 5.0, ha="center",
              va="top" if refside > 0 else "bottom", color="#4a5c68")
    return T(-w / 2, 0), T(w / 2, 0)


def capacitor(ax, x, y, gap=1.1, plate=3.0, rot=0, ref="", val="", lead=2.6):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def T(px, py):
        return (x + px * c - py * s, y + px * s + py * c)
    wire(ax, [T(-gap / 2, -plate / 2), T(-gap / 2, plate / 2)], lw=LW * 1.6)
    wire(ax, [T(gap / 2, -plate / 2), T(gap / 2, plate / 2)], lw=LW * 1.6)
    wire(ax, [T(-gap / 2 - lead, 0), T(-gap / 2, 0)])
    wire(ax, [T(gap / 2, 0), T(gap / 2 + lead, 0)])
    if ref:
        label(ax, *T(0, plate / 2 + 1.2), ref, 5.2, ha="center", va="bottom")
    if val:
        label(ax, *T(0, -plate / 2 - 1.2), val, 5.0, ha="center", va="top", color="#4a5c68")
    return T(-gap / 2 - lead, 0), T(gap / 2 + lead, 0)


def diode(ax, x, y, size=2.4, rot=0, ref="", val="", lead=2.6, schottky=False):
    """Anode at the left pin, cathode at the right pin (before rotation)."""
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def T(px, py):
        return (x + px * c - py * s, y + px * s + py * c)
    tri = [T(-size / 2, -size / 2), T(-size / 2, size / 2), T(size / 2, 0),
           T(-size / 2, -size / 2)]
    ax.fill([p[0] for p in tri], [p[1] for p in tri], color=INK, zorder=3)
    wire(ax, [T(size / 2, -size / 2), T(size / 2, size / 2)], lw=LW * 1.6)
    if schottky:
        wire(ax, [T(size / 2 - 0.7, size / 2), T(size / 2, size / 2),
                  T(size / 2, size / 2 - 0.7)], lw=LW * 1.2)
        wire(ax, [T(size / 2 + 0.7, -size / 2), T(size / 2, -size / 2),
                  T(size / 2, -size / 2 + 0.7)], lw=LW * 1.2)
    wire(ax, [T(-size / 2 - lead, 0), T(-size / 2, 0)])
    wire(ax, [T(size / 2, 0), T(size / 2 + lead, 0)])
    if ref:
        label(ax, *T(0, size / 2 + 1.2), ref, 5.2, ha="center", va="bottom")
    if val:
        label(ax, *T(0, -size / 2 - 1.2), val, 5.0, ha="center", va="top", color="#4a5c68")
    return T(-size / 2 - lead, 0), T(size / 2 + lead, 0)


def opamp(ax, x, y, w=11.0, h=10.0, ref="", sub="", inv_top=True, comparator=False):
    """Triangle pointing right.  Returns (in_top, in_bot, out, vplus, vminus)."""
    tri = [(x - w / 2, y - h / 2), (x - w / 2, y + h / 2), (x + w / 2, y),
           (x - w / 2, y - h / 2)]
    wire(ax, tri)
    it = (x - w / 2 - 3.0, y + h / 4)
    ib = (x - w / 2 - 3.0, y - h / 4)
    wire(ax, [it, (x - w / 2, y + h / 4)])
    wire(ax, [ib, (x - w / 2, y - h / 4)])
    out = (x + w / 2 + 3.0, y)
    wire(ax, [(x + w / 2, y), out])
    label(ax, x - w / 2 + 1.4, y + h / 4, "-" if inv_top else "+", 7, ha="left")
    label(ax, x - w / 2 + 1.4, y - h / 4, "+" if inv_top else "-", 7, ha="left")
    if ref:
        label(ax, x - 1.0, y + h / 2 + 1.2, ref, 5.4, ha="center", va="bottom")
    if sub:
        label(ax, x - 1.0, y - h / 2 - 1.2, sub, 4.8, ha="center", va="top", color="#4a5c68")
    vp = (x - w / 6, y + h / 4 + 1.0)
    vm = (x - w / 6, y - h / 4 - 1.0)
    return it, ib, out, vp, vm


def gnd(ax, x, y, kind="agnd", size=2.6, text=None):
    wire(ax, [(x, y), (x, y - 1.6)])
    if kind == "earth":
        for i, wd in enumerate((size, size * 0.65, size * 0.3)):
            wire(ax, [(x - wd / 2, y - 1.6 - i * 0.8), (x + wd / 2, y - 1.6 - i * 0.8)])
    else:
        wire(ax, [(x - size / 2, y - 1.6), (x + size / 2, y - 1.6), (x, y - 3.0),
                  (x - size / 2, y - 1.6)])
    if text:
        label(ax, x, y - 3.6, text, 4.6, ha="center", va="top", color="#4a5c68")


def rail(ax, x, y, name, up=True, color=HILITE):
    d = 1 if up else -1
    wire(ax, [(x, y), (x, y + 2.2 * d)], color=color)
    wire(ax, [(x - 2.0, y + 2.2 * d), (x + 2.0, y + 2.2 * d)], color=color, lw=LW * 1.5)
    label(ax, x, y + (3.0 * d), name, 5.2, ha="center",
          va="bottom" if up else "top", color=color)


def netlabel(ax, x, y, name, direction="right", size=5.2, color="#1b5e8a"):
    d = 1 if direction == "right" else -1
    pts = [(x, y), (x + 1.6 * d, y + 1.3), (x + 8.0 * d, y + 1.3),
           (x + 8.0 * d, y - 1.3), (x + 1.6 * d, y - 1.3), (x, y)]
    wire(ax, pts, color=color, lw=LW * 0.9)
    label(ax, x + 4.8 * d, y, name, size, ha="center", color=color)


def connector(ax, x, y, pins, ref, title, pitch=5.0, width=26.0, side="right"):
    """Vertical connector body with numbered pins.  Returns [(px, py)] per pin."""
    n = len(pins)
    h = pitch * (n - 1) + 6.0
    x0, y0 = x, y - h + 3.0
    wire(ax, [(x0, y0), (x0 + width, y0), (x0 + width, y0 + h), (x0, y0 + h), (x0, y0)],
         lw=LW * 1.25)
    label(ax, x0 + width / 2, y0 + h + 1.4, ref, 6.4, ha="center", va="bottom",
          weight="bold")
    label(ax, x0 + width / 2, y0 - 1.4, title, 4.8, ha="center", va="top", color="#4a5c68")
    out = []
    for i, p in enumerate(pins):
        py = y - i * pitch
        if side == "right":
            px = x0 + width
            wire(ax, [(px, py), (px + 4.0, py)])
            label(ax, x0 + width - 1.2, py, f"{i+1}", 4.4, ha="right")
            label(ax, x0 + 1.5, py, p, 5.0, ha="left")
            out.append((px + 4.0, py))
        else:
            px = x0
            wire(ax, [(px - 4.0, py), (px, py)])
            label(ax, x0 + 1.2, py, f"{i+1}", 4.4, ha="left")
            label(ax, x0 + width - 1.5, py, p, 5.0, ha="right")
            out.append((px - 4.0, py))
    ax.plot([x0 + (2.0 if side == "right" else width - 2.0)], [y], marker="s", ms=2.2,
            c=INK, zorder=6)
    return out


def block(ax, x, y, w, h, title, lines=(), fc="#eef3f7", ec=INK, title_size=6.4):
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=1.2",
                                fc=fc, ec=ec, lw=LW * 1.3, zorder=2))
    label(ax, x + w / 2, y + h - 3.2, title, title_size, ha="center", va="center",
          weight="bold")
    for i, ln in enumerate(lines):
        label(ax, x + 2.5, y + h - 7.5 - i * 3.4, ln, 5.0, ha="left", va="center")


def sheet(fig_w=420, fig_h=297, title="", subtitle="", sheet_no="", rev="B",
          date="2026-09-01"):
    """Create an A3 landscape sheet with a title block.  Returns (fig, ax)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(fig_w / 25.4, fig_h / 25.4))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.set_aspect("equal")
    ax.axis("off")
    m = 8
    wire(ax, [(m, m), (fig_w - m, m), (fig_w - m, fig_h - m), (m, fig_h - m), (m, m)],
         lw=1.0)
    tb_w, tb_h = 150, 26
    x0, y0 = fig_w - m - tb_w, m
    wire(ax, [(x0, y0), (x0 + tb_w, y0), (x0 + tb_w, y0 + tb_h), (x0, y0 + tb_h), (x0, y0)],
         lw=1.0)
    wire(ax, [(x0, y0 + 16), (x0 + tb_w, y0 + 16)], lw=0.7)
    wire(ax, [(x0, y0 + 8), (x0 + tb_w, y0 + 8)], lw=0.7)
    wire(ax, [(x0 + 100, y0), (x0 + 100, y0 + 8)], lw=0.7)
    label(ax, x0 + 3, y0 + 21, title, 8.2, weight="bold")
    label(ax, x0 + 3, y0 + 12, subtitle, 5.6, color="#4a5c68")
    label(ax, x0 + 3, y0 + 4, "TI One Voice research programme -- CC BY-SA 4.0", 5.0)
    label(ax, x0 + 103, y0 + 4, f"Rev {rev}   {date}   Sheet {sheet_no}", 5.4)
    return fig, ax
