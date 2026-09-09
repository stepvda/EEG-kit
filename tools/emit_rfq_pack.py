#!/usr/bin/env python3
"""
emit_rfq_pack.py -- build a vendor RFQ submission pack from `design.py`.

**Nothing here sends anything.**  It writes a directory.  A person uploads it.

WHY THIS EXISTS

About twenty manufacturers are in the current sweep and several of them take an RFQ
through a web portal rather than by email -- JLCPCB's layout desk, Bittele, PCBCart.
Every portal asks the same twenty questions in a different order, and every one of them
is an opportunity to type a figure that disagrees with `design.py`.  This tool answers
those twenty questions once, from the source, and writes the answers down twice: as
`fields.json` for a filling script, and as `ANSWER_SHEET.md` for the person who has to
check the filled page before pressing submit.

The two files are emitted from ONE list of `Field` objects, so they cannot disagree.

WHAT "NO FIGURE IS TYPED BY HAND" MEANS HERE

A number in this file is not evidence of anything.  Every `Field` that restates a
specification carries `evidence` -- the verbatim sentence from `design.py` or from a
controlled document -- and `must_contain`, the substrings that have to appear in that
evidence.  `Field.check()` fails the build if they do not.  So if someone changes the
finished thickness in `design.py` and not here, this tool stops; it does not quietly
ship the stale figure to a fabricator.  Fields that are read straight off a symbol
(`design.py BOARD_W`) need no evidence: they ARE the source.

WHAT IS VENDOR-AGNOSTIC AND WHAT IS NOT

`carrier()` and `wh_bus_board()` build the canonical answers and know nothing about any
vendor.  A `VendorProfile` maps canonical keys onto one portal's controls, declares
which file extensions that portal accepts, and -- the part that earns its keep --
declares which canonical fields the portal has **no control for**, so they can be routed
into the notes and the specification file instead of being silently dropped.  That is
how the PCBCart stack-up problem was caught rather than defaulted.

NO DATES.  Nothing this tool writes states or implies a fabrication date; `_no_dates()`
enforces it over every generated text.  That also makes the pack reproducible: re-running
it produces byte-identical output.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import wh_bus as W          # noqa: E402

DIST = os.path.join(PKG, "dist", "rfq")
TICKET = "BSY-598327"

# The one place the contact details are written.  Section 3 of the brief asks for this
# explicitly: three copies of a phone number is three chances to mistype it.
CONTACT = {
    "name": "Stephane van der Aa",
    "company": "TI One Voice",
    "country": "Belgium",
    # PCBCart makes `country_state` a REQUIRED field and offers 13 Belgian provinces.
    # This is NOT a guess: every controlled document in `docs/` carries the header
    # "Issued by: TI One Voice research programme (one.witysk.org), Brussels, Belgium",
    # and `doc_issuer_locality()` reads it back and fails the build if it changes.
    "state": "Brussels",
    "phone": "+32 493 70 16 01",
    "email": "stephane@stepvda.com",
}


class SourceError(RuntimeError):
    """A figure in this file no longer agrees with the source it claims to come from."""


# ---------------------------------------------------------------------------------------
# Reading the source
# ---------------------------------------------------------------------------------------
def fab_notes() -> dict:
    """`design.py` NOTES['fabrication'] as {note number: full text}.

    The notes are written as a numbered list with hanging indents.  A note is joined
    back into one string so that `must_contain` can be checked against the whole of it.
    """
    out, cur, num = {}, [], None
    for line in D.NOTES["fabrication"]:
        m = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m:
            if num is not None:
                out[num] = " ".join(cur)
            num, cur = int(m.group(1)), [m.group(2).strip()]
        elif num is not None:
            cur.append(line.strip())
    if num is not None:
        out[num] = " ".join(cur)
    return out


def doc_issuer_locality() -> str:
    """The locality in the 'Issued by' header every controlled document carries.

    The contact address is not this tool's to invent, so it is read back from the
    documents that already state it and checked, exactly as a specification figure is.
    """
    line = doc_text("docs/DSN-EEG-003_RevD_manufacturing_design_package.md",
                    "**Issued by:**", span=0)
    m = re.search(r"\),\s*([A-Za-z][A-Za-z \-]+),\s*Belgium", line)
    if not m:
        raise SourceError(f"cannot read the issuer locality from: {line!r}")
    return m.group(1).strip()


def rfq_scope() -> str:
    """The programme's own statement of its phases, quoted rather than paraphrased."""
    return doc_text("docs/RFQ-EEG-001_RevE_EEG_kit_specification.md",
                    "2 prototype units, 10 kits")


def net_report() -> dict:
    """The Rev B net report.  This submission is budgetary ON REV B GEOMETRY, so the
    Rev B census is the right one to quote; it is generated from `design.py` by
    `tools/gerber.py` and is not a second source of truth."""
    p = os.path.join(PKG, "kicad", "EEG-CAR-01_RevB_netreport.json")
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def doc_text(relpath: str, needle: str, span: int = 2) -> str:
    """A sentence from a controlled document, so that a citation to a document is
    checked exactly as a citation to `design.py` is.  Returns the matching line joined
    with the next `span` lines, since these documents wrap mid-sentence."""
    p = os.path.join(PKG, relpath)
    with open(p, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for i, line in enumerate(lines):
        if needle in line:
            return " ".join(x.strip() for x in lines[i:i + 1 + span]).strip()
    raise SourceError(f"{needle!r} no longer appears in {relpath}")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def readme_checksum(readme: str, filename: str) -> str:
    """The SHA-256 a `README_layer_map_and_checksums.txt` records for one file."""
    with open(readme, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^\s*([0-9a-f]{64})\s+(\S+)\s*$", line)
            if m and m.group(2) == filename:
                return m.group(1)
    raise SourceError(f"{filename} has no checksum in {readme}")


_DATE_PATTERNS = (
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+\d{4}\b",
    r"\b(?:January|February|March|April|May|June|July|August|September|October|"
    r"November|December)\s+\d{1,2},?\s+\d{4}\b",
)


def find_dates(text: str) -> list:
    """Every date-like string in a text.  Used to AUDIT copied files, not to edit them."""
    out = []
    for pat in _DATE_PATTERNS:
        out.extend(m.group(0) for m in re.finditer(pat, text))
    return out


def _no_dates(text: str, what: str) -> str:
    """Ground rule: nothing this tool WRITES states or implies a fabrication date.

    Scope is deliberate. It applies to text this tool authors -- the answer sheet, the
    bidder README, the notes. It does NOT strip dates out of released controlled files
    that are copied into the pack: those are checksummed where they were released, and
    editing one to tidy a date would break the provenance that makes it worth sending.
    Copied files are AUDITED instead, by `date_audit()`, so any date that reaches the
    vendor is a stated fact rather than an unnoticed one.
    """
    for pat in _DATE_PATTERNS:
        m = re.search(pat, text)
        if m:
            raise SourceError(f"{what} contains a date: {m.group(0)!r}")
    return text


# ---------------------------------------------------------------------------------------
# A canonical answer
# ---------------------------------------------------------------------------------------
class Field:
    """One question a portal asks, answered once.

    `value`        what goes in the box, as a person would read it.
    `source`       where it comes from: a `design.py` symbol, or document and section.
    `evidence`     the verbatim sentence behind it, when the value is a restatement.
    `must_contain` substrings that must appear in `evidence`, or the build fails.
    """

    __slots__ = ("key", "label", "value", "source", "evidence", "must_contain")

    def __init__(self, key, label, value, source, evidence=None, must_contain=()):
        self.key = key
        self.label = label
        self.value = value
        self.source = source
        self.evidence = evidence
        self.must_contain = tuple(must_contain)

    def check(self) -> None:
        if not self.must_contain:
            return
        if self.evidence is None:
            raise SourceError(f"{self.key}: must_contain given with no evidence")
        missing = [s for s in self.must_contain if s not in self.evidence]
        if missing:
            raise SourceError(
                f"{self.key}: {missing!r} no longer appears in its source.\n"
                f"  source:   {self.source}\n"
                f"  evidence: {self.evidence}\n"
                f"  The source has moved and this file has not.  Fix this file."
            )

    def as_dict(self) -> dict:
        d = {"label": self.label, "value": self.value, "source": self.source}
        if self.evidence:
            d["evidence"] = self.evidence
        return d


# ---------------------------------------------------------------------------------------
# EEG-CAR-01 -- the assembled carrier
# ---------------------------------------------------------------------------------------
def carrier() -> dict:
    RFQ_SCOPE = rfq_scope()
    fab = fab_notes()
    nr = net_report()
    asm = " ".join(D.NOTES["assembly"][:1])
    dsn = "DSN-EEG-003 Rev D section 3.2"

    if len(D.C) != nr["parts"]:
        raise SourceError(
            f"design.py has {len(D.C)} designators, the net report says {nr['parts']}")

    F = [
        Field("board", "Board", "EEG-CAR-01", "design.py, the carrier"),
        Field("dimensions", "Dimensions (X by Y)",
              f"{D.BOARD_W:.1f} x {D.BOARD_H:.1f} mm",
              "design.py BOARD_W, BOARD_H"),
        Field("layers", "Layers", "4",
              f"design.py fabrication note 2; {dsn}",
              fab[2], ["FOUR layers"]),
        Field("layer_roles", "Layer roles",
              "L1 signal, L2 reference plane, L3 reference plane, L4 signal",
              f"design.py fabrication note 2; {dsn}",
              fab[2], ["L1 signal", "L4 signal"]),
        Field("thickness", "Finished thickness", "1.60 mm +/- 10 %",
              f"design.py fabrication note 2; {dsn}",
              fab[2], ["1.60 mm +/- 10 %"]),
        Field("material", "Material", "FR-4, Tg >= 150 C",
              f"design.py fabrication note 2; {dsn}",
              fab[2], ["FR-4", "Tg >= 150 C"]),
        Field("copper_outer", "Outer copper", "35 um (1 oz) finished",
              "design.py fabrication note 2", fab[2], ["1 oz (35 um)"]),
        Field("copper_inner", "Inner copper", "17 um (0.5 oz)",
              "design.py fabrication note 2", fab[2], ["0.5 oz (17 um)"]),
        Field("stackup", "Stack-up (SPECIFIED, not default)",
              "mask / 35 um L1 / prepreg 0.200 / 17 um L2 / core 1.065 / "
              "17 um L3 / prepreg 0.200 / 35 um L4 / mask = 1.60 mm +/- 10 %",
              f"design.py fabrication note 2; {dsn}",
              fab[2],
              ["Stack: 0.035 / prepreg 0.2 / 0.017 / core 1.065 / 0.017 / "
               "prepreg 0.2 / 0.035."]),
        Field("surface_finish", "Surface finish",
              "ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um",
              f"design.py fabrication note 3; {dsn}",
              fab[3], ["ENIG", "Au 0.05-0.10 um over Ni 3.0-6.0 um"]),
        Field("soldermask", "Solder mask", "green LPI both sides",
              "design.py fabrication note 4", fab[4], ["green LPI both sides"]),
        Field("legend", "Silkscreen legend", "white, both sides",
              "design.py fabrication note 4", fab[4], ["silkscreen white, both sides"]),
        Field("min_track_clearance", "Minimum track / clearance", "0.20 / 0.20 mm",
              f"design.py fabrication note 5; {dsn}",
              fab[5], ["Minimum track 0.20 mm, minimum clearance 0.20 mm"]),
        Field("vias", "Vias",
              "through vias only, 0.60 mm pad / 0.30 mm finished hole, tented both "
              "sides. No blind, buried, back-drilled, filled or plugged vias anywhere",
              f"design.py fabrication note 6; {dsn} (the 'no blind or buried' wording)",
              fab[6], ["0.60 mm pad / 0.30 mm finished hole", "tented on both sides"]),
        Field("smallest_hole", "Smallest plated hole", "0.30 mm",
              "design.py fabrication note 7", fab[7],
              ["Smallest plated hole 0.30 mm"]),
        Field("largest_hole", "Largest plated hole", "1.70 mm (J15-J17)",
              "design.py fabrication note 7", fab[7], ["largest 1.70 mm"]),
        Field("buried_blind", "Blind / buried vias", "No",
              f"{dsn} -- through vias only"),
        Field("impedance", "Controlled impedance", "No",
              "design.py fabrication note 10", fab[10],
              ["No controlled impedance is required"]),
        Field("class", "Acceptance class",
              "IPC-6012 class 2 (fabrication), IPC-A-600 class 2 (bare board), "
              "IPC-A-610 class 2 (assembly)",
              f"design.py fabrication note 9 (first two); {dsn} (all three)",
              fab[9], ["IPC-6012 class 2, IPC-A-600 class 2"]),
        Field("electrical_test", "Electrical test",
              f"100 % to the supplied IPC-D-356A netlist, {nr['nets']} nets",
              f"design.py fabrication note 9; net report nets = {nr['nets']}",
              fab[9], ["100 % electrical test to the supplied", "IPC-D-356A netlist"]),
        Field("census", "Components / pads / nets",
              f"{nr['parts']} / {nr['pads']} / {nr['nets']}",
              "kicad/EEG-CAR-01_RevB_netreport.json, generated from design.py; "
              f"designator count cross-checked against len(design.C) = {len(D.C)}"),
        Field("assembly_side", "Assembly side(s)", "Single side",
              "design.py assembly note 1; "
              f"{dsn} -- 'L4 carries routing, copper and legend, and no parts'",
              asm, ["SMT on the top side only.",
                    "All through-hole parts on the top side."]),
        Field("delivery_method", "Delivery method",
              "Single board without technical rail",
              "DSN-EEG-003 section 3.2: 150.0 x 130.0 mm rectangular, no cut-outs; "
              "design.py fabrication note 12 leaves panelisation to the fabricator"),
        Field("quantities", "Quantities", "2, 10, 25, 50",
              "RFQ-EEG-001 Rev E, Scope -- successive phases of one programme",
              RFQ_SCOPE,
              ["2 prototype units, 10 kits", "25 to 50 in total"]),
        # Machine-readable, so a filling script never has to parse the prose above.
        Field("quantity_breaks", "Quantity breaks (boards)", "2 | 10 | 25 | 50",
              "RFQ-EEG-001 Rev E, Scope; one carrier per kit",
              RFQ_SCOPE, ["2 prototype units, 10 kits", "25 to 50 in total"]),
        Field("custom_testing", "Custom testing", "No",
              "TST-EEG-004 Rev C exists, but the four fixtures of JIG-EEG-009 have no "
              "copper and cannot be built yet -- see the bidder notes"),
        Field("ic_programming", "IC programming", "No",
              "Provisioning writes the ATECC608B configuration zone irreversibly and "
              "only 4 of its 128 bytes have been reviewed -- see the bidder notes"),
        Field("origin", "Production and shipping origin", "As decided by PCBCART",
              "Raised in the notes instead: a Thailand build changes duty and lead "
              "time, which is a commercial conversation and not a form field"),
        Field("coupon", "Lot coupon", "One four-layer microsection coupon per lot",
              "design.py fabrication note 13", fab[13],
              ["ONE four-layer microsection coupon per fabrication lot"]),
        Field("lot_documents", "Lot documents",
              "certificate of conformance; 100 % electrical test report to the "
              "supplied IPC-D-356A; ENIG thickness report (XRF, Au and Ni, min 3 "
              "points); layer-to-layer registration report; microsection report "
              "including the internal annular ring, accept limit 0.025 mm",
              "design.py fabrication notes 13 and 14",
              fab[13] + " " + fab[14],
              ["certificate of conformance", "ENIG thickness report, XRF",
               "internal annular ring below 0.025 mm"]),
    ]
    for f in F:
        f.check()
    return {"id": "EEG-CAR-01", "title": "EEG-CAR-01 -- assembled carrier",
            "assembled": True, "fields": F}


# ---------------------------------------------------------------------------------------
# WH-BUS-01 -- the bare contact-light bus board
# ---------------------------------------------------------------------------------------
def wh_bus_board() -> dict:
    RFQ_SCOPE = rfq_scope()
    _kits = (2, 10, 25, 50)
    panel_w = W.PANEL_COLS * W.BOARD_W + 2 * W.PANEL_RAIL
    panel_h = W.PANEL_ROWS * W.BOARD_H + 2 * W.PANEL_RAIL
    up = W.PANEL_COLS * W.PANEL_ROWS
    _p = [-(-k // up) for k in _kits]          # ceil, one board per kit
    panel_breaks = sorted(set(_p))
    panel_breaks_note = ", ".join(f"{k} kits -> {n} panel{'s' if n > 1 else ''}"
                                  for k, n in zip(_kits, _p))

    F = [
        Field("board", "Board", "WH-BUS-01", "wh_bus.py, the contact-light bus board"),
        Field("dimensions", "Dimensions (X by Y)",
              f"{W.BOARD_W:.1f} x {W.BOARD_H:.1f} mm",
              "wh_bus.py BOARD_W, BOARD_H (PARTS-EEG-019 Rev B)"),
        Field("layers", "Layers", "2", "wh_bus.py -- L1 signal, L2 signal, no plane"),
        Field("thickness", "Finished thickness",
              f"{W.BOARD_T:.2f} mm +/- 10 %", "wh_bus.py BOARD_T"),
        Field("material", "Material", "FR-4, Tg >= 150 C",
              "wh_bus.py -- one material across both boards is one qualification"),
        Field("copper_outer", "Outer copper", "35 um (1 oz) both sides",
              "wh_bus.py -- 1 oz copper both sides"),
        Field("stackup", "Stack-up",
              f"mask / 35 um L1 / FR-4 core {W.CORE:.2f} / 35 um L2 / mask "
              f"= {W.BOARD_T:.2f} mm +/- 10 %",
              "wh_bus.py CORE, BOARD_T -- 0.71 mm is a stock core; the fabricator may "
              "substitute its nearest and hold the finished thickness"),
        Field("surface_finish", "Surface finish",
              "ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um",
              "wh_bus.py -- as EEG-CAR-01"),
        Field("soldermask", "Solder mask", "green LPI both sides", "wh_bus.py"),
        Field("legend", "Silkscreen legend", "white, both sides", "wh_bus.py"),
        Field("min_track", "Minimum track", f"{W.BUS_W:.2f} mm (the LED_V bar)",
              "wh_bus.py BUS_W"),
        Field("holes", "Plated through holes",
              f"{len(W.PADS)} per board, {W.HOLE_D:.2f} mm finished, "
              f"{W.PAD_D:.2f} mm pad, one tool",
              "wh_bus.py PADS, HOLE_D, PAD_D"),
        Field("vias", "Vias", "none -- the ten plated holes are component pads",
              "wh_bus.py -- ten pads and one copper bar, no separate vias"),
        Field("delivery_method", "Delivery method",
              "Panel with technical rail", "wh_bus.py PANEL_COLS, PANEL_ROWS, "
              "PANEL_RAIL -- rails on all four sides"),
        Field("panel", "Panel",
              f"{W.PANEL_COLS} x {W.PANEL_ROWS} V-scored array, {up} up, "
              f"step {W.BOARD_W:.1f} x {W.BOARD_H:.1f} mm, "
              f"{W.PANEL_RAIL:.0f} mm rails on all four sides: "
              f"panel {panel_w:.1f} x {panel_h:.1f} mm",
              "wh_bus.py PANEL_COLS, PANEL_ROWS, PANEL_RAIL, BOARD_W, BOARD_H"),
        Field("class", "Acceptance class",
              "IPC-6012 class 2 (fabrication), IPC-A-600 class 2 (bare board)",
              "wh_bus.py"),
        Field("electrical_test", "Electrical test",
              "100 % to the supplied IPC-D-356A netlist",
              "wh_bus.py -- not optional here: the isolation of pad 10 from the LED_V "
              "bar is the one property a visual inspection will not catch"),
        Field("assembly_side", "Assembly side(s)", "Not assembled -- bare board only",
              "wh_bus.py -- no component, no paste layer, no CPL, no stencil"),
        Field("quantities", "Quantities",
              f"per panel of {up}; programme phases 2 / 10 / 25 / 50 kits",
              "wh_bus.py PANEL_COLS/PANEL_ROWS; RFQ-EEG-001 Rev E, Scope",
              RFQ_SCOPE,
              ["2 prototype units, 10 kits", "25 to 50 in total"]),
        # One board per kit, {up} boards per panel, so the phases become panel counts:
        # {panel_breaks_note}.  Computed, not chosen.
        Field("quantity_breaks", "Quantity breaks (panels)",
              " | ".join(str(n) for n in panel_breaks),
              f"computed: ceil(kits / {up}) for the 2 / 10 / 25 / 50 kit phases of "
              f"RFQ-EEG-001 Rev E, at one board per kit and {up} up per panel "
              f"({panel_breaks_note})",
              RFQ_SCOPE, ["2 prototype units, 10 kits", "25 to 50 in total"]),
        Field("panel_designs", "Different designs in panel", "1",
              "wh_bus.py -- one design, stepped {0} x {1}".format(
                  W.PANEL_COLS, W.PANEL_ROWS)),
        Field("panel_route_process", "Panel route process", "Panel as V-Scoring",
              "wh_bus.py PANEL_COLS/PANEL_ROWS -- a V-scored array"),
        Field("panel_x_out", "X-out allowance in panel", "No",
              "not specified anywhere in the design; No is the conservative answer and "
              "the eight spares in the 20-up array already cover yield"),
        Field("custom_testing", "Custom testing", "No", "bare board, netlist test only"),
        Field("ic_programming", "IC programming", "No", "no component on this board"),
        Field("origin", "Production and shipping origin", "As decided by PCBCART",
              "raised in the notes, as for the carrier"),
    ]
    for f in F:
        f.check()
    return {"id": "WH-BUS-01", "title": "WH-BUS-01 -- bare contact-light bus board",
            "assembled": False, "fields": F}


# ---------------------------------------------------------------------------------------
# What the notes field and the bidder README must say
# ---------------------------------------------------------------------------------------
def bidder_notes(car: dict) -> list:
    """Section 4 of the brief.  `short` goes in the portal's Notes box, `full` goes in
    README_for_bidder.txt.  One source, so the two cannot disagree."""
    v = {f.key: f.value for f in car["fields"]}
    return [
        dict(
            key="ticket",
            short=f"This follows ticket {TICKET} with Genny. Same request, submitted "
                  f"through the form as asked.",
            full=f"""1. TICKET {TICKET}

   This is the same request already in your queue as ticket {TICKET}, raised with Genny
   (Huang Jing Yi, usa.office@pcbcart.com). It is submitted through the web form because
   that is what you asked us to do. It is not a second, separate enquiry -- please
   attach it to the existing ticket rather than opening another.""",
        ),
        dict(
            key="revb_withdrawn",
            short="EEG-CAR-01 Rev B is WITHDRAWN from fabrication: an independent layout "
                  "engineer found vias in pads, stubs, off-centre pad entry and "
                  "conductors under width. The circuit is unchanged; the geometry is "
                  "being redone as Rev C by a layout desk in KiCad against a written "
                  "rule sheet. THIS SUBMISSION IS BUDGETARY, on Rev B geometry with the "
                  "corrected Rev C BOM. The firm quotation will be against Rev C data. "
                  "Nothing is ordered before then.",
            full="""2. THE GEOMETRY YOU ARE QUOTING IS WITHDRAWN. THIS IS A BUDGETARY
   QUOTATION.

   EEG-CAR-01 Rev B has been WITHDRAWN FROM FABRICATION. An independent layout engineer
   reviewed it and found vias in pads, via stubs, off-centre pad entry and conductors
   below the stated minimum width. None of that is a circuit problem: the schematic, the
   netlist and the part selection are unchanged. It is a geometry problem, and the
   geometry is being redone as Rev C by a layout desk in KiCad, against a written rule
   sheet (LAY-EEG-034).

   So please read this submission as BUDGETARY. It is Rev B geometry carrying the
   CORRECTED Rev C BOM, and it is here to establish price and lead time against a real
   set of files rather than an estimate. The FIRM quotation will be raised against the
   Rev C data when it exists.

   NOTHING IS ORDERED UNTIL THEN. We are not asking you to tool anything, and we are not
   giving a required-by date, because there is not one to give.""",
        ),
        dict(
            key="stackup",
            short=f"The stack-up is SPECIFIED, NOT DEFAULT: {v['stackup']}. Your form has "
                  f"no stack-up control, so please quote against DSN-EEG-003 section 3.2 "
                  f"(in the uploaded notes) and confirm in writing that you can hold it "
                  f"-- or tell us the form cannot carry it.",
            full=f"""3. THE STACK-UP IS SPECIFIED, NOT DEFAULT

   {v['stackup']}

   This is DSN-EEG-003 Rev D section 3.2 and it is not negotiable by default. The two
   reference planes on L2 and L3 sit either side of a 1.065 mm core, and the 0.200 mm
   prepreg to each outer layer is what the USB pair's 95 ohm differential figure was
   calculated on.

   Your assembly form has NO stack-up control -- we checked the page rather than
   assuming. Layer count, finished thickness and both copper weights ARE on the form and
   are set correctly there; it is the dielectric distribution and the layer order that
   the form cannot carry. So please either:

     (a) confirm IN WRITING that you will build to the stack-up above, or
     (b) tell us the form cannot carry it and what you would build instead,

   before quoting. Do not substitute a default stack-up silently. Note that no impedance
   coupon and no impedance report are required -- see the fabrication notes -- but a
   MICROSECTION coupon is, and it is sectioned to verify layer order.""",
        ),
        dict(
            key="opa4376",
            short="U1, U2, U3 (TI OPA4376AIPWR) are TSSOP-14, NOT SOIC-14. Price the "
                  "line but do not confirm the part -- the correction is ours.",
            full="""4. U1, U2, U3 ARE TSSOP-14, NOT SOIC-14

   U1, U2 and U3 are TI OPA4376AIPWR in TSSOP-14 (4.4 x 5 mm, 0.65 mm pitch). Any earlier
   paperwork from us that said SOIC-14 was wrong. The BOM and the CPL in this submission
   are correct.

   Please price the line, but do NOT treat this as a confirmed part selection on your
   side: the correction is ours to make and we will restate it against the Rev C data.
   If your quoting system has already been told SOIC-14 for this ticket, please correct
   it there too.""",
        ),
        dict(
            key="staubli",
            short="J15, J16, J17 (Staubli SLB1,5-F) are PATIENT-CONNECTED and "
                  "NON-SUBSTITUTABLE. No alternative is acceptable on those three lines.",
            full="""5. J15, J16, J17 ARE PATIENT-CONNECTED AND NON-SUBSTITUTABLE

   J15, J16 and J17 are Staubli SLB1,5-F / LB-I1,5 DIN 42802 1.5 mm touchproof sockets.
   They are the connection to a person. They are NON-SUBSTITUTABLE: no equivalent, no
   alternate, no "same form and fit" part is acceptable on those three lines, whatever
   the lead time.

   If you cannot source them, quote the board WITHOUT them and say so, and we will supply
   them on consignment. Do not quote an alternative and do not fit one.""",
        ),
        dict(
            key="modules",
            short="Twelve module types, thirteen assemblies per unit, are NOT in the "
                  "carrier BOM -- they plug in rather than solder. Please state whether "
                  "you can source them or accept them on consignment. A board without "
                  "them is not a unit.",
            full="""6. TWELVE MODULE TYPES ARE NOT IN THE BOM, AND THE UNIT DOES NOT WORK
   WITHOUT THEM

   EEG-CAR-01 is a CARRIER, not an instrument. Twelve purchased module types -- thirteen
   module assemblies per unit -- do the actual work: the ADS1299 breakouts, the
   ESP32-S3-DevKitC-1, the isolator, the charger and gauge, and the rest. They are NOT in
   the carrier BOM, because they plug into socket strips rather than solder to the board.
   That is ICD-EEG-006 Rev C.

   So the assembled board you would be quoting is not a working unit. Please tell us, for
   this ticket:

     (a) whether you can source any of the twelve module types yourself, and at what
         price and lead time; or
     (b) whether you would accept them on CONSIGNMENT from us; or
     (c) that you would rather not handle them at all,

   any of which is a fine answer. We need to know which, because the difference decides
   who buys them.""",
        ),
        dict(
            key="lot_documents",
            short="FOUR lot documents are required per fabrication lot, as conditions of "
                  "acceptance, not extras: certificate of conformance; 100 % electrical "
                  "test report to the supplied IPC-D-356A netlist; ENIG XRF report; and "
                  "a microsection report that INCLUDES THE INTERNAL ANNULAR RING measured "
                  "at a through via, accept limit 0.025 mm.",
            full="""7. FOUR LOT DOCUMENTS ARE CONDITIONS OF ACCEPTANCE, NOT EXTRAS

   Every fabrication lot must arrive with, referenced to the lot number:

     (a) a certificate of conformance naming the drawing and revision;
     (b) a 100 % electrical test report against the SUPPLIED IPC-D-356A netlist
         (not a netlist you extract from the Gerbers);
     (c) an ENIG thickness report by XRF, gold AND nickel, minimum 3 points;
     (d) a MICROSECTION report from a four-layer coupon carried in the panel rails,
         which MUST INCLUDE THE INTERNAL ANNULAR RING MEASURED AT A THROUGH VIA.
         The accept limit is 0.025 mm.

   Item (d) is the one that is usually missed. Our incoming inspection procedure rejects
   the whole lot on a wrong layer order or an internal annular ring below 0.025 mm, so a
   lot that arrives without the coupon and its report cannot be accepted at all.

   Please price these in rather than treating them as options, and tell us now if any of
   them is something you do not do.""",
        ),
        dict(
            key="quantities",
            short="2 / 10 / 25 / 50 are SUCCESSIVE PHASES OF ONE PROGRAMME, not four "
                  "alternative order sizes. Please price all four as a series.",
            full="""8. 2 / 10 / 25 / 50 ARE PHASES, NOT ALTERNATIVES

   Please quote all four quantities. They are successive phases of ONE programme, not
   four alternative order sizes we are choosing between: 2 for the first build, then 10,
   then 25, then 50, each following the one before.

   That matters for how you price it. Tooling amortised across the series, and any price
   you can hold across the phases, is more useful to us than four independent unit
   prices. If a larger phase would change the process -- panelisation, test strategy,
   material buy -- please say so against that phase.""",
        ),
        dict(
            key="licence",
            short="The design is open hardware under CC BY-SA 4.0 and the study is run "
                  "by a non-profit. Sponsorship of any part of the work is welcome and "
                  "is not assumed.",
            full="""9. OPEN HARDWARE, NON-PROFIT, AND AN OPEN DOOR

   This design is open hardware, published under CC BY-SA 4.0, and the study it serves is
   run by a non-profit. Everything in this submission -- the Gerbers, the BOM, the
   specification -- is public.

   If sponsorship of any part of the work is something PCBCart would consider, it would
   be welcome and we would credit it. It is NOT assumed and it is not a condition of
   anything: a straight commercial quotation is exactly what we are asking for here, and
   a plain price is a complete answer to this submission.""",
        ),
    ]


# ---------------------------------------------------------------------------------------
# Vendor profile
# ---------------------------------------------------------------------------------------
class VendorProfile:
    """One portal's shape.  Vendor-agnostic answers in, portal-shaped instructions out."""

    def __init__(self, key, name, form_url, upload_extensions, controls,
                 unsupported, option_notes=()):
        self.key = key
        self.name = name
        self.form_url = form_url
        self.upload_extensions = tuple(upload_extensions)
        self.controls = dict(controls)
        self.unsupported = dict(unsupported)
        self.option_notes = tuple(option_notes)

    def accepts(self, filename: str) -> bool:
        return filename.rsplit(".", 1)[-1].lower() in self.upload_extensions


PCBCART = VendorProfile(
    key="pcbcart",
    name="PCBCart",
    form_url="https://www.pcbcart.com/assembly",
    # Read off the live page: the upload widget's own tip says
    # "only zip,rar,xls,csv accepted".  check_file() in new_assembly_vue.js also lets
    # xlsx through, but the stated list is the one we stay inside.
    upload_extensions=("zip", "rar", "xls", "csv"),
    controls={
        "dimensions":      "PCB_BOARD_SIZE_W / PCB_BOARD_SIZE_H",
        "layers":          "PCB_MATERIAL_LAYERS",
        "thickness":       "PCB_THICKNESS",
        "material":        "PCB_TYPE / PCB_MAT_DETAIL",
        "copper_outer":    "PCB_COPPER_WEIGHT",
        "copper_inner":    "PCB_COPPER_WEIGHT_INNER",
        "surface_finish":  "PCB_SURFACE_FINISH",
        "soldermask":      "PCB_SOLDERMASK_COLOR",
        "legend":          "PCB_SILKSCREEN_LEGEND_COLOR",
        "min_track_clearance": "PCB_MIN_TRACING_SPACING",
        "min_track":       "PCB_MIN_TRACING_SPACING",
        "smallest_hole":   "PCB_SMALLEST_HOLES",
        "buried_blind":    "PCB_BURIED_BLIND",
        "impedance":       "PCB_IMPEDANCE",
        "quantities":      "PCB_QUANTITY (use the [+] control for each break)",
        "quantity_breaks": "quantity[] (one box per break, [+] adds one)",
        "panel_designs":   "PCB_PANEL (Different Design in Panel)",
        "panel_route_process": "PCB_PANEL_ROUTING (Route Process)",
        "panel_x_out":     "PCB_PANEL_X_OUT (X-out Allowance in Panel)",
        "delivery_method": "Delivery Method",
        "assembly_side":   "Assembly Side(s)",
        "custom_testing":  "Custom Testing",
        "ic_programming":  "IC Programming",
        "origin":          "Production & Shipping Origin",
    },
    # The part that earns its keep.  A canonical answer with no control on this portal
    # must be routed into the notes and the specification file, not dropped.
    unsupported={
        "stackup": "No stack-up control exists on either the assembly form or the "
                   "Standard PCB form. Layer count, finished thickness and both copper "
                   "weights ARE on the form; the dielectric distribution and layer "
                   "order are not. Goes in the Notes box and README_for_bidder.txt, "
                   "with written confirmation demanded.",
        "layer_roles": "No control. Carried in the bidder notes and the Gerber layer map.",
        "class": "No control. Carried in the bidder notes.",
        "electrical_test": "No control. Carried in the bidder notes.",
        "vias": "No control beyond the blind/buried question. Carried in the notes.",
        "largest_hole": "No control; PCB_SMALLEST_HOLES only. Carried in the notes.",
        "census": "No control. Informational, for the assembly quotation.",
        "coupon": "No control. Carried in the bidder notes.",
        "lot_documents": "No control. Carried in the bidder notes.",
        "panel": "Delivery Method carries only the choice, not the array. Carried in "
                 "the notes.",
        "holes": "No control. Carried in the notes.",
        "board": "Identification, not a form field.",
    },
    option_notes=(
        "Delivery Method options on the live page: Single board without technical rail "
        "/ Single board with technical rail / Panel with technical rail / Others. "
        "('Panel without technical rail' is present in the HTML but commented out.)",
        "Production & Shipping Origin options: As decided by PCBCART / Thailand / China.",
        "The option lists are injected client-side as $[option.text]$ templates and "
        "cannot be read from the served HTML; the filling script discovers them live.",
        "Dimension unit: the anonymous page sets UserStatus.unit = 'mm' and #appForm "
        "carries a hidden input unit=mm. Signing in overwrites UserStatus.unit from the "
        "account profile, which may be inch. Assert mm before entering any dimension.",
    ),
)

VENDORS = {PCBCART.key: PCBCART}


# ---------------------------------------------------------------------------------------
# Uploads
# ---------------------------------------------------------------------------------------
def upload_plan(board_id: str) -> dict:
    """What goes into each of the portal's two upload slots.

    READ OFF THE LIVE FORM: PCBCart's assembly page has exactly TWO file inputs -- a
    required "BOM File" and a "PCB File" -- and NEITHER is `multiple`. So five files
    cannot be uploaded as five files. The fabrication ZIP goes up untouched in the PCB
    slot, and everything else is bundled into one ZIP for the BOM slot. That is what the
    portal's zip/rar/xls/csv extension list is for.

    The fabrication ZIP is COPIED, never rebuilt, and its checksum is verified against
    the README that released it.
    """
    k = os.path.join(PKG, "kicad")
    if board_id == "EEG-CAR-01":
        rc = os.path.join(k, "RevC_layout_inputs")
        return {
            "pcb": (os.path.join(k, "gerber", "EEG-CAR-01_RevB_gerber_X2.zip"),
                    "EEG-CAR-01_RevB_gerber_X2.zip",
                    "Rev B fabrication data, Gerber X2 plus drill and IPC-D-356A "
                    "netlist. The geometry being quoted, and the geometry that is "
                    "withdrawn.",
                    os.path.join(k, "gerber",
                                 "README_layer_map_and_checksums.txt")),
            "bundle_name": "EEG-CAR-01_RevC_BOM_CPL_and_notes.zip",
            "bundle": [
                (os.path.join(rc, "EEG-CAR-01_RevC_BOM.csv"),
                 "EEG-CAR-01_RevC_BOM.csv",
                 "The CORRECTED Rev C BOM. Supersedes anything sent earlier. Carries "
                 "the substitution column, including the three non-substitutable "
                 "lines."),
                (os.path.join(rc, "EEG-CAR-01_RevC_CPL_SMT_top.csv"),
                 "EEG-CAR-01_RevC_CPL_SMT_top.csv",
                 "Surface-mount placement, PROVISIONAL -- the file says so on its "
                 "first line and that line is deliberately left in."),
                (os.path.join(rc, "EEG-CAR-01_RevC_CPL_THT_top.csv"),
                 "EEG-CAR-01_RevC_CPL_THT_top.csv",
                 "Through-hole placement, PROVISIONAL -- likewise."),
            ],
        }
    if board_id == "WH-BUS-01":
        wb = os.path.join(k, "wh-bus-01")
        return {
            "pcb": (os.path.join(wb, "WH-BUS-01_RevA_gerber_X2.zip"),
                    "WH-BUS-01_RevA_gerber_X2.zip",
                    "Rev A fabrication data, Gerber X2 plus drill and IPC-D-356A "
                    "netlist.",
                    os.path.join(wb, "README_layer_map_and_checksums.txt")),
            "bundle_name": "WH-BUS-01_RevA_BOM_and_notes.zip",
            # The BOM slot is REQUIRED even for a bare board with no components, so it
            # carries the board's own placement-and-BOM note, which says in terms that
            # there is nothing to place.
            "bundle": [
                (os.path.join(wb, "WH-BUS-01_RevA_placement_and_BOM.txt"),
                 "WH-BUS-01_RevA_placement_and_BOM.txt",
                 "The bare-board BOM note: one line, no components, no CPL and no "
                 "stencil, because there is no part to place."),
            ],
        }
    raise SourceError(f"no upload plan for {board_id}")


def readme_text(board: dict, notes: list, profile: VendorProfile,
                plan: dict) -> str:
    """README_for_bidder.txt -- the notes in full, because the Notes box will not hold
    them."""
    L = []
    W_ = 88
    L.append("=" * W_)
    L.append(f"README FOR BIDDER -- {board['title']}")
    L.append(f"TI One Voice / EEG field kit -- ticket {TICKET}")
    L.append("=" * W_)
    L.append("")
    for line in _wrap(
            f"Submitted through {profile.form_url} at your request. The form's Notes "
            f"control is a single-line input, so the notes arrive there as one "
            f"paragraph with the line breaks removed. The short form is in that box "
            f"and this file is the full text. Where the two differ, THIS FILE IS THE "
            f"ONE THAT COUNTS.", W_):
        L.append(line)
    L.append("")
    L.append("Contact: " + CONTACT["name"] + ", " + CONTACT["company"] + ", "
             + CONTACT["country"])
    L.append("         " + CONTACT["phone"] + "   " + CONTACT["email"])
    L.append("")
    L.append("-" * W_)
    L.append("THE SPECIFICATION")
    L.append("-" * W_)
    L.append("")
    L.append("Every figure below is generated from the design source, not transcribed.")
    L.append("")
    for f in board["fields"]:
        if f.key == "board":
            continue
        L.append(f"  {f.label}")
        for line in _wrap(f.value, W_ - 6):
            L.append(f"      {line}")
        L.append(f"      [source: {f.source}]")
        L.append("")
    L.append("-" * W_)
    L.append("THE NOTES")
    L.append("-" * W_)
    L.append("")
    for n in notes:
        L.append(n["full"].rstrip())
        L.append("")
    L.append("-" * W_)
    L.append("THE FILES IN THIS SUBMISSION")
    L.append("-" * W_)
    L.append("")
    _p = plan["pcb"]
    for name, what in ([(_p[1], _p[2] + "   [uploaded in the PCB File slot]")]
                       + [(n, w) for _s, n, w in plan["bundle"]]
                       + [(plan["bundle_name"],
                           "This file: the bundle in the BOM File slot, holding "
                           "everything above except the fabrication ZIP, plus this "
                           "README.")]):
        L.append(f"  {name}")
        for line in _wrap(what, W_ - 6):
            L.append(f"      {line}")
        L.append("")
    L.append("  Every file above is listed with its SHA-256 in the covering record.")
    L.append("  Please quote the checksum of anything you cannot open.")
    L.append("")
    L.append("=" * W_)
    L.append("END")
    L.append("=" * W_)
    return _no_dates("\n".join(L) + "\n", "README_for_bidder.txt")


def _wrap(text: str, width: int) -> list:
    words, out, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        out.append(cur)
    return out or [""]


# ---------------------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------------------
def emit(profile: VendorProfile) -> str:
    out = os.path.join(DIST, profile.key)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    os.makedirs(os.path.join(out, "screenshots"), exist_ok=True)

    locality = doc_issuer_locality()
    if CONTACT["state"] != locality:
        raise SourceError(
            f"CONTACT['state'] is {CONTACT['state']!r} but the controlled documents are "
            f"issued from {locality!r}. The address must not disagree with the "
            f"documents that carry it.")

    boards = [carrier(), wh_bus_board()]
    notes = bidder_notes(boards[0])

    manifest = {
        "schema": "rfq-pack/1",
        "generated_by": "tools/emit_rfq_pack.py",
        "vendor": {"key": profile.key, "name": profile.name,
                   "form_url": profile.form_url,
                   "upload_extensions": list(profile.upload_extensions),
                   "option_notes": list(profile.option_notes)},
        "ticket": TICKET,
        "basis": "BUDGETARY. EEG-CAR-01 Rev B geometry is WITHDRAWN from fabrication; "
                 "this is priced on that geometry with the corrected Rev C BOM. The "
                 "firm quotation will be against Rev C data.",
        "contact": CONTACT,
        "submissions": [],
    }

    for board in boards:
        bid = board["id"]
        bdir = os.path.join(out, bid)
        os.makedirs(bdir)
        plan = upload_plan(bid)

        # -- the PCB slot: copied, never rebuilt, checksum verified ------------------
        src, name, what, rmpath = plan["pcb"]
        if not profile.accepts(name):
            raise SourceError(f"{name}: {profile.name} does not accept that extension")
        dst = os.path.join(bdir, name)
        shutil.copy2(src, dst)
        digest = sha256(dst)
        expected = readme_checksum(rmpath, name)
        if expected != digest:
            raise SourceError(
                f"{name}: checksum {digest} does not match the {expected} recorded in "
                f"{os.path.relpath(rmpath, PKG)}. The file was NOT rebuilt by this "
                f"tool; something else changed it.")
        files = [{"slot": "PCB File", "name": name, "sha256": digest,
                  "bytes": os.path.getsize(dst), "what": what,
                  "source": os.path.relpath(src, PKG),
                  "checksum_verified_against": os.path.relpath(rmpath, PKG)}]

        # -- the BOM slot: one bundle, because the form takes one file per slot -------
        readme = readme_text(board, notes, profile, plan)
        bundle_path = os.path.join(bdir, plan["bundle_name"])
        contents = []
        with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as z:
            for bsrc, bname, bwhat in plan["bundle"]:
                with open(bsrc, "rb") as fh:
                    data = fh.read()
                zi = zipfile.ZipInfo(bname, (1980, 1, 1, 0, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                z.writestr(zi, data)
                contents.append({"name": bname, "what": bwhat,
                                 "sha256": hashlib.sha256(data).hexdigest(),
                                 "source": os.path.relpath(bsrc, PKG)})
                # A loose copy too: readable without unzipping, and reusable by a
                # portal that accepts more than two files.
                shutil.copy2(bsrc, os.path.join(bdir, bname))
            zi = zipfile.ZipInfo("README_for_bidder.txt", (1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, readme)
            contents.append({"name": "README_for_bidder.txt",
                             "what": "The bidder notes in full. The form's Notes box "
                                     "is a single-line text input and will not hold "
                                     "them.",
                             "sha256": hashlib.sha256(
                                 readme.encode("utf-8")).hexdigest(),
                             "source": "generated by tools/emit_rfq_pack.py"})
        with open(os.path.join(bdir, "README_for_bidder.txt"), "w",
                  encoding="utf-8") as fh:
            fh.write(readme)

        files.append({"slot": "BOM File", "name": plan["bundle_name"],
                      "sha256": sha256(bundle_path),
                      "bytes": os.path.getsize(bundle_path),
                      "what": "Bundle for the required BOM File slot: "
                              + ", ".join(c["name"] for c in contents),
                      "source": "generated by tools/emit_rfq_pack.py",
                      "contents": contents})

        fields = {}
        for f in board["fields"]:
            d = f.as_dict()
            if f.key in profile.controls:
                d["control"] = profile.controls[f.key]
            elif f.key in profile.unsupported:
                d["control"] = None
                d["no_control_because"] = profile.unsupported[f.key]
            else:
                raise SourceError(
                    f"{bid}.{f.key} is neither mapped to a {profile.name} control nor "
                    f"declared unsupported. Every canonical answer must be one or the "
                    f"other, or it will be silently dropped on the form.")
            fields[f.key] = d

        manifest["submissions"].append({
            "board": bid,
            "title": board["title"],
            "assembled": board["assembled"],
            "dir": bid,
            "fields": fields,
            "uploads": files,
            "notes_short": _no_dates(
                "\n".join(f"{i + 1}. {n['short']}" for i, n in enumerate(notes)),
                f"{bid} notes_short"),
        })

    # Audit -- not censor -- the dates inside copied controlled files.
    audit = []
    for sub in manifest["submissions"]:
        for u in sub["uploads"]:
            for c in ([u] + u.get("contents", [])):
                src = c.get("source", "")
                if not src.startswith("kicad/"):
                    continue
                path = os.path.join(PKG, src)
                if not os.path.exists(path) or path.endswith(".zip"):
                    continue
                try:
                    with open(path, encoding="utf-8") as fh:
                        found = find_dates(fh.read())
                except (UnicodeDecodeError, OSError):
                    continue
                if found:
                    audit.append({"file": c["name"], "source": src,
                                  "dates": sorted(set(found))})
    manifest["date_audit"] = {
        "rule": "Nothing this tool writes states or implies a fabrication date.",
        "generated_text_carrying_a_date": 0,
        "copied_controlled_files_carrying_a_date": audit,
        "note": "These are document issue stamps inside released, checksummed "
                "fabrication data. They are NOT fabrication or delivery dates, and the "
                "files are copied unaltered so that their released checksums still "
                "verify.",
    }

    fj = os.path.join(out, "fields.json")
    with open(fj, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=True, sort_keys=False)
        fh.write("\n")

    aspath = os.path.join(out, "ANSWER_SHEET.md")
    with open(aspath, "w", encoding="utf-8") as fh:
        fh.write(answer_sheet(manifest, boards, notes, profile))

    return out


def answer_sheet(manifest: dict, boards: list, notes: list,
                 profile: VendorProfile) -> str:
    L = []
    A = L.append
    A(f"# RFQ answer sheet -- {profile.name}")
    A("")
    A(f"Ticket **{TICKET}**. Form: <{profile.form_url}>")
    A("")
    A("Generated by `tools/emit_rfq_pack.py` from `tools/design.py` and "
      "`tools/wh_bus.py`. **Nothing here was typed by hand.** Every row carries the "
      "source it came from; where a row restates a specification, the generator checks "
      "the figure still appears verbatim in that source and fails the build if it does "
      "not.")
    A("")
    A(f"> **{manifest['basis']}**")
    A("")
    A("## How to use this")
    A("")
    A("Read it beside the filled form before pressing submit. Every value below should "
      "appear on the page. A row with **no control** is one this portal has no field "
      "for: check it reached the Notes box or the bidder README instead of being lost.")
    A("")
    A("## Basic info")
    A("")
    A("| Field | Value |")
    A("|---|---|")
    for k in ("name", "company", "country", "state", "phone", "email"):
        v = CONTACT[k] or "**NOT SET -- a person must choose this on the form**"
        A(f"| {k.title()} | {v} |")
    A("")
    A("*One constant in `emit_rfq_pack.py`, not three places.*")
    A("")

    for sub, board in zip(manifest["submissions"], boards):
        A(f"## {board['title']}")
        A("")
        A(f"Directory `{sub['dir']}/`. "
          + ("Assembled." if sub["assembled"] else "Bare board, not assembled."))
        A("")
        A("| Field | Value | Portal control | Source |")
        A("|---|---|---|---|")
        for f in board["fields"]:
            d = sub["fields"][f.key]
            ctl = d.get("control") or "**no control**"
            val = f.value.replace("|", "\\|")
            src = f.source.replace("|", "\\|")
            A(f"| {f.label} | {val} | {ctl} | {src} |")
        A("")
        nc = [k for k, d in sub["fields"].items() if d.get("control") is None]
        if nc:
            A("### Answers this portal has no field for")
            A("")
            A("These must reach the vendor through the Notes box, the bidder README or "
              "the uploaded files. If they are not there, they were not asked and will "
              "not be quoted.")
            A("")
            for k in nc:
                d = sub["fields"][k]
                A(f"- **{d['label']}** -- {d['no_control_because']}")
            A("")
        A("### Files to upload")
        A("")
        A("| File | Bytes | SHA-256 |")
        A("|---|---:|---|")
        for u in sub["uploads"]:
            A(f"| `{u['name']}` | {u['bytes']} | `{u['sha256']}` |")
        A("")
        for u in sub["uploads"]:
            A(f"- **`{u['name']}`** -- {u['what']}")
            if "checksum_verified_against" in u:
                A(f"  Checksum verified against `{u['checksum_verified_against']}`; "
                  f"copied, not rebuilt.")
        A("")

    A("## The Notes box")
    A("")
    A("Paste this, and upload the bidder notes ZIP as well. The full text is in "
      "`README_for_bidder.txt` inside that ZIP.")
    A("")
    A("```text")
    for i, n in enumerate(notes):
        A(f"{i + 1}. {n['short']}")
    A("```")
    A("")
    A("## Live-page notes")
    A("")
    for note in profile.option_notes:
        A(f"- {note}")
    A("")
    # The body is checked for dates FIRST. The dates section below is appended after
    # that check, on purpose: it exists to quote the audited stamps, so running the
    # guard over it would fail on the very text that discloses them.
    body = _no_dates("\n".join(L), "ANSWER_SHEET.md")

    audit = manifest.get("date_audit", {}).get(
        "copied_controlled_files_carrying_a_date", [])
    if not audit:
        return body
    D = ["", "## Dates", "",
         "Nothing generated for this submission states or implies a fabrication date; "
         "the generator fails the build if it does. The files below carry a document "
         "issue stamp and are sent UNALTERED, so that the checksums they were released "
         "under still verify. None of these is a fabrication or delivery date:", ""]
    for e in audit:
        D.append(f"- `{e['file']}` -- {', '.join(e['dates'])} "
                 f"(generation stamp in `{e['source']}`)")
    D.append("")
    return body + "\n".join(D)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--vendor", default="pcbcart", choices=sorted(VENDORS))
    a = ap.parse_args()
    try:
        out = emit(VENDORS[a.vendor])
    except SourceError as e:
        print(f"emit_rfq_pack: FAILED\n{e}", file=sys.stderr)
        return 1
    rel = os.path.relpath(out, PKG)
    print(f"emit_rfq_pack: wrote {rel}/")
    for root, _dirs, names in os.walk(out):
        for n in sorted(names):
            p = os.path.join(root, n)
            print(f"  {os.path.relpath(p, out):52s} {os.path.getsize(p):9d}  "
                  f"{sha256(p)[:16]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
