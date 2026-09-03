#pragma once
#include "tusb.h"
typedef struct { const void* device_descriptor; const char** string_descriptor; int string_descriptor_count; const void* configuration_descriptor; bool external_phy; } tinyusb_config_t;
typedef int esp_err_t;
static inline esp_err_t tinyusb_driver_install(const tinyusb_config_t* c){(void)c;return 0;}
