import time

from neopixel import *


class LedController(object):
    def __init__(self, logger):
        # LED strip configuration:
        self.LED_COUNT      = 20      # Number of LED pixels.
        self.LED_OFFSET     = self.LED_COUNT / 2
        self.LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LEDS = self.make_led_values()
        self.idle = True
        self.player1color = Color(0, 0, 255)
        self.player2color = Color(0, 255, 0)
        self.logger = logger

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,
                                       self.LED_BRIGHTNESS)
        # Initialize the library (must be called once before other functions).
        self.strip.begin()
        logger.info("%s Initialized", __name__)

    def flash_player_colors(self):
        p1 = 0
        p2 = 1
        for a in range(0, 3):
            if a % 2 == 0:
                p1 = 0
                p2 = 1
            else:
                p1 = 1
                p2 = 0

            for i in (0, self.LED_OFFSET-1):
                self.LEDS[i] = p1
            for i in (self.LED_OFFSET, self.LED_COUNT-1):
                self.LEDS[i] = p2
            self._update_leds()
            time.sleep(.25)
        self.clear()

    def make_led_values(self):
        l={}
        for i in range(0, self.LED_COUNT-1):
            l[i] = 0
        return l

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

    def set_player_colors(self, color1, color2):
        c1 = self.hex_to_rgb(color1)
        self.player1color = Color(c1)

        c2 = self.hex_to_rgb(color2)
        self.player1color = Color(c2)

    def set_player_score(self, player, score):
        if player % 2 == 0:
            self.logger.info("player: " + str(player) + " score: " + str(score))
            for i in (0, score-1):
                self.LEDS[self.LED_OFFSET + i] = 1
        else:
            self.logger.info("player: " + str(player) + " score: " + str(score))
            for i in (0, score-1):
                self.LEDS[i] = 1

        self._update_leds()

    def _update_leds(self):
        for i in range(0, self.LED_COUNT-1):
            color = Color(0, 0, 0)
            if self.LEDS[i] == 1:
                if i <= self.LED_OFFSET:
                    color = self.player1color
                else:
                    color = self.player2color
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def clear(self):
        self.idle = False
        for i in range(0, self.LED_COUNT):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        self.idle = True
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            if self.idle == False:
                break
            for i in range(self.strip.numPixels() - self.LED_OFFSET):
                self.strip.setPixelColor(i, self.wheel(((i * 256 / self.LED_OFFSET) + j) & 255))
            for i in range(self.LED_OFFSET+1, self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(((i * 256 / self.LED_OFFSET) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)