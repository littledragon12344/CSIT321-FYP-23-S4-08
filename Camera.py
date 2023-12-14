import tkinter as tk
from tkinter import font
import cv2 as cv
from PIL import Image, ImageTk

import HandDetector as DT

class Camera:
    timestamp = 0
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

        # Open the camera
        self.cap = cv.VideoCapture(0)  # 0 for default camera, adjust if needed

        # Call the update method to continuously update the canvas with new frames
        self.update()

    def update(self):
        
        # Read a frame from the camera
        ret, frame = self.cap.read()
        
        if ret:
            # Flip the frame horizontally (mirror effect)
            mirrored_frame = cv.flip(frame, 1)
            detection = DT.detect(mirrored_frame, self.timestamp)
            self.timestamp = self.timestamp + 1 # should be monotonically increasing, because in LIVE_STREAM mode
            # Convert the OpenCV frame to a Tkinter-compatible photo image
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(detection, cv.COLOR_BGR2RGB)))
          
            # Update the canvas with the new photo image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
            # Update the label text with the detected hand gestures
            gestures = DT.current_gestures
            label_txt = "No gestures detected."
            if len(gestures) == 1:
                label_txt = f"{gestures[0]}"
            elif len(gestures) > 1:
                label_txt = ", ".join(gestures)
            self.text.configure(text=label_txt)

        # Schedule the update method to be called after a delay (e.g., 10 milliseconds)
        self.window.after(10, self.update)

    def close(self):
        # Release the camera and close the application
        self.cap.release()
        self.window.destroy()

    