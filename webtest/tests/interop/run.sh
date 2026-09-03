#!/bin/sh
# run.sh -- prove the firmware and the browser test tool agree, without hardware.
#
# WHY THIS EXISTS
#
# webtest/tests/roundtrip.test.mjs drives the real host code against a SIMULATED device
# written in JavaScript.  That is useful, and it is not the same question.  The JS
# simulation was written by hand from the same specification as main.c, and both drifted
# from it independently and in DIFFERENT directions: main.c dispatched on the frame's
# first byte (the protocol version, so every command ran as START_SESSION), the JS
# simulation answered { opcode, 0xFF }, and FW-EEG-001 section 6.2 specified a third
# shape.  Every JS test passed throughout, because the JS host and the JS device shared
# the same misunderstanding.
#
# This harness removes the shared misunderstanding: it compiles the ACTUAL firmware
# translation unit against small ESP-IDF stubs, wires stdin/stdout to the simulated USB
# endpoints, and drives it with the ACTUAL webtest protocol module under Node.  If the two
# ever disagree again about framing, CRC, the header, an opcode or the acknowledgement
# layout, this fails and the JS-only tests will not.
#
# It does NOT test the analogue front end, the converters, timing, or anything that needs
# a board.  Peripherals are simulated in drivers_sim.c.  It answers exactly one question:
# do the firmware and the test program speak the same protocol.
#
# Usage:  sh webtest/tests/interop/run.sh
# Needs:  a C compiler and Node 18+.  No ESP-IDF, no hardware.
# Licence: CC BY-SA 4.0.
set -e

HERE=$(cd "$(dirname "$0")" && pwd)
PKG=$(cd "$HERE/../../.." && pwd)
FW="$PKG/firmware/main"
WT="$PKG/webtest"
BUILD="$HERE/build"

command -v cc   >/dev/null 2>&1 || { echo "no C compiler on PATH"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "no node on PATH";       exit 1; }

mkdir -p "$BUILD"

# main.c carries a _Static_assert on the length of the MS OS 2.0 descriptor.  The assert is
# correct and worth keeping; it cannot hold here because the stubs expand TinyUSB's
# descriptor macros to a placeholder byte.  Neutralise it in the COPY only -- the shipped
# source is never modified.
sed 's/_Static_assert(sizeof(ms_os_20_desc)/_Static_assert(1 || sizeof(ms_os_20_desc)/' \
    "$FW/main.c" > "$BUILD/main_under_test.c"
cp "$FW/board_pins.h" "$FW/drivers.h" "$BUILD/"

cc -std=c11 -w -ferror-limit=200 \
   -I "$HERE/stubs" -I "$BUILD" -I "$FW" \
   -o "$BUILD/device" "$HERE/harness.c" "$HERE/drivers_sim.c"

SC="$BUILD" WT="$WT" node "$HERE/host.mjs"
