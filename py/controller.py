import time
import threading

from py.neopixels import NeoPixels
from py.virtual_strip import VirtualStrip

class Controller:
    def __init__(self, remote=False):
        self.virtual_strips = {}
        self.neo = NeoPixels(**{"remote": remote})
        self.base_layer = []
        self.animation_layer = []
        self.overlay_layer = []
        self.control_layer = []
        self.on = True
        self.active = True
        self.paused = False
        self.starttime = time.time()
        self.set_framerate(0)
        self._init_data()
        self._start_loop()

    def add_strip(self, name):
        pass

    def get_framerate(self):
        return self.framerate

    def set_framerate(self, value):
        if value is not None:
            self.framerate = value
            if value == 0:
                self.wait_time = 60000
            else:
                self.wait_time = 1000 / self.framerate
            print("Setting framerate to", self.framerate, "with waittime", self.wait_time)
            self.starttime = time.time()

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
        print(settings, self.on)

    def set_base(self, data):
        self.base_layer = self._layer(self.base_layer, data)
        # print("Base Layer is now:", self.base_layer)

    def set_animation(self, data):
        if len(data) > 0:
            self.animation_layer = data
            print("Animation layer is now:", self.animation_layer)

    def set_control(self, data):
        self.control_layer = data
        print("Control Layer is now:", self.control_layer)

    def info(self):
        data = {
            "controller_id": 0,
            "error": False,
            "message": None,
            "strip_info": [],
            "strips": [{
                "strip_id": 0,
            #    "data": self.strips[0].save_split()
            }]
        }
        return data

    def _init_data(self):
        self.base_layer = [0] * self.neo.num_pixels()
        self.animation_layer.append([])
        for i in range(self.neo.num_pixels()):
            self.animation_layer[0].append(0)
   
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
            time.sleep(.001)

    def _start_loop(self):
        threading_thread = threading.Thread(target=self._loop)
        threading_thread.start()
    
    def _loop(self):
        self.starttime = time.time()
        self.counter = 0
        while self.active:
            if not self.paused:
                self.counter = (self.counter + 1) % len(self.animation_layer)
                self.neo.update_pixels(self._layer(self.base_layer, self.animation_layer[self.counter], self.control_layer))
                self.neo.show(20)
                # print(self.control_layer)
            self._sleep(self.wait_time)

