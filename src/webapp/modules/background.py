import threading
import time


class Background:
    def __init__(self, socketio, controller, pixels_simulate):
        self.socketio = socketio
        self.controller = controller
        self.active = True
        self.pixels_simulate = pixels_simulate
        self.delay_ms = 25
        self.pixel_interval = 25
        self.pixels_active = self.pixels_simulate
        self.emit_delay_ms = 1000
        self.full_cycle = 12
        self.data = {}
        self.start_time = time.time()

    def startLoop(self):
        thread = threading.Thread(target=self._loop)
        thread.start()

    def updatePing(self):
        self.controller.updateControllerLatencies(self)
        self.data["ping"] = self.controller.getControllerLatencies()

    def updateData(self):
        self.data.update(self.controller.getBackgroundData())

    def emitUpdate(self):
        if len(self.data) > 0:
            self.socketio.emit("update", self.data)

    def setPixelInterval(self, value):
        if value >= self.delay_ms:
            self.pixel_interval = value

    def getPixelInterval(self):
        return self.pixel_interval

    def setPixelsActive(self, value):
        if value == "true":
            self.pixels_active = True
        else:
            self.pixels_active = False

    def getPixelsActive(self):
        return self.pixels_active

    def _loop(self):
        counter = 0
        loop_counter = 0
        self.data = {}
        while self.active:
            if counter % self.emit_delay_ms == 0:
                if loop_counter % self.full_cycle == 0:
                    self.updatePing()
                loop_counter += 1
                counter = 0
                self.emitUpdate()
                self.data = {}
            if (
                counter % self.pixel_interval == 0
                and self.pixels_simulate
                and self.pixels_active
            ):
                pixels = self.controller.getPixels()
                self.socketio.emit("pixels", pixels)
            time.sleep(self.delay_ms / 1000)
            counter += self.delay_ms
