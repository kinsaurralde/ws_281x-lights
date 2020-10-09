import time

import ctypes
import threading
from rpi_ws281x import Adafruit_NeoPixel
from wrapper import Pixels, AnimationArgs, Frame, List, LIB


# Initial LED strip configuration:
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

# TODO: multiple pixel strips


class Animations:
    color = 0
    wipe = 1
    pulse = 2
    rainbow = 3
    cycle = 4


class NeoPixels:
    """Control access to Adafruit_Neopixel()"""

    def __init__(
        self,
        led_count=300,
        max_brightness=255,
        pin=18,
        max_watts=1,
        watts_per_60=18,
        grb=False,
        testing=True,
        flipped=True,
    ):
        # Configuration Settings
        self.pixels = []
        self.led_count = led_count
        self.max_brightness = max_brightness
        self.pin = pin
        self.testing = testing
        self.led_channel = self.pin in [13, 19, 41, 45, 53]
        self.led_strip_count = LIB.ledStripCount()
        self.strip = []
        self._setup()

        self.starttime = time.time()
        self.active = True
        self.paused = False
        self.delay_ms = 5
        self._start_loop()

    def _setup(self):
        for i in range(self.led_strip_count):
            self.pixels.append(Pixels(self.led_count))
            self.strip.append(Adafruit_NeoPixel(
                self.led_count,
                self.pin,
                LED_FREQ_HZ,
                LED_DMA,
                LED_INVERT,
                self.max_brightness,
                self.led_channel,
            ))
            if not self.testing:
                self.strip[i].begin()

    def _sleep(self, amount):
        self.starttime += amount / 1000
        while time.time() < self.starttime:
            time.sleep(self.delay_ms / 2000)

    def _start_loop(self):
        threading_thread = threading.Thread(target=self._loop, daemon=True)
        threading_thread.start()

    def _loop(self):
        self.starttime = time.time()
        while self.active:
            self.updatePixels()
            self._sleep(self.delay_ms / 1000)

    def handleBrightness(self, id, value=None):
        print("Brightness", value, id)
        id = int(id)
        value = int(value)
        if value is not None:
            self.pixels[id].setBrightness(value)
        return self.pixels[id].getBrightness()

    @staticmethod
    def setArgs(values):
        args = AnimationArgs()
        args.animation = int(values["animation"])
        args.color = int(values["color"])
        args.color_bg = int(values["color_bg"])
        args.wait_ms = int(values["wait_ms"])
        args.arg1 = int(values["arg1"])
        args.arg2 = int(values["arg2"])
        args.arg3 = int(values["arg3"])
        args.arg4 = int(values["arg4"])
        args.arg5 = int(values["arg5"])
        args.arg6 = bool(values["arg6"])
        args.arg7 = bool(values["arg7"])
        args.arg8 = bool(values["arg8"])
        colors_list = List(len(values["colors"]))
        args.colors = colors_list.obj
        for i in range(colors_list.size()):
            colors_list.set(i, int(values["colors"][i]))
        return args

    def handleData(self, commands):
        for command in commands:
            pixels_id = int(command["id"])
            self.pixels[pixels_id].setIncrementSteps(int(command["inc_steps"]))
            args = self.setArgs(command)
            if args.wait_ms > 0:
                self.pixels[pixels_id].setDelay(args.wait_ms)
            print(f"Run Animation {args.animation} on id {pixels_id}")
            if args.animation == Animations.color:
                self.pixels[pixels_id].color(args)
            elif args.animation == Animations.wipe:
                self.pixels[pixels_id].wipe(args)
            elif args.animation == Animations.pulse:
                self.pixels[pixels_id].pulse(args)
            elif args.animation == Animations.rainbow:
                self.pixels[pixels_id].rainbow(args)
            elif args.animation == Animations.cycle:
                self.pixels[pixels_id].cycle(args)

    def updatePixels(self):
        for i in range(self.led_strip_count):
            if self.pixels[i].canShow(int(time.time() * 1000)):
                self.pixels[i].increment()
                self.strip[i].setBrightness(self.pixels[i].getBrightness())
                data = self.pixels[i].get()
                if not self.testing:
                    for j in range(self.led_count):
                        self.strip[i].setPixelColor(j, data.contents.main[j])
                    self.strip[i].show()

    def getPixels(self):
        return [list(self.pixels[0].get().contents.main), list(self.pixels[1].get().contents.main)]

    def getInit(self):
        strips = []
        for i in range(self.led_strip_count):
            strips.append(self.pixels[i].isInitialized())
        return strips

    def init(self, values):
        print("Init strip", values)
        strip_id = values["id"]
        self.pixels[strip_id].initialize(values["init"].get("num_leds", 60), values["init"].get("milliwatts", 1000), values["init"].get("brightness", 100), values["init"].get("max_brightness", 127))
        return self.getInit()

