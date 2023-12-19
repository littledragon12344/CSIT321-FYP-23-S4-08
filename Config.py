import tkinter as tk
import iConfig as icfg
import math
from PIL import Image, ImageTk

class Config:
    cfglist = []
    def __init__(self, window):
        self.window = window
        
        # create a canvas for list display
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=2)

        # create a vertical scrollbar and attach it to the display frame
        self.scrollbar = tk.Scrollbar(self.window, width=20, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # config the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # create a frame to contain the widgets within the canvas
        self.frame = tk.Frame(self.canvas)
        #self.frame.grid_propagate(False)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        # Read loadout information
        self.getloadout()

        # update the scrollregion
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    # For testing sake, no params
    def getloadout(self):
        size = 120, 120
        img = Image.open("TestImage.jpg")
        img.thumbnail(size)
        phi = ImageTk.PhotoImage(img)
        
        for i in range(10):
            # create test object
            cfgobject = icfg.iConfig(self.frame, phi, f"test object {i+1}", "X")
            
            # Place test objects in vector
            self.cfglist.append(cfgobject)
            
        for ind, x in enumerate(self.cfglist):
            z = ind % 5
            y = math.floor(ind/5)
            x.base.grid(column=z, row=y, padx=8, pady=8)
