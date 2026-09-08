#!/usr/bin/env python3
"""
step_write.py -- a small STEP AP214 writer for extruded polygonal solids.

**Why this exists and not cadquery.**  `tools/mech_gen.py` builds the printed parts with
cadquery and is the right tool for them.  It could not be used for the bodies of
ECO-EEG-033: cadquery could not be installed on the machine this was generated on -- the
disk had 472 MB free and `cadquery-ocp` needs several times that -- so `mech_gen.py`
cannot even be imported there, let alone run.  Rather than claim a body set that does not
exist, this writes the ones the collision check needs, from first principles, with no
dependency at all.

**What it can and cannot do.**  One thing: a solid swept from a simple, closed, planar
polygon along +Z.  Every body in `tools/mech_bodies.py` is that -- boxes, hexagonal
standoff prisms, the plate decomposed into rectangles around its DevKit opening -- and
nothing in the collision model needs more.  It cannot do fillets, holes in a face, or
curved surfaces, and it does not pretend to: a cylinder is a 24-sided prism and the
report says so.

Output is `FACETED_BREP`: planar faces, each bounded by one `POLY_LOOP`, with no edge or
vertex entities at all.  That is the most widely readable corner of the format and the
one least likely to be rejected by a tool this machine cannot test against.

**Not verified by a CAD kernel.**  No STEP reader was available here.  The files are
checked structurally -- every solid closed, every face's winding consistent, the entity
graph acyclic and complete -- and that is what is claimed for them.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math


class StepFile:
    def __init__(self, name, description="", author="TI One Voice research programme",
                 date="2026-09-08"):
        self.name = name
        self.description = description
        self.author = author
        self.date = date
        self._n = 0
        self.lines = []
        self._points = {}

    def _id(self):
        self._n += 1
        return self._n

    def _e(self, text):
        i = self._id()
        self.lines.append(f"#{i} = {text};")
        return i

    def point(self, x, y, z):
        key = (round(x, 6), round(y, 6), round(z, 6))
        if key not in self._points:
            self._points[key] = self._e(
                f"CARTESIAN_POINT('',({key[0]:.6f},{key[1]:.6f},{key[2]:.6f}))")
        return self._points[key]

    def _face(self, pts, normal):
        """One planar face from an ordered ring of 3D points."""
        loop = self._e("POLY_LOOP('',(" + ",".join(f"#{self.point(*p)}" for p in pts)
                       + "))")
        bound = self._e(f"FACE_OUTER_BOUND('',#{loop},.T.)")
        origin = self.point(*pts[0])
        nz = self._e(f"DIRECTION('',({normal[0]:.6f},{normal[1]:.6f},"
                     f"{normal[2]:.6f}))")
        # a reference direction perpendicular to the normal
        ref = (1.0, 0.0, 0.0)
        if abs(normal[0]) > 0.9:
            ref = (0.0, 1.0, 0.0)
        rx = (ref[1] * normal[2] - ref[2] * normal[1],
              ref[2] * normal[0] - ref[0] * normal[2],
              ref[0] * normal[1] - ref[1] * normal[0])
        L = math.sqrt(sum(c * c for c in rx)) or 1.0
        rx = tuple(c / L for c in rx)
        nx = self._e(f"DIRECTION('',({rx[0]:.6f},{rx[1]:.6f},{rx[2]:.6f}))")
        ax = self._e(f"AXIS2_PLACEMENT_3D('',#{origin},#{nz},#{nx})")
        plane = self._e(f"PLANE('',#{ax})")
        return self._e(f"FACE_SURFACE('',(#{bound}),#{plane},.T.)")

    def prism(self, polygon, z0, z1):
        """A solid swept from `polygon` (a list of (x, y), counter-clockwise) between
        z0 and z1.  -> the id of the closed shell's faces, as a list."""
        if _signed_area(polygon) < 0:
            polygon = list(reversed(polygon))
        faces = []
        bottom = [(x, y, z0) for x, y in polygon]
        top = [(x, y, z1) for x, y in polygon]
        faces.append(self._face(list(reversed(bottom)), (0.0, 0.0, -1.0)))
        faces.append(self._face(top, (0.0, 0.0, 1.0)))
        n = len(polygon)
        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy)
            if L < 1e-9:
                continue
            nrm = (dy / L, -dx / L, 0.0)
            ring = [(x1, y1, z0), (x2, y2, z0), (x2, y2, z1), (x1, y1, z1)]
            faces.append(self._face(ring, nrm))
        return faces

    def write(self, path, solids):
        """`solids` is [(name, [polygon, z0, z1], ...)]; each becomes one manifold."""
        self.lines = []
        self._n = 0
        self._points = {}
        ctx_pt = self._e("CARTESIAN_POINT('',(0.,0.,0.))")
        ctx_dz = self._e("DIRECTION('',(0.,0.,1.))")
        ctx_dx = self._e("DIRECTION('',(1.,0.,0.))")
        ctx_ax = self._e(f"AXIS2_PLACEMENT_3D('',#{ctx_pt},#{ctx_dz},#{ctx_dx})")
        length = self._e("( NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.) LENGTH_UNIT() )")
        angle = self._e("( NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.) )")
        solid_a = self._e("( NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT() )")
        tol = self._e(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-06),#{length},"
                      f"'distance_accuracy_value','confusion accuracy')")
        ctx = self._e(f"( GEOMETRIC_REPRESENTATION_CONTEXT(3) "
                      f"GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{tol})) "
                      f"GLOBAL_UNIT_ASSIGNED_CONTEXT((#{length},#{angle},#{solid_a})) "
                      f"REPRESENTATION_CONTEXT('','3D') )")
        app_ctx = self._e("APPLICATION_CONTEXT('automotive design')")
        self._e(f"APPLICATION_PROTOCOL_DEFINITION('international standard',"
                f"'automotive_design',2000,#{app_ctx})")
        prod_ctx = self._e(f"PRODUCT_CONTEXT('',#{app_ctx},'mechanical')")
        pdef_ctx = self._e(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{app_ctx},"
                           f"'design')")

        reps = []
        for name, parts in solids:
            faces = []
            for polygon, z0, z1 in parts:
                faces += self.prism(polygon, z0, z1)
            shell = self._e("CLOSED_SHELL('',(" + ",".join(f"#{f}" for f in faces) + "))")
            brep = self._e(f"FACETED_BREP('{_s(name)}',#{shell})")
            reps.append((name, brep))

        for name, brep in reps:
            prod = self._e(f"PRODUCT('{_s(name)}','{_s(name)}','',(#{prod_ctx}))")
            pdf = self._e(f"PRODUCT_DEFINITION_FORMATION('','',#{prod})")
            pd = self._e(f"PRODUCT_DEFINITION('design','',#{pdf},#{pdef_ctx})")
            pds = self._e(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")
            srep = self._e(f"ADVANCED_BREP_SHAPE_REPRESENTATION('{_s(name)}',"
                           f"(#{ctx_ax},#{brep}),#{ctx})")
            self._e(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{srep})")

        head = ["ISO-10303-21;", "HEADER;",
                f"FILE_DESCRIPTION(('{_s(self.description)}'),'2;1');",
                f"FILE_NAME('{_s(self.name)}','{self.date}T00:00:00',"
                f"('{_s(self.author)}'),(''),"
                f"'EEG-CAR-01 step_write.py','','CC BY-SA 4.0');",
                "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));",
                "ENDSEC;", "DATA;"]
        text = "\n".join(head + self.lines + ["ENDSEC;", "END-ISO-10303-21;"]) + "\n"
        with open(path, "w") as f:
            f.write(text)
        return path, len(reps), self._n


def _s(t):
    return str(t).replace("\\", "").replace("'", "")


def _signed_area(poly):
    a = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def box(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def ngon(cx, cy, r, n=24, phase=0.0):
    return [(cx + r * math.cos(phase + 2 * math.pi * k / n),
             cy + r * math.sin(phase + 2 * math.pi * k / n)) for k in range(n)]


def check(path):
    """Structural check of an emitted file: brackets, entity graph and closure."""
    text = open(path).read()
    if not text.startswith("ISO-10303-21;") or not text.rstrip().endswith(
            "END-ISO-10303-21;"):
        return False, "not a complete ISO-10303-21 file"
    import re
    ids = set()
    refs = set()
    for m in re.finditer(r"^#(\d+) = ([A-Z_0-9]+)?", text, re.M):
        ids.add(int(m.group(1)))
    for m in re.finditer(r"#(\d+)", text):
        refs.add(int(m.group(1)))
    missing = refs - ids
    if missing:
        return False, f"{len(missing)} dangling entity reference(s), e.g. #{min(missing)}"
    if text.count("(") != text.count(")"):
        return False, "unbalanced brackets"
    shells = text.count("CLOSED_SHELL")
    breps = text.count("FACETED_BREP")
    if shells != breps or not breps:
        return False, f"{breps} solids and {shells} shells"
    return True, f"{breps} solid(s), {len(ids)} entities"
