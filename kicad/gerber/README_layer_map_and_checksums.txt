EEG-CAR-01 Rev B -- fabrication data manifest
generated 2026-09-02 from package_v2.4/tools/design.py

LAYER MAP
  EEG-CAR-01-F_Cu.gbr           top copper          Copper,L1,Top,Signal
  EEG-CAR-01-In1_Cu.gbr         inner copper L2     Copper,L2,Inr,Signal
  EEG-CAR-01-In2_Cu.gbr         inner copper L3     Copper,L3,Inr,Signal
  EEG-CAR-01-B_Cu.gbr           bottom copper       Copper,L4,Bot,Signal
  EEG-CAR-01-F_Mask.gbr         top solder mask     Soldermask,Top
  EEG-CAR-01-B_Mask.gbr         bottom solder mask  Soldermask,Bot
  EEG-CAR-01-F_Silkscreen.gbr   top legend          Legend,Top
  EEG-CAR-01-B_Silkscreen.gbr   bottom legend       Legend,Bot
  EEG-CAR-01-F_Paste.gbr        stencil (top only)  Paste,Top
  EEG-CAR-01-Edge_Cuts.gbr      board profile       Profile,NP
  EEG-CAR-01-User_Drawings.gbr  reference only, do not image
  EEG-CAR-01-PTH.drl            plated holes, Excellon 2, metric
  EEG-CAR-01-NPTH.drl           non-plated holes, Excellon 2, metric
  EEG-CAR-01-IPC-D-356A.ipc     netlist for bare-board electrical test

FORMAT
  Gerber X2 (RS-274X with file attributes), 4.6 absolute, metric,
  leading zeros omitted.  Origin is the BOTTOM-LEFT board corner with Y up,
  which is also the origin of both drill files and of the CPL files.
  The design source uses a top-left origin with Y down; the conversion is
  y_gerber = 130.0 - y_design, applied once, in package_v2.4/tools/gerber.py.

SHA-256
  afd374133cec74732d8a3fde9ae7617e3ad56c6a67ad0d30e05777d58ff4c2f0  EEG-CAR-01-B_Cu.gbr
  2a88a9a57303df75b750859a3e8fd09e7305f6a919099001f6ca3bfe734e7c7f  EEG-CAR-01-B_Mask.gbr
  1385d91e30634c763d53d7e22735db07d6fa84051b8d127c4904b6006c5f4962  EEG-CAR-01-B_Silkscreen.gbr
  66ecda070a0393e94042580b419965f87b1e6f1dc27e8a02722f7b974a63f985  EEG-CAR-01-Edge_Cuts.gbr
  97beec4306cb4a2a1ed8c18a122bfcbbbe5dd497ec7bbf7ae94eb95afc89abfd  EEG-CAR-01-F_Cu.gbr
  c5d13b597ba09862ab1aa20c9f0da2132cb6fc56cce91e0ab4d4a9591444da3a  EEG-CAR-01-F_Mask.gbr
  a8730108b720e543aaafb1cae683198b307845f4819cd94e2ad39949cf42c3a1  EEG-CAR-01-F_Paste.gbr
  3980bdffd9e054e4c85fe0bee458831c8f01c8d41903f6e2572abb31b73f9676  EEG-CAR-01-F_Silkscreen.gbr
  db043b4b6d498e3b5fc108b25c8d125b1193da58892d28d3e74db9839165c00f  EEG-CAR-01-IPC-D-356A.ipc
  800112e66c689719c829b9ee6886c85d7f71c1d1d50f17931820fea247f525eb  EEG-CAR-01-In1_Cu.gbr
  1c5b7e1fe2facbbdd02e14a50bfd88ed52aeed5f0792b8602a16bbe540842df0  EEG-CAR-01-In2_Cu.gbr
  6d125eebaeea2aba11472f155ff5dab93dd1fb56329b540edc2af1a677502f8e  EEG-CAR-01-NPTH.drl
  0ce600f55d1c3fbfb64f55d04a898d6de84edab92654d4044bdad17387de2c1a  EEG-CAR-01-PTH.drl
  018ba876500aa4cbae086586b80795f9e5a2353015026010b2e87964d9ba7b07  EEG-CAR-01-User_Drawings.gbr
  756f8b0da9bbfbb97711abca7c6c36f86ac36fde7958b002631508cf03780679  EEG-CAR-01_RevB_gerber_X2.zip
