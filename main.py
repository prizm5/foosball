#!/usr/bin/env python

import logging
import logging.handlers
import argparse
import sys
import time  # this is only being used as part of the example
from logger import *
import time

from ledcontroller import *

# Deafults
LOG_FILENAME = "myservice.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Replace stdout with logging to file at INFO level
#sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
#sys.stderr = MyLogger(logger, logging.ERROR)

led = LedController()


i = 0

# Loop forever, doing something useful hopefully:
while True:
        try:
                logger.info("The counter is now " + str(i))
                print "This is a print"
                i += 1

                led.SetPlayerScore(1,i)
                time.sleep(1)
                if i == 5:
                        led.Clear()
                        j = 1/0  # cause an exception to be thrown and the program to exit
        except KeyboardInterrupt:
                break
