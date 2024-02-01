
import os
from datetime import datetime
import pickle
import FileManager as FM

#TO DO: 
# - save/load from file
# - gesture images

#gesture recognition
#'Open_Palm', 'Closed_Fist', 'Victory', 'Pointing_Up', 'Thumbs_Up', 'Thumbs_Down'
allowed_gestures = []
                    
# folder paths
data_folder_path = os.path.join(os.getcwd(), "Datasets")
model_folder_path = os.path.join(os.getcwd(), "Models")
image_folder_path = os.path.join(os.getcwd(), "Gesture_Images")
# landmark extraction settings
recorded_frame_count = 100 # total number of frames to save during recording
recorded_gesture_class = '' # current gesture being recorded

# ML model settings
model_name_rf = 'rf_model_2024_02_01__20_33_32.pkl'
current_model_path = os.path.join(model_folder_path, model_name_rf)

def __init__():
    print("Initalize program settings")
    #save_gesture_file()
    load_gesture_file()
    print(allowed_gestures)
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
    global allowed_gestures
    allowed_gestures.append(name)
    save_gesture_file()
    return

def delete_gesture(name):
    # global allowed_gestures
    # allowed_gestures.append(name)
    # save_gesture_file()
    return

def load_gesture_file():
    with open('gestures.pkl', 'rb') as f:
        global allowed_gestures
        allowed_gestures = pickle.load(f)

def save_gesture_file():
    with open('gestures.pkl', 'wb') as f: 
        print(allowed_gestures)
        pickle.dump(allowed_gestures, f)
        f.close()


     