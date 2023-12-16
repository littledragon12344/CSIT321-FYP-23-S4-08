import tkinter as tk

# loadout display class
class LoadoutDisplay():
    def __init__(self, frame, width, height):
        # saving the frame and its dimension
        self.root = frame
        self.width = width
        self.height = height
        
        # initializing values
        self.selected = -1
        
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
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # add some sample items to the frame
        for i in range(30):
            # create a frame for the item
            item_frame = tk.Frame(self.frame, bg="yellow", pady=2, padx=2)
            item_frame.pack(fill="x", expand=True, padx=2, pady=2)
            # bind mouse event to the frame
            item_frame.bind("<Button-1>", self.loadout_select_handler(i))

            label = tk.Label(item_frame, text=f"Item {i + 1}")
            label.grid(column=0, row=i, padx=2, sticky="news")

            label = tk.Label(item_frame, text=f"Label {i + 1}")
            label.grid(column=1, row=i, padx=2, sticky="news")

            button = tk.Button(item_frame, text="Click Me")
            button.grid(column=2, row=i, padx=2, sticky="news")
            
        # update the scrollregion
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    def search_loadout(self):
        # getting the input text
        search_txt = self.searchbar.get("1.0", "end-1c")
        print(f"Searched for {search_txt} loadout!")
    
    def enable_loadout(self, id):
        print(f"Enabled {id} loadout!")
    
    def disable_loadout(self, id):
        print(f"Disabled {id} loadout!")
        
    def loadout_select_handler(self, id):
        def handler(event):
            # reset the frames appearance
            for child in self.frame.winfo_children():
                child.configure(bg="yellow")
            
            # hightlight the selected frame
            selected_frame = self.frame.winfo_children()[id]
            selected_frame.config(bg="brown")
            
            self.selected = id
            print(f"Selected frame #{id}")    
        return handler
        
# loadout item class
class Loadout():
    pass