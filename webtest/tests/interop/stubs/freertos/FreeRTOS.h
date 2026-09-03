#pragma once
#include "esp_err.h"
#include "esp_attr.h"
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
typedef int BaseType_t; typedef unsigned UBaseType_t; typedef void* TaskHandle_t;
typedef uint32_t TickType_t; typedef void* QueueHandle_t; typedef void* SemaphoreHandle_t;
#define pdMS_TO_TICKS(x) (x)
#define portMAX_DELAY 0xFFFFFFFF
#define pdTRUE 1
#define pdFALSE 0
#define portTICK_PERIOD_MS 1
