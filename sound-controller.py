
import os


class SoundController(object):
    def __init__(self, logger, sounds):
        self.logger = logger

    def play_scored(self):
        os.system("mpg123 -q %s &", os.path.join(self.path, "EMDropFlourish.wav"))

    def play_start(self):
        os.system("mpg123 -q %s &", os.path.join(self.path, "CoinIn5.wav"))

    def play_end(self):
        os.system("mpg123 -q %s &", os.path.join(self.path, "piano.wav"))

test = SoundController(os.path.combine(os.path.dirname("."), "wavs"))

test.play_start()