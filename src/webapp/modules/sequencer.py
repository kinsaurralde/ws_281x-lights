class Sequencer:
    def __init__(self, controller):
        self.controller = controller

    @staticmethod
    def create_animation_args():
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
    def create_controller_args(steps=1, wait_ms=40, strip_id=0):
        return {"inc_steps": int(steps), "wait_ms": int(wait_ms), "id": strip_id}

    def color(self, color=0, controller_args=None):
        if controller_args is None:
            controller_args = self.create_controller_args()
        args = self.create_animation_args()
        args["animation"] = 0
        args["color"] = int(color)
        args.update(controller_args)
        self.controller.send([args])

    def wipe(self, color=0, background=-1, reverse=False, controller_args=None):
        if controller_args is None:
            controller_args = self.create_controller_args()
        args = self.create_animation_args()
        args["animation"] = 1
        args["color"] = int(color)
        args["color_bg"] = int(background)
        args["arg1"] = int(controller_args["inc_steps"])
        args["arg6"] = bool(reverse)
        args.update(controller_args)
        self.controller.send([args])
