import time
import threading

from py.neopixels import NeoPixels
from py.animation import Animations

class Controller:
    def __init__(self, name_id, config, testing=False):
        self.id = name_id
        self.config = config
        self.base_layer = []
        self.animation_layer = []
        self.overlay_layer = []
        self.control_layer = []
        self.on = True
        self.active = True
        self.paused = False
        self.starttime = time.time()
        self.framerate = 50
        self.wait_time = 1000 / self.framerate
        self.animation_framerate_multiplier = 1
        self.animation_framerate = 60
        self.animation_wait_time = 1000 / self.animation_framerate
        self.remote = not config["calculate"]
        self.neo = NeoPixels(**config["neopixels"], testing=(testing or self.remote))
        self.neo.set_brightness(int(config["settings"]["initial_brightness"]))
        self.neo.set_gamma(config["settings"]["correction"]["gamma"])
        self.a = Animations(self.neo.num_pixels())
        self._init_data()
        self._start_loop()
        print("Created controller with id", name_id)

    def set_strip(self, data):
        raise NotImplementedError

    def get_framerate(self):
        return {
            "draw_framerate": self.framerate, 
            "draw_waitms": self.wait_time,
            "animation_framerate": self.animation_framerate,
            "animation_waitms": self.animation_wait_time,
            "animation_multiplier": self.animation_framerate_multiplier
        }

    def set_framerate_value(self, value):
        if value > 0:
            self.framerate = value
            self.wait_time = 1000 / self.framerate

    def set_framerate(self, data):
        if "draw" in data:
            value = int(data["draw"])
            if value > 0:
                self.framerate = value
                self.wait_time = 1000 / self.framerate
        if "animation" in data:
            value = int(data["animation"])
            if value > 0:
                self.animation_framerate = value
                self.animation_wait_time = 1000 / self.animation_framerate
        if "animation_multiplier" in data:
            value = int(data["animation_multiplier"])
            if value > 0:
                self.animation_framerate_multiplier = value
        return self.get_framerate()

    def num_pixels(self):
        return self.neo.num_pixels()

    def get_pixels(self):
        data = self.neo.get_pixels()
        return data

    def get_id(self):
        return self.id

    def set_settings(self, settings):
        for setting in settings:
            if setting == "on":
                self.on = bool(settings[setting])

    def set_base(self, data):
        self.base_layer = data
        self._draw_frame()

    def set_animation(self, data):
        if len(data) > 0:
            self.animation_layer = data

    def set_control(self, data):
        self.control_layer = data
        self._draw_frame()

    def set_brightness(self, data):
        return self.neo.set_brightness(data)

    def get_brightness(self):
        return self.neo.get_brightness()

    def get_power_usage(self):
        return self.neo.get_power_usage(False)

    def calc(self, actions):
        return self.a.calc(actions)

    def info(self):
        data = {"controller_id": self.id, "remote": self.config["remote"]}
        data["neopixels"] = self.neo.info()
        data["framerate"] = self.get_framerate()
        return data

    def ping(self):
        return time.time()

    def _init_data(self):
        self.base_layer = [0] * self.neo.num_pixels()
        self.animation_layer.append([])
        self.animation_layer[0] = [[], []]
        for i in range(self.neo.num_pixels()):
            self.animation_layer[0][0].append(-1)

    def _valid_range(self, start, end):
        if start < 0 or start > self.neo.num_pixels():
            return False
        if end < 0 or end > self.neo.num_pixels():
            return False
        if start > end:
            return False
        return True
   
    def _layer(self, *args):
        layer = [-1] * max([len(i) for i in args])
        for l in args:
            if len(l) > 0 and isinstance(l[0], list):
                l = l[0]
            for i in range(len(l)):
                if l[i] >= 0:
                    layer[i] = l[i]
        return layer

    def _sleep(self, amount):
        self.starttime += (amount / 1000)
        while time.time() < self.starttime:
            time.sleep(.003)

    def _start_loop(self):
        threading_thread = threading.Thread(target=self._loop)
        threading_thread.start()

    def _special(self, frame):
        for action in frame[1]:
            if action == "animation_to_base":
                self.base_layer = frame[0]

    def _draw_animation(self):
        frame = self.animation_layer[self.counter]
        if isinstance(frame, list):
            self._special(frame)
            return frame[0]
        return frame

    def _draw_frame(self):
        if self.counter < len(self.animation_layer):
            self.neo.update_pixels(self._layer(self.base_layer, self._draw_animation(), self.control_layer))
            self.neo.show(20)
    
    def _loop(self):
        self.starttime = time.time()
        self.counter = 0
        while self.active:
            if not self.paused and len(self.animation_layer) > 0:
                self.counter = (self.counter + self.animation_framerate_multiplier) % len(self.animation_layer)
                self._draw_frame()
            self._sleep(self.animation_wait_time)
