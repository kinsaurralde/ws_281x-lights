import time
import threading

from py.neopixels import NeoPixels
from py.section import Section

class Controller:
    def __init__(self, name_id, config, testing=False):
        self.id = name_id
        self.config = config
        self.neo = NeoPixels(**config["neopixels"], testing=testing)
        self.base_layer = []
        self.animation_layer = []
        self.overlay_layer = []
        self.control_layer = []
        self.sections = {}
        self.on = True
        self.active = True
        self.paused = False
        self.starttime = time.time()
        # self.framerate = 60
        self.wait_time = 8
        self._init_data()
        self._start_loop()

    def set_strip(self, data):
        for i in data:
            self.sections[str(data[i]["virtual_id"]) + "_" + str(data[i]["section_id"])] = Section(data[i], self.neo.num_pixels())

    def get_framerate(self):
        return self.framerate

    def set_framerate(self, value, vs_id):
        self.sections[vs_id].set_framerate(value)

    def next_frame(self):
        self.starttime = time.time()

    def num_pixels(self):
        return self.neo.num_pixels()

    def get_pixels(self):
        data = self.neo.get_pixels()
        return data

    def set_settings(self, settings):
        for setting in settings:
            if setting == "on":
                self.on = bool(settings[setting])
        # print(settings, self.on)

    def set_base(self, data, start=0, end=None):
        if end is None:
            end = self.neo.num_pixels()
        if not self._valid_range(start, end):
            return 
        self.base_layer[start:end] = self._layer(self.base_layer[start:end], data[0:end-start])
        self._draw_frame()
        # print("Base Layer is now", self.base_layer)

    def set_animation(self, data, vs_id):
        if len(data) > 0:
            self.sections[vs_id].set_animation(data)

    def set_control(self, data):
        self.control_layer = data
        self._draw_frame()

    def set_brightness(self, data):
        return self.neo.set_brightness(data)

    def info(self):
        data = {"controller_id": self.id, "remote": self.config["remote"]}
        data["neopixels"] = self.neo.info()
        return data

    def _init_data(self):
        self.base_layer = [0] * self.neo.num_pixels()
        self.animation_layer.append([])
        for i in range(self.neo.num_pixels()):
            self.animation_layer[0].append(-1)

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
            for i in range(len(l)):
                if l[i] >= 0:
                    layer[i] = l[i]
        return layer

    def _sleep(self, amount):
        self.starttime += (amount / 1000)
        while time.time() < self.starttime:
            time.sleep(.0025)

    def _start_loop(self):
        threading_thread = threading.Thread(target=self._loop)
        threading_thread.start()

    def _draw_animation(self):
        frame = [-1] * self.neo.num_pixels()
        for s in self.sections:
            frame = self._layer(frame, self.sections[s].get_frame())
        return frame

    def _draw_frame(self):
        if self.counter < len(self.animation_layer):
            # self._draw_animation()
            self.neo.update_pixels(self._layer(self.base_layer, self._draw_animation(), self.control_layer))
            self.neo.show(20)
    
    def _loop(self):
        self.starttime = time.time()
        self.counter = 0
        while self.active:
            if not self.paused:
                self.counter = (self.counter + 1) % len(self.animation_layer)
                self._draw_frame()
            self._sleep(self.wait_time)

