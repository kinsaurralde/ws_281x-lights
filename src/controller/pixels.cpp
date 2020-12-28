#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "structs.h"
#include "pixels.h"

#if defined (__AVR__)
    #include <Arduino.h>
#else
    #include <iostream>
#endif

#define BRIGHTNESS_MUTLIPLIER 0.5   // value of 0.5 means half brightness

#define RED         16711680
#define GREEN       65280
#define BLUE        255
#define YELLOW      16769280
#define CYAN        65535
#define MAGENTA     16711935
#define ORANGE      16737280
#define PURPLE      3604735
#define TURQUOISE   65335
#define PINK        16711735

#define NUM_COLORS  10 

static unsigned int COLORS[NUM_COLORS] = {RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE, TURQUOISE, PINK};

Pixels::Pixels(unsigned int num_leds, unsigned int max_brightness) : num_leds(num_leds), max_brightness(max_brightness) {
    initialized = false;
    brightness = 100;
    brightness_hold = 100;
    previous_show_time = 0;
    delay = 30;
    increment_steps = 1;
    incrementor = &Pixels::nothing;
    incArgs.list = new List();
    memset(&data, 0, MAX_LED_PER_STRIP);
}

Frame* Pixels::get() {
    return &data;
}

void Pixels::setAll(int color) {
    if (color < 0) {
        return;
    }
    for (unsigned int i = 0; i < num_leds; i++) {
        data.main[i] = color;
    }
}

unsigned int Pixels::rainbowWheel(unsigned int pos) {
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

unsigned int Pixels::rgbGetR(unsigned int value) {
    return (value >> 16) & 0xFF;
}

unsigned int Pixels::rgbGetG(unsigned int value) {
    return (value >> 8) & 0xFF;
}

unsigned int Pixels::rgbGetB(unsigned int value) {
    return (value >> 0) & 0xFF;
}

unsigned int Pixels::mixColors(unsigned int color_1, unsigned int color_2, unsigned int percent) {
    int r_diff = ((int) rgbGetR(color_2) - (int) rgbGetR(color_1)) * (percent / 100.0);
    int g_diff = ((int) rgbGetG(color_2) - (int) rgbGetG(color_1)) * (percent / 100.0);
    int b_diff = ((int) rgbGetB(color_2) - (int) rgbGetB(color_1)) * (percent / 100.0);
    return rgbCombine(rgbGetR(color_1) + r_diff, rgbGetG(color_1) + g_diff, rgbGetB(color_1) + b_diff);
}

bool Pixels::canShow(unsigned int time) {
    if (!initialized) {
        return false;
    }
    if (time - delay >= previous_show_time) {
        previous_show_time = time;
        return true;
    }
    return false;
}

void Pixels::setDelay(unsigned int value) {
    delay = value;
}

unsigned int Pixels::getDelay() {
    return delay;
}

void Pixels::setSize(unsigned int size) {
    if (size > MAX_LED_PER_STRIP) {
        size = MAX_LED_PER_STRIP;
    }
    num_leds = size;
}

unsigned int Pixels::size() {
    return num_leds;
}

 unsigned int Pixels::getBrightness() {
     return brightness;
 }

void Pixels::setBrightness(unsigned int value) {
    value *= BRIGHTNESS_MUTLIPLIER;
    if (value <= 255 && value <= max_brightness) {
        brightness = value;
    } else {
        brightness = max_brightness;
    }
}

void Pixels::setIncrementSteps(unsigned int value) {
    increment_steps = value;
}

void Pixels::initialize(unsigned int num_leds, unsigned int milliwatts, unsigned int brightness, unsigned int max_brightness, bool grb) {
    if (max_brightness <= 255 && max_brightness < this->max_brightness) {
        this->max_brightness = max_brightness;
    }
    this->grb = grb;
    setSize(num_leds);
    setBrightness(brightness);
    initialized = true;
}

bool Pixels::isInitialized() {
    return initialized;
}

bool Pixels::isGRB() {
    return grb;
}

void Pixels::increment() {
    for (unsigned int i = 0; i < increment_steps; i++) {
        (this->*incrementor)();
    }
}

void Pixels::nothing() {
    return;
}

/*
    IncrementArgs:
        arg1:           amount
        arg2:           mode                    (blank / first_pixel / loop) 
        arg6:           reverse                 (true / false)  
        list:           expanded pixels         (required for loop mode)
*/
void Pixels::shifter() {
    unsigned int amount = incArgs.arg1;
    unsigned int mode = incArgs.arg2;
    bool reverse = incArgs.arg6;
    List* temp = incArgs.list;
    unsigned int first_pixel = data.main[incArgs.arg6 ? (num_leds - 1) : 0];
    unsigned int num_expanded_leds = temp->size();
    unsigned int counter = temp->getCounter();
    if (mode == ShiftMode::loop_shift) {
        if (reverse) {
            temp->incrementCounter();
        } else {
            temp->decrementCounter();
        }
        for (unsigned int i = 0; i < num_leds; i++) {
            unsigned int cur = (counter + i) % num_expanded_leds;
            if (cur < 0) {
                cur += num_leds;
            }
            data.main[i] = temp->get(cur);
        }
    } else {
        if (mode == ShiftMode::blank_shift) {
            first_pixel = 0;
        }
        if (mode == ShiftMode::first_pixel_shift) {
            for (unsigned int i = 0; i < amount; i++) {
                unsigned int cur = counter + i;
                if (reverse) {
                    cur = num_leds - 1 - cur;
                }
                if (cur >= 0 && cur < num_leds) {
                    data.main[cur] = first_pixel;
                }
            }
        }
        temp->setCounter(counter + amount);
    }
}

/*
    IncrementArgs:
        colors:         color list and counter
*/
void Pixels::cycler() {
    setAll(incArgs.list->getNext());
}

void Pixels::animation(AnimationArgs args) {
    switch (args.animation) {
        case Animation::color:
            color(args);
            break;
        case Animation::wipe:
            wipe(args);
            break;
        case Animation::pulse:
            pulse(args);
            break;
        case Animation::rainbow:
            rainbow(args);
            break;
        case Animation::cycle:
            cycle(args);
            break;
        case Animation::randomCycle:
            randomCycle(args);
            break;
        case Animation::reverser:
            reverser(args);
            break;
    }
}

/*
    AnimationArgs:
        color:          color
*/
void Pixels::color(AnimationArgs args) {
    setAll(args.color);
    incrementor = &Pixels::nothing;
    previous_show_time = 0;
}

/*
    AnimationArgs:
        colors:         list of pulse colors
        color_bg:       background color
        arg1:           length
        arg2:           spacing length
        arg3:           shifter amount
        arg4:           expanded size           ( < num_leds if not used)
        arg6:           reverse                 (true / false)     
*/
void Pixels::pulse(AnimationArgs args) {
    resetIncArgs(incArgs, 0, false);
    unsigned int length = args.arg1;
    unsigned int spacing_length = args.arg2;
    unsigned int counter = length;
    unsigned int counter_bg = spacing_length;
    unsigned int expanded_size = args.arg4 > 0 ? args.arg4 : num_leds;
    delete incArgs.list;
    incArgs.list = new List(expanded_size);
    args.colors->setCounter(0);
    for (unsigned int i = 0; i < expanded_size; i++) {
        int color = -1;
        if (counter > 0) {
            color = args.colors->getCurrent();
            counter -= 1;
        } else if (counter_bg == 0) {
            args.colors->incrementCounter();
            color = args.colors->getCurrent();
            counter = length - 1;
            counter_bg = spacing_length;
        } else {
            if (args.color_bg >= 0) {
                color = args.color_bg;
            }
            counter_bg -= 1;
        }
        if (color >= 0) {
            incArgs.list->set(i, color);
            if (i < num_leds) {
                data.main[i] = color;
            }
        }   
    }
    incArgs.arg1 = args.arg3;
    incArgs.arg2 = ShiftMode::loop_shift;
    incArgs.arg6 = args.arg6;
    incrementor = &Pixels::shifter;
}

/*
    AnimationArgs:
        color:          wipe color
        color_bg:       background color
        arg1:           steps
        arg6:           reverse
*/
void Pixels::wipe(AnimationArgs args) {
    resetIncArgs(incArgs, 0, false);
    delete incArgs.list;
    incArgs.list = new List(num_leds);
    setAll(args.color_bg);
    data.main[args.arg6 ? (num_leds - 1) : 0] = args.color;
    incArgs.arg1 = args.arg1;
    incArgs.arg2 = ShiftMode::first_pixel_shift;
    incArgs.arg6 = args.arg6;
    incrementor = &Pixels::shifter;
}

/*
    AnimationArgs:
        arg3:           shifter amount
        arg6:           reverse                 (true / false)     
*/
void Pixels::rainbow(AnimationArgs args) {
    resetIncArgs(incArgs, 0, false);
    delete incArgs.list;
    incArgs.list = new List(num_leds);
    for (unsigned int i = 0; i < num_leds; i++) {
        data.main[i] = rainbowWheel(((float)i / (float)num_leds) * 255);
        incArgs.list->set(i, data.main[i]);
    }
    incArgs.arg1 = args.arg3;
    incArgs.arg2 = ShiftMode::loop_shift;
    incArgs.arg6 = args.arg6;
    incrementor = &Pixels::shifter;
}

/*
    AnimationArgs:
        colors:         list of colors to cycler
        arg1:           steps between colors
*/
void Pixels::cycle(AnimationArgs args) {
    resetIncArgs(incArgs, 0, false);
    unsigned int steps = args.arg1;
    delete incArgs.list;
    incArgs.list = new List((args.colors->size() - 1) * steps);
    if (incArgs.list->size() <= 0 || steps > 100) {
        incrementor = &Pixels::nothing;
        return;
    }
    for (unsigned int i = 0; i < args.colors->size() - 1; i++) {
        for (unsigned int j = 0; j < steps; j++) {
            incArgs.list->set(i * steps + j, mixColors(args.colors->get(i), args.colors->get(i + 1), j * 100.0 / steps));
        }
    }
    setAll(incArgs.list->get(0));
    incrementor = &Pixels::cycler;
}

/*
    AnimationArgs:
        arg1:           seed
*/
void Pixels::randomCycle(AnimationArgs args) {
    resetIncArgs(incArgs, 0, false);
    unsigned int seed = args.arg1;
    unsigned int list_size = NUM_COLORS * 5;
    delete incArgs.list;
    incArgs.list = new List(list_size);
    srand(seed);
    unsigned int previous_index = 0;
    for (unsigned int i = 0; i < list_size; i++) {
        unsigned int index = rand() % NUM_COLORS;
        while (index == previous_index) {
            index = rand() % NUM_COLORS;
        }
        incArgs.list->set(i, COLORS[index]);
    }
    setAll(incArgs.list->get(0));
    incrementor = &Pixels::cycler;
}

/*
    AnimationArgs:
        arg6:           reverse incrementor     (true / false)
        arg7:           reverse pixels          (true / false)
*/
void Pixels::reverser(AnimationArgs args) {
    if (args.arg6) {
        incArgs.arg6 = !incArgs.arg6;
    }
    if (args.arg7) {
        unsigned int last_pixel = num_leds - 1;
        for (unsigned int i; i < num_leds / 2; i++) {
            unsigned int temp = data.main[i];
            data.main[i] = data.main[last_pixel - i];
            data.main[last_pixel - i] = temp;
        }
    }
}
