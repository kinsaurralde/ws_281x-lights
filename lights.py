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
# LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

PROVIDED_MILLIAMPS = 10000
POWER_MULTIPLIER = 0.9
MAX_MILLIAMPS = PROVIDED_MILLIAMPS*POWER_MULTIPLIER

PROVIDED_WATTS = 1
VOLTAGE = 5


def time_func(func):
    def wrapper(*args, **kwargs):
        s_time = time.time()
        print("Start Time:", s_time)
        return_val = func(*args, **kwargs)
        e_time = time.time()
        print("End Time:", e_time)
        print("Difference:", e_time - s_time)
        print("")
        return return_val
    return wrapper


class Timer:
    def __init__(self, num_pixels=0, start_time=time.time()):
        self.start_time = start_time
        self.sleep_count = 0
        self.early = num_pixels * .00004

    def set_start(self, value):
        self.start_time = value
        while time.time() < (self.start_time - self.early):
            pass
        self.sleep_count = 0

    def get_time(self):
        return self.start_time + self.sleep_count

    def sleep(self, value):
        self.sleep_count += (value/1000)
        while time.time() < self.start_time + self.sleep_count - self.early:
            time.sleep(.001)

    def sleepBreak(self, id_function, this_id, value):
        self.sleep_count += (value/1000)
        while time.time() < self.start_time + self.sleep_count - self.early:
            time.sleep(.001)
            if this_id != id_function():
                return True
        if this_id != id_function():
            return True
        return False


# Create NeoPixel object with appropriate configuration.
# Intialize the library (must be called once before other functions).


class NeoPixels:
    def __init__(self, controller_id, testing = False):
        self.testing = testing
        self.id = controller_id
        self.num_pixels = LED_COUNT
        self.v_strips = []
        self.pixel_owner = [0] * self.num_pixels
        self.max_brightness = LED_BRIGHTNESS
        self.max_watts = PROVIDED_WATTS
        self.voltage = VOLTAGE
        self.last_show = 0
        self.pin = LED_PIN
        self.grb = False
        self.test_strip = [] * self.num_pixels

    def init_neopixels(self, data):
        if "led_count" in data:
            self.num_pixels = data["led_count"]
        if "max_brightness" in data:
            self.max_brightness = data["max_brightness"]
        if "max_watts" in data:
            self.max_watts = data["max_watts"]
        if "volts" in data:
            self.voltage = data["volts"]
        if "pin" in data:
            self.pin = data["pin"]
        if "grb" in data:
            self.grb = data["grb"]
        led_channel = 0
        if self.pin in [13, 19, 41, 45, 53]:
            led_channel = 1
        self.pixel_owner = [0] * self.num_pixels
        self.test_strip = [0] * self.num_pixels
        self.strip = Adafruit_NeoPixel(
            self.num_pixels, self.pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, self.max_brightness, led_channel)
        if self.testing:
            print("Testing Mode")
            return
        self.strip.begin()
        print("Neopixel [", self.id ,"] created with values:", self.num_pixels, self.pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, self.max_brightness, led_channel, self.grb)
    
    
    def update(self, strip_data):
        self.v_strips = strip_data

    def update_pixel_owner(self, strip_id, pixel_id=None):
        if pixel_id == None:
            for i in range(self.v_strips[strip_id]["start"], self.v_strips[strip_id]["end"] + 1):
                self.pixel_owner[i] = strip_id
        else:
            real_pixel_id = self.v_strips[strip_id]["start"] + pixel_id
            if real_pixel_id < 0 or real_pixel_id >= self.num_pixels:
                print("Pixel does not exist:", real_pixel_id, pixel_id)
                return
            self.pixel_owner[real_pixel_id] = strip_id

    def get_color(self, r, g, b):
        """ Gets int value of rgb color 

            Parameters:

                r, g, b: color
        """
        if self.grb:
            return ((int(g) * 65536) + (int(r) * 256) + int(b))
        return ((int(r) * 65536) + (int(g) * 256) + int(b))

    def get_color_seperate(self, value):
        """Seperates colors into rgb from single value
            Parameters:
                value: value of color to seperate
        """
        r = (value >> 16) & 0xFF
        g = (value >> 8) & 0xFF
        b = value & 0xFF
        if self.grb:
            return (g, r, b)
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
        if self.testing:
            return 0
        if value >= 0 and value <= self.max_brightness:
            self.strip.setBrightness(value)

    def getBrightness(self):
        if self.testing:
            return 0
        return self.strip.getBrightness()

    def setPixelColor(self, strip_id, pixel_id, r, g=None, b=None):
        real_pixel_id = self.v_strips[strip_id]["start"] + pixel_id
        if real_pixel_id >= self.num_pixels:
            print("Pixel does not exist:", real_pixel_id, pixel_id, self.v_strips[strip_id]["start"])
            return 1
        color = r
        if g is not None:
            color = self.get_color(r, g, b)
        if pixel_id <= self.v_strips[strip_id]["end"] and self.pixel_owner[real_pixel_id] == strip_id:
            if self.testing:
                self.test_strip[real_pixel_id] = color
            else:
                self.strip.setPixelColor(real_pixel_id, color)
            return 0
        return 1    # used to count if all pixels off

    def getPixelColor(self, strip_id, pixel_id):
        real_id = self.v_strips[strip_id]["start"] + pixel_id
        if self.testing:
            return self.test_strip[real_id]
        return self.strip.getPixelColor(real_id)

    def check_power_usage(self):
        if self.testing:
            return 0
        total_color = 0
        for i in range(self.num_pixels):
            pixel_color = self.strip.getPixelColor(i)
            pixel_colors = self.get_color_seperate(pixel_color)
            total_color += pixel_colors[0] + pixel_colors[1] + pixel_colors[2]
        total_color = (total_color / 765) * 18 / 60
        while total_color * (self.getBrightness() / 255) > self.max_watts:
            self.setBrightness(self.getBrightness() - 1)
        return total_color * (self.getBrightness() / 255)

    def get_power_info(self):
        return {
            "max_watts": self.max_watts,
            "strip_max": self.num_pixels * 18 / 60,
            "now_watts": self.check_power_usage()
        }

    def show(self, limit=0):
        if self.testing:
            return
        if time.time() >= self.last_show + (limit / 1000) or limit == 0:
            self.check_power_usage()
            self.strip.show()
            self.last_show = time.time()

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

    def check(self, other_id):
        """Check if other id is equal to this id"""
        return other_id == self.id


class Lights:
    def __init__(self, neopixels, id):
        self.neo = neopixels
        self.id = id
        self.start_time = time.time()
        self.layer = False
        self.animation_id = AnimationID()

    def stop_animation(self):
        self.animation_id.increment()

    def add_start_time(self, value):
        self.start_time += value / 1000

    def set_owner(self):
        self.neo.update_pixel_owner(self.id)

    def set_layer(self,value):
        self.layer = bool(value)

    def off(self):
        self.stop_animation()
        self.set_all(0, 0, 0)

    def save(self):
        """Return current color of strip"""
        lights_save = []
        for i in range(self.neo.numPixels(self.id)):
            lights_save.append(self.neo.getPixelColor(self.id, i))
        return lights_save

    def save_split(self):
        """Return current color of strip"""
        lights_save = []
        for i in range(self.neo.numPixels(self.id)):
            cur_color = self.neo.get_color_seperate(
                self.neo.getPixelColor(self.id, i))
            lights_save.append({
                "id": i,
                "r": int(cur_color[0]),
                "g": int(cur_color[1]),
                "b": int(cur_color[2]),
            })
        return lights_save

    def set_all(self, r, g, b, color=None):
        """Set color of entire strip
        
                Parameters:

                r, g, b: color
        """
        self.neo.update_pixel_owner(self.id)
        for i in range(0, self.neo.numPixels(self.id)):
            self.neo.setPixelColor(self.id, i, r, g, b)
        self.neo.show()
        return 0

    def set_pixel(self, pixel_id, r, g, b):
        """Set specific pixel to color

            Parameters:

                pixel_id: which pixel to change

                r, g, b: color to change pixel to  
        """
        self.neo.update_pixel_owner(self.id, pixel_id)
        self.neo.setPixelColor(self.id, pixel_id, r, g, b)
        self.neo.show()
        return 0

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
            self.neo.update_pixel_owner(self.id, int(data[0]))
            self.neo.setPixelColor(self.id, int(data[0]), int(
                data[1]), int(data[2]), int(data[3]))
        self.neo.show()
        return 0

    def _set_save(self, pixels):
        """Set pixels to save

            Parameters:

                pixels: array of pixels from self.save()
        """
        self.neo.update_pixel_owner(self.id)
        for i, pixel in enumerate(pixels[:self.neo.numPixels(self.id)]):
            self.neo.setPixelColor(self.id, i, pixel)
        return 0

    def reverse(self):
        """Reverse order of lights on strip"""
        lights_save = self.save()
        for i in range(self.neo.numPixels(self.id)):
            self.neo.setPixelColor(self.id, i, lights_save.pop())
        self.neo.show()
        return 0

    def shift(self, amount, post_delay=0, iterations=None, pixels=None):
        """Shift each pixel by amount
        
            Parameters:

                amount: number of pixels to shift by

                post_delay: number of ms to sleep after shift (default: 0)

                iterations: number of times to shift (default: num_pixels)

                pixels: (default: None)
                    None: shift current pixels
                    Save array: shift given pixel array
        """
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        start_time = time.time()
        this_id = self.animation_id.get()
        if pixels is None:
            pixels = self.save()
        num_pixels = len(pixels)
        if iterations is None:
            iterations = num_pixels
        cur_start = 0
        interval = 1
        if post_delay != 0:
            interval = int(15 / post_delay)
        for k in range(iterations):
            if post_delay >= 15 or k % interval == 0:
                self._set_save(pixels[cur_start:] + pixels[:cur_start])
            cur_start = (cur_start + 1) % num_pixels
            self.neo.show(15)
            asd = time.time()
            if t.sleepBreak(self.animation_id.get, this_id, post_delay):
                return 0
        return post_delay * iterations

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
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        start_time = time.time()
        this_id = self.animation_id.get()
        iter_range = range(self.neo.numPixels(self.id))
        if direction == -1:
            iter_range = reversed(iter_range)
        each_wait = wait_ms
        if wait_total:
            each_wait = wait_ms / self.neo.numPixels(self.id)
        for i in iter_range:
            self.neo.update_pixel_owner(self.id, i)
            self.neo.setPixelColor(self.id, i, self.neo.get_color(r, g, b))
            self.neo.show(15)
            if t.sleepBreak(self.animation_id.get, this_id, each_wait):
                return 0
        expected_time = each_wait / 1000 * self.neo.numPixels(self.id)
        actual_time = time.time() - start_time
        self.neo.show()
        return each_wait * self.neo.numPixels(self.id)


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
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        this_id = self.animation_id.get()
        iter_range = range(interval)
        if direction == -1:
            iter_range = reversed(iter_range)
        for j in range(iterations):
            saves = []
            for q in iter_range:
                for i in range(0, self.neo.numPixels(self.id), interval):
                    if i + q >= self.neo.numPixels(self.id):
                        break
                    saves.append(self.neo.getPixelColor(self.id, i))
                    self.neo.setPixelColor(self.id, i + q, r, g, b)
                self.neo.show()
                if t.sleepBreak(self.animation_id.get, this_id, wait_ms):
                    return 0
                for i in range(0, self.neo.numPixels(self.id), interval):
                    if i + q >= self.neo.numPixels(self.id):
                        break
                    if layer:
                        self.neo.setPixelColor(self.id, i + q, saves[int(i / interval)])
                    else:
                        self.neo.setPixelColor(self.id, i + q, 0)
        return wait_ms * interval


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
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        this_id = self.animation_id.get()
        previous = []
        max_pixels = self.neo.numPixels(self.id)
        iter_range = range(max_pixels + length)
        if direction == -1:
            iter_range = reversed(iter_range)
        each_wait = wait_ms
        total_wait = each_wait * (self.neo.numPixels(self.id) + length)
        if wait_total:
            each_wait = wait_ms / (self.neo.numPixels(self.id) + length)
            total_wait = wait_ms
        no_own_count = 0
        for i in iter_range:
            j = i - length
            if direction == -1:
                i, j = j, i
            if i < max_pixels and i >= 0:
                previous.append(self.neo.getPixelColor(self.id, i))
                no_own_count += self.neo.setPixelColor(self.id, i, r, g, b)
            if j < max_pixels and j >= 0:
                if layer:
                    self.neo.setPixelColor(self.id, j, previous.pop(0))
                else:
                    self.neo.setPixelColor(self.id, j, 0)
            self.neo.show(15)
            if t.sleepBreak(self.animation_id.get, this_id, each_wait):
                return 0
            if no_own_count == self.neo.numPixels(self.id):    # stop animation if all pixels belong to others
                self.animation_id.increment()
                return 0
        self.neo.show()
        return total_wait

    def random_cycle(self, each, wait_ms=250, iterations=1):
        """Flashes random lights
            
            Parameters:
                
                each: number of pixels before new color is selected

                wait_ms: time between color changes (in ms) (default: 250)

                iterations: number of time to change (default: 1)
        """
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        this_id = self.animation_id.get()
        current_color = self.neo.get_random_color()
        if each == -1:
            each = self.neo.numPixels(self.id)
        for i in range(iterations):
            for j in range(self.neo.numPixels(self.id)):
                if j % each == 0:
                        current_color = self.neo.get_random_color()
                self.neo.setPixelColor(self.id, j, current_color)
            self.neo.show()
            if t.sleepBreak(self.animation_id.get, this_id, wait_ms):
                return 0
        return wait_ms * iterations

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
            each_wait = wait_ms / self.neo.numPixels(self.id)
        for i in range(self.neo.numPixels(self.id)):
            self.neo.setPixelColor(self.id, i, self.wheel(int(i / self.neo.numPixels(self.id) * 255)))
        self.neo.show()
        for i in range(iterations * self.neo.numPixels(self.id)):
            self.shift(direction, 0, 15)
            if self.sleepListenForBreak(self.id, each_wait, this_id):
                return 0
        return 0

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
                for i in range(0, self.neo.numPixels(self.id), 3):
                    self.neo.setPixelColor(self.id, i + j, self.wheel(int((i) / self.neo.numPixels(self.id) * 255)))
                self.neo.show()
                if self.sleepListenForBreak(self.id, wait_ms, this_id):
                    return 0
                for i in range(0, self.neo.numPixels(self.id), 3):
                    self.neo.setPixelColor(self.id, i + j, 0)
        return 0

    def mix_switch(self, colors, wait_ms=2000, instant=False):
        """Cycle fading between multiple colors

            Parameters:

                colors: list of colors to split between

                wait_ms: time between full colors (default: 2000)

                instant: if true, dont calculate difference (default: False)
        """
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        this_id = self.animation_id.get()
        if instant:
            self._mix_switch_instant(abs(wait_ms), colors, t)
            return wait_ms * len(colors)
        for k in range(0, len(colors) - 1):
            percent = 0
            for j in range(100):
                for i in range(0, self.neo.numPixels(self.id)):
                    self.neo.setPixelColor(self.id, i, self.get_mix(
                        colors[k], colors[k+1], percent))
                self.neo.show(15)
                percent += 1
                if t.sleepBreak(self.animation_id.get, this_id, wait_ms/100.0):
                    return 0
        self.neo.show()
        return wait_ms * (len(colors) - 1)

    def _mix_switch_instant(self, wait_ms, colors, t):
        """Switch to next color after wait_ms

            Parameters:

                wait_ms: time between colors

                colors: list of colors to split between

                t: timer
        """
        this_id = self.animation_id.get()
        for j in range(0, len(colors)):
            for i in range(0, self.neo.numPixels(self.id)):
                self.neo.setPixelColor(self.id, i, self.get_mix(
                    colors[j], colors[j], 100))
            self.neo.show()
            if t.sleepBreak(self.animation_id.get, this_id, wait_ms):
                return 0


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
        total_time = 0
        for color in colors:
            run_time = 0
            if "r" in color and "g" in color and "b" in color:
                run_time += self.pulse(color["r"],color["g"],color["b"],direction, wait_ms, length, layer, wait_total)
            else:
                run_time += self.pulse(color[0],color[1],color[2],direction, wait_ms, length, layer, wait_total)
            direction *= -1
            self.add_start_time(run_time)
            total_time += run_time
            if this_id != self.animation_id.get():
                break
        return total_time

    def _get_pattern(self, colors, interval=3, fraction=True, blend=False):
        """Return pattern

            Parameters:

                    colors: list of colors

                    interval: how to divide pixels (default: 3)

                    fraction: (default: True)
                        True: interval is number of sections
                        False: interval is num pixels for each color

                    blend: true if colors are mixed (default: False)
        """
        if fraction:
            interval = self.get_fraction(interval)
        color = 0
        save = [0] * self.neo.numPixels(self.id)
        i = 0
        while i < self.neo.numPixels(self.id) or color != 0:
            if i + interval >= len(save):
                save.extend([0] * (i + interval - len(save) + 1))
            for j in range(interval):
                if blend:
                    cur_color = self.get_mix(colors[color], colors[(color + 1) % len(colors)], (j / interval) * 100)
                    save[i + j] = cur_color
                else:
                    save[i + j] = self.neo.get_color(*colors[color])
            color = (color + 1) % len(colors)
            i += interval
        return save

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
        self.neo.update_pixel_owner(self.id)
        self._set_save(self._get_pattern(colors, interval, fraction, blend))
        self.neo.show()
        return 0

    def blend(self, radius=5, wait_ms=0, iterations=1):
        """Average pixel color with neighboors

            Parameters:

                radius: amount of neighboors on each side (default: 5)

                wait_ms: amount of time between iterations (default: 0)

                iterations: number of times to blend (default: 1)
        """
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        this_id = self.animation_id.get()
        num_pixels = self.neo.numPixels(self.id)
        amount = .5
        radius += 1
        sides = (1 - float(amount)) / 2
        for i in range(iterations):
            saved = self.save_split()
            for j in range(num_pixels):
                r, g, b = 0, 0, 0
                for k in range(radius):
                    r += saved[(j - k + num_pixels) % num_pixels]["r"]
                    r += saved[(j + k + num_pixels) % num_pixels]["r"]
                    g += saved[(j - k + num_pixels) % num_pixels]["g"]
                    g += saved[(j + k + num_pixels) % num_pixels]["g"]
                    b += saved[(j - k + num_pixels) % num_pixels]["b"]
                    b += saved[(j + k + num_pixels) % num_pixels]["b"]
                r /= radius * 2
                g /= radius * 2
                b /= radius * 2
                self.neo.setPixelColor(self.id, j, r, g, b)
            if wait_ms > 0:
                self.neo.show(15)
                if t.sleepBreak(self.animation_id.get, this_id, wait_ms):
                    return 0
        self.neo.show()
        return wait_ms * iterations

    def fade(self, target=0, wait_ms=1000, restore_mode="off", steps=100):
        """Set brightness to target in steps

            Parameters:

                target: final brightness (default: 0)
        
                wait_ms: total time before target brightness is reached (default: 1000)

                restore_mode: set brightness after (default: off)
                    "off": set pixels to off then restore brightness to original
                    "brightnesss": set pixels to original brightness
                    *: keep brightness at target brightness and color original

                steps: number of brightness changes before target (default: 100)
        """
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        this_id = self.animation_id.get()
        brightness = self.neo.getBrightness()
        change = (target - brightness) / steps
        wait = wait_ms / steps
        original = brightness
        for i in range(steps):
            brightness += change
            self.neo.setBrightness(int(brightness))
            self.neo.show(15)
            if t.sleepBreak(self.animation_id.get, this_id, wait):
                return 0
        if restore_mode == "off":
            self.set_all(0,0,0)
            self.neo.setBrightness(original)
            self.animation_id.increment()
        elif restore_mode == "brightness":
            self.neo.setBrightness(original)
        self.neo.show()
        return wait_ms

    def fade_alt(self, target=0, wait_ms=1000, steps=100, color=None):
        """Similar to fade but switches all pixels to color at target brightness

            Parameters:

                target: final brightness (default: 0)
        
                wait_ms: total time before target brightness is reached (default: 1000)

                steps: number of brightness changes before target (default: 100)

                color: (default: None)
                    None: use current color
                    random: change to random color
                    Anything else: use given color
        """
        original = self.neo.getBrightness()
        self.fade(target, int(wait_ms / 2), "none", steps)
        if color == "random":
            c = self.neo.get_color_seperate(self.neo.get_random_color())
            self.set_all(c[0], c[1], c[2])
        elif isinstance(color, list):
            self.set_all(color[0], color[1], color[2])
        elif color is not None:
            c = self.neo.get_color_seperate(color)
            self.set_all(c[0], c[1], c[2])
        self.fade(original, int(wait_ms / 2), "none", steps)
        return wait_ms

    def pulse_pattern(self, colors, length=5, wait_ms=50, wait_total=False, spacing=3, direction=0):
        """Shift pattern across shift

            Parameters:

                colors: list of colors (1st is background color if multiple given)

                length: how many pixels per color (default: 5)

                wait_ms: delay between shifts (default: 50)

                wait_total: if true, wait_ms is total time of each pulse (default: False)

                spacing: how many background color in between each color (default: 3)

                direction: initial direction (default: 0)
                    -1: backwards
                    *: forwards
        """
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        this_id = self.animation_id.get()
        sep_color = [0, 0, 0]
        if len(colors) > 1:
            sep_color = colors[0]
            colors = colors[1:]
        p_colors = []
        for i in colors:
            p_colors.append(i)
            for j in range(spacing):
                p_colors.append(sep_color)
        pixels = self._get_pattern(p_colors, length, False, False)
        s_amount = 1
        if direction == -1:
            s_amount = -1
        each_wait = wait_ms
        if wait_total:
            each_wait = wait_ms / self.neo.numPixels(self.id)
        self.shift(s_amount, each_wait, len(pixels), pixels)
        return each_wait * len(pixels)

    def twinkle(self, wait_ms=250, iterations=10, l=0.05, u=1, restore=True):
        """Cause individual pixels to flicker

            Parameters:

                wait_ms: time between changes in ms (default: 250)

                iterations: number of times to repeat (default: 10)

                l: lower bound of possible brightnesses (default: 0.05)

                u: upper bound of possible brightnesses (default: 1)

                restore: undo changes when done (default: True)
        """
        t = Timer(self.neo.numMaxPixels(), self.start_time)
        this_id = self.animation_id.get()
        mx = 255
        mn = 0
        lights_save = self.save_split()
        ls = self.save()
        for itr in range(iterations):
            for v in lights_save:
                br = random.uniform(l, u)
                nr = int(v["r"] * br)
                ng = int(v["g"] * br)
                nb = int(v["b"] * br)
                new = [nr, ng, nb]
                if nr > mx or nb > mx or ng > mx or nr < mn or ng < mn or nb < mn:
                    new = [v["r"], v["g"], v["b"]]
                pr, pg, pb = new[0], new[1], new[2]
                self.neo.setPixelColor(self.id, v["id"], pr, pg, pb)
            self.neo.show(15)
            if t.sleepBreak(self.animation_id.get, this_id, wait_ms):
                return 0
        if restore:
            self._set_save(ls)
        return wait_ms * iterations


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
        """Returns rounded fraction"""
        return round(self.neo.numPixels(self.id) / int(num))

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions.
        
            Parameters:

                pos: current pixel
        """
        if pos < 85:
            return self.neo.get_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return self.neo.get_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return self.neo.get_color(0, pos * 3, 255 - pos * 3)

    def get_mix(self, color_1, color_2, percent):
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
        return self.neo.get_color(r, g, b)
