# "color": strip.set_all,
# "random": strip.random_cycle,
# "wipe": strip.wipe,
# "single": strip.set_pixel,
# "specific": strip.set_pixels,
# "pulse": strip.pulse,
# "chase": strip.chase,
# "shift": strip.shift,
# "rainbowCycle": strip.rainbow_cycle,
# "rainbow": strip.rainbow_cycle,
# "rainbowChase": strip.rainbow_chase,
# "mix": strip.mix_switch,
# "reverse": strip.reverse,
# "bounce": strip.bounce,
# "pattern": strip.pattern,
# "blend": strip.blend,
# "fade": strip.fade,
# "fade_alt": strip.fade_alt,
# "twinkle": strip.twinkle,
# "pulse_pattern": strip.pulse_pattern

class Animations:
    def __init__(self):
        self.led_count = 0
        self.grb = False

    def calc(self, actions, led_count):
        self.led_count = led_count
        result = []
        for action in actions:
            if action["type"] in ["run", "animate", "thread"]:
                result.extend(self._get_function(action["function"], action["arguments"]))
        return result
            
    def _get_function(self, function, arguments):
        if function == "color":
            return self._set_all(**arguments)
        elif function == "chase":
            return self._chase(**arguments)

    def _set_all(self, r, g=None, b=None):
        result = self._get_blank()
        for i in range(len(result)):
            if g is None or b is None:
                result[i] = r
            else:
                result[i] = self._get_color(r, g, b)
        return [result]

    def _chase(self, r, g, b, wait_ms=50, interval=5, direction=1, layer=False):
        frames = []
        iter_range = range(interval)
        if direction == -1:
            iter_range = reversed(iter_range)
        for q in iter_range:
            frame = [0] * self.led_count
            if layer:
                frame = self._set_all(-1)
            for i in range(0, self.led_count, interval):
                if i + q >= self.led_count:
                    break
                frame[i + q] = self._get_color(r, g, b)
            frames.append(frame)
        return frames

    def _get_color(self, r, g, b):
        """ Gets int value of rgb color 

            Parameters:

                r, g, b: color
        """
        if self.grb:
            return ((int(g) * 65536) + (int(r) * 256) + int(b))
        return ((int(r) * 65536) + (int(g) * 256) + int(b))

    def _get_color_seperate(self, value):
        """Seperates colors into rgb from single value
            Parameters:
                value: value of color to seperate
        """
        r = (value >> 16) & 0xFF
        g = (value >> 8) & 0xFF
        b = value & 0xFF
        if self.grb:
            return (g, r, b)
        return (r, g, b)

    def _get_random_color(self):
        """Generates a random color"""
        r = 0
        g = 0
        b = 0
        color_off = random.randint(0, 2)
        if color_off != 0:
            r = random.randint(0, 255)
        if color_off != 1:
            g = random.randint(0, 255)
        if color_off != 2:
            b = random.randint(0, 255)
        return self.get_color(r, g, b)

    def _get_blank(self):
        return [0] * self.led_count