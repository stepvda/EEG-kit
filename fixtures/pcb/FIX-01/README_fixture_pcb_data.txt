FIX-01 Rev A -- fixture board data
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

  FIX-01-Edge_Cuts.gbr                       641 bytes  31684c5b32eb4c3ae9d88770b8b7c8c7cdf4efe5eee1a2be16fbd475d4d84bfa
  FIX-01-F_Silkscreen.gbr                  56081 bytes  b75fc880877319f7a008060ffb13912b75a8c6a5bea5b50184eb746b2b561e0d
  FIX-01-NPTH.drl                            471 bytes  aae5ccd02c7d3bef2c7cefe8690ed0f93d272627115344359436bdd7157c9f27
  FIX-01-Zoning.gbr                         7614 bytes  fbc7ed159a2200d795f9209b3702c23f74ca8ce7978cecdf2744a4d7209d9af2
  FIX-01_constraints.txt                    5707 bytes  5c3c4c0d396127177e67926f88c9bfc2ff6e72045639f5e3b20da11b8572ac4b
  FIX-01_netlist.json                      14926 bytes  667c2b284de9039c260478eaa05e46922ace10fcfa48ab7988a28e7e6376fbb6
  FIX-01_netlist.txt                       30346 bytes  b0cf17c3e2df4fc2f21abde089343e4cf328bec1c8f83fb6ea7c860c6693c152

LAYER MAP

  FIX-01-Edge_Cuts.gbr        board outline, profile on the centre line
  FIX-01-F_Silkscreen.gbr     panel legend, zone captions, the two bench warnings
  FIX-01-Zoning.gbr           zone boundaries, keep-outs, screening can, connector
                              way-1 marks.  A mechanical layer, not copper.
  FIX-01-NPTH.drl             four M3 mounting holes.  No plated programme exists.
  FIX-01_netlist.txt          the connectivity, human-readable
  FIX-01_netlist.json         the same connectivity, machine-readable
  FIX-01_constraints.txt      stack-up, rules, zoning and the area budget

GERBER CONVENTIONS

  Gerber X2, format 4.6 absolute, metric, leading zeros omitted, bottom-left origin with
  Y up -- the same %FSLAX46Y46*% / %MOMM*% pair EEG-CAR-01 and WH-BUS-01 use, so one CAM
  import setting covers every board in this package. Every file carries a
  TF.FileFunction attribute and a G04 line saying it is not a fabrication set.

AREA BUDGET

  board area                          16000 mm2  (160.0 x 100.0)
   83 relays at  70.0 mm2 each       5810 mm2  ASSUMED envelope, not a datasheet figure
   77 resistors, 0603                  462 mm2
   16 integrated circuits             1664 mm2  SOIC-20W nominal
    1 controller module               1071 mm2  Raspberry Pi Pico outline
   35 connector ways                  533 mm2
      total occupied                   9540 mm2  60 % of the board
      free                             6460 mm2
      of which inside the can          2400 mm2  shared with the relay and resistor counts above

  VERDICT: feasible at the assumed envelope. The outline carries the bill of materials
  at 60 % occupancy against a 60 % working limit for a two-layer board of this density.
  The largest relay land-pattern envelope the outline can carry is 70.7 mm2, so the
  fitted relay's land pattern must be at or under that -- roughly 10.1 x 7.0 mm at the
  aspect ratio assumed here. That is the number to check against the Omron G6K-2F-Y
  datasheet before any layout is commissioned, and it is the only datasheet figure the
  outline depends on. THE MARGIN IS 1.0 %. A board that closes only if the relay is at
  or under the size assumed for it is a board that does not close if the assumption is 2
  mm out on one axis, so this outline is provisional until the datasheet is opened --
  and FIX-01's enclosure, the Hammond 1590D at 188 x 119 mm, has room for a larger board
  if it needs one.

