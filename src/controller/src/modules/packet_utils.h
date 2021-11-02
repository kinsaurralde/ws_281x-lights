#ifndef SRC_MODULES_PACKET_UTILS_H_
#define SRC_MODULES_PACKET_UTILS_H_

#include "../../config.h"
#include "../nanopb/packet.pb.h"
#include "../nanopb/pb.h"
#include "../nanopb/pb_common.h"
#include "../nanopb/pb_decode.h"
#include "../nanopb/pb_encode.h"

void serialWritePacketHeader(const Header& header);

Packet decodePacket(uint8_t* buffer, int length);

int encodePacket(uint8_t* buffer, int buffer_size, Packet* packet);

#endif  // SRC_MODULES_PACKET_UTILS_H_
