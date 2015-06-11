#!/usr/bin/env python

import logging
import logging.handlers
import argparse
import sys
from GameController import *
from logger import *


def setupLogging(logfile="service.log"):
    # Deafults

    LOG_FILENAME = logfile
    LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    stderr_log_handler = logging.StreamHandler()
    logger.addHandler(stderr_log_handler)
    stderr_log_handler.setFormatter(formatter)

    logger.info("Logger Created")
    # Replace stdout with logging to file at INFO level
    sys.stdout = MyLogger(logger, logging.INFO)
    # Replace stderr with logging to file at ERROR level
    sys.stderr = MyLogger(logger, logging.ERROR)

    return logger

def main():

    # Define and parse command line arguments
    parser = argparse.ArgumentParser(description="My simple Python service")
    parser.add_argument("-l", "--log", help="file to write log to (default service.log)")

    # If the log file is specified on the command line then override the default
    args = parser.parse_args()

    LOG_FILENAME = 'service.log'
    if args.log:
        LOG_FILENAME = args.log

    logger = setupLogging(LOG_FILENAME)

    game = GameController(logger)

    # Loop forever, doing something useful hopefully:
    while True:
        try:
            game.checkState()
            time.sleep(.25)
        except KeyboardInterrupt:
            game.led.clear()
            break



if __name__ == "__main__":
    main()