WH-BUS-01 Rev A -- fabrication data manifest
generated 2026-09-01 from package_v2.4/tools/wh_bus.py

WHAT THIS BOARD IS

  The contact-light bus board.  It sits at frame node N1, immediately inside occipital
  entry OE-2 under its own cover strip, and splits LED_V from WH-02 into the eight tails
  that reach the second lead of each site LED.  It replaces what would otherwise have been
  eight crimp splices, and it is the reason WH-EEG-008 can say there is no splice anywhere
  in the kit.  Ten plated pads, one copper bar, no components.

  PARTS-EEG-019 Rev B registered it and recorded that no Gerber set existed.  This is that
  set.  Two things in that register entry are superseded by this data and need re-issuing:
  the board is TWO layers, not single-layer, because the pads are plated through holes; and
  "specified, not built" is now "specified, data released for quotation".

LAYER MAP
  WH-BUS-01-F_Cu.gbr           top copper          Copper,L1,Top,Signal
  WH-BUS-01-B_Cu.gbr           bottom copper       Copper,L2,Bot,Signal
  WH-BUS-01-F_Mask.gbr         top solder mask     Soldermask,Top
  WH-BUS-01-B_Mask.gbr         bottom solder mask  Soldermask,Bot
  WH-BUS-01-F_Silkscreen.gbr   top legend          Legend,Top
  WH-BUS-01-B_Silkscreen.gbr   bottom legend       Legend,Bot
  WH-BUS-01-Edge_Cuts.gbr      board profile       Profile,NP
  WH-BUS-01-PTH.drl            plated holes, Excellon 2, metric
  WH-BUS-01-IPC-D-356A.ipc     netlist for bare-board electrical test

  There is no paste layer, no CPL file and no NPTH file.  Nothing is surface-mounted,
  nothing is placed, and the only holes are the ten plated pads.  Their absence is the
  design, not an omission.

  WH-BUS-01_RevA_gerber_X2.zip holds the nine files above and nothing else, which is
  the same convention EEG-CAR-01 uses.  It is the imaging data only: send this README and
  WH-BUS-01_RevA_placement_and_BOM.txt with it, because the stack-up, the finish and
  the panel are not anywhere in the Gerbers.

FORMAT
  Gerber X2 (RS-274X with file attributes), 4.6 absolute, metric, leading zeros omitted.
  Origin is the BOTTOM-LEFT board corner with Y up, which is also the origin of the drill
  file and of the netlist.  Unlike EEG-CAR-01 there is no top-left design source and so no
  y conversion: this board is laid out directly in fabrication coordinates.

  Both layers are written in board coordinates as seen from the top, as KiCad writes them.
  The bottom legend is mirrored in the data so that it reads correctly on the finished
  board; do not mirror it again.

THE BOARD
  Size                     14.0 x 10.0 mm, rectangular, no cut-outs, no slots
  Layers                   two: L1 signal, L2 signal.  No plane, no pour
  Stack-up                 mask / 35 um L1 / FR-4 core 0.71 / 35 um L2 / mask
                           = 0.80 mm +/- 10 % finished, mask included.  0.71 mm is
                           a stock core; the fabricator may substitute its nearest and hold
                           the finished 0.80 mm
  Material                 FR-4, Tg >= 150 C, 1 oz (35 um) copper both sides.  Tg 130 would
                           carry this board, but the carrier is already quoted at Tg 150 and
                           one material across both boards is one qualification, not two
  Finish                   ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um, as EEG-CAR-01.
                           Lead-free HASL is acceptable on notice: this is a two-net board
                           with a 0.40 mm annular ring and no fine pitch, so
                           coplanarity buys nothing here.  ENIG is specified for shelf life
                           and because the same fabricator is already quoting it
  Mask / legend            green LPI both sides; white legend both sides
  Mask expansion           0.051 mm per side, ten openings each side, none tented
  Pads                     ten, 1.60 mm, on a 2.70 x 4.80 mm grid.
                           Pad 9 is square and marks the WH-02 input end
  Plated holes             ten, 0.80 mm finished, one tool.  Aspect ratio 1.0:1
  Annular ring             0.40 mm
  Minimum track            1.20 mm (the LED_V bar).  Nothing here is near a fabricator's
                           limit; the width is for the solder joints, not for the 10.4 mA
  Minimum clearance        1.10 mm, LED_V to the LED_GND island
  Copper to board edge     0.60 mm minimum
  Legend to mask opening   0.17 mm minimum
  Class                    IPC-6012 class 2 (fabrication), IPC-A-600 class 2 (bare board)
  Electrical test          100 % to the supplied IPC-D-356A netlist.  This is not optional
                           on this board: the isolation of pad 10 from the LED_V bar is the
                           one property that a visual inspection will not catch
  Conformal coating        none

PANELISATION
  Supplied as a 5 x 4 V-scored array, 20 up, step 14.0 x 10.0 mm, with 5 mm rails on all
  four sides: panel 80.0 x 50.0 mm. The boards abut: the step IS the board size, there is
  no gap and no rout line between them. One panel covers Phase 1 (2 units) and Phase 2 (10
  kits) with eight spares, which is the whole current buy.

  V-scoring is possible because the nearest copper is 0.60 mm from the board edge on every
  side. A fabricator whose rule is 0.80 mm copper-to-score cannot V-score this layout and
  should tab-rout instead -- 2.0 mm tabs, two per 14.0 mm edge, five 0.50 mm mouse-bite
  holes per tab -- on notice to the programme rather than silently.

  The residual web a V-score leaves in 0.80 mm material is the fabricator's standard and
  is not specified here. 0.80 mm is at or near the lower V-score limit at several houses,
  so this is the line of the panel spec most likely to come back as a question. It has not
  been tried.

WHAT IS NOT IN THIS DATA SET
  No fabrication drawing.  On a rectangular board with one drill size and no mechanical
  features, this README and the placement note carry everything a drawing would, and a
  drawing that repeats them is one more thing to keep in step.
  No impedance control, no coupon, no cross-section.  Nothing on this board is a
  transmission line; the fastest edge it sees is a 240 Hz phase reversal.
  No pocket, no mounting feature and no location dimension at node N1.  HM-01 has no
  geometry for this board, so where it beds is undefined.  That is an open item against the
  mechanical package.
  No measurement of anything.  Nothing here has been fabricated, soldered or tested.

SHA-256
  b8a3da8a8b3b17b9cd2cfd1a6b35e6d4d1bbd8f43c480834092e7cde0ee96946  WH-BUS-01-B_Cu.gbr
  5b6f38466af47124e30be0155b44badbc162629ed4ef7c226b6ac9aac72c0559  WH-BUS-01-B_Mask.gbr
  c0826f33cb24feb1b6e3d155c1fdfac52c32d4dfd15c92c1ba9e562045875ab8  WH-BUS-01-B_Silkscreen.gbr
  183063f8ef65d3ef76ad87917d9b56ba72d9315b4ba7c39f6f059a5bae3231fd  WH-BUS-01-Edge_Cuts.gbr
  3c3cd58277f597d5a8388ac2094366329703cc778a32292d62b9d76b37a8bc22  WH-BUS-01-F_Cu.gbr
  9444270deb07227352fb7b0f4c3096e1f12149ab8886d632e9a8f4f5bfb3e127  WH-BUS-01-F_Mask.gbr
  e26dad30a94ce7046c5c4936cb6b94113995c50804c733d6fe3dbabb6ab31e59  WH-BUS-01-F_Silkscreen.gbr
  2beefc0802e44eebc8cced8124dac128a82e07339e3a416b12af4872c985d368  WH-BUS-01-IPC-D-356A.ipc
  8eb266550445d67a8ed20558c32fca783c37efccb3de73378c9861f889feeccb  WH-BUS-01-PTH.drl
  21404a2462192d34f4ba35cba30a030f2b2adeb47930b09ba7aa61e9cb46173f  WH-BUS-01_RevA_gerber_X2.zip
  eca563999ade591725f1e12e660dfad31e43f9e57ffc642b19f21be18bf3c9cb  WH-BUS-01_RevA_placement_and_BOM.txt
