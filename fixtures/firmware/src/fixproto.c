/*
 * fixproto.c -- the FIXPROTO v1 engine: line assembly, tokenising, dispatch, replies.
 *
 * Role-independent.  Every verb the three fixtures share lives here; the role files add
 * their own table and the dispatcher searches the common table first, so no role can
 * quietly redefine ID, RESET or STATE.
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#include "fixproto.h"
#include "fixhal.h"

#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* Set by the build.  BUILD_ID is the short hash of the source tree the image was built
 * from; the Makefile and the CMake build both pass it, and it is what the fixture
 * calibration record of JIG-EEG-009 section 5.2 pins for FIX-03.  A build that does not
 * pass one says so rather than pretending to a version. */
#ifndef FX_BUILD_ID
#define FX_BUILD_ID "unset"
#endif

static char     line[FX_LINE_MAX + 1];
static int      line_len;
static int      line_overflow;
static char     detail[FX_REPLY_MAX];
static uint32_t errors;
static uint32_t wdt_seconds;
static uint64_t last_command_us;
static int      wdt_tripped;

const char *fx_status_keyword(int status)
{
    switch (status) {
    case FX_OK:               return "OK";
    case FX_ERR_UNKNOWN_VERB: return "UNKNOWN_VERB";
    case FX_ERR_SYNTAX:       return "SYNTAX";
    case FX_ERR_RANGE:        return "RANGE";
    case FX_ERR_STATE:        return "STATE";
    case FX_ERR_INTERLOCK:    return "INTERLOCK";
    case FX_ERR_HARDWARE:     return "HARDWARE";
    case FX_ERR_TIMEOUT:      return "TIMEOUT";
    case FX_ERR_UNSUPPORTED:  return "UNSUPPORTED";
    default:                  return "ERROR";
    }
}

void fx_reply(const char *fmt, ...)
{
    char buf[FX_REPLY_MAX];
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(buf, sizeof buf, fmt, ap);
    va_end(ap);
    hal_putline(buf);
}

void fx_info(const char *fmt, ...)
{
    char buf[FX_REPLY_MAX];
    char out[FX_REPLY_MAX + 2];
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(buf, sizeof buf, fmt, ap);
    va_end(ap);
    snprintf(out, sizeof out, "# %s", buf);
    hal_putline(out);
}

void fx_detail(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(detail, sizeof detail, fmt, ap);
    va_end(ap);
}

/* ------------------------------------------------------------------ argument helpers */
int fx_arg_int(const char *s, long lo, long hi, long *out)
{
    char *end;
    long v;
    if (!s || !*s) {
        fx_detail("empty argument");
        return FX_ERR_SYNTAX;
    }
    v = strtol(s, &end, 0);
    if (*end != '\0') {
        fx_detail("%s is not an integer", s);
        return FX_ERR_SYNTAX;
    }
    if (v < lo || v > hi) {
        fx_detail("%ld outside %ld..%ld", v, lo, hi);
        return FX_ERR_RANGE;
    }
    *out = v;
    return FX_OK;
}

static int hexval(char c)
{
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}

int fx_arg_hex(const char *s, uint8_t *out, int nbytes)
{
    int i;
    if ((int)strlen(s) != nbytes * 2) {
        fx_detail("expected %d hex digits, got %d", nbytes * 2, (int)strlen(s));
        return FX_ERR_SYNTAX;
    }
    for (i = 0; i < nbytes; i++) {
        int hi = hexval(s[2 * i]), lo = hexval(s[2 * i + 1]);
        if (hi < 0 || lo < 0) {
            fx_detail("%s is not hexadecimal", s);
            return FX_ERR_SYNTAX;
        }
        out[i] = (uint8_t)((hi << 4) | lo);
    }
    return FX_OK;
}

int fx_arg_keyword(const char *s, const char *const *table, int n, int *out)
{
    int i;
    for (i = 0; i < n; i++) {
        if (strcmp(s, table[i]) == 0) {
            *out = i;
            return FX_OK;
        }
    }
    fx_detail("%s is not one of the accepted keywords", s);
    return FX_ERR_SYNTAX;
}

/* ------------------------------------------------------------------ common verbs ---- */
static int cmd_id(int argc, char **argv)
{
    (void)argc; (void)argv;
    fx_reply("OK ID role=%s fixture=%s proto=%d fw=%s build=%s uptime_ms=%lu",
             fx_role_name, fx_fixture_name, FX_PROTO_VERSION, FX_FW_VERSION,
             FX_BUILD_ID, (unsigned long)(hal_now_us() / 1000u));
    return FX_OK;
}

static int cmd_echo(int argc, char **argv)
{
    /* The link check.  It is here for the same reason FW-EEG-001 gives LOOPBACK its own
     * opcode: before anything is believed about a fixture, something has to prove the
     * cable and the framing.  Arguments are re-joined with single spaces, so the reply is
     * a canonical form of what was sent and not a byte copy of it. */
    char buf[FX_REPLY_MAX];
    int i;
    size_t n = 0;
    buf[0] = '\0';
    for (i = 0; i < argc; i++) {
        size_t need = strlen(argv[i]) + (i ? 1u : 0u);
        if (n + need >= sizeof buf) break;
        if (i) buf[n++] = ' ';
        strcpy(buf + n, argv[i]);
        n += strlen(argv[i]);
    }
    fx_reply("OK ECHO %s", buf);
    return FX_OK;
}

static int cmd_reset(int argc, char **argv)
{
    (void)argc; (void)argv;
    fx_role_safe();
    wdt_tripped = 0;
    fx_reply("OK RESET");
    return FX_OK;
}

static int cmd_state(int argc, char **argv)
{
    (void)argc; (void)argv;
    fx_role_state();                 /* the role prints its own "# ..." lines */
    fx_reply("OK STATE role=%s wdt_s=%lu wdt_tripped=%d errors=%lu",
             fx_role_name, (unsigned long)wdt_seconds, wdt_tripped,
             (unsigned long)errors);
    return FX_OK;
}

static int cmd_wdt(int argc, char **argv)
{
    long v;
    int rc;
    if (argc == 0) {
        fx_reply("OK WDT seconds=%lu tripped=%d", (unsigned long)wdt_seconds, wdt_tripped);
        return FX_OK;
    }
    if (strcmp(argv[0], "OFF") == 0) {
        wdt_seconds = 0;
        fx_reply("OK WDT seconds=0 tripped=%d", wdt_tripped);
        return FX_OK;
    }
    rc = fx_arg_int(argv[0], 1, 3600, &v);
    if (rc != FX_OK) return rc;
    wdt_seconds = (uint32_t)v;
    last_command_us = hal_now_us();
    fx_reply("OK WDT seconds=%lu tripped=%d", (unsigned long)wdt_seconds, wdt_tripped);
    return FX_OK;
}

static int cmd_errs(int argc, char **argv)
{
    (void)argc; (void)argv;
    fx_reply("OK ERRS count=%lu", (unsigned long)errors);
    return FX_OK;
}

static void help_table(const struct fx_command *t)
{
    int i;
    for (i = 0; t[i].verb; i++)
        fx_info("%-10s %s", t[i].verb, t[i].help);
}

static const struct fx_command fx_common[];

static int cmd_help(int argc, char **argv)
{
    (void)argc; (void)argv;
    fx_info("FIXPROTO v%d  %s / %s  fw %s  build %s",
            FX_PROTO_VERSION, fx_role_name, fx_fixture_name, FX_FW_VERSION, FX_BUILD_ID);
    fx_info("one request line, one response line: OK <VERB> ... or ERR <VERB> <n> <KEY> ...");
    help_table(fx_common);
    help_table(fx_commands);
    fx_reply("OK HELP");
    return FX_OK;
}

static const struct fx_command fx_common[] = {
    { "ID",    cmd_id,    0, 0,           "identity, protocol version, build and uptime" },
    { "ECHO",  cmd_echo,  0, FX_ARGS_MAX, "echo the arguments back -- the link check" },
    { "RESET", cmd_reset, 0, 0,           "return the fixture to its safe state" },
    { "STATE", cmd_state, 0, 0,           "dump the commanded state of the whole fixture" },
    { "WDT",   cmd_wdt,   0, 1,           "comms watchdog, seconds or OFF; OFF at boot" },
    { "ERRS",  cmd_errs,  0, 0,           "protocol errors counted since boot" },
    { "HELP",  cmd_help,  0, 0,           "this list" },
    { NULL, NULL, 0, 0, NULL }
};

/* ------------------------------------------------------------------ dispatch -------- */
static const struct fx_command *find(const struct fx_command *t, const char *verb)
{
    int i;
    for (i = 0; t[i].verb; i++)
        if (strcmp(t[i].verb, verb) == 0)
            return &t[i];
    return NULL;
}

static void fail(const char *verb, int status)
{
    errors++;
    if (detail[0])
        fx_reply("ERR %s %d %s %s", verb, status, fx_status_keyword(status), detail);
    else
        fx_reply("ERR %s %d %s", verb, status, fx_status_keyword(status));
}

static void execute(char *buf)
{
    char *argv[FX_ARGS_MAX + 1];
    int argc = 0, rc;
    char *p = buf;
    const struct fx_command *c;

    detail[0] = '\0';

    /* Tokenise on runs of spaces and tabs.  A line of only whitespace is not an error and
     * is not answered: an operator pressing return at a terminal has not asked anything. */
    while (*p) {
        while (*p == ' ' || *p == '\t') p++;
        if (!*p) break;
        if (argc > FX_ARGS_MAX) {
            errors++;
            fx_reply("ERR ? %d %s more than %d arguments",
                     FX_ERR_SYNTAX, fx_status_keyword(FX_ERR_SYNTAX), FX_ARGS_MAX);
            return;
        }
        argv[argc++] = p;
        while (*p && *p != ' ' && *p != '\t') {
            if (*p >= 'a' && *p <= 'z') *p = (char)(*p - 'a' + 'A');   /* case-insensitive */
            p++;
        }
        if (*p) *p++ = '\0';
    }
    if (argc == 0) return;
    if (argv[0][0] == '#') return;      /* a comment line from a script file */

    c = find(fx_common, argv[0]);
    if (!c) c = find(fx_commands, argv[0]);
    if (!c) {
        errors++;
        fx_reply("ERR %s %d %s try HELP", argv[0], FX_ERR_UNKNOWN_VERB,
                 fx_status_keyword(FX_ERR_UNKNOWN_VERB));
        return;
    }
    if (argc - 1 < c->argc_min || argc - 1 > c->argc_max) {
        fx_detail("%s takes %d to %d arguments, got %d",
                  c->verb, c->argc_min, c->argc_max, argc - 1);
        fail(c->verb, FX_ERR_SYNTAX);
        return;
    }

    last_command_us = hal_now_us();
    rc = c->fn(argc - 1, argv + 1);
    if (rc != FX_OK)
        fail(c->verb, rc);
}

void fx_feed(int ch)
{
    if (ch == '\r') return;
    if (ch == '\n') {
        if (line_overflow) {
            errors++;
            fx_reply("ERR ? %d %s line over %d characters, discarded",
                     FX_ERR_SYNTAX, fx_status_keyword(FX_ERR_SYNTAX), FX_LINE_MAX);
            line_overflow = 0;
            line_len = 0;
            return;
        }
        line[line_len] = '\0';
        execute(line);
        line_len = 0;
        return;
    }
    if (line_len >= FX_LINE_MAX) {
        line_overflow = 1;              /* keep eating until the newline */
        return;
    }
    line[line_len++] = (char)ch;
}

void fx_boot(void)
{
    line_len = 0;
    line_overflow = 0;
    errors = 0;
    wdt_seconds = 0;
    wdt_tripped = 0;
    detail[0] = '\0';
    fx_role_init();
    last_command_us = hal_now_us();
    fx_info("%s %s FIXPROTO v%d fw %s build %s -- JIG-EEG-009 section 8",
            fx_role_name, fx_fixture_name, FX_PROTO_VERSION, FX_FW_VERSION, FX_BUILD_ID);
    fx_info("safe state on reset: every relay open, no source connected. HELP lists verbs.");
}

void fx_poll(void)
{
    fx_role_poll();
    if (wdt_seconds == 0 || wdt_tripped) return;
    if (hal_now_us() - last_command_us > (uint64_t)wdt_seconds * 1000000u) {
        wdt_tripped = 1;
        fx_role_safe();
        /* Unsolicited, and the one exception to "no unsolicited traffic": it is prefixed
         * "# " like every other informational line, so a host matching responses by
         * arrival order is not confused by it. */
        fx_info("WATCHDOG %lus expired -- fixture returned to its safe state",
                (unsigned long)wdt_seconds);
    }
}

uint32_t fx_error_count(void) { return errors; }
void     fx_watchdog_set(uint32_t s) { wdt_seconds = s; last_command_us = hal_now_us(); }
uint32_t fx_watchdog_get(void) { return wdt_seconds; }
