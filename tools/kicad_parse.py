#!/usr/bin/env python3
"""
kicad_parse.py -- minimal reader for the legacy (KiCad 4/5 s-expression) .kicad_pcb
format used by EEG-CAR-01, part of the TI One Voice EEG field kit package v2 toolchain.

It exists because EEG-CAR-01.kicad_pcb was written by a generator script, is placed and
netlisted but unrouted, and every downstream artifact in this package (schematic sheets,
routing, Gerbers, drill, CPL, IPC-D-356 netlist, drawings, DRC) is derived from it so that
one file remains the single source of truth.

Licence: CC BY-SA 4.0 (same as the hardware).
"""
from __future__ import annotations
import math
import re
from dataclasses import dataclass, field


# --------------------------------------------------------------------------- s-expression
def tokenize(text: str):
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c in "()":
            out.append(c)
            i += 1
        elif c.isspace():
            i += 1
        elif c == '"':
            j = i + 1
            buf = []
            while j < n:
                if text[j] == "\\":
                    buf.append(text[j + 1])
                    j += 2
                elif text[j] == '"':
                    break
                else:
                    buf.append(text[j])
                    j += 1
            out.append(("str", "".join(buf)))
            i = j + 1
        else:
            j = i
            while j < n and not text[j].isspace() and text[j] not in "()":
                j += 1
            out.append(("atom", text[i:j]))
            i = j
    return out


def parse_sexp(text: str):
    toks = tokenize(text)
    stack = [[]]
    for t in toks:
        if t == "(":
            stack.append([])
        elif t == ")":
            node = stack.pop()
            stack[-1].append(node)
        else:
            stack[-1].append(t[1] if t[0] == "str" else t[1])
    return stack[0][0]


def head(node):
    return node[0] if node and isinstance(node[0], str) else None


def children(node, name):
    return [c for c in node[1:] if isinstance(c, list) and head(c) == name]


def child(node, name):
    c = children(node, name)
    return c[0] if c else None


def fnum(x):
    return float(x)


# --------------------------------------------------------------------------- data model
@dataclass
class Pad:
    ref: str            # parent footprint reference designator
    num: str            # pad number/name
    kind: str           # 'thru_hole' | 'smd' | 'np_thru_hole'
    shape: str          # 'rect' | 'oval' | 'circle' | 'roundrect'
    x: float            # absolute board mm
    y: float
    w: float
    h: float
    rot: float          # absolute degrees
    drill: float        # 0 for SMD
    layers: list        # raw layer tokens
    net: int
    netname: str

    @property
    def is_tht(self):
        return self.kind in ("thru_hole", "np_thru_hole")

    @property
    def on_front(self):
        return self.is_tht or any(l.startswith("F.") or l == "*.Cu" for l in self.layers)

    @property
    def on_back(self):
        return self.is_tht or any(l.startswith("B.") for l in self.layers)

    def outline(self):
        """Axis-aligned-ish half sizes after rotation (0/90 only in this board)."""
        r = round(self.rot / 90.0) % 2
        return (self.h, self.w) if r == 1 else (self.w, self.h)


@dataclass
class Graphic:
    layer: str
    kind: str           # 'line' | 'circle' | 'arc' | 'text'
    pts: list
    width: float
    text: str = ""
    size: float = 1.0
    rot: float = 0.0


@dataclass
class Footprint:
    ref: str
    value: str
    lib: str
    x: float
    y: float
    rot: float
    layer: str
    pads: list = field(default_factory=list)
    graphics: list = field(default_factory=list)

    @property
    def side(self):
        return "bottom" if self.layer == "B.Cu" else "top"


@dataclass
class Board:
    nets: dict                  # code -> name
    footprints: list
    outline: list               # list of ((x1,y1),(x2,y2))
    width: float
    height: float
    setup: dict

    def pads(self):
        for f in self.footprints:
            for p in f.pads:
                yield p

    def net_pads(self):
        d = {}
        for p in self.pads():
            if p.net:
                d.setdefault(p.net, []).append(p)
        return d

    def fp(self, ref):
        for f in self.footprints:
            if f.ref == ref:
                return f
        return None


def _rot(px, py, deg):
    a = math.radians(deg)
    return (px * math.cos(a) - py * math.sin(a),
            px * math.sin(a) + py * math.cos(a))


def load(path: str) -> Board:
    root = parse_sexp(open(path, "r", encoding="utf-8").read())
    assert head(root) == "kicad_pcb", head(root)

    nets = {}
    for n in children(root, "net"):
        nets[int(n[1])] = n[2] if len(n) > 2 else ""

    setup = {}
    s = child(root, "setup")
    if s:
        for c in s[1:]:
            if isinstance(c, list) and len(c) >= 2:
                setup[c[0]] = c[1]

    outline = []
    for g in children(root, "gr_line"):
        if (child(g, "layer") or [None, None])[1] == "Edge.Cuts":
            st = child(g, "start")
            en = child(g, "end")
            outline.append(((fnum(st[1]), fnum(st[2])), (fnum(en[1]), fnum(en[2]))))

    fps = []
    for m in children(root, "module"):
        at = child(m, "at")
        fx, fy = fnum(at[1]), fnum(at[2])
        frot = fnum(at[3]) if len(at) > 3 else 0.0
        lay = (child(m, "layer") or [None, "F.Cu"])[1]
        ref, val = "?", ""
        for t in children(m, "fp_text"):
            if t[1] == "reference":
                ref = t[2]
            elif t[1] == "value":
                val = t[2]
        fp = Footprint(ref=ref, value=val, lib=m[1], x=fx, y=fy, rot=frot, layer=lay)

        for p in children(m, "pad"):
            num = str(p[1])
            kind = p[2]
            shape = p[3]
            pat = child(p, "at")
            px, py = fnum(pat[1]), fnum(pat[2])
            prot = fnum(pat[3]) if len(pat) > 3 else 0.0
            sz = child(p, "size")
            pw, ph = fnum(sz[1]), fnum(sz[2])
            dr = child(p, "drill")
            drill = fnum(dr[1]) if dr and len(dr) > 1 else 0.0
            lys = child(p, "layers")
            layers = [str(x) for x in lys[1:]] if lys else []
            nt = child(p, "net")
            net = int(nt[1]) if nt else 0
            nname = nt[2] if nt and len(nt) > 2 else ""
            rx, ry = _rot(px, py, frot)
            fp.pads.append(Pad(ref=ref, num=num, kind=kind, shape=shape,
                               x=fx + rx, y=fy + ry, w=pw, h=ph,
                               rot=(frot + prot) % 360.0, drill=drill,
                               layers=layers, net=net, netname=nname))

        for gname, kind in (("fp_line", "line"), ("fp_circle", "circle"), ("fp_arc", "arc")):
            for g in children(m, gname):
                lyr = (child(g, "layer") or [None, ""])[1]
                st = child(g, "start")
                en = child(g, "end") or child(g, "center")
                if not st or not en:
                    continue
                a = _rot(fnum(st[1]), fnum(st[2]), frot)
                b = _rot(fnum(en[1]), fnum(en[2]), frot)
                wd = child(g, "width")
                fp.graphics.append(Graphic(layer=lyr, kind=kind,
                                           pts=[(fx + a[0], fy + a[1]), (fx + b[0], fy + b[1])],
                                           width=fnum(wd[1]) if wd else 0.12))
        fps.append(fp)

    xs = [p for seg in outline for p in (seg[0][0], seg[1][0])] or [0, 130]
    ys = [p for seg in outline for p in (seg[0][1], seg[1][1])] or [0, 124]
    return Board(nets=nets, footprints=fps, outline=outline,
                 width=max(xs) - min(xs), height=max(ys) - min(ys), setup=setup)


if __name__ == "__main__":
    import sys, collections
    b = load(sys.argv[1])
    pads = list(b.pads())
    print(f"board {b.width} x {b.height} mm, {len(b.footprints)} footprints, "
          f"{len(b.nets)} nets, {len(pads)} pads")
    kinds = collections.Counter(p.kind for p in pads)
    print("pad kinds:", dict(kinds))
    print("unassigned pads:", sum(1 for p in pads if not p.net))
    np_ = b.net_pads()
    single = [b.nets[n] for n, ps in np_.items() if len(ps) < 2]
    print(f"nets with <2 pads ({len(single)}):", single[:40])
    big = sorted(((len(ps), b.nets[n]) for n, ps in np_.items()), reverse=True)[:12]
    print("largest nets:", big)
    print("footprint libs:", dict(collections.Counter(f.lib for f in b.footprints)))
