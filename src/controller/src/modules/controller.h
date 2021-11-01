#ifndef SRC_MODULES_CONTROLLER_H_
#define SRC_MODULES_CONTROLLER_H_

#include "../nanopb/packet.pb.h"
#include "pixels.h"

typedef struct EspInfo {
  bool is_request;
  uint32_t heap_free;
  uint32_t heap_frag;
  uint32_t sketch_size;
  uint32_t free_sketch_size;
  uint32_t flash_chip_size;
  uint32_t flash_chip_speed;
  uint32_t cpu_freq;
  uint32_t cycle_count;
  uint32_t supply_voltage;
  uint32_t chip_id;
  uint32_t flash_id;
  uint32_t flash_crc;
} EspInfo;

class Controller {
 public:
  Controller(){};

  Pixels& getPixels();
  const FrameBuffer& getFrameBuffer();
  bool updatePixels(unsigned long millis);

  Status handlePacket(Packet& packet);

 private:
  Pixels pixels_;

  Status beginAnimation(Packet& packet);
  Status setFrameBuffer(Packet& packet);
  Status setLedInfo(Packet& packet);
  Status getVersion(Packet& packet);
  Status getESPInfo(Packet* packet);
};

#endif  // SRC_MODULES_CONTROLLER_H_