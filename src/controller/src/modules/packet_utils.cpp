#include "packet_utils.h"

#include "logger.h"

void serialWritePacketHeader(const Header& header) {
  Version version = header.version;
  Logger::println("\tPacket:\n\t\tId: %lld\n\t\tStatus: %d\n\t\tTimestamp: %lld\n\t\tVersion: %d.%d.%d", header.id,
                  header.status, header.timestamp_millis, version.major, version.minor, version.patch);
}

Packet decodePacket(uint8_t* buffer, int length) {
  Packet packet = Packet_init_zero;
  pb_istream_t stream = pb_istream_from_buffer(buffer, length);
  pb_decode(&stream, Packet_fields, &packet);
  if (DEBUG_PRINT) {
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
    Logger::println("Encoded Packet of size: %d", message_length);
    if (packet.has_header) {
      serialWritePacketHeader(packet.header);
    }
  }
  return message_length;
}
