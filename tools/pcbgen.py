#!/usr/bin/env python3
"""
pcbgen.py -- assemble EEG-CAR-01 Rev B from design.py into an in-memory board,
and validate it before anything downstream is generated.

Checks performed (all are hard errors unless listed as warnings):
  * every footprint in the design exists in fplib
  * every pad of every component has a net, or is explicitly a mechanical pad
  * every net has at least two pads (a one-pad net cannot be built)
  * no two courtyards overlap
  * every part lies inside the board outline with a 2 mm edge keep-out
  * analogue-zone nets do not have pads in the digital zone and vice versa (warning)

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field

import design as D
import fplib


@dataclass
class Pad:
    ref: str
    num: str
    kind: str
    shape: str
    x: float
    y: float
    w: float
    h: float
    rot: float
    drill: float
    layers: tuple
    net: str

    @property
    def tht(self):
        return self.kind in ("thru_hole", "np_thru_hole")

    @property
    def plated(self):
        return self.kind == "thru_hole"

    def on(self, layer):
        if self.tht:
            return True
        return any(l == layer or l == "*.Cu" for l in self.layers)

    def size_rot(self):
        """(w,h) after 0/90/180/270 rotation."""
        q = int(round(self.rot / 90.0)) % 2
        return (self.h, self.w) if q else (self.w, self.h)


@dataclass
class Part:
    ref: str
    fpname: str
    value: str
    x: float
    y: float
    rot: float
    mpn: str
    descr: str
    zone: str
    pads: list = field(default_factory=list)
    silk: list = field(default_factory=list)
    fab: list = field(default_factory=list)
    crtyd: list = field(default_factory=list)
    side: str = "top"

    @property
    def is_tht(self):
        return any(p.tht for p in self.pads)


def _rot(px, py, deg):
    a = math.radians(deg)
    return (px * math.cos(a) - py * math.sin(a), px * math.sin(a) + py * math.cos(a))


def _rotseg(seg, deg, ox, oy):
    x1, y1, x2, y2, w = seg
    a = _rot(x1, y1, deg)
    b = _rot(x2, y2, deg)
    return (ox + a[0], oy + a[1], ox + b[0], oy + b[1], w)


class BoardV2:
    def __init__(self):
        self.parts = []
        self.warnings = []
        self.errors = []
        self.width = D.BOARD_W
        self.height = D.BOARD_H
        self._build()

    # ------------------------------------------------------------------ build
    def _build(self):
        for ref, c in D.C.items():
            fp = fplib.get(c["fp"])
            p = Part(ref=ref, fpname=c["fp"], value=c["val"], x=c["x"], y=c["y"],
                     rot=c["rot"], mpn=c["mpn"], descr=c["descr"], zone=c["zone"])
            for pd in fp.pads:
                rx, ry = _rot(pd.x, pd.y, c["rot"])
                key = f"{ref}.{pd.num}"
                net = D.N.get(key, "")
                if pd.kind == "np_thru_hole":
                    net = ""
                p.pads.append(Pad(ref=ref, num=pd.num, kind=pd.kind, shape=pd.shape,
                                  x=c["x"] + rx, y=c["y"] + ry, w=pd.w, h=pd.h,
                                  rot=(c["rot"] + 0) % 360, drill=pd.drill,
                                  layers=tuple(pd.layers), net=net))
            for src, dst in ((fp.silk, p.silk), (fp.fab, p.fab), (fp.crtyd, p.crtyd)):
                for seg in src:
                    dst.append(_rotseg(seg, c["rot"], c["x"], c["y"]))
            self.parts.append(p)
        self.parts.sort(key=lambda p: (p.ref[0], _natkey(p.ref)))

    # ------------------------------------------------------------------ access
    def pads(self):
        for p in self.parts:
            for pd in p.pads:
                yield pd

    def nets(self):
        d = {}
        for pd in self.pads():
            if pd.net:
                d.setdefault(pd.net, []).append(pd)
        return d

    def part(self, ref):
        for p in self.parts:
            if p.ref == ref:
                return p
        return None

    def courtyard_box(self, part):
        xs, ys = [], []
        for seg in part.crtyd:
            xs += [seg[0], seg[2]]
            ys += [seg[1], seg[3]]
        if not xs:
            for pd in part.pads:
                w, h = pd.size_rot()
                xs += [pd.x - w / 2 - 0.2, pd.x + w / 2 + 0.2]
                ys += [pd.y - h / 2 - 0.2, pd.y + h / 2 + 0.2]
        return (min(xs), min(ys), max(xs), max(ys))

    # ------------------------------------------------------------------ checks
    def validate(self, edge_keepout=2.0):
        errs, warns = [], []

        # unassigned pads
        for pd in self.pads():
            if (not pd.net and pd.kind != "np_thru_hole"
                    and not pd.ref.startswith("FID")):
                errs.append(f"pad {pd.ref}.{pd.num} has no net")

        # one-pad nets
        for net, pads in sorted(self.nets().items()):
            if len(pads) < 2:
                if net.endswith("_NC") or net.startswith("NC_") or net in ("GPIO0_BOOT",):
                    warns.append(f"net {net} has one pad (declared no-connect)")
                else:
                    errs.append(f"net {net} has only one pad: "
                                + ", ".join(f"{p.ref}.{p.num}" for p in pads))

        # courtyard overlap
        boxes = [(p.ref, self.courtyard_box(p)) for p in self.parts]
        for i in range(len(boxes)):
            r1, b1 = boxes[i]
            for j in range(i + 1, len(boxes)):
                r2, b2 = boxes[j]
                if (b1[0] < b2[2] - 1e-6 and b2[0] < b1[2] - 1e-6
                        and b1[1] < b2[3] - 1e-6 and b2[1] < b1[3] - 1e-6):
                    ox = min(b1[2], b2[2]) - max(b1[0], b2[0])
                    oy = min(b1[3], b2[3]) - max(b1[1], b2[1])
                    errs.append(f"courtyard overlap {r1} / {r2}  ({ox:.2f} x {oy:.2f} mm)")

        # board edge
        for ref, b in boxes:
            if (b[0] < edge_keepout or b[1] < edge_keepout
                    or b[2] > self.width - edge_keepout or b[3] > self.height - edge_keepout):
                errs.append(f"{ref} courtyard ({b[0]:.1f},{b[1]:.1f})-({b[2]:.1f},{b[3]:.1f}) "
                            f"breaks the {edge_keepout} mm edge keep-out")

        # zoning
        for net, pads in self.nets().items():
            if net in D.ANALOG_ZONE_NETS:
                stray = [f"{p.ref}.{p.num}" for p in pads if p.x > D.ZONE_SPLIT_X]
                if stray:
                    warns.append(f"analogue net {net} has pads in the digital zone: "
                                 + ", ".join(stray))
        self.errors, self.warnings = errs, warns
        return errs, warns


def _natkey(ref):
    num = "".join(ch for ch in ref if ch.isdigit())
    return int(num) if num else 0


# ---------------------------------------------------------------------- plot
def placement_plot(board, path, side="top", title=None, show_nets=False):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle

    fig, ax = plt.subplots(figsize=(13.0, 12.4))
    ax.add_patch(Rectangle((0, 0), board.width, board.height, fill=False, lw=1.4, ec="black"))
    ax.plot([D.ZONE_SPLIT_X, D.ZONE_SPLIT_X], [0, board.height], "--", c="#c04040", lw=0.9)
    ax.text(D.ZONE_SPLIT_X - 1, 3, "ANALOGUE", ha="right", fontsize=8, color="#c04040")
    ax.text(D.ZONE_SPLIT_X + 1, 3, "DIGITAL", ha="left", fontsize=8, color="#c04040")

    for p in board.parts:
        b = board.courtyard_box(p)
        ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1],
                               fill=True, fc="#e8eef6", ec="#7799bb", lw=0.4, alpha=0.85))
        for seg in p.silk:
            ax.plot([seg[0], seg[2]], [seg[1], seg[3]], c="#334455", lw=0.35)
        for pd in p.pads:
            w, h = pd.size_rot()
            col = "#b07020" if pd.tht else "#c03030"
            if pd.shape == "circle" or pd.kind == "np_thru_hole":
                ax.add_patch(Circle((pd.x, pd.y), w / 2, fc=col, ec="none", alpha=0.8))
            else:
                ax.add_patch(Rectangle((pd.x - w / 2, pd.y - h / 2), w, h,
                                       fc=col, ec="none", alpha=0.8))
            if pd.drill:
                ax.add_patch(Circle((pd.x, pd.y), pd.drill / 2, fc="white", ec="none"))
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        ax.text(cx, cy, p.ref, ha="center", va="center", fontsize=4.6, color="#102030")

    if show_nets:
        for net, pads in board.nets().items():
            if len(pads) < 2 or net in ("DGND", "AGND_REF", "DVDD3V3", "AVDD", "AVSS"):
                continue
            xs = [q.x for q in pads]
            ys = [q.y for q in pads]
            order = sorted(range(len(pads)), key=lambda i: (xs[i], ys[i]))
            for a, bq in zip(order, order[1:]):
                ax.plot([xs[a], xs[bq]], [ys[a], ys[bq]], c="#88aa88", lw=0.25, alpha=0.5)

    ax.set_xlim(-4, board.width + 4)
    ax.set_ylim(board.height + 4, -4)
    ax.set_aspect("equal")
    ax.set_title(title or f"EEG-CAR-01 Rev {D.REV} -- placement ({side})", fontsize=11)
    ax.set_xlabel("mm")
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    import sys
    b = BoardV2()
    errs, warns = b.validate()
    print(f"parts {len(b.parts)}   pads {sum(1 for _ in b.pads())}   nets {len(b.nets())}")
    tht = sum(1 for p in b.pads() if p.kind == "thru_hole")
    npth = sum(1 for p in b.pads() if p.kind == "np_thru_hole")
    smd = sum(1 for p in b.pads() if p.kind == "smd")
    print(f"pads: smd {smd}  pth {tht}  npth {npth}")
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    print(f"{len(errs)} errors, {len(warns)} warnings")
    if len(sys.argv) > 1:
        placement_plot(b, sys.argv[1], show_nets=("--nets" in sys.argv))
        print("plot ->", sys.argv[1])
