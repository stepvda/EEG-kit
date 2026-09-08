#!/usr/bin/env python3
"""
kicad_sch.py -- the primitives for writing a KiCad 8 hierarchical schematic.

This is the drawing layer: symbols, wires, junctions, labels, hierarchical sheets and
their pins, and the symbol library that goes with them.  `tools/emit_kicad_sch.py` is the
layer above it and decides what goes where.

Two things about it are deliberate.

**Every uuid is derived, not random.**  KiCad identifies everything by uuid, and a
generator that rolls a fresh one on every run produces a file that differs from itself
for no reason -- which makes a diff useless and makes the reviewer's copy and ours
incomparable.  `uid()` is uuid5 over a fixed namespace and a stable key, so the same
schematic emits byte for byte.

**The symbols are generated, not copied.**  ICD-EEG-006 section 1 is the one home of the
connector way tables, so the connector symbols are built from it rather than drawn.  A
symbol whose pin count or pin names disagree with the ICD is then impossible rather than
merely unlikely.

Format: KiCad 8, `(kicad_sch (version 20231120) ...)`.  Coordinates are millimetres with
the origin at the top-left of the sheet and Y increasing downward, which is Eeschema's
convention and the same handedness as `design.py`.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import uuid as _uuid

# A fixed namespace, so that a regeneration reproduces the file.  Any constant would do;
# this one is uuid5 of the DNS name of the programme, and it never changes.
NS = _uuid.uuid5(_uuid.NAMESPACE_DNS, "one.witysk.org/EEG-CAR-01")

MM = 1.27               # the schematic grid Eeschema snaps to

# Landscape sizes, millimetres.  A3 is too small for a board with thirty connectors and
# sixteen protection networks; the analogue sheet needs A1.
PAPERS = {"A4": (297.0, 210.0), "A3": (420.0, 297.0), "A2": (594.0, 420.0),
          "A1": (841.0, 594.0), "A0": (1189.0, 841.0)}
MARGIN = 12.0


def uid(*key):
    return str(_uuid.uuid5(NS, "|".join(str(k) for k in key)))


def esc(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def n(v):
    """KiCad writes coordinates with up to four decimals and no trailing zeros."""
    return f"{v:.4f}".rstrip("0").rstrip(".") or "0"


# --------------------------------------------------------------------------- effects
def _eff(size=1.27, hide=False, justify=None, bold=False, italic=False):
    f = f"(font (size {n(size)} {n(size)})"
    if bold:
        f += " (bold yes)"
    if italic:
        f += " (italic yes)"
    f += ")"
    j = f" (justify {justify})" if justify else ""
    h = " (hide yes)" if hide else ""
    return f"(effects {f}{j}{h})"


# --------------------------------------------------------------------------- library
class Pin:
    def __init__(self, number, name, x, y, angle, length=2.54, etype="passive",
                 shape="line"):
        self.number, self.name = str(number), name
        self.x, self.y, self.angle = x, y, angle
        self.length, self.etype, self.shape = length, etype, shape

    def sexp(self, hide_names=False, hide_numbers=False):
        nm = _eff(1.27, hide=hide_names)
        nu = _eff(1.27, hide=hide_numbers)
        return (f'      (pin {self.etype} {self.shape} (at {n(self.x)} {n(self.y)} '
                f'{n(self.angle)}) (length {n(self.length)})\n'
                f'        (name "{esc(self.name)}" {nm})\n'
                f'        (number "{esc(self.number)}" {nu}))')


class LibSymbol:
    """One library symbol.  `units` maps a unit number to its graphics and pins, so a
    quad op-amp is four amplifier units and one power unit rather than a 14-pin box."""

    def __init__(self, name, ref_prefix, description="", power=False,
                 hide_pin_numbers=False, hide_pin_names=False, keywords=""):
        self.name = name
        self.ref_prefix = ref_prefix
        self.description = description
        self.power = power
        self.hide_pin_numbers = hide_pin_numbers
        self.hide_pin_names = hide_pin_names
        self.keywords = keywords
        self.units = {}          # unit number -> {"graphics": [...], "pins": [...]}
        self.ref_at = (0.0, -5.08, 0)
        self.val_at = (0.0, 5.08, 0)

    def unit(self, k):
        return self.units.setdefault(k, {"graphics": [], "pins": []})

    # -- graphics helpers, all in the symbol's own coordinates ----------------
    def rect(self, unit, x1, y1, x2, y2, fill="background"):
        self.unit(unit)["graphics"].append(
            f"      (rectangle (start {n(x1)} {n(y1)}) (end {n(x2)} {n(y2)})\n"
            f"        (stroke (width 0.254) (type default)) (fill (type {fill})))")

    def poly(self, unit, pts, width=0.254, fill="none"):
        p = " ".join(f"(xy {n(x)} {n(y)})" for x, y in pts)
        self.unit(unit)["graphics"].append(
            f"      (polyline (pts {p})\n"
            f"        (stroke (width {n(width)}) (type default)) "
            f"(fill (type {fill})))")

    def circle(self, unit, cx, cy, r, fill="none"):
        self.unit(unit)["graphics"].append(
            f"      (circle (center {n(cx)} {n(cy)}) (radius {n(r)})\n"
            f"        (stroke (width 0.254) (type default)) (fill (type {fill})))")

    def text(self, unit, x, y, s, size=1.0):
        self.unit(unit)["graphics"].append(
            f'      (text "{esc(s)}" (at {n(x)} {n(y)} 0) {_eff(size)})')

    def pin(self, unit, *a, **k):
        self.unit(unit)["pins"].append(Pin(*a, **k))

    def pins_of(self, unit):
        return self.units.get(unit, {"pins": []})["pins"]

    def all_pins(self):
        out = {}
        for u, d in self.units.items():
            for p in d["pins"]:
                out[p.number] = (u, p)
        return out

    def n_units(self):
        return max(self.units) if self.units else 1

    def sexp(self):
        L = [f'    (symbol "{esc(self.name)}"']
        if self.power:
            L.append("      (power)")
        if self.hide_pin_numbers:
            L.append("      (pin_numbers (hide yes))")
        L.append("      (pin_names (offset 0.254))")
        L.append("      (exclude_from_sim no) (in_bom yes) (on_board yes)")
        rx, ry, ra = self.ref_at
        vx, vy, va = self.val_at
        L.append(f'      (property "Reference" "{esc(self.ref_prefix)}" '
                 f'(at {n(rx)} {n(ry)} {n(ra)}) {_eff(1.27, justify="left")})')
        L.append(f'      (property "Value" "{esc(self.name)}" '
                 f'(at {n(vx)} {n(vy)} {n(va)}) {_eff(1.27, justify="left")})')
        L.append(f'      (property "Footprint" "" (at 0 0 0) {_eff(1.27, hide=True)})')
        L.append(f'      (property "Datasheet" "~" (at 0 0 0) {_eff(1.27, hide=True)})')
        L.append(f'      (property "Description" "{esc(self.description)}" '
                 f'(at 0 0 0) {_eff(1.27, hide=True)})')
        if self.keywords:
            L.append(f'      (property "ki_keywords" "{esc(self.keywords)}" '
                     f'(at 0 0 0) {_eff(1.27, hide=True)})')
        for u in sorted(self.units):
            d = self.units[u]
            L.append(f'      (symbol "{esc(self.name)}_{u}_1"')
            L += ["  " + g for g in d["graphics"]]
            L += ["  " + p.sexp(self.hide_pin_names, self.hide_pin_numbers)
                  for p in d["pins"]]
            L.append("      )")
        L.append("    )")
        return "\n".join(L)


# --------------------------------------------------------------------------- sheet
class Sheet:
    """One .kicad_sch file."""

    def __init__(self, filename, name, title, page, rev, date, company,
                 comments=(), root=False, root_uuid=None, project="EEG-CAR-01_RevC",
                 paper="A2"):
        self.filename = filename
        self.name = name
        self.title = title
        self.page = str(page)
        self.rev, self.date, self.company = rev, date, company
        self.comments = list(comments)
        self.root = root
        self.uuid = uid("sheetfile", filename)
        self.root_uuid = root_uuid or self.uuid
        self.project = project
        self.paper = paper
        self.extent = [1e9, 1e9, -1e9, -1e9]     # x0, y0, x1, y1 of everything drawn
        self.lib = {}            # symbol name -> LibSymbol
        self.items = []          # raw s-expressions
        self.symbols = []        # (ref, lib_name, x, y, rot, unit, props, pin_numbers)
        self.child_sheets = []   # (Sheet, x, y, w, h, [(name, shape, dx, dy, side)])
        self._instance_path = "/" if root else f"/{self.root_uuid}"

    # -- content -------------------------------------------------------------
    def use(self, libsym):
        self.lib[libsym.name] = libsym
        return libsym

    def _seen(self, *xy):
        for i in range(0, len(xy), 2):
            x, y = xy[i], xy[i + 1]
            self.extent[0] = min(self.extent[0], x)
            self.extent[1] = min(self.extent[1], y)
            self.extent[2] = max(self.extent[2], x)
            self.extent[3] = max(self.extent[3], y)

    def wire(self, x1, y1, x2, y2):
        self._seen(x1, y1, x2, y2)
        self.items.append(
            f"  (wire (pts (xy {n(x1)} {n(y1)}) (xy {n(x2)} {n(y2)}))\n"
            f"    (stroke (width 0) (type default))\n"
            f'    (uuid "{uid(self.filename, "w", x1, y1, x2, y2)}"))')

    def polyline(self, pts, width=0.15, style="dash"):
        p = " ".join(f"(xy {n(x)} {n(y)})" for x, y in pts)
        self.items.append(
            f"  (polyline (pts {p})\n"
            f"    (stroke (width {n(width)}) (type {style}))\n"
            f'    (uuid "{uid(self.filename, "poly", *[c for xy in pts for c in xy])}"))')

    def junction(self, x, y):
        self._seen(x, y)
        self.items.append(
            f"  (junction (at {n(x)} {n(y)}) (diameter 0) (color 0 0 0 0)\n"
            f'    (uuid "{uid(self.filename, "j", x, y)}"))')

    def label(self, name, x, y, rot=0, justify="left bottom"):
        self._seen(x, y, x + 2.0 * len(name), y)
        self.items.append(
            f'  (label "{esc(name)}" (at {n(x)} {n(y)} {n(rot)})\n'
            f"    {_eff(1.27, justify=justify)}\n"
            f'    (uuid "{uid(self.filename, "lbl", name, x, y)}"))')

    def hier_label(self, name, x, y, rot=0, shape="passive", justify="left"):
        self._seen(x, y, x + 2.0 * len(name), y)
        self.items.append(
            f'  (hierarchical_label "{esc(name)}" (shape {shape}) '
            f"(at {n(x)} {n(y)} {n(rot)})\n"
            f"    {_eff(1.27, justify=justify)}\n"
            f'    (uuid "{uid(self.filename, "hlbl", name, x, y)}"))')

    def text(self, s, x, y, size=1.6, rot=0, justify="left"):
        self._seen(x, y, x + 0.65 * size * len(s), y)
        self.items.append(
            f'  (text "{esc(s)}" (at {n(x)} {n(y)} {n(rot)})\n'
            f"    {_eff(size, justify=justify)}\n"
            f'    (uuid "{uid(self.filename, "txt", s, x, y)}"))')

    def box(self, x1, y1, x2, y2, note=""):
        self._seen(x1, y1, x2, y2)
        self.items.append(
            f"  (rectangle (start {n(x1)} {n(y1)}) (end {n(x2)} {n(y2)})\n"
            f"    (stroke (width 0.1) (type dash)) (fill (type none))\n"
            f'    (uuid "{uid(self.filename, "box", x1, y1, x2, y2, note)}"))')

    def place(self, ref, libname, x, y, rot=0, unit=1, value="", footprint="",
              datasheet="~", extra_props=(), mirror=None, hide_value=False,
              dnp=False):
        sy = self.lib.get(libname)
        if sy is not None:
            xs = [q.x for d in sy.units.values() for q in d["pins"]] or [0.0]
            ys = [q.y for d in sy.units.values() for q in d["pins"]] or [0.0]
            self._seen(x + min(xs), y - max(ys), x + max(xs), y - min(ys))
        else:
            self._seen(x, y)
        self.symbols.append(dict(ref=ref, lib=libname, x=x, y=y, rot=rot, unit=unit,
                                 value=value, footprint=footprint, datasheet=datasheet,
                                 extra=list(extra_props), mirror=mirror,
                                 hide_value=hide_value, dnp=dnp))

    def add_child(self, child, x, y, w, h, pins):
        self._seen(x, y - 6.0, x + w, y + h + 6.0)
        """pins: [(net name, shape, side, offset)] with side in l/r and offset in mm
        down from the sheet symbol's top edge."""
        self.child_sheets.append((child, x, y, w, h, pins))

    # -- output --------------------------------------------------------------
    def _symbol_sexp(self, s):
        libsym = self.lib[s["lib"]]
        L = [f'  (symbol (lib_id "EEG-CAR-01:{esc(s["lib"])}") '
             f'(at {n(s["x"])} {n(s["y"])} {n(s["rot"])})']
        if s["mirror"]:
            L.append(f'    (mirror {s["mirror"]})')
        L.append(f'    (unit {s["unit"]})')
        L.append("    (exclude_from_sim no) (in_bom yes) (on_board yes) "
                 f'(dnp {"yes" if s["dnp"] else "no"})')
        L.append(f'    (uuid "{uid(self.filename, "sym", s["ref"], s["unit"])}")')
        rx, ry = s["x"], s["y"] - 5.08
        vx, vy = s["x"], s["y"] + 5.08
        L.append(f'    (property "Reference" "{esc(s["ref"])}" '
                 f'(at {n(rx)} {n(ry)} 0) {_eff(1.27, justify="left")})')
        L.append(f'    (property "Value" "{esc(s["value"])}" '
                 f'(at {n(vx)} {n(vy)} 0) '
                 f'{_eff(1.0, hide=s["hide_value"], justify="left")})')
        L.append(f'    (property "Footprint" "{esc(s["footprint"])}" '
                 f'(at {n(s["x"])} {n(s["y"])} 0) {_eff(1.27, hide=True)})')
        L.append(f'    (property "Datasheet" "{esc(s["datasheet"])}" '
                 f'(at {n(s["x"])} {n(s["y"])} 0) {_eff(1.27, hide=True)})')
        for k, val in s["extra"]:
            L.append(f'    (property "{esc(k)}" "{esc(val)}" '
                     f'(at {n(s["x"])} {n(s["y"])} 0) {_eff(1.27, hide=True)})')
        for num, (u, _p) in sorted(libsym.all_pins().items(),
                                   key=lambda kv: (kv[1][0], kv[0])):
            if u != s["unit"]:
                continue
            L.append(f'    (pin "{esc(num)}" '
                     f'(uuid "{uid(self.filename, "pin", s["ref"], s["unit"], num)}"))')
        L.append(f'    (instances (project "{esc(self.project)}"')
        L.append(f'      (path "{self._instance_path}"')
        L.append(f'        (reference "{esc(s["ref"])}") (unit {s["unit"]}))))')
        L.append("  )")
        return "\n".join(L)

    def _child_sexp(self, child, x, y, w, h, pins):
        L = [f"  (sheet (at {n(x)} {n(y)}) (size {n(w)} {n(h)}) (fields_autoplaced yes)",
             "    (stroke (width 0.1524) (type solid))",
             "    (fill (color 0 0 0 0.0000))",
             f'    (uuid "{child.uuid}")',
             f'    (property "Sheetname" "{esc(child.name)}" '
             f'(at {n(x)} {n(y - 1.0)} 0) {_eff(1.6, justify="left bottom")})',
             f'    (property "Sheetfile" "{esc(child.filename)}" '
             f'(at {n(x)} {n(y + h + 1.5)} 0) {_eff(1.0, justify="left top")})']
        for name, shape, side, off in pins:
            px = x if side == "l" else x + w
            py = y + off
            rot = 180 if side == "l" else 0
            L.append(f'    (pin "{esc(name)}" {shape} (at {n(px)} {n(py)} {rot})')
            L.append(f"      {_eff(1.0, justify='right' if side == 'l' else 'left')}")
            L.append(f'      (uuid "{uid(self.filename, "spin", child.filename, name)}"))')
        L.append(f'    (instances (project "{esc(self.project)}"')
        L.append(f'      (path "/{self.root_uuid}" (page "{child.page}"))))')
        L.append("  )")
        return "\n".join(L)

    def render(self):
        L = ["(kicad_sch",
             "  (version 20231120)",
             '  (generator "eeg-car-01-generator")',
             '  (generator_version "8.0")',
             f'  (uuid "{self.uuid}")',
             f'  (paper "{self.paper}")',
             "  (title_block",
             f'    (title "{esc(self.title)}")',
             f'    (date "{esc(self.date)}")',
             f'    (rev "{esc(self.rev)}")',
             f'    (company "{esc(self.company)}")']
        for i, c in enumerate(self.comments[:9], start=1):
            L.append(f'    (comment {i} "{esc(c)}")')
        L.append("  )")
        L.append("  (lib_symbols")
        for name in sorted(self.lib):
            L.append(self.lib[name].sexp())
        L.append("  )")
        L += self.items
        for s in self.symbols:
            L.append(self._symbol_sexp(s))
        for child, x, y, w, h, pins in self.child_sheets:
            L.append(self._child_sexp(child, x, y, w, h, pins))
        if self.root:
            L.append('  (sheet_instances (path "/" (page "1")))')
        else:
            L.append(f'  (sheet_instances (path "/" (page "{self.page}")))')
        L.append(")")
        return "\n".join(L) + "\n"

    def fits(self):
        """Everything drawn, against the page it is drawn on.

        Content that runs off the sheet is invisible in a PDF export and reaches a
        reviewer as "the schematic is missing the comparator".  The build fails rather
        than emitting it.
        """
        w, h = PAPERS[self.paper]
        x0, y0, x1, y1 = self.extent
        if x1 < x0:
            return True, ""
        bad = []
        if x0 < MARGIN or y0 < MARGIN:
            bad.append(f"top-left ({x0:.0f}, {y0:.0f}) is inside the {MARGIN:.0f} mm "
                       f"margin")
        if x1 > w - MARGIN or y1 > h - MARGIN:
            bad.append(f"bottom-right ({x1:.0f}, {y1:.0f}) is outside "
                       f"{w - MARGIN:.0f} x {h - MARGIN:.0f} on {self.paper}")
        return (not bad), "; ".join(bad)

    def write(self, path):
        ok, why = self.fits()
        if not ok:
            raise SystemExit(f"{self.filename}: content does not fit the page -- {why}")
        with open(path, "w") as f:
            f.write(self.render())
        return path


# --------------------------------------------------------------------------- checks
def balanced(text):
    """Parenthesis balance outside quoted strings.  A .kicad_sch that is one bracket
    short does not open at all, and there is no KiCad here to find out for us."""
    depth, in_str, esc_next = 0, False, False
    for ch in text:
        if esc_next:
            esc_next = False
            continue
        if ch == "\\" and in_str:
            esc_next = True
        elif ch == '"':
            in_str = not in_str
        elif not in_str:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth < 0:
                    return False, "closing bracket with nothing open"
    if in_str:
        return False, "file ends inside a quoted string"
    return (depth == 0), (f"{depth} bracket(s) unclosed" if depth else "")
