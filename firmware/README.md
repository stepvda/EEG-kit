# FW-EEG-001 — EEG field kit firmware

**Revision:** B **Date:** 1 September 2026, corrected 2 September 2026
**Licence:** MIT (the hardware is CC BY-SA 4.0)
**Specification:** `docs/FW-EEG-001_RevC_firmware_build_and_provisioning.md`
**Target:** ESP32-S3-DevKitC-1-N16R8 on EEG-CAR-01 Rev B

## Status, stated plainly

**Corrected 2 September 2026.** This section used to read: "This firmware **has never been
compiled against a real ESP-IDF installation and has never run on hardware.** It is the
specification in executable form. Five drivers are stubs: the ES8388 codec, the SDMMC
layer, the ATECC608B, the MAX17048 gauge and the envelope onset detector."

Both halves of that are now out of date, and the replacement is deliberately narrow,
because three different things have happened to this source and they prove three different
amounts.

| What has happened | Date | What it proves | What it does not |
|---|---|---|---|
| **It builds.** ESP-IDF **v5.2.5**, target `esp32s3`, `sdkconfig.defaults` + `sdkconfig.phase1`, clean at ESP-IDF's default `-Wall -Werror=all`. Images and a SHA-256 manifest in `release/` | 2 Sep 2026 | every ESP-IDF header, Kconfig option and TinyUSB macro this source names resolves; both `_Static_assert`s held; the image links and fits | that any of it is *right*. A register value that assembles is not one the ADS1299 accepts |
| **It runs under QEMU.** `qemu-system-xtensa -M esp32s3`, one full boot, captured in `release/qemu_boot.log` | 2 Sep 2026 | the image boots, the bootloader reads **this** partition table, the app loads from `factory` at `0x20000`, `app_main()` runs, and the microSD, codec and ring-buffer paths behave as written | every peripheral. QEMU's `esp32s3` has **no** octal PSRAM, **no** microSD, **no** ES8388 and **no** ADS1299 |
| **It agrees with the browser tool.** `sh webtest/tests/interop/run.sh` compiles this `main.c` on a development host against ESP-IDF stubs and drives it with the real protocol module: **57 checks, all passing** | 2 Sep 2026 | framing, CRC, header, opcodes, the acknowledgement layout, the S-01 interlock and the `0x4A`/`0x4B` split | nothing about ESP-IDF, the descriptors or any peripheral |

**It has never run on hardware, and no hardware exists.** No board has been fabricated and
no unit has been assembled. The daisy-chain order, the SPI timing, every ADS1299 register
value, the USB enumeration and the whole analogue front end are still assumptions that no
silicon has answered. No safety engineer has reviewed this design.

**The drivers are written and none of them has run.** `drivers.c` implements the ES8388
codec, the one-bit SDMMC layer, the ATECC608B, the MAX17048 gauge and the envelope onset
detector — they are not stubs any more — but writing a driver and proving one are different
claims and only the first has happened. Not one I2C address, register write or timeout in
that file has been answered by a part. Under QEMU the microSD and codec bring-up both timed
out and both degraded gracefully, which is a bring-up *behaviour* test and nothing more:
QEMU emulates neither part, so a timeout is the only answer it could have given.

**One thing genuinely is not written.** The block-signing task does not exist — no SHA-256,
no chained digest, no signing call, nothing declares it — so `FT_SIGNATURE` frames are never
emitted and TST-EEG-004 T16 has no input at all. F-08 is unimplemented, not merely untested.

Completing bring-up and getting a clean enumeration on Windows, macOS and Linux is the
first task of the firmware volunteer, and TST-EEG-004 step T5 is its acceptance test. The
open defects are FW-D04, FW-D05, FW-D06, FW-D07, FW-D09 and FW-D10; the specification
carries them with an acceptance test each.

What package v2 adds over v1, which shipped `main.c` alone:

| File | What it is |
|---|---|
| `CMakeLists.txt`, `main/CMakeLists.txt` | the ESP-IDF project |
| `main/idf_component.yml` | pinned dependency versions — the TinyUSB descriptor macros moved between releases, and an unpinned build is a silent difference between units |
| `dependencies.lock` | what the component manager actually resolved: IDF 5.2.5, `esp_tinyusb` 1.4.5 |
| `sdkconfig.defaults` | PSRAM in octal mode, USB device, partitions, secure boot, flash encryption, IRAM placement for the DRDY path. Every line is a requirement |
| `sdkconfig.phase1` | the Phase 1 overlay — turns secure boot, flash encryption and anti-rollback off so the two prototypes burn no eFuses and stay re-flashable |
| `sdkconfig.qemu` | the emulator overlay. **Not a configuration for any unit** — see below |
| `partitions.csv` | A/B OTA with rollback, a calibration NVS partition and a provisioning NVS partition |
| `main/board_pins.h` | **generated from `tools/design.py`** so the firmware and the board cannot disagree |
| `main/drivers.h`, `main/drivers.c` | the peripheral API `main.c` calls, and its implementations |
| `tools/provision.py` | the end-of-line provisioning script of RFQ F-18 |
| `tools/verify_stream.py` | the host verifier used at T5, T13, T14 and T16 |
| `release/` | **added 2 September 2026**: the built images, `manifest.json`, `size.json` and `qemu_boot.log` |

## Build

There are two builds, and which one you run decides whether the unit can ever be
re-flashed. **Phase 1**, the two prototypes, and the build that produced `release/`:

```sh
. $IDF_PATH/export.sh          # ESP-IDF v5.2.5
idf.py set-target esp32s3
idf.py -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.phase1" build
```

**Phase 2 onward**, production, from `sdkconfig.defaults` alone:

```sh
idf.py build
```

`sdkconfig.defaults` enables secure boot v2 and flash encryption in release mode. Build a
prototype that way by mistake and its bootloader burns the eFuses on first boot, after
which UART re-flashing is refused for the life of the board — so the Phase 1 rule is that
prototypes **burn no eFuses at all** (RUL-EEG-021 section B), and `sdkconfig.phase1` is how
that rule is kept. Never move between phases by editing `sdkconfig.defaults`; the overlay
is the only switch. FW-EEG-001 section 2.4 lists all three files in full and section 7.5
states the eFuse phasing.

The release image is signed by the programme before it reaches the manufacturer. The
manufacturer flashes a pre-signed binary and never holds the signing key (RFQ F-19).
`CONFIG_SECURE_BOOT_BUILD_SIGNED_BINARIES=n` is deliberate: the build container never holds
the key, and signing is a separate offline step.

### What the first real build cost, and why it is written down

Five things had to be corrected before `idf.py build` completed, and none of them was a
protocol defect — every one was a project or configuration defect that reading the source
could not have found. They are recorded here because the same five will bite anyone
building this from a clean checkout of an older revision.

* `esp_driver_i2c` **does not exist at ESP-IDF 5.2** — the I2C driver was split out at 5.3 —
  and `idf_component.yml` permits `>=5.2,<5.4`, so the configure step stopped with
  "component could not be found". `main/CMakeLists.txt` requires `driver`, which provides
  I2C across the whole pinned range.
* `CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK=y` had been appended to `sdkconfig.phase1` **below**
  the deliberate `=n`. A later duplicate of the same key silently wins, so the Phase 1
  intent was being undone by a line that read as an addition. ESP-IDF also refuses
  anti-rollback on a table carrying a `factory` partition, and `partitions.csv` has one, so
  the build stopped there — which is how it was found.
* **`CONFIG_TINYUSB_VENDOR_ENABLED` is not an option that exists** in `esp_tinyusb` 1.4.x,
  and ESP-IDF warns rather than fails on an unrecognised key. So the setting looked present,
  `CFG_TUD_VENDOR` stayed 0, `tusb.h` declared none of the `tud_vendor_*` functions, and the
  WebUSB interface this device is built around would simply not have existed. The real key
  is `CONFIG_TINYUSB_VENDOR_COUNT=1`.
* Three descriptor callbacks — `tud_descriptor_device_cb()`, `tud_descriptor_configuration_cb()`
  and `tud_descriptor_string_cb()` — were defined here **and** in `esp_tinyusb`, and the link
  failed with three "multiple definition" errors. With `CONFIG_TINYUSB_DESC_CUSTOM=y` you
  supply the descriptors as *data* through `tinyusb_config_t` and the component owns the
  callbacks. `tud_descriptor_bos_cb()` stays in `main.c`, because the component defines none
  and without a BOS descriptor there is no WebUSB and no MS OS 2.0 capability.
* The five `sdkconfig` lines the specification had listed as "must be added before the first
  build" were still absent. They are in both configuration files now.

### What it measures

| Figure | Value | Reading |
|---|---|---|
| Image, as `idf.py size` reports it | **405,245 bytes** | 13 % of the 3 MB `factory` slot. Ample |
| `release/eeg_field_kit.bin` on disk | 405,360 bytes | the same image plus padding and the appended SHA-256 |
| DIRAM used | 88,799 of 345,856 (25.7 %) | ample |
| **Static IRAM used** | **16,383 of 16,384 — one byte free** | **not a pass.** See below |

The IRAM figure is a cliff, not a margin: the next function anyone marks `IRAM_ATTR` fails
the link with an error naming a section rather than a cause, and this design has more
interrupt work coming. Turning off the SPI-slave and gptimer ISRs — neither of which this
firmware uses, and both removed in `sdkconfig.phase1` — **did not move the figure by a
single byte**, so it is not those. The change is kept because carrying handlers for a bus
and a timer this firmware does not use is wrong either way, but it is **not** the fix.
Either the pool is genuinely full and a bring-up engineer must choose what leaves IRAM, or
`esp_idf_size` is reporting against a fixed 16 kB window that is not the real limit on an
ESP32-S3 with octal SPIRAM and XIP. Reading the linker map against hardware settles it;
guessing at `sdkconfig` from here does not. Carried as FW-EEG-001 section 10 item 17 and
SIM-EEG-018 open item 1.

The build was made on a developer machine from a working tree with uncommitted changes —
the boot log records the app version as `e91f9d58-dirty` — so the SHA-256 list in
`release/manifest.json` is **not yet reproducible**. Rebuilding from a clean tree in the
pinned `espressif/idf:v5.2.5` container is open.

## Running it without hardware

```sh
idf.py -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.phase1;sdkconfig.qemu" build
```

then a merged flash image under `qemu-system-xtensa 9.0.0 (esp-develop)` with
`-M esp32s3 -m 4M`, which is what the capture records.
`release/qemu_boot.log` is that capture. **It is an emulator, not a unit.** What the boot
settles is the part that needs no peripheral: the image boots, the bootloader reads this
partition table row for row, the app loads from `factory`, `app_main()` runs, the microSD
and ES8388 bring-up paths degrade gracefully instead of aborting, and the ring-buffer guard
fires with its named diagnostic. What it settles about register values, the daisy order, SPI
timing, USB enumeration or the contact lights is **nothing**, because none of those parts
exists in the machine.

`sdkconfig.qemu` differs from the shipped build in exactly one option,
`CONFIG_SPIRAM_IGNORE_NOTFOUND=y`, and **must never be used to build a unit**: it turns a
missing 6 MiB ring buffer — which is F-06 and the whole of the retransmit story — from a
refusal to boot into a silent degradation.

The boot ends in `abort()`, and that is correct here: QEMU has no PSRAM, so the ring cannot
be allocated and `app_main()` refuses to carry on without it. It is also the wrong failure
mode for a field device — a unit that aborts in a participant's home cannot be told apart
from a dead battery or a bad cable, because it never enumerates and the browser tool cannot
ask it what is wrong. That is an open item, not a fixed one.

## The pin map is generated, not written

`main/board_pins.h` is regenerated from `tools/design.py`. Do not edit it by hand.

**ECO-EEG-009.** The Rev A map used GPIO35, 36 and 37 for the contact-light shift register.
Those three pins carry the **octal PSRAM** on the -N16R8 variant and are not connected on
this carrier; GPIO45 is the VDD_SPI strapping pin and is also left open. The shift register
moved to GPIO41, 42 and 0, and the microSD interface dropped to one-bit SDMMC to free them.
70 kB/s is needed at 1000 Hz and about 2 MB/s is available, so the headroom is ample.

## Contact lights

**Written 2 September 2026.** This section used to describe the phase scheme as a
specification; it is now what the source does. `lights_phase()` and `lights_task()` in
`main.c` drive it, FW-D16 is closed, and **RFQ E-27 is met in the source**. It has never
been run: no unit exists, and QEMU has no shift register.

Eight two-lead bicolour LEDs, one per site, sit between their `LEDn` line and the `LED_V`
common. Phase A drives `LED_V` high and the wanted sites low, which shows green; phase B
drives `LED_V` low and the wanted sites high, which shows red; a site lit in both phases
shows amber.

The colour comes from the converter's own lead-off measurement, which is what E-27 asks for,
read at **two comparator thresholds**: a site that trips neither is **green**, one that trips
only the sensitive threshold is **amber** — marginal, re-gel it — and one that trips both is
**red**. The insensitive set is a subset of the sensitive one, so the three states are
exhaustive and cannot overlap.

*Corrected 2026-09-02 (FW-D17).* This read that the colour came from **both** halves of the
lead-off word, `LOFF_STATP` and `LOFF_STATN`. It could not: **the montage is single-ended**,
J2 carries IN1 to IN8 with one shared `SRB1` reference, and `ads_init()` enabled
`LOFF_SENSP` only — so `LOFF_STATN` read zero for every channel for ever, `bad = p & n` was
always zero and **red was unreachable**. Enabling `LOFF_SENSN` would not have fixed it
either: with `SRB1` closed, all eight N bits report the one shared reference and carry no
per-site information at all. Sweeping `COMP_TH` is what this hardware supports.

The alternation is **about 250 Hz, not the nominal 240**. `LIGHT_PHASE_HZ` is 240, so a
half-phase is 2.083 ms; the task delays in FreeRTOS ticks at `CONFIG_FREERTOS_HZ` 1000, so
it quantises to 2 ms. The requirement is "above 100 Hz" and 250 Hz meets it with room; both
half-phases quantise identically, so the duty stays 50/50 and the colour does not shift.
Exactly 240 Hz would need a hardware timer rather than a task delay.

`LED_V` is GPIO48, which is an **input at reset**, so no current can flow through any light
whatever the shift register contains. That is the dark-at-boot guarantee, and it is why
E-27 can be met without a hardware output-enable line. While a block is recording, or when
the host switches the lights off, the task clears the register and returns `LED_V` to an
input — dark by construction, rather than dark for as long as a level stays right.

Forcing a colour is **not** implemented: `CMD_LIGHTS` modes 2, 3 and 4 are accepted and
answered `0x00` OK while the automatic colour continues, where the honest reply would be
`0x0B` not-implemented. Open.

## Provisioning

```sh
python3 tools/provision.py --port /dev/ttyACM0 --serial TIOV-B-0007 \
        --calibration cal_TIOV-B-0007.json --out records/TIOV-B-0007.json \
        --write-config --lock
```

**Corrected 2 September 2026.** This block used to omit `--write-config` and `--lock` and
to describe the run as "ten steps". Neither irreversible action is implied any more: without
`--lock` nothing in a run is irreversible and the run cannot produce a finished unit, which
is what a training or station-validation run wants. `--serial` is checked against the
PKG-EEG-015 format before anything is sent, and the lock additionally needs the serial typed
back or passed with `--confirm-serial`.

The steps are 1, 2, 2b, 2c, 3, 4, 5, 6, 6b, 7, 7b, 8/9 and 10 — each one printed, each one
recorded. **The configuration-zone write and lock run at 2b and 2c, before GenKey**, and not
at step 8: a factory-fresh ATECC608B will not generate a key into a slot whose configuration
has not been written and locked, and locking Microchip's defaults instead is irreversible,
scraps the breakout and produces no device identity. If `--lock` was given and the template
did not reach the part, the run stops **before** the lock rather than continuing. Step 7b
reads the calibration constants back with opcode `0x4A` and compares them byte for byte,
which is TST-EEG-004 T6's acceptance limit and was not executable at all until that opcode
existed. FW-EEG-001 section 7.3 has the full table.

The private device key is generated inside the ATECC608B and cannot be read out by anyone,
including us. The public key fingerprint goes on the enclosure label (RFQ M-03) and the
record travels with the unit.

**None of it has ever been run against a real ATECC608B.** The interop harness drives the
provisioning opcodes and the mode gate against a simulated part, which proves the framing
and the refusals and nothing about the silicon.

Two comments inside `tools/provision.py` and `tools/README_provisioning.md` are known to be
out of date and are not this file's to fix: they describe the old NVS layout — namespace
`"tiov"` in the default partition — which `drivers.c` no longer uses, and their two
skipped-step hints name each other's opcode (`0x4A` and `0x4B` are transposed).

## Verification

```sh
python3 tools/verify_stream.py --file session.bin --pubkey records/TIOV-B-0007.json
```

Decodes the COBS frame stream, checks every CRC-32, checks sequence and sample-index
continuity, counts GAP frames and verifies the ECDSA P-256 block-signature chain against
the exported public key. Exit status 0 only if everything passes, so it can be used as a
test step directly.

Two limits to know before relying on it: it reports `pass` when there are **no** SIGNATURE
frames at all, so T16's operator must assert `signature_blocks > 0` separately; and it has
no `--session-id`, so it roots the chain at 32 zero bytes where TST-EEG-004 T16 roots it at
the session identifier. Both are open items in FW-EEG-001 section 10.
