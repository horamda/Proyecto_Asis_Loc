import cv2
import os
import numpy as np
from flask import Flask, render_template, Response, request

app = Flask(__name__)

camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    name = request.form['name']
    directory = f'dataset/{name}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    count = 0
    while count < 50:
        success, frame = camera.read()
        if success:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                resized_face = cv2.resize(face_img, (100, 100))
                cv2.imwrite(f'{directory}/{name}_{count}.jpg', resized_face)
                count += 1
                if count >= 400:
                    break
    return 'Capturadas 50 imagenes'

if __name__ == '__main__':
    app.run(debug=True)
