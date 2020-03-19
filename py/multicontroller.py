# import requests
import time
# import socketio

from py.controller import Controller
from py.animation import Animations


class MultiController:
    def __init__(self, remote=False):
        self.a = Animations()
        self.controllers = [0] * 1
        self.controllers[0] = Controller(**{"remote": remote})
        self.reset_all()

    def reset_all(self):
        actions = [{
            "type": "base",
            "function": "color",
            "arguments": {"r": 0, "g": 0, "b": 0}
        }]
        data = self.a.calc(actions, self.controllers[0].num_pixels())["base"]
        for c in self.controllers:
            c.set_base(data)
            c.next_frame()

    def execute(self, actions):
        data = self.a.calc(actions, self.controllers[0].num_pixels())
        if data.get("settings") is not None:
            self.controllers[0].set_settings(data["settings"])
        if data.get("base") is not None:
            self.controllers[0].set_base(data["base"])
        if data.get("animation") is not None:
            self.controllers[0].set_animation(data["animation"])
        if data.get("control") is not None:
            self.controllers[0].set_control(data["control"])
        if data.get("framerate") is not None:
            self.controllers[0].set_framerate(data["framerate"])

    def pixel_info(self):
        response = []
        for i in range(len(self.controllers)):
            info = {}
            info["strip_info"] = [{"id": 0, "start": 0, "end": self.controllers[i].num_pixels() - 1}]
            info["pixels"] = self.controllers[i].get_pixels()
            response.append(info)
        return response

    def info(self):
        data = []
        for c in self.controllers:
            data.append(c.info())
        return data
