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
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)

PROVIDED_MILLIAMPS = 10000
POWER_MULTIPLIER = 0.9
MAX_MILLIAMPS = PROVIDED_MILLIAMPS*POWER_MULTIPLIER

PROVIDED_WATTS = 1
VOLTAGE = 5

class NeoPixels:
    def __init__(self, led_count=60, max_brightness=20, pin=18, grb=False, remote=True):
        # Configuration Settings
        self.led_count = led_count
        self.max_brightness = max_brightness
        self.pin = pin
        self.grb = grb
        self.remote = remote
        self.led_channel = self.pin in [13, 19, 41, 45, 53]
        # Current Pixels
        self.led_data = [0] * led_count
        self.brightness = self.max_brightness
        # Other
        self.last_show = time.time()
        # Actual Strip
        self.strip = Adafruit_NeoPixel(
            self.led_count, self.pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, self.max_brightness, self.led_channel)
        print(self.remote)
        if not self.remote:
            print("Not remote")
            self.strip.begin()

    def _valid_range(self, start, end):
        if start < 0 or start >= self.led_count:
            return False
        if end < 0 or end >= self.led_count:
            return False
        if start > end:
            return False
        return True

    def num_pixels(self):
        return self.led_count

    def set_brightness(self, value):
        if value >= 0 and value <= self.max_brightness:
            self.brightness = value
            if not self.remote:
                self.strip.setBrightness(self.brightness)

    def get_brightness(self):
        return self.brightness

    def get_pixels(self):
        return self.led_data

    def update_pixels(self, data):
        if len(data) < self.led_count:
            return -1
        for i in range(0, self.led_count):
            if data[i] != -1:
                self.led_data[i] = data[i]

    def show(self, limit=0):
        # print("Showing:", self.led_data)
        if not self.remote:
            if time.time() >= self.last_show + (limit / 1000) or limit == 0:
                for i in range(self.led_count):
                    self.strip.setPixelColor(i, self.led_data[i])
                self.strip.show()
                self.last_show = time.time()

if __name__ == "__main__":
    neo = NeoPixels(60, 255, 18, True, True)