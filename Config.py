import tkinter as tk
import iConfig as icfg
import Loadout as ld
import math
from PIL import Image, ImageTk

class Config:
    cfglist = []
    cfggestures = []
    cfgkeys = []
    
    def __init__(self, window, widget):
        self.loadoutwidget = widget

        self.window = window
        base = tk.Frame(self.window, highlightbackground="black", highlightthickness=2)
        base.pack(side="left", fill="both", expand=True, padx=10)
        
        # create a canvas for list display
        self.canvas = tk.Canvas(base)
        self.canvas.pack(side="left", fill="both", expand=True)

        # create a vertical scrollbar and attach it to the display frame
        self.scrollbar = tk.Scrollbar(base, width=20, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # config the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # create a frame to contain the widgets within the canvas
        self.frame = tk.Frame(self.canvas)
        #self.frame.grid_propagate(False)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        # Read loadout information
        self.getconfig()

        # update the scrollregion
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    # For testing sake, no params
    def getconfig(self):
        size = 120, 120
        img = Image.open("TestImage.jpg")
        img.thumbnail(size)
        phi = ImageTk.PhotoImage(img)
        
        currentload = self.loadoutwidget.controller.get_currently_enabled()
        controls = currentload.get_all_pairs()
        print(f"{type(controls)}")

        for (gesture, key) in controls.items():
            self.cfggestures.append(gesture)
            self.cfgkeys.append(key)

        for i in range(len(controls.items())):
            # create test object
            cfgobject = icfg.iConfig(self.frame, phi, f"{self.cfggestures[i]}", f"{self.cfgkeys[i]}")
            
            # Place test objects in vector
            self.cfglist.append(cfgobject)
            
        for ind, x in enumerate(self.cfglist):
            z = ind % 5
            y = math.floor(ind/5)
            x.base.grid(column=z, row=y, padx=8, pady=8)

    def setloadout(self, load):
        self.loadoutwidget = load