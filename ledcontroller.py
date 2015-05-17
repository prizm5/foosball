import time

from neopixel import *


class LedController(object):
    def __init__(self):
        # LED strip configuration:
        self.LED_COUNT      = 10      # Number of LED pixels.
        self.LED_OFFSET     = self.LED_COUNT / 2
        self.LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LEDS = self.make_led_values()
        self.player1color = Color(0, 0, 255)
        self.player2color = Color(0, 255, 0)

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,
                                       self.LED_BRIGHTNESS)
        # Initialize the library (must be called once before other functions).
        self.strip.begin()

    def make_led_values(self):
        l={}
        for i in range(0, 10):
            l[i]=0
        return

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
        if player %2 == 0:
            print "player: " + str(player) + " score: " + str(score)
            for i in (0, score-1):
                self.LEDS[self.LED_OFFSET + i] = 1
        else:
            print "player: " + str(player) + " score: " + str(score)
            for i in (0, score-1):
                self.LEDS[i] = 1

        self._update_leds()

    def _update_leds(self):
        for i in range(0,self.LED_COUNT):
            if self.LEDS[i] == 1:
                self.strip.setPixelColor(i, self.player2color)
            else:
                self.strip.setPixelColor(i, self.player1color)

        self.strip.show()

    def clear(self):
        for i in range(0,self.LED_COUNT):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
