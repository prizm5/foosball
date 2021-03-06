import RPi.GPIO as GPIO
import time

class SensorController(object):
    def __init__(self, logger):
        GPIO.setmode(GPIO.BCM)
        self.logger = logger
        logger.info("%s Initialized", __name__)

    def AddSensor(self, port, callback, bounce):
        p = int(port)
        b = int(bounce)
        self.logger.info("Sensor added: Port: %s | Callback: %s | Bounce: %s", p, callback, b)
        GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(p, GPIO.FALLING, callback=callback, bouncetime=b)

    def AddButton(self, port, callback, bounce):
        p = int(port)
        b = int(bounce)
        self.logger.info("Button added: Port: %s | Callback: %s | Bounce: %s", p, callback, b)
        GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(p, GPIO.FALLING, callback=callback, bouncetime=b)