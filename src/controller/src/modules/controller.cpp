#include "controller.h"

#include <iostream>

#include "../../config.h"
#include "../../version.h"
#include "../nanopb/packet.pb.h"
#include "logger.h"
#include "pixels.h"

#if defined(ESP8266)
#include <Arduino.h>

Status getEspInfo(EspInfo* esp_info) {
  esp_info->is_request = false;
  esp_info->heap_free = ESP.getFreeHeap();
  esp_info->heap_frag = ESP.getHeapFragmentation();
  esp_info->sketch_size = ESP.getSketchSize();
  esp_info->free_sketch_size = ESP.getFreeSketchSpace();
  esp_info->flash_chip_size = ESP.getFlashChipSize();
  esp_info->flash_chip_speed = ESP.getFlashChipSpeed();
  esp_info->cpu_freq = ESP.getCpuFreqMHz();
  esp_info->cycle_count = ESP.getCycleCount();
  esp_info->supply_voltage = ESP.getVcc();
  esp_info->chip_id = ESP.getChipId();
  esp_info->flash_id = ESP.getFlashChipId();
  esp_info->flash_crc = ESP.checkFlashCRC();
  return Status_GOOD;
}
#else
Status getEspInfo(EspInfo* esp_info) { return Status_ESP_ONLY_OPTION; }
#endif

Pixels& Controller::getPixels() { return pixels_; }

const FrameBuffer& Controller::getFrameBuffer() { return pixels_.get(); }

bool Controller::updatePixels(uint64_t millis) {
  if (pixels_.frameReady(millis)) {
    pixels_.increment();
    return true;
  }
  return false;
}

Status Controller::handlePacket(Packet* packet) {
  if (!packet->has_payload) {
    return Status_MISSING_PAYLOAD;
  }
  Logger::println("Packet payload type: %d", packet->payload.which_payload);
  Status status = Status_REQUEST;
  switch (packet->payload.which_payload) {
    case Payload_animation_args_tag:
      status = beginAnimation(*packet);
      break;
    case Payload_frame_tag:
      // status = setFrameBuffer(packet);
      status = Status_NOT_IMPLEMENTED;
      break;
    case Payload_version_tag:
      status = getVersion(packet);
      break;
    case Payload_led_info_tag:
      status = setLedInfo(*packet);
      break;
    case Payload_esp_info_tag:
      status = getESPInfo(packet);
      break;
    default:
      status = Status_MISSING_PAYLOAD;
      break;
  }
  return status;
}

void Controller::setSaveServerIp(void (*callback)(uint16_t)) { saveServerIp = callback; }

Status Controller::beginAnimation(const Packet& packet) {
  pixels_.animation(packet.payload.payload.animation_args);
  return Status_GOOD;
}

Status Controller::setFrameBuffer(const Packet& packet) {
  FrameBuffer frame_buffer = FrameBuffer();
  Frame frame = packet.payload.payload.frame;
  if (frame.pixel_count == 0) {
    return Status_ARGUMENT_ERROR;
  }
  if (frame.has_brightness) {
    frame.brightness = Brightness_init_zero;
    frame.brightness.brightness = pixels_.getLEDInfo().brightness;
  }
  frame_buffer.brightness = frame.brightness.brightness;
  for (int i = 0; i < frame.pixel_count && i < MAX_LED; i++) {
    int index = i / ITEMS_PER_COLOR_BLOCK;
    int offset = (i % ITEMS_PER_COLOR_BLOCK) * BITS_PER_BYTE;
    int r = (frame.red[index] >> offset) & 0xFF;
    int g = (frame.green[index] >> offset) & 0xFF;
    int b = (frame.blue[index] >> offset) & 0xFF;
    int value = r << 16 | g << 8 | b;
    frame_buffer.pixels[i] = static_cast<uint32_t>(value);
  }
  return Status_GOOD;
}

Status Controller::setLedInfo(const Packet& packet) {
  if (packet.payload.payload.led_info.initialize) {
    if (saveServerIp != nullptr) {
      saveServerIp(packet.payload.payload.led_info.initialize_port);
    }
    Logger::good("Initialized");
  }
  pixels_.setLEDInfo(packet.payload.payload.led_info);
  return Status_GOOD;
}

Status Controller::getVersion(Packet* packet) {
  packet->payload.payload.version.major = MAJOR;
  packet->payload.payload.version.minor = MINOR;
  packet->payload.payload.version.patch = PATCH;
  return Status_GOOD;
}

Status Controller::getESPInfo(Packet* packet) {
  if (packet == nullptr) {
    return Status_ERROR;
  }
  if (!packet->payload.payload.esp_info.is_request) {
    return Status_ARGUMENT_ERROR;
  }
  EspInfo esp_info = EspInfo();
  return getEspInfo(&esp_info);
}
