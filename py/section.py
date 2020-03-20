import time

class Section:
    def __init__(self, data, controller_led_count):
        print("Section:", data)
        self.led_count = controller_led_count
        self.data = data
        self.framerate = 0
        self.wait_time = None
        self.animation_layer = []
        self.animation_layer.append([-1] * self.data["length"])
        self.starttime = time.time()
        self.counter = 0

    def _expand_frame(self, data):
        frame = [-1] * self.led_count
        frame[self.data["start"]:self.data["end"]] = data[self.data["offset"]:self.data["offset"] + self.data["length"]]
        return frame

    def set_animation(self, data):
        # print("Setting animation to", data)
        if len(self.animation_layer) > 0:
            self.counter = 0
            self.starttime = time.time()
            self.animation_layer = data

    def set_framerate(self, value):
        self.framerate = value
        if value == 0:
            self.wait_time = None
            return
        self.wait_time = 1 / self.framerate
        print("Set framerate", self.framerate, self.wait_time)

    def get_frame(self):
        # print("Get frame", self.wait_time, self.counter)
        if self.wait_time is None:
            return self._expand_frame(self.animation_layer[self.counter % len(self.animation_layer)])
        if time.time() > (self.starttime + self.counter * self.wait_time):
            self.counter += 1
        return self._expand_frame(self.animation_layer[self.counter % len(self.animation_layer)])