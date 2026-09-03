/* Simulated powered-on device: the REAL firmware translation unit, driven over a
   simulated USB wire.  stdin = host->device bytes, stdout = device->host bytes. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int g_sim_vbus = 0;
static uint8_t  in_buf[65536]; static size_t in_len = 0, in_pos = 0;
static uint8_t  out_buf[262144]; static size_t out_len = 0;

uint32_t sim_cdc_avail(void){ return (uint32_t)(in_len - in_pos); }
uint32_t sim_cdc_read(void* d, uint32_t n){
    uint32_t a = (uint32_t)(in_len - in_pos); if (n > a) n = a;
    memcpy(d, in_buf + in_pos, n); in_pos += n; return n;
}
static uint8_t vnd_buf[262144]; static size_t vnd_len = 0;
static int s_vendor_up = 0;      /* the host under test speaks WebSerial = CDC only */
int sim_vendor_up(void){ return s_vendor_up; }
uint32_t sim_write_cdc(const void* d, uint32_t n){
    if (out_len + n > sizeof out_buf) n = (uint32_t)(sizeof out_buf - out_len);
    memcpy(out_buf + out_len, d, n); out_len += n; return n;
}
uint32_t sim_write_vnd(const void* d, uint32_t n){
    if (vnd_len + n > sizeof vnd_buf) n = (uint32_t)(sizeof vnd_buf - vnd_len);
    memcpy(vnd_buf + vnd_len, d, n); vnd_len += n; return n;
}
int64_t esp_timer_get_time(void){ static int64_t t = 0; t += 1000; return t; }

/* the device under test */
#include "main_under_test.c"

int main(int argc, char** argv){
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--vbus"))   g_sim_vbus = 1;
        if (!strcmp(argv[i], "--vendor")) s_vendor_up = 1;
    }
    in_len = fread(in_buf, 1, sizeof in_buf, stdin);
    /* one pass of the firmware's own receive loop over everything the host sent */
    for (size_t guard = 0; guard < 4 && in_pos < in_len; guard++) rx_poll();
    /* stdout is what a WebSerial host sees: the CDC endpoint only. */
    fwrite(out_buf, 1, out_len, stdout);
    if (getenv("SIM_DUMP_VENDOR")) fwrite(vnd_buf, 1, vnd_len, stderr);
    return 0;
}

/* Defined here, after main.c, so the board's own pin numbers are in scope. */
int sim_gpio_level(int pin){ return pin == PIN_VBUS_DET ? g_sim_vbus : 0; }
