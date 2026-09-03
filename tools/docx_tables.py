#!/usr/bin/env python3
"""
docx_tables.py -- make the generated .docx (and therefore the .pdf) render tables properly.

The symptom was severe: in the delivered PDFs many tables were not tables at all.  Every
cell appeared as its own full-width paragraph, one per line, with no rules and no columns,
so a twenty-row connector table read as a hundred and sixty loose lines.

There were two causes, both in how the .docx was built:

  1. **No table style.**  Pandoc writes ``<w:tblStyle w:val="Table"/>`` on every table and
     expects the reference document to define a style whose styleId is exactly ``Table``.
     The generated reference had none, so the tables inherited nothing -- no borders, no
     header treatment, no cell padding.

  2. **A grid far wider than the page.**  Pandoc emitted ``<w:tblLayout w:type="fixed"/>``
     with equal columns of 2640 twips each.  On an eight-column table that is 21 120 twips
     against the 9 411 twips of A4 text width -- 2.24 times the page.  LibreOffice cannot
     fit that, so it abandoned the table layout and stacked the cells.

This module fixes both, and then does what a person would do by eye: weights each column by
what is actually in it, repeats the header row on every page, stops rows splitting across a
page break, and steps wide tables down a font size so they still fit A4 portrait.

Everything here is done with a real XML parser.  An earlier regex version corrupted the
header rows by inserting ``<w:sz>`` at the front of every ``<w:rPr>``; WordprocessingML
fixes the order of the children of ``<w:rPr>``, and out-of-order children make a renderer
discard the run.  Hence ElementTree, and hence the font size lives in a style rather than
being injected into runs.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import copy
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{NS}}}"

# A4 (21.0 cm) less the 2.2 cm margins the reference document sets, in twips.
TEXT_WIDTH_TWIPS = int(round((21.0 - 2 * 2.2) / 2.54 * 1440))     # 9411

HEAD_FILL = "1F3864"
LINE = "8FA0AD"
BAND = "F2F5F8"

# Wide tables get a smaller style instead of edited runs.  half-points.
SIZE_STEPS = {"Table": None, "TableSmall": 16, "TableTiny": 14}


def _q(tag: str) -> str:
    return W + tag


def table_style_xml(style_id: str = "Table", half_points: int | None = None) -> str:
    """The <w:style> pandoc asks for.  styleId MUST be exactly 'Table' for the base one."""
    def edge(tag):
        return f'<w:{tag} w:val="single" w:sz="4" w:space="0" w:color="{LINE}"/>'
    borders = "".join(edge(t) for t in
                      ("top", "left", "bottom", "right", "insideH", "insideV"))
    rpr = (f'<w:rPr><w:sz w:val="{half_points}"/><w:szCs w:val="{half_points}"/></w:rPr>'
           if half_points else "")
    return (
        f'<w:style w:type="table" w:styleId="{style_id}">'
        f'<w:name w:val="{style_id}"/>'
        '<w:basedOn w:val="TableNormal"/>'
        '<w:uiPriority w:val="59"/>'
        '<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        f'{rpr}'
        '<w:tblPr>'
        '<w:tblInd w:w="0" w:type="dxa"/>'
        f'<w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblCellMar>'
        '<w:top w:w="60" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="90" w:type="dxa"/>'
        '</w:tblCellMar>'
        '</w:tblPr>'
        '<w:tblStylePr w:type="firstRow"><w:pPr><w:keepNext/></w:pPr>'
        '<w:rPr><w:b/><w:color w:val="FFFFFF"/></w:rPr>'
        f'<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{HEAD_FILL}"/></w:tcPr>'
        '</w:tblStylePr>'
        '<w:tblStylePr w:type="band2Horz">'
        f'<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="{BAND}"/></w:tcPr>'
        '</w:tblStylePr>'
        '</w:style>'
    )


def install_style(styles_xml: str) -> str:
    """Add (or replace) the three table styles in a styles.xml."""
    for sid in SIZE_STEPS:
        styles_xml = re.sub(rf'<w:style [^>]*w:styleId="{sid}"[ >].*?</w:style>', "",
                            styles_xml, flags=re.S)
    body = "".join(table_style_xml(sid, hp) for sid, hp in SIZE_STEPS.items())
    return styles_xml.replace("</w:styles>", body + "</w:styles>")


# --------------------------------------------------------------------------- widths
def _cell_text(tc: ET.Element) -> str:
    return "".join(t.text or "" for t in tc.iter(_q("t")))


def _weights(rows: list[ET.Element], ncols: int) -> list[float]:
    """Column weights from content: the 85th-percentile cell length, softened.

    Softening matters.  Raw maximum length gives a single 300-character notes column most of
    the table and starves the rest; the fourth root keeps the long column widest while the
    short ones stay legible, which is what a person does by eye.
    """
    lens: list[list[int]] = [[] for _ in range(ncols)]
    for r in rows:
        for i, tc in enumerate(r.findall(_q("tc"))[:ncols]):
            lens[i].append(len(_cell_text(tc)))
    out = []
    for col in lens:
        if not col:
            out.append(1.0)
            continue
        col.sort()
        p85 = col[min(len(col) - 1, int(0.85 * len(col)))]
        out.append(max(float(p85), 2.0) ** 0.25)
    return out


def _alloc(weights: list[float], total: int) -> list[int]:
    """Allocate `total` twips across columns, with a floor so nothing collapses."""
    n = len(weights)
    floor = max(400, min(700, total // (n * 3)))
    free = total - floor * n
    if free <= 0:
        return [total // n] * n
    s = sum(weights) or 1.0
    out = [floor + int(free * (x / s)) for x in weights]
    out[-1] += total - sum(out)
    return out


def _set(parent: ET.Element, tag: str, attrs: dict, index: int = 0) -> ET.Element:
    """Replace-or-insert a single child element."""
    el = parent.find(_q(tag))
    if el is None:
        el = ET.Element(_q(tag))
        parent.insert(index, el)
    el.attrib.clear()
    for k, v in attrs.items():
        el.set(W + k, v)
    return el


def _fix_table(tbl: ET.Element) -> None:
    grid = tbl.find(_q("tblGrid"))
    if grid is None:
        return
    rows = tbl.findall(_q("tr"))
    ncols = max([len(r.findall(_q("tc"))) for r in rows] or [0])
    if ncols < 1:
        return

    widths = _alloc(_weights(rows, ncols), TEXT_WIDTH_TWIPS)

    # rebuild the grid
    for gc in list(grid):
        grid.remove(gc)
    for wv in widths:
        ET.SubElement(grid, _q("gridCol")).set(W + "w", str(wv))

    pr = tbl.find(_q("tblPr"))
    if pr is not None:
        # autofit, not fixed: let the renderer reflow long cells
        _set(pr, "tblLayout", {"type": "autofit"})
        _set(pr, "tblW", {"w": "5000", "type": "pct"})
        # a wide table gets a smaller *style*, never edited runs
        st = pr.find(_q("tblStyle"))
        if st is not None:
            st.set(W + "val", "TableTiny" if ncols >= 9
                   else "TableSmall" if ncols >= 7 else "Table")

    # per-cell widths must agree with the grid or the renderer re-derives its own
    for r in rows:
        for i, tc in enumerate(r.findall(_q("tc"))):
            if i >= ncols:
                break
            tcpr = tc.find(_q("tcPr"))
            if tcpr is None:
                tcpr = ET.Element(_q("tcPr"))
                tc.insert(0, tcpr)
            _set(tcpr, "tcW", {"w": str(widths[i]), "type": "dxa"})

    # header repeats on every page; rows do not split across a page break
    for i, r in enumerate(rows):
        trpr = r.find(_q("trPr"))
        if trpr is None:
            trpr = ET.Element(_q("trPr"))
            r.insert(0, trpr)
        for tag in ("cantSplit", "tblHeader"):
            for old in trpr.findall(_q(tag)):
                trpr.remove(old)
        ET.SubElement(trpr, _q("cantSplit"))
        if i == 0:
            ET.SubElement(trpr, _q("tblHeader"))


def fix_document(doc_xml: bytes) -> tuple[bytes, int]:
    for prefix, uri in _NSMAP.items():
        ET.register_namespace(prefix, uri)
    root = ET.fromstring(doc_xml)
    tables = list(root.iter(_q("tbl")))
    for t in tables:
        _fix_table(t)
    return ET.tostring(root, encoding="UTF-8", xml_declaration=True), len(tables)


_NSMAP = {
    "w": NS,
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
    "wpg": "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "v": "urn:schemas-microsoft-com:vml",
}


def process(path: str) -> int:
    """Rewrite a .docx in place.  Returns the number of tables fixed."""
    tmp = path + ".tmp"
    n = 0
    with zipfile.ZipFile(path) as zin, \
            zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                data = install_style(data.decode("utf8")).encode("utf8")
            elif item.filename == "word/document.xml":
                data, n = fix_document(data)
            zout.writestr(item, data)
    shutil.move(tmp, path)
    return n


if __name__ == "__main__":
    import glob
    import os
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
    for f in sorted(glob.glob(os.path.join(target, "*.docx"))):
        print(f"  {os.path.basename(f)}: {process(f)} tables")
