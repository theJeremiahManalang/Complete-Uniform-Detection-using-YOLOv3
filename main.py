import torch
import cv2
import numpy as np
import pathlib
import serial
import time


# Modify the path handling for Windows
pathlib.PosixPath = pathlib.WindowsPath


# Specify the path to your YOLOv5 repository directory and weights file
yolov5_dir = r'C:\Users\jere\yolov5'
weights_path = r'C:\Users\jere\yolov5\best (1).pt'


# Load the YOLOv5 model using torch.hub.load()
model = torch.hub.load(str(yolov5_dir), 'custom', path=str(weights_path), source='local')


# Initialize webcam (1 is the secondary camera)
cap = cv2.VideoCapture(0)


# Initialize serial communication with Arduino
arduino_port = 'COM8'  # Replace 'COM7' with your Arduino port
arduino_baudrate = 9600
arduino = serial.Serial(arduino_port, arduino_baudrate)
time.sleep(2)  # Allow time for Arduino to initialize


# Main loop for processing frames from the webcam
while True:
   # Capture frame from the webcam
   ret, frame = cap.read()
   if not ret:
       break


   # Perform inference using the YOLOv5 model
   results = model(frame)


   # Extract class names and corresponding bounding boxes
   class_names = results.names
   boxes = results.xyxy[0]


   # Initialize flags for detecting resistor, capacitor, and transistor
   polo_detected = False
   id_detected = False
   slacks_detected = False
   shoes_detected = False
   # Check each detection for resistor, capacitor, and transistor
   for box in boxes:
       label = int(box[5])
       if label == 0:  # polo
           polo_detected = True
       elif label == 1:  # id
           id_detected = True
       elif label == 2:  # slacks
           slacks_detected = True
       elif label == 3:  # shoes
           shoes_detected = True


   # Send signals to Arduino based on detection results
   if polo_detected:
       arduino.write(b'A')  # Turn on resistor LED
   else:
       arduino.write(b'E')  # Turn off resistor LED


   if id_detected:
       arduino.write(b'B')  # Turn on capacitor LED
   else:
       arduino.write(b'E')  # Turn off capacitor LED


   if slacks_detected:
       arduino.write(b'C')  # Turn on transistor LED
   else:
       arduino.write(b'E')  # Turn off transistor LED


   if shoes_detected:
       arduino.write(b'D')  # Turn on transistor LED
   else:
       arduino.write(b'E')  # Turn off transistor LED


   # Render detection results on the frame
   rendered_frames = results.render()
   if rendered_frames:
       # Get the first frame with annotations
       annotated_frame = rendered_frames[0]


       # Convert annotated_frame to NumPy array if it is not already
       if not isinstance(annotated_frame, np.ndarray):
           annotated_frame = np.array(annotated_frame)


       # Display the frame with annotations
       cv2.imshow('YOLOv5 Detection', annotated_frame)
   else:
       print("No frames to render.")


   # Exit the loop on 'q' key press
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break


# Release webcam, close OpenCV windows, and close serial connection
cap.release()
cv2.destroyAllWindows()
arduino.close()
