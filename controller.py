from lights import *
import threading
import time

class Controller:
    def __init__(self):
        # Settings
        self.brightness = 100
        neopixels.setBrightness(self.brightness)
        self.num_pixels = LED_COUNT
        self.break_animation = True

        self.strips = []
        self.strip_data = []
        self._create_strip(0, self.num_pixels - 1)
        self._create_strip(0, 29)
        self._create_strip(30, 59)
        self._create_strip(20, 39)

    def _create_strip(self, start, end):
        strip_id = len(self.strips)
        self.strips.append(Lights(strip_id))
        data = {
            "id": strip_id,
            "start": start,
            "end": end,
        }
        self.strip_data.append(data)
        neopixels.update(self.strip_data)

    def stop(self, strip_id=None):
        if strip_id == None:
            for strip in self.strips:
                strip.stop_animation()
        else:
            self.strips[strip_id].stop_animation()

    def off(self, strip_id=None):
        if strip_id == None:
            for strip in self.strips:
                strip.off()
        else:
            self.strips[strip_id].off()

    def get_brightness(self):
        return self.brightness

    def set_brightness(self, value):
        self.brightness = value
        neopixels.setBrightness(value)
        neopixels.show()

    def get_break_animation(self):
        return self.break_animation

    def set_break_animation(self, value):
        self.break_animation = value

    def get_all_settings(self):
        cur_settings = {
            "brightness": self.brightness,
            "break_animation": self.break_animation,
            "num_pixels": self.num_pixels,
        }
        return cur_settings

    def _run_functions(self, name, strip):
        run_functions = {
            "color": strip.set_all,
            "random": strip.random_cycle,
            "wipe": strip.wipe,
            "single": strip.set_pixel,
            "specific": strip.set_pixels,
            "pulse" : strip.pulse,
            "chase": strip.chase,
            "shift": strip.shift,
            "rainbowCycle": strip.rainbow_cycle,
            "rainbow": strip.rainbow,
            "rainbowChase": strip.rainbow_chase,
            "mix": strip.mix_switch,
            "reverse": strip.reverse,
        }
        if name in run_functions:
            return run_functions[name]

    def run(self, strip_id, function, arguments = None):
        print("[    Run    ] ", "[", strip_id, "] ", function, arguments)
        self.strips[strip_id].animation_id.increment()
        run_function = self._run_functions(function, self.strips[strip_id])
        if arguments == None:
            run_function()
        elif function == "specific" or function == "mix":
            run_function(arguments)
        else:
            run_function(*arguments)

    def thread(self, strip_id, function, arguments):
        print("[  Threads  ] ", "[", strip_id, "] ", function, arguments)
        threading_function = self._run_functions(
            function, self.strips[strip_id])
        threading_thread = threading.Thread(
            target=threading_function, args=arguments)
        threading_thread.start()

    def animate(self, strip_id, function, arguments, delay_between=0, dont_split=False):
        print("[ Animation ] ", "[", strip_id, "] ", function, arguments, "Delay Between:",delay_between)
        self.strips[strip_id].animation_id.increment()
        this_id = self.strips[strip_id].animation_id.get()
        if function == "mix":
            dont_split = True
        animation_function = self._run_functions(
            function, self.strips[strip_id])
        animation_arguments = (
            strip_id, animation_function, arguments, this_id, delay_between, dont_split)
        animation_thread = threading.Thread(
            target=self._animate_run, args=animation_arguments)
        animation_thread.start()

    def _animate_run(self, strip_id, function, arguments, animation_id, delay_between, dont_split):
        while animation_id == self.strips[strip_id].animation_id.get():
            if dont_split:
                function(arguments)
            elif delay_between == 0:
                function(*arguments)
            else:
                threading_thread = threading.Thread(
                    target=function, args=arguments)
                threading_thread.start()
                time.sleep(int(delay_between)/1000)

controller = Controller()

controller.run(0, "wipe", (255, 0, 0, 1, 1))
controller.run(0, "wipe", (0, 255, 0, 1, 1))
controller.run(0, "wipe", (0, 0, 255, 1, 1))
controller.run(0, "wipe", (0, 0, 0, 1, 1))

print("controller.py loaded")
