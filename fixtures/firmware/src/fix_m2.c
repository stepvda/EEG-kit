/*
 * fix_m2.c -- M2, the FIX-02 controller: acoustic injection and the onset marker.
 *
 * The hardware is JIG-EEG-009 Rev B sections 2.2, 2.3 and 8.6: an RP2040 driving a
 * PCM5102A I2S DAC into a TPA6132 amplifier, one of two coupler drivers at a time, two
 * reference electrets read on the ADC, and the FIX-02/D onset comparator U201 brought back
 * to a GPIO so that the fixture can timestamp its own marker.
 *
 * The one command worth explaining is BURST.  TST-EEG-004 T12b measures the delay between
 * the DUT's envelope onset and the marker onset ON THE DUT'S OWN converter, which is the
 * point of the marker: the comparison never crosses a clock boundary.  BURST does not
 * replace that measurement.  It reports the delay from the fixture's own t0 -- the first
 * sample handed to the I2S peripheral -- to the comparator's first edge, which is the
 * fixture's own contribution to the total and is what section 5.2 calibrates every six
 * months against a 100 MHz oscilloscope.  Two independent numbers, and a disagreement
 * between them tells the test engineer which side moved.
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#include "fixproto.h"
#include "fixhal.h"

#include <stdio.h>
#include <string.h>

const char *const fx_role_name    = FIX_ROLE_NAME_M2;
const char *const fx_fixture_name = "FIX-02";

/* Limits.  The frequency range is the audio band the couplers are calibrated over
 * (section 2.2 sets the 1 kHz reference); the level is in tenths of a decibel below
 * digital full scale, matching the DUT's own SET_HP_LEVEL argument in FW-EEG-001
 * section 6.3 so that one unit of level means one thing on both sides of the bench. */
#define TONE_HZ_MIN        20
#define TONE_HZ_MAX     20000
#define TONE_MS_MAX     60000
#define LEVEL_TENTHS_MIN (-800)      /* -80.0 dBFS */
#define LEVEL_TENTHS_MAX      0      /*   0.0 dBFS */
#define BURST_WAIT_US   1000000ull   /* one second before a missing edge is a timeout    */

enum { DRV_OFF = 0, DRV_A, DRV_B };
static const char *const drv_name[] = { "OFF", "A", "B" };

static int      drv_sel;
static int      last_hz, last_level;
static uint64_t last_t0_us, last_edge_us;
static int      last_edge_valid;

void fx_role_safe(void)
{
    hal_tone_stop();
    hal_gpio_set(FX_OUT_AMP_EN, 0);
    hal_gpio_set(FX_OUT_DRV_A, 0);
    hal_gpio_set(FX_OUT_DRV_B, 0);
    drv_sel = DRV_OFF;
}

void fx_role_init(void)
{
    last_hz = 0;
    last_level = 0;
    last_t0_us = 0;
    last_edge_us = 0;
    last_edge_valid = 0;
    fx_role_safe();
}

void fx_role_state(void)
{
    fx_info("driver=%s tone=%s last_hz=%d last_level_tenths_db=%d",
            drv_name[drv_sel], hal_tone_busy() ? "on" : "off", last_hz, last_level);
    fx_info("marker_now=%d last_burst_delay_us=%s%lld",
            hal_gpio_get(FX_IN_MARKER),
            last_edge_valid ? "" : "invalid:",
            last_edge_valid ? (long long)(last_edge_us - last_t0_us) : 0);
}

void fx_role_poll(void) { }

/* ------------------------------------------------------------------ verbs ----------- */
static int cmd_drv(int argc, char **argv)
{
    int sel, rc;
    if (argc == 0) {
        fx_reply("OK DRV sel=%s", drv_name[drv_sel]);
        return FX_OK;
    }
    rc = fx_arg_keyword(argv[0], drv_name, 3, &sel);
    if (rc != FX_OK) return rc;
    if (hal_tone_busy()) {
        fx_detail("a tone is playing; send TONE STOP first");
        return FX_ERR_STATE;
    }
    /* Never both.  The two couplers have different cavity volumes and different recorded
     * drive constants (section 2.2), so a state in which both are driven has no calibrated
     * meaning and is refused rather than allowed and warned about. */
    hal_gpio_set(FX_OUT_DRV_A, sel == DRV_A);
    hal_gpio_set(FX_OUT_DRV_B, sel == DRV_B);
    hal_gpio_set(FX_OUT_AMP_EN, sel != DRV_OFF);
    drv_sel = sel;
    fx_reply("OK DRV sel=%s", drv_name[drv_sel]);
    return FX_OK;
}

static int parse_tone(char **argv, long *hz, long *lvl, long *ms)
{
    int rc;
    rc = fx_arg_int(argv[0], TONE_HZ_MIN, TONE_HZ_MAX, hz);
    if (rc != FX_OK) return rc;
    rc = fx_arg_int(argv[1], LEVEL_TENTHS_MIN, LEVEL_TENTHS_MAX, lvl);
    if (rc != FX_OK) return rc;
    return fx_arg_int(argv[2], 1, TONE_MS_MAX, ms);
}

static int cmd_tone(int argc, char **argv)
{
    long hz, lvl, ms;
    int rc;
    if (argc == 1 && strcmp(argv[0], "STOP") == 0) {
        hal_tone_stop();
        fx_reply("OK TONE stopped=1");
        return FX_OK;
    }
    if (argc != 3) {
        fx_detail("TONE <hz> <tenths_db_below_fs> <ms>, or TONE STOP");
        return FX_ERR_SYNTAX;
    }
    if (drv_sel == DRV_OFF) {
        fx_detail("no coupler driver selected; send DRV A or DRV B first");
        return FX_ERR_STATE;
    }
    rc = parse_tone(argv, &hz, &lvl, &ms);
    if (rc != FX_OK) return rc;
    last_t0_us = hal_tone_start((int)hz, (int)lvl, (int)ms);
    if (last_t0_us == 0) {
        /* A HAL with no I2S block returns 0 rather than a plausible timestamp.  Reporting
         * a t0 for a tone nobody played is the one failure mode this fixture must not
         * have: every T12b number is a difference against it. */
        fx_detail("the I2S block is not implemented in this build (JIG-EEG-009 section 8.6)");
        return FX_ERR_UNSUPPORTED;
    }
    last_hz = (int)hz;
    last_level = (int)lvl;
    fx_reply("OK TONE hz=%ld level_tenths_db=%ld ms=%ld drv=%s t0_us=%llu",
             hz, lvl, ms, drv_name[drv_sel], (unsigned long long)last_t0_us);
    return FX_OK;
}

static int cmd_mic(int argc, char **argv)
{
    static const char *const which[] = { "A", "B" };
    int sel, rc, mv;
    long navg = 64;
    rc = fx_arg_keyword(argv[0], which, 2, &sel);
    if (rc != FX_OK) return rc;
    if (argc > 1) {
        rc = fx_arg_int(argv[1], 1, 4096, &navg);
        if (rc != FX_OK) return rc;
    }
    mv = hal_adc_mv_aux(sel, (int)navg);
    if (mv < 0) {
        fx_detail("reference microphone %s did not read", which[sel]);
        return FX_ERR_HARDWARE;
    }
    /* Millivolts, and nothing else.  The sensitivity of each reference electret and the
     * 70.0 dB SPL drive constant of its coupler are recorded on the host at calibration
     * (section 2.2); a sound pressure computed in here would be a number with no
     * traceability behind it. */
    fx_reply("OK MIC which=%s mv=%d navg=%ld spl=host", which[sel], mv, navg);
    return FX_OK;
}

static int cmd_mark(int argc, char **argv)
{
    (void)argc; (void)argv;
    fx_reply("OK MARK level=%d", hal_gpio_get(FX_IN_MARKER));
    return FX_OK;
}

static int cmd_burst(int argc, char **argv)
{
    long hz, lvl, ms;
    int rc, started;
    uint64_t t0, deadline;

    if (drv_sel == DRV_OFF) {
        fx_detail("no coupler driver selected; send DRV A or DRV B first");
        return FX_ERR_STATE;
    }
    if (argc != 3) {
        fx_detail("BURST <hz> <tenths_db_below_fs> <ms>");
        return FX_ERR_SYNTAX;
    }
    rc = parse_tone(argv, &hz, &lvl, &ms);
    if (rc != FX_OK) return rc;

    started = hal_gpio_get(FX_IN_MARKER);
    if (started == 1) {
        /* The comparator is already high before the burst.  Reporting a delay from a
         * threshold that was crossed before t0 would be a fiction, so the burst is
         * refused instead. */
        fx_detail("marker is already high; check the comparator threshold "
                  "and that no tone is playing");
        return FX_ERR_STATE;
    }

    t0 = hal_tone_start((int)hz, (int)lvl, (int)ms);
    if (t0 == 0) {
        fx_detail("the I2S block is not implemented in this build (JIG-EEG-009 section 8.6)");
        return FX_ERR_UNSUPPORTED;
    }
    last_t0_us = t0;
    last_hz = (int)hz;
    last_level = (int)lvl;
    last_edge_valid = 0;
    deadline = t0 + BURST_WAIT_US;
    while (hal_now_us() < deadline) {
        if (hal_gpio_get(FX_IN_MARKER) == 1) {
            last_edge_us = hal_now_us();
            last_edge_valid = 1;
            break;
        }
    }
    if (!last_edge_valid) {
        hal_tone_stop();
        fx_detail("no comparator edge within %llu us of t0",
                  (unsigned long long)BURST_WAIT_US);
        return FX_ERR_TIMEOUT;
    }
    /* The delay reported here is the FIXTURE-side delay: DAC, amplifier, load and
     * comparator.  It is polled in software, so its resolution is the loop period and not
     * the microsecond the number is printed in; section 8.6 says so and section 5.2
     * calibrates the constant on a scope. */
    fx_reply("OK BURST hz=%ld ms=%ld t0_us=%llu edge_us=%llu delay_us=%llu polled=1",
             hz, ms, (unsigned long long)t0, (unsigned long long)last_edge_us,
             (unsigned long long)(last_edge_us - t0));
    return FX_OK;
}

const struct fx_command fx_commands[] = {
    { "DRV",   cmd_drv,   0, 1, "DRV [OFF|A|B] -- select one coupler driver, never both" },
    { "TONE",  cmd_tone,  1, 3, "TONE <hz> <tenths_db> <ms> | TONE STOP" },
    { "BURST", cmd_burst, 3, 3, "BURST <hz> <tenths_db> <ms> -- tone, then time the marker" },
    { "MIC",   cmd_mic,   1, 2, "MIC <A|B> [navg] -- reference electret, millivolts" },
    { "MARK",  cmd_mark,  0, 0, "MARK -- the U201 comparator output right now" },
    { NULL, NULL, 0, 0, NULL }
};
