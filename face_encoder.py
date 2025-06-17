import cv2
import os
import numpy as np
import sqlite3

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def encode_faces_from_folder(folder_path):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, labels = [], []
    label_ids, current_id = {}, 0

    conn = sqlite3.connect('database/attendance.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            image_path TEXT
        )
    """)
    cursor.execute("DELETE FROM students")

    os.makedirs('known_faces', exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            name = os.path.splitext(filename)[0]
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Warning: Cannot read image {image_path}")
                continue

            face_rects = detect_faces(image)
            if len(face_rects) > 0:
                (x, y, w, h) = face_rects[0]
                face_roi = cv2.cvtColor(image[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)

                if name not in label_ids:
                    label_ids[name] = current_id
                    current_id += 1

                cursor.execute("INSERT OR IGNORE INTO students (name, image_path) VALUES (?, ?)", (name, image_path))
                faces.append(face_roi)
                labels.append(label_ids[name])

    if faces:
        recognizer.train(faces, np.array(labels))
        recognizer.save('known_faces/face_recognizer.yml')
        print("Face recognizer trained and saved.")
    else:
        print("No faces found to train.")

    conn.commit()
    conn.close()
    return label_ids
