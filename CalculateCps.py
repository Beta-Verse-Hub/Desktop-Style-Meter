from threading import Thread
from time import sleep
import keyboard


def init():

    """
    Initializes the char_hits and time_of_total_hits lists. These lists are used by the timer function to keep track of
    the number of key presses and the time between those key presses respectively. The timer function will reset the
    char_hits list every second and store the length of the list in the time_of_total_hits list at that time. If the
    length of the time_of_total_hits list exceeds 10, it will remove the first element of the list. The timer function is
    a separate thread and runs indefinitely until the program is stopped.
    """

    global char_hits
    global time_of_total_hits
    char_hits = []
    time_of_total_hits = []


def detectCharHit():

    """
    Continuously listens for keyboard input and appends the detected key to the char_hits list.

    The function captures every key press using the `keyboard` library and stores it in the
    global list `char_hits`, which is used to track the sequence of keys pressed over time.
    """

    while True:

        global char_hits
        char_hits.append(keyboard.read_key())


def timer():
    
    """
    Resets the char_hits list every second and stores the length of the list right before the reset in the time_of_total_hits list.
    If the length of the time_of_total_hits list is greater than 10, it removes the first element of the list.
    """
    
    while True:
    
        global char_hits

        if len(char_hits) > 5:
            time_of_total_hits.append(len(char_hits))
    
        if len(time_of_total_hits) > 10:
            time_of_total_hits.pop(0)
    
        char_hits = []
    
        sleep(1)

def runThreads():
    resetterThread = Thread(target=timer, daemon=True)
    resetterThread.start()

    detectCharHitThread = Thread(target=detectCharHit, daemon=True)
    detectCharHitThread.start()