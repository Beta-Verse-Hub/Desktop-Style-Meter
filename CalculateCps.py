from threading import Thread
from time import sleep
import keyboard


def init():
    global char_hits
    global time_of_total_hits
    char_hits = []
    time_of_total_hits = []


def detectCharHit():

    while True:

        global char_hits
        char_hits.append(keyboard.read_key())


def timer():
    
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