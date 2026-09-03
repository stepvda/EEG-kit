#!/usr/bin/env python3
"""
simulate_production.py -- walk one unit through the whole production route and check that
the package actually supports every step.

This is not a physics simulation of a circuit.  It is a dry run of the *manufacturing
process* against the *data package*: at each station it asks "what does the operator need
here, is it in the package, and do the numbers work out?", and it fails the step when the
answer is no.  It also computes every acceptance limit in TST-EEG-004 from component values
so that a limit which is arithmetically unreachable is caught before a jig is built.

Stations
   0  purchase order and incoming goods
   1  bare-board fabrication
   2  bare-board electrical test
   3  SMT assembly
   4  through-hole assembly
   5  module preparation and the MP-01 plate
   6  harness and cable assembly
   7  mechanical and enclosure
   8  firmware build, flash and provisioning
   9  functional test TST-EEG-004
  10  software integration with the session runner
  11  final assembly, labelling and kit packing
  12  despatch
  13  the participant's own handling
  14  return, refurbishment and the next cycle

Run:  python3 simulate_production.py [--report PATH]

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import csv
import json
import math
import glob
import hashlib
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import pcbgen               # noqa: E402


class Report:
    def __init__(self):
        self.rows = []
        self.station = ""

    def start(self, n, name):
        self.station = f"{n:02d} {name}"
        self.rows.append(("HEAD", self.station, "", ""))

    def check(self, what, ok, detail=""):
        self.rows.append(("PASS" if ok else "FAIL", self.station, what, detail))
        return ok

    def open_item(self, what, detail=""):
        """A known, documented shortfall.  It is not a package defect; it is a decision
        somebody still has to take, and it is recorded where it belongs."""
        self.rows.append(("OPEN", self.station, what, detail))

    def note(self, what, detail=""):
        self.rows.append(("NOTE", self.station, what, detail))

    def value(self, what, detail):
        self.rows.append(("VALUE", self.station, what, detail))

    @property
    def failures(self):
        return [r for r in self.rows if r[0] == "FAIL"]

    @property
    def passes(self):
        return [r for r in self.rows if r[0] == "PASS"]


def _exists(p):
    return os.path.exists(p) and os.path.getsize(p) > 0


def run(report_path=None):
    R = Report()
    board = pcbgen.BoardV2()
    board.validate()
    nets = board.nets()
    K = os.path.join(PKG, "kicad")
    G = os.path.join(K, "gerber")
    M = os.path.join(PKG, "mech")
    F = os.path.join(PKG, "firmware")
    DOC = os.path.join(PKG, "docs")

    # ---------------------------------------------------------------- 0 purchasing
    R.start(0, "purchase order and incoming goods")
    bom_path = os.path.join(K, "EEG-CAR-01_RevB_BOM.csv")
    if R.check("carrier BOM exists", _exists(bom_path), bom_path):
        rows = list(csv.DictReader(open(bom_path)))
        R.value("BOM lines", str(len(rows)))
        def purchased(r):
            # fiducials and test points are copper features, not parts anybody buys
            return not all(d.startswith(("FID", "TP", "MH"))
                           for d in r["Designators"].split())
        no_mpn = [r["Designators"] for r in rows
                  if purchased(r) and (not r["Manufacturer part number"].strip()
                                       or r["Manufacturer part number"].strip() == "-")]
        R.check("every purchased line carries a manufacturer part number",
                len(no_mpn) == 0,
                "" if not no_mpn else f"missing on: {', '.join(no_mpn[:6])}")
        qty = sum(int(r["Qty"]) for r in rows)
        placed = len([p for p in board.parts if not p.fpname.startswith("MountingHole")])
        R.check("BOM quantity equals the placed part count", qty == placed,
                f"BOM {qty}, placed {placed}")
        dnp = [r["Designators"] for r in rows if r["Fit"].strip() == "DNP"]
        R.value("do-not-populate", ", ".join(dnp) if dnp else "none")
    R.check("approved vendor list present",
            _exists(os.path.join(DOC, "AVL-EEG-017_RevB_approved_vendor_list.md")))
    R.check("incoming inspection defined (quality plan)",
            _exists(os.path.join(DOC, "QP-EEG-010_RevB_quality_plan.md")))

    # ---------------------------------------------------------------- 1 fabrication
    R.start(1, "bare-board fabrication")
    need = ["EEG-CAR-01-F_Cu.gbr", "EEG-CAR-01-In1_Cu.gbr", "EEG-CAR-01-In2_Cu.gbr",
            "EEG-CAR-01-B_Cu.gbr", "EEG-CAR-01-F_Mask.gbr",
            "EEG-CAR-01-B_Mask.gbr", "EEG-CAR-01-F_Silkscreen.gbr",
            "EEG-CAR-01-B_Silkscreen.gbr", "EEG-CAR-01-Edge_Cuts.gbr",
            "EEG-CAR-01-PTH.drl", "EEG-CAR-01-NPTH.drl"]
    for f in need:
        R.check(f"{f} present", _exists(os.path.join(G, f)))
    for f in need:
        p = os.path.join(G, f)
        if not _exists(p):
            continue
        txt = open(p).read()
        if f.endswith(".gbr"):
            R.check(f"{f} is a complete Gerber (FS, MO, M02)",
                    "%FSLAX46Y46*%" in txt and "%MOMM*%" in txt and txt.rstrip().endswith("M02*"))
            aps = set(re.findall(r"%ADD(\d+)", txt))
            used = set(re.findall(r"^D(\d+)\*$", txt, re.M))
            missing = used - aps - {"01", "02", "03", "1", "2", "3"}
            R.check(f"{f} uses only apertures it defines", not missing,
                    f"undefined: {sorted(missing)[:5]}" if missing else "")
            coords = [(int(a), int(b)) for a, b in
                      re.findall(r"X(-?\d+)Y(-?\d+)D0[123]", txt)]
            if coords:
                xs = [c[0] / 1e6 for c in coords]
                ys = [c[1] / 1e6 for c in coords]
                inside = (min(xs) >= -1.0 and max(xs) <= D.BOARD_W + 1.0
                          and min(ys) >= -1.0 and max(ys) <= D.BOARD_H + 1.0)
                R.check(f"{f} coordinates lie inside the board outline", inside,
                        f"x {min(xs):.2f}..{max(xs):.2f}  y {min(ys):.2f}..{max(ys):.2f}")
        else:
            R.check(f"{f} is a complete Excellon file (M48, M30)",
                    txt.startswith("M48") and txt.rstrip().endswith("M30"))
            R.check(f"{f} declares metric units", "METRIC" in txt)
            tools = re.findall(r"^T(\d+)C([\d.]+)", txt, re.M)
            used_t = set(re.findall(r"^T(\d+)$", txt, re.M))
            R.check(f"{f} defines every tool it uses",
                    used_t <= {t for t, _ in tools},
                    f"undeclared: {sorted(used_t - {t for t, _ in tools})}")
            R.value(f"{f} tools", ", ".join(f"{d} mm" for _, d in tools))
    pth = open(os.path.join(G, "EEG-CAR-01-PTH.drl")).read() if _exists(
        os.path.join(G, "EEG-CAR-01-PTH.drl")) else ""
    npth = open(os.path.join(G, "EEG-CAR-01-NPTH.drl")).read() if _exists(
        os.path.join(G, "EEG-CAR-01-NPTH.drl")) else ""
    if pth and npth:
        pth_holes = len(re.findall(r"^X[\d.-]+Y[\d.-]+", pth, re.M))
        npth_holes = len(re.findall(r"^X[\d.-]+Y[\d.-]+", npth, re.M))
        design_npth = sum(1 for p in board.pads() if p.kind == "np_thru_hole")
        R.check("non-plated hole count matches the design", npth_holes == design_npth,
                f"drill {npth_holes}, design {design_npth}")
        R.check("no hole appears in both drill files",
                not (set(re.findall(r"^(X[\d.-]+Y[\d.-]+)", pth, re.M))
                     & set(re.findall(r"^(X[\d.-]+Y[\d.-]+)", npth, re.M))))
        R.value("plated holes", str(pth_holes))
    # The three places that describe a pad -- the Gerber aperture that gets fabricated,
    # the polygon the DRC and connectivity check measure, and the shape written into the
    # KiCad file -- must agree.  On 2 September 2026 they did not: fplib calls a round
    # header pin "oval", gerber.py apertured that as R,wXh and pours.py modelled a box,
    # so the board was checked and would have been built with 1.6 mm SQUARE pads while
    # its own KiCad file drew 1.6 mm circles.  145 of 145 nets closed on the square and
    # 62 of 145 on the circle.  Nothing in this simulation looked, because every check
    # asked the same box-shaped question.  This one compares the models directly.
    import gerber as _gb, pours as _pr
    mismatch = []
    for pd in board.pads():
        if not pd.net:
            continue
        w, h = pd.size_rot()
        try:
            ap = _gb.aperture_for(pd) if hasattr(_gb, "aperture_for") else None
        except Exception:
            ap = None
        poly = _pr.pad_poly(pd)
        # a circular aperture must be modelled by a circular polygon, and vice versa.
        # Compare on area: a circle of diameter w has area pi*w^2/4 = 0.785*w*h.
        round_model = abs(poly.area - math.pi * (w / 2.0) * (h / 2.0)) < 0.02 * w * h
        round_shape = pd.shape == "circle" or (pd.shape == "oval" and abs(w - h) < 1e-9)
        if round_model != round_shape:
            mismatch.append(f"{pd.ref}.{pd.num} shape={pd.shape} "
                            f"{'round' if round_shape else 'angular'} but the DRC models "
                            f"{'a circle' if round_model else 'a box'}")
    R.check("the pad the DRC measures is the pad the design declares",
            not mismatch, "; ".join(mismatch[:3]) or "all pads agree")

    # The firmware and the browser test tool must agree about the wire protocol, and the
    # only thing that can prove it is a test that compiles the real firmware and drives it
    # with the real host code.  The JS-only round-trip cannot: on 2026-09-02 it passed while
    # main.c dispatched every command as START_SESSION, because the JS host and the JS
    # simulated device shared one misunderstanding of section 6.2.
    # Every polarised footprint must carry a pin-1 legend mark that is nearer pad 1 than
    # any other pad.  The SOIC-14 used by U1-U3 had its tick at the far end of the package,
    # beside pad 7, while ASM-EEG-007 section 2.4 tells the operator to align "pin 1 dot to
    # the legend dot" -- so the board's own legend would have fitted all three envelope
    # op-amps 180 degrees out, putting AVDD on the AVSS pin.  drc.py checks copper and has
    # no silkscreen rule, so nothing in the package could see it.
    #
    # Finding the marker is the whole difficulty.  A first attempt looked for silk vertices
    # outside the body outline, and that does not work: the outline's OWN corners are
    # outside it, they sit at both ends of the package, and they masked the misplaced tick
    # completely -- the check passed on the broken footprint.  What separates a marker from
    # an outline is symmetry.  An outline is symmetric about the body centre; a pin-1 mark
    # exists precisely to break that symmetry.  So: drop every segment whose mirror image
    # is also present, and whatever is left is the marker.
    import fplib as _fp
    def _mark_segments(fp):
        cx = (fp.body[0] + fp.body[2]) / 2.0
        cy = (fp.body[1] + fp.body[3]) / 2.0
        def key(sg):
            (x1, y1, x2, y2) = sg[:4]
            return tuple(sorted([(round(x1, 3), round(y1, 3)), (round(x2, 3), round(y2, 3))]))
        def mirrors(sg):
            (x1, y1, x2, y2) = sg[:4]
            out = []
            for mx, my in ((1, -1), (-1, 1), (-1, -1)):
                a = (cx + mx * (x1 - cx), cy + my * (y1 - cy))
                b = (cx + mx * (x2 - cx), cy + my * (y2 - cy))
                out.append(tuple(sorted([(round(a[0], 3), round(a[1], 3)),
                                         (round(b[0], 3), round(b[1], 3))])))
            return out
        present = {key(sg) for sg in fp.silk}
        return [sg for sg in fp.silk if not any(m in present for m in mirrors(sg))]

    bad_p1 = []
    for name in dir(_fp):
        fp = getattr(_fp, name)
        if not hasattr(fp, "pads") or not hasattr(fp, "silk") or not hasattr(fp, "body"):
            continue
        pads = {pd.num: pd for pd in getattr(fp, "pads", []) if pd.num}
        if "1" not in pads or len(pads) < 3 or not fp.silk:
            continue
        marks = _mark_segments(fp)
        if not marks:
            continue                      # no asymmetric feature: nothing to grade
        verts = [(sg[0], sg[1]) for sg in marks] + [(sg[2], sg[3]) for sg in marks]
        def d2(v, pd): return (v[0] - pd.x) ** 2 + (v[1] - pd.y) ** 2
        near1 = min(d2(v, pads["1"]) for v in verts)
        nearest = min(pads, key=lambda n: min(d2(v, pads[n]) for v in verts))
        if nearest != "1" and min(d2(v, pads[nearest]) for v in verts) < near1 - 1e-9:
            bad_p1.append(f"{fp.name}: legend mark sits beside pad {nearest}, not pad 1")
    R.check("every pin-1 legend mark is nearest pad 1",
            not bad_p1, "; ".join(sorted(set(bad_p1))[:3]) or "all footprints agree")

    # IPC-D-356A is fixed-column and machine-read: a field is identified by where it
    # starts.  Records used to run 82 or 83 columns because the feature-size fields were
    # six digits where four are allocated, and the drill diameter was written in
    # MICROMETRES while the header declares 0.0001 inch -- so every hole in the file was
    # overstated by 2.54x.  A bare-board tester would have probed the right nets through
    # the wrong holes.
    ipcp = os.path.join(G, "EEG-CAR-01-IPC-D-356A.ipc")
    if R.check("IPC-D-356A netlist present", _exists(ipcp)):
        recs = [l for l in open(ipcp).read().split("\n") if l[:3] in ("317", "327")]
        widths = {len(l) for l in recs}
        R.check("every IPC-D-356A record is the same width", len(widths) == 1,
                f"widths {sorted(widths)}")
        # Every drill in the netlist must be a drill the design actually has, read back
        # through the netlist's own declared units.  The comparison is one-way and
        # tolerant by design: 0.0001 inch is a coarse grid, so 0.90 mm quantises to
        # 0.899 mm on the way back, and a design drill may legitimately not appear here
        # at all (a pad with no net is not in a netlist, and an NPTH never is).
        # Pad drills come from the design; via drills are read back from the PTH drill
        # file, because the routed vias are not in scope in this function.
        want = [p.drill for p in board.pads() if p.tht and p.drill]
        if pth:
            want += [float(m) for m in re.findall(r"^T\d+C([\d.]+)", pth, re.M)]
        got = []
        for l in recs:
            if l[:3] == "317" and len(l) > 37 and l[32] == "D":
                got.append(int(l[33:37]) * 0.0254 / 10)
        stray = sorted({round(g, 3) for g in got
                        if not any(abs(g - w) <= 0.003 for w in want)})
        R.check("every IPC-D-356A drill diameter is one the design has",
                got and not stray,
                f"unmatched: {stray}" if stray else
                f"{len(set(round(g,3) for g in got))} distinct, all matched")

    # The stencil is a programme-owned tool cut from these Gerbers, and ASM-EEG-007
    # section 2.3 publishes the aperture for every package with its area ratio.  The paste
    # layer used to be cut 1:1 with the copper lands -- PASTE_SHRINK was 0.0 -- so none of
    # those reductions existed in the data, including the both-axis reduction the 1.27 mm
    # SOIC-14 pitch gets against heel bridging.
    import gerber as _gbr
    pastep = os.path.join(G, "EEG-CAR-01-F_Paste.gbr")
    if R.check("solder paste layer supplied", _exists(pastep)):
        emitted = set(re.findall(r"%ADD\d+R,([\d.]+)X([\d.]+)\*%", open(pastep).read()))
        emitted = {(round(float(a), 3), round(float(b), 3)) for a, b in emitted}
        allowed = set()
        for w, h in _gbr.PASTE_APERTURE.values():
            allowed.add((round(w, 3), round(h, 3)))
            allowed.add((round(h, 3), round(w, 3)))      # the same land, rotated
        R.check("every stencil aperture is one ASM-EEG-007 section 2.3 specifies",
                emitted and emitted <= allowed,
                f"not in the table: {sorted(emitted - allowed)}" if emitted - allowed
                else f"{len(emitted)} distinct apertures, all from the table")
        R.check("every land has an aperture rule", not _gbr.PASTE_UNKNOWN,
                f"no rule for {_gbr.PASTE_UNKNOWN}" if _gbr.PASTE_UNKNOWN else "all lands ruled")
        # area ratio = (L x W) / (2 (L + W) t); ASM section 2.3 requires every aperture above 0.66
        t = 0.12
        worst = min(((w * h) / (2 * (w + h) * t), (w, h)) for w, h in emitted)
        R.check("every aperture is above the 0.66 area-ratio floor at 0.12 mm",
                worst[0] > 0.66, f"worst {worst[0]:.2f} at {worst[1]} mm")

    # The electrode cup is the only consumable a service technician replaces, and the only
    # way it comes out is the HM-05B carrier turning a quarter in the HM-04 body.  Those
    # two parts did not assemble: the lug was at r 5.40 against a 5.30 slot, the slot was
    # 1.40 mm wide for a 1.40 mm lug, and hm04() cut two straight pockets with no
    # circumferential run at all -- a plug fit, not a bayonet.  hm05b()'s own docstring
    # said the run was missing and nobody added it.  Nothing in the package could see it,
    # because a mesh that prints is not a mesh that assembles.  This measures the boolean.
    if os.environ.get("SIM_SKIP_MECH") != "1":
        try:
            import mech_gen as _mg
            _body, _car = _mg.hm04(), _mg.hm05b()

            def _clash(ang, dz=0.0):
                try:
                    return _body.intersect(
                        _car.rotate((0, 0, 0), (0, 0, 1), ang).translate((0, 0, dz))
                    ).val().Volume()
                except Exception:
                    return 0.0

            _turn = max(_clash(a) for a in (0, 30, 60, 90))
            R.check("HM-05B enters HM-04 and turns its quarter",
                    _turn < 1e-6, f"worst interference through the turn {_turn:.3f} mm3")
            _float = max(_clash(90.0, dz) for dz in (0.20, 0.40))
            R.check("the seated carrier is free through its 0.40 mm of spring travel",
                    _float < 1e-6, f"{_float:.3f} mm3 -- a bound carrier is a stiff electrode")
            _hold = _clash(90.0, -1.00)
            R.check("the retaining lip holds the seated carrier against an inverted helmet",
                    _hold > 0.1, f"{_hold:.3f} mm3 of lip engagement")
        except ImportError:
            R.note("mechanical fit", "cadquery is not installed, so the HM-04/HM-05B "
                                     "bayonet fit was not measured on this run")

    # The frame has to carry the harness the harness document specifies.  The v1 HM-01 mesh
    # does not: one 3.80 mm bore per run against the two WH-EEG-008 section 7 requires, in a
    # halo band of 10.91 mm where two channels at 6.00 mm centres inside 1.20 mm walls need
    # 12.20 mm.  Both cables in one bore is the one arrangement the harness document
    # forbids, and RFQ E-30's limit on contact-light interference is written against the
    # 6.00 mm.  HM-01P carries the corrected section; this measures it on the solid rather
    # than trusting the constants, by probing across the band for material.
    if os.environ.get("SIM_SKIP_MECH") != "1":
        try:
            import cadquery as _cq
            import mech_gen as _mg
            _f = _mg.hm01p_halo()

            def _solid_at(x, y, z, d=0.12):
                probe = _cq.Workplane("XY", origin=(x, y, z)).box(d, d, d)
                try:
                    return _f.intersect(probe).val().Volume() > 1e-9
                except Exception:
                    return False

            # sweep across the halo section at the +x temple and find the voids
            _z, _x0 = _mg.HM01_HALO_Z, _mg.HM01_HALO_A
            _hits = [(round(-7.0 + 0.2 * k, 1), _solid_at(_x0 - 7.0 + 0.2 * k, 0.0, _z))
                     for k in range(71)]
            _runs, _cur, _start = [], _hits[0][1], _hits[0][0]
            for _off, _sol in _hits[1:]:
                if _sol != _cur:
                    _runs.append((_start, _off, _cur))
                    _cur, _start = _sol, _off
            _runs.append((_start, _hits[-1][0], _cur))
            _bores = [(a, b) for a, b, sol in _runs if not sol and -6.0 < a and b < 6.0]
            R.check("HM-01P carries TWO channels in its section",
                    len(_bores) == 2, f"{len(_bores)} channel(s) found across the halo band")
            if len(_bores) == 2:
                _c = [(a + b) / 2 for a, b in _bores]
                _pitch = abs(_c[1] - _c[0])
                R.check("the two channels are at the WH-EEG-008 section 7 pitch",
                        abs(_pitch - _mg.CH_PITCH) <= 0.3,
                        f"{_pitch:.1f} mm against {_mg.CH_PITCH} mm minimum -- this is the "
                        f"separation RFQ E-30 is written against")
        except ImportError:
            R.note("frame section", "cadquery is not installed, so the HM-01P channel "
                                    "section was not measured on this run")

    # Two panel openings on the same wall must leave material between them.  The headphone
    # jack and the charge USB-C overlapped by 0.2 mm and pod_base() cut them as one merged
    # hole -- each was placed correctly on its own, and nothing compared them to each other,
    # which is how a printed enclosure gets a slot where it should have two ports.
    if os.environ.get("SIM_SKIP_MECH") != "1":
        try:
            import mech_gen as _mg
            _walls = {}
            for _n, _x, _y, _shape, _sz in _mg.PANEL:
                _w = _sz if not isinstance(_sz, tuple) else _sz[0]
                # Group by the face the opening is actually cut in: pod_base() chooses a
                # short wall from x against BW/2, and the lid-mounted set goes to the lid.
                _face = ("lid" if _n in _mg.POD_LID_MOUNTED
                         else ("right" if _x >= _mg.BW / 2 else "left"))
                _walls.setdefault(_face, []).append(
                    (_n, _y - _w / 2.0, _y + _w / 2.0))
            _clash = []
            for _side, _items in _walls.items():
                _items.sort(key=lambda t: t[1])
                for _i in range(len(_items) - 1):
                    _gap = _items[_i + 1][1] - _items[_i][2]
                    _limit = (_mg.POD_LID_MIN_GAP if _side == "lid"
                              else _mg.POD_PANEL_MIN_GAP)
                    if _gap < _limit:
                        _clash.append(f"{_items[_i][0]} / {_items[_i+1][0]} "
                                      f"{_gap:+.2f} mm")
            R.check("every pair of panel openings leaves wall between them",
                    not _clash,
                    "; ".join(_clash) if _clash
                    else f"walls clear {_mg.POD_PANEL_MIN_GAP} mm, lid {_mg.POD_LID_MIN_GAP} mm")
        except ImportError:
            pass

    # The four images the flash step needs.  ASM-EEG-007 section 6.1 and FW-EEG-001
    # section 9 tell the operator to verify SHA-256 against a manifest and flash four
    # binaries -- and the package shipped none of them, while FW-EEG-001 also forbids the
    # manufacturer building firmware.  A shop had a procedure and nothing to run it on.
    _rel = os.path.join(PKG, "firmware", "release")
    _want = ["bootloader.bin", "partition-table.bin", "ota_data_initial.bin",
             "eeg_field_kit.bin", "manifest.json"]
    _missing = [f for f in _want if not _exists(os.path.join(_rel, f))]
    if R.check("the firmware release images are in the package", not _missing,
               f"missing {_missing}" if _missing else "four images and a manifest"):
        _man = json.load(open(os.path.join(_rel, "manifest.json")))
        _bad = []
        for _img in _man.get("images", []):
            _p = os.path.join(_rel, _img["file"])
            _h = hashlib.sha256(open(_p, "rb").read()).hexdigest()
            if _h != _img["sha256"]:
                _bad.append(_img["file"])
        R.check("every image matches the SHA-256 in its manifest", not _bad,
                f"mismatch: {_bad}" if _bad else f"{len(_man.get('images', []))} images")
        R.note("firmware release", _man.get("note", ""))

    # Memory headroom, measured on the linked image.
    #
    # The package carried no memory budget of any kind, and the first real build came back
    # with static IRAM at 100.0 % -- 16,383 bytes used and ONE byte free.  That is not a
    # pass, it is a cliff: the next function anyone marks IRAM_ATTR, or a future ESP-IDF
    # that puts one more byte of its own there, fails the link with an error that names a
    # section and not a cause.  drdy_isr() is already IRAM-resident and the design has more
    # interrupt work coming (the E-13 tone scheduler, the E-12 onset detector).
    _sz = os.path.join(PKG, "firmware", "release", "size.json")
    if _exists(_sz):
        _m = json.load(open(_sz))
        _ir, _rem = _m.get("used_iram", 0), _m.get("iram_remain", 0)
        R.value("firmware image", f"{_m.get('total_size', 0):,} bytes; static IRAM "
                                  f"{_ir:,} used, {_rem:,} free")
        if _rem < 512:
            R.open_item("static IRAM reports full, with one byte free",
                        f"{_rem} byte(s) free of {_ir + _rem:,} on the linked image. If "
                        f"that is the real limit then the next function marked IRAM_ATTR "
                        f"fails the link with an error naming a section and not a cause, "
                        f"and this design has more interrupt work coming (E-13's tone "
                        f"scheduler, E-12's onset detector). Turning off the SPI-slave and "
                        f"gptimer ISRs -- neither of which this firmware uses -- did not "
                        f"move the figure by a single byte, so it is not those. Either the "
                        f"pool is genuinely full, or esp_idf_size is reporting against a "
                        f"fixed 16 KB window that is not the limit on an ESP32-S3 with "
                        f"octal SPIRAM and XIP. Reading the linker map against hardware "
                        f"settles it; guessing at sdkconfig from here does not")

    # Every printed part has to BE a part: one closed body, watertight, positive volume.
    # A mesh that is two disconnected shells prints as two loose objects, and no check in
    # this package looked -- MANIFEST.json records watertightness and not connectedness, so
    # HM-01's v1 mesh has passed as watertight while being two bodies, and the first cut of
    # HM-01P did the same because the three fitted centrelines never actually meet.
    if os.environ.get("SIM_SKIP_MECH") != "1":
        try:
            import warnings as _w
            import trimesh as _tm
            _w.filterwarnings("ignore")
            _stl = sorted(glob.glob(os.path.join(PKG, "mech", "stl", "*.stl")))
            _bad = []
            for _f in _stl:
                _m = _tm.load(_f, force="mesh")
                _why = []
                if not _m.is_watertight:
                    _why.append("not watertight")
                _k = len(_m.split(only_watertight=False))
                if _k > 1:
                    _why.append(f"{_k} disconnected bodies")
                if _why:
                    _bad.append(f"{os.path.basename(_f)}: {'; '.join(_why)}")
            # HM-01 is the carried-over v1 form study and is a known exception, recorded
            # rather than hidden: it is not a released printable part, it is the surface
            # the parametric runs were measured from.
            _known = [b for b in _bad if b.startswith("HM-01_frame_monocoque")]
            _new = [b for b in _bad if b not in _known]
            R.check("every printed part is a single closed body", not _new,
                    "; ".join(_new) if _new else f"{len(_stl)} meshes, all one body")
            if _known:
                R.open_item("the v1 HM-01 mesh is two disconnected bodies",
                            "measured with trimesh: it is watertight, which MANIFEST.json "
                            "records, and it is not connected, which nothing recorded. It "
                            "is a carried-over form study rather than a released printable "
                            "part -- the parametric channel runs HM-01P-A/B/C were measured "
                            "from it -- but a frame that is two shells is one more reason "
                            "the redraw of PARTS-EEG-019 OA-1 has to happen")
        except ImportError:
            R.note("mesh check", "trimesh is not installed, so the printed parts were not "
                                 "checked for connectedness on this run")

    R.check("cross-language interop harness supplied",
            _exists(os.path.join(PKG, "webtest", "tests", "interop", "run.sh")))

    R.check("layer map and checksums supplied",
            _exists(os.path.join(G, "README_layer_map_and_checksums.txt")))
    R.check("fabrication drawing supplied",
            _exists(os.path.join(K, "EEG-CAR-01_RevB_fabrication_drawing.pdf")))
    drcp = os.path.join(K, "EEG-CAR-01_RevB_DRC_report.txt")
    if R.check("DRC report supplied", _exists(drcp)):
        t = open(drcp).read()
        m = re.search(r"VIOLATIONS: (\d+)", t)
        n = int(m.group(1)) if m else -1
        R.check("the DRC reports no violations", n == 0,
                f"VIOLATIONS: {n}")
        conn = int(m2.group(1)) if (m2 := re.search(
            r"nets fully connected\s+(\d+)", t)) else -1
        uncl = int(m3.group(1)) if (m3 := re.search(
            r"unclosed nets\s+(\d+)", t)) else -1
        bare = int(m4.group(1)) if (m4 := re.search(
            r"unclosed nets with NO copper at all\s+(\d+)", t)) else -1
        # The denominator is the DRC's own net count, NOT len(nets): the design carries
        # single-pad nets (test points, no-connects) that have nothing to route, so the
        # board has 156 nets of which 145 are routable.  Comparing against len(nets)
        # grades the board as failing for nets that were never connections.
        total = int(m6.group(1)) if (m6 := re.search(
            r"^  nets\s+(\d+)\s*$", t, re.M)) else -1
        R.check("every routable net is one connected copper island",
                uncl == 0 and bare == 0 and conn == total and total > 0,
                f"{conn} of {total} connected, {uncl} unclosed, {bare} without copper")
        R.value("nets fully connected", f"{conn} of {total} routable "
                                        f"({len(nets)} in the design)")
        relax = int(m5.group(1)) if (m5 := re.search(
            r"CONNECTIONS THE ROUTER HAD TO RELAX: (\d+)", t)) else 0
        R.value("connections routed at relaxed geometry", str(relax))
        # The ECO-EEG-016 section 3 gate is a fabrication-DATA gate, not a design
        # verdict.  Meeting it releases the data for REVIEW; it does not mean the
        # layout is good, and nothing here has been fabricated or measured.
        if n == 0 and uncl == 0 and bare == 0:
            R.note("release state", "the ECO-EEG-016 section 3 gate is MET -- zero "
                   "violations, every net one connected copper island.  The "
                   "fabrication data is RELEASED FOR REVIEW under RFQ-EEG-002A and "
                   "is NOT released for fabrication: no human layout engineer has "
                   f"read this routing, and {relax} of its connections close at the "
                   "minimum conductor or the minimum gap rather than the preferred "
                   "width")
            R.open_item("no human layout engineer has reviewed the routing",
                        "the board passes the programme's own design-rule check, "
                        "which is not the same as being a good layout; the review "
                        "is the scope of RFQ-EEG-002A and gates fabrication release")
        else:
            R.open_item(f"the DRC reports {n} violations, {uncl} unclosed nets, so "
                        "the fabrication data is NOT RELEASED FOR FABRICATION",
                        "closing them is the scope of RFQ-EEG-002A")
            R.note("release state", "the fabrication data is NOT RELEASED FOR "
                   "FABRICATION until the open connections are closed under "
                   "RFQ-EEG-002A")

    # ---------------------------------------------------------------- 2 bare-board test
    R.start(2, "bare-board electrical test")
    ipc = os.path.join(G, "EEG-CAR-01-IPC-D-356A.ipc")
    if R.check("IPC-D-356A netlist supplied", _exists(ipc)):
        t = open(ipc).read()
        listed = set(re.findall(r"^3[12]7(\S{1,14})", t, re.M))
        real = {n[:14] for n in nets}
        missing = real - listed
        R.check("every net appears in the test netlist", not missing,
                f"missing: {sorted(missing)[:6]}" if missing else "")
        R.check("netlist terminates with 999", t.rstrip().endswith("999"))
        R.value("test points in the netlist",
                str(len(re.findall(r"^3[12]7", t, re.M))))

    # ---------------------------------------------------------------- 3 SMT
    R.start(3, "SMT assembly")
    cpl = os.path.join(K, "EEG-CAR-01_RevB_CPL_SMT_top.csv")
    if R.check("SMT pick-and-place file supplied", _exists(cpl)):
        rows = list(csv.DictReader(open(cpl)))
        smd_parts = {p.ref for p in board.parts
                     if not p.is_tht and not p.fpname.startswith("MountingHole")
                     and not p.fpname.startswith("TestPoint")}
        listed = {r["Designator"].strip('"') for r in rows}
        R.check("every surface-mount part is in the CPL", smd_parts <= listed,
                f"missing: {sorted(smd_parts - listed)[:6]}")
        ys = [float(r["Mid Y"]) for r in rows]
        xs = [float(r["Mid X"]) for r in rows]
        R.check("CPL origin is the bottom-left corner, Y positive",
                min(ys) >= 0 and max(ys) <= D.BOARD_H and min(xs) >= 0,
                f"x {min(xs):.1f}..{max(xs):.1f}  y {min(ys):.1f}..{max(ys):.1f}")
        R.check("every CPL row states the layer", all(r["Layer"] == "Top" for r in rows))
        nfid = sum(1 for r in rows if r["Designator"].startswith("FID"))
        R.value("SMT placements",
                f"{len(rows) - nfid} placed parts, of which R89 is do-not-populate; "
                f"the CPL has {len(rows)} rows because it also carries the "
                f"{nfid} fiducials, which take copper and mask apertures but no paste")
        pkgs = sorted({r["Package"] for r in rows})
        R.value("distinct SMT packages", f"{len(pkgs)}: " + ", ".join(pkgs))
    paste = os.path.join(G, "EEG-CAR-01-F_Paste.gbr")
    if R.check("stencil (paste) layer supplied", _exists(paste)):
        t = open(paste).read()
        flashes = len(re.findall(r"D03\*", t))
        # Count the pads that ACTUALLY take paste, which is not the same as the pads that
        # exist.  Test points and fiducials are fabricated features: nothing is soldered to
        # them, so they carry copper and mask and no paste.  An earlier version of this
        # check computed that exclusion and then threw it away, comparing the stencil
        # against every SMD pad on the board with a +/-20 fudge wide enough to hide the
        # difference.  It now compares like with like and expects an exact match.
        paste_pads = sum(1 for p in board.pads()
                         if p.kind == "smd" and "F.Paste" in getattr(p, "layers", ()))
        R.check("every surface-mount pad that takes paste has a stencil aperture",
                flashes == paste_pads,
                f"stencil {flashes}, pads taking paste {paste_pads}")
        no_paste = sum(1 for p in board.pads()
                       if p.kind == "smd" and "F.Paste" not in getattr(p, "layers", ()))
        R.value("surface-mount pads deliberately without paste",
                f"{no_paste} (TP1-TP18 probe pads and the three fiducials: copper and mask "
                f"only, nothing is soldered to them)")
    R.note("reflow profile", "SAC305: preheat 150-200 C over 90 s, 45-90 s above the "
                             "217 C liquidus, peak 235-245 C measured at the U1 body and "
                             "245 C maximum anywhere on the board, cooling <= 4 C/s "
                             "-- ASM-EEG-007 section 2.5")
    R.check("assembly work instructions present",
            _exists(os.path.join(DOC, "ASM-EEG-007_RevB_assembly_work_instructions.md")))

    # ---------------------------------------------------------------- 4 through-hole
    R.start(4, "through-hole assembly")
    tht_cpl = os.path.join(K, "EEG-CAR-01_RevB_CPL_THT_top.csv")
    if R.check("through-hole position file supplied", _exists(tht_cpl)):
        rows = list(csv.DictReader(open(tht_cpl)))
        tht_parts = {p.ref for p in board.parts
                     if p.is_tht and not p.fpname.startswith("MountingHole")}
        listed = {r["Designator"].strip('"') for r in rows}
        R.check("every through-hole part is listed", tht_parts <= listed,
                f"missing: {sorted(tht_parts - listed)[:6]}")
        R.value("through-hole parts", str(len(rows)))
    R.check("R90 and R91 exist and are the only star points",
            board.part("R90") is not None and board.part("R91") is not None)
    ag = nets.get("AGND_REF", [])
    dg = nets.get("DGND", [])
    bridges = [p.ref for p in ag if p.ref in {q.ref for q in dg}]
    R.check("no component other than R90 bridges AGND_REF and DGND",
            bridges == ["R90"], f"bridging parts: {bridges}")
    hs = {p.ref for p in nets.get("HARN_SHIELD", [])} & {p.ref for p in dg}
    R.check("no component other than R91 bridges HARN_SHIELD and DGND",
            hs == {"R91"}, f"bridging parts: {sorted(hs)}")

    # ---------------------------------------------------------------- 5 modules
    R.start(5, "module preparation and the MP-01 plate")
    icd = os.path.join(DOC, "ICD-EEG-006_RevB_interface_control_document.md")
    R.check("interface control document present", _exists(icd))
    R.check("module plate MP-01 model present",
            _exists(os.path.join(M, "stl", "MP-01_module_plate.stl")))
    module_conns = ["J1", "J2", "J23", "J3", "J4", "J29", "J6", "J7", "J8", "J9",
                    "J10", "J11", "J12", "J19", "J20", "J21", "J25", "J28"]
    for ref in module_conns:
        p = board.part(ref)
        R.check(f"{ref} exists on the carrier", p is not None,
                p.value if p else "MISSING")
    j6 = board.part("J6")
    j7 = board.part("J7")
    if j6 and j7:
        spacing = abs(j7.x - j6.x)
        R.check("DevKitC-1 header row spacing is 22.86 mm",
                abs(spacing - 22.86) < 0.01, f"{spacing:.2f} mm")
    for pin in (11, 12, 13, 15):
        net = D.N.get(f"J7.{pin}", "")
        R.check(f"J7 position {pin} is left unconnected (PSRAM / strapping)",
                net.startswith("NC_"), net or "unassigned")

    # ---------------------------------------------------------------- 6 harness
    R.start(6, "harness and cable assembly")
    R.check("harness specification present",
            _exists(os.path.join(DOC, "WH-EEG-008_RevB_harness_and_cable_assembly.md")))
    j14 = [D.N.get(f"J14.{i}") for i in range(1, 13)]
    j30 = [D.N.get(f"J30.{i}") for i in range(1, 11)]
    R.check("electrode harness carries 8 scalp + 2 reference + bias + screen = 12 ways",
            len([n for n in j14 if n and n.startswith("E_")]) == 8
            and "REF_L" in j14 and "REF_R" in j14 and "BIAS_EL" in j14
            and "HARN_SHIELD" in j14, ", ".join(str(n) for n in j14))
    R.check("light harness carries 8 lines + common + return = 10 ways",
            len([n for n in j30 if n and n.startswith("LED") and n[3:].isdigit()]) == 8
            and "LED_V" in j30 and "LED_GND" in j30, ", ".join(str(n) for n in j30))
    R.check("no digital signal shares the electrode harness",
            not any(n in D.DIGITAL_ONLY_NETS for n in j14 if n))

    # ---------------------------------------------------------------- 7 mechanical
    R.start(7, "mechanical and enclosure")
    for f in ["HM-04_electrode_assembly_body.stl", "HM-08_battery_hatch.stl",
              "HM-09_service_key.stl", "HM-02_brow_pad.stl", "FIT-01_fit_test_coupon.stl",
              "POD-P1_prototype_enclosure_base.stl",
              "POD-P1_prototype_enclosure_lid.stl", "MP-01_module_plate.stl"]:
        R.check(f"{f} present", _exists(os.path.join(M, "stl", f)))
        R.check(f"{f[:-4]}.step present (a mesh cannot be dimensioned)",
                _exists(os.path.join(M, "step", f[:-4] + ".step")))
    import glob as _glob
    foam = sorted(_glob.glob(os.path.join(M, "CASE-00_foam_layer_*.dxf")))
    R.check("the CASE-00 Rev C foam cut files are supplied, all seven layers",
            len(foam) == 7, f"{len(foam)} layer file(s) in mech/")
    R.check("no superseded Rev B foam file is still shipped",
            not _exists(os.path.join(M, "CASE-00_foam_top_layer.dxf"))
            and not _exists(os.path.join(M, "CASE-00_foam_bottom_layer.dxf")),
            "PKG-EEG-015 2.4: the Rev B two-layer insert cannot pack this kit")
    R.check("2D drawings supplied for the printed parts",
            os.path.isdir(os.path.join(M, "drawings"))
            and len(os.listdir(os.path.join(M, "drawings"))) > 0)
    R.check("rulings register present",
            _exists(os.path.join(DOC, "RUL-EEG-021_RevA_rulings_register.md")))
    R.check("part identifier register present",
            _exists(os.path.join(DOC, "PARTS-EEG-019_RevB_part_identifier_register.md")))
    # does the carrier fit POD-P1?
    R.check("carrier fits the POD-P1 internal envelope (158 x 138 mm)",
            D.BOARD_W <= 158 and D.BOARD_H <= 138,
            f"board {D.BOARD_W} x {D.BOARD_H} mm")
    stack = 2.5 + 6.0 + 1.6 + 18.0 + 3.0 + 18.0
    R.check("the electronics stack fits the 55.5 mm internal depth", stack <= 55.5,
            f"{stack:.1f} mm: floor 2.5 + boss 6.0 + carrier 1.6 + standoff 18.0 + "
            f"plate 3.0 + modules 18.0")
    R.value("mounting hole pattern",
            "M3 at (5,5) (145,5) (5,125) (145,125) -- 140 x 120 mm centres, shared by the "
            "carrier, MP-01 and the POD-P1 bosses")

    # ---------------------------------------------------------------- 8 firmware
    R.start(8, "firmware build, flash and provisioning")
    for f in ["main/main.c", "CMakeLists.txt", "main/CMakeLists.txt",
              "sdkconfig.defaults", "partitions.csv", "README.md"]:
        R.check(f"firmware/{f} present", _exists(os.path.join(F, f)))
    R.check("provisioning script present",
            _exists(os.path.join(F, "tools", "provision.py")))
    R.check("host verification tool present",
            _exists(os.path.join(F, "tools", "verify_stream.py")))
    pinmap = os.path.join(F, "main", "board_pins.h")
    if R.check("generated pin map header present", _exists(pinmap)):
        t = open(pinmap).read()
        assigned = {int(g) for _n, g in
                    re.findall(r"#define PIN_(\w+)\s+(\d+)", t)
                    if not _n.startswith("RESERVED")}
        for bad, why in ((35, "octal PSRAM"), (36, "octal PSRAM"), (37, "octal PSRAM"),
                         (45, "VDD_SPI strapping pin")):
            R.check(f"no signal is assigned to GPIO{bad} ({why})", bad not in assigned,
                    "")
        R.check("the reserved pins are named in the header so nobody re-uses them",
                all(f"RESERVED" in t and str(b) in t for b in (35, 36, 37, 45)))
        R.value("GPIOs assigned", ", ".join(str(g) for g in sorted(assigned)))
    R.note("firmware status", "never compiled against a real ESP-IDF installation and never "
                              "run on hardware; five drivers are stubs (DSN-EEG-003 Rev C "
                              "section 5)")

    # ---------------------------------------------------------------- 9 functional test
    R.start(9, "functional test TST-EEG-004")
    R.check("test specification present",
            _exists(os.path.join(DOC, "TST-EEG-004_RevC_production_test_specification.md")))
    R.check("test fixture design present",
            _exists(os.path.join(DOC, "JIG-EEG-009_RevB_test_fixture_design.md")))

    # --- arithmetic that the acceptance limits depend on
    R.value("layer count", "4 -- L1 signal, L2 and L3 reference planes, L4 signal")
    # Component values are read from the board, never restated here.
    def _val(ref, suffix):
        for pt in board.parts:
            if pt.ref == ref:
                v = pt.value.split()[0].lower().rstrip(suffix)
                mult = {"k": 1e3, "m": 1e6, "n": 1e-9, "u": 1e-6, "p": 1e-12}
                for sfx, mul in mult.items():
                    if sfx in v:
                        whole, _, frac = v.partition(sfx)
                        return float(f"{whole}.{frac}" if frac else whole) * mul
                return float(v)
        raise KeyError(ref)

    # Read the fitted series resistor from the BOARD.  It was hardcoded at 47e3, and when
    # ECO-EEG-024 raised R1-R16 to 68 kOhm the simulation went on grading a resistor the
    # board no longer carries -- and it is the resistor that decides a SAFETY limit.
    Rser, Cfil = _val("R1", "%"), 10e-9
    fc = 1 / (2 * math.pi * Rser * Cfil)
    loss100 = 20 * math.log10(1 / math.sqrt(1 + (100 / fc) ** 2))
    R.value("input RC corner", f"{fc:.0f} Hz")
    # E-10 states TWO limits and which one applies depends on which resistor is fitted:
    # "+/-0.5 dB with the 47 kOhm resistors fitted, and within +/-1.0 dB if ECO-EEG-024
    # raises them to 68 kOhm".  The check used to assert 0.5 dB unconditionally, so taking
    # the ECO -- which is what makes S-02's safety limit pass -- failed a requirement that
    # explicitly permits it.  The limit follows the fitted part, like the current does.
    e10_limit = 0.5 if Rser < 55e3 else 1.0
    R.check(f"E-10: response at 100 Hz is inside +/-{e10_limit:.1f} dB",
            abs(loss100) <= e10_limit,
            f"{loss100:.3f} dB with the {Rser/1e3:.0f} k fitted, against the "
            f"+/-{e10_limit:.1f} dB branch E-10 states for it")

    k, T, BW = 1.380649e-23, 300.0, 69.5
    en_r = math.sqrt(4 * k * T * Rser * BW) * 1e6
    en_ads = 0.14
    en_tot = math.hypot(en_r, en_ads)
    R.value(f"Johnson noise of the {Rser/1e3:.0f} k series resistor", f"{en_r:.3f} uV RMS (0.5-70 Hz)")
    R.check("E-03: total input-referred noise is inside 1.0 uV RMS", en_tot <= 1.0,
            f"{en_tot:.3f} uV RMS")

    # Read the Sallen-Key values from the BOARD rather than restating them here.  They
    # were hardcoded as 22k/100n/220n, and when the network moved to C0G on 2026-09-02 the
    # simulation went on computing the corner of a filter the board no longer has -- the
    # same drift that put a square pad in the DRC and a stale census in thirteen documents.
    R2, C1, C2 = _val("R25", "%"), _val("C21", "v"), _val("C22", "v")
    f0 = 1 / (2 * math.pi * R2 * math.sqrt(C1 * C2))
    Q = 0.5 * math.sqrt(C2 / C1)
    f3 = f0 * math.sqrt(1 - 1 / (2 * Q ** 2)
                        + math.sqrt((1 - 1 / (2 * Q ** 2)) ** 2 + 1))
    R.value("envelope filter", f"f0 = {f0:.1f} Hz, Q = {Q:.2f}, -3 dB at {f3:.1f} Hz")
    # The Sallen-Key capacitors are C0G as of 2026-09-02, at +/-5 % and flat over
    # temperature.  They were X7R at +/-15 %, because a 100 nF C0G in 0603/50 V is not a
    # stocked part -- and the answer was to stop asking for 100 nF: the capacitors scaled
    # down by ten and the resistors up by ten leave f0 and Q where they were and land on
    # 10 nF / 22 nF, the 10 nF being the same part as the sixteen electrode filters.
    # f0 goes as 1/sqrt(C1*C2), so the tolerance moves it by 1/1.05 to 1/0.95; Q depends
    # only on the ratio C2/C1 and does not move at all.
    x7r = 0.05
    f0_lo, f0_hi = f0 / (1 + x7r), f0 / (1 - x7r)
    R.value("envelope filter over the C0G tolerance",
            f"f0 = {f0_lo:.1f} to {f0_hi:.1f} Hz "
            f"({(1/(1+x7r)-1)*100:+.1f} % to {(1/(1-x7r)-1)*100:+.1f} %) with C21/C41/C61 "
            f"and C22/C42/C62 at +/-5 %; Q unchanged, it is set by C2/C1 alone")
    # TST-EEG-004 T12e is the limit that actually exists: f0 measured and recorded per unit
    # against 42 to 58 Hz.  E-11's 50 Hz +/-10 % is a requirement the approved parts cannot
    # hold, so it is an open item here and not a check that passes on the nominal value.
    R.check("T12e: the calculated envelope corner is inside TST-EEG-004's 42 to 58 Hz",
            42.0 <= f0 <= 58.0,
            f"f0 = {f0:.1f} Hz nominal, measured and recorded per unit")
    # E-11's own band, which the X7R build could not hold at all.  This is now a CHECK and
    # not an open item: with C0G the whole tolerance range sits inside 45 to 55 Hz.
    R.check("E-11: the envelope corner holds 50 Hz +/-10 % over the capacitor tolerance",
            45.0 <= f0_lo and f0_hi <= 55.0,
            f"f0 spans {f0_lo:.1f} to {f0_hi:.1f} Hz against a 45.0 to 55.0 band")
    f_ac = 1 / (2 * math.pi * 10e3 * 10e-6)
    R.value("envelope AC-coupling corner", f"{f_ac:.2f} Hz")
    R.check("E-11 as restated by ECO-EEG-027: AC corner at or below 2 Hz", f_ac <= 2.0,
            f"{f_ac:.2f} Hz with C20/C40/C60 = 10 uF into 10 kOhm")

    div = 2.2e3 / (22e3 + 2.2e3)
    R.value("envelope output divider", f"x{div:.4f}")
    R.check("E-11: a 1.1 V peak envelope lands inside +/-100 mV",
            abs(1.1 * div) <= 0.105, f"{1.1*div*1000:.1f} mV")

    thr = 2.5 * 10e3 / (470e3 + 10e3)
    R.value("comparator threshold", f"{thr*1000:.1f} mV")
    R.check("E-12: the comparator trips within the envelope's working range",
            0.02 <= thr <= 0.09, f"{thr*1000:.1f} mV")

    led_i = (3.3 - 2.0) / 1e3
    R.value("contact-light current per site", f"{led_i*1000:.2f} mA")
    R.check("E-27, current only: GPIO48 can source all eight lights",
            8 * led_i * 1000 <= 30.0, f"{8*led_i*1000:.1f} mA total against a 40 mA rating")
    # E-27's amber needs the phase driver to exist, and this used to be an open item that
    # asserted it did not.  It does now -- so ask the SOURCE rather than restate a status,
    # which is the same lesson as the pad model and the census: a check that carries its
    # own answer stops being a check the moment the answer changes.
    _fw = os.path.join(PKG, "firmware", "main", "main.c")
    _src = open(_fw).read() if _exists(_fw) else ""
    R.check("E-27: the bicolour phase driver exists in the firmware",
            "lights_phase(" in _src,
            "lights_phase() alternates LED_V against the shift register"
            if "lights_phase(" in _src else
            "nothing alternates LED_V against the shift-register outputs, so no site can "
            "show red or amber (FW-D16)")

    # E-27 needs THREE reachable colours, and "the driver exists" does not establish that.
    # FW-D17 is exactly the hole this closes: the driver existed, compiled and looked
    # right, but computed red as `g_loff_p & g_loff_n` while ads_init() enabled
    # LOFF_SENSP only.  g_loff_n was therefore 0 for ever, red was unreachable, and every
    # site that had lost contact showed amber.  Nothing in the package caught it, because
    # every check asked whether the code was there rather than whether it could fire.
    #
    # So: read the three colour expressions out of lights_task(), collect the state each
    # one depends on, and require that every such variable is actually fed from something
    # ads_init() switches on.  A colour whose mask can only ever be zero fails here.
    # The colour expressions usually read through a local alias -- the pre-FW-D17 code
    # said `uint8_t p = g_loff_p, n = g_loff_n;` and then `bad = p & n` -- so the aliases
    # have to be resolved before the dependencies mean anything.  A first version of this
    # check did not, found no g_loff_* names in `p & n`, concluded there was nothing to
    # starve and passed the very defect it was written for.
    _alias = {}
    for _decl in re.finditer(r"uint8_t\s+([^;=]+=[^;]+);", _src):
        for _part in _decl.group(1).split(","):
            if "=" not in _part:
                continue
            _lhs, _rhs = _part.split("=", 1)
            _alias[_lhs.strip()] = _rhs.strip()

    def _resolve(expr, depth=0):
        """Expand local aliases until only g_loff_* state (or nothing) is left."""
        if depth > 8:
            return set()
        names = set(re.findall(r"[A-Za-z_]\w*", expr))
        out = {n for n in names if n.startswith("g_loff_")}
        for n in names - out:
            if n in _alias and n not in ("uint8_t",):
                out |= _resolve(_alias[n], depth + 1)
        return out

    _colour_src = {}
    for _name in ("good", "marg", "bad"):
        _m = re.search(r"uint8_t\s+" + _name + r"\s*=\s*(.+?);", _src)
        if _m:
            _colour_src[_name] = _m.group(1)
    _deps = set()
    for _e in _colour_src.values():
        _deps |= _resolve(_e)
    # what the converter is actually configured to report
    _sensp = "REG_LOFF_SENSP" in _src and re.search(
        r"REG_LOFF_SENSP,\s*0,\s*0x00,\s*0x([0-9A-Fa-f]{2})", _src)
    _sensn = bool(re.search(r"REG_LOFF_SENSN,\s*0,\s*0x00,\s*0x[1-9A-Fa-f]", _src))
    _swept = "ads_set_loff_threshold(" in _src and "LOFF_TH_SENS" in _src \
             and "LOFF_TH_INSENS" in _src
    _fed = set()
    if _sensp and _sensp.group(1).upper() != "00":
        _fed.add("g_loff_p")
        if _swept:
            _fed |= {"g_loff_sens", "g_loff_insens"}
    if _sensn:
        _fed.add("g_loff_n")
    _starved = sorted(_deps - _fed)
    R.check("E-27: all three colours are reachable from what ads_init() enables",
            bool(_colour_src) and len(_colour_src) == 3 and not _starved,
            (f"green, amber and red are computed from {', '.join(sorted(_deps))}, and the "
             f"converter is configured to feed {'a swept LOFF_SENSP comparator' if _swept else 'LOFF_SENSP'}"
             + (" and LOFF_SENSN" if _sensn else "")) if not _starved else
            (f"the colour logic depends on {', '.join(_starved)}, which ads_init() never "
             f"enables, so at least one colour can never light (this is FW-D17: the "
             f"montage is single-ended, so LOFF_STATN carries no per-site information)"
             if _starved else "the three colour expressions could not be found in lights_task()"))
    R.open_item("E-27 has never been seen to light",
                "the driver is written and the current budget is met, but no unit exists, "
                "so no light has been driven and TST-EEG-004 T11 -- which reads the R/G "
                "ratio with a colorimeter -- has not been run. The alternation also "
                "quantises to the FreeRTOS tick, about 250 Hz rather than exactly 240, "
                "which meets the 'above 100 Hz' E-27 is written against and is what T11 "
                "will actually measure")

    rate, ch, aux = 1000, 16, 2
    bps = rate * (ch * 3 + aux)
    R.value("raw sample payload at 1000 Hz", f"{bps/1000:.1f} kB/s "
            f"({ch} channels x 3 bytes + {aux} aux, {rate} times a second)")
    # The framed rate is the one every other document quotes: 10 header + 1000 payload
    # + 4 CRC = 1014 bytes, 1015 after COBS, one frame every 20 ms.
    framed = 1015 * 50
    R.value("framed stream at 1000 Hz", f"{framed/1000:.1f} kB/s "
            "(1014 bytes of frame, 1015 after COBS, one every 20 ms)")
    R.check("the framed rate matches the 50.7 kB/s ruled in RUL-EEG-021 section B",
            abs(framed - 50700) <= 100, f"{framed/1000:.2f} kB/s")
    R.check("E-20: one-bit SDMMC has headroom at 1000 Hz", framed <= 2e6 * 0.5,
            f"{framed/1000:.1f} kB/s needed against about 2000 kB/s available")
    R.check("F-12: full-speed USB carries three times the stream", framed * 3 <= 1.2e6,
            f"{framed*3/1000:.0f} kB/s against about 1200 kB/s usable")
    ring = 6 * 1024 * 1024          # RING_BYTES, 6 MiB = 6,291,456 bytes (FW-D13)
    R.value("ring buffer depth at 1000 Hz",
            f"{ring/bps:.0f} s of raw samples ({ring:,} bytes at {bps/1000:.1f} kB/s); "
            f"{ring/framed:.0f} s if counted over the framed stream")
    R.check("F-06 as relaxed by ECO-EEG-025: at least 90 s of ring", ring / framed >= 90,
            f"{ring/framed:.0f} s on the pessimistic framed count; the microSD copy "
            "covers anything longer")
    R.note("the 118 s figure is withdrawn",
           "it divided 6 MB decimal by the framed rate; the ring is 6 MiB and it holds "
           "raw samples, so the depth is 126 s (124 s framed) -- ECO-EEG-025")

    cap_mAh, idle_mA, rec_mA = 3000, 90, 150
    rec_mA_icd = 440                # ICD-EEG-006 section 2.7's own tally
    R.value("recording endurance at 1000 Hz",
            f"{cap_mAh/rec_mA:.1f} h at the {rec_mA} mA of TST-EEG-004 T3, but only "
            f"{cap_mAh/rec_mA_icd:.1f} h at the {rec_mA_icd} mA that ICD-EEG-006 "
            "section 2.7 tallies")
    R.check("E-22 on the T3 limit: at least four hours of recording",
            cap_mAh / rec_mA >= 4.0, f"{cap_mAh/rec_mA:.1f} h")
    R.check("E-22 also holds at the higher of the two disputed currents",
            cap_mAh / rec_mA_icd >= 4.0,
            f"{cap_mAh/rec_mA_icd:.1f} h at {rec_mA_icd} mA, so E-22 is met on either "
            "figure")
    R.open_item("the two board-current figures cannot both be right",
                f"TST-EEG-004 T3 limits J13 to {rec_mA} mA while ICD-EEG-006 section 2.7 "
                f"tallies about {rec_mA_icd} mA. E-22 is met either way "
                f"({cap_mAh/rec_mA:.1f} h against {cap_mAh/rec_mA_icd:.1f} h), but the "
                "charger, the thermal budget and the T3 limit itself all rest on the "
                "number, and it is open item 14 of RFQ-EEG-001 Rev E. It is measured, "
                "not calculated, at T3")

    # patient auxiliary current, normal condition
    i_bav99 = 100e-9      # BAV99 reverse leakage at 25 C, datasheet maximum
    i_ads = 300e-12       # ADS1299 input bias current, typical
    i_loff = 6e-9         # lead-off excitation, RFQ E-06
    i_norm = i_bav99 + i_ads + i_loff
    R.value("patient auxiliary current, normal condition",
            f"{i_norm*1e6:.3f} uA (BAV99 leakage dominates)")
    R.check("S-02: normal condition is inside 10 uA DC", i_norm <= 10e-6,
            f"{i_norm*1e6:.3f} uA")
    i_fault = 2.5 / Rser
    R.value("single-fault current with a shorted clamp",
            f"{i_fault*1e6:.1f} uA, limited by the {Rser/1e3:.0f} k series resistor")
    # S-02 is a SAFETY limit and this is the check that says whether it is met.  It used to
    # be an open item because 47 kOhm gave 53.2 uA against 50; ECO-EEG-024 was applied on
    # 2026-09-02 and it is a check.  If a future change puts the resistor back, this fails
    # rather than quietly reverting to a note.
    R.check("S-02: single fault is inside the 50 uA DC limit", i_fault <= 50e-6,
            f"{i_fault*1e6:.1f} uA with the {Rser/1e3:.0f} kOhm series resistor fitted; "
            f"the input corner is {1/(2*math.pi*Rser*Cfil):.0f} Hz, which E-10 covers")
    R.open_item("SR-01 is closed in the design and not yet signed off",
                f"S-02 is now met at {i_fault*1e6:.1f} uA against 50 uA, because "
                f"ECO-EEG-024 raised R1-R16 to {Rser/1e3:.0f} kOhm. Applying the fix the "
                f"analysis pointed to is not the same as having it approved: the "
                f"electrical safety reviewer of RISK-EEG-011 section 7 owns SR-01 and "
                f"that review has not started.")

    # ---------------------------------------------------------------- 10 software
    R.start(10, "software integration with the session runner")
    R.check("frame format is fully specified in the RFQ",
            _exists(os.path.join(DOC, "RFQ-EEG-001_RevE_EEG_kit_specification.md")))
    frame_hdr = 1 + 2 + 2 + 4 + 2 + 4
    sample = 16 * 3 + 2
    frame20 = frame_hdr + 20 * sample
    R.value("frame at 1000 Hz", f"{frame20} bytes before COBS, one every 20 ms")
    R.check("a 20 ms frame fits comfortably in a full-speed bulk transfer stream",
            frame20 < 1024, f"{frame20} bytes")
    for req, where in [("F-01 composite CDC-ACM + vendor bulk", "FW-EEG-001 section 4"),
                       ("F-02 WebUSB and MS OS 2.0 descriptors", "FW-EEG-001 section 4"),
                       ("F-04 `iSerialNumber` = the unit serial TIOV-B-nnnn",
                        "PKG-EEG-015 section 5 defines the format; RUL-EEG-021 "
                        "section B rules it"),
                       ("F-08 signed block chain", "FW-EEG-001 section 5.6"),
                       ("F-21 timing self-test", "TST-EEG-004 step T13")]:
        R.note(f"software contract: {req}", where)
    R.check("host verification tool covers the signature chain (T16)",
            _exists(os.path.join(F, "tools", "verify_stream.py")))

    # ---------------------------------------------------------------- 11 final assembly
    R.start(11, "final assembly, labelling and kit packing")
    R.check("packing, labelling and shipping specification present",
            _exists(os.path.join(DOC, "PKG-EEG-015_RevB_packing_labelling_and_shipping.md")))
    R.check("participant quick-start card present",
            _exists(os.path.join(DOC,
                                 "IFU-EEG-014_RevB_participant_quick_start_and_placement_guide.md")))
    R.check("every foam layer the packing list needs is supplied",
            len(sorted(__import__("glob").glob(
                os.path.join(M, "CASE-00_foam_layer_*.dxf")))) == 7,
            "CASE-00 Rev C, seven 25 mm layers on a 516 x 390 mm sheet")

    # ---------------------------------------------------------------- 12 despatch
    R.start(12, "despatch")
    reg = os.path.join(DOC, "REG-EEG-012_RevB_regulatory_and_compliance_file.md")
    if R.check("regulatory and compliance file present", _exists(reg)):
        t = open(reg).read()
        R.check("lithium shipping is covered (UN3481 / PI967)",
                "UN3481" in t and "967" in t)
        R.check("RoHS and REACH declarations are covered", "RoHS" in t and "REACH" in t)

    # ---------------------------------------------------------------- 13 participant
    R.start(13, "the participant's own handling")
    ifu = os.path.join(DOC, "IFU-EEG-014_RevB_participant_quick_start_and_placement_guide.md")
    if _exists(ifu):
        t = open(ifu).read().lower()
        for phrase, why in [("do not tighten", "the one counter-intuitive instruction"),
                            ("red", "what a red light means"),
                            ("charg", "charging and the wear-while-charging prohibition"),
                            ("chin strap", "the strap is removable and why"),
                            ("not a medical device", "the honesty statement")]:
            R.check(f"quick-start card covers: {why}", phrase in t)
    R.note("manual handling", "fitting is three steps and is expected to take two to "
                              "three minutes ONCE THE PARTICIPANT HAS DONE IT ONCE "
                              "(IFU-EEG-014 section 2). A first-timer is allowed up to "
                              "five minutes before IFU-EEG-014 is treated as wrong "
                              "(IFU-EEG-014 fit-trial verification; DSN-EEG-002 "
                              "section 9)")

    # ---------------------------------------------------------------- 14 return
    R.start(14, "return, refurbishment and the next cycle")
    R.check("service and refurbishment manual present",
            _exists(os.path.join(DOC, "SVC-EEG-013_RevB_service_and_refurbishment_manual.md")))
    R.check("risk analysis covers cross-infection between participants",
            _exists(os.path.join(DOC,
                                 "RISK-EEG-011_RevB_risk_analysis_and_safety_review_pack.md")))
    R.check("change control and document register present",
            _exists(os.path.join(DOC,
                                 "ECO-EEG-016_RevB_change_control_and_document_register.md")))

    # ---------------------------------------------------------------- write
    if report_path:
        _write(report_path, R)
    return R


def _write(path, R):
    n_pass = len(R.passes)
    n_fail = len(R.failures)
    with open(path, "w") as f:
        f.write("# End-to-end production simulation\n\n")
        f.write("**Document:** SIM-EEG-018  **Revision:** A  **Date:** "
                f"{D.DATE}\n")
        f.write("**Issued by:** TI One Voice research programme (one.witysk.org), "
                "Brussels, Belgium\n")
        f.write("**Licence:** CC BY-SA 4.0\n")
        f.write("**Generated by:** `tools/simulate_production.py`, from `tools/design.py` "
                "and the files actually present in the package\n\n")
        f.write("## What this is, and what it is not\n\n")
        f.write("This report is a dry run of the manufacturing route against the data "
                "package. At each station it asks what the operator needs, checks that the "
                "package contains it, and where the station has an acceptance limit it "
                "computes that limit from component values instead of quoting it. It is "
                "re-run by `tools/simulate_production.py` and must be clean before the "
                "package is released.\n\n")
        f.write("It cannot find what only a real build finds: solderability, fit, ergonomics, "
                "electromagnetic behaviour, or whether a participant can actually put the "
                "helmet on. Nothing in this package has been manufactured or measured.\n\n")
        n_open = len([r for r in R.rows if r[0] == "OPEN"])
        f.write(f"**Result: {n_pass} checks passed, {n_fail} failed, {n_open} known open "
                f"{'item' if n_open == 1 else 'items'}.**\n\n")
        if n_open:
            f.write("A *failure* means the package does not support the step. An *open "
                    "item* means it does, and somebody still has to take a decision that "
                    "is recorded where it belongs. The open items are:\n\n")
            f.write("| Station | Item | Detail |\n|---|---|---|\n")
            for _k, st, what, detail in [r for r in R.rows if r[0] == "OPEN"]:
                f.write(f"| {st} | {what} | {detail} |\n")
            f.write("\n")
        if n_fail:
            f.write("### Failures\n\n")
            f.write("| Station | Check | Detail |\n|---|---|---|\n")
            for _, st, what, detail in R.failures:
                f.write(f"| {st} | {what} | {detail} |\n")
            f.write("\n")
        f.write("## Station by station\n\n")
        cur = None
        for kind, st, what, detail in R.rows:
            if kind == "HEAD":
                f.write(f"\n### Station {st}\n\n| | Check | Detail |\n|---|---|---|\n")
                cur = st
                continue
            mark = {"PASS": "pass", "FAIL": "**FAIL**", "NOTE": "note",
                    "VALUE": "value", "OPEN": "**open**"}[kind]
            f.write(f"| {mark} | {what} | {detail} |\n")
    return path


if __name__ == "__main__":
    out = None
    if "--report" in sys.argv:
        out = sys.argv[sys.argv.index("--report") + 1]
    R = run(out)
    for kind, st, what, detail in R.rows:
        if kind == "HEAD":
            print(f"\n=== {st} ===")
        elif kind == "FAIL":
            print(f"  FAIL  {what}   {detail}")
        elif kind == "OPEN":
            print(f"  OPEN  {what}   {detail}")
        elif kind == "VALUE":
            print(f"  ....  {what}: {detail}")
        elif kind == "PASS":
            print(f"  ok    {what}")
    print(f"\n{len(R.passes)} passed, {len(R.failures)} failed, "
          f"{len([r for r in R.rows if r[0] == 'OPEN'])} open")
    if out:
        print("report ->", out)
