import time
import logging

log = logging.getLogger(__name__)
log.setLevel("DEBUG")

class SequenceBase:
    def __init__(self) -> None:
        self.name = "UNSET"
        self.function_table = {}

    def setup(self, name, send_callback, functions):
        self.name = name
        self.send = send_callback
        self._createFunctions(functions)

    @staticmethod
    def createAnimationArgs():
        return {
            "controllers": [],
            "animation_args": {}
        }

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

    def color(self, color=0):
        args = self.createAnimationArgs()
        args["controllers"] = ["all"]
        args["animation_args"]["type"] = "color"
        args["animation_args"]["color"] = color
        self.send(args)

    def wipe(self, color=0, background=-1, reverse=False, frame_ms=40, steps=1):
        args = self.createAnimationArgs()
        args["controllers"] = ["all"]
        args["animation_args"]["type"] = "wipe"
        args["animation_args"]["color"] = color
        args["animation_args"]["backgtound_color"] = int(background)
        args["animation_args"]["reverse"] = bool(reverse)
        args["animation_args"]["frame_multiplier"] = int(steps)
        args["animation_args"]["frame_ms"] = int(frame_ms)
        self.send(args)

    def pulse(self, colors=["red", "blue", "green"], background=-1, length=5, spacing=5, reverse=False, frame_ms=40, steps=1):
        args = self.createAnimationArgs()
        args["controllers"] = ["all"]
        args["animation_args"]["type"] = "pulse"
        args["animation_args"]["colors"] = colors
        args["animation_args"]["background_color"] = int(background)
        args["animation_args"]["length"] = int(length)
        args["animation_args"]["spacing"] = int(spacing)
        args["animation_args"]["reverse"] = bool(reverse)
        args["animation_args"]["frame_multiplier"] = int(steps)
        args["animation_args"]["frame_ms"] = int(frame_ms)
        self.send(args)

    def rainbow(self, reverse=False, frame_ms=40, steps=1):
        args = self.createAnimationArgs()
        args["controllers"] = ["all"]
        args["animation_args"]["type"] = "rainbow"
        args["animation_args"]["reverse"] = bool(reverse)
        args["animation_args"]["frame_multiplier"] = int(steps)
        args["animation_args"]["frame_ms"] = int(frame_ms)
        self.send(args)

    def cycle(self, colors=["red", "blue", "green", "red"], steps_between_colors=100, frame_ms=40, steps=1):
        args = self.createAnimationArgs()
        args["controllers"] = ["all"]
        args["animation_args"]["type"] = "cycle"
        args["animation_args"]["colors"] = colors
        args["animation_args"]["steps"] = int(steps_between_colors)
        args["animation_args"]["frame_multiplier"] = int(steps)
        args["animation_args"]["frame_ms"] = int(frame_ms)
        self.send(args)

    def randomCycle(self, frame_ms=250, steps=1):
        args = self.createAnimationArgs()
        args["controllers"] = ["all"]
        args["animation_args"]["type"] = "randomcycle"
        args["animation_args"]["frame_multiplier"] = int(steps)
        args["animation_args"]["frame_ms"] = int(frame_ms)
        self.send(args)

    def reverser(self, reverse_animation=True, reverse_pixels=False):
        args = self.createAnimationArgs()
        args["controllers"] = ["all"]
        args["animation_args"]["type"] = "reverser"
        args["animation_args"]["reverse"] = bool(reverse_animation)
        args["animation_args"]["reverse2"] = bool(reverse_pixels)
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
