# FaceRecognition-Attendance

A Python-based system that automates attendance tracking using facial recognition. Capture images of faces, train a recognition model, and mark attendance in real time.

## Table of Contents
- [Features](#features)
- [System Architecture / Workflow](#system-architecture--workflow)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Collect Images](#1-collect-images)
  - [2. Train Model](#2-train-model)
  - [3. Mark Attendance](#3-mark-attendance)
  - [4. View Attendance](#4-view-attendance)
  - [Manual Mode](#manual-mode)
  - [Testing](#testing)
- [File Structure](#file-structure)
- [Configuration / Customization](#configuration--customization)
- [Limitations & Future Improvements](#limitations--future-improvements)
- [Credits / Acknowledgments](#credits--acknowledgments)
- [License](#license)

## Features
- Real-time face detection using Haar cascades
- Face recognition to identify students
- Automatic attendance logging with timestamps
- Ability to manually add attendance entries
- Export or view attendance records
- Lightweight and easy to adapt for small class settings

## System Architecture / Workflow
1. **Image Capture** — Use webcam to capture face images of students.
2. **Training** — Train a facial recognition model on the captured images.
3. **Recognition + Attendance** — Run a real-time recognition session; recognized faces get marked as present in a database.
4. **Presentation / Reporting** — View or export attendance records via GUI or script.

## Prerequisites
- Python 3.6+
- OpenCV
- NumPy
- SQLite3 (or built-in Python’s sqlite3)
- Other dependencies listed in `requirements.txt`

## Installation
```bash
# 1. Clone the repo
git clone https://github.com/amnaarriyas/FaceRecognition-Attendance.git
cd FaceRecognition-Attendance

# 2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt
