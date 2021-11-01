#ifndef SRC_MODULES_FRAMEBUFFER_H_
#define SRC_MODULES_FRAMEBUFFER_H_

#include "../../config.h"

typedef struct FrameBuffer {
  explicit FrameBuffer() : brightness(INIT_BRIGHTNESS), pixel_count(MAX_LED) { memset(&pixels, 0, pixel_count); }
  int brightness;
  int pixel_count;
  uint32_t pixels[MAX_LED] = {0};
} FrameBuffer;

#endif  // SRC_MODULES_FRAMEBUFFER_H_