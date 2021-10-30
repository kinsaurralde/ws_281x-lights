#include "packet_utils.h"

#include "logger.h"

String formatVersion(const Version& v) {
  String result;
  result += String(v.major) + ".";
  result += String(v.minor) + ".";
  result += String(v.patch);
  return result;
}

void serialWritePacketHeader(const Header& header) {
  Version version = header.version;
  Serial.println("\tPacket:");
  Serial.print("\t\tId: ");
  Serial.println(header.id);
  Serial.print("\t\tStatus: ");
  Serial.println(header.status);
  Serial.print("\t\tTimestamp (millis): ");
  Serial.println(header.timestamp_millis);
  Serial.print("\t\tVersion: ");
  Serial.println(formatVersion(version));
  Logger::println("\tPacket2:\n\t\tId: %d\n\t\tStatus: %d\n\t\tTimestamp: %d\n\t\tVersion: %d.%d.%d", header.id, header.status, header.timestamp_millis, version.major, version.minor, version.patch);
}

Packet decodePacket(uint8_t* buffer, int length) {
  Packet packet = Packet_init_zero;
  pb_istream_t stream = pb_istream_from_buffer(buffer, length);
  pb_decode(&stream, Packet_fields, &packet);
  if (DEBUG_PRINT) {
    // Serial.print("Decoded Packet of size: ");
    // Serial.println(length);
    // Serial.print("Packet has Payload: ");
    // Serial.println(packet.has_payload);
    if (packet.has_header) {
      serialWritePacketHeader(packet.header);
    }
  }
  return packet;
}

int encodePacket(uint8_t* buffer, int buffer_size, Packet packet) {
  pb_ostream_t ostream = pb_ostream_from_buffer(buffer, buffer_size);
  pb_encode(&ostream, Packet_fields, &packet);
  int message_length = ostream.bytes_written;
  if (DEBUG_PRINT) {
    // Serial.print("Encoded Packet of size: ");
    // Serial.println(message_length);
    Logger::println("Encoded Packet of size: %d", message_length);
    if (packet.has_header) {
      serialWritePacketHeader(packet.header);
    }
  }
  return message_length;
}

Status setESPInfo(Packet* packet) {
  if (packet == nullptr) {
    return Status_ERROR;
  }
  if (!packet->payload.payload.esp_info.is_request) {
    return Status_ARGUMENT_ERROR;
  }
  packet->payload.payload.esp_info.is_request = false;
  packet->payload.payload.esp_info.heap_free = ESP.getFreeHeap();
  packet->payload.payload.esp_info.heap_frag = ESP.getHeapFragmentation();
  packet->payload.payload.esp_info.sketch_size = ESP.getSketchSize();
  packet->payload.payload.esp_info.free_sketch_size = ESP.getFreeSketchSpace();
  packet->payload.payload.esp_info.flash_chip_size = ESP.getFlashChipSize();
  packet->payload.payload.esp_info.flash_chip_speed = ESP.getFlashChipSpeed();
  packet->payload.payload.esp_info.cpu_freq = ESP.getCpuFreqMHz();
  packet->payload.payload.esp_info.cycle_count = ESP.getCycleCount();
  packet->payload.payload.esp_info.supply_voltage = ESP.getVcc();
  packet->payload.payload.esp_info.chip_id = ESP.getChipId();
  packet->payload.payload.esp_info.flash_id = ESP.getFlashChipId();
  packet->payload.payload.esp_info.flash_crc = ESP.checkFlashCRC();
}
