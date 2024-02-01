
import os
from datetime import datetime

#TO DO: 
# - save/load from file
# - gesture images

#gesture recognition
allowed_gestures = ["Open_Palm", 
                    "Closed_Fist", 
                    "Victory", 
                    "Pointing_Up",
                    "Thumbs_Up",
                    "Thumbs_Down",
                    ]

# folder paths
data_folder_path = os.path.join(os.getcwd(), "Datasets")
model_folder_path = os.path.join(os.getcwd(), "Models")
image_folder_path = os.path.join(os.getcwd(), "Gesture_Images")
# landmark extraction settings
recorded_frame_count = 100 # total number of frames to save during recording
recorded_gesture_class = '' # current gesture being recorded

# ML model settings
model_name_rf = 'rf_model_2024_02_01__14_18_12.pkl'
current_model_path = os.path.join(model_folder_path, model_name_rf)

#gesture label file
gesture_file_path = ''

def __init__():
    print("Initalize program settings")
    # need to read from gesture file and fill array here
    counter = 0
    
    global recorded_gesture_class
    recorded_gesture_class = allowed_gestures[0]

    #incase the dataset folder doesn't exist
    if os.path.exists(data_folder_path) == False:
            os.makedirs(data_folder_path)

    for gesture in allowed_gestures:
        sub_dir_path = os.path.join(data_folder_path, gesture) 
        #if directory for gesture data does not exist, create it
        if os.path.exists(sub_dir_path) == False:
            os.makedirs(sub_dir_path)

def get_datetime():
    now = datetime.now()
    return now.strftime("%d_%m_%Y_%H_%M_%S")

def change_recorded_gesture(name):# change the Name
    global recorded_gesture_class
    print(f"Changed {recorded_gesture_class} to {name}")
    recorded_gesture_class = name 

def add_new_gesture(name):
     # placeholder
     return

def update_gesture_labels():
     # placeholder
     return