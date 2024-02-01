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

        buttonfr=tk.Frame(self.base, width=130, height=40)
        b_input = tk.Button(buttonfr, text=self.inp.upper(), command=self.change_input, bg="grey")
        b_delete = tk.Button(buttonfr, text="DEL", command=self.delete_prompt, bg="grey")

        self.base.grid(column=0, row=0, padx=5, pady=5)
        imgfr.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
        img.grid(column=0, columnspan=2, row=0)
        textfr.grid(column=0, row=1, columnspan=2)
        text.grid(column=0, row=1, columnspan=2, sticky="news")
        buttonfr.grid(column=0, row=2, columnspan=2)
        buttonfr.columnconfigure(0, weight=1, minsize=65)
        buttonfr.columnconfigure(1, weight=1, minsize=65)
        b_input.grid(column=0, row=2, sticky="news")
        b_delete.grid(column=1, row=2, sticky="news")
        
    def change_input(self):
        global tButton
        global tInput

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
    
    def delete_prompt(self):
        if self.pop:
            self.pop_win = self.pop("Delete Confirmation")
            tFrame = tk.Frame(self.pop_win, width=400, height=200)
            tFrame.pack_propagate(False)
            tEmpty = tk.Label(tFrame, height=3)
            tEmpty2 = tk.Label(tFrame)
            tLabel = tk.Label(tFrame, width=55, text="Are you sure you want to delete this config?")
            tConfirm = tk.Button(tFrame, text="Confirm", command=self.delete_input)
            tCancel = tk.Button(tFrame, text="Cancel", command=self.pop_win.destroy)
            tFrame.grid(column=0, row=0)
            tEmpty.grid(column=0, row=0, columnspan=5)
            tLabel.grid(column=0, row=1, columnspan=5, sticky="news")
            tEmpty2.grid(column=0, row=2, columnspan=5)
            tConfirm.grid(column=1, row=3)
            tCancel.grid(column=3, row=3)

            for i in range(5):
                tFrame.columnconfigure(i, weight=1)
                tFrame.rowconfigure(i, weight=1)
        
    def delete_input(self):
        self.config.update_key(self.name)
        self.pop_win.destroy()
        return