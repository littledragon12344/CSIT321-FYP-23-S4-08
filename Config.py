import tkinter as tk
import iConfig as icfg
import Loadout as ld
import math
import ModelTrainer as MT
from PIL import Image, ImageTk

class Config:
    def __init__(self, window, widget, pop):
        self.cfglist = []
        self.cfggestures = []
        self.cfgkeys = []

        self.loadout_widget = widget
        self.pop = pop
        self.pop_win = None

        self.btnText = tk.StringVar()

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
        self.get_config()

        # update the scrollregion
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    # For testing sake, no params
    def get_config(self):
        last = 0
        size = 120, 120
        img = Image.open("TestImage.jpg")
        img.thumbnail(size)
        phi = ImageTk.PhotoImage(img)
        
        currentload = self.loadout_widget.controller.get_currently_enabled()
        controls = currentload.get_all_pairs()

        for (gesture, key) in controls.items():
            self.cfggestures.append(gesture)
            self.cfgkeys.append(key)

        for i in range(len(controls.items())):
            # create test object
            cfgobject = icfg.iConfig(self.frame, phi, f"{self.cfggestures[i]}", f"{self.cfgkeys[i]}")
            
            # Place test objects in vector
            self.cfglist.append(cfgobject)
            
        for ind, x in enumerate(self.cfglist):
            last = ind + 1
            z = ind % 5
            y = math.floor(ind/5)
            x.base.grid(column=z, row=y, padx=8, pady=8)
        
        # Create Gesture button
        cImg = Image.open("AddSlot.png")
        cImage = ImageTk.PhotoImage(cImg)
        cFrame = tk.Frame(self.frame, width=150, height=210)
        cButton = tk.Button(cFrame, width=150, height=210, image=cImage, command=self.create_gesture)
        cButton.image = cImage
        
        nextZ = last % 5
        nextY = math.floor(last/5)
        cFrame.grid(column=nextZ, row=nextY)
        cButton.grid(column=0, row=0, sticky=("N", "S", "E", "W"))
        
        print(f"Showing total of {len(self.cfglist)} results!")

    def set_loadout(self, load):
        self.loadout_widget = load
    
    def create_gesture(self):
        self.btnText.set("Record")
        if self.pop:
            self.pop_win = self.pop("Test")
            tFrame = tk.Frame(self.pop_win, width=400, height=200)
            tLabel = tk.Label(tFrame, text="Button closes this window")
            tRecord = tk.Button(tFrame, textvariable=self.btnText, command=self.button_trigger)
            tClose = tk.Button(tFrame, text="Close", command=self.pop_win.destroy)

            tFrame.grid(column=0, row=0, sticky=("N", "S", "E", "W"))
            tLabel.grid(column=0, row=0, columnspan=2, sticky=("N", "S", "E", "W"))
            tRecord.grid(column=0, row=1, sticky=("N", "S", "E", "W"))
            tClose.grid(column=1, row=1, sticky=("N", "S", "E", "W"))
        
    def button_trigger(self):
        self.change_button()
        self.record_gesture()
    
    def change_button(self):
        if self.pop_win:
            if self.btnText.get() == "Record": self.btnText.set("Stop")
            else: self.btnText.set("Record")
    
    def record_gesture(self):
        self.change_button()
        MT.ModelTrainer.preprocess_data()
        print(f"The record button is functioning.")