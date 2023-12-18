import cv2
import mediapipe as mp

from mediapipe.tasks import python
import threading 

gesture_dict = {
    "Open_Palm": "test1",
    "Closed_Fist": "test2"
    }

#setup
timestamp = 0
num_hands = 2 
model_path = "hand_gesture_recognizer.task"
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def __result_callback(result, output_image, timestamp_ms):
        lock.acquire() # solves potential concurrency issues
        current_gestures.clear()
        if result is not None and any(result.gestures):
            #print("Recognized gestures:")
            for single_hand_gesture_data in result.gestures:
                gesture_name = single_hand_gesture_data[0].category_name
                #print(gesture_name)
                current_gestures.append(gesture_name)
        lock.release()

lock = threading.Lock()
current_gestures = []
options = GestureRecognizerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands = num_hands,
    result_callback=__result_callback)
        
recognizer = GestureRecognizer.create_from_options(options)
        
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

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
        np_array = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
        if results.multi_hand_landmarks:
          #print(timestamp)
          global timestamp
          counter = 0
          current_timestamp = timestamp
          for hand_landmarks in results.multi_hand_landmarks:  
            counter += 1        
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())  
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np_array)    
            if current_timestamp == timestamp and counter == 2:
                timestamp += 1
                recognizer.recognize_async(mp_image, timestamp) 
            elif counter > 2:
                print("3hand+ error")
                #if it detect 3 hands for some reason so it doesnt crash             
            else:
                recognizer.recognize_async(mp_image, timestamp)    
            
    return image

