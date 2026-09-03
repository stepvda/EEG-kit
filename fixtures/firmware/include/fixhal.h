/*
 * fixhal.h -- the board interface the EEG-kit fixture firmware is written against.
 *
 * What this is: the whole of the hardware surface used by the three fixture controllers
 * M1 (FIX-01), M2 (FIX-02) and M3 (FIX-04) of JIG-EEG-009 Rev B section 8.  Nothing above
 * this header touches a register, so the command layer can be compiled and driven on a
 * workstation against test/hal_sim.c, and src/hal_rp2040.c is the only file that has to be
 * read with an RP2040 datasheet open.
 *
 * Written by hand (this is source, not generated output).  Part of package_v2.3,
 * TI One Voice research programme.  Licence: CC BY-SA 4.0.
 *
 * NOTHING HERE HAS BEEN RUN ON HARDWARE.  No fixture has been built (JIG-EEG-009
 * section 7).  The protocol layer and the three command sets are exercised natively by
 * test/run.sh; the RP2040 implementation compiles and has never been executed.
 */
#ifndef FIXHAL_H
#define FIXHAL_H

#include <stdint.h>

/* ---------------------------------------------------------------- roles ------------ */
/* One firmware, three personalities.  The role is fixed at build time by -DFIX_ROLE_Mn
 * rather than read from a strap, because a fixture that can be talked into being another
 * fixture is a fixture that will one day drive 500 V DC relays with FIX-01's relay map.
 */
#define FIX_ROLE_NAME_M1 "M1"
#define FIX_ROLE_NAME_M2 "M2"
#define FIX_ROLE_NAME_M3 "M3"

/* ---------------------------------------------------------------- named GPIO -------- */
/* Logical input and output names.  The pin numbers live in hal_rp2040.c; the command
 * layer never sees one.  A HAL that has no such line returns HAL_GPIO_ABSENT.
 */
enum fx_gpio {
    FX_IN_LID_INTERLOCK = 0, /* FIX-04 lid switch, JIG-EEG-009 section 6.1.  1 = lid shut */
    FX_IN_MARKER,            /* FIX-02 U201 comparator output, after R201/R202            */
    FX_OUT_MUX_PULL,         /* FIX-01 readback pull-up enable, JIG-EEG-009 section 8.4   */
    FX_OUT_DRV_A,            /* FIX-02/A coupler driver enable                            */
    FX_OUT_DRV_B,            /* FIX-02/B coupler driver enable                            */
    FX_OUT_AMP_EN,           /* FIX-02 TPA6132 enable                                     */
    FX_GPIO_COUNT
};
#define HAL_GPIO_ABSENT (-1)

/* ---------------------------------------------------------------- lifecycle --------- */
void     hal_init(void);
uint64_t hal_now_us(void);
void     hal_sleep_ms(uint32_t ms);

/* ---------------------------------------------------------------- host link --------- */
/* Line in, line out, over USB CDC.  hal_getchar() returns -1 when nothing is waiting; the
 * main loop never blocks in it, so a fixture that is mid-test still answers STATE.
 */
int  hal_getchar(void);
void hal_putline(const char *s);

/* ---------------------------------------------------------------- relay chain ------- */
/* The TPIC6B595 daisy chain.  `bytes[0]` is shifted out FIRST and therefore ends up in the
 * LAST device of the chain; see JIG-EEG-009 section 8.4 for the map from relay number to
 * chain bit.  hal_sr_write() shifts, then pulses RCK once, so every relay in one call
 * changes on one latch edge.
 */
void hal_sr_write(const uint8_t *bytes, int n);
void hal_sr_clear(void);          /* all outputs off -- also what hal_init() leaves behind */

/* ---------------------------------------------------------------- analogue ---------- */
/* hal_mux_select() drives the CD74HC4067 address lines; hal_adc_mv() averages `navg`
 * conversions on the ADC input the mux common is wired to and returns millivolts.
 * Returns < 0 on a HAL that has no ADC.
 */
void hal_mux_select(int ch);      /* 0..15 */
int  hal_adc_mv(int navg);
int  hal_adc_mv_aux(int input, int navg);   /* M2 reference microphones: input 0 or 1 */

/* ---------------------------------------------------------------- I2C --------------- */
/* Returns 0 on success, negative on NAK or timeout. */
int hal_i2c_write(uint8_t addr, const uint8_t *buf, int n);
int hal_i2c_read(uint8_t addr, uint8_t reg, uint8_t *buf, int n);

/* ---------------------------------------------------------------- discrete ---------- */
int  hal_gpio_get(enum fx_gpio which);
void hal_gpio_set(enum fx_gpio which, int level);

/* ---------------------------------------------------------------- audio (M2) -------- */
/* A tone of `hz` at `level_tenths_db` below full scale for `ms` milliseconds, started
 * immediately and reported as started.  hal_tone_start() returns the microsecond stamp of
 * the first sample handed to the I2S peripheral -- the fixture-side t0 that JIG-EEG-009
 * section 8.6 BURST reports beside the marker edge.
 */
uint64_t hal_tone_start(int hz, int level_tenths_db, int ms);
void     hal_tone_stop(void);
int      hal_tone_busy(void);

#endif /* FIXHAL_H */
