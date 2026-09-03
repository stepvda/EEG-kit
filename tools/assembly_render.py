#!/usr/bin/env python3
"""
assembly_render.py -- 3D views of the electronics stack, for the assembly instructions,
the RFQ and the package cover.

Three pictures:
    stack        the carrier, the module plate and the enclosure as they sit together
    exploded     the same, pulled apart, with the assembly order
    board3d      the routed carrier on its own, with the part bodies

The carrier is drawn from tools/design.py, so the picture and the board agree; component
bodies are boxes at the real footprint size and a plausible height per package.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
import os
import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh

import design as D
import pcbgen

HEIGHT = {          # component body height above the board, in millimetres
    "R_0603_1608Metric": 0.55, "C_0603_1608Metric": 0.9, "L_0603_1608Metric": 0.9,
    "R_1206_3216Metric": 0.7, "SOT-23": 1.1, "SOT-23-5": 1.1,
    "TSSOP-14_4.4x5.0mm_P0.65mm": 1.2, "SW_PUSH_6mm_H5mm": 5.0,
    "DIN42802_1p5mm_Socket": 9.0, "JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical": 6.0,
    "TestPoint_Pad_D1.5mm": 0.05, "MountingHole_3.2mm_M3": 0.0,
}
SOCKET_H = 8.5

COL = {"socket": "#2b3a45", "chip": "#1c1c1c", "passive": "#2e3f4a",
       "switch": "#7a2d2d", "din": "#2f6b8f", "jst": "#c8a23a", "pcb": "#1f6b45",
       "copper": "#c9962e", "plate": "#c9d3db", "pod": "#8fa0ad"}


def _box(cx, cy, z0, w, h, dz):
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    z1 = z0 + dz
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [[v[0], v[1], v[2], v[3]], [v[4], v[5], v[6], v[7]],
         [v[0], v[1], v[5], v[4]], [v[2], v[3], v[7], v[6]],
         [v[1], v[2], v[6], v[5]], [v[3], v[0], v[4], v[7]]]
    return f


def _shade(faces, base, light=(0.4, -0.6, 0.7)):
    light = np.asarray(light, float)
    light /= np.linalg.norm(light)
    b = np.array([int(base[1:3], 16), int(base[3:5], 16), int(base[5:7], 16)]) / 255.0
    cols = []
    for f in faces:
        p = np.asarray(f)
        n = np.cross(p[1] - p[0], p[2] - p[0])
        ln = np.linalg.norm(n)
        n = n / ln if ln > 1e-9 else np.array([0, 0, 1.0])
        s = max(0.18, float(n @ light))
        cols.append(np.clip(b * (0.35 + 0.8 * s), 0, 1))
    return cols


def board_faces(board, z0=0.0, tracks=None, vias=None):
    faces, cols = [], []
    f = _box(D.BOARD_W / 2, D.BOARD_H / 2, z0, D.BOARD_W, D.BOARD_H, 1.6)
    faces += f
    cols += _shade(f, COL["pcb"])
    for p in board.parts:
        if p.fpname.startswith("MountingHole"):
            continue
        b = board.courtyard_box(p)
        w, h = b[2] - b[0], b[3] - b[1]
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        if p.fpname.startswith("PinSocket"):
            dz, c = SOCKET_H, COL["socket"]
        elif p.fpname.startswith("SW_"):
            dz, c = HEIGHT[p.fpname], COL["switch"]
        elif p.fpname.startswith("DIN"):
            dz, c = HEIGHT[p.fpname], COL["din"]
        elif p.fpname.startswith("JST"):
            dz, c = HEIGHT[p.fpname], COL["jst"]
        elif p.fpname.startswith("TSSOP") or p.fpname.startswith("SOT"):
            dz, c = HEIGHT[p.fpname], COL["chip"]
        else:
            dz, c = HEIGHT.get(p.fpname, 0.6), COL["passive"]
        if dz <= 0.01:
            continue
        ff = _box(cx, cy, z0 + 1.6, w * 0.9, h * 0.9, dz)
        faces += ff
        cols += _shade(ff, c)
    if tracks:
        for t in tracks:
            if t.layer != "F.Cu":
                continue
            dx, dy = t.x2 - t.x1, t.y2 - t.y1
            L = math.hypot(dx, dy)
            if L < 0.05:
                continue
            ang = math.atan2(dy, dx)
            cx, cy = (t.x1 + t.x2) / 2, (t.y1 + t.y2) / 2
            hw, hh = L / 2, t.width / 2
            corners = []
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                px, py = sx * hw, sy * hh
                corners.append((cx + px * math.cos(ang) - py * math.sin(ang),
                                cy + px * math.sin(ang) + py * math.cos(ang),
                                z0 + 1.61))
            faces.append(corners)
            cols.append(np.array([0.79, 0.59, 0.18]))
    return faces, cols


def mesh_faces(path, dx=0.0, dy=0.0, dz=0.0, color="#c9d3db", scale=1.0):
    m = trimesh.load(path)
    m.apply_translation(-m.bounds[0])
    v = m.triangles * scale + np.array([dx, dy, dz])
    return list(v), _shade(list(v), color)


def draw(faces, cols, out, title, elev=26, azim=-58, note=None):
    fig = plt.figure(figsize=(10.5, 8.0))
    ax = fig.add_subplot(111, projection="3d")
    e, a = math.radians(elev), math.radians(azim)
    view = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    keep = []
    for f, c in zip(faces, cols):
        p = np.asarray(f)
        n = np.cross(p[1] - p[0], p[2] - p[0])
        ln = np.linalg.norm(n)
        if ln > 1e-9 and (n / ln) @ view < -0.03:
            continue
        keep.append((float(p.mean(axis=0) @ view), f, c))
    keep.sort(key=lambda t: t[0])
    pc = Poly3DCollection([k[1] for k in keep], facecolors=[k[2] for k in keep],
                          edgecolors=(0, 0, 0, 0.07), linewidths=0.1)
    ax.add_collection3d(pc)
    allv = np.concatenate([np.asarray(f) for f in faces])
    c = allv.mean(axis=0)
    s = float(np.abs(allv - c).max()) * 0.80
    ax.set_xlim(c[0] - s, c[0] + s)
    ax.set_ylim(c[1] - s, c[1] + s)
    ax.set_zlim(c[2] - s, c[2] + s)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=12, color="#12212e")
    if note:
        import textwrap
        fig.text(0.5, 0.055, "\n".join(textwrap.wrap(note, 96)), ha="center",
                 va="top", fontsize=8.4, color="#4a5c68")
        fig.subplots_adjust(bottom=0.14)
    fig.savefig(out, dpi=175, facecolor="white")
    plt.close(fig)
    return out


def build(outdir, tracks=None, vias=None):
    os.makedirs(outdir, exist_ok=True)
    board = pcbgen.BoardV2()
    board.validate()
    here = os.path.dirname(os.path.abspath(__file__))
    mech = os.path.join(os.path.dirname(here), "mech", "stl")
    made = []

    f, c = board_faces(board, 0.0, tracks, vias)
    made.append(draw(f, c, os.path.join(outdir, "EEG-CAR-01_RevB_board_3d.png"),
                     f"EEG-CAR-01 Rev {D.REV} -- carrier board, top side",
                     note=f"Four layers, {D.BOARD_W:.0f} x {D.BOARD_H:.0f} mm. Analogue zone left of "
                          f"x = {D.ZONE_SPLIT_X:.0f} mm, digital right. Gold: the routed top "
                          f"layer. Component bodies at footprint size; socket strips 8.5 mm "
                          f"tall. The purchased modules are not shown -- they sit on the "
                          f"MP-01 plate above."))

    # stack: pod base, carrier on its bosses, module plate above
    f, c = mesh_faces(os.path.join(mech, "POD-P1_prototype_enclosure_base.stl"),
                      -2.5, -2.5, 0.0, COL["pod"])
    bf, bc = board_faces(board, 8.5)
    f += bf
    c += bc
    pf, pc_ = mesh_faces(os.path.join(mech, "MP-01_module_plate.stl"), 2.0, 2.0, 35.0,
                         COL["plate"])
    f += pf
    c += pc_
    made.append(draw(f, c, os.path.join(outdir, "assembly_stack.png"),
                     "Phase 1 electronics stack",
                     note="POD-P1 base, the carrier on four M3 bosses, and the MP-01 module "
                          "plate 25 mm above it. The purchased modules bolt to the plate and "
                          "reach the carrier on keyed 2.54 mm ribbon jumpers (ICD-EEG-006)."))

    f, c = mesh_faces(os.path.join(mech, "POD-P1_prototype_enclosure_base.stl"),
                      -2.5, -2.5, 0.0, COL["pod"])
    bf, bc = board_faces(board, 60.0)
    f += bf
    c += bc
    pf, pc_ = mesh_faces(os.path.join(mech, "MP-01_module_plate.stl"), 2.0, 2.0, 110.0,
                         COL["plate"])
    f += pf
    c += pc_
    lf, lc = mesh_faces(os.path.join(mech, "POD-P1_prototype_enclosure_lid.stl"),
                        -2.5, -2.5, 150.0, COL["pod"])
    f += lf
    c += lc
    made.append(draw(f, c, os.path.join(outdir, "assembly_exploded.png"),
                     "Phase 1 electronics stack -- exploded",
                     elev=18, azim=-62,
                     note="Assembly order, bottom to top: POD-P1 base with its silicone cord "
                          "seal, the carrier on M3 x 8 into the four bosses, M3 x 18 mm standoffs, "
                          "the MP-01 module plate with the modules already bolted to it, then "
                          "the lid. ASM-EEG-007 stages 2 and 4."))
    return made


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "graphics")
    tr = None
    if os.path.exists(os.path.join(here, "routed.pkl")) and "--plain" not in sys.argv:
        r = pickle.load(open(os.path.join(here, "routed.pkl"), "rb"))
        tr = r.get("tracks")
    for p in build(out, tracks=tr):
        print(p)
