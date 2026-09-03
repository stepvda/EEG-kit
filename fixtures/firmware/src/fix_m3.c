/*
 * fix_m3.c -- M3, the FIX-04 24-channel harness scanner card.
 *
 * The hardware is JIG-EEG-009 Rev B section 4.1 and section 8.7: twenty-four DPDT relays
 * on three TPIC6B595 devices, each relay taking one harness conductor either to the
 * instrument bus (energised) or to the common bus (released), plus the interlocked lid
 * switch that section 6.1 already prices.
 *
 * This is the only fixture in the set that switches a lethal voltage.  WH-EEG-008 H4 and
 * H10 apply 500 V DC through this card, and a relay changing state under that voltage arcs
 * its contacts and can carry the test voltage somewhere the operator did not intend.  The
 * firmware therefore refuses every switching command while HV is armed, refuses to arm
 * while the lid is open, and refuses to switch for a stated discharge dwell after
 * disarming.  None of that is a substitute for the interlock being wired: the firmware can
 * only refuse a command it is sent, and it cannot open a relay a stuck driver is holding.
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#include "fixproto.h"
#include "fixhal.h"

#include <stdio.h>
#include <string.h>

const char *const fx_role_name    = FIX_ROLE_NAME_M3;
const char *const fx_fixture_name = "FIX-04";

#define SCAN_CHANNELS  24
#define CHAIN_BYTES     3            /* three TPIC6B595, 24 outputs, none spare          */
#define RELAY_SETTLE_MS 10           /* as M1; the same stated constant, the same reason */

/* HV_DISCHARGE_MS is a stated fixture constant and not a measurement.  It has to be at
 * least the time the fitted insulation tester takes to discharge the cable capacitance it
 * has just charged to 500 V, and the Megger MIT525-class tester named in section 6.1 is
 * not in this package.  Five seconds is what the firmware enforces and it is the number to
 * check against the tester's own discharge specification before the first H4. */
#define HV_DISCHARGE_MS 5000

static uint8_t  chain[CHAIN_BYTES];
static int      hv_armed;
static uint64_t hv_safe_us;          /* when HV last went from armed to safe             */
static int      ever_armed;

/* Chain order: U30 receives SER, then U31, then U32 last.  hal_sr_write() shifts bytes[0]
 * first and first-out travels furthest, so bytes[0] lands in U32 and bytes[2] in U30.
 * Channel c of 1..24 is therefore in byte 2 - (c-1)/8, bit (c-1)%8. */
static int ch_byte(int c) { return 2 - (c - 1) / 8; }
static int ch_bit(int c)  { return (c - 1) % 8; }

static void chain_push(void)
{
    hal_sr_write(chain, CHAIN_BYTES);
    hal_sleep_ms(RELAY_SETTLE_MS);
}

static int scan_mask_get(void)
{
    int c, m = 0;
    for (c = 1; c <= SCAN_CHANNELS; c++)
        if ((chain[ch_byte(c)] >> ch_bit(c)) & 1) m |= 1 << (c - 1);
    return m;
}

/* The one gate every switching verb goes through. */
static int switching_allowed(void)
{
    if (hv_armed) {
        fx_detail("HV is armed; send HV SAFE and wait %d ms before switching",
                  HV_DISCHARGE_MS);
        return FX_ERR_INTERLOCK;
    }
    if (ever_armed && hal_now_us() - hv_safe_us < (uint64_t)HV_DISCHARGE_MS * 1000ull) {
        fx_detail("within the %d ms discharge dwell after HV SAFE", HV_DISCHARGE_MS);
        return FX_ERR_INTERLOCK;
    }
    return FX_OK;
}

void fx_role_safe(void)
{
    memset(chain, 0, sizeof chain);
    hal_sr_write(chain, CHAIN_BYTES);
    hv_armed = 0;
    hv_safe_us = hal_now_us();
}

void fx_role_init(void)
{
    ever_armed = 0;
    fx_role_safe();
    ever_armed = 0;                  /* a boot is not a disarm, so no dwell is owed */
}

void fx_role_state(void)
{
    fx_info("scan_mask=%06X channels_to_instrument=%d",
            (unsigned)scan_mask_get(), __builtin_popcount((unsigned)scan_mask_get()));
    fx_info("hv=%s lid_interlock=%d discharge_dwell_ms=%d",
            hv_armed ? "ARMED" : "safe", hal_gpio_get(FX_IN_LID_INTERLOCK),
            HV_DISCHARGE_MS);
}

void fx_role_poll(void)
{
    /* The lid opening while HV is armed is the case the interlock exists for.  The
     * firmware cannot open the tester's own contactor, so it does the two things it can:
     * it drops every relay to the common bus and it says so. */
    if (hv_armed && hal_gpio_get(FX_IN_LID_INTERLOCK) == 0) {
        hv_armed = 0;
        hv_safe_us = hal_now_us();
        memset(chain, 0, sizeof chain);
        hal_sr_write(chain, CHAIN_BYTES);
        fx_info("INTERLOCK lid opened with HV armed -- all channels dropped to the common "
                "bus and HV disarmed. Stop the tester before opening the lid.");
    }
}

/* ------------------------------------------------------------------ verbs ----------- */
static int cmd_scan(int argc, char **argv)
{
    long c;
    int rc;
    if (argc == 0) {
        fx_reply("OK SCAN mask=%06X", (unsigned)scan_mask_get());
        return FX_OK;
    }
    rc = switching_allowed();
    if (rc != FX_OK) return rc;
    if (strcmp(argv[0], "OFF") == 0) {
        memset(chain, 0, sizeof chain);
        chain_push();
        fx_reply("OK SCAN mask=000000 all=common");
        return FX_OK;
    }
    rc = fx_arg_int(argv[0], 1, SCAN_CHANNELS, &c);
    if (rc != FX_OK) return rc;
    /* One-hot, and break-before-make: every channel to the common bus, then the one
     * channel to the instrument. */
    memset(chain, 0, sizeof chain);
    chain_push();
    chain[ch_byte((int)c)] |= (uint8_t)(1 << ch_bit((int)c));
    chain_push();
    fx_reply("OK SCAN ch=%ld mask=%06X", c, (unsigned)scan_mask_get());
    return FX_OK;
}

static int cmd_scanmask(int argc, char **argv)
{
    uint8_t b[CHAIN_BYTES];
    int rc;
    if (argc == 0) {
        fx_reply("OK SCANMASK mask=%06X", (unsigned)scan_mask_get());
        return FX_OK;
    }
    rc = switching_allowed();
    if (rc != FX_OK) return rc;
    rc = fx_arg_hex(argv[0], b, CHAIN_BYTES);
    if (rc != FX_OK) return rc;
    memset(chain, 0, sizeof chain);
    chain_push();
    memcpy(chain, b, CHAIN_BYTES);
    chain_push();
    /* The all-pairs isolation matrix of WH-EEG-008 H2 is what this verb is for: one
     * conductor on the instrument, the other twenty-three on the common bus, twenty-four
     * times over. */
    fx_reply("OK SCANMASK mask=%06X count=%d", (unsigned)scan_mask_get(),
             __builtin_popcount((unsigned)scan_mask_get()));
    return FX_OK;
}

static int cmd_hv(int argc, char **argv)
{
    static const char *const sub[] = { "SAFE", "ARM" };
    int which, rc;
    if (argc == 0) {
        fx_reply("OK HV state=%s lid=%d", hv_armed ? "ARMED" : "SAFE",
                 hal_gpio_get(FX_IN_LID_INTERLOCK));
        return FX_OK;
    }
    rc = fx_arg_keyword(argv[0], sub, 2, &which);
    if (rc != FX_OK) return rc;
    if (which == 0) {
        if (hv_armed) { hv_safe_us = hal_now_us(); ever_armed = 1; }
        hv_armed = 0;
        fx_reply("OK HV state=SAFE dwell_ms=%d", HV_DISCHARGE_MS);
        return FX_OK;
    }
    if (hal_gpio_get(FX_IN_LID_INTERLOCK) != 1) {
        fx_detail("lid interlock open; close the lid before arming");
        return FX_ERR_INTERLOCK;
    }
    hv_armed = 1;
    ever_armed = 1;
    fx_reply("OK HV state=ARMED mask=%06X switching=refused",
             (unsigned)scan_mask_get());
    return FX_OK;
}

static int cmd_lid(int argc, char **argv)
{
    (void)argc; (void)argv;
    fx_reply("OK LID closed=%d", hal_gpio_get(FX_IN_LID_INTERLOCK));
    return FX_OK;
}

const struct fx_command fx_commands[] = {
    { "SCAN",     cmd_scan,     0, 1, "SCAN [1-24|OFF] -- one conductor to the instrument" },
    { "SCANMASK", cmd_scanmask, 0, 1, "SCANMASK [6 hex digits] -- 24-bit pattern (H2)" },
    { "HV",       cmd_hv,       0, 1, "HV [ARM|SAFE] -- 500 V DC gate; blocks switching" },
    { "LID",      cmd_lid,      0, 0, "LID -- the interlock switch state" },
    { NULL, NULL, 0, 0, NULL }
};
