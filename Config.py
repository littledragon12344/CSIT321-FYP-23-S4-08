import tkinter as tk
from tkinter import ttk
import iConfig as icfg
import math
import Camera as cam
import ModelTrainer as MT
import HandDetector as HD
import ProgramSettings as PS
import keyboard as kb

from PIL import Image, ImageTk

class Config:
    def __init__(self, window, widget, pop, update):
        self.cfglist = []
        self.cfggestures = []
        self.cfgkeys = []

        self.gui_update = update
        self.loadout_widget = widget
        self.pop = pop
        self.pop_win = None
        self.val = None
        self.this_id = -1

        self.btnText = tk.StringVar()

        self.window = window
        base = tk.Frame(self.window, highlightbackground="black", highlightthickness=2)
        base.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10)

        # create a canvas for list display
        self.canvas = tk.Canvas(base, width=750, height=450)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # create a vertical scrollbar and attach it to the display frame
        self.scrollbar = tk.Scrollbar(base, width=20, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # config the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # create a frame to contain the widgets within the canvas
        self.frame = tk.Frame(self.canvas)
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

        # Empty old data
        if len(self.cfggestures) > 0:
            self.cfggestures.clear()
            self.cfgkeys.clear()
        
        self.this_id = self.loadout_widget.selected_id
        currentload = self.loadout_widget.controller.get_currently_enabled()
        controls = currentload.get_all_pairs()

        for (gesture, key) in controls.items():
            self.cfggestures.append(gesture)
            self.cfgkeys.append(key)
        
        # Insert objects using loadout data
        for i in range(len(controls.items())):
            image_path = PS.os.path.join(PS.image_folder_path, f'{self.cfggestures[i]}.png')
            if PS.os.path.exists(image_path):
                img = Image.open(image_path)
                phi2 = ImageTk.PhotoImage(img.resize(size))
                cfgobject = icfg.iConfig(self.frame, phi2, f"{self.cfggestures[i]}", f"{self.cfgkeys[i]}", self, self.pop)
            else:
                cfgobject = icfg.iConfig(self.frame, phi, f"{self.cfggestures[i]}", f"{self.cfgkeys[i]}", self, self.pop)
            
            self.cfglist.append(cfgobject)

        for ind, x in enumerate(self.cfglist):
            last = ind + 1
            z = ind % 5
            y = math.floor(ind/5)
            x.base.grid(column=z, row=y, padx=7, pady=7)
        
        # Create Gesture button
        cImg = Image.open("AddSlot.png")
        cImage = ImageTk.PhotoImage(cImg)
        cFrame = tk.Frame(self.frame, width=145, height=210)
        cButton = tk.Button(cFrame, width=145, height=210, image=cImage, command=self.create_gesture)
        cButton.image = cImage
        
        nextZ = last % 5
        nextY = math.floor(last/5)
        cFrame.grid(column=nextZ, row=nextY)
        cButton.grid(column=0, row=0, sticky="news")
        
        print(f"Showing total of {len(self.cfglist)} results!")

    def set_loadout(self, load):
        self.loadout_widget = load         

    def create_gesture(self):
        self.btnText.set("Record")
        global nameText
        global menuText
        global tInput
        global tChange

        if self.pop:
            def change_name(x):   
                gesture_name=menuText.get()
                gesture_name.replace(" ", "_") # incase user enters a name with Space
                PS.change_recorded_gesture(gesture_name)
            
            self.pop_win = self.pop("Create New Gesture")
            tFrame = tk.Frame(self.pop_win)
            eLabel = tk.Label(tFrame)
            tLabel = tk.Label(tFrame, width=39, text="Click Record to record and add new gesture data")
            iLabel = tk.Label(tFrame, width=13, text="New Input:")
            cLabel = tk.Label(tFrame, width=52, text="Click Confirm to add gesture from the")
            cLabel2 = tk.Label(tFrame, width=52, text="drop down list with the above input")
            nameLabel = tk.Label(tFrame, text="New Gesture Name:")
            nameText = tk.Text(tFrame, height=1, width=32)
            tRecord = tk.Button(tFrame, textvariable=self.btnText, command= lambda : self.button_trigger(tFrame))
            tConfirm = tk.Button(tFrame, text="Confirm", command=self.confirm_trigger)
            menuText = tk.StringVar() 
            menuText.set(PS.allowed_gestures[0]) 
            dropDown = tk.OptionMenu(tFrame , menuText , *PS.allowed_gestures, command=change_name)
            tInput = tk.Text(tFrame, height=1, width=24)
            tInput.config(state="disabled")
            tChange = tk.Button(tFrame, width=11, text="Change Input", command=self.change_key)
            tAddGesture = tk.Button(tFrame, width=11, text="Add Gesture", command=self.set_name)
            #===============================================================#
            tFrame.grid(column=0, row=0, sticky="news")
            iLabel.grid(column=0, row=0, sticky="news")
            tInput.grid(column=1, row=0, columnspan=2, sticky="news")
            tChange.grid(column=3, row=0, sticky="news")
            nameLabel.grid(column=0, row=1, sticky="news")
            nameText.grid(column=1, row=1, columnspan=4, sticky="news")
            tAddGesture.grid(column=3, row=1, sticky="news")
            tLabel.grid(column=0, row=2, columnspan=3, sticky="news")
            tRecord.grid(column=3, row=2, sticky="news")
            eLabel.grid(column=0, row=3, columnspan=4, sticky="news")
            cLabel.grid(column=0, row=4, columnspan=4, sticky="news")
            cLabel2.grid(column=0, row=5, columnspan=4, sticky="news")
            tConfirm.grid(column=2, row=6, columnspan=2, sticky="news")
            dropDown.grid(column=0, row=6, columnspan=2, sticky="news")
            
            # progress bar
            self.progress_var = tk.IntVar()
            self.recordProgressBar = ttk.Progressbar(tFrame, variable=self.progress_var, orient="horizontal", mode="determinate")
            self.recordProgressBar.grid(column=0, row=7, sticky="news", columnspan=4)
            # hide progress bar
            self.recordProgressBar.grid_remove()
        
    def empty_alert(self):
        alert = self.pop("Alert")
        aLabel = tk.Label(alert, text="No Input detected")
        aClose = tk.Button(alert, text="Close", command=alert.destroy)
        aLabel.grid(column=0, row=0, sticky="news")
        aClose.grid(column=0, row=1, sticky="news")
        
    def button_trigger(self, widget):
        if tInput.compare("end-1c", "==", "1.0"):
            self.empty_alert()
            return
        self.change_button()
        self.record_gesture()
        # show the progress bar
        self.recordProgressBar.grid()
        widget.after(100, self.update_progress_var, widget)  
    
    def confirm_trigger(self):
        if tInput.compare("end-1c", "==", "1.0"):
            self.empty_alert()
            return
        self.update_key(menuText.get(), self.val)
        if self.pop_win:
            self.pop_win.destroy()
    
    def change_button(self):
        if self.pop_win:
            if self.btnText.get() == "Record": self.btnText.set("Stop")
            else: self.btnText.set("Record")
    
    def record_gesture(self):
        self.change_button()
        cam.Camera.start_landmark_recording()
    
    def set_name(self):
        PS.add_new_gesture(nameText.get("1.0", "end-1c"))
        self.pop_win.destroy()
        self.create_gesture()
    
    def change_key(self):
        tChange.config(text="Input Key")
        if self.pop_win:
            self.pop_win.update_idletasks()
        self.val = kb.read_key()
        tInput.config(state="normal")
        tInput.delete('1.0', tk.END)
        tInput.insert(tk.INSERT, self.val.upper())
        tInput.config(state="disabled")
        tChange.config(text="Change Input")
        
    def update_progress_var(self, widget):
        counter = HD.iteration_counter
        
        self.progress_var.set(counter)
        self.recordProgressBar.update_idletasks()
        
        if counter > 99:
            # hide the progress bar
            self.recordProgressBar.grid_remove()
        else:
            widget.after(100, self.update_progress_var, widget)
    
    def complete_key(self, gest):
        self.update_key(gest, self.val)
        if self.pop_win:
            self.pop_win.destroy()

    def build_model(self):
        MT.ModelTrainer.preprocess_data()
        HD.reload_model()
    
    def update_key(self, gest, key=None, newkey=None):
        # Delete, Add or Update gesture-key configuration
        if key==None and newkey==None:
            keypos = self.cfggestures.index(gest)
            self.cfggestures.remove(gest)
            self.cfgkeys.remove(self.cfgkeys[keypos])
        elif (key!=None and newkey==None):
            self.cfggestures.append(gest)
            self.cfgkeys.append(key)
        else: 
            keypos = self.cfggestures.index(gest)
            if self.cfgkeys[keypos] == key:
                self.cfgkeys[keypos] = newkey
        # Create new dictionary to hold updated gesture-key information
        gesturedata = {}
        for gesture, key in zip(self.cfggestures, self.cfgkeys):
            gest_name = gesture
            gest_name.replace(" ", "_")
            key_name = key.lower()
            gesturedata[gest_name] = key_name
        # Update loadout
        self.loadout_widget.controller.update_loadout(self.this_id, gesturedata)
        # Refresh config
        self.gui_update()