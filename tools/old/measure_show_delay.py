#!/usr/bin/env python3
import time
import random
import sys

from rpi_ws281x import Adafruit_NeoPixel as neo

class Tester():
    def __init__(self):
        self.num_pixels = 1
        self._create_strip(1)
        self.data = []
        self.cur_test = []

    def _create_strip(self, num_pixels):
        self.num_pixels = num_pixels
        self.strip = neo(self.num_pixels, 18, 800000, 10, False, 255, 0)
        self.strip.begin()

    def _time_show(self):
        start_time = time.time()
        self.strip.show()
        end_time = time.time()
        self.cur_test.append((end_time - start_time) * 1000)

    def _set_color(self, r, g, b):
        for i in range(0, self.strip.numPixels()):
            self.strip.setPixelColorRGB(i, r, g, b)
        self._time_show()

    def test(self, max_pixels, num_trials):
        for i in range(max_pixels + 1):
            num_pixels = i
            self._create_strip(num_pixels)
            self.cur_test = []
            for j in range(num_trials):
                self._set_color(int(255 * (i / max_pixels)), 0, int(255 * (j / num_trials)))
            self.data.append({
                "num_pixels": num_pixels,
                "data": self.cur_test
            })

    def print(self):
        top_row = ""
        for i in range(len(self.data[0]["data"])):
            top_row += "," + str(i + 1)
        print(top_row)
        for row in self.data:
            print(str(row["num_pixels"]) + "," + str(row["data"]).strip('[]'))


if __name__ == '__main__':
    t = Tester()
    t.test(int(sys.argv[1]),100)
    t.print()

