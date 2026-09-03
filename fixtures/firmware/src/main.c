/*
 * main.c -- entry point for the three EEG-kit fixture controllers.
 *
 * There is nothing in here but the loop, on purpose: everything a reviewer has to check
 * lives either in fixproto.c (the protocol) or in a role file (what the fixture does).
 *
 * Written by hand.  Part of package_v2.3, TI One Voice research programme.
 * Licence: CC BY-SA 4.0.
 */
#include "fixproto.h"
#include "fixhal.h"

#ifndef FIX_MAIN_IS_TEST        /* the host test provides its own main() */
int main(void)
{
    int c;
    hal_init();
    fx_boot();
    for (;;) {
        while ((c = hal_getchar()) >= 0)
            fx_feed(c);
        fx_poll();
    }
}
#endif
