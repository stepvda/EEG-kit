fixtures/ -- test fixture data for JIG-EEG-009 Rev B
TI One Voice research programme (one.witysk.org), Brussels, Belgium
Licence: CC BY-SA 4.0
Generated 2026-09-02 by package_v2.4/tools/fixture_gen.py, except firmware/, which is hand-written source.

WHAT IS HERE

  JIG-EEG-009 Rev B designs four fixtures and prices them. Three things it called for
  had no files: the fixture printed circuit boards, the printed fixture parts, and the
  controller firmware. This directory is those three.

  firmware/        M1, M2 and M3 controller firmware, and the FIXPROTO v1 host
                   protocol of JIG-EEG-009 section 8. Hand-written C, built for
                   the RP2040 and tested natively -- see firmware/README.md.
  pcb/FIX-01/      board data for the injection fixture.  NOT A FABRICATION SET.
  pcb/FIX-04/      board data for the harness scanner.   NOT A FABRICATION SET.
  step/, stl/      the seven printed fixture parts, one parametric model each.
  MANIFEST.json    every file above with its SHA-256, in the schema
                   mech/MANIFEST.json uses.

WHAT IS NOT HERE, AND WHY

  There is no copper layer for either fixture board. The outline, the mounting pattern,
  the zoning, the legend, the non-plated drill and the complete netlist are released
  because JIG-EEG-009 determines them; the copper is not derivable from any document in
  this package and depends on one datasheet the package does not carry, the land pattern
  of the Omron G6K-2F-Y. Each board's constraints file computes what that land pattern
  has to be for its outline to be feasible.

  There is no I2S driver in the M2 firmware. The specification the block has to meet is
  in the source where the code will go, and the command layer refuses the tone verbs
  rather than reporting a start time for a tone nobody played.

NOTHING HERE HAS BEEN BUILT

  No fixture has been fabricated, printed, assembled or measured, and no safety engineer
  has reviewed any of it (JIG-EEG-009 section 7). Every dimension is a model figure and
  every constant marked as stated is stated, not measured.

AREA BUDGET SUMMARY

  FIX-01  9540 of 16000 mm2 (60 %), largest relay land pattern 70.7 mm2 -- feasible
  FIX-04  3581 of 9600 mm2 (37 %), largest relay land pattern 160.8 mm2 -- feasible

FILES

  README_fixture_data_index.txt                            6391  e99587fc7aaabf4d
  firmware/CMakeLists.txt                                  2383  88d755fd88ca5b07
  firmware/README.md                                       5066  db5373c157823d58
  firmware/include/fixhal.h                                4811  7a1047075eef887e
  firmware/include/fixproto.h                              4318  cffd4fb32c7d2f8a
  firmware/src/fix_m1.c                                   21324  f263af986b6580d0
  firmware/src/fix_m2.c                                    9277  b858f291e535bf11
  firmware/src/fix_m3.c                                    7851  fb463ea8db67587a
  firmware/src/fixproto.c                                 11657  f7af78cd1cb66753
  firmware/src/hal_rp2040.c                                9726  5f173ed13bb249c5
  firmware/src/main.c                                       652  17cc8e6ec93e9f8f
  firmware/test/.gitignore                                    7  181314065df2f2fd
  firmware/test/hal_sim.c                                  7672  1c640b69e5091102
  firmware/test/host_test.c                               11175  66efcf3b2dcfe10c
  firmware/test/run.sh                                     2317  b1389b7d6ab11f41
  firmware/test/stubs/hardware/adc.h                        334  715ad41676ce416f
  firmware/test/stubs/hardware/gpio.h                       606  225822aba835497f
  firmware/test/stubs/hardware/i2c.h                        571  da69a3078718c758
  firmware/test/stubs/hardware/spi.h                        407  aa5c74d4300db213
  firmware/test/stubs/pico/stdlib.h                         748  95ad7be5bba948e0
  pcb/FIX-01/FIX-01-Edge_Cuts.gbr                           641  31684c5b32eb4c3a
  pcb/FIX-01/FIX-01-F_Silkscreen.gbr                      56081  b75fc880877319f7
  pcb/FIX-01/FIX-01-NPTH.drl                                471  aae5ccd02c7d3bef
  pcb/FIX-01/FIX-01-Zoning.gbr                             7614  fbc7ed159a2200d7
  pcb/FIX-01/FIX-01_constraints.txt                        5707  5c3c4c0d39612717
  pcb/FIX-01/FIX-01_netlist.json                          14926  667c2b284de9039c
  pcb/FIX-01/FIX-01_netlist.txt                           30346  b0cf17c3e2df4fc2
  pcb/FIX-01/README_fixture_pcb_data.txt                   4086  ff9c12e94cac7c62
  pcb/FIX-04/FIX-04-Edge_Cuts.gbr                           639  ad1a582945a77227
  pcb/FIX-04/FIX-04-F_Silkscreen.gbr                      45713  ed385e75e4d41158
  pcb/FIX-04/FIX-04-NPTH.drl                                471  24b1137385c47155
  pcb/FIX-04/FIX-04-Zoning.gbr                             7379  f9a90f1e2a4c9ae8
  pcb/FIX-04/FIX-04_constraints.txt                        4830  a8f124ae5d3256df
  pcb/FIX-04/FIX-04_netlist.json                           4324  e6dd10d8acdd0593
  pcb/FIX-04/FIX-04_netlist.txt                            8462  ef0af1abda7964c4
  pcb/FIX-04/README_fixture_pcb_data.txt                   3642  005bd6093137e75d
  step/FIX-01E_colorimeter_manifold.step                 644043  1fd066beb1c9db52
  step/FIX-01E_sensor_carrier.step                       126181  2a503f7ce292930c
  step/FIX-02A_sealing_lip.step                           13688  7988d92d1b544e37
  step/FIX-02A_voice_coupler_body.step                   396266  ff626033cdd8e9f0
  step/FIX-02B_room_coupler_body.step                    434027  8f80a9265e2bc42e
  step/FIX-02B_sealing_lip.step                           13699  c7b97b4cc71b005b
  step/FIX-03A_carrier_nest.step                         418015  4623574d970a7d60
  stl/FIX-01E_colorimeter_manifold.stl                   536584  0bf3c7207df3e53e
  stl/FIX-01E_sensor_carrier.stl                         182284  a955340bbfd16acd
  stl/FIX-02A_sealing_lip.stl                             75684  a8afa1986e89b4bb
  stl/FIX-02A_voice_coupler_body.stl                     250184  dc7c05b69250fb6a
  stl/FIX-02B_room_coupler_body.stl                      286884  95ed871cf574102a
  stl/FIX-02B_sealing_lip.stl                             75684  b19246add3a181da
  stl/FIX-03A_carrier_nest.stl                           279784  3fdc2578bc3c9af3
