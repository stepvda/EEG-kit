========================================================================================
README FOR BIDDER -- EEG-CAR-01 -- assembled carrier
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
      150.0 x 130.0 mm
      [source: design.py BOARD_W, BOARD_H]

  Layers
      4
      [source: design.py fabrication note 2; DSN-EEG-003 Rev D section 3.2]

  Layer roles
      L1 signal, L2 reference plane, L3 reference plane, L4 signal
      [source: design.py fabrication note 2; DSN-EEG-003 Rev D section 3.2]

  Finished thickness
      1.60 mm +/- 10 %
      [source: design.py fabrication note 2; DSN-EEG-003 Rev D section 3.2]

  Material
      FR-4, Tg >= 150 C
      [source: design.py fabrication note 2; DSN-EEG-003 Rev D section 3.2]

  Outer copper
      35 um (1 oz) finished
      [source: design.py fabrication note 2]

  Inner copper
      17 um (0.5 oz)
      [source: design.py fabrication note 2]

  Stack-up (SPECIFIED, not default)
      mask / 35 um L1 / prepreg 0.200 / 17 um L2 / core 1.065 / 17 um L3 / prepreg 0.200
      / 35 um L4 / mask = 1.60 mm +/- 10 %
      [source: design.py fabrication note 2; DSN-EEG-003 Rev D section 3.2]

  Surface finish
      ENIG, Au 0.05-0.10 um over Ni 3.0-6.0 um
      [source: design.py fabrication note 3; DSN-EEG-003 Rev D section 3.2]

  Solder mask
      green LPI both sides
      [source: design.py fabrication note 4]

  Silkscreen legend
      white, both sides
      [source: design.py fabrication note 4]

  Minimum track / clearance
      0.20 / 0.20 mm
      [source: design.py fabrication note 5; DSN-EEG-003 Rev D section 3.2]

  Vias
      through vias only, 0.60 mm pad / 0.30 mm finished hole, tented both sides. No
      blind, buried, back-drilled, filled or plugged vias anywhere
      [source: design.py fabrication note 6; DSN-EEG-003 Rev D section 3.2 (the 'no blind or buried' wording)]

  Smallest plated hole
      0.30 mm
      [source: design.py fabrication note 7]

  Largest plated hole
      1.70 mm (J15-J17)
      [source: design.py fabrication note 7]

  Blind / buried vias
      No
      [source: DSN-EEG-003 Rev D section 3.2 -- through vias only]

  Controlled impedance
      No
      [source: design.py fabrication note 10]

  Acceptance class
      IPC-6012 class 2 (fabrication), IPC-A-600 class 2 (bare board), IPC-A-610 class 2
      (assembly)
      [source: design.py fabrication note 9 (first two); DSN-EEG-003 Rev D section 3.2 (all three)]

  Electrical test
      100 % to the supplied IPC-D-356A netlist, 156 nets
      [source: design.py fabrication note 9; net report nets = 156]

  Components / pads / nets
      211 / 636 / 156
      [source: kicad/EEG-CAR-01_RevB_netreport.json, generated from design.py; designator count cross-checked against len(design.C) = 211]

  Assembly side(s)
      Single side
      [source: design.py assembly note 1; DSN-EEG-003 Rev D section 3.2 -- 'L4 carries routing, copper and legend, and no parts']

  Delivery method
      Single board without technical rail
      [source: DSN-EEG-003 section 3.2: 150.0 x 130.0 mm rectangular, no cut-outs; design.py fabrication note 12 leaves panelisation to the fabricator]

  Quantities
      2, 10, 25, 50
      [source: RFQ-EEG-001 Rev E, Scope -- successive phases of one programme]

  Quantity breaks (boards)
      2 | 10 | 25 | 50
      [source: RFQ-EEG-001 Rev E, Scope; one carrier per kit]

  Custom testing
      No
      [source: TST-EEG-004 Rev C exists, but the four fixtures of JIG-EEG-009 have no copper and cannot be built yet -- see the bidder notes]

  IC programming
      No
      [source: Provisioning writes the ATECC608B configuration zone irreversibly and only 4 of its 128 bytes have been reviewed -- see the bidder notes]

  Production and shipping origin
      As decided by PCBCART
      [source: Raised in the notes instead: a Thailand build changes duty and lead time, which is a commercial conversation and not a form field]

  Lot coupon
      One four-layer microsection coupon per lot
      [source: design.py fabrication note 13]

  Lot documents
      certificate of conformance; 100 % electrical test report to the supplied
      IPC-D-356A; ENIG thickness report (XRF, Au and Ni, min 3 points); layer-to-layer
      registration report; microsection report including the internal annular ring,
      accept limit 0.025 mm
      [source: design.py fabrication notes 13 and 14]

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

  EEG-CAR-01_RevB_gerber_X2.zip
      Rev B fabrication data, Gerber X2 plus drill and IPC-D-356A netlist. The geometry
      being quoted, and the geometry that is withdrawn. [uploaded in the PCB File slot]

  EEG-CAR-01_RevC_BOM.csv
      The CORRECTED Rev C BOM. Supersedes anything sent earlier. Carries the
      substitution column, including the three non-substitutable lines.

  EEG-CAR-01_RevC_CPL_SMT_top.csv
      Surface-mount placement, PROVISIONAL -- the file says so on its first line and
      that line is deliberately left in.

  EEG-CAR-01_RevC_CPL_THT_top.csv
      Through-hole placement, PROVISIONAL -- likewise.

  EEG-CAR-01_RevC_BOM_CPL_and_notes.zip
      This file: the bundle in the BOM File slot, holding everything above except the
      fabrication ZIP, plus this README.

  Every file above is listed with its SHA-256 in the covering record.
  Please quote the checksum of anything you cannot open.

========================================================================================
END
========================================================================================
