/*
 * drivers.h -- the peripheral API that drivers.c provides and main.c calls.
 *
 * WHY THIS FILE EXISTS
 *
 * It did not, and main.c called seven of these functions with no declaration in scope:
 * sd_free_mb, unit_serial_into, atecc_serial_into, battery_percent, envelope_onset_after,
 * codec_play_tone_at and the drv_* group.  In C99 and later an implicit declaration is an
 * ERROR, not a warning, and ESP-IDF compiles with -Werror=implicit-function-declaration,
 * so the firmware could not have been built as shipped.  Worse than the build failure:
 * where a compiler does accept it, an undeclared function is assumed to return int, so
 * sd_free_mb()'s uint32_t and the pointer returns would have been truncated or misread at
 * runtime with no diagnostic at all.
 *
 * Include it from BOTH main.c and drivers.c, so the compiler checks the definitions
 * against the same prototypes the callers use.
 *
 * Licence: CC BY-SA 4.0.
 */
#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "esp_err.h"

/* ---------------------------------------------------------------- bring-up */
esp_err_t drv_i2c_init(void);
esp_err_t drv_init_all(void);

/* ---------------------------------------------------------------- fuel gauge (MAX17048) */
uint8_t battery_percent(void);

/* ---------------------------------------------------------------- card (one-bit SDMMC) */
esp_err_t drv_sd_init(void);
esp_err_t drv_sd_open_session(const char *name);
void      sd_append(const uint8_t *p, size_t n);
void      drv_sd_flush(void);
uint32_t  sd_free_mb(void);

/* ---------------------------------------------------------------- codec (ES8388) */
esp_err_t drv_codec_init(void);
void      codec_play_tone_at(uint32_t sample_index);

/* Blocks until the envelope comparator asserts after `since_sample`, or the timeout
   expires.  Returns the sample index of the onset, or -1 on timeout. */
int       envelope_onset_after(uint32_t since_sample, int timeout_ms);

/* ---------------------------------------------------------------- identity */
/* Both write a NUL-terminated string of at most n bytes. */
void      unit_serial_into(char *dst, size_t n);
void      atecc_serial_into(char *dst, size_t n);

/* ---------------------------------------------------------------- ATECC608B */
esp_err_t drv_atecc_genkey(uint8_t pub[64]);
esp_err_t drv_atecc_pubkey(uint8_t pub[64]);
/* Write the masked words of one 32-byte config-zone block.  `mask` and `image` are both
   32 bytes; a word with an all-zero mask keeps its factory value.  Must succeed before
   drv_atecc_lock_config() is called -- locking a zone this station never wrote locks
   Microchip's defaults and scraps the part. */
esp_err_t drv_atecc_write_config(uint8_t block, const uint8_t *mask, const uint8_t *image);
bool      drv_atecc_config_locked(void);
esp_err_t drv_atecc_lock_config(void);

/* ---------------------------------------------------------------- what came up */
/* "Is the part fitted and talking", which is NOT the same question as "is it
   provisioned".  CMD_IDENTIFY needs the first; drv_atecc_config_locked() is the second. */
bool      drv_codec_ready(void);
bool      drv_atecc_present(void);

/* ---------------------------------------------------------------- NVS */
esp_err_t drv_nvs_set_str(const char *key, const char *val);
esp_err_t drv_nvs_set_blob(const char *key, const void *val, size_t n);
/* Read a blob back. `n` is in/out: the buffer size going in, the length coming out.
   TST-EEG-004 T6 cannot verify what it wrote without this. */
esp_err_t drv_nvs_get_blob(const char *key, void *out, size_t *n);
