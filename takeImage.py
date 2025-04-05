import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time

# Soft Pixel-Art Color Palette
BG_COLOR = "#f5f5f5"  # Soft off-white
TEXT_COLOR = "#333333"  # Dark gray (soft)
ACCENT_1 = "#a8d8ea"  # Pastel blue
ACCENT_2 = "#aa96da"  # Pastel purple
ERROR_COLOR = "#ff6b6b"  # Soft red

# Fonts
PIXEL_FONT = ("Courier New", 12)
PIXEL_FONT_BOLD = ("Courier New", 12, "bold")

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    # Input validation with improved messaging
    if not l1 and not l2:
        err_msg = 'Please enter both Enrollment Number and Name.'
        text_to_speech(err_msg)
        err_screen()
        return
    elif not l1:
        err_msg = 'Please enter your Enrollment Number.'
        text_to_speech(err_msg)
        err_screen()
        return
    elif not l2:
        err_msg = 'Please enter your Name.'
        text_to_speech(err_msg)
        err_screen()
        return

    try:
        # Initialize camera and face detector
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        # Create directory for student images
        Enrollment = l1.strip()
        Name = l2.strip()
        directory = f"{Enrollment}_{Name}"
        path = os.path.join(trainimage_path, directory)
        
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            raise FileExistsError(f"Data already exists for {Enrollment}")

        # Image capture loop
        sampleNum = 0
        while sampleNum <= 50:
            ret, img = cam.read()
            if not ret:
                text_to_speech("Failed to capture image from camera")
                break
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                # Draw rectangle around face (now in accent color)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 170, 212), 2)
                
                # Save face image
                sampleNum += 1
                img_path = os.path.join(
                    path, 
                    f"{Name}_{Enrollment}_{sampleNum}.jpg"
                )
                cv2.imwrite(img_path, gray[y:y+h, x:x+w])
                
                # Display preview with styled text
                cv2.putText(
                    img, 
                    f"Captured: {sampleNum}/50", 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, 
                    (0, 170, 212), 
                    2
                )
                cv2.imshow("Register Face", img)

            # Exit conditions
            if cv2.waitKey(1) & 0xFF == ord('q') or sampleNum > 50:
                break

        # Cleanup
        cam.release()
        cv2.destroyAllWindows()

        # Save student details
        if sampleNum > 0:
            os.makedirs("StudentDetails", exist_ok=True)
            with open("StudentDetails/studentdetails.csv", "a+", newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([Enrollment, Name])
            
            success_msg = f"Registration complete for {Name} ({Enrollment})"
            if message:
                message.configure(
                    text=success_msg, 
                    fg="#2ecc71"  # Success green
                )
            text_to_speech(success_msg)

    except FileExistsError as e:
        error_msg = f"Student data already exists: {str(e)}"
        if message:
            message.configure(
                text=error_msg,
                fg=ERROR_COLOR
            )
        text_to_speech(error_msg)
        err_screen()
    except Exception as e:
        error_msg = f"Error during registration: {str(e)}"
        if message:
            message.configure(
                text=error_msg,
                fg=ERROR_COLOR
            )
        text_to_speech("An error occurred during face capture")
        err_screen()