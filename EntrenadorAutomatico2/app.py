from flask import Flask, render_template, Response, request
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'dataset'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

camera = cv2.VideoCapture(0)

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
    person_folder = os.path.join(app.config['UPLOAD_FOLDER'], name)

    if not os.path.exists(person_folder):
        os.makedirs(person_folder)

    existing_files = os.listdir(person_folder)
    start_index = len(existing_files)

    for i in range(start_index, start_index + 50):
        success, frame = camera.read()
        if success:
            filename = os.path.join(person_folder, f"{name}_{i}.jpg")
            cv2.imwrite(filename, frame)

    return f"Captura de imágenes completa para {name}. Proceda al siguiente ángulo."

if __name__ == '__main__':
    app.run(debug=True)
