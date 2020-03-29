# "color": strip.set_all, #
# "random": strip.random_cycle,
# "wipe": strip.wipe, #
# "single": strip.set_pixel,
# "specific": strip.set_pixels,
# "pulse": strip.pulse,
# "chase": strip.chase, #
# "shift": strip.shift,
# "rainbowCycle": strip.rainbow_cycle,
# "rainbow": strip.rainbow_cycle,
# "rainbowChase": strip.rainbow_chase,
# "mix": strip.mix_switch, #
# "reverse": strip.reverse,
# "bounce": strip.bounce, #
# "pattern": strip.pattern,
# "blend": strip.blend,
# "fade": strip.fade,
# "fade_alt": strip.fade_alt,
# "twinkle": strip.twinkle,
# "pulse_pattern": strip.pulse_pattern

import random

class Animations:
    def __init__(self, led_count):
        self.led_count = led_count
        self.grb = False
        self.layers = {}

    def set_led_count(self, value):
        if value > 0:
            self.led_count = value

    def calc(self, actions):
        self._reset_layers()
        for action in actions:
            if action["type"] == "run":
                self.layers["animation"].extend(self._get_function(action["function"], action.get("arguments")))
                self.layers["framerate"] = action.get("framerate", 0)
            elif action["type"] == "base":
                self.layers["base"] = self._get_function(action["function"], action.get("arguments"))[0]
            elif action["type"] == "control":
                self.layers["control"] = self._get_function(action["function"], action.get("arguments"))[0] 
            elif action["type"] == "setting":
                self.layers["settings"] = self._get_settings(action["options"])
        return self.layers

    def _reset_layers(self):
        self.layers = {}
        self.layers["animation"] = []

    def _get_function(self, function, arguments):
        if function == "clear":
            return self._set_all(-1)
        elif function == "color":
            return self._set_all(**arguments)
        elif function == "random":
            return self._random(**arguments)
        elif function == "chase":
            return self._chase(**arguments)
        elif function == "mix_switch":
            return self._mix_switch(**arguments)
        elif function == "pulse":
            return self._pulse(**arguments)
        elif function == "bounce":
            return self._bounce(**arguments)
        elif function == "wipe":
            return self._wipe(**arguments)
        elif function == "reset":
            self.layers["base"] = self._set_all(0)[0]
            # self.layers["animation"].extend(self._set_all(-1))
            self.layers["animation"] = [[self._get_blank(),'']]
            return self._set_all(-1)
        else:
            return self._set_all(0)

    def _get_settings(self, options):
        settings = {}
        for option in options:
            settings[option] = options[option]
            if option == "on":
                self.layers["control"] = self._set_all(-1 if options[option] else 0)[0]
        return settings

    def _set_all(self, r, g=None, b=None):
        result = self._get_blank()
        for i in range(len(result)):
            if g is None or b is None:
                result[i] = r
            else:
                result[i] = self._get_color(r, g, b)
        return [result]

    def _random(self, interval=-1, frame_delay=5, iterations=40):
        """Flashes random lights
            
            Parameters:
                
                interval: number of pixels before new color is selected
        """
        frames = []
        current_color = self._get_random_color()
        if interval == -1:
            interval = self.led_count
        for i in range(iterations):
            frame = self._get_blank()
            for j in range(self.led_count):
                if j % interval == 0:
                    current_color = self._get_random_color()
                frame[j] = current_color
            frames.extend([[frame, []]] * frame_delay)
        return frames

    def _chase(self, r, g, b, interval=5, direction=1):
        frames = []
        iter_range = range(interval)
        if direction == -1:
            iter_range = reversed(iter_range)
        for q in iter_range:
            frame = self._set_all(-1)[0]
            for i in range(0, self.led_count, interval):
                if i + q >= self.led_count:
                    break
                frame[i + q] = self._get_color(r, g, b)
            frames.append(self._make_frame(frame))
        return frames

    def _mix_switch(self, colors, instant=False):
        """Cycle fading between multiple colors

            Parameters:

                colors: list of colors to split between

                instant: if true, dont calculate difference (default: False)
        """
        frames = []
        for k in range(0, len(colors) - 1):
            percent = 0
            for j in range(100):
                frame = self._get_blank()
                for i in range(0, self.led_count):
                    frame[i] = self._get_mix(colors[k], colors[k+1], percent)
                percent += 1
                frames.append(self._make_frame(frame))
        return frames

    def _pulse(self, r, g, b, direction=1, length=5):
        """Sends a pulse of color through strip

        Parameters:

            r, g, g: color of pulse

            direction: (default: 1)
                1: forward direction
                -1: reverse direction

            length: how many pixels in pulse (default: 5)
        """
        frames = []
        iter_range = range(self.led_count + length)
        if direction == -1:
            iter_range = reversed(iter_range)
        for i in iter_range:
            frame = self._set_all(-1)[0]
            j = i - length
            lower_index = max(j, 0)
            upper_index = min(i, self.led_count)
            frame[lower_index:upper_index] = [self._get_color(r, g, b)] * abs(lower_index - upper_index)
            frames.append(self._make_frame(frame))
        return frames

    def _bounce(self, colors, length=5, direction=1):
        """Bounce Pulse across strip

            Parameters:

                colors: list of colors to pulse

                length: how many pixels in pulse (default: 5)

                direction: initial direction (default: 1)
                    1: forwards
                    -1: backwards
        """
        frames = []
        for color in colors:
            frames.extend(self._pulse(color[0], color[1], color[2], direction, length))
            direction *= -1
        return frames

    def _wipe(self, r, g, b, direction=1):
        """New color wipes across strip
            
            Parameters:

                r, g, b: color

                direction: (default: 1)
                    1: forward direction
                    -1: reverse direction
        """
        frames = []
        start = 0
        iter_range = range(self.led_count)
        if direction == -1:
            start = self.led_count
            iter_range = reversed(iter_range)
        for i, j in enumerate(iter_range):
            frame = self._set_all(-1)[0]
            frame[start:j:direction] = [self._get_color(r, g, b)] * (i + 1)
            frames.append(self._make_frame(frame))
        frames[len(frames) - 1][1].append("animation_to_base")
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

    def _get_mix(self, color_1, color_2, percent):
        """Get the mixed color between 2 colors
        
            Parameters:
                
                color_1, color_2: two colors to mix

                percent: how far towards color 2 from color 1
        
        """
        r_diff = color_2[0] - color_1[0]
        g_diff = color_2[1] - color_1[1]
        b_diff = color_2[2] - color_1[2]
        r = color_1[0] + (r_diff * percent/100.0)
        g = color_1[1] + (g_diff * percent/100.0)
        b = color_1[2] + (b_diff * percent/100.0)
        return self._get_color(r, g, b)

    def _get_random_color(self):
        """Generates a random color"""
        r = 0
        g = 0
        b = 0
        color_off = random.randint(0, 2)
        if color_off != 0:
            r = random.randint(0, 127) * 2
        if color_off != 1:
            g = random.randint(0, 127) * 2
        if color_off != 2:
            b = random.randint(0, 127) * 2
        return self._get_color(r, g, b)

    def _make_frame(self, data):
        return [data, []]

    def _get_blank(self):
        return [-1] * self.led_count