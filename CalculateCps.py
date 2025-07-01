from threading import Thread
from time import sleep
import keyboard


def init():
    
    """
    Initializes the variables used by the module.

    Sets the global variables to their initial states. This function is called
    at the start of the program to reset the variables.
    """

    global char_hits, time_of_total_hits, last_key

    char_hits = []
    time_of_total_hits = []
    last_key = None


def detectCharHit():

    """
    Detects when a key is pressed and appends the key to the char_hits list.
    
    This function is a blocking call and waits until a key is pressed. When a key is pressed, it appends the key to the char_hits list and returns the key.
    
    Returns:
        str: The key that was pressed.
    """

    global char_hits
    
    key = keyboard.read_key()
    char_hits.append(key)

    return key


def timer():

    """
    Keeps track of the total hits of keys.

    This function runs in a separate thread and waits until the char_hits list
    has more than 5 elements. When this condition is met, it appends the length
    of the char_hits list to the time_of_total_hits list. If the
    time_of_total_hits list has more than 10 elements, it removes the oldest
    element. Then, it resets the char_hits list to an empty list and sleeps for
    1 second.
    """
    
    while True:
    
        global char_hits

        if len(char_hits) > 5:
            time_of_total_hits.append(len(char_hits))
    
        if len(time_of_total_hits) > 10:
            time_of_total_hits.pop(0)
    
        char_hits = []
    
        sleep(1)


def startKeyListener():

    """
    Starts an infinite loop that waits for a key to be pressed and appends the key to the char_hits list.

    This function is a blocking call and should be called in a separate thread to
    keep the main program responsive.

    Returns:
        None
    """

    while True:
        last_key = detectCharHit()


def mainChecker():

    """
    Initializes and starts threads for tracking key presses and managing key hit timing.

    This function creates and starts two daemon threads: one for periodically resetting
    the character hit count and another for continuously listening for key presses. The
    threads allow the program to track the number of key presses over time without blocking
    the main program execution.

    Returns:
        None
    """

    resetterThread = Thread(target=timer, daemon=True)
    resetterThread.start()

    startKeyListenerThread = Thread(target=startKeyListener, daemon=True)
    startKeyListenerThread.start()
