# Smart-attendance-system
# Smart Attendance System 🧠🎓

A smart facial recognition-based attendance system built with **Python**, **OpenCV**, **Flask**, and **SQLite3**. It automatically detects faces using your webcam and marks attendance in real-time.

---

## 🚀 Features

- 🎥 Live face detection using OpenCV
- 🧠 Face recognition with LBPH algorithm
- 🗃️ SQLite3 database for students & attendance records
- 📤 Upload images of students for training
- 📊 Attendance history viewer
- 🎨 Beautiful, responsive UI with HTML + CSS

---

## 📸 Screenshots

<img src="static/screenshots/home.png" width="600">
<img src="static/screenshots/upload.png" width="600">
<img src="static/screenshots/history.png" width="600">

---

## 🧰 Tech Stack

| Category         | Tools Used               |
|------------------|---------------------------|
| Backend          | Python, Flask             |
| Face Recognition | OpenCV, LBPH              |
| Frontend         | HTML, CSS (custom)        |
| Database         | SQLite3                   |
| Version Control  | Git, GitHub               |

---

## 📁 Project Structure
Smart-Attendance-System/
│
├── app.py # Flask app
├── face_encoder.py # Face training logic
├── attendance_system.py # Real-time face recognition
├── database/attendance.db # SQLite3 DB
├── known_faces/ # Trained student images
├── static/styles.css # Styling
├── templates/ # HTML pages
│ ├── index.html
│ ├── upload.html
│ └── history.html
├── .gitignore
└── README.md

