from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3 
from werkzeug.utils import secure_filename
from face_encoder import encode_faces_from_folder
from attendance_system import AttendanceSystem

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'known_faces'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Encode the uploaded faces
        encode_faces_from_folder(app.config['UPLOAD_FOLDER'])
        
        return redirect(url_for('run_attendance'))
    
    return render_template('upload.html')

@app.route('/run')
def run_attendance():
    attendance_system = AttendanceSystem()
    attendance_system.run_recognition()
    return "Attendance system stopped. <a href='/'>Go back</a>"

@app.route('/history')
def view_history():
    conn = sqlite3.connect('database/attendance.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.name, attendance.date, attendance.time
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        ORDER BY attendance.date DESC, attendance.time DESC
    """)
    
    records = cursor.fetchall()
    conn.close()
    
    return render_template('history.html', records=records)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('database', exist_ok=True)
    app.run(debug=True)
