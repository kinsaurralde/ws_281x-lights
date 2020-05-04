from rpi_ws281x import Adafruit_NeoPixel
import time

# Initial LED strip configuration:
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)

class NeoPixels:
    """Control access to Adafruit_Neopixel()"""
    def __init__(self, led_count=60, max_brightness=255, pin=18, max_watts=1, watts_per_60=18, grb=False, testing=True, flipped=True):
        # Configuration Settings
        self.led_count = led_count
        self.max_brightness = max_brightness
        self.pin = pin
        self.grb = grb
        self.max_watts = max_watts
        self.watts_per_60 = watts_per_60
        self.watts_per_led = (self.watts_per_60 / 60)
        self.power_usage = 0
        self.testing = testing
        self.flipped = flipped
        self.led_channel = self.pin in [13, 19, 41, 45, 53]
        self.gamma = [None] * 256
        # Current Pixels
        self.led_data = [0] * led_count
        self.brightness = self.max_brightness
        # Other
        self.last_show = time.time()
        # Actual Strip
        self.strip = Adafruit_NeoPixel(
            self.led_count, self.pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, self.max_brightness, self.led_channel)
        if not self.testing:
            self.strip.begin()
        self.active = True

    def info(self) -> dict:
        """Get information about these neopixels
        
            Parameters: None

            Return: neopixel information
        """
        return {
            "num_pixels": self.led_count,
            "max_brightness": self.max_brightness,
            "brightness": self.brightness,
            "max_watts": self.max_watts,
            "flipped": self.flipped
        }

    def set_gamma(self, data: list):
        """Set gamma array used for gamma correction

            Parameters: 

                data (lenth 256): values to remap brightness to

            Return: None
        """
        if not isinstance(data, list) or len(data) != 256:
            print("Invalid Gamma")
        else:
            self.gamma = data

    def num_pixels(self) -> int:
        """Get number of pixels

            Parameters: None

            Return: number of pixels
        """
        return self.led_count

    def set_brightness(self, value: int) -> int:
        """Set strip brightness
        
            Parameters:

                value: new brightness value

            Return: brightness
        """
        if value >= 0 and value <= self.max_brightness:
            self.brightness = value
            if not self.testing:
                b = self.brightness
                if self.gamma[value] is not None:
                    b = self.gamma[value]
                self.strip.setBrightness(b)
        return self.brightness

    def get_brightness(self) -> int:
        """Get current brightness
        
            Parameters: None

            Return: brightness
        """
        return self.brightness

    def get_pixels(self) -> list:
        """Get pixel data
        
            Parameters: None

            Return: list of pixel data
        """
        return self.led_data

    def check_power_usage(self) -> float:
        """Recalculate power usage
        
            Parameters: None

            Return: power usage
        """
        total_color = 0
        for i in range(self.led_count):
            pixel_color = self._get_color_seperate(self.led_data[i])
            total_color += pixel_color[0] + pixel_color[1] + pixel_color[2]
        total_color = (total_color / 765) * self.watts_per_led
        return total_color * (self.brightness / 255)

    def get_power_usage(self, refresh: bool = True) -> float:
        """Return current power usage
        
            Parameters:

                refresh: If true, update value before returning

            Return: power usage
        """
        if refresh:
            self.power_usage = self.check_power_usage()
        return self.power_usage

    def update_pixels(self, data: list):
        """Update led_data with given pixel data
        
            Parameters:

                data (length led_count): list with pixel data to update with

            Return: None
        """
        if len(data) < self.led_count:
            return -1
        if len(data) > self.led_count:
            data = data[0:self.led_count]
        if self.flipped:
            data = list(reversed(data))
        self.get_pixels()
        for i in range(0, self.led_count):
            if data[i] != -1:
                self.led_data[i] = data[i]

    def show(self, limit: int = 0):
        """ Update pixels with data in led_data if sufficient time has passed
            since last update
        
            Parameters:

                limit: how many ms to wait between shows 

            Return: None
        """
        if time.time() >= self.last_show + (limit / 1000) or limit == 0:
            self.get_power_usage(True)
            if not self.testing:
                for i in range(self.led_count):
                    self.strip.setPixelColor(i, self.led_data[i])
                self.strip.show()
            self.last_show = time.time()

    def _get_color_seperate(self, value: int) -> (int, int, int):
        """Seperates colors into rgb from single value

            Parameters:

                value: value of color to seperate

            Return: (r, g, b)
        """
        r = (value >> 16) & 0xFF
        g = (value >> 8) & 0xFF
        b = value & 0xFF
        if self.grb:
            return (g, r, b)
        return (r, g, b)

    def _get_color(self, r: int, g: int, b: int) -> int:
        """ Gets int value of rgb color

            Parameters:

                r, g, b: color

            Return: color
        """
        if self.grb:
            return ((int(g) * 65536) + (int(r) * 256) + int(b))
        return ((int(r) * 65536) + (int(g) * 256) + int(b))
