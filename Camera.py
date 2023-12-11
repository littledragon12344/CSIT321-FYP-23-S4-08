import tkinter as tk
import cv2
from PIL import Image, ImageTk

class Camera:
    def __init__(self, window, _width, _height):
        self.window = window

        # Create a canvas to display the camera feed
        self.canvas = tk.Canvas(window, width=_width, height=_height)
        self.canvas.pack()

        # Open the camera
        self.cap = cv2.VideoCapture(0)  # 0 for default camera, adjust if needed

        # Call the update method to continuously update the canvas with new frames
        self.update()

        # Add a button to close the application
        #self.close_button = tk.Button(window, text="Close", command=self.close)
        #self.close_button.pack()
        
        self.text = tk.Label(window, text="Gesture Display")

    def update(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        if ret:
            # Flip the frame horizontally (mirror effect)
            mirrored_frame = cv2.flip(frame, 1)
            # Convert the OpenCV frame to a Tkinter-compatible photo image
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(mirrored_frame, cv2.COLOR_BGR2RGB)))

            # Update the canvas with the new photo image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Schedule the update method to be called after a delay (e.g., 10 milliseconds)
        self.window.after(10, self.update)

    def close(self):
        # Release the camera and close the application
        self.cap.release()
        self.window.destroy()