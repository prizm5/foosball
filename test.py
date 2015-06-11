import os
from time import sleep


os.system("aplay %s &".format(os.path.join(os.path.dirname(os.path.realpath(__file__)), "wavs/CoinIn5.wav")))
