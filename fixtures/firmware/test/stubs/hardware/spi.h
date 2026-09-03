/* hardware/spi.h -- STUB, declarations only.
 * Part of package_v2.3, TI One Voice research programme.  Licence: CC BY-SA 4.0. */
#ifndef STUB_HW_SPI_H
#define STUB_HW_SPI_H
#include <stdint.h>
#include <stddef.h>
typedef struct spi_inst spi_inst_t;
extern spi_inst_t *spi0;
unsigned spi_init(spi_inst_t *spi, unsigned baud);
int spi_write_blocking(spi_inst_t *spi, const uint8_t *src, size_t len);
#endif
