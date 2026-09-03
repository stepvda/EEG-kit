/* Simulated peripherals: a powered-on device with a battery, a card and a secure element.
   Implements drivers.h so main.c links against the SAME prototypes the real drivers use. */
#include "drivers.h"
#include <string.h>
#include <stdio.h>

esp_err_t drv_i2c_init(void){ return ESP_OK; }
esp_err_t drv_init_all(void){ return ESP_OK; }
uint8_t   battery_percent(void){ return 87; }
esp_err_t drv_sd_init(void){ return ESP_OK; }
esp_err_t drv_sd_open_session(const char *n){ (void)n; return ESP_OK; }
void      sd_append(const uint8_t *p, size_t n){ (void)p; (void)n; }
void      drv_sd_flush(void){}
uint32_t  sd_free_mb(void){ return 29184; }
esp_err_t drv_codec_init(void){ return ESP_OK; }
void      codec_play_tone_at(uint32_t s){ (void)s; }
int       envelope_onset_after(uint32_t s, int t){ (void)s; (void)t; return 12; }
void      unit_serial_into(char *d, size_t n){ snprintf(d, n, "TIOV-B-0042"); }
void      atecc_serial_into(char *d, size_t n){ snprintf(d, n, "0123B4B5C6D7E8F9EE"); }
esp_err_t drv_atecc_genkey(uint8_t p[64]){ memset(p, 0xA5, 64); return ESP_OK; }
esp_err_t drv_atecc_pubkey(uint8_t p[64]){ memset(p, 0xA5, 64); return ESP_OK; }
bool      drv_atecc_config_locked(void){ return false; }
esp_err_t drv_atecc_lock_config(void){ return ESP_OK; }
esp_err_t drv_nvs_set_str(const char *k, const char *v){ (void)k; (void)v; return ESP_OK; }
esp_err_t drv_nvs_set_blob(const char *k, const void *v, size_t n){ (void)k; (void)v; (void)n; return ESP_OK; }
/* A simulated calibration blob, so the read-back path of CMD_READ_CALIBRATION has
   something to return.  Pattern is byte i = i*3+1 so a wrong offset is obvious. */
esp_err_t drv_nvs_get_blob(const char *k, void *out, size_t *n){
    (void)k;
    size_t len = 512;
    if (*n < len) len = *n;
    for (size_t i = 0; i < len; i++) ((unsigned char*)out)[i] = (unsigned char)(i*3+1);
    *n = len;
    return ESP_OK;
}
bool drv_codec_ready(void){ return true; }
bool drv_atecc_present(void){ return true; }
esp_err_t drv_atecc_write_config(uint8_t b, const uint8_t *m, const uint8_t *i){
    (void)b; (void)m; (void)i; return ESP_OK;
}
