import cv2
import mediapipe as mp

from mediapipe.tasks import python
import Camera as cam
import ModelTrainer as MT
import ProgramSettings as PS

#Setup
current_gestures = []
hand_array = [None] * 2
num_hands = 2 
pred_threshold = 0.5
    
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#For landmark extraction
iteration_counter = 0
X, y = [], []

#For benchmarking predictions
e_counter = 0
total_e = 0.0

#Load ML model
model = MT.joblib.load(PS.current_model_path)

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
        og_image = image
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
                hand_landmark_array = []
                mp_drawing.draw_landmarks(
                    image,
                    res,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                #RF model gesture prediction      
                for lm in res.landmark:
                    hand_landmark_array.extend([lm.x, lm.y, lm.z])         

                predict(hand_landmark_array)
 
                hand_array[counter] = results.multi_handedness[counter].classification[0].label    

                counter += 1 
 
            #RF model: extract keypoints from results
            if cam.Camera.record == True:
                global X
                global y
                one_sample = []
                global iteration_counter
                if iteration_counter < PS.recorded_frame_count:
                    iteration_counter += 1
                    print(iteration_counter)  
                    if results.multi_hand_landmarks:
                        for res in results.multi_hand_landmarks:  
                            for lm in res.landmark:    
                                one_sample.extend([lm.x, lm.y, lm.z])

                            X.append(one_sample)
                            y.append(PS.recorded_gesture_class)

                    if iteration_counter == PS.recorded_frame_count:
                        np_x = cam.np.array(X)
                        np_y = cam.np.array(y)
                        print(np_x.shape)
                        print(np_y.shape)
                        cam.np.savez(PS.os.path.join(PS.data_folder_path, PS.recorded_gesture_class, f'data_{PS.recorded_gesture_class}_{PS.get_datetime()}.npz'), X=np_x, y=np_y)
                        cv2.imwrite(PS.os.path.join(PS.image_folder_path, f'{PS.recorded_gesture_class}.png'), og_image)
                        print(f'Landmark data for label {PS.recorded_gesture_class} saved.')
                        X = []
                        y = []
                        cam.Camera.record = False
                        iteration_counter = 0                           
            #===============================================================#
        
    return image

def predict(array):
    #==Benchmark==
    #start = time.perf_counter() 
    #global e_counter, total_e
    #==Benchmark==

    hand_landmark_array = MT.np.array(array) # 1D array of current landmark positions
    hand_landmark_array = hand_landmark_array[None, :]     # adds a new dimension to x to avoid input shape error

    yhat_preds = model.predict_proba(hand_landmark_array)  # The estimated or predicted values in a regression or
                                                           # other predictive model are termed the y-hat values  
    yhat_idx = -1
    yhat_prob = 0.0
    counter = 0
    print(yhat_preds)
    for pred_prob in yhat_preds[0]:  
        if pred_prob > pred_threshold and pred_prob > yhat_prob:
            yhat_idx = counter
            yhat_prob = pred_prob
        counter += 1

    if yhat_idx >= 0:
        gesture = model.classes_[yhat_idx]                                                             
        current_gestures.append(gesture)    

    #==Benchmark==
    #e_counter += 1
    #total_e += time.perf_counter() - start
    #print("Average prediction time:", (total_e / e_counter))
    #==Benchmark==
        
def reload_model():
    global model
    model = MT.joblib.load(PS.current_model_path) 



