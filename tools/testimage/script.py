import signal
from time import sleep
def terminator(signum, frame): exit()
signal.signal(signal.SIGTERM, terminator)
while 1: sleep(1)