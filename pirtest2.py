# http://RasPi.itv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
import RPi.GPIO as GPIO

import time

from neopixel import *

# LED strip configuration:
LED_COUNT      = 10      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()


def setScore(player,score):
    if player%2==0:
        start = 5
    else:
        start = 0

    for i in range(0,score):
        strip.setPixelColor(start+i, Color(0, 0, 255))
	strip.show()

p2=0

def play2():
    global p2
    if p2<10:
        p2=p2+1
    setScore(2,p2)
    print(p2)

p=0

def play():
    global p
    if p < 10:
        p=p+1
    setScore(1,p1)
    print(p)

def reset():
    global p
    p=0
    global p2
    p2=0


def my_callback(channel):
    play()
    print('Player 1 score {}'.format(p))

def my_callback2(channel):
    play2()
    print('Player 2 score {}'.format(p2))
 

def my_callback3(channel):
    reset()
    print('Resetting scores')
 

def start():
    
    strip.setPixelColor(0, Color(0, 0, 255))
    GPIO.setmode(GPIO.BCM)
    
    # GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
    # Both ports are wired to connect to GND on button press.
    # So we'll be setting up falling edge detection for both
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # GPIO 24 set up as an input, pulled down, connected to 3V3 on button press
    #GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    #GPIO.add_event_detect(18, GPIO.FALLING, callback=my_callback, bouncetime=500)
    GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback2, bouncetime=500)
    #GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback3, bouncetime=10)

    try:
        global p
        p = 0
        input('Waiting...')
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit

start()


