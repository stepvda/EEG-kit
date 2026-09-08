#!/usr/bin/env python3
"""
dxf_out.py -- the board outline and the fixed connector positions as DXF.

Input 4 of the list promised to the layout contractor (ECO-EEG-030): "board outline and
fixed connector positions (DXF)".  It is a mechanical drawing, not a fabrication file:
the outline, the four mounting holes and their keep-outs, the isolation keep-out, the
zone split, and every one of the thirty connectors drawn as its own courtyard with a
pin-1 mark and its reference.

**The coordinate convention is `design.py`'s: top-left origin, Y down**, the same as the
`.kicad_pcb` this ships beside, so a contractor can overlay the two without transforming
anything.  It is NOT the CAM convention -- Gerber, drill and both CPL files use a
bottom-left origin with Y up, and `tools/gerber.py` is the one place that flips.  A
reader who mixes the two gets a board mirrored about its own middle, so the convention is
written into the file as a text entity as well as into the README.

Written as R12 ASCII DXF: LINE, CIRCLE and TEXT only, on named layers.  R12 because every
CAD tool reads it and nothing here needs more.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import fplib                # noqa: E402
import rules                # noqa: E402

LAYERS = [
    ("OUTLINE", 7),
    ("MOUNTING_HOLES", 1),
    ("MOUNTING_KEEPOUT", 1),
    ("ISOLATION_KEEPOUT", 1),
    ("ZONE_SPLIT", 3),
    ("CONNECTORS_FIXED", 5),
    ("CONNECTOR_PIN1", 2),
    ("TEXT", 7),
]


class Dxf:
    def __init__(self):
        self.body = []

    def _pair(self, code, value):
        self.body.append(f"{code:>3d}")
        self.body.append(str(value))

    def line(self, layer, x1, y1, x2, y2):
        self._pair(0, "LINE")
        self._pair(8, layer)
        self._pair(10, f"{x1:.4f}")
        self._pair(20, f"{y1:.4f}")
        self._pair(30, "0.0")
        self._pair(11, f"{x2:.4f}")
        self._pair(21, f"{y2:.4f}")
        self._pair(31, "0.0")

    def circle(self, layer, cx, cy, r):
        self._pair(0, "CIRCLE")
        self._pair(8, layer)
        self._pair(10, f"{cx:.4f}")
        self._pair(20, f"{cy:.4f}")
        self._pair(30, "0.0")
        self._pair(40, f"{r:.4f}")

    def rect(self, layer, x1, y1, x2, y2):
        self.line(layer, x1, y1, x2, y1)
        self.line(layer, x2, y1, x2, y2)
        self.line(layer, x2, y2, x1, y2)
        self.line(layer, x1, y2, x1, y1)

    def text(self, layer, x, y, s, h=2.0):
        self._pair(0, "TEXT")
        self._pair(8, layer)
        self._pair(10, f"{x:.4f}")
        self._pair(20, f"{y:.4f}")
        self._pair(30, "0.0")
        self._pair(40, f"{h:.4f}")
        self._pair(1, s)

    def render(self):
        out = ["  0", "SECTION", "  2", "HEADER",
               "  9", "$INSUNITS", " 70", "4",          # millimetres
               "  9", "$EXTMIN", " 10", "0.0", " 20", "0.0", " 30", "0.0",
               "  9", "$EXTMAX", " 10", f"{D.BOARD_W:.4f}", " 20",
               f"{D.BOARD_H:.4f}", " 30", "0.0",
               "  0", "ENDSEC",
               "  0", "SECTION", "  2", "TABLES",
               "  0", "TABLE", "  2", "LAYER", " 70", str(len(LAYERS))]
        for name, colour in LAYERS:
            out += ["  0", "LAYER", "  2", name, " 70", "0",
                    " 62", str(colour), "  6", "CONTINUOUS"]
        out += ["  0", "ENDTAB", "  0", "ENDSEC",
                "  0", "SECTION", "  2", "ENTITIES"]
        out += self.body
        out += ["  0", "ENDSEC", "  0", "EOF"]
        return "\n".join(out) + "\n"


def write(path, board):
    d = Dxf()
    W, H = D.BOARD_W, D.BOARD_H

    d.rect("OUTLINE", 0, 0, W, H)
    d.line("ZONE_SPLIT", D.ZONE_SPLIT_X, 0, D.ZONE_SPLIT_X, H)

    for i, (mx, my) in enumerate(D.MOUNTING_HOLES, start=1):
        d.circle("MOUNTING_HOLES", mx, my, 3.4 / 2.0)
        d.circle("MOUNTING_KEEPOUT", mx, my, D.MOUNTING_KEEPOUT_D / 2.0)
        d.text("TEXT", mx + 3.6, my - 1.0, f"MH{i}", 1.6)

    x0, y0, x1, y1 = rules.ISOLATION_KEEPOUT
    d.rect("ISOLATION_KEEPOUT", x0, y0, x1, y1)
    d.text("TEXT", x0 - 34.0, y0 + 3.0, "ISOLATION KEEP-OUT, NO COPPER ANY LAYER", 1.6)

    fixed = 0
    for part in sorted(board.parts, key=lambda p: p.ref):
        if not part.ref.startswith("J"):
            continue
        fixed += 1
        b = board.courtyard_box(part)
        d.rect("CONNECTORS_FIXED", b[0], b[1], b[2], b[3])
        d.text("TEXT", b[0], b[1] - 1.4, part.ref, 1.6)
        # pin 1 is the connector's origin on every socket strip in this library
        p1 = next((pd for pd in part.pads if pd.num == "1"), None)
        if p1 is not None:
            d.circle("CONNECTOR_PIN1", p1.x, p1.y, 0.9)
            d.line("CONNECTOR_PIN1", p1.x - 1.4, p1.y, p1.x + 1.4, p1.y)
            d.line("CONNECTOR_PIN1", p1.x, p1.y - 1.4, p1.x, p1.y + 1.4)

    d.text("TEXT", 2.0, H + 6.0,
           f"EEG-CAR-01 Rev {D.REV_C} -- outline and FIXED connector positions. "
           f"{fixed} connectors, LOCKED.", 3.0)
    d.text("TEXT", 2.0, H + 11.0,
           "COORDINATES: top-left origin, X right, Y DOWN -- design.py and the "
           ".kicad_pcb convention.", 2.2)
    d.text("TEXT", 2.0, H + 15.0,
           "Gerber, drill and both CPL files use a BOTTOM-LEFT origin with Y UP: "
           "y_cam = 130.0 - y_here.  Do not mix them.", 2.2)
    d.text("TEXT", 2.0, H + 19.0,
           f"Board {W:.1f} x {H:.1f} mm, four layers, through vias only. "
           f"Zone split x = {D.ZONE_SPLIT_X:.1f} mm, analogue left.", 2.2)

    open(path, "w").write(d.render())
    return path, fixed
