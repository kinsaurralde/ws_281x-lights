# import requests
import time
# import socketio

from py.controller import Controller
from py.animations import Animations


class MultiController:
    def __init__(self):
        self.a = Animations()
        self.controllers = [0] * 1
        self.controllers[0] = Controller()
        self.reset_all()

    def reset_all(self):
        actions = [{
            "type": "run",
            "function": "color",
            "arguments": {"r": 1, "g": 1, "b": 1}
        }]
        data = self.a.calc(actions, self.controllers[0].num_pixels())
        for c in self.controllers:
            c.set_data(data)

    def execute(self, actions):
        data = self.a.calc(actions, self.controllers[0].num_pixels())
        self.controllers[0].set_data(data)

    def pixel_info(self):
        response = []
        for i in range(len(self.controllers)):
            info = self.controllers[i].get_pixels()
            if info is not None:
                response.append(info)
        return response

    def info(self):
        data = []
        for c in self.controllers:
            data.append(c.info())
        return data
