#pragma once
#include <stddef.h>
#include <stdlib.h>
#define MALLOC_CAP_SPIRAM 1
#define MALLOC_CAP_8BIT 2
#define MALLOC_CAP_INTERNAL 4
static inline void* heap_caps_malloc(size_t n,uint32_t c){(void)c;return malloc(n);}
static inline size_t heap_caps_get_free_size(uint32_t c){(void)c;return 8u*1024*1024;}
