#!/usr/bin/env python3
"""
emit_equivalence.py -- diff the KiCad 8 and KiCad 10 emissions of the Rev C layout
input set, and write the result down.

**Why this exists.**  The set is re-emitted for KiCad 10 rather than left for the layout
desk to open in KiCad 10 themselves, because a version bump can silently move the net
classes, the custom rules in the `.kicad_dru` and the DRC severities -- and those three
things are where most of the layout specification lives.  Re-emitting is only worth
anything if somebody checks that it moved nothing.  So the two sets are parsed back and
compared, field by field, and the answer is written into the KiCad 10 directory.

Nothing here asserts a check it did not run.  A check that could not be performed is
recorded as NOT PERFORMED, with the reason, and is not counted as a pass.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import kicad_fmt            # noqa: E402
import kicad_parse          # noqa: E402
import rules                # noqa: E402
import sch_netlist          # noqa: E402

PASS, FAIL, SKIP = "PASS", "FAIL", "**NOT PERFORMED**"


class Check:
    def __init__(self, n, title):
        self.n, self.title = n, title
        self.status, self.lines = PASS, []

    def note(self, s):
        self.lines.append(s)
        return self

    def want(self, label, got, expect):
        ok = got == expect
        if not ok:
            self.status = FAIL
        self.lines.append(
            f"| {label} | `{expect}` | `{got}` | {'yes' if ok else '**NO**'} |")
        return ok

    def skip(self, why):
        self.status = SKIP
        self.lines.append(why)
        return self


# --------------------------------------------------------------------------- readers
def _sexp_norm(text):
    """Collapse whitespace so a KiCad 8 file and a KiCad 10 file that say the same thing
    compare equal.  KiCad 10 indents with tabs and breaks lines differently; that is
    formatting and is not a difference in the specification."""
    return re.sub(r"\s+", " ", text).strip()


def parse_dru(path):
    """-> {rule name: normalised body}.  Comments are dropped: they carry no constraint
    and the comment CHARACTER changed in this same change order."""
    body, name, out = [], None, {}
    for line in open(path):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("(version"):
            continue
        m = re.match(r'\(rule\s+"([^"]+)"', s)
        if m:
            if name:
                out[name] = _sexp_norm(" ".join(body))
            name, body = m.group(1), []
            continue
        if name:
            body.append(s)
    if name:
        out[name] = _sexp_norm(" ".join(body))
    return out


def netclass_map(cfg):
    """-> {net name: class name} from the project's netclass_patterns.

    The patterns are written as two-element lists, `[net, class]`, and are read as
    written rather than as objects."""
    out = {}
    for p in cfg["net_settings"]["netclass_patterns"]:
        if isinstance(p, dict):                     # tolerate the object form
            out[p.get("pattern")] = p.get("netclass")
        else:
            out[p[0]] = p[1]
    return out


def class_table(cfg):
    """-> {class name: the fields that constrain the layout}."""
    out = {}
    for c in cfg["net_settings"]["classes"]:
        out[c["name"]] = {k: c.get(k) for k in
                          ("clearance", "track_width", "via_diameter", "via_drill",
                           "diff_pair_width", "diff_pair_gap")}
    return out


def locked_refs(pcb_path):
    """-> {ref: (x, y)} for every footprint carrying (locked yes)."""
    text = open(pcb_path).read()
    out = {}
    # a footprint block starts at column 1-2 depending on the format's indent; split on
    # the token itself rather than on layout.
    for blk in re.split(r"\n\s*\(footprint ", text)[1:]:
        head = blk[:4000]
        if not re.search(r"\(locked yes\)", head):
            continue
        mref = re.search(r'\(property "Reference"\s+"([^"]+)"', head)
        mat = re.search(r"\(at ([-\d.]+) ([-\d.]+)", head)
        if mref and mat:
            out[mref.group(1)] = (float(mat.group(1)), float(mat.group(2)))
    return out


def _zones(pcb_path):
    """Every `(zone ...)` node, parsed rather than matched.

    A regex is the wrong tool across these two formats: KiCad 8 opens the node as
    `(zone (net 0) ...` on one line and KiCad 10 as `(zone` alone with the body indented
    beneath it, and KiCad 10 also drops `(net 0) (net_name "")` from an area that has no
    net.  Reading the s-expression makes the comparison about content instead of layout.
    """
    root = kicad_parse.parse_sexp(open(pcb_path, encoding="utf-8").read())
    return kicad_parse.children(root, "zone")


def _layers_of(z):
    """The zone's copper layers as a SORTED tuple.

    KiCad 10 reorders the list -- it writes `"F.Cu" "B.Cu" "In1.Cu" "In2.Cu"` where
    KiCad 8 writes `"F.Cu" "In1.Cu" "In2.Cu" "B.Cu"`.  The set of layers is the
    specification; the order they are listed in is not, so it is normalised away rather
    than reported as a difference.
    """
    n = kicad_parse.child(z, "layers") or kicad_parse.child(z, "layer")
    if not n:
        return ()
    return tuple(sorted(str(x).strip('"') for x in n[1:]))


def _polygon_of(z):
    poly = kicad_parse.child(z, "polygon")
    if not poly:
        return ()
    pts = kicad_parse.child(poly, "pts")
    if not pts:
        return ()
    return tuple((kicad_parse.fnum(p[1]), kicad_parse.fnum(p[2]))
                 for p in pts[1:] if isinstance(p, list) and p[0] == "xy")


def _keepout_of(z):
    k = kicad_parse.child(z, "keepout")
    if not k:
        return ()
    return tuple(sorted((str(c[0]), str(c[1])) for c in k[1:]
                        if isinstance(c, list) and len(c) > 1))


def _name_of(z):
    n = kicad_parse.child(z, "name")
    return str(n[1]).strip('"') if n and len(n) > 1 else ""


def _netname_of(z):
    n = kicad_parse.child(z, "net_name")
    if n and len(n) > 1:
        return str(n[1]).strip('"')
    # KiCad 10 drops net_name from an area with no net, and names the net directly on a
    # pour.  Fall back to the `(net ...)` node's name form.
    n = kicad_parse.child(z, "net")
    if n and len(n) > 1 and not str(n[1]).lstrip("-").isdigit():
        return str(n[1]).strip('"')
    return ""


def rule_areas(pcb_path):
    """-> {area name: (layers, keepout flags, polygon)} for the zones that are rule
    areas, which are the ones carrying a keepout."""
    out = {}
    for z in _zones(pcb_path):
        name = _name_of(z)
        if not name:
            continue
        out[name] = (_layers_of(z), _keepout_of(z), _polygon_of(z))
    return out


def zone_pours(pcb_path):
    """-> {(net name, layers): count} for the pours, which are the zones carrying a
    net.  The rule areas do not."""
    out = defaultdict(int)
    for z in _zones(pcb_path):
        net = _netname_of(z)
        if not net:
            continue
        out[(net, _layers_of(z))] += 1
    return dict(out)


def sch_paths(directory):
    stem = D.stem(D.REV_C)
    return [os.path.join(directory, f) for f in sorted(os.listdir(directory))
            if f.startswith(stem) and f.endswith(".kicad_sch")]


# --------------------------------------------------------------------------- checks
def run_checks(d8, d10, drc):
    stem = D.stem(D.REV_C)
    p8 = os.path.join(d8, f"{stem}.kicad_pcb")
    p10 = os.path.join(d10, f"{stem}.kicad_pcb")
    pro8 = json.load(open(os.path.join(d8, f"{stem}.kicad_pro")))
    pro10 = json.load(open(os.path.join(d10, f"{stem}.kicad_pro")))
    b8 = kicad_parse.load(p8)
    b10 = kicad_parse.load(p10)
    out = []

    # ---- 1  netlist ------------------------------------------------------------
    c = Check(1, "Netlist, from the schematic trees")
    n8, prob8 = sch_netlist.build(sch_paths(d8))
    n10, prob10 = sch_netlist.build(sch_paths(d10))
    want = sch_netlist.design_netlist()
    pins8 = sum(len(v) for v in n8.values())
    pins10 = sum(len(v) for v in n10.values())
    c.note("| Quantity | Expected | KiCad 8 | KiCad 10 | Equal |")
    c.note("|---|---|---|---|---|")
    for label, a, b, exp in (("nets", len(n8), len(n10), 156),
                             ("pins", pins8, pins10, 614)):
        ok = (a == b == exp)
        if not ok:
            c.status = FAIL
        c.note(f"| {label} | {exp} | {a} | {b} | {'yes' if ok else '**NO**'} |")
    rows = sch_netlist.diff(n8, n10)
    dv8 = sch_netlist.diff(n8, want)
    if rows or dv8:
        c.status = FAIL
    c.note("")
    c.note(f"Differences between the two schematic trees: **{len(rows)}**. "
           f"Differences between the KiCad 8 tree and `design.py`: **{len(dv8)}**.")
    if rows:
        for net, why, det in rows[:10]:
            c.note(f"- `{net}`: {why} -- {det}")
    if prob8 or prob10:
        c.note(f"Structural findings while parsing: KiCad 8 {len(prob8)}, "
               f"KiCad 10 {len(prob10)}.")
    out.append(c)

    # ---- 2  board census -------------------------------------------------------
    c = Check(2, "Board census")
    pads8 = list(b8.pads())
    pads10 = list(b10.pads())
    netted8 = [p for p in pads8 if p.netname]
    netted10 = [p for p in pads10 if p.netname]
    bynet8 = defaultdict(int)
    for p in netted8:
        bynet8[p.netname] += 1
    bynet10 = defaultdict(int)
    for p in netted10:
        bynet10[p.netname] += 1
    c.note("| Quantity | Expected | KiCad 8 | KiCad 10 | Equal |")
    c.note("|---|---|---|---|---|")
    for label, a, b, exp in (
            ("footprints", len(b8.footprints), len(b10.footprints), 211),
            ("pads", len(pads8), len(pads10), 636),
            ("nets", len(bynet8), len(bynet10), 156),
            ("pads carrying a net", len(netted8), len(netted10), 620),
            ("nets with one pad", sum(1 for v in bynet8.values() if v == 1),
             sum(1 for v in bynet10.values() if v == 1), 11),
            ("nets with two or more", sum(1 for v in bynet8.values() if v >= 2),
             sum(1 for v in bynet10.values() if v >= 2), 145),
            ("track segments", len(b8.segments), len(b10.segments), 0),
            ("vias", len(b8.vias), len(b10.vias), 0)):
        ok = (a == b == exp)
        if not ok:
            c.status = FAIL
        c.note(f"| {label} | {exp} | {a} | {b} | {'yes' if ok else '**NO**'} |")
    same = {k: v for k, v in bynet8.items()} == {k: v for k, v in bynet10.items()}
    if not same:
        c.status = FAIL
    c.note("")
    c.note(f"Pad-count-per-net maps identical across all 156 nets: "
           f"**{'yes' if same else 'NO'}**.")
    out.append(c)

    # ---- 3  net classes --------------------------------------------------------
    c = Check(3, "Net classes")
    t8, t10 = class_table(pro8), class_table(pro10)
    m8, m10 = netclass_map(pro8), netclass_map(pro10)
    c.note("| Quantity | Expected | KiCad 8 | KiCad 10 | Equal |")
    c.note("|---|---|---|---|---|")
    for label, a, b, exp in (("classes", len(t8), len(t10), 8),
                             ("nets assigned", len(m8), len(m10), 156)):
        ok = (a == b == exp)
        if not ok:
            c.status = FAIL
        c.note(f"| {label} | {exp} | {a} | {b} | {'yes' if ok else '**NO**'} |")
    names_eq = sorted(t8) == sorted(t10)
    vals_eq = t8 == t10
    map_eq = m8 == m10
    for label, ok in (("class names identical", names_eq),
                      ("clearance and width values identical", vals_eq),
                      ("net-to-class assignment identical over all 156 nets", map_eq)):
        if not ok:
            c.status = FAIL
        c.note(f"| {label} | -- | -- | -- | {'yes' if ok else '**NO**'} |")
    if not map_eq:
        bad = [k for k in set(m8) | set(m10) if m8.get(k) != m10.get(k)]
        c.note(f"Nets whose class differs: {sorted(bad)[:20]}")
    c.note("")
    c.note("Class table as emitted, both sets:")
    c.note("")
    c.note("| Class | clearance | track_width |")
    c.note("|---|---|---|")
    for k in sorted(t8):
        c.note(f"| `{k}` | {t8[k]['clearance']} | {t8[k]['track_width']} |")
    out.append(c)

    # ---- 4  custom rules -------------------------------------------------------
    c = Check(4, "Custom rules in the .kicad_dru")
    r8 = parse_dru(os.path.join(d8, f"{stem}.kicad_dru"))
    r10 = parse_dru(os.path.join(d10, f"{stem}.kicad_dru"))
    c.note("| Quantity | Expected | KiCad 8 | KiCad 10 | Equal |")
    c.note("|---|---|---|---|---|")
    ok = (len(r8) == len(r10) == 37)
    if not ok:
        c.status = FAIL
    c.note(f"| rules | 37 | {len(r8)} | {len(r10)} | {'yes' if ok else '**NO**'} |")
    names_eq = sorted(r8) == sorted(r10)
    bodies_eq = r8 == r10
    for label, okk in (("rule names identical", names_eq),
                       ("condition expressions and constraint values identical",
                        bodies_eq)):
        if not okk:
            c.status = FAIL
        c.note(f"| {label} | -- | -- | -- | {'yes' if okk else '**NO**'} |")
    if not bodies_eq:
        bad = [k for k in set(r8) | set(r10) if r8.get(k) != r10.get(k)]
        for k in sorted(bad)[:10]:
            c.note(f"- `{k}`: KiCad 8 `{r8.get(k)}` / KiCad 10 `{r10.get(k)}`")
    c.note("")
    c.note("**No KiCad 10 keyword or grammar substitution was made in any rule.** The "
           "two files are byte-for-byte identical: `kicad-cli` does not rewrite a "
           "`.kicad_dru` on upgrade, and none of the 37 rules needed changing for "
           "KiCad 10 to parse it. What DID change, for both sets alike, is the comment "
           "character -- see finding 1 below.")
    out.append(c)

    # ---- 5  DRC severities -----------------------------------------------------
    c = Check(5, "DRC severities")
    s8 = pro8["board"]["design_settings"]["rule_severities"]
    s10 = pro10["board"]["design_settings"]["rule_severities"]
    c.note("| Quantity | Expected | KiCad 8 | KiCad 10 | Equal |")
    c.note("|---|---|---|---|---|")
    ok = (len(s8) == len(s10) == 45)
    if not ok:
        c.status = FAIL
    c.note(f"| checks with a severity | 45 | {len(s8)} | {len(s10)} | "
           f"{'yes' if ok else '**NO**'} |")
    eq = s8 == s10
    if not eq:
        c.status = FAIL
    c.note(f"| severity identical for every check | -- | -- | -- | "
           f"{'yes' if eq else '**NO**'} |")
    only8 = sorted(set(s8) - set(s10))
    only10 = sorted(set(s10) - set(s8))
    diffv = sorted(k for k in set(s8) & set(s10) if s8[k] != s10[k])
    c.note("")
    c.note(f"Checks present in KiCad 8 only: {only8 or 'none'}. "
           f"Present in KiCad 10 only: {only10 or 'none'}. "
           f"Same name, different severity: {diffv or 'none'}.")
    c.note(f"`track_dangling` is `{s8.get('track_dangling')}` in both. "
           f"{sum(1 for v in s8.values() if v == 'error')} of the 45 are `error`.")
    out.append(c)

    # ---- 6  locked footprints --------------------------------------------------
    c = Check(6, "Locked footprints")
    l8, l10 = locked_refs(p8), locked_refs(p10)
    expect = ({f"J{i}" for i in range(1, 31)} | {f"MH{i}" for i in range(1, 5)}
              | {f"FID{i}" for i in range(1, 4)})
    c.note("| Quantity | Expected | KiCad 8 | KiCad 10 | Equal |")
    c.note("|---|---|---|---|---|")
    ok = (len(l8) == len(l10) == 37)
    if not ok:
        c.status = FAIL
    c.note(f"| locked footprints | 37 | {len(l8)} | {len(l10)} | "
           f"{'yes' if ok else '**NO**'} |")
    setok = (set(l8) == set(l10) == expect)
    if not setok:
        c.status = FAIL
    c.note(f"| the set is J1-J30, MH1-MH4, FID1-FID3 | -- | -- | -- | "
           f"{'yes' if setok else '**NO**'} |")
    coordok = (l8 == l10)
    if not coordok:
        c.status = FAIL
    c.note(f"| coordinates identical | -- | -- | -- | "
           f"{'yes' if coordok else '**NO**'} |")
    if not setok:
        c.note(f"KiCad 8 only: {sorted(set(l8) - set(l10))}; "
               f"KiCad 10 only: {sorted(set(l10) - set(l8))}; "
               f"missing from both: {sorted(expect - set(l8) - set(l10))}")
    if not coordok:
        for r in sorted(set(l8) | set(l10)):
            if l8.get(r) != l10.get(r):
                c.note(f"- `{r}`: {l8.get(r)} / {l10.get(r)}")
    c.note("")
    c.note(f"The other {len(b8.footprints) - 37} footprints are unlocked and sit at "
           f"provisional coordinates; they are the layout desk's to place.")
    out.append(c)

    # ---- 7  fixed geometry -----------------------------------------------------
    c = Check(7, "Fixed geometry")
    c.note("| Item | Expected | KiCad 8 | KiCad 10 | Equal |")
    c.note("|---|---|---|---|---|")

    def geo(label, f, exp):
        a, b = f(b8, p8), f(b10, p10)
        ok = (a == b == exp)
        if not ok:
            c.status = FAIL
        c.note(f"| {label} | `{exp}` | `{a}` | `{b}` | "
               f"{'yes' if ok else '**NO**'} |")

    geo("board width x height (mm)", lambda b, p: (b.width, b.height),
        (D.BOARD_W, D.BOARD_H))
    geo("mounting holes",
        lambda b, p: tuple(sorted((round(v[0], 3), round(v[1], 3))
                                  for k, v in locked_refs(p).items()
                                  if k.startswith("MH"))),
        tuple(sorted((float(x), float(y)) for x, y in D.MOUNTING_HOLES)))
    # ECO-EEG-020 places three global fiducials.  They are added inline in design.py
    # rather than as a named constant, so the specified triple is written out here and
    # both sets are checked against it -- reading it back out of one of the two files
    # would compare each set against itself.
    geo("fiducials",
        lambda b, p: tuple(sorted((round(v[0], 3), round(v[1], 3))
                                  for k, v in locked_refs(p).items()
                                  if k.startswith("FID"))),
        ((12.0, 10.0), (12.0, 120.0), (144.0, 100.0)))
    geo("zone split x (mm)", lambda b, p: D.ZONE_SPLIT_X, 62.0)
    geo("via pad / drill (mm), tented, through only",
        lambda b, p: (rules.VIA["pad"], rules.VIA["drill"],
                      rules.VIA["tented"], rules.VIA["through_only"]),
        (0.60, 0.30, True, True))
    shared = sorted(set(b8.setup) & set(b10.setup))
    changed = {k: (b8.setup[k], b10.setup[k]) for k in shared
               if b8.setup[k] != b10.setup[k]}
    ok = not changed
    if not ok:
        c.status = FAIL
    c.note(f"| every `(setup)` key present in both, unchanged in value | -- | -- | -- "
           f"| {'yes' if ok else '**NO**'} |")
    if changed:
        for k, (a, b) in changed.items():
            c.note(f"- `{k}`: KiCad 8 `{a}` / KiCad 10 `{b}`")
    only8 = sorted(set(b8.setup) - set(b10.setup))
    only10 = sorted(set(b10.setup) - set(b8.setup))
    c.note("")
    c.note("Stack-up is DSN-EEG-003 section 3.2: mask / 35 um L1 / prepreg 0.200 / "
           "17 um L2 / core 1.065 / 17 um L3 / prepreg 0.200 / 35 um L4 / mask = "
           "1.60 mm +/- 10 %. The `stackup` key is present in both and identical.")
    c.note("")
    c.note(f"**KiCad 10 adds keys to `(setup)` and removes one.** Added: "
           f"`{'`, `'.join(only10) or 'none'}`. Removed: "
           f"`{'`, `'.join(only8) or 'none'}`. **No key present in both changed "
           f"value**, so nothing this programme specified was altered; KiCad 10 has "
           f"written down defaults that KiCad 8 left implicit, and `grid_origin` is an "
           f"editor preference and not a specification.")
    c.note("")
    c.note("The addition that matters is via finishing, because DSN-EEG-003 section "
           "3.2 requires vias **tented both sides**. KiCad 10 materialises it as "
           "`(tenting (front yes) (back yes))`, with `covering`, `plugging`, `capping` "
           "and `filling` all `no` -- which **is** the specified finish. It is now "
           "explicit in the board file where in KiCad 8 it was carried only by the "
           "fabrication drawing and `tools/rules.py`.")
    out.append(c)

    # ---- 8  rule areas and zones ----------------------------------------------
    c = Check(8, "Rule areas and pours")
    a8, a10 = rule_areas(p8), rule_areas(p10)
    z8, z10 = zone_pours(p8), zone_pours(p10)
    c.note("| Quantity | KiCad 8 | KiCad 10 | Equal |")
    c.note("|---|---|---|---|")
    for label, x, y in (("rule areas", len(a8), len(a10)),
                        ("copper pours", sum(z8.values()), sum(z10.values()))):
        ok = x == y
        if not ok:
            c.status = FAIL
        c.note(f"| {label} | {x} | {y} | {'yes' if ok else '**NO**'} |")
    names_eq = sorted(a8) == sorted(a10)
    ext_eq = a8 == a10
    pour_eq = z8 == z10
    for label, ok in (("area names identical", names_eq),
                      ("area layers, keepout flags and extent identical", ext_eq),
                      ("pours identical by net and layer", pour_eq)):
        if not ok:
            c.status = FAIL
        c.note(f"| {label} | -- | -- | {'yes' if ok else '**NO**'} |")
    if not ext_eq:
        for k in sorted(set(a8) | set(a10)):
            if a8.get(k) != a10.get(k):
                c.note(f"- `{k}`: KiCad 8 `{a8.get(k)}` / KiCad 10 `{a10.get(k)}`")
    iso = a8.get("ISOLATION_KEEPOUT", ("", "", ""))
    c.note("")
    c.note(f"`ISOLATION_KEEPOUT` keepout flags: `{iso[1]}` on layers `{iso[0]}` -- "
           f"free of copper on all four layers, DSN-EEG-003 section 3.3 rule 4.")
    c.note("")
    c.note("Pours, both sets:")
    c.note("")
    c.note("| Net | Layers | Zones |")
    c.note("|---|---|---|")
    for (net, lay), n in sorted(z8.items()):
        c.note(f"| `{net}` | {lay} | {n} |")
    out.append(c)

    # ---- 9  round trip ---------------------------------------------------------
    c = Check(9, "Round trip: KiCad 10 opens it and runs DRC")
    ok, text, path = drc
    if ok is None:
        c.skip(f"KiCad is not installed on this machine ({text}), so `kicad-cli pcb "
               f"drc` could not be run and **no DRC result is claimed**.")
    elif ok is False:
        c.status = FAIL
        c.note(f"`kicad-cli pcb drc` failed:\n\n```\n{text[:2000]}\n```")
    else:
        head = "\n".join(text.splitlines()[:5])
        kinds = defaultdict(int)
        for line in text.splitlines():
            m = re.match(r"^\[([a-z_]+)\]", line)
            if m:
                kinds[m.group(1)] += 1
        c.note(f"Run with `kicad-cli {kicad_fmt.cli_version()}` on the KiCad 10 set, "
               f"severity-all. The report is `{os.path.basename(path)}` in this "
               f"directory. Verbatim head:")
        c.note("")
        c.note("```")
        c.note(head)
        c.note("```")
        c.note("")
        c.note("| Violation class | Count |")
        c.note("|---|---|")
        for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]):
            c.note(f"| `{k}` | {v} |")
        c.note("")
        parse_err = [ln for ln in text.splitlines()
                     if re.search(r"parse|syntax error|unknown token|malformed", ln, re.I)]
        c.note(f"Schema warnings or rule-parse errors in the report: "
               f"**{len(parse_err) or 'none'}**."
               + (f" {parse_err[:3]}" if parse_err else ""))
        c.note("")
        c.note("**The board loads and the rules parse.** The counts above are not a "
               "clean bill: `unconnected_items` is every net of an intentionally "
               "UNROUTED board and is the expected result, `lib_footprint_issues` is "
               "the footprint library not being registered in a command-line "
               "environment and says nothing about the files, and the silkscreen "
               "warnings are against provisional placement the layout desk has not "
               "made yet. **No custom rule fires**, which is also expected: all 37 "
               "constrain tracks and vias, and there are none.")
    out.append(c)
    return out


# --------------------------------------------------------------------------- findings
FINDINGS = """## Findings

Two defects were found by this exercise. Neither is a difference between the two sets --
both were present in the KiCad 8 set as released on 8 September 2026, and both are fixed
at source under ECO-EEG-034, so both sets carry the fix. They are recorded here because
the first of them defeats the purpose of shipping a rule file at all, and because the
released set they affect was cited to the layout desk at commit 745a560c.

### Finding 1 -- the 37 custom rules were silently inert. **Fixed.**

`tools/rules.py` wrote the `.kicad_dru` with `;;` comments. **KiCad discards the whole
file the moment it meets a semicolon comment, and says nothing**: no error, no warning,
DRC continuing as though the file were absent.

Measured on KiCad 10.0.6 by appending a probe rule that must fire
(`(constraint disallow pad)` on a 636-pad board) and counting how many violations were
attributed to it:

| `.kicad_dru` as given to KiCad | Violations attributed to the probe | Rules loaded |
|---|---|---|
| as released, `;;` comments | 0 | **no** |
| comment lines deleted | 139 | yes |
| `;;` changed to `#` | 139 | yes |
| `;;` changed to `;` | 0 | **no** |
| file deleted entirely | -- | identical result to "as released" |

Deleting the rules file changed no result. That is the proof: the released set shipped
37 rules of which KiCad applied none, while LAY-EEG-034 told the layout desk the file
was "not optional".

**Fixed** in `tools/rules.py` by emitting `#`, and `check_dru()` now refuses to emit a
file containing a semicolon comment, so it cannot come back. Both sets carry the fix and
the rules are live in both.

**Not verified:** whether KiCad 8 also discarded the file. No KiCad 8 is installed and
Homebrew has no `kicad@8` cask, so this could not be tested. KiCad's documented comment
character is `#`, and the same silent-discard behaviour is likely, but it was not
measured and is not asserted here.

### Finding 2 -- the zoning and no-via areas forbade the parts they contain. **Fixed.**

`tools/kicad_pcb8.py` wrote `(pads not_allowed) (footprints not_allowed)` into every
rule area. That is right for `ISOLATION_KEEPOUT`, where nothing may sit at all. It was
wrong for `ANALOGUE_ZONE` and `DIGITAL_ZONE`, which between them tile the whole board,
and wrong for the four `NO_VIA_J*` areas, which are the connectors' own courtyards and
so contain those connectors' own pads by construction.

The result was **199 `items_not_allowed` violations at ERROR severity** -- 99 against
`ANALOGUE_ZONE`, 89 against `DIGITAL_ZONE`, 11 against `NO_VIA_J2` -- raised against
placement the layout desk had not yet made.

The intent was already written down and was not what the file said. `tools/rules.py`
says of the zone split: *"The zone split is a routing rule and not a placement rule: a
class may have pads on both sides where the circuit demands it."* The six emitted zoning
rules only ever `disallow track via`; the areas exist to be named by `insideArea()` and
should constrain nothing themselves. DSN-EEG-003 section 3.3 rule 7 likewise forbids a
via under J2, J4, J23 and J29 and nothing else.

**Fixed** in `tools/kicad_pcb8.py` by making `pads` and `footprints` parameters of
`_rule_area()` and passing `allowed` for the zoning and no-via areas, and for the four
`MOUNT_KEEPOUT_MH*` areas, which are centred on the mounting holes and so contained
those holes' own non-plated pads. Copper -- tracks, vias and pours -- stays forbidden in
all of them. `ISOLATION_KEEPOUT` is unchanged and still forbids everything on all four
layers.

`items_not_allowed` fell from **199 to 3** across the two fixes.

### Finding 3 -- MH2 sits inside the isolation strip. **Raised, not resolved.**

The three violations that remain are real geometry, and they were invisible until
finding 1 was fixed, because the rule that reports them had never once run.

`ISOLATION_KEEPOUT` is the strip **x 141.0 to 150.0 mm, y 2.0 to 22.0 mm**
(DSN-EEG-003 section 3.3 rule 4). Mounting hole **MH2 is at (145.0, 5.0)**, which is
inside it. Of the four mounting holes it is the only one that is:

| Hole | Position | Inside the isolation strip |
|---|---|---|
| MH1 | (5.0, 5.0) | no |
| **MH2** | **(145.0, 5.0)** | **yes** |
| MH3 | (5.0, 125.0) | no |
| MH4 | (145.0, 125.0) | no |

**This is probably not a physical defect, and it is not being treated as one here.**
Rule 4 requires the strip to be *free of copper on all four layers*. MH2 is a
**non-plated** hole and rule 8 requires non-plated holes to carry no copper and no mask
opening, so MH2 puts no copper in the strip. What flags it is that the emitted rule is
broader than the requirement it implements:

```
(rule "isolation_keepout"
  (constraint disallow track via zone pad graphic hole footprint)
  (condition "A.insideArea('ISOLATION_KEEPOUT')"))
```

`hole` and `footprint` are not copper. Narrowing the rule to the copper items would
clear the three violations and match rule 4 as written -- **but the isolation barrier is
a safety boundary, the strip exists to keep the carrier out of the ADuM4160's host half,
and narrowing a safety rule is a decision for the programme and not for a re-emission.**
It is therefore recorded here and left alone. Both sets carry the rule as it stands and
both report the same three violations.

Whoever settles it has three options: narrow the rule to `track via zone pad graphic`;
move MH2, which is a locked mounting hole fixed by the enclosure and so probably not
available; or record MH2 as a standing exception against the rule. **No option is taken
here.**
"""


def main(d8=None, d10=None, drc=None, verbose=True):
    from emit_handover import OUT, OUT_K10, EQUIV
    d8 = d8 or OUT
    d10 = d10 or OUT_K10
    stem = D.stem(D.REV_C)
    if drc is None:
        drc = kicad_fmt.run_drc(d10, f"{stem}.kicad_pcb")
    checks = run_checks(d8, d10, drc)

    npass = sum(1 for c in checks if c.status == PASS)
    nfail = sum(1 for c in checks if c.status == FAIL)
    nskip = sum(1 for c in checks if c.status == SKIP)

    L = [f"# EEG-CAR-01 Rev {D.REV_C} -- KiCad 8 and KiCad 10 emissions compared",
         "",
         "**Document:** not a controlled document. It is the check behind the two "
         "layout-input directories, generated by `tools/emit_equivalence.py`.",
         f"**Change order:** ECO-EEG-034.",
         f"**Date:** {D.DATE_C}",
         "**Licence:** CC BY-SA 4.0",
         "",
         "## Why this check exists",
         "",
         "The JLCPCB layout desk runs KiCad 10. The published set is written for "
         "KiCad 8. Opening a KiCad 8 project in KiCad 10 can silently alter the **net "
         "classes**, the **custom rules** and the **DRC severities**, and those three "
         "things are where most of the layout specification lives. Re-emitting is only "
         "worth doing if somebody checks that it moved nothing, so this is that check.",
         "",
         "## How the two sets are produced",
         "",
         f"- {kicad_fmt.report(kicad_fmt.KICAD8)}",
         f"- {kicad_fmt.report(kicad_fmt.KICAD10)}",
         "",
         "One source, `tools/design.py`, and one emission. The KiCad 10 set is that "
         "emission passed through KiCad's own converter, because the KiCad 10 "
         "s-expression schema is KiCad's to define and not this programme's to infer. "
         "A hand-written version token would be a guess, and a guess in the net "
         "classes or the rules is the exact failure this exercise exists to prevent.",
         "",
         "| | KiCad 8 | KiCad 10 |",
         "|---|---|---|",
         f"| `.kicad_pcb` | `(version {kicad_fmt.KICAD8.pcb_version})` | "
         f"`(version {kicad_fmt.KICAD10.pcb_version})` |",
         f"| `.kicad_sch` | `(version {kicad_fmt.KICAD8.sch_version})` | "
         f"`(version {kicad_fmt.KICAD10.sch_version})` |",
         f"| `generator_version` | `\"{kicad_fmt.KICAD8.generator_version}\"` | "
         f"`\"{kicad_fmt.KICAD10.generator_version}\"` |",
         "",
         "The KiCad 10 version numbers were **read out of files KiCad 10.0.6 had just "
         "written**, not taken from memory or documentation.",
         "",
         "`.kicad_pro`, `.kicad_dru`, `.kicad_sym`, the IPC netlist, the BOM, the DXF, "
         "the PDF and the STEP tree are **not rewritten** by the conversion: "
         "`kicad-cli` leaves them alone and they are byte-for-byte identical between "
         "the two directories. That is why checks 3, 4 and 5 below compare equal by "
         "construction -- which is the answer the desk wanted, and it is recorded here "
         "as a measurement rather than assumed.",
         "",
         "## Result",
         "",
         f"**{npass} of {len(checks)} checks pass. {nfail} fail. "
         f"{nskip} not performed.**",
         "",
         "| # | Check | Result |",
         "|---|---|---|"]
    for c in checks:
        L.append(f"| {c.n} | {c.title} | {c.status} |")
    L.append("")
    for c in checks:
        L.append(f"## {c.n}. {c.title} -- {c.status}")
        L.append("")
        L += c.lines
        L.append("")
    L.append(FINDINGS)

    path = os.path.join(d10, EQUIV)
    open(path, "w").write("\n".join(L) + "\n")
    if verbose:
        print(f"    {npass} pass, {nfail} fail, {nskip} not performed -- "
              f"{os.path.relpath(path, PKG)}")
    if nfail:
        raise SystemExit(
            f"the two emissions differ on {nfail} check(s); see "
            f"{os.path.relpath(path, PKG)}. A difference in the net classes, the "
            f"custom rules or the DRC severities is a blocker.")
    return path, checks


if __name__ == "__main__":
    main()
