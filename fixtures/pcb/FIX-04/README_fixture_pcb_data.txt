FIX-04 Rev A -- fixture board data
TI One Voice research programme -- CC BY-SA 4.0
Generated 2026-09-02 by package_v2.4/tools/fixture_gen.py.  Regenerate with: python3 tools/fixture_gen.py --pcb

READ THIS FIRST

  THIS IS NOT A FABRICATION SET. There is no copper layer, no plated drill programme, no
  solder-paste layer and no assembly drawing in this directory, and a board fabricated
  from what is here would be a bare piece of FR-4 with four holes in it. What is here is
  everything about the board that JIG-EEG-009 determines: the outline, the mounting
  pattern, the zoning, the panel legend, the non-plated drill and the complete netlist.
  The copper is a layout engineer's work and is priced in JIG-EEG-009 section 6.1 and
  scheduled in section 6.3.

FILES

  FIX-04-Edge_Cuts.gbr                       639 bytes  ad1a582945a772279cb2d628d44144a514b64347631a50bde5b2989eb3cfa310
  FIX-04-F_Silkscreen.gbr                  45713 bytes  ed385e75e4d41158cc3588f048b93dd8de0ea8e93c621091a2bd895246461bda
  FIX-04-NPTH.drl                            471 bytes  24b1137385c4715596a66d318aaf9b5bdda7bd83e695c576f61715b18038b23c
  FIX-04-Zoning.gbr                         7379 bytes  f9a90f1e2a4c9ae84a153bece3d8986ca332d26cfef3b5fe9532073ef4a66578
  FIX-04_constraints.txt                    4830 bytes  a8f124ae5d3256dfd3e2ee3f656615b81d2e219073c3d0d0ecadeed35b038b14
  FIX-04_netlist.json                       4324 bytes  e6dd10d8acdd05938d05b6f8b56d5aa4c1cdcd929b049e32e0c8433c104e94c6
  FIX-04_netlist.txt                        8462 bytes  ef0af1abda7964c48241b06286c804e00c38388610cb745ba8878134cc70425f

LAYER MAP

  FIX-04-Edge_Cuts.gbr        board outline, profile on the centre line
  FIX-04-F_Silkscreen.gbr     panel legend, zone captions, the two bench warnings
  FIX-04-Zoning.gbr           zone boundaries, keep-outs, screening can, connector
                              way-1 marks.  A mechanical layer, not copper.
  FIX-04-NPTH.drl             four M3 mounting holes.  No plated programme exists.
  FIX-04_netlist.txt          the connectivity, human-readable
  FIX-04_netlist.json         the same connectivity, machine-readable
  FIX-04_constraints.txt      stack-up, rules, zoning and the area budget

GERBER CONVENTIONS

  Gerber X2, format 4.6 absolute, metric, leading zeros omitted, bottom-left origin with
  Y up -- the same %FSLAX46Y46*% / %MOMM*% pair EEG-CAR-01 and WH-BUS-01 use, so one CAM
  import setting covers every board in this package. Every file carries a
  TF.FileFunction attribute and a G04 line saying it is not a fabrication set.

AREA BUDGET

  board area                           9600 mm2  (120.0 x 80.0)
   24 relays at  70.0 mm2 each       1680 mm2  ASSUMED envelope, not a datasheet figure
    0 resistors, 0603                    0 mm2
    3 integrated circuits              312 mm2  SOIC-20W nominal
    1 controller module               1071 mm2  Raspberry Pi Pico outline
   34 connector ways                  518 mm2
      total occupied                   3581 mm2  37 % of the board
      free                             6019 mm2

  VERDICT: feasible at the assumed envelope. The outline carries the bill of materials
  at 37 % occupancy against a 60 % working limit for a two-layer board of this density.
  The largest relay land-pattern envelope the outline can carry is 160.8 mm2, so the
  fitted relay's land pattern must be at or under that -- roughly 15.2 x 10.6 mm at the
  aspect ratio assumed here. That is the number to check against the Omron G6K-2F-Y
  datasheet before any layout is commissioned, and it is the only datasheet figure the
  outline depends on.

