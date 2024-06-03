from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

TARGET_LAT = -36.7232497  # Ejemplo: Latitud de Buenos Aires
TARGET_LON = -56.6750185  # Ejemplo: Longitud de Buenos Aires
RADIUS = 0.01  # Radio en grados, ajusta según necesites

def is_within_target_location(lat, lon):
    return abs(lat - TARGET_LAT) < RADIUS and abs(lon - TARGET_LON) < RADIUS

def is_before_target_time():
    current_time = datetime.datetime.now().time()
    target_time = datetime.time(7, 0, 0)  # 7:00 AM
    return current_time < target_time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-location', methods=['POST'])
def check_location():
    data = request.get_json()
    lat = data['latitude']
    lon = data['longitude']
    
    if is_within_target_location(lat, lon) and is_before_target_time():
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"})

if __name__ == '__main__':
    app.run(debug=True)
