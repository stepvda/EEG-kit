/*
 * host_test.c -- drives the real fixture firmware against hal_sim.c on a workstation.
 *
 * What it proves: that the command layer of M1, M2 and M3 does what JIG-EEG-009 section 8
 * says it does -- including the two things a reviewer cannot see by reading, that a
 * channel mode change breaks before it makes, and that a switching command is refused
 * while HV is armed.  What it does not prove is in the firmware README: no pin number, no
 * peripheral setup and no timing here has met hardware.
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#define FIX_MAIN_IS_TEST 1
#include "fixproto.h"
#include "fixhal.h"

#include <stdio.h>
#include <string.h>

/* hal_sim.c */
const char *sim_output(void);
void        sim_clear(void);
int         sim_latches(void);
int         sim_relay(int k);
int         sim_scan_relay(int c);
void        sim_set_lid(int closed);
void        sim_tcs_present(int yes);
int         sim_gpio_out(enum fx_gpio which);

static int checks, fails;

static void send(const char *s)
{
    const char *p;
    sim_clear();
    for (p = s; *p; p++) fx_feed(*p);
    fx_feed('\n');
}

static void want(const char *what, const char *needle)
{
    checks++;
    if (!strstr(sim_output(), needle)) {
        fails++;
        printf("  FAIL %s\n        wanted: %s\n        got:    %s",
               what, needle, sim_output());
    }
}

static void want_not(const char *what, const char *needle)
{
    checks++;
    if (strstr(sim_output(), needle)) {
        fails++;
        printf("  FAIL %s\n        did not want: %s\n        got: %s",
               what, needle, sim_output());
    }
}

static void want_int(const char *what, int got, int expect)
{
    checks++;
    if (got != expect) {
        fails++;
        printf("  FAIL %s: got %d, expected %d\n", what, got, expect);
    }
}

/* ------------------------------------------------------------------ common ---------- */
static void test_common(void)
{
    send("ID");
    want("ID names the role", fx_role_name);
    want("ID carries the protocol version", "proto=1");

    send("id");
    want("verbs are case-insensitive", "OK ID");

    send("ECHO the quick brown fox");
    want("ECHO returns its arguments", "OK ECHO THE QUICK BROWN FOX");

    send("NOSUCHVERB");
    want("an unknown verb is answered, not ignored", "ERR NOSUCHVERB 1 UNKNOWN_VERB");

    send("");
    want_int("a blank line produces no response", (int)strlen(sim_output()), 0);

    send("# a comment line from a script");
    want_int("a comment produces no response", (int)strlen(sim_output()), 0);

    {   /* A line longer than FX_LINE_MAX must be refused whole, never executed short. */
        char big[FX_LINE_MAX + 40];
        memset(big, 'A', sizeof big - 1);
        big[sizeof big - 1] = '\0';
        memcpy(big, "ECHO ", 5);
        send(big);
        want("an over-long line is refused", "ERR ? 2 SYNTAX");
        want_not("and is not executed", "OK ECHO");
    }

    send("WDT");
    want("the watchdog is off at boot", "OK WDT seconds=0");
    send("WDT 5");
    want("the watchdog can be armed", "OK WDT seconds=5");
    send("WDT OFF");
    want("and disarmed", "OK WDT seconds=0");

    send("STATE");
    want("STATE answers with one OK line", "OK STATE");
    send("HELP");
    want("HELP ends with one OK line", "OK HELP");
}

/* ------------------------------------------------------------------ M1 ------------- */
static void test_m1(void)
{
    int before, after, n;

    send("RESET");
    want("reset acknowledges", "OK RESET");
    want_int("reset opens every channel relay", sim_relay(1) + sim_relay(2) +
             sim_relay(3) + sim_relay(4) + sim_relay(5), 0);

    send("CH 1 RB");
    want("a channel takes a mode", "OK CH ch=1 mode=RB");
    want_int("K3 is the RB relay of channel 1", sim_relay(3), 1);
    want_int("and nothing else on channel 1 is closed",
             sim_relay(1) + sim_relay(2) + sim_relay(4) + sim_relay(5), 0);

    /* Break before make: two latch events per mode change, and the first one is the
     * all-open pattern.  Counting latches is the only way to see it from outside. */
    before = sim_latches();
    send("CH 1 RC");
    after = sim_latches();
    want_int("a mode change is two latch events", after - before, 2);
    want_int("the new position is closed", sim_relay(4), 1);
    want_int("the old position is open", sim_relay(3), 0);

    send("CH 1 SIN");
    want("SIN is accepted as a mode name", "mode=SRC");
    want("and it commands the source too", "src=SIN");
    send("CH 2 CAL");
    want("CAL selects the reference source", "src=CAL");
    want_int("K103 is energised for CAL", sim_relay(103), 1);
    send("CH 3 4K99");
    want("the document's own reference names work", "mode=RA");

    send("CH 11 RB");
    want("channel 11 refuses to be driven", "ERR CH 3 RANGE");
    want("and says why", "BIAS_EL");
    send("CH 11 SHORT");
    want("channel 11 accepts SHORT", "OK CH ch=11 mode=SHORT");

    send("CH 17 OPEN");
    want("there is no channel 17", "ERR CH 3 RANGE");
    send("CH 1 SIDEWAYS");
    want("an unknown mode is a syntax error", "ERR CH 2 SYNTAX");

    send("CHALL SHORT");
    want("CHALL answers once", "OK CHALL mode=SHORT");
    for (n = 1; n <= 16; n++)
        want_int("every channel is shorted", sim_relay(5 * n), 1);
    send("CHALL RB");
    want("CHALL reports what happened to channel 11", "ch11=OPEN");
    want_int("channel 11 is not driven by CHALL", sim_relay(5 * 11 - 2), 0);
    want_int("channel 12 is", sim_relay(5 * 12 - 2), 1);

    send("POL B");
    want_int("the commutator moves as a pair, K101", sim_relay(101), 1);
    want_int("and K102", sim_relay(102), 1);

    send("RLY 90 1");
    want("relays 81 to 100 do not exist", "ERR RLY 3 RANGE");
    send("RLYMASK F80000000000000000000000");
    want("a 24-digit mask is the wrong length", "ERR RLYMASK 2 SYNTAX");
    send("RLYMASK F8000000000000000000FF");
    want("the spare outputs must be zero", "ERR RLYMASK 3 RANGE");

    /* The readback.  Refused until armed, because armed is when RP1 is switched on. */
    send("SELFTEST RELAYS");
    want("the readback is refused unarmed", "ERR SELFTEST 4 STATE");
    send("SELFTEST ARM");
    want("arming warns about the pull-up", "must be UNMATED");
    want_int("but does not switch it on yet", sim_gpio_out(FX_OUT_MUX_PULL), 0);

    send("SELFTEST RELAYS");
    want("the sweep completes", "OK SELFTEST relays=80 readings=96");
    want_int("and leaves the pull-up off", sim_gpio_out(FX_OUT_MUX_PULL), 0);
    /* The four numbers the design turns on, read back through the model of section 8.4. */
    want("OPEN reads the pull-up rail",   "mode=OPEN  k=0 mv=3300 nominal_mv=3300");
    want("SRC reads the divider source",  "mode=SRC   k=1 mv=5 nominal_mv=5");
    want("RA reads 4k99",                 "mode=RA    k=2 mv=1098 nominal_mv=1098");
    want("RB reads 10k0",                 "mode=RB    k=3 mv=1650 nominal_mv=1650");
    want("RC reads 49k9",                 "mode=RC    k=4 mv=2749 nominal_mv=2749");
    want("SHORT reads zero",              "mode=SHORT k=5 mv=0 nominal_mv=0");
    want("channel 16 is swept too",       "ch=16 mode=RC");

    /* FIX-01/E. */
    send("COL READ");
    want("the colorimeter must be initialised first", "ERR COL 4 STATE");
    send("COL INIT");
    want("initialisation reports the 300 ms integration", "integ_ms=300 atime=131");
    send("COL READ");
    want("a read returns all four channels", "OK COL c=2000 r=1200 g=400 b=300");
    want("and the ratio in per mille", "rg_per_mille=3000");
    sim_tcs_present(0);
    send("COL INIT");
    want("a missing sensor is a hardware error, not a reading", "ERR COL 7 HARDWARE");
    sim_tcs_present(1);
}

/* ------------------------------------------------------------------ M2 ------------- */
static void test_m2(void)
{
    send("RESET");
    send("TONE 1000 -200 100");
    want("a tone needs a coupler selected", "ERR TONE 4 STATE");

    send("DRV A");
    want("a driver can be selected", "OK DRV sel=A");
    want_int("and only that one is enabled", sim_gpio_out(FX_OUT_DRV_A), 1);
    want_int("never both", sim_gpio_out(FX_OUT_DRV_B), 0);
    want_int("with the amplifier on", sim_gpio_out(FX_OUT_AMP_EN), 1);

    send("TONE 30000 -200 100");
    want("30 kHz is out of range", "ERR TONE 3 RANGE");
    send("TONE 1000 200 100");
    want("a positive level is out of range", "ERR TONE 3 RANGE");

    send("TONE 1000 -200 50");
    want("a tone reports its own t0", "OK TONE hz=1000 level_tenths_db=-200 ms=50");
    send("TONE STOP");
    want("and can be stopped", "OK TONE stopped=1");

    send("BURST 1000 -200 50");
    want("BURST finds the marker edge", "OK BURST hz=1000 ms=50");
    want("and says the edge was polled, not captured", "polled=1");

    send("MIC A");
    want("a reference microphone reads in millivolts", "OK MIC which=A mv=734");
    want("and leaves the sound pressure to the host", "spl=host");
    send("MIC C");
    want("there are two reference microphones", "ERR MIC 2 SYNTAX");

    send("MARK");
    want("the marker can be read on its own", "OK MARK level=");
}

/* ------------------------------------------------------------------ M3 ------------- */
static void test_m3(void)
{
    int c;

    send("RESET");
    send("SCAN 5");
    want("one channel goes to the instrument", "OK SCAN ch=5");
    want_int("channel 5 is energised", sim_scan_relay(5), 1);
    for (c = 1; c <= 24; c++)
        if (c != 5) want_int("every other channel is on the common bus",
                             sim_scan_relay(c), 0);

    send("SCAN 25");
    want("there are twenty-four channels", "ERR SCAN 3 RANGE");

    send("SCANMASK 000011");
    want("a mask sets several at once", "OK SCANMASK mask=000011 count=2");

    send("HV ARM");
    want("HV arms with the lid shut", "OK HV state=ARMED");
    send("SCAN 3");
    want("switching is refused while HV is armed", "ERR SCAN 5 INTERLOCK");
    send("SCANMASK 000001");
    want("and so is a mask", "ERR SCANMASK 5 INTERLOCK");

    send("HV SAFE");
    want("HV disarms", "OK HV state=SAFE");
    send("SCAN 3");
    want("but the discharge dwell still blocks switching", "ERR SCAN 5 INTERLOCK");
    hal_sleep_ms(6000);
    send("SCAN 3");
    want("and releases it after the dwell", "OK SCAN ch=3");

    sim_set_lid(0);
    send("HV ARM");
    want("HV will not arm with the lid open", "ERR HV 5 INTERLOCK");
    sim_set_lid(1);
    send("HV ARM");
    want("and will once it is shut again", "OK HV state=ARMED");
    sim_set_lid(0);
    fx_poll();
    want_int("opening the lid while armed drops every channel", sim_scan_relay(3), 0);
    send("HV");
    want("and disarms HV", "OK HV state=SAFE");
    sim_set_lid(1);
}

int main(void)
{
    hal_init();
    fx_boot();
    printf("FIXPROTO host test -- role %s (%s)\n", fx_role_name, fx_fixture_name);
    test_common();
    if (strcmp(fx_role_name, "M1") == 0) test_m1();
    if (strcmp(fx_role_name, "M2") == 0) test_m2();
    if (strcmp(fx_role_name, "M3") == 0) test_m3();
    printf("  %d checks, %d failures\n", checks, fails);
    return fails ? 1 : 0;
}
