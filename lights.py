#!/usr/bin/env python3

import time
from random import randint
from rpi_ws281x import *
import math
import argparse

# LED strip configuration:
LED_COUNT = 60      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).

strip.begin()

# Classes

class Settings:
    """Holds current global settings"""

    def __init__(self):
        self.brightness = 75
        self.num_pixels = strip.numPixels()
        self.break_animation = True

    def get_brightness(self):
        return self.brightness

    def set_brightness(self, value):
        self.brightness = value
        strip.setBrightness(value)
        strip.show()
    
    def get_break_animation(self):
        return self.break_animation

    def set_break_animation(self, value):
        self.break_animation = value

    def get_all_settings(self):
        cur_settings = {
            "brightness": self.brightness,
            "break_animation": self.break_animation,
            "num_pixels": self.num_pixels,
        }
        return cur_settings

global_settings = Settings()
    
class AnimationID:
    """Holds the current animation_id used globally"""

    def __init__(self):
        self.id = 0

    def increment(self):
        """Increase animation_id by 1"""
        self.id += 1

    def get(self):
        """Return current animation_id"""
        return self.id


animation_id = AnimationID()

class State:
    def __init__(self):
        pass

    def get_pixel_data(self):
        pixel_data_save = save_lights()
        pixel_data = []
        for i in range(len(pixel_data_save)):
            cur_pixel = get_color_seperate(pixel_data_save[i])
            pixel = {
                "id": i,
                "r": cur_pixel[0],
                "g": cur_pixel[1],
                "b": cur_pixel[2],
            }
            pixel_data.append(pixel)
        return pixel_data
    
    def get_state(self):
        settings = global_settings.get_all_settings()
        pixel_data = self.get_pixel_data()
        data = {
            "settings": settings,
            "pixel_data": pixel_data
        }
        return data

state = State()


# Strip shifting


def lights_reverse():
    """Reverse order of lights on strip"""
    lights_save = [None] * strip.numPixels()
    for i in range(strip.numPixels() // 2):
        lights_save[i] = strip.getPixelColor(i)
        strip.setPixelColor(i, 0)
        lights_save[strip.numPixels()-i -
                    1] = strip.getPixelColor(strip.numPixels()-i-1)
        strip.setPixelColor(strip.numPixels()-i-1, 0)
        strip.show()
        time.sleep(.005)
    high_start = int(math.floor(strip.numPixels() // 2))
    low_start = int(math.ceil(strip.numPixels() // 2)) - 1

    for i in range((strip.numPixels() // 2)):
        strip.setPixelColor(low_start-i, lights_save[high_start+i])
        strip.setPixelColor(high_start+i, lights_save[low_start-i])
        strip.show()
        time.sleep(.005)


def lights_shift(amount, post_delay=0):
    """Shift each pixel by amount
    
        Parameters:

            amount: number of pixels to shift by

            post_delay: number of ms to sleep after shift (default = 0)

    """
    if amount == 0:
        return
    lights_save = save_lights()
    for i in range(strip.numPixels()):
        new_i = i + amount
        if (new_i < 0):
            new_i += strip.numPixels()
        new_i = new_i % strip.numPixels()
        strip.setPixelColor(new_i, lights_save[i])
    strip.show()
    time.sleep(int(post_delay)/1000.0)


def lights_average_neighbors():
    """Make each pixel the average color of its neighboors"""
    lights_save = save_lights()
    for i in range(strip.numPixels()):
        average_value = [[None]*3] * strip.numPixels()
        for j in range(-1, 1):
            value_index = (i + j)
            if (value_index < 0):
                value_index += strip.numPixels()
            value_index = value_index % strip.numPixels()
            for k in range(3):
                average_value[i][k] = get_color_seperate(lights_save[i])[k]
            for k in range(3):
                average_value[i][k] /= 3
        strip.setPixelColor(i, get_color(
            average_value[i][0], average_value[i][1], average_value[i][2]))
        strip.show()


def rainbow(wait_ms, iterations, this_id):
    """Draw rainbow that fades across all pixels at once

        Parameters:

            wait_ms: time between iterations (in ms)

            iterations: number of times to repeat
    
            this_id: break if this value does not equal global animation_id
    """
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        if sleepListenForBreak(wait_ms, this_id):
            return


def lights_random_cycle(each, wait_ms, iterations, this_id):
    """Flashes random lights
        
        Parameters:
            
            each: number of pixels before new color is selected

            wait_ms: time between color changes (in ms)

            iterations: number of time to change

            this_id: break if this value does not equal global animation_id
    """
    current_color = get_random_color()
    for i in range(iterations):
        for j in range(strip.numPixels()):
            # if each == "true":
            #     current_color = get_random_color()
            if j % each == 0:
                    current_color = get_random_color()
            strip.setPixelColor(j, current_color)
        strip.show()
        if sleepListenForBreak(wait_ms, this_id):
            return


def lights_pulse(r, g, b, direction, wait_ms, length, this_id, layer=True):
    """Sends a pulse of color through strip

    Parameters:

        r, g, g: color of pulse

        direction:
            1: forward direction
            -1: reverse direction

        wait_ms: how long before moving to next pixel (in ms)

        length: how many pixels in pulse

        layer: 
            True: restore pixel to previous color after pulse passes (default)
            False: pixels turn off after pulse passes

        this_id: break if this value does not equal global animation_id
    """
    previous = []
    if direction == 1:
        for i in range(strip.numPixels()+length):
            previous.append(strip.getPixelColor(i))
            j = i - length
            strip.setPixelColor(i, get_color(r, g, b))
            if j >= 0:
                if layer:
                    strip.setPixelColor(j, previous[j])
                else:
                    strip.setPixelColor(j, 0)
            if sleepListenForBreak(wait_ms, this_id):
                return
            strip.show()
    else:
        for i in reversed(range(strip.numPixels()+length)):
            j = i - length
            previous.append(strip.getPixelColor(j))
            if j >= 0:
                strip.setPixelColor(j, get_color(r, g, b))
            if i < strip.numPixels():
                if layer:
                    strip.setPixelColor(i, previous[strip.numPixels()-i-1])
                else:
                    strip.setPixelColor(i, 0)
            if sleepListenForBreak(wait_ms, this_id):
                return
            strip.show()


def lights_wipe(r, g, b, direction, wait_ms, this_id):
    """New color wipes across strip
        
        Parameters:

            r, g, b: color

            direction:
                1: forward direction
                -1: reverse direction

            wait_ms: how long before moving to next pixel (in ms)

            this_id: break if this value does not equal global animation_id
    """
    if direction == 1:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, get_color(r, g, b))
            strip.show()
            if sleepListenForBreak(wait_ms, this_id):
                return
    elif direction == -1:
        for i in reversed(range(strip.numPixels())):
            strip.setPixelColor(i, get_color(r, g, b))
            strip.show()
            if sleepListenForBreak(wait_ms, this_id):
                return


def lights_chase(r, g, b, wait_ms, iterations, this_id):
    """Movie theater light style chaser animation

        Parameters:
        
            r, g, b: color

            wait_ms: how long before next frame (in ms)

            iterations: how many times to run

            this_id: break if this value does not equal global animation_id
    """
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, get_color(r, g, b))
            strip.show()
            if sleepListenForBreak(wait_ms, this_id):
                return
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def lights_rainbow_cycle(wait_ms, iterations, this_id):
    """Draw rainbow that uniformly distributes itself across all pixels

        Parameters:

            wait_ms: how long before next frame (in ms)

            iterations: how many times to run

            this_id: break if this value does not equal global animation_id
    """
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(
                i, wheel((int(i * 256 // strip.numPixels()) + j) & 255))
        strip.show()
        if sleepListenForBreak(wait_ms, this_id):
                return


def lights_rainbow_chase(wait_ms, this_id):
    """Rainbow movie theater light style chaser animation

        Parameters:

            wait_ms: how long before next frame (in ms)

            this_id: break if this value does not equal global animation_id
    """
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            #time.sleep(wait_ms/1000.0)
            if sleepListenForBreak(wait_ms, this_id):
                return
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def lights_mix_switch(wait_ms, colors, this_id):
    """Cycle fading between multiple colors

        Parameters:
            
            wait_ms: time between full colors
                < 0: instant change between colors
                >= 0: blend between colors

            colors: list of colors to switch between

            this_id: break if this value does not equal global animation_id
    """
    if wait_ms < 0:
        lights_mix_switch_instant(abs(wait_ms), colors, this_id)
        return
    for k in range(0, len(colors) - 1):
        percent = 0
        for j in range(100):
            for i in range(0, strip.numPixels()):
                strip.setPixelColor(i, get_mix(
                    colors[k], colors[k+1], percent))
            strip.show()
            percent += 1
            if sleepListenForBreak(wait_ms/100.0, this_id):
                return


def lights_mix_switch_instant(wait_ms, colors, this_id):
    """Switch to next color after wait_ms

        Parameters:

            wait_ms: time between colors

            colors: list of colors to split between

            this_id: break if this value does not equal global animation_id
    """
    for j in range(0, len(colors)):
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i, get_mix(
                colors[j], colors[j], 100))
        strip.show()
        print("lights_mix_instant", wait_ms)
        if sleepListenForBreak(wait_ms, this_id):
            return

# Instant no animation


def lights_off():
    """Turns all pixels off"""
    for i in range(strip.numPixels() // 2 + 1):
        strip.setPixelColor(i, 0)
        strip.setPixelColor(LED_COUNT - i, 0)
        strip.show()
        time.sleep(5/1000.0)


def lights_set_color(r, g, b):
    """Sets all pixels to rgb color given

        Parameters:

            r, g, b: color
    """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, get_color(r, g, b))
    strip.show()


def lights_set_random(each):
    """Set lights randomly

        Parameters:

            each:
                True: set each pixel to a random color
                False: set entire strip to same random color
    """
    if each:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, get_random_color())
    else:
        color = get_random_color()
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
    strip.show()


def lights_set(id, r, g, b):
    """Set specific pixel to color

        Parameters:

           id: which pixel to change

           r, g, b: color to change pixel to  
    """
    strip.setPixelColor(id, get_color(r, g, b))
    strip.show()


def lights_set_multiple():
    """For future implementaion"""
    pass

# Utilities


def wheel(pos):
    """Generate rainbow colors across 0-255 positions.
    
        Parameters:

            pos: current pixel
    """
    if pos < 85:
        return get_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return get_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return get_color(0, pos * 3, 255 - pos * 3)


def get_mix(color_1, color_2, percent):
    """Get the mixed color between 2 colors
    
        Parameters:
            
            color_1, color_2: two colors to mix

            percent: how far towards color 2 from color 1
    
    """
    r_diff = color_2[0] - color_1[0]
    g_diff = color_2[1] - color_1[1]
    b_diff = color_2[2] - color_1[2]
    r = color_1[0] + (r_diff * percent/100.0)
    g = color_1[1] + (g_diff * percent/100.0)
    b = color_1[2] + (b_diff * percent/100.0)
    return get_color(r, g, b)


def save_lights():
    """Return current color of strip"""
    lights_save = []
    for i in range(strip.numPixels()):
        lights_save.append(strip.getPixelColor(i))
    return lights_save


def sleepListenForBreak(wait_ms, this_id):
    """While sleeping check if global id has changed

        Parameters:

            wait_ms: total sleep time (in ms)

            this_id: break sleep if global animation_id does not equal this value    
    """
    while wait_ms > 0:
        if wait_ms <= 100:
            time.sleep(wait_ms/1000.0)
        else:
            time.sleep(.1)
        if this_id != animation_id.get() and global_settings.get_break_animation():
            return True
        wait_ms -= 100
    return False


def get_random_color():
    """Generates a random color"""
    r = 0
    g = 0
    b = 0
    color_off = randint(0, 2)
    if color_off != 0:
        r = randint(0, 255)
    if color_off != 1:
        g = randint(0, 255)
    if color_off != 2:
        b = randint(0, 255)
    return get_color(r, g, b)


def get_color(r, g, b):
    """ Gets int value of rgb color 

        Parameters:

            r, g, b: color
    """
    return ((int(r) * 65536) + (int(g) * 256) + int(b))


def get_color_seperate(value):
    """Seperates colors into rgb from single value

        Parameters:

            value: value of color to seperate
    """
    r = (value >> 16) & 0xFF
    g = (value >> 8) & 0xFF
    b = value & 0xFF
    return (r, g, b)

# Run on Startup
strip.setBrightness(75)

lights_wipe(255, 0, 0, 1, 1, 0)
lights_wipe(0, 255, 0, 1, 1, 0)
lights_wipe(0, 0, 255, 1, 1, 0)
lights_wipe(0, 0, 0, 1, 1, 0)
