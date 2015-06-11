import os
from time import sleep

p = os.path.join(os.path.dirname(os.path.realpath(__file__)), "wavs/CoinIn5.wav")
print p
os.system("aplay {0} &".format(p))
