#!/usr/bin/env python3
"""
mech_drawings.py -- 2D dimensioned drawings and 3D renders of the printed parts.

Rev A supplied STL meshes only. A print bureau can quote from a mesh; an inspector cannot
measure one and a fitter cannot read one. Each part here gets a drawing sheet with three
orthographic views, overall dimensions, the critical features called out, and the process
and tolerance notes -- plus a shaded render for the assembly instructions and the RFQ.

Views are produced by projecting the real mesh and taking the silhouette, so the drawing
cannot disagree with the model it was made from.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon as MplPoly
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh
from shapely.geometry import Polygon as ShPoly
from shapely.ops import unary_union

import sym as S

VIEWS = [("FRONT (looking along -Y)", (0, 2), 1),
         ("TOP (looking along -Z)", (0, 1), 2),
         ("RIGHT (looking along -X)", (1, 2), 0)]

NOTES = {
    "MP-01_module_plate": [
        "Material PA12, MJF. 3.0 mm plate.",
        "Stands 18 mm above the carrier on M3 x 18 mm nylon hex female-female standoffs",
        "through the four 3.4 mm holes, which match the carrier pattern at (5,5) (145,5)",
        "(5,125) (145,125). The 101 slots are 12 x 3 mm ribbon-jumper channels on a",
        "16 x 7 mm grid; the 104 D2.7 mm M2.5 clearance holes between the slot rows are",
        "the universal module fixing, to which any purchased module is bolted.",
        "The large opening clears the ESP32-S3-DevKitC-1, which is inserted directly into",
        "J6 and J7 and stands proud of the carrier.",
        "Tolerance on hole positions +/-0.20 mm. Deburr all edges.",
    ],
    "POD-P1_prototype_enclosure_base": [
        "Material PA12, MJF (FDM PETG acceptable for Phase 1 form studies only).",
        "Internal 158 x 138 x 55.5 mm, external 163 x 143 x 58 mm; walls 2.5 mm.",
        "Gasket groove 1.6 x 1.2 mm in the rim, for a 1.5 mm silicone cord seal: 20 %",
        "compression and 92 % groove fill. A 2 mm cord cannot seat in this groove.",
        "CARRIER BOSSES: four, D8.0 x 6.0 mm off the internal floor on MH1-MH4, bored",
        "D4.0 x 5.5 mm for an M3 brass heat-set insert. The carrier is held by the male",
        "stud of an M3 x 18 MALE-FEMALE nylon standoff, and the same standoff carries",
        "MP-01 above it: one fixing, both jobs. That settles the open point in",
        "ASM-EEG-007 section 3.3, where a female-female standoff and the pod boss wanted",
        "the same four holes and no fastener could do both. The stack is unchanged at",
        "49.1 mm and the standoff is still 18 mm of nylon, so the RISK-EEG-011 SR-08",
        "creepage path is unchanged with it.",
        "LID BOSSES: four, D8.0 at +/-75.5 x +/-65.5 mm from the pod centre, top face at",
        "55.8 mm, bored D4.0 x 7.0 mm for the same insert, carried to the floor on a",
        "corner column held 1.5 mm off the carrier corner. M3 x 12 A2 through 6.0 mm of",
        "lid. The boss tops sit 0.2 mm below the lid spigot, so the rim and the cord",
        "seal set the gasket compression and the boss never lifts the lid off its seal.",
        "Every M3 thread in this part is a brass insert and not a thread-formed PA12",
        "hole: ASM-EEG-007 3.3 puts the strip limit at about 0.5 N.m and 5.1 torques",
        "these joints to 0.60 N.m. 0.60 N.m is itself at the top of what a 5.7 mm insert",
        "in PA12 will hold, so first article measures pull-out or the torque comes down.",
        "The bore is printed, so the drilling operation ASM-EEG-007 5.1 item 1 left open",
        "is not needed.",
        "HARNESS ENTRY: two M12 x 1.5 cable glands, D12.5 through a 3.5 mm panel on a",
        "38 x 22 x 1.0 mm pad, each with a POD-P1-04 P-clip boss (D8.0, 2.5 mm",
        "thread-forming pilot) 16.0 mm off its axis. Left wall at y = 53.0 for WH-01",
        "into J14; front wall at x = -9.0 for WH-02 into J30; both axes at z = 21.0, in",
        "the harness layer between the carrier top at 10.1 and MP-01 at 28.1 mm. Two",
        "entries and not one, because RISK-EEG-011 H-05 and SF-9 exclude an LED-to-",
        "electrode fault on the strength of two cables in two separate glands.",
        "The 3.0 to 6.5 mm clamping range brackets the 4.6 and 4.5 mm jackets of",
        "WH-EEG-008 section 4, but no gland datasheet has been read: thread length,",
        "locknut size and the 3.5 mm panel are settled at first article. The clip",
        "anchors the service loop; it is NOT the '40 mm behind its housing' of",
        "WH-EEG-008 section 6, which with the gland 9 mm from J14 falls outside the pod.",
        "Panel openings per RFQ M-02: three DIN 42802 (left wall), headphone, boom TRRS,",
        "room-microphone port, data USB-C, charge USB-C, microSD and three 13 mm button",
        "openings (right wall). Every opening is recessed or gasketed so that gel and",
        "saline cannot reach the board.",
        "Tolerance +/-0.30 mm on the envelope, +0.15/-0.05 mm on the gasket groove.",
    ],
    "POD-P1_prototype_enclosure_lid": [
        "Material PA12, MJF. 4.0 mm plate with a 2.0 mm spigot that locates in the base.",
        "Four D3.4 M3 clearance holes at +/-75.5 x +/-65.5 mm from the centre. These are",
        "the same four points the base puts a boss under: both come from one constant in",
        "tools/mech_gen.py, so they cannot drift apart again. In Rev B the holes were",
        "here and there was no boss anywhere near them -- the lid could not be fastened.",
        "M3 x 12 A2 pan screws, 0.60 N.m in two passes (ASM-EEG-007 5.1 step 6): 6.0 mm",
        "through the lid and 6.0 mm into the brass insert in the base boss.",
        "The lid seats on the base rim on a 1.5 mm silicone cord; the base bosses stop",
        "0.2 mm short of the spigot face so they cannot hold the lid off its own seal.",
        "The spigot is a full 157.6 x 137.6 mm plate, so the clear height under a closed",
        "lid is 53.5 mm and not the 55.5 mm quoted as the internal depth. The stack is",
        "49.1 mm, so the margin against the lid is 4.4 mm, not the 6.4 mm of the",
        "ICD-EEG-006 section 4 budget. Reconciled there, not here.",
        "No opening in this face: RFQ M-02's pod indicator is deleted and all eight",
        "contact lights are in the helmet.",
    ],
    "HM-04_electrode_assembly_body": [
        "Material PA12, MJF. Ten per kit (eight fitted, two spare).",
        "Bonded into the HM-01 frame at manufacture with a two-part epoxy; see ASM-EEG-007.",
        "The 9.2 mm bore takes the sintered Ag/AgCl cup on its service bayonet; the two",
        "2.2 x 1.4 mm slots are the bayonet engagement and are turned only by the HM-09",
        "service key, which no finger can reach.",
        "The 2.5 mm port through the top is coaxial with the cup and takes a blunt syringe.",
        "The side window carries the bicolour contact light, facing up and outward so it can",
        "be read in a mirror (DSN-EEG-002 section 5).",
        "Critical fits +0.15/-0.05 mm. Check on the FIT-01 coupon before accepting a batch.",
    ],
    "HM-08_battery_hatch": [
        "Material PA12, MJF. Quarter-turn, tool-free, three lugs at 120 degrees.",
        "Called HM-07 in package v1; renamed in PARTS-EEG-019 because DSN-EEG-002 section 10",
        "already used HM-07 for the boom microphone arm.",
        "The seal groove takes a 1.5 mm silicone cord. The coin slot is for service only;",
        "a participant turns it by hand.",
        "Interlocked: opening it ends the session cleanly and writes a marker rather than",
        "truncating the recording mid-block.",
    ],
    "HM-09_service_key": [
        "Material PA12. ONE PER OPERATOR. Deliberately absent from the participant's kit.",
        "Engages the two HM-04 bayonet slots to release a cup for cleaning or replacement.",
        "Controlled item: see SVC-EEG-013 section 3.",
    ],
    "HM-02_brow_pad": [
        "Material TPU 85A, printed or cast. Consumable, replaced at every turnaround.",
        "The only part that touches the forehead. ISO 10993-5 and -10 declarations required",
        "from the material supplier (RFQ S-05).",
    ],
    "FIT-01_fit_test_coupon": [
        "Material PA12, same build as the batch it qualifies.",
        "Three bores at 9.20, 9.35 and 9.15 mm: nominal, upper limit and lower limit of the",
        "cup bayonet fit. A cup must enter the 9.20 and 9.35 bores and must NOT enter 9.15.",
        "Printed with every batch and checked before the batch is accepted (QP-EEG-010).",
    ],
}


# What each part actually carries, from tools/mech_gen.py MARKING and PARTS-EEG-019
# section 4.1.  Rev A printed "Part ID engraved in the model" on all ten sheets, including
# the three parts section 4.1 exempts and the two that no generator marks.
MARKING = {
    "MP-01_module_plate": [
        "Marked MP-01 B, engraved 0.40 mm into the top face inside the 8 mm border,",
        "0.72 mm stroke. Engraved, not labelled, so it survives disinfection.",
    ],
    "POD-P1_prototype_enclosure_base": [
        "Marked POD-P1-01 B, engraved 0.40 mm into the external floor, 0.87 mm stroke.",
        "Engraved, not labelled, so it survives disinfection.",
    ],
    "POD-P1_prototype_enclosure_lid": [
        "Marked POD-P1-02 B, engraved 0.40 mm into the inside face of the spigot,",
        "0.87 mm stroke. The outer face is the ART-LBL-01 keep-out and stays flat.",
    ],
    "HM-08_battery_hatch": [
        "Marked HM-08 B, engraved 0.40 mm into the top face below the coin slot,",
        "0.72 mm stroke. Engraved, not labelled, so it survives disinfection.",
    ],
    "HM-09_service_key": [
        "Marked HM-09 A, engraved 0.40 mm into the grip end face, 0.58 mm stroke. That is",
        "under the 0.60 mm minimum of PARTS-EEG-019 section 4.1: a 17.93 mm face will not",
        "hold the identifier any larger, and will not hold the SVC-EEG-013 section 4.2",
        "legend at all. Legend and key number are applied per key when a key is issued.",
    ],
    "HM-04_electrode_assembly_body": [
        "Not marked; identified by the bag label at kitting (PARTS-EEG-019 section 4.1).",
    ],
    "HM-02_brow_pad": [
        "Not marked; identified by the bag label at kitting (PARTS-EEG-019 section 4.1).",
    ],
    "FIT-01_fit_test_coupon": [
        "Not marked; identified by the bag label at kitting (PARTS-EEG-019 section 4.1).",
    ],
    "HM-01_frame_monocoque": [
        "PARTS-EEG-019 section 4.1 requires the identifier, the revision, the eight site",
        "names and the print build number modelled in. The carried-over v1 mesh carries",
        "none of them, and will not until the parametric model exists (PARTS OA-1).",
    ],
    "EEG-CAR-01_RevB_board_outline": [
        "Marked as a white LPI legend on the board, not engraved in this outline solid",
        "(PARTS-EEG-019 section 4.1). This sheet is the board envelope, not the",
        "fabrication drawing.",
    ],
}
MARKING_DEFAULT = ["Marking not stated for this part (PARTS-EEG-019 section 4.1)."]

# M29: the register cites sheet numbers by hand and drifted two pages when the sheet set
# grew.  build() writes the index it actually paginated, so the citation can be checked.
PART_ID = {
    "EEG-CAR-01_RevB_board_outline": "EEG-CAR-01",
    "FIT-01_fit_test_coupon": "FIT-01",
    "HM-01_frame_monocoque": "HM-01",
    "HM-02_brow_pad": "HM-02A",
    "HM-04_electrode_assembly_body": "HM-04",
    "HM-08_battery_hatch": "HM-08",
    "HM-09_service_key": "HM-09",
    "MP-01_module_plate": "MP-01",
    "POD-P1_prototype_enclosure_base": "POD-P1-01",
    "POD-P1_prototype_enclosure_lid": "POD-P1-02",
}


# A silhouette cannot show an internal feature: a boss inside a box projects onto material
# that is already there.  Every fixing in POD-P1-01 -- the carrier bosses, the corner columns
# that carry the lid bosses, the two gland entries -- is internal, so the sheet showed a
# blank rectangle and the reader had to take the notes on trust.  A part may declare
# horizontal sections here and they are drawn over its TOP view, cut from the same released
# mesh as the silhouette, so they cannot disagree with it either.  Heights are in the part's
# own coordinates; the sheet translates the mesh to its bounding box, and so does the cut.
SECTIONS = {
    "POD-P1_prototype_enclosure_base": [
        (21.0, "A-A  z 21.0, the harness layer: gland entries and P-clip bosses", "#b03a2e"),
        (50.0, "B-B  z 50.0, above the stack: the four lid bosses", "#1f6f8b"),
        (5.0, "C-C  z 5.0, floor: the four carrier bosses on MH1-MH4", "#6b7f2e"),
    ],
}


def _draw_section(ax, mesh, z, ox, oy, sc, color):
    """Cut `mesh` at height `z` and draw the section outline over a TOP view."""
    try:
        sec = mesh.section(plane_origin=[0.0, 0.0, z], plane_normal=[0.0, 0.0, 1.0])
    except Exception:
        sec = None
    if sec is None:
        return 0
    n = 0
    for poly in sec.discrete:
        ax.plot(ox + poly[:, 0] * sc, oy + poly[:, 1] * sc,
                lw=0.5, color=color, zorder=4)
        n += 1
    return n


def _silhouette(mesh, axes):
    tris = mesh.triangles[:, :, axes]
    polys = []
    for t in tris:
        p = ShPoly(t)
        if p.is_valid and p.area > 1e-9:
            polys.append(p)
    if not polys:
        return None
    return unary_union(polys).buffer(0)


def _draw_view(ax, geom, title, ox, oy, sc, dims=None):
    from shapely.geometry import Polygon as SP, MultiPolygon
    ps = [geom] if isinstance(geom, SP) else list(geom.geoms)
    for poly in ps:
        ext = np.asarray(poly.exterior.coords)
        ax.add_patch(MplPoly(np.column_stack([ox + ext[:, 0] * sc, oy + ext[:, 1] * sc]),
                             closed=True, fc="#eef2f6", ec="#12212e", lw=0.7, zorder=2))
        for ring in poly.interiors:
            r = np.asarray(ring.coords)
            ax.add_patch(MplPoly(np.column_stack([ox + r[:, 0] * sc, oy + r[:, 1] * sc]),
                                 closed=True, fc="white", ec="#12212e", lw=0.5, zorder=3))
    b = geom.bounds
    S.label(ax, ox + (b[0] + b[2]) / 2 * sc, oy + b[3] * sc + 5, title, 6.0, ha="center")
    if dims:
        S.wire(ax, [(ox + b[0] * sc, oy + b[1] * sc - 4),
                    (ox + b[2] * sc, oy + b[1] * sc - 4)], lw=0.6)
        S.label(ax, ox + (b[0] + b[2]) / 2 * sc, oy + b[1] * sc - 3,
                f"{b[2]-b[0]:.2f}", 5.4, ha="center", va="bottom")
        S.wire(ax, [(ox + b[2] * sc + 4, oy + b[1] * sc),
                    (ox + b[2] * sc + 4, oy + b[3] * sc)], lw=0.6)
        S.label(ax, ox + b[2] * sc + 5, oy + (b[1] + b[3]) / 2 * sc,
                f"{b[3]-b[1]:.2f}", 5.4, rot=90, va="center")


def part_sheet(pdf, png_dir, stl_path, name, sheet_no, total):
    mesh = trimesh.load(stl_path)
    origin = mesh.bounds[0].copy()
    mesh.apply_translation(-mesh.bounds[0])
    ext = mesh.extents
    fig, ax = S.sheet(420, 297, f"{name.split('_')[0]} -- {name.split('_', 1)[1].replace('_', ' ')}",
                      f"Printed part drawing.  Projections from the released mesh.",
                      f"MECH {sheet_no} of {total}")
    sc = min(150.0 / max(ext[0], 1), 110.0 / max(ext[2], 1), 110.0 / max(ext[1], 1), 3.0)
    sc = max(sc, 0.35)
    for i, (title, axes, _) in enumerate(VIEWS):
        g = _silhouette(mesh, list(axes))
        if g is None or g.is_empty:
            continue
        ox = 30 + i * 130
        oy = 170
        _draw_view(ax, g, title, ox, oy, sc, dims=True)
        if axes == (0, 1):          # TOP view: overlay the declared horizontal sections
            for j, (zc, cap, col) in enumerate(SECTIONS.get(name, [])):
                if _draw_section(ax, mesh, zc - origin[2], ox, oy, sc, col):
                    S.label(ax, ox, 160 - j * 5.0, "SECTION " + cap, 5.2, color=col)
    S.label(ax, 30, 140, "OVERALL", 6.6, weight="bold")
    S.label(ax, 30, 133, f"X {ext[0]:.2f} mm    Y {ext[1]:.2f} mm    Z {ext[2]:.2f} mm", 6.0)
    S.label(ax, 30, 127, f"volume {mesh.volume/1000.0:.2f} cm3    "
                         f"surface {mesh.area/100.0:.1f} cm2    "
                         f"triangles {len(mesh.faces)}    "
                         f"watertight {'yes' if mesh.is_watertight else 'NO'}", 6.0)
    # NOTES run down the left of the sheet and wrap into a second column at 17 lines;
    # GENERAL sits in its own column on the right.  Rev A ran both from x = 30 and the
    # POD-P1 sheet, which is the one part with a fixing scheme worth stating, ran its
    # notes straight through the GENERAL block and off the sheet.
    S.label(ax, 30, 118, "NOTES", 6.6, weight="bold")
    for i, ln in enumerate(NOTES.get(name, ["--"])):
        col, row = divmod(i, 20)
        S.label(ax, 30 + col * 145.0, 111 - row * 4.8, ln, 5.4)
    S.label(ax, 270, 118, "GENERAL", 6.6, weight="bold")
    general = [
        "Dimensions in millimetres. Projections are silhouettes of the released mesh,",
        "so this drawing and the STEP and STL files cannot disagree.",
        "General tolerance +/-0.30 mm or +/-0.5 % of the dimension, whichever is greater,",
        "which is the normal MJF PA12 capability. Critical fits are called out above.",
        "Finish: bead-blasted, dyed graphite. No paint on any skin-contact surface.",
    ] + MARKING.get(name, MARKING_DEFAULT)
    for i, ln in enumerate(general):
        S.label(ax, 270, 111 - i * 4.8, ln, 5.4, color="#4a5c68")
    fig.tight_layout(pad=0.2)
    pdf.savefig(fig)
    if png_dir:
        fig.savefig(os.path.join(png_dir, f"drawing_{name}.png"), dpi=150)
    plt.close(fig)


def render(stl_path, out_png, title, elev=24, azim=-56, color="#c8d4de"):
    mesh = trimesh.load(stl_path)
    mesh.apply_translation(-mesh.centroid)
    fig = plt.figure(figsize=(7.0, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    tris = mesh.triangles
    n = mesh.face_normals
    e, a = math.radians(elev), math.radians(azim)
    view = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    facing = n @ view > -0.02                      # cull the back faces
    tris, n = tris[facing], n[facing]
    depth = tris.mean(axis=1) @ view               # painter's algorithm, far first
    order = np.argsort(depth)
    tris, n = tris[order], n[order]
    light = np.array([0.45, -0.65, 0.62])
    light /= np.linalg.norm(light)
    shade = np.clip(n @ light, 0.10, 1.0)
    base = np.array([int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)]) / 255.0
    cols = np.clip(base[None, :] * (0.32 + 0.78 * shade[:, None]), 0, 1)
    pc = Poly3DCollection(tris, facecolors=cols, edgecolors=(0, 0, 0, 0.10),
                          linewidths=0.12, zsort="min")
    ax.add_collection3d(pc)
    s = mesh.extents.max() / 2 * 1.15
    ax.set_xlim(-s, s)
    ax.set_ylim(-s, s)
    ax.set_zlim(-s, s)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=10, color="#12212e")
    fig.tight_layout(pad=0.1)
    fig.savefig(out_png, dpi=170, facecolor="white")
    plt.close(fig)
    return out_png


def build(mech_dir, out_pdf, png_dir=None, index_csv=None):
    """Paginate one sheet per released mesh, in filename order, and record which sheet
    each part landed on.

    The sheet set follows `mech/stl/`, so adding a mesh renumbers every sheet after it.
    PARTS-EEG-019 cites these numbers by hand and drifted two pages when HM-01 and the
    carrier outline joined the set, so the index below is written as the PDF is built and
    the citations can be checked against it instead of read off a printout.
    """
    stl_dir = os.path.join(mech_dir, "stl")
    names = sorted(n[:-4] for n in os.listdir(stl_dir) if n.endswith(".stl"))
    if png_dir:
        os.makedirs(png_dir, exist_ok=True)
    index = []
    with PdfPages(out_pdf) as pdf:
        for i, n in enumerate(names, start=1):
            part_sheet(pdf, png_dir, os.path.join(stl_dir, n + ".stl"), n, i, len(names))
            index.append((i, PART_ID.get(n, n.split("_")[0]), n + ".stl"))
    if index_csv:
        with open(index_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["sheet", "of", "part_id", "stl"])
            for i, pid, stl in index:
                w.writerow([i, len(names), pid, stl])
    if png_dir:
        for n in names:
            render(os.path.join(stl_dir, n + ".stl"),
                   os.path.join(png_dir, f"render_{n}.png"),
                   n.replace("_", " "))
    return out_pdf


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    pkg = os.path.dirname(here)
    mech = os.path.join(pkg, "mech")
    out = os.path.join(mech, "drawings", "MECH-EEG-020_RevA_printed_part_drawings.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    idx = os.path.join(mech, "drawings", "MECH-EEG-020_sheet_index.csv")
    print(build(mech, out, os.path.join(mech, "renders"), index_csv=idx))
    print(idx)
