import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Define the correct username and password
USERNAME = "faculty"
PASSWORD = "password123"

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join(os.getcwd(), 'traininglabel', 'trainer.yml')
trainimage_path = "dataset/"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

def show_login_window():
    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("300x250")
    login_window.configure(background="black")

    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        if username == USERNAME and password == PASSWORD:
            login_window.destroy()
            show_main_window()
        else:
            error_label.config(text="Invalid credentials, please try again.")

    title_label = Label(login_window, text="Login", bg="black", fg="white", font=("Helvetica", 15))
    title_label.pack(pady=10)

    username_label = Label(login_window, text="Username:", bg="black", fg="white", font=("Helvetica", 12))
    username_label.pack(pady=5)
    username_entry = Entry(login_window, width=20, font=("Helvetica", 12))
    username_entry.pack(pady=5)

    password_label = Label(login_window, text="Password:", bg="black", fg="white", font=("Helvetica", 12))
    password_label.pack(pady=5)
    password_entry = Entry(login_window, width=20, font=("Helvetica", 12), show="*")
    password_entry.pack(pady=5)

    login_button = Button(login_window, text="Login", command=authenticate, bg="black", fg="white", font=("Helvetica", 12))
    login_button.pack(pady=10)

    error_label = Label(login_window, text="", bg="black", fg="red", font=("Helvetica", 12))
    error_label.pack(pady=5)

    login_window.mainloop()

def show_main_window():
    window = Tk()
    window.title("Attendify")
    window.attributes('-fullscreen', True)
    window.configure(background="white")

    # Create a frame to hold all the content
    content_frame = Frame(window, bg="white")
    content_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # to destroy screen
    def del_sc1():
        sc1.destroy()

    # error message for name and no
    def err_screen():
        global sc1
        sc1 = tk.Tk()
        sc1.geometry("300x100")
        sc1.title("Warning!!")
        sc1.configure(background="white")
        sc1.resizable(0, 0)
        tk.Label(
            sc1,
            text="Enrollment & Name required!!!",
            fg="black",
            bg="white",
            font=("Helvetica", 12, "bold"),
        ).pack(pady=10)
        tk.Button(
            sc1,
            text="OK",
            command=del_sc1,
            fg="black",
            bg="white",
            width=9,
            height=1,
            font=("Helvetica", 12, "bold"),
        ).pack()

    def testVal(inStr, acttyp):
        if acttyp == "1":  # insert
            if not inStr.isdigit():
                return False
        return True

    def TakeImageUI():
        ImageUI = Tk()
        ImageUI.title("Register")
        ImageUI.geometry("400x300")
        ImageUI.configure(background="white")
        ImageUI.resizable(0, 0)
        
        tk.Label(ImageUI, text="Register Your Face", bg="white", fg="black", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(ImageUI, text="Enrollment No", bg="white", fg="black", font=("Helvetica", 12)).pack(pady=5)
        txt1 = tk.Entry(ImageUI, width=20, font=("Helvetica", 12))
        txt1.pack(pady=5)
        txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

        tk.Label(ImageUI, text="Name", bg="white", fg="black", font=("Helvetica", 12)).pack(pady=5)
        txt2 = tk.Entry(ImageUI, width=20, font=("Helvetica", 12))
        txt2.pack(pady=5)

        message = tk.Label(ImageUI, text="", bg="white", fg="black", font=("Helvetica", 12))
        message.pack(pady=5)

        def take_image():
            l1 = txt1.get()
            l2 = txt2.get()
            takeImage.TakeImage(
                l1,
                l2,
                haarcasecade_path,
                trainimage_path,
                message,
                err_screen,
                text_to_speech,
            )
            txt1.delete(0, "end")
            txt2.delete(0, "end")

        tk.Button(ImageUI, text="Take Image", command=take_image, bg="white", fg="black", font=("Helvetica", 12, "bold")).pack(pady=10)

        def train_image():
            trainImage.TrainImage(
                haarcasecade_path,
                trainimage_path,
                trainimagelabel_path,
                message,
                text_to_speech,
            )

        tk.Button(ImageUI, text="Train Image", command=train_image, bg="white", fg="black", font=("Helvetica", 12, "bold")).pack(pady=10)

    tk.Label(content_frame, text="Attendify", bg="white", fg="black", font=("Helvetica", 24, "bold")).pack(pady=20)
    tk.Label(content_frame, text="Face Recognition Based Attendance Management System", bg="white", fg="black", font=("Helvetica", 14, "italic")).pack(pady=10)

    # Create a frame to hold the buttons
    button_frame = Frame(content_frame, bg="white")
    button_frame.pack(pady=20)

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

    def create_rounded_button(text, command):
        canvas = Canvas(button_frame, width=250, height=120, bg="white", highlightthickness=0)
        canvas.pack(side=LEFT, padx=10)
        create_rounded_rectangle(canvas, 10, 10, 240, 110, radius=20, fill="black")
        button = Button(canvas, text=text, command=command, bg="black", fg="white", font=("Helvetica", 12, "bold"), relief=FLAT)
        button.place(relx=0.5, rely=0.5, anchor=CENTER)
        canvas.tag_bind("all", "<Button-1>", lambda event, cmd=command: cmd())
        return button

    create_rounded_button("Register a new student", TakeImageUI)
    create_rounded_button("Take Attendance", lambda: automaticAttedance.subjectChoose(text_to_speech))
    create_rounded_button("View Attendance", lambda: show_attendance.subjectchoose(text_to_speech))

    # Exit button
    exit_button = Button(content_frame, text="EXIT", command=quit, bg="black", fg="white", font=("Helvetica", 12, "bold"), relief=FLAT)
    exit_button.pack(pady=20)

    window.mainloop()

# Start the application with the login window
show_login_window()
