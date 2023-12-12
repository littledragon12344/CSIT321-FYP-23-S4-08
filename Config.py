import tkinter as tk
import iConfig as icfg
import math
from PIL import Image, ImageTk

class Config:
    cfglist = []
    def __init__(self, window):
        self.window = window

        # Create a Frame to store config information
        self.container = tk.Frame(self.window, width=780, height=235,
                                  highlightbackground="black",
                                  highlightthickness=2)
        self.container.grid_propagate(False)
        
        # Read loadout information
        self.getloadout()
        
        self.container.grid(column=0, row=0, padx=10, pady=5)
        for ind, x in enumerate(self.cfglist):
            z = ind % 5
            y = math.floor(ind/5)
            x.base.grid(column=z, row=y, padx=8, pady=8)
    
    # For testing sake, no params
    def getloadout(self):
        size = 120, 120
        img = Image.open("TestImage.jpg")
        img.thumbnail(size)
        phi = ImageTk.PhotoImage(img)
        cfgobject = icfg.iConfig(self.container, phi, "testname", "X")
        cfgobject1 = icfg.iConfig(self.container, phi, "testname", "X")
        cfgobject2 = icfg.iConfig(self.container, phi, "testname", "X")
        cfgobject3 = icfg.iConfig(self.container, phi, "testname", "X")
        cfgobject4 = icfg.iConfig(self.container, phi, "testname", "X")

        # Place test objects in vector
        self.cfglist.append(cfgobject)
        self.cfglist.append(cfgobject1)
        self.cfglist.append(cfgobject2)
        self.cfglist.append(cfgobject3)
        self.cfglist.append(cfgobject4)

        # Place objects within frame
        # Place test objects in window
        # cfgobject.base.grid(column=0, row=0)