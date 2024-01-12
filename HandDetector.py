import cv2
import mediapipe as mp

from mediapipe.tasks import python
import threading 
import Camera as cam
import ModelTrainer as MT

#setup
timestamp = 0
num_hands = 2 

#for recording
n_samples_save = 100
iteration_counter = 1
folder_counter = 1
X, y = [], []

idx_to_class = {
    0: 'open_palm',
    1: 'closed_fist',
    2: 'pointing_up',
}

gesture_map = {
    'open_palm': 0,
    'closed_fist': 1,
    'pointing_up': 2,
}

subdir = 'pointing_up'

# def __result_callback(result, output_image, timestamp_ms):
#         current_gestures.clear()
#         if result is not None and any(result.gestures):
#             #print("Recognized gestures:")
#             for single_hand_gesture_data in result.gestures:
#                 gesture_name = single_hand_gesture_data[0].category_name
#                 #print(gesture_name)
#                 current_gestures.append(gesture_name)

current_gestures = []
        
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

model_name_rf = 'model_rf__date_time_2024_01_13__03_52_28__acc_1.0__hand__oneimage.pkl'
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

        one_sample = []
        x = []

        if results.multi_hand_landmarks:
          global timestamp
          counter = 0
          current_timestamp = timestamp
          for res in results.multi_hand_landmarks:  
            counter += 1        
            mp_drawing.draw_landmarks(
                image,
                res,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())                                                       

            #RF model gesture prediction      
            for lm in res.landmark:
                x.extend([lm.x, lm.y])

            x = MT.np.array(x)  # 1D array of current landmark positions
            x = x[None, :]  # adds a new dimension to x to avoid input shape error
            yhat_idx = int(model.predict(x)[0])
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
                  
            if current_timestamp == timestamp and counter == 2:
                timestamp += 1
            elif counter > 2:
                print("3hand+ error")
                #if it detect 3 hands for some reason so it doesnt crash    

        #For RF model: extract keypoints from results
        if cam.Camera.record == True:
            global iteration_counter
            if iteration_counter < n_samples_save + 1:
                if results.multi_hand_landmarks:
                    for res in results.multi_hand_landmarks:  
                        for lm in res.landmark:    
                            one_sample.extend([lm.x, lm.y])

                        global X
                        global y
                        X.append(one_sample)
                        y.append(gesture_map[subdir])

                if iteration_counter == n_samples_save:
                    X = cam.np.array(X)
                    y = cam.np.array(y)
                    print(X.shape)
                    print(y.shape)
                    cam.np.savez(cam.os.path.join(cam.Camera.rec_folder_path, f'data_{subdir}.npz'), X=X, y=y)
                    print(f'Landmarks for category {subdir} saved.')
                    cam.Camera.record = False

            iteration_counter += 1
            print(iteration_counter)               
        
    return image

