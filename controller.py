import threading
import time

from lights import *


class Controller:
    def __init__(self, controller_id):
        # Settings
        self.brightness = 100
        neopixels.setBrightness(self.brightness)
        self.num_pixels = neopixels.numMaxPixels()
        self.break_animation = True
        self.layer = False
        self.id = controller_id

        self.strips = []
        self.strip_data = []
        self.create_strip(0, self.num_pixels - 1)


    def init_neopixels(self, data):
        neopixels.init_neopixels(data["neopixels"])
        self.num_pixels = neopixels.numMaxPixels()
        if "settings" in data:
            if "initial_brightness" in data["settings"]:
                neopixels.setBrightness(data["settings"]["initial_brightness"])
        self.strips = []
        self.strip_data = []
        self.create_strip(0, self.num_pixels - 1)
        for strip in data["strips"]:
            self.create_strip(strip["start"], strip["end"])

    def create_strip(self, start, end):
        strip_id = len(self.strips)
        self.strips.append(Lights(strip_id))
        data = {
            "id": strip_id,
            "start": start,
            "end": end,
        }
        self.strip_data.append(data)
        neopixels.update(self.strip_data)

    def info(self):
        data = self.response("info", False, None, True)
        data["power"] = neopixels.get_power_info()
        return data

    def response(self, command_run, error, message, detailed=False, strip_id=None):
        data = {
            "controller_id": self.id,
            "command_run": command_run,
            "error": error,
            "message": message,
            "strip_info": self.strip_data,
        }
        if detailed:
            data["settings"] = self.get_all_settings()
            data["strips"] = []
            if strip_id == None:
                for i in range(len(self.strips)):
                    data["strips"].append({
                        "strip_id": i,
                        "data": self.strips[i].save_split()
                    })
            else:
                data["strips"].append({
                    "strip_id": strip_id,
                    "data": self.strips[strip_id].save_split()
                })
        return data

    def stop(self, strip_id=None):
        if strip_id == None:
            for strip in self.strips:
                strip.stop_animation()
        else:
            self.strips[strip_id].stop_animation()
        return self.response("stop", False, None, False, strip_id)

    def off(self, strip_id=None):
        if strip_id == None:
            for strip in self.strips:
                strip.off()
        else:
            self.strips[strip_id].off()
        return self.response("off", False, None, False, strip_id)

    def get_brightness(self):
        self.brightness = neopixels.getBrightness()
        return self.brightness

    def set_brightness(self, value):
        self.brightness = value
        neopixels.setBrightness(value)
        neopixels.show()

    def set_layer(self, value):
        self.layer = bool(value)
        for strip in self.strips:
            strip.set_layer(self.layer)

    def get_break_animation(self):
        return self.break_animation

    def set_break_animation(self, value):
        self.break_animation = value

    def get_all_settings(self):
        self.brightness = neopixels.getBrightness()
        cur_settings = {
            "brightness": self.brightness,
            "break_animation": self.break_animation,
            "num_pixels": self.num_pixels,
        }
        return cur_settings

    def _run_functions(self, name, strip):
        run_functions = {   # all functions
            "color": strip.set_all,
            "random": strip.random_cycle,
            "wipe": strip.wipe,
            "single": strip.set_pixel,
            "specific": strip.set_pixels,
            "pulse": strip.pulse,
            "chase": strip.chase,
            "shift": strip.shift,
            "rainbowCycle": strip.rainbow_cycle,
            "rainbow": strip.rainbow,
            "rainbowChase": strip.rainbow_chase,
            "mix": strip.mix_switch,
            "reverse": strip.reverse,
            "bounce": strip.bounce,
        }
        if name in run_functions:
            return run_functions[name]
        else:
            raise NameError

    def run(self, strip_id, function, arguments=None, is_dict=False):
        self.strips[strip_id].animation_id.increment()
        run_function = self._run_functions(function, self.strips[strip_id])
        if arguments == None:
            run_function()
        elif isinstance(arguments, dict):
            run_function(**arguments)
        elif function == "specific" or function == "mix":
            run_function(arguments)
        else:
            run_function(*arguments)
        return self.response(function, False, None, False, strip_id)

    def thread(self, strip_id, function, arguments, is_dict=False):
        neopixels.update_pixel_owner(strip_id)
        threading_function = self._run_functions(
            function, self.strips[strip_id])
        if isinstance(arguments, dict):
            threading_thread = threading.Thread(target=threading_function, kwargs=arguments)
        else:
            threading_thread = threading.Thread(target=threading_function, args=arguments)
        threading_thread.start()
        return self.response(function, False, None, False, strip_id)

    def animate(self, strip_id, function, arguments, delay_between=0, dont_split=False):
        self.strips[strip_id].animation_id.increment()
        this_id = self.strips[strip_id].animation_id.get()
        neopixels.update_pixel_owner(strip_id)
        if function == "mix":
            dont_split = True
        animation_function = self._run_functions(
            function, self.strips[strip_id])
        animation_arguments = (
            strip_id, animation_function, arguments, this_id, delay_between, dont_split)
        animation_thread = threading.Thread(
            target=self._animate_run, args=animation_arguments)
        animation_thread.start()
        return self.response(function, False, None, False, strip_id)

    def _animate_run(self, strip_id, function, arguments, animation_id, delay_between, dont_split):
        while animation_id == self.strips[strip_id].animation_id.get():
            if dont_split:
                function(arguments)
            elif isinstance(arguments, dict):
                function(**arguments)
            elif delay_between == 0:
                function(*arguments)
            else:
                threading_thread = threading.Thread(
                    target=function, args=arguments)
                threading_thread.start()
                time.sleep(int(delay_between)/1000)

    def execute_json(self, data):
        for action in data:
            if action["type"] == "command":
                if action["function"] == "wait":
                    time.sleep(int(action["arguments"]["amount"]) / 1000)
                elif action["function"] == "stopanimation":
                    self.stop(action.get("strip_id"))
                elif action["function"] == "off":
                    self.off(action.get("strip_id"))
            elif action["type"] == "animate":
                self.animate(action["strip_id"], action["function"], action["arguments"], action.get("delay_between", 0))
            elif action["type"] == "run":
                self.run(action["strip_id"], action["function"], action["arguments"], True)
            elif action["type"] == "thread":
                self.thread(action["strip_id"], action["function"], action["arguments"], True)
        self.queue = []

print("controller.py loaded")
