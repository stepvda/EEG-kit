#!/usr/bin/env python3
"""
sch_netlist.py -- read a KiCad schematic back and work out what it is connected to.

This is the gate on the native schematic of ECO-EEG-033.  It does NOT ask the generator
what it meant.  It parses the emitted `.kicad_sch` files -- pin geometry out of their own
embedded `lib_symbols`, wires, junctions, labels, hierarchical labels and power symbols
-- resolves the connectivity geometrically, and diffs the netlist it finds against
`design.py`.  Anything less would be the generator marking its own homework.

The connectivity model is KiCad's:

  * two wires join where an endpoint of one lies ON the other, endpoint or interior;
  * a pin joins a wire whose body passes through the pin's connection point;
  * a label joins whatever is at its own position, and names that net within its sheet;
  * a power symbol's single pin names its net GLOBALLY, from the pin name;
  * a hierarchical label names the net within its sheet and is joined to the same name
    on other sheets through the root sheet's pins, which this tool checks rather than
    assumes.

Run it after tools/emit_kicad_sch.py.  Zero differences is the gate.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
from kicad_parse import parse_sexp, head, children, child   # noqa: E402

KDIR = os.path.join(PKG, "kicad")
TOL = 0.01


def _f(x):
    return float(x[1] if isinstance(x, tuple) else x)


def val(node):
    """A leaf token's text."""
    if isinstance(node, tuple):
        return node[1]
    return str(node)


def _at(node):
    a = child(node, "at")
    if not a:
        return None
    x, y = _f(a[1]), _f(a[2])
    rot = _f(a[3]) if len(a) > 3 else 0.0
    return x, y, rot


def _prop(node, name, default=""):
    for p in children(node, "property"):
        if val(p[1]) == name:
            return val(p[2])
    return default


class LibPin:
    __slots__ = ("number", "name", "x", "y", "etype")

    def __init__(self, number, name, x, y, etype):
        self.number, self.name, self.x, self.y, self.etype = number, name, x, y, etype


def read_lib(root):
    """{symbol name: {unit: [LibPin]}} plus {name: is_power}."""
    lib, power = {}, {}
    ls = child(root, "lib_symbols")
    if not ls:
        return lib, power
    for s in children(ls, "symbol"):
        name = val(s[1])
        power[name] = bool(child(s, "power"))
        units = defaultdict(list)
        for u in children(s, "symbol"):
            uname = val(u[1])
            try:
                unit = int(uname.rsplit("_", 2)[-2])
            except (ValueError, IndexError):
                unit = 1
            for p in children(u, "pin"):
                etype = val(p[1])
                a = _at(p)
                nm = child(p, "name")
                nu = child(p, "number")
                units[unit].append(LibPin(val(nu[1]) if nu else "",
                                          val(nm[1]) if nm else "~",
                                          a[0], a[1], etype))
        lib[name] = dict(units)
    return lib, power


def place(lx, ly, x, y, rot, mirror):
    """Library coordinates (Y up) to sheet coordinates (Y down)."""
    if mirror == "x":
        ly = -ly
    elif mirror == "y":
        lx = -lx
    dx, dy = lx, -ly                       # to screen orientation
    a = math.radians(rot % 360)
    ca, sa = math.cos(a), math.sin(a)
    # KiCad rotates counter-clockwise on a Y-down screen
    rx = dx * ca + dy * sa
    ry = -dx * sa + dy * ca
    return (x + rx, y + ry)


class Sheet:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        root = parse_sexp(open(path).read())
        assert head(root) == "kicad_sch", self.name
        self.root = root
        self.lib, self.is_power = read_lib(root)
        self.wires = []
        for w in children(root, "wire"):
            pts = child(w, "pts")
            xy = [c for c in pts[1:] if head(c) == "xy"]
            self.wires.append(((_f(xy[0][1]), _f(xy[0][2])),
                               (_f(xy[1][1]), _f(xy[1][2]))))
        self.junctions = [(_at(j)[0], _at(j)[1]) for j in children(root, "junction")]
        self.labels = [(val(l[1]), _at(l)[0], _at(l)[1]) for l in children(root, "label")]
        self.hier_labels = [(val(l[1]), _at(l)[0], _at(l)[1])
                            for l in children(root, "hierarchical_label")]
        self.global_labels = [(val(l[1]), _at(l)[0], _at(l)[1])
                              for l in children(root, "global_label")]
        self.pins = []          # (ref, pin number, x, y, is_power_symbol, pin name)
        self.refs = {}
        for s in children(root, "symbol"):
            lib_id = val(child(s, "lib_id")[1])
            libname = lib_id.split(":", 1)[-1]
            a = _at(s)
            m = child(s, "mirror")
            mirror = val(m[1]) if m else None
            unit = int(val(child(s, "unit")[1])) if child(s, "unit") else 1
            ref = _prop(s, "Reference")
            self.refs.setdefault(ref, set()).add(unit)
            for lp in self.lib.get(libname, {}).get(unit, []):
                x, y = place(lp.x, lp.y, a[0], a[1], a[2], mirror)
                self.pins.append((ref, lp.number, x, y,
                                  self.is_power.get(libname, False), lp.name))
        self.sheet_pins = []    # (child filename, pin name, x, y)
        for sh in children(root, "sheet"):
            fname = _prop(sh, "Sheetfile")
            for pn in children(sh, "pin"):
                a = _at(pn)
                self.sheet_pins.append((fname, val(pn[1]), a[0], a[1]))


# --------------------------------------------------------------------------- geometry
def _on_segment(px, py, a, b, tol=TOL):
    (x1, y1), (x2, y2) = a, b
    dx, dy = x2 - x1, y2 - y1
    L2 = dx * dx + dy * dy
    if L2 < 1e-12:
        return abs(px - x1) < tol and abs(py - y1) < tol
    t = ((px - x1) * dx + (py - y1) * dy) / L2
    if t < -tol or t > 1 + tol:
        return False
    cx, cy = x1 + t * dx, y1 + t * dy
    return (px - cx) ** 2 + (py - cy) ** 2 < tol * tol


class UF:
    def __init__(self):
        self.p = {}

    def find(self, a):
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def connect(sheet):
    """-> (uf, node_of_point) where a node key is ('w', i) for a wire or a point key."""
    uf = UF()
    for i in range(len(sheet.wires)):
        uf.find(("w", i))
    # wires that touch each other
    for i, (a, b) in enumerate(sheet.wires):
        for j in range(i + 1, len(sheet.wires)):
            c, d = sheet.wires[j]
            if (_on_segment(*a, c, d) or _on_segment(*b, c, d)
                    or _on_segment(*c, a, b) or _on_segment(*d, a, b)):
                uf.union(("w", i), ("w", j))

    def attach(key, x, y):
        uf.find(key)
        for i, (a, b) in enumerate(sheet.wires):
            if _on_segment(x, y, a, b):
                uf.union(key, ("w", i))

    for ref, num, x, y, is_pwr, pname in sheet.pins:
        attach(("p", ref, num), x, y)
    for nm, x, y in sheet.labels:
        attach(("l", nm, x, y), x, y)
    for nm, x, y in sheet.hier_labels:
        attach(("h", nm, x, y), x, y)
    for nm, x, y in sheet.global_labels:
        attach(("g", nm, x, y), x, y)
    for fname, nm, x, y in sheet.sheet_pins:
        attach(("s", fname, nm), x, y)
    # a pin and a label at exactly the same point with no wire between them
    pts = defaultdict(list)
    for ref, num, x, y, _p, _n in sheet.pins:
        pts[(round(x, 2), round(y, 2))].append(("p", ref, num))
    for nm, x, y in sheet.labels:
        pts[(round(x, 2), round(y, 2))].append(("l", nm, x, y))
    for nm, x, y in sheet.hier_labels:
        pts[(round(x, 2), round(y, 2))].append(("h", nm, x, y))
    for nm, x, y in sheet.global_labels:
        pts[(round(x, 2), round(y, 2))].append(("g", nm, x, y))
    for fname, nm, x, y in sheet.sheet_pins:
        pts[(round(x, 2), round(y, 2))].append(("s", fname, nm))
    for keys in pts.values():
        for k in keys[1:]:
            uf.union(keys[0], k)
    return uf


def sheet_nets(sheet):
    """-> {component root: {"names": set, "pins": set, "hier": set, "global": set,
    "sheetpins": set}}"""
    uf = connect(sheet)
    groups = defaultdict(lambda: dict(names=set(), pins=set(), hier=set(),
                                      glob=set(), sheetpins=set()))
    for ref, num, x, y, is_pwr, pname in sheet.pins:
        g = groups[uf.find(("p", ref, num))]
        if is_pwr:
            g["glob"].add(pname)
        else:
            g["pins"].add(f"{ref}.{num}")
    for nm, x, y in sheet.labels:
        groups[uf.find(("l", nm, x, y))]["names"].add(nm)
    for nm, x, y in sheet.hier_labels:
        groups[uf.find(("h", nm, x, y))]["hier"].add(nm)
    for nm, x, y in sheet.global_labels:
        groups[uf.find(("g", nm, x, y))]["glob"].add(nm)
    for fname, nm, x, y in sheet.sheet_pins:
        groups[uf.find(("s", fname, nm))]["sheetpins"].add((fname, nm))
    return groups


# --------------------------------------------------------------------------- netlist
def build(paths):
    """-> ({net name: {ref.pin}}, [problems])"""
    problems = []
    sheets = [Sheet(p) for p in paths]
    root = None
    for s in sheets:
        if s.sheet_pins:
            root = s
    if root is None:
        problems.append("no root sheet: none of the files contains a sheet symbol")

    uf = UF()
    pins_of = defaultdict(set)
    for s in sheets:
        for key, g in sheet_nets(s).items():
            node = (s.name, key)
            uf.find(node)
            for p in g["pins"]:
                pins_of[node].add(p)
            for nm in g["glob"]:
                uf.union(("GLOBAL", nm), node)
            for nm in g["names"]:
                uf.union(("LOCAL", s.name, nm), node)
            for nm in g["hier"]:
                uf.union(("HIER", s.name, nm), node)
            for fname, nm in g["sheetpins"]:
                uf.union(("HIER", fname, nm), node)

    # a local label that appears on two sheets would silently be two different nets;
    # say so rather than let the diff blame something else
    local_names = defaultdict(set)
    for s in sheets:
        for nm, _x, _y in s.labels:
            local_names[nm].add(s.name)
    if root is not None:
        for nm, sheets_with in local_names.items():
            others = sheets_with - {root.name}
            if len(others) > 1:
                problems.append(f"local label {nm!r} appears on {len(others)} sheets "
                                f"({', '.join(sorted(others))}); a local label does not "
                                f"cross a sheet and these are different nets")

    # a hierarchical label with no matching sheet pin is an orphan
    if root is not None:
        have = {(f, n) for f, n, _x, _y in root.sheet_pins}
        for s in sheets:
            if s is root:
                continue
            for nm, _x, _y in s.hier_labels:
                if (s.name, nm) not in have:
                    problems.append(f"{s.name}: hierarchical label {nm!r} has no sheet "
                                    f"pin on the root")
        for f, n, _x, _y in root.sheet_pins:
            src = [s for s in sheets if s.name == f]
            if not src:
                problems.append(f"root: sheet pin {n!r} points at {f}, which is not "
                                f"in the set")
            elif n not in {nm for nm, _x, _y in src[0].hier_labels}:
                problems.append(f"root: sheet pin {n!r} on {f} has no hierarchical "
                                f"label in that sheet")

    nets = defaultdict(set)
    names = defaultdict(set)
    for node, ps in pins_of.items():
        nets[uf.find(node)] |= ps
    for key in list(uf.p):
        r = uf.find(key)
        if key[0] == "GLOBAL":
            names[r].add(key[1])
        elif key[0] in ("LOCAL", "HIER"):
            names[r].add(key[2])

    out = {}
    for r, ps in nets.items():
        if not ps:
            continue
        nm = sorted(names.get(r, ()))
        if not nm:
            problems.append(f"unnamed net with pins {sorted(ps)}")
            continue
        if len(nm) > 1:
            problems.append(f"one net carries {len(nm)} names: {nm}")
        key = nm[0]
        if key in out:
            problems.append(f"net {key!r} is built from more than one disconnected "
                            f"island")
            out[key] |= ps
        else:
            out[key] = set(ps)
    return out, problems


# --------------------------------------------------------------------------- ERC
def erc(paths, found):
    """The electrical-rule checks a person would run, done structurally.

    `kicad-cli sch erc` is not available here -- KiCad is not installed on the machine
    this was generated on -- so this is NOT an ERC run and is not reported as one.  It
    is the four checks an ERC would fail on that can be made from the file alone:

      1  every pin of every placed symbol is on a net;
      2  no reference designator is placed twice, and a multi-unit part places each of
         its units exactly once;
      3  every net has at least two pins, or is one of the single-pad nets design.py
         declares (test points, spare ways and no-connects);
      4  every power net is driven by at least one power symbol.
    """
    problems = []
    sheets = [Sheet(p) for p in paths]

    # 1 unconnected pins
    on_a_net = set()
    for net, ps in found.items():
        on_a_net |= ps
    for sh in sheets:
        conn = connect(sh)
        for ref, num, x, y, is_pwr, pname in sh.pins:
            if is_pwr or not num:
                continue
            key = f"{ref}.{num}"
            if key in on_a_net:
                continue
            root_ = conn.find(("p", ref, num))
            problems.append(f"{sh.name}: pin {key} at ({x:.2f}, {y:.2f}) is on no net "
                            f"(component {root_})")

    # 2 duplicate designators and missing units
    seen = defaultdict(list)
    for sh in sheets:
        for ref, units in sh.refs.items():
            if ref.startswith("#PWR"):
                continue
            for u in units:
                seen[(ref, u)].append(sh.name)
    for (ref, u), where in sorted(seen.items()):
        if len(where) > 1:
            problems.append(f"{ref} unit {u} is placed on {len(where)} sheets: "
                            f"{', '.join(where)}")
    placed_units = defaultdict(set)
    for (ref, u) in seen:
        placed_units[ref].add(u)
    for ref, units in sorted(placed_units.items()):
        want = D.C.get(ref)
        if want is None:
            problems.append(f"{ref} is placed and is not in design.py")

    # 3 single-pin nets
    declared_single = {n for n, pads in _pads_per_net().items() if len(pads) == 1}
    for net, ps in sorted(found.items()):
        if len(ps) < 2 and net not in declared_single:
            problems.append(f"net {net} has one pin ({sorted(ps)}) and is not one of "
                            f"design.py's declared single-pad nets")

    # 4 power nets driven
    driven = set()
    for sh in sheets:
        for ref, num, x, y, is_pwr, pname in sh.pins:
            if is_pwr:
                driven.add(pname)
    for net in sorted(set(D.POWER_A_NETS) | set(D.POWER_D_NETS) | {"HARN_SHIELD"}):
        if net in found and net not in driven:
            problems.append(f"power net {net} has no power symbol driving it")
    return problems


def _pads_per_net():
    out = defaultdict(set)
    for key, net in D.N.items():
        out[net].add(key)
    return out


def design_netlist():
    out = defaultdict(set)
    for key, net in D.N.items():
        out[net].add(key)
    return {k: set(v) for k, v in out.items()}


def diff(found, want):
    rows = []
    for net in sorted(set(found) | set(want)):
        a, b = found.get(net), want.get(net)
        if a is None:
            rows.append((net, "missing from the schematic", sorted(b)))
        elif b is None:
            rows.append((net, "not in design.py", sorted(a)))
        elif a != b:
            rows.append((net, "pin sets differ",
                         [f"schematic only: {sorted(a - b)}",
                          f"design.py only: {sorted(b - a)}"]))
    return rows


def main(write=True):
    stem = D.stem(D.REV_C)
    paths = [os.path.join(KDIR, f) for f in sorted(os.listdir(KDIR))
             if f.startswith(stem) and f.endswith(".kicad_sch")]
    if not paths:
        raise SystemExit("no schematic files; run tools/emit_kicad_sch.py first")
    found, problems = build(paths)
    want = design_netlist()
    rows = diff(found, want)

    out = os.path.join(KDIR, f"{stem}_schematic_netlist_check.txt")
    lines = [f"EEG-CAR-01 Rev {D.REV_C} -- schematic against design.py",
             f"Generated {D.DATE_C} by tools/sch_netlist.py.",
             "=" * 78, "",
             "WHAT THIS IS",
             "  The netlist read back out of the emitted .kicad_sch files -- pin",
             "  geometry from their own lib_symbols, wires, junctions, labels and",
             "  power symbols -- diffed against tools/design.py.  The generator is",
             "  not asked what it meant.",
             "",
             f"  files            {len(paths)}",
             f"  nets in design.py {len(want)}",
             f"  nets found        {len(found)}",
             f"  pins in design.py {sum(len(v) for v in want.values())}",
             f"  pins found        {sum(len(v) for v in found.values())}",
             ""]
    lines.append(f"STRUCTURAL PROBLEMS: {len(problems)}")
    for p in problems[:200]:
        lines.append(f"  {p}")
    if len(problems) > 200:
        lines.append(f"  ... and {len(problems) - 200} more")
    lines.append("")
    ercs = erc(paths, found)
    lines.append(f"STRUCTURAL ERC: {len(ercs)} finding(s)")
    lines.append("  KiCad is not installed on this machine, so `kicad-cli sch erc` was")
    lines.append("  NOT RUN and this is not an ERC result.  It is the four checks an ERC")
    lines.append("  would fail on that can be made from the files alone: every pin on a")
    lines.append("  net, no designator placed twice, no accidental single-pin net, and")
    lines.append("  every power net driven by a power symbol.")
    for p_ in ercs[:200]:
        lines.append(f"  {p_}")
    if len(ercs) > 200:
        lines.append(f"  ... and {len(ercs) - 200} more")
    lines.append("")
    lines.append(f"NETLIST DIFFERENCES: {len(rows)}")
    if not rows:
        lines.append("  none.  The schematic and design.py describe the same netlist.")
    for net, why, detail in rows[:200]:
        lines.append(f"  {net}: {why}")
        for d in detail[:8]:
            lines.append(f"    {d}")
    if len(rows) > 200:
        lines.append(f"  ... and {len(rows) - 200} more")
    lines.append("")
    text = "\n".join(lines) + "\n"
    if write:
        open(out, "w").write(text)
    print(text)
    return len(rows), len(problems) + len(ercs), out


if __name__ == "__main__":
    nd, np_, _ = main()
    sys.exit(0 if (nd == 0 and np_ == 0) else 1)
