/*
 * drivers.c -- the peripheral drivers main.c calls.
 *
 * FW-D02 to FW-D04, and the link failure they caused.  main.c declared seven functions and
 * nothing defined them, so the project did not link even after it compiled:
 *
 *     sd_append  sd_free_mb  battery_percent  codec_play_tone_at
 *     envelope_onset_after  unit_serial_into  atecc_serial_into
 *
 * Four devices sit behind those seven names: the microSD card on one-bit SDMMC, the
 * MAX17048 fuel gauge on I2C, the ES8388 codec on I2C plus I2S, and the ATECC608B secure
 * element on the same I2C bus.  Pin assignments come from board_pins.h, which is generated
 * from design.py, so they cannot drift from the board.
 *
 * WHAT IS REAL HERE AND WHAT IS NOT.  The bus plumbing, the register sequences, the card
 * mount, the NVS access and the error handling are real and complete.  Two things are
 * deliberately partial and say so at their definition:
 *
 *   codec_play_tone_at()   queues a tone and returns; the sample-accurate scheduling
 *                          against the ADS1299 sample clock (E-13) is not written.
 *   envelope_onset_after() reads the latched comparator bit, which is the hardware half of
 *                          E-12; the sub-sample interpolation is not written.
 *
 * Neither has ever run on hardware.  Nothing in this file has.
 *
 * Licence: MIT.
 */
#include <string.h>
#include <stdio.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/i2c.h"
#include "driver/sdmmc_host.h"
#include "esp_vfs_fat.h"
#include "sdmmc_cmd.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "esp_log.h"
#include "esp_check.h"

#include "board_pins.h"
#include "drivers.h"   /* check these definitions against the prototypes main.c uses */

static const char *TAG = "drv";

/* I2C addresses, 7-bit.  ICD-EEG-006 section 2.6 carries the bus map. */
#define ADDR_MAX17048   0x36
#define ADDR_ES8388     0x10
#define ADDR_ATECC608B  0x60

#define I2C_PORT        I2C_NUM_0
#define I2C_HZ          100000
#define SD_MOUNT        "/sdcard"

/* Defined with the NVS helpers below; declared here because unit_serial_into() reads the
   unit serial back long before that section of the file. */
static esp_err_t nvs_open_for(const char *key, nvs_open_mode_t mode, nvs_handle_t *h,
                              const char **part_out);
static bool s_i2c_up;
/* CMD_IDENTIFY advertises what the unit HAS.  It used to derive the codec bit from
 * nothing at all (it was never set) and the ATECC bit from whether the config zone
 * was LOCKED, so a sound board with an unprovisioned ATECC reported neither. */
static bool s_codec_up;
static bool s_atecc_present;
static bool s_sd_up;
static sdmmc_card_t *s_card;
static FILE *s_session;

/* ------------------------------------------------------------------ I2C */
esp_err_t drv_i2c_init(void)
{
    if (s_i2c_up)
        return ESP_OK;
    i2c_config_t c = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = PIN_I2C_SDA,
        .scl_io_num = PIN_I2C_SCL,
        .sda_pullup_en = GPIO_PULLUP_DISABLE,   /* R94/R95 4k7 are fitted on the carrier */
        .scl_pullup_en = GPIO_PULLUP_DISABLE,
        .master.clk_speed = I2C_HZ,
    };
    ESP_RETURN_ON_ERROR(i2c_param_config(I2C_PORT, &c), TAG, "i2c config");
    ESP_RETURN_ON_ERROR(i2c_driver_install(I2C_PORT, c.mode, 0, 0, 0), TAG, "i2c install");
    s_i2c_up = true;
    return ESP_OK;
}

static esp_err_t i2c_rd(uint8_t addr, uint8_t reg, uint8_t *buf, size_t n)
{
    if (!s_i2c_up)
        return ESP_ERR_INVALID_STATE;
    return i2c_master_write_read_device(I2C_PORT, addr, &reg, 1, buf, n,
                                        pdMS_TO_TICKS(50));
}

static esp_err_t i2c_wr(uint8_t addr, uint8_t reg, uint8_t val)
{
    if (!s_i2c_up)
        return ESP_ERR_INVALID_STATE;
    uint8_t b[2] = { reg, val };
    return i2c_master_write_to_device(I2C_PORT, addr, b, sizeof b, pdMS_TO_TICKS(50));
}

/* ------------------------------------------------------------------ MAX17048 fuel gauge */
uint8_t battery_percent(void)
{
    uint8_t r[2];
    /* SOC register 0x04: 1/256 % per LSB. */
    if (i2c_rd(ADDR_MAX17048, 0x04, r, 2) != ESP_OK)
        return 0xFF;                    /* 0xFF means "not known", not "full" */
    unsigned pct = r[0];                /* high byte is whole percent */
    return pct > 100 ? 100 : (uint8_t) pct;
}

/* ------------------------------------------------------------------ microSD, one-bit SDMMC
 *
 * One-bit, not four: GPIO35/36/37 carry the octal PSRAM on the -N16R8 and are not
 * connected, so D1-D3 do not exist on this carrier (ECO-EEG-009, board_pins.h).
 */
esp_err_t drv_sd_init(void)
{
    if (s_sd_up)
        return ESP_OK;
    sdmmc_host_t host = SDMMC_HOST_DEFAULT();
    host.flags = SDMMC_HOST_FLAG_1BIT;
    host.max_freq_khz = SDMMC_FREQ_DEFAULT;

    sdmmc_slot_config_t slot = SDMMC_SLOT_CONFIG_DEFAULT();
    slot.width = 1;
    slot.clk = PIN_SD_CLK;
    slot.cmd = PIN_SD_CMD;
    slot.d0  = PIN_SD_D0;
    slot.flags = SDMMC_SLOT_FLAG_INTERNAL_PULLUP;

    esp_vfs_fat_sdmmc_mount_config_t mnt = {
        .format_if_mount_failed = false,     /* never silently erase a session card */
        .max_files = 4,
        .allocation_unit_size = 32 * 1024,
    };
    esp_err_t e = esp_vfs_fat_sdmmc_mount(SD_MOUNT, &host, &slot, &mnt, &s_card);
    if (e != ESP_OK) {
        ESP_LOGE(TAG, "microSD mount failed: %s", esp_err_to_name(e));
        return e;
    }
    s_sd_up = true;
    return ESP_OK;
}

esp_err_t drv_sd_open_session(const char *name)
{
    if (!s_sd_up)
        return ESP_ERR_INVALID_STATE;
    char path[64];
    snprintf(path, sizeof path, SD_MOUNT "/%s.eeg", name);
    s_session = fopen(path, "ab");
    return s_session ? ESP_OK : ESP_FAIL;
}

/* The authoritative copy of the session (E-20).  Appends are buffered by the VFS; the
 * caller flushes at block boundaries. */
void sd_append(const uint8_t *p, size_t n)
{
    if (s_session && p && n)
        fwrite(p, 1, n, s_session);
}

void drv_sd_flush(void)
{
    if (s_session)
        fflush(s_session);
}

uint32_t sd_free_mb(void)
{
    if (!s_sd_up || !s_card)
        return 0;
    FATFS *fs;
    DWORD free_clusters;
    if (f_getfree("0:", &free_clusters, &fs) != FR_OK)
        return 0;
    uint64_t free_bytes = (uint64_t) free_clusters * fs->csize * FF_MAX_SS;
    return (uint32_t) (free_bytes / (1024 * 1024));
}

/* ------------------------------------------------------------------ ES8388 codec
 *
 * Minimum viable init: power up, I2S slave, 16-bit, headphone out enabled at a level the
 * firmware clamps.  E-29 caps the acoustic output at 100 dB SPL and that clamp is applied
 * here, in the one place the level is set, rather than trusted to the host.
 */
#define ES8388_HP_MAX 0x1E        /* -3 dB of full scale; see FW-EEG-001 section 5.9 */

esp_err_t drv_codec_init(void)
{
    static const uint8_t seq[][2] = {
        { 0x00, 0x80 },   /* reset */
        { 0x00, 0x00 },
        { 0x01, 0x58 },   /* power management, both DACs on */
        { 0x02, 0xF3 },
        { 0x08, 0x00 },   /* I2S slave */
        { 0x04, 0x3C },   /* DAC power up, both channels */
        { 0x17, 0x18 },   /* 16-bit I2S */
        { 0x18, 0x02 },
        { 0x1A, 0x00 },   /* DAC volume, 0 dB */
        { 0x1B, 0x00 },
        { 0x26, ES8388_HP_MAX },
        { 0x27, ES8388_HP_MAX },
        { 0x02, 0x00 },   /* release the DAC state machine */
    };
    for (size_t i = 0; i < sizeof seq / sizeof seq[0]; i++) {
        esp_err_t e = i2c_wr(ADDR_ES8388, seq[i][0], seq[i][1]);
        if (e != ESP_OK) {
            ESP_LOGE(TAG, "ES8388 register 0x%02X: %s", seq[i][0], esp_err_to_name(e));
            return e;
        }
        vTaskDelay(pdMS_TO_TICKS(1));
    }
    s_codec_up = true;
    return ESP_OK;
}

/* PARTIAL, and it must not be mistaken for finished.
 *
 * E-13 wants the tone to start on a NAMED SAMPLE INDEX, so that the stimulus and the EEG
 * share one clock.  This queues the request and returns; the I2S write happens in the
 * audio task on the next buffer boundary, which is within a millisecond or two, not within
 * a sample.  Closing it needs the I2S DMA descriptor chain to be armed from the DRDY ISR.
 * Until then T13 measures what this actually achieves rather than what E-13 asks for.
 */
QueueHandle_t drv_tone_q;

void codec_play_tone_at(uint32_t sample_index)
{
    if (drv_tone_q)
        xQueueSend(drv_tone_q, &sample_index, 0);
}

/* PARTIAL, same warning.
 *
 * The hardware half of E-12 is real: U7's output is latched in the DRDY ISR and carried as
 * an aux bit, so the onset is known to within one sample.  Interpolating WITHIN the sample
 * from the envelope slope is not written, so this returns the latched sample index and a
 * zero sub-sample offset.
 */
extern volatile uint32_t g_onset_sample;      /* written by drdy_isr() in main.c */
extern volatile uint8_t  g_onset_valid;

int envelope_onset_after(uint32_t since_sample, int timeout_ms)
{
    const int step = 5;
    for (int waited = 0; waited <= timeout_ms; waited += step) {
        if (g_onset_valid && g_onset_sample >= since_sample)
            return (int) (g_onset_sample - since_sample);
        vTaskDelay(pdMS_TO_TICKS(step));
    }
    return -1;                                 /* no onset inside the window */
}

/* ------------------------------------------------------------------ identity
 *
 * Two different identifiers, and confusing them is the defect the package spent a revision
 * correcting.  RUL-EEG-021 section B rules it:
 *
 *   unit_serial_into()   TIOV-B-nnnn, the PROGRAMME serial, written into NVS at
 *                        end-of-line provisioning.  This is the USB iSerialNumber (F-04)
 *                        and it is what the browser's persistent authorisation binds to.
 *   atecc_serial_into()  the ATECC608B's nine-byte factory serial.  Printed on the label
 *                        and in the Data Matrix so a swapped secure element is detectable.
 *                        NOT the descriptor string.
 */
void unit_serial_into(char *dst, size_t n)
{
    if (!dst || n == 0)
        return;
    strncpy(dst, "TIOV-B-0000", n - 1);        /* until provisioned */
    dst[n - 1] = 0;

    nvs_handle_t h;
    if (nvs_open_for("unit_serial", NVS_READONLY, &h, NULL) != ESP_OK)
        return;
    size_t len = n;
    nvs_get_str(h, "unit_serial", dst, &len);  /* leaves the default on failure */
    nvs_close(h);
}

void atecc_serial_into(char *dst, size_t n)
{
    if (!dst || n == 0)
        return;
    dst[0] = 0;
    /* SN[0:3] at word 0 and SN[4:8] at word 2 of the config zone.  Read command 0x02,
     * param1 = 0x00 (config zone), 4 bytes at a time. */
    uint8_t sn[9] = { 0 };
    uint8_t buf[4];
    if (i2c_rd(ADDR_ATECC608B, 0x00, buf, 4) != ESP_OK)
        return;
    memcpy(sn, buf, 4);
    if (i2c_rd(ADDR_ATECC608B, 0x02, buf, 4) != ESP_OK)
        return;
    memcpy(sn + 4, buf, 4);
    sn[8] = 0xEE;

    s_atecc_present = true;   /* it answered both config reads */

    static const char hex[] = "0123456789ABCDEF";
    size_t w = 0;
    for (size_t i = 0; i < sizeof sn && w + 2 < n; i++) {
        dst[w++] = hex[sn[i] >> 4];
        dst[w++] = hex[sn[i] & 0x0F];
    }
    dst[w] = 0;
}

/* ------------------------------------------------------------------ bring-up */
esp_err_t drv_init_all(void)
{
    esp_err_t e = nvs_flash_init();
    if (e == ESP_ERR_NVS_NO_FREE_PAGES || e == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        e = nvs_flash_init();
    }
    ESP_RETURN_ON_ERROR(e, TAG, "nvs");
    ESP_RETURN_ON_ERROR(drv_i2c_init(), TAG, "i2c");

    drv_tone_q = xQueueCreate(4, sizeof(uint32_t));

    /* The card and the codec are not fatal at boot: a unit with no card still enumerates
     * and streams, and TST-EEG-004 T20 is the step that fails if the card is absent. */
    if (drv_sd_init() != ESP_OK)
        ESP_LOGW(TAG, "continuing without microSD; E-20's authoritative copy is not being written");
    if (drv_codec_init() != ESP_OK)
        ESP_LOGW(TAG, "continuing without the codec; no stimulus audio");
    return ESP_OK;
}

/* ------------------------------------------------------------------ ATECC608B, provisioning
 *
 * Enough of the ATECC608B command set for end-of-line provisioning (F-18), and no more.
 * The parts that matter for the study are: a P-256 key pair that never leaves the device,
 * its public half exported once, and a config zone locked so the key cannot be replaced in
 * the field.
 *
 * The wire protocol is the ATECC's I2C command packet: word address 0x03, then
 * [count][opcode][param1][param2 lo][param2 hi][data...][crc lo][crc hi], then a wait, then
 * a read of [count][data...][crc lo][crc hi].  CRC-16/ATECC is the polynomial below.
 *
 * NEVER RUN ON HARDWARE.  The sequences follow the datasheet; the timings are the datasheet
 * maxima rather than measured.  T6 is the step that proves this works.
 */
static uint16_t atecc_crc16(const uint8_t *p, size_t n)
{
    uint16_t crc = 0;
    for (size_t i = 0; i < n; i++) {
        for (uint8_t sh = 0x01; sh > 0x00; sh <<= 1) {
            uint8_t d = (p[i] & sh) ? 1 : 0;
            uint8_t c = (crc >> 15) ? 1 : 0;
            crc <<= 1;
            if (d != c)
                crc ^= 0x8005;
        }
    }
    return crc;
}

static esp_err_t atecc_cmd(uint8_t opcode, uint8_t p1, uint16_t p2,
                           const uint8_t *data, size_t dlen,
                           uint8_t *resp, size_t rlen, int wait_ms)
{
    uint8_t pkt[8 + 64];
    size_t count = 7 + dlen;                 /* count..crc inclusive */
    if (count > sizeof pkt - 1)
        return ESP_ERR_INVALID_SIZE;
    size_t i = 0;
    pkt[i++] = 0x03;                         /* word address: command */
    pkt[i++] = (uint8_t) count;
    pkt[i++] = opcode;
    pkt[i++] = p1;
    pkt[i++] = p2 & 0xFF;
    pkt[i++] = p2 >> 8;
    if (data && dlen) { memcpy(pkt + i, data, dlen); i += dlen; }
    uint16_t crc = atecc_crc16(pkt + 1, count - 2);
    pkt[i++] = crc & 0xFF;
    pkt[i++] = crc >> 8;

    ESP_RETURN_ON_ERROR(i2c_master_write_to_device(I2C_PORT, ADDR_ATECC608B, pkt, i,
                                                   pdMS_TO_TICKS(50)),
                        TAG, "atecc write");
    vTaskDelay(pdMS_TO_TICKS(wait_ms));

    uint8_t in[4 + 64];
    size_t want = rlen + 3;
    if (want > sizeof in)
        return ESP_ERR_INVALID_SIZE;
    ESP_RETURN_ON_ERROR(i2c_master_read_from_device(I2C_PORT, ADDR_ATECC608B, in, want,
                                                    pdMS_TO_TICKS(50)),
                        TAG, "atecc read");
    if (in[0] != want)
        return ESP_ERR_INVALID_RESPONSE;
    if (atecc_crc16(in, want - 2) != (uint16_t) (in[want - 2] | (in[want - 1] << 8)))
        return ESP_ERR_INVALID_CRC;
    if (resp && rlen)
        memcpy(resp, in + 1, rlen);
    return ESP_OK;
}

#define ATECC_SLOT_KEY 0        /* the device key lives in slot 0 and never leaves it */

esp_err_t drv_atecc_genkey(uint8_t pub[64])
{
    /* GenKey, mode 0x04 = create a new private key and return the public half. */
    return atecc_cmd(0x40, 0x04, ATECC_SLOT_KEY, NULL, 0, pub, 64, 115);
}

esp_err_t drv_atecc_pubkey(uint8_t pub[64])
{
    /* GenKey, mode 0x00 = return the public key of an existing private key. */
    return atecc_cmd(0x40, 0x00, ATECC_SLOT_KEY, NULL, 0, pub, 64, 115);
}

bool drv_atecc_config_locked(void)
{
    uint8_t w[4];
    /* Read, zone 0 (config), word 21: LockConfig is byte 87 = word 21 byte 3. */
    if (atecc_cmd(0x02, 0x00, 21, NULL, 0, w, 4, 5) != ESP_OK)
        return false;
    return w[3] == 0x00;                     /* 0x55 = unlocked, 0x00 = locked */
}

esp_err_t drv_atecc_write_config(uint8_t block, const uint8_t *mask, const uint8_t *image)
{
    /* Write the bytes of ONE 32-byte config-zone block that `mask` selects.
     *
     * The ATECC608B config zone is written 4 bytes at a time before it is locked, so a
     * block is eight Write commands.  The mask exists because most of the zone is
     * Microchip's and must not be touched: the provisioning station holds a template and
     * a mask, and only the masked words are ours to set.  A word is written only if the
     * mask has any byte of it set, so an all-zero mask word leaves the factory value.
     *
     * Zone 0x00 is the config zone; bit 7 clear selects a 4-byte write.  The address for
     * a config write is the word index, which is block * 8 + word.
     *
     * IRREVERSIBLE ONCE LOCKED, but a write before locking is not: this is the step that
     * must succeed BEFORE drv_atecc_lock_config() is ever called, and provision.py
     * refuses to lock a zone this station did not write.
     */
    if (!mask || !image)
        return ESP_ERR_INVALID_ARG;
    for (uint8_t word = 0; word < 8; word++) {
        const uint8_t *m = mask + word * 4;
        if (!(m[0] | m[1] | m[2] | m[3]))
            continue;                       /* nothing of ours in this word */
        uint8_t buf[4];
        for (int i = 0; i < 4; i++)
            buf[i] = image[word * 4 + i];
        uint16_t addr = (uint16_t)(block * 8 + word);
        uint8_t r;
        ESP_RETURN_ON_ERROR(atecc_cmd(0x12, 0x00, addr, buf, 4, &r, 1, 45),
                            TAG, "atecc write cfg blk %u word %u", block, word);
    }
    return ESP_OK;
}

esp_err_t drv_atecc_lock_config(void)
{
    /* Lock, mode 0x80 = lock the config zone without a CRC check.  IRREVERSIBLE. */
    uint8_t r;
    return atecc_cmd(0x17, 0x80, 0x0000, NULL, 0, &r, 1, 35);
}

/* ------------------------------------------------------------------ NVS helpers
 *
 * partitions.csv allocates TWO dedicated 32 kB NVS partitions -- `calib` at 0x920000 and
 * `prov` at 0x928000 -- and FW-EEG-001 section 7.4 names the namespaces that live in them,
 * `eegcal` and `eegcfg`.  Every one of these helpers used to open namespace "tiov" in the
 * DEFAULT `nvs` partition instead, so:
 *
 *   - the two dedicated partitions were allocated and never written: 64 kB unused;
 *   - provisioning and calibration landed in the default partition, which is 0x6000 =
 *     24 kB and is shared with system state;
 *   - and a conforming calibration blob CANNOT FIT THERE.  FW-EEG-001 sizes `calib` at
 *     32 kB; the default partition is 24 kB before anything else is stored in it, so the
 *     write would have failed on a full-size calibration set with an out-of-space error
 *     from a partition the documents never said was involved.
 *
 * Each partition is initialised on first use.  A partition that has never been written is
 * empty rather than corrupt, so ESP_ERR_NVS_NO_FREE_PAGES on first open is expected and is
 * handled by erasing that partition alone -- never the default one, which holds state this
 * code did not put there.
 */
#define NVS_PART_CALIB  "calib"
#define NVS_NS_CALIB    "eegcal"
#define NVS_PART_PROV   "prov"
#define NVS_NS_PROV     "eegcfg"

static esp_err_t nvs_part_ready(const char *part)
{
    esp_err_t e = nvs_flash_init_partition(part);
    if (e == ESP_ERR_NVS_NO_FREE_PAGES || e == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_RETURN_ON_ERROR(nvs_flash_erase_partition(part), TAG, "nvs erase %s", part);
        e = nvs_flash_init_partition(part);
    }
    return e;
}

/* Which partition a key belongs in.  `calib` is the calibration set of T6; everything
   else provisioning writes is identity and belongs in `prov`. */
static void nvs_home(const char *key, const char **part, const char **ns)
{
    if (strcmp(key, "calib") == 0) { *part = NVS_PART_CALIB; *ns = NVS_NS_CALIB; }
    else                           { *part = NVS_PART_PROV;  *ns = NVS_NS_PROV;  }
}

static esp_err_t nvs_open_for(const char *key, nvs_open_mode_t mode, nvs_handle_t *h,
                              const char **part_out)
{
    const char *part, *ns;
    nvs_home(key, &part, &ns);
    if (part_out) *part_out = part;
    ESP_RETURN_ON_ERROR(nvs_part_ready(part), TAG, "nvs init %s", part);
    return nvs_open_from_partition(part, ns, mode, h);
}

esp_err_t drv_nvs_set_str(const char *key, const char *val)
{
    nvs_handle_t h;
    const char *part;
    ESP_RETURN_ON_ERROR(nvs_open_for(key, NVS_READWRITE, &h, &part), TAG, "nvs open");
    esp_err_t e = nvs_set_str(h, key, val);
    if (e == ESP_OK)
        e = nvs_commit(h);
    nvs_close(h);
    return e;
}

esp_err_t drv_nvs_set_blob(const char *key, const void *val, size_t n)
{
    nvs_handle_t h;
    const char *part;
    ESP_RETURN_ON_ERROR(nvs_open_for(key, NVS_READWRITE, &h, &part), TAG, "nvs open");
    esp_err_t e = nvs_set_blob(h, key, val, n);
    if (e == ESP_OK)
        e = nvs_commit(h);
    if (e == ESP_ERR_NVS_NOT_ENOUGH_SPACE)
        ESP_LOGE(TAG, "%s does not fit in the %s partition (%u bytes offered)",
                 key, part, (unsigned) n);
    nvs_close(h);
    return e;
}

esp_err_t drv_nvs_get_blob(const char *key, void *out, size_t *n)
{
    nvs_handle_t h;
    ESP_RETURN_ON_ERROR(nvs_open_for(key, NVS_READONLY, &h, NULL), TAG, "nvs open");
    esp_err_t e = nvs_get_blob(h, key, out, n);
    nvs_close(h);
    return e;
}


/* ------------------------------------------------------------------ what came up
 *
 * CMD_IDENTIFY reports the unit's capabilities, and a production tester reads that report
 * to decide whether the board in front of them is complete.  These two answer "is the part
 * fitted and talking", which is a different question from "has it been provisioned".
 */
bool drv_codec_ready(void)
{
    return s_codec_up;
}

bool drv_atecc_present(void)
{
    if (!s_atecc_present) {
        char probe[24];
        atecc_serial_into(probe, sizeof probe);   /* sets s_atecc_present on success */
    }
    return s_atecc_present;
}
