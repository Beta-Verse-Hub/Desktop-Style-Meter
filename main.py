# Imports
from tkinter import *
import threading
import keyboard
from pynput.mouse import Controller
from time import sleep
import pygetwindow as gw
import CalculateCps


allStyles = []


def addStyleText(text : str, styleText : Label):

    """
    Adds a style text message to the given styleText label.

    The message is prefixed with "+ " and appended to the list of all styles.
    If there are more than 10 messages, the oldest one is removed first.

    Args:
        text (str): The message to add.
        styleText (Label): The label to update with the new message.
    """

    if styleText:
        # Check if the last added item is the same as the current text to avoid
        # excessive duplicates if you only want unique messages
        allStyles.append("+ "+text)
    
        if len(allStyles) > 10:
            allStyles.pop(0)
        
        styleText.configure(text="\n".join(allStyles))


def periodic_gui_update(window, styleText):

    """
    Periodically updates the GUI with the current CPS and checks for mouse movement and escape key presses.

    Args:
        window (Tk): The Tkinter window to update.
        styleText (Label): The Label to update with the current CPS.

    This function schedules itself to be called every 100ms and runs indefinitely until the window is destroyed.
    It checks for the following events:

    1. Escape key presses: Destroys the window if pressed.
    2. Mouse movement: If the mouse has moved more than 150 pixels in either the x or y direction, it adds a style text message
        to the styleText label with the message "John Cena's mouse".

    """
    
    while window.winfo_exists():

        mouse = Controller()
        
        old_mouse_position = [-1,-1]

        # If the window has been destroyed, stop scheduling further updates
        if not window or not window.winfo_exists():
            return

        # 1. Input/Escape Key Check
        if keyboard.is_pressed("esc"):
        
            window.destroy()
            return

        # 2. Update Local CPS
        current_cps_hits = CalculateCps.getCurrentCps()
        addStyleText(str(current_cps_hits), styleText)

        # 3. Check Mouse Movement

        current_mouse_position = mouse.position

        if current_mouse_position != old_mouse_position:

            if old_mouse_position != [-1,-1] and (abs(current_mouse_position[0]-old_mouse_position[0]) > 150 or abs(current_mouse_position[1]-old_mouse_position[1]) > 150):

                addStyleText("John Cena's mouse", styleText)

            old_mouse_position = current_mouse_position



def main():
    
    # Create an instance of Tkinter Frame
    window = Tk()

    # Get the screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Set the geometry
    window.geometry(f"288x432+{screen_width-350}+{screen_height//2-216}")

    # Make the window borderless
    window.overrideredirect(True)

    # Set the window on top
    window.attributes('-topmost', True)

    # Adding transparent background property
    transparent_color = "#010101"
    window.wm_attributes('-transparentcolor', transparent_color)

    # Create a Label with the same background color as the transparent color
    bg_image = PhotoImage(file="Background.png")

    styleTextCanvas = Canvas(window, width=bg_image.width(), height=bg_image.height(), highlightthickness=0)
    styleTextCanvas.pack(fill="both", expand=True)
    styleTextCanvas.create_image(0, 0, image=bg_image, anchor="nw")
    
    styleText = Label(styleTextCanvas, text=allStyles, font=('Helvetica 18'), foreground="#000000", background = "#ffffff")
    styleText.pack(ipadx=0, ipady=0, pady=60)

    # Threads
    keyListenerThread = threading.Thread(target=CalculateCps.startKeyListener, daemon=True)
    keyListenerThread.start()

    window.after(100, periodic_gui_update, window, styleText)

    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    main()
