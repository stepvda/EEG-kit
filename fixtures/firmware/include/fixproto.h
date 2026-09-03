/*
 * fixproto.h -- FIXPROTO v1, the host-to-fixture line protocol of JIG-EEG-009 section 8.
 *
 * One request line, one response line, always, in order, with no unsolicited traffic after
 * the boot banner.  ASCII, because the two things a fixture line has to survive are an
 * operator with a terminal emulator and a test engineer reading a log six months later,
 * and neither is helped by a binary envelope.  The DUT's own protocol is binary and framed
 * (FW-EEG-001 section 6) because it carries a 50.7 kB/s sample stream; a fixture carries
 * relay commands at a few per second and has nothing to gain from the same machinery.
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#ifndef FIXPROTO_H
#define FIXPROTO_H

#include <stddef.h>
#include <stdint.h>

#define FX_PROTO_VERSION 1
#define FX_FW_VERSION    "1.0.0"

/* A line longer than this is answered ERR 2 LINE_TOO_LONG and the rest of it is discarded
 * up to the next newline, so a truncated line can never be executed as a short one. */
#define FX_LINE_MAX   160
#define FX_ARGS_MAX    12
#define FX_REPLY_MAX  240

/* Status codes.  Deliberately the same shape as FW-EEG-001 section 6.2's list -- one
 * numeric code, one fixed keyword, one free-text tail -- so an operator moving between the
 * DUT log and a fixture log reads the same kind of line. */
enum fx_status {
    FX_OK               = 0,
    FX_ERR_UNKNOWN_VERB = 1,
    FX_ERR_SYNTAX       = 2,
    FX_ERR_RANGE        = 3,
    FX_ERR_STATE        = 4,
    FX_ERR_INTERLOCK    = 5,
    FX_ERR_HARDWARE     = 7,
    FX_ERR_TIMEOUT      = 10,
    FX_ERR_UNSUPPORTED  = 11    /* the verb exists in this protocol, not in this role */
};

const char *fx_status_keyword(int status);

/* A command handler.  argc/argv exclude the verb itself.  Return an fx_status; anything
 * non-zero is turned into "ERR <VERB> <code> <keyword> <detail>" using the detail the
 * handler left in fx_detail().  A handler that has already produced its own OK line by
 * calling fx_reply() returns FX_OK and the dispatcher emits nothing further. */
typedef int (*fx_handler)(int argc, char **argv);

struct fx_command {
    const char *verb;
    fx_handler  fn;
    int         argc_min;
    int         argc_max;
    const char *help;
};

/* Implemented by the role file (fix_m1.c, fix_m2.c, fix_m3.c). */
extern const struct fx_command fx_commands[];
extern const char *const fx_role_name;      /* "M1" | "M2" | "M3" */
extern const char *const fx_fixture_name;   /* "FIX-01" | "FIX-02" | "FIX-04" */
void fx_role_init(void);                    /* leaves the fixture in its safe state */
void fx_role_safe(void);                    /* called by RESET and by the watchdog */
void fx_role_state(void);                   /* prints the role's STATE lines */
void fx_role_poll(void);                    /* role housekeeping, once per loop pass */

/* Called by handlers. */
void fx_reply(const char *fmt, ...);        /* one whole line, no newline in fmt */
void fx_info(const char *fmt, ...);         /* a "# ..." line: never a response */
void fx_detail(const char *fmt, ...);       /* the free-text tail of the next ERR */

/* Argument helpers.  Each returns 0 on success and leaves a detail on failure. */
int fx_arg_int(const char *s, long lo, long hi, long *out);
int fx_arg_hex(const char *s, uint8_t *out, int nbytes);   /* exactly 2*nbytes digits */
int fx_arg_keyword(const char *s, const char *const *table, int n, int *out);

/* The engine. */
void fx_boot(void);                          /* banner, role init */
void fx_feed(int ch);                        /* one received character */
void fx_poll(void);                          /* watchdog and any role housekeeping */
uint32_t fx_error_count(void);

/* Comms watchdog.  OFF by default and it matters that it is: TST-EEG-004 T7 leaves the
 * relay matrix driving all sixteen channels for fourteen unattended minutes
 * (JIG-EEG-009 section 1.1), and a fixture that drops its relays because the host went
 * quiet would abort exactly the step it exists to serve.  A host that wants the fixture to
 * fail safe on a lost link arms it explicitly, for the step that wants it. */
void fx_watchdog_set(uint32_t seconds);      /* 0 = off */
uint32_t fx_watchdog_get(void);

#endif /* FIXPROTO_H */
