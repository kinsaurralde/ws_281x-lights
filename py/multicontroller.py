# import requests
import time
# import socketio

from py.controller import Controller
from py.virtualcontroller import VirtualController

class MultiController:
    def __init__(self, testing, config, virtual_controller_config):
        self.testing = testing
        self.controllers = {}
        self.virtual_controllers = {}
        self._init_controllers(config)
        self._init_virtual_controllers(virtual_controller_config)

    def _init_controllers(self, config):
        counter = 0
        self.virtual_controllers["ALL"] = VirtualController("ALL", False)
        for c in config["controllers"]:
            if c["active"]:
                self.controllers[c["name"]] = Controller(c["name"], c, testing=self.testing)
                self.virtual_controllers[c["name"]] = VirtualController(c["name"] + "_virtual", True)
                self.virtual_controllers[c["name"]].add_controller_info(c["name"], 0, c["neopixels"]["led_count"] - 1, 0)
                self.controllers[c["name"]].set_strip(self.virtual_controllers[c["name"]].get_controller_info(c["name"]))
                self.virtual_controllers["ALL"].add_controller_info(c["name"], 0, c["neopixels"]["led_count"] - 1, 0)
                counter += 1
        
    def _init_virtual_controllers(self, config):
        for v in config["virtual_controllers"]:
            self.virtual_controllers[v["name"]] = VirtualController(v["name"], False)
            for s in v["sections"]:
                self.virtual_controllers[v["name"]].add_controller_info(**s)
        for c in self.controllers:
            for v in self.virtual_controllers:
                self.controllers[c].set_strip(self.virtual_controllers[v].get_controller_info(c))

    def _get_options(self, options):
        virtual_controllers = ["middle_half"]
        if options is not None:
            if "virtual_controllers" in options:
                virtual_controllers = options["virtual_controllers"]
        return {"virtual_controllers": virtual_controllers}

    def execute(self, actions, options={}):
        options = self._get_options(options)
        vcontrollers = options["virtual_controllers"]
        print("V", vcontrollers)
        for vc in vcontrollers:
            if vc not in self.virtual_controllers and vc + "_virtual" not in self.virtual_controllers:
                print("CONTINUE")
                continue
            data = self.virtual_controllers[vc].calc(actions)
            layers = data["layers"]
            controller_info = data["controllers"]
            print("Contorller info", vc, controller_info)
            for c in controller_info:
                if c["id"] not in self.controllers:
                    continue
                section_id = c["virtual_id"] + "_" + c["section_id"]
                if layers.get("settings") is not None:
                    self.controllers[c["id"]].set_settings(layers["settings"])
                if layers.get("base") is not None:
                    self.controllers[c["id"]].set_base(layers["base"][c["offset"]:c["offset"] + c["length"]], c["start"], c["end"] + 1)
                if layers.get("animation") is not None:
                    self.controllers[c["id"]].set_animation(layers["animation"], section_id)
                if layers.get("control") is not None:
                    self.controllers[c["id"]].set_control(layers["control"])
                if layers.get("framerate") is not None:
                    self.controllers[c["id"]].set_framerate(layers["framerate"], section_id)

    def set_brightness(self, data):
        result = []
        for row in data:
            id = row["id"]
            if id in self.controllers:
                result.append({"id": id, "value": self.controllers[id].set_brightness(int(row["value"]))})
        return result

    def pixel_info(self):
        response = []
        for i in self.controllers:
            info = {}
            info["strip_info"] = [{"id": 0, "start": 0, "end": self.controllers[i].num_pixels() - 1}]
            info["pixels"] = self.controllers[i].get_pixels()
            response.append(info)
        return response

    def info(self):
        data = []
        for c in self.controllers:
            data.append(self.controllers[c].info())
        return data

    def vinfo(self):
        data = []
        for v in self.virtual_controllers:
            data.append(self.virtual_controllers[v].info())
        return data
