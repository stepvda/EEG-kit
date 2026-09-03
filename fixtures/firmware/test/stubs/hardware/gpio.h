/* hardware/gpio.h -- STUB, declarations only.  See pico/stdlib.h in this directory.
 * Part of package_v2.3, TI One Voice research programme.  Licence: CC BY-SA 4.0. */
#ifndef STUB_HW_GPIO_H
#define STUB_HW_GPIO_H
#include <stdint.h>
#include <stdbool.h>
enum gpio_function { GPIO_FUNC_SPI = 1, GPIO_FUNC_I2C = 3 };
#define GPIO_IN  0
#define GPIO_OUT 1
void gpio_init(unsigned gpio);
void gpio_set_dir(unsigned gpio, bool out);
void gpio_put(unsigned gpio, bool value);
bool gpio_get(unsigned gpio);
void gpio_set_function(unsigned gpio, enum gpio_function fn);
void gpio_pull_up(unsigned gpio);
#endif
