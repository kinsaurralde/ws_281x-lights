import threading
import time

from lights import *
from variables import Variables


class Controller:
    def __init__(self, controller_id):
        self.neo = NeoPixels(controller_id)

        # Settings
        self.brightness = 100
        self.neo.setBrightness(self.brightness)
        self.num_pixels = self.neo.numMaxPixels()
        self.break_animation = True
        self.layer = False
        self.id = controller_id
        self.json_id = AnimationID()

        self.strips = []
        self.strip_data = []
        self.create_strip(0, self.num_pixels - 1)
        self.v = Variables()
        self.enable = True


    def init_neopixels(self, data):
        self.neo.init_neopixels(data["neopixels"])
        self.num_pixels = self.neo.numMaxPixels()
        if "settings" in data:
            if "initial_brightness" in data["settings"]:
                self.neo.setBrightness(data["settings"]["initial_brightness"])
        self.strips = []
        self.strip_data = []
        self.create_strip(0, self.num_pixels - 1)
        for strip in data["strips"]:
            self.create_strip(strip["start"], strip["end"])

    def create_strip(self, start, end):
        strip_id = len(self.strips)
        self.strips.append(Lights(self.neo, strip_id))
        data = {
            "id": strip_id,
            "start": start,
            "end": end,
        }
        self.strip_data.append(data)
        self.neo.update(self.strip_data)

    def info(self):
        data = self.response("info", False, None, True)
        data["power"] = self.neo.get_power_info()
        data["variables"] = self.v.info()
        return data

    def toggle_enable(self, value):
        if value is None:
            self.enable = not self.enable
        else:
            self.enable = value

    def is_enabled(self):
        return self.enable

    def is_connected(self):
        return True

    def ping(self):
        return time.time()

    def response(self, command_run, error, message, detailed=False, strip_id=None):
        data = {
            "controller_id": self.id,
            "command_run": command_run,
            "error": error,
            "message": message,
            "strip_info": self.strip_data,
            "error": False
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

    def increment_animation_id(self, strip_id):
        self.strips[strip_id].animation_id.increment()
        s = self.strip_data[strip_id]["start"]
        e = self.strip_data[strip_id]["end"]
        for i in self.strip_data:
            i_start = i["start"]
            i_end = i["end"]
            if i_start >= s or i_start <= e or i_end >= s or i_end <= e:
                self.strips[i["id"]].animation_id.increment()

    def get_brightness(self):
        self.brightness = self.neo.getBrightness()
        return self.brightness

    def set_brightness(self, value):
        self.brightness = value
        self.neo.setBrightness(value)
        self.neo.show()

    def set_layer(self, value):
        self.layer = bool(value)
        for strip in self.strips:
            strip.set_layer(self.layer)

    def get_break_animation(self):
        return self.break_animation

    def set_break_animation(self, value):
        self.break_animation = value

    def get_all_settings(self):
        self.brightness = self.neo.getBrightness()
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
            "rainbow": strip.rainbow_cycle,
            "rainbowChase": strip.rainbow_chase,
            "mix": strip.mix_switch,
            "reverse": strip.reverse,
            "bounce": strip.bounce,
            "pattern": strip.pattern,
            "blend": strip.blend,
            "fade": strip.fade,
            "fade_alt": strip.fade_alt,
            "twinkle": strip.twinkle,
            "pulse_pattern": strip.pulse_pattern
        }
        if name in run_functions:
            return run_functions[name]
        else:
            raise NameError

    def run(self, strip_id, function, arguments=None, start_time=time.time()):
        self.increment_animation_id(strip_id)
        run_function = self._run_functions(function, self.strips[strip_id])
        self.strips[strip_id].start_time = start_time
        if arguments == None:
            run_function()
        elif isinstance(arguments, dict):
            run_function(**arguments)
        elif function == "specific":
            run_function(arguments)
        else:
            run_function(*arguments)
        return self.response(function, False, None, False, strip_id)

    def thread(self, strip_id, function, arguments, start_time=time.time()):
        self.neo.update_pixel_owner(strip_id)
        threading_function = self._run_functions(
            function, self.strips[strip_id])
        self.strips[strip_id].start_time = start_time
        if arguments == None:
            threading_thread = threading.Thread(target=threading_function)
        elif isinstance(arguments, dict):
            threading_thread = threading.Thread(target=threading_function, kwargs=arguments)
        else:
            threading_thread = threading.Thread(target=threading_function, args=arguments)
        threading_thread.start()
        return self.response(function, False, None, False, strip_id)

    def animate(self, strip_id, function, arguments, delay_between=0, start_time=time.time()):
        self.increment_animation_id(strip_id)
        this_id = self.strips[strip_id].animation_id.get()
        self.neo.update_pixel_owner(strip_id)
        animation_function = self._run_functions(
            function, self.strips[strip_id])
        animation_arguments = (
            strip_id, animation_function, arguments, this_id, delay_between, start_time)
        animation_thread = threading.Thread(
            target=self._animate_run, args=animation_arguments)
        animation_thread.start()
        return self.response(function, False, None, False, strip_id)

    def _animate_run(self, strip_id, function, arguments, animation_id, delay_between, start_time):
        t = Timer(self.num_pixels, start_time)
        total_time = 0
        self.strips[strip_id].start_time = start_time
        delay = int(delay_between)
        while animation_id == self.strips[strip_id].animation_id.get():
            self.strips[strip_id].start_time = start_time + (total_time / 1000)
            if arguments is None:
                total_time += function()
            elif isinstance(arguments, dict):
                total_time += function(**arguments)
            elif delay_between == 0:
                total_time += function(*arguments)
            else:
                threading_thread = threading.Thread(
                    target=function, args=arguments)
                threading_thread.start()
                t.sleep(delay/1000)
                total_time += delay

    def _loop(self, t, animation_id, action):
        amount = action["arguments"]["amount"]
        if amount == "forever":
            amount = -1
        amount = int(amount)
        while amount != 0 and self.json_id.get() == animation_id:
            amount -= 1
            for sub_action in action["loop"]:
                if self.json_id.get() != animation_id:
                    break
                self._execute(t, animation_id, sub_action)

    def _execute(self, t, animation_id, action):
        action = self.v.p_values(action)
        if action["type"] == "command":
            if action["function"] == "wait":
                t.sleep(int(action["arguments"]["amount"]))
            elif action["function"] == "starttime":
                t.set_start(action["arguments"]["amount"])
            elif action["function"] == "stopanimation":
                self.stop(action.get("strip_id", 0))
            elif action["function"] == "off":
                self.off(action.get("strip_id", 0))
        elif action["type"] == "control":
            if action["function"] == "wait":
                t.sleep(int(action["arguments"]["amount"]))
            elif action["function"] == "loop":
                self._loop(t, animation_id, action)
            elif action["function"] == "execute":
                for a in action["value"]:
                    self._execute(t, animation_id, a)
        elif action["type"] == "debug":
            if action["function"] == "time":
                print("Current time:", time.time())
            elif action["function"] == "print":
                print("Message:", action["message"])
        elif action["type"] == "variable":
            if action["function"] == "set_value":
                self.v.add(action["name"], action["value"], action.get("v_type"))
            elif action["function"] == "set_function":
                self.v.add(action["name"], [action["arguments"], action["value"]], "function")
            elif action["function"] == "list_all":
                self.v.list_all()
        elif action["type"] == "setting":
            if action["function"] == "brightness":
                self.set_brightness(action.get("arguments"))
        elif action["type"] == "animate":
            self.animate(action.get("strip_id", 0), action["function"], action["arguments"], action.get("delay_between", 0), t.get_time())
        elif action["type"] == "run":
            self.run(action.get("strip_id", 0), action["function"], action["arguments"], t.get_time())
        elif action["type"] == "thread":
            self.thread(action.get("strip_id", 0), action["function"], action["arguments"], t.get_time())

    def _execute_json(self, data):
        self.json_id.increment()
        animation_id = self.json_id.get()
        t = Timer(self.num_pixels, time.time())
        for action in data:
            self._execute(t, animation_id, action)
            if self.json_id.get() != animation_id:
                break

    def execute_json(self, data):
        execute = self._execute_json
        thread = threading.Thread(target=execute, args=[data])
        thread.start()


print("controller.py loaded")
