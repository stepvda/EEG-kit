/*
 * fix_m1.c -- M1, the FIX-01 controller: 83 relays, the relay readback and FIX-01/E.
 *
 * The hardware this is written against is JIG-EEG-009 Rev B sections 1.2, 1.5, 1.7, 1.8
 * and 8.4.  Two things in it are worth reading before the code:
 *
 *   The relay map is the one in the section 1.2 text schematic and nowhere else.  Channel
 *   n owns K(5n-4) SRC, K(5n-3) RA, K(5n-2) RB, K(5n-1) RC and K(5n) SHORT, for n = 1..16,
 *   and the three source relays are K101, K102 (polarity commutator) and K103 (SIN/CAL).
 *   That is 83 relays and eleven TPIC6B595 devices -- not the ten of the Rev B bill of
 *   materials, which is 80 outputs for 83 loads.  JIG-EEG-009 section 1.8 carries the
 *   correction and section 8.4 the chain map.
 *
 *   Every mode change is break-before-make.  The five relays of a channel share one node;
 *   closing RB before SRC has opened would put the 5.0000 V reference across a 10.0 kOhm
 *   leg through the divider for the operate time of one relay, and the whole point of the
 *   1000:1 divider is that no switch contact ever appears in a ratio leg.
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#include "fixproto.h"
#include "fixhal.h"

#include <stdio.h>
#include <string.h>

const char *const fx_role_name    = FIX_ROLE_NAME_M1;
const char *const fx_fixture_name = "FIX-01";

/* ------------------------------------------------------------------ constants ------- */
#define CHANNELS      16
#define CHAIN_BYTES   11              /* eleven TPIC6B595, 88 outputs, 83 used           */
#define RELAY_SETTLE_MS 10            /* stated fixture constant; see the note below     */

/* RELAY_SETTLE_MS is a fixture constant, not a measurement.  It has to be at least the
 * operate time and at least the release time of the fitted relay, and the Omron G6K-2F-Y
 * datasheet is not in this package, so 10 ms is stated here as the value the firmware
 * uses and as the number to check.  If the fitted relay is slower, this is the one line
 * to change; if it is faster, nothing breaks and a channel change costs 20 ms instead of
 * the minimum it could.  A whole-fixture CHALL is two writes, so 20 ms, not 16 x 20 ms. */

/* The readback network of JIG-EEG-009 section 8.4: one 10.0 kOhm 0.1 % resistor RP1 from
 * a GPIO to the CD74HC4067 common, enabled only while a readback is running.  These are
 * the nominal figures; the shift-start check of section 1.12 step 2 is made against the
 * value RECORDED at fixture calibration, not against these. */
#define PULL_MV      3300L            /* the RP2040 3V3 rail, nominal                    */
#define PULL_OHM     10000L
#define REF_RA_OHM    4990L
#define REF_RB_OHM   10000L
#define REF_RC_OHM   49900L
#define SRC_ZO_OHM      18L           /* divider output impedance, JIG-EEG-009 section 1.3 */

/* TCS34725, FIX-01/E.  Register numbers are from the AMS datasheet and are confirmed at
 * run time: COL INIT reads the ID register and refuses to go on if it is not 0x44, so a
 * wrong address or a different sensor on the breakout is a clean error and not a column
 * of plausible numbers. */
#define TCS_ADDR      0x29
#define TCS_CMD       0xA0            /* command | auto-increment                        */
#define TCS_ENABLE    0x00
#define TCS_ATIME     0x01
#define TCS_CONTROL   0x0F
#define TCS_ID        0x12
#define TCS_STATUS    0x13
#define TCS_CDATAL    0x14
#define TCS_EN_PON    0x01
#define TCS_EN_AEN    0x02
#define TCS_ID_34725  0x44
/* 300 ms = 125 integration steps of 2.4 ms, JIG-EEG-009 section 1.7.  ATIME counts down
 * from 256, so 256 - 125 = 131. */
#define TCS_ATIME_300MS 131
#define TCS_INTEG_MS    300

enum { M_OPEN = 0, M_SRC, M_RA, M_RB, M_RC, M_SHORT, M_MODES };
static const char *const mode_name[M_MODES] = { "OPEN", "SRC", "RA", "RB", "RC", "SHORT" };
/* The document's own vocabulary.  Section 1.5 calls the source modes SIN and CAL and the
 * reference modes 4k99 / 10k0 / 49k9; those names are accepted here and mean the same
 * relays, so a test script can be written in the words of the document it came from. */
static const char *const alias_name[] = { "SIN", "CAL", "4K99", "10K0", "49K9" };
static const int         alias_mode[] = { M_SRC, M_SRC, M_RA,  M_RB,   M_RC   };

enum { SRC_OFF = 0, SRC_SIN, SRC_CAL };
static const char *const src_name[] = { "OFF", "SIN", "CAL" };

/* ------------------------------------------------------------------ state ----------- */
static uint8_t  chain[CHAIN_BYTES];
static int      ch_mode[CHANNELS + 1];
static int      src_sel;
static int      pol_b;                /* 0 = polarity A, 1 = polarity B (K101/K102)      */
static int      selftest_armed;
static uint64_t selftest_armed_us;
static int      col_ready;
static int      col_gain;

#define ARM_TIMEOUT_US (300ull * 1000000ull)   /* five minutes, then it disarms itself   */

/* ------------------------------------------------------------------ relay plumbing -- */
/* Chain order: U10 receives SER from the controller, then U11..U19, then U22 last.  Data
 * shifted out first travels furthest, and hal_sr_write() shifts bytes[0] first, so
 * bytes[0] lands in U22 and bytes[10] in U10.  Relay k of 1..80 is therefore in byte
 * 10 - (k-1)/8, and K101..K103 are bits 0..2 of byte 0. */
static int relay_byte(int k) { return (k >= 101) ? 0 : 10 - (k - 1) / 8; }
static int relay_bit(int k)  { return (k >= 101) ? (k - 101) : ((k - 1) % 8); }

static void relay_set(int k, int on)
{
    int b = relay_byte(k), m = 1 << relay_bit(k);
    if (on) chain[b] |= (uint8_t)m;
    else    chain[b] &= (uint8_t)~m;
}

static int relay_get(int k)
{
    return (chain[relay_byte(k)] >> relay_bit(k)) & 1;
}

static void chain_push(void)
{
    hal_sr_write(chain, CHAIN_BYTES);
    hal_sleep_ms(RELAY_SETTLE_MS);
}

static int channel_relay(int n, int mode)
{
    switch (mode) {
    case M_SRC:   return 5 * n - 4;
    case M_RA:    return 5 * n - 3;
    case M_RB:    return 5 * n - 2;
    case M_RC:    return 5 * n - 1;
    case M_SHORT: return 5 * n;
    default:      return 0;
    }
}

static void channel_open(int n)
{
    int i;
    for (i = 5 * n - 4; i <= 5 * n; i++) relay_set(i, 0);
}

/* ------------------------------------------------------------------ safe state ------ */
void fx_role_safe(void)
{
    int n;
    memset(chain, 0, sizeof chain);
    hal_sr_write(chain, CHAIN_BYTES);
    hal_gpio_set(FX_OUT_MUX_PULL, 0);
    for (n = 0; n <= CHANNELS; n++) ch_mode[n] = M_OPEN;
    src_sel = SRC_OFF;
    pol_b = 0;
    selftest_armed = 0;
}

void fx_role_init(void)
{
    col_ready = 0;
    col_gain = 1;                     /* 4x; recorded at calibration, section 1.7        */
    fx_role_safe();
}

void fx_role_state(void)
{
    char buf[FX_REPLY_MAX];
    int n;
    size_t used = 0;
    buf[0] = '\0';
    for (n = 1; n <= CHANNELS; n++) {
        int w = snprintf(buf + used, sizeof buf - used, "%s%s",
                         n == 1 ? "" : ",", mode_name[ch_mode[n]]);
        if (w < 0 || (size_t)w >= sizeof buf - used) break;
        used += (size_t)w;
    }
    fx_info("channels %s", buf);
    fx_info("src=%s pol=%s selftest=%s colorimeter=%s gain=%d",
            src_name[src_sel], pol_b ? "B" : "A",
            selftest_armed ? "ARMED" : "disarmed",
            col_ready ? "ready" : "not initialised", col_gain);
}

/* ------------------------------------------------------------------ verbs ----------- */
static int parse_mode(const char *s, int *mode)
{
    int i;
    for (i = 0; i < M_MODES; i++)
        if (strcmp(s, mode_name[i]) == 0) { *mode = i; return FX_OK; }
    for (i = 0; i < (int)(sizeof alias_name / sizeof alias_name[0]); i++)
        if (strcmp(s, alias_name[i]) == 0) { *mode = alias_mode[i]; return FX_OK; }
    fx_detail("%s is not a channel mode "
              "(OPEN SRC RA RB RC SHORT, or SIN CAL 4K99 10K0 49K9)", s);
    return FX_ERR_SYNTAX;
}

/* SIN and CAL name a source as well as a mode, so a channel command that uses one of them
 * also commands K103.  That is convenient and it is also a hidden side effect, so it is
 * reported in the reply rather than done quietly. */
static int mode_implies_src(const char *s)
{
    if (strcmp(s, "SIN") == 0) return SRC_SIN;
    if (strcmp(s, "CAL") == 0) return SRC_CAL;
    return -1;
}

static void apply_src(int sel)
{
    src_sel = sel;
    relay_set(103, sel == SRC_CAL);   /* K103 energised selects CAL, released selects SIN */
}

static int cmd_ch(int argc, char **argv)
{
    long n;
    int mode, rc, implied;
    rc = fx_arg_int(argv[0], 1, CHANNELS, &n);
    if (rc != FX_OK) return rc;
    if (argc == 1) {
        fx_reply("OK CH ch=%ld mode=%s", n, mode_name[ch_mode[n]]);
        return FX_OK;
    }
    rc = parse_mode(argv[1], &mode);
    if (rc != FX_OK) return rc;

    /* Channel 11 is the BIAS output, not an input: section 1.5 permits OPEN and SHORT and
     * nothing else, because driving it fights the ADS1299 bias amplifier. */
    if (n == 11 && mode != M_OPEN && mode != M_SHORT) {
        fx_detail("channel 11 is the BIAS_EL output; only OPEN and SHORT are allowed "
                  "(JIG-EEG-009 section 1.5)");
        return FX_ERR_RANGE;
    }

    implied = mode_implies_src(argv[1]);
    channel_open(n);
    chain_push();                                     /* break */
    if (implied >= 0) apply_src(implied);
    if (mode != M_OPEN) relay_set(channel_relay((int)n, mode), 1);
    chain_push();                                     /* then make */
    ch_mode[n] = mode;
    fx_reply("OK CH ch=%ld mode=%s src=%s", n, mode_name[mode], src_name[src_sel]);
    return FX_OK;
}

static int cmd_chall(int argc, char **argv)
{
    int mode, rc, n, implied;
    (void)argc;
    rc = parse_mode(argv[0], &mode);
    if (rc != FX_OK) return rc;
    if (mode != M_OPEN && mode != M_SHORT && mode != M_SRC &&
        mode != M_RA && mode != M_RB && mode != M_RC) {
        fx_detail("unreachable mode");
        return FX_ERR_RANGE;
    }
    implied = mode_implies_src(argv[0]);
    for (n = 1; n <= CHANNELS; n++) channel_open(n);
    chain_push();
    if (implied >= 0) apply_src(implied);
    for (n = 1; n <= CHANNELS; n++) {
        int m = mode;
        if (n == 11 && m != M_OPEN && m != M_SHORT) m = M_OPEN;   /* section 1.5 */
        if (m != M_OPEN) relay_set(channel_relay(n, m), 1);
        ch_mode[n] = m;
    }
    chain_push();
    /* One reply, and it says what happened to channel 11, because the operator asked for
     * sixteen channels and got fifteen plus a stated exception. */
    fx_reply("OK CHALL mode=%s src=%s ch11=%s settle_ms=%d",
             mode_name[mode], src_name[src_sel], mode_name[ch_mode[11]],
             2 * RELAY_SETTLE_MS);
    return FX_OK;
}

static int cmd_src(int argc, char **argv)
{
    int sel, rc;
    if (argc == 0) {
        fx_reply("OK SRC sel=%s", src_name[src_sel]);
        return FX_OK;
    }
    rc = fx_arg_keyword(argv[0], src_name, 3, &sel);
    if (rc != FX_OK) return rc;
    apply_src(sel);
    chain_push();
    fx_reply("OK SRC sel=%s", src_name[src_sel]);
    return FX_OK;
}

static int cmd_pol(int argc, char **argv)
{
    static const char *const pol[] = { "A", "B" };
    int sel, rc;
    if (argc == 0) {
        fx_reply("OK POL pol=%s", pol_b ? "B" : "A");
        return FX_OK;
    }
    rc = fx_arg_keyword(argv[0], pol, 2, &sel);
    if (rc != FX_OK) return rc;
    /* K101 and K102 are one commutator and are always driven together.  Driving them
     * separately reverses one side of the pair only, which shorts the reference through
     * the ratio network. */
    relay_set(101, sel);
    relay_set(102, sel);
    pol_b = sel;
    chain_push();
    fx_reply("OK POL pol=%s dwell_note=host owns the 5 s dwell (section 1.2)", pol[sel]);
    return FX_OK;
}

static int cmd_rly(int argc, char **argv)
{
    long k, v;
    int rc;
    rc = fx_arg_int(argv[0], 1, 103, &k);
    if (rc != FX_OK) return rc;
    if (k > 80 && k < 101) {
        fx_detail("relays 81..100 do not exist; K1-K80 then K101-K103");
        return FX_ERR_RANGE;
    }
    if (argc == 1) {
        fx_reply("OK RLY k=%ld on=%d", k, relay_get((int)k));
        return FX_OK;
    }
    rc = fx_arg_int(argv[1], 0, 1, &v);
    if (rc != FX_OK) return rc;
    relay_set((int)k, (int)v);
    chain_push();
    /* A raw relay command leaves the cached channel mode meaningless, so it is invalidated
     * rather than left to be read back as a fact. */
    if (k <= 80) ch_mode[(k - 1) / 5 + 1] = M_OPEN;
    fx_reply("OK RLY k=%ld on=%ld raw=1", k, v);
    return FX_OK;
}

static int cmd_rlymask(int argc, char **argv)
{
    uint8_t b[CHAIN_BYTES];
    int rc, n;
    if (argc == 0) {
        char hex[2 * CHAIN_BYTES + 1];
        for (n = 0; n < CHAIN_BYTES; n++) snprintf(hex + 2 * n, 3, "%02X", chain[n]);
        fx_reply("OK RLYMASK mask=%s", hex);
        return FX_OK;
    }
    rc = fx_arg_hex(argv[0], b, CHAIN_BYTES);
    if (rc != FX_OK) return rc;
    if (b[0] & 0xF8) {
        fx_detail("bits 3..7 of the first byte are spare outputs and must be zero");
        return FX_ERR_RANGE;
    }
    memcpy(chain, b, CHAIN_BYTES);
    hal_sr_write(chain, CHAIN_BYTES);
    hal_sleep_ms(RELAY_SETTLE_MS);
    for (n = 1; n <= CHANNELS; n++) ch_mode[n] = M_OPEN;
    fx_reply("OK RLYMASK mask=%s raw=1 make_before_break=1", argv[0]);
    return FX_OK;
}

/* ------------------------------------------------------------------ readback -------- */
/* The arithmetic of JIG-EEG-009 section 8.4, computed rather than tabulated so that a
 * change to a reference value cannot leave a stale expectation behind. */
static long expect_mv(int mode)
{
    switch (mode) {
    case M_OPEN:  return PULL_MV;
    case M_SHORT: return 0;
    case M_RA:    return PULL_MV * REF_RA_OHM / (REF_RA_OHM + PULL_OHM);
    case M_RB:    return PULL_MV * REF_RB_OHM / (REF_RB_OHM + PULL_OHM);
    case M_RC:    return PULL_MV * REF_RC_OHM / (REF_RC_OHM + PULL_OHM);
    case M_SRC:   return PULL_MV * SRC_ZO_OHM / (SRC_ZO_OHM + PULL_OHM);
    default:      return -1;
    }
}

static int cmd_selftest(int argc, char **argv)
{
    static const char *const sub[] = { "ARM", "DISARM", "RELAYS" };
    int which, rc, n, m;
    (void)argc;
    rc = fx_arg_keyword(argv[0], sub, 3, &which);
    if (rc != FX_OK) return rc;

    if (which == 0) {
        fx_role_safe();
        selftest_armed = 1;
        selftest_armed_us = hal_now_us();
        fx_info("SELFTEST ARM enables the readback pull-up on the mux common.");
        fx_info("The fixture must be UNMATED: with a unit fitted, RP1 drives 3.3 V through");
        fx_info("10 kOhm into a protected input. Disarms itself after 300 s.");
        fx_reply("OK SELFTEST arm=1 timeout_s=300");
        return FX_OK;
    }
    if (which == 1) {
        selftest_armed = 0;
        hal_gpio_set(FX_OUT_MUX_PULL, 0);
        fx_reply("OK SELFTEST arm=0");
        return FX_OK;
    }

    if (!selftest_armed) {
        fx_detail("send SELFTEST ARM first, with the fixture unmated");
        return FX_ERR_STATE;
    }
    fx_role_safe();
    selftest_armed = 1;
    hal_gpio_set(FX_OUT_MUX_PULL, 1);
    /* One channel at a time, one relay at a time.  The mux reads the relay-common node, so
     * RS(n) is outside the measurement and its 100 Ohm does not appear in the result. */
    for (n = 1; n <= CHANNELS; n++) {
        hal_mux_select(n - 1);
        for (m = M_OPEN; m < M_MODES; m++) {
            int mv;
            channel_open(n);
            if (m != M_OPEN) relay_set(channel_relay(n, m), 1);
            hal_sr_write(chain, CHAIN_BYTES);
            hal_sleep_ms(RELAY_SETTLE_MS);
            mv = hal_adc_mv(64);      /* 64 conversions; see section 8.4 on resolution */
            if (mv < 0) {
                hal_gpio_set(FX_OUT_MUX_PULL, 0);
                fx_role_safe();
                fx_detail("ADC read failed on channel %d", n);
                return FX_ERR_HARDWARE;
            }
            fx_info("RLYREAD ch=%d mode=%-5s k=%d mv=%d nominal_mv=%ld",
                    n, mode_name[m], channel_relay(n, m), mv, expect_mv(m));
        }
        channel_open(n);
    }
    hal_sr_write(chain, CHAIN_BYTES);
    hal_gpio_set(FX_OUT_MUX_PULL, 0);
    fx_role_safe();
    selftest_armed = 0;
    /* The limits are not applied here.  Section 1.12 step 2 measures each relay against
     * ITS OWN recorded value, and the recorded values live in the fixture calibration
     * record on the host, not in this firmware. */
    fx_reply("OK SELFTEST relays=%d readings=%d limits=host",
             CHANNELS * (M_MODES - 1), CHANNELS * M_MODES);
    return FX_OK;
}

/* ------------------------------------------------------------------ FIX-01/E -------- */
static int tcs_w8(uint8_t reg, uint8_t val)
{
    uint8_t b[2];
    b[0] = (uint8_t)(TCS_CMD | reg);
    b[1] = val;
    return hal_i2c_write(TCS_ADDR, b, 2);
}

static int cmd_col(int argc, char **argv)
{
    static const char *const sub[] = { "INIT", "READ", "GAIN" };
    int which, rc;
    uint8_t buf[8];

    rc = fx_arg_keyword(argv[0], sub, 3, &which);
    if (rc != FX_OK) return rc;

    if (which == 0) {
        if (hal_i2c_read(TCS_ADDR, (uint8_t)(TCS_CMD | TCS_ID), buf, 1) != 0) {
            fx_detail("no acknowledgement from 0x%02X", TCS_ADDR);
            return FX_ERR_HARDWARE;
        }
        if (buf[0] != TCS_ID_34725) {
            fx_detail("device at 0x%02X reports ID 0x%02X, not the TCS34725's 0x%02X",
                      TCS_ADDR, buf[0], TCS_ID_34725);
            return FX_ERR_HARDWARE;
        }
        if (tcs_w8(TCS_ATIME, TCS_ATIME_300MS) != 0 ||
            tcs_w8(TCS_CONTROL, (uint8_t)col_gain) != 0 ||
            tcs_w8(TCS_ENABLE, TCS_EN_PON) != 0) {
            fx_detail("write failed during initialisation");
            return FX_ERR_HARDWARE;
        }
        hal_sleep_ms(3);                     /* PON to AEN, datasheet minimum 2.4 ms */
        if (tcs_w8(TCS_ENABLE, (uint8_t)(TCS_EN_PON | TCS_EN_AEN)) != 0) {
            fx_detail("could not enable the ADC");
            return FX_ERR_HARDWARE;
        }
        col_ready = 1;
        fx_reply("OK COL init=1 integ_ms=%d atime=%d gain_code=%d",
                 TCS_INTEG_MS, TCS_ATIME_300MS, col_gain);
        return FX_OK;
    }

    if (which == 2) {
        long g;
        if (argc < 2) {
            fx_reply("OK COL gain_code=%d", col_gain);
            return FX_OK;
        }
        rc = fx_arg_int(argv[1], 0, 3, &g);
        if (rc != FX_OK) return rc;
        col_gain = (int)g;
        if (col_ready && tcs_w8(TCS_CONTROL, (uint8_t)col_gain) != 0) {
            fx_detail("could not write the gain register");
            return FX_ERR_HARDWARE;
        }
        /* The gain is fixed and recorded at calibration (section 1.7).  Changing it
         * invalidates the recorded green and red ratios, so the reply says so. */
        fx_reply("OK COL gain_code=%d note=recalibrate FIX-01/E after a gain change",
                 col_gain);
        return FX_OK;
    }

    if (!col_ready) {
        fx_detail("send COL INIT first");
        return FX_ERR_STATE;
    }
    hal_sleep_ms(TCS_INTEG_MS + 10);
    if (hal_i2c_read(TCS_ADDR, (uint8_t)(TCS_CMD | TCS_CDATAL), buf, 8) != 0) {
        fx_detail("read of the four data registers failed");
        return FX_ERR_HARDWARE;
    }
    {
        unsigned c = (unsigned)buf[0] | ((unsigned)buf[1] << 8);
        unsigned r = (unsigned)buf[2] | ((unsigned)buf[3] << 8);
        unsigned g = (unsigned)buf[4] | ((unsigned)buf[5] << 8);
        unsigned b = (unsigned)buf[6] | ((unsigned)buf[7] << 8);
        /* R/G is reported as an integer per thousand.  The firmware does no floating
         * point and applies no limit: TST-EEG-004 T11 owns the 0.30 / 3.0 / 0.6-1.7 bands
         * and the host tool applies them against the values recorded at calibration. */
        unsigned rg = g ? (unsigned)((r * 1000ul + g / 2) / g) : 0u;
        fx_reply("OK COL c=%u r=%u g=%u b=%u rg_per_mille=%s%u integ_ms=%d gain_code=%d",
                 c, r, g, b, g ? "" : "inf:", rg, TCS_INTEG_MS, col_gain);
    }
    return FX_OK;
}

/* ------------------------------------------------------------------ table ----------- */
const struct fx_command fx_commands[] = {
    { "CH",       cmd_ch,       1, 2, "CH <1-16> [OPEN|SRC|RA|RB|RC|SHORT|SIN|CAL|4K99|10K0|49K9]" },
    { "CHALL",    cmd_chall,    1, 1, "CHALL <mode> -- all sixteen on one latch edge (T7)" },
    { "SRC",      cmd_src,      0, 1, "SRC [OFF|SIN|CAL] -- K103 source select" },
    { "POL",      cmd_pol,      0, 1, "POL [A|B] -- K101/K102 polarity commutator" },
    { "RLY",      cmd_rly,      1, 2, "RLY <1-80|101-103> [0|1] -- raw relay, fault-finding" },
    { "RLYMASK",  cmd_rlymask,  0, 1, "RLYMASK [22 hex digits] -- raw chain, no interlock" },
    { "SELFTEST", cmd_selftest, 1, 1, "SELFTEST ARM|RELAYS|DISARM -- section 1.12 step 2" },
    { "COL",      cmd_col,      1, 2, "COL INIT|READ|GAIN [0-3] -- FIX-01/E colorimeter" },
    { NULL, NULL, 0, 0, NULL }
};

/* Housekeeping the engine calls once per main-loop pass. */
void fx_role_poll(void)
{
    if (selftest_armed && hal_now_us() - selftest_armed_us > ARM_TIMEOUT_US) {
        selftest_armed = 0;
        hal_gpio_set(FX_OUT_MUX_PULL, 0);
        fx_info("SELFTEST disarmed on its 300 s timeout");
    }
}
