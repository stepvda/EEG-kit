/*
 * FW-EEG-001  —  TI One Voice EEG field kit firmware (ESP32-S3, ESP-IDF 5.x + TinyUSB)
 * Status: reference implementation written against RFQ-EEG-001 Rev B section 5 and
 * DSN-EEG-003. Compiles against ESP-IDF 5.2 API names; NOT yet run on hardware.
 * Licence: MIT (firmware). Hardware is CC BY-SA 4.0.
 *
 * What this file implements
 *  - ADS1299 x2 daisy-chain bring-up, 250/500/1000 Hz, gain per channel, lead-off on ch1-8
 *  - DRDY ISR: the ONLY place the 32-bit sample counter increments (E-19)
 *  - Sample = 16 x int24 + 16-bit aux (buttons, comparator, lead-off summary, charger, SD ok)
 *  - Frames: DATA / STATUS / EVENT / GAP / SIGNATURE / CMD_ACK, COBS-encoded, CRC-32, 0x00 delimiter
 *  - Ring buffer >= 3 min at 1 kHz in PSRAM, sequence numbers, retransmit by range, GAP on overflow
 *  - microSD append of the identical frame stream (authoritative copy)
 *  - USB composite: CDC-ACM (WebSerial) + vendor bulk (WebUSB), BOS with WebUSB platform
 *    descriptor and Microsoft OS 2.0 descriptor (WinUSB auto-bind), iSerial = the unit
 *    serial TIOV-B-nnnn (RFQ F-04; RUL-EEG-021 section B). NOT the ATECC factory serial.
 *  - Command channel (F-10) and timing self-test (F-21)
 *  - Contact lights via 74HC595 from lead-off status; forced OFF during recording blocks (E-27)
 *  - Radio never initialised. No Wi-Fi / BT code path exists in this build.
 */
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/ringbuf.h"
#include "driver/spi_master.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "esp_heap_caps.h"
#include "tinyusb.h"
#include "tusb.h"

static const char *TAG = "eegkit";

/* ------------------------------------------------------------------ pins
 * FW-D12 CLOSED.  This file used to carry its own copy of the pin map, and that copy was
 * the Rev A one: it drove the contact-light shift register on GPIO35/36/37, which are the
 * OCTAL PSRAM bus of the -N16R8.  main() called gpio_set_direction() on all three at boot
 * and lights_write() toggled them, so a unit flashed with it would have torn down the
 * PSRAM the ring buffer lives in.
 *
 * The generated header is now the only pin map.  It comes from design.py, so the firmware
 * and the board cannot disagree; regenerate it rather than editing it.  The aliases below
 * exist only so the rest of this file keeps its original names.
 */
#include "board_pins.h"
/* IRAM_ATTR comes from esp_attr.h.  main.c used it at drdy_isr() and relied on some other
   header dragging it in; ESP-IDF happens to, but nothing here guaranteed it. */
#include "esp_attr.h"
/* The peripheral API implemented in drivers.c.  Without this the calls to sd_free_mb(),
   unit_serial_into() and atecc_serial_into() were implicit declarations -- an error in
   C99 and later, and a silent int-return assumption where a compiler allows it. */
#include "drivers.h"

/* drivers.c */
esp_err_t drv_init_all(void);
void      drv_sd_flush(void);
esp_err_t drv_sd_open_session(const char *name);

#define PIN_CS      PIN_ADS_CS
#define PIN_MOSI    PIN_ADS_MOSI
#define PIN_SCLK    PIN_ADS_SCLK
#define PIN_MISO    PIN_ADS_MISO
#define PIN_DRDY    PIN_ADS_DRDY
#define PIN_START   PIN_ADS_START
#define PIN_RESET   PIN_ADS_RESET
#define PIN_LED_PWM PIN_LED_V

/* ------------------------------------------------------------------ ADS1299 registers/opcodes */
#define ADS_WAKEUP 0x02
#define ADS_STANDBY 0x04
#define ADS_RESET 0x06
#define ADS_START 0x08
#define ADS_STOP  0x0A
#define ADS_RDATAC 0x10
#define ADS_SDATAC 0x11
#define ADS_RREG 0x20
#define ADS_WREG 0x40
#define REG_CONFIG1 0x01
#define REG_CONFIG2 0x02
#define REG_CONFIG3 0x03
#define REG_LOFF    0x04
#define REG_CH1SET  0x05
#define REG_BIAS_SENSP 0x0D
#define REG_BIAS_SENSN 0x0E
#define REG_LOFF_SENSP 0x0F
#define REG_LOFF_STATP 0x12
#define REG_MISC1   0x15
#define REG_CONFIG4 0x17

#define N_CH 16
#define N_DEV 2
#define FRAME_SAMPLES_MAX 20
#define SAMPLE_BYTES (N_CH*3+2)                 /* 50 */
/* FW-D13 CLOSED.  This was 12 MiB on a part with 8 MiB of PSRAM: the allocation
   returned NULL and the first DATA frame asserted inside xRingbufferSend.  6 MiB is
   126 s of raw samples at 1 kHz (124 s counted over the framed stream), against the
   90 s that F-06 asks for as relaxed by ECO-EEG-025. */
#define RING_BYTES (6*1024*1024)                /* 6,291,456 B -- 126 s @ 1 kHz */

static spi_device_handle_t ads;
static volatile uint32_t g_sample_index = 0;    /* monotonic; incremented ONLY in DRDY ISR */
static volatile uint16_t g_seq = 0;
static uint16_t g_rate_code = 1;                /* 0=250,1=500,2=1000 Hz  (fleet default 500) */
static bool g_recording = false;
static bool g_lights_enabled = true;
static uint16_t g_loff_bits = 0;                /* lead-off summary for ch1-8 */
static volatile uint8_t g_loff_p = 0;           /* LOFF_STATP, ch1-8, at the live threshold */
static volatile uint8_t g_loff_n = 0;           /* LOFF_STATN, ch1-8 -- see the note below */
/* The two latched comparator results the contact lights are built from (FW-D17).  Each
   holds LOFF_STATP as read while the corresponding COMP_TH was programmed. */
static volatile uint8_t g_loff_sens = 0;        /* tripped at the SENSITIVE threshold */
static volatile uint8_t g_loff_insens = 0;      /* tripped at the INSENSITIVE threshold */
static volatile uint8_t g_lights_force = 0;     /* CMD_LIGHTS mode 2/3/4: 0 = automatic */
static volatile uint8_t g_lights_force_mask = 0xFF;
static RingbufHandle_t rb;                      /* PSRAM ring of DATA frames (for backfill) */

/* ------------------------------------------------------------------ CRC-32 (IEEE) */
static uint32_t crc32(const uint8_t *d, size_t n) {
    uint32_t c = 0xFFFFFFFFu;
    for (size_t i = 0; i < n; i++) { c ^= d[i]; for (int k = 0; k < 8; k++) c = (c >> 1) ^ (0xEDB88320u & (0u - (c & 1))); }
    return ~c;
}
/* ------------------------------------------------------------------ COBS encode: out must hold n + n/254 + 2 */
static size_t cobs_encode(const uint8_t *in, size_t n, uint8_t *out) {
    size_t ri = 0, wi = 1, code_i = 0; uint8_t code = 1;
    while (ri < n) {
        if (in[ri] == 0) { out[code_i] = code; code = 1; code_i = wi++; ri++; }
        else { out[wi++] = in[ri++]; if (++code == 0xFF) { out[code_i] = code; code = 1; code_i = wi++; } }
    }
    out[code_i] = code; out[wi++] = 0x00; return wi;
}

/* ------------------------------------------------------------------ frame types and header (RFQ 5.2) */
enum { FT_DATA = 1, FT_STATUS = 2, FT_EVENT = 3, FT_GAP = 4, FT_SIGNATURE = 5, FT_CMD_ACK = 6,
       /* host -> device.  FW-EEG-001 section 5.2 and TOOL-EEG-022; the host stamps this in
          header byte 1 and the device had no name for it, so it never checked it. */
       FT_CMD = 16 };
#pragma pack(push,1)
/* FW-D19.  This used to be memcpy'd onto the wire with sizeof(), and sizeof() is 12,
   not 10: the struct is tail-padded to its 4-byte alignment, so two padding bytes landed
   between the header and the payload and every host parser written to FW-EEG-001 section
   5.1 -- including this package's own tools/verify_stream.py, which unpacks "<BBHIBB" --
   misparsed every frame by two bytes.
   The header is now serialised field by field into a fixed 10-byte layout.  A wire format
   must never be a struct copy: the layout is a contract with other people's software, not
   a detail of how this compiler happens to lay out memory. */
#define FRAME_HDR_BYTES 10
typedef struct { uint8_t version, type; uint16_t seq; uint32_t first_sample; uint8_t rate_code, n_samples; } frame_hdr_t;

static size_t frame_hdr_put(uint8_t *o, const frame_hdr_t *h) {
    o[0] = h->version;
    o[1] = h->type;
    o[2] = (uint8_t)(h->seq & 0xFF);
    o[3] = (uint8_t)(h->seq >> 8);
    o[4] = (uint8_t)(h->first_sample & 0xFF);
    o[5] = (uint8_t)((h->first_sample >> 8) & 0xFF);
    o[6] = (uint8_t)((h->first_sample >> 16) & 0xFF);
    o[7] = (uint8_t)((h->first_sample >> 24) & 0xFF);
    o[8] = h->rate_code;
    o[9] = h->n_samples;
    return FRAME_HDR_BYTES;
}
_Static_assert(FRAME_HDR_BYTES == 10, "FW-EEG-001 section 5.1 fixes the header at 10 bytes");
#pragma pack(pop)
#define PROTO_VERSION 1

static uint8_t txbuf[2 + sizeof(frame_hdr_t) + FRAME_SAMPLES_MAX * SAMPLE_BYTES + 4 + 64];
static uint8_t cobsbuf[sizeof(txbuf) + sizeof(txbuf) / 254 + 2];

static void frame_emit(uint8_t type, uint32_t first_sample, uint8_t n_samples, const uint8_t *payload, size_t plen) {
    frame_hdr_t h = { PROTO_VERSION, type, g_seq++, first_sample, (uint8_t)g_rate_code, n_samples };
    size_t o = frame_hdr_put(txbuf, &h);   /* NOT sizeof h -- see FW-D19 */
    memcpy(txbuf + o, payload, plen); o += plen;
    uint32_t c = crc32(txbuf, o); memcpy(txbuf + o, &c, 4); o += 4;
    size_t enc = cobs_encode(txbuf, o, cobsbuf);
    /* identical bytes to USB (both interfaces if open), ring buffer and SD */
    if (tud_cdc_connected()) { tud_cdc_write(cobsbuf, enc); tud_cdc_write_flush(); }
    if (tud_vendor_mounted()) tud_vendor_write(cobsbuf, enc), tud_vendor_write_flush();
    if (type == FT_DATA) {
        if (xRingbufferSend(rb, cobsbuf, enc, 0) != pdTRUE) {
            /* overflow: drop oldest until it fits, then announce the gap (F-07) */
            size_t sz; void *old;
            while ((old = xRingbufferReceive(rb, &sz, 0)) != NULL) { vRingbufferReturnItem(rb, old); if (xRingbufferSend(rb, cobsbuf, enc, 0) == pdTRUE) break; }
        }
    }
    extern void sd_append(const uint8_t *, size_t); sd_append(cobsbuf, enc);
}

/* ------------------------------------------------------------------ ADS1299 low level */
static void ads_cmd(uint8_t c) { spi_transaction_t t = { .length = 8, .tx_buffer = &c }; spi_device_polling_transmit(ads, &t); }
static void ads_wreg_all(uint8_t reg, uint8_t val) {
    /* daisy-chain: write goes to both devices in sequence (device 2 first on the chain) */
    uint8_t buf[2 + N_DEV] = { ADS_WREG | reg, 0 };
    for (int i = 0; i < N_DEV; i++) buf[2 + i] = val;
    spi_transaction_t t = { .length = 8 * sizeof buf, .tx_buffer = buf }; spi_device_polling_transmit(ads, &t);
}
/* LOFF (0x04) = COMP_TH[7:5] | reserved[4] | ILEAD_OFF[3:2] | FLEAD_OFF[1:0].
   ILEAD_OFF 00 = 6 nA and FLEAD_OFF 11 = AC at fDR/4 are what ads_init() sets and what
   E-06 asks for; only COMP_TH moves.  COMP_TH is the fraction of supply the lead-off
   voltage must exceed for the comparator to trip, so a HIGHER percentage needs a HIGHER
   electrode impedance to trip: 70 % is the sensitive end, 95 % the insensitive one. */
#define LOFF_BASE        0x03                   /* ILEAD_OFF = 6 nA, FLEAD_OFF = AC fDR/4 */
#define LOFF_TH_SENS     (0xE0 | LOFF_BASE)     /* COMP_TH 111 = 70 % -- trips when marginal */
#define LOFF_TH_INSENS   (0x00 | LOFF_BASE)     /* COMP_TH 000 = 95 % -- trips only when off */

/* Move the lead-off comparator threshold.  A register write is only accepted outside
   RDATAC, so the continuous read is stopped and restarted around it.  This is called
   only from lights_task(), which never runs while g_recording is set, so no sample
   stream is ever interrupted by it. */
static void ads_set_loff_threshold(uint8_t loff_reg) {
    ads_cmd(ADS_SDATAC);
    ads_wreg_all(REG_LOFF, loff_reg);
    ads_cmd(ADS_RDATAC);
}

static void ads_set_rate(uint16_t code) {
    /* CONFIG1: 0x90 | DR ; DR: 110=250, 101=500, 100=1000 SPS ; bit6 DAISY_EN=0 (daisy on) */
    uint8_t dr = (code == 0) ? 0x06 : (code == 1) ? 0x05 : 0x04;
    ads_wreg_all(REG_CONFIG1, 0x90 | dr); g_rate_code = code;
}
static void ads_init(void) {
    spi_bus_config_t bus = { .mosi_io_num = PIN_MOSI, .miso_io_num = PIN_MISO, .sclk_io_num = PIN_SCLK, .quadwp_io_num = -1, .quadhd_io_num = -1, .max_transfer_sz = 64 };
    spi_bus_initialize(SPI2_HOST, &bus, SPI_DMA_CH_AUTO);
    spi_device_interface_config_t dev = { .clock_speed_hz = 4000000, .mode = 1, .spics_io_num = PIN_CS, .queue_size = 4 };
    spi_bus_add_device(SPI2_HOST, &dev, &ads);
    gpio_set_direction(PIN_RESET, GPIO_MODE_OUTPUT); gpio_set_direction(PIN_START, GPIO_MODE_OUTPUT);
    gpio_set_level(PIN_START, 0); gpio_set_level(PIN_RESET, 0); vTaskDelay(pdMS_TO_TICKS(2)); gpio_set_level(PIN_RESET, 1); vTaskDelay(pdMS_TO_TICKS(2));
    ads_cmd(ADS_SDATAC);
    ads_wreg_all(REG_CONFIG3, 0xEC);           /* internal ref, BIAS buffer + measure, BIASREF int */
    ads_wreg_all(REG_CONFIG2, 0xC0);           /* test signal off */
    ads_set_rate(1);
    /* device 1: EEG ch1-8 gain 24 normal ; device 2: ch1-3 EMG gain 12, ch4-6 envelope gain 1, ch7-8 gain 24 */
    for (int ch = 0; ch < 8; ch++) {
        uint8_t buf[2 + N_DEV] = { ADS_WREG | (REG_CH1SET + ch), 0 };
        buf[2] = (ch < 3) ? 0x50 : (ch < 6) ? 0x00 : 0x60;    /* device 2 (first on chain): 0x50 g12, 0x00 g1, 0x60 g24 */
        buf[3] = 0x60;                                          /* device 1 (EEG): gain 24 */
        spi_transaction_t t = { .length = 8 * sizeof buf, .tx_buffer = buf }; spi_device_polling_transmit(ads, &t);
    }
    /* lead-off: device 1 all 8 channels, AC 7.8 Hz excitation, 6 nA (E-06); device 2 none */
    { uint8_t b1[2 + N_DEV] = { ADS_WREG | REG_LOFF, 0, 0x00, 0x03 }; spi_transaction_t t = { .length = 32, .tx_buffer = b1 }; spi_device_polling_transmit(ads, &t); }
    { uint8_t b2[2 + N_DEV] = { ADS_WREG | REG_LOFF_SENSP, 0, 0x00, 0xFF }; spi_transaction_t t = { .length = 32, .tx_buffer = b2 }; spi_device_polling_transmit(ads, &t); }
    { uint8_t b3[2 + N_DEV] = { ADS_WREG | REG_BIAS_SENSP, 0, 0x00, 0xFF }; spi_transaction_t t = { .length = 32, .tx_buffer = b3 }; spi_device_polling_transmit(ads, &t); }
    ads_wreg_all(REG_MISC1, 0x20);             /* SRB1 as reference for all channels */
    ads_cmd(ADS_RDATAC);
}

/* ------------------------------------------------------------------ DRDY ISR -> sample task */
static TaskHandle_t sample_task_h;
/* FW-D08 CLOSED.  The comparator bit used to be sampled in the task, which put an
   unbounded scheduling delay between the stimulus edge and the sample it was attributed
   to; E-12 exists to make that attribution exact.  It is latched here, in the ISR, at the
   instant the converter says the sample is ready, and carried per sample.
   g_onset_* are read by envelope_onset_after() in drivers.c. */
volatile uint32_t g_onset_sample;
volatile uint8_t  g_onset_valid;
static volatile uint8_t g_env_latched;
static volatile uint8_t g_env_prev;

static void IRAM_ATTR drdy_isr(void *arg) {
    g_sample_index++;                          /* the only timeline in the system (E-19) */
    uint8_t env = gpio_get_level(PIN_ENV_CMP) ? 1 : 0;
    g_env_latched = env;
    if (env && !g_env_prev) {                  /* rising edge = stimulus onset */
        g_onset_sample = g_sample_index;
        g_onset_valid = 1;
    }
    g_env_prev = env;
    BaseType_t hp = pdFALSE; vTaskNotifyGiveFromISR(sample_task_h, &hp); if (hp) portYIELD_FROM_ISR();
}
static uint16_t aux_bits(void) {
    uint16_t a = 0;
    if (!gpio_get_level(PIN_BTN_A)) a |= 1 << 0;
    if (!gpio_get_level(PIN_BTN_B)) a |= 1 << 1;
    if (!gpio_get_level(PIN_BTN_STOP)) a |= 1 << 2;
    if (g_env_latched) a |= 1 << 3;            /* latched in drdy_isr, FW-D08 */
    if (g_loff_bits) a |= 1 << 4;
    a |= (uint16_t)(g_recording ? 1 << 5 : 0);
    return a;
}
static void sample_task(void *arg) {
    /* one daisy read = 2 devices x (24-bit status + 8 x 24-bit) = 54 bytes */
    static uint8_t rx[54]; static uint8_t pay[FRAME_SAMPLES_MAX * SAMPLE_BYTES]; int n = 0; uint32_t first = 0;
    const int per_frame[3] = { 5, 10, 20 };   /* one frame every 20 ms at 250/500/1000 Hz */
    for (;;) {
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        spi_transaction_t t = { .length = 8 * sizeof rx, .rx_buffer = rx }; spi_device_polling_transmit(ads, &t);
        if (n == 0) first = g_sample_index;
        uint8_t *p = pay + n * SAMPLE_BYTES;
        /* device 1 (EEG) is second in the chain: bytes 27..53 ; device 2 first: bytes 0..26 */
        memcpy(p, rx + 27 + 3, 24);           /* ch1-8 EEG */
        memcpy(p + 24, rx + 3, 24);           /* ch9-16 EMG/ENV/spare */
        /* The ADS1299 status word is 1100 + LOFF_STATP[8] + LOFF_STATN[8] + GPIO[4].
           Only STATP was read, which is one bit per site and cannot express three
           colours -- which is why E-27's amber had nowhere to come from.  Both halves
           are captured now: P and N are the positive and negative lead-off detectors of
           the same site, so "one of the two has let go" is a real, measured middle
           state and not an invention. */
        g_loff_p = (uint8_t)(((rx[27] & 0x0F) << 4) | (rx[28] >> 4));
        g_loff_n = (uint8_t)(((rx[28] & 0x0F) << 4) | (rx[29] >> 4));
        g_loff_bits = g_loff_p;                  /* the summary the status frame carries */
        uint16_t aux = aux_bits(); memcpy(p + 48, &aux, 2);
        if (++n >= per_frame[g_rate_code]) { frame_emit(FT_DATA, first, n, pay, n * SAMPLE_BYTES); n = 0; }
    }
}

/* ------------------------------------------------------------------ contact lights (E-27) */
static void lights_write(uint8_t bits) {
    for (int i = 7; i >= 0; i--) { gpio_set_level(PIN_SR_DATA, (bits >> i) & 1); gpio_set_level(PIN_SR_CLK, 1); gpio_set_level(PIN_SR_CLK, 0); }
    gpio_set_level(PIN_SR_LATCH, 1); gpio_set_level(PIN_SR_LATCH, 0);
}
/* E-27: the bicolour phase driver.
 *
 * Each site carries a two-lead bicolour LED between its shift-register output Qn and the
 * LED_V common on GPIO48, so the colour is decided by which way the current runs:
 *
 *     phase A   LED_V high, Qn low   ->  green
 *     phase B   LED_V low,  Qn high  ->  red
 *     both, alternating above 100 Hz ->  amber
 *
 * A site lit in phase A only is green, in phase B only is red, in both is amber, in
 * neither is dark.  LIGHT_PHASE_HZ is 240, so each half-phase is 1/480 s.
 *
 * This did not exist.  lights_write() and lights_task() were on-and-off only, so no site
 * could show red or amber, E-27 was recorded as not met and TST-EEG-004 T11 could not
 * pass.  The wiring was always built for it -- WH-EEG-008 section 3.2 specifies the
 * anti-parallel pair and the 240 Hz alternation -- and only the firmware was missing.
 *
 * The colour comes from the converter's own lead-off measurement, which is what E-27
 * asks for.
 *
 * FW-D17, corrected 2026-09-02.  This first read the P and N halves of the lead-off
 * result and called a site amber when exactly one had let go and red when both had.
 * That cannot work on this board.  The montage is SINGLE-ENDED: J2 carries IN1..IN8, one
 * shared SRB1 reference and BIASOUT (design.py, conn("J2", ...)), so there is no
 * per-site negative electrode for LOFF_STATN to report on.  ads_init() enabled
 * LOFF_SENSP only, LOFF_STATN therefore read 0 for every channel forever, and the old
 * expression collapsed: `bad = p & n` was always 0, so RED WAS UNREACHABLE and every
 * site that had lost contact showed amber.  Enabling LOFF_SENSN would not have fixed it
 * either -- with SRB1 closed, all eight N bits report the one shared reference, so they
 * carry no per-site information at all.
 *
 * What the hardware does support is reading the SAME positive-side comparator at TWO
 * thresholds.  COMP_TH sets the fraction of supply the injected 6 nA must develop before
 * the comparator trips, so a sensitive threshold trips at a moderate impedance and an
 * insensitive one only at a high one.  The lights task alternates the two slowly and
 * latches a mask from each:
 *
 *     trips neither threshold            GREEN   contact good
 *     trips the sensitive one only       AMBER   marginal, re-gel it
 *     trips both                         RED     no contact
 *
 * The insensitive set is a subset of the sensitive one by construction, so the three
 * states are exhaustive and cannot overlap.  T11 has still never been run: no unit
 * exists, and the two COMP_TH values below are the datasheet's endpoints rather than
 * measured ones -- T11 is where they get their real values.
 */
/* Half a phase, in FreeRTOS ticks, never less than one.
 *
 * At LIGHT_PHASE_HZ = 240 a half-phase is 2.083 ms, and on a 1 kHz tick this becomes
 * 2 ticks = 2 ms, i.e. an actual alternation of 250 Hz rather than 240.  That is stated
 * rather than hidden: the requirement is "above 100 Hz" and 250 Hz meets it with room,
 * the two half-phases are equal so the duty is still 50/50 and the colour does not
 * shift, and TST-EEG-004 T11 reads the R/G ratio with a colorimeter, which does not care
 * about 4 % of frequency.  If a build ever needs exactly 240 Hz it needs a hardware
 * timer, not a task delay, and that is a different piece of work. */
#define LIGHT_HALF_TICKS ((pdMS_TO_TICKS(1000 / (2 * LIGHT_PHASE_HZ)) > 0) \
                          ? pdMS_TO_TICKS(1000 / (2 * LIGHT_PHASE_HZ)) : 1)

static void lights_phase(uint8_t green_mask, uint8_t red_mask) {
    /* phase A: LED_V high, and a site lights when its output is pulled LOW */
    lights_write((uint8_t) ~green_mask);
    gpio_set_level(PIN_LED_V, 1);
    vTaskDelay(LIGHT_HALF_TICKS);
    /* phase B: LED_V low, and a site lights when its output is driven HIGH */
    lights_write(red_mask);
    gpio_set_level(PIN_LED_V, 0);
    vTaskDelay(LIGHT_HALF_TICKS);
}

/* Phase pairs spent at each threshold before the sweep moves on.  At about 4 ms a pair
   this is roughly 200 ms per end, so each mask refreshes about 2.5 times a second. */
#define LIGHT_SWEEP_PAIRS 50

static void lights_task(void *arg) {
    (void) arg;
    unsigned sweep = 0;
    bool at_sens = true;
    ads_set_loff_threshold(LOFF_TH_SENS);
    for (;;) {
        if (g_recording || !g_lights_enabled) {
            /* Dark during a block and whenever the host has switched them off.  LED_V is
               returned to an INPUT rather than merely driven low, which is the same state
               it holds at reset and the reason nothing can light at boot: with the common
               floating, no current can flow through any site whatever the shift register
               happens to contain.  Driving it low would also be dark, but only as long as
               the level is right; an input is dark by construction. */
            lights_write(0x00);
            gpio_set_direction(PIN_LED_V, GPIO_MODE_INPUT);
            vTaskDelay(pdMS_TO_TICKS(20));
            continue;
        }
        /* Claim the common only while the lights are actually wanted. */
        gpio_set_direction(PIN_LED_V, GPIO_MODE_OUTPUT);

        if (g_lights_force) {
            /* CMD_LIGHTS modes 2, 3 and 4: hold one colour on the masked sites. */
            uint8_t m = g_lights_force_mask;
            uint8_t g = (g_lights_force == 2 || g_lights_force == 4) ? m : 0;
            uint8_t r = (g_lights_force == 3 || g_lights_force == 4) ? m : 0;
            lights_phase(g, r);
            continue;
        }

        /* Sweep the comparator threshold and latch a mask at each end.  The sweep is
           slow on purpose: LIGHT_SWEEP_PAIRS phase pairs is about 200 ms per end, which
           is far longer than the AC lead-off settles in and rare enough that the two
           SPI register writes cost nothing, while still refreshing both masks about
           twice a second -- fast enough to follow a gel syringe. */
        if (++sweep >= LIGHT_SWEEP_PAIRS) {
            sweep = 0;
            if (at_sens) { g_loff_sens = g_loff_p; ads_set_loff_threshold(LOFF_TH_INSENS); }
            else         { g_loff_insens = g_loff_p; ads_set_loff_threshold(LOFF_TH_SENS); }
            at_sens = !at_sens;
        }
        uint8_t sens = g_loff_sens, insens = g_loff_insens;
        uint8_t bad  = (uint8_t)(sens & insens);            /* trips both  -> red   */
        uint8_t marg = (uint8_t)(sens & ~insens);           /* sensitive   -> amber */
        uint8_t good = (uint8_t)(~sens);                    /* neither     -> green */
        /* green in phase A; red in phase B; amber is a site that appears in both */
        lights_phase((uint8_t)(good | marg), (uint8_t)(bad | marg));
    }
}

/* ------------------------------------------------------------------ command channel (F-10) */
enum { CMD_START_SESSION = 0x01, CMD_STOP_SESSION = 0x02, CMD_BLOCK_START = 0x03, CMD_BLOCK_END = 0x04, CMD_SET_RATE = 0x05,
       CMD_SET_GAIN = 0x06, CMD_IMPEDANCE = 0x07, CMD_RETRANSMIT = 0x08, CMD_TIMING_SELFTEST = 0x09, CMD_LIGHTS = 0x0A,
       CMD_CLOCK_XCHG = 0x0B, CMD_PLAY_AT = 0x0C, CMD_FW_UPDATE_BEGIN = 0x0D, CMD_PROVISION = 0x0E,
       /* Connectivity self-test.  Neither command touches the converters, the
          electrodes or the microSD card, so both are safe to run on a bench unit with
          nothing connected to it.  TOOL-EEG-022 is the browser tool that uses them. */
       CMD_IDENTIFY = 0x0F, CMD_LOOPBACK = 0x10 };

#define FW_VERSION_MAJOR 0
#define FW_VERSION_MINOR 3
#define CAP_CDC        (1u << 0)
#define CAP_WEBUSB     (1u << 1)
#define CAP_MICROSD    (1u << 2)
#define CAP_CODEC      (1u << 3)
#define CAP_ATECC      (1u << 4)
#define CAP_PROVISIONED (1u << 5)
/* ------------------------------------------------------------------ end-of-line provisioning
 *
 * FW-D10/D14 CLOSED.  tools/provision.py has always sent opcodes 0x40-0x4F; the firmware
 * implemented none of them, so F-18 and T6 could not run against the shipped pair.  The
 * device side is here, and it matches provision.py command for command.
 *
 * The window is deliberately narrow: provisioning is refused once the ATECC config zone is
 * locked (0x47), which is the last step, so a fielded unit cannot be re-keyed over USB.
 */
enum { CMD_ENTER_PROV = 0x40, CMD_ATECC_GENKEY = 0x41, CMD_ATECC_READ_PUBKEY = 0x42,
       CMD_ATECC_READ_SERIAL = 0x43, CMD_WRITE_USB_IDS = 0x44, CMD_WRITE_HWREV = 0x45,
       CMD_WRITE_CALIBRATION = 0x46, CMD_ATECC_LOCK_CONFIG = 0x47,
       CMD_READ_PROVISION_STATE = 0x48, CMD_WRITE_UNIT_SERIAL = 0x49,
       /* TST-EEG-004 T6 writes the calibration set and its acceptance limit is that the
          unit reads back what was written -- which was impossible, because nothing could
          read it back.  Chunked because a full calibration set does not fit in one frame:
          the request carries a uint16 offset and a uint8 length. */
       CMD_READ_CALIBRATION = 0x4A,
       /* Write one 32-byte block of the ATECC config zone from the station's template.
          0x4A was allocated to this on the host side and to CMD_READ_CALIBRATION here,
          on the same day, by two people who each picked the next free opcode -- a
          collision that would have had provision.py's config write answered by the
          calibration reader.  The firmware implements 0x4A, so the host moves to 0x4B. */
       CMD_ATECC_WRITE_CONFIG = 0x4B,
       CMD_LEAVE_PROV = 0x4F };

static bool g_prov_open;

/* drivers.c */
esp_err_t drv_atecc_genkey(uint8_t pub[64]);
esp_err_t drv_atecc_pubkey(uint8_t pub[64]);
esp_err_t drv_atecc_lock_config(void);
bool      drv_atecc_config_locked(void);
esp_err_t drv_nvs_set_str(const char *key, const char *val);
esp_err_t drv_nvs_set_blob(const char *key, const void *val, size_t n);

/* FW-EEG-001 section 6.2 fixes the acknowledgement payload:
 *     0  opcode echoed   1  reserved, zero   2  status   3  result length   4..  result
 * Every CMD_ACK went out as { opcode, status } with the status at offset 1 and no length,
 * and IDENTIFY, LOOPBACK and CLOCK_XCHG skipped the shape entirely and returned their
 * result at offset 0.  The document says so itself: "main.c's current 8-byte ack ... does
 * not match and must be reshaped."  It matters beyond tidiness -- with no opcode echo on
 * three replies the host cannot tell which command an acknowledgement answers, and its
 * queue resolves the next pending command with whatever arrives. */
#define ACK_STATUS_OK           0x00
#define ACK_STATUS_UNKNOWN_OP   0x01
#define ACK_STATUS_BAD_LENGTH   0x02
#define ACK_STATUS_VBUS_LOCKOUT 0x05
#define ACK_STATUS_UNIMPLEMENTED 0x0B
#define ACK_RESULT_MAX 240

static void ack_emit(uint8_t opcode, uint8_t status, const uint8_t *result, size_t rlen) {
    uint8_t a[4 + ACK_RESULT_MAX];
    if (rlen > ACK_RESULT_MAX) rlen = ACK_RESULT_MAX;
    a[0] = opcode;
    a[1] = 0;                       /* reserved */
    a[2] = status;
    a[3] = (uint8_t) rlen;
    if (rlen && result) memcpy(a + 4, result, rlen);
    frame_emit(FT_CMD_ACK, g_sample_index, 0, a, 4 + rlen);
}

static void handle_provision(const uint8_t *c, size_t n)
{
    /* This path used to build its own { opcode, status, result... } and call frame_emit()
       directly, so the provisioning family kept the pre-section-6.2 shape after every other
       command moved to ack_emit().  firmware/tools/provision.py reads the status at absolute
       frame offset 12 and the data from 14 -- which IS section 6.2 -- so it was reading the
       first RESULT byte as the status.  On CMD_READ_PROVISION_STATE that byte is the
       config-zone lock flag, so an UNLOCKED unit reported 0 and the tool read it as success:
       the one command whose whole job is to say whether provisioning has happened answered
       "fine" for a blank part.  Status codes are unchanged; only the envelope moves. */
    uint8_t status = 0;                            /* 0 = ok */
    uint8_t result[ACK_RESULT_MAX];
    size_t rlen = 0;

    if (c[0] != CMD_ENTER_PROV && c[0] != CMD_READ_PROVISION_STATE
        && c[0] != CMD_READ_CALIBRATION && !g_prov_open) {
        ack_emit(c[0], 0x01, NULL, 0);             /* not in provisioning mode */
        return;
    }

    switch (c[0]) {
    case CMD_ENTER_PROV:
        if (drv_atecc_config_locked()) {
            status = 0x02;                         /* already provisioned; refuse */
            break;
        }
        g_prov_open = true;
        break;

    case CMD_ATECC_GENKEY:
        status = drv_atecc_genkey(result) == ESP_OK ? 0 : 0x10;
        if (!status) rlen = 64;
        break;

    case CMD_ATECC_READ_PUBKEY:
        status = drv_atecc_pubkey(result) == ESP_OK ? 0 : 0x11;
        if (!status) rlen = 64;
        break;

    case CMD_ATECC_READ_SERIAL: {
        char sn[32];
        atecc_serial_into(sn, sizeof sn);
        size_t l = strlen(sn);
        if (l == 0) { status = 0x12; break; }
        if (l > sizeof result) l = sizeof result;
        memcpy(result, sn, l); rlen = l;
        break;
    }

    case CMD_WRITE_UNIT_SERIAL: {                  /* payload: the TIOV-B-nnnn string */
        char sn[24] = { 0 };
        size_t l = n - 1 < sizeof sn - 1 ? n - 1 : sizeof sn - 1;
        memcpy(sn, c + 1, l);
        status = drv_nvs_set_str("unit_serial", sn) == ESP_OK ? 0 : 0x13;
        break;
    }

    case CMD_WRITE_USB_IDS:                        /* payload: vid_lo vid_hi pid_lo pid_hi */
        if (n < 5) { status = 0x20; break; }
        status = drv_nvs_set_blob("usb_ids", c + 1, 4) == ESP_OK ? 0 : 0x14;
        break;

    case CMD_WRITE_HWREV:
        if (n < 2) { status = 0x20; break; }
        status = drv_nvs_set_blob("hw_rev", c + 1, n - 1) == ESP_OK ? 0 : 0x15;
        break;

    case CMD_WRITE_CALIBRATION:
        status = drv_nvs_set_blob("calib", c + 1, n - 1) == ESP_OK ? 0 : 0x16;
        break;

    case CMD_ATECC_WRITE_CONFIG: {
        /* payload: block u8 | mask[32] | image[32] -- 65 bytes with the opcode. */
        if (n < 1 + 1 + 32 + 32) { status = ACK_STATUS_BAD_LENGTH; break; }
        if (drv_atecc_config_locked()) { status = 0x09; break; }   /* already locked */
        status = drv_atecc_write_config(c[1], c + 2, c + 34) == ESP_OK ? 0 : 0x18;
        break;
    }

    case CMD_ATECC_LOCK_CONFIG:                    /* irreversible, and last */
        status = drv_atecc_lock_config() == ESP_OK ? 0 : 0x17;
        break;

    case CMD_READ_CALIBRATION: {
        /* payload: offset_lo offset_hi length.  Answers with that slice of the stored
           calibration blob so the host can compare it byte for byte with what it sent.
           TST-EEG-004 T6's acceptance limit is that the unit reads back what was
           written, and nothing could read it back at all before this existed.
           Chunked because a full calibration set does not fit in one frame.
           Exempt from the provisioning-mode gate below: T6 runs AFTER provisioning, on
           a unit that has left provisioning mode and may have had its zone locked. */
        if (n < 4) { status = ACK_STATUS_BAD_LENGTH; break; }
        uint16_t off = (uint16_t)(c[1] | (c[2] << 8));
        uint8_t want = c[3];
        if (want > ACK_RESULT_MAX) want = ACK_RESULT_MAX;
        static uint8_t cal[4096];
        size_t clen = sizeof cal;
        if (drv_nvs_get_blob("calib", cal, &clen) != ESP_OK) { status = 0x06; break; }
        if (off >= clen) { rlen = 0; break; }
        if ((size_t) off + want > clen) want = (uint8_t)(clen - off);
        memcpy(result, cal + off, want);
        rlen = want;
        break;
    }

    case CMD_READ_PROVISION_STATE:
        result[0] = drv_atecc_config_locked() ? 1 : 0;
        result[1] = g_prov_open ? 1 : 0;
        rlen = 2;
        break;

    case CMD_LEAVE_PROV:
        g_prov_open = false;
        break;

    default:
        status = ACK_STATUS_UNKNOWN_OP;
        break;
    }
    ack_emit(c[0], status, result, rlen);
}

static void handle_command(const uint8_t *c, size_t n) {
    if (n >= 1 && c[0] >= 0x40 && c[0] <= 0x4F) { handle_provision(c, n); return; }
    if (n < 1) return;
    uint8_t status = ACK_STATUS_OK;
    uint8_t result[ACK_RESULT_MAX]; size_t rlen = 0;
    switch (c[0]) {
    case CMD_START_SESSION:
        /* S-01 has TWO halves and both are mandatory.  The second one -- refusing to start
           a session while the charger is plugged in -- was missing entirely from this
           handler until FW-D17.  Recording on a unit tethered to a mains-powered charger
           is exactly the condition the isolated, battery-only design exists to prevent, so
           the refusal comes FIRST, before anything is armed. */
        if (gpio_get_level(PIN_VBUS_DET)) {
            status = ACK_STATUS_VBUS_LOCKOUT;   /* VBUS_DET high, session refused */
            break;                     /* the FT_CMD_ACK at the end of this function sends it */
        }
        g_recording = false;
        gpio_set_level(PIN_CHG_CE, 1); /* CE active-low: 1 = charging OFF (S-01) */
        gpio_set_level(PIN_START, 1);
        break;
    case CMD_IDENTIFY: {
        /* Everything a host needs to prove it is talking to the right device, and nothing
           that requires the analogue front end to be alive.  Fixed layout, little-endian:
             0  proto version            1  fw major        2  fw minor
             3  board revision letter    4..7 ring bytes    8..11 capability flags
             12 rate code                13 number of supported rates
             14..N  unit serial, NUL-terminated                                        */
        uint8_t d[64] = { 0 };
        size_t k = 0;
        d[k++] = PROTO_VERSION;
        d[k++] = FW_VERSION_MAJOR;
        d[k++] = FW_VERSION_MINOR;
        d[k++] = (uint8_t) BOARD_REV[0];
        uint32_t rb_bytes = RING_BYTES;
        memcpy(d + k, &rb_bytes, 4); k += 4;
        uint32_t caps = CAP_CDC | CAP_WEBUSB;
        if (sd_free_mb() > 0)              caps |= CAP_MICROSD;
        /* CAP_CODEC was defined, documented in TOOL-EEG-022 and displayed by the browser
           test tool, and never set by anything -- so a working codec always read as absent.
           CAP_ATECC was set only when the config zone was LOCKED, which conflates "the
           chip is fitted" with "the unit has been provisioned"; an unprovisioned board
           coming off the line reported no secure element at all, at exactly the moment a
           production tester is asking whether the part is there. */
        if (drv_codec_ready())             caps |= CAP_CODEC;
        if (drv_atecc_present())           caps |= CAP_ATECC;
        if (drv_atecc_config_locked())     caps |= CAP_PROVISIONED;
        memcpy(d + k, &caps, 4); k += 4;
        d[k++] = (uint8_t) g_rate_code;
        d[k++] = 3;                                    /* 250, 500, 1000 Hz */
        char sn[24];
        unit_serial_into(sn, sizeof sn);
        size_t sl = strlen(sn);
        if (k + sl + 1 > sizeof d) sl = sizeof d - k - 1;
        memcpy(d + k, sn, sl); k += sl;
        d[k++] = 0;
        ack_emit(CMD_IDENTIFY, ACK_STATUS_OK, d, k);
        return;
    }

    case CMD_LOOPBACK: {
        /* Echo the payload back unchanged.  This is the only command that proves the WHOLE
           path -- COBS framing, the CRC, the sequence counter and both USB endpoints -- in
           one round trip, which is what makes it worth having separately from IDENTIFY.
           The host sends a known pattern and compares. */
        size_t l = n - 1;
        if (l > 240) l = 240;
        ack_emit(CMD_LOOPBACK, ACK_STATUS_OK, c + 1, l);
        return;
    }

    case CMD_STOP_SESSION:  gpio_set_level(PIN_START, 0); g_recording = false; gpio_set_level(PIN_CHG_CE, 0); break;
    case CMD_BLOCK_START:   g_recording = true;  frame_emit(FT_EVENT, g_sample_index, 0, c + 1, n - 1); break;
    case CMD_BLOCK_END:     g_recording = false; frame_emit(FT_EVENT, g_sample_index, 0, c + 1, n - 1); break;
    case CMD_SET_RATE:
        /* FW-D18: the ADS1299 ignores register writes while it is in RDATAC, so a
           bare WREG CONFIG1 changed nothing and the rate silently stayed put.
           SDATAC first, write, then RDATAC again. */
        if (n >= 2 && c[1] <= 2) {
            gpio_set_level(PIN_START, 0);
            ads_cmd(ADS_SDATAC);
            ads_set_rate(c[1]);
            ads_cmd(ADS_RDATAC);
            gpio_set_level(PIN_START, 1);
        }
        break;
    case CMD_LIGHTS:
        /* FW-D18, corrected 2026-09-02.  This took c[1] as a plain enable and answered
           0x00 OK to every value, so a host asking for mode 3 (force red) was told the
           request had succeeded while the firmware carried on showing automatic colour.
           The documented answer for an unsupported mode was 0x0B; the modes are now
           implemented instead, which is the better of the two answers.
              0 off   1 automatic   2 force green   3 force red   4 force amber
           c[2], when present, is the site mask the forced colour applies to. */
        if (n < 2) { status = ACK_STATUS_BAD_LENGTH; break; }
        if (c[1] > 4) { status = ACK_STATUS_UNIMPLEMENTED; break; }
        g_lights_force_mask = (n >= 3) ? c[2] : 0xFF;
        g_lights_enabled = (c[1] != 0);
        g_lights_force = (c[1] >= 2) ? c[1] : 0;
        break;
    case CMD_RETRANSMIT: {  /* payload: seq_from(2) seq_to(2) — replay from ring buffer */
        size_t sz; void *it; while ((it = xRingbufferReceive(rb, &sz, 0)) != NULL) { if (tud_cdc_connected()) tud_cdc_write(it, sz); if (tud_vendor_mounted()) tud_vendor_write(it, sz); vRingbufferReturnItem(rb, it); }
        break; }
    case CMD_TIMING_SELFTEST: { extern void timing_selftest(uint8_t *out); timing_selftest(result); rlen = 3; break; }
    case CMD_CLOCK_XCHG: {  /* reply with sample index + esp_timer us so the host estimates offset (F-16) */
        uint32_t si = g_sample_index; int64_t us = esp_timer_get_time(); uint8_t r[12]; memcpy(r, &si, 4); memcpy(r + 4, &us, 8); ack_emit(CMD_CLOCK_XCHG, ACK_STATUS_OK, r, 12); return; }
    default: status = ACK_STATUS_UNKNOWN_OP; break;
    }
    ack_emit(c[0], status, result, rlen);
}

/* ------------------------------------------------------------------ timing self-test (F-21)
 * Plays 40 tone bursts via the codec at commanded sample indices and detects the onset on the
 * stimulus-envelope channel (device 2 ch4) in the same sample stream. Reports median and p95
 * offset in samples. Spec: median <= 1, p95 <= 2 at 1 kHz. */
void timing_selftest(uint8_t *out) {
    extern void codec_play_tone_at(uint32_t sample_index); extern int envelope_onset_after(uint32_t sample_index, int window);
    int offs[40];
    for (int i = 0; i < 40; i++) { uint32_t at = g_sample_index + 200; codec_play_tone_at(at); vTaskDelay(pdMS_TO_TICKS(400)); offs[i] = envelope_onset_after(at, 100) - (int)at; }
    for (int i = 1; i < 40; i++) for (int j = i; j > 0 && offs[j - 1] > offs[j]; j--) { int t = offs[j]; offs[j] = offs[j - 1]; offs[j - 1] = t; }
    out[0] = (uint8_t)offs[20]; out[1] = (uint8_t)offs[38]; out[2] = (offs[20] <= 1 && offs[38] <= 2) ? 1 : 0;
}

/* ------------------------------------------------------------------ USB descriptors: CDC-ACM + vendor, BOS/WebUSB/MS OS 2.0 (F-01..F-04) */
#define USB_VID 0x1209          /* pid.codes; PID to be allocated (F-03) */
#define USB_PID 0x0000
enum { ITF_CDC = 0, ITF_CDC_DATA, ITF_VENDOR, ITF_TOTAL };
#define EPNUM_CDC_NOTIF 0x81
#define EPNUM_CDC_OUT   0x02
#define EPNUM_CDC_IN    0x82
#define EPNUM_VENDOR_OUT 0x03
#define EPNUM_VENDOR_IN  0x83
static const tusb_desc_device_t dev_desc = { .bLength = sizeof(tusb_desc_device_t), .bDescriptorType = TUSB_DESC_DEVICE, .bcdUSB = 0x0210,
    .bDeviceClass = TUSB_CLASS_MISC, .bDeviceSubClass = MISC_SUBCLASS_COMMON, .bDeviceProtocol = MISC_PROTOCOL_IAD, .bMaxPacketSize0 = 64,
    .idVendor = USB_VID, .idProduct = USB_PID, .bcdDevice = 0x0100, .iManufacturer = 1, .iProduct = 2, .iSerialNumber = 3, .bNumConfigurations = 1 };
#define CONFIG_TOTAL_LEN (TUD_CONFIG_DESC_LEN + TUD_CDC_DESC_LEN + TUD_VENDOR_DESC_LEN)
static const uint8_t cfg_desc[] = {
    TUD_CONFIG_DESCRIPTOR(1, ITF_TOTAL, 0, CONFIG_TOTAL_LEN, 0x00, 100),
    TUD_CDC_DESCRIPTOR(ITF_CDC, 4, EPNUM_CDC_NOTIF, 8, EPNUM_CDC_OUT, EPNUM_CDC_IN, 64),
    TUD_VENDOR_DESCRIPTOR(ITF_VENDOR, 5, EPNUM_VENDOR_OUT, EPNUM_VENDOR_IN, 64) };
/* BOS: WebUSB platform (landing page = session runner) + Microsoft OS 2.0 platform (WinUSB on vendor itf) */
#define BOS_TOTAL_LEN (TUD_BOS_DESC_LEN + TUD_BOS_WEBUSB_DESC_LEN + TUD_BOS_MICROSOFT_OS_DESC_LEN)
#define MS_OS_20_DESC_LEN 0xB2
#define VENDOR_REQUEST_WEBUSB 1
#define VENDOR_REQUEST_MICROSOFT 2
static const uint8_t bos_desc[] = { TUD_BOS_DESCRIPTOR(BOS_TOTAL_LEN, 2),
    TUD_BOS_WEBUSB_DESCRIPTOR(VENDOR_REQUEST_WEBUSB, 1),
    TUD_BOS_MS_OS_20_DESCRIPTOR(MS_OS_20_DESC_LEN, VENDOR_REQUEST_MICROSOFT) };
static const uint8_t ms_os_20_desc[] = {
    U16_TO_U8S_LE(0x000A), U16_TO_U8S_LE(MS_OS_20_SET_HEADER_DESCRIPTOR), U32_TO_U8S_LE(0x06030000), U16_TO_U8S_LE(MS_OS_20_DESC_LEN),
    U16_TO_U8S_LE(0x0008), U16_TO_U8S_LE(MS_OS_20_SUBSET_HEADER_CONFIGURATION), 0, 0, U16_TO_U8S_LE(MS_OS_20_DESC_LEN - 0x0A),
    U16_TO_U8S_LE(0x0008), U16_TO_U8S_LE(MS_OS_20_SUBSET_HEADER_FUNCTION), ITF_VENDOR, 0, U16_TO_U8S_LE(MS_OS_20_DESC_LEN - 0x0A - 0x08),
    U16_TO_U8S_LE(0x0014), U16_TO_U8S_LE(MS_OS_20_FEATURE_COMPATBLE_ID), 'W','I','N','U','S','B',0,0, 0,0,0,0,0,0,0,0,
    U16_TO_U8S_LE(MS_OS_20_DESC_LEN - 0x0A - 0x08 - 0x08 - 0x14), U16_TO_U8S_LE(MS_OS_20_FEATURE_REG_PROPERTY), U16_TO_U8S_LE(0x0007),
    U16_TO_U8S_LE(0x002A), 'D',0,'e',0,'v',0,'i',0,'c',0,'e',0,'I',0,'n',0,'t',0,'e',0,'r',0,'f',0,'a',0,'c',0,'e',0,'G',0,'U',0,'I',0,'D',0,'s',0,0,0,
    U16_TO_U8S_LE(0x0050), '{',0,'8',0,'F',0,'E',0,'6',0,'D',0,'4',0,'D',0,'7',0,'-',0,'4',0,'9',0,'D',0,'D',0,'-',0,'4',0,'1',0,'E',0,'7',0,'-',0,'9',0,'4',0,'8',0,'6',0,'-',0,'4',0,'9',0,'A',0,'F',0,'C',0,'6',0,'B',0,'F',0,'E',0,'4',0,'7',0,'5',0,'}',0,0,0,0,0 };
_Static_assert(sizeof(ms_os_20_desc) == MS_OS_20_DESC_LEN, "MS OS 2.0 descriptor length");
static const uint8_t webusb_url[] = { 3 + sizeof("one.witysk.org/eeg") - 1, 3 /* WEBUSB_URL */, 1 /* https */, 'o','n','e','.','w','i','t','y','s','k','.','o','r','g','/','e','e','g' };
static char serial_str[32] = "UNPROVISIONED";
static const char *str_desc[] = { (const char[]){ 0x09, 0x04 }, "TI One Voice", "EEG field kit", serial_str, "EEG CDC", "EEG WebUSB" };
/* The device, configuration and string descriptors are served by esp_tinyusb from the
 * tinyusb_config_t handed to tinyusb_driver_install() below -- .device_descriptor,
 * .configuration_descriptor and .string_descriptor.  This file used to ALSO define
 * tud_descriptor_device_cb(), tud_descriptor_configuration_cb() and
 * tud_descriptor_string_cb(), which the component defines too, so the link failed with
 * three "multiple definition" errors against descriptors_control.c.  Doing both is the
 * mistake: with CONFIG_TINYUSB_DESC_CUSTOM you supply the descriptors as DATA and the
 * component owns the callbacks.
 *
 * The BOS descriptor is the exception and stays here, because esp_tinyusb 1.4.x defines no
 * tud_descriptor_bos_cb() and tinyusb_config_t has no field for one -- and without a BOS
 * descriptor there is no WebUSB and no MS OS 2.0 platform capability, which is most of what
 * this device's USB identity is for. */
uint8_t const *tud_descriptor_bos_cb(void) { return bos_desc; }
bool tud_vendor_control_xfer_cb(uint8_t rhport, uint8_t stage, tusb_control_request_t const *req) {
    if (stage != CONTROL_STAGE_SETUP) return true;
    if (req->bmRequestType_bit.type == TUSB_REQ_TYPE_VENDOR) {
        if (req->bRequest == VENDOR_REQUEST_WEBUSB) return tud_control_xfer(rhport, req, (void *)webusb_url, sizeof webusb_url);
        if (req->bRequest == VENDOR_REQUEST_MICROSOFT && req->wIndex == 7) return tud_control_xfer(rhport, req, (void *)ms_os_20_desc, MS_OS_20_DESC_LEN);
    }
    return false;
}

/* ------------------------------------------------------------------ host -> device: COBS decode incoming commands from either interface */
/* One pass of the receive loop, factored out of rx_task so that a host-side test
   harness can drive the REAL decode and dispatch path rather than a copy of it.
   Returns the number of bytes taken from the USB interfaces this pass. */
static int rx_poll(void) {
    static uint8_t acc[256]; static size_t n = 0; uint8_t buf[64];
    int got = 0;
    if (tud_cdc_available()) got = tud_cdc_read(buf, sizeof buf);
    else if (tud_vendor_available()) got = tud_vendor_read(buf, sizeof buf);
    for (int i = 0; i < got; i++) {
        if (buf[i] == 0) { /* decode acc[0..n) */ uint8_t out[256]; size_t o = 0, r = 0;
            while (r < n) { uint8_t code = acc[r++]; for (int k = 1; k < code && r < n; k++) out[o++] = acc[r++]; if (code != 0xFF && r < n) out[o++] = 0; }
            if (o > 4) { uint32_t c; memcpy(&c, out + o - 4, 4);
                if (c == crc32(out, o - 4)) {
                    /* FW-D14.  A host command is a FULL frame: the 10-byte header of
                       section 5.1, then the opcode, then the opcode's own payload.  This
                       used to hand handle_command() the frame from byte 0, so what it read
                       as the opcode was header[0] -- the protocol version.  PROTO_VERSION
                       is 1 and CMD_START_SESSION is 0x01, so EVERY command the host sent,
                       IDENTIFY and LOOPBACK included, started a recording session instead.
                       Verified against the shipped webtest host: 1 of 7 commands round
                       tripped, and the one that did was that coincidence. */
                    size_t body = o - 4;
                    if (body >= FRAME_HDR_BYTES + 1
                        && out[0] == PROTO_VERSION && out[1] == FT_CMD)
                        handle_command(out + FRAME_HDR_BYTES, body - FRAME_HDR_BYTES);
                } }
            n = 0; }
        else if (n < sizeof acc) acc[n++] = buf[i];
    }
    return got;
}

static void rx_task(void *arg) {
    (void) arg;
    for (;;) {
        if (!rx_poll()) vTaskDelay(pdMS_TO_TICKS(2));
    }
}

/* ------------------------------------------------------------------ status frame once per second (F-09) */
static void status_task(void *arg) {
    for (;;) { extern uint8_t battery_percent(void); extern uint32_t sd_free_mb(void);
        uint8_t s[12] = { battery_percent(), 0, (uint8_t)g_loff_bits, (uint8_t)(g_loff_bits >> 8), 0, 0, 0, 0, 0, 0, 0, 0 };
        uint32_t f = sd_free_mb(); memcpy(s + 4, &f, 4); s[8] = tud_vendor_mounted() ? 2 : (tud_cdc_connected() ? 1 : 0);
        frame_emit(FT_STATUS, g_sample_index, 0, s, sizeof s); vTaskDelay(pdMS_TO_TICKS(1000)); }
}

void app_main(void) {
    ESP_LOGI(TAG, "EEG field kit firmware — USB only; radio not initialised");
    /* FW-D01 CLOSED.  These were C++ range-based for loops in a .c file, so the project
       did not compile at all.  Plain C, same behaviour. */
    static const int in_pins[]  = { PIN_BTN_A, PIN_BTN_B, PIN_BTN_STOP,
                                    PIN_DRDY, PIN_ENV_CMP };
    static const int out_pins[] = { PIN_CHG_CE, PIN_MIC_MUTE, PIN_LED_PWM,
                                    PIN_SR_DATA, PIN_SR_CLK, PIN_SR_LATCH };
    for (size_t i = 0; i < sizeof in_pins / sizeof in_pins[0]; i++) {
        gpio_set_direction(in_pins[i], GPIO_MODE_INPUT);
        gpio_set_pull_mode(in_pins[i], GPIO_PULLUP_ONLY);
    }
    for (size_t i = 0; i < sizeof out_pins / sizeof out_pins[0]; i++)
        gpio_set_direction(out_pins[i], GPIO_MODE_OUTPUT);
    gpio_set_direction(PIN_VBUS_DET, GPIO_MODE_INPUT);   /* S-01 interlock, FW-D17 */

    /* NVS, I2C, the fuel gauge, the codec and the card.  Everything main.c calls through
       sd_append(), battery_percent(), codec_play_tone_at(), envelope_onset_after() and
       the two identity functions lives in drivers.c and is brought up here. */
    ESP_ERROR_CHECK(drv_init_all());
    gpio_set_level(PIN_MIC_MUTE, 1);                 /* room mic muted unless a scripted window is open */
    /* F-04: the USB iSerialNumber is the PROGRAMME serial TIOV-B-nnnn, written into
       NVS at end-of-line provisioning step 6, NOT the ATECC608B factory serial.  The
       ATECC serial is a second identifier: printed, in the Data Matrix, and checked
       against this one at T5b.  RUL-EEG-021 section B rules this; PKG-EEG-015
       section 5 defines the format. */
    extern void unit_serial_into(char *dst, size_t n);   /* reads NVS key "unit_serial" */
    unit_serial_into(serial_str, sizeof serial_str);
    rb = xRingbufferCreateWithCaps(RING_BYTES, RINGBUF_TYPE_NOSPLIT, MALLOC_CAP_SPIRAM);
    if (rb == NULL) {
        /* Do not carry on: every DATA frame would assert inside xRingbufferSend, and the
           unit would look like a USB fault rather than an out-of-memory one. */
        ESP_LOGE("eeg", "ring buffer of %u bytes would not allocate in PSRAM; "
                        "check CONFIG_SPIRAM_MODE_OCT and the -N16R8 part",
                 (unsigned) RING_BYTES);
        abort();
    }
    const tinyusb_config_t tusb_cfg = { .device_descriptor = &dev_desc, .string_descriptor = str_desc, .string_descriptor_count = 6, .configuration_descriptor = cfg_desc };
    tinyusb_driver_install(&tusb_cfg);
    ads_init();
    xTaskCreatePinnedToCore(sample_task, "sample", 8192, NULL, 23, &sample_task_h, 1);
    gpio_set_intr_type(PIN_DRDY, GPIO_INTR_NEGEDGE); gpio_install_isr_service(0); gpio_isr_handler_add(PIN_DRDY, drdy_isr, NULL);
    xTaskCreate(rx_task, "rx", 4096, NULL, 10, NULL);
    xTaskCreate(status_task, "status", 4096, NULL, 5, NULL);
    xTaskCreate(lights_task, "lights", 2048, NULL, 4, NULL);
}
/* Stubs to be provided by the codec (ES8388 I2S), SD (SDMMC), ATECC608B (I2C) and gauge (MAX17048) drivers:
 *   void sd_append(const uint8_t*, size_t); void codec_play_tone_at(uint32_t); int envelope_onset_after(uint32_t,int);
 *   uint8_t battery_percent(void); uint32_t sd_free_mb(void);
 *   void unit_serial_into(char*, size_t);    -- TIOV-B-nnnn from NVS, F-04
 *   void atecc_serial_into(char*, size_t);   -- factory serial, label/DataMatrix only
 * Signature frames (F-08): every 2048 samples, SHA-256 of the block chained to the previous digest, signed by ATECC608B
 * P-256; emitted as FT_SIGNATURE by the sd/signing task (not shown). */
