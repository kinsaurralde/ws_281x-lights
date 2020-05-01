# import requests
import time
# import socketio

from py.remote_controller import RemoteController
from py.controller import Controller
from py.animation import Animations

class MultiController:
    def __init__(self, testing, config, virtual_controller_config):
        self.testing = testing
        self.controllers = {}
        self._init_controllers(config)

    def _init_controllers(self, config):
        for c in config["controllers"]:
            if c["active"]:
                if c["remote"]:
                    controller = RemoteController(c["name"], c, testing=self.testing)
                else:
                    controller = Controller(c["name"], c, testing=self.testing)
                self.controllers[c["name"]] = controller
                
    def execute(self, actions, options={}):
        controllers = self.controllers.keys()
        a = Animations(0)
        for controller in controllers:
            a.set_led_count(self.controllers[controller].num_pixels())
            a.set_grb(self.controllers[controller].neo.grb)
            layers = a.calc(actions)
            if layers.get("settings") is not None:
                self.controllers[controller].set_settings(layers["settings"])
            if layers.get("base") is not None:
                self.controllers[controller].set_base(layers["base"])
            if layers.get("animation") is not None:
                if len(layers.get("animation")) > 0:
                    self.controllers[controller].set_animation(layers["animation"])
            if layers.get("control") is not None:
                self.controllers[controller].set_control(layers["control"])
            if layers.get("framerate") is not None:
                self.controllers[controller].set_framerate_value(layers["framerate"])

    def set_brightness(self, data):
        result = []
        for row in data:
            cid = row["id"]
            if cid in self.controllers:
                result.append({"id": cid, "value": self.controllers[cid].set_brightness(int(row["value"]))})
        return result

    def set_framerate(self, data):
        result = []
        for row in data:
            cid = row["id"]
            if cid in self.controllers:
                result.append({"id": cid,"value": self.controllers[cid].set_framerate(row["data"])})
        return result

    def get_brightness(self):
        result = []
        for c in self.controllers:
           result.append({"id": c, "value": self.controllers[c].get_brightness()})
        return result 

    def pixel_info(self):
        response = []
        for i in self.controllers:
            response.append({
                "controller_id": self.controllers[i].get_id(),
                "pixels": self.controllers[i].get_pixels(),
                "watts": self.controllers[i].get_power_usage()
            })
        return response

    def info(self):
        data = []
        for c in self.controllers:
            data.append(self.controllers[c].info())
        print("Info", data, len(self.controllers))
        return data

    def vinfo(self):
        return data

    def ping(self):
        data = []
        for c in self.controllers:
            info = {"controller_id": c}
            start = time.time()
            mid = self.controllers[c].ping()
            end = time.time()
            info["start"] = start
            info["mid"] = mid
            info["end"] = end
            info["ping"] = (end - start) * 1000
            data.append(info)
        return data
