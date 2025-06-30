# Imports
from tkinter import *
import threading
import keyboard
from pynput.mouse import Controller
from time import sleep
import pygetwindow as gw


AllStyles = []


def addStyleText(text):
    AllStyles.append("+ "+text)
    if len(AllStyles) > 10:
        AllStyles.pop(0)


def input(window):
    """
    Monitors the existence of the window and waits for input to be pressed.
    If the "esc" key is pressed and the window is still open, it destroys the window.
    
    Args:
        window: A Tkinter window instance to monitor and potentially destroy.
    """

    while window.winfo_exists():
        if keyboard.is_pressed("esc"):
            window.destroy()


def check_mouse(window):
    
    """
    Monitors the mouse position and checks if the user has moved it over a certain distance.
    If the user has moved the mouse over the specified distance, then it prints "+ John Cena's mouse" to the console.
    
    Args:
        window: A Tkinter window instance to monitor and potentially destroy.
    """

    mouse = Controller()
    breaks_for_check = {
        "distance" : [1,1]
    }
    old_mouse_position = [-1,-1]
    open_windows = gw.getAllTitles()

    while window.winfo_exists():
    
        if breaks_for_check["distance"][0] == breaks_for_check["distance"][1]:

            if mouse.position != old_mouse_position:
    
                if old_mouse_position != [-1,-1] and (abs(mouse.position[0]-old_mouse_position[0]) > 150 or abs(mouse.position[1]-old_mouse_position[1]) > 150):
                    addStyleText("John Cena's mouse")

                old_mouse_position = mouse.position

        if len(gw.getAllTitles()) != len(open_windows):        
            addStyleText("RECONSTRUCT WHAT!?!")
            open_windows = gw.getAllTitles()

        for i in breaks_for_check:
            if breaks_for_check[i][0] == 0:
                breaks_for_check[i][0] = breaks_for_check[i][1]
                continue
            breaks_for_check[i][0] -= 1
        
        newest_window = gw.getAllTitles()
        print(newest_window)
    
        sleep(0.01)


# Create an instance of Tkinter Frame
window = Tk()


# Get the screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()


# Threads
input_thread = threading.Thread(target=input, args=(window,), daemon=True)
input_thread.start()
check_mouse_thread = threading.Thread(target=check_mouse, args=(window,), daemon=True)
check_mouse_thread.start()

# Set the geometry
window.geometry(f"200x300+{screen_width-300}+{screen_height//2-150}")


# Make the window borderless
window.overrideredirect(True)


# Set the window on top
window.attributes('-topmost', True)


# Adding transparent background property
transparent_color = "#010101"
window.wm_attributes('-transparentcolor', transparent_color)


# Create a Label with the same background color as the transparent color
Label(window, text=AllStyles, font=('Helvetica 18'), bg="#ffffff").pack(ipadx=100, ipady=150)


# Start the main loop
window.mainloop()