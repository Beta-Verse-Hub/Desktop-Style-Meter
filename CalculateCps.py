import collections
from threading import Lock
from time import time, sleep
import keyboard


char_hits = []
time_of_total_hits = collections.deque()
cps_lock = Lock()


def onKeyPress(event):
    """Callback function for keyboard presses."""

    char_hits.append(event.name)
    with cps_lock:
        time_of_total_hits.append(time())


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
        keyboard.on_press(onKeyPress)
        sleep(0.01)
