#include "../config.h"
#include "../src/modules/logger.h"
#include "../src/modules/packet_utils.h"
#include "../src/modules/pixels.h"
#include "../version.h"

#include <iostream>

typedef struct {
  Pixels pixels;
  uint32_t leds[MAX_LED];
  bool grb;
  bool initialized;
} Neopixels;


typedef struct {
  unsigned long last_frame_millis;
  int frame_count;
  int udp_packet_count;
  int http_packet_count;
} Stats;

Neopixels neopixels;
Stats stats;

uint32_t* getLeds() {
  return neopixels.leds;
}

void displayFrameBuffer(const FrameBuffer& frame) {
  for (int i = 0; i < frame.pixel_count && i < MAX_LED; i++) {
    int value = frame.pixels[i];
    if (neopixels.grb) {
      int r = (value >> 8) & 0xFF;
      int g = (value >> 16) & 0xFF;
      int b = value & 0xFF;
      value = r << 16 | g << 8 | b;
    }
    neopixels.leds[i] = (uint32_t)value;
  }
}

void updatePixels(unsigned long millis) {
  if (neopixels.pixels.frameReady(millis)) {
    neopixels.pixels.increment();
    displayFrameBuffer(neopixels.pixels.get());
    stats.frame_count += 1;
    stats.last_frame_millis = millis;
  }
}

Status displayFrame(Packet& packet) {
  Frame frame = packet.payload.payload.frame;
  if (!frame.has_brightness) {
    frame.brightness = Brightness_init_zero;
    frame.brightness.brightness = neopixels.pixels.getLEDInfo().brightness;
  }
  if (frame.pixel_count == 0) {
    return Status_ARGUMENT_ERROR;
  }
  for (int i = 0; i < frame.pixel_count && i < MAX_LED; i++) {
    int index = i / ITEMS_PER_COLOR_BLOCK;
    int offset = (i % ITEMS_PER_COLOR_BLOCK) * BITS_PER_BYTE;
    int r = (frame.red[index] >> offset) & 0xFF;
    int g = (frame.green[index] >> offset) & 0xFF;
    int b = (frame.blue[index] >> offset) & 0xFF;
    int value = r << 16 | g << 8 | b;
    neopixels.leds[i] = (uint32_t)value;
  }
  return Status_GOOD;
}

Status beginAnimation(Packet& packet) {
  neopixels.pixels.animation(packet.payload.payload.animation_args);
  return Status_GOOD;
}

Status handleLEDInfo(Packet& packet) {
  if (packet.payload.payload.led_info.initialize) {
    neopixels.grb = packet.payload.payload.led_info.grb;
    neopixels.initialized = true;
    Logger::good("Initialized");
  }
  neopixels.pixels.setLEDInfo(packet.payload.payload.led_info);
  return Status_GOOD;
}

Status handleVersion(Packet& packet) {
  packet.payload.payload.version.major = MAJOR;
  packet.payload.payload.version.minor = MINOR;
  packet.payload.payload.version.patch = PATCH;
  return Status_GOOD;
}

Status setESPInfo(Packet* packet) {
  if (packet == nullptr) {
    return Status_ERROR;
  }
  if (!packet->payload.payload.esp_info.is_request) {
    return Status_ARGUMENT_ERROR;
  }
  return Status_ESP_ONLY_OPTION;
}

Status handlePacket(Packet& packet) {
  if (!packet.has_payload) {
    return Status_MISSING_PAYLOAD;
  }
  // if (DEBUG_PRINT) {
    Logger::println("Packet payload type: %d", packet.payload.which_payload);
  // }
  Status status = Status_REQUEST;
  switch (packet.payload.which_payload) {
    case Payload_animation_args_tag:
      status = beginAnimation(packet);
      break;
    case Payload_frame_tag:
      status = displayFrame(packet);
      break;
    case Payload_version_tag:
      status = handleVersion(packet);
      break;
    case Payload_led_info_tag:
      status = handleLEDInfo(packet);
      break;
    case Payload_esp_info_tag:
      status = setESPInfo(&packet);
      break;
    default:
      status = Status_MISSING_PAYLOAD;
      break;
  }
  return status;
}
