from rpi_ws281x import Adafruit_NeoPixel
import random
import math
import time
import threading

# Initial LED strip configuration:
LED_COUNT = 0      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 0     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

PROVIDED_MILLIAMPS = 10000
POWER_MULTIPLIER = 0.9
MAX_MILLIAMPS = PROVIDED_MILLIAMPS*POWER_MULTIPLIER

# Create NeoPixel object with appropriate configuration.
# Intialize the library (must be called once before other functions).


class NeoPixels:
    def __init__(self):
        self.num_pixels = LED_COUNT
        self.v_strips = []
        self.pixel_owner = [0] * self.num_pixels
        self.max_milliamps = MAX_MILLIAMPS
        self.max_brightness = LED_BRIGHTNESS
        self.last_show = 0

    def init_neopixels(self, data):
        if "led_count" in data:
            self.num_pixels = data["led_count"]
        if "max_brightness" in data:
            self.max_brightness = data["max_brightness"]
        if "max_milliamps" in data:
            self.max_milliamps = data["max_milliamps"]
        self.pixel_owner = [0] * self.num_pixels
        self.strip = Adafruit_NeoPixel(
            self.num_pixels, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, self.max_brightness, LED_CHANNEL)
        self.strip.begin()

    def update(self, strip_data):
        self.v_strips = strip_data

    def update_pixel_owner(self, strip_id, pixel_id=None):
        if pixel_id == None:
            for i in range(self.v_strips[strip_id]["start"], self.v_strips[strip_id]["end"] + 1):
                self.pixel_owner[i] = strip_id
        else:
            real_pixel_id = self.v_strips[strip_id]["start"] + pixel_id
            if real_pixel_id < 0 or real_pixel_id >= self.num_pixels:
                raise IndexError("Pixel does not exist:",
                                 real_pixel_id, pixel_id)
            self.pixel_owner[real_pixel_id] = strip_id

    def get_color(self, r, g, b):
        """ Gets int value of rgb color 

            Parameters:

                r, g, b: color
        """
        return ((int(r) * 65536) + (int(g) * 256) + int(b))

    def get_color_seperate(self, value):
        """Seperates colors into rgb from single value
            Parameters:
                value: value of color to seperate
        """
        r = (value >> 16) & 0xFF
        g = (value >> 8) & 0xFF
        b = value & 0xFF
        return (r, g, b)

    def get_random_color(self):
        """Generates a random color"""
        r = 0
        g = 0
        b = 0
        color_off = random.randint(0, 2)
        if color_off != 0:
            r = random.randint(0, 255)
        if color_off != 1:
            g = random.randint(0, 255)
        if color_off != 2:
            b = random.randint(0, 255)
        return self.get_color(r, g, b)

    def numPixels(self, strip_id):
        return int(self.v_strips[strip_id]["end"] - self.v_strips[strip_id]["start"] + 1)

    def numMaxPixels(self):
        return self.num_pixels

    def setBrightness(self, value):
        if value >= 0 and value <= self.max_brightness:
            self.strip.setBrightness(value)

    def getBrightness(self):
        return self.strip.getBrightness()

    def setPixelColor(self, strip_id, pixel_id, r, g=None, b=None):
        real_pixel_id = self.v_strips[strip_id]["start"] + pixel_id
        if real_pixel_id >= self.num_pixels:
            raise IndexError("Pixel does not exist:", real_pixel_id,
                             pixel_id, self.v_strips[strip_id]["start"])
        color = r
        if g is not None:
            color = self.get_color(r, g, b)
        if pixel_id <= self.v_strips[strip_id]["end"] and self.pixel_owner[real_pixel_id] == strip_id:
            self.strip.setPixelColor(real_pixel_id, color)
            return 0
        return 1    # used to count if all pixels off

    def getPixelColor(self, strip_id, pixel_id):
        return self.strip.getPixelColor(self.v_strips[strip_id]["start"] + pixel_id)

    def check_power_usage(self):
        total_color = 0
        for i in range(self.num_pixels):
            pixel_color = self.strip.getPixelColor(i)
            pixel_colors = self.get_color_seperate(pixel_color)
            total_color += pixel_colors[0] + pixel_colors[1] + pixel_colors[2]
        total_color = (total_color / 765) * 60
        while total_color * (self.getBrightness() / 255) > self.max_milliamps:
            self.setBrightness(self.getBrightness() - 1)
        return math.ceil(total_color * (self.getBrightness() / 255))

    def get_power_info(self):
        return {
            "max_milliamps": self.max_milliamps,
            "now_milliamps": self.check_power_usage()
        }

    def show(self, limit=0):
        if time.time() >= self.last_show + (limit / 1000) or limit == 0:
            self.check_power_usage()
            self.strip.show()
            self.last_show = time.time()


neopixels = NeoPixels()


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


class Lights:
    def __init__(self, id):
        self.id = id
        self.layer = False
        self.animation_id = AnimationID()

    def stop_animation(self):
        self.animation_id.increment()

    def set_owner(self):
        neopixels.update_pixel_owner(self.id)

    def set_layer(self,value):
        self.layer = bool(value)

    def off(self):
        self.stop_animation()
        self.set_all(0, 0, 0)

    def save(self):
        """Return current color of strip"""
        lights_save = []
        for i in range(neopixels.numPixels(self.id)):
            lights_save.append(neopixels.getPixelColor(self.id, i))
        return lights_save

    def save_split(self):
        """Return current color of strip"""
        lights_save = []
        for i in range(neopixels.numPixels(self.id)):
            cur_color = neopixels.get_color_seperate(
                neopixels.getPixelColor(self.id, i))
            lights_save.append({
                "id": i,
                "r": cur_color[0],
                "g": cur_color[1],
                "b": cur_color[2],
            })
        return lights_save

    def set_all(self, r, g, b):
        """Set color of entire strip
        
                Parameters:

                r, g, b: color
        """
        neopixels.update_pixel_owner(self.id)
        for i in range(0, neopixels.numPixels(self.id)):
            neopixels.setPixelColor(self.id, i, r, g, b)
        neopixels.show()

    def set_pixel(self, pixel_id, r, g, b):
        """Set specific pixel to color

            Parameters:

                pixel_id: which pixel to change

                r, g, b: color to change pixel to  
        """
        neopixels.update_pixel_owner(self.id, pixel_id)
        neopixels.setPixelColor(self.id, pixel_id, r, g, b)
        neopixels.show()

    def set_pixels(self, pixels):
        """Set multiple pixels to colors
        
            Parameters:

                pixels: array of pixels to change in string form (sub paramters seperated by '.')
                    [0]: id (which pixel to change)
                    [1]: r value
                    [2]: g value
                    [3]: b value
        """
        for pixel in pixels:
            data = pixel.split(".")
            neopixels.update_pixel_owner(self.id, int(data[0]))
            neopixels.setPixelColor(self.id, int(data[0]), int(
                data[1]), int(data[2]), int(data[3]))
        neopixels.show()

    def reverse(self):
        """Reverse order of lights on strip"""
        lights_save = self.save()
        for i in range(neopixels.numPixels(self.id)):
            neopixels.setPixelColor(self.id, i, lights_save.pop())
        neopixels.show()

    def shift(self, amount, post_delay=0, show_delay=0):
        """Shift each pixel by amount
        
            Parameters:

                amount: number of pixels to shift by

                post_delay: number of ms to sleep after shift (default = 0)

                show_delay: number of ms to pass to show() (default = 0)
        """
        if amount == 0:
            return
        lights_save = self.save()
        for i in range(neopixels.numPixels(self.id)):
            new_i = i + amount
            if (new_i < 0):
                new_i += neopixels.numPixels(self.id)
            new_i = new_i % neopixels.numPixels(self.id)
            neopixels.setPixelColor(self.id, new_i, lights_save[i])
        neopixels.show(show_delay)
        time.sleep(int(post_delay)/1000.0)

    def wipe(self, r, g, b, direction=1, wait_ms=50, wait_total=False):
        """New color wipes across strip
            
            Parameters:

                r, g, b: color

                direction: (default: 1)
                    1: forward direction
                    -1: reverse direction

                wait_ms: how long before moving to next pixel (in ms) (default: 50)

                wait_total: if true, wait_ms is total time of each pulse (default: False)
        """
        start_time = time.time()
        this_id = self.animation_id.get()
        iter_range = range(neopixels.numPixels(self.id))
        if direction == -1:
            iter_range = reversed(iter_range)
        each_wait = wait_ms
        if wait_total:
            each_wait = wait_ms / neopixels.numPixels(self.id)
        for i in iter_range:
            neopixels.update_pixel_owner(self.id, i)
            neopixels.setPixelColor(self.id, i, neopixels.get_color(r, g, b))
            neopixels.show(15)
            if self.sleepListenForBreak(self.id, each_wait, this_id):
                return
        expected_time = each_wait / 1000 * neopixels.numPixels(self.id)
        actual_time = time.time() - start_time
        neopixels.show()


    def chase(self, r, g, b, wait_ms=50, interval=5, direction=1, layer=False, iterations=1):
        """Movie theater light style chaser animation

            Parameters:
            
                r, g, b: color

                wait_ms: how long before next frame (in ms) (default: 50)

                interval: step amount from pixel to next (default: 5)

                direction: (default: 1)
                    1: forward direction
                    -1: reverse direction

                layer: if true, save pixel color before pulse (default: False)

                iterations: how many times to run (default: 1)
        """
        this_id = self.animation_id.get()
        iter_range = range(interval)
        if direction == -1:
            iter_range = reversed(iter_range)
        for j in range(iterations):
            saves = []
            for q in iter_range:
                for i in range(0, neopixels.numPixels(self.id), interval):
                    saves.append(neopixels.getPixelColor(self.id, i))
                    neopixels.setPixelColor(self.id, i + q, r, g, b)
                neopixels.show()
                if self.sleepListenForBreak(self.id, wait_ms, this_id):
                    return
                for i in range(0, neopixels.numPixels(self.id), interval):
                    if layer:
                        neopixels.setPixelColor(self.id, i + q, saves[int(i / interval)])
                    else:
                        neopixels.setPixelColor(self.id, i + q, 0)


    def pulse(self, r, g, b, direction=1, wait_ms=50, length=5, layer=False, wait_total=False):
        """Sends a pulse of color through strip

        Parameters:

            r, g, g: color of pulse

            direction: (default: 1)
                1: forward direction
                -1: reverse direction

            wait_ms: how long before moving to next pixel (in ms) (default: 50)

            length: how many pixels in pulse (default: 5)

            layer: (default: False)
                True: Keep previous color after pulse passes
                False: Turn off pixel after pulse passes

            wait_total: if true, wait_ms is total time of each pulse (default: False)
        """
        this_id = self.animation_id.get()
        previous = []
        max_pixels = neopixels.numPixels(self.id)
        iter_range = range(max_pixels + length)
        if direction == -1:
            iter_range = reversed(iter_range)
        each_wait = wait_ms
        if wait_total:
            each_wait = wait_ms / neopixels.numPixels(self.id)
        no_own_count = 0
        for i in iter_range:
            j = i - length
            if direction == -1:
                i, j = j, i
            if i < max_pixels and i >= 0:
                previous.append(neopixels.getPixelColor(self.id, i))
                no_own_count += neopixels.setPixelColor(self.id, i, r, g, b)
            if j < max_pixels and j >= 0:
                if layer:
                    neopixels.setPixelColor(self.id, j, previous.pop(0))
                else:
                    neopixels.setPixelColor(self.id, j, 0)
            neopixels.show(15)
            if self.sleepListenForBreak(self.id, each_wait, this_id):
                return
            if no_own_count == neopixels.numPixels(self.id):    # stop animation if all pixels belong to others
                self.animation_id.increment()
                return
        neopixels.show()


    def random_cycle(self, each, wait_ms=250, iterations=1):
        """Flashes random lights
            
            Parameters:
                
                each: number of pixels before new color is selected

                wait_ms: time between color changes (in ms) (default: 250)

                iterations: number of time to change (default: 1)
        """
        this_id = self.animation_id.get()
        current_color = neopixels.get_random_color()
        for i in range(iterations):
            for j in range(neopixels.numPixels(self.id)):
                if j % each == 0:
                        current_color = neopixels.get_random_color()
                neopixels.setPixelColor(self.id, j, current_color)
            neopixels.show()
            if self.sleepListenForBreak(self.id, wait_ms, this_id):
                return

    def rainbow_cycle(self, wait_ms, direction=1, wait_total=False, iterations=1):
        """Draw rainbow that fades across all pixels at once

            Parameters:

                wait_ms: time between iterations (in ms)

                direction: initial direction (default: 1)
                    1: forwards
                    -1: backwards

                wait_total: if true, wait_ms is total time of each pulse (default: False)

                iterations: how many times to repeat (default: 1)
        """
        this_id = self.animation_id.get()
        each_wait = wait_ms
        if wait_total:
            each_wait = wait_ms / neopixels.numPixels(self.id)
        for i in range(neopixels.numPixels(self.id)):
            neopixels.setPixelColor(self.id, i, wheel(int(i / neopixels.numPixels(self.id) * 255)))
        neopixels.show()
        for i in range(iterations * neopixels.numPixels(self.id)):
            self.shift(direction, 0, 15)
            if self.sleepListenForBreak(self.id, each_wait, this_id):
                return

    def rainbow_chase(self, wait_ms, direction=1, iterations=1):
        """Rainbow movie theater light style chaser animation

            Parameters:

                wait_ms: how long before next frame (in ms)

                direction: initial direction (default: 1)
                    1: forwards
                    -1: backwards

                iterations: how many times to repeat (default: 1)
        """
        this_id = self.animation_id.get()
        iter_range = range(3)
        if direction == -1:
            iter_range = reversed(iter_range)
        for k in range(iterations):
            for j in iter_range:
                for i in range(0, neopixels.numPixels(self.id), 3):
                    neopixels.setPixelColor(self.id, i + j, wheel(int((i) / neopixels.numPixels(self.id) * 255)))
                neopixels.show()
                if self.sleepListenForBreak(self.id, wait_ms, this_id):
                    return
                for i in range(0, neopixels.numPixels(self.id), 3):
                    neopixels.setPixelColor(self.id, i + j, 0)

    def mix_switch(self, colors, wait_ms=2000, instant=False):
        """Cycle fading between multiple colors

            Parameters:

                colors: list of colors to split between

                wait_ms: time between full colors (default: 2000)

                instant: if true, dont calculate difference (default: False)
        """
        this_id = self.animation_id.get()
        if instant:
            self.mix_switch_instant(abs(wait_ms), colors)
            return
        for k in range(0, len(colors) - 1):
            percent = 0
            for j in range(100):
                for i in range(0, neopixels.numPixels(self.id)):
                    neopixels.setPixelColor(self.id, i, get_mix(
                        colors[k], colors[k+1], percent))
                neopixels.show()
                percent += 1
                if self.sleepListenForBreak(self.id, wait_ms/100.0, this_id):
                    return

    def mix_switch_instant(self, wait_ms, colors):
        """Switch to next color after wait_ms

            Parameters:

                wait_ms: time between colors

                colors: list of colors to split between
        """
        this_id = self.animation_id.get()
        for j in range(0, len(colors)):
            for i in range(0, neopixels.numPixels(self.id)):
                neopixels.setPixelColor(self.id, i, get_mix(
                    colors[j], colors[j], 100))
            neopixels.show()
            if self.sleepListenForBreak(self.id, wait_ms, this_id):
                return

    def bounce(self, colors, wait_ms=50, length=5, direction=1, layer=False, wait_total=False):
        """Bounce Pulse across strip

            Parameters:

                colors: list of colors to pulse

                wait_ms: how long before next frame (in ms) (default: 50)

                length: how many pixels in pulse (default: 5)

                direction: initial direction (default: 1)
                    1: forwards
                    -1: backwards

                layer: if true, save pixel color before pulse (default: False)

                wait_total: if true, wait_ms is total time of each pulse (default: False)
        """
        this_id = self.animation_id.get()
        for color in colors:
            if "r" in color and "g" in color and "b" in color:
                self.pulse(color["r"],color["g"],color["b"],direction, wait_ms, length, layer, wait_total)
            else:
                self.pulse(color[0],color[1],color[2],direction, wait_ms, length, layer, wait_total)
            direction *= -1
            if this_id != self.animation_id.get():
                break

    def pattern(self, colors, interval=3, fraction=True, blend=False):
        """Repeat colors across strip
        
            Parameters:

                colors: list of colors

                interval: how to divide pixels (default: 3)

                fraction: (default: True)
                    True: interval is number of sections
                    False: interval is num pixels for each color

                blend: true if colors are mixed (default: False)
        """
        this_id = self.animation_id.get()
        if fraction:
            interval = self.get_fraction(interval)
        color = 0
        for i in range(0, neopixels.numPixels(self.id), interval):
            for j in range(interval):
                if blend:
                    cur_color = get_mix(colors[color], colors[(color + 1) % len(colors)], (j / interval) * 100)
                    neopixels.setPixelColor(self.id, i + j, cur_color)
                else:
                    if i + j < neopixels.numPixels(self.id):
                        neopixels.setPixelColor(self.id, i + j, *colors[color])
            color = (color + 1) % len(colors)
        neopixels.show()

    def sleepListenForBreak(self, strip_id, wait_ms, this_id):
        """While sleeping check if global id has changed

            Parameters:

                wait_ms: total sleep time (in ms)

                this_id: value to compare animation id against
        """
        expected_end = time.time() + wait_ms/1000.0
        while wait_ms > 0 and time.time() < expected_end:
            if wait_ms <= 100:
                time.sleep(wait_ms/1000.0)
            else:
                time.sleep(.1)
            if this_id != self.animation_id.get():
                return True
            wait_ms -= 100
        return False

    def get_fraction(self, num):
        return round(neopixels.numPixels(self.id) / int(num))


class Timer:
    def __init__(self, num_pixels):
        self.start_time = time.time()
        self.sleep_count = 0
        self.early = num_pixels * .00004

    def set_start(self, value):
        self.start_time = value
        while time.time() < (self.start_time - self.early):
            pass
        self.sleep_count = 0

    def sleep(self, value):
        self.sleep_count += value
        while time.time() < self.start_time + self.sleep_count:
            time.sleep(.001)


# Utilities

def wheel(pos):
    """Generate rainbow colors across 0-255 positions.
    
        Parameters:

            pos: current pixel
    """
    if pos < 85:
        return neopixels.get_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return neopixels.get_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return neopixels.get_color(0, pos * 3, 255 - pos * 3)

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
    return neopixels.get_color(r, g, b)

print("lights.py loaded")
