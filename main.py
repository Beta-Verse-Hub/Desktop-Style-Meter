from tkinter import *
import threading

# Create an instance of Tkinter Frame
window = Tk()

# Set the geometry
window.geometry("200x200+100+100")

# Make the window borderless
window.overrideredirect(True)

# Adding transparent background property
transparent_color = "#010101"
window.wm_attributes('-transparentcolor', transparent_color)

# Create a Label with the same background color as the transparent color
Label(window, text="Hello", font=('Helvetica 18'), bg=transparent_color).pack(ipadx=100, ipady=100, padx=0)

window.bind("<Escape>", lambda event: window.destroy())

window.mainloop()