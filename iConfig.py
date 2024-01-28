import tkinter as tk
import keyboard as kb
from PIL import Image, ImageTk

class iConfig(object):

    def __init__(self, target, picture, name, inp, pop):
        self.target = target
        self.picture = picture # image is already resized in config
        self.name = name
        self.inp = inp
        
        self.pop = pop
        self.pop_win = None

        cleaned = self.name.replace("_", " ")

        # Create frame for each configuration object
        self.base = tk.Frame(self.target, width=130, height=200, bg="green")

        imgfr = tk.Frame(self.base, width=120, height=120)
        img = tk.Label(imgfr, image=self.picture)
        img.image=self.picture

        textfr = tk.Frame(self.base, width=130, height=40)
        text = tk.Label(self.base, text=cleaned.upper(), bg="white")

        choicefr=tk.Frame(self.base, width=130, height=40)
        choice = tk.Button(self.base, text=self.inp.upper(), command=self.change_input, bg="grey")

        self.base.grid(column=0, row=0, padx=5, pady=5)
        imgfr.grid(column=0, row=0, padx=5, pady=5)
        img.grid(column=0, row=0)
        textfr.grid(column=0, row=1)
        text.grid(column=0, row=1, sticky=("N", "S", "E", "W"))
        choicefr.grid(column=0, row=2)
        choice.grid(column=0, row=2, sticky=("N", "S", "E", "W"))
        
    def change_input(self):
        # Create popup
        
        # Get input value
        # val = kb.wait()
        # self.inp = val
        print("This button is working.")