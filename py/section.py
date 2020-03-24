import time

class Section:
    def __init__(self, data, controller_led_count):
        self.led_count = controller_led_count
        self.data = data
        self.framerate = 0
        self.wait_time = None
        self.control_layer = []
        self.animation_layer = []
        self.base_layer = []
        self.animation_layer.append([[-1] * self.data["length"], 'test'])
        self.starttime = time.time()
        self.counter = 0

    def _expand_frame(self, data):
        frame = [-1] * self.led_count
        frame[self.data["start"]:self.data["end"]] = data[self.data["offset"]:self.data["offset"] + self.data["length"]]
        return frame

    def _layer(self, *args):
        layer = [-1] * max([len(i) for i in args])
        for l in args:
            for i in range(len(l)):
                if l[i] >= 0:
                    layer[i] = l[i]
        return layer

    def _special(self, actions):
        for action in actions:
            if action == "animation_to_base":
                self.set_base(self.animation_layer[self.counter % len(self.animation_layer)][0])

    def set_control(self, data):
        self.control_layer = self._expand_frame(data)

    def set_animation(self, data):
        if len(self.animation_layer) > 0:
            self.counter = 0
            self.starttime = time.time()
            self.animation_layer = data

    def set_base(self, data):
        self.base_layer = self._expand_frame(data)

    def set_framerate(self, value):
        self.framerate = value
        if value == 0:
            self.wait_time = None
            return
        self.wait_time = 1 / self.framerate

    def get_frame(self):
        animation_frame = self.animation_layer[self.counter % len(self.animation_layer)]
        if isinstance(animation_frame[0], list):
            animation_layer = self._expand_frame(animation_frame[0])
            self._special(animation_frame[1])
        else:
            animation_layer = animation_frame
        frame = self._layer(self.base_layer, animation_layer, self.control_layer)
        if self.wait_time is not None:
            if time.time() > (self.starttime + self.counter * self.wait_time):
                self.counter += 1
        return frame
