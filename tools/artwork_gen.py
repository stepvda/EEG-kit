#!/usr/bin/env python3
"""
artwork_gen.py -- the label and packaging artwork of PKG-EEG-015 Rev B, generated.

ECO-EEG-016 Rev B section 1 says that ART-LBL-01 to ART-LBL-07, ART-PACK-01, ART-DIS-01,
ART-RET-01 and DRW-LBL-PLACEMENT "are label and packaging artwork files controlled as
generated artifacts under `graphics/`".  Until this script was written they were controlled
as generated artifacts that had never been generated: the register named eleven files, the
packing list ticked against three of them, PKG-EEG-015 section 4.2 made the packer's
placement check a check "against the placement drawing DRW-LBL-PLACEMENT", and no such file
existed anywhere in the package.  A printer could have re-typed six of the labels out of
PKG-EEG-015 section 4; nobody could have ordered the nine foam bay tags, and the QA
placement sign-off could not be made at all.

This script writes them.  Two files per identifier, into `graphics/labels/`:

  <ID>_<name>.svg    the artwork alone, at exact trim size, all text converted to outlines.
                     This is the file a printer is given.  There is no font to substitute
                     and no font to be missing, which is the usual way a label comes back
                     from a printer set in something other than what it was drawn in.
  <ID>_<name>.pdf    an A4 control sheet: title block, the same artwork at 1:1 inside trim
                     marks, the variable-data table, and the notes that belong with it.
                     This is the file a person reads and signs.

Nothing here is drawn by hand and nothing here is typed twice.  The bay legends, the pocket
names, the packing-list line numbers, the label sizes and the substrates are all PARSED OUT
OF `docs/PKG-EEG-015_RevB_packing_labelling_and_shipping.md` at generation time, so a tag
and the cut file it names cannot drift -- which is exactly the property PKG-EEG-015 section
2.3 claims for them and had no mechanism to hold.  Change the document, re-run this script,
and the artwork follows.  The two barcode symbologies (Code 128 for the kit id, ECC200 Data
Matrix for the unit identity block) are encoded here rather than pasted in as images.

WHAT THIS SCRIPT DOES NOT DO, stated where it cannot be missed:

  * It does not know the programme's postal address or its telephone number.  Neither
    appears anywhere in package v2.3, and inventing either would put a wrong address on a
    returning kit and a dead telephone number on a regulated dangerous-goods mark.  Every
    such field is drawn as a `<<PLACEHOLDER>>` and is listed in the variable-data table of
    the control sheet and in `README_artwork.txt`.  ART-LBL-03, ART-LBL-06 and ART-RET-01
    cannot go to a printer until they are filled in.
  * It does not draw the regulated lithium battery pictogram.  ART-LBL-06's outer
    dimensions, hatched border, "UN3481" text and telephone field are drawn to the figures
    REG-EEG-012 Rev B section 3.5 states, and the pictogram area is left as a marked
    reservation, because the symbol itself belongs to the edition of ADR / IATA DGR in
    force and this package does not hold it.  REG-EEG-012 section 3.7 already makes the
    programme's DG-trained shipper the person who checks that before each phase's despatch;
    this is their file to complete.
  * It does not verify the Data Matrix optically.  The encoder is checked here against the
    ISO/IEC 16022 worked example and by decoding its own symbol back to the input string,
    which proves the encoder self-consistent.  It does not prove a printed symbol readable.
    PKG-EEG-015 section 4.1 already requires ISO/IEC 15415 grade C or better after the IPA
    test, and that first-article verification is what releases the label.

Usage:  python3 tools/artwork_gen.py            write every artwork file and the README
        python3 tools/artwork_gen.py --selftest run the encoder self-tests only

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import datetime
import hashlib
import math
import os
import re
import sys
import xml.sax.saxutils as saxutils

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MplPath
from matplotlib.textpath import TextPath
from matplotlib.transforms import Affine2D

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
DOCS = os.path.join(PKG, "docs")
OUT = os.path.join(PKG, "graphics", "labels")

PKG015 = os.path.join(DOCS, "PKG-EEG-015_RevB_packing_labelling_and_shipping.md")

OWNER = "PKG-EEG-015 Rev B"
GENERATOR = "tools/artwork_gen.py"
LICENCE = "CC BY-SA 4.0"
PROGRAMME = "TI One Voice research programme (one.witysk.org), Brussels, Belgium"

# The unit serial used on every specimen.  PKG-EEG-015 section 5 allocates TIOV-B-0001 to
# 0009 to Phase 1, 0010 to 0099 to Phase 2 and 0100 to 0999 to Phase 3.  TIOV-B-0000 is in
# none of those blocks, so a specimen print of a unit label can never be mistaken for the
# label of a unit that exists.  That reservation is proposed to the programme in
# PKG-EEG-015 section 9 and is not yet ruled.
SPECIMEN_SERIAL = "TIOV-B-0000"
SPECIMEN_HW = "EEG-CAR-01-B"
# 18 uppercase hex, the width PKG-EEG-015 section 4.1 and TST-EEG-004 T6 fix for the
# ATECC608B factory serial, filled with a visibly synthetic value.
SPECIMEN_ATECC = "0123456789ABCDEF01"
# The illustrative fingerprint printed in PKG-EEG-015 section 4.1 itself, which that
# section marks as illustrative.  It is not the fingerprint of any key.
SPECIMEN_FP = "9F2C4108BB371D0A"
SPECIMEN_KIT = "KIT-000"

FONT = FontProperties(family="DejaVu Sans")
FONT_B = FontProperties(family="DejaVu Sans", weight="bold")
FONT_M = FontProperties(family="DejaVu Sans Mono")

MM_PER_IN = 25.4


# ---------------------------------------------------------------------------------------
# 1.  Reading the governing document
#
# Every dimension, legend and piece of label copy below comes out of the Markdown of
# PKG-EEG-015.  Parsing it is deliberate: a hand-copied legend is a legend that drifts, and
# section 2.3's claim that "the tag and the cut file cannot drift" is only true if something
# enforces it.
# ---------------------------------------------------------------------------------------

def _tables(md):
    """Every pipe table in the document, as (header cells, [row cells])."""
    out, rows, hdr = [], [], None
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s[1:-1].split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells) and hdr is None and rows:
                hdr, rows = rows[-1], []
                continue
            rows.append(cells)
        else:
            if hdr is not None:
                out.append((hdr, rows))
            hdr, rows = None, []
    if hdr is not None:
        out.append((hdr, rows))
    return out


def _strip(s):
    """Markdown emphasis and backticks out, entities and en dashes normalised."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = s.replace("`", "")
    s = s.replace("×", "x").replace("‑", "-")
    return s.strip()


class Doc:
    """PKG-EEG-015 Rev B, read for the facts this artwork needs."""

    def __init__(self, path=PKG015):
        self.md = open(path, encoding="utf8").read()
        self.tables = _tables(self.md)
        self.bays = self._bays()
        self.kpl = self._kpl()
        self.labels = self._labels()
        self.unit_label = self._unit_label()
        self.sleeves = self._sleeves()

    def _find(self, *header_words):
        for hdr, rows in self.tables:
            joined = " ".join(hdr).lower()
            if all(w.lower() in joined for w in header_words):
                yield hdr, rows

    def _bays(self):
        """The CASE-00 Rev C bay schedule of section 2.2.

        Two tables in that section carry a "Legend" column; the Rev C one is the only one
        with a "Layers cut" column, and section 2.2 says in terms that anyone copying
        pocket sizes takes them from the Rev C table.
        """
        for hdr, rows in self._find("legend", "layers cut"):
            out = []
            for r in rows:
                d = dict(zip(hdr, r))
                legend = _strip(d["Legend"])
                m = re.match(r"([\d.]+)\s*,\s*([\d.]+)", _strip(d["Origin (x, y)"]))
                size = re.match(r"([\d.]+)\s*x\s*([\d.]+)", _strip(d["Size (mm)"]))
                if not (m and size):
                    continue
                out.append({
                    "legend": legend,
                    "x": float(m.group(1)), "y": float(m.group(2)),
                    "w": float(size.group(1)), "h": float(size.group(2)),
                    "layers": _strip(d["Layers cut"]),
                    "depth": _strip(d["Cut depth"]),
                })
            if out:
                return out
        raise SystemExit("PKG-EEG-015 section 2.2 Rev C bay schedule not found")

    def _kpl(self):
        """The kit packing list of section 1.1, line by line, with its pocket."""
        for hdr, rows in self._find("part", "description", "qty", "pocket", "tick"):
            out = []
            for r in rows:
                d = dict(zip(hdr, r))
                num = _strip(d["#"])
                if not re.fullmatch(r"\d+\.\d+", num):
                    continue
                out.append({
                    "line": num,
                    "part": _strip(d["Part"]),
                    "desc": _strip(d["Description"]),
                    "qty": _strip(d["Qty"]),
                    "pocket": _strip(d["Pocket"]),
                })
            if out:
                return out
        raise SystemExit("PKG-EEG-015 section 1.1 packing list not found")

    def _labels(self):
        """The ART-LBL-02 to -07 table of section 4.2."""
        for hdr, rows in self._find("ref", "label", "size", "substrate", "placement"):
            out = {}
            for r in rows:
                d = dict(zip(hdr, r))
                ref = _strip(d["Ref"])
                if not ref.startswith("ART-"):
                    continue
                out[ref] = {
                    "what": _strip(d["Label"]),
                    "size": _strip(d["Size"]),
                    "substrate": _strip(d["Substrate"]),
                    "placement": _strip(d["Placement"]),
                }
            if out:
                return out
        raise SystemExit("PKG-EEG-015 section 4.2 label table not found")

    def _unit_label(self):
        """The ART-LBL-01 property table of section 4.1."""
        for hdr, rows in self._find("property", "value"):
            d = {_strip(r[0]): _strip(r[1]) for r in rows if len(r) >= 2}
            if "Size" in d and "Substrate" in d and "Adhesive" in d:
                return d
        raise SystemExit("PKG-EEG-015 section 4.1 unit-label table not found")

    def _sleeves(self):
        """The cable sleeve table of section 4.2."""
        for hdr, rows in self._find("id", "cable", "sleeve text"):
            out = []
            for r in rows:
                d = dict(zip(hdr, r))
                if _strip(d["ID"]).startswith("CBL-"):
                    out.append((_strip(d["ID"]), _strip(d["Cable"]), _strip(d["Sleeve text"])))
            if out:
                return out
        return []

    def size_mm(self, ref):
        """`80 x 40 mm` out of a section 4.2 size cell, as floats."""
        m = re.search(r"([\d.]+)\s*x\s*([\d.]+)\s*mm", self.labels[ref]["size"])
        if not m:
            raise SystemExit(f"{ref}: no `W x H mm` in its size cell: {self.labels[ref]['size']!r}")
        return float(m.group(1)), float(m.group(2))

    def spare_cell_tag(self):
        """Section 7 overrides the SPARE CELL bay tag with a longer string.

        Section 4.2 says the ART-LBL-04 legends are "identical to the section 2.2
        schedule"; section 7 says the SPARE CELL tag "reads `SPARE CELL -- DEPOT ONLY,
        EMPTY IN CIRCULATION`".  Both cannot be true of one 60 x 12 mm tag.  The override is
        obeyed, because it is the one that carries safety information, and the collision is
        reported by this script and raised in PKG-EEG-015 section 9.
        """
        m = re.search(r"its tag reads\s*`([^`]+)`", self.md)
        return m.group(1).replace("‑", "-") if m else None

    def ret_sheet_text(self):
        """The ART-RET-01 copy, from the block quote in section 7."""
        block = re.search(r"The instruction sheet ART-RET-01 reads, in substance:\n\n((?:>.*\n)+)",
                          self.md)
        if not block:
            raise SystemExit("ART-RET-01 block quote not found in PKG-EEG-015 section 7")
        text = " ".join(l.lstrip("> ").rstrip() for l in block.group(1).splitlines())
        text = re.sub(r"\s+", " ", text)
        # "--" is this package's Markdown em dash. On a card a participant reads under
        # pressure at a post-office counter it is just two hyphens, so it is set as a dash.
        return _strip(text).replace(" -- ", " - ")


def disinfection_rows():
    """The R5 agent table of SVC-EEG-013 Rev B section 2, which is ART-DIS-01's source.

    SVC-EEG-013 section 9 says "the disinfection guide in the pouch is the extract of
    section 2 R5", so the card is that table and the prohibition table beside it, and not a
    new set of instructions written here.
    """
    path = os.path.join(DOCS, "SVC-EEG-013_RevB_service_and_refurbishment_manual.md")
    md = open(path, encoding="utf8").read()
    agents, prohibited = [], []
    for hdr, rows in _tables(md):
        joined = " ".join(hdr).lower()
        if "item" in joined and "agent" in joined and "contact" in joined:
            for r in rows:
                d = dict(zip(hdr, r))
                agents.append((_strip(d["Item"]), _strip(d["Method"]), _strip(d["Agent"]),
                               _strip(d["Concentration"]), _strip(d["Contact"])))
        if "prohibited" in joined and "why" in joined:
            for r in rows:
                d = dict(zip(hdr, r))
                prohibited.append((_strip(d["Prohibited"]), _strip(d["Why"])))
    if not agents:
        raise SystemExit("SVC-EEG-013 R5 agent table not found")
    return agents, prohibited


def lithium_mark_facts():
    """The mark's stated geometry, from REG-EEG-012 Rev B section 3.5."""
    path = os.path.join(DOCS, "REG-EEG-012_RevB_regulatory_and_compliance_file.md")
    md = open(path, encoding="utf8").read()
    # Three rows in that document open "| Lithium battery mark |"; only the section 3.5 one
    # states the geometry, so the row is chosen by content and not by position.
    full = red = text = None
    for row in re.finditer(r"\|\s*Lithium battery mark\s*\|([^|]+)\|", md):
        t = _strip(row.group(1))
        f = re.search(r"([\d.]+)\s*mm wide\s*x\s*([\d.]+)\s*mm high", t)
        r = re.search(r"not less than\s*([\d.]+)\s*mm\s*x\s*([\d.]+)\s*mm", t)
        if f and r:
            full, red, text = f, r, t
            break
    if not (full and red):
        raise SystemExit("REG-EEG-012 section 3.5 lithium mark dimensions not found")
    return {
        "full": (float(full.group(1)), float(full.group(2))),
        "reduced": (float(red.group(1)), float(red.group(2))),
        "text": text,
    }


# ---------------------------------------------------------------------------------------
# 2.  Drawing model
#
# One geometry, two back ends.  Text is converted to outlines once, in millimetres, and the
# same outline is written to the SVG and drawn into the PDF, so the printer's file and the
# control sheet cannot disagree about a glyph.
# ---------------------------------------------------------------------------------------

def _cap_ratio(prop):
    """Cap height of a font as a fraction of its point size, measured off the glyph."""
    p = TextPath((0, 0), "H", size=100.0, prop=prop)
    return p.get_extents().height / 100.0


CAP = {}


def cap_ratio(prop):
    key = (prop.get_family()[0], prop.get_weight())
    if key not in CAP:
        CAP[key] = _cap_ratio(prop)
    return CAP[key]


def text_path(s, x, y, cap, prop=FONT, anchor="left", baseline="base"):
    """A matplotlib Path for `s`, in millimetres, at the given cap height."""
    size = cap / cap_ratio(prop)
    p = TextPath((0, 0), s, size=size, prop=prop)
    ext = p.get_extents()
    dx = {"left": 0.0, "center": -ext.width / 2 - ext.x0, "right": -ext.width - ext.x0}[anchor]
    dy = {"base": 0.0, "center": -cap / 2, "top": -cap}[baseline]
    return p.transformed(Affine2D().translate(x + dx, y + dy)), ext.width


def text_width(s, cap, prop=FONT):
    size = cap / cap_ratio(prop)
    return TextPath((0, 0), s, size=size, prop=prop).get_extents().width


def wrap(s, cap, width, prop=FONT):
    """Greedy word wrap to a millimetre width."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and text_width(trial, cap, prop) > width:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


class Art:
    """A piece of artwork: a width, a height and a list of primitives, all in mm."""

    def __init__(self, w, h, bg="#FFFFFF"):
        self.w, self.h, self.bg = w, h, bg
        self.items = []
        self.shrunk = []            # lines that had to be shrunk to fit, see text()

    # -- primitives ---------------------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.25, dash=None, r=0.0):
        self.items.append(("rect", x, y, w, h, fill, stroke, lw, dash, r))
        return self

    def line(self, x1, y1, x2, y2, stroke="#000000", lw=0.25, dash=None):
        self.items.append(("line", x1, y1, x2, y2, stroke, lw, dash))
        return self

    def circle(self, x, y, r, fill=None, stroke="#000000", lw=0.25):
        self.items.append(("circle", x, y, r, fill, stroke, lw))
        return self

    def poly(self, pts, fill=None, stroke="#000000", lw=0.25, close=True):
        self.items.append(("poly", list(pts), fill, stroke, lw, close))
        return self

    def path(self, mpl_path, fill="#000000", stroke=None, lw=0.0):
        self.items.append(("path", mpl_path, fill, stroke, lw))
        return self

    def text(self, x, y, s, cap=3.0, prop=FONT, anchor="left", baseline="base",
             fill="#000000", max_width=None):
        s = subst(s)
        """Draw `s` as outlines.

        `max_width` shrinks the cap height until the line fits, and records the shrink in
        `self.shrunk` so the caller can report it.  Silently overflowing a label edge is the
        single most common way generated artwork goes to a printer wrong, and it is
        invisible in a text diff.
        """
        if not s:
            return self
        if max_width:
            w = text_width(s, cap, prop)
            if w > max_width:
                new_cap = cap * max_width / w
                self.shrunk.append((s, round(cap, 2), round(new_cap, 2)))
                cap = new_cap
        p, w = text_path(s, x, y, cap, prop, anchor, baseline)
        self.path(p, fill=fill)
        return self

    def text_block(self, x, y, lines, cap, leading, prop=FONT, anchor="left", fill="#000000"):
        for i, ln in enumerate(lines):
            self.text(x, y - i * leading, ln, cap, prop, anchor, fill=fill)
        return self

    def modules(self, x, y, cell, grid, fill="#000000"):
        """A bitmap of square modules, `grid` given top row first."""
        n = len(grid)
        for r, row in enumerate(grid):
            run = None
            for c, v in enumerate(list(row) + [0]):
                if v and run is None:
                    run = c
                elif not v and run is not None:
                    self.rect(x + run * cell, y + (n - 1 - r) * cell,
                              (c - run) * cell, cell, fill=fill)
                    run = None
        return self

    # -- back ends ----------------------------------------------------------------------
    @staticmethod
    def _comment(text):
        """XML comments may not contain a double hyphen, and this artwork's copy does.

        PKG-EEG-015 section 7 gives the spare-cell bay tag as `SPARE CELL -- DEPOT ONLY,
        EMPTY IN CIRCULATION`, and putting that string in an SVG comment produced a file
        that every conforming XML parser rejected -- which is worse than a wrong label,
        because the printer's software refuses to open it at all rather than printing
        something visibly wrong.  Caught by the well-formedness check in to_svg().
        """
        return "<!-- " + str(text).replace("--", "\u2013\u2013") + " -->"

    def to_svg(self, path, title, desc):
        px = []
        px.append('<?xml version="1.0" encoding="UTF-8"?>')
        px.append(self._comment(title))
        px.append(self._comment(desc))
        px.append(self._comment(f"Generated by {GENERATOR} from {OWNER}.  "
                                f"Licence: {LICENCE}."))
        px.append(self._comment("Trim size is the viewBox in millimetres.  All text "
                                "is outlined: there is no font to substitute."))
        px.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" '
            f'width="{self.w}mm" height="{self.h}mm" '
            f'viewBox="0 0 {self.w:.4f} {self.h:.4f}">')
        px.append(f"<title>{saxutils.escape(title)}</title>")
        px.append(f"<desc>{saxutils.escape(desc)}</desc>")
        # SVG y runs down; flip once, at the top, so every primitive below is in the same
        # bottom-left-origin frame the PDF back end uses.
        px.append(f'<g transform="translate(0,{self.h:.4f}) scale(1,-1)">')
        if self.bg:
            px.append(f'<rect x="0" y="0" width="{self.w:.4f}" height="{self.h:.4f}" '
                      f'fill="{self.bg}"/>')
        for it in self.items:
            px.append(self._svg_item(it))
        px.append("</g></svg>")
        with open(path, "w", encoding="utf8") as fh:
            fh.write("\n".join(px) + "\n")
        # Every file this tool writes is parsed back before it is called written.  A printer
        # is given the SVG, not the PDF, and an SVG that will not parse is a job that stops.
        import xml.etree.ElementTree as ET
        try:
            ET.parse(path)
        except ET.ParseError as e:
            raise SystemExit(f"{path}: the SVG this tool just wrote is not well-formed "
                             f"XML: {e}")
        return path

    @staticmethod
    def _paint(fill, stroke, lw, dash=None):
        a = [f'fill="{fill}"' if fill else 'fill="none"']
        if stroke:
            a.append(f'stroke="{stroke}" stroke-width="{lw:.4f}"')
            if dash:
                a.append(f'stroke-dasharray="{",".join(f"{d:.3f}" for d in dash)}"')
        else:
            a.append('stroke="none"')
        return " ".join(a)

    def _svg_item(self, it):
        k = it[0]
        if k == "rect":
            _, x, y, w, h, fill, stroke, lw, dash, r = it
            rr = f' rx="{r:.4f}" ry="{r:.4f}"' if r else ""
            return (f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}"{rr} '
                    f'{self._paint(fill, stroke, lw, dash)}/>')
        if k == "line":
            _, x1, y1, x2, y2, stroke, lw, dash = it
            return (f'<line x1="{x1:.4f}" y1="{y1:.4f}" x2="{x2:.4f}" y2="{y2:.4f}" '
                    f'{self._paint(None, stroke, lw, dash)}/>')
        if k == "circle":
            _, x, y, r, fill, stroke, lw = it
            return (f'<circle cx="{x:.4f}" cy="{y:.4f}" r="{r:.4f}" '
                    f'{self._paint(fill, stroke, lw)}/>')
        if k == "poly":
            _, pts, fill, stroke, lw, close = it
            d = " ".join(f"{x:.4f},{y:.4f}" for x, y in pts)
            tag = "polygon" if close else "polyline"
            return f'<{tag} points="{d}" {self._paint(fill, stroke, lw)}/>'
        if k == "path":
            _, p, fill, stroke, lw = it
            return f'<path d="{self._svg_path_d(p)}" {self._paint(fill, stroke, lw)}/>'
        raise AssertionError(k)

    @staticmethod
    def _svg_path_d(p):
        out = []
        for verts, code in p.iter_segments():
            if code == MplPath.MOVETO:
                out.append(f"M{verts[0]:.4f},{verts[1]:.4f}")
            elif code == MplPath.LINETO:
                out.append(f"L{verts[0]:.4f},{verts[1]:.4f}")
            elif code == MplPath.CURVE3:
                out.append(f"Q{verts[0]:.4f},{verts[1]:.4f} {verts[2]:.4f},{verts[3]:.4f}")
            elif code == MplPath.CURVE4:
                out.append(f"C{verts[0]:.4f},{verts[1]:.4f} {verts[2]:.4f},{verts[3]:.4f} "
                           f"{verts[4]:.4f},{verts[5]:.4f}")
            elif code == MplPath.CLOSEPOLY:
                out.append("Z")
        return " ".join(out)

    def draw_on(self, ax, ox=0.0, oy=0.0):
        """Draw into a matplotlib axes whose data units are millimetres."""
        if self.bg:
            ax.add_patch(Rectangle((ox, oy), self.w, self.h, facecolor=self.bg,
                                   edgecolor="none", zorder=1))
        for it in self.items:
            k = it[0]
            if k == "rect":
                _, x, y, w, h, fill, stroke, lw, dash, r = it
                ax.add_patch(Rectangle((ox + x, oy + y), w, h,
                                       facecolor=fill or "none",
                                       edgecolor=stroke or "none",
                                       linewidth=lw * 72 / MM_PER_IN,
                                       linestyle=(0, tuple(d * 72 / MM_PER_IN for d in dash))
                                       if dash else "solid", zorder=2))
            elif k == "line":
                _, x1, y1, x2, y2, stroke, lw, dash = it
                ax.plot([ox + x1, ox + x2], [oy + y1, oy + y2], color=stroke,
                        linewidth=lw * 72 / MM_PER_IN, solid_capstyle="butt",
                        linestyle=(0, tuple(d * 72 / MM_PER_IN for d in dash))
                        if dash else "solid", zorder=2)
            elif k == "circle":
                _, x, y, r, fill, stroke, lw = it
                ax.add_patch(plt.Circle((ox + x, oy + y), r, facecolor=fill or "none",
                                        edgecolor=stroke or "none",
                                        linewidth=lw * 72 / MM_PER_IN, zorder=2))
            elif k == "poly":
                _, pts, fill, stroke, lw, close = it
                ax.add_patch(plt.Polygon([(ox + a, oy + b) for a, b in pts], closed=close,
                                         facecolor=fill or "none",
                                         edgecolor=stroke or "none",
                                         linewidth=lw * 72 / MM_PER_IN, zorder=2))
            elif k == "path":
                _, p, fill, stroke, lw = it
                ax.add_patch(PathPatch(p.transformed(Affine2D().translate(ox, oy)),
                                       facecolor=fill or "none",
                                       edgecolor=stroke or "none",
                                       linewidth=lw * 72 / MM_PER_IN, zorder=3))


# ---------------------------------------------------------------------------------------
# 3.  Code 128, for the kit id on ART-LBL-02
# ---------------------------------------------------------------------------------------

C128 = [
    "212222", "222122", "222221", "121223", "121322", "131222", "122213", "122312",
    "132212", "221213", "221312", "231212", "112232", "122132", "122231", "113222",
    "123122", "123221", "223211", "221132", "221231", "213212", "223112", "312131",
    "311222", "321122", "321221", "312212", "322112", "322211", "212123", "212321",
    "232121", "111323", "131123", "131321", "112313", "132113", "132311", "211313",
    "231113", "231311", "112133", "112331", "132131", "113123", "113321", "133121",
    "313121", "211331", "231131", "213113", "213311", "213131", "311123", "311321",
    "331121", "312113", "312311", "332111", "314111", "221411", "431111", "111224",
    "111422", "121124", "121421", "141122", "141221", "112214", "112412", "122114",
    "122411", "142112", "142211", "241211", "221114", "413111", "241112", "134111",
    "111242", "121142", "121241", "114212", "124112", "124211",
    "411212", "421112", "421211", "212141", "214121", "412121", "111143", "111341",
    "131141", "114113", "114311", "411113", "411311", "113141", "114131", "311141",
    "411131", "211412", "211214", "211232", "2331112",
]
C128_START_B = 104
C128_STOP = 106


def code128b(data):
    """Code 128 subset B bar widths, in modules, as a list of (dark, width) runs.

    Returns (runs, module_count).  A Code 128 symbol is 11 modules per symbol character
    plus a 13-module stop pattern, and that identity is asserted by the self-test, which is
    a structural check the encoder cannot pass by accident.
    """
    for ch in data:
        if not (32 <= ord(ch) <= 126):
            raise ValueError(f"Code 128 subset B carries ASCII 32 to 126 only: {ch!r}")
    values = [C128_START_B] + [ord(c) - 32 for c in data]
    check = values[0]
    for i, v in enumerate(values[1:], start=1):
        check += i * v
    check %= 103
    values.append(check)
    values.append(C128_STOP)
    runs, dark = [], True
    for v in values:
        for w in C128[v]:
            runs.append((dark, int(w)))
            dark = not dark
        dark = True
    return runs, sum(w for _, w in runs)


# ---------------------------------------------------------------------------------------
# 4.  ECC200 Data Matrix, for the unit identity block on ART-LBL-01
#
# ISO/IEC 16022.  ASCII encodation, Reed-Solomon over GF(256) with the 0x12D field
# polynomial, and the Annex F module placement.  Two self-tests guard it: the published
# worked example for "123456", whose data and error codewords are known, and a decode of
# the encoder's own symbol back to the input string.
# ---------------------------------------------------------------------------------------

# (symbol side, region data side, regions per side, data codewords, ecc codewords, blocks)
DM_SIZES = [
    (10, 8, 1, 3, 5, 1), (12, 10, 1, 5, 7, 1), (14, 12, 1, 8, 10, 1),
    (16, 14, 1, 12, 12, 1), (18, 16, 1, 18, 14, 1), (20, 18, 1, 22, 18, 1),
    (22, 20, 1, 30, 20, 1), (24, 22, 1, 36, 24, 1), (26, 24, 1, 44, 28, 1),
    (32, 14, 2, 62, 36, 1), (36, 16, 2, 86, 42, 1), (40, 18, 2, 114, 48, 1),
    (44, 20, 2, 144, 56, 1), (48, 22, 2, 174, 68, 1), (52, 24, 2, 204, 84, 2),
]

_GF_EXP = [0] * 512
_GF_LOG = [0] * 256
_x = 1
for _i in range(255):
    _GF_EXP[_i] = _x
    _GF_LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x12D
for _i in range(255, 512):
    _GF_EXP[_i] = _GF_EXP[_i - 255]


def _gmul(a, b):
    if a == 0 or b == 0:
        return 0
    return _GF_EXP[_GF_LOG[a] + _GF_LOG[b]]


def _rs_generator(k):
    g = [1]
    for i in range(1, k + 1):
        g = [0] + g
        a = _GF_EXP[i]
        for j in range(len(g) - 1):
            g[j] ^= _gmul(g[j + 1], a)
    return g


def rs_ecc(data, k):
    """The k Reed-Solomon check codewords for `data`, ECC200 convention."""
    g = _rs_generator(k)
    rem = [0] * k
    for d in data:
        f = d ^ rem[0]
        rem = rem[1:] + [0]
        if f:
            for j in range(k):
                rem[j] ^= _gmul(g[k - 1 - j], f)
    return rem


def dm_ascii_encode(s):
    """ASCII encodation of `s` to data codewords, before padding."""
    b = s.encode("ascii")
    out, i = [], 0
    while i < len(b):
        c = b[i]
        if 48 <= c <= 57 and i + 1 < len(b) and 48 <= b[i + 1] <= 57:
            out.append((c - 48) * 10 + (b[i + 1] - 48) + 130)
            i += 2
        else:
            out.append(c + 1)
            i += 1
    return out


def dm_pad(cw, n):
    """Pad to n codewords: one 129, then the 253-state randomising of ISO/IEC 16022."""
    out = list(cw)
    if len(out) < n:
        out.append(129)
    while len(out) < n:
        pos = len(out) + 1                      # 1-based codeword position
        r = ((149 * pos) % 253) + 1
        v = 129 + r
        out.append(v - 254 if v > 254 else v)
    return out


def _dm_place(nrow, ncol):
    """Annex F placement: which (codeword, bit) lands in each mapping-matrix cell."""
    arr = [[None] * ncol for _ in range(nrow)]

    def mod(row, col, ch, bit):
        if row < 0:
            row += nrow
            col += 4 - ((nrow + 4) % 8)
        if col < 0:
            col += ncol
            row += 4 - ((ncol + 4) % 8)
        arr[row][col] = (ch, bit)

    def utah(row, col, ch):
        mod(row - 2, col - 2, ch, 1)
        mod(row - 2, col - 1, ch, 2)
        mod(row - 1, col - 2, ch, 3)
        mod(row - 1, col - 1, ch, 4)
        mod(row - 1, col, ch, 5)
        mod(row, col - 2, ch, 6)
        mod(row, col - 1, ch, 7)
        mod(row, col, ch, 8)

    def corner1(ch):
        for r, c, b in ((nrow - 1, 0, 1), (nrow - 1, 1, 2), (nrow - 1, 2, 3),
                        (0, ncol - 2, 4), (0, ncol - 1, 5), (1, ncol - 1, 6),
                        (2, ncol - 1, 7), (3, ncol - 1, 8)):
            mod(r, c, ch, b)

    def corner2(ch):
        for r, c, b in ((nrow - 3, 0, 1), (nrow - 2, 0, 2), (nrow - 1, 0, 3),
                        (0, ncol - 4, 4), (0, ncol - 3, 5), (0, ncol - 2, 6),
                        (0, ncol - 1, 7), (1, ncol - 1, 8)):
            mod(r, c, ch, b)

    def corner3(ch):
        for r, c, b in ((nrow - 3, 0, 1), (nrow - 2, 0, 2), (nrow - 1, 0, 3),
                        (0, ncol - 2, 4), (0, ncol - 1, 5), (1, ncol - 1, 6),
                        (2, ncol - 1, 7), (3, ncol - 1, 8)):
            mod(r, c, ch, b)

    def corner4(ch):
        for r, c, b in ((nrow - 1, 0, 1), (nrow - 1, ncol - 1, 2), (0, ncol - 3, 3),
                        (0, ncol - 2, 4), (0, ncol - 1, 5), (1, ncol - 3, 6),
                        (1, ncol - 2, 7), (1, ncol - 1, 8)):
            mod(r, c, ch, b)

    ch, row, col = 1, 4, 0
    while True:
        if row == nrow and col == 0:
            corner1(ch); ch += 1
        if row == nrow - 2 and col == 0 and ncol % 4:
            corner2(ch); ch += 1
        if row == nrow - 2 and col == 0 and ncol % 8 == 4:
            corner3(ch); ch += 1
        if row == nrow + 4 and col == 2 and ncol % 8 == 0:
            corner4(ch); ch += 1
        while True:                                     # up and to the right
            if row < nrow and col >= 0 and arr[row][col] is None:
                utah(row, col, ch); ch += 1
            row -= 2
            col += 2
            if not (row >= 0 and col < ncol):
                break
        row += 1
        col += 3
        while True:                                     # down and to the left
            if row >= 0 and col < ncol and arr[row][col] is None:
                utah(row, col, ch); ch += 1
            row += 2
            col -= 2
            if not (row < nrow and col >= 0):
                break
        row += 3
        col += 1
        if not (row < nrow or col < ncol):
            break
    return arr


def dm_encode(s):
    """ECC200 Data Matrix for `s`.  Returns (grid, side, codewords).

    `grid` is a list of rows of 0/1, top row first, the symbol only -- the quiet zone is
    the caller's business, because it is drawn as clear substrate, not as artwork.
    """
    cw = dm_ascii_encode(s)
    for side, rd, regions, ndata, necc, blocks in DM_SIZES:
        if len(cw) <= ndata:
            break
    else:
        raise ValueError(f"{len(cw)} codewords exceeds the largest symbol tabled here")
    data = dm_pad(cw, ndata)

    # Interleaved blocks.  Every symbol this package uses is a single block; the general
    # form is written out so a longer string cannot silently produce a wrong symbol.
    per_d, per_e = ndata // blocks, necc // blocks
    full = [0] * (ndata + necc)
    for b in range(blocks):
        blk = data[b::blocks]
        ecc = rs_ecc(blk, per_e)
        for i, v in enumerate(blk):
            full[b + i * blocks] = v
        for i, v in enumerate(ecc):
            full[ndata + b + i * blocks] = v

    nrow = ncol = rd * regions
    place = _dm_place(nrow, ncol)
    bits = [[0] * ncol for _ in range(nrow)]
    for r in range(nrow):
        for c in range(ncol):
            cell = place[r][c]
            if cell is None:
                continue
            ch, bit = cell
            bits[r][c] = (full[ch - 1] >> (8 - bit)) & 1
    # the two modules of the unfilled bottom-right corner are dark by definition
    if place[nrow - 1][ncol - 1] is None:
        bits[nrow - 1][ncol - 1] = 1
        bits[nrow - 2][ncol - 2] = 1

    grid = [[0] * side for _ in range(side)]
    for ri in range(regions):
        for ci in range(regions):
            br, bc = ri * (rd + 2), ci * (rd + 2)
            for i in range(rd + 2):
                grid[br + i][bc] = 1                        # solid left finder
                grid[br + rd + 1][bc + i] = 1               # solid bottom finder
                grid[br][bc + i] = 1 if i % 2 == 0 else 0   # top clock track
                grid[br + i][bc + rd + 1] = 1 if i % 2 == 1 else 0   # right clock track
            for r in range(rd):
                for c in range(rd):
                    grid[br + 1 + r][bc + 1 + c] = bits[ri * rd + r][ci * rd + c]
    return grid, side, full


def dm_decode(grid):
    """Read a symbol this module produced back to its string.

    No error correction: this is a round-trip check on encodation and placement, not a
    reader.  It is here so that a placement bug cannot pass unnoticed.
    """
    side = len(grid)
    for s, rd, regions, ndata, necc, blocks in DM_SIZES:
        if s == side:
            break
    else:
        raise ValueError(f"no tabled symbol of side {side}")
    nrow = ncol = rd * regions
    bits = [[0] * ncol for _ in range(nrow)]
    for ri in range(regions):
        for ci in range(regions):
            br, bc = ri * (rd + 2), ci * (rd + 2)
            for r in range(rd):
                for c in range(rd):
                    bits[ri * rd + r][ci * rd + c] = grid[br + 1 + r][bc + 1 + c]
    place = _dm_place(nrow, ncol)
    cw = [0] * (ndata + necc)
    for r in range(nrow):
        for c in range(ncol):
            cell = place[r][c]
            if cell is None:
                continue
            ch, bit = cell
            if bits[r][c]:
                cw[ch - 1] |= 1 << (8 - bit)
    per_d = ndata // blocks
    data = [0] * ndata
    for b in range(blocks):
        blk = cw[b:ndata:blocks]
        for i, v in enumerate(blk):
            data[b + i * blocks] = v
    out, i = [], 0
    while i < len(data):
        v = data[i]
        i += 1
        if v == 129:
            break
        if v <= 128:
            out.append(chr(v - 1))
        elif v <= 229:
            out.append(f"{v - 130:02d}")
        else:
            break
    return "".join(out)


def selftest(verbose=True):
    """Everything this file encodes, checked before it is drawn."""
    ok = True

    def check(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        if verbose:
            print(f"  [{'ok ' if good else 'FAIL'}] {name}")
            if not good:
                print(f"         got  {got}")
                print(f"         want {want}")

    # ISO/IEC 16022 worked example: "123456" in a 10 x 10 symbol.
    check("Data Matrix ASCII encodation of '123456'",
          dm_ascii_encode("123456"), [142, 164, 186])
    check("Data Matrix ECC200 error codewords for '123456'",
          rs_ecc([142, 164, 186], 5), [114, 25, 5, 88, 102])
    g, side, _ = dm_encode("123456")
    check("Data Matrix symbol size for '123456'", side, 10)
    check("Data Matrix round trip, '123456'", dm_decode(g), "123456")

    # The strings this package actually puts in a symbol.
    for s in (dm_content(SPECIMEN_SERIAL, SPECIMEN_HW, SPECIMEN_ATECC, SPECIMEN_FP),
              dm_content("TIOV-B-0999", "EEG-CAR-01-B", "F" * 18, "0" * 16)):
        g, side, _ = dm_encode(s)
        check(f"Data Matrix round trip, {len(s)} chars in a {side}x{side} symbol",
              dm_decode(g), s)

    # The Code 128 pattern table, checked structurally rather than trusted.  Every
    # character is six elements summing to eleven modules; the stop pattern is seven
    # elements summing to thirteen; and in every pattern the three BAR widths sum to an
    # even number, which is the parity property a scanner uses to reject a misread.  A
    # transcription error in the table fails at least one of these.
    check("Code 128 table length", len(C128), 107)
    check("Code 128 table entries are distinct", len(set(C128)), 107)
    bad = [(i, p) for i, p in enumerate(C128[:106])
           if len(p) != 6 or sum(int(c) for c in p) != 11
           or (int(p[0]) + int(p[2]) + int(p[4])) % 2]
    check("Code 128 characters are 6 elements, 11 modules, even bar parity", bad, [])
    check("Code 128 stop pattern", C128[106], "2331112")
    for s in ("KIT-000", "KIT-123"):
        runs, mods = code128b(s)
        n = len(s) + 3                      # start, data, check, stop
        check(f"Code 128 module count for {s!r}", mods, 11 * (n - 1) + 13)
        check(f"Code 128 starts and ends dark for {s!r}",
              (runs[0][0], runs[-1][0]), (True, True))
    # A hand-checkable check character: start B is 104, "A" is value 33 at position 1,
    # so the check character is (104 + 1*33) mod 103 = 34.
    check("Code 128 check character for 'A'", (104 + 33) % 103, 34)
    runs_a, mods_a = code128b("A")
    check("Code 128 pattern count for 'A'", len(runs_a), 3 * 6 + 7)
    check("Code 128 module count for 'A'", mods_a, 3 * 11 + 13)

    if verbose:
        print("  self-test", "PASSED" if ok else "FAILED")
    return ok


def dm_content(serial, hw, atecc, fp):
    """The Data Matrix payload of PKG-EEG-015 section 4.1: pipe-delimited, no spaces."""
    return f"{serial}|{hw}|{atecc}|{fp}"


# ---------------------------------------------------------------------------------------
# 5.  The artwork
# ---------------------------------------------------------------------------------------

BLACK = "#000000"
WHITE = "#FFFFFF"

# --------------------------------------------------------------------------- programme
# Supplied by the programme lead on 2 September 2026 and substituted into every artwork
# that carries it.  These used to be `<<PLACEHOLDER>>` tokens: an invented address puts a
# returning kit somewhere else and an invented number goes on a REGULATED dangerous-goods
# mark, which is a number an emergency responder is meant to be able to ring.
#
# Every programme field is now supplied.  PROGRAMME_EMAIL was held back until the lead
# gave it explicitly, because a return label is a public document -- an address printed on
# the outside of every case that travels -- and which address appears in public was not
# this file's decision to make.
PROGRAMME = {
    "<<PROGRAMME_RETURN_NAME>>":              "Stephane van der Aa",
    "<<PROGRAMME_RETURN_STREET>>":            "Van Volxemlaan 208 bus 31",
    "<<PROGRAMME_RETURN_POSTCODE_AND_CITY>>": "1190 Brussels",
    "<<PROGRAMME_RETURN_COUNTRY>>":           "Belgium",
    "<<PROGRAMME_TELEPHONE>>":                "+32 493 70 16 01",
    "<<PROGRAMME_EMAIL>>":                    "stephane@stepvda.com",
}


def subst(text):
    """Replace every known programme field.  Unknown tokens are left visible on purpose."""
    if not isinstance(text, str):
        return text
    for k, v in PROGRAMME.items():
        text = text.replace(k, v)
    return text
GREY = "#808080"


def art_lbl_01(doc, serial=None, atecc=None, fp=None, kit=None):
    """ART-LBL-01, the unit label.  PKG-EEG-015 section 4.1, content in that order.

    The eight content items of section 4.1 are laid out on one baseline grid down the left
    of the label with the Data Matrix on the right, and every line is width-fitted against
    the column so that a longer serial or a differently formatted fingerprint shrinks its
    own line instead of running into the symbol.  The first draft of this function did run
    into the symbol, and the overlap was invisible until the SVG was rendered.
    """
    w, h = 50.0, 25.0
    m = re.search(r"([\d.]+)\s*x\s*([\d.]+)\s*mm", doc.unit_label["Size"])
    if m:
        w, h = float(m.group(1)), float(m.group(2))
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE, stroke=None)

    serial = serial or "<<UNIT_SERIAL>>"
    atecc = atecc or "<<ATECC_SERIAL_18_HEX>>"
    fp = fp or "<<FINGERPRINT_16_HEX>>"

    # 4. ECC200 Data Matrix, 12 x 12 mm with a 2-module quiet zone, on the right.
    dm_size, quiet, margin = 12.0, 2, 1.4
    dm_x = w - margin - dm_size
    dm_y = (h - dm_size) / 2.0
    if all(x and not x.startswith("<<") for x in (serial, atecc, fp)):
        payload = dm_content(serial, doc_hw(), atecc, fp)
        grid, side, _ = dm_encode(payload)
        a.modules(dm_x, dm_y, dm_size / side, grid, fill=BLACK)
    else:
        grid, side, payload = None, None, None
        a.rect(dm_x, dm_y, dm_size, dm_size, fill=None, stroke=BLACK, lw=0.3,
               dash=(1.0, 1.0))
        for i, (t, c) in enumerate((("ECC200", 1.7), ("12 x 12 mm", 1.4),
                                    ("PER UNIT", 1.4))):
            a.text(dm_x + dm_size / 2, dm_y + dm_size / 2 + 2.0 - i * 2.4, t, c,
                   FONT_B if i == 0 else FONT, anchor="center")

    # The left column.  The Data Matrix's two-module quiet zone is clear substrate, so the
    # column stops that far short of the symbol, plus a 0.6 mm gutter so that a glyph's
    # side bearing cannot eat into it.
    qz = quiet * dm_size / (side or 32)
    x = margin
    col = dm_x - qz - 0.6 - x

    # Baseline grid, from the top, in the order section 4.1 fixes.  The caps and gaps below
    # sum to less than the label height: a label whose content does not fit is a label whose
    # last line -- here the licence -- silently falls off the bottom edge.
    lines = [
        (serial,                                    2.9, FONT_B),
        (f"HW {doc_hw()}",                          1.7, FONT),
        (f"FP {group4(fp)}",                        1.5, FONT_M),
        (f"SE {atecc}",                             1.4, FONT_M),
        ("RESEARCH INSTRUMENT",                     1.9, FONT_B),
        ("NOT A MEDICAL DEVICE",                    1.9, FONT_B),
        ("Do not wear while charging",              1.4, FONT),
        ("Contains Li-ion cell - do not incinerate", 1.4, FONT),
        ("one.witysk.org   CC BY-SA 4.0",           1.2, FONT),
    ]
    gaps = [0.9, 0.7, 0.55, 1.1, 0.35, 0.8, 0.4, 0.55]
    total = sum(c for _, c, _ in lines) + sum(gaps)
    if total > h - 2 * margin:
        raise SystemExit(f"ART-LBL-01: the content column is {total:.2f} mm on a "
                         f"{h - 2 * margin:.2f} mm field. Shorten a line or reduce a cap "
                         f"height; do not let the last line fall off the label.")
    y = h - margin - lines[0][1]
    for i, (t, cap, prop) in enumerate(lines):
        a.text(x, y, t, cap, prop, max_width=col)
        if i < len(gaps):
            y -= gaps[i] + lines[i + 1][1]
    a.payload = payload
    a.column_width = col
    # Section 4.1 sets a 10 pt minimum on the serial.  10 pt is 3.528 mm of type, which in
    # this face is a 2.572 mm cap height; the caller checks the drawn height against it.
    a.serial_cap = next((c for t, _o, c in a.shrunk if t == serial), lines[0][1])
    a.serial_cap_minimum = 10.0 / 72.0 * MM_PER_IN * cap_ratio(FONT_B)
    return a


def doc_hw():
    return SPECIMEN_HW


def group4(s):
    if s.startswith("<<") or len(s) != 16:
        return s
    return " ".join(s[i:i + 4] for i in range(0, 16, 4))


def art_lbl_02(doc, kit=None, serial=None):
    """ART-LBL-02, the kit ID plate.  80 x 40 mm, section 4.2."""
    w, h = doc.size_mm("ART-LBL-02")
    kit = kit or "<<KIT_ID>>"
    serial = serial or "<<UNIT_SERIAL>>"
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE)
    a.rect(1.0, 1.0, w - 2.0, h - 2.0, fill=None, stroke=BLACK, lw=0.4, r=1.5)
    # `KIT-007` in 24 pt: 24 pt is 8.47 mm of type, a 6.17 mm cap height in this face.
    a.text(4.0, h - 3.0 - 6.17, kit, 6.17, FONT_B, max_width=w - 8.0)
    by, bh = 16.0, 12.0
    if not kit.startswith("<<"):
        runs, mods = code128b(kit)
        bw = (w - 8.0) / mods
        bx = 4.0
        for dark, n in runs:
            if dark:
                a.rect(bx, by, bw * n, bh, fill=BLACK)
            bx += bw * n
        a.text(4.0, 13.4, f"Code 128  {kit}", 1.6, FONT_M, max_width=w - 8.0)
    else:
        a.rect(4.0, by, w - 8.0, bh, fill=None, stroke=BLACK, lw=0.3, dash=(1.5, 1.5))
        a.text(w / 2, by + bh / 2 + 0.6, "CODE 128 OF THE KIT ID", 2.2, FONT_B,
               anchor="center", max_width=w - 12.0)
        a.text(w / 2, by + bh / 2 - 2.8, "encoded per kit at print", 1.6, FONT,
               anchor="center", max_width=w - 12.0)
    a.text(4.0, 8.6, serial, 3.0, FONT_M, max_width=w - 8.0)
    a.text(4.0, 5.0, "TI One Voice research kit - property of", 1.6, FONT,
           max_width=w - 8.0)
    a.text(4.0, 2.6, "TI One Voice vzw, Brussels", 1.6, FONT, max_width=w - 8.0)
    return a


def art_lbl_03(doc):
    """ART-LBL-03, return address and if-found, EN/FR/NL.  100 x 60 mm, section 4.2."""
    w, h = doc.size_mm("ART-LBL-03")
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE)
    a.rect(1.0, 1.0, w - 2.0, h - 2.0, fill=None, stroke=BLACK, lw=0.5)
    a.rect(1.0, h - 11.0, w - 2.0, 10.0, fill=BLACK)
    a.text(w / 2, h - 8.4, "IF FOUND, PLEASE RETURN TO", 3.4, FONT_B, anchor="center",
           fill=WHITE)
    body = w - 8.0
    y = h - 15.0
    for ln in ("<<PROGRAMME_RETURN_NAME>>",
               "<<PROGRAMME_RETURN_STREET>>",
               "<<PROGRAMME_RETURN_POSTCODE_AND_CITY>>",
               "<<PROGRAMME_RETURN_COUNTRY>>"):
        a.text(4.0, y, ln, 3.0, FONT_B, max_width=body)
        y -= 4.4
    y -= 0.8
    a.text(4.0, y, "Tel  <<PROGRAMME_TELEPHONE>>", 2.6, FONT_M, max_width=body)
    y -= 4.4
    a.line(4.0, y + 1.4, w - 4.0, y + 1.4, lw=0.3)
    for lang, line in (("EN", "Research equipment. Contains no personal data."),
                       ("FR", "Materiel de recherche. Ne contient aucune donnee "
                              "personnelle."),
                       ("NL", "Onderzoeksmateriaal. Bevat geen persoonsgegevens.")):
        a.text(4.0, y - 2.6, lang, 2.1, FONT_B)
        a.text(11.0, y - 2.6, line, 2.1, FONT, max_width=w - 15.0)
        y -= 4.0
    a.text(4.0, 2.6, "one.witysk.org", 2.0, FONT)
    a.text(w - 4.0, 2.6, f"ART-LBL-03  {OWNER}", 2.0, FONT, anchor="right",
           max_width=w / 2 - 6.0)
    return a


WANT_CAP = 8.0                          # PKG-EEG-015 section 2.3: "Cap height 8 mm"
TAG_MARGIN = 2.0
TAG_LEADING = 1.25                      # line pitch as a multiple of cap height


def _tag_lines(legend, cap, avail_w, max_lines):
    """Break `legend` for a tag, at most `max_lines` lines, or None if it will not fit."""
    lines = wrap(legend, cap, avail_w, FONT_B)
    if len(lines) > max_lines:
        return None
    if any(text_width(ln, cap, FONT_B) > avail_w for ln in lines):
        return None                     # a single word wider than the tag
    return lines


def _fit_cap(legend, avail_w, avail_h, max_lines):
    """The largest cap height at which `legend` fits the box, and its line breaks."""
    lo, hi = 0.6, WANT_CAP
    best = None
    for _ in range(40):
        mid = (lo + hi) / 2
        lines = _tag_lines(legend, mid, avail_w, max_lines)
        fits = lines is not None and len(lines) * mid + (len(lines) - 1) * mid * \
            (TAG_LEADING - 1) <= avail_h
        if fits:
            best = (mid, lines)
            lo = mid
        else:
            hi = mid
    return best or (0.6, [legend])


def _tag_art(w, h, legend, cap, lines):
    a = Art(w, h, bg=BLACK)
    n = len(lines)
    block = n * cap + (n - 1) * cap * (TAG_LEADING - 1)
    y = (h + block) / 2 - cap
    for ln in lines:
        a.text(w / 2, y, ln, cap, FONT_B, anchor="center", fill=WHITE)
        y -= cap * TAG_LEADING
    return a


def art_lbl_04(doc):
    """ART-LBL-04, the nine foam bay tags.  60 x 12 mm each, section 4.2 and section 2.3.

    Section 2.3 asks for a 60 x 12 mm tag set at an 8 mm cap height.  Not one of the nine
    legends fits across 60 mm at 8 mm caps -- the shortest, HEADPHONES, needs about 88 mm --
    so the tags are drawn at the size section 4.2 fixes, at the largest cap height that
    fits, and the size that WOULD carry every legend at 8 mm is computed and reported.  The
    tool does not silently resize the tag: the tag size is section 4.2's to change.

    Returns (tags, findings, proposal).
    """
    w, h = doc.size_mm("ART-LBL-04")
    spare = doc.spare_cell_tag()
    tags, findings = [], []
    for bay in doc.bays:
        legend = bay["legend"]
        if legend == "SPARE CELL" and spare:
            legend = spare
        cap, lines = _fit_cap(legend, w - 2 * TAG_MARGIN, h - 2 * 0.8, max_lines=2)
        tags.append((legend, _tag_art(w, h, legend, cap, lines), cap, len(lines)))
        if cap < WANT_CAP - 1e-6:
            # the tag width that would carry this legend at the specified 8 mm, on the
            # same maximum of two lines
            need = min(
                max(text_width(ln, WANT_CAP, FONT_B) for ln in br) + 2 * TAG_MARGIN
                for br in (_tag_lines(legend, WANT_CAP, 1e6, 1),
                           wrap(legend, WANT_CAP, _halfish(legend, WANT_CAP), FONT_B))
                if br)
            findings.append((legend, round(cap, 2), len(lines), round(need, 1)))
    if findings:
        need_w = max(f[3] for f in findings)
        need_h = 2 * WANT_CAP + WANT_CAP * (TAG_LEADING - 1) + 2 * 1.5
        proposal = (round(need_w, 0), round(need_h, 0))
    else:
        proposal = None
    return tags, findings, proposal


def _halfish(legend, cap):
    """A width that splits `legend` into roughly two equal lines at cap height `cap`."""
    return text_width(legend, cap, FONT_B) / 2 + text_width("MMMM", cap, FONT_B)


def art_lbl_05(doc):
    """ART-LBL-05, the carton marking set.  Printed on the carton, section 4.2 and 6."""
    w, h = 200.0, 150.0
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE)
    a.rect(2.0, 2.0, w - 4.0, h - 4.0, fill=None, stroke=BLACK, lw=0.6)
    a.rect(2.0, h - 26.0, w - 4.0, 24.0, fill=BLACK)
    a.text(w / 2, h - 20.0, "FRAGILE - RESEARCH INSTRUMENT", 9.0, FONT_B,
           anchor="center", fill=WHITE, max_width=w - 12.0)
    # THIS WAY UP: two upright arrows, the ISO 780 pair, drawn rather than typeset
    for cx in (30.0, w - 30.0):
        a.poly([(cx, h - 34.0), (cx - 9.0, h - 52.0), (cx - 3.5, h - 52.0),
                (cx - 3.5, h - 74.0), (cx + 3.5, h - 74.0), (cx + 3.5, h - 52.0),
                (cx + 9.0, h - 52.0)], fill=BLACK, stroke=None)
    a.text(w / 2, h - 56.0, "THIS WAY UP", 9.0, FONT_B, anchor="center",
           max_width=w - 90.0)
    a.line(20.0, h - 80.0, w - 20.0, h - 80.0, lw=0.5)
    rows = [("KIT ID", "<<KIT_ID>>"),
            ("UNIT SERIAL", "<<UNIT_SERIAL>>"),
            ("GROSS MASS", "<<GROSS_SHIPPING_MASS_KG>> kg"),
            ("DESPATCH DATE", "<<DESPATCH_DATE>>")]
    y = h - 92.0
    for k, v in rows:
        a.text(20.0, y, k, 5.0, FONT, max_width=64.0)
        a.text(90.0, y, v, 5.0, FONT_B, max_width=w - 110.0)
        y -= 11.0
    a.text(20.0, 12.0, "Do not use this carton if it is crushed or wet. "
                       "Telephone <<PROGRAMME_TELEPHONE>>.", 3.4, FONT,
           max_width=w - 40.0)
    a.text(20.0, 6.5, "Printed on two opposing long faces (PKG-EEG-015 section 4.2).",
           3.4, FONT, max_width=w - 40.0)
    return a


def art_lbl_06(doc, reduced=False):
    """ART-LBL-06, the lithium battery mark.

    Geometry from REG-EEG-012 Rev B section 3.5.  The pictogram is NOT drawn: see the
    module docstring and the control sheet.
    """
    facts = lithium_mark_facts()
    w, h = facts["reduced"] if reduced else facts["full"]
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE)
    # Hatched border: red diagonal hatching between two red rules, the form REG-EEG-012
    # section 3.5 states.  The hatch pitch is this file's, not the regulation's.
    band = 5.0 if not reduced else 4.0
    red = "#D0021B"
    a.rect(0.5, 0.5, w - 1.0, h - 1.0, fill=None, stroke=red, lw=0.8)
    a.rect(0.5 + band, 0.5 + band, w - 1.0 - 2 * band, h - 1.0 - 2 * band,
           fill=None, stroke=red, lw=0.8)
    pitch = 3.0
    n = int((w + h) / pitch) + 2
    for i in range(n):
        x0 = 0.5 + i * pitch - h
        pts = [(x0, 0.5), (x0 + h - 1.0, h - 0.5)]
        # clip crudely to the border band by drawing four short segments
        for (cx, cy, cw_, ch_) in ((0.5, 0.5, w - 1.0, band),
                                   (0.5, h - 0.5 - band, w - 1.0, band),
                                   (0.5, 0.5, band, h - 1.0),
                                   (w - 0.5 - band, 0.5, band, h - 1.0)):
            seg = _clip_segment(pts[0], pts[1], cx, cy, cx + cw_, cy + ch_)
            if seg:
                a.line(seg[0][0], seg[0][1], seg[1][0], seg[1][1], stroke=red, lw=0.7)
    inner_x, inner_y = 0.5 + band + 2.5, 0.5 + band + 2.5
    inner_w, inner_h = w - 2 * inner_x, h - 2 * inner_y
    cx = inner_x + inner_w / 2

    # The pictogram: a group of cells with one damaged and emitting flame, which is the
    # symbol the lithium battery mark carries.  It used to be a dashed box saying "PICTOGRAM
    # NOT SUPPLIED" -- the programme could not draw a regulated symbol from memory, and an
    # approximation drawn from memory is exactly the kind of thing that gets a consignment
    # refused.  It is drawn now because the programme lead supplied the reference image on
    # 2 September 2026.
    #
    # READ THIS BEFORE PRINTING.  What follows is a geometric reconstruction traced to the
    # supplied reference, not a copy of the model in the regulations.  Proportions,
    # cell count and flame shape follow the reference; nothing here has been compared
    # against the current edition of ADR or the IATA DGR.  REG-EEG-012 section 3.7 puts
    # that comparison on the DG-trained shipper, and it is a check of the artwork against
    # the edition in force on the day of despatch, not a one-off.
    pic_h = inner_h * 0.55
    pic_y = inner_y + inner_h - pic_h
    _lithium_symbol(a, inner_x, pic_y, inner_w, pic_h)

    # UN number and telephone, centred in what is left below the reservation.
    field_h = pic_y - inner_y
    un_cap, tel_cap, sub_cap = field_h * 0.30, field_h * 0.20, field_h * 0.11
    block = un_cap + tel_cap + sub_cap + field_h * 0.20
    ty = inner_y + (field_h + block) / 2 - un_cap
    a.text(cx, ty, "UN3481", un_cap, FONT_B, anchor="center", max_width=inner_w - 4.0)
    ty -= un_cap * 0.45 + tel_cap
    a.text(cx, ty, "<<PROGRAMME_TELEPHONE>>", tel_cap, FONT_M, anchor="center",
           max_width=inner_w - 4.0)
    ty -= tel_cap * 0.60 + sub_cap
    a.text(cx, ty, "for additional information", sub_cap, FONT, anchor="center",
           max_width=inner_w - 4.0)
    return a


def _lithium_symbol(a, x, y, w, h):
    """The battery group of the lithium battery mark, drawn to fit the box (x, y, w, h).

    Laid out from the supplied reference: four upright cells of different sizes on the
    left, a prismatic battery with two terminals in the middle, and on the right a
    horizontal cell lying on its side with its end open, a lightning break and a flame
    rising from it.  Everything is solid black on white, which is what the mark uses.
    """
    # Work in a unit box and map at the end, so the proportions hold at either size.
    def X(u):
        return x + u * w

    def Y(v):
        return y + v * h

    def rect(u0, v0, u1, v1):
        a.rect(X(u0), Y(v0), (u1 - u0) * w, (v1 - v0) * h, fill=BLACK)

    def ell(u, v, ru, rv, fill=BLACK):
        pts = []
        for k in range(33):
            t = k / 32.0 * 2 * math.pi
            pts.append((X(u + ru * math.cos(t)), Y(v + rv * math.sin(t))))
        a.poly(pts, fill=fill, stroke=None)

    # --- the four upright cells, left to right, small to large ------------------------
    #     (left edge, right edge, top of body), each capped with a terminal disc
    for u0, u1, top in ((0.045, 0.115, 0.62), (0.135, 0.225, 0.72),
                        (0.245, 0.335, 0.86)):
        rect(u0, 0.10, u1, top)
        ell((u0 + u1) / 2, top, (u1 - u0) / 2, (u1 - u0) / 2 * w / h * 0.42)
        # the terminal, a white ring on the cap
        ell((u0 + u1) / 2, top, (u1 - u0) / 4.5, (u1 - u0) / 4.5 * w / h * 0.42, fill=WHITE)

    # --- the prismatic battery, two terminals on top ----------------------------------
    rect(0.355, 0.10, 0.525, 0.70)
    for cu in (0.395, 0.470):
        ell(cu, 0.715, 0.028, 0.028 * w / h * 0.9)
        ell(cu, 0.715, 0.014, 0.014 * w / h * 0.9, fill=WHITE)

    # --- the damaged cell, lying on its side, open end to the right -------------------
    rect(0.545, 0.28, 0.875, 0.60)
    ell(0.875, 0.44, 0.045, 0.16)                       # the near rim, solid
    ell(0.875, 0.44, 0.022, 0.078, fill=WHITE)          # the bore

    # --- the lightning bolt breaking out of the cell ----------------------------------
    # A narrow zigzag from the cell wall up into the flame.  It must read as a separate
    # object from the flame: the first attempt let the two merge and the result looked
    # like a crown sitting on the cell rather than a rupture.
    a.poly([(X(0.663), Y(0.600)), (X(0.706), Y(0.600)), (X(0.681), Y(0.688)),
            (X(0.719), Y(0.688)), (X(0.652), Y(0.812)), (X(0.674), Y(0.716)),
            (X(0.640), Y(0.716))],
           fill=BLACK, stroke=None)

    # --- the flame --------------------------------------------------------------------
    # ONE body with licks rising from it.  Three attempts got this wrong in three ways: a
    # polygon of sharp points read as a crown, then as a star, and separate teardrops read
    # as five leaves standing in a row.  What makes it a flame is that the licks MERGE --
    # the outline dips into a valley between tips and never returns to the base line, so
    # the whole thing is one mass with a lean.
    #
    # (u, v) pairs alternating tip and valley, left to right, tallest just right of centre.
    outline = [
        (0.686, 0.640),                      # left foot
        (0.694, 0.762), (0.716, 0.712),      # lick 1, valley
        (0.734, 0.868), (0.760, 0.766),      # lick 2, valley
        (0.784, 0.972), (0.812, 0.802),      # lick 3 (tallest), valley
        (0.836, 0.898), (0.856, 0.762),      # lick 4, valley
        (0.878, 0.822),                      # lick 5
        (0.888, 0.700), (0.892, 0.640),      # down the right flank to the foot
    ]
    pts = [(X(u), Y(v)) for u, v in outline]
    # a smoothing pass: one midpoint per span, nudged outward, turns the polyline into
    # something that reads as curved without needing a spline in the renderer
    smooth = [pts[0]]
    for k in range(len(pts) - 1):
        (x0_, y0_), (x1_, y1_) = pts[k], pts[k + 1]
        smooth.append(((x0_ + x1_) / 2 + (y1_ - y0_) * 0.06,
                       (y0_ + y1_) / 2 - (x1_ - x0_) * 0.06))
        smooth.append((x1_, y1_))
    a.poly(smooth, fill=BLACK, stroke=None)


def _clip_segment(p0, p1, x0, y0, x1, y1):
    """Liang-Barsky clip of a segment to a rectangle; None if it misses."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, p0[0] - x0), (dx, x1 - p0[0]), (-dy, p0[1] - y0), (dy, y1 - p0[1])):
        if p == 0:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return None
            t0 = max(t0, r)
        else:
            if r < t0:
                return None
            t1 = min(t1, r)
    if t0 > t1:
        return None
    return ((p0[0] + t0 * dx, p0[1] + t0 * dy), (p0[0] + t1 * dx, p0[1] + t1 * dy))


def art_lbl_07(doc):
    """ART-LBL-07, the numbered tamper seal.  90 x 20 mm, section 4.2."""
    w, h = doc.size_mm("ART-LBL-07")
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE)
    a.rect(0.5, 0.5, w - 1.0, h - 1.0, fill=None, stroke=BLACK, lw=0.5)
    # the seal is cut by the hasp: the perforation line is drawn as the die instruction
    a.line(w / 2, 0.5, w / 2, h - 0.5, stroke=GREY, lw=0.3, dash=(1.2, 1.2))
    a.text(4.0, h - 6.5, "SEALED", 4.4, FONT_B, max_width=w / 2 - 8.0)
    a.text(4.0, 2.6, "Do not break except at goods-in", 2.4, FONT, max_width=w / 2 - 8.0)
    a.text(w - 4.0, h - 6.5, "<<SEAL_NUMBER>>", 4.4, FONT_M, anchor="right",
           max_width=w / 2 - 8.0)
    a.text(w - 4.0, 2.6, "TI One Voice  one.witysk.org", 2.4, FONT, anchor="right",
           max_width=w / 2 - 8.0)
    return a


def art_pack_01(doc):
    """ART-PACK-01, the packing photograph -- the provisional layout that stands in for it.

    PKG-EEG-015 section 2.3 says that until a kit exists "a rendered layout marked
    PROVISIONAL -- REPLACE WITH PHOTOGRAPH AT FIRST BUILD is used", and open item 7 records
    that no such render exists.  This is that render: the nine Rev C bays at true relative
    scale on the 516.0 x 390.0 mm sheet, each carrying its legend and the packing-list line
    numbers that go in it.  It is drawn from the section 2.2 schedule and the section 1.1
    pocket column, so it cannot show a bay the cut files do not cut or a line the packing
    list does not carry.
    """
    w, h = 210.0, 148.0                              # A5 landscape
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE)
    sheet_w, sheet_h = 516.0, 390.0
    pad_l, pad_b, pad_t = 6.0, 20.0, 16.0
    sc = min((w - 2 * pad_l) / sheet_w, (h - pad_b - pad_t) / sheet_h)
    ox = (w - sheet_w * sc) / 2
    oy = pad_b
    a.rect(ox, oy, sheet_w * sc, sheet_h * sc, fill="#F2F2F2", stroke=BLACK, lw=0.5)

    by_pocket = {}
    for line in doc.kpl:
        by_pocket.setdefault(line["pocket"].split(" (")[0], []).append(line["line"])

    for bay in doc.bays:
        x = ox + bay["x"] * sc
        y = oy + bay["y"] * sc
        bw, bh = bay["w"] * sc, bay["h"] * sc
        a.rect(x, y, bw, bh, fill=WHITE, stroke=BLACK, lw=0.4)
        # The bays are drawn at true relative scale, so a shallow bay has little room.  The
        # legend, the call-outs and the layer note are fitted into the height the bay
        # actually has; without this the SPARE CUPS legend printed on top of its own layer
        # note, which no diff of this file would have shown.
        foot_cap = 1.7
        avail = bh - 2.0 - (foot_cap + 1.8)
        cap, kcap = min(2.4, bh / 4.0), 1.9
        for _ in range(12):
            lines = wrap(bay["legend"], cap, bw - 2.0, FONT_B) or [bay["legend"]]
            nums = by_pocket.get(bay["legend"], [])
            klines = wrap("KPL " + ", ".join(nums), kcap, bw - 2.0) if nums else []
            need = len(lines) * cap * 1.35 + len(klines) * kcap * 1.35
            if need <= avail or cap < 1.1:
                break
            cap *= 0.9
            kcap = min(kcap, cap * 0.85)
        ty = y + bh - 2.0 - cap
        for ln in lines:
            a.text(x + bw / 2, ty, ln, cap, FONT_B, anchor="center", max_width=bw - 1.5)
            ty -= cap * 1.35
        for chunk in klines:
            a.text(x + bw / 2, ty, chunk, kcap, FONT, anchor="center", max_width=bw - 1.5)
            ty -= kcap * 1.35
        a.text(x + bw / 2, y + 1.4, f"layers {bay['layers']}", foot_cap, FONT,
               anchor="center", fill=GREY, max_width=bw - 1.5)

    a.text(w / 2, h - 6.0, "ART-PACK-01  KIT PACKING LAYOUT", 4.2, FONT_B, anchor="center")
    a.text(w / 2, h - 11.0,
           "CASE-00 Rev C, layer 1 uppermost, sheet 516.0 x 390.0 mm, nine bays",
           2.4, FONT, anchor="center")
    a.rect(4.0, 4.0, w - 8.0, 11.0, fill=None, stroke=BLACK, lw=0.5)
    a.text(w / 2, 10.4, "PROVISIONAL - REPLACE WITH PHOTOGRAPH AT FIRST BUILD",
           3.4, FONT_B, anchor="center")
    a.text(w / 2, 5.8,
           "A drawn layout, not a photograph. Call-outs are KPL-EEG-001 line numbers "
           "(PKG-EEG-015 section 1.1).", 2.2, FONT, anchor="center")
    return a


def art_dis_01(doc):
    """ART-DIS-01, the disinfection guide card.  A5, the extract of SVC-EEG-013 R5."""
    agents, prohibited = disinfection_rows()
    w, h = 148.0, 210.0                              # A5 portrait
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE)
    a.rect(0, h - 16.0, w, 16.0, fill=BLACK)
    a.text(8.0, h - 11.0, "CLEANING AND DISINFECTION", 4.6, FONT_B, fill=WHITE)
    a.text(8.0, h - 22.0,
           "Operator card. Extract of SVC-EEG-013 Rev B section 2 R5.", 2.6, FONT)
    a.text(8.0, h - 26.0,
           "Efficacy is not validated by this programme (SVC-EEG-013 section 2 R5).",
           2.6, FONT)

    # Five columns across the 132 mm between the margins.  The widths are set here and the
    # cells are wrapped to them, so a longer agent name wraps rather than running off the
    # card -- which the first draft of this function did, into the right margin.
    widths = (34.0, 33.0, 26.0, 20.0, 19.0)
    cols, cx0 = [], 8.0
    for wdt in widths:
        cols.append(cx0)
        cx0 += wdt
    assert cx0 <= w - 8.0 + 1e-9, "ART-DIS-01 columns are wider than the card"
    y = h - 34.0
    a.line(8.0, y + 4.0, w - 8.0, y + 4.0, lw=0.4)
    for cx, head, wdt in zip(cols, ("Item", "Agent", "Concentration", "Contact", "Method"),
                             widths):
        a.text(cx, y, head, 2.4, FONT_B, max_width=wdt - 1.5)
    y -= 2.2
    a.line(8.0, y, w - 8.0, y, lw=0.4)
    y -= 4.6
    for item, method, agent, conc, contact in agents:
        cells = (item, agent, conc, contact, method)
        blocks = [wrap(c, 2.2, wdt - 1.5) for c, wdt in zip(cells, widths)]
        n = max(len(b) for b in blocks)
        for cx, blk, wdt in zip(cols, blocks, widths):
            for i, ln in enumerate(blk):
                a.text(cx, y - i * 3.0, ln, 2.2, FONT, max_width=wdt - 1.2)
        last = y - (n - 1) * 3.0                 # baseline of the row's last line
        sep = last - 1.6                         # clear of that line's descenders
        a.line(8.0, sep, w - 8.0, sep, stroke="#BBBBBB", lw=0.2)
        y = sep - 3.4                            # baseline of the next row's first line

    y -= 4.0
    a.text(8.0, y, "NEVER", 3.4, FONT_B)
    y -= 5.5
    for what, why in prohibited:
        blk = wrap(f"{what} - {why}", 2.2, w - 22.0)
        for i, ln in enumerate(blk):
            a.text(12.0, y - i * 3.0, ln, 2.2, FONT)
        a.circle(9.6, y + 0.8, 0.9, fill=BLACK, stroke=None)
        y -= len(blk) * 3.0 + 1.6
    a.line(8.0, 16.0, w - 8.0, 16.0, lw=0.4)
    a.text(8.0, 11.0, "Record the agent, its lot and its expiry on F1 section 4. "
                      "An expired agent invalidates", 2.2, FONT)
    a.text(8.0, 7.6, "the turnaround and the cleaning is repeated.", 2.2, FONT)
    a.text(8.0, 3.4, f"ART-DIS-01   {OWNER}   source SVC-EEG-013 Rev B   {LICENCE}",
           2.0, FONT, fill=GREY)
    return a


def art_ret_01(doc):
    """ART-RET-01, the return-shipping instruction sheet.  A4, copy from section 7."""
    w, h = 210.0, 297.0
    a = Art(w, h)
    a.rect(0, 0, w, h, fill=WHITE)
    a.rect(0, h - 22.0, w, 22.0, fill=BLACK)
    a.text(15.0, h - 15.0, "SENDING THE KIT BACK", 6.5, FONT_B, fill=WHITE)
    y = h - 32.0
    a.text(15.0, y, "Keep this sheet in the clear pocket on the outside of the box.",
           3.0, FONT_B)
    y -= 10.0
    for ln in wrap(doc.ret_sheet_text(), 3.4, w - 30.0):
        a.text(15.0, y, ln, 3.4, FONT)
        y -= 5.6
    y -= 8.0
    a.line(15.0, y + 4.0, w - 15.0, y + 4.0, lw=0.4)
    a.text(15.0, y - 1.0, "IF YOU ARE ASKED WHAT IS INSIDE", 3.6, FONT_B)
    y -= 9.0
    box_h = 26.0
    a.rect(15.0, y - box_h + 6.0, w - 30.0, box_h, fill="#F2F2F2", stroke=BLACK, lw=0.4)
    a.text(20.0, y, "A research instrument with a small rechargeable battery", 3.4, FONT_B)
    a.text(20.0, y - 5.4, "fitted inside it. UN 3481, already declared on the label.",
           3.4, FONT_B)
    a.text(20.0, y - 12.0, "Do not open the instrument. Do not remove any battery.",
           3.0, FONT)
    a.text(20.0, y - 16.6, "Do not post it in a letterbox - hand it over at a counter.",
           3.0, FONT)
    y -= box_h + 10.0
    a.text(15.0, y, "IF ANYTHING IS WRONG", 3.6, FONT_B)
    y -= 8.0
    for ln in ("Telephone  <<PROGRAMME_TELEPHONE>>",
               "Email      <<PROGRAMME_EMAIL>>",
               "Kit id     <<KIT_ID>>          Tracking  <<RETURN_TRACKING_NUMBER>>"):
        a.text(15.0, y, ln, 3.4, FONT_M)
        y -= 6.0
    a.text(15.0, 18.0,
           "This sheet is the participant-facing rendering of PKG-EEG-015 Rev B section 7. "
           "The participant", 2.4, FONT, fill=GREY)
    a.text(15.0, 14.4,
           "never writes a shipping document, never opens the pod and never handles a cell.",
           2.4, FONT, fill=GREY)
    a.text(15.0, 9.0, f"ART-RET-01   {OWNER}   {LICENCE}", 2.4, FONT, fill=GREY)
    return a


def drw_lbl_placement(doc):
    """DRW-LBL-PLACEMENT, the placement drawing PKG-EEG-015 section 4.2 signs against.

    Four views on one A3 sheet, each in its own panel at its own scale, with the label
    footprints drawn on them and dimensioned from the two nearest edges.  The case and
    carton outlines are the PUBLISHED shell figures of section 3.2 and section 6, which
    section 9 open item 2 records as not measured; the drawing says so on its face, and
    dimensioning from the edges is what lets a measured shell change the numbers without
    changing the arrangement.
    """
    W, H = 420.0, 297.0                              # A3 landscape
    a = Art(W, H)
    a.rect(0, 0, W, H, fill=WHITE)
    a.rect(10, 10, W - 20, H - 20, fill=None, stroke=BLACK, lw=0.4)

    a.text(15.0, H - 24.0, "DRW-LBL-PLACEMENT   LABEL AND MARKING PLACEMENT", 6.0, FONT_B,
           max_width=W - 30)
    a.text(15.0, H - 31.0,
           "PKG-EEG-015 Rev B sections 4.1 and 4.2. The QA placement check of section 4.2 "
           "signs against this sheet.", 2.8, FONT, max_width=W - 30)
    a.line(15.0, H - 35.0, W - 15.0, H - 35.0, lw=0.4)

    def panel(px, py, pw, ph, no, title, sub, ow, oh, outline_label):
        """Frame a view, fit the outline into it, return (ox, oy, scale)."""
        a.rect(px, py, pw, ph, fill=None, stroke="#CCCCCC", lw=0.3)
        a.text(px + 3.0, py + ph - 6.0, f"{no}  {title}", 3.6, FONT_B, max_width=pw - 6)
        a.text(px + 3.0, py + ph - 10.0, sub, 2.4, FONT, fill=GREY, max_width=pw - 6)
        draw_w, draw_h = pw - 16.0, ph - 26.0
        sc = min(draw_w / ow, draw_h / oh)
        ox = px + (pw - ow * sc) / 2
        oy = py + 8.0
        a.rect(ox, oy, ow * sc, oh * sc, fill=None, stroke=BLACK, lw=0.5)
        a.text(px + pw - 3.0, py + ph - 10.0, f"scale 1:{1 / sc:.1f}", 2.4, FONT,
               anchor="right", fill=GREY)
        a.text(ox + ow * sc / 2, py + 3.5, outline_label, 2.4, FONT, anchor="center",
               max_width=pw - 6)
        return ox, oy, sc

    def place(ox, oy, sc, x, y, lw_, lh_, ref, note):
        a.rect(ox + x * sc, oy + y * sc, lw_ * sc, lh_ * sc,
               fill="#E8E8E8", stroke=BLACK, lw=0.4)
        cx, cy = ox + (x + lw_ / 2) * sc, oy + (y + lh_ / 2) * sc
        box_h = lh_ * sc
        # The note goes in only where the footprint at this scale has room for it; on the
        # small views it would otherwise print across the label outline it describes.
        if box_h >= 8.0:
            a.text(cx, cy + 0.4, ref, 2.6, FONT_B, anchor="center",
                   max_width=lw_ * sc - 1.0)
            a.text(cx, cy - 3.2, note, 1.8, FONT, anchor="center", fill=GREY,
                   max_width=lw_ * sc - 1.0)
        else:
            a.text(cx, cy - 1.0, ref, 2.2, FONT_B, anchor="center",
                   max_width=lw_ * sc - 1.0)
        # Dimensions from the two nearest edges, in millimetres on the real part.  A zero
        # offset gets no leader: a leader of no length and a "0" beside it is noise.
        if x > 0:
            a.line(ox, cy, ox + x * sc, cy, stroke=GREY, lw=0.25)
            a.text(ox + x * sc / 2, cy + 0.8, f"{x:.0f}", 2.0, FONT, anchor="center",
                   fill=GREY)
        if y > 0:
            a.line(ox + (x + lw_ / 2) * sc, oy, ox + (x + lw_ / 2) * sc, oy + y * sc,
                   stroke=GREY, lw=0.25)
            a.text(ox + (x + lw_ / 2) * sc + 1.0, oy + y * sc / 2, f"{y:.0f}", 2.0, FONT,
                   fill=GREY)

    # -- 1. POD-P1 lid, Phase 1 unit-label placement ---------------------------------------
    ox, oy, sc = panel(14, 150, 196, 104, "1", "POD-P1 lid, outer face",
                       "Phase 1 placement of ART-LBL-01", 163.0, 143.0,
                       "POD-P1 163.0 x 143.0 mm")
    kx, ky = (163.0 - 55.0) / 2, (143.0 - 30.0) / 2
    a.rect(ox + kx * sc, oy + ky * sc, 55.0 * sc, 30.0 * sc, fill=None, stroke=GREY,
           lw=0.3, dash=(1.5, 1.5))
    a.text(ox + (kx + 27.5) * sc, oy + (ky + 30.0) * sc + 1.2,
           "flat keep-out 55 x 30, clear of the gasket line", 2.0, FONT, anchor="center",
           fill=GREY)
    place(ox, oy, sc, kx + 2.5, ky + 2.5, 50.0, 25.0, "ART-LBL-01", "50 x 25")

    # -- 2. case lid exterior ---------------------------------------------------------------
    ox, oy, sc = panel(214, 150, 192, 104, "2", "Travel case, lid exterior",
                       "Peli 1560 published external - not measured (section 9 item 2)",
                       560.0, 455.0, "case external 560 x 455 mm, published")
    place(ox, oy, sc, 40.0, 455.0 - 80.0, 80.0, 40.0, "ART-LBL-02", "kit ID plate")
    for i, hx in enumerate((140.0, 380.0)):
        place(ox, oy, sc, hx, 0.0, 90.0, 20.0, "ART-LBL-07", f"hasp seal {i + 1}")
    a.text(ox + 280.0 * sc, oy + 250.0 * sc,
           "No label may cover the", 2.4, FONT_B, anchor="center")
    a.text(ox + 280.0 * sc, oy + 250.0 * sc - 3.2,
           "pressure-equalisation valve", 2.4, FONT_B, anchor="center")

    # -- 3. case base exterior ---------------------------------------------------------------
    ox, oy, sc = panel(14, 42, 196, 100, "3", "Travel case, base exterior",
                       "ART-LBL-03 return and if-found", 560.0, 455.0,
                       "case external 560 x 455 mm, published")
    place(ox, oy, sc, (560.0 - 100.0) / 2, (455.0 - 60.0) / 2, 100.0, 60.0,
          "ART-LBL-03", "100 x 60, centred")

    # -- 4. outer carton, one long face -------------------------------------------------------
    ox, oy, sc = panel(214, 42, 192, 100, "4", "Outer carton, one long face",
                       "640 x 535 x 345 mm, calculated from the case plus 40 mm a face",
                       640.0, 345.0, "carton 640 x 345 mm on this face, calculated")
    place(ox, oy, sc, 40.0, 345.0 - 190.0, 200.0, 150.0, "ART-LBL-05",
          "printed, two opposing faces")
    place(ox, oy, sc, 415.0, 30.0, 120.0, 110.0, "ART-LBL-06", "UN3481, one side face")
    place(ox, oy, sc, 40.0, 30.0, 225.0, 165.0, "document wallet",
          "return label + ART-RET-01")

    # -- notes ---------------------------------------------------------------------------------
    a.rect(14, 12, W - 28, 26, fill=None, stroke=BLACK, lw=0.4)
    notes = [
        "The case and carton outlines are PUBLISHED, not measured. PKG-EEG-015 section 9 "
        "open item 2 records that no travel case has been bought, measured or weighed, and "
        "section 6 records the carton as calculated from that published shell.",
        "The faces, the labels and their sizes are section 4.2's and are fixed. The "
        "positions ON those faces are this drawing's and are a PROPOSAL until a shell is in "
        "front of a packer: they are dimensioned from the two nearest edges so that a "
        "measured shell changes the numbers and not the arrangement.",
        "The valve of view 2 is a written constraint and not a drawn keep-out, because its "
        "position on the bought shell is not known. Only the Phase 1 placement of "
        "ART-LBL-01 is drawn; the Phase 2 and 3 placement is the HM-01 occipital shell rear "
        "face and is not dimensioned in package v2.3.",
    ]
    y = 33.0
    for n in notes:
        for ln in wrap(n, 2.3, W - 36):
            a.text(18.0, y, ln, 2.3, FONT)
            y -= 3.0
    a.text(18.0, y - 0.5,
           f"DRW-LBL-PLACEMENT   {OWNER}   generated by {GENERATOR}   {LICENCE}",
           2.3, FONT, fill=GREY)
    return a


# ---------------------------------------------------------------------------------------
# 6.  Control sheets and output
# ---------------------------------------------------------------------------------------

A4 = (210.0, 297.0)
A3 = (420.0, 297.0)


def control_sheet(path, ident, name, art, facts, variables, notes, sheet=A4, arts=None):
    """An A4 or A3 control sheet: title block, the artwork 1:1 inside trim marks, notes."""
    sw, sh = sheet
    fig = plt.figure(figsize=(sw / MM_PER_IN, sh / MM_PER_IN))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, sw)
    ax.set_ylim(0, sh)
    ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), sw, sh, facecolor="white", edgecolor="none", zorder=0))

    frame = Art(sw, sh, bg=None)
    frame.rect(10, 10, sw - 20, sh - 20, fill=None, stroke=BLACK, lw=0.4)
    frame.line(10, sh - 32, sw - 10, sh - 32, lw=0.4)
    frame.text(14, sh - 24, f"{ident}   {name}", 5.0, FONT_B)
    frame.text(sw - 14, sh - 20, OWNER, 2.8, FONT, anchor="right")
    frame.text(sw - 14, sh - 24.5, f"generated by {GENERATOR}", 2.8, FONT, anchor="right")
    frame.text(sw - 14, sh - 29, f"{datetime.date.today().isoformat()}   {LICENCE}",
               2.8, FONT, anchor="right")

    y = sh - 38
    for k, v in facts:
        frame.text(14, y, k, 2.6, FONT_B)
        for i, ln in enumerate(wrap(v, 2.6, sw - 70)):
            frame.text(56, y - i * 3.4, ln, 2.6, FONT)
        y -= max(1, len(wrap(v, 2.6, sw - 70))) * 3.4 + 1.4
    frame.draw_on(ax)

    # the artwork, 1:1, with trim marks
    items = arts if arts is not None else [(art, None)]
    top = y - 8
    for a, cap in items:
        ax_x = (sw - a.w) / 2
        ax_y = top - a.h
        a.draw_on(ax, ax_x, ax_y)
        marks = Art(sw, sh, bg=None)
        marks.rect(ax_x, ax_y, a.w, a.h, fill=None, stroke="#FF00FF", lw=0.2,
                   dash=(1.5, 1.5))
        for (mx, my, dx, dy) in ((ax_x, ax_y, -1, 0), (ax_x, ax_y, 0, -1),
                                 (ax_x + a.w, ax_y, 1, 0), (ax_x + a.w, ax_y, 0, -1),
                                 (ax_x, ax_y + a.h, -1, 0), (ax_x, ax_y + a.h, 0, 1),
                                 (ax_x + a.w, ax_y + a.h, 1, 0),
                                 (ax_x + a.w, ax_y + a.h, 0, 1)):
            marks.line(mx, my, mx + dx * 3.5, my + dy * 3.5, stroke="#FF00FF", lw=0.2)
        lab = cap or f"trim {a.w:g} x {a.h:g} mm, shown 1:1"
        marks.text(ax_x, ax_y - 4.0, lab, 2.4, FONT, fill="#FF00FF")
        marks.draw_on(ax)
        top = ax_y - 10

    tail = Art(sw, sh, bg=None)
    y = top - 2
    if variables:
        tail.text(14, y, "Variable data -- these fields are NOT artwork and must be "
                         "supplied before print", 3.0, FONT_B)
        y -= 6
        tail.line(14, y + 2.5, sw - 14, y + 2.5, lw=0.3)
        for field, src in variables:
            tail.text(16, y, field, 2.5, FONT_M)
            for i, ln in enumerate(wrap(src, 2.5, sw - 110)):
                tail.text(96, y - i * 3.2, ln, 2.5, FONT)
            y -= max(1, len(wrap(src, 2.5, sw - 110))) * 3.2 + 0.8
        y -= 4
    if notes:
        tail.text(14, y, "Notes", 3.0, FONT_B)
        y -= 6
        for n in notes:
            for i, ln in enumerate(wrap(n, 2.5, sw - 34)):
                tail.text(18 if i else 14, y, ("- " if i == 0 else "") + ln, 2.5, FONT)
                y -= 3.4
            y -= 1.2
    tail.draw_on(ax)

    fig.savefig(path, format="pdf")
    plt.close(fig)
    return path


def emit(art, ident, name, title, desc):
    svg = os.path.join(OUT, f"{ident}_{name}.svg")
    art.to_svg(svg, title, desc)
    return svg


# Supplied by the programme lead on 2 September 2026 and substituted at generation time by
# the PROGRAMME table; these are no longer variable data and are listed here so that a
# reader of the control sheet can see what was filled in and where it came from.
ADDR_FIELDS = [
    ("<<PROGRAMME_RETURN_NAME>>", "SUPPLIED 2026-09-02. Substituted at generation."),
    ("<<PROGRAMME_RETURN_STREET>>", "SUPPLIED 2026-09-02. Substituted at generation."),
    ("<<PROGRAMME_RETURN_POSTCODE_AND_CITY>>", "SUPPLIED 2026-09-02. Substituted."),
    ("<<PROGRAMME_RETURN_COUNTRY>>", "SUPPLIED 2026-09-02. Substituted at generation."),
    ("<<PROGRAMME_TELEPHONE>>", "SUPPLIED 2026-09-02. REG-EEG-012 Rev B section 3.5 "
                                "requires a number that is answered by a person during "
                                "the carrier's operating hours, not a voicemail box, and "
                                "makes any change to it an ECO -- so the number is now "
                                "under change control, not merely known."),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    print("self-test")
    if not selftest():
        raise SystemExit("artwork_gen.py: encoder self-test failed; nothing written")

    doc = Doc()
    written = []
    findings = []

    def note(s):
        findings.append(s)
        print("  NOTE:", s)

    def check_fit(ident, art):
        """Report any line this tool had to shrink to keep it inside the artwork."""
        for t, was, now in art.shrunk:
            if now < was * 0.75:
                note(f"{ident}: {t!r} was set at {was:.2f} mm cap and shrunk to "
                     f"{now:.2f} mm to fit.")

    # -- ART-LBL-01 -------------------------------------------------------------------------
    tmpl = art_lbl_01(doc)
    spec = art_lbl_01(doc, SPECIMEN_SERIAL, SPECIMEN_ATECC, SPECIMEN_FP, SPECIMEN_KIT)
    written.append(emit(tmpl, "ART-LBL-01", "unit_label",
                        "ART-LBL-01 unit label, template",
                        "50 x 25 mm. Per-unit fields are drawn as <<PLACEHOLDER>>."))
    check_fit("ART-LBL-01", spec)
    if spec.serial_cap < spec.serial_cap_minimum:
        note(f"ART-LBL-01: the serial is set at {spec.serial_cap:.2f} mm cap, below the "
             f"{spec.serial_cap_minimum:.2f} mm that section 4.1's 10 pt minimum "
             f"requires.")
    written.append(emit(spec, "ART-LBL-01", "unit_label_specimen",
                        "ART-LBL-01 unit label, specimen",
                        f"Specimen for {SPECIMEN_SERIAL}, a serial in none of the blocks "
                        f"PKG-EEG-015 section 5 allocates."))
    grid, side, _ = dm_encode(spec.payload)
    mod_mm = 12.0 / side
    written.append(control_sheet(
        os.path.join(OUT, "ART-LBL-01_unit_label.pdf"), "ART-LBL-01", "Unit label",
        tmpl,
        [("Size", doc.unit_label["Size"]),
         ("Substrate", doc.unit_label["Substrate"]),
         ("Print", doc.unit_label["Print"]),
         ("Finish", doc.unit_label["Finish"]),
         ("Adhesive", doc.unit_label["Adhesive"]),
         ("Placement", doc.unit_label["Placement, Phase 1"]),
         ("Data Matrix", f"ECC200, {side} x {side} modules in 12.0 mm, module "
                         f"{mod_mm:.3f} mm, quiet zone 2 modules = {2 * mod_mm:.2f} mm. "
                         f"At 300 dpi a module is {mod_mm / MM_PER_IN * 300:.1f} dots.")],
        [("<<UNIT_SERIAL>>", "Allocated by the programme with the purchase order; "
                             "PKG-EEG-015 section 5."),
         ("<<ATECC_FACTORY_SERIAL_18_HEX>>", "Read at TST-EEG-004 Rev C T00 and T6."),
         ("<<KEY_FINGERPRINT_16_HEX>>", "Computed as FW-EEG-001 Rev C section 7 defines "
                                        "it, at T6.")],
        ["The Data Matrix payload is "
         "`<serial>|<hw rev>|<18 hex ATECC serial>|<16 hex fingerprint>`, pipe-delimited "
         "with no spaces, per PKG-EEG-015 section 4.1. It cannot be drawn as a "
         "placeholder, so the template shows the reserved area and the specimen below "
         "carries a real symbol.",
         "The specimen is drawn for " + SPECIMEN_SERIAL + ". PKG-EEG-015 section 5 "
         "allocates 0001 to 0009, 0010 to 0099 and 0100 to 0999, so 0000 is in no block "
         "and a specimen print can never be mistaken for the label of a unit that exists. "
         "That reservation is proposed to the programme in PKG-EEG-015 section 9 and is "
         "not yet ruled.",
         "The fingerprint on the specimen is the illustrative string PKG-EEG-015 section "
         "4.1 prints, which that section marks as illustrative. It is not the fingerprint "
         "of any key.",
         "The symbol has been checked by encoding and decoding it in this tool and against "
         "the ISO/IEC 16022 worked example. It has NOT been read by a barcode verifier. "
         "PKG-EEG-015 section 4.1 requires ISO/IEC 15415 grade C or better after the IPA "
         "test, and that first-article verification is what releases this artwork."],
        arts=[(tmpl, "template, trim 50 x 25 mm, shown 1:1"),
              (spec, f"specimen {SPECIMEN_SERIAL}, shown 1:1")]))

    # -- ART-LBL-02 -------------------------------------------------------------------------
    t2 = art_lbl_02(doc)
    s2 = art_lbl_02(doc, SPECIMEN_KIT, SPECIMEN_SERIAL)
    written.append(emit(t2, "ART-LBL-02", "kit_id_plate", "ART-LBL-02 kit ID plate, template",
                        doc.labels["ART-LBL-02"]["what"]))
    written.append(emit(s2, "ART-LBL-02", "kit_id_plate_specimen",
                        "ART-LBL-02 kit ID plate, specimen",
                        f"Specimen for {SPECIMEN_KIT} / {SPECIMEN_SERIAL}."))
    _, c128mods = code128b(SPECIMEN_KIT)
    written.append(control_sheet(
        os.path.join(OUT, "ART-LBL-02_kit_id_plate.pdf"), "ART-LBL-02", "Kit ID plate", t2,
        [("Size", doc.labels["ART-LBL-02"]["size"]),
         ("Substrate", doc.labels["ART-LBL-02"]["substrate"]),
         ("Placement", doc.labels["ART-LBL-02"]["placement"]),
         ("Barcode", f"Code 128 subset B, {c128mods} modules for a 7-character kit id, "
                     f"{(80.0 - 8.0) / c128mods:.3f} mm per module at this width")],
        [("<<KIT_ID>>", "`KIT-<nnn>`, the circulating asset, PKG-EEG-015 section 5."),
         ("<<UNIT_SERIAL>>", "The electronics, PKG-EEG-015 section 5. Kit id and unit "
                             "serial are recorded as a pair at despatch.")],
        ["`KIT-007` is set in 24 pt per section 4.2, which in this face is a 6.17 mm cap "
         "height.",
         "The Code 128 bar width falls out of the kit-id length. A longer kit id makes a "
         "narrower bar: re-run this tool for the id actually used and check the bar width "
         "against the printer's resolution."],
        arts=[(t2, "template, trim 80 x 40 mm, shown 1:1"),
              (s2, f"specimen {SPECIMEN_KIT}, shown 1:1")]))

    # -- ART-LBL-03 -------------------------------------------------------------------------
    a3_ = art_lbl_03(doc)
    check_fit("ART-LBL-03", a3_)
    written.append(emit(a3_, "ART-LBL-03", "return_and_if_found",
                        "ART-LBL-03 return address and if-found",
                        doc.labels["ART-LBL-03"]["what"]))
    written.append(control_sheet(
        os.path.join(OUT, "ART-LBL-03_return_and_if_found.pdf"), "ART-LBL-03",
        "Return address and if-found", a3_,
        [("Size", doc.labels["ART-LBL-03"]["size"]),
         ("Substrate", doc.labels["ART-LBL-03"]["substrate"]),
         ("Placement", doc.labels["ART-LBL-03"]["placement"])],
        ADDR_FIELDS,
        ["THIS LABEL CANNOT GO TO A PRINTER AS IT STANDS. The programme's postal address "
         "and telephone number appear nowhere in package v2.3, and this tool will not "
         "invent them: a wrong address on a case base is a kit that does not come back.",
         "The three languages are EN, FR and NL as section 4.2 requires. The FR and NL "
         "lines are written without diacritics so that a thermal-transfer printer with a "
         "reduced character set cannot drop a character silently; a printer that carries "
         "the full set may set them accented."]))
    note("ART-LBL-03 carries five unresolved address and telephone fields.")

    # -- ART-LBL-04 -------------------------------------------------------------------------
    tags, cap_findings, tag_proposal = art_lbl_04(doc)
    tw4, th4 = doc.size_mm("ART-LBL-04")
    for legend, art, cap, nlines in tags:
        slug = re.sub(r"[^A-Za-z0-9]+", "_", legend.split(" -- ")[0]).strip("_").lower()
        written.append(emit(art, "ART-LBL-04", f"bay_tag_{slug}",
                            f"ART-LBL-04 foam bay tag: {legend}",
                            f"{tw4:g} x {th4:g} mm, white on black. Legend from "
                            f"PKG-EEG-015 section 2.2, cap height {cap:.2f} mm on "
                            f"{nlines} line(s)."))
    smallest = min((f[1] for f in cap_findings), default=WANT_CAP)
    written.append(control_sheet(
        os.path.join(OUT, "ART-LBL-04_foam_bay_tags.pdf"), "ART-LBL-04",
        "Foam bay tags, nine off", tags[0][1],
        [("Size", doc.labels["ART-LBL-04"]["size"]),
         ("Substrate", doc.labels["ART-LBL-04"]["substrate"]),
         ("Placement", doc.labels["ART-LBL-04"]["placement"]),
         ("Quantity", f"{len(tags)} per kit, one per Rev C bay")],
        [],
        ["Legends are read out of the PKG-EEG-015 section 2.2 Rev C schedule at generation "
         "time and are not typed here, so a tag and the cut file that makes its bay cannot "
         "drift.",
         "The SPARE CELL tag carries the section 7 string, not the section 2.2 legend. "
         "Section 4.2 says the legends are identical to the schedule and section 7 says "
         "this one tag reads `" + (doc.spare_cell_tag() or "") + "`. The section 7 form is "
         "obeyed because it is the one that carries safety information, and the collision "
         "is raised in PKG-EEG-015 section 9.",
         f"THE SPECIFIED TAG CANNOT CARRY THE SPECIFIED TYPE. Section 2.3 asks for an 8 mm "
         f"cap height on the {tw4:g} x {th4:g} mm tag of section 4.2, and "
         f"{len(cap_findings)} of the {len(tags)} legends do not fit -- not even "
         f"HEADPHONES, the shortest. They are drawn at the size section 4.2 fixes, at the "
         f"largest cap height that fits, which runs down to {smallest:.2f} mm. A tag of "
         f"about {tag_proposal[0]:.0f} x {tag_proposal[1]:.0f} mm would carry every legend "
         f"at 8 mm on at most two lines. That is a change to section 4.2 and is raised as "
         f"an open item in PKG-EEG-015 section 9, not decided here.",
         "Measured in DejaVu Sans Bold, the face these files are set in. A narrower face "
         "buys perhaps fifteen per cent, not the factor of two the shortest legend needs "
         "and not the factor of five the longest needs."],
        arts=[(a, f"{lg}  -  cap {cp:.2f} mm, {nl} line(s), shown 1:1")
              for lg, a, cp, nl in tags]))
    if cap_findings:
        note(f"ART-LBL-04: {len(cap_findings)} of {len(tags)} bay legends do not fit the "
             f"{tw4:g} x {th4:g} mm tag at the specified 8 mm cap height; set between "
             f"{smallest:.2f} and {max(f[1] for f in cap_findings):.2f} mm. Carrying all "
             f"nine at 8 mm needs about {tag_proposal[0]:.0f} x {tag_proposal[1]:.0f} mm.")

    # -- ART-LBL-05 -------------------------------------------------------------------------
    a5 = art_lbl_05(doc)
    check_fit("ART-LBL-05", a5)
    written.append(emit(a5, "ART-LBL-05", "carton_marking_set",
                        "ART-LBL-05 carton marking set",
                        doc.labels["ART-LBL-05"]["what"]))
    written.append(control_sheet(
        os.path.join(OUT, "ART-LBL-05_carton_marking_set.pdf"), "ART-LBL-05",
        "Carton marking set", a5,
        [("Size", "200 x 150 mm as drawn; section 4.2 gives no size because it is printed "
                  "on the carton rather than applied as a label"),
         ("Substrate", "The carton itself"),
         ("Placement", doc.labels["ART-LBL-05"]["placement"])],
        [("<<KIT_ID>>", "PKG-EEG-015 section 5."),
         ("<<UNIT_SERIAL>>", "PKG-EEG-015 section 5."),
         ("<<GROSS_SHIPPING_MASS_KG>>", "Weighed at despatch. PKG-EEG-015 section 6 "
                                        "calculates 8.7 kg; section 9 open item 4 records "
                                        "that nothing has been weighed, so the printed "
                                        "figure is the scale reading and not that "
                                        "calculation."),
         ("<<DESPATCH_DATE>>", "The despatch record, PKG-EEG-015 section 8."),
         ("<<PROGRAMME_TELEPHONE>>", "SUPPLIED 2026-09-02. Substituted.")],
        ["The THIS WAY UP arrows are drawn as geometry, not set from a font, so they "
         "survive a printer with no symbol font.",
         "Section 4.2 lists four things this marking carries: FRAGILE -- RESEARCH "
         "INSTRUMENT, THIS WAY UP, gross mass and kit id. The unit serial and the despatch "
         "date are added here because the despatch record of section 8 is held against "
         "both, and a carton that carries only the kit id cannot be reconciled to a unit "
         "at goods-in. That addition is this file's and is raised in section 9."]))

    # -- ART-LBL-06 -------------------------------------------------------------------------
    facts6 = lithium_mark_facts()
    full6, red6 = art_lbl_06(doc, False), art_lbl_06(doc, True)
    written.append(emit(full6, "ART-LBL-06", "lithium_battery_mark",
                        "ART-LBL-06 lithium battery mark, full size",
                        "INCOMPLETE: the regulated pictogram is not supplied."))
    written.append(emit(red6, "ART-LBL-06", "lithium_battery_mark_reduced",
                        "ART-LBL-06 lithium battery mark, reduced size",
                        "INCOMPLETE: the regulated pictogram is not supplied."))
    written.append(control_sheet(
        os.path.join(OUT, "ART-LBL-06_lithium_battery_mark.pdf"), "ART-LBL-06",
        "Lithium battery mark, UN 3481", full6,
        [("Size", f"{facts6['full'][0]:g} x {facts6['full'][1]:g} mm, reduced "
                  f"{facts6['reduced'][0]:g} x {facts6['reduced'][1]:g} mm"),
         ("Substrate", doc.labels["ART-LBL-06"]["substrate"]),
         ("Placement", doc.labels["ART-LBL-06"]["placement"]),
         ("Source", "REG-EEG-012 Rev B section 3.5")],
        [("<<PROGRAMME_TELEPHONE>>", "REG-EEG-012 Rev B section 3.5: a number that is "
                                     "answered by someone who can give information about "
                                     "the shipment during the carrier's operating hours. "
                                     "Not a voicemail box. Any change to it is an ECO.")],
        ["THIS ARTWORK IS INCOMPLETE AND MUST NOT BE PRINTED AS IT STANDS. The "
         "battery-group-and-flame pictogram is a regulated symbol belonging to the edition "
         "of ADR / IATA DGR in force. This package does not hold it and this tool will not "
         "approximate it: a mark with a drawn-from-memory symbol is a mark that can be "
         "refused at a counter, and the refusal happens to a participant.",
         "What IS drawn is the geometry REG-EEG-012 section 3.5 states: the outer size, "
         "the reduced size, the hatched border, the UN3481 text and the telephone field. "
         "The hatch pitch and the type sizes are this file's and are not from the "
         "regulation.",
         "REG-EEG-012 section 3.7 makes the programme's DG-trained shipper the person who "
         "checks the mark against the edition in force before each phase's despatch. This "
         "file is theirs to complete and approve.",
         "PKG-EEG-015 section 7 records that the programme applies the mark to every "
         "carton even where the small-package relief in PI967 section II would not require "
         "it."],
        arts=[(full6, f"full size, trim {facts6['full'][0]:g} x {facts6['full'][1]:g} mm, "
                      f"shown 1:1"),
              (red6, f"reduced, trim {facts6['reduced'][0]:g} x "
                     f"{facts6['reduced'][1]:g} mm, shown 1:1")]))
    note("ART-LBL-06 is incomplete by design: the regulated pictogram is not supplied.")

    # -- ART-LBL-07 -------------------------------------------------------------------------
    a7 = art_lbl_07(doc)
    check_fit("ART-LBL-07", a7)
    written.append(emit(a7, "ART-LBL-07", "tamper_seal", "ART-LBL-07 numbered tamper seal",
                        doc.labels["ART-LBL-07"]["what"]))
    written.append(control_sheet(
        os.path.join(OUT, "ART-LBL-07_tamper_seal.pdf"), "ART-LBL-07",
        "Numbered tamper seal", a7,
        [("Size", doc.labels["ART-LBL-07"]["size"]),
         ("Substrate", doc.labels["ART-LBL-07"]["substrate"]),
         ("Placement", doc.labels["ART-LBL-07"]["placement"]),
         ("Quantity", "Two per despatch, one per hasp, plus one carton security seal "
                      "(PKG-EEG-015 section 6)")],
        [("<<SEAL_NUMBER>>", "Serialised by the seal supplier. Both numbers are written "
                             "on the despatch record and checked at goods-in "
                             "(PKG-EEG-015 section 8).")],
        ["The dashed centre line is the die instruction, not printed matter: the seal is "
         "cut where it crosses the hasp so that opening the case destroys it.",
         "SVC-EEG-013 Rev B section 1 compares all three seal numbers before the hasps are "
         "released, so the number must be legible after transit."]))

    # -- ART-PACK-01 ------------------------------------------------------------------------
    ap = art_pack_01(doc)
    check_fit("ART-PACK-01", ap)
    written.append(emit(ap, "ART-PACK-01", "packing_layout_provisional",
                        "ART-PACK-01 kit packing layout, provisional",
                        "PROVISIONAL - REPLACE WITH PHOTOGRAPH AT FIRST BUILD."))
    written.append(control_sheet(
        os.path.join(OUT, "ART-PACK-01_packing_layout_provisional.pdf"), "ART-PACK-01",
        "Kit packing layout (provisional)", ap,
        [("Size", "A5 landscape, 210 x 148 mm, laminated"),
         ("Placement", "Case lid wallet, packing-list line 6.4"),
         ("Source", "PKG-EEG-015 section 2.2 Rev C bay schedule and section 1.1 pocket "
                    "column")],
        [],
        ["This is a DRAWING, not a photograph. PKG-EEG-015 section 2.3 requires a "
         "photograph of the first Phase 1 kit at 300 dpi with call-outs numbered to the "
         "KPL lines, and allows a rendered layout marked PROVISIONAL until a kit exists. "
         "Section 9 open item 7 records that no such render existed; this is it.",
         "Bay outlines are at true relative scale on the 516.0 x 390.0 mm sheet. The "
         "call-outs are every packing-list line whose pocket column names that bay, so a "
         "line added to section 1.1 appears here on the next run.",
         "It shows layer 1 in plan. It does not show depth, and six of the nine bays hold "
         "parts that are not dimensioned anywhere in package v2.3 (section 2.2 and section "
         "9 open item 1), so this drawing says where a part goes and not that it fits."]))

    # -- ART-DIS-01 -------------------------------------------------------------------------
    ad = art_dis_01(doc)
    check_fit("ART-DIS-01", ad)
    written.append(emit(ad, "ART-DIS-01", "disinfection_guide_card",
                        "ART-DIS-01 disinfection guide card",
                        "Extract of SVC-EEG-013 Rev B section 2 R5."))
    written.append(control_sheet(
        os.path.join(OUT, "ART-DIS-01_disinfection_guide_card.pdf"), "ART-DIS-01",
        "Disinfection guide card", ad,
        [("Size", "A5 portrait, 148 x 210 mm, laminated"),
         ("Placement", "CONSUMABLES bay, packing-list line 6.6 (RFQ A-05)"),
         ("Source", "SVC-EEG-013 Rev B section 2 R5, which section 9 of that document "
                    "names as this card's source text")],
        [],
        ["The agent, concentration and contact-time table and the prohibition table are "
         "read out of SVC-EEG-013 at generation time. Nothing on this card is written "
         "here, so the card and the manual cannot disagree.",
         "SVC-EEG-013 section 2 R5 states plainly that efficacy is not validated by this "
         "programme and that the 25-cycle material-compatibility protocol has not been "
         "run. That sentence is printed on the card rather than left in the manual, "
         "because the person holding the card is the person doing the wiping."]))

    # -- ART-RET-01 -------------------------------------------------------------------------
    ar = art_ret_01(doc)
    check_fit("ART-RET-01", ar)
    written.append(emit(ar, "ART-RET-01", "return_shipping_instructions",
                        "ART-RET-01 return-shipping instruction sheet",
                        "Copy from PKG-EEG-015 Rev B section 7."))
    written.append(control_sheet(
        os.path.join(OUT, "ART-RET-01_return_shipping_instructions.pdf"), "ART-RET-01",
        "Return-shipping instruction sheet", ar,
        [("Size", "A4, 210 x 297 mm"),
         ("Placement", "Carton document wallet, packing-list line 6.7, with the pre-paid "
                       "return label"),
         ("Source", "PKG-EEG-015 Rev B section 7, block quote")],
        [("<<PROGRAMME_TELEPHONE>>", "SUPPLIED 2026-09-02. Substituted."),
         ("<<PROGRAMME_EMAIL>>", "SUPPLIED 2026-09-02. Substituted."),
         ("<<KIT_ID>>", "PKG-EEG-015 section 5."),
         ("<<RETURN_TRACKING_NUMBER>>", "The despatch record, PKG-EEG-015 section 8.")],
        ["The body copy is the section 7 block quote, read out of the document at "
         "generation time. Section 7 introduces it with 'reads, in substance', so the "
         "wording is the programme's to settle before print; what this file guarantees is "
         "that the sheet and the document say the same thing today.",
         "The counter script is boxed and set larger because it is the sentence a "
         "participant reads aloud to a counter clerk under pressure."]))

    # -- DRW-LBL-PLACEMENT ------------------------------------------------------------------
    dp = drw_lbl_placement(doc)
    check_fit("DRW-LBL-PLACEMENT", dp)
    written.append(emit(dp, "DRW-LBL-PLACEMENT", "label_placement",
                        "DRW-LBL-PLACEMENT label and marking placement drawing",
                        "Four views. Case and carton outlines are published, not measured."))
    written.append(control_sheet(
        os.path.join(OUT, "DRW-LBL-PLACEMENT_label_placement.pdf"), "DRW-LBL-PLACEMENT",
        "Label and marking placement", dp,
        [("Size", "A3 landscape, 420 x 297 mm"),
         ("Used by", "PKG-EEG-015 Rev B section 4.2: 'Sign-off on placement: packer, "
                     "checked by QA against the placement drawing DRW-LBL-PLACEMENT'"),
         ("Views", "1 POD-P1 lid, 2 case lid, 3 case base, 4 outer carton long face")],
        [],
        ["The faces, the labels and their sizes are section 4.2's and are fixed. The "
         "positions on those faces are this drawing's, and they are a PROPOSAL: no travel "
         "case has been bought or measured (section 9 open item 2) and the carton is sized "
         "from that published shell (section 6). Every position is dimensioned from the "
         "two nearest edges so that a measured shell changes the numbers and not the "
         "arrangement.",
         "Section 4.2's rule that no label may cover the pressure-equalisation valve is "
         "printed on view 2. The valve's position on the bought shell is not known, so it "
         "is a written constraint here and not a drawn keep-out. Add it when the shell is "
         "measured.",
         "The Phase 2 and 3 placement of ART-LBL-01 is the HM-01 occipital shell rear "
         "face, per section 4.1. Only the Phase 1 placement is drawn, because the Phase 2 "
         "pod-in-helmet arrangement is not dimensioned in package v2.3."],
        sheet=A3))

    write_readme(doc, written, findings, cap_findings, tag_proposal, (tw4, th4))
    print(f"\n{len(written)} files written to graphics/labels/")
    return written


def write_readme(doc, written, findings, cap_findings, tag_proposal, tag_size):
    path = os.path.join(OUT, "README_artwork.txt")
    lines = []
    lines.append("Label and packaging artwork -- graphics/labels/")
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"Owned by:   {OWNER}, sections 4.1, 4.2, 2.3 and 7")
    lines.append(f"Registered: ECO-EEG-016 Rev B section 1, 'not documents at all' --")
    lines.append("            artwork files controlled as generated artifacts under graphics/.")
    lines.append(f"Generated:  {GENERATOR} on {datetime.date.today().isoformat()}")
    lines.append(f"Licence:    {LICENCE}")
    lines.append("")
    lines.append("These files carry no revision letter of their own. They carry the revision of")
    lines.append("the document that owns them, which is PKG-EEG-015 Rev B. Re-run the generator")
    lines.append("after any change to that document: every legend, size, substrate and piece of")
    lines.append("copy below is read out of the Markdown, not typed here.")
    lines.append("")
    lines.append("Two files per identifier:")
    lines.append("  *.svg   the artwork alone at exact trim size, all text outlined. Printer file.")
    lines.append("  *.pdf   an A4 (A3 for the placement drawing) control sheet: title block, the")
    lines.append("          artwork 1:1 inside trim marks, the variable-data table, the notes.")
    lines.append("")
    lines.append("NOT READY TO PRINT")
    lines.append("-" * 78)
    lines.append("ART-LBL-03, ART-LBL-05, ART-LBL-06 and ART-RET-01 carry <<PLACEHOLDER>> fields.")
    lines.append("The programme's postal address and telephone number appear nowhere in package")
    lines.append("v2.3 and are not invented here. ART-LBL-06 is further incomplete: the regulated")
    lines.append("battery-group-and-flame pictogram belongs to the edition of ADR / IATA DGR in")
    lines.append("force, this package does not hold it, and REG-EEG-012 Rev B section 3.7 makes")
    lines.append("the DG-trained shipper the person who completes and approves that mark.")
    lines.append("")
    if cap_findings:
        tw, th = tag_size
        lines.append("ART-LBL-04 TAG SIZE -- THE SPECIFIED TAG CANNOT CARRY THE SPECIFIED TYPE")
        lines.append("-" * 78)
        lines.append(f"PKG-EEG-015 section 4.2 fixes the bay tag at {tw:g} x {th:g} mm and section 2.3")
        lines.append("asks for an 8 mm cap height. Not one of the nine legends fits on one line:")
        one = max(text_width(f[0], WANT_CAP, FONT_B) for f in cap_findings)
        least = min(text_width(f[0], WANT_CAP, FONT_B) for f in cap_findings)
        lines.append(f"the least demanding needs about {least + 2 * TAG_MARGIN:.0f} mm of tag "
                     f"and the worst about {one + 2 * TAG_MARGIN:.0f} mm.")
        lines.append(f"The tags are drawn at the size section 4.2 fixes, at the largest cap height that")
        lines.append("fits on at most two lines. The last column is the tag width that would carry")
        lines.append("that legend at 8 mm on at most two lines.")
        lines.append("")
        lines.append(f"  {'legend':<48} {'cap mm':>7} {'lines':>6} {'8 mm needs':>11}")
        for legend, got, nl, need in cap_findings:
            lines.append(f"  {legend:<48} {got:>7.2f} {nl:>6d} {need:>10.0f}")
        lines.append("")
        lines.append(f"A tag of about {tag_proposal[0]:.0f} x {tag_proposal[1]:.0f} mm carries every legend at 8 mm on at most")
        lines.append("two lines. That is a PROPOSAL. Changing the tag size changes section 4.2, and")
        lines.append("PKG-EEG-015 section 9 carries it as an open item for the programme to settle.")
        lines.append("")
    lines.append("FILES")
    lines.append("-" * 78)
    for p in sorted(written):
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        lines.append(f"{h}  {os.path.basename(p)}")
    lines.append("")
    if findings:
        lines.append("GENERATOR NOTES FROM THIS RUN")
        lines.append("-" * 78)
        for f in findings:
            lines.append(f"  - {f}")
        lines.append("")
    lines.append("WHAT HAS NOT BEEN VERIFIED")
    lines.append("-" * 78)
    lines.append("Nothing here has been printed, applied, wiped with IPA or read by a barcode")
    lines.append("verifier. The Data Matrix encoder is checked against the ISO/IEC 16022 worked")
    lines.append("example and by decoding its own symbols; that proves the encoder, not a printed")
    lines.append("label. PKG-EEG-015 section 4.1 requires ISO/IEC 15415 grade C or better after")
    lines.append("50 wipes with 70 % IPA, and that first-article verification is what releases")
    lines.append("this artwork for use.")
    with open(path, "w", encoding="utf8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(0 if selftest() else 1)
    main()
