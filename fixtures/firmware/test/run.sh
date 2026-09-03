#!/bin/sh
# run.sh -- compile and run the fixture-firmware host tests, then compile the RP2040 HAL
# against stub headers so that a change to it cannot go unparsed on a machine with no
# Raspberry Pi Pico SDK installed.
#
# Two passes, and they prove different things:
#   1. the three role builds, linked against test/hal_sim.c and driven by host_test.c --
#      this is the real firmware answering real command lines;
#   2. a compile-only pass over src/hal_rp2040.c against test/stubs/ -- this proves the C
#      is valid and that it implements every function fixhal.h declares, and nothing more.
#
# Part of package_v2.3, TI One Voice research programme.  Licence: CC BY-SA 4.0.
set -e
cd "$(dirname "$0")/.."
BUILD=${BUILD:-test/build}
CC=${CC:-cc}
CFLAGS="-std=c99 -Wall -Wextra -Werror -O1 -Iinclude"
TESTFLAGS="-DFIX_MAIN_IS_TEST=1"
mkdir -p "$BUILD"

BUILD_ID=$(git -C . rev-parse --short=8 HEAD 2>/dev/null || echo unset)

fail=0
for role in m1 m2 m3; do
    up=$(echo "$role" | tr 'a-z' 'A-Z')
    $CC $CFLAGS $TESTFLAGS -DFX_BUILD_ID="\"$BUILD_ID\"" -DFIX_ROLE_$up \
        -o "$BUILD/test_$role" \
        src/fixproto.c "src/fix_$role.c" src/main.c test/hal_sim.c test/host_test.c
    "$BUILD/test_$role" || fail=1
done

echo "RP2040 HAL, compile-only against test/stubs/"
$CC $CFLAGS -Itest/stubs -c src/hal_rp2040.c -o "$BUILD/hal_rp2040.o"
echo "  hal_rp2040.c compiles and defines:"
if command -v nm >/dev/null 2>&1; then
    nm -g "$BUILD/hal_rp2040.o" | sed -n 's/.* T _\{0,1\}\(hal_[a-z_0-9]*\)$/    \1/p' | sort
fi

# Every function fixhal.h declares must exist in the RP2040 object, or a Pico build fails
# at link time on a machine that has the SDK and passes here on a machine that does not.
missing=0
for sym in hal_init hal_now_us hal_sleep_ms hal_getchar hal_putline hal_sr_write \
           hal_sr_clear hal_mux_select hal_adc_mv hal_adc_mv_aux hal_i2c_write \
           hal_i2c_read hal_gpio_get hal_gpio_set hal_tone_start hal_tone_stop \
           hal_tone_busy; do
    if ! nm -g "$BUILD/hal_rp2040.o" | grep -q "[Tt] _\{0,1\}$sym$"; then
        echo "    MISSING $sym"
        missing=1
    fi
done
[ "$missing" = 0 ] && echo "    all 17 fixhal.h functions are defined"
[ "$missing" = 0 ] || fail=1

if [ "$fail" = 0 ]; then
    echo "PASS"
else
    echo "FAIL"
fi
exit $fail
