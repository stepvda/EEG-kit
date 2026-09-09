# Vendor submission record -- PCBCart, ticket BSY-598327

| | |
|---|---|
| Vendor | PCBCart (Sota Electronics / General Circuits), assembly quote desk |
| Contact | Genny (Huang Jing Yi), usa.office@pcbcart.com |
| Vendor ticket | **BSY-598327** |
| Route | web form, <https://www.pcbcart.com/assembly>, at the vendor's written request |
| Boards | EEG-CAR-01 (assembled carrier), WH-BUS-01 (bare bus board) |
| Pack built | 2026-09-09 |
| Pack | `dist/rfq/pcbcart/`, from `tools/emit_rfq_pack.py` |
| Filled by | `tools/rfq_pcbcart.py`, Playwright 1.58.0 / Chromium 145.0.7632.6 |
| Submitted | 2026-09-09, signed in as `stephane@stepvda.com` |
| EEG-CAR-01 | **Quote# 20260909185** (`quote_id=53125`) |
| WH-BUS-01 | **Quote# 20260909781** (`quote_id=53126`) |
| Status | **SUBMITTED.** Two quotations raised, one per board |

## What this quotation is, and is not

**It is budgetary.** EEG-CAR-01 **Rev B geometry is WITHDRAWN from fabrication**: an
independent layout engineer found vias in pads, via stubs, off-centre pad entry and
conductors below the stated minimum width. The circuit is unchanged. The geometry is
being redone as Rev C by a layout desk in KiCad against LAY-EEG-034.

So any figure obtained against this submission is priced on **withdrawn geometry**
carrying the **corrected Rev C BOM**, and is for budget only. The firm quotation will
be raised against Rev C data, and **nothing is ordered before then**. No fabrication
date is stated or implied anywhere in the submission.

## Status: submitted

The pack was built, both boards were filled on the live form, every field was verified
against `fields.json`, every section was screenshotted, and **both were then submitted**
on Stephane van der Aa's written instruction in the working session, given after he had
reviewed the filled-form screenshots for both boards.

**Two quotations, one per board, and no submission was made twice.** PCBCart returns two
identifiers per quotation and they are different numbers -- a `Quote#` in the page and a
`quote_id` in the success URL -- and both are recorded above and in
`dist/rfq/pcbcart/submission_record.json`, together with the authority the submission was
made on.

`tools/rfq_pcbcart.py` still refuses to submit a page that does not match `fields.json`,
or one with a required field unfilled, whoever authorises it. The `--authorised-by` text
stands in for the typed confirmation where there is no interactive terminal; it is
recorded verbatim and relaxes nothing else.

Two things settled before submitting, both of which had been open:

1. **State/province.** Set to **Brussels**, and NOT guessed: every controlled document in
   `docs/` carries the header "Issued by: TI One Voice research programme
   (one.witysk.org), Brussels, Belgium". `emit_rfq_pack.py` reads that header back and
   fails the build if the constant and the documents ever disagree.
2. **The account.** `stephane@stepvda.com` was **not** previously registered -- so the
   anonymous route would have worked -- and an account was created on instruction. The
   risk that mattered did not materialise: the new account's `pcb_dimension` profile
   setting defaults to **mm**, and `UserStatus.unit` read `mm` on both signed-in runs.
   The unit was asserted from two independent places on the page before any dimension was
   typed, on every run.

## Files in the submission

SHA-256 read from `dist/rfq/pcbcart/fields.json`, not transcribed. The form has exactly
two upload slots and neither accepts multiple files, so everything that is not the
fabrication ZIP travels in one bundle.

### EEG-CAR-01

| Slot | File | Bytes | SHA-256 |
|---|---|---:|---|
| PCB File | `EEG-CAR-01_RevB_gerber_X2.zip` | 626645 | `756f8b0da9bbfbb97711abca7c6c36f86ac36fde7958b002631508cf03780679` |
| BOM File | `EEG-CAR-01_RevC_BOM_CPL_and_notes.zip` | 13384 | `e36aadf3c37aad42baa6ef9175c6052cf14a40d2d5cee252eff03e87c0225136` |

`EEG-CAR-01_RevB_gerber_X2.zip` was **copied, not rebuilt**; checksum verified against
`kicad/gerber/README_layer_map_and_checksums.txt`.

`EEG-CAR-01_RevC_BOM_CPL_and_notes.zip` contains:

| File | SHA-256 |
|---|---|
| `EEG-CAR-01_RevC_BOM.csv` | `d48616df092ee46231ee21debf7855f34011968ad782e32d0533620421a8178c` |
| `EEG-CAR-01_RevC_CPL_SMT_top.csv` | `e7cdababa85d0fea5a51ef44573561c97da70d5573e9c55079a11e14f4e87fac` |
| `EEG-CAR-01_RevC_CPL_THT_top.csv` | `2dd0fdecaad729697d5de573c76a4967006df9e850c3c67d66ed57ff5707a3d8` |
| `README_for_bidder.txt` | `5b1763f28c06d4c373a5a9545ac1bc7528f0d24f3a9c6645202bba20da5098b7` |

### WH-BUS-01

| Slot | File | Bytes | SHA-256 |
|---|---|---:|---|
| PCB File | `WH-BUS-01_RevA_gerber_X2.zip` | 6701 | `21404a2462192d34f4ba35cba30a030f2b2adeb47930b09ba7aa61e9cb46173f` |
| BOM File | `WH-BUS-01_RevA_BOM_and_notes.zip` | 7285 | `0545e5497fb208080ac08be3e1229210d11ac29e8b26c6f945d655448b600ab6` |

`WH-BUS-01_RevA_gerber_X2.zip` was **copied, not rebuilt**; checksum verified against
`kicad/wh-bus-01/README_layer_map_and_checksums.txt`.

`WH-BUS-01_RevA_BOM_and_notes.zip` contains:

| File | SHA-256 |
|---|---|
| `WH-BUS-01_RevA_placement_and_BOM.txt` | `eca563999ade591725f1e12e660dfad31e43f9e57ffc642b19f21be18bf3c9cb` |
| `README_for_bidder.txt` | `d33bf2cae8f0383531f44040db9fbd8b03b992f3ceed965e1295f95a605079b1` |

## Deviations recorded at fill time

Where the portal's option list has no exact match for the specification, the nearest
option was selected and the difference stated in the Notes box and in
`README_for_bidder.txt`. Nothing was silently rounded.

| Board | Control | Selected | Specification |
|---|---|---|---|
| EEG-CAR-01 | `PCB_COPPER_WEIGHT_INNER` | 18 um | 17 um (0.5 oz) |
| WH-BUS-01 | `PCB_MIN_TRACING_SPACING` | 0.20 mm | 1.20 mm (the LED_V bar) |
| WH-BUS-01 | `PCB_SMALLEST_HOLES` | 0.40 mm | 10 per board, 0.80 mm finished, 1.60 mm pad, one tool |

## The form has no control for these

They reach the vendor through the Notes box and `README_for_bidder.txt` instead. The
most consequential is the stack-up: **no PCBCart form carries one**, on the assembly
route or the Standard PCB route, so DSN-EEG-003 section 3.2 is quoted in the notes with
written confirmation demanded rather than a default accepted silently.

- **Layer roles**
- **Stack-up (SPECIFIED, not default)**
- **Vias**
- **Largest plated hole**
- **Acceptance class**
- **Electrical test**
- **Components / pads / nets**
- **Lot coupon**
- **Lot documents**
- **Plated through holes**
- **Panel**

## Dates

Nothing generated for this submission carries a date; the generator fails the build if
it does. One copied file carries a document generation stamp and is sent UNALTERED so
that its released checksum still verifies:

- `WH-BUS-01_RevA_placement_and_BOM.txt` -- 2026-09-01 (generation stamp in `kicad/wh-bus-01/WH-BUS-01_RevA_placement_and_BOM.txt`)

## Provenance

Every figure in the submission is generated from `tools/design.py`, `tools/wh_bus.py`
or a controlled document, and `tools/emit_rfq_pack.py` **fails the build** if a figure
it restates no longer appears verbatim in its source. Nothing was typed by hand.

Licence: CC BY-SA 4.0.
