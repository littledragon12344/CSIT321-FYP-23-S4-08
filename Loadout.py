import tkinter as tk
from tkinter import filedialog
import LoadoutGestures as LOG
from ReadWriteFile import *

# loadout display class
class LoadoutDisplay():
    def __init__(self, frame, width, height):
        # saving the frame and its dimension
        self.root = frame
        self.width = width
        self.height = height
    
        # initializing values
        self.selected = -1
        self.loadouts = {
            'Loadout 1': {'Open_Palm': 'Space', 'Victory': 'W'}, 
            'Loadout 2': {'Open_Palm': 'A', 'Victory': 'S'}
        }
        
        loadout = Loadout()
        loadout.add_pair(gesture='Open_Palm', key='S')
        
        self.loadouts['Loadout 3'] = loadout
        
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
        enable_btn = tk.Button(container, width=6, text="Enable", command= lambda: self.enable_loadout(self.selected))
        enable_btn.grid(column=2, row=0, sticky="news", padx=1, pady=1.5)
        # create a disable button
        disable_btn = tk.Button(container, width=6,text="Disable", command= lambda: self.disable_loadout(self.selected))
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
        
        #display loadouts
        self.display_loadouts(self.loadouts)

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
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
    def update_display(self, loadout_list):
        # clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        # display loadouts
        self.display_loadouts(loadout_list)
    
    def search_loadout(self):
        # getting the input text
        search_txt = self.searchbar.get("1.0", "end-1c")
        # initializing an empty dictionary
        loadouts_found = {}
        # start searching by the loadout name
        for loadout_name, loadout_data in self.loadouts.items():
            if search_txt.casefold() in loadout_name.casefold():
                loadouts_found[loadout_name] = loadout_data
        # update the display
        self.update_display(loadouts_found)
        
        print(f"Searched for {search_txt} loadout!")
    
    def enable_loadout(self, id):
        print(f"Enabled {id} loadout!")
    
    def disable_loadout(self, id):
        print(f"Disabled {id} loadout!")
        
    def loadout_select_handler(self, id, loadout_name):
        def handler(event):
            # reset the frames appearance
            for child in self.frame.winfo_children():
                child.configure(bg="yellow")
            
            # hightlight the selected frame
            selected_frame = self.frame.winfo_children()[id]
            selected_frame.config(bg="brown")
            
            print(f"{loadout_name}")
            
            self.selected = id
            print(f"Selected frame #{id}")    
        return handler
    
def dictionary_to_string(dictionary):
    str = ""
    for gesture, key in dictionary.items():
        str += f"{gesture}: {key}\n"
    return str

def string_to_dictionary(str):
    lines = str.splitlines()
    result = {}
    for line in lines:
        line = line.strip()
        # skip empty lines
        if line:
            gesture, key = line.split(': ', 1)
            result[gesture] = key
    return result

def importLoadout():
    # ask the user to choose a file location
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        print(f"Selected file: {file_path}")
        LOG.LoadLoadoutFile(file_path)

def exportLoadout():
    # ask the user to choose a file location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        print(f"Selected export location: {file_path}")
        file_str = readFromFile()
        
        LOG.SaveLoadoutFile(file_path)

# loadout controller class
class LoadoutController():
    pass

# loadout entity class
class Loadout():
    def __init__(self, gestures_map=None):
        if gestures_map is None:
            self.dictionary = {}
        else:
            self.dictionary = gestures_map
        
    def add_pair(self, gesture, key):
        self.dictionary[gesture] = key
        
    def items(self):
        return self.dictionary.items()
