#include "structs.h"

#ifndef PIXELS_H
#define PIXELS_H

class Pixels {
   private:
    bool initialized;
    unsigned int num_leds;
    unsigned int previous_show_time;
    unsigned int delay;
    unsigned int brightness;
    unsigned int brightness_hold;
    unsigned int max_brightness;
    unsigned int max_milliwatts;
    unsigned int increment_steps;
    void (Pixels::*incrementor)(void);
    IncrementArgs incArgs;
    Frame data;

    void setAll(int color);

    unsigned int rainbowWheel(unsigned int pos);
    unsigned int rgbCombine(unsigned int r, unsigned int g, unsigned int b);
    unsigned int rgbGetR(unsigned int value);
    unsigned int rgbGetG(unsigned int value);
    unsigned int rgbGetB(unsigned int value);
    unsigned int mixColors(unsigned int color_1, unsigned int color_2, unsigned int percent);

    void nothing();
    void shifter();
    void cycler();

   public:
    Pixels(unsigned int num_leds, unsigned int max_brightness);


    bool canShow(unsigned int ms = 0);
    void setDelay(unsigned int value);
    void setSize(unsigned int size);
    unsigned int size();
    unsigned int getBrightness();
    void setBrightness(unsigned int value);
    void setIncrementSteps(unsigned int value = 1);
    void initialize(unsigned int num_leds, unsigned int milliwatts, unsigned int brightness, unsigned int max_brightness=255);

    Frame* get();
    void increment();

    void color(AnimationArgs args);
    void pulse(AnimationArgs args);
    void wipe(AnimationArgs args);
    void rainbow(AnimationArgs args);
    void cycle(AnimationArgs args);
};

#endif