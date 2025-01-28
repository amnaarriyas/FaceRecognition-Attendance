import tkinter as tk
from tkinter import Tk, Frame, Label, Canvas, Entry, Button, RIDGE, FLAT, LEFT, CENTER
import os
import cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join(os.getcwd(), 'traininglabel', 'trainer.yml')
trainimage_path = "dataset/"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

def Attf():
    # Define the functionality for checking sheets here
    pass

def subjectChoose(text_to_speech):
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("800x600")
    subject.configure(background="black")
    content_frame = Frame(subject, bg="black")
    content_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Notifica = tk.Label(subject, text="", bg="black", fg="white", width=33, relief=RIDGE, bd=5, font=("Helvetica", 15, "bold"))
    
    def FillAttendance():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except cv2.error as e:
                    e = "Model not found, please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="white",
                        width=33,
                        font=("Helvetica", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                    return
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 0, 0), 4  # Change text color to black
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == ord('q'):  # Press 'q' to stop the attendance process
                        break

                ts = time.time()
                print(aa)
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    f"{Subject}_{date}_{Hour}-{Minute}-{Second}.csv"
                )
                filePath = os.path.join(path, fileName)
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv(filePath, index=False)

                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="white",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("Helvetica", 15, "bold"),
                )
                text_to_speech(m)

                Notifica.place(relx=0.5, rely=0.8, anchor=CENTER)

                cam.release()
                cv2.destroyAllWindows()

                root = tk.Tk()
                root.title("Attendance of " + Subject)
                root.geometry("800x600")
                root.configure(background="black")
                content_frame = Frame(root, bg="black")
                content_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
                with open(filePath, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:

                            label = Label(
                                content_frame,
                                width=10,
                                height=1,
                                fg="white",
                                font=("Helvetica", 15, "bold"),
                                bg="black",
                                text=row,
                                relief=RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except cv2.error as e:
                f = "OpenCV error: " + str(e)
                text_to_speech(f)
                print(f)
                cv2.destroyAllWindows()
            except Exception as e:
                f = "An error occurred: " + str(e)
                text_to_speech(f)
                print(f)
                cv2.destroyAllWindows()

    # Create a frame for the subject entry and label
    subject_entry_frame = Frame(content_frame, bg="black")
    subject_entry_frame.pack(pady=20)

    sub = tk.Label(
        subject_entry_frame,
        text="Enter Subject",
        width=20,
        height=3,
        bg="black",
        fg="white",
        font=("Helvetica", 15),
    )
    sub.pack(side=LEFT, padx=10)

    # Create a canvas for the text box with border radius
    canvas = Canvas(subject_entry_frame, width=300, height=50, bg="black", highlightthickness=0)
    canvas.pack(side=LEFT, padx=10)
    create_rounded_rectangle(canvas, 10, 10, 290, 40, outline="white", width=2, radius=10)
    tx = tk.Entry(
        subject_entry_frame,
        width=15,
        bd=0,
        bg="black",
        fg="white",
        font=("Helvetica", 15, "bold"),
        highlightthickness=0,
        insertbackground="white"
    )
    tx_window = canvas.create_window(150, 25, window=tx)

    # Create a frame for the buttons
    button_frame = Frame(content_frame, bg="black")
    button_frame.pack(pady=20)

    def create_rounded_button(text, command):
        button_canvas = Canvas(button_frame, width=250, height=60, bg="black", highlightthickness=0)
        button_canvas.pack(side=LEFT, padx=10)
        create_rounded_rectangle(button_canvas, 10, 10, 240, 50, fill="white", outline="", radius=10)
        button = Button(button_canvas, text=text, command=command, bg="white", fg="black", font=("Helvetica", 15), relief=FLAT)
        button.place(relx=0.5, rely=0.5, anchor=CENTER)
        return button

    fill_a = create_rounded_button("Fill Attendance", FillAttendance)
    attf = create_rounded_button("Check Sheets", Attf)

    subject.mainloop()

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)
