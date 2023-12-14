import cv2
import mediapipe as mp

from mediapipe.tasks import python
import threading 

gesture_dict = {
    "Open_Palm": "test1",
    "Closed_Fist": "test2"
    }

#setup
num_hands = 2 
model_path = "hand_gesture_recognizer.task"
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def __result_callback(result, output_image, timestamp_ms):
        lock.acquire() # solves potential concurrency issues
        current_gestures.clear()
        if result is not None and any(result.gestures):
            print("Recognized gestures:")
            for single_hand_gesture_data in result.gestures:
                gesture_name = single_hand_gesture_data[0].category_name
                print(gesture_name)
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

# def identify_gesture(frame):
#         lock.acquire()
#         gestures = current_gestures
#         lock.release()
#         y_pos = 50
#         for hand_gesture_name in gestures:
#             # show the prediction on the frame
#             cv2.putText(frame, hand_gesture_name, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
#                                 1, (0,0,255), 2, cv2.LINE_AA)
#             y_pos += 50

#             if hand_gesture_name in gesture_dict:
#              cv2.putText(frame, gesture_dict[hand_gesture_name], (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
#                                 1, (0,255,0), 2, cv2.LINE_AA)
#             y_pos += 50


def detect(image, timestamp):
    # For webcam input:
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5) as hands:
      
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

          for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np_array)
            recognizer.recognize_async(mp_image, timestamp)
            #identify_gesture(image)
    
   
    return image

