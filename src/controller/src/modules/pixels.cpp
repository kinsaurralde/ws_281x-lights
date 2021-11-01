#include "pixels.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

#include "../../config.h"
#include "../nanopb/animation.pb.h"
#include "logger.h"

constexpr int RED = 16711680;
constexpr int GREEN = 65280;
constexpr int BLUE = 255;
constexpr int YELLOW = 16769280;
constexpr int CYAN = 65535;
constexpr int MAGENTA = 16711935;
constexpr int ORANGE = 16737280;
constexpr int PURPLE = 3604735;
constexpr int TURQUOISE = 65335;
constexpr int PINK = 16711735;

constexpr int NUM_COLORS = 10;

static int COLORS[NUM_COLORS] = {RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE, TURQUOISE, PINK};

Pixels::Pixels() : previous_show_time_(0), frame_count_(0) {
  info_ = LEDInfo_init_zero;
  info_.brightness = INIT_BRIGHTNESS;
  info_.num_leds = MAX_LED;
  info_.frame_ms = INIT_FRAME_MS;
  info_.frame_multiplier = 1;
  frame_buffer_.pixel_count = info_.num_leds;
  frame_buffer_.brightness = info_.brightness;
  inc_args_ = IncrementArgs();
  animation_args_ = AnimationArgs_init_zero;
  incrementor = &Pixels::nothing;
}

const FrameBuffer& Pixels::get() { return frame_buffer_; }

void Pixels::setAll(int color) {
  if (color < 0) {
    return;
  }
  for (int i = 0; i < info_.num_leds; i++) {
    setFrameBuffer(i, color);
  }
}

void Pixels::setFrameBuffer(int index, int color) {
  if (color < 0 || index < 0 || index > frame_buffer_.pixel_count) {
    return;
  }
  frame_buffer_.pixels[index] = processColor(color);
}

int Pixels::processColor(int color) {
  if (info_.grb) {
    int r = (color >> 16) & 0xFF;
    int g = (color >> 8) & 0xFF;
    int b = color & 0xFF;
    return g << 16 | r << 8 | b;
  }
  return color;
}

bool Pixels::frameReady(unsigned long time) {
  if (time == 0) {
    return true;
  }
  if (time - info_.frame_ms >= previous_show_time_) {
    previous_show_time_ = time;
    return true;
  }
  return false;
}

void Pixels::setLEDInfo(const LEDInfo& led_info) {
  if (led_info.initialize) {
    info_.initialize = true;
    info_.grb = led_info.grb;
  }
  if (led_info.set_brightness) {
    info_.brightness = led_info.brightness;
  }
  if (led_info.set_num_leds) {
    info_.num_leds = led_info.num_leds;
  }
  if (led_info.set_frame_ms) {
    info_.frame_ms = led_info.frame_ms;
  }
  if (led_info.set_frame_multiplier) {
    info_.frame_multiplier = led_info.frame_multiplier;
  }
}

const LEDInfo& Pixels::getLEDInfo() { return info_; }

const AnimationArgs& Pixels::getAnimationArgs() { return animation_args_; }

void Pixels::increment() {
  this->frame_count_ += info_.frame_multiplier;
  for (int i = 0; i < info_.frame_multiplier; i++) {
    (this->*incrementor)();
  }
  frame_buffer_.brightness = info_.brightness;
}

void Pixels::nothing() {}

void Pixels::shifter() {
  if (inc_args_.reverse) {
    inc_args_.list.increment();
  } else {
    inc_args_.list.decrement();
  }
  int counter = inc_args_.list.counter();
  switch (inc_args_.shift_mode) {
    case ShiftMode::LOOP: {
      for (int i = 0; i < info_.num_leds; i++) {
        int index = (counter + i) % inc_args_.list.size();
        if (index < 0) {
          index += info_.num_leds;
        }
        setFrameBuffer(i, inc_args_.list.get(index));
      }
      break;
    }
    case ShiftMode::BLANK: {
      setFrameBuffer(counter, 0);
      break;
    }
    case ShiftMode::FIRST: {
      setFrameBuffer(counter, frame_buffer_.pixels[inc_args_.reverse ? (info_.num_leds - 1) : 0]);
      break;
    }
  }
}

void Pixels::cycler() { setAll(inc_args_.list.getNext()); }

void Pixels::setFrameBuffer(const FrameBuffer frame_buffer) { frame_buffer_ = frame_buffer; }

void Pixels::animation(const AnimationArgs& args) {
  this->frame_count_ = 0;
  if (args.frame_ms > 0) {
    info_.frame_ms = args.frame_ms;
  }
  if (args.frame_multiplier > 0) {
    info_.frame_multiplier = args.frame_multiplier;
  }
  animation_args_ = args;
  switch (args.type) {
    case AnimationType_NONE:
      break;
    case AnimationType_COLOR:
      color(args);
      break;
    case AnimationType_WIPE:
      wipe(args);
      break;
    case AnimationType_PULSE:
      pulse(args);
      break;
    case AnimationType_RAINBOW:
      rainbow(args);
      break;
    case AnimationType_CYCLE:
      cycle(args);
      break;
    case AnimationType_RANDOM_CYCLE:
      randomCycle(args);
      break;
    case AnimationType_REVERSER:
      reverser(args);
      break;
  }
  Logger::println("Begin animation %d", args.type);
}

void Pixels::color(const AnimationArgs& args) {
  setAll(args.color);
  incrementor = &Pixels::nothing;
  previous_show_time_ = 0;
}

void Pixels::pulse(const AnimationArgs& args) {
  int length = args.length;
  int spacing = args.spacing;
  int num_colors = args.colors.items_count;
  int pattern_size = (num_colors * (length + spacing));
  if (pattern_size <= 0) {
    return;
  }
  int pattern_repeats = (info_.num_leds + (pattern_size - 1)) / pattern_size;
  inc_args_.list.reset();
  inc_args_.list.setSize(pattern_size * pattern_repeats);
  for (int i = 0; i < pattern_repeats; i++) {
    for (int j = 0; j < num_colors; j++) {
      int base_index = i * pattern_size + j * (length + spacing);
      for (int k = 0; k < length; k++) {
        inc_args_.list.set(base_index + k, args.colors.items[j]);
      }
      for (int k = 0; k < spacing; k++) {
        inc_args_.list.set(base_index + length + k, args.background_color);
      }
    }
  }
  inc_args_.shift_mode = ShiftMode::LOOP;
  inc_args_.reverse = args.reverse;
  previous_show_time_ = 0;
  incrementor = &Pixels::shifter;
}

void Pixels::wipe(const AnimationArgs& args) {
  inc_args_.list.reset();
  inc_args_.list.setSize(info_.num_leds);
  setAll(args.background_color);
  setFrameBuffer(args.reverse ? (info_.num_leds - 1) : 0, args.color);
  inc_args_.shift_mode = ShiftMode::FIRST;
  previous_show_time_ = 0;
  incrementor = &Pixels::shifter;
}

void Pixels::rainbow(const AnimationArgs& args) {
  inc_args_.list.reset();
  inc_args_.list.setSize(info_.num_leds);
  for (int i = 0; i < info_.num_leds; i++) {
    int value = rainbowWheel((static_cast<float>(i) / static_cast<float>(info_.num_leds)) * 255);
    inc_args_.list.set(i, value);
    setFrameBuffer(i, value);
  }
  inc_args_.shift_mode = ShiftMode::LOOP;
  previous_show_time_ = 0;
  incrementor = &Pixels::shifter;
}

void Pixels::cycle(const AnimationArgs& args) {
  int steps = args.steps;
  int num_color_changes = args.colors.items_count - 1;
  int list_size = num_color_changes * steps;
  if (list_size > LIST_CAPACITY) {
    steps = LIST_CAPACITY / num_color_changes;
    list_size = num_color_changes * steps;
  }
  inc_args_.list.reset();
  inc_args_.list.setSize(list_size);
  for (int i = 0; i < num_color_changes; i++) {
    for (int j = 0; j < steps; j++) {
      inc_args_.list.set(i * steps + j, mixColors(args.colors.items[i], args.colors.items[i + 1], j * 100.0 / steps));
    }
  }
  setAll(inc_args_.list.get(0));
  previous_show_time_ = 0;
  incrementor = &Pixels::cycler;
}

void Pixels::randomCycle(const AnimationArgs& args) {
  int previous_index = 0;
  int list_size = 20;
  inc_args_.list.reset();
  inc_args_.list.setSize(list_size);
  for (int i = 0; i < list_size; i++) {
    int index = 0;
    do {
      index = random() % NUM_COLORS;
    } while (index == previous_index);
    previous_index = index;
    inc_args_.list.set(i, COLORS[index]);
  }
  setAll(inc_args_.list.get(0));
  incrementor = &Pixels::cycler;
  previous_show_time_ = 0;
}

void Pixels::reverser(const AnimationArgs& args) {
  if (args.reverse) {
    inc_args_.reverse = !inc_args_.reverse;
  }
  if (args.reverse2) {
    int last_pixel = info_.num_leds - 1;
    for (int i = 0; i < info_.num_leds / 2; i++) {
      int temp = frame_buffer_.pixels[i];
      setFrameBuffer(i, frame_buffer_.pixels[last_pixel - i]);
      setFrameBuffer(last_pixel - i, temp);
    }
  }
}

int Pixels::rainbowWheel(int pos) {
  if (pos < 85) {
    return rgbCombine(pos * 3, 255 - pos * 3, 0);
  }
  if (pos < 170) {
    pos -= 85;
    return rgbCombine(255 - pos * 3, 0, pos * 3);
  }
  pos -= 170;
  return rgbCombine(0, pos * 3, 255 - pos * 3);
}

unsigned int Pixels::rgbCombine(unsigned int r, unsigned int g, unsigned int b) {
  return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF);
}

unsigned int Pixels::rgbGetR(unsigned int value) { return (value >> 16) & 0xFF; }

unsigned int Pixels::rgbGetG(unsigned int value) { return (value >> 8) & 0xFF; }

unsigned int Pixels::rgbGetB(unsigned int value) { return (value >> 0) & 0xFF; }

int Pixels::mixColors(int color_1, int color_2, int percent) {
  if (color_1 < 0 || color_2 < 0) {
    return -1;
  }
  int r_diff = ((int)rgbGetR(color_2) - (int)rgbGetR(color_1)) * (percent / 100.0);                    // NOLINT
  int g_diff = ((int)rgbGetG(color_2) - (int)rgbGetG(color_1)) * (percent / 100.0);                    // NOLINT
  int b_diff = ((int)rgbGetB(color_2) - (int)rgbGetB(color_1)) * (percent / 100.0);                    // NOLINT
  return rgbCombine(rgbGetR(color_1) + r_diff, rgbGetG(color_1) + g_diff, rgbGetB(color_1) + b_diff);  // NOLINT
}
