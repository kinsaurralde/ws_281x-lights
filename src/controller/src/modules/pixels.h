#ifndef SRC_MODULES_PIXELS_H_
#define SRC_MODULES_PIXELS_H_

#include "../../config.h"
#include "../modules/framebuffer.h"
#include "../modules/list.h"
#include "../nanopb/animation.pb.h"

enum ShiftMode { BLANK, FIRST, LOOP };

typedef struct IncrementArgs {
  explicit IncrementArgs() : shift_mode(ShiftMode::BLANK), amount(0), reverse(false) {}

  ShiftMode shift_mode;
  int amount;
  bool reverse;
  List list;
} IncrementArgs;

class Pixels {
 public:
  Pixels();

  bool frameReady(uint64_t time);

  void setLEDInfo(const LEDInfo& led_info);
  const LEDInfo& getLEDInfo();
  const AnimationArgs& getAnimationArgs();

  const FrameBuffer& get();
  void increment();
  void setFrameBuffer(FrameBuffer frame_buffer);
  void animation(const AnimationArgs& args);

 private:
  uint64_t previous_show_time_;
  int frame_count_;
  FrameBuffer frame_buffer_;
  LEDInfo info_;
  IncrementArgs inc_args_;
  AnimationArgs animation_args_;
  void (Pixels::*incrementor)(void);

  void setAll(int color);
  void setFrameBuffer(int index, int color);
  int processColor(int color) const;

  static int rainbowWheel(int pos);
  int setPixel(int id, int value);
  static unsigned int rgbCombine(unsigned int r, unsigned int g, unsigned int b);
  static unsigned int rgbGetR(unsigned int value);
  static unsigned int rgbGetG(unsigned int value);
  static unsigned int rgbGetB(unsigned int value);
  static int mixColors(int color_1, int color_2, int percent);

  void nothing();
  void shifter();
  void cycler();

  void color(const AnimationArgs& args);
  void pulse(const AnimationArgs& args);
  void wipe(const AnimationArgs& args);
  void rainbow(const AnimationArgs& args);
  void cycle(const AnimationArgs& args);
  void randomCycle(const AnimationArgs& args);
  void reverser(const AnimationArgs& args);
};

#endif  // SRC_MODULES_PIXELS_H_
