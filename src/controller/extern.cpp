#include <stdio.h>
#include <iostream>

#include "structs.h"
#include "pixels.h"

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

    void Pixels_initialize(Pixels* p, unsigned int num_leds, unsigned int milliwatts, unsigned int brightness, unsigned int max_brightness) {
        p->initialize(num_leds, milliwatts, brightness, max_brightness);
    }

    bool Pixels_isInitialized(Pixels* p) {
        return p->isInitialized();
    }

    Frame* Pixels_get(Pixels* p) {
        return p->get();
    }

    void Pixels_increment(Pixels* p) {
        p->increment();
    }

    void Pixels_color(Pixels* p, AnimationArgs args) {
        p->color(args);
    }

    void Pixels_wipe(Pixels* p, AnimationArgs args) {
        p->wipe(args);
    }

    void Pixels_pulse(Pixels* p, AnimationArgs args) {
        p->pulse(args);
    }

    void Pixels_rainbow(Pixels* p, AnimationArgs args) {
        p->rainbow(args);
    }

    void Pixels_cycle(Pixels* p, AnimationArgs args) {
        p->cycle(args);
    }
}
