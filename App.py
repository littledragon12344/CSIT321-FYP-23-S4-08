import tkinter as tk
from pynput import keyboard
import Camera as cam
import Config as cfg
import Loadout as lo

loadout_widget = None
current_loadout = None
config = None
cfgwidget = None

def new_window():     
    def export_loadout():
        if loadout_widget is None: return
        loadout_widget.export_loadout()
        
    def import_loadout():
        if loadout_widget is None: return
        loadout_widget.import_loadout()

    def create_loadout():
        if loadout_widget is None: return
        loadout_widget.create_loadout_popup()

    def update_gui():
        global config
        if config:
            config.destroy()  # Destroy the existing Config frame
        config = tk.Frame(base, width=800, height=275, bg="blue")  # Recreate the Config frame
        cfgwidget = cfg.Config(config, loadout_widget, pop_up, update_gui)  # Pass the update_gui function
        cfgwidget.set_loadout(loadout_widget)  # Pass the LoadoutDisplay instance directly
        config.grid(column=0, row=2, columnspan=5, rowspan=2, sticky="news")  # Grid the new Config frame

    def start_build_model():
        if cfgwidget is None: return
        # create popup
        popup = tk.Toplevel(root)
        popup.title("Build model")
        popup.geometry("300x50")
        popup.resizable(width=False, height=False)
        # add a label
        msg = tk.Label(popup, text="Building your model...\nPlease wait...")
        msg.pack(expand=True, fill="both", anchor="center")
        # force gui to update
        root.update()
        # start build model after a delay
        popup.after(2000, cfgwidget.build_model())
        # destroy popup after finish
        popup.after(3000, popup.destroy)

    def pop_up(title_text: str):
        top = tk.Toplevel(root)
        top.geometry("400x200")
        top.geometry(f"+{root.winfo_x()+200}+{root.winfo_y()+200}")
        top.title(title_text)
        top.resizable(width=False, height=False)
        return top

    root = tk.Tk()
    root.title("Gesture Detection Prototype")
    root.geometry("800x800")    
    root.resizable(width=False, height=False)
    
    #label = tk.Label(root, text="Created by group CSIT321-FYP-23-S4-08")
    #label.pack()

    #======================== MENU BAR ========================
    # creates a new menu bar
    menubar = tk.Menu(root)
    
    # file menu items
    file_menu = tk.Menu(menubar, tearoff=0)
    # loadout creation
    file_menu.add_command(label="New loadout...", command=create_loadout)
    # loadout import/export
    file_menu.add_separator()
    file_menu.add_command(label="Import a loadout", command=import_loadout)
    file_menu.add_command(label="Export a loadout", command=export_loadout)
    # exit from app
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # options menu items
    options_menu = tk.Menu(menubar, tearoff=0)
    # tutorial
    options_menu.add_command(label="Start tutorial...")
    # build model 
    options_menu.add_command(label="Build a model", command=start_build_model)

    # display the options on the menu bar
    menubar.add_cascade(label="File", menu=file_menu)
    menubar.add_cascade(label="Options", menu=options_menu)
    # set menu bar for the main window
    root.config(menu=menubar)
    #==========================================================
    
    #======================== UI LAYOUT ========================
    # create a base frame for the layout
    base = tk.Frame(root)
    # create a frame to contain the camera
    camera = tk.Frame(base, width=480, height=280, bg="green")
    # get the camera feed for the frame 
    cam_display = cam.Camera(camera, 466, 305)

    # create a frame for the loadout display
    loadout_display = tk.Frame(base, borderwidth=1, relief="solid", bg="red")
    loadout_widget = lo.LoadoutDisplay(loadout_display, 302, 280, update_gui)
    # set the reference of the camera to the loadout
    loadout_widget.set_camera_display(cam_display)
    
    # create a frame for the gesture list display
    config = tk.Frame(base, width=800, height=475, bg="blue")
    cfgwidget = cfg.Config(config, loadout_widget, pop_up, update_gui)
    cfgwidget.set_loadout(loadout_widget)
    
    # placing the frames onto a grid for the UI layout
    base.grid(column=0, row=0, sticky="news")
    camera.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="news")
    loadout_display.grid(column=3, row=0, columnspan=2, rowspan=2, sticky="news")
    config.grid(column=0, row=2, columnspan=5, rowspan=4, sticky="news")
    #===========================================================

    # start the window
    root.mainloop()

new_window()