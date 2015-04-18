# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
import RPi.GPIO as GPIO

p2=0

def play2():
    global p2
    if p2<10:
        p2=p2+1
    print(p2)

p=0

def play():
    global p
    if p < 10:
        p=p+1
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
    GPIO.setmode(GPIO.BCM)
    
    # GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
    # Both ports are wired to connect to GND on button press.
    # So we'll be setting up falling edge detection for both
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # GPIO 24 set up as an input, pulled down, connected to 3V3 on button press
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(18, GPIO.FALLING, callback=my_callback, bouncetime=500)
    GPIO.add_event_detect(4, GPIO.FALLING, callback=my_callback2, bouncetime=500)
    GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback3, bouncetime=10)

    try:
        global p
        p = 0
        input('Waiting...')
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit

start()
