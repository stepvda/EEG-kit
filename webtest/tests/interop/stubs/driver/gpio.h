#pragma once
#include <stdint.h>
typedef int gpio_num_t; typedef int esp_err_t;
#define GPIO_MODE_INPUT 1
#define GPIO_MODE_OUTPUT 2
#define GPIO_INTR_NEGEDGE 3
#define GPIO_PULLUP_ENABLE 1
int sim_gpio_level(int pin);
#define gpio_get_level(p) sim_gpio_level(p)
static inline esp_err_t gpio_set_level(gpio_num_t p,uint32_t v){(void)p;(void)v;return 0;}
static inline esp_err_t gpio_set_direction(gpio_num_t p,int m){(void)p;(void)m;return 0;}
static inline esp_err_t gpio_isr_handler_add(gpio_num_t p,void(*f)(void*),void*a){(void)p;(void)f;(void)a;return 0;}
static inline esp_err_t gpio_install_isr_service(int f){(void)f;return 0;}
static inline esp_err_t gpio_set_intr_type(gpio_num_t p,int t){(void)p;(void)t;return 0;}
static inline esp_err_t gpio_config(const void* c){(void)c;return 0;}

#define GPIO_PULLUP_ONLY 1
static inline esp_err_t gpio_set_pull_mode(gpio_num_t p,int m){(void)p;(void)m;return 0;}
