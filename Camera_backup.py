import tkinter as tk
from tkinter import font
import cv2 as cv
from PIL import Image, ImageTk
import requests
import numpy as np 
import imutils 
import os
from pynput import keyboard
from datetime import datetime

import HandDetector as DT
import ModelTrainer as MT
import KeyboardInput as KeyInput

class Camera:
    timestamp = 0
    gestures = list

    #For ip webcam
    use_ip_webcam = False 
     #Replace the below URL with your own. Make sure to add "/shot.jpg" at last. 
    url = "https://192.168.1.78:8080/shot.jpg"

    #For hand landmark recording
    record_hotkey = keyboard.Key.f12
    build_hotkey = keyboard.Key.f11
    record = False                      
    start_time = ''
    rec_folder_path = ""     # specify which hand gesture directory to save the landmark arrays
    #sub_dir = "test_gesture" 

    def __init__(self, window, _width, _height):
        # Initialize variables
        self.window = window

        # Create a canvas to display the camera feed
        self.canvas = tk.Canvas(window, width=_width, height=_height)
        self.canvas.pack()
        # Create a label to display detected gesture
        custom_font = font.Font(size=14)
        self.text = tk.Label(window, text="Gesture Display", font=custom_font)
        self.text.pack(ipadx=3)

        self.controller = GestureDetectionController()

        # Open the camera
        if Camera.use_ip_webcam == False :
            self.cap = cv.VideoCapture(0)  # 0 for default camera, adjust if needed

        #Listener for keyboard input
        keyboard_listener = keyboard.Listener(
            on_press=Camera.keyboard_input_update)
        keyboard_listener.start()

        # Call the update method to continuously update the canvas with new frames
        self.update()

    def update(self):
        # Read a frame from the camera
        if Camera.use_ip_webcam == False:
            ret, frame = self.cap.read()
        else:
            requests.packages.urllib3.disable_warnings() 
            img_resp = requests.get(Camera.url, verify=False) 
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
            frame = cv.imdecode(img_arr, -1) 
            frame = imutils.resize(frame, width=480, height=280)
            ret = True
             
        if ret:
            # Flip the frame horizontally (mirror effect)
            mirrored_frame = cv.flip(frame, 1)
            detection = DT.detect(mirrored_frame)
            DT.timestamp += 1 # should be monotonically increasing, because in LIVE_STREAM mode
            # Convert the OpenCV frame to a Tkinter-compatible photo image
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(detection, cv.COLOR_BGR2RGB)))
          
            # Update the canvas with the new photo image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
            # Update the label text with the detected hand gestures
            #global gestures
            self.detected_gestures = DT.current_gestures
            label_txt = "No gestures detected."
            if len(self.detected_gestures) == 1:
                label_txt = f"{self.detected_gestures[0]}"
            elif len(self.detected_gestures) > 1:
                label_txt = ", ".join(self.detected_gestures)
            else:
                label_txt = "No gestures detected."
            self.text.configure(text=label_txt)     

        # Schedule the update method to be called after a delay (e.g., 10 milliseconds)
        self.window.after(5, self.update) 
        self.window.after(5, self.gesture_input_update) 

    def keyboard_input_update(key):
        if key == Camera.record_hotkey:
            Camera.start_landmark_recording()
        elif key == Camera.build_hotkey:
            MT.ModelTrainer.preprocess_data()
    
    def gesture_input_update(self):
        self.controller.gesture_to_input(self.detected_gestures)

    def close(self):
        # Release the camera and close the application
        self.cap.release()
        self.window.destroy()
        
    def set_loadout(self, loadout):
        self.controller.set_loadout(loadout)

    def start_landmark_recording():
        if Camera.record == False:
                now = datetime.now()
                Camera.start_time = now.strftime("%d_%m_%Y_%H_%M_%S")
                Camera.rec_folder_path = os.path.join(os.getcwd(), "Recorded_Data", f"recording_{Camera.start_time}")
                os.mkdir(Camera.rec_folder_path)
                Camera.record = True
                print("Recording started")

class GestureDetectionController:
    def __init__(self):
        self.loadout = {}
     
    def set_loadout(self, loadout):
        self.loadout = loadout
        
    def gesture_to_input(self, detected):
        # check if the loadout is empty
        if len(self.loadout) < 1: return
        # check if the detected gesture list is empty
        if len(detected) < 1: return
        
        # loop through the detected gestures and translate them to key input
        for gesture in detected:
            # check if the gesture is part of the loadout
            if gesture in self.loadout:
                # check if the key is release
                if self.loadout[gesture].casefold() == "Release".casefold():
                    KeyInput.ReleaseAllKeys(self.loadout.values())
                    continue
                # press all key detected otherwise
                KeyInput.PressKey(self.loadout[gesture])
        