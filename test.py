from datetime import datetime
from datetime import timedelta
import time


then = datetime.now()

for i in range(0, 10):
    now = datetime.now()
    delta = timedelta(seconds = 1)
    if then + delta < now:
        print "timeout"
    else:
        print "waiting"
    time.sleep(.5)