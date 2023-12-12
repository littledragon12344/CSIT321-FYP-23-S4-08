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
    
    cam.Camera(camera)
    catalog = tk.Frame(base, width=320, height=400, bg="red")

    config = tk.Frame(base, width=800, height=400, bg="blue")

    cfg.Config(config)
    
    base.grid(column=0, row=0, sticky="news")
    camera.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="news")
    catalog.grid(column=3, row=0, columnspan=2, rowspan=2, sticky="news")
    config.grid(column=0, row=2, columnspan=5, rowspan=2, sticky="news")

    window.mainloop()
    

new_window()
