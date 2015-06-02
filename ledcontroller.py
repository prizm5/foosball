import time

from neopixel import *


class LedController(object):
    def __init__(self, logger):
        # LED strip configuration:
        self.logger = logger
        self.LED_COUNT      = 20      # Number of LED pixels.
        self.LED_OFFSET     = self.LED_COUNT / 2
        self.LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.player1color = Color(0, 0, 255)
        self.player2color = Color(0, 255, 0)
        self.LEDS = self.make_led_values()
        #self.make_led_values()
        self.idle = True

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(20, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,
                                       self.LED_BRIGHTNESS)
        # Initialize the library (must be called once before other functions).
        self.strip.begin()
        logger.info("%s Initialized", __name__)

    def flash_player_colors(self):
        p1 = 0
        p2 = 1
        for a in range(0, 2):
            if a % 2 == 0:
                p1 = 0
                p2 = 1
            else:
                p1 = 1
                p2 = 0

            for i in range(0, self.LED_OFFSET):
                self.LEDS[i] = p1
                self.LEDS[self.LED_OFFSET + i] = p2
            self._update_leds()
            time.sleep(.25)
        self.clear()

    def make_led_values(self):
        return {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0}

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
        self.logger.info("player: " + str(player) + " score: " + str(score))
        for i in range(0, score):
            if player % 2 == 0:
                self.LEDS[self.LED_COUNT - i] = 1
                #self.LEDS[self.LED_OFFSET + i] = 1
            else:
                self.LEDS[i] = 1

        self._update_leds()

    def _update_leds(self):
        self.logger.info("Updating LEDS: %s", self.LEDS)
        for i in range(0, self.LED_COUNT-1):
            color = Color(0, 0, 0)
            if self.LEDS[i] == 1:
                if i < self.LED_OFFSET:
                    color = self.player1color
                    self.logger.info("Setting %s pixel to player 1 color", i)
                else:
                    self.logger.info("Setting %s pixel to player 2 color", i)
                    color = self.player2color
            self.logger.info("Setting %s pixel to player 0 color", i)
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def clear(self):
        self.idle = False
        self.LEDS = self.make_led_values()
        self._update_leds()

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            if not self.idle:
                break
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)
    
    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            if not self.idle:
                break
            for q in range(3):
                if not self.idle:
                    break
                for i in range(0, self.strip.numPixels(), 3):
                    if not self.idle:
                        break
                    self.strip.setPixelColor(i+q, color)
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
    
    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            if not self.idle:
                break
            for i in range(self.strip.numPixels()):
                if not self.idle:
                    break
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)
    
    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            if not self.idle:
                break
            for i in range(self.strip.numPixels()):
                if not self.idle:
                    break
                self.strip.setPixelColor(i, self.wheel(((i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)
    
    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            if not self.idle:
                break
            for q in range(3):
                if not self.idle:
                    break
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    if not self.idle:
                        break
                    self.strip.setPixelColor(i+q, 0)

