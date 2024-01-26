import tkinter as tk
from tkinter import messagebox, ttk
from FileManager import *
from KeyboardInput import detect_key
from ProgramSettings import allowed_gestures

# loadout display class
class LoadoutDisplay():
    def __init__(self, frame, width, height, updatefunction):
        # saving the frame and its dimension
        self.root = frame
        self.width = width
        self.height = height

        # save reference to gui update function
        self.gui_update = updatefunction
        # create reference list to the loadout name labels
        self.loadout_name_labels = []
    
        # initializing values
        self.selected_name = ""
        self.selected_id = -1
        
        # create a controller
        self.controller = LoadoutController()
        
        # getting the layout
        self.get_layout()

    def get_layout(self):
        # create a frame as a container
        container = tk.Frame(self.root, height=1, bg="magenta")
        container.pack(side="top", fill="x", expand=True, padx=1, pady=1, anchor="n")
        # create a text input field
        self.searchbar = tk.Entry(container, width=20, font=('', 12))
        self.searchbar.grid(column=0, row=0, sticky="news", pady=1.5)
        # bind the search bar to enter key to search loadout
        self.searchbar.bind("<Return>", lambda _: self.search_loadout())
        # create a search button
        self.search_btn = tk.Button(container, width=8, text="Search", command=self.search_loadout)
        self.search_btn.grid(column=1, row=0, sticky="news", padx=1, pady=1.5)
        # create an enable button
        self.enable_btn = tk.Button(container, width=8, text="Enable", command=self.enable_loadout)
        self.enable_btn.grid(column=2, row=0, sticky="news", padx=1, pady=1.5)
        # create a disable button
        #disable_btn = tk.Button(container, width=6,text="Disable", command= lambda: self.controller.disable_loadout(self.selected_name))
        #disable_btn.grid(column=3, row=0, sticky="news", padx=1, pady=1.5)
        
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
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", width=self.width+5)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
        #display loadouts
        self.display_loadouts(self.controller.get_dictionaries())
    
    def on_mousewheel(self, event):
        # Scroll the canvas when the mouse wheel is used
        scroll_speed = 1.0  # Adjust this value to control the scroll speed
        self.canvas.yview_scroll(int(-1 * (event.delta / 120) * scroll_speed), "units")
        
    def on_canvas_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()

    def bind_recursive(self, widget, event_string, callback):
        # bind the widget to an event callback
        widget.bind(event_string, callback)
        # bind all children in the widget to an event callback
        for child in widget.winfo_children():
            self.bind_recursive(child, event_string, callback)

    def display_loadouts(self, loadout_list):
        # clear references
        self.loadout_name_labels.clear()
        # add loadouts to the display
        for id, (name, sub_dict) in enumerate(loadout_list.items()):
            # create a frame for the item
            item_frame = tk.Frame(self.frame, bg="yellow", bd=0.5, relief=tk.SOLID)
            item_frame.pack(fill="x", expand=True, pady=2)
            
            # loadout name label
            loadout_name = tk.Label(item_frame, text=f"{name}", width=12, anchor="center")
            loadout_name.grid(column=0, row=0, padx=1, sticky="news", columnspan=2)
            self.loadout_name_labels.append(loadout_name)
            
            # gestures and their repective keys labels
            # connect to iConfig object
            for i, (gesture, key) in enumerate(sub_dict.items()):
                # create a label for the gesture 
                gesture_label = tk.Label(item_frame, text=f"{gesture}", width=14, anchor="center")
                gesture_label.grid(column=2, row=i+1, padx=1, sticky="news", columnspan=2)
                # create a label for the key 
                key_label = tk.Label(item_frame, text=f"{key.upper()}", width=14, anchor="center")
                key_label.grid(column=4, row=i+1, padx=1, sticky="news", columnspan=2)
            
            # create the new gesture key pair button to the current loadout
            new_loadout_btn = tk.Button(item_frame, text="+")
            new_loadout_btn.grid(column=5, row=0, sticky="ne", padx=6)
            # create a frame to contain the buttons
            hbox = tk.Frame(item_frame)
            hbox.grid(column=0, row=i+1, sticky="news")
            # create the edit name button
            rename_btn = tk.Button(hbox, text="Rename", command=self.rename_selected)
            rename_btn.grid(column=0, row=0, sticky="news")
            # create the delete loadout button
            delete_btn = tk.Button(hbox, text="Delete", bg="red", command=self.remove_selected)
            delete_btn.grid(column=1, row=0, sticky="news")
            
            # bind mouse click event to the item frame and its children
            self.bind_recursive(item_frame, "<Button-1>", self.loadout_select_handler(id, name))
            # bind scroll wheel event to the item frame and its children
            self.bind_recursive(item_frame, "<MouseWheel>", self.on_mousewheel)
        
        # update the scrollregion
        self.canvas.after(10, self.on_canvas_configure)
        
    def update_display(self, loadout_list):
        # clear the frame
        for widget in self.frame.winfo_children():
            widget.unbind_all(None)
            widget.destroy()
        # display loadouts
        self.display_loadouts(loadout_list)
    
    def search_loadout(self):
        # getting the input text
        search_txt = self.searchbar.get()
        # stop focus on the searchbar
        self.search_btn.focus_force()
        # search for the matching loadout
        loadouts_found = self.controller.find_loadout(search_txt)
        # update the display
        self.update_display(loadouts_found)
        
        print(f"Searched for {search_txt} loadout!")
    
    def enable_loadout(self):
        # enable the selected loadout
        self.controller.enable_loadout(self.selected_id)
        # update the enable button
        self.enable_btn.config(text="Enabled!", state=tk.DISABLED)
        # call update gui function in main window
        self.gui_update()
        # update the enabled frame background
        frame_children = self.frame.winfo_children()
        if self.selected_id >= 0 and self.selected_id < len(frame_children):
            frame_children[self.selected_id].config(bg="orange")
    
    def create_loadout_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Create new loadout")
        popup.geometry("500x300")
        
        # title label
        title_label = tk.Label(popup, text="Enter loadout information:", anchor="w", font=("",16,"bold"))
        title_label.pack(fill="x")
        # create container to contain the loadout name field
        name_frame = tk.Frame(popup)
        name_frame.pack(fill="x")
        # configure the column weight
        for i in range(2):
            name_frame.columnconfigure(i, weight=1)
        # loadout name field
        name_label = tk.Label(name_frame, text="Name:", anchor="w")
        name_label.grid(column=0, row=0, padx=10, sticky="news")
        name_entry = tk.Entry(name_frame)
        name_entry.grid(column=1, row=0, sticky="news")
        
        # create container to contain the gesture key pairs
        gesturekey_frame = tk.Frame(popup)
        gesturekey_frame.pack(fill="x")
        # configure the column weight
        for i in range(3):
            gesturekey_frame.columnconfigure(i, weight=1)
        # gesture label
        gesture_label = tk.Label(gesturekey_frame, text="Gestures")
        gesture_label.grid(column=1, row=0, sticky="news")
        # key label
        key_label = tk.Label(gesturekey_frame, text="Keys")
        key_label.grid(column=2, row=0, sticky="news")
        
        gesture_entries = []
        key_entries = []
        # create a container to contain the buttons
        btn_container = tk.Frame(gesturekey_frame)
        btn_container.grid(column=0, row=1)
        # create entry field button
        create_btn = tk.Button(btn_container, anchor="ne", text="+", command=lambda: self.create_gesturekey_field(gesturekey_frame, gesture_entries, key_entries))
        create_btn.grid(column=0, row=0, padx=5)
        # remove entry field button
        remove_btn = tk.Button(btn_container, anchor="nw", text="-", command=lambda: self.remove_gesturekey_field(gesture_entries, key_entries))
        remove_btn.grid(column=1, row=0, padx=5)
        
        # release gesture entry
        entry = ttk.Combobox(gesturekey_frame, values=allowed_gestures, state="readonly")
        # select the 1st option in
        entry.current(0)
        entry.grid(column=1, row=1, sticky="news")
        gesture_entries.append(entry)
        
        # release key entry
        entry = tk.Button(gesturekey_frame, text="Release", state=tk.DISABLED)
        entry.grid(column=2, row=1, sticky="news")
        key_entries.append(entry)
        
        self.create_gesturekey_field(gesturekey_frame, gesture_entries, key_entries)
        
        # create container to contain the buttons
        btn_frame = tk.Frame(popup)
        btn_frame.pack(fill="x")
        # configure the column weight
        for i in range(2):
            btn_frame.columnconfigure(i, weight=1)
        # confirm button
        confirmBtn = tk.Button(btn_frame, anchor="e", text="Confirm", bg="green", command=lambda: self.create_loadout(popup, name_entry.get(), gesture_entries, key_entries))
        confirmBtn.grid(column=0, row=0)
        # cancel button
        cancelBtn = tk.Button(btn_frame, anchor="w", text="Cancel", bg="red", command=popup.destroy)
        cancelBtn.grid(column=1, row=0)
    
    def create_gesturekey_field(self, base, gesture_entries, key_entries):
        gestures = allowed_gestures
        
        # get the current number of gestures
        gesture_count = len(gesture_entries)
        # prevent user from creating too many gestures
        if gesture_count >= len(gestures):
            return
        
        # gesture entry
        entry = ttk.Combobox(base, values=gestures, state="readonly")
        # select the 1st option in
        entry.current(0)
        entry.grid(column=1, row=gesture_count+1, sticky="news")
        gesture_entries.append(entry)
        
        # key entry
        # key entry callback
        def key_entry_callback(id):
            def on_key_press():
                key = detect_key()
                key_entries[id]["text"] = key.upper()
            return on_key_press 
        # create the entry
        entry = tk.Button(base, text="Click to start", command=key_entry_callback(gesture_count))
        entry.grid(column=2, row=gesture_count+1, sticky="news")
        key_entries.append(entry)
    
    def remove_gesturekey_field(self, gesture_entries, key_entries):
        if(len(gesture_entries) > 1):
            # remove the widget from list
            gesture_entry = gesture_entries.pop()
            # destroy the widget
            gesture_entry.unbind_all(None)
            gesture_entry.destroy()
            
        if(len(key_entries) > 1):
            # remove the widget from list
            key_entry = key_entries.pop()
            # destroy the widget
            key_entry.unbind_all(None)
            key_entry.destroy()
    
    def create_loadout(self, widget, name, gestures, keys):
        # convert the data into dictionary
        gesture_map = {}
        for gesture, key in zip(gestures, keys):
            gesture_name = gesture.get()
            key_name = key["text"]
            gesture_map[gesture_name] = key_name
        # clear the data
        gestures.clear()
        keys.clear()    
        # close the popup
        widget.destroy()
        # create a record of the new loadout in the controller
        self.controller.create_loadout(name=name, data=gesture_map)
        self.update_display(self.controller.get_dictionaries())
        # update the scrollregion
        self.canvas.after(10, self.on_canvas_configure)
    
    def rename_selected(self):
        # exit if nothing is selected yet 
        if self.selected_id < 0 : return
        
        # get the currently selected frame and its label name
        selected_frame = self.frame.winfo_children()[self.selected_id]
        name_label = self.loadout_name_labels[self.selected_id]
        
        # check if the label is mapped
        if name_label.winfo_ismapped():     # unmap the label and create a new entry widget
            name_label.grid_forget()
            self.entry = tk.Entry(selected_frame)
            self.entry.insert(0, name_label.cget("text"))
            self.entry.grid(column=0, row=0, padx=1, sticky="news", columnspan=2)
            # bind the enter key to the entry
            self.entry.bind("<Return>", lambda _: self.rename_loadout())
        else: 
            # update the new name of the loadout
            self.controller.rename_loadout(self.selected_id, self.entry.get())
            # map the label with the updated text
            name_label.config(text=self.entry.get())
            name_label.grid(column=0, row=0, padx=1, sticky="news", columnspan=2)
            # destroy the entry widget
            if hasattr(self, 'entry') and self.entry.winfo_exists():
                self.entry.unbind_all(None)
                self.entry.destroy()
            # update the loadout display 
            self.update_display(self.controller.get_dictionaries())

    def remove_selected(self):
        # exit if nothing is selected yet 
        if self.selected_id < 0 : return
        
        # ask user for confirmation
        result = messagebox.askyesno("Confirmation", "Are you sure you want to delete this loadout?")
        if result:
            # remove the selected loadout from the list
            self.controller.remove_loadout(self.selected_id)
            # update the display with the new list
            new_loadouts = self.controller.get_dictionaries()
            self.update_display(new_loadouts)
    
    def loadout_select_handler(self, id, loadout_name):
        def handler(event):
            # save the selected information
            self.selected_name = loadout_name
            self.selected_id = id
            
            # reset the frames appearance
            for child in self.frame.winfo_children():
                child.configure(bg="yellow")
            
            # hightlight the selected frame
            selected_frame = self.frame.winfo_children()[id]
            selected_frame.config(bg="brown")
            
            # update enable button base on the enabled loadout name
            if self.controller.enabled.name == loadout_name:
                self.enable_btn.config(text="Enabled!", state=tk.DISABLED)
                selected_frame.config(bg="orange")
            else:
                self.enable_btn.config(text="Enable", state=tk.NORMAL)
            
            print(f"Selected frame #{id}, with name: {loadout_name}")    
        return handler
    
    def import_loadout(self):
        self.controller.import_loadout_from_file()
        self.update_display(self.controller.get_dictionaries())
        
    def export_loadout(self):
        for loadout in self.controller.loadouts:
            if self.selected_name.casefold() in loadout.name.casefold():
                self.controller.export_loadout_to_file(loadout)

    def set_camera_display(self, camera):
        # set reference to the camera
        self.controller.set_camera_display(camera)
        # enable default loadout
        self.controller.enable_default_loadout()
        # select the 1st item in the loadout list
        self.loadout_select_handler(0, self.controller.loadouts[0].name)(None)
        # disable the enable button
        self.enable_btn.config(text="Enabled!", state=tk.DISABLED)

    def set_config(self, config):
        self.controller.set_config(config)
    
    def get_current_loadout(self):
        return self.controller.get_currently_enabled()

# ====================================== CONTROLLER ======================================
class LoadoutController():
    def __init__(self):
        # declaring variables
        self.loadouts = []
        self.filenames = []
        self.enabled = None
        # create a references
        self.cam_display = None
        self.cfg = None
        
        # import all loadouts from a folder
        self.load_loadouts_from_folder("Loadout_Info")
    
    def create_loadout(self, name, data):
        new_loadout = Loadout(name=name, gestures_map=data)
        self.loadouts.append(new_loadout)
    
    # append a loadout obj
    def add_loadout(self, loadout):
        self.loadouts.append(loadout)
    
    def find_loadout(self, search_txt):
        # initializing an empty dictionary
        found = {}
        # start searching by the loadout name
        for loadout in self.loadouts:
            if search_txt.casefold() in loadout.name.casefold():
                found[loadout.name] = loadout.get_all_pairs()
        # returns a dictionary of found loadout
        return found
    
    def enable_loadout(self, id=None):
        if id is not None:
            self.enabled = self.loadouts[id]
        else: 
            print("Which to enable???")
            return
        
        if self.cam_display is not None: 
            # get the dictionary from the loadout obj
            self.cam_display.set_loadout(self.enabled.get_all_pairs())
        print(f"Enabled loadout: {self.enabled.name}!")
    
    def enable_default_loadout(self):
        #self.enable_loadout(next(iter(self.loadouts)))
        self.enable_loadout(0)
        
    def rename_loadout(self, id, new_name):
        self.loadouts[id].name = new_name
    
    def remove_loadout(self, id):
        self.loadouts.pop(id)
    
    def set_camera_display(self, camera):
        self.cam_display = camera
    
    def set_config(self, config):
        self.cfg = config

    def get_currently_enabled(self):
        # returns a dictionary of the currently enabled loadout obj
        return self.enabled
    
    def get_dictionaries(self):
        loadout_dicts = {}
        # convert list of loadout obj into dictionary
        for loadout in self.loadouts:
            loadout_dicts[loadout.name] = loadout.dictionary
        # returns dictionary
        return loadout_dicts
    
    def load_loadouts_from_folder(self, folder_name):
        contents, self.filenames = readFromFolder(folder_name)
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
            self.add_loadout(loadout)
    
    def import_loadout_from_file(self):
        # get data from a file
        str = readFromFile()
        # if file is empty return False
        if str == "" or str is None: return False
        
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
        
        self.add_loadout(loadout)
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
