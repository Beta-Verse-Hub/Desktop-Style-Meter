from tkinter import *

# Create an instance of Tkinter Frame
window = Tk()

# Set the geometry
window.geometry("700x250")

# Adding transparent background property
window.wm_attributes('-transparentcolor', '#ab23ff')

# Create a Label with the same background color as the transparent color
Label(window, text="This is a New line Text", font=('Helvetica 18'), bg='#ab23ff').pack(ipadx=50, ipady=50, padx=20)

window.mainloop()