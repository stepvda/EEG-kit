/* hardware/i2c.h -- STUB, declarations only.
 * Part of package_v2.3, TI One Voice research programme.  Licence: CC BY-SA 4.0. */
#ifndef STUB_HW_I2C_H
#define STUB_HW_I2C_H
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
typedef struct i2c_inst i2c_inst_t;
extern i2c_inst_t *i2c0;
unsigned i2c_init(i2c_inst_t *i2c, unsigned baud);
int i2c_write_blocking(i2c_inst_t *i2c, uint8_t addr, const uint8_t *src, size_t len,
                       bool nostop);
int i2c_read_blocking(i2c_inst_t *i2c, uint8_t addr, uint8_t *dst, size_t len, bool nostop);
#endif
