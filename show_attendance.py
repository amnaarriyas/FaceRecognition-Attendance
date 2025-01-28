import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import time
import datetime

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return
        subject_path = os.path.join("Attendance", Subject)
        filenames = glob(os.path.join(subject_path, f"{Subject}*.csv"))
        if not filenames:
            t = 'No attendance files found for the subject.'
            text_to_speech(t)
            return
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        
        # Ensure the "Attendance" column exists and is of string type
        if "Attendance" not in newdf.columns:
            newdf["Attendance"] = ""
        
        for i in range(len(newdf)):
            newdf.loc[i, "Attendance"] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
        
        # Ensure the directory exists
        if not os.path.exists(subject_path):
            os.makedirs(subject_path)
        
        # Correct the file path construction
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H-%M-%S")
        fileName = f"{Subject}_{date}_{timeStamp}.csv"
        filePath = os.path.join(subject_path, fileName)
        
        newdf.to_csv(filePath, index=False)

        root = tkinter.Tk()
        root.title("Attendance of " + Subject)
        root.geometry("1600x900")  # Increase window size
        root.configure(background="white")  # Change background to white

        # Add a canvas and scrollbars
        canvas = Canvas(root, bg="white")
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        v_scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview, bg="black", troughcolor="black", activebackground="black")
        v_scrollbar.pack(side=RIGHT, fill=Y)

        h_scrollbar = Scrollbar(root, orient=HORIZONTAL, command=canvas.xview, bg="black", troughcolor="black", activebackground="black")
        h_scrollbar.pack(side=BOTTOM, fill=X)

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        content_frame = Frame(canvas, bg="white")  # Change background to white
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        content_frame.bind("<Configure>", on_frame_configure)

        with open(filePath) as file:
            reader = csv.reader(file)
            for r, col in enumerate(reader):
                for c, row in enumerate(col):
                    label = tkinter.Label(
                        content_frame,
                        width=20,  # Increase width for better visibility
                        height=1,
                        fg="black",  # Change text color to black for better visibility
                        font=("Helvetica", 15, "bold"),
                        bg="white",  # Change background to white
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
        root.update()
        print(newdf)

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("800x600")
    subject.configure(background="black")
    content_frame = Frame(subject, bg="black")
    content_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    titl = tk.Label(content_frame, bg="black", relief=RIDGE, bd=10, font=("Helvetica", 30))
    titl.pack(fill=X)
    titl = tk.Label(
        content_frame,
        text="Which Subject of Attendance?",
        bg="black",
        fg="white",
        font=("Helvetica", 25),
    )
    titl.pack(pady=20)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    attf = tk.Button(
        content_frame,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("Helvetica", 15),
        bg="black",
        fg="white",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.pack(pady=10)

    sub = tk.Label(
        content_frame,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="white",
        bd=5,
        relief=RIDGE,
        font=("Helvetica", 15),
    )
    sub.pack(pady=10)

    tx = tk.Entry(
        content_frame,
        width=15,
        bd=5,
        bg="black",
        fg="white",
        relief=RIDGE,
        font=("Helvetica", 30, "bold"),
    )
    tx.pack(pady=10)

    fill_a = tk.Button(
        content_frame,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("Helvetica", 15),
        bg="black",
        fg="white",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.pack(pady=10)
    subject.mainloop()
