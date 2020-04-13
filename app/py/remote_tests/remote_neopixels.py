import time
import socketio

from py.neopixels import NeoPixels

class RemoteNeopixels(NeoPixels):
    def __init__(self, led_count=60, max_brightness=255, pin=18, max_watts=1, watts_per_60=18, grb=False, testing=True, flipped=True, url=None):
        self.url = url
        self.sio = socketio.Client()
        self._connect()
        super().__init__(led_count=led_count, max_brightness=max_brightness, pin=pin, max_watts=max_watts, watts_per_60=watts_per_60, grb=grb, testing=testing, flipped=flipped)

    def _connect(self):
        try:
            self.sio.connect(self.url)
        except socketio.exceptions.ConnectionError:
            print("Failed to connect to", self.url)

    def _emit(self, message, data):
        start_time = time.time()
        self.sio.emit(message, data, self._emit_response(start_time))

    def _emit_response(self, start_time):
        # print("Time:", time.time() - start_time)
        pass

    def show(self, limit=0):
        self._emit("neopixel_update", {"pixels": self.get_pixels()})
        super().show(limit)
            
    def set_brightness(self, value):
        brightness = super().set_brightness(value)
        b = brightness
        if self.gamma[value] is not None:
            b = self.gamma[value]
        self._emit("neopixel_set_brightness", {"value": b})
        return brightness
        