import tkinter as tk
#import LoadoutGestures as LOG
from ReadWriteFile import *

# loadout display class
class LoadoutDisplay():
    def __init__(self, frame, width, height):
        # saving the frame and its dimension
        self.root = frame
        self.width = width
        self.height = height
    
        # initializing values
        self.selected = ""
        
        # create a controller
        self.controller = LoadoutController()
        
        # getting the layout
        self.get_layout()

    def get_layout(self):
        # create a frame as a container
        container = tk.Frame(self.root, height=1, bg="magenta")
        container.pack(side="top", fill="x", expand=True, padx=1, pady=1, anchor="n")
        # create a text input field
        self.searchbar = tk.Text(container, width=20, height=1, wrap="none")
        self.searchbar.grid(column=0, row=0, sticky="news", pady=1.5)
        # create a search button
        search_btn = tk.Button(container, width=6, text="Search", command=self.search_loadout)
        search_btn.grid(column=1, row=0, sticky="news", padx=1, pady=1.5)
        # create an enable button
        enable_btn = tk.Button(container, width=6, text="Enable", command= lambda: self.controller.enable_loadout(self.selected))
        enable_btn.grid(column=2, row=0, sticky="news", padx=1, pady=1.5)
        # create a disable button
        disable_btn = tk.Button(container, width=6,text="Disable", command= lambda: self.controller.disable_loadout(self.selected))
        disable_btn.grid(column=3, row=0, sticky="news", padx=1, pady=1.5)
        
        # create a canvas for list display
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height + 15, bg="cyan")
        self.canvas.pack(side="left", fill="both", expand=True, padx=1)

        # create a vertical scrollbar and attach it to the LoadoutDisplay frame
        self.scrollbar = tk.Scrollbar(self.root, width=20, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # config the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # create a frame to contain the widgets within the canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", width=self.width)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        #display loadouts
        self.display_loadouts(self.controller.loadouts)

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def display_loadouts(self, loadout_list):
        # add loadouts to the display
        for id, (name, sub_dict) in enumerate(loadout_list.items()):
            # create a frame for the item
            item_frame = tk.Frame(self.frame, bg="yellow", pady=2, padx=2)
            item_frame.pack(fill="x", expand=True, padx=2, pady=2)
            # bind mouse event to the frame
            item_frame.bind("<Button-1>", self.loadout_select_handler(id, name))
            
            # loadout name label
            loadout_name = tk.Label(item_frame, text=f"{name}", width=14, anchor="center")
            loadout_name.grid(column=0, row=0, padx=1, sticky="news", columnspan=2)
            
            # gestures and their repective keys labels
            for i, (gesture, key) in enumerate(sub_dict.items()):
                gesture_label = tk.Label(item_frame, text=f"{gesture}", width=12, anchor="center")
                gesture_label.grid(column=2, row=i+1, padx=1, sticky="news", columnspan=2)
                
                key_label = tk.Label(item_frame, text=f"{key}", width=12, anchor="center")
                key_label.grid(column=4, row=i+1, padx=1, sticky="news", columnspan=2)
        
        # update the scrollregion
        self.on_canvas_configure(None)
        
    def update_display(self, loadout_list):
        # clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # display loadouts
        self.display_loadouts(loadout_list)
    
    def search_loadout(self):
        # getting the input text
        search_txt = self.searchbar.get("1.0", "end-1c")
        # search for the matching loadout
        loadouts_found = self.controller.find_loadout(search_txt)
        # update the display
        self.update_display(loadouts_found)
        
        print(f"Searched for {search_txt} loadout!")
    
    def loadout_select_handler(self, id, loadout_name):
        def handler(event):
            # reset the frames appearance
            for child in self.frame.winfo_children():
                child.configure(bg="yellow")
            
            # hightlight the selected frame
            selected_frame = self.frame.winfo_children()[id]
            selected_frame.config(bg="brown")
            
            print(f"{loadout_name}")
            
            self.selected = loadout_name
            print(f"Selected frame #{id}, with name: {loadout_name}")    
        return handler
    
    def import_loadout(self):
        self.controller.import_loadout_from_file()
        self.update_display(self.controller.loadouts)
        
    def export_loadout(self):
        for name, data in self.controller.loadouts.items():
            if self.selected.casefold() in name.casefold():
                self.controller.export_loadout_to_file(data)

    def set_camera_display(self, camera):
        # set reference to the camera
        self.controller.set_camera_display(camera)
        # enable default loadout
        self.controller.enable_default_loadout()
    
    def get_current_loadout(self):
        return self.controller.get_currently_enabled()

# ====================================== CONTROLLER ======================================
class LoadoutController():
    def __init__(self):
        self.loadouts = {}
        self.enabled = ""
        # create a reference to the camera display
        self.cam_display = None
        
        # import all loadouts from a folder
        self.load_loadouts_from_folder("Loadout_Info")
    
    def add_loadout(self, name, data):
        self.loadouts[name] = data
    
    def find_loadout(self, search_txt):
        # initializing an empty dictionary
        found = {}
        # start searching by the loadout name
        for name, data in self.loadouts.items():
            if search_txt.casefold() in name.casefold():
                found[name] = data
        
        return found
    
    def enable_loadout(self, name):
        self.enabled = name
        if self.cam_display is not None: 
            # get the entity class
            curr_enabled = self.get_currently_enabled()
            # convert the entity class to dictionarys
            self.cam_display.set_loadout(curr_enabled.get_all_pairs())
        print(f"Enabled loadout: {name}!")
    
    def enable_default_loadout(self):
        self.enable_loadout(next(iter(self.loadouts)))
        
    def disable_loadout(self, name):
        print(f"Disabled loadout: {name}!")
    
    def set_camera_display(self, camera):
        self.cam_display = camera

    def get_currently_enabled(self):
        return self.loadouts[self.enabled]
    
    def load_loadouts_from_folder(self, folder_name):
        contents = readFromFolder(folder_name)
        # loop through the content list and extract the data
        for content in contents:
            lines = content.splitlines()
            # initialize the loadout
            loadout = Loadout()
            # start converting string data to loadout
            for line in lines:
                line = line.strip()
                # skip empty lines
                if line:
                    if ':' in line:
                        parts = line.split(':', 1)
                        loadout.name = parts[0].strip()
                    elif '-' in line:
                        gesture, key = line.split('-', 1)
                        loadout.add_pair(gesture, key)
            # add the loadout to the list
            self.add_loadout(loadout.name, loadout)
    
    def import_loadout_from_file(self):
        # get data from a file
        str = readFromFile()
        # if file is empty return False
        if str == "": return False
        
        # split the string data into lines
        lines = str.splitlines()
        # initialize the loadout
        loadout = Loadout()
        # start converting string data to loadout
        for line in lines:
            line = line.strip()
            # skip empty lines
            if line:
                if ':' in line:
                    parts = line.split(':', 1)
                    loadout.name = parts[0].strip()
                elif '-' in line:
                    gesture, key = line.split('-', 1)
                    loadout.add_pair(gesture, key)
        
        self.add_loadout(loadout.name, loadout)
        return True

    def export_loadout_to_file(self, loadout):
        str = loadout.to_string()
        writeToFile(str)

# ====================================== ENTITY ======================================
class Loadout():
    def __init__(self, name=None, gestures_map=None, gesture=None, key=None):
        # initialize name
        if(name is None):
            self.name = "New Loadout"
        else: 
            self.name = name
        # initialize dictionary
        if gestures_map is None:
            self.dictionary = {}
        else:
            self.dictionary = gestures_map
        # adding gesture key pair
        if gesture is not None and key is not None:
            self.add_pair(gesture, key)
        
    def add_pair(self, gesture, key):
        self.dictionary[gesture] = key
        
    def items(self):
        return self.dictionary.items()
    
    def to_string(self):
        str = f"{self.name}:\n"
        for gesture, key in self.dictionary.items():
            str += f"{gesture}-{key}\n"
        return str
    
    def get_all_pairs(self):
        return self.dictionary
