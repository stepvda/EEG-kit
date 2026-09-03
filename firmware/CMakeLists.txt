# FW-EEG-001 -- TI One Voice EEG field kit firmware
# ESP-IDF 5.2.x.  Target: esp32s3 on an ESP32-S3-DevKitC-1-N16R8.
# Licence: MIT.
cmake_minimum_required(VERSION 3.16)
set(SUPPORTED_TARGETS esp32s3)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(eeg_field_kit VERSION 0.2.0)
