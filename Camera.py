import tkinter as tk
from tkinter import font
import cv2 as cv
from PIL import Image, ImageTk
import requests
import numpy as np 
import imutils 
from datetime import datetime

import HandDetector as DT
import ModelTrainer as MT
import KeyboardInput as KeyInput

import threading
from queue import Queue
import concurrent.futures

class Camera:
    detected_gestures = []

    #For ip webcam - would be nice to have a toggle for this on the UI
    use_ip_webcam = False 
     #Replace the below URL with your own. Make sure to add "/shot.jpg" at last. 
    url = "https://192.168.1.79:8080/shot.jpg"

    #For hand landmark recording
    record = False                      
    start_time = ''

    def __init__(self, window, _width, _height):
        # Initialize variables
        self.window = window
        DT.PS.__init__()
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

        # Call the update method to continuously update the canvas with new frames
        #self.update()

        # Create a thread-safe queue for frames
        self.frame_queue = Queue()

        # Create a thread for video processing
        self.video_thread = threading.Thread(target=self.update)
        self.video_thread.daemon = True
        self.video_thread.start()

        # Create multiple threads for frame processing
        self.processing_threads = []
        for _ in range(3):  # Adjust the number of threads as needed
            thread = threading.Thread(target=self.process_frames)
            thread.daemon = True
            self.processing_threads.append(thread)
            thread.start()

        # Create a thread pool for parallel gesture checking
        self.gesture_pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)        

    def update(self):
        while True:
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
                #DT.timestamp += 1 # should be monotonically increasing, because in LIVE_STREAM mode
                # Convert the OpenCV frame to a Tkinter-compatible photo image
                photo = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(detection, cv.COLOR_BGR2RGB)))
                # Put the frame in the queue for processing
                self.frame_queue.put(photo)   

            # Schedule the update method to be called after a delay (e.g., 10 milliseconds)
            #self.window.after(5, self.update) 
            self.window.after(5, self.gesture_input_update) 
    
    def gesture_input_update(self):
        if Camera.record == True: return # so it doesnt press any keys during Recording
        
        self.controller.gesture_to_input(self.detected_gestures)

    def close(self):
        # Release the camera and close the application
        self.cap.release()
        self.window.destroy()
        
    def set_loadout(self, loadout):
        self.controller.set_loadout(loadout)

    def start_landmark_recording():
        if Camera.record == False:
                Camera.record = True
                print("Frame recording started")

    def process_frames(self):
        while True:
            # Get a frame from the queue
            photo = self.frame_queue.get()

            # Submit the frame for parallel gesture checking
            self.gesture_pool.submit(self.check_gesture, photo)

            # Mark the task as done in the queue
            self.frame_queue.task_done()

    def check_gesture(self, photo):
        # Process the frame (e.g., perform gesture detection)
            
            # Check brightness of the frame
            dark = self.check_brightness(photo)

            # Update the label text with the detected hand gestures
            self.detected_gestures = DT.current_gestures
            label_txt = "No gestures detected."
            
            if (dark == False):
                if len(self.detected_gestures) == 1:
                    label_txt = f"{self.detected_gestures[0]}"
                elif len(self.detected_gestures) > 1:
                    label_txt = ", ".join(self.detected_gestures)
                elif len(self.detected_gestures) < 1:
                    label_txt = "No gestures detected."
            else:
                label_txt = "The environment is too dark"
            
            self.text.configure(text=label_txt)

            # Update the canvas with the processed frame
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    def check_brightness(self, photo, threshold=50):
        # Convert PhotoImage to PIL Image
        pil_image = ImageTk.getimage(photo)
        
        # Convert to NumPy array
        frame = np.array(pil_image)

        # Convert to BGR format
        frame_bgr = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        # Access the red channel directly
        red_channel = frame_bgr[:, :, 2]

        # Calculate average intensity
        avg_intensity = np.mean(red_channel)

        return avg_intensity < threshold


if __name__ == "__main__":
    app = tk.Tk()
    camera = Camera(app, 640, 480)
    app.mainloop()

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
                else:
                    KeyInput.PressKey(self.loadout[gesture])  # press all key detected otherwise
        