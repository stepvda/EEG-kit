#!/usr/bin/env python3
"""
mech_gen.py -- parametric mechanical parts for the EEG field kit, package v2.

Rev A of the package supplied five STL meshes and one DXF. An STL cannot be dimensioned,
so a print bureau could quote from it but a machinist, an inspector or anyone checking a
fit could not work from it at all. Every part modelled here is exported as **STEP** (for
dimensioning, fit checks and inspection) and as **STL** (for MJF printing), from one
parametric definition, so the two can never disagree.

Parts modelled here:
    MP-01   module mounting plate  (new in v2 -- the modules do not plug into the carrier)
    POD-P1  prototype enclosure base and lid, with the panel openings of RFQ M-02
    HM-04   electrode assembly body, with the gel port, spring seat and bayonet slot
    HM-08   battery hatch, quarter-turn  (was called HM-07 in Rev A -- see PARTS-EEG-019)
    HM-09   service key for the cup bayonet
    HM-02   TPU comfort pads
    FIT-01  fit-test coupon carrying the three critical fits
    CASE-00 foam insert, both layers, as DXF
    WH-KEY-01 printed keying shroud over J14, J30 and J22 (WH-EEG-008 section 6)
    WH-ADP   printed panel adapters -02, -03 and -04 (WH-EEG-008 section 3.9)
    HM-12   occipital umbilical entry plate, the OE-1 and OE-2 entries of WH-EEG-008
            section 7 (identifier proposed, not yet issued -- see oe_entry_plate())

HM-01, the helmet frame, is carried over from Rev A as a watertight STL. It is a rendered
form study rather than a parametric model, and its geometry will change once the Stage 0 fit
measurement of DSN-EEG-002 section 12 objection 3 is done, so a STEP model of it is a Phase 1
deliverable and is listed as such in PARTS-EEG-019.

Two things that were missing in Rev A are done here rather than downstream:

  * the **PARTS-EEG-019 section 4.1 marking** is cut into every part with a face big enough
    to hold it, so the identifier and revision letter are in the released STEP and STL and
    the MECH-EEG-020 sheets can claim the feature. HM-04, HM-02A and FIT-01 are exempt --
    too small or too soft to hold a legible engraving -- and say so on their sheets;
  * **`mech/MANIFEST.json` is written here**, by `build()`, with the SHA-256, revision,
    material, process and units of every released mechanical file, the two CASE-00 DXFs and
    the STEP files included. There is one manifest generator and one schema.

`build()` also writes two Markdown files into `mech/`, from the same constants that cut the
geometry, so that neither can drift away from the model it describes:

  * **`mech/HARDWARE_SCHEDULE.md`** -- every insert, screw, standoff and gland the released
    geometry actually needs, per pod and per helmet, with the size and length of each one
    derived from the bore or boss it goes into. The sizes are derived and are stated as
    such; the vendor part behind each line is a purchasing choice and is marked OPEN WITH
    CRITERIA in the AVL-EEG-017 sense, because no fastener datasheet is in this package.
  * **`mech/MECH_RELEASE_STATUS.md`** -- one row per part this file releases, against what
    the registers currently record, because eight parts that now have geometry are still
    carried as "to be created" in PARTS-EEG-019 and are outside the AVL-EEG-017 K24 print
    set that the MJF bureau is quoted against.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
import re

import cadquery as cq

import design as D

# carrier mounting pattern, shared by MP-01 and POD-P1
MH = [(5.0, 5.0), (145.0, 5.0), (5.0, 125.0), (145.0, 125.0)]
BW, BH = D.BOARD_W, D.BOARD_H


def _c(x, y):
    """Carrier coordinates (top-left origin, Y down) to part coordinates (centred)."""
    return (x - BW / 2.0, BH / 2.0 - y)


# --------------------------------------------------------------------------- marking
# PARTS-EEG-019 section 4.1: the identifier and its revision letter are modelled into the
# part, recessed at least 0.4 mm with a stroke of at least 0.6 mm, because a printed label
# does not survive the 70 % IPA wipe of SVC-EEG-013.  HM-04, HM-02A and FIT-01 are exempt
# -- too small or too soft to hold a legible engraving -- and are identified by the bag
# label at kitting.  A part is in scope when it has a flat face that will hold the mark.
MARKING = {
    "MP-01_module_plate":              ("MP-01 B",     5.0),
    "POD-P1_prototype_enclosure_base": ("POD-P1-01 B", 6.0),
    "POD-P1_prototype_enclosure_lid":  ("POD-P1-02 B", 6.0),
    "HM-08_battery_hatch":             ("HM-08 B",     5.0),
    "HM-09_service_key":               ("HM-09 A",     4.0),
    "HM-10_keyed_cell_carrier":        ("HM-10 A",     5.0),
    "HM-03A_occipital_yoke":           ("HM-03A A",    5.0),
}
ENGRAVE_FONT = "DejaVu Sans"    # present wherever matplotlib is, and on mainstream Linux
ENGRAVE_DEPTH = 0.4             # PARTS-EEG-019 section 4.1 minimum
STROKE_PER_EM = 0.1447          # DejaVu Sans Bold stem width, as a fraction of the em size


def _face(origin, normal=(0.0, 0.0, 1.0), xdir=(1.0, 0.0, 0.0)):
    """A plane on the nominated face, in part coordinates.  `normal` points out of the
    material, so `_engrave` always cuts inwards and the text reads the right way round
    when the face is looked at."""
    return cq.Plane(origin=cq.Vector(*origin), xDir=cq.Vector(*xdir),
                    normal=cq.Vector(*normal))


def _engrave(part, txt, plane, size=5.0, depth=ENGRAVE_DEPTH):
    """Cut `txt` into `plane` to `depth`, and return the marked part.

    The stroke follows the font size: DejaVu Sans Bold is 0.1447 em wide in the stem, so
    5.0 mm text is a 0.72 mm stroke and 4.0 mm text is 0.58 mm.  Sizes are chosen per part
    in MARKING against the face that has to hold the mark; where the face forces a stroke
    below the section 4.1 minimum the MECH-EEG-020 sheet says so rather than implying the
    rule is met.
    """
    glyphs = cq.Workplane(plane).text(txt, size, -depth, combine=False,
                                      font=ENGRAVE_FONT, kind="bold")
    return part.cut(glyphs)


# --------------------------------------------------------------------------- MP-01
def mp01():
    """MP-01 module mounting plate.

    It exists because no public standard fixes the header geometry of a PIEEG-8, an ES8388
    breakout or a bq24074 module, so a socket drawn at a chosen coordinate on the carrier is
    a guess.  The modules bolt to this plate instead and reach the carrier through keyed
    2.54 mm ribbon jumpers (ICD-EEG-006).

    The plate is a perforated frame: an 8 mm solid border, a field of 12 x 3 mm jumper slots
    on a 16 x 7 mm grid, M2.5 clearance holes between the slot rows for module fixings, and
    one large opening for the ESP32-S3-DevKitC-1, which is inserted directly into J6 and J7
    and stands proud of the carrier.
    """
    t = 3.0
    pw, ph = BW - 4.0, BH - 4.0
    p = cq.Workplane("XY").box(pw, ph, t, centered=(True, True, False))
    p = p.edges("|Z").fillet(4.0)

    # four M3 clearance holes on the carrier pattern
    for x, y in MH:
        cx, cy = _c(x, y)
        p = p.cut(cq.Workplane("XY", origin=(cx, cy, -1)).circle(1.7).extrude(t + 2))

    # opening for the DevKit, which is taller than every other module
    d0, d1 = _c(78.0, 4.0), _c(109.0, 65.0)
    p = p.cut(cq.Workplane("XY",
                           origin=((d0[0] + d1[0]) / 2, (d0[1] + d1[1]) / 2, -1))
              .rect(abs(d1[0] - d0[0]), abs(d1[1] - d0[1])).extrude(t + 2))

    def clear(cx, cy, r=6.0):
        if not (10.0 < cx < BW - 10.0 and 10.0 < cy < BH - 10.0):
            return False
        if 74.0 < cx < 113.0 and 0.0 < cy < 69.0:               # DevKit opening + margin
            return False
        return all((cx - mx) ** 2 + (cy - my) ** 2 > 64.0 for mx, my in MH)

    slots, holes = [], []
    for gy in range(0, 22):
        cy = 12.0 + gy * 7.0
        for gx in range(0, 14):
            cx = 14.0 + gx * 16.0
            if clear(cx, cy):
                slots.append(_c(cx, cy))
            hx = cx + 8.0
            if clear(hx, cy + 3.5):
                holes.append(_c(hx, cy + 3.5))
    for sx, sy in slots:
        p = p.cut(cq.Workplane("XY", origin=(sx, sy, -1)).slot2D(12.0, 3.0, 0)
                  .extrude(t + 2))
    for hx, hy in holes:
        p = p.cut(cq.Workplane("XY", origin=(hx, hy, -1)).circle(1.35).extrude(t + 2))
    # section 4.1 mark, in the 8 mm border below the slot field and clear of the two
    # lower M3 holes at part (-70, -60) and (70, -60)
    txt, size = MARKING["MP-01_module_plate"]
    p = _engrave(p, txt, _face((0.0, -58.0, t)), size)
    return p


# --------------------------------------------------------------------------- POD-P1
POD_PANEL_MIN_GAP = 2.0     # material between two openings on a WALL
POD_LID_MIN_GAP = 1.5       # ...and on the lid, where the pitch is the carrier's and the
                            # cap size is RFQ E-26's, so neither is free to move

# The three buttons are on the LID, not on a side wall.
#
# pod_base() sends every PANEL entry to a short wall, choosing the side by whether x is
# below or above BW/2.  The buttons sit at x = 102, so all three went to the RIGHT wall --
# 48 mm from where the button actually is on the carrier, so the hole lined up with
# nothing, and 13 mm across, so they cut straight through the headphone, charge, boom and
# room-microphone openings that share that wall.  Seven openings in 60 mm of wall, four of
# them merged.  A button is pressed from above on a pod lying on a table; it belongs in the
# lid, which had no openings at all.
POD_LID_MOUNTED = {"BTN_A", "BTN_B", "BTN_STOP"}
PANEL = [
    # (name, x from the board origin, y, shape, size).  Left-wall parts have x < BW/2.
    ("EMG1 DIN 42802", 8.0, 76.0, "circle", 8.2),
    ("EMG2 DIN 42802", 8.0, 88.0, "circle", 8.2),
    ("EMG3 DIN 42802", 8.0, 100.0, "circle", 8.2),
    # Right-wall spacing, re-laid 2 September 2026.
    #
    # The headphone opening spanned y 68.75..75.25 and the charge USB-C 75.00..85.00: they
    # OVERLAPPED by 0.2 mm, so pod_base() cut them as one merged hole with no material
    # between a 3.5 mm jack and a USB-C receptacle.  Nothing checked, because each opening
    # was placed correctly on its own and no rule compared them to each other.
    #
    # These are PANEL positions, not board positions.  Both connectors reach their walls on
    # pigtails -- WH-04 for the headphone, WH-07 for the charge port -- so the opening can
    # move along the wall without moving anything on the carrier.  Re-spaced to leave at
    # least 2.0 mm of wall between every pair; POD_PANEL_MIN_GAP below is the rule and
    # simulate_production.py enforces it.
    ("headphone 3.5 mm", 128.0, 71.0, "circle", 6.5),
    ("boom microphone TRRS", 122.0, 92.0, "circle", 6.5),
    ("room microphone port", 122.0, 102.0, "circle", 4.0),
    ("data USB-C (isolator module)", 146.0, 12.0, "rect", (10.0, 4.0)),
    ("charge USB-C", 143.0, 81.5, "rect", (10.0, 4.0)),
    ("microSD", 136.0, 58.0, "rect", (13.0, 3.0)),
    # 12.4 mm, not 13.0.  The three buttons sit on 14.0 mm centres fixed by the carrier, so
    # a 13.0 mm opening leaves 1.0 mm of lid between neighbours -- thinner than the 1.20 mm
    # minimum printed wall used everywhere else in this design, in a 3.0 mm plate that is
    # pressed on.  12.4 mm is the smallest opening that still clears the 12 mm cap RFQ E-26
    # specifies (0.2 mm radial), and it leaves a 1.60 mm web.  A first cut at 12.0 mm was
    # wrong: it would have met the wall rule by making the cap not fit.
    ("BTN_A", 102.0, 76.0, "circle", 12.4),
    ("BTN_B", 102.0, 90.0, "circle", 12.4),
    ("BTN_STOP", 102.0, 104.0, "circle", 12.4),
]

# --- POD-P1 principal dimensions, in one place, so the base and the lid cannot drift ---
# These are the Rev B figures already published in ASM-EEG-007 section 5.1 and WH-EEG-008
# section 6 -- 163.0 x 143.0 x 58.0 external, 158.0 x 138.0 x 55.5 internal, 2.5 mm walls,
# a 4.0 mm lid with a 2.0 mm spigot.  Nothing added below changes the envelope or the
# ICD-EEG-006 section 4 stack budget.
POD_WALL = 2.5
POD_IW, POD_IH = 158.0, 138.0
POD_OW, POD_OH = POD_IW + 2 * POD_WALL, POD_IH + 2 * POD_WALL      # 163.0 x 143.0
POD_DEPTH = 58.0                    # external, outside of the floor to the rim
POD_LID_T = 4.0                     # lid plate
POD_SPIGOT_T = 2.0                  # lid spigot, the part that enters the cavity
POD_FLOOR_BOSS_H = 6.0              # carrier boss, ICD-EEG-006 section 4 stack budget
POD_FLOOR_BOSS_D = 8.0              # as ASM-EEG-007 section 5.1 item 1 states it

# The heights the stack reaches inside the pod, from the same budget, used below to keep
# every new feature off the electronics: 2.5 floor + 6.0 boss = 8.5 to the underside of the
# carrier, + 1.6 board = 10.1 to its top, + 18.0 standoff = 28.1 to the underside of MP-01,
# + 3.0 plate = 31.1, and the tallest module tops out at 49.1.
Z_CARRIER_TOP = POD_WALL + POD_FLOOR_BOSS_H + 1.6                  # 10.1
Z_PLATE_UNDER = Z_CARRIER_TOP + 18.0                               # 28.1
Z_STACK_TOP = 49.1

# --- the four lid fixings ---------------------------------------------------------------
# ONE definition of the pattern.  pod_lid() drills its clearance holes on these points and
# pod_base() puts a boss under the same points, so the fault that shipped in Rev B -- four
# D3.4 holes in the lid with nothing under any of them, the lid unfastenable -- cannot come
# back by editing one function and not the other.
LID_FIX = [(sx * (POD_OW / 2 - 6.0), sy * (POD_OH / 2 - 6.0))
           for sx in (-1.0, 1.0) for sy in (-1.0, 1.0)]            # (+/-75.5, +/-65.5)
LID_HOLE_D = 3.4                    # M3 clearance through the lid
LID_BOSS_D = 8.0
# Boss top 0.2 mm below the spigot face.  The lid seats on the rim, on the 1.5 mm silicone
# cord in the 1.2 mm groove, and that is what sets the 20 % compression of ASM-EEG-007 5.1
# item 2; a boss printed even slightly proud would hold the lid off its own seal, so the
# boss is deliberately short of it and takes the screw, not the load.
LID_BOSS_TOP = POD_DEPTH - POD_SPIGOT_T - 0.2                      # 55.8
# The boss hangs from the rim rather than standing on the floor, and the reason is the
# 4.0 mm gap: the cavity is 158 x 138 around a 150 x 130 carrier with square corners
# (DSN-EEG-003 section 3, "board outline 150.0 x 130.0 mm, rectangular"), so there is
# nowhere beside the board for a D8 boss and the corner is the only place one fits at all.
# It starts at 44.0, below the fixing but above nothing that is in the way: the tallest
# module reaches 49.1 and does so inside the MP-01 outline, whose filleted corner is
# 1.19 mm clear of the D8 boss at (+/-75.5, +/-65.5).  A corner column carries it down to
# the floor so the boss is integral with two walls over its whole height.
LID_BOSS_BOTTOM = 44.0
LID_COL_IN = 2.5                    # column inner faces, inboard of each INNER wall face:
                                    # 79.0 - 2.5 = 76.5 and 69.0 - 2.5 = 66.5, which is
                                    # 1.5 mm clear of the carrier corner at (75, 65)

# --- M3 threads in POD-P1 ---------------------------------------------------------------
# They are brass heat-set inserts, not thread-formed PA12 pilots, and that is a decision,
# not a preference.  ASM-EEG-007 section 3.3 states that an M3 thread strips above about
# 0.5 N.m in this material class; section 5.1 then torques the lid screws and the carrier
# fixing to 0.60 N.m.  A thread formed straight into PA12, which is what the Rev B D2.5
# pilot asks for, is being asked to hold more than it holds.  The bore is modelled at
# 4.0 mm, the hole a standard brass M3 insert (4.6 mm OD, 5.7 mm long) wants; the exact
# figure is the insert maker's and is settled at first article.  Printing the bore also
# closes ASM-EEG-007 5.1 item 1 the other way: there is no drilling operation, because the
# part comes off the machine with the insert bore already in it.
INSERT_BORE_D = 4.0
INSERT_LEADIN_D = 5.0
INSERT_LEADIN_T = 0.5
FLOOR_INSERT_DEPTH = 5.5            # in a 6.0 mm boss on a 2.5 mm floor: 3.0 mm under it
LID_INSERT_DEPTH = 7.0              # 5.7 mm insert + 1.3 mm for the screw to run past it

# --- harness entry ----------------------------------------------------------------------
# Rev B had none at all: ASM-EEG-007 5.1 item 3 records that the twelve-way electrode cable
# and the ten-way light cable have to reach J14 and J30 inside a gasketed pod and that
# mech_gen.py generated no aperture, gland or strain relief for either.  Two entries, not
# one: RISK-EEG-011 H-05 and SF-9 exclude "an LED conductor contacts an electrode
# conductor" as not credible on the strength of two separate cables in two separate glands
# with separate internal channels, and a shared entry would put that exclusion back in play.
#
# Each entry sits on the wall nearest its own connector, with its axis on the connector's
# own coordinate, read from the ICD-EEG-006 Rev B section 3 connector table.
J14_XY = _c(5.0, 12.0)              # WH-01, 12-way screened  -> part (-70.0,  53.0)
J30_XY = _c(66.0, 90.0)             # WH-02, 10-way lights    -> part ( -9.0, -25.0)
# The axis height is the harness layer, and it is the same for both: the carrier top is at
# 10.1 and the underside of MP-01 at 28.1, so a D12.5 bore centred at 21.0 spans 14.75 to
# 27.25 and touches neither.  It also matches where the cable leaves a 2.54 mm crimp
# housing sitting on J14, about 20 mm above the floor -- a catalogue height for a 12-way
# housing, not a part anyone here has measured.
ENTRY_Z = 21.0
# D12.5 through a 3.5 mm panel is the hole for an M12 x 1.5 gland with a 3.0 to 6.5 mm
# clamping range -- the SKINTOP ST-M12x1.5 that SVC-EEG-013 already names, or equivalent --
# which brackets the WH-01 jacket at 4.3 nom / 4.6 max mm and the WH-02 jacket at 4.5 mm
# (WH-EEG-008 section 4).  This is NOT the withdrawn WH-08 host gland: the host connection
# stays a socket behind the panel aperture at (146, 12).  The gland's thread length and
# locknut height have not been read off a datasheet, so the panel is held at 3.5 mm, in the
# middle of the 1 to 6 mm range glands of this class quote, and the first article checks it.
ENTRY_BORE_D = 12.5
ENTRY_PAD_D = 22.0                  # flat seat inside, over the locknut's corners
ENTRY_PAD_T = 1.0                   # 2.5 wall + 1.0 pad = 3.5 mm of panel at the entry
# The gland class as named values rather than as prose, because the same gland is fitted at
# the helmet end of both umbilicals (oe_entry_plate() below) and because HARDWARE_SCHEDULE.md
# is generated from these figures.  Every one of them is a REQUIREMENT ON THE PART TO BE
# BOUGHT and not a measurement of one: there is no gland datasheet anywhere in this package,
# and the across-flats figure in particular is an assumption that sets ENTRY_PAD_D and has
# to be checked against whatever gland is actually approved.
GLAND_THREAD = "M12 x 1.5"
GLAND_CLAMP_MIN, GLAND_CLAMP_MAX = 3.0, 6.5     # jacket range the two cables need covered
GLAND_PANEL_MIN, GLAND_PANEL_MAX = 1.0, 6.0     # panel thickness the gland must accept
GLAND_LOCKNUT_AF = 17.0                         # assumed across flats; sets ENTRY_PAD_D
WH01_JACKET_MAX = 4.60              # WH-EEG-008 section 4: TPU, 4.30 nom, 4.60 max
WH02_JACKET_NOM = 4.50              # WH-EEG-008 section 4: TPU, 4.50 nom
# WH-EEG-008 section 6 clips each helmet cable "to a POD-P1 boss" with a printed P-clip,
# and POD-P1-04 in this file is that clip; its own docstring records that the boss it screws
# to did not exist.  One per entry, on the same pad as the gland -- the pad is drawn as an
# obround reaching from the gland axis to the clip boss, so the two are one raised feature
# and not two with a sliver of wall between them.  D8.0 with a 2.5 mm hole is what POD-P1-04
# is drawn to sit on.  The boss stands 5.0 mm off the wall, which stops it 1.0 mm short of
# the MP-01 outline, and 16.0 mm off the gland axis, which leaves 2.2 mm between its D8 body
# and the corner of a 17 mm across-flats locknut -- a size assumed from the gland class and
# not off a datasheet.
#
# What this boss can and cannot do, stated rather than implied.  POD-P1-04 puts its D3.4
# fixing hole 10.0 mm from the cable it holds and its foot 3.0 mm thick, so the clipped
# cable runs parallel to the wall, 9.0 mm off it, on a 10.0 mm radius about the boss axis:
# turned away from the gland that is 26.0 mm from the gland axis, and the cable makes its
# quarter turn over 26 mm against a 13 mm static bend radius.  It anchors the service loop.
# It is NOT the "40 mm behind its housing" of WH-EEG-008 section 6: with the gland 9 mm from
# J14, that point is outside the pod.  The gland is the primary strain relief here and the
# clip is secondary, which is the reverse of what section 6 assumes and has to be reconciled
# there.  Its pilot is a 2.5 mm thread-forming hole, not an insert bore: a P-clip screw is a
# hand-tight cable retainer at about 0.3 N.m, fitted once, and is the one threaded joint in
# this part that stays under the strip limit of ASM-EEG-007 section 3.3 without an insert.
CLIP_BOSS_D = 8.0
CLIP_BOSS_H = 5.0
CLIP_PILOT_D = 2.5
CLIP_PILOT_DEPTH = 5.5              # 5.0 boss + 2.5 wall = 7.5, so 2.0 mm is left outboard
HARNESS = [
    # (cable, connector, point on the inner wall face, inward normal, along-wall direction,
    #  P-clip offset along that direction -- always away from the corner column)
    ("WH-01 12-way screened electrode cable", "J14",
     (-POD_IW / 2.0, J14_XY[1], ENTRY_Z), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), -16.0),
    ("WH-02 10-way contact-light cable", "J30",
     (J30_XY[0], -POD_IH / 2.0, ENTRY_Z), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), 16.0),
]


def _pod_holds():
    """The clearances the POD-P1 features above are placed on, checked rather than trusted.

    Every one of them is a distance to a part that exists in this file or in design.py, so
    if the carrier grows, the plate outline changes or the stack budget moves, this fails at
    import instead of printing a pod that cannot be closed.  It is the same reason
    foam_dxf() checks its own bay schedule.
    """
    # carrier and plate, in part coordinates
    cx, cy = BW / 2.0, BH / 2.0                     # carrier corner, square: 75.0, 65.0
    px, py, pr = BW / 2.0 - 2.0, BH / 2.0 - 2.0, 4.0    # MP-01 is BW-4 x BH-4, R4 corners
    ax, ay = px - pr, py - pr                       # its corner fillet centre: 69.0, 59.0

    # (a) every lid fixing has a boss under it, and the boss is short of the spigot
    for fx, fy in LID_FIX:
        assert abs(abs(fx) - (POD_OW / 2 - 6.0)) < 1e-9, "lid fixing off pattern"
        assert LID_BOSS_TOP < POD_DEPTH - POD_SPIGOT_T, "boss would hold the lid off the seal"
        assert 12.0 - (POD_LID_T + POD_SPIGOT_T) <= LID_INSERT_DEPTH, "M3 x 12 bottoms out"
        # the D8 boss clears the MP-01 corner arc, which is the nearest thing to it
        gap = math.hypot(abs(fx) - ax, abs(fy) - ay) - LID_BOSS_D / 2.0 - pr
        assert gap > 1.0, f"lid boss fouls MP-01 by {-gap:.2f} mm"
        # and it stays inside the wall rather than breaking the outside face
        assert abs(fx) + LID_BOSS_D / 2.0 <= POD_OW / 2.0, "lid boss breaks the wall"
        assert abs(fy) + LID_BOSS_D / 2.0 <= POD_OH / 2.0, "lid boss breaks the wall"
    # (b) the corner column that carries it clears the carrier corner
    assert POD_IW / 2.0 - LID_COL_IN - cx >= 1.0, "corner column fouls the carrier in X"
    assert POD_IH / 2.0 - LID_COL_IN - cy >= 1.0, "corner column fouls the carrier in Y"
    # (c) the floor boss keeps material under its insert bore
    assert POD_WALL + POD_FLOOR_BOSS_H - FLOOR_INSERT_DEPTH >= 2.0, "insert bore too deep"
    assert INSERT_BORE_D + 2 * 1.5 <= POD_FLOOR_BOSS_D, "boss wall thinner than 1.5 mm"
    # (d) the harness entry sits in the harness layer and touches neither end of it
    assert ENTRY_Z - ENTRY_BORE_D / 2.0 > Z_CARRIER_TOP, "gland bore breaks into the carrier"
    assert ENTRY_Z + ENTRY_BORE_D / 2.0 < Z_PLATE_UNDER, "gland bore breaks into MP-01"
    # (d2) the gland the entry is drawn for can actually be bought against these features:
    # the seat covers the assumed locknut's corners, the panel is inside the range a gland
    # of this class quotes, and the clamping range brackets both jackets with margin
    assert ENTRY_PAD_D >= GLAND_LOCKNUT_AF / math.cos(math.radians(30.0)), \
        "the locknut seat is smaller than the nut's corners"
    assert GLAND_PANEL_MIN <= POD_WALL + ENTRY_PAD_T <= GLAND_PANEL_MAX, \
        "the pod panel is outside the gland's panel range"
    for _od in (WH01_JACKET_MAX, WH02_JACKET_NOM):
        assert GLAND_CLAMP_MIN < _od < GLAND_CLAMP_MAX, "gland range misses a jacket"
    for cable, conn, centre, inward, along, clip in HARNESS:
        # the entry is on the wall it claims to be on, at its connector's own coordinate
        onwall = [abs(abs(centre[i]) - (POD_IW / 2.0 if i == 0 else POD_IH / 2.0)) < 1e-9
                  for i in (0, 1)]
        assert any(onwall), f"{conn} entry is not on a wall"
        # the P-clip boss stops short of the MP-01 outline it stands next to
        reach = (POD_IW / 2.0 - CLIP_BOSS_H) - px if onwall[0] else (POD_IH / 2.0 - CLIP_BOSS_H) - py
        assert reach >= 1.0, f"{conn} P-clip boss fouls MP-01"
        # and clear of the corner column, on the same wall
        u = 1 if onwall[0] else 0                   # the along-wall axis
        far = abs(centre[u] + clip) + CLIP_BOSS_D / 2.0
        edge = (POD_IH / 2.0 if u else POD_IW / 2.0) - LID_COL_IN
        assert max(far, abs(centre[u]) + ENTRY_PAD_D / 2.0) < edge, f"{conn} entry hits a column"
    # (e) the stack still fits under the closed lid, which is what the whole pod is for
    assert Z_STACK_TOP < POD_DEPTH - POD_SPIGOT_T, "the stack does not fit under the lid"


_pod_holds()


def _box(x0, x1, y0, y1, z0, z1):
    """An axis-aligned box from two opposite corners, in part coordinates."""
    return cq.Workplane("XY", origin=(min(x0, x1), min(y0, y1), min(z0, z1))).box(
        abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=(False, False, False))


def _lid_boss(b, fx, fy):
    """One corner boss under one lid fixing, with the column that carries it to the floor.

    Clearances, all to parts that already exist in this file or in design.py:
      * carrier, 150.0 x 130.0 square-cornered, centred: its corner is at (+/-75, +/-65)
        and the column is held 1.5 mm off it on both axes;
      * MP-01, 146.0 x 126.0 with a 4.0 mm corner fillet: the boss clears its corner arc by
        1.19 mm, and everything on the plate is inboard of that.  A module that overhangs
        the plate edge is not modelled and would have to be checked at first article.
    """
    sx = 1.0 if fx > 0 else -1.0
    sy = 1.0 if fy > 0 else -1.0
    ix, iy = sx * POD_IW / 2.0, sy * POD_IH / 2.0          # inner wall faces, +/-79, +/-69
    ox, oy = sx * POD_OW / 2.0, sy * POD_OH / 2.0          # outer faces, +/-81.5, +/-71.5
    col = _box(ix - sx * LID_COL_IN, ox, iy - sy * LID_COL_IN, oy,
               POD_WALL, LID_BOSS_BOTTOM)
    b = b.union(col)
    b = b.union(cq.Workplane("XY", origin=(fx, fy, LID_BOSS_BOTTOM))
                .circle(LID_BOSS_D / 2.0).extrude(LID_BOSS_TOP - LID_BOSS_BOTTOM))
    b = b.union(_box(fx, ox, fy, oy, LID_BOSS_BOTTOM, LID_BOSS_TOP))
    b = b.cut(cq.Workplane("XY", origin=(fx, fy, LID_BOSS_TOP - LID_INSERT_DEPTH))
              .circle(INSERT_BORE_D / 2.0).extrude(LID_INSERT_DEPTH + 0.5))
    b = b.cut(cq.Workplane("XY", origin=(fx, fy, LID_BOSS_TOP - INSERT_LEADIN_T))
              .circle(INSERT_LEADIN_D / 2.0).extrude(INSERT_LEADIN_T + 0.5))
    return b


def _harness_entry(b, centre, inward, along, clip_offset):
    """One cable-gland entry through a wall, with its locknut pad and its P-clip boss.

    `centre` is a point on the INNER wall face, `inward` the unit normal pointing into the
    cavity, `along` the unit vector along the wall that the P-clip boss is offset on.
    """
    n = cq.Vector(*inward)
    u = cq.Vector(*along)
    o = cq.Vector(*centre)
    # Both bosses are started 0.5 mm inside the wall rather than on its face.  A cylinder
    # raised from a face it is exactly coplanar with leaves a seam the mesher can turn into
    # a T-junction, and the STL then fails the watertight check in build().
    bury = 0.5
    pad = cq.Plane(origin=o - n * bury + u * (clip_offset / 2.0), xDir=u, normal=n)
    b = b.union(cq.Workplane(pad)
                .slot2D(abs(clip_offset) + ENTRY_PAD_D, ENTRY_PAD_D, 0)
                .extrude(ENTRY_PAD_T + bury))
    pl = cq.Plane(origin=o - n * bury, xDir=u, normal=n)
    b = b.cut(cq.Workplane(pl).circle(ENTRY_BORE_D / 2.0).extrude(10.0, both=True))
    cpl = cq.Plane(origin=o - n * bury + u * clip_offset, xDir=u, normal=n)
    b = b.union(cq.Workplane(cpl).circle(CLIP_BOSS_D / 2.0).extrude(CLIP_BOSS_H + bury))
    end = cq.Plane(origin=o + u * clip_offset + n * CLIP_BOSS_H, xDir=u, normal=n)
    b = b.cut(cq.Workplane(end).circle(CLIP_PILOT_D / 2.0).extrude(-CLIP_PILOT_DEPTH))
    return b


def pod_base():
    """POD-P1 base: 158 x 138 mm internal, 55.5 mm deep inside, 2.5 mm walls, a gasket
    groove in the rim, four carrier bosses on the internal floor, four corner bosses that
    take the lid screws, two cable-gland entries for the helmet harness, and the panel
    openings of RFQ M-02.  Sized for the 150 x 130 mm carrier with the MP-01 module plate
    18 mm above it and the modules above that.

    On the carrier fixing, which ASM-EEG-007 section 3.3 carries as an open point.  MH1 to
    MH4 are the only four fixings on the carrier and three things want them: the pod boss
    below, the standoff above, and the carrier itself in between.  Of the two resolutions
    that section offers, this model takes the first -- **one fixing does both jobs** -- and
    not the second.  Four additional fixing points would have to be four additional holes in
    the carrier, and the carrier is a different file at a different revision; a pod boss
    pattern clear of MH1 to MH4 would have nothing to bolt to.  So: the boss is bored for an
    M3 brass insert and the standoff becomes **male-female**, its male stud passing down
    through the carrier's MH clearance hole into that insert, its female end taking the
    M3 x 6 nylon screw that carries MP-01.  The carrier is clamped between the standoff
    shoulder and the boss face.  Nothing about the stack height changes -- floor 2.5 + boss
    6.0 + carrier 1.6 + standoff 18.0 + plate 3.0 is still 49.1 mm against 55.5 -- and the
    standoff is still an 18 mm nylon part, so RISK-EEG-011 SR-08's 8 mm creepage is still
    met by the same 18 mm slant path.  What does change is outside this file and is listed
    in KNOWN_ISSUES: ASM-EEG-007 section 3.3 and the stage 4 torque table (the M3 x 8 A2 is
    deleted, the eight M3 x 6 nylon screws become four), AVL-EEG-017 and the BOM (a
    male-female standoff, and eight M3 brass inserts per pod), and PARTS-EEG-019.
    """
    wall, depth = POD_WALL, POD_DEPTH
    iw, ih = POD_IW, POD_IH
    ow, oh = POD_OW, POD_OH
    b = (cq.Workplane("XY").box(ow, oh, depth, centered=(True, True, False))
         .faces(">Z").shell(-wall))
    # gasket groove, 1.6 mm wide and 1.2 mm deep, in the top rim
    b = b.cut(cq.Workplane("XY", origin=(0, 0, depth - 1.2))
              .rect(iw + wall + 0.8, ih + wall + 0.8).extrude(2.0)
              .cut(cq.Workplane("XY", origin=(0, 0, depth - 1.2))
                   .rect(iw + wall - 0.8, ih + wall - 0.8).extrude(2.0)))
    # four carrier bosses standing 6 mm off the internal floor, bored for an M3 insert
    for x, y in MH:
        cx, cy = _c(x, y)
        top = wall + POD_FLOOR_BOSS_H
        b = b.union(cq.Workplane("XY", origin=(cx, cy, wall))
                    .circle(POD_FLOOR_BOSS_D / 2.0).extrude(POD_FLOOR_BOSS_H))
        b = b.cut(cq.Workplane("XY", origin=(cx, cy, top - FLOOR_INSERT_DEPTH))
                  .circle(INSERT_BORE_D / 2.0).extrude(FLOOR_INSERT_DEPTH + 0.5))
        b = b.cut(cq.Workplane("XY", origin=(cx, cy, top - INSERT_LEADIN_T))
                  .circle(INSERT_LEADIN_D / 2.0).extrude(INSERT_LEADIN_T + 0.5))
    # four corner bosses under the lid fixings, and the columns that carry them down
    for fx, fy in LID_FIX:
        b = _lid_boss(b, fx, fy)
    # two cable-gland entries, one per helmet cable
    for _cable, _conn, centre, inward, along, clip in HARNESS:
        b = _harness_entry(b, centre, inward, along, clip)
    # panel openings, on the two short walls
    for name, x, y, shape, size in PANEL:
        if name in POD_LID_MOUNTED:
            continue                      # cut by pod_lid(), not by a wall
        cx, cy = _c(x, y)
        side = -1 if x < BW / 2 else 1
        wp = cq.Workplane("YZ", origin=(side * (ow / 2 + 3.0), cy, depth * 0.45))
        cut = (wp.circle(size / 2) if shape == "circle"
               else wp.rect(size[0], size[1])).extrude(-side * 12.0)
        b = b.cut(cut)
    # section 4.1 mark, on the external floor: the one face that is flat, big and still
    # readable with the lid on and the carrier fitted
    txt, size = MARKING["POD-P1_prototype_enclosure_base"]
    b = _engrave(b, txt, _face((0.0, 0.0, 0.0), normal=(0, 0, -1)), size)
    return b


def pod_lid():
    """POD-P1 lid: a 4.0 mm plate with a 2.0 mm spigot, and four M3 clearance holes on the
    LID_FIX pattern -- the same four points pod_base() puts a boss under.  An M3 x 12 A2
    pan screw (ASM-EEG-007 5.1 step 6) passes through 6.0 mm of lid and takes 6.0 mm of
    brass insert in the base boss."""
    wall = POD_WALL
    iw, ih = POD_IW, POD_IH
    ow, oh = POD_OW, POD_OH
    lid = cq.Workplane("XY").box(ow, oh, POD_LID_T, centered=(True, True, False))
    lid = lid.union(cq.Workplane("XY", origin=(0, 0, -POD_SPIGOT_T))
                    .rect(iw - 0.4, ih - 0.4).extrude(POD_SPIGOT_T))
    # fixing holes at the four corners
    for fx, fy in LID_FIX:
        lid = (lid.faces(">Z").workplane(origin=(fx, fy, 0))
               .circle(LID_HOLE_D / 2.0).cutThruAll())

    # The three buttons, through the lid.  They used to be cut into the right-hand WALL by
    # pod_base(), because PANEL puts an opening on a wall chosen from its x coordinate and
    # the buttons sit at x = 102 -- 48 mm inboard of that wall.  The holes lined up with
    # nothing and merged with four connector openings.  A button is pressed from above.
    for _name, _x, _y, _shape, _size in PANEL:
        if _name not in POD_LID_MOUNTED:
            continue
        _cx, _cy = _c(_x, _y)
        lid = lid.cut(cq.Workplane("XY", origin=(_cx, _cy, -1.0))
                      .circle(_size / 2.0).extrude(POD_LID_T + 2.0))
    # section 4.1 mark, on the inside face of the spigot.  It goes inside because the
    # outer face is the ART-LBL-01 label keep-out (PKG-EEG-015), which must stay flat.
    txt, size = MARKING["POD-P1_prototype_enclosure_lid"]
    lid = _engrave(lid, txt, _face((0.0, -50.0, -POD_SPIGOT_T), normal=(0, 0, -1)), size)
    return lid


# --------------------------------------------------------------------------- HM-04
def hm04():
    """Electrode assembly body: 12.4 x 12.4 x 18 mm.

    A bore for the sintered Ag/AgCl cup on its service bayonet, a spring seat above it, a
    2.5 mm gel port through the top coaxial with the cup, TWO separated side pockets -- an
    outboard LED seat and an inboard conductor run, with 1.60 mm of material between them --
    and a real bayonet: entry slots, a 100 deg circumferential run and a retaining lip that
    only the HM-09 service key can turn back out.

    The side pockets used to be one box straight through the body, which put an electrode
    conductor and a switched LED conductor in one shared cavity about 3 mm apart at all
    eight sites.  RISK-EEG-011 SF-9 is exactly that fault.
    """
    w, h = 12.4, 18.0
    b = cq.Workplane("XY").box(w, w, h, centered=(True, True, False))
    b = b.faces(">Z").fillet(1.2)
    # cup bore from the underside
    b = b.faces("<Z").workplane().circle(4.6).cutBlind(-9.0)
    # spring seat
    # Spring seat, 6.60 mm deep, not 4.50.
    #
    # The HM-05B spigot is D6.60 x 3.50 and its top lands at z 12.10, so a seat roof at
    # 13.50 left 1.40 mm of free height for the compression spring.  That is not a spring,
    # it is a washer: a 3-6 N spring with the carrier's 0.40 mm of working travel needs a
    # free length near 5 mm and an installed height near 3.5 mm.  And the seat is only
    # 0.10 mm larger than the spigot ON THE RADIUS, so no coil fits around it either --
    # the spring must sit ON the spigot top, which makes the free height the whole budget.
    # AVL-EEG-017 K12 has carried "3-6 N stainless 302 compression spring" as an open
    # purchase for three revisions and it could not have been bought.
    #
    # Roof to 15.60 gives 3.50 mm of free height and still leaves 2.40 mm of material
    # above it, carrying only the D2.50 gel port.
    b = b.faces("<Z").workplane(offset=-9.0).circle(3.4).cutBlind(-6.6)
    # gel port through the top, coaxial
    b = b.faces(">Z").workplane().circle(1.25).cutThruAll()
    # bayonet slots, two at 180 degrees
    for a in (0.0, math.pi):
        x, y = 4.2 * math.cos(a), 4.2 * math.sin(a)
        b = (b.faces("<Z").workplane(origin=(x, y, 0))
             .rect(2.2, 1.4).cutBlind(-2.4))
    # light window on one side
    b = (cq.Workplane("XZ", origin=(0, -w / 2, 13.5)).rect(4.0, 3.0)
         .extrude(3.0, both=True).cut(b).cut(b))
    body = cq.Workplane("XY").box(w, w, h, centered=(True, True, False))
    body = body.faces(">Z").fillet(1.2)
    body = body.faces("<Z").workplane().circle(4.6).cutBlind(-9.0)
    body = body.faces("<Z").workplane(offset=-9.0).circle(3.4).cutBlind(-6.6)
    body = body.faces(">Z").workplane().circle(1.25).cutThruAll()
    # Entry slots.  These were rect(2.2, 1.4) centred at r = 4.2 -- outer radius 5.30 and
    # a 1.40 mm slot for a 1.40 mm lug, i.e. zero tangential clearance in a material
    # printed to +/-0.15 mm.  Widened to 1.70 (0.15 mm a side) and moved out so the slot
    # clears the corrected 5.20 mm lug with 0.35 mm to spare.
    SLOT_W, SLOT_RADIAL, SLOT_R_C = 1.70, 2.30, 4.40      # outer radius 5.55
    SLOT_DEPTH = 3.60                                     # clears the lug's 1.20..3.30
    for a in (0.0, math.pi):
        x, y = SLOT_R_C * math.cos(a), SLOT_R_C * math.sin(a)
        body = (body.faces("<Z").workplane(origin=(x, y, 0))
                .rect(SLOT_RADIAL, SLOT_W).cutBlind(-SLOT_DEPTH))

    # THE CIRCUMFERENTIAL RUN.  hm04() cut two straight axial pockets and nothing else, so
    # the carrier went in and could not rotate: a plug fit, not a bayonet.  hm05b()'s own
    # docstring said so -- "the run that joins them belongs in HM-04 and is not this part's
    # to add" -- and nobody added it.  Without it the drive notches never come round under
    # the slots, the HM-09 key cannot reach them, and the cup is not replaceable, which is
    # the entire service model of the kit.
    #
    # The lug occupies z 1.20..3.30.  The run is cut at z 1.10..3.40, leaving z 0..1.10 of
    # solid material below it as the RETAINING LIP: after the quarter turn the lug rests on
    # that lip and the carrier cannot fall out of an inverted helmet.  The first attempt
    # put the run at 0.95..2.35 against a lug at 0.15..2.25, which buried the lug's lower
    # 0.80 mm in the lip -- entry was clean and the carrier then would not turn, which a
    # boolean interference check caught and a drawing would not have.
    # Ceiling at 3.80, not 3.40.  The carrier body is 8.60 mm in a 9.00 mm bore, so it has
    # 0.40 mm of axial float, and that float is not slack -- it is the travel the cup makes
    # when it is pressed against the scalp and the spring takes up.  A run that clears the
    # lug at rest and not through its travel binds the electrode at exactly the moment it
    # is supposed to be compliant.  3.30 (lug top) + 0.40 (travel) + 0.10 (clearance).
    RUN_Z0, RUN_Z1 = 1.10, 3.80
    RUN_R_IN, RUN_R_OUT = 4.30, 5.55
    RUN_DEG = 100.0                      # 90 deg of travel plus 10 deg of over-run
    for a0 in (0.0, 180.0):
        pts = [(0.0, 0.0)]
        steps = 24
        for k in range(steps + 1):
            t = math.radians(a0 + RUN_DEG * k / steps)
            pts.append((RUN_R_OUT * math.cos(t), RUN_R_OUT * math.sin(t)))
        for k in range(steps, -1, -1):
            t = math.radians(a0 + RUN_DEG * k / steps)
            pts.append((RUN_R_IN * math.cos(t), RUN_R_IN * math.sin(t)))
        sector = (cq.Workplane("XY", origin=(0, 0, RUN_Z0))
                  .polyline(pts).close().extrude(RUN_Z1 - RUN_Z0))
        body = body.cut(sector)

    # NO SNAP DETENT.  One was drawn here and removed after measuring it.  Two reasons.
    # A snap needs the lug to deform past an interference, and PA12 printed at +/-0.15 mm
    # is the wrong material to ask for a 0.35 mm interference fit -- the tolerance is half
    # the feature.  And the lug is 1.40 mm wide at r ~4.7, so it subtends about 17 deg:
    # a detent 5 deg from the end of a 100 deg run put the lug's trailing corner past the
    # end of the run, which measured as 0.726 mm3 of interference.
    #
    # What holds a seated carrier is what should hold it: the compression spring pushes it
    # down onto the retaining lip, the lip carries it axially, and the end of the run is a
    # positive angular stop.  Turning it back out needs the HM-09 key, which is the point.

    # The contact-light window.  This was ONE box straight through the body, so its
    # "inboard" and "outboard" openings were two ends of a single cavity and any scheme
    # putting the electrode conductor in one end and the LED in the other had them sharing
    # open volume about 3 mm apart at all eight sites.  RISK-EEG-011 SF-9 is exactly that
    # fault.  It is now TWO pockets with 1.60 mm of printed PA12 between them: the outboard
    # pocket is the LED seat, the inboard pocket is the electrode conductor's run.
    WIN_Z, WIN_H = 13.0, 2.6
    win_out = cq.Workplane("XY", origin=(0, -(w / 4 + 0.8), WIN_Z)).box(3.2, w / 2, WIN_H)
    win_in = cq.Workplane("XY", origin=(0, +(w / 4 + 0.8), WIN_Z)).box(3.2, w / 2, WIN_H)
    return body.cut(win_out).cut(win_in)


# --------------------------------------------------------------------------- HM-08
def hm08():
    """Battery hatch, quarter-turn, 48 x 36 x 6.5 mm. Three lugs, a coin slot and a seal
    groove. Called HM-07 in Rev A; renamed in PARTS-EEG-019 because DSN-EEG-002 section 10
    already used HM-07 for the boom microphone arm."""
    b = cq.Workplane("XY").box(48.0, 36.0, 4.0, centered=(True, True, False))
    b = b.edges("|Z").fillet(4.0)
    b = b.faces(">Z").fillet(1.0)
    # coin slot
    b = (b.faces(">Z").workplane().rect(20.0, 2.6).cutBlind(-1.4))
    # three quarter-turn lugs on the underside
    for a in (90.0, 210.0, 330.0):
        r = 19.0
        x, y = r * math.cos(math.radians(a)), (r * 0.72) * math.sin(math.radians(a))
        lug = (cq.Workplane("XY", origin=(x, y, -2.5)).box(6.0, 3.0, 2.5,
                                                           centered=(True, True, False)))
        b = b.union(lug)
    # seal groove
    b = (b.faces("<Z").workplane(invert=True)
         .rect(43.0, 31.0).rect(41.0, 29.0).cutBlind(-1.0))
    # section 4.1 mark, on the top face beside the coin slot
    txt, size = MARKING["HM-08_battery_hatch"]
    b = _engrave(b, txt, _face((0.0, -10.5, 4.0)), size)
    return b


# --------------------------------------------------------------------------- HM-09
def hm09():
    """Service key: a quarter-turn key that engages the HM-04 bayonet slots. Deliberately
    absent from the participant's kit -- one per operator (SVC-EEG-013 section 3)."""
    k = cq.Workplane("XY").circle(9.0).extrude(6.0)
    k = k.faces(">Z").workplane().circle(5.0).extrude(28.0)
    k = k.faces(">Z").workplane().circle(4.4).extrude(4.0)
    for a in (0.0, math.pi):
        x, y = 4.2 * math.cos(a), 4.2 * math.sin(a)
        k = k.union(cq.Workplane("XY", origin=(x, y, 38.0)).box(2.0, 1.2, 2.2,
                                                               centered=(True, True, False)))
    # knurl: eight flats around the grip
    for i in range(8):
        a = 2 * math.pi * i / 8
        x, y = 8.6 * math.cos(a), 8.6 * math.sin(a)
        cut = (cq.Workplane("XY", origin=(x, y, 0)).box(1.6, 1.6, 6.0,
                                                        centered=(True, True, False))
               .rotate((x, y, 0), (x, y, 1), math.degrees(a)))
        k = k.cut(cut)
    # Section 4.1 mark, on the grip end face.  A 17.93 mm face will not hold "HM-09 A" any
    # larger than 4.0 mm, which is a 0.58 mm stroke against the 0.60 mm minimum, and it
    # will not hold the SVC-EEG-013 section 4.2 legend at all.  The shortfall is stated on
    # the MECH-EEG-020 sheet; the legend and the key number are applied per key at issue.
    txt, size = MARKING["HM-09_service_key"]
    k = _engrave(k, txt, _face((0.0, 0.0, 0.0), normal=(0, 0, -1)), size)
    return k


# --------------------------------------------------------------------------- HM-02
def hm02_brow():
    """TPU brow pad, 85 x 22 x 8 mm, consumable, replaced every turnaround."""
    p = cq.Workplane("XY").box(85.0, 22.0, 8.0, centered=(True, True, False))
    p = p.edges("|Z").fillet(6.0)
    p = p.faces(">Z").fillet(2.5)
    p = (p.faces("<Z").workplane(invert=True).rect(70.0, 8.0).cutBlind(-1.5))
    return p


# --------------------------------------------------------------------------- FIT-01
def fit01():
    """Fit-test coupon. Carries the three fits that decide whether a print is usable:
    the cup bayonet, the HM-04 collar and the hatch lug. Printed with every batch and
    checked before the batch is accepted (QP-EEG-010)."""
    c = cq.Workplane("XY").box(60.0, 24.0, 10.0, centered=(True, True, False))
    # bayonet bore at nominal, +0.15 and -0.05
    for i, d in enumerate((9.20, 9.35, 9.15)):
        c = (c.faces(">Z").workplane(origin=(-20.0 + i * 20.0, 0, 0))
             .circle(d / 2).cutThruAll())
    return c


# ======================================================================= v2.1 additions
# Nine of the parts the packing list names had an identifier, a material and a quantity in
# PARTS-EEG-019 Rev B and no geometry at all, so a print bureau could not quote them and a
# kit could not be built.  They are modelled below.  Every dimension is derived from a part
# that already exists -- the HM-01 mesh, HM-04, HM-08, HM-09, the POD-P1 bosses, the
# protected 18650 envelope or the WH cable jackets -- and each docstring says which, and says
# what about the part is still unmeasured.
#
# Five more are still missing and are deliberately NOT modelled, because nothing in the
# package dimensions them and a part that is the wrong shape is worse than one that is
# honestly absent: HM-03B ratchet dial housing (HM-03C, the mechanism it houses, has no
# vendor), HM-06A chin cup and HM-06B liner (the package fixes the 20 mm webbing and the
# 200 N anchor pull and nothing at all about the shell), HM-07A boom temple mount (HM-07B,
# the gooseneck it clamps, has no vendor and no diameter) and POD-P1-05 cable gland
# (bought-in, quantity zero, withdrawn from the Phase 1 build by WH-EEG-008 Rev B section 1).

# --- the HM-01 frame, as measured on mech/stl/HM-01_frame_monocoque.stl -------------------
# The frame is a carried-over v1 mesh with no parametric source (PARTS-EEG-019 OA-1), so the
# parts that mate with it are dimensioned by sectioning the mesh.  What follows are
# least-squares fits through the section centres, with their residuals, so a reader can see
# how far each fit is being trusted:
#
#   sagittal arch  bore centre on a circle R = 118.03 mm about (y = 0, z = -31.32),
#                  15 sections at |y| = 10..90 mm, RMS residual 0.86 mm, worst 2.36 mm
#   coronal arch   bore centre on a circle R = 87.28 mm about (x = 0, z = -0.83),
#                  12 sections at |x| = 10..75 mm, RMS residual 0.53 mm, worst 1.29 mm
#   halo           band centre on an ellipse a = 81.10 mm (lateral), b = 96.80 mm (fore-aft)
#                  at z = 14.79 mm, 12 azimuths, RMS residual 0.32 mm
#
# The bore measures 3.74 to 3.80 mm across every one of those sections, which is the 3.80 mm
# channel WH-EEG-008 Rev B section 7 specifies.  That is the only thing about the channel
# system on which the released frame and the released harness document agree -- see hm11a().
HM01_SAG_R, HM01_SAG_ZC = 118.03, -31.32
HM01_COR_R, HM01_COR_ZC = 87.28, -0.83
HM01_HALO_A, HM01_HALO_B, HM01_HALO_Z = 81.10, 96.80, 14.79
# The azimuth range in which the z = 14.79 mm section is occipital shell and not halo band,
# measured: no cover strip can run there, so HM-03A has to.
HM01_SHELL_T0, HM01_SHELL_T1 = 235.0, 305.0
HM01_HALO_BAND_W = 10.91        # measured radial width of the v1 halo band at the temple;
                                # it widens to 11.93 mm at the front
HM01_SHELL_W = 116.0            # measured width of the occipital shell, x = -58.0 .. +58.0

# --- the occipital shell itself, measured the same way ------------------------------------
# The arches and the halo are curved and had to be fitted, with the residuals above.  The
# occipital shell is not: it is a rectangular box, and the sections come back exact.  The
# figures below are from horizontal and vertical sections of the same mesh, and the sample
# standard deviation is quoted because it is what says how much of a fit this is:
#
#   shell wall     outer (cavity-side) face y = -82.410, skull-facing face y = -80.010,
#                  thickness 2.400 mm, over a 13 x 14 grid of x = -30..+30, z = -50..+28,
#                  n = 182 points, sd 0.000 mm on every one of the three
#   shell floor    underside z = -56.000, cavity face z = -53.600, thickness 2.400 mm,
#                  30 points over x = -27..+27, y = -118..-83, sd 0.000 mm
#   footprint      x = +/-58.000, y = -126.010 (open rear edge) to -80.010, so 116.00 wide
#                  and 46.00 deep; side walls 2.40 thick with inner faces at x = +/-55.600;
#                  roof plate z = 29.600 to 32.000
#
# The shell is therefore a 116.00 x 46.00 x 88.00 mm box, open at the back, which is the
# same shell ASM-EEG-007 section 5.2 describes as "116 x 46 x 88 mm" for Phase 2.
HM01_SHELL_Y_OUT = -82.41       # cavity-side face of the shell wall
HM01_SHELL_Y_IN = -80.01        # skull-facing face, the face the HM-02B pads sit on
HM01_SHELL_Y_BACK = -126.01     # open rear edge of the floor and roof plates
HM01_SHELL_X = 58.00            # +/- , the outside of the side walls
HM01_SHELL_WALL_T = 2.40        # every wall and plate of the shell, measured
HM01_SHELL_FLOOR_Z = -56.00     # underside of the floor plate: the lowest point of HM-01
HM01_SHELL_FLOOR_T = 2.40
HM01_SHELL_ROOF_Z = 29.60       # cavity-side face of the roof plate

# The three channel mouths on the occiput, and the reason the umbilicals have to go where
# they go.  **Every channel that reaches the occiput opens into the shell cavity**, and
# nothing opens anywhere else: the floor plate has no hole in it at all (a section at
# z = -54.8, through the middle of the plate, returns no closed loop), and the roof plate has
# exactly one within the shell footprint.
#
#   rear sagittal, through the roof plate.  Sectioning at 0.2 mm intervals from z = 29.8 to
#   36.0 finds a single 3.78 mm bore on the midline whose centre moves forward as it rises;
#   a least-squares fit through 32 section centres gives dy/dz = 0.3203, RMS residual
#   0.035 mm, extrapolating to y = -95.379 at the cavity face of the roof plate.  Below that
#   face there is no bore, so the channel opens downward into the cavity.
#
#   two halo branches, through the shell wall.  A branch leaves the halo channel at about
#   y = -50 on each side and descends inboard -- (66.50, -55, 11.44), (63.65, -60, 7.44),
#   (56.80, -70, -0.77), (45.87, -82, -10.90) on the +x side -- and stops dead at the cavity
#   face: the loop is still there at y = -82.41 and gone at y = -82.50.  So it opens into the
#   cavity at (+/-45.41, -82.41, -11.25).
#
# Those three mouths are where WH-EEG-008 section 7's three trunks out of node N1 go -- rear
# sagittal to the crown, and round the halo left and right -- so **N1 is inside the occipital
# shell cavity**, and a conductor that is going to reach any channel has to be in that cavity
# first.  That is what puts the entries below in the shell floor.
HM01_N1_MOUTH = (0.00, -95.38, HM01_SHELL_ROOF_Z)
HM01_N1_MOUTH_D = 3.78
HM01_HALO_MOUTH = (45.41, HM01_SHELL_Y_OUT, -11.25)     # and its mirror at -45.41

# --- the channel system the HM-11 strips close (WH-EEG-008 Rev B section 7) ---------------
CH_BORE = 3.80          # measured on the HM-01 mesh; the same figure WH-EEG-008 s7 states
CH_PITCH = 6.00         # channel A to channel B, centre to centre, WH-EEG-008 s7 minimum
CH_WALL = 1.20          # material outboard of each bore, set by MJF PA12 practice
STRIP_W = CH_PITCH + CH_BORE        # 9.80 -- the strip spans both channel mouths
STRIP_T = 1.60          # web
STRIP_LIP = 0.60        # snap lip, proud of the web on each edge
STRIP_LIP_H = 0.50
STRIP_PICK = 8.00       # unlipped strip at one end, to start the plastic pick
# What a section has to be to hold the pair: 6.00 + 3.80 + 2 x 1.20 = 12.20 mm.  The v1 halo
# band measures 10.91 mm, so the frame is 1.29 mm too narrow for its own harness document.
SECTION_W_MIN = CH_PITCH + CH_BORE + 2 * CH_WALL


def _cl_ellipse(a, b, t0, t1, n=481):
    """Centreline of an elliptical band: [((u, v), outward unit normal), ...]."""
    out = []
    for i in range(n):
        t = math.radians(t0 + (t1 - t0) * i / (n - 1))
        nx, ny = b * math.cos(t), a * math.sin(t)
        L = math.hypot(nx, ny)
        out.append(((a * math.cos(t), b * math.sin(t)), (nx / L, ny / L)))
    return out


def _cl_arc(R, cv, t0, t1, n=241):
    """Centreline of a circular arc of radius R about (0, cv) in a local (u, v) plane, the
    angle measured from the +v axis.  The normal points away from the centre."""
    out = []
    for i in range(n):
        t = math.radians(t0 + (t1 - t0) * i / (n - 1))
        nu, nv = math.sin(t), math.cos(t)
        out.append(((R * nu, cv + R * nv), (nu, nv)))
    return out


def _band(cl, o1, o2):
    """Closed polygon of the material between normal offsets o1 and o2 of centreline `cl`."""
    inner = [(u + o1 * nu, v + o1 * nv) for (u, v), (nu, nv) in cl]
    outer = [(u + o2 * nu, v + o2 * nv) for (u, v), (nu, nv) in cl]
    return outer + inner[::-1]


def _cl_len(cl):
    return sum(math.dist(cl[i][0], cl[i + 1][0]) for i in range(len(cl) - 1))


def _cl_trim(cl, mm):
    """Drop `mm` of centreline off the far end, which is what makes the pick relief."""
    run = 0.0
    for i in range(len(cl) - 1, 0, -1):
        run += math.dist(cl[i][0], cl[i - 1][0])
        if run >= mm:
            return cl[:i]
    return cl


# --------------------------------------------------------------------------- HM-11A/B/C
def _strip_planar(cl, z0):
    """A cover strip whose centreline is flat in plan: width radial, thickness in Z.  This
    is the halo, whose band lies in a horizontal plane."""
    main = (cq.Workplane("XY", origin=(0, 0, z0))
            .polyline(_band(cl, -STRIP_W / 2, STRIP_W / 2)).close().extrude(STRIP_T))
    lip = (cq.Workplane("XY", origin=(0, 0, z0 + STRIP_T - STRIP_LIP_H))
           .polyline(_band(_cl_trim(cl, STRIP_PICK),
                           -STRIP_W / 2 - STRIP_LIP, STRIP_W / 2 + STRIP_LIP))
           .close().extrude(STRIP_LIP_H))
    return main.union(lip)


def _strip_swept(cl):
    """A cover strip whose centreline is an arc in a vertical plane: thickness radial, width
    across the arch.  Built in the local XY plane; the caller rotates it into the frame."""
    main = (cq.Workplane("XY").polyline(_band(cl, -STRIP_T / 2, STRIP_T / 2))
            .close().extrude(STRIP_W))
    lip = (cq.Workplane("XY")
           .polyline(_band(_cl_trim(cl, STRIP_PICK), STRIP_T / 2 - STRIP_LIP_H, STRIP_T / 2))
           .close().extrude(STRIP_W + 2 * STRIP_LIP).translate((0, 0, -STRIP_LIP)))
    return main.union(lip).translate((0, 0, -STRIP_W / 2))


def hm11a_halo():
    """HM-11A channel cover strip, halo.

    WH-EEG-008 Rev B section 7 gives every frame section **two** channels -- A on the outer
    wall for the electrode cable WH-01, B on the skull-facing wall for the light cable WH-02,
    3.80 mm bore, at least 6.00 mm centre to centre -- and closes both with a snap-in strip on
    the skull-facing side, laid in with a plastic pick (ASM-EEG-007 section 4.4 step 4).  The
    strip is on the packing list at line 1.1 and has never existed as geometry.  This is it:
    a 9.80 mm wide, 1.60 mm web with a 0.60 x 0.50 mm snap lip down each edge and 8.00 mm of
    unlipped strip at one end for the pick to get under.

    Centreline: the ellipse fitted to the HM-01 halo band, a = 81.10, b = 96.80 mm at
    z = 14.79 mm, running from azimuth -55 deg round the front to +235 deg -- the whole band
    except the 70 deg the occipital shell occupies, which is HM-03A's arc.  The strip sits
    with its outer face 1.90 mm below the bore centres, at z = 11.29 mm; the measured
    underside of the v1 halo band is at z = 11.20 mm, so it lands 0.09 mm proud of it.

    **The released HM-01 cannot take this strip.**  Sectioned, the v1 frame has ONE fully
    enclosed 3.80 mm bore per section -- no second channel, and no rebate for a strip -- and
    its halo band measures 10.91 mm across at the temple and 11.93 mm at the front, where two
    channels at 6.00 mm centres inside 1.20 mm walls need 12.20 mm.  The strip is modelled to
    the harness document because that is the document that governs the channel; the frame has
    to grow between 0.3 and 1.3 mm and gain the rebate when the parametric HM-01 of
    PARTS-EEG-019 OA-1 is drawn.  Until then this part fits nothing, and that is a frame
    problem and not a strip problem.
    """
    cl = _cl_ellipse(HM01_HALO_A, HM01_HALO_B, -55.0, 235.0)
    return _strip_planar(cl, HM01_HALO_Z - CH_BORE / 2 - STRIP_T)


def hm11b_sagittal():
    """HM-11B channel cover strip, sagittal arch.  The same 9.80 x 1.60 mm lipped section as
    HM-11A, on the circle fitted to the HM-01 sagittal bore centres (R = 118.03 mm about
    z = -31.32 mm), 105.0 mm of arc each side of the crown.

    105.0 mm is where the arch ends.  Sectioning the mesh every 5 mm finds the bore out to
    |y| = 90 mm and not at |y| = 95, and 105.0 mm of arc from the apex reaches y = 91.7 mm.
    WH-EEG-008 section 3.1 routes 110 mm forward from the crown to Fz, which agrees with the
    measured arch to within 5 mm, and 175 mm rearward from node N1 to the crown, of which only
    105 mm is on the arch.  **The other 70 mm is inside the occipital shell, where the v1 mesh
    models no channel at all**, so no strip is drawn for it; that length is a Phase 1
    measurement and not a number to be guessed here.

    The strip runs on radius 115.33 mm, 2.70 mm inside the bore centres, so its own developed
    length is a little under the 210.0 mm of bore centreline it covers.  Same caveat as
    HM-11A: the v1 arch is a Ø9.20 mm rod with one enclosed bore, which is 3.00 mm narrower
    than the 12.20 mm the two-channel section needs, and has no rebate for this strip.
    """
    th = math.degrees(105.0 / HM01_SAG_R)
    cl = _cl_arc(HM01_SAG_R - CH_BORE / 2 - STRIP_T / 2, HM01_SAG_ZC, -th, th)
    # local (u, v, w) -> global (w, u, v): u is fore-aft, v is up, w is the strip width
    return _strip_swept(cl).rotate((0, 0, 0), (1, 1, 1), 120)


def hm11c_coronal():
    """HM-11C channel cover strip, coronal arch.  The same section again, on the circle fitted
    to the HM-01 coronal bore centres (R = 87.28 mm about z = -0.83 mm), 80.0 mm of arc each
    side of the crown, 160.0 mm in all.

    80.0 mm is WH-EEG-008 section 3.1's own figure: C3 and C4 are 285 mm of in-frame run
    against Cz's 205 mm, so the crown-to-C3 leg is 80 mm.  On this circle that ends at
    x = 69.2, z = 52.3 mm, and the mesh section at x = 70 mm has its bore centre at
    z = 51.6 mm.  Those two numbers being 0.7 mm apart is the check that the harness cut
    length and the frame geometry are describing the same arch.  The HM-11A caveat about the
    v1 section width and the missing rebate applies here too.
    """
    th = math.degrees(80.0 / HM01_COR_R)
    cl = _cl_arc(HM01_COR_R - CH_BORE / 2 - STRIP_T / 2, HM01_COR_ZC, -th, th)
    # local (u, v, w) -> global (u, -w, v): u is lateral, v is up, w is the strip width
    return _strip_swept(cl).rotate((0, 0, 0), (1, 0, 0), 90)


# --------------------------------------------------------------------------- HM-01P
# The frame section that can actually hold the harness.
#
# HM-01 ships as a watertight STL carried over from Rev A -- a rendered form study with no
# parametric source.  Sectioned, it has ONE fully enclosed 3.80 mm bore per run, and its
# halo band measures 10.91 mm across at the temple.  WH-EEG-008 section 7 gives every
# section TWO channels: A on the outer wall for the electrode cable, B on the skull-facing
# wall for the light cable, 3.80 mm bore at 6.00 mm centres inside 1.20 mm walls, which
# needs 12.20 mm.  The frame is 1.29 mm too narrow for its own harness document, it has no
# second channel, and it has no rebate for the HM-11 cover strips.
#
# That is not a detail.  The 6.00 mm of separation is the physical form of the ECO-EEG-014
# rule that the light group stays away from the electrode group, and RFQ E-30 -- the limit
# on how much noise the contact lights may add to the measurement they report -- is written
# against it.  A frame with one channel means both cables in one bore, which is the one
# arrangement the harness document forbids.
#
# So the sections are drawn here, parametrically, from the centrelines already fitted to the
# v1 mesh: the halo ellipse (a 81.10, b 96.80 at z 14.79), the sagittal circle (R 118.03
# about z -31.32) and the coronal circle (R 87.28 about z -0.83).  The FORM is the v1 study's;
# what changes is the section.
#
# WHAT THIS IS AND IS NOT.  It is a corrected channel-bearing frame: the right sections on
# the measured centrelines, with both bores, the strip rebate and the wall thicknesses the
# harness needs.  It is NOT an ergonomic re-design.  DSN-EEG-002 section 12 objection 3 puts
# the Stage 0 fit measurement ahead of any final frame, and that measurement has not been
# taken, so the head-shape surfaces, the pad seats and the electrode-site normals still come
# from the v1 study and will move when it is.  What is settled here is the one thing that
# could be settled from the documents alone: a section that carries the cables the design
# says it carries.

SEC_W = CH_PITCH + CH_BORE + 2 * CH_WALL        # 12.20, the width the harness needs
SEC_H = CH_BORE + 2 * CH_WALL                   # 6.20, wall-bore-wall through the section
REBATE_W = STRIP_W + 0.30                       # 10.10, the HM-11 strip plus fit clearance
REBATE_D = STRIP_T + STRIP_LIP_H                # 2.10, web plus the snap lip


def _section_profile(w=SEC_W, h=SEC_H, rebate=True):
    """The 2-D section of a channel run, in (across, up): a rounded rectangle carrying two
    bores side by side, with a rebate cut in the skull-facing face for the cover strip."""
    half_w, half_h = w / 2.0, h / 2.0
    pts = [(-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h)]
    return pts, half_w, half_h


def hm01p_halo():
    """The halo run, as a section that holds both channels.

    Swept round the ellipse the v1 halo band was fitted to, from azimuth -55 to +235 deg --
    the whole band except the 70 deg the occipital shell occupies, which is HM-03A's arc,
    exactly the span HM-11A covers.
    """
    cl = _cl_ellipse(HM01_HALO_A, HM01_HALO_B, -55.0, 235.0)
    z0 = HM01_HALO_Z - SEC_H / 2.0
    body = (cq.Workplane("XY", origin=(0, 0, z0))
            .polyline(_band(cl, -SEC_W / 2, SEC_W / 2)).close().extrude(SEC_H))
    # the two channels, at -CH_PITCH/2 and +CH_PITCH/2 across the section
    for off in (-CH_PITCH / 2.0, +CH_PITCH / 2.0):
        bore = (cq.Workplane("XY", origin=(0, 0, HM01_HALO_Z - CH_BORE / 2))
                .polyline(_band(cl, off - CH_BORE / 2, off + CH_BORE / 2))
                .close().extrude(CH_BORE))
        body = body.cut(bore)
    # the rebate the HM-11A strip snaps into, in the underside (skull-facing) face
    reb = (cq.Workplane("XY", origin=(0, 0, z0))
           .polyline(_band(cl, -REBATE_W / 2, REBATE_W / 2)).close().extrude(REBATE_D))
    return body.cut(reb)


def hm01p_arch(radius, z_centre, half_len_mm, rotate_deg):
    """One arch run -- sagittal or coronal -- swept on its fitted circle.

    `half_len_mm` is the arc length each side of the crown, and `rotate_deg` turns the arch
    into its plane: 0 for the sagittal (front-back), 90 for the coronal (left-right).
    """
    th = math.degrees(half_len_mm / radius)
    cl = _cl_arc(radius, z_centre, -th, th)
    body = (cq.Workplane("XY").polyline(_band(cl, -SEC_H / 2, SEC_H / 2))
            .close().extrude(SEC_W).translate((0, 0, -SEC_W / 2)))
    for off in (-CH_PITCH / 2.0, +CH_PITCH / 2.0):
        bore = (cq.Workplane("XY").polyline(_band(cl, -CH_BORE / 2, CH_BORE / 2))
                .close().extrude(CH_BORE)
                .translate((0, 0, off - CH_BORE / 2)))
        body = body.cut(bore)
    reb = (cq.Workplane("XY").polyline(_band(cl, SEC_H / 2 - REBATE_D, SEC_H / 2))
           .close().extrude(REBATE_W).translate((0, 0, -REBATE_W / 2)))
    body = body.cut(reb)
    body = body.rotate((0, 0, 0), (1, 0, 0), 90)
    if rotate_deg:
        body = body.rotate((0, 0, 0), (0, 0, 1), rotate_deg)
    return body


def hm01p_sagittal():
    """The sagittal run, on the circle fitted to the v1 bore centres, 105 mm each side."""
    return hm01p_arch(HM01_SAG_R, HM01_SAG_ZC, 105.0, 0.0)


def hm01p_coronal():
    """The coronal run, on its fitted circle, 80 mm each side of the crown."""
    return hm01p_arch(HM01_COR_R, HM01_COR_ZC, 80.0, 90.0)


# THREE PARTS, NOT ONE, and the reason is worth stating because the first attempt got it
# wrong.  hm01p() unioned the halo and the two arches into a single "frame".  It printed as
# TWO DISCONNECTED BODIES, which a mesh check caught: the fitted centrelines do not meet.
# The sagittal arch ends at 91.7 mm horizontal and z 43.0, the coronal at 69.3 and z 52.3,
# and the halo plane is z 14.79 -- both arches finish some 28 mm ABOVE the ring and never
# touch it.  That is not a modelling slip; the three centrelines were fitted independently
# to the v1 mesh to place the three cover strips, and nothing ever required them to join.
#
# So these are the three channel RUNS, each a valid solid with the section the harness
# needs, and they are emitted separately.  Joining them into a monocoque needs the real
# head surface between them, and that surface is what DSN-EEG-002 section 12 objection 3
# holds until the Stage 0 fit measurement is taken.  Three correct runs and an honest gap
# is worth more than one part that cannot be printed.


# --------------------------------------------------------------------------- HM-10
# Protected 18650 assembly envelope.  AVL-EEG-017 K16 is OPEN WITH CRITERIA: the pack is not a
# catalogue part but a pack-builder assembly of a Panasonic NCR18650B or Samsung INR18650-35E
# cell, a Seiko S-8261-class PCM and a tab-welded JST PHR-2 lead, so there is no drawing to
# copy.  These are the figures that bound any such pack -- the IEC 61960 18650 cell is
# 18.50 mm diameter and 65.20 mm long at maximum material, and the PCM, its insulator and the
# heat-shrink sleeve add 5.80 mm of length and 0.10 mm of radius.  The first pack has to be
# measured at goods-in against this pocket before the carrier is released for the fleet.
CELL_D = 18.60          # over the sleeve
CELL_L = 71.00          # cell + PCM + insulator + sleeve, maximum material
CELL_BORE = 19.00       # 0.40 mm diametral clearance
CELL_POCKET = 71.30     # 0.30 mm axial clearance


def hm10():
    """HM-10 keyed 18650 cell carrier.  Class A safety part (RFQ S-04, REG-EEG-012 section 7).

    RFQ S-04 wants the cell mechanically retained and impossible to insert reversed.  Two
    facts decide how that is done.  The cell is not a bare cell: AVL-EEG-017 K16 buys a
    **protected pack with a tab-welded JST PHR-2 lead**, and both conductors leave the pack at
    the PCM end.  And the pack is loaded end-on through the HM-08 hatch, whose three lugs sit
    on a 38.0 x 27.4 mm ellipse, so the aperture behind it passes a 19 mm cylinder.

    **The key is the lead, and it is a lead slot at one end of the carrier and nowhere else.**
    The carrier is a 19.00 mm bore, 71.30 mm deep pocket in a 25.00 mm tube.  The far end is a
    solid 3.00 mm wall whose only opening is a Ø3.00 mm vent.  The mouth has a 6.00 x 5.00 mm
    slot in its rim, and the pack's twin lead leaves through it on its way to J13.  Loaded the
    right way round the pack bottoms on the end wall with its + button clear in a Ø7.00 mm
    relief, so the vent is never loaded, and the lead reaches J13.  Loaded end-for-end the
    lead is inside a closed pocket with no way out: a JST PHR-2 pair does not pass a Ø3.00 mm
    vent, so **the pack cannot be connected at all**, and the empty lead slot and the empty
    witness window say so before anyone tries.  That is the deterministic half of the key.

    The dimensional half is smaller and is stated as such.  Reversed, the trapped lead holds
    the pack off the end wall by at least one conductor diameter (1.15 mm, the thinnest PVC
    primary in WH-EEG-008 section 4) and the + button now stands at the mouth, adding 1.10 mm
    more, against 0.30 mm of pocket clearance: about **1.95 mm proud**.  HM-08's lugs are
    2.50 mm tall, so that is close but not certain to stop the hatch, which is why the lead
    exit and not the length is what this part relies on.

    Retention, the other half of S-04, is two integral snap fingers at the mouth with a
    1.20 mm barb on a 2.50 mm hook face, so any pack from 68.8 to 71.3 mm is held.  Each
    finger is an 18.0 x 7.0 x 1.80 mm cantilever: deflecting it 1.20 mm to let a pack past
    needs 3.6 N and puts 17 MPa in the root, against about 48 MPa for MJF PA12.  The hatch
    clamps the pack end and the four M3 feet hold the carrier to the enclosure floor.

    **What this does not do.**  It keys the pack, not the cell.  A bare cell is symmetric
    except for a 1.10 mm button, and no passive one-piece holder can stop one going in
    backwards on length alone.  A pack built with its lead at the wrong end would fit, and the
    K16 goods-in check is the only thing that catches that.  S-04's cell thermistor is still
    not met by anything: there is no NTC net in design.py and no thermistor way on J12 or J13,
    so nothing in this part or anywhere else reads a cell temperature.

    **It does not fit POD-P1-01 as drawn, and the base is not this file's to change.**  The
    carrier is 23.5 mm tall.  The enclosure floor is covered by the 150 x 130 mm carrier
    board, which leaves 4.0 mm each side inside the 158 x 138 mm internal envelope; the space
    under the board is 8.5 mm and the space above the MP-01 plate is 24.9 mm with the modules
    in it.  POD-P1-01 has no HM-08 aperture and no bosses for these feet either.  Both are
    open items against the enclosure.
    """
    od, wall, endw = CELL_BORE + 6.0, 3.0, 3.0          # 25.00 mm over a 3.00 mm wall
    ln = CELL_POCKET + endw                              # 74.30 mm overall, axis along +X
    r, br, flat = od / 2, CELL_BORE / 2, -11.0

    b = cq.Workplane("YZ").circle(r).extrude(ln)
    b = b.cut(cq.Workplane("YZ", origin=(endw, 0, 0)).circle(br).extrude(ln))
    # flat underside, so it stands on the enclosure floor.  It is cut at -11.00 and not at
    # the bore, which is tangent at -9.50: that leaves a 1.50 mm floor under the pocket and
    # makes the carrier 23.50 mm tall overall.
    b = b.cut(cq.Workplane("XY", origin=(ln / 2, 0, flat - 10.0))
              .box(ln + 4, od + 4, 10.0, centered=(True, True, False)))
    # positive-button relief in the closed end wall.  The button is 5.50 mm across and stands
    # 1.10 mm proud, so Ø7.00 x 2.00 mm clears it and the vent is never loaded
    b = b.cut(cq.Workplane("YZ", origin=(endw - 2.0, 0, 0)).circle(3.5).extrude(2.0))
    # vent through the closed end: a pack that swells must be able to push air out of a
    # blind 19.00 mm pocket, and Ø3.00 mm is too small for the JST lead to escape through
    b = b.cut(cq.Workplane("YZ", origin=(-1, 0, 0)).circle(1.5).extrude(endw + 2))
    # THE KEY: lead slot in the mouth rim, at the open end and nowhere else
    b = b.cut(cq.Workplane("XY", origin=(ln - 5.0, 0, 8.0))
              .box(5.0 + 2.0, 6.0, r + 2, centered=(False, True, False)))
    # witness window, so the two conductor colours can be read with the hatch off
    b = b.cut(cq.Workplane("XY", origin=(ln - 36.0, 0, 8.0))
              .box(25.0, 5.0, r + 2, centered=(False, True, False)))
    # two snap fingers at the mouth, one each side; slotted out of the wall and thinned
    for sy in (-1, 1):
        for sz in (-1, 1):
            b = b.cut(cq.Workplane("XY", origin=(ln - 18.0, sy * 9.0, sz * 4.5))
                      .box(18.0 + 2, 8.0, 2.0, centered=(False, True, True)))
        b = b.cut(cq.Workplane("XY", origin=(ln - 18.0, sy * (br + 1.8 + 3.0), -4.0))
                  .box(18.0 + 2, 6.0, 8.0, centered=(False, True, False)))
        b = b.union(cq.Workplane("XY", origin=(ln - 5.0, sy * (br - 0.6), -3.0))
                    .box(2.5, 1.2, 6.0, centered=(False, True, False)))
    # four M3 feet, two a side on 45.0 mm centres, for bosses POD-P1-01 has still to grow.
    # They run inboard to y = +/-5.00 so that they meet the tube on the flat and are part of
    # the same solid rather than four pads floating beside it.
    for sy in (-1, 1):
        b = b.union(cq.Workplane("XY", origin=(7.0, sy * 13.25, flat))
                    .box(60.0, 16.5, 3.0, centered=(False, True, False)))
        for xc in (14.5, 59.5):
            b = b.cut(cq.Workplane("XY", origin=(xc, sy * 17.0, flat - 1.0))
                      .circle(1.7).extrude(5.0))
    # a flat on the side to carry the section 4.1 mark: 1.50 mm off the 25.00 mm tube.  It
    # stops 22.0 mm short of the mouth so that it does not thin either snap finger, and it is
    # only 14.0 mm tall so that it does not cut through the foot underneath it
    mx0, mx1 = 4.0, ln - 22.0
    b = b.cut(cq.Workplane("XY", origin=((mx0 + mx1) / 2, 11.0, 0))
              .box(mx1 - mx0, 4.0, 14.0, centered=(True, False, True)))
    txt, size = MARKING["HM-10_keyed_cell_carrier"]
    b = _engrave(b, txt, _face(((mx0 + mx1) / 2, 11.0, 0), normal=(0, 1, 0),
                               xdir=(-1, 0, 0)), size)
    return b


# --------------------------------------------------------------------------- HM-05B
def hm05b():
    """HM-05B cup bayonet carrier: the printed part that holds the bought-in sintered Ag/AgCl
    cup (HM-05A) and turns in the HM-04 bore.  Eight fitted, two spare.

    Every dimension comes off hm04() and hm09() above, because those are the two parts it has
    to work with:

      * body Ø9.10 x 8.60 mm for HM-04's Ø9.20 x 9.00 mm bore -- 0.10 mm diametral clearance
        and 0.40 mm of axial take-up.  FIT-01 gates that fit at 9.20 / 9.35 / 9.15 mm;
      * a Ø6.60 x 3.50 mm spigot on top for HM-04's Ø6.80 x 4.50 mm spring seat, which is what
        the compression spring works against;
      * a Ø2.40 mm passage on the axis, under HM-04's Ø2.50 mm gel port, so a blunt syringe
        reaches the cup without the carrier being removed;
      * two bayonet lugs 1.40 mm wide x 2.10 mm tall standing 0.65 mm proud at r = 4.55 mm
        (outer radius 5.20), at 0 and 180 deg and 1.20 to 3.30 mm above the underside, so
        that they pass through hm04()'s two 2.30 x 1.70 x 3.60 mm entry slots and turn into
        its 100 deg run;
      * two drive notches 1.50 mm wide x 2.60 mm deep cut radially into the underside rim,
        **at 90 deg to the lugs**, which is what hm09()'s two 2.00 x 1.20 x 2.20 mm tip lugs
        at r = 4.20 mm engage.  That 90 deg is the whole sequence: the carrier goes in with
        its lugs in the HM-04 slots, turns a quarter, and its notches are then under those
        slots, which is the only way the key can reach it.  The key comes from the skull
        side; nothing a finger can reach turns it, which is why HM-09 is operator-only;
      * a 1.60 x 0.80 mm slot in the flank for the WH-01 conductor's solder tag, which
        WH-EEG-008 H6 pull-tests at 15 N.

    **The cup pocket is provisional.**  7.00 x 3.00 mm deep is the 9.10 mm body less a
    1.05 mm wall each side, and the wall is what sets it: the drive notches cut that wall in
    two places, so it carries the whole release torque.  HM-05A is a bought-in sintered cup
    "modified for the service bayonet" and the modification has never been drawn, so the
    pocket is sized by what is left rather than by the cup, and it has to be re-cut to the
    cup once one is chosen.

    **The bayonet turns, as of 2 September 2026.**  It did not before, and the reason is
    recorded here because the failure was invisible to every check the package had.  hm04()
    cut a straight 2.40 mm entry pocket and no circumferential run behind it, so the carrier
    went in and could not rotate: a plug fit, not a bayonet.  This docstring said so and the
    run was never added.  Two more faults compounded it: the entry slot was 1.40 mm wide for
    a 1.40 mm lug, zero clearance in a material printed to +/-0.15 mm; and the lug itself sat
    at r 5.40 rather than the 5.20 this docstring claims, because the 0.40 mm of union
    overlap was added to the box WIDTH without being taken off its CENTRE.  The mesh and the
    docstring disagreed by 0.20 mm and the mesh is what gets printed.

    What it is now: lug 1.40 mm wide standing 0.65 mm proud at r 4.55 (outer 5.20), raised
    to z 1.20..3.30 so it comes to rest ON the retaining lip rather than inside it; HM-04's
    entry slots 1.70 mm wide with an outer radius of 5.55; a 100 deg circumferential run at
    z 1.10..3.80 with 1.10 mm of lip below it.  The run's ceiling clears the carrier's full
    0.40 mm of axial float, because that float is the travel the cup makes when it is
    pressed against the scalp, not slack.

    tools/simulate_production.py measures the boolean at four rotations and three axial
    positions.  A drawing would not have caught any of this; an intersection volume does.
    """
    d, h = 9.10, 8.60
    c = cq.Workplane("XY").circle(d / 2).extrude(h)
    c = c.union(cq.Workplane("XY", origin=(0, 0, h)).circle(6.60 / 2).extrude(3.50))
    c = c.cut(cq.Workplane("XY", origin=(0, 0, -1)).circle(2.40 / 2).extrude(h + 5.5))
    c = c.cut(cq.Workplane("XY", origin=(0, 0, -0.1)).circle(7.00 / 2).extrude(3.00))
    # bayonet lugs at 0 and 180 deg, 0.15 to 2.25 mm above the underside, so they pass
    # through hm04()'s two 2.40 mm deep entry slots and no higher
    for a in (0.0, math.pi):
        # The box is 0.4 mm wider than the lug so it buries into the body and unions
        # cleanly.  That 0.4 mm used to be added to the WIDTH without being taken off the
        # CENTRE, which pushed the lug to r = 5.40 against a docstring that says 5.20 --
        # 0.10 mm of interference with hm04()'s 5.30 mm slot, so the carrier could not
        # enter at all.  Centre = d/2 + proud/2 - buried/2.
        # The lug sits at z 1.20..3.30, not 0.15..2.25.  A bayonet lug has to come to rest
        # ON TOP of the retaining lip, and a lug starting 0.15 mm above the underside
        # leaves room for a lip 0.15 mm thick, which is one printed layer.  Raised to
        # 1.20 gives HM-04 a 1.10 mm lip to carry the whole weight of an inverted helmet.
        LUG_PROUD, LUG_BURIED, LUG_Z0, LUG_H = 0.65, 0.40, 1.20, 2.10
        c = c.union(cq.Workplane("XY",
                    origin=(d / 2 + LUG_PROUD / 2 - LUG_BURIED / 2, 0, LUG_Z0))
                    .box(LUG_PROUD + LUG_BURIED, 1.40, LUG_H, centered=(True, True, False))
                    .rotate((0, 0, 0), (0, 0, 1), math.degrees(a)))
    # HM-09 drive notch, at 90 deg to the lugs.  One straight slot across the axis is both
    # notches.  90 deg is the whole sequence: the carrier enters with its lugs in the HM-04
    # slots, turns a quarter, and its notches are then under those slots, which is where the
    # key's tip lugs come through.
    c = c.cut(cq.Workplane("XY", origin=(0, 0, -0.1))
              .box(1.50, d + 3, 2.60, centered=(True, True, False)))
    # solder-tag slot in the flank, above everything the key touches
    c = c.cut(cq.Workplane("XY", origin=(0, d / 2 - 0.4, 5.60)).box(1.60, 1.60, 0.80,
                                                                    centered=(True, True, False)))
    return c


# --------------------------------------------------------------------------- HM-02B / HM-02C
def _tpu_pad(length, width, aperture=None):
    """The HM-02A section, reused: 8.00 mm thick, R6.00 in plan, R2.50 on the crown, and a
    1.50 mm deep x 8.00 mm wide retention groove in the underside inset 7.50 mm from each end.
    Only the plan size changes between the four pads, which is what makes them one family and
    one process."""
    p = cq.Workplane("XY").box(length, width, 8.0, centered=(True, True, False))
    p = p.edges("|Z").fillet(6.0)
    p = p.faces(">Z").fillet(2.5)
    p = p.faces("<Z").workplane(invert=True).rect(length - 15.0, 8.0).cutBlind(-1.5)
    if aperture:
        p = p.cut(cq.Workplane("XY", origin=(0, 0, -1)).rect(aperture, aperture).extrude(12.0))
    return p


def hm02b_occiput():
    """HM-02B TPU comfort pad, occiput.  Two fitted, two spare, replaced every turnaround.

    Same section as HM-02A -- 22.00 mm wide, 8.00 mm thick, R6.00 in plan, R2.50 crown, and
    the same 8.00 x 1.50 mm retention groove -- because they are one family printed or cast in
    one TPU 85A tool, and only the plan length differs.  Length 50.00 mm: the occipital shell
    measures 116.0 mm across on the HM-01 mesh (x = -58.0 to +58.0), and two pads share it
    with a 16.0 mm web on the midline.

    **The reason recorded for that web has been corrected.**  It used to read "for the two
    cable entries OE-1 and OE-2, which WH-EEG-008 section 7 puts one either side of the
    midline", and the measurement in the HM-12 section below shows it cannot be that: the
    only channel mouth on the occiput opens downward into the shell cavity, on the far side
    of the wall these pads sit on, so the umbilicals never cross this face at all and the
    entries are in the shell floor.  No dimension of this pad moves -- the web is still
    16.00 mm and the pad is still 50.00 mm -- but the entries it used to be justified by are
    in the floor plate, 23.0 mm behind and 44 mm below the wall, and what the web is for is
    now an open question for this pad's own drawing.  The pad's curvature is not
    modelled: a TPU 85A pad 8 mm thick conforms to the shell it is pressed onto, and the seats
    it presses into are not in the v1 mesh.
    """
    return _tpu_pad((HM01_SHELL_W - 16.0) / 2.0, 22.0)


def hm02c_crown():
    """HM-02C TPU comfort pad, crown.  One fitted, one spare.

    Same family and same section as HM-02A and HM-02B.  Length 72.00 mm is the crown zone
    measured on the mesh: the sagittal arch stays within 5 mm of its apex over |y| <= 36.0 mm,
    and past that the pad would be standing on a falling arch.  Width 26.00 mm rather than
    22.00 mm so that the 13.00 mm aperture leaves a 6.50 mm web each side; the aperture clears
    the Cz electrode assembly, which hm04() makes 12.40 mm square, with 0.30 mm each side.
    """
    return _tpu_pad(72.0, 26.0, aperture=13.0)


# --------------------------------------------------------------------------- HM-03A
def hm03a_yoke():
    """HM-03A occipital yoke.  One per kit, fitted to the frame, not a kit accessory.

    ASM-EEG-007 section 4.5 fixes what it has to do: it goes into the two rear halo anchor
    pockets on M3 x 10 A2 screws into brass heat-set inserts at 0.50 N.m, and it must hold
    20 N for two hours without slipping.  Its span comes off the mesh.  At z = 14.79 mm the
    halo section is halo band up to azimuth 235 deg and from 305 deg, and occipital shell in
    between, so the two anchors sit at 235 and 305 deg on the fitted ellipse: (-46.5, -79.3)
    and (+46.5, -79.3), a 93.0 mm chord.  The yoke is the band across that arc, 20.00 mm tall
    and 4.00 mm thick, hanging from the measured underside of the halo at z = 11.20 mm.

    That section is chosen against the 20 N: as a simply supported beam over the 93.0 mm span,
    M = 465 N.mm, I = 106.7 mm^4, so the outer fibre sees 8.7 MPa against roughly 48 MPa for
    MJF PA12 -- a factor of 5.5, before any allowance for the print's layer orientation, which
    the bureau chooses and this file cannot.

    The anchor pads are 5.00 mm thick with Ø3.40 mm clearance holes, so an M3 x 10 leaves
    5.00 mm in the insert, which is what a standard 5.80 mm M3 heat-set insert wants.  **The
    anchor pockets are not in the v1 HM-01 mesh**, so the pad thickness is dimensioned by the
    screw and the insert rather than by the pocket, and it has to be checked against the
    pocket when the parametric frame exists.

    **The ratchet land is deliberately blank.**  HM-03B is meant to house HM-03C, and
    AVL-EEG-017 has no vendor for HM-03C, so its outline, its spindle, its fixing pattern and
    its band width are all unknown.  The yoke therefore presents a flat 36 x 22 mm land with
    no holes in it, to be drilled and slotted when the ratchet is chosen.  PARTS-EEG-019 also
    lists HM-03B as a printed dial housing with a POM pawl **and** HM-03C as a complete
    bought-in ratchet; one of those two is redundant and the package does not say which.
    """
    z0, z1, t = -8.80, 11.20, 4.00
    cl = _cl_ellipse(HM01_HALO_A, HM01_HALO_B, HM01_SHELL_T0, HM01_SHELL_T1, n=241)
    y = (cq.Workplane("XY", origin=(0, 0, z0))
         .polyline(_band(cl, -t / 2, t / 2)).close().extrude(z1 - z0))
    # anchor pads at the two ends, on top, with M3 clearance
    for (px, py), (nx, ny) in (cl[0], cl[-1]):
        ang = math.degrees(math.atan2(ny, nx))
        pad = (cq.Workplane("XY", origin=(px, py, z1 - 5.0))
               .box(16.0, 14.0, 5.0, centered=(True, True, False))
               .rotate((px, py, 0), (px, py, 1), ang))
        y = y.union(pad)
        y = y.cut(cq.Workplane("XY", origin=(px, py, z1 - 6.0)).circle(1.7).extrude(8.0))
    # blank ratchet land on the outside face at the midline
    y = y.union(cq.Workplane("XY", origin=(0, -98.8, (z0 + z1) / 2))
                .box(36.0, 8.0, z1 - z0, centered=(True, True, True)))
    txt, size = MARKING["HM-03A_occipital_yoke"]
    y = _engrave(y, txt, _face((0.0, -102.8, (z0 + z1) / 2), normal=(0, -1, 0),
                               xdir=(1, 0, 0)), size)
    return y


# --------------------------------------------------------------------------- POD-P1-04
def podp1_04():
    """POD-P1-04 harness P-clip.  One per clipped cable end: WH-01 and WH-02 at their pod-end
    housings, and the WH-09 module-end USB-B plug (WH-EEG-008 section 3.8 and section 6).

    WH-EEG-008 section 4 gives the jackets it has to hold: WH-01 is 4.30 mm nominal and
    4.60 mm maximum, WH-02 is 4.50 mm nominal, WH-09 is 4.00 to 4.50 mm.  One clip covers all
    three -- Ø4.80 mm bore, 1.60 mm band, 6.00 mm wide, with a 3.60 mm throat so it snaps over
    a 4.60 mm jacket and then grips it -- rather than three clips that look alike and are not.
    The throat is flared 45 deg so the cable can be pushed in without a tool at service, which
    is the same reason the service loop is tied with hook-and-loop and not a cable tie.

    The foot is 12.00 mm long with a Ø3.40 mm hole 10.00 mm from the bore axis, which clears
    the Ø8.00 mm boss it sits on: the pod bosses in pod_base() are Ø8.00 mm with a Ø2.50 mm
    hole for an M3 thread-forming screw driven straight into PA12.  **The bosses this clip
    screws to do not exist yet.**  WH-EEG-008 puts each one 40 mm behind its connector, and
    POD-P1-01 has only the four carrier bosses.  Adding them is enclosure work, not clip work.
    """
    bore, band, w = 4.80, 1.60, 6.00
    ro = bore / 2 + band
    c = cq.Workplane("XZ").circle(ro).extrude(w).translate((0, w / 2, 0))
    c = c.cut(cq.Workplane("XZ").circle(bore / 2).extrude(w + 2).translate((0, w / 2 + 1, 0)))
    # throat: a 3.60 mm gap at the top, flared so the cable can be pushed in by hand
    c = c.cut(cq.Workplane("XY", origin=(0, 0, bore / 2 - 0.4))
              .box(3.60, w + 2, ro + 2, centered=(True, True, False)))
    c = c.cut(cq.Workplane("XY", origin=(0, 0, ro - 0.6))
              .box(6.40, w + 2, 1.2, centered=(True, True, False)))
    # foot, tangent to the underside of the band
    c = c.union(cq.Workplane("XY", origin=(2.0, 0, -ro))
                .box(14.0, 8.0, 3.0, centered=(False, True, False)))
    c = c.cut(cq.Workplane("XY", origin=(10.0, 0, -ro - 1))
              .circle(1.7).extrude(5.0))
    return c


# ------------------------------------------------- HM-12, the two occipital umbilical entries
# WH-EEG-008 Rev B section 7 names two occipital entries -- OE-1 for the electrode cable
# WH-01 and OE-2 for the contact-light cable WH-02 -- and puts node N1 immediately inside
# them.  It gives no coordinate, no bore, no grommet, no bushing and no anchor for either,
# and MECH-EEG-020 sheet 3, the only released HM-01 drawing, is three silhouettes and an
# overall size with no internal feature on it at all.  So two 4.3 to 4.5 mm cables leave a
# printed monocoque, run 1500 mm to a pod that a participant moves, and nothing in the
# package says where they leave, through what, or what takes the pull; the 15 N site-end
# pull of WH-EEG-008 H6 has nothing to react against.  This section is that geometry.
#
# HM-01 itself cannot be given the feature here.  It is a carried-over v1 mesh with no
# parametric source (PARTS-EEG-019 OA-1), so nothing in this file can print a hole in it.
# What is done instead is what hm03a_yoke(), hm05b() and hm02b_occiput() already do --
# section the released mesh, dimension the mating part to what is measured, and say which
# figure came from where.  The result is one printed part, two bores that HM-01 has to
# carry, and a bought gland that the pod entries already need.
#
# **The route is not a preference; the released mesh leaves one way through.**  All three
# channel mouths at the occiput -- HM01_N1_MOUTH in the roof plate and HM01_HALO_MOUTH and
# its mirror in the wall -- open into the occipital shell cavity, so a conductor that is
# going to reach a channel has to be inside that cavity first.  There are two ways into the
# cavity: the open rear face and the floor plate.  The shell wall is not one of them -- the
# far side of that wall is the participant's occiput and the HM-02B pads sit on it, so an
# entry there would run the umbilical between the shell and the back of the head.  The floor
# is taken rather than the open rear face because the umbilical hangs downward to a bench
# pod: a floor entry costs the cable no bend at the frame at all, which matters against
# WH-01's 26 mm dynamic bend radius (WH-EEG-008 section 4), and it puts the entry hardware
# behind the neck rather than behind the head.
#
# What is NOT closed by this: the run from each entry to each mouth is stripped conductor
# hanging in an open cavity -- 85.1 mm to the roof mouth, 55.5 mm to the halo mouth on the
# same side and 77.4 mm to the one on the other side -- because the released frame has no
# channel, no clip and no pocket anywhere inside the shell.  WH-EEG-008 open item 16 (no
# geometry for WH-BUS-01 at N1) is the same gap seen from the other end, and section 7's
# "N1 immediately inside the occipital entry" does not describe the released frame: N1 is
# 55 to 85 mm from the entry, wherever in the cavity it is put.
OE_BORE_D = ENTRY_BORE_D            # 12.50: the same gland as the pod entries, deliberately
OE_PLATE_T = 2.0                    # doubler: 2.40 floor + 2.00 = 4.40 mm of panel
OE_X = 16.0                         # bore axes at x = -16.00 (OE-1) and +16.00 (OE-2)
OE_Y = (HM01_SHELL_Y_BACK + HM01_SHELL_Y_IN) / 2.0        # -103.01, mid-depth of the floor
OE_SEAT_D = ENTRY_PAD_D             # 22.00, the seat an assumed 17 mm locknut's corners need
OE_MARGIN = 4.0                     # plate material outboard of each seat
OE_PLATE_W = 2 * (OE_X + OE_SEAT_D / 2.0 + OE_MARGIN)     # 62.00
OE_PLATE_D = 2 * (OE_SEAT_D / 2.0 + OE_MARGIN)            # 30.00
OE_PLATE_R = 4.0                    # corner radius in plan
# Where each number comes from, since none of them is a choice made for looks:
#   OE_X       two locknuts and one spanner.  An assumed 17.00 mm across-flats nut is
#              19.63 mm across corners, so 32.00 mm between the axes leaves 12.37 mm of
#              clear space between the two nuts.  It is also over five times the 6.00 mm the
#              electrode and light groups have to be kept apart by (WH-EEG-008 section 7).
#   OE_Y       the middle of the floor plate's own 46.00 mm depth, so the plate cannot
#              overhang either edge and the clamp load is spread evenly on it.  It puts the
#              entries 20.60 mm behind the shell wall and 23.00 mm inside the open rear edge.
#   OE_PLATE_* the seat plus OE_MARGIN of material, twice, on each axis.
_OE_IN = (OE_X, OE_Y, HM01_SHELL_FLOOR_Z + HM01_SHELL_FLOOR_T)      # where a conductor
OE_TRUNK = math.dist(_OE_IN, HM01_N1_MOUTH)                         # enters the cavity
OE_TRUNK_HALO = math.dist(_OE_IN, HM01_HALO_MOUTH)
OE_TRUNK_HALO_FAR = math.dist(_OE_IN, (-HM01_HALO_MOUTH[0],) + HM01_HALO_MOUTH[1:])


def _oe_holds():
    """The clearances the OE features are placed on, checked rather than trusted, for the
    same reason _pod_holds() checks the pod's."""
    # (a) the plate stays on the floor plate that clamps it, with 2 mm to spare at each edge
    assert OE_PLATE_W / 2.0 <= HM01_SHELL_X - 2.0, "entry plate overhangs the shell in X"
    assert OE_Y + OE_PLATE_D / 2.0 <= HM01_SHELL_Y_IN - 2.0, "plate overhangs the front edge"
    assert OE_Y - OE_PLATE_D / 2.0 >= HM01_SHELL_Y_BACK + 2.0, "plate overhangs the rear edge"
    # (b) each seat keeps OE_MARGIN of plate around it
    assert OE_PLATE_W / 2.0 - OE_X - OE_SEAT_D / 2.0 >= OE_MARGIN - 1e-9, "seat near the edge"
    assert OE_PLATE_D / 2.0 - OE_SEAT_D / 2.0 >= OE_MARGIN - 1e-9, "seat near the edge"
    # (c) two locknuts, one spanner
    acorner = GLAND_LOCKNUT_AF / math.cos(math.radians(30.0))
    assert 2 * OE_X - acorner > 4.0, "the two locknuts foul each other"
    assert OE_SEAT_D >= acorner, "the seat is smaller than the locknut's corners"
    # (d) the separation WH-EEG-008 section 7 puts between the electrode and light groups
    assert 2 * OE_X >= CH_PITCH, "OE-1 and OE-2 are closer than the section 7 minimum"
    # (e) the panel one gland has to accept at BOTH ends of the same umbilical
    for panel in (POD_WALL + ENTRY_PAD_T, HM01_SHELL_FLOOR_T + OE_PLATE_T):
        assert GLAND_PANEL_MIN <= panel <= GLAND_PANEL_MAX, f"panel {panel:.2f} out of range"
    # (f) the locknut has room inside the cavity, and the bore does not break the plate
    assert OE_Y - HM01_SHELL_Y_OUT < -OE_SEAT_D / 2.0, "the locknut fouls the shell wall"
    assert OE_BORE_D / 2.0 + 1.0 < OE_SEAT_D / 2.0, "the seat is thinner than 1 mm"
    # (g) the trunk lengths this file quotes in prose are the model's own figures
    assert abs(OE_TRUNK - 85.1) < 0.05, "the quoted trunk length no longer matches the model"
    assert abs(OE_TRUNK_HALO - 55.5) < 0.05, "the quoted halo trunk no longer matches"
    assert abs(OE_TRUNK_HALO_FAR - 77.4) < 0.05, "the quoted far halo trunk no longer matches"


_oe_holds()


def oe_entry_plate():
    """HM-12 occipital umbilical entry plate.  One per helmet.

    **The identifier is a proposal, not an allocation.**  PARTS-EEG-019 Rev B section 1.2
    allocates HM-01 to HM-11 and reserves HM-12 to HM-19 for Phase 2; this is a Phase 1
    part, so it takes the next free number in the series and the register owner has to
    confirm HM-12 or issue another.  It is also why the part carries no engraved mark: a
    number the register has not issued must not go onto hardware, and MARKING gains the row
    when the number does.  Change the key in PARTS and REGISTER and regenerate if the
    register answers differently; no dimension moves.

    **What it is.**  A flat 62.00 x 30.00 x 2.00 mm plate with two Ø12.50 mm bores 32.00 mm
    apart, held against the underside of the occipital shell floor by the two cable glands
    that pass through it.  Nothing bonds it and nothing screws it: the two threads locate it
    and clamp it, so there is no adhesive joint to qualify -- which is what WH-ADP-03 and
    WH-ADP-04 have to live with on the pod wall -- and it comes off with the glands at
    service.

    **What it is for**, in the order the jobs matter:

      * it doubles the panel at the entry.  The shell floor is 2.40 mm of PA12 (measured)
        and a Ø12.50 hole through it with a locknut pulled down on it is a thin section
        around a large hole in a printed part.  With the plate the gland clamps 4.40 mm,
        which is also inside the 1 to 6 mm panel range a gland of this class quotes;
      * it fixes where the two holes are.  Until a parametric HM-01 exists the holes have to
        be made in the print, and this plate is the drill jig for them: set on the floor to
        the dimensions below, clamped, and both bores opened through it, which is also the
        only way the two ends of the same bore stay concentric;
      * it gives the jacket 4.40 mm of bore to bear in instead of 2.40 mm.

    **What it does not do**, stated because an assembler will otherwise assume it.  It does
    not anchor the conductors between the entry and N1.  The gland clamps the jacket, so a
    pull at a site end is reacted at the frame and is not carried down the umbilical to the
    pod, which is what WH-EEG-008 H6 needs; what stays unanchored is the stripped conductor
    between the gland and the three channel mouths inside the shell cavity -- 55.5 mm to the
    halo mouth on the same side, 77.4 mm to the one on the other side and 85.1 mm to the
    rear sagittal mouth in the roof -- and nothing in the released frame anchors any of it.

    The locknut bears directly on the 2.40 mm floor while the plate takes the flange side.
    If the first article shows the nut embedding in the PA12, the answer is a second plate
    on the cavity side or a stainless washer under the nut; that is a first-article decision
    and it is not taken here.

    **The two bores HM-01 has to carry**, in frame coordinates, because this is the file
    that fixes them:

        OE-1   x = -16.00, y = -103.01    WH-01, the 12-way screened electrode cable
        OE-2   x = +16.00, y = -103.01    WH-02, the 10-way contact-light cable
        Ø12.50 mm through the floor plate, z = -56.00 to -53.60, axis vertical.

    WH-EEG-008 section 7 puts OE-1 left of the midline and OE-2 right of it.  **No document
    in this package states which way the frame's +x points**, so OE-1 is put on -x here; if
    the frame convention turns out to be the other way the two swap, and nothing else moves,
    because the plate is symmetrical and the glands are identical.

    The plate is modelled about its own centre, like every other printed part in this file.
    It is fitted centred on (0.00, -103.01) with its top face on the floor underside at
    z = -56.00, so its own bores land on OE-1 and OE-2.
    """
    p = cq.Workplane("XY").box(OE_PLATE_W, OE_PLATE_D, OE_PLATE_T, centered=(True, True, False))
    p = p.edges("|Z").fillet(OE_PLATE_R)
    for sx in (-1.0, 1.0):
        p = p.cut(cq.Workplane("XY", origin=(sx * OE_X, 0.0, -1.0))
                  .circle(OE_BORE_D / 2.0).extrude(OE_PLATE_T + 2.0))
    return p


# --------------------------------------------------------------------------- foam
def foam_dxf(path, layer=1):
    """One layer of the CASE-00 **Rev C** foam stack, 1:1 in millimetres, for die-cutting
    or laser-cutting.  One call writes one layer, so a bay is drawn here only if the
    schedule cuts it through this layer.

    The schedule is PKG-EEG-015 Rev B section 2.2, "CASE-00 Rev C -- the schedule that will
    be cut", transcribed field for field: seven loose-laid 25 mm closed-cell PE layers on a
    516.0 x 390.0 mm sheet, 175 mm of stack, nine bays, layer 1 uppermost, datum at the
    bottom-left corner of the sheet with X to the right and Y up.

    CASE-00 Rev B -- two 25 mm sheets on 340 x 250 mm, eleven pockets -- cannot be emitted
    from here any more, and writing layer 1 deletes the two Rev B files if it finds them.
    PKG-EEG-015 section 2.4 records why they are dead: five of the eleven pockets are
    smaller than the part their legend names, every pocket is a through-cut in a single
    25 mm sheet against parts 62, 80 and 158 mm tall, and the helmet bay alone needs more
    sheet than the Rev B sheet has.  A superseded cut file left beside a live one is
    eventually cut.

    What this file states that the Rev C table does not, and where it comes from:

      * the **corner radii**.  The table gives no radius.  These are the radii of the Rev B
        cut file, which took them from package v1: R40 on the helmet bay because the frame
        is domed, R10 on the two large equipment bays and on the ear-clip bay, R8 on the
        rest, R14 on the sheet.
        Section 2.3 orders a steel-rule die at Phase 3 and steel rule cannot be folded to a
        true 90 degree inside corner, so a square profile either tears the foam or quietly
        becomes whatever radius the die maker chooses;
      * the **title block** and its placement, in the solid patch above the POD-P1 bay and
        in the bottom edge margin;
      * that **layers 5, 6 and 7 are the same cut** -- the helmet opening alone.  The table
        says seven layers and says which layers each bay is cut through; that three of them
        come out identical is arithmetic, not a decision.

    Everything else -- legend, origin, size, layers cut, relief centre -- is the table's.

    Two things the schedule leaves open and this file does not invent.  The **packers**,
    the plain uncut PE pads that make up the difference between a part and the 25 mm
    granularity of the stack, are not drawn: the table gives a thickness for two of the
    nine bays (POD-P1 10 mm, HEADPHONES 17 mm) and "at the trial pack" for the other six,
    and no packer outline anywhere.  And the **finger reliefs** are drawn exactly where the
    table puts them, which is wholly inside the bay opening -- see `_relief` below.
    """
    import ezdxf

    n = layer
    if isinstance(n, str):
        if n in ("top", "bottom"):
            raise ValueError(
                "CASE-00 Rev B ('top' / 'bottom') is withdrawn -- PKG-EEG-015 section 2.4. "
                "Call foam_dxf(path, n) with a Rev C layer number, 1 to 7.")
        n = int(n)
    if n not in range(1, 8):
        raise ValueError(f"CASE-00 Rev C is seven layers, 1 to 7; asked for {layer!r}")

    # Sheet: PKG-EEG-015 section 2.1, "the Peli 1560's published 518 x 392 mm internal
    # footprint minus 2 mm on each axis".  Published, not measured: section 3.2 holds the
    # cut file until the first shell has been measured in the base and in the lid.
    W, H = 516.0, 390.0
    SHEET_R = 14.0
    THICK, N_LAYERS = 25.0, 7
    EDGE, WEB, RELIEF_D = 14.0, 8.0, 22.0

    # (legend, x, y, w, h, first layer cut, last layer cut, corner radius, relief centre)
    BAYS = [
        ("HELMET HM-01",                14.0,  14.0, 197.0, 236.0, 1, 7, 40.0, None),
        ("HEADPHONES",                 219.0,  14.0, 181.0, 161.0, 1, 4, 10.0, (309.0,  28.0)),
        ("POD-P1 ENCLOSURE",           219.0, 183.0, 169.0, 149.0, 1, 3, 10.0, (303.0, 197.0)),
        ("BOOM MICROPHONE",             14.0, 258.0, 197.0,  58.0, 1, 2,  8.0, (112.0, 272.0)),
        ("SPARE CUPS + KEYLESS SPARES", 14.0, 324.0,  96.0,  52.0, 1, 2,  8.0, ( 62.0, 338.0)),
        ("SPARE CELL",                 118.0, 324.0,  93.0,  52.0, 1, 2,  8.0, (164.0, 338.0)),
        ("CONSUMABLES",                408.0,  14.0,  94.0, 140.0, 1, 3,  8.0, (455.0,  28.0)),
        ("EAR CLIPS + EMG LEADS",      408.0, 162.0,  94.0, 100.0, 1, 2, 10.0, (455.0, 176.0)),
        ("CABLES + CHARGER",           408.0, 270.0,  94.0, 106.0, 1, 3,  8.0, (455.0, 284.0)),
    ]
    # The helmet bay is the only opening that changes with the layer.  In layer 1 it is cut
    # 8 mm smaller all round, 181 x 220 from (22, 22); that 8 mm ledge is the shelf the
    # HM-01 halo rim lands on and it is the only load path in the pack.  Layers 2 to 7 are
    # the full 197 x 236 opening, so the electrode cups hang in the void and touch nothing.
    SHELF = (22.0, 22.0, 181.0, 220.0)

    def _layout_holds():
        """The three rules PKG-EEG-015 section 2.2 states for this layout, checked against
        the transcribed table rather than trusted: 14 mm to the sheet edge, 8 mm of web
        between bays, and every bay at least 3 mm larger than its part.  The third is only
        checkable for the three bays whose part is dimensioned in the package, so it is
        checked there and stated as unknown elsewhere."""
        assert EDGE + 197.0 + WEB + 181.0 + WEB + 94.0 + EDGE == W, "X does not close"
        assert EDGE + 236.0 + WEB + 58.0 + WEB + 52.0 + EDGE == H, "Y does not close"
        for legend, x, y, w, h, _f, _l, r, relief in BAYS:
            assert r <= min(w, h) / 2.0, legend
            assert x >= EDGE and y >= EDGE, legend
            assert x + w <= W - EDGE and y + h <= H - EDGE, legend
            if relief:
                cx, cy = relief
                assert (x <= cx - RELIEF_D / 2.0 and cx + RELIEF_D / 2.0 <= x + w
                        and y <= cy - RELIEF_D / 2.0 and cy + RELIEF_D / 2.0 <= y + h), legend
        for i, a in enumerate(BAYS):
            for b in BAYS[i + 1:]:
                dx = max(a[1] - (b[1] + b[3]), b[1] - (a[1] + a[3]))
                dy = max(a[2] - (b[2] + b[4]), b[2] - (a[2] + a[4]))
                assert max(dx, dy) >= WEB, f"{a[0]} / {b[0]} web is {max(dx, dy):.1f} mm"
        # the three bays whose part is dimensioned: 3 mm clearance on both plan axes
        # The pod's external footprint is read from this module's own POD_OW and POD_OH,
        # which pod_base() builds the enclosure from, so the bay is tied to the part it
        # holds: grow the pod past 166 x 146 mm and this assertion stops the cut file being
        # written rather than letting a 169 x 149 bay be cut for a pod that no longer fits
        # it.  The fallback is the published 163.0 x 143.0 of PKG-EEG-015 section 1.2.
        # 191.1 x 229.6 is HM-01 standing on the halo, DSN-EEG-002 Rev E section 11.  The
        # ATH-M20x folded envelope is PKG-EEG-015 section 2.4's "about 175 x 155 x 80" and
        # is the one of the three that has been read off a datasheet rather than a model.
        for legend, part_w, part_h in (("HELMET HM-01", 191.1, 229.6),
                                       ("POD-P1 ENCLOSURE",
                                        float(globals().get("POD_OW", 163.0)),
                                        float(globals().get("POD_OH", 143.0))),
                                       ("HEADPHONES", 175.0, 155.0)):
            b = next(x for x in BAYS if x[0] == legend)
            assert b[3] - part_w >= 3.0 and b[4] - part_h >= 3.0, legend

    _layout_holds()

    doc = ezdxf.new("R2010")
    doc.units = 4       # millimetres
    msp = doc.modelspace()
    # Two layers, and only two: CUT is cut through, TEXT is marked.  Rev A also declared
    # an ENGRAVE layer that nothing ever drew on, which invites a cutter to quote a third
    # operation that does not exist.
    doc.layers.add("CUT", color=1)
    doc.layers.add("TEXT", color=5)

    def rounded(x, y, w, h, r, layer="CUT"):
        """A closed rounded rectangle, drawn as an LWPOLYLINE with bulged corners.

        Corner radii are not decoration.  PKG-EEG-015 section 2.3 orders a steel-rule die
        for Phase 3, and steel rule cannot be folded to a true 90 degree inside corner --
        a square profile either tears the foam or quietly becomes a radius the die maker
        chooses.  Package v1 specified these radii; package v2 Rev A drew every profile
        square and stated none.  Restored under ECO-EEG-016 section 2A, C-18.
        """
        r = max(0.0, min(r, w / 2, h / 2))
        if r == 0:
            msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
                               close=True, dxfattribs={"layer": layer})
            return
        b = 0.41421356237      # tan(45/2): a 90-degree arc as a polyline bulge
        pts = [(x + r, y, 0, 0, 0),          (x + w - r, y, 0, 0, b),
               (x + w, y + r, 0, 0, 0),      (x + w, y + h - r, 0, 0, b),
               (x + w - r, y + h, 0, 0, 0),  (x + r, y + h, 0, 0, b),
               (x, y + h - r, 0, 0, 0),      (x, y + r, 0, 0, b)]
        msp.add_lwpolyline(pts, format="xyseb", close=True,
                           dxfattribs={"layer": layer})

    def _text(s, x, y, height=4.0):
        msp.add_text(s, dxfattribs={"layer": "TEXT", "height": height}).set_placement((x, y))

    def _relief(centre):
        """A finger relief, drawn where the schedule puts it.

        Every relief centre in the Rev C table is at least 3 mm inside its own bay opening,
        so the circle falls entirely within material that the bay profile already removes
        and it cuts nothing.  It is drawn anyway, because the schedule is the authority and
        this file must not quietly differ from it, and the defect is recorded in
        PKG-EEG-015 sections 2.2 and 9 rather than fixed by guesswork here.  It cannot be
        fixed by moving the circle outwards either: a relief that straddles a bay wall
        needs 11 mm of foam beyond it and every web in this layout is 8 mm.  The two ways
        out -- a scallop cut in the first uncut layer beneath the bay, or a re-columned
        sheet with wider webs -- are Rev D questions and the trial pack decides them.
        """
        msp.add_circle(centre, RELIEF_D / 2.0, dxfattribs={"layer": "CUT"})

    rounded(0, 0, W, H, SHEET_R)
    cut = [b for b in BAYS if b[5] <= n <= b[6]]
    for legend, x, y, w, h, _f, _l, r, relief in cut:
        if legend == "HELMET HM-01" and n == 1:
            x, y, w, h = SHELF          # the 8 mm halo shelf
        rounded(x, y, w, h, r)
        _text(legend, x + 4.0, y + h - 9.0, 5.0)
        if relief:
            _relief(relief)

    # The cut file carries its own identity and revision.  A DXF on a cutter's screen is
    # cut off from the register that names it, and five of the seven layers share a size.
    ident = f"CASE-00-0{n}"
    same = " -- layers 5, 6 and 7 are the same cut" if n >= 5 else ""
    for i, line in enumerate((
            f"{ident}  FOAM LAYER {n} OF {N_LAYERS}  Rev C  --  EEG FIELD KIT",
            f"{THICK:.0f} mm CLOSED-CELL PE, 28-33 kg/m3  --  SHEET {W:.1f} x {H:.1f} mm",
            f"STACK {THICK * N_LAYERS:.0f} mm, SEVEN LOOSE-LAID LAYERS, LAYER 1 UPPERMOST",
            f"{len(cut)} of the 9 bays of PKG-EEG-015 section 2.2 are cut here{same}",
            "CC BY-SA 4.0  --  one.witysk.org")):
        _text(line, 223.0, 370.0 - 7.5 * i, 3.5)
    _text("CUT is cut through this layer.  TEXT is not an output layer -- nothing on it is "
          "cut or engraved; the bay legends are the printed tags ART-LBL-04.", 16.0, 8.5, 3.5)
    _text("Sheet = the MEASURED case internal footprint minus 2 mm on each axis.  516.0 x "
          "390.0 is the published Peli 1560 figure; no shell has been measured.", 16.0, 2.5, 3.5)

    # A superseded cut file left in mech/ is eventually cut, so the two CASE-00 Rev B files
    # are removed rather than left beside the Rev C stack.  Once, with layer 1.
    if n == 1:
        for dead in ("CASE-00_foam_top_layer.dxf", "CASE-00_foam_bottom_layer.dxf"):
            dead = os.path.join(os.path.dirname(os.path.abspath(path)), dead)
            if os.path.exists(dead):
                os.remove(dead)

    # The register row for this layer is written from the same schedule that cut it.  Seven
    # hand-written rows can drift from the cut file; a generated one cannot, and CASE-00 is
    # the one released mechanical file whose row changes with its layer number.
    stem = _stem(path)
    REGISTER[stem] = dict(
        part_id=ident, name=f"foam insert, layer {n} of {N_LAYERS}", revision="C",
        material=f"{THICK:.0f} mm closed-cell PE, 28-33 kg/m3",
        process="die-cut or laser-cut, CUT and TEXT layers",
        description=(f"foam insert layer {n} of {N_LAYERS}, {W:.1f} x {H:.1f} mm sheet, "
                     f"{len(cut)} of the 9 bays of the PKG-EEG-015 section 2.2 Rev C "
                     f"schedule; sheet size is published, not measured"),
        source="tools/mech_gen.py foam_dxf()")
    UNMARKED[stem] = f"{ident} Rev C in the TEXT layer"

    doc.saveas(path)
    return path


# ------------------------------------------------------------------- WH-KEY-01, WH-ADP
# The harness parts.  Everything from here to the driver belongs to WH-EEG-008 Rev B: the
# keying shroud that stands over the two helmet-harness sockets, and the three printed
# panel adapters its pigtails terminate on.  None of it has been printed or measured.
#
# Two of the five WH-ADP adapters are NOT modelled because they are bought parts and a
# printed stand-in for them would be a fiction: WH-ADP-01 and WH-ADP-01B are a 3.5 mm
# 4-conductor panel jack with its own nut and sealing washer, specified by class in
# WH-EEG-008 section 3.9.

# Raised marks, not cut ones.  ICD-EEG-006 section 6.1 asks for the socket designator
# "raised on its outer face", so these parts are embossed where MP-01 and HM-08 are
# engraved; the depth rule of PARTS-EEG-019 section 4.1 is read as 0.40 mm of relief
# either way.  They are recorded in UNMARKED, which is the manifest's marking field for
# anything MARKING does not engrave.
EMBOSS_PROUD = 0.40
EMBOSS_SINK = 0.20      # the glyph starts inside the wall so the union is manifold


def _one_solid(part, what):
    """A raised mark laid over a pocket or a window comes off as a loose solid, and an STL
    made of two bodies still reports watertight.  Every part in this section is checked
    here instead, on the solid, before it is exported."""
    n = len(part.val().Solids())
    assert n == 1, f"{what} came out as {n} solids, not one"
    return part


def _emboss(part, txt, plane, size=3.0, proud=EMBOSS_PROUD, sink=EMBOSS_SINK):
    """Raise `txt` off `plane` by `proud`, and return the marked part.

    `plane` sits `sink` inside the face, so the glyph solid always shares material with
    the part.  Text laid over a pocket or a window would come off as a loose solid, so
    every caller places it over material and `_one_solid()` checks the result is one body.
    """
    g = cq.Workplane(plane).text(txt, size, proud + sink, combine=False,
                                 font=ENGRAVE_FONT, kind="bold")
    return part.union(g)


# --------------------------------------------------------------------------- WH-KEY-01
# Everything here is derived from parts that already exist:
#
#   PITCH, and the socket body and pad sizes   fplib.pinsocket_1xn(): pads 1.6 mm on a
#                                              2.54 mm pitch, insulator body x -1.27..+1.27,
#                                              so a 1xN socket is 2.54 mm wide by N x 2.54
#                                              mm long
#   SOCK_MATE_H                                ICD-EEG-006 section 4, which budgets "8.5 mm
#                                              of socket mating height" under MP-01
#   the 18.0 mm ceiling                        ICD-EEG-006 section 4, carrier top to MP-01
#                                              underside
#
# and from two dimensions of the mating housing that the package does NOT carry, which are
# named here so that the part regenerates when they are measured:
KEY_PITCH = 2.54            # design.py / fplib.pinsocket_1xn
SOCK_BODY_W = 2.54          # fplib.pinsocket_1xn body: x -1.27 .. +1.27
SOCK_MATE_H = 8.50          # ICD-EEG-006 section 4
PLATE_GAP = 18.00           # ICD-EEG-006 section 4: carrier top to MP-01 underside

# ---- the two unconfirmed inputs -------------------------------------------------------
# WH-EEG-008 section 6 specifies a Harwin M20 polarised male crimp housing at J14, J30 and
# J22 and confirms the ordering suffix at IQC.  Its body width and the length its male
# contacts stand proud of the mating face are not in this package and have not been
# measured, so the shroud is cut for the figures below and MUST be reprinted from a
# measured housing before a build: a cavity 0.3 mm narrower than the housing will not
# accept the cable at all, and one 0.5 mm wider stops keying it.
M20_HSG_W = 4.20            # housing body across the flats -- UNCONFIRMED
M20_PIN_PROUD = 4.00        # male contact protrusion below the mating face -- UNCONFIRMED
# and one dimension the shroud imposes on the housing rather than taking from it:
M20_KEY_MIN = 0.70          # polarising rib, proud of the body, at the way-1 end

KEY_CAV_W = M20_HSG_W + 0.30        # 4.50: the housing enters, a reversed rib does not
KEY_CAV_END = 0.20                  # end clearance per end -> 0.40 total, well under a pitch
KEY_WALL = 1.20                     # MJF PA12; the thinnest wall on any part in this file
KEY_DEPTH = 1.00                    # keyway into the wall, 0.30 clear of M20_KEY_MIN
KEY_SLOT_L = 2.60                   # one pitch + 0.06, so the rib may sit anywhere in way 1
KEY_H = SOCK_MATE_H + M20_PIN_PROUD  # 12.50, engaged before the contacts touch
KEY_LEAD_IN = 0.60                  # chamfer at the mouth
KEY_GRIP = 2.50                     # between the locating ribs, on a 2.54 mm socket body

# Which side of the socket the keyway is cut on is a board-clearance decision, not a
# preference, and it is recorded per form because the harness housing has to match it:
#   J14 (5.0, 12.0)   FID1 sits at x = 10.0 mm and the board edge at x = 0, so the keyway
#                     goes on +X and the shroud runs x = 1.55 to 9.45 mm, 0.55 mm clear of
#                     the fiducial and 1.55 mm inside the board edge
#   J30 (66.0, 90.0)  R70's pad starts at x = 70.53 mm, so the keyway goes on -X and the
#                     shroud runs x = 61.55 to 69.45 mm, 1.08 mm clear of R70
#   J22 (30.0, 116.0, rotated 90 deg)  local +X is board +Y, which is open to the board
#                     edge at y = 130 mm
KEY_FORMS = [
    ("J14", 12, +1, "helmet electrode cable WH-01"),
    ("J30", 10, -1, "helmet contact-light cable WH-02"),
    ("J22", 3, +1, "EOG panel option, Phase 2 only"),
]


def _key_checks():
    """The three fits this part exists to make, checked at generation.

    They are arithmetic on the constants above, not measurements: nothing has been
    printed and no housing has been in a shroud.
    """
    assert KEY_CAV_W - M20_HSG_W >= 0.20, "the housing will not enter"
    assert M20_HSG_W + M20_KEY_MIN - KEY_CAV_W >= 0.30, "a reversed housing still enters"
    assert 2 * KEY_CAV_END < KEY_PITCH, "the housing can sit one way out"
    assert KEY_DEPTH - M20_KEY_MIN >= 0.20, "the rib bottoms out before the housing seats"
    assert KEY_H < PLATE_GAP, "the shroud fouls MP-01 before the cable does"
    assert KEY_GRIP < SOCK_BODY_W, "the shroud is loose on the socket"


def wh_key01(ways, key_x=+1, designator="J14"):
    """WH-KEY-01, the printed keying shroud, in the form for a 1xN carrier socket.

    A rectangular tube that drops over the socket strip and stands 4.0 mm proud of it, so
    that it has hold of the harness housing before the male contacts reach the socket.  It
    is the only mitigation WH-EEG-008 section 6 carries against the one safety-relevant
    mis-mate in the kit -- WH-01 reversed, which puts the driven BIAS_EL output onto a
    protected scalp electrode -- so what it blocks and what it does not is worth stating:

      * **reversal is blocked.**  The keyway is a 2.60 x 1.00 mm slot in one long wall at
        the way-1 end.  Right way round the housing's polarising rib enters it; turned end
        for end the rib meets a flat wall and the housing needs 4.90 mm of a 4.50 mm
        cavity.  This works only if the housing carries a rib at least 0.70 mm proud
        within the first way, which is a requirement this part places ON the bought
        housing and which no housing has yet been measured against.
      * **an offset of one way is blocked.**  The cavity is the housing length plus
        0.40 mm and is closed at both ends; a pitch is 2.54 mm.
      * **a shorter housing dropped into a longer shroud is NOT blocked.**  A 10-way WH-02
        housing is 25.4 mm long and will enter the 30.9 mm cavity of the J14 form.  Way
        count alone does not prevent it either, and WH-EEG-008 section 6's claim that the
        two helmet cables "physically cannot be swapped" holds only in the one direction.
        What catches it is the pin-by-pin read-back at step 8 and test H9, not this part.

    Retention is a pair of locating ribs each side, closing to 2.50 mm on the socket's
    2.54 mm body below the mating face, plus a bead of adhesive at the rim.  MJF PA12
    holds about +/-0.30 mm on a feature this size, so the ribs locate the shroud and the
    adhesive holds it; neither has been tested.
    """
    _key_checks()
    n = ways
    y0, y1 = -1.27 - KEY_CAV_END, (n - 1) * KEY_PITCH + 1.27 + KEY_CAV_END
    ymid = (n - 1) * KEY_PITCH / 2.0
    x_key = KEY_CAV_W / 2 + KEY_WALL + KEY_DEPTH
    x_pln = KEY_CAV_W / 2 + KEY_WALL
    x_lo, x_hi = (-x_pln, x_key) if key_x > 0 else (-x_key, x_pln)

    b = (cq.Workplane("XY", origin=((x_lo + x_hi) / 2, (y0 + y1) / 2, 0))
         .rect(x_hi - x_lo, (y1 - y0) + 2 * KEY_WALL).extrude(KEY_H))
    # the cavity is open top and bottom: the shroud drops over a socket already soldered
    b = b.cut(cq.Workplane("XY", origin=(0, (y0 + y1) / 2, -1.0))
              .rect(KEY_CAV_W, y1 - y0).extrude(KEY_H + 2))
    # keyway, over way 1 only, full height so the rib can slide down it
    kx = key_x * (KEY_CAV_W / 2 + KEY_DEPTH / 2)
    b = b.cut(cq.Workplane("XY", origin=(kx, 0.0, -1.0))
              .rect(KEY_DEPTH, KEY_SLOT_L).extrude(KEY_H + 2))
    # lead-in at the mouth, on the cavity and on the keyway
    for ox, w, l in ((0.0, KEY_CAV_W, y1 - y0), (kx, KEY_DEPTH, KEY_SLOT_L)):
        oy = (y0 + y1) / 2 if ox == 0.0 else 0.0
        b = b.cut(cq.Workplane("XY", origin=(ox, oy, KEY_H - KEY_LEAD_IN)).rect(w, l)
                  .workplane(offset=KEY_LEAD_IN)
                  .rect(w + 2 * KEY_LEAD_IN, l + 2 * KEY_LEAD_IN).loft(ruled=True))
    # locating ribs, below the 8.5 mm mating face so they never touch the housing
    proj = (KEY_CAV_W - KEY_GRIP) / 2.0
    rib_ys = [KEY_PITCH] if n < 6 else [KEY_PITCH, (n - 2) * KEY_PITCH]
    for ry in rib_ys:
        for s in (-1, 1):
            b = b.union(cq.Workplane("XY", origin=(s * (KEY_CAV_W / 2 - proj / 2), ry, 1.0))
                        .rect(proj, 2.0).extrude(SOCK_MATE_H - 2.0))
    # marks.  The identifier goes on the plain long wall, the designator on the way-1 end
    # wall, where it is also the pin-1 mark.  The J22 form's wall is 10.4 mm long and will
    # not hold "WH-KEY-01" at a legible size, so it carries the designator twice and the
    # MECH-EEG-020 sheet says so rather than implying PARTS 4.1 is met.
    s = -key_x
    wall_len = (y1 - y0) + 2 * KEY_WALL
    ident = "WH-KEY-01" if wall_len - 2.0 > 0.62 * 4.2 * len("WH-KEY-01") else designator
    b = _emboss(b, ident, _face((s * (x_pln - EMBOSS_SINK), ymid, KEY_H / 2),
                                normal=(s, 0, 0), xdir=(0, s, 0)), 4.2)
    b = _emboss(b, designator, _face((0.0, y0 - KEY_WALL + EMBOSS_SINK, KEY_H / 2),
                                     normal=(0, -1, 0), xdir=(1, 0, 0)), 4.2)
    return _one_solid(b, f"WH-KEY-01 {designator} form")


# ------------------------------------------------------------------------- WH-ADP-02
def wh_adp02():
    """WH-ADP-02, the room-microphone carrier, 32.0 x 24.0 x 3.0 mm.

    Bonded to the inside of the POD-P1 wall behind the 4.0 mm acoustic port at carrier
    (122.0, 102.0).  The port, the gasket recess and the seal recess are dimensioned from
    that opening, which `PANEL` in this file cuts at 4.0 mm diameter.

    The module it carries is the open item, not the plate: RFQ E-15 wants the mute to be a
    hardware gate in the signal path and **no catalogue module is known to meet it**
    (WH-EEG-008 section 3.5), so no hole pattern is known either.  The plate therefore does
    what MP-01 does for the same reason -- a grid, not a drilled pattern: six M2.5
    clearance holes on an 8 mm grid, of which any small breakout picks up at least two, and
    two 6.0 x 2.5 mm tie slots for one that picks up none.  That is deliberately crude and
    it is what the unqualified module leaves available.
    """
    W, H, T = 32.0, 24.0, 3.0
    p = cq.Workplane("XY").box(W, H, T, centered=(True, True, False)).edges("|Z").fillet(3.0)
    p = p.cut(cq.Workplane("XY", origin=(0, 0, -1)).circle(2.0).extrude(T + 2))   # port
    # gasket recess, wall side: a die-cut silicone washer seals the plate to the pod wall
    p = p.cut(cq.Workplane("XY", origin=(0, 0, T - 0.8)).circle(5.0).extrude(1.0))
    # seal recess, module side: the capsule's own gasket seals the capsule to the plate
    p = p.cut(cq.Workplane("XY", origin=(0, 0, -0.001)).circle(5.0).extrude(0.8))
    for x, y in ((-12, -8), (-12, 8), (-4, 8), (4, 8), (12, -8), (12, 8)):
        p = p.cut(cq.Workplane("XY", origin=(x, y, -1)).circle(1.35).extrude(T + 2))
    for x in (-13.0, 13.0):
        p = p.cut(cq.Workplane("XY", origin=(x, 0, -1)).slot2D(6.0, 2.5, 90).extrude(T + 2))
    p = _emboss(p, "WH-ADP-02", _face((0.0, -9.0, EMBOSS_SINK), normal=(0, 0, -1)), 3.0)
    return _one_solid(p, "WH-ADP-02")


# ------------------------------------------------------------------- WH-ADP-03, -04
def wh_adp_usb(gasketed):
    """WH-ADP-03 (charge) and WH-ADP-04 (host): the panel USB-C receptacle clamp plate.

    Both POD-P1 openings are 10.0 x 4.0 mm rectangles in a 2.5 mm wall, from `PANEL`:
    the charge port at carrier (143.0, 80.0) and the host port at (146.0, 12.0).  A USB-C
    receptacle nose fills that opening, so nothing of this plate can sit in it and the
    plate works from behind: a 2.4 mm-wide picture-frame rim lands on the inside of the
    wall, the receptacle's mounting flange is trapped inside the rim, and the plate is
    bonded to the wall.  The 14.0 x 8.0 mm window passes the receptacle body and its
    wires.

    The rim accepts **any** flange up to 24.0 x 14.0 mm and 1.6 mm thick, rather than being
    cut to one receptacle, because no receptacle is bought: the class is a panel-mount
    USB-C 2.0 receptacle with a two-hole flange and solder cups or a short pigtail, with
    the two 5.1 kOhm CC pull-downs fitted (WH-EEG-008 sections 3.7 and 3.8).  Its nose must
    stand at least 2.5 mm proud of the flange to reach through the wall -- 3.3 mm on
    WH-ADP-04, which carries a 0.8 mm gasket in front of the flange -- and that has not
    been confirmed against a part.

    WH-ADP-04 differs in two ways, both because it is on the host side of the ADuM4160
    barrier: the rim is 0.8 mm deeper for the flange gasket of WH-EEG-008 section 3.8, and
    a 2.0 mm skirt stands round the window on the pod side, which adds 4.0 mm to the
    surface path from the receptacle's own terminals to anything bonded to the pod wall.
    PA12 is not conductive and the plate carries no insert, so nothing in it can be the
    bond the isolator exists to prevent.

    The two M2.5 clearance holes are for screws into POD-P1 bosses **that do not exist**:
    pod_base() puts bosses on the floor only.  Until they do, both plates are bonded, and
    test H6's 50 N pull on the panel receptacle is a pull on a bonded joint that has not
    been made or tested.
    """
    W, H, T = 34.0, 20.0, 3.0
    rim = 2.4 if gasketed else 1.6
    skirt = 2.0 if gasketed else 0.0
    p = cq.Workplane("XY").box(W, H, T, centered=(True, True, False)).edges("|Z").fillet(2.5)
    fr = (cq.Workplane("XY", origin=(0, 0, T)).rect(W, H).extrude(rim)
          .edges("|Z").fillet(2.5))
    fr = fr.cut(cq.Workplane("XY", origin=(0, 0, T - 1.0)).rect(24.0, 14.0).extrude(rim + 2))
    p = p.union(fr)
    p = p.cut(cq.Workplane("XY", origin=(0, 0, -skirt - 1.0)).rect(14.0, 8.0)
              .extrude(T + rim + skirt + 2))
    for x in (-14.5, 14.5):
        p = p.cut(cq.Workplane("XY", origin=(x, 0, -1)).circle(1.35).extrude(T + rim + 2))
    if gasketed:
        sk = cq.Workplane("XY", origin=(0, 0, -skirt)).rect(18.0, 12.0).extrude(skirt)
        sk = sk.cut(cq.Workplane("XY", origin=(0, 0, -skirt - 1.0)).rect(14.0, 8.0)
                    .extrude(skirt + 2))
        p = p.union(sk)
    ident = "WH-ADP-04" if gasketed else "WH-ADP-03"
    p = _emboss(p, ident, _face((0.0, -7.0, EMBOSS_SINK), normal=(0, 0, -1)), 3.0)
    return _one_solid(p, ident)


# --------------------------------------------------------------------------- driver
PARTS = [
    ("MP-01_module_plate", mp01),
    ("POD-P1_prototype_enclosure_base", pod_base),
    ("POD-P1_prototype_enclosure_lid", pod_lid),
    ("HM-04_electrode_assembly_body", hm04),
    ("HM-08_battery_hatch", hm08),
    ("HM-09_service_key", hm09),
    ("HM-02_brow_pad", hm02_brow),
    ("FIT-01_fit_test_coupon", fit01),
    # Nine parts the packing list names and no file existed for.  Five more are still
    # missing on purpose -- HM-03B, HM-06A, HM-06B, HM-07A and POD-P1-05 -- for the
    # reasons given above hm11a_halo(); nothing in the package dimensions them.
    ("HM-02B_occiput_pad", hm02b_occiput),
    ("HM-02C_crown_pad", hm02c_crown),
    ("HM-03A_occipital_yoke", hm03a_yoke),
    ("HM-05B_cup_bayonet_carrier", hm05b),
    ("HM-10_keyed_cell_carrier", hm10),
    ("HM-01P-A_channel_run_halo", hm01p_halo),
    ("HM-01P-B_channel_run_sagittal", hm01p_sagittal),
    ("HM-01P-C_channel_run_coronal", hm01p_coronal),
    ("HM-11A_channel_cover_halo", hm11a_halo),
    ("HM-11B_channel_cover_sagittal", hm11b_sagittal),
    ("HM-11C_channel_cover_coronal", hm11c_coronal),
    ("POD-P1-04_harness_p_clip", podp1_04),
    # v2.3: the helmet end of both umbilicals, which had no entry and no strain relief at
    # all.  The identifier is proposed and not yet issued -- see oe_entry_plate().
    ("HM-12_occipital_umbilical_entry_plate", oe_entry_plate),
]

# Every released mechanical file, with the identity PARTS-EEG-019 Rev B section 2 gives it.
# The revision letter belongs to the part, not to the package, so it is carried here beside
# the model that defines it and is what MARKING engraves into the part.  The last two rows
# are not built here -- HM-01 is the v1 mesh carried over and EEG-CAR-01 is written by
# tools/emit_extras.py -- but they are released files and the manifest has to cover them.
REGISTER = {
    "MP-01_module_plate": dict(
        part_id="MP-01", name="module mounting plate", revision="B",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="module mounting plate, 3.0 mm, 8 mm border, jumper slot field",
        source="tools/mech_gen.py mp01()"),
    "POD-P1_prototype_enclosure_base": dict(
        part_id="POD-P1-01", name="prototype enclosure base", revision="B",
        material="PA12", process="MJF (FDM PETG for Phase 1 form studies only)",
        description="prototype enclosure base, gasket groove, carrier and lid bosses, "
                    "two M12 gland harness entries, RFQ M-02 panel",
        source="tools/mech_gen.py pod_base()"),
    "POD-P1_prototype_enclosure_lid": dict(
        part_id="POD-P1-02", name="prototype enclosure lid", revision="B",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="prototype enclosure lid, 4.0 mm plate with a 2.0 mm locating spigot, "
                    "four M3 clearance holes on the base boss pattern",
        source="tools/mech_gen.py pod_lid()"),
    "HM-04_electrode_assembly_body": dict(
        part_id="HM-04", name="electrode assembly body", revision="B",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="electrode assembly body, 8 fitted + 2 spare per kit",
        source="tools/mech_gen.py hm04()"),
    "HM-08_battery_hatch": dict(
        part_id="HM-08", name="battery hatch", revision="B",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="battery hatch, quarter-turn, three lugs, coin slot, seal groove",
        source="tools/mech_gen.py hm08()"),
    "HM-09_service_key": dict(
        part_id="HM-09", name="service key", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="cup service key, one per operator, NOT in the participant kit",
        source="tools/mech_gen.py hm09()"),
    "HM-02_brow_pad": dict(
        part_id="HM-02A", name="brow pad", revision="A",
        material="TPU 85A", process="printed or cast",
        description="brow pad, consumable, replaced at every turnaround",
        source="tools/mech_gen.py hm02_brow()"),
    "FIT-01_fit_test_coupon": dict(
        part_id="FIT-01", name="fit-test coupon", revision="A",
        material="PA12", process="MJF, printed in the same build as the batch it qualifies",
        description="fit-test coupon, three bores at 9.20, 9.35 and 9.15 mm",
        source="tools/mech_gen.py fit01()"),
    "HM-02B_occiput_pad": dict(
        part_id="HM-02B", name="comfort pad, occiput", revision="A",
        material="TPU 85A", process="printed or cast, one tool family with HM-02A",
        description="occiput pad, 2 fitted + 2 spare, consumable, replaced every turnaround",
        source="tools/mech_gen.py hm02b_occiput()"),
    "HM-02C_crown_pad": dict(
        part_id="HM-02C", name="comfort pad, crown", revision="A",
        material="TPU 85A", process="printed or cast, one tool family with HM-02A",
        description="crown pad, 1 fitted + 1 spare, 13.0 mm aperture over the Cz assembly",
        source="tools/mech_gen.py hm02c_crown()"),
    "HM-03A_occipital_yoke": dict(
        part_id="HM-03A", name="occipital yoke", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="occipital yoke, 93.0 mm anchor span; the ratchet land is blank because "
                    "HM-03C has no vendor and no outline",
        source="tools/mech_gen.py hm03a_yoke()"),
    "HM-05B_cup_bayonet_carrier": dict(
        part_id="HM-05B", name="cup bayonet carrier", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="cup bayonet carrier, 8 fitted + 2 spare; the cup pocket is provisional "
                    "because the HM-05A cup modification has never been drawn",
        source="tools/mech_gen.py hm05b()"),
    "HM-10_keyed_cell_carrier": dict(
        part_id="HM-10", name="keyed 18650 cell carrier", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="keyed cell carrier: lead-slot polarity key, two snap fingers, four M3 "
                    "feet. Class A, RFQ S-04. Does not fit POD-P1-01 as drawn",
        source="tools/mech_gen.py hm10()"),
    "HM-01P-A_channel_run_halo": dict(
        part_id="HM-01P-A", name="channel run, halo", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="the halo run with the section WH-EEG-008 section 7 needs: 12.20 mm "
                    "wide, two 3.80 mm channels at 6.00 mm centres inside 1.20 mm walls, "
                    "and a 10.10 x 2.10 mm rebate for HM-11A",
        source="tools/mech_gen.py hm01p_halo()"),
    "HM-01P-B_channel_run_sagittal": dict(
        part_id="HM-01P-B", name="channel run, sagittal arch", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="the sagittal run, same section, on the circle fitted to the v1 bore "
                    "centres; 105 mm of arc each side of the crown",
        source="tools/mech_gen.py hm01p_sagittal()"),
    "HM-01P-C_channel_run_coronal": dict(
        part_id="HM-01P-C", name="channel run, coronal arch", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="the halo and the sagittal and coronal arches, drawn parametrically on "
                    "the centrelines fitted to the v1 HM-01 mesh, with the SECTION the "
                    "harness needs: 12.20 mm wide, two 3.80 mm channels at 6.00 mm centres "
                    "inside 1.20 mm walls, and a 10.10 x 2.10 mm rebate for the HM-11 cover "
                    "strips. The v1 halo band is 10.91 mm with ONE bore and no rebate, so it "
                    "cannot take its own harness; this is the section that can. It is a "
                    "channel correction and NOT an ergonomic re-design: the head-shape "
                    "surfaces still come from the v1 study and move when the Stage 0 fit "
                    "measurement of DSN-EEG-002 section 12 is taken",
        source="tools/mech_gen.py hm01p()"),
    "HM-11A_channel_cover_halo": dict(
        part_id="HM-11A", name="channel cover strip, halo", revision="A",
        material="PA12", process="MJF, printed with HM-01",
        description="halo channel cover strip, 9.80 x 1.60 mm lipped section; the v1 HM-01 "
                    "has no rebate for it and its band is 1.29 mm too narrow",
        source="tools/mech_gen.py hm11a_halo()"),
    "HM-11B_channel_cover_sagittal": dict(
        part_id="HM-11B", name="channel cover strip, sagittal arch", revision="A",
        material="PA12", process="MJF, printed with HM-01",
        description="sagittal channel cover strip, 105.0 mm of arc each side of the crown; "
                    "the rear 70 mm of the WH-EEG-008 run is inside the occipital shell",
        source="tools/mech_gen.py hm11b_sagittal()"),
    "HM-11C_channel_cover_coronal": dict(
        part_id="HM-11C", name="channel cover strip, coronal arch", revision="A",
        material="PA12", process="MJF, printed with HM-01",
        description="coronal channel cover strip, 80.0 mm of arc each side of the crown",
        source="tools/mech_gen.py hm11c_coronal()"),
    "POD-P1-04_harness_p_clip": dict(
        part_id="POD-P1-04", name="harness P-clip", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="harness P-clip, 4.00 to 4.60 mm jacket range, 3 per kit for WH-01, "
                    "WH-02 and WH-09; the bosses it screws to are not in POD-P1-01 yet",
        source="tools/mech_gen.py podp1_04()"),
    "HM-12_occipital_umbilical_entry_plate": dict(
        part_id="HM-12", name="occipital umbilical entry plate", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="occipital umbilical entry plate: the OE-1 and OE-2 gland entries of "
                    "WH-EEG-008 section 7, clamped to the shell floor by the two glands "
                    "themselves. IDENTIFIER PROPOSED -- PARTS-EEG-019 has not issued it",
        source="tools/mech_gen.py oe_entry_plate()"),
    # CASE-00 has no literal row here.  The insert is CASE-00 Rev C, seven layers, and
    # each layer's row -- which bays it carries, how many of the nine they are -- is
    # written by foam_dxf() from the same PKG-EEG-015 section 2.2 schedule that cuts it,
    # so the row and the cut file cannot drift.  The two Rev B rows, "top layer" and
    # "bottom layer" on a 340 x 250 mm sheet, are deleted with the files they described.
    "HM-01_frame_monocoque": dict(
        part_id="HM-01", name="frame monocoque", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description="helmet frame monocoque, carried over from package v1 unchanged",
        source="package/mech/HM-01_frame_monocoque.stl, copied by tools/emit_extras.py"),
    "HARDWARE_SCHEDULE": dict(
        part_id="--", name="fixing hardware schedule", revision="--",
        material="--", process="--",
        description="every insert, screw, standoff, gland and cord the released geometry "
                    "needs, each size derived from the feature it goes into and each vendor "
                    "choice left OPEN WITH CRITERIA",
        source="tools/mech_gen.py hardware_schedule()"),
    "MECH_RELEASE_STATUS": dict(
        part_id="--", name="mechanical release status", revision="--",
        material="--", process="--",
        description="what tools/mech_gen.py releases as geometry, what is deliberately not "
                    "modelled, and which register rows still record the released parts as "
                    "unmade",
        source="tools/mech_gen.py release_status()"),
    "EEG-CAR-01_RevB_board_outline": dict(
        part_id="EEG-CAR-01", name="carrier board outline", revision="B",
        material="FR-4 Tg >= 150, ENIG", process="PCB fabrication to the Gerber X2 set",
        description="carrier board envelope solid, for fit checks only; not the fab drawing",
        source="tools/emit_extras.py board_step()"),
}

UNMARKED = {
    "HM-04_electrode_assembly_body": "none -- too small; bag label at kitting (PARTS 4.1)",
    "HM-05B_cup_bayonet_carrier": "none -- 9.10 x 8.60 mm, too small; bag label at kitting "
                                  "(PARTS 4.1)",
    "HM-02B_occiput_pad": "none -- too soft; bag label at kitting (PARTS 4.1)",
    "HM-02C_crown_pad": "none -- too soft; bag label at kitting (PARTS 4.1)",
    "POD-P1-04_harness_p_clip": "none -- the 14 x 8 mm foot is under the 20 x 8 mm face "
                                "PARTS 4.1 asks for; bag label at kitting",
    "HM-12_occipital_umbilical_entry_plate":
        "none -- the identifier is a proposal and PARTS-EEG-019 has not issued it. A number "
        "the register has not allocated must not be engraved into hardware; the mark is cut "
        "when the number is issued (PARTS 4.1). Bag label at kitting until then",
    "HM-11A_channel_cover_halo": "none -- the only exposed face is the 9.80 mm skull-facing "
                                 "surface, and a 0.40 mm recess there lies against the "
                                 "scalp; bag label at kitting",
    "HM-11B_channel_cover_sagittal": "none -- as HM-11A; bag label at kitting",
    "HM-11C_channel_cover_coronal": "none -- as HM-11A; bag label at kitting",
    "HM-02_brow_pad": "none -- too soft; bag label at kitting (PARTS 4.1)",
    "FIT-01_fit_test_coupon": "none -- bag label at kitting (PARTS 4.1)",
    "HM-01_frame_monocoque": "NOT MARKED -- PARTS 4.1 requires it; the carried-over v1 mesh "
                             "has no engraving. Arrives with the parametric model, OA-1",
    "EEG-CAR-01_RevB_board_outline": "white LPI legend on the board, not in this solid",
    "HARDWARE_SCHEDULE": "not a part -- a generated document",
    "MECH_RELEASE_STATUS": "not a part -- a generated document",
    # the seven CASE-00 Rev C layers are added here by foam_dxf(), with the register row
}


# WH-EEG-008's own printed parts are added to the build list and to the register here,
# after both are defined, so that the shroud -- one model in three forms -- does not have
# to be written out three times in the literal above.
PARTS += [(f"WH-KEY-01_shroud_{d}", (lambda w=n, k=s, dd=d: wh_key01(w, k, dd)))
          for d, n, s, _ in KEY_FORMS]
PARTS += [
    ("WH-ADP-02_room_microphone_carrier", wh_adp02),
    ("WH-ADP-03_charge_usb_c_plate", lambda: wh_adp_usb(False)),
    ("WH-ADP-04_host_usb_c_plate", lambda: wh_adp_usb(True)),
]

for _d, _n, _s, _what in KEY_FORMS:
    REGISTER[f"WH-KEY-01_shroud_{_d}"] = dict(
        part_id="WH-KEY-01", name=f"keying shroud, {_d} form", revision="A",
        material="PA12", process="MJF, bead-blast, dyed graphite",
        description=(f"printed keying shroud over the 1x{_n} socket {_d}, {_what}; "
                     f"keyway on {'+' if _s > 0 else '-'}X, cut for a housing body of "
                     f"{M20_HSG_W:.2f} mm that has not been measured"),
        source="tools/mech_gen.py wh_key01()")
    UNMARKED[f"WH-KEY-01_shroud_{_d}"] = (
        f"{'WH-KEY-01' if _n > 5 else _d} raised {EMBOSS_PROUD:.2f} mm on the long wall and "
        f"{_d} raised on the way-1 end wall (ICD-EEG-006 6.1)"
        + ("" if _n > 5 else "; the 10.4 mm wall will not hold WH-KEY-01 legibly, so this "
                             "form carries the designator twice and PARTS 4.1 is not met"))

REGISTER["WH-ADP-02_room_microphone_carrier"] = dict(
    part_id="WH-ADP-02", name="room microphone carrier", revision="A",
    material="PA12", process="MJF, bead-blast, dyed graphite",
    description="room-microphone carrier, 4.0 mm acoustic port, two gasket recesses and a "
                "six-hole M2.5 grid for a module that is not yet qualified",
    source="tools/mech_gen.py wh_adp02()")
REGISTER["WH-ADP-03_charge_usb_c_plate"] = dict(
    part_id="WH-ADP-03", name="charge USB-C panel plate", revision="A",
    material="PA12", process="MJF, bead-blast, dyed graphite",
    description="charge-port receptacle clamp plate, rim for a flange up to 24 x 14 x 1.6 mm, "
                "bonded to the pod wall because POD-P1 has no wall bosses",
    source="tools/mech_gen.py wh_adp_usb()")
REGISTER["WH-ADP-04_host_usb_c_plate"] = dict(
    part_id="WH-ADP-04", name="host USB-C panel plate", revision="A",
    material="PA12", process="MJF, bead-blast, dyed graphite",
    description="host-port receptacle clamp plate, 0.8 mm flange gasket and a 2.0 mm "
                "isolation skirt; every conductor it holds is on the host side of the barrier",
    source="tools/mech_gen.py wh_adp_usb()")
for _k in ("WH-ADP-02_room_microphone_carrier", "WH-ADP-03_charge_usb_c_plate",
           "WH-ADP-04_host_usb_c_plate"):
    UNMARKED[_k] = (f"{REGISTER[_k]['part_id']} raised {EMBOSS_PROUD:.2f} mm on the face "
                    f"that is not bonded to the pod wall (PARTS 4.1)")


def _stem(path):
    """The register key of a released file: the filename with its extension removed."""
    return os.path.basename(path).rsplit(".", 1)[0]


def _identity(stem):
    """The one-line identity stamped into a STEP header and an STL header block."""
    r = REGISTER.get(stem)
    if not r:
        return stem
    return f"{r['part_id']} {r['name']} Rev {r['revision']} -- EEG field kit -- CC BY-SA 4.0"


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _stamp_step(path, ident):
    """Write the part identity into the STEP header, in place.

    An exporter leaves FILE_NAME and PRODUCT saying "Open CASCADE Shape Model", so a STEP
    file opened on its own does not say which part it is or at what revision.  Only the
    first FILE_NAME field and the PRODUCT name are touched; the geometry is not reopened.
    """
    txt = _read_text(path)
    txt, n1 = re.subn(r"FILE_NAME\('[^']*'", f"FILE_NAME('{ident}'", txt, count=1)
    txt, n2 = re.subn(r"PRODUCT\('[^']*',\s*'[^']*'",
                      f"PRODUCT('{ident}',\n  '{ident}'", txt, count=1)
    assert n1 == 1 and n2 == 1, f"STEP header not recognised in {path}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    return True


def _stamp_stl(path, ident):
    """Write the part identity into the 80-byte header of a binary STL, in place.

    Returns False and leaves the file alone if it is not a binary STL.  The header must not
    begin with "solid" or a reader will try to parse the file as ASCII.
    """
    with open(path, "rb") as f:
        head = f.read(84)
    if len(head) < 84:
        return False
    ntri = int.from_bytes(head[80:84], "little")
    if os.path.getsize(path) != 84 + 50 * ntri:
        return False                                   # ASCII STL, or not an STL
    stamp = ident.encode("ascii", "replace")[:80].ljust(80, b" ")
    assert not stamp.lower().startswith(b"solid"), ident
    with open(path, "r+b") as f:
        f.write(stamp)
    return True


def manifest(outdir):
    """`mech/MANIFEST.json`: every released mechanical file with the properties goods-in
    has to check it against -- identity, revision, material, process, units, geometry,
    marking and SHA-256.  One generator, one schema (PARTS-EEG-019 OA-2).

    Model figures throughout.  No part has been printed, so nothing here has been measured
    on hardware; the bounding box is from the vertex extremes and the volume by the
    divergence theorem over the closed mesh.

    The two generated Markdown files in `mech/` are covered as well.  They are not parts and
    carry no geometry row, but they are released files that a goods-in check has to be able
    to verify, and there is one manifest rather than one per file type.
    """
    import trimesh
    files = {}
    for sub, ext in (("stl", ".stl"), ("step", ".step"), ("", ".dxf"), ("", ".md")):
        d = os.path.join(outdir, sub) if sub else outdir
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(ext):
                continue
            path = os.path.join(d, fn)
            stem = _stem(path)
            r = REGISTER.get(stem, {})
            row = {
                "part_id": r.get("part_id", "--"),
                "revision": r.get("revision", "--"),
                "description": r.get("description", "--"),
                "material": r.get("material", "--"),
                "process": r.get("process", "--"),
                "units": "mm/cm3" if ext != ".md" else "--",
                "marking": (f"{MARKING[stem][0]} engraved {ENGRAVE_DEPTH:.2f} mm deep, "
                            f"{MARKING[stem][1] * STROKE_PER_EM:.2f} mm stroke")
                           if stem in MARKING else UNMARKED.get(stem, "--"),
                "bytes": os.path.getsize(path),
                "sha256": _sha256(path),
                "source": r.get("source", "--"),
            }
            if ext == ".stl":
                m = trimesh.load(path)
                row.update({
                    "watertight": bool(m.is_watertight),
                    "bbox_mm": [round(float(v), 2) for v in m.extents],
                    "volume_cm3": round(float(m.volume) / 1000.0, 2),
                    "surface_cm2": round(float(m.area) / 100.0, 1),
                    "triangles": int(len(m.faces)),
                    "step": os.path.exists(os.path.join(outdir, "step", stem + ".step")),
                })
            elif ext == ".dxf":
                # CASE-00 Rev C sheet, PKG-EEG-015 section 2.1: the published case
                # internal footprint minus 2 mm on each axis, not yet measured
                row.update({"sheet_mm": [516.0, 390.0], "layers": ["CUT", "TEXT"]})
            files[os.path.join(sub, fn) if sub else fn] = row
    return {
        "document": "mech/MANIFEST.json",
        "generated_by": "tools/mech_gen.py manifest()",
        "schema": "PARTS-EEG-019 Rev B OA-2",
        "units": "mm/cm3",
        "note": "Model figures. No part has been printed, so no figure here has been "
                "verified against hardware. Filenames are as released: the two EEG-CAR-01 "
                "files carry RevB in the name and the other eight do not, which "
                "PARTS-EEG-019 section 1.3 rule 2 has still to settle.",
        "licence": "CC BY-SA 4.0",
        "files": files,
    }


# ------------------------------------------------------------------ generated schedules
# Two Markdown files, written from the constants above rather than typed beside them, for
# the reason LID_FIX exists: a figure that is written twice is a figure that will disagree
# with itself at the next revision.

def hardware_schedule():
    """`mech/HARDWARE_SCHEDULE.md`: every insert, screw, standoff, gland and cord the
    released mechanical geometry needs, with the size and length of each derived from the
    feature it goes into, and with every vendor choice left open and named as open."""
    corner = GLAND_LOCKNUT_AF / math.cos(math.radians(30.0))
    floor_under = POD_WALL + POD_FLOOR_BOSS_H - FLOOR_INSERT_DEPTH
    boss_wall = (POD_FLOOR_BOSS_D - INSERT_BORE_D) / 2.0
    lid_stack = POD_LID_T + POD_SPIGOT_T
    lid_gap = POD_DEPTH - POD_SPIGOT_T - LID_BOSS_TOP
    lid_engage = 12.0 - lid_stack - lid_gap
    board_t = Z_CARRIER_TOP - POD_WALL - POD_FLOOR_BOSS_H
    stud_min, stud_max = board_t + 3.0, board_t + FLOOR_INSERT_DEPTH
    plate_t = 3.0
    pod_panel = POD_WALL + ENTRY_PAD_T
    hm_panel = HM01_SHELL_FLOOR_T + OE_PLATE_T
    cord = 2.0 * ((POD_IW + POD_WALL) + (POD_IH + POD_WALL))
    return f"""# FIXING HARDWARE SCHEDULE -- EEG FIELD KIT, MECHANICAL PACKAGE

**File:** `mech/HARDWARE_SCHEDULE.md`
**Generated by:** `tools/mech_gen.py hardware_schedule()`, from the same constants that cut
the geometry in `mech/step/` and `mech/stl/`. Do not edit it by hand; change the model and
regenerate, or the schedule and the part it describes will disagree.
**Licence:** CC BY-SA 4.0

## Why this file exists

The released POD-P1-01 solid has eight {INSERT_BORE_D:.2f} mm insert bores, two
{ENTRY_BORE_D:.2f} mm gland entries and two {CLIP_PILOT_D:.2f} mm P-clip pilots in it, and
not one of those features had a purchasing line anywhere in the package. AVL-EEG-017
section 1.6 and kit BOM item 31 buy an **M3 x 18 mm nylon hex standoff, female-female**,
which has no stud to enter a boss insert, and **eight** M3 x 6 mm nylon screws for a joint
that takes four; nothing anywhere buys a brass insert, a lid screw, a P-clip screw or a
cable gland. A shop cannot raise a purchase order against a hole.

Every **size and length** below is derived from the released geometry, and the arithmetic is
shown in section 3 so it can be checked against the model instead of believed. Every
**vendor part** is a purchasing choice that nobody in this package has made: there is no
fastener, insert or gland datasheet in the package, so those lines are written as **OPEN
WITH CRITERIA** in the AVL-EEG-017 sense -- what the part has to do, and who has to choose
it -- and not as part numbers. *Nothing here has been fitted to a printed part; every
clearance is a model figure.*

## 1. POD-P1, per pod

| # | Item | Qty | Size, derived | Goes into | Torque |
|---|---|---|---|---|---|
| H-1 | M3 brass heat-set insert, carrier bosses | 4 | for a {INSERT_BORE_D:.2f} mm hole; insert length **at most {FLOOR_INSERT_DEPTH - 0.3:.1f} mm** ({FLOOR_INSERT_DEPTH:.2f} mm of bore less an assumed 0.3 mm blind-hole allowance) | the four floor bosses, blind, {FLOOR_INSERT_DEPTH:.2f} mm deep with {floor_under:.2f} mm of material under it | installed with a heat-set tool, not driven |
| H-2 | M3 brass heat-set insert, lid bosses | 4 | for a {INSERT_BORE_D:.2f} mm hole; insert length **{lid_engage:.1f} to {LID_INSERT_DEPTH - 0.3:.1f} mm** | the four corner bosses, {LID_INSERT_DEPTH:.2f} mm deep, top face at z = {LID_BOSS_TOP:.2f} | as above |
| H-3 | M3 x 12 A2 pan screw | 4 | length **12 mm**: {lid_stack:.2f} mm of lid plus {lid_gap:.2f} mm of gap leaves {lid_engage:.2f} mm in the insert | lid to base, through the {LID_HOLE_D:.2f} mm lid holes into H-2 | 0.60 N.m, diagonal, two passes |
| H-4 | M3 x {Z_PLATE_UNDER - Z_CARRIER_TOP:.0f} mm nylon standoff, **male-female** | 4 | body {Z_PLATE_UNDER - Z_CARRIER_TOP:.2f} mm; **male stud {stud_min:.1f} to {stud_max:.1f} mm**, a catalogue 6 mm stud engaging {6.0 - board_t:.2f} mm of insert | stud through the carrier's MH clearance hole into H-1; the carrier is clamped between the standoff shoulder and the boss face | 0.40 N.m |
| H-5 | M3 x 6 mm nylon pan screw | **4**, not 8 | length 6 mm: {plate_t:.2f} mm of MP-01 leaves {6.0 - plate_t:.2f} mm in the standoff's female end | MP-01 to the top of each H-4 | 0.40 N.m |
| H-6 | M2.5 x 6 mm nylon standoff and screw | 24 | not derived here; ASM-EEG-007 section 3.3 owns this line | each module to MP-01 | 0.25 N.m |
| H-7 | M3 x 8 thread-forming screw for plastics | 2 | length **8 mm**: {3.0:.2f} mm of P-clip foot plus {8.0 - 3.0:.2f} mm into a {CLIP_PILOT_DEPTH:.2f} mm pilot | the two POD-P1-04 P-clip bosses, {CLIP_PILOT_D:.2f} mm pilots -- **not** an insert, see section 3 | hand tight, about 0.3 N.m |
| H-8 | Cable gland, {GLAND_THREAD} | 2 | bore {ENTRY_BORE_D:.2f} mm, panel **{pod_panel:.2f} mm**, clamping range must cover {WH02_JACKET_NOM:.2f} and {WH01_JACKET_MAX:.2f} mm | the two harness entries, one per helmet cable | to the gland maker's figure |
| H-9 | Silicone O-cord, {1.5:.1f} mm, 60 Shore A | 1 | cut length **{cord:.1f} mm**, the groove centreline; butt-bonded at one corner | the {1.6:.1f} x {1.2:.1f} mm rim groove | -- |

POD-P1-03 already exists in PARTS-EEG-019 for H-9 and says "the cut length changes with the
Rev B rim". It is {cord:.1f} mm, twice each side of the
{POD_IW + POD_WALL:.1f} x {POD_IH + POD_WALL:.1f} mm groove centreline. The cord is cut long enough to butt at the joint and is
trimmed there; no stretch allowance is added here because none is measured.

## 2. HM-01, per helmet

| # | Item | Qty | Size, derived | Goes into | Torque |
|---|---|---|---|---|---|
| H-10 | Cable gland, {GLAND_THREAD} | 2 | bore {OE_BORE_D:.2f} mm, panel **{hm_panel:.2f} mm** ({HM01_SHELL_FLOOR_T:.2f} floor + {OE_PLATE_T:.2f} plate) | OE-1 and OE-2 in the occipital shell floor, through HM-12 | to the gland maker's figure |
| H-11 | HM-12 entry plate | 1 | printed, {OE_PLATE_W:.2f} x {OE_PLATE_D:.2f} x {OE_PLATE_T:.2f} mm | clamped under the floor by H-10; nothing else holds it | -- |

**H-8 and H-10 are the same part**, which is deliberate: one gland type, one AVL line, one
spare. What it costs is that the one gland has to accept two panel thicknesses --
{pod_panel:.2f} mm at the pod and {hm_panel:.2f} mm at the helmet. Both are inside the
{GLAND_PANEL_MIN:.1f} to {GLAND_PANEL_MAX:.1f} mm panel range glands of this class quote, and
`_pod_holds()` and `_oe_holds()` fail the build if either figure ever leaves that range.

Four glands per kit, two at each end of the two umbilicals.

## 3. The derivations

**H-1, the floor insert.** The boss stands {POD_FLOOR_BOSS_H:.2f} mm off a {POD_WALL:.2f} mm
floor, so its face is at z = {POD_WALL + POD_FLOOR_BOSS_H:.2f}. The bore is
{INSERT_BORE_D:.2f} mm with a {INSERT_LEADIN_D:.2f} x {INSERT_LEADIN_T:.2f} mm lead-in and is
{FLOOR_INSERT_DEPTH:.2f} mm deep, leaving {floor_under:.2f} mm of material under it and
{boss_wall:.2f} mm of boss wall around it. The bore is **blind**, so the insert has to be
shorter than the bore by whatever the maker allows for displaced material -- 0.3 mm is
assumed here and it is the maker's figure, not this package's. A 5.7 mm insert, the length
the pod_base() commentary names as typical, **does not fit this bore**; that is a real
constraint on the choice, not a preference.

**H-2 and H-3, the lid joint.** The boss top is {lid_gap:.2f} mm below the spigot face, so
the lid seats on its gasket and not on the boss. An M3 x 12 passes {POD_LID_T:.2f} mm of
plate and {POD_SPIGOT_T:.2f} mm of spigot, crosses {lid_gap:.2f} mm of gap, and has
{lid_engage:.2f} mm left for the insert; the bore is {LID_INSERT_DEPTH:.2f} mm deep so the
screw tip stops {LID_INSERT_DEPTH - lid_engage:.2f} mm clear of the bottom whatever insert in
that range is fitted.

**H-4, the standoff, and why it is male-female.** MH1 to MH4 are the only four fixings on
the carrier and three things want them: the pod boss below, the standoff above and the
carrier in between. pod_base() takes the resolution in which one fixing does both jobs, so
the standoff needs a **male stud** at the carrier end. The stud passes {board_t:.2f} mm of
carrier and then has {FLOOR_INSERT_DEPTH:.2f} mm of insert to enter: at least one diameter
of thread engagement puts the minimum stud at {stud_min:.1f} mm, and bottoming in the bore
puts the maximum at {stud_max:.1f} mm. A catalogue 6 mm stud sits in the middle of that
window with {6.0 - board_t:.2f} mm engaged. **The AVL and BOM part is female-female and
cannot be used.**

**H-7, the P-clip screw, and why it is not an insert.** Every other M3 thread in POD-P1 is a
brass insert because ASM-EEG-007 section 3.3 puts the strip limit of a thread formed in PA12
at about 0.5 N.m and section 5.1 torques those joints to 0.60 N.m. A P-clip screw is a
hand-tight cable retainer at about 0.3 N.m, fitted once, so it stays under that limit and a
{CLIP_PILOT_D:.2f} mm thread-forming pilot is enough. That is why POD-P1 has six insert
bores of one kind and two pilots of another, and it is not an inconsistency.

**H-8 and H-10, the gland.** {ENTRY_BORE_D:.2f} mm through {pod_panel:.2f} mm of panel is
the hole for an {GLAND_THREAD} gland. The clamping range has to bracket both jackets --
WH-01 at {WH01_JACKET_MAX:.2f} mm maximum and WH-02 at {WH02_JACKET_NOM:.2f} mm nominal
(WH-EEG-008 section 4) -- so a {GLAND_CLAMP_MIN:.1f} to {GLAND_CLAMP_MAX:.1f} mm range part
covers the pair with margin at both ends. The seat is {ENTRY_PAD_D:.2f} mm across, which
covers the corners of an assumed {GLAND_LOCKNUT_AF:.0f} mm across-flats locknut
({corner:.2f} mm across corners). **That across-flats figure is an assumption**, and it is
the one dimension in this schedule that can make the seat too small; check it against the
gland that is actually approved.

## 4. OPEN WITH CRITERIA

Nothing in this section is decided. Each line says what the part has to do and who has to
decide it; none of them may be closed by picking a part number off a distributor's site
without checking the criteria against its datasheet, because the criteria are what the
released geometry can accept.

| Ref | What has to be chosen | Criteria the released geometry sets | Who decides |
|---|---|---|---|
| H-1 | M3 brass heat-set insert, 4 per pod | recommended hole {INSERT_BORE_D:.2f} mm +/- the maker's tolerance; overall length at most {FLOOR_INSERT_DEPTH:.2f} mm less the maker's blind-hole allowance; outside diameter at most {POD_FLOOR_BOSS_D - 2 * 1.5:.2f} mm so {1.5:.1f} mm of boss wall is left | AVL-EEG-017, with the insert maker's installation data on the file |
| H-2 | M3 brass heat-set insert, 4 per pod | same hole; length {lid_engage:.1f} to {LID_INSERT_DEPTH - 0.3:.1f} mm -- at least {lid_engage:.1f} so that the screw's {lid_engage:.2f} mm of engagement is all in thread, at most {LID_INSERT_DEPTH - 0.3:.1f} so it does not bottom in a {LID_INSERT_DEPTH:.2f} mm blind bore | AVL-EEG-017 |
| H-3 | M3 x 12 A2 pan screw | A2 stainless, pan or cheese head under {LID_HOLE_D:.2f} mm clearance; head diameter to clear the {LID_BOSS_D:.2f} mm boss footprint on the lid | AVL-EEG-017 |
| H-4 | M3 x {Z_PLATE_UNDER - Z_CARRIER_TOP:.0f} mm **male-female** nylon standoff | body {Z_PLATE_UNDER - Z_CARRIER_TOP:.2f} mm, hex; stud {stud_min:.1f} to {stud_max:.1f} mm; nylon or another non-conductive polymer, because RISK-EEG-011 SR-08's creepage rests on it and the M3 holes have a 6 mm copper keep-out | AVL-EEG-017 and the safety reviewer together, since the material is part of the safety case |
| H-7 | M3 x 8 thread-forming screw for plastics | for a {CLIP_PILOT_D:.2f} mm pilot in PA12, 30-degree or trilobular thread form; A2 or steel | AVL-EEG-017 |
| H-8, H-10 | Cable gland, {GLAND_THREAD}, 4 per kit | clamping range covering {GLAND_CLAMP_MIN:.1f} to {GLAND_CLAMP_MAX:.1f} mm; panel range covering {pod_panel:.2f} and {hm_panel:.2f} mm; locknut at most {GLAND_LOCKNUT_AF:.0f} mm across flats; sealing at least IP54 to match the pod's design target; cable retention at least the 15 N of WH-EEG-008 H6, stated by the maker and recorded. **At the helmet end the umbilical flexes with the participant's head**, so a bend-restricting form is preferred there and the two ends may end up different parts; that is a decision, and it has not been taken | AVL-EEG-017, with WH-EEG-008 for the retention figure |
| H-9 | Silicone O-cord, 1.5 mm, 60 Shore A | cut {cord:.1f} mm; cyanoacrylate butt joint; the 20 % compression and 92 % groove fill of ASM-EEG-007 section 5.1 item 2 are calculated and not measured | AVL-EEG-017 |
| -- | Identifier for the gland | PARTS-EEG-019 section 1.2 has POD-P1-01 to -05 allocated, so **POD-P1-06 is proposed** for the harness-entry gland. It is not POD-P1-05, which is the withdrawn captive-host-lead gland and must stay withdrawn | PARTS-EEG-019 |
| -- | Identifier for the entry plate | **HM-12 is proposed** as the next free number. Section 1.2 reserves HM-12 to HM-19 for Phase 2 and this is a Phase 1 part, so the register owner has to confirm it or issue another; the part is deliberately not engraved until then | PARTS-EEG-019 |

## 5. What this file needs changed elsewhere

This schedule cannot correct another document. The five that carry the wrong part today:

1. **AVL-EEG-017 section 1.6**, the "Carrier-to-plate standoff" row: the part is
   female-female with eight M3 x 6 screws, and the released geometry needs a male-female
   standoff with four. The insert, lid screw, P-clip screw and gland lines do not exist.
2. **AVL-EEG-017 section 4**: the gland has no K-line, so no bidder is quoting it.
3. **Kit BOM item 31** repeats the AVL standoff line.
4. **PARTS-EEG-019 sections 2.1 and 2.2**: POD-P1-06 and HM-12 above, and the POD-P1-05 row,
   which says "no gland feature exists in POD-P1-01". Two do, and they are not POD-P1-05.
5. **SVC-EEG-013 section 5** says "POD-P1 carries no gland feature", so the service manual has
   no procedure for replacing a helmet cable at the pod end -- which is now a gland to undo
   and not a soldered joint to remake.

ASM-EEG-007 Rev B section 3.3 and the section 5.1 torque table are corrected at this issue
against this schedule.
"""


def release_status(outdir):
    """`mech/MECH_RELEASE_STATUS.md`: what this file releases, part by part, against what
    the registers still record.  It exists because eight parts that now have STEP, STL, a
    MECH-EEG-020 sheet and a MANIFEST.json row are carried as "to be created" in
    PARTS-EEG-019 and sit outside the AVL-EEG-017 K24 print set the bureau is quoted on.

    The drawing column is read from `mech/drawings/MECH-EEG-020_sheet_index.csv` rather than
    typed, so a released part with no sheet shows up here as one."""
    sheets = {}
    idx = os.path.join(outdir, "drawings", "MECH-EEG-020_sheet_index.csv")
    if os.path.exists(idx):
        for line in _read_text(idx).splitlines()[1:]:
            f = line.split(",")
            if len(f) == 4:
                sheets[f[3].strip()] = f[0].strip()
    rows = []
    for name, _fn in PARTS:
        r = REGISTER[name]
        sh = sheets.get(f"{name}.stl")
        sh = f"sheet {sh}" if sh else "**none**"
        rows.append(f"| {r['part_id']} | {r['revision']} | `mech/stl/{name}.stl` + "
                    f"`mech/step/{name}.step` | {r['material']} | {r['process']} | "
                    f"`{r['source'].split()[-1]}` | {sh} |")
    table = "\n".join(rows)
    return f"""# MECHANICAL RELEASE STATUS -- WHAT IS PRINTABLE TODAY

**File:** `mech/MECH_RELEASE_STATUS.md`
**Generated by:** `tools/mech_gen.py release_status()`, from the same PARTS and REGISTER
tables that build the geometry, so a part cannot appear here without a file behind it.
**Licence:** CC BY-SA 4.0

## Why this file exists

A print bureau reading PARTS-EEG-019 Rev B sections 2.1 and 2.2 is told that HM-02B, HM-02C,
HM-03A, HM-05B, HM-10, HM-11A, HM-11B, HM-11C, POD-P1-04 and the WH-ADP adapters have
"Defining file: none" and are "to be created", and section 6 says they have no geometry.
The directory says otherwise: each has an STL, a STEP, a MECH-EEG-020 sheet and a row in
`mech/MANIFEST.json`. AVL-EEG-017 K24 -- the single line the MJF bureau quotes against --
lists only HM-01, HM-02, HM-03 yoke, HM-04, HM-06, HM-08, HM-09, MP-01, the POD-P1 base and
lid, WH-KEY-01 and FIT-01, so the rest are unquoted and unpriced whatever the register says.

This file is the list of what `tools/mech_gen.py` actually writes. **It does not overrule
PARTS-EEG-019**, which is the governing register; it is the evidence that register has to be
corrected against, and section 3 says exactly which rows.

*No part in this list has been printed. Every figure in `mech/MANIFEST.json` is a model
figure.*

## 1. Released as geometry by `tools/mech_gen.py`

| Part | Rev | Files | Material | Process | Generator | MECH-EEG-020 |
|---|---|---|---|---|---|---|
{table}

**A "none" in the last column is a released part with no drawing sheet.** The drawing set is
built by `tools/mech_drawings.py` and is not written here, so a part added to the model
reaches this table one revision before it reaches MECH-EEG-020; that is the gap to close,
not a reason to leave the part out of the model.

The seven CASE-00 Rev C foam layers are written by the same file, as
`mech/CASE-00_foam_layer_1..7.dxf`. HM-01 is carried over from package v1 as an STL and has
no parametric source (PARTS-EEG-019 OA-1); `mech/step/EEG-CAR-01_RevB_board_outline.step` is
written by `tools/emit_extras.py`.

## 2. Named in the package and deliberately NOT modelled

A part that is the wrong shape is worse than a part that is honestly absent, so these are
left out rather than guessed:

| Part | Why there is no geometry |
|---|---|
| HM-03B | ratchet dial housing for HM-03C, and HM-03C has no vendor, no outline, no spindle and no fixing pattern |
| HM-06A, HM-06B | the package fixes the 20 mm webbing and the 200 N anchor pull and nothing at all about the shell |
| HM-07A | boom temple mount for HM-07B, a gooseneck with no vendor and no diameter |
| POD-P1-05 | withdrawn from the Phase 1 build with WH-08. It is **not** the harness-entry gland of `HARDWARE_SCHEDULE.md`, which is a different part in a different place |

## 3. What the registers have to be corrected against

| Document | What it says | What the directory says |
|---|---|---|
| PARTS-EEG-019 sections 2.1 and 2.2 | HM-02B, HM-02C, HM-03A, HM-05B, HM-10, HM-11A/B/C and POD-P1-04 have "Defining file: none" and are "To be created"; the WH-ADP rows say the same | all have STL, STEP and a MECH-EEG-020 sheet, listed in section 1 above |
| PARTS-EEG-019 section 6 | records the same parts as having no geometry | as above |
| PARTS-EEG-019 section 1.2 | HM-12 to HM-19 reserved for Phase 2; POD-P1-01 to -05 allocated | HM-12 and POD-P1-06 are proposed in `HARDWARE_SCHEDULE.md` section 4 and need issuing or replacing |
| PARTS-EEG-019 OA-2 | `mech/MANIFEST.json` carries 56 file entries | the manifest is regenerated at this issue and the count changes with it; read it from the file |
| AVL-EEG-017 K24 | print set of twelve items | the set in section 1 above, plus HM-12; everything not in K24 is unquoted |
| KNOWN_ISSUES section 8 | repeats "no geometry" | as above |

Each of those documents is owned by someone else. This file changes none of them.
"""


def write_schedules(outdir):
    """Write both generated Markdown files into `mech/`."""
    for fn, text in (("HARDWARE_SCHEDULE.md", hardware_schedule()),
                     ("MECH_RELEASE_STATUS.md", release_status(outdir))):
        with open(os.path.join(outdir, fn), "w", encoding="utf-8") as f:
            f.write(text)


def build(outdir):
    stl = os.path.join(outdir, "stl")
    step = os.path.join(outdir, "step")
    os.makedirs(stl, exist_ok=True)
    os.makedirs(step, exist_ok=True)
    for name, fn in PARTS:
        obj = fn()
        solid = obj.val()
        bb = solid.BoundingBox()
        sp = os.path.join(stl, f"{name}.stl")
        tp = os.path.join(step, f"{name}.step")
        cq.exporters.export(obj, sp)
        cq.exporters.export(obj, tp, cq.exporters.ExportTypes.STEP)
        ident = _identity(name)
        _stamp_step(tp, ident)
        _stamp_stl(sp, ident)
        print(f"  {name:42s} {bb.xlen:7.1f} x {bb.ylen:6.1f} x {bb.zlen:6.1f} mm "
              f"{solid.Volume()/1000.0:8.1f} cm3  {MARKING.get(name, ('unmarked',))[0]}")
    for n in range(1, 8):        # CASE-00 Rev C is a seven-layer stack, not two sheets
        foam_dxf(os.path.join(outdir, f"CASE-00_foam_layer_{n}.dxf"), n)
    write_schedules(outdir)
    return manifest(outdir)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mech")
    m = build(out)
    p = os.path.join(out, "MANIFEST.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=1)
        f.write("\n")
    print(f"  {len(m['files'])} files -> {p}")
