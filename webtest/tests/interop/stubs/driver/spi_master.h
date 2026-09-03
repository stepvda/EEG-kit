#pragma once
#include <stdint.h>
#include <stddef.h>
typedef void* spi_device_handle_t;
typedef struct { size_t length; const void* tx_buffer; void* rx_buffer; size_t rxlength; uint32_t flags; uint8_t tx_data[4]; uint8_t rx_data[4]; void* user; uint16_t cmd; uint64_t addr; } spi_transaction_t;
typedef int esp_err_t;
static inline esp_err_t spi_device_polling_transmit(spi_device_handle_t h, spi_transaction_t* t){(void)h;(void)t;return 0;}
static inline esp_err_t spi_device_transmit(spi_device_handle_t h, spi_transaction_t* t){(void)h;(void)t;return 0;}
typedef struct { int mosi_io_num, miso_io_num, sclk_io_num, quadwp_io_num, quadhd_io_num; int max_transfer_sz; } spi_bus_config_t;
typedef struct { int clock_speed_hz, mode, spics_io_num, queue_size, command_bits, address_bits, flags; void* pre_cb; void* post_cb; int cs_ena_pretrans, cs_ena_posttrans, input_delay_ns, duty_cycle_pos; } spi_device_interface_config_t;
#define SPI2_HOST 1
#define SPI3_HOST 2
#define SPI_DMA_CH_AUTO 3
static inline esp_err_t spi_bus_initialize(int h,const spi_bus_config_t*c,int d){(void)h;(void)c;(void)d;return 0;}
static inline esp_err_t spi_bus_add_device(int h,const spi_device_interface_config_t*c,spi_device_handle_t*o){(void)h;(void)c;*o=(void*)1;return 0;}
