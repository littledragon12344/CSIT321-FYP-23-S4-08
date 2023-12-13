import tkinter as tk

class LoadoutDisplay():
    def __init__(self, frame, width, height):
        self.root = frame
        self.width = width
        self.height = height
        self.create_widgets()

    def create_widgets(self):
        # create a canvas for list display
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(side="left", fill="both", expand=True, padx=2)

        # create a vertical scrollbar and attach it to the LoadoutDisplay frame
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        
        # config the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # create a frame to contain the widgets within the canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # add some sample items to the frame
        for i in range(30):
            item_frame = tk.Frame(self.frame, bg="yellow", pady=2, padx=2)
            item_frame.pack(fill="x", expand=True, padx=2, pady=2)

            label = tk.Label(item_frame, text=f"Item {i + 1}")
            label.grid(column=0, row=i, padx=2, sticky="news")

            label = tk.Label(item_frame, text=f"Label {i + 1}")
            label.grid(column=1, row=i, padx=2, sticky="news")

            button = tk.Button(item_frame, text="Click Me")
            button.grid(column=2, row=i, padx=2, sticky="news")
            
        # update the scrollregion
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
