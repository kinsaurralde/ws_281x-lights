import random

import config


class Colors:
    def __init__(self) -> None:
        self.colors = {}

    def addColor(self, color, r, g, b):
        self.colors[color.upper().strip()] = {"r": r, "g": g, "b": b, "value": rgbToInt(r, g, b)}

    def addColors(self, colors):
        for color in colors:
            if "value" not in colors[color]:
                continue
            value = colors[color]["value"]
            if len(value) != 3:
                continue
            r, g, b = value
            self.addColor(color, r, g, b)

    def getColor(self, color):
        try:
            return int(color)
        except ValueError:
            color = color.upper().strip()
            if color in self.colors:
                return self.colors[color]["value"]
            if color == "RANDOM":
                return self.getRandomColor()
            return -1

    def getRandomColor(self):
        if len(self.colors) == 0:
            return 0
        keys = list(self.colors.keys())
        value = 0
        while value == 0:
            value = self.colors[keys[random.randint(0, len(keys) - 1)]]
        return value

    def getColorList(self, colors):
        result = []
        for color in colors:
            result.append(self.getColor(color))
        print(self.colors)
        return result

    def validateColor(self, color) -> bool:
        if isinstance(color, int):
            return config.MIN_COLOR <= color <= config.MAX_COLOR
        return color == "none" or color == "random" or color in self.colors


def rgbToInt(r, g, b):
    return int((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)
