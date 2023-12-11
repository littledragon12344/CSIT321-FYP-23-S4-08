import tkinter as tk
import Camera as cam
import Config as cfg

def new_window(): 
    root = tk.Tk()
    root.title("Gesture Detection Prototype")
    root.geometry("800x800")
    
    #label = tk.Label(root, text="Created by group CSIT321-FYP-23-S4-08")
    #label.pack()
    
    #======================== MENU BAR ========================
    # creates a new menu bar
    menubar = tk.Menu(root)
    
    # file menu items
    file_menu = tk.Menu(menubar, tearoff=0)
    # 
    file_menu.add_command(label="New")
    # loadouts
    file_menu.add_separator()
    file_menu.add_command(label="Import loadouts")
    file_menu.add_command(label="Export loadouts")
    # exit from app
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # options menu items
    options_menu = tk.Menu(menubar, tearoff=0)
    # tutorial
    options_menu.add_command(label="Start tutorial...")
    
    # display the options on the menu bar
    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Options", menu=options_menu)
    # set menu bar for the main window
    root.config(menu=menubar)
    #==========================================================
    
    base = tk.Frame(root)
    camera = tk.Frame(base, width=480, height=400, bg="green")
    # get the camera feed for the frame
    cam.Camera(camera, 450, 320)
    #frame.place(x=25, y=22.5)
    
    catalog = tk.Frame(base, bg="red")

    config = tk.Frame(base, width=800, height=400, bg="blue")
    #frame.place(x=25, y=392.5)

    #cfg.Config(frame)
    
    base.grid(column=0, row=0, sticky=("N", "S", "E", "W"))
    camera.grid(column=1, row=1, columnspan=3, rowspan=2, sticky=("N", "S", "E", "W"))
    catalog.grid(column=4, row=1, columnspan=2, rowspan=2, sticky=("N", "S", "E", "W"))
    config.grid(column=1, row=3, columnspan=5, rowspan=2, sticky=("N", "S", "E", "W"))

    #root.columnconfigure(0, weight=1)
    #root.rowconfigure(0, weight=1)
    #base.columnconfigure(0, weight=1)
    #base.columnconfigure(1, weight=1)
    #base.columnconfigure(2, weight=1)
    #base.columnconfigure(3, weight=1)
    #base.columnconfigure(4, weight=1)
    #base.rowconfigure(0, weight=1)
    #base.rowconfigure(1, weight=1)
    #base.rowconfigure(2, weight=1)
    #base.rowconfigure(3, weight=1)

    root.mainloop()
    

new_window()
