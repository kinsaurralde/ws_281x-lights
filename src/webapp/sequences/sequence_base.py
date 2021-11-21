import time
import logging

log = logging.getLogger(__name__)
log.setLevel("DEBUG")

class SequenceBase:
    def __init__(self) -> None:
        self.name = "UNSET"
        self.function_table = {}

    def setup(self, name, functions):
        self.name = name
        self._createFunctions(functions)

    @staticmethod
    def createAnimationArgs():
        return {
            "id": "all",
            "animation": 0,
            "color": 0,
            "color_bg": 0,
            "colors": [],
            "wait_ms": 40,
            "inc_steps": 1,
            "steps": 1,
            "arg1": 0,
            "arg2": 0,
            "arg3": 0,
            "arg4": 0,
            "arg5": 0,
            "arg6": False,
            "arg7": False,
            "arg8": False,
        }

    @staticmethod
    def combineRGB(r, g, b):
        return (int(r) & 0xFF) << 16 | (int(g) & 0xFF) << 8 | (int(b) & 0xFF)

    def convertColor(self, color):
        value = [0, 0, 0]
        if isinstance(color, int):
            return color
        if color in self.colors:
            value = self.colors[color]
        return self.combineRGB(value[0], value[1], value[2])

    def convertColors(self, colors):
        result = []
        for color in colors:
            result.append(self.convertColor(color))
        return result

    def sleep(self, value):
        name = self.sequencer.thread_local.name
        if name not in self.sequencer.active:
            time.sleep(value)
            return
        end_time = time.time() + value
        while time.time() < end_time:
            time.sleep(0.01)
            if not self.sequencer.checkActive(name):
                raise Exception("Early Exit")

    def color(self, controller_id="all", color=0):
        args = self.createAnimationArgs()
        args["id"] = controller_id
        args["animation"] = 0
        args["color"] = self.convertColor(color)
        args["wait_ms"] = 1000
        self.send(args)

    def wipe(self, controller_id="all", color=0, background=-1, shift_amount=1, reverse=False, wait_ms=40, steps=1):
        args = self.createAnimationArgs()
        args["id"] = controller_id
        args["animation"] = 1
        args["color"] = self.convertColor(color)
        args["color_bg"] = int(background)
        args["arg1"] = int(shift_amount)
        args["arg6"] = bool(reverse)
        args["inc_steps"] = int(steps)
        args["wait_ms"] = int(wait_ms)
        self.send(args)

    def pulse(self, controller_id="all", colors=["red", "blue", "green"], background=-1, length=5, spacing=5, shift_amount=1, pattern_size=-1, reverse=False, wait_ms=40, steps=1):
        args = self.createAnimationArgs()
        args["id"] = controller_id
        args["animation"] = 2
        args["colors"] = self.convertColors(colors)
        args["color_bg"] = int(background)
        args["arg1"] = int(length)
        args["arg2"] = int(spacing)
        args["arg3"] = int(shift_amount)
        args["arg4"] = int(pattern_size)
        args["arg6"] = bool(reverse)
        args["inc_steps"] = int(steps)
        args["wait_ms"] = int(wait_ms)
        self.send(args)

    def rainbow(self, controller_id="all", shift_amount=1, reverse=False, wait_ms=40, steps=1):
        args = self.createAnimationArgs()
        args["id"] = controller_id
        args["animation"] = 3
        args["arg3"] = int(shift_amount)
        args["arg6"] = bool(reverse)
        args["inc_steps"] = int(steps)
        args["wait_ms"] = int(wait_ms)
        self.send(args)

    def cycle(self, controller_id="all", colors=["red", "blue", "green", "red"], steps_between_colors=100, wait_ms=40, steps=1):
        args = self.createAnimationArgs()
        args["id"] = controller_id
        args["animation"] = 4
        args["colors"] = self.convertColors(colors)
        args["arg1"] = int(steps_between_colors)
        args["inc_steps"] = int(steps)
        args["wait_ms"] = int(wait_ms)
        self.send(args)

    def randomCycle(self, controller_id="all", seed=0, wait_ms=250, steps=1):
        args = self.createAnimationArgs()
        args["id"] = controller_id
        args["animation"] = 5
        args["arg1"] = int(seed)
        args["inc_steps"] = int(steps)
        args["wait_ms"] = int(wait_ms)
        self.send(args)

    def reverser(self, controller_id="all", reverse_animation=True, reverse_pixels=False):
        args = self.createAnimationArgs()
        args["id"] = controller_id
        args["animation"] = 6
        args["arg6"] = bool(reverse_animation)
        args["arg7"] = bool(reverse_pixels)
        self.send(args)
    
    def run(self, function_name):
        if function_name in self.function_table:
            self.function_table[function_name]()

    def _createFunctions(self, functions):
        for function in functions:
            try:
                self.function_table[function] = getattr(self, function)
            except AttributeError:
                log.warning(f"Function {function} for sequence {self.name} does not exist!")
        log.info(f"Sequence {self.name} has functions {self.function_table.keys()}")

Preset = {
    'color_blue': {
        'color': 255
    },
    'wipe_green': {
        'color': 65280
    },
    'wipe_green_r': {
        'color': 65280,
        'reverse': True
    },
    'pulse_red': {
        'colors': ["red"]
    }
}
























































































































































