idf_component_register(
    SRCS "main.c" "drivers.c"
    INCLUDE_DIRS "."
    # `driver` and NOT `esp_driver_i2c`.  The I2C driver was split into its own component
    # at ESP-IDF 5.3; at 5.2, which idf_component.yml also allows, `esp_driver_i2c` does
    # not exist and the build stops at configure with "component could not be found".
    # `driver` provides I2C on both, so it is the requirement that spans the pinned range.
    REQUIRES driver esp_timer esp_psram sdmmc fatfs esp_partition app_update
             nvs_flash
    PRIV_REQUIRES esp_tinyusb
)
