import tkinter as tk
import iConfig as icfg
import Loadout as ld
import math
import Camera as cam
import ModelTrainer as MT
import HandDetector as HD
import ProgramSettings as PS

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
        self.buildText = tk.StringVar()

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
            image_path = PS.os.path.join(PS.image_folder_path, f'{self.cfggestures[i]}.png')
            if PS.os.path.exists(image_path):
                img = Image.open(image_path)
                phi2 = ImageTk.PhotoImage(img.resize(size))
                cfgobject = icfg.iConfig(self.frame, phi2, f"{self.cfggestures[i]}", f"{self.cfgkeys[i]}", self.pop)
            else:
                cfgobject = icfg.iConfig(self.frame, phi, f"{self.cfggestures[i]}", f"{self.cfgkeys[i]}", self.pop)
            
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
        self.buildText.set("Ready to build")

        if self.pop:
            def ChangeName(x):   
                gesture_name=menuText.get()
                gesture_name.replace(" ", "_") # incase user enters a name with Space
                PS.change_recorded_gesture(gesture_name)

            def SetName():
                return   

            self.pop_win = self.pop("Test")
            tFrame = tk.Frame(self.pop_win)
            tLabel = tk.Label(tFrame, width=55, text="Click the button to record a new gesture")
            NameLabel = tk.Label(tFrame, width=15, text="Name:")
            NameText = tk.Text(tFrame, height = 1, width = 15)
            NameChangeBtn= tk.Button(tFrame,text="Change Name", command=ChangeName)
            tRecord = tk.Button(tFrame, textvariable=self.btnText, command=self.button_trigger)
            buildLabel = tk.Label(tFrame, textvariable=self.buildText)
            tBuild = tk.Button(tFrame, text="Build", command=self.build_model)
            tClose = tk.Button(tFrame, text="Close", command=self.pop_win.destroy)
            menuText = tk.StringVar() 
            menuText.set(PS.allowed_gestures[0]) 
            dropDown = tk.OptionMenu(tFrame , menuText , *PS.allowed_gestures, command=ChangeName) 
            #===============================================================#
            tFrame.grid(column=0, row=0, sticky=("N", "S", "E", "W"))
            NameLabel.grid(column=0, row=0, sticky=("N", "S", "E", "W"))
            NameText.grid(column=1, row=0, columnspan=2, sticky=("N", "S", "E", "W"))
            NameChangeBtn.grid(column=3, row=0, sticky=("N", "S", "E", "W"))
            tLabel.grid(column=0, row=1, columnspan=4, sticky=("N", "S", "E", "W"))
            tRecord.grid(column=0, row=2, sticky=("N", "S", "E", "W"))
            tBuild.grid(column=0, row=3, sticky=("N", "S", "E", "W"))
            buildLabel.grid(column=1, row=3, sticky=("N", "S", "E", "W"))
            tClose.grid(column=2, row=2, columnspan=2, sticky=("N", "S", "E", "W"))
            dropDown.grid(column=1, row=2, sticky=("N", "S", "E", "W"))
        
    def button_trigger(self):
        self.change_button()
        self.record_gesture()
    
    def change_button(self):
        if self.pop_win:
            if self.btnText.get() == "Record": self.btnText.set("Stop")
            else: self.btnText.set("Record")
    
    def record_gesture(self):
        self.change_button()
        cam.Camera.start_landmark_recording()

    def build_model(self):
        MT.ModelTrainer.preprocess_data()
        self.buildText.set("Build complete!")