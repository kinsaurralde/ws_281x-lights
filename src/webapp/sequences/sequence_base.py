import time

class SequenceBase:
    def __init__(self, sequencer, send, config) -> None:
        self.sequencer = sequencer
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
        print(self.function_table)

    @staticmethod
    def createAnimationArgs():
        return {
            "animation": 0,
            "color": 0,
            "color_bg": 0,
            "colors": [],
            "wait_ms": 40,
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
    def createControllerArgs(steps=1, wait_ms=40, strip_id=0):
        return {"inc_steps": int(steps), "wait_ms": int(wait_ms), "id": strip_id}

    def sleep(self, value):
        name = self.sequencer.thread_local.name
        if name not in self.sequencer.active:
            time.sleep(value)
            return
        end_time = time.time() + value
        while time.time() < end_time:
            time.sleep(0.01)
            if not self.sequencer.checkActive(name):
                break

    def color(self, color=0, controller_args=None):
        if controller_args is None:
            controller_args = self.createControllerArgs()
        args = self.createAnimationArgs()
        args["animation"] = 0
        args["color"] = int(color)
        args.update(controller_args)
        self.send(args)

    def wipe(self, color=0, background=-1, reverse=False, controller_args=None):
        if controller_args is None:
            controller_args = self.createControllerArgs()
        args = self.createAnimationArgs()
        args["animation"] = 1
        args["color"] = int(color)
        args["color_bg"] = int(background)
        args["arg1"] = int(controller_args["inc_steps"])
        args["arg6"] = bool(reverse)
        args.update(controller_args)
        self.send(args)

    def pulse(self, colors=[], background=-1, length=5, spacing=5, shift_amount=1, pattern_size=-1, reverse=False, controller_args=None):
        if controller_args is None:
            controller_args = self.createControllerArgs()
        args = self.createAnimationArgs()
        args["animation"] = 2
        args["colors"] = colors
        args["color_bg"] = int(background)
        args["arg1"] = int(length)
        args["arg2"] = int(spacing)
        args["arg3"] = int(shift_amount)
        args["arg4"] = int(pattern_size)
        args["arg6"] = bool(reverse)
        args.update(controller_args)
        self.send(args)

    def hasFunction(self, name):
        return name in self.function_table

    def run(self, function_name):
        if function_name in self.function_table:
            self.function_table[function_name]()
    