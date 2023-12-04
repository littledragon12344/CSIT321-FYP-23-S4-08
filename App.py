import tkinter as tk
import Camera as cam

def new_window(): 
    window = tk.Tk()
    window.title("Gesture Detection Prototype")
    #label = tk.Label(window, text="Created by group CSIT321-FYP-23-S4-08")
    #label.pack()
    window.geometry("800x600")
    
    frame = tk.Frame(window, width=500, height=375)
    frame.place(x=50, y=37.5)
    
    cam.Camera(frame)
    
    window.mainloop()
    

new_window()
