import tkinter as tk
import keyboard as kb
from PIL import Image, ImageTk

class iConfig(object):

    def __init__(self, target, picture, name, inp, config, pop):
        self.target = target
        self.picture = picture # image is already resized in config
        self.name = name
        self.inp = inp
        
        self.config = config
        self.pop = pop
        self.pop_win = None
        self.val = None

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
        global tButton
        global tInput

        print(self.inp)

        if self.pop:
            self.pop_win = self.pop("Change Keys")
            tFrame = tk.Frame(self.pop_win)
            tLabel = tk.Label(tFrame, width=40, text="Click on the button to change the key")
            tInput = tk.Text(tFrame, height=1, width=5)
            tInput.insert(tk.INSERT, self.inp.upper())
            tInput.config(state="disabled")
            tButton = tk.Button(tFrame, text="Change", command=self.button_trigger)
            tConfirm = tk.Button(tFrame, text="Confirm", command=self.confirm_trigger)
            tFrame.grid(column=0, row=0, sticky="news")
            tLabel.grid(column=0, row=0, sticky="news")
            tInput.grid(column=0, row=1, sticky="news")
            tButton.grid(column=0, row=2, sticky="news")
            tConfirm.grid(column=0, row=3, sticky="news")
    
    def button_trigger(self):
        self.change_key()
        self.read_input()
    
    def confirm_trigger(self):
        self.config.update_key(self.name, self.inp, self.val)
        if self.pop_win:
            self.pop_win.destroy()
    
    def change_key(self):
        tButton.config(text="Input your desired key")
        if self.pop_win:
            self.pop_win.update_idletasks()
    
    def read_input(self):
        self.val = kb.read_key()
        tInput.config(state="normal")
        tInput.delete('1.0', tk.END)
        tInput.insert(tk.INSERT, self.val.upper())
        tInput.config(state="disabled")
        tButton.config(text="Change")