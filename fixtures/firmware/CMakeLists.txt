# CMakeLists.txt -- the three EEG-kit fixture controller images.
#
# Raspberry Pi Pico SDK build.  It is not vendored in this package: set PICO_SDK_PATH to a
# checkout of https://github.com/raspberrypi/pico-sdk (the SDK's own pico_sdk_import.cmake
# is copied beside this file by `cmake -DPICO_SDK_FETCH_FROM_GIT=ON` or by hand).
#
#   cmake -B build -DPICO_SDK_PATH=/path/to/pico-sdk
#   cmake --build build
#
# produces build/fix_m1.uf2, build/fix_m2.uf2 and build/fix_m3.uf2.  Flashing is drag and
# drop: hold BOOTSEL, plug the Pico in, copy the .uf2 onto the mass-storage device it
# presents.  There is no bootloader to write and no fuse to burn -- deliberately, because
# a fixture controller is a piece of test equipment and a technician has to be able to
# reflash one on a Friday afternoon without a programmer.
#
# NONE OF THIS HAS BEEN BUILT.  The package has no Pico SDK checkout and no board to run
# it on; test/run.sh compiles the same sources natively and is what has actually been run.
#
# Part of package_v2.3, TI One Voice research programme.  Licence: CC BY-SA 4.0.
cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
project(eeg_fixture_controllers C CXX ASM)
set(CMAKE_C_STANDARD 99)
pico_sdk_init()

execute_process(COMMAND git rev-parse --short=8 HEAD
                OUTPUT_VARIABLE FX_BUILD_ID OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET RESULT_VARIABLE _git_rc)
if(NOT _git_rc EQUAL 0)
  set(FX_BUILD_ID "unset")
endif()

function(fixture_target name role)
  add_executable(${name}
    src/main.c
    src/fixproto.c
    src/${role}
    src/hal_rp2040.c)
  target_include_directories(${name} PRIVATE include)
  target_compile_definitions(${name} PRIVATE FX_BUILD_ID="${FX_BUILD_ID}")
  target_compile_options(${name} PRIVATE -Wall -Wextra)
  target_link_libraries(${name} pico_stdlib hardware_adc hardware_i2c hardware_spi)
  # The host link is USB CDC and only USB CDC.  The UART is left off so that a stray
  # printf cannot appear on the debug header of a fixture sitting inside a metal box.
  pico_enable_stdio_usb(${name} 1)
  pico_enable_stdio_uart(${name} 0)
  pico_add_extra_outputs(${name})
endfunction()

fixture_target(fix_m1 fix_m1.c)   # FIX-01, front-end injection and lead-off
fixture_target(fix_m2 fix_m2.c)   # FIX-02, audio loopback and onset
fixture_target(fix_m3 fix_m3.c)   # FIX-04, harness scanner
