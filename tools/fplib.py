#!/usr/bin/env python3
"""
fplib.py -- parametric footprint library for EEG-CAR-01 Rev B.

Every footprint used on the carrier is generated here from its dimensions so that the
board file, the Gerbers, the placement drawings, the CPL and the DRC all come from one
definition. Dimensions follow the KiCad standard libraries (IPC-7351 nominal density)
so a house that re-imports the netlist into its own CAD gets the same land patterns.

Coordinates are millimetres, local to the footprint origin, X right / Y down (KiCad).

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class PadDef:
    num: str
    kind: str          # 'smd' | 'thru_hole' | 'np_thru_hole'
    shape: str         # 'rect' | 'oval' | 'circle' | 'roundrect'
    x: float
    y: float
    w: float
    h: float
    drill: float = 0.0
    layers: tuple = ()

    def __post_init__(self):
        if not self.layers:
            self.layers = (("F.Cu", "F.Paste", "F.Mask") if self.kind == "smd"
                           else ("*.Cu", "*.Mask"))


@dataclass
class FootprintDef:
    name: str
    descr: str
    pads: list
    silk: list = field(default_factory=list)      # [(x1,y1,x2,y2,width)]
    fab: list = field(default_factory=list)
    crtyd: list = field(default_factory=list)
    body: tuple = (0, 0, 0, 0)                    # (x1,y1,x2,y2) fab body extent
    tht: bool = False

    def bbox(self):
        xs, ys = [], []
        for p in self.pads:
            xs += [p.x - p.w / 2, p.x + p.w / 2]
            ys += [p.y - p.h / 2, p.y + p.h / 2]
        for seg in self.crtyd or self.silk:
            xs += [seg[0], seg[2]]
            ys += [seg[1], seg[3]]
        return (min(xs), min(ys), max(xs), max(ys))


def _rect(x1, y1, x2, y2, w):
    return [(x1, y1, x2, y1, w), (x2, y1, x2, y2, w),
            (x2, y2, x1, y2, w), (x1, y2, x1, y1, w)]


# --------------------------------------------------------------------- chip 2-terminal
def chip(name, descr, pad_dx, pad_w, pad_h, body_w, body_h):
    pads = [PadDef("1", "smd", "roundrect", -pad_dx, 0, pad_w, pad_h),
            PadDef("2", "smd", "roundrect", +pad_dx, 0, pad_w, pad_h)]
    hx, hy = body_w / 2, body_h / 2
    cx = pad_dx + pad_w / 2 + 0.25
    cy = max(pad_h / 2, hy) + 0.25
    silk_y = max(pad_h / 2, hy) + 0.15
    return FootprintDef(
        name=name, descr=descr, pads=pads,
        silk=[(-hx, -silk_y, hx, -silk_y, 0.12), (-hx, silk_y, hx, silk_y, 0.12)],
        fab=_rect(-hx, -hy, hx, hy, 0.1),
        crtyd=_rect(-cx, -cy, cx, cy, 0.05),
        body=(-hx, -hy, hx, hy))


R_0603 = chip("R_0603_1608Metric", "Resistor SMD 0603 (1608 metric)", 0.825, 0.8, 0.95, 1.6, 0.8)
C_0603 = chip("C_0603_1608Metric", "Capacitor SMD 0603 (1608 metric)", 0.7875, 0.875, 0.95, 1.6, 0.8)
L_0603 = chip("L_0603_1608Metric", "Ferrite bead / inductor SMD 0603", 0.825, 0.8, 0.95, 1.6, 0.8)
R_1206 = chip("R_1206_3216Metric", "PTC resettable fuse SMD 1206", 1.4625, 1.125, 1.75, 3.2, 1.6)


# --------------------------------------------------------------------- SOT-23 (3 lead)
def _sot23():
    pads = [PadDef("1", "smd", "roundrect", -0.9375, 1.04, 1.025, 0.6),
            PadDef("2", "smd", "roundrect", +0.9375, 1.04, 1.025, 0.6),
            PadDef("3", "smd", "roundrect", 0.0, -1.04, 1.025, 0.6)]
    return FootprintDef("SOT-23", "SOT-23, 3 lead (dual diode / small signal)", pads,
                        silk=[(-0.7, -1.61, 0.7, -1.61, 0.12), (-0.7, 1.61, 0.7, 1.61, 0.12),
                              (-1.75, 1.05, -1.75, 1.75, 0.12)],
                        fab=_rect(-0.65, -1.4, 0.65, 1.4, 0.1),
                        crtyd=_rect(-1.72, -1.8, 1.72, 1.8, 0.05),
                        body=(-0.65, -1.4, 0.65, 1.4))


SOT23 = _sot23()


def _sot23_5():
    pads = [PadDef("1", "smd", "roundrect", -1.1, 0.95, 1.1, 0.6),
            PadDef("2", "smd", "roundrect", -1.1, 0.0, 1.1, 0.6),
            PadDef("3", "smd", "roundrect", -1.1, -0.95, 1.1, 0.6),
            PadDef("4", "smd", "roundrect", +1.1, -0.95, 1.1, 0.6),
            PadDef("5", "smd", "roundrect", +1.1, 0.95, 1.1, 0.6)]
    return FootprintDef("SOT-23-5", "SOT-23-5 (comparator)", pads,
                        silk=[(-0.8, -1.6, 0.8, -1.6, 0.12), (-0.8, 1.6, 0.8, 1.6, 0.12),
                              (-1.9, 1.0, -1.9, 1.6, 0.12)],
                        fab=_rect(-0.8, -1.45, 0.8, 1.45, 0.1),
                        crtyd=_rect(-1.9, -1.8, 1.9, 1.8, 0.05),
                        body=(-0.8, -1.45, 0.8, 1.45))


SOT23_5 = _sot23_5()


# --------------------------------------------------------------------- TSSOP-14 (quad op-amp)
def _tssop14():
    pads = []
    # 14 pins, 0.65 mm pitch, 7 per side, pad 1.45 x 0.45, span 5.7 mm centre-to-centre
    for i in range(7):
        y = (i - 3) * 0.65
        pads.append(PadDef(str(i + 1), "smd", "roundrect", -2.85, y, 1.45, 0.45))
    for i in range(7):
        y = (3 - i) * 0.65
        pads.append(PadDef(str(i + 8), "smd", "roundrect", +2.85, y, 1.45, 0.45))
    return FootprintDef("TSSOP-14_4.4x5.0mm_P0.65mm", "TSSOP-14, 4.4x5.0 mm body, 0.65 mm pitch",
                        pads,
                        silk=[(-2.2, -2.5, 2.2, -2.5, 0.12), (-2.2, 2.5, 2.2, 2.5, 0.12),
                              (-3.7, -2.5, -3.7, -2.05, 0.12)],   # pin 1 is at y = -1.95, not +1.95
                        fab=_rect(-2.2, -2.5, 2.2, 2.5, 0.1),
                        crtyd=_rect(-3.75, -2.85, 3.75, 2.85, 0.05),
                        body=(-2.2, -2.5, 2.2, 2.5))


TSSOP14 = _tssop14()


def _soic14():
    """SOIC-14, 1.27 mm pitch, 3.9 mm body, 6.0 mm lead span.

    Chosen over TSSOP-14 for U1-U3: the 0.67 mm gap between adjacent SOIC lands takes a
    0.25 mm track at 0.20 mm clearance, and a 0.65 mm TSSOP does not.  On a two-layer
    board with no vias allowed between the lands, that is the difference between the
    envelope detectors routing and not routing.
    """
    pads = []
    for i in range(7):
        y = (i - 3) * 1.27
        pads.append(PadDef(str(i + 1), "smd", "roundrect", -2.7, y, 1.95, 0.60))
    for i in range(7):
        y = (3 - i) * 1.27
        pads.append(PadDef(str(i + 8), "smd", "roundrect", +2.7, y, 1.95, 0.60))
    return FootprintDef("SOIC-14_3.9x8.7mm_P1.27mm", "SOIC-14, 3.9 x 8.7 mm body, "
                        "1.27 mm pitch", pads,
                        # The pin-1 tick belongs beside PAD 1, which is at y = -3.81.
                        # It used to sit at y = +4.0..+4.5, beside pad 7 at the other end of
                        # the package.  ASM-EEG-007 section 2.4 tells the operator to align
                        # "pin 1 dot to the legend dot", so the board's own legend would have
                        # fitted U1, U2 and U3 rotated 180 degrees -- and pad 4 is AVDD while
                        # pad 11 is AVSS, so that puts +2.5 V on the negative rail pin and
                        # destroys all three envelope channels at first power-up.
                        silk=[(-1.95, -4.5, 1.95, -4.5, 0.12), (-1.95, 4.5, 1.95, 4.5, 0.12),
                              (-3.9, -4.5, -3.9, -4.0, 0.12)],
                        fab=_rect(-1.95, -4.35, 1.95, 4.35, 0.1),
                        crtyd=_rect(-3.95, -4.75, 3.95, 4.75, 0.05),
                        body=(-1.95, -4.35, 1.95, 4.35))


SOIC14 = _soic14()


# --------------------------------------------------------------------- pin sockets
def pinsocket_1xn(n, pitch=2.54, pad=1.6, drill=1.0):
    pads = []
    for i in range(n):
        pads.append(PadDef(str(i + 1), "thru_hole", "rect" if i == 0 else "oval",
                           0.0, i * pitch, pad, pad, drill))
    y0, y1 = -1.33, (n - 1) * pitch + 1.33
    # Pin 1 is a rect pad where the rest are oval, but that pad sits at (0, 0) -- INSIDE the
    # body outline, so it disappears under the socket once the part is fitted.  There was no
    # legend marker of any kind outside the body, while ASM-EEG-007 section 2.2 step 8 tells
    # the receiving operator to confirm that every socket strip has exactly that, and section
    # 2.7 repeats it for J14 and J30.  The check could not pass on any board ever built.
    # A chevron outside the outline at the pin-1 end, which survives the fitted socket.
    return FootprintDef(f"PinSocket_1x{n:02d}_P2.54mm_Vertical",
                        f"Through-hole socket strip 1x{n}, 2.54 mm pitch", pads,
                        silk=[(-1.33, y0, 1.33, y0, 0.12), (1.33, y0, 1.33, y1, 0.12),
                              (1.33, y1, -1.33, y1, 0.12), (-1.33, y1, -1.33, y0, 0.12),
                              # A filled-looking chevron at the pin-1 end, drawn OUTSIDE
                              # the 1.33 mm body outline so it survives the fitted socket,
                              # and INSIDE the 1.8 mm courtyard because the module no-via
                              # keep-out is derived from the courtyard: enlarging it to
                              # make room put two existing vias under J4 in violation.
                              (-1.75, y0, -1.40, y0, 0.12),
                              (-1.75, y0, -1.575, y0 - 0.30, 0.12),
                              (-1.40, y0, -1.575, y0 - 0.30, 0.12)],
                        fab=_rect(-1.27, -1.27, 1.27, (n - 1) * pitch + 1.27, 0.1),
                        crtyd=_rect(-1.8, y0 - 0.4, 1.8, y1 + 0.4, 0.05),
                        body=(-1.27, -1.27, 1.27, (n - 1) * pitch + 1.27), tht=True)


def pinsocket_2xn(n, pitch=2.54, pad=1.6, drill=1.0):
    """Pin 1 top-left; odd pins column x=0, even pins column x=+2.54 (KiCad convention)."""
    pads = []
    for i in range(n):
        for col in (0, 1):
            num = i * 2 + col + 1
            pads.append(PadDef(str(num), "thru_hole", "rect" if num == 1 else "oval",
                               col * pitch, i * pitch, pad, pad, drill))
    y0, y1 = -1.33, (n - 1) * pitch + 1.33
    x0, x1 = -1.33, pitch + 1.33
    return FootprintDef(f"PinSocket_2x{n:02d}_P2.54mm_Vertical",
                        f"Through-hole socket strip 2x{n}, 2.54 mm pitch", pads,
                        silk=[(x0, y0, x1, y0, 0.12), (x1, y0, x1, y1, 0.12),
                              (x1, y1, x0, y1, 0.12), (x0, y1, x0, y0, 0.12)],
                        fab=_rect(x0 + 0.06, y0 + 0.06, x1 - 0.06, y1 - 0.06, 0.1),
                        crtyd=_rect(x0 - 0.4, y0 - 0.4, x1 + 0.4, y1 + 0.4, 0.05),
                        body=(x0, y0, x1, y1), tht=True)


def _jst_ph2():
    pads = [PadDef("1", "thru_hole", "rect", -1.0, 0, 1.7, 1.7, 0.9),
            PadDef("2", "thru_hole", "oval", 1.0, 0, 1.7, 1.7, 0.9)]
    return FootprintDef("JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",
                        "JST PH series 2.00 mm 2-way vertical header", pads,
                        silk=[(-2.95, -1.8, 2.95, -1.8, 0.12), (2.95, -1.8, 2.95, 2.7, 0.12),
                              (2.95, 2.7, -2.95, 2.7, 0.12), (-2.95, 2.7, -2.95, -1.8, 0.12)],
                        fab=_rect(-2.9, -1.75, 2.9, 2.65, 0.1),
                        crtyd=_rect(-3.4, -2.2, 3.4, 3.1, 0.05),
                        body=(-2.9, -1.75, 2.9, 2.65), tht=True)


JST_PH2 = _jst_ph2()


def _din42802():
    """Touch-proof 1.5 mm DIN 42802 panel socket, PCB-mount version.
    One 1.7 mm signal pin plus two 1.5 mm mechanical retention posts (NPTH)."""
    pads = [PadDef("1", "thru_hole", "circle", 0.0, 0.0, 2.6, 2.6, 1.7),
            PadDef("", "np_thru_hole", "circle", -3.5, 0.0, 1.5, 1.5, 1.5, layers=("",)),
            PadDef("", "np_thru_hole", "circle", +3.5, 0.0, 1.5, 1.5, 1.5, layers=("",))]
    return FootprintDef("DIN42802_1p5mm_Socket",
                        "Touch-proof 1.5 mm safety socket to DIN 42802 (Staubli LB-I1,5 class)",
                        pads,
                        silk=[(-5.0, -4.0, 5.0, -4.0, 0.12), (5.0, -4.0, 5.0, 4.0, 0.12),
                              (5.0, 4.0, -5.0, 4.0, 0.12), (-5.0, 4.0, -5.0, -4.0, 0.12)],
                        fab=_rect(-4.9, -3.9, 4.9, 3.9, 0.1),
                        crtyd=_rect(-5.4, -4.4, 5.4, 4.4, 0.05),
                        body=(-4.9, -3.9, 4.9, 3.9), tht=True)


DIN42802 = _din42802()


def _sw_push_6mm():
    pads = [PadDef("1", "thru_hole", "circle", -3.25, -2.25, 2.0, 2.0, 1.2),
            PadDef("1", "thru_hole", "circle", -3.25, 2.25, 2.0, 2.0, 1.2),
            PadDef("2", "thru_hole", "circle", 3.25, -2.25, 2.0, 2.0, 1.2),
            PadDef("2", "thru_hole", "circle", 3.25, 2.25, 2.0, 2.0, 1.2)]
    return FootprintDef("SW_PUSH_6mm_H5mm", "Tactile switch 6x6 mm THT, 5 mm actuator", pads,
                        silk=[(-3.0, -3.2, 3.0, -3.2, 0.12), (3.0, -3.2, 3.0, 3.2, 0.12),
                              (3.0, 3.2, -3.0, 3.2, 0.12), (-3.0, 3.2, -3.0, -3.2, 0.12)],
                        fab=_rect(-3.0, -3.0, 3.0, 3.0, 0.1),
                        crtyd=_rect(-4.6, -3.6, 4.6, 3.6, 0.05),
                        body=(-3.0, -3.0, 3.0, 3.0), tht=True)


SW_PUSH = _sw_push_6mm()


def _mounting_hole_m3():
    return FootprintDef("MountingHole_3.2mm_M3", "M3 mounting hole, 3.2 mm drill, non-plated",
                        [PadDef("", "np_thru_hole", "circle", 0, 0, 3.2, 3.2, 3.2, layers=("",))],
                        silk=[], fab=[], crtyd=_rect(-3.0, -3.0, 3.0, 3.0, 0.05),
                        body=(-3.0, -3.0, 3.0, 3.0), tht=True)


MH_M3 = _mounting_hole_m3()


def _testpoint():
    """A bare probe pad.  Copper and mask only -- NO PASTE.

    A test point is a fabricated feature, not a placement: nothing is soldered to it, so
    paste on it just prints solder that the probe then has to push through.  The default
    smd layer set includes F.Paste, which put eighteen 1.5 mm paste apertures on the
    stencil of the released Rev B artwork.
    """
    return FootprintDef("TestPoint_Pad_D1.5mm", "SMD test pad, 1.5 mm round",
                        [PadDef("1", "smd", "circle", 0, 0, 1.5, 1.5,
                                layers=("F.Cu", "F.Mask"))],
                        silk=[], fab=[], crtyd=_rect(-1.1, -1.1, 1.1, 1.1, 0.05),
                        body=(-0.75, -0.75, 0.75, 0.75))


TESTPOINT = _testpoint()


def _fiducial():
    """Global fiducial: 1.0 mm copper, 3.0 mm mask opening, no net.

    ECO-EEG-020.  Rev B had none, and the interim answer -- a two-point vision teach on
    the plated test-point pads -- costs the assembler time on every board.
    """
    return FootprintDef("Fiducial_1mm_Mask3mm", "Fiducial, 1 mm copper, 3 mm mask opening",
                        [PadDef("1", "smd", "circle", 0, 0, 1.0, 1.0,
                                layers=("F.Cu",)),
                         PadDef("1", "smd", "circle", 0, 0, 3.0, 3.0,
                                layers=("F.Mask",))],
                        silk=[], fab=[], crtyd=_rect(-2.0, -2.0, 2.0, 2.0, 0.05),
                        body=(-1.5, -1.5, 1.5, 1.5))


FIDUCIAL = _fiducial()

LIB = {}
for _fp in (R_0603, C_0603, L_0603, R_1206, SOT23, SOT23_5, TSSOP14, SOIC14,
            JST_PH2, DIN42802, SW_PUSH, MH_M3, TESTPOINT, FIDUCIAL):
    LIB[_fp.name] = _fp
for _n in (2, 3, 4, 6, 8, 10, 12, 14, 16, 22):
    _f = pinsocket_1xn(_n)
    LIB[_f.name] = _f
for _n in (10,):
    _f = pinsocket_2xn(_n)
    LIB[_f.name] = _f


def get(name):
    if name in LIB:
        return LIB[name]
    raise KeyError(f"footprint {name!r} not in library; known: {sorted(LIB)}")


if __name__ == "__main__":
    for k in sorted(LIB):
        f = LIB[k]
        b = f.bbox()
        print(f"{k:42s} pads={len(f.pads):3d}  bbox=({b[0]:6.2f},{b[1]:6.2f})-({b[2]:6.2f},{b[3]:6.2f})")
