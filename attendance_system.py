import cv2
import numpy as np
import sqlite3
from datetime import datetime
import os

class AttendanceSystem:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.label_ids = {}
        self.recently_marked = set()

        if os.path.exists('known_faces/face_recognizer.yml'):
            try:
                self.recognizer.read('known_faces/face_recognizer.yml')
                self.label_ids = self.load_label_ids()
                print("Recognizer loaded.")
            except Exception as e:
                print(f"Error loading recognizer: {e}")
        else:
            print("Train the system first. Recognizer not found.")

    def load_label_ids(self):
        conn = sqlite3.connect('database/attendance.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students")
        rows = cursor.fetchall()
        conn.close()
        return {i: row[0] for i, row in enumerate(rows)}

    def mark_attendance(self, name):
        if name in self.recently_marked:
            return

        conn = sqlite3.connect('database/attendance.db')
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """)

        cursor.execute("SELECT id FROM students WHERE name=?", (name,))
        result = cursor.fetchone()
        if result is None:
            print(f"Student {name} not in DB")
            conn.close()
            return

        student_id = result[0]
        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("SELECT id FROM attendance WHERE student_id=? AND date=?", (student_id, today))
        if not cursor.fetchone():
            now = datetime.now()
            cursor.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)",
                           (student_id, today, now.strftime("%H:%M:%S")))
            conn.commit()
            print(f"Marked: {name}")
            self.recently_marked.add(name)
        else:
            print(f"{name} already marked today.")

        conn.close()

    def run_recognition(self):
        if not os.path.exists('known_faces/face_recognizer.yml'):
            print("Recognizer not trained.")
            return

        cap = cv2.VideoCapture(0)
        print("Press 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Camera error.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                try:
                    label_id, confidence = self.recognizer.predict(roi)
                    if confidence < 80:
                        name = self.label_ids.get(label_id, "Unknown")
                        self.mark_attendance(name)
                        color = (0, 255, 0)
                    else:
                        name = "Unknown"
                        color = (0, 0, 255)

                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                except Exception as e:
                    print(f"Recognition error: {e}")

            cv2.imshow("Attendance", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Session ended.")
