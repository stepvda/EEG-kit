/*
 * hal_rp2040.c -- the fixhal.h board interface on a Raspberry Pi Pico (RP2040).
 *
 * THIS FILE HAS NEVER BEEN RUN.  No fixture board exists (JIG-EEG-009 section 7), so
 * nothing below has met a relay, a mux or a colour sensor.  It compiles against the
 * Raspberry Pi Pico SDK, and test/run.sh compiles it a second time against the stub
 * headers in test/stubs/ so that a change to it cannot go unparsed just because the SDK is
 * not installed on the machine doing the review.  A stub compile proves the C is valid and
 * the fixhal.h contract is met.  It proves nothing about the peripherals.
 *
 * Pin assignment.  The numbers below are this file's, not a datasheet's: no fixture
 * schematic has been laid out, so a pin map has to start somewhere and this is it.  It is
 * the map fixtures/pcb/FIX-01/FIX-01_netlist.txt carries, and the two are generated and
 * hand-written respectively, so they are checked against each other by
 * tools/fixture_gen.py --check rather than by eye.
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#include "fixhal.h"
#include "fixproto.h"

#include <stdio.h>
#include <string.h>

#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/gpio.h"
#include "hardware/i2c.h"
#include "hardware/spi.h"

/* ------------------------------------------------------------------ pin map --------- */
/* TPIC6B595 chain.  SRCK and SER go to the SPI0 peripheral, RCK is driven by hand so that
 * a whole chain lands on one latch edge, and G is held low so the outputs are enabled.
 * SRCLR is tied to the RP2040 RUN-derived reset so a controller in reset opens the
 * relays without any code running -- that is the safe state and it must not depend on
 * firmware. */
#define PIN_SR_SER    3     /* SPI0 TX  */
#define PIN_SR_SRCK   2     /* SPI0 SCK */
#define PIN_SR_RCK    4
#define PIN_SR_G      5     /* output enable, active low */

/* CD74HC4067 address lines and the readback pull-up. */
#define PIN_MUX_A0    6
#define PIN_MUX_A1    7
#define PIN_MUX_A2    8
#define PIN_MUX_A3    9
#define PIN_MUX_EN   10     /* active low */
#define PIN_MUX_PULL 11     /* RP1 10k0 to the mux common; high = pull-up on, else Hi-Z */

/* Analogue inputs.  ADC0 is the mux common (M1); ADC1 and ADC2 are the two reference
 * electret preamplifier outputs (M2). */
#define ADC_MUX_INPUT 0
#define ADC_MIC_A     1
#define ADC_MIC_B     2

/* I2C0 to the TCS34725 breakout, FIX-01/E. */
#define PIN_I2C_SDA  16
#define PIN_I2C_SCL  17
#define I2C_HZ   100000

/* Discrete lines. */
#define PIN_LID_INTERLOCK 20    /* FIX-04, closed = low, so it is read inverted below */
#define PIN_MARKER        21    /* FIX-02, U201 comparator output through R201/R202    */
#define PIN_DRV_A         18
#define PIN_DRV_B         19
#define PIN_AMP_EN        22

#define ADC_VREF_MV  3300
#define ADC_FULL     4095

/* ------------------------------------------------------------------ lifecycle ------- */
void hal_init(void)
{
    stdio_init_all();

    spi_init(spi0, 4 * 1000 * 1000);
    gpio_set_function(PIN_SR_SER, GPIO_FUNC_SPI);
    gpio_set_function(PIN_SR_SRCK, GPIO_FUNC_SPI);

    gpio_init(PIN_SR_RCK);  gpio_set_dir(PIN_SR_RCK, GPIO_OUT);  gpio_put(PIN_SR_RCK, 0);
    gpio_init(PIN_SR_G);    gpio_set_dir(PIN_SR_G, GPIO_OUT);    gpio_put(PIN_SR_G, 0);

    gpio_init(PIN_MUX_A0);  gpio_set_dir(PIN_MUX_A0, GPIO_OUT);
    gpio_init(PIN_MUX_A1);  gpio_set_dir(PIN_MUX_A1, GPIO_OUT);
    gpio_init(PIN_MUX_A2);  gpio_set_dir(PIN_MUX_A2, GPIO_OUT);
    gpio_init(PIN_MUX_A3);  gpio_set_dir(PIN_MUX_A3, GPIO_OUT);
    gpio_init(PIN_MUX_EN);  gpio_set_dir(PIN_MUX_EN, GPIO_OUT); gpio_put(PIN_MUX_EN, 0);

    /* The pull-up line is left as an input, i.e. high impedance, and is only driven when a
     * readback is running.  A GPIO left as a driven low would put RP1 across the mux
     * common to ground and load every channel it selects. */
    gpio_init(PIN_MUX_PULL);
    gpio_set_dir(PIN_MUX_PULL, GPIO_IN);

    adc_init();
    adc_gpio_init(26 + ADC_MUX_INPUT);
    adc_gpio_init(26 + ADC_MIC_A);
    adc_gpio_init(26 + ADC_MIC_B);

    i2c_init(i2c0, I2C_HZ);
    gpio_set_function(PIN_I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(PIN_I2C_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(PIN_I2C_SDA);
    gpio_pull_up(PIN_I2C_SCL);

    gpio_init(PIN_LID_INTERLOCK);
    gpio_set_dir(PIN_LID_INTERLOCK, GPIO_IN);
    gpio_pull_up(PIN_LID_INTERLOCK);
    gpio_init(PIN_MARKER);
    gpio_set_dir(PIN_MARKER, GPIO_IN);

    gpio_init(PIN_DRV_A);  gpio_set_dir(PIN_DRV_A, GPIO_OUT);  gpio_put(PIN_DRV_A, 0);
    gpio_init(PIN_DRV_B);  gpio_set_dir(PIN_DRV_B, GPIO_OUT);  gpio_put(PIN_DRV_B, 0);
    gpio_init(PIN_AMP_EN); gpio_set_dir(PIN_AMP_EN, GPIO_OUT); gpio_put(PIN_AMP_EN, 0);

    hal_sr_clear();
}

uint64_t hal_now_us(void)      { return to_us_since_boot(get_absolute_time()); }
void     hal_sleep_ms(uint32_t ms) { sleep_ms(ms); }

/* ------------------------------------------------------------------ host link ------- */
int  hal_getchar(void)         { return getchar_timeout_us(0); }

void hal_putline(const char *s)
{
    fputs(s, stdout);
    fputc('\n', stdout);
    fflush(stdout);
}

/* ------------------------------------------------------------------ relay chain ----- */
void hal_sr_write(const uint8_t *bytes, int n)
{
    spi_write_blocking(spi0, bytes, (size_t)n);
    /* One rising edge on RCK moves every shift-register bit to its output latch at the
     * same instant, which is what makes CHALL one relay event and not sixteen. */
    gpio_put(PIN_SR_RCK, 1);
    sleep_us(1);
    gpio_put(PIN_SR_RCK, 0);
}

void hal_sr_clear(void)
{
    uint8_t zero[16];
    memset(zero, 0, sizeof zero);
    hal_sr_write(zero, (int)sizeof zero);   /* longer than any chain in the set */
}

/* ------------------------------------------------------------------ analogue -------- */
void hal_mux_select(int ch)
{
    gpio_put(PIN_MUX_A0, (ch >> 0) & 1);
    gpio_put(PIN_MUX_A1, (ch >> 1) & 1);
    gpio_put(PIN_MUX_A2, (ch >> 2) & 1);
    gpio_put(PIN_MUX_A3, (ch >> 3) & 1);
}

static int adc_mv(int input, int navg)
{
    uint32_t sum = 0;
    int i;
    if (navg < 1) navg = 1;
    adc_select_input(input);
    for (i = 0; i < navg; i++) sum += adc_read();
    return (int)((sum / (uint32_t)navg) * ADC_VREF_MV / ADC_FULL);
}

int hal_adc_mv(int navg)                 { return adc_mv(ADC_MUX_INPUT, navg); }
int hal_adc_mv_aux(int input, int navg)  { return adc_mv(input ? ADC_MIC_B : ADC_MIC_A,
                                                         navg); }

/* ------------------------------------------------------------------ I2C ------------- */
int hal_i2c_write(uint8_t addr, const uint8_t *buf, int n)
{
    return i2c_write_blocking(i2c0, addr, buf, (size_t)n, false) == n ? 0 : -1;
}

int hal_i2c_read(uint8_t addr, uint8_t reg, uint8_t *buf, int n)
{
    if (i2c_write_blocking(i2c0, addr, &reg, 1, true) != 1) return -1;
    return i2c_read_blocking(i2c0, addr, buf, (size_t)n, false) == n ? 0 : -1;
}

/* ------------------------------------------------------------------ discrete -------- */
int hal_gpio_get(enum fx_gpio which)
{
    switch (which) {
    /* The lid switch is wired to close to ground, so a closed lid reads low.  A broken
     * wire then reads open, which is the safe answer. */
    case FX_IN_LID_INTERLOCK: return gpio_get(PIN_LID_INTERLOCK) ? 0 : 1;
    case FX_IN_MARKER:        return gpio_get(PIN_MARKER) ? 1 : 0;
    default:                  return HAL_GPIO_ABSENT;
    }
}

void hal_gpio_set(enum fx_gpio which, int level)
{
    switch (which) {
    case FX_OUT_MUX_PULL:
        /* Driven high enables RP1; anything else returns the pin to high impedance so the
         * pull-up is not merely at the wrong level but absent. */
        if (level) {
            gpio_set_dir(PIN_MUX_PULL, GPIO_OUT);
            gpio_put(PIN_MUX_PULL, 1);
        } else {
            gpio_set_dir(PIN_MUX_PULL, GPIO_IN);
        }
        break;
    case FX_OUT_DRV_A:  gpio_put(PIN_DRV_A, level ? 1 : 0);  break;
    case FX_OUT_DRV_B:  gpio_put(PIN_DRV_B, level ? 1 : 0);  break;
    case FX_OUT_AMP_EN: gpio_put(PIN_AMP_EN, level ? 1 : 0); break;
    default: break;
    }
}

/* ------------------------------------------------------------------ audio (M2) ------ */
/* The I2S transmitter is NOT written here.  The PCM5102A needs BCK, LRCK and DATA at an
 * exact ratio, which on an RP2040 means a PIO program and a DMA chain, and a PIO program
 * written against no hardware and never run is not firmware -- it is a guess with a
 * comment on it.  What is stated instead is the contract the PIO block has to meet, in
 * JIG-EEG-009 section 8.6, and the three functions it has to provide.  Until it is
 * written, an M2 build refuses the tone verbs with FX_ERR_UNSUPPORTED rather than
 * returning a t0 for a tone nobody played, and TST-EEG-004 T12a, T12b and T13 stay
 * blocked on it -- which is the same state as the host test tool they also need
 * (JIG-EEG-009 section 7).
 *
 * The specification the block must meet:
 *   48.0 kHz sample rate, 16-bit stereo, BCK = 32 x LRCK, PCM5102A in software-free mode;
 *   a full-scale sine table generated at start, amplitude scaled by the commanded level in
 *   tenths of a decibel; the returned t0 is the time the FIRST sample is handed to the PIO
 *   FIFO, taken with interrupts disabled, so the number is the DMA start and not the
 *   command parse.
 */
uint64_t hal_tone_start(int hz, int level_tenths_db, int ms)
{
    (void)hz; (void)level_tenths_db; (void)ms;
    return 0;               /* zero means "no tone started"; fix_m2.c reports it as such */
}

void hal_tone_stop(void) { }
int  hal_tone_busy(void) { return 0; }
