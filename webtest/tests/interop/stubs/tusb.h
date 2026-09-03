#pragma once
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
/* The harness feeds bytes in through these, and captures what the device writes out. */
uint32_t sim_cdc_avail(void);
uint32_t sim_cdc_read(void*, uint32_t);
uint32_t sim_write_cdc(const void*, uint32_t);
uint32_t sim_write_vnd(const void*, uint32_t);
int sim_vendor_up(void);
#define tud_cdc_available()      sim_cdc_avail()
#define tud_cdc_read(b,n)        sim_cdc_read(b,n)
#define tud_cdc_write(b,n)       sim_write_cdc(b,n)
#define tud_cdc_write_flush()    (0)
#define tud_cdc_connected()      (1)
#define tud_vendor_available()   (0)
#define tud_vendor_read(b,n)     (0)
#define tud_vendor_write(b,n)    sim_write_vnd(b,n)
#define tud_vendor_write_flush() (0)
#define tud_mounted()            (1)
#define tud_vendor_mounted()     sim_vendor_up()
#define tud_cdc_write_available() (64)
/* --- descriptor scaffolding, enough to compile the descriptor tables --- */
typedef struct __attribute__((packed)) { uint8_t bLength, bDescriptorType; uint16_t bcdUSB;
  uint8_t bDeviceClass, bDeviceSubClass, bDeviceProtocol, bMaxPacketSize0;
  uint16_t idVendor, idProduct, bcdDevice; uint8_t iManufacturer, iProduct, iSerialNumber, bNumConfigurations; } tusb_desc_device_t;
#define TUSB_DESC_DEVICE 0x01
#define TUSB_DESC_CONFIGURATION 0x02
#define TUSB_CLASS_MISC 0xEF
#define MISC_SUBCLASS_COMMON 0x02
#define MISC_PROTOCOL_IAD 0x01
#define TUD_CONFIG_DESC_LEN 9
#define TUD_CDC_DESC_LEN 66
#define TUD_VENDOR_DESC_LEN 23
#define TUSB_DESC_CONFIG_ATT_REMOTE_WAKEUP 0x20
#define TUD_CONFIG_DESCRIPTOR(...) 0
#define TUD_CDC_DESCRIPTOR(...) 0
#define TUD_VENDOR_DESCRIPTOR(...) 0
#define portYIELD_FROM_ISR(...) do{}while(0)

#define TUD_BOS_DESC_LEN 5
#define TUD_BOS_WEBUSB_DESC_LEN 24
#define TUD_BOS_MICROSOFT_OS_DESC_LEN 28
#define TUD_BOS_DESCRIPTOR(...) 0
#define TUD_BOS_WEBUSB_DESCRIPTOR(...) 0
#define TUD_BOS_MS_OS_20_DESCRIPTOR(...) 0
#define U16_TO_U8S_LE(x) 0
#define U32_TO_U8S_LE(x) 0
#define MS_OS_20_SET_HEADER_DESCRIPTOR 0
#define MS_OS_20_SUBSET_HEADER_CONFIGURATION 0
#define MS_OS_20_SUBSET_HEADER_FUNCTION 0
#define MS_OS_20_FEATURE_COMPATBLE_ID 0
#define MS_OS_20_FEATURE_REG_PROPERTY 0
#define TUSB_REQ_TYPE_VENDOR 2
#define TUSB_REQ_TYPE_CLASS 1
#define CONTROL_STAGE_SETUP 0
typedef struct { union { uint8_t bmRequestType; struct { uint8_t recipient:5; uint8_t type:2; uint8_t direction:1; } bmRequestType_bit; }; uint8_t bRequest; uint16_t wValue, wIndex, wLength; } tusb_control_request_t;
#define TUSB_DESC_STRING 0x03
static inline bool tud_control_xfer(uint8_t r, const tusb_control_request_t* q, void* b, uint16_t l){(void)r;(void)q;(void)b;(void)l;return true;}
