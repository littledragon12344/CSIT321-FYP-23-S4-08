import tkinter as tk
import Camera as cam
import Config as cfg

def new_window(): 
    window = tk.Tk()
    window.title("Gesture Detection Prototype")
    #label = tk.Label(window, text="Created by group CSIT321-FYP-23-S4-08")
    #label.pack()
    window.geometry("800x800")
    
    base = tk.Frame(window)
    camera = tk.Frame(base, width=480, height=400, bg="green")
    #frame.place(x=25, y=22.5)
    
    cam.Camera(camera)
    catalog = tk.Frame(base, bg="red")

    config = tk.Frame(base, width=800, height=400, bg="blue")
    #frame.place(x=25, y=392.5)

    #cfg.Config(frame)
    
    base.grid(column=0, row=0, sticky=("N", "S", "E", "W"))
    camera.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=("N", "S", "E", "W"))
    catalog.grid(column=3, row=0, columnspan=2, rowspan=2, sticky=("N", "S", "E", "W"))
    config.grid(column=0, row=2, columnspan=5, rowspan=2, sticky=("N", "S", "E", "W"))

    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    base.columnconfigure(0, weight=1)
    base.columnconfigure(1, weight=1)
    base.columnconfigure(2, weight=1)
    base.columnconfigure(3, weight=1)
    base.columnconfigure(4, weight=1)
    base.rowconfigure(0, weight=1)
    base.rowconfigure(1, weight=1)
    base.rowconfigure(2, weight=1)
    base.rowconfigure(3, weight=1)

    window.mainloop()
    

new_window()
