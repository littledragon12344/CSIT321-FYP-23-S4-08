
import os
from datetime import datetime

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

# current model file path
model_name_rf = 'rf_model_2024_01_29__21_08_24.pkl'
current_model_path = os.path.join(model_folder_path, model_name_rf)

def __init__():
    print("Initalize program settings")
    # read from gesture file and fill array here
    counter = 0
    
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

def update_gesture_labels():
     # placeholder
     return