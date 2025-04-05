import tkinter as tk
from tkinter import *
import os
import cv2
import pandas as pd
import datetime
import time
import csv
from PIL import Image, ImageTk

# Soft Pixel-Art Color Palette
BG_COLOR = "#f5f5f5"  # Soft off-white
TEXT_COLOR = "#333333"  # Dark gray (soft)
ACCENT_1 = "#a8d8ea"  # Pastel blue
ACCENT_2 = "#aa96da"  # Pastel purple
ACCENT_3 = "#fcbad3"  # Pastel pink
SUCCESS_COLOR = "#2ecc71"  # Soft green
ERROR_COLOR = "#ff6b6b"  # Soft red

# Fonts
PIXEL_FONT = ("Courier New", 12)
PIXEL_FONT_BOLD = ("Courier New", 12, "bold")
TITLE_FONT = ("Courier New", 16, "bold")

# Path configurations
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join(os.getcwd(), 'traininglabel', 'trainer.yml')
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

def Attf():
    """Functionality for checking attendance sheets"""
    # Implementation would go here
    pass

def load_student_details():
    """Robust CSV loading with error handling"""
    try:
        # Try reading with pandas first
        try:
            df = pd.read_csv(studentdetail_path, header=None, names=['Enrollment', 'Name'])
            return df.dropna()
        except pd.errors.ParserError:
            # Fallback to manual CSV parsing if pandas fails
            with open(studentdetail_path, 'r') as f:
                reader = csv.reader(f)
                data = [row[:2] for row in reader if len(row) >= 2]  # Take first 2 columns only
            return pd.DataFrame(data, columns=['Enrollment', 'Name'])
    except Exception as e:
        print(f"Error loading student details: {str(e)}")
        return pd.DataFrame(columns=['Enrollment', 'Name'])

def subjectChoose(text_to_speech):
    subject = Tk()
    subject.title("Take Attendance • Attendify")
    subject.geometry("800x600")
    subject.configure(background=BG_COLOR)
    subject.resizable(False, False)

    # Main content frame
    content_frame = Frame(subject, bg=BG_COLOR)
    content_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Notification label
    Notifica = Label(
        content_frame, 
        text="", 
        bg=BG_COLOR, 
        fg=TEXT_COLOR, 
        width=40, 
        font=TITLE_FONT
    )
    Notifica.pack(pady=20)

    def FillAttendance():
        sub = tx.get().strip()
        if not sub:
            t = "Please enter the subject name!"
            Notifica.config(text=t, fg=ERROR_COLOR)
            text_to_speech(t)
            return

        try:
            # Initialize face recognizer
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            try:
                recognizer.read(trainimagelabel_path)
            except:
                e = "Model not found, please train model first"
                Notifica.config(text=e, fg=ERROR_COLOR)
                text_to_speech(e)
                return

            # Load student details with robust error handling
            df = load_student_details()
            if df.empty:
                e = "No student data found or data is corrupted"
                Notifica.config(text=e, fg=ERROR_COLOR)
                text_to_speech(e)
                return

            face_cascade = cv2.CascadeClassifier(haarcasecade_path)
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            attendance = pd.DataFrame(columns=["Enrollment", "Name"])
            
            cv2.namedWindow("Taking Attendance", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Taking Attendance", 800, 600)

            while True:
                ret, im = cam.read()
                if not ret:
                    text_to_speech("Failed to capture video")
                    break

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                    
                    if conf < 70:
                        try:
                            student_name = df.loc[df["Enrollment"] == str(Id)]["Name"].values[0]
                            student_id = f"{Id}-{student_name}"
                            
                            if Id not in attendance["Enrollment"].values:
                                attendance.loc[len(attendance)] = [Id, student_name]
                            
                            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 170, 212), 4)
                            cv2.putText(im, student_id, (x, y-10), font, 0.9, (0, 170, 212), 2)
                        except:
                            # If student not found in database
                            cv2.rectangle(im, (x, y), (x+w, y+h), (255, 165, 0), 4)
                            cv2.putText(im, f"{Id}-Unknown", (x, y-10), font, 0.9, (255, 165, 0), 2)
                    else:
                        cv2.rectangle(im, (x, y), (x+w, y+h), (255, 102, 102), 4)
                        cv2.putText(im, "Unknown", (x, y-10), font, 0.9, (255, 102, 102), 2)

                cv2.imshow("Taking Attendance", im)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            if not attendance.empty:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H-%M-%S")
                
                os.makedirs(os.path.join(attendance_path, sub), exist_ok=True)
                filename = f"{sub}_{date}_{timeStamp}.csv"
                filepath = os.path.join(attendance_path, sub, filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                attendance.to_csv(filepath, index=False)
                
                success_msg = f"Attendance saved for {sub} ({len(attendance)} students)"
                Notifica.config(text=success_msg, fg=SUCCESS_COLOR)
                text_to_speech(success_msg)
                
                show_attendance_table(filepath)
            else:
                Notifica.config(text="No attendance recorded", fg=ERROR_COLOR)

            cam.release()
            cv2.destroyAllWindows()

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            Notifica.config(text=error_msg, fg=ERROR_COLOR)
            text_to_speech("An error occurred")
            print(error_msg)
            cv2.destroyAllWindows()

    def show_attendance_table(csv_path):
        """Display attendance in a styled table with error handling"""
        try:
            table_window = Toplevel(subject)
            table_window.title(f"Attendance Sheet")
            table_window.geometry("800x600")
            table_window.configure(background=BG_COLOR)
            
            canvas = Canvas(table_window, bg=BG_COLOR)
            scrollbar = Scrollbar(table_window, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg=BG_COLOR)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Robust CSV reading
            try:
                with open(csv_path, newline="", encoding='utf-8') as file:
                    reader = csv.reader(file)
                    headers = next(reader)
                    
                    # Header row
                    for col_idx, header in enumerate(headers):
                        Label(
                            scrollable_frame,
                            text=header,
                            bg=ACCENT_1,
                            fg="white",
                            font=PIXEL_FONT_BOLD,
                            width=20,
                            padx=5,
                            pady=5
                        ).grid(row=0, column=col_idx, sticky="nsew")
                    
                    # Data rows
                    for row_idx, row in enumerate(reader, start=1):
                        for col_idx, cell in enumerate(row):
                            bg_color = BG_COLOR if row_idx % 2 == 0 else "#e8e8e8"
                            Label(
                                scrollable_frame,
                                text=cell,
                                bg=bg_color,
                                fg=TEXT_COLOR,
                                font=PIXEL_FONT,
                                width=20,
                                padx=5,
                                pady=5
                            ).grid(row=row_idx, column=col_idx, sticky="nsew")
            except Exception as e:
                error_label = Label(
                    scrollable_frame,
                    text=f"Error displaying attendance: {str(e)}",
                    bg=ERROR_COLOR,
                    fg="white",
                    font=PIXEL_FONT_BOLD
                )
                error_label.pack(pady=20)
                
        except Exception as e:
            print(f"Error creating attendance table: {str(e)}")

    # Subject entry
    Label(
        content_frame,
        text="Enter Subject:",
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        font=TITLE_FONT
    ).pack(pady=10)

    tx = Entry(
        content_frame,
        width=25,
        font=PIXEL_FONT_BOLD,
        bg="white",
        fg=TEXT_COLOR,
        relief=FLAT,
        highlightthickness=1,
        highlightcolor=ACCENT_2,
        highlightbackground=ACCENT_2
    )
    tx.pack(pady=10)

    # Buttons
    button_frame = Frame(content_frame, bg=BG_COLOR)
    button_frame.pack(pady=20)

    fill_btn = Button(
        button_frame,
        text="Take Attendance",
        command=FillAttendance,
        bg=ACCENT_2,
        fg="white",
        font=PIXEL_FONT_BOLD,
        relief=FLAT,
        padx=20,
        pady=10
    )
    fill_btn.pack(side=LEFT, padx=10)

    sheets_btn = Button(
        button_frame,
        text="View Sheets",
        command=Attf,
        bg=ACCENT_3,
        fg="white",
        font=PIXEL_FONT_BOLD,
        relief=FLAT,
        padx=20,
        pady=10
    )
    sheets_btn.pack(side=LEFT, padx=10)

    subject.mainloop()