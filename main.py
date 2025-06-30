# Imports
from tkinter import *
import threading
import keyboard
from pynput.mouse import Controller
from time import sleep
import pygetwindow as gw


AllStyles = []


def addStyleText(text, StyleText):

    """
    Adds a string to the AllStyles list and updates the text of the StyleText Label.
    
    Args:
        text (str): The string to be added to AllStyles.
        StyleText (Label): The Label to be updated.
    """

    if StyleText:
        AllStyles.append("+ "+text)
        
        if len(AllStyles) > 10:
            AllStyles.pop(0)
        
        StyleText.configure(text="\n".join(AllStyles))



def input(window, StyleText):
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


def check_mouse(window, StyleText):
    
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

    StyleTextCanvas = Canvas(window, width=bg_image.width(), height=bg_image.height(), highlightthickness=0)
    StyleTextCanvas.pack(fill="both", expand=True)
    StyleTextCanvas.create_image(0, 0, image=bg_image, anchor="nw")
    
    StyleText = Label(StyleTextCanvas, text=AllStyles, font=('Helvetica 18'), foreground="#000000", background = "#ffffff")
    StyleText.pack(ipadx=0, ipady=0, pady=30)

    # Threads
    input_thread = threading.Thread(target=input, args=(window, StyleText,), daemon=True)
    input_thread.start()
    check_mouse_thread = threading.Thread(target=check_mouse, args=(window, StyleText, ), daemon=True)
    check_mouse_thread.start()

    # Start the main loop
    window.mainloop()

if __name__ == "__main__":
    main()