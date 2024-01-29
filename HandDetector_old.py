import cv2
import mediapipe as mp

from mediapipe.tasks import python
import Camera as cam
import ModelTrainer as MT
import ProgramSettings as PS

#Current issues: 
# - Inaccuracy (likely just due to the small dataset)
#TO DO: 
# - try adding the z-coordinates
# - algo optimization
# - Front end for gesture creation and model training

#Setup
timestamp = 0 
current_gestures = []
num_hands = 2 
pred_threshold = 0.5
    
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#For landmark extraction
recorded_frame_count = 100 #total number of frames to save during recording
recorded_gesture_class = 'pointing_up' #current gesture being recorded
X, y = [], []
iteration_counter = 1

#For benchmarking prediction
e_counter = 0
total_e = 0.0

gesture_map = {
    'open_palm': 0,
    'closed_fist': 1,
    'pointing_up': 2,
    'thumbs_down': 3
}

idx_to_string = {
    0: 'Open_Palm',
    1: 'Closed_Fist',
    2: 'Pointing_Up',
    3: 'Thumb_Down',
}

#Load ML model
model_name_rf = 'model_rf__date_time_2024_01_17__16_11_06_acc_1.0.pkl'
model = MT.joblib.load(model_name_rf)

def detect(image):
    global recorded_gesture_class

    # For webcam input:
    with mp_hands.Hands(
        model_complexity=0,
        static_image_mode=False,
        max_num_hands=num_hands,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        # To improve performance, optionally mark the image as 
        # not writeable to pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        current_gestures.clear()

        if results.multi_hand_landmarks:
            counter = 0
            for res in results.multi_hand_landmarks:  
                counter += 1
                hand_landmark_array = []        
                mp_drawing.draw_landmarks(
                    image,
                    res,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                #RF model gesture prediction      
                for lm in res.landmark:
                    hand_landmark_array.extend([lm.x, lm.y])         

                predict(hand_landmark_array) 
 
            #For RF model: extract keypoints from results
            if cam.Camera.record == True:
                one_sample = []
                global iteration_counter
                if iteration_counter < recorded_frame_count + 1:
                    if results.multi_hand_landmarks:
                        for res in results.multi_hand_landmarks:  
                            for lm in res.landmark:    
                                one_sample.extend([lm.x, lm.y, lm.z])

                            global X
                            global y
                            X.append(one_sample)
                            y.append(gesture_map[recorded_gesture_class])

                    if iteration_counter == recorded_frame_count:
                        X = cam.np.array(X)
                        y = cam.np.array(y)
                        print(X.shape)
                        print(y.shape)
                        cam.np.savez(cam.os.path.join(cam.Camera.rec_folder_path, f'data_{recorded_gesture_class}_{cam.Camera.start_time}.npz'), X=X, y=y)
                        print(f'Landmarks for category {recorded_gesture_class} saved.')
                        cam.Camera.record = False

                iteration_counter += 1
                print(iteration_counter)               
            #===============================================================#
        
    return image

def predict(array):
    #start = time.perf_counter() # For benchmarking execution time

    hand_landmark_array = MT.np.array(array) # 1D array of current landmark positions
    hand_landmark_array = hand_landmark_array[None, :]     # adds a new dimension to x to avoid input shape error
    #global e_counter, total_e

    #yhat = model.predict(hand_landmark_array)             # The estimated or predicted values in a regression or
                                                           # other predictive model are termed the y-hat values  
    yhat_preds = model.predict_proba(hand_landmark_array)
    print(model.classes_) 

    yhat_idx = -1
    yhat_prob = 0.0
    counter = 0
    
    # note:if the order of the gestures saved is changed the model will need to be retrained
    for pred_prob in yhat_preds[0]:  
        if pred_prob > pred_threshold and pred_prob > yhat_prob:
            yhat_idx = counter
            yhat_prob = pred_prob
        counter += 1


    #yhat_idx = yhat[0]
    if yhat_idx >= 0:
        gesture = idx_to_string[yhat_idx]                                                             
        current_gestures.append(gesture)    

    #e_counter += 1
    #total_e += time.perf_counter() - start
    #print("Average prediction time:", (total_e / e_counter))

def GestureName_Record(NameChange):# change the Name
    global recorded_gesture_class
    print(f"Changed {recorded_gesture_class} to {NameChange}")
    recorded_gesture_class = NameChange 

