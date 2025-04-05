import tkinter as tk
from tkinter import *
import os, cv2
import pyttsx3
from PIL import ImageTk, Image
import shutil, csv, numpy as np, pandas as pd, datetime, time

# --- Import custom modules ---
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# --- Configurations ---
USERNAME = "faculty"
PASSWORD = "password123"

# Soft Pixel-Art Color Palette
BG_COLOR = "#f5f5f5"  # Soft off-white
TEXT_COLOR = "#333333"  # Dark gray (soft)
ACCENT_1 = "#a8d8ea"  # Pastel blue
ACCENT_2 = "#aa96da"  # Pastel purple
ACCENT_3 = "#fcbad3"  # Pastel pink
ERROR_COLOR = "#ff6b6b"  # Soft red

# Fonts
PIXEL_FONT = ("Courier New", 12)  # Clean but slightly pixelated
PIXEL_FONT_BOLD = ("Courier New", 12, "bold")
TITLE_FONT = ("Courier New", 18, "bold")

# Paths
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join(os.getcwd(), 'traininglabel', 'trainer.yml')
trainimage_path = "dataset/"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# --- Login Window (Soft Pixel Style) ---
def show_login_window():
    login_window = Tk()
    login_window.title("Login • Attendify")
    login_window.geometry("340x300")
    login_window.configure(background=BG_COLOR)
    login_window.resizable(False, False)
    
    # Frame for centering
    login_frame = Frame(login_window, bg=BG_COLOR)
    login_frame.pack(pady=20)
    
    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        if username == USERNAME and password == PASSWORD:
            login_window.destroy()
            show_main_window()
        else:
            error_label.config(text="Invalid credentials!")
    
    # Title
    Label(login_frame, text="ATTENDIFY", bg=BG_COLOR, fg=ACCENT_2, font=TITLE_FONT).pack(pady=10)
    
    # Username
    Label(login_frame, text="Username:", bg=BG_COLOR, fg=TEXT_COLOR, font=PIXEL_FONT).pack(pady=5)
    username_entry = Entry(login_frame, width=25, font=PIXEL_FONT, bg="white", fg=TEXT_COLOR, relief="flat", bd=2)
    username_entry.pack(pady=5)
    
    # Password
    Label(login_frame, text="Password:", bg=BG_COLOR, fg=TEXT_COLOR, font=PIXEL_FONT).pack(pady=5)
    password_entry = Entry(login_frame, width=25, font=PIXEL_FONT, bg="white", fg=TEXT_COLOR, show="*", relief="flat", bd=2)
    password_entry.pack(pady=5)
    
    # Login Button (Rounded look)
    login_button = Button(login_frame, text="Login", command=authenticate, bg=ACCENT_1, fg="white", font=PIXEL_FONT_BOLD, relief="flat", padx=20)
    login_button.pack(pady=15)
    
    # Error Label
    error_label = Label(login_frame, text="", bg=BG_COLOR, fg=ERROR_COLOR, font=PIXEL_FONT)
    error_label.pack()
    
    login_window.mainloop()

# --- TakeImageUI Function (Registration Window) ---
def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Register • Attendify")
    ImageUI.geometry("500x450")
    ImageUI.configure(background=BG_COLOR)
    ImageUI.resizable(False, False)

    # Error message function
    def err_screen():
        error_win = Toplevel(ImageUI)
        error_win.title("Error")
        error_win.geometry("300x120")
        error_win.configure(background=BG_COLOR)
        Label(error_win, text="Enrollment & Name required!", bg=BG_COLOR, fg=ERROR_COLOR, font=PIXEL_FONT).pack(pady=20)
        Button(error_win, text="OK", command=error_win.destroy, bg=ACCENT_1, fg="white", font=PIXEL_FONT).pack()

    # UI Elements
    Label(ImageUI, text="REGISTER STUDENT", bg=BG_COLOR, fg=ACCENT_2, font=TITLE_FONT).pack(pady=10)
    
    Label(ImageUI, text="Enrollment No:", bg=BG_COLOR, fg=TEXT_COLOR, font=PIXEL_FONT).pack(pady=5)
    txt_enroll = Entry(ImageUI, width=25, font=PIXEL_FONT, bg="white", fg=TEXT_COLOR, relief="flat", bd=2)
    txt_enroll.pack(pady=5)
    
    Label(ImageUI, text="Name:", bg=BG_COLOR, fg=TEXT_COLOR, font=PIXEL_FONT).pack(pady=5)
    txt_name = Entry(ImageUI, width=25, font=PIXEL_FONT, bg="white", fg=TEXT_COLOR, relief="flat", bd=2)
    txt_name.pack(pady=5)
    
    message = Label(ImageUI, text="", bg=BG_COLOR, fg=TEXT_COLOR, font=PIXEL_FONT)
    message.pack(pady=10)
    
    # Button Functions
    def take_image():
        enroll = txt_enroll.get()
        name = txt_name.get()
        if enroll and name:
            takeImage.TakeImage(enroll, name, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech)
            txt_enroll.delete(0, END)
            txt_name.delete(0, END)
        else:
            err_screen()
    
    def train_images():
        trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech)
    
    # Buttons
    Button(ImageUI, text="📷 Take Image", command=take_image, bg=ACCENT_1, fg="white", font=PIXEL_FONT_BOLD, relief="flat", padx=20).pack(pady=10)
    Button(ImageUI, text="🔧 Train Images", command=train_images, bg=ACCENT_3, fg="white", font=PIXEL_FONT_BOLD, relief="flat", padx=20).pack(pady=10)
    
    ImageUI.mainloop()

# --- Main Window (Soft Pixel-Art UI) ---
def show_main_window():
    window = Tk()
    window.title("Attendify • Dashboard")
    window.geometry("720x580")
    window.configure(background=BG_COLOR)
    window.resizable(False, False)
    
    # Main Frame
    main_frame = Frame(window, bg=BG_COLOR)
    main_frame.pack(pady=30)
    
    # Header
    Label(main_frame, text="ATTENDIFY", bg=BG_COLOR, fg=ACCENT_2, font=TITLE_FONT).pack(pady=10)
    Label(main_frame, text="Face Recognition Attendance", bg=BG_COLOR, fg=TEXT_COLOR, font=PIXEL_FONT).pack(pady=5)
    
    # Button Frame
    button_frame = Frame(main_frame, bg=BG_COLOR)
    button_frame.pack(pady=20)
    
    # Styled Buttons (Soft Pixel Aesthetic)
    def create_pixel_button(text, command, bg_color):
        btn = Button(button_frame, text=text, command=command, bg=bg_color, fg="white", 
                    font=PIXEL_FONT_BOLD, relief="flat", padx=20, pady=10, bd=0)
        btn.pack(pady=10, fill="x")
        return btn
    
    # Buttons
    create_pixel_button("📷 Register Student", TakeImageUI, ACCENT_1)
    create_pixel_button("📝 Take Attendance", lambda: automaticAttedance.subjectChoose(text_to_speech), ACCENT_2)
    create_pixel_button("📊 View Attendance", lambda: show_attendance.subjectchoose(text_to_speech), ACCENT_3)
    
    # Exit Button
    Button(main_frame, text="Exit", command=quit, bg=ERROR_COLOR, fg="white", font=PIXEL_FONT_BOLD, relief="flat", padx=20).pack(pady=20)
    
    window.mainloop()

# --- Run ---
if __name__ == "__main__":
    show_login_window()