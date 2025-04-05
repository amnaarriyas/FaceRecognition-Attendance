import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
import time
import datetime

# Soft Pixel-Art Color Palette
BG_COLOR = "#f5f5f5"  # Soft off-white
TEXT_COLOR = "#333333"  # Dark gray (soft)
ACCENT_1 = "#a8d8ea"  # Pastel blue
ACCENT_2 = "#aa96da"  # Pastel purple
ACCENT_3 = "#fcbad3"  # Pastel pink
ERROR_COLOR = "#ff6b6b"  # Soft red

# Fonts
PIXEL_FONT = ("Courier New", 12)
PIXEL_FONT_BOLD = ("Courier New", 12, "bold")
TITLE_FONT = ("Courier New", 16, "bold")

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

        # Attendance calculation logic
        if "Attendance" not in newdf.columns:
            newdf["Attendance"] = ""

        numeric_columns = newdf.iloc[:, 2:].select_dtypes(include=["number"]).columns
        for i in range(len(newdf)):
            if not numeric_columns.empty:
                mean_value = newdf.loc[i, numeric_columns].mean()
                newdf.loc[i, "Attendance"] = str(int(round(mean_value * 100))) + '%'
            else:
                newdf.loc[i, "Attendance"] = "0%"

        # Reorder columns
        columns = list(newdf.columns)
        if "Attendance" in columns:
            columns.remove("Attendance")
            name_index = columns.index("Name") + 1
            columns.insert(name_index, "Attendance")
            newdf = newdf[columns]

        # Save to CSV
        if not os.path.exists(subject_path):
            os.makedirs(subject_path)
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H-%M-%S")
        fileName = f"{Subject}_{date}_{timeStamp}.csv"
        filePath = os.path.join(subject_path, fileName)
        newdf.to_csv(filePath, index=False)

        # Display attendance table
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Header
        tk.Label(content_frame, 
                text="Attendance Sheet", 
                bg=BG_COLOR, 
                fg=ACCENT_2, 
                font=TITLE_FONT).grid(row=0, column=0, 
                                    columnspan=len(newdf.columns), 
                                    pady=10)

        # Column headers
        for col_idx, col_name in enumerate(newdf.columns):
            tk.Label(content_frame, 
                    text=col_name, 
                    bg=ACCENT_1, 
                    fg="white", 
                    font=PIXEL_FONT_BOLD, 
                    width=15, 
                    relief=FLAT).grid(row=1, 
                                    column=col_idx, 
                                    padx=2, 
                                    pady=2)

        # Data rows
        for row_idx, row in newdf.iterrows():
            for col_idx, value in enumerate(row):
                bg_color = BG_COLOR if row_idx % 2 == 0 else "#e8e8e8"
                tk.Label(content_frame, 
                        text=value, 
                        bg=bg_color, 
                        fg=TEXT_COLOR, 
                        font=PIXEL_FONT, 
                        width=15, 
                        relief=FLAT).grid(row=row_idx + 2, 
                                        column=col_idx, 
                                        padx=2, 
                                        pady=2)

    # Main window
    subject = Tk()
    subject.title("View Attendance • Attendify")
    subject.geometry("900x600")
    subject.configure(background=BG_COLOR)
    subject.resizable(False, False)

    # Content frame with scrollbar
    main_frame = Frame(subject, bg=BG_COLOR)
    main_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

    # Input frame
    input_frame = Frame(main_frame, bg=BG_COLOR)
    input_frame.pack(fill=X)

    tk.Label(input_frame, 
            text="Enter Subject Name:", 
            bg=BG_COLOR, 
            fg=TEXT_COLOR, 
            font=PIXEL_FONT).pack(side=LEFT, padx=5)
            
    tx = tk.Entry(input_frame, 
                width=25, 
                font=PIXEL_FONT, 
                bg="white", 
                fg=TEXT_COLOR, 
                relief=FLAT)
    tx.pack(side=LEFT, padx=5)

    tk.Button(input_frame, 
             text="View Attendance", 
             command=calculate_attendance, 
             bg=ACCENT_2, 
             fg="white", 
             font=PIXEL_FONT_BOLD, 
             relief=FLAT).pack(side=LEFT, padx=10)

    # Table frame with scrollbar
    table_frame = Frame(main_frame, bg=BG_COLOR)
    table_frame.pack(fill=BOTH, expand=True)

    canvas = Canvas(table_frame, bg=BG_COLOR)
    scrollbar = Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=BG_COLOR)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    content_frame = scrollable_frame

    subject.mainloop()