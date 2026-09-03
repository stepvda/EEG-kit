/*
 * hal_sim.c -- a workstation implementation of fixhal.h, for test/host_test.c.
 *
 * It is a MODEL OF THE FIXTURE, not a model of the firmware: the relay chain, the readback
 * divider, the mux, the colour sensor and the marker comparator are simulated from the
 * arithmetic in JIG-EEG-009 section 8, and the firmware above it is the real firmware.
 * That is the same arrangement webtest/tests/interop uses for the product firmware, and it
 * catches the same class of defect -- a command layer that says one thing and does
 * another.  It cannot catch a wrong pin number or a peripheral misconfiguration, and the
 * firmware README says so.
 *
 * The clock is virtual: hal_now_us() advances one microsecond per call and hal_sleep_ms()
 * advances the whole interval without sleeping, so a self-test that costs 9.6 s of relay
 * settling on hardware costs nothing here and a one-second timeout is reached in a few
 * thousand loop passes rather than a second.
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#include "fixhal.h"

#include <stdio.h>
#include <string.h>

/* ------------------------------------------------------------------ clock ----------- */
static uint64_t now_us;

uint64_t hal_now_us(void)          { return ++now_us; }
void     hal_sleep_ms(uint32_t ms) { now_us += (uint64_t)ms * 1000u; }

/* ------------------------------------------------------------------ host link ------- */
/* The test drives the firmware directly through fx_feed(), so there is no input queue;
 * output is captured by the test through sim_take_output(). */
static char   out[65536];
static size_t out_len;

int hal_getchar(void) { return -1; }

void hal_putline(const char *s)
{
    size_t n = strlen(s);
    if (out_len + n + 2 >= sizeof out) return;
    memcpy(out + out_len, s, n);
    out_len += n;
    out[out_len++] = '\n';
    out[out_len] = '\0';
}

const char *sim_output(void)   { return out; }
void        sim_clear(void)    { out_len = 0; out[0] = '\0'; }

/* ------------------------------------------------------------------ relay chain ----- */
static uint8_t chain[16];
static int     chain_len;
static int     latches;

void hal_sr_write(const uint8_t *bytes, int n)
{
    if (n > (int)sizeof chain) n = (int)sizeof chain;
    memcpy(chain, bytes, (size_t)n);
    chain_len = n;
    latches++;
}

void hal_sr_clear(void)
{
    memset(chain, 0, sizeof chain);
    latches++;
}

int sim_latches(void) { return latches; }

int sim_relay(int k)   /* the M1 map of fix_m1.c, duplicated here on purpose */
{
    int b = (k >= 101) ? 0 : 10 - (k - 1) / 8;
    int i = (k >= 101) ? (k - 101) : ((k - 1) % 8);
    if (b < 0 || b >= (int)sizeof chain) return -1;
    return (chain[b] >> i) & 1;
}

int sim_scan_relay(int c)  /* the M3 map of fix_m3.c */
{
    int b = 2 - (c - 1) / 8;
    int i = (c - 1) % 8;
    if (b < 0 || b >= (int)sizeof chain) return -1;
    return (chain[b] >> i) & 1;
}

/* ------------------------------------------------------------------ analogue -------- */
/* The readback network of JIG-EEG-009 section 8.4, modelled: RP1 = 10.0 kOhm from 3.300 V
 * to the mux common, and whatever the closed relay of the selected channel puts across it.
 * Two relays closed at once is modelled as the parallel combination, so a firmware that
 * forgot to break before it made would read a number that no single position produces. */
static int mux_ch;
static int pull_on;

void hal_mux_select(int ch) { mux_ch = ch; }

int hal_adc_mv(int navg)
{
    const long long PULL_MV = 3300, PULL_OHM = 10000, S = 1000000000LL;
    long long g = 0;                      /* conductance in units of 1e-9 siemens */
    int  n = mux_ch + 1;
    int  shorted = 0;
    (void)navg;
    if (!pull_on) return 0;
    if (n < 1 || n > 16) return 0;
    if (sim_relay(5 * n - 4)) g += S / 18LL;       /* SRC, divider Zo 18 R */
    if (sim_relay(5 * n - 3)) g += S / 4990LL;     /* RA 4k99              */
    if (sim_relay(5 * n - 2)) g += S / 10000LL;    /* RB 10k0              */
    if (sim_relay(5 * n - 1)) g += S / 49900LL;    /* RC 49k9              */
    if (sim_relay(5 * n))     shorted = 1;         /* SHORT                */
    if (shorted) return 0;
    if (g == 0) return (int)PULL_MV;               /* OPEN                 */
    {
        long long r = S / g;
        return (int)(PULL_MV * r / (r + PULL_OHM));
    }
}

int hal_adc_mv_aux(int input, int navg)
{
    (void)navg;
    return input ? 812 : 734;             /* two arbitrary but distinguishable readings */
}

/* ------------------------------------------------------------------ I2C ------------- */
/* A TCS34725 with a fixed reading.  R = 1200, G = 400, so R/G is exactly 3000 per mille
 * and the test can check the firmware's rounding rather than a sensor's noise. */
static uint8_t tcs[0x20] = { 0 };
static int     tcs_present = 1;

void sim_tcs_present(int yes) { tcs_present = yes; }

static void tcs_init_once(void)
{
    static int done;
    if (done) return;
    done = 1;
    tcs[0x12] = 0x44;                                   /* ID  */
    tcs[0x14] = 2000 & 0xFF; tcs[0x15] = 2000 >> 8;     /* C   */
    tcs[0x16] = 1200 & 0xFF; tcs[0x17] = 1200 >> 8;     /* R   */
    tcs[0x18] =  400 & 0xFF; tcs[0x19] =  400 >> 8;     /* G   */
    tcs[0x1A] =  300 & 0xFF; tcs[0x1B] =  300 >> 8;     /* B   */
}

int hal_i2c_write(uint8_t addr, const uint8_t *buf, int n)
{
    tcs_init_once();
    if (!tcs_present || addr != 0x29 || n < 2) return -1;
    tcs[buf[0] & 0x1F] = buf[1];
    return 0;
}

int hal_i2c_read(uint8_t addr, uint8_t reg, uint8_t *buf, int n)
{
    int i;
    tcs_init_once();
    if (!tcs_present || addr != 0x29) return -1;
    for (i = 0; i < n; i++) buf[i] = tcs[(reg + i) & 0x1F];
    return 0;
}

/* ------------------------------------------------------------------ discrete -------- */
static int lid_closed = 1;
static int marker_level;
static uint64_t tone_t0, tone_end_us;

void sim_set_lid(int closed) { lid_closed = closed ? 1 : 0; }

int hal_gpio_get(enum fx_gpio which)
{
    switch (which) {
    case FX_IN_LID_INTERLOCK: return lid_closed;
    case FX_IN_MARKER:
        /* The comparator goes high 250 us after the tone starts and stays high for the
         * length of the burst.  250 us is a made-up model constant and is here so that
         * BURST has an edge to find; it is not a claim about any real signal path. */
        if (tone_t0 && now_us >= tone_t0 + 250 && now_us < tone_end_us) return 1;
        return marker_level;
    default: return HAL_GPIO_ABSENT;
    }
}

static int gpio_out[FX_GPIO_COUNT];

void hal_gpio_set(enum fx_gpio which, int level)
{
    if ((int)which < FX_GPIO_COUNT) gpio_out[which] = level ? 1 : 0;
    if (which == FX_OUT_MUX_PULL) pull_on = level ? 1 : 0;
}

int sim_gpio_out(enum fx_gpio which) { return gpio_out[which]; }

/* ------------------------------------------------------------------ audio ----------- */
uint64_t hal_tone_start(int hz, int level_tenths_db, int ms)
{
    (void)hz; (void)level_tenths_db;
    tone_t0 = ++now_us;
    tone_end_us = tone_t0 + (uint64_t)ms * 1000u;
    return tone_t0;
}

void hal_tone_stop(void) { tone_t0 = 0; tone_end_us = 0; }
int  hal_tone_busy(void) { return tone_t0 && now_us < tone_end_us; }

/* ------------------------------------------------------------------ lifecycle ------- */
void hal_init(void)
{
    now_us = 1;
    out_len = 0;
    out[0] = '\0';
    memset(chain, 0, sizeof chain);
    chain_len = 0;
    latches = 0;
    mux_ch = 0;
    pull_on = 0;
    lid_closed = 1;
    marker_level = 0;
    tone_t0 = tone_end_us = 0;
    memset(gpio_out, 0, sizeof gpio_out);
}
