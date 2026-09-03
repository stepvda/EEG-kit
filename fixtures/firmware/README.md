# Fixture controller firmware -- M1, M2 and M3

**Document:** part of JIG-EEG-009 Rev B, section 8
**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium
**Licence:** CC BY-SA 4.0
**Written by hand.** This directory is source, not generated output. The only generated
thing near it is `fixtures/MANIFEST.json`, which records the SHA-256 of every file here so
that a fixture's firmware can be tied to a build.

## What this is

Three fixture controllers are named in JIG-EEG-009 and none of them had any source, any
command set or any host contract: M1 in section 1.8 ("Fixture controller, USB CDC, no
radio, Raspberry Pi Pico"), M2 in section 2.4 and M3 in section 4.1 ("a 24-channel relay
scanner card, controller M3"). This is that firmware, and section 8 of the document is the
protocol it speaks.

One source tree, three images, selected at build time:

| Image | Role | Fixture | Drives |
|---|---|---|---|
| `fix_m1.uf2` | M1 | FIX-01 | 83 relays through eleven TPIC6B595, the CD74HC4067 readback, the TCS34725 of FIX-01/E |
| `fix_m2.uf2` | M2 | FIX-02 | the PCM5102A/TPA6132 chain, the two coupler drivers, the two reference electrets, the FIX-02/D marker comparator |
| `fix_m3.uf2` | M3 | FIX-04 | 24 scanner relays through three TPIC6B595, the lid interlock, the 500 V DC gate |

The role is a compile-time choice and not a strap or a stored setting. A fixture that can
be talked into being another fixture is a fixture that will one day drive FIX-04's 500 V
relay map with FIX-01's channel numbers.

## Layout

```
include/fixhal.h     the whole hardware surface -- 17 functions, nothing else
include/fixproto.h   FIXPROTO v1: status codes, the command-table type, the engine
src/fixproto.c       line assembly, tokenising, dispatch, the shared verbs, the watchdog
src/fix_m1.c         M1: relay map, break-before-make, the readback sweep, FIX-01/E
src/fix_m2.c         M2: coupler select, tone, BURST and the marker timestamp
src/fix_m3.c         M3: scanner, the HV gate and the lid interlock
src/hal_rp2040.c     fixhal.h on a Pico.  Compiles.  Has never run.
src/main.c           the loop, and nothing else
test/hal_sim.c       a MODEL OF THE FIXTURE -- relays, readback divider, sensor, marker
test/host_test.c     drives the real firmware against that model
test/stubs/          five stub Pico SDK headers, declarations only
test/run.sh          builds and runs everything below
CMakeLists.txt       the Pico SDK build, for a machine that has the SDK
```

## Build and test

```
sh test/run.sh                     # 154 checks across the three roles, then a HAL compile
cmake -B build -DPICO_SDK_PATH=... # the real images, on a machine with the SDK
cmake --build build
```

`test/run.sh` does two different things and it is worth knowing which is which.

1. It compiles each role against `test/hal_sim.c` and drives it with `test/host_test.c`.
   That is **the real firmware answering real command lines**, and it is what proves the
   two behaviours a reviewer cannot see by reading: that a channel mode change breaks
   before it makes (counted in latch events, not asserted in a comment), and that a
   switching command is refused while HV is armed.
2. It compiles `src/hal_rp2040.c` against the stub headers and checks that all seventeen
   `fixhal.h` functions are defined in the object. That proves the C is valid and the
   contract is met. It proves nothing at all about the peripherals.

## What has not been done

* **No board exists.** JIG-EEG-009 section 7 says no fixture has been built or measured,
  and that includes these. Every pin number in `hal_rp2040.c` is this file's own choice
  against a fixture PCB that has not been laid out.
* **The I2S block is not written.** `hal_tone_start()` on the RP2040 returns 0, `fix_m2.c`
  turns that into `ERR ... 11 UNSUPPORTED`, and the specification the block has to meet is
  in the comment where the code will go. A PIO program written against no hardware and
  never run is a guess with a comment on it, and TST-EEG-004 T12a, T12b and T13 are blocked
  on the host test tool as well (JIG-EEG-009 section 7), so writing one now would buy
  nothing and would look like progress.
* **`RELAY_SETTLE_MS` and `HV_DISCHARGE_MS` are stated constants, not measurements.** Each
  is 10 ms and 5000 ms in the source, each has a comment saying what has to be checked
  against which datasheet, and neither datasheet is in this package.
* **The TCS34725 register numbers are from its datasheet and are checked at run time.**
  `COL INIT` reads the ID register and refuses to go on unless it reads 0x44, so a wrong
  address or a different sensor is a clean error rather than a column of plausible numbers.

## The one thing to read before changing anything

Every response is one line, and every request gets exactly one. Lines beginning `#` are
informational and are never a response. That rule is what lets a host match replies by
arrival order without a sequence number, and the watchdog notice -- the only unsolicited
line the firmware ever emits -- obeys it too.
