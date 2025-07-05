import collections
from threading import Lock
from time import time, sleep
import keyboard
from KeyDetectorWrapper import getKey


char_hits = []
time_of_total_hits = collections.deque()
cps_lock = Lock()


def onKeyPress(key):
    """Callback function for keyboard presses."""

    char_hits.append(key)
    with cps_lock:
        time_of_total_hits.append(time())
    print(getCurrentCps())


def getCurrentCps():
    """Calculates and returns the current CPS."""

    with cps_lock:
        # Remove timestamps older than 1 second
        now = time()
        while time_of_total_hits and time_of_total_hits[0] < now - 1.0:
            time_of_total_hits.popleft()
        return len(time_of_total_hits)


def startKeyListener():
    """Starts the keyboard listener in a non-blocking way."""

    while True:
        key = getKey()
        if key != -1:
            onKeyPress(key)
        sleep(0.01)
