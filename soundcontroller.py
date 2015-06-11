import os


class SoundController(object):
    def __init__(self, logger):
        self.logger = logger
        self.dir = os.path.dirname(os.path.realpath(__file__))
        logger.info("%s Initialized", __name__)

    def __play_file(self, file):
        f = os.path.join(self.dir, "wavs/{0}".format(file))
        os.system("aplay {0}".format(f))

    def play_scored(self):
        self.__play_file("EMDropFlourish.wav")

    def play_start(self):
        self.__play_file("CoinIn5.wav")

    def play_end(self):
        self.__play_file("piano.wav")

