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
  Controller() : auto_off_time_(0){};

  Pixels& getPixels();
  const FrameBuffer& getFrameBuffer();
  bool updatePixels(uint64_t millis);

  Status handlePacket(Packet* packet, uint64_t millis);

  void setSaveServerIp(void (*callback)(uint16_t));

  uint64_t getAutoOffTime();

 private:
  uint64_t auto_off_time_;
  Pixels pixels_;
  void (*saveServerIp)(uint16_t);

  Status beginAnimation(const Packet& packet, uint64_t millis);
  Status setFrameBuffer(const Packet& packet);
  Status setLedInfo(const Packet& packet);
  static Status getVersion(Packet* packet);
  static Status getESPInfo(Packet* packet);
};

#endif  // SRC_MODULES_CONTROLLER_H_