#include <stdio.h>

#include <iostream>

#include "pixels.h"
#include "structs.h"

extern "C" {
unsigned int maxLEDPerStrip() {
    return MAX_LED_PER_STRIP;
}

unsigned int ledStripCount() {
    return LED_STRIP_COUNT;
}

List* List_new(unsigned int length) {
    return new List(length);
}

unsigned int List_get(List* l, unsigned int index) {
    return l->get(index);
}

void List_set(List* l, unsigned int index, unsigned int value) {
    return l->set(index, value);
}

unsigned int List_size(List* l) {
    return l->size();
}

void List_incrementCounter(List* l) {
    l->incrementCounter();
}

void List_decrementCounter(List* l) {
    l->decrementCounter();
}

void List_setCounter(List* l, int value) {
    l->setCounter(value);
}

unsigned int List_getCounter(List* l) {
    return l->getCounter();
}

unsigned int List_getNext(List* l) {
    return l->getNext();
}

unsigned int List_getCurrent(List* l) {
    return l->getCurrent();
}

Pixels* Pixels_new(unsigned int num_leds, unsigned int max_brightness) {
    return new Pixels(num_leds, max_brightness);
}

bool Pixels_canShow(Pixels* p, unsigned int ms = 0) {
    return p->canShow(ms);
}

void Pixels_setDelay(Pixels* p, unsigned int value) {
    p->setDelay(value);
}

unsigned int Pixels_getDelay(Pixels* p) {
    return p->getDelay();
}

void Pixels_setSize(Pixels* p, unsigned int value) {
    p->setSize(value);
}

unsigned int Pixels_size(Pixels* p) {
    return p->size();
}

unsigned int Pixels_getBrightness(Pixels* p) {
    return p->getBrightness();
}

void Pixels_setBrightness(Pixels* p, unsigned int value) {
    p->setBrightness(value);
}

void Pixels_setIncrementSteps(Pixels* p, unsigned int value = 1) {
    p->setIncrementSteps(value);
}

void Pixels_initialize(Pixels* p, unsigned int num_leds, unsigned int milliwatts, unsigned int brightness, unsigned int max_brightness, bool grb) {
    p->initialize(num_leds, milliwatts, brightness, max_brightness, grb);
}

bool Pixels_isInitialized(Pixels* p) {
    return p->isInitialized();
}

bool Pixels_isGRB(Pixels* p) {
    return p->isGRB();
}

Frame* Pixels_get(Pixels* p) {
    return p->get();
}

void Pixels_increment(Pixels* p) {
    p->increment();
}

void Pixels_animation(Pixels* p, AnimationArgs* args) {
    p->animation(*args);
}

long* Pixels_getCurrentState(Pixels* p) {
    return p->getCurrentState();
}

AnimationArgs* createAnimationArgs(
    Animation animation,
    int color,
    int color_bg,
    List* colors,
    unsigned int wait_ms,
    unsigned int arg1,
    unsigned int arg2,
    unsigned int arg3,
    int arg4,
    int arg5,
    bool arg6,
    bool arg7,
    bool arg8) {
    AnimationArgs* args = new AnimationArgs();
    args->animation = animation;
    args->color = color;
    args->colors = colors;
    args->color_bg = color_bg;
    args->wait_ms = wait_ms;
    args->arg1 = arg1;
    args->arg2 = arg2;
    args->arg3 = arg3;
    args->arg4 = arg4;
    args->arg5 = arg5;
    args->arg6 = arg6;
    args->arg7 = arg7;
    args->arg8 = arg8;
    return args;
}
}
