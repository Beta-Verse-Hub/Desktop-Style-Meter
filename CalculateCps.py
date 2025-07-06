import collections
from threading import Lock
from time import time, sleep
import keyboard
from KeyDetectorWrapper import getKey


char_hits = []
time_of_total_hits = collections.deque()
cps_lock = Lock()


def onKeyPress(key: int, key_pressed: bool) -> None:
    """
    A callback function that is called whenever a key is pressed.

    Args:
        key (int): The key code of the key that was pressed.

    Returns:
        None

    This function appends the key code to the `char_hits` list and the current time to the `time_of_total_hits` deque.
    It also acquires the `cps_lock` while updating the `time_of_total_hits` deque to ensure thread safety.
    """
    
    if key_pressed and key == char_hits[-1]:
        return
    
    # Append the key to the list
    char_hits.append(key)
    
    # Acquire the lock
    with cps_lock:

        # Append the current time to the deque
        time_of_total_hits.append(time())


def getCurrentCps() -> int:
    """
    Returns the current CPS (characters per second) based on the last second of key presses.

    This function is thread-safe. It returns the number of key presses that occurred
    in the last second, or 0 if no key presses occurred in the last second.

    Returns:
        int: The current CPS.
    """
    # Acquire the lock
    with cps_lock:

        # Remove timestamps older than 1 second
        now: float = time()

        # Remove timestamps older than 1 second
        while time_of_total_hits and time_of_total_hits[0] < now - 1.0:
            time_of_total_hits.popleft()
        
        # Calculate the number of key presses in the last second
        return len(time_of_total_hits)


def startKeyListener() -> None:
    """
    Starts a thread that listens for key presses using the KeyDetectorDLL.

    This function does not return until the program is terminated. It
    continuously checks for key presses using the `getKey` function from
    the KeyDetectorDLL, and calls the `onKeyPress` callback function with
    the key code as the argument whenever a key press is detected.

    The callback function is called from the context of the thread started
    by this function. The callback function should be thread-safe and
    should not block for long periods of time, or else the key press
    detection will be delayed.

    This function should be called once at the start of the program, and
    should not be called again until the program is terminated.
    """
    key_pressed = False

    while True:

        key: int = getKey()

        key = keyboard.read_key()

        if key:
            onKeyPress(key, key_pressed)
            key_pressed = True
        else:
            key_pressed = False
