/* hardware/adc.h -- STUB, declarations only.
 * Part of package_v2.3, TI One Voice research programme.  Licence: CC BY-SA 4.0. */
#ifndef STUB_HW_ADC_H
#define STUB_HW_ADC_H
#include <stdint.h>
void     adc_init(void);
void     adc_gpio_init(unsigned gpio);
void     adc_select_input(unsigned input);
uint16_t adc_read(void);
#endif
