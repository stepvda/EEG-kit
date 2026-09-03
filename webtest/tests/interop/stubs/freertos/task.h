#pragma once
#include "freertos/FreeRTOS.h"
static inline void vTaskDelay(TickType_t t){(void)t;}
static inline BaseType_t xTaskCreate(void(*f)(void*),const char*n,uint32_t s,void*p,UBaseType_t pr,TaskHandle_t*h){(void)f;(void)n;(void)s;(void)p;(void)pr;(void)h;return 1;}
static inline void vTaskDelete(TaskHandle_t h){(void)h;}
static inline TickType_t xTaskGetTickCount(void){return 0;}
static inline uint32_t ulTaskNotifyTake(BaseType_t clr, TickType_t w){(void)clr;(void)w;return 1;}
static inline BaseType_t xTaskNotifyGive(TaskHandle_t t){(void)t;return 1;}
static inline void vTaskNotifyGiveFromISR(TaskHandle_t t, BaseType_t* w){(void)t;(void)w;}
static inline TaskHandle_t xTaskGetCurrentTaskHandle(void){return (void*)1;}

static inline BaseType_t xTaskCreatePinnedToCore(void(*f)(void*),const char*n,uint32_t s,void*p,UBaseType_t pr,TaskHandle_t*h,int c){(void)f;(void)n;(void)s;(void)p;(void)pr;(void)h;(void)c;return 1;}
