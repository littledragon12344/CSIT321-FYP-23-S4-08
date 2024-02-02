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
    global tutorial_label
    def export_loadout():
        if loadout_widget is None: return
        loadout_widget.export_loadout()
        
    def import_loadout():
        if loadout_widget is None: return
        loadout_widget.import_loadout()

    def create_loadout():
        if loadout_widget is None: return
        loadout_widget.create_loadout_popup()
        
    tutorial_steps = [
        {"message": "Welcome to the Tutorial!", "highlight": None},
        {"message": "At the left is the loadout panel \nwhere you can view all your loadouts! -->", "highlight": None},
        {"message": "Press the search button --> \nto search for the loadout you want", "highlight": None},
        {"message": "Press the enable button ----------------> \nto enable and start using the selected loadout!", "highlight":None},
        {"message": "At the bottom is the configuration panel \nwhere you can add new gestures to your loadout! \nv", "highlight": None},
        {"message": "^ For creating a loadout:\nClick on file --> New loadout", "highlight": None},
        {"message": "^ For importing or exporting a loadout:\nClick on file --> Import or Export a loadout", "highlight": None},
        {"message": "Try doing an open palm hand gesture!", "highlight": None},
        {"message": "Tutorial complete! You're ready to use the application.", "highlight": None},
        {"message": "", "highlight": None}
    ]
    
    current_step = 0
    
    def start_tutorial():
        global tutorial_label, current_step
        current_step = 0
        tutorial_label = tk.Label(root, text="", font=("Helvetica", 14), fg="white", bg="grey")
        tutorial_label.place(x=450, y=100, anchor="center")
        
        root.bind("<Button-1>", show_tutorial_step)
    
    def show_tutorial_step(event):
        global current_step
        print(current_step)
        message = tutorial_steps[current_step]["message"]
        highlight_element = tutorial_steps[current_step]["highlight"]

        if current_step == 1:  # Check if it's the second message
            tutorial_label.place(x=250, y=100, anchor="center") 
        elif current_step == 2:
            tutorial_label.place(x=510, y=30, anchor="center")
        elif current_step == 3:
            tutorial_label.place(x=520, y=30, anchor="center")
        elif current_step == 4:
            tutorial_label.place(x=250, y=300, anchor="center")
        elif current_step == 5:
            tutorial_label.place(x=122, y=25, anchor="center")
        elif current_step == 6:
            tutorial_label.place(x=175, y=25, anchor="center")
        elif current_step == 7:
            tutorial_label.place(x=450, y=100, anchor="center")
        
        tutorial_label.config(text=message)
        current_step += 1
        if current_step < len(tutorial_steps):
            show_tutorial_step
        else:
            tutorial_label.destroy()
            root.unbind("<Button-1>")

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
    options_menu.add_command(label="Start tutorial...", command=start_tutorial)
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