# Imports
from tkinter import *
import threading
import keyboard
from pynput.mouse import Controller
from time import sleep
import pygetwindow as gw
import CalculateCps


allStyles = []


def LocalCps(styleText):
    
    """
    Updates the styleText Label with the current count of character hits.

    This function retrieves the length of the char_hits list from the CalculateCps module and 
    passes it to the addStyleText function to update the styleText Label. It also initiates 
    the threads in the CalculateCps module.

    Args:
        styleText (Label): The Label to be updated with the count of character hits.
    """

    while True:
        addStyleText(str(len(CalculateCps.char_hits)), styleText)


def addStyleText(text : str, styleText : Label):

    """
    Adds a string to the AllStyles list and updates the text of the StyleText Label.
    
    Args:
        text (str): The string to be added to AllStyles.
        StyleText (Label): The Label to be updated.
    """

    if styleText:
        allStyles.append("+ "+text)
        
        if len(allStyles) > 10:
            allStyles.pop(0)
        
        styleText.configure(text="\n".join(allStyles))



def Input(window, styleText):
    
    """
    Monitors the existence of the window and waits for input to be pressed.
    If the "esc" key is pressed and the window is still open, it destroys the window.
    
    Args:
        window: A Tkinter window instance to monitor and potentially destroy.
    """

    while window.winfo_exists():
        if keyboard.is_pressed("esc"):
            window.destroy()
        
        sleep(0.01)


def CheckMouse(window, StyleText):
    
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

    while window.winfo_exists():
    
        if breaks_for_check["distance"][0] == breaks_for_check["distance"][1]:

            if mouse.position != old_mouse_position:
    
                if old_mouse_position != [-1,-1] and (abs(mouse.position[0]-old_mouse_position[0]) > 150 or abs(mouse.position[1]-old_mouse_position[1]) > 150):
                    addStyleText("John Cena's mouse", StyleText)

                old_mouse_position = mouse.position

                # addStyleText("RECONSTRUCT WHAT!?!", StyleText)

        for i in breaks_for_check:
            if breaks_for_check[i][0] == 0:
                breaks_for_check[i][0] = breaks_for_check[i][1]
                continue
            breaks_for_check[i][0] -= 1
        
        sleep(0.01)


def addStyleText(text : str, styleText : Label):
    """
    Adds a string to the AllStyles list and updates the text of the StyleText Label.
    This function MUST be called from the main Tkinter thread.
    
    Args:
        text (str): The string to be added to AllStyles.
        StyleText (Label): The Label to be updated.
    """
    if styleText:
        # Check if the last added item is the same as the current text to avoid
        # excessive duplicates if you only want unique messages
        if not allStyles or allStyles[-1] != "+ " + text:
            allStyles.append("+ "+text)
        
            if len(allStyles) > 10:
                allStyles.pop(0)
            
            styleText.configure(text="\n".join(allStyles))


def periodic_gui_update(window, styleText):

    """
    Periodically checks for key presses and mouse movement to update the styleText label accordingly.

    This function is called every 100ms to update the styleText label with the current count of character hits and to check for mouse movement.
    If the user has moved the mouse over the specified distance, it adds "+ John Cena's mouse" to the styleText label.
    If the user has pressed the "esc" key, it destroys the window and stops scheduling further updates.

    This function MUST be called from the main Tkinter thread.

    Returns:
        None
    """


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
    current_cps_hits = len(CalculateCps.char_hits)
    addStyleText(str(current_cps_hits), styleText)

    # 3. Check Mouse Movement

    current_mouse_position = mouse.position

    if current_mouse_position != old_mouse_position:

        if old_mouse_position != [-1,-1] and (abs(current_mouse_position[0]-old_mouse_position[0]) > 150 or abs(current_mouse_position[1]-old_mouse_position[1]) > 150):

            addStyleText("John Cena's mouse", styleText)

        old_mouse_position = current_mouse_position



def main():

    # Initialize the CalculateCps module's variables
    CalculateCps.init()
    
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
    CalculateCps.mainChecker()
    window.after(100, periodic_gui_update, window, styleText)

    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    main()
