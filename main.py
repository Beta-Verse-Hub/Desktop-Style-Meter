# Imports
from tkinter import *
import threading
import keyboard
from pynput.mouse import Controller
from time import sleep
import CalculateCps


allStyles = []
mouse = Controller()
old_mouse_position = [-1,-1]


def addStyleText(text: str, styleText: Label) -> None:
    """
    Adds a style text message to the given styleText label.

    The message is prefixed with "+ " and appended to the list of all styles.
    If there are more than 10 messages, the oldest one is removed first.

    Args:
        text (str): The message to add.
        styleText (Label): The label to update with the new message.

    Returns:
        None
    """

    if styleText:
        # Check if the last added item is the same as the current text to avoid
        # excessive duplicates if you only want unique messages
        allStyles.append("+ " + text)
    
        if len(allStyles) > 7:
            allStyles.pop(0)
        
        styleText.configure(text="\n".join(allStyles))


def periodic_gui_update(window: Tk, styleText: Label) -> None:
    """
    A function that periodically updates the GUI, checking for input and mouse movement.

    Called every 100ms by `window.after()`, this function checks for several conditions:

    1. If the Escape key is pressed, it closes the window.
    2. If the user has 10 or more CPS in the last second, it adds a style text message
       showing their CPS.
    3. If the mouse has moved more than 500 pixels in either the x or y direction, it
       adds a style text message saying "John Cena's mouse".
    """

    global old_mouse_position, mouse

    # If the window has been destroyed, stop scheduling further updates
    if not window or not window.winfo_exists():
        return

    # 1. Input/Escape Key Check
    if keyboard.is_pressed("esc"):
    
        window.destroy()
        return

    # 2. Update Local CPS
    current_cps_hits = CalculateCps.getCurrentCps()
    if current_cps_hits > 10:
        addStyleText(str(current_cps_hits), styleText)

    # 3. Check Mouse Movement

    current_mouse_position = list(mouse.position)

    if current_mouse_position != old_mouse_position:

        if old_mouse_position != [-1,-1] and abs(current_mouse_position[0]-old_mouse_position[0]) > 500 or abs(current_mouse_position[1]-old_mouse_position[1]) > 500:
            print(old_mouse_position, current_mouse_position)
            addStyleText("John Cena's mouse", styleText)

        old_mouse_position = current_mouse_position
    
    window.after(100, periodic_gui_update, window, styleText)



def main():
    
    """
    The main function of the program.

    This function creates a window with a transparent background and a label that displays
    the current CPS and mouse movement. It also starts a thread that listens for key presses
    and updates the label accordingly. The window is set to be on top of all other windows
    and is positioned at the bottom right corner of the screen.

    Returns:
        None
    """
    
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
    window.attributes('-alpha', 0.5)

    # Create a Label with the same background color as the transparent color
    bg_image = PhotoImage(file="Background.png")

    styleTextCanvas = Canvas(window, width=bg_image.width(), height=bg_image.height(), highlightthickness=0)
    styleTextCanvas.pack(fill="both", expand=True)
    styleTextCanvas.create_image(0, 0, image=bg_image, anchor="nw")
    
    styleText = Label(styleTextCanvas, text=allStyles, font=('Helvetica 18'), foreground="#000000", wraplength=300, background = "#ffffff")
    styleText.grid(row=0, column=0, padx=20, pady=160)

    # Threads
    keyListenerThread = threading.Thread(target=CalculateCps.startKeyListener, daemon=True)
    keyListenerThread.start()

    window.after(100, periodic_gui_update, window, styleText)

    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    main()
