#ifndef SRC_MODULES_PACKET_UTILS_H_
#define SRC_MODULES_PACKET_UTILS_H_

#include <Arduino.h>

#include "../../config.h"
#include "../nanopb/packet.pb.h"
#include "../nanopb/pb.h"
#include "../nanopb/pb_common.h"
#include "../nanopb/pb_decode.h"
#include "../nanopb/pb_encode.h"

typedef struct StaticFrame {
  uint8_t pixels[PACKET_BUFFER_SIZE];
  int size;
  int brightness;
} StaticFrame;

String formatVersion(const Version& v);

void serialWritePacketHeader(const Header& header);

bool read_ints(pb_istream_t* stream, const pb_field_iter_t* field, void** arg);

Packet decodePacket(uint8_t* buffer, int length);

int encodePacket(uint8_t* buffer, int buffer_size, Packet packet);

Status setESPInfo(Packet* packet);

#endif  // SRC_MODULES_PACKET_UTILS_H_
