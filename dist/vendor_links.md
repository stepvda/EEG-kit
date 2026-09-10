# Vendor links — commit-pinned

**Every link on this page is pinned to commit `342691454f5e`.**

Pinned, not `main`, so that a link quoted in an email cannot drift when the repository
moves. If you want the latest instead, replace the commit hash with `main` in any URL.

Each row gives the SHA-256 of the file **as it stands at that commit**. If what you
download does not match, tell us — do not work from it.

## Which set applies to you

The contact register holds 45 manufacturers across fabrication, assembly, layout, fixtures
and electrodes, so this page is organised by **what you were asked to quote** rather than
by company. Read *Everyone* plus the set that matches your scope.

**PCBCart**, ticket **BSY-598327**, quotations **20260909185** and **20260909781**: read
*Everyone*, *Bare-board fabrication*, *Assembly* and **Connectors and electrodes**. The last
of those carries a correction to what you were sent on 9 September — see ECO-EEG-036.

**Wuhan Greentek**: *Everyone* and *Connectors and electrodes*. AVL-EEG-017 §1.4.1 names you
as a candidate for the DIN 42802 socket line, which has no qualified vendor.

## Everyone — read these first

| File | What it is | SHA-256 |
|---|---|---|
| [`README.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/README.md) | what the programme is, and the licence position including the third-party datasheet exclusion | `1a07b5d24c129064e82446e70981e847…` |
| [`README_package_index.txt`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/README_package_index.txt) | the package index | `a28283a6939942e3d212694467e4fb83…` |
| [`ECO-EEG-016_RevC_change_control_and_document_register.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/ECO-EEG-016_RevC_change_control_and_document_register.pdf) | the change register. ECO-EEG-035 and ECO-EEG-036 are the newest entries and ECO-EEG-036 records what was stated to manufacturers in error | `31e637f7e73b65d61183016693ba92f7…` |
| [`RFQ-EEG-001_RevE_EEG_kit_specification.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/RFQ-EEG-001_RevE_EEG_kit_specification.pdf) | the specification and the requirement register | `cb983e9d418b1b3871eb3388f2a46da4…` |
| [`KNOWN_ISSUES.txt`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/KNOWN_ISSUES.txt) | what is open, stated by the programme rather than found by you | `cf3911ba0f6813c50521c39df5773298…` |

## Bare-board fabrication

| File | What it is | SHA-256 |
|---|---|---|
| [`DSN-EEG-003_RevD_manufacturing_design_package.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/DSN-EEG-003_RevD_manufacturing_design_package.pdf) | the board specification. Section 3.2 is the single specification of the bare board and now states finished-versus-drilled hole sizes and the external-versus-internal annular ring | `a306917c9ee236086b9af49e89f97153…` |
| [`QP-EEG-010_RevB_quality_plan.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/QP-EEG-010_RevB_quality_plan.pdf) | incoming inspection and the lot documents. NOTE: IQC-B12's 0.125 mm misregistration budget is SUPERSEDED -- see the report below | `77415341a0aa7b94b7fb6893ebd96643…` |
| [`DECISION_internal_annular_ring.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/reports/DECISION_internal_annular_ring.md) | why 0.125 mm is superseded, and the options. No decision has been taken and your answer is wanted | `06ec895e1abc6410f2e74a32ed82396d…` |
| [`EEG-CAR-01_RevB_gerber_X2.zip`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/kicad/gerber/EEG-CAR-01_RevB_gerber_X2.zip) | Rev B fabrication data. BUDGETARY ONLY -- this geometry is WITHDRAWN and Rev C is being laid out | `756f8b0da9bbfbb97711abca7c6c36f8…` |
| [`README_layer_map_and_checksums.txt`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/kicad/gerber/README_layer_map_and_checksums.txt) | layer map and checksums for the above | `fed7020fabbfa478b5bff70c4a965439…` |
| [`WH-BUS-01_RevA_gerber_X2.zip`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/kicad/wh-bus-01/WH-BUS-01_RevA_gerber_X2.zip) | the bus board, Rev A | `21404a2462192d34f4ba35cba30a030f…` |

## Assembly

| File | What it is | SHA-256 |
|---|---|---|
| [`ASM-EEG-007_RevB_assembly_work_instructions.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/ASM-EEG-007_RevB_assembly_work_instructions.pdf) | assembly instructions | `9cb85ad2520e21bfc9e7b22535355861…` |
| [`ICD-EEG-006_RevC_interface_control_document.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/ICD-EEG-006_RevC_interface_control_document.pdf) | the twelve module types are specified BY INTERFACE here, not by part | `3caef753d038f2848e0af7e078ce71ed…` |
| [`AVL-EEG-017_RevC_approved_vendor_list.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/AVL-EEG-017_RevC_approved_vendor_list.pdf) | approved vendors. Section 1.4.1 is the J15-J17 line and it has NO QUALIFIED VENDOR | `8059bc48b8848dbacec0d032f761953d…` |
| [`EEG_kit_BOM_for_bidders_RevC.xlsx`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/EEG_kit_BOM_for_bidders_RevC.xlsx) | the kit BOM. Rows 4, 10 and 11 are open and say what is open about them | `c319cd0d4a1cdc91d5a77783508aee6c…` |
| [`EEG-CAR-01_RevC_BOM.csv`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/kicad/RevC_layout_inputs/EEG-CAR-01_RevC_BOM.csv) | the corrected Rev C carrier BOM | `d48616df092ee46231ee21debf7855f3…` |
| [`EEG-CAR-01_RevC_CPL_SMT_top.csv`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/kicad/RevC_layout_inputs/EEG-CAR-01_RevC_CPL_SMT_top.csv) | surface-mount placement, PROVISIONAL | `e7cdababa85d0fea5a51ef44573561c9…` |
| [`EEG-CAR-01_RevC_CPL_THT_top.csv`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/kicad/RevC_layout_inputs/EEG-CAR-01_RevC_CPL_THT_top.csv) | through-hole placement, PROVISIONAL | `2dd0fdecaad729697d5de573c76a4967…` |

## Connectors and electrodes

| File | What it is | SHA-256 |
|---|---|---|
| [`INVESTIGATION_din42802_sockets_J15_J17.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/reports/INVESTIGATION_din42802_sockets_J15_J17.md) | READ THIS BEFORE QUOTING J15-J17. The named part cannot be found in any catalogue and no verified candidate meets the requirement | `fc2ffaea4598911e01da2a6b8f9cb2ca…` |
| [`README_datasheets.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/datasheets/README_datasheets.md) | the datasheet index | `6b68fe7790d4877bd8ef090432ff87cd…` |
| [`OPEN_LOOKUPS.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/datasheets/OPEN_LOOKUPS.md) | three figures still needed | `cd347930918491cc2dadae8dfdde4016…` |
| [`WH-EEG-008_RevB_harness_and_cable_assembly.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/WH-EEG-008_RevB_harness_and_cable_assembly.pdf) | the harness | `463e091fd96eb2808741ee3ee0765492…` |

## Layout desk (Rev C)

| File | What it is | SHA-256 |
|---|---|---|
| [`LAY-EEG-034_RevA_carrier_layout_rule_sheet.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/LAY-EEG-034_RevA_carrier_layout_rule_sheet.pdf) | the rule sheet. The two ELECTRODE and ANALOGUE_REF width rows are marked confirm and are PROPOSALS, not requirements | `e664cda66681e6115a85c129f047c9c5…` |
| [`DECISION_electrode_analogue_ref_widths.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/reports/DECISION_electrode_analogue_ref_widths.md) | the evidence behind those two rows; no value has been chosen | `49abbedbc3cd9dfca2062fb566b515a1…` |
| [`README_layout_inputs.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/kicad/RevC_layout_inputs/README_layout_inputs.md) | the handover set | `9776fdd378efaab08de33a244c5db6b6…` |
| [`SHA256SUMS.txt`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/kicad/RevC_layout_inputs/SHA256SUMS.txt) | checksums for the handover set | `de3cd21ede5e3b5b99739b07ef260c80…` |

## Fixtures

| File | What it is | SHA-256 |
|---|---|---|
| [`JIG-EEG-009_RevC_test_fixture_design.pdf`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/JIG-EEG-009_RevC_test_fixture_design.pdf) | the fixture set | `25cd9e648796b38ea92a5944926c4fdf…` |
| [`INVESTIGATION_fixture_pcb_copper.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/reports/INVESTIGATION_fixture_pcb_copper.md) | FIX-01 and FIX-04 have NO COPPER and cannot be built by anyone yet; FIX-02 and FIX-03 are not boards | `4e3463fcb5e6f1e47bd0a12321409b2b…` |

## Downloading

The links above open the file on GitHub. For a direct download, or for `curl`, use the raw
host with the same commit:

```
https://raw.githubusercontent.com/stepvda/EEG-kit/342691454f5eecfac57b6c5f365ee220c9b2e8cc/<path>
```

To check a file after downloading:

```
shasum -a 256 <file>
```

## Two things to read before you price anything

1. **EEG-CAR-01 Rev B geometry is WITHDRAWN from fabrication.** An independent layout
   engineer found vias in pads, stubs, off-centre pad entry and conductors under width. The
   circuit is unchanged. Any quotation against Rev B data is **budgetary**; the firm
   quotation will be against Rev C, which a layout desk is producing. Nothing is ordered
   before then, and no fabrication date is stated or implied anywhere in this package.
2. **Nothing in this package has been manufactured or measured.** Where a figure is
   calculated rather than measured, the documents say so. Where a reading is asserted
   rather than read out of a primary document, they say that too.

Licence: CC BY-SA 4.0 for this package. **Third-party datasheets are excluded** — see
[`LICENCE_NOTE.md`](https://github.com/stepvda/EEG-kit/blob/342691454f5eecfac57b6c5f365ee220c9b2e8cc/docs/datasheets/third_party/LICENCE_NOTE.md).
