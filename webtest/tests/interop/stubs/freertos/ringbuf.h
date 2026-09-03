#pragma once
#include "freertos/FreeRTOS.h"
typedef void* RingbufHandle_t;
typedef enum { RINGBUF_TYPE_NOSPLIT, RINGBUF_TYPE_BYTEBUF } ringbuf_type_t;
static inline RingbufHandle_t xRingbufferCreate(size_t s, ringbuf_type_t t){(void)s;(void)t;return (void*)1;}
static inline RingbufHandle_t xRingbufferCreateWithCaps(size_t s, ringbuf_type_t t, uint32_t c){(void)s;(void)t;(void)c;return (void*)1;}
static inline BaseType_t xRingbufferSend(RingbufHandle_t r,const void*d,size_t n,TickType_t w){(void)r;(void)d;(void)n;(void)w;return 1;}
static inline void* xRingbufferReceive(RingbufHandle_t r,size_t*n,TickType_t w){(void)r;(void)w;*n=0;return 0;}
static inline void* xRingbufferReceiveUpTo(RingbufHandle_t r,size_t*n,TickType_t w,size_t m){(void)r;(void)w;(void)m;*n=0;return 0;}
static inline void vRingbufferReturnItem(RingbufHandle_t r,void*i){(void)r;(void)i;}
