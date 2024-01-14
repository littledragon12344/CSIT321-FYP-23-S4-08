import cv2
import mediapipe as mp

from mediapipe.tasks import python
import Camera as cam
import ModelTrainer as MT

#setup
timestamp = 0 
current_gestures = []
num_hands = 2 

#Current issues: 
# - Inaccuracy (likely just due to the small dataset)
# - gesture recognition only works for the hand used in the recording
#TO DO: 
# - Refactor landmark extraction to a separate class
# - try adding the z-coordinates
# - implementing other algos and benchmarking performance
# - improve on them???

#For landmark extraction
sample_frame_count = 100 #total number of frames to save during recording
iteration_counter = 1
recorded_gesture_class = 'thumbs_down' #current gesture being recorded
X, y = [], [] 

gesture_map = {
    'open_palm': 0,
    'closed_fist': 1,
    'pointing_up': 2,
    'thumbs_down': 3
}

idx_to_class = {
    0: 'open_palm',
    1: 'closed_fist',
    2: 'pointing_up',
    3: 'thumbs_down',
}
        
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

model_name_rf = 'model_rf__date_time_2024_01_13__15_36_25_acc_1.0.pkl'
model = MT.joblib.load(model_name_rf)

def detect(image):
    # For webcam input:
    with mp_hands.Hands(
        model_complexity=0,
        static_image_mode=False,
        max_num_hands=num_hands,
        min_detection_confidence=0.4,
        min_tracking_confidence=0.4) as hands:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        

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
            
                hand_landmark_array = MT.np.array(hand_landmark_array)  # 1D array of current landmark positions
                hand_landmark_array = hand_landmark_array[None, :]  # adds a new dimension to x to avoid input shape error
                yhat_idx = int(model.predict(hand_landmark_array)[0]) #The estimated or predicted values in a regression or other predictive model are termed the y-hat values
                yhat = idx_to_class[yhat_idx]
                print(yhat)    
            #For LSTM: extract keypoints from results
            # if cam.Camera.record == True:
            #     global iteration_counter
            #     iteration_counter += 1
            #     for lm in res.landmark:
            #         recorded_landmarks = cam.np.array([lm.x, lm.y, lm.z]).flatten()
            #         npy_path = cam.os.path.join(cam.Camera.rec_folder_path, f"frame_{iteration_counter}")      
            #         cam.np.save(npy_path, recorded_landmarks)
            #         print(recorded_landmarks)                 

        #For RF model: extract keypoints from results
        if cam.Camera.record == True:
            one_sample = []
            global iteration_counter
            if iteration_counter < sample_frame_count + 1:
                if results.multi_hand_landmarks:
                    for res in results.multi_hand_landmarks:  
                        for lm in res.landmark:    
                            one_sample.extend([lm.x, lm.y])

                        global X
                        global y
                        X.append(one_sample)
                        y.append(gesture_map[recorded_gesture_class])

                if iteration_counter == sample_frame_count:
                    X = cam.np.array(X)
                    y = cam.np.array(y)
                    print(X.shape)
                    print(y.shape)
                    cam.np.savez(cam.os.path.join(cam.Camera.rec_folder_path, f'data_{recorded_gesture_class}_{cam.Camera.start_time}.npz'), X=X, y=y)
                    print(f'Landmarks for category {recorded_gesture_class} saved.')
                    cam.Camera.record = False

            iteration_counter += 1
            print(iteration_counter)               
        
    return image

