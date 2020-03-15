import time
import threading

from py.neopixels import NeoPixels
from py.virtual_strip import VirtualStrip

class Controller:
    def __init__(self):
        self.virtual_strips = {}
        self.neo = NeoPixels()
        self.data = []
        self.on = True
        self.active = True
        self.starttime = time.time()
        self.framerate = 2
        self.wait_time = 1000 / self.framerate
        self._init_data()
        self._start_loop()

    def add_strip(self, name):
        pass

    def get_framerate(self):
        return self.framerate

    def set_framerate(self, value):
        self.framerate = value
        self.wait_time = 1000 / self.framerate

    def num_pixels(self):
        return self.neo.num_pixels()

    def get_pixels(self):
        data = self.neo.get_pixels()
        return data

    def set_data(self, data):
        print("Updaing pixels with data", data)
        self.data = data

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
        self.data.append([])
        for i in range(self.neo.num_pixels()):
            self.data[0].append(0)

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
            self.counter = (self.counter + 1) % len(self.data)
            self.neo.update_pixels(self.data[self.counter])
            self.neo.show()
            self._sleep(self.wait_time)

