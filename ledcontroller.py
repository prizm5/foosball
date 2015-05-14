import time

from neopixel import *

class LedController(object):
    def __init__(self):
        self.LEDS = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
        #LED strip configuration:
        self.LED_COUNT      = 10      # Number of LED pixels.
        self.LED_OFFSET     = self.LED_COUNT / 2
        self.LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS)
        ## Intialize the library (must be called once before other functions).
        self.strip.begin()

    def SetPlayerScore(self,player,score):
        if player%2==0:
            print "player: " + str(player) + " score: " + str(score)
            for i in (0,score-1):
                self.LEDS[self.LED_OFFSET + i] = 1
        else:
            print "player: " + str(player) + " score: " + str(score)
            for i in (0,score-1):
                self.LEDS[i] = 1

        self._updateLeds()

    def _updateLeds(self):
        for i in range(0,9):
            if self.LEDS[i]==1:
                self.strip.setPixelColor(i, Color(0, 0, 255))
            else:
                self.strip.setPixelColor(i, Color(0, 0, 0))


        self.strip.show()

    def Clear(self):
        for i in range(0,self.LED_COUNT-1):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
