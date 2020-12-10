import time

class SequenceBase:
    def __init__(self, sequencer, send, config) -> None:
        self.sequencer = sequencer
        self.colors = self.sequencer.colors
        self.send = send
        self.name = config["name"]
        self.functions_config = config["functions"]
        self.function_table = {}

        self._createFunctionTable()

    def _createFunctionTable(self):
        for function in self.functions_config:
            try:
                self.function_table[function] = getattr(self, function)
            except AttributeError:
                print(f"Function {function} for sequence {self.name} does not exist!")

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

    def hasFunction(self, name):
        return name in self.function_table

    def run(self, function_name):
        if function_name in self.function_table:
            self.function_table[function_name]()

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