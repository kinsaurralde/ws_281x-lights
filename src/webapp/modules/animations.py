import logging
from typing import Optional

import packet_pb2 as proto_packet
import animation_pb2 as proto_animation
from animation_pb2 import AnimationType

log = logging.getLogger(__name__)
log.setLevel("DEBUG")


class Animations:
    def __init__(self, colors, config, controllers) -> None:
        self.colors = colors
        self.controllers = controllers
        self.animations = self._processAnimationConfig(config["animations"])
        self.animation_args = config["animation_args"]

    def createAnimationPayload(self, animations):
        # pylint: disable=no-member
        packets = []
        for animation in animations:
            if "controllers" not in animation or "animation_args" not in animation:
                continue
            controllers = animation["controllers"]
            ips = self.controllers.getControllerIps(controllers)
            args = self._fillMissingArgs(animation["animation_args"])
            if args is None:
                continue
            log.info(f"Create Animation Args: {args}")
            payload = proto_packet.Payload()
            payload.animation_args.type = args.get("type", AnimationType.NONE)
            payload.animation_args.frame_ms = int(args.get("frame_ms", 40))
            payload.animation_args.color = self.colors.getColor(args.get("color", -1))
            payload.animation_args.background_color = self.colors.getColor(args.get("background_color", -1))
            payload.animation_args.length = int(args.get("length", 0))
            payload.animation_args.spacing = int(args.get("spacing", 0))
            payload.animation_args.steps = int(args.get("steps", 0))
            payload.animation_args.frame_multiplier = int(args.get("frame_multiplier", 1))
            payload.animation_args.reverse = args.get("reverse", 0)
            payload.animation_args.reverse2 = args.get("reverse2", 0)
            if "colors" in args:
                payload.animation_args.colors.CopyFrom(args["colors"])
            for ip in ips:
                packets.append((ip, payload))
        return packets

    def _fillMissingArgs(self, args) -> Optional[dict]:
        new_args = {}
        arg_type = args.get("type", "").upper()
        new_args["type"] = self._getAnimationType(arg_type)
        if arg_type is None or arg_type not in self.animations:
            return None
        for arg in self.animations[arg_type]:
            if arg == "web_options":
                continue
            value = args.get(arg)
            if not self._validateArg(arg, value):
                log.info(f"Arg {arg} is not valid: {value}")
                value = self.animations[arg_type][arg]
            if arg == "colors":
                colors = proto_animation.ListMax25()
                colors.items.extend(self.colors.getColorList(value))  # pylint: disable=no-member
                value = colors
            new_args[arg] = value
        return new_args

    def _validateArg(self, arg, value):
        if arg is None or arg not in self.animation_args:
            return False
        arg_type = self.animation_args[arg]["type"]
        if arg_type == "color":
            return self.colors.validateColor(value)
        if arg_type == "int":
            return validateInt(value, self.animation_args[arg]["min"], self.animation_args[arg]["max"])
        if arg_type == "bool":
            return validateBool(value)
        if arg_type == "list":
            return validateList(
                value,
                self.animation_args[arg]["max_size"],
                self.animation_args[arg]["min"],
                self.animation_args[arg]["max"],
            )
        if arg_type == "animation":
            return value.upper() in self.animations
        return False

    def _getAnimationType(self, name):
        name = name.upper()
        if name in self.animations:
            if name == "COLOR":
                return AnimationType.COLOR
            if name == "WIPE":
                return AnimationType.WIPE
            if name == "PULSE":
                return AnimationType.PULSE
            if name == "RAINBOW":
                return AnimationType.RAINBOW
            if name == "CYCLE":
                return AnimationType.CYCLE
            if name == "RANDOMCYCLE":
                return AnimationType.RANDOM_CYCLE
            if name == "REVERSER":
                return AnimationType.REVERSER
        return AnimationType.NONE

    @staticmethod
    def _processAnimationConfig(animations):
        result = {}
        for animation in animations:
            result[animation.upper().strip()] = animations[animation]
        return result


def validateInt(value, lower, upper):
    try:
        value = int(value)
    except TypeError:
        return False
    return lower <= value <= upper


def validateBool(value):
    try:
        value = bool(value)
        return True
    except TypeError:
        return False


def validateList(values, max_size, lower, upper):
    if len(values) > max_size:
        return False
    for value in values:
        if not validateInt(value, lower, upper):
            return False
    return True
