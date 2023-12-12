import tkinter as tk
import Camera as cam
import Config as cfg

#import cv2 as cv
#import numpy as np
#import mediapipe as mp

def new_window(): 
    root = tk.Tk()
    root.title("Gesture Detection Prototype")
    root.geometry("800x600")
    root.resizable(width=False, height=False)
    
    #label = tk.Label(root, text="Created by group CSIT321-FYP-23-S4-08")
    #label.pack()

    #======================== MENU BAR ========================
    # creates a new menu bar
    menubar = tk.Menu(root)
    
    # file menu items
    file_menu = tk.Menu(menubar, tearoff=0)
    # 
    file_menu.add_command(label="New")
    # loadouts
    file_menu.add_separator()
    file_menu.add_command(label="Import loadouts")
    file_menu.add_command(label="Export loadouts")
    # exit from app
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # options menu items
    options_menu = tk.Menu(menubar, tearoff=0)
    # tutorial
    options_menu.add_command(label="Start tutorial...")
    
    # display the options on the menu bar
    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Options", menu=options_menu)
    # set menu bar for the main window
    root.config(menu=menubar)
    #==========================================================
    
    #======================== UI LAYOUT ========================
    # create a base frame for the layout
    base = tk.Frame(root)
    # create a frame to contain the camera
    camera = tk.Frame(base, width=480, height=350, bg="green")
    # get the camera feed for the frame
    cam.Camera(camera, 450, 320)
    
    # create a frame for the loadout display
    catalog = tk.Frame(base, bg="red")
    # create a frame for the gesture list display
    config = tk.Frame(base, width=800, height=300, bg="blue")

    cfg.Config(config)
    
    # placing the frames onto a grid for the UI layout
    base.grid(column=0, row=0, sticky=("N", "S", "E", "W"))
    camera.grid(column=0, row=0, columnspan=3, rowspan=2, padx=2, pady=2, sticky="news")
    catalog.grid(column=3, row=0, columnspan=2, rowspan=2, padx=0, pady=2, sticky="news")
    config.grid(column=0, row=2, columnspan=5, rowspan=2, sticky="news")
    #===========================================================

    # start the window
    root.mainloop()
    

new_window()
