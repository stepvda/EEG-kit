========================================================================================
README FOR BIDDER -- WH-BUS-01 -- bare contact-light bus board
TI One Voice / EEG field kit -- ticket BSY-598327
========================================================================================

Submitted through https://www.pcbcart.com/assembly at your request. The form's Notes
control is a single-line input, so the notes arrive there as one paragraph with the line
breaks removed. The short form is in that box and this file is the full text. Where the
two differ, THIS FILE IS THE ONE THAT COUNTS.

Contact: Stephane van der Aa, TI One Voice, Belgium
         +32 493 70 16 01   stephane@stepvda.com

----------------------------------------------------------------------------------------
THE SPECIFICATION
----------------------------------------------------------------------------------------

Every figure below is generated from the design source, not transcribed.

  Dimensions (X by Y)
      14.0 x 10.0 mm
      [source: wh_bus.py BOARD_W, BOARD_H (PARTS-EEG-019 Rev B)]

  Layers
      2
      [source: wh_bus.py -- L1 signal, L2 signal, no plane]

  Finished thickness
      0.80 mm +/- 10 %
      [source: wh_bus.py BOARD_T]

  Material
      FR-4, Tg >= 150 C
      [source: wh_bus.py -- one material across both boards is one qualification]

  Outer copper
      35 um (1 oz) both sides
      [source: wh_bus.py -- 1 oz copper both sides]

  Stack-up
      mask / 35 um L1 / FR-4 core 0.71 / 35 um L2 / mask = 0.80 mm +/- 10 %
      [source: wh_bus.py CORE, BOARD_T -- 0.71 mm is a stock core; the fabricator may substitute its nearest and hold the finished thickness]

  Surface finish
      ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um
      [source: wh_bus.py -- as EEG-CAR-01]

  Solder mask
      green LPI both sides
      [source: wh_bus.py]

  Silkscreen legend
      white, both sides
      [source: wh_bus.py]

  Minimum track
      1.20 mm (the LED_V bar)
      [source: wh_bus.py BUS_W]

  Plated through holes
      10 per board, 0.80 mm finished, 1.60 mm pad, one tool
      [source: wh_bus.py PADS, HOLE_D, PAD_D]

  Vias
      none -- the ten plated holes are component pads
      [source: wh_bus.py -- ten pads and one copper bar, no separate vias]

  Delivery method
      Panel with technical rail
      [source: wh_bus.py PANEL_COLS, PANEL_ROWS, PANEL_RAIL -- rails on all four sides]

  Panel
      5 x 4 V-scored array, 20 up, step 14.0 x 10.0 mm, 5 mm rails on all four sides:
      panel 80.0 x 50.0 mm
      [source: wh_bus.py PANEL_COLS, PANEL_ROWS, PANEL_RAIL, BOARD_W, BOARD_H]

  Acceptance class
      IPC-6012 class 2 (fabrication), IPC-A-600 class 2 (bare board)
      [source: wh_bus.py]

  Electrical test
      100 % to the supplied IPC-D-356A netlist
      [source: wh_bus.py -- not optional here: the isolation of pad 10 from the LED_V bar is the one property a visual inspection will not catch]

  Assembly side(s)
      Not assembled -- bare board only
      [source: wh_bus.py -- no component, no paste layer, no CPL, no stencil]

  Quantities
      per panel of 20; programme phases 2 / 10 / 25 / 50 kits
      [source: wh_bus.py PANEL_COLS/PANEL_ROWS; RFQ-EEG-001 Rev E, Scope]

  Quantity breaks (panels)
      1 | 2 | 3
      [source: computed: ceil(kits / 20) for the 2 / 10 / 25 / 50 kit phases of RFQ-EEG-001 Rev E, at one board per kit and 20 up per panel (2 kits -> 1 panel, 10 kits -> 1 panel, 25 kits -> 2 panels, 50 kits -> 3 panels)]

  Different designs in panel
      1
      [source: wh_bus.py -- one design, stepped 5 x 4]

  Panel route process
      Panel as V-Scoring
      [source: wh_bus.py PANEL_COLS/PANEL_ROWS -- a V-scored array]

  X-out allowance in panel
      No
      [source: not specified anywhere in the design; No is the conservative answer and the eight spares in the 20-up array already cover yield]

  Custom testing
      No
      [source: bare board, netlist test only]

  IC programming
      No
      [source: no component on this board]

  Production and shipping origin
      As decided by PCBCART
      [source: raised in the notes, as for the carrier]

----------------------------------------------------------------------------------------
THE NOTES
----------------------------------------------------------------------------------------

1. TICKET BSY-598327

   This is the same request already in your queue as ticket BSY-598327, raised with Genny
   (Huang Jing Yi, usa.office@pcbcart.com). It is submitted through the web form because
   that is what you asked us to do. It is not a second, separate enquiry -- please
   attach it to the existing ticket rather than opening another.

2. THE GEOMETRY YOU ARE QUOTING IS WITHDRAWN. THIS IS A BUDGETARY
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
   giving a required-by date, because there is not one to give.

3. THE STACK-UP IS SPECIFIED, NOT DEFAULT

   mask / 35 um L1 / prepreg 0.200 / 17 um L2 / core 1.065 / 17 um L3 / prepreg 0.200 / 35 um L4 / mask = 1.60 mm +/- 10 %

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
   MICROSECTION coupon is, and it is sectioned to verify layer order.

4. U1, U2, U3 ARE TSSOP-14, NOT SOIC-14

   U1, U2 and U3 are TI OPA4376AIPWR in TSSOP-14 (4.4 x 5 mm, 0.65 mm pitch). Any earlier
   paperwork from us that said SOIC-14 was wrong. The BOM and the CPL in this submission
   are correct.

   Please price the line, but do NOT treat this as a confirmed part selection on your
   side: the correction is ours to make and we will restate it against the Rev C data.
   If your quoting system has already been told SOIC-14 for this ticket, please correct
   it there too.

5. J15, J16, J17 ARE PATIENT-CONNECTED AND NON-SUBSTITUTABLE

   J15, J16 and J17 are Staubli SLB1,5-F / LB-I1,5 DIN 42802 1.5 mm touchproof sockets.
   They are the connection to a person. They are NON-SUBSTITUTABLE: no equivalent, no
   alternate, no "same form and fit" part is acceptable on those three lines, whatever
   the lead time.

   If you cannot source them, quote the board WITHOUT them and say so, and we will supply
   them on consignment. Do not quote an alternative and do not fit one.

6. TWELVE MODULE TYPES ARE NOT IN THE BOM, AND THE UNIT DOES NOT WORK
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
   who buys them.

7. FOUR LOT DOCUMENTS ARE CONDITIONS OF ACCEPTANCE, NOT EXTRAS

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
   them is something you do not do.

8. 2 / 10 / 25 / 50 ARE PHASES, NOT ALTERNATIVES

   Please quote all four quantities. They are successive phases of ONE programme, not
   four alternative order sizes we are choosing between: 2 for the first build, then 10,
   then 25, then 50, each following the one before.

   That matters for how you price it. Tooling amortised across the series, and any price
   you can hold across the phases, is more useful to us than four independent unit
   prices. If a larger phase would change the process -- panelisation, test strategy,
   material buy -- please say so against that phase.

9. OPEN HARDWARE, NON-PROFIT, AND AN OPEN DOOR

   This design is open hardware, published under CC BY-SA 4.0, and the study it serves is
   run by a non-profit. Everything in this submission -- the Gerbers, the BOM, the
   specification -- is public.

   If sponsorship of any part of the work is something PCBCart would consider, it would
   be welcome and we would credit it. It is NOT assumed and it is not a condition of
   anything: a straight commercial quotation is exactly what we are asking for here, and
   a plain price is a complete answer to this submission.

----------------------------------------------------------------------------------------
THE FILES IN THIS SUBMISSION
----------------------------------------------------------------------------------------

  WH-BUS-01_RevA_gerber_X2.zip
      Rev A fabrication data, Gerber X2 plus drill and IPC-D-356A netlist. [uploaded in
      the PCB File slot]

  WH-BUS-01_RevA_placement_and_BOM.txt
      The bare-board BOM note: one line, no components, no CPL and no stencil, because
      there is no part to place.

  WH-BUS-01_RevA_BOM_and_notes.zip
      This file: the bundle in the BOM File slot, holding everything above except the
      fabrication ZIP, plus this README.

  Every file above is listed with its SHA-256 in the covering record.
  Please quote the checksum of anything you cannot open.

========================================================================================
END
========================================================================================
