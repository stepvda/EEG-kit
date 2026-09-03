/*
 * pico/stdlib.h -- STUB.  Not the Raspberry Pi Pico SDK.
 *
 * Declarations only, enough for `cc -c src/hal_rp2040.c` to typecheck on a machine with no
 * SDK installed.  There are no bodies here and nothing links against it; see test/run.sh.
 * Part of package_v2.3, TI One Voice research programme.  Licence: CC BY-SA 4.0.
 */
#ifndef STUB_PICO_STDLIB_H
#define STUB_PICO_STDLIB_H
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
typedef uint64_t absolute_time_t;
absolute_time_t get_absolute_time(void);
uint64_t        to_us_since_boot(absolute_time_t t);
void            sleep_ms(uint32_t ms);
void            sleep_us(uint64_t us);
void            stdio_init_all(void);
int             getchar_timeout_us(uint32_t us);
#endif
