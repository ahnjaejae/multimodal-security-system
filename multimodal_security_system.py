import threading
import random
import time
import cv2
from flask import Flask, jsonify

# Sensor Class
class Sensor:
    def read_temperature(self):
        return round(random.uniform(20.0, 30.0), 2)

    def read_humidity(self):
        return round(random.uniform(30.0, 60.0), 2)

    def read_air_quality(self):
        return round(random.uniform(0, 500), 2)

    def read_light_level(self):
        return round(random.uniform(0, 1000), 2)

def run_sensors():
    sensor = Sensor()
    while True:
        print(f"온도: {sensor.read_temperature()}°C, 습도: {sensor.read_humidity()}%, 공기질: {sensor.read_air_quality()}, 조도: {sensor.read_light_level()} lux")
        time.sleep(2)

# Camera AI Detection
def detect_faces():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_camera():
    detect_faces()

# Web Dashboard API
app = Flask(__name__)

@app.route('/api/sensors')
def get_sensor_data():
    sensor = Sensor()
    return jsonify({
        "temperature": sensor.read_temperature(),
        "humidity": sensor.read_humidity(),
        "air_quality": sensor.read_air_quality(),
        "light_level": sensor.read_light_level()
    })

def run_web():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_sensors)
    t2 = threading.Thread(target=run_camera)
    t3 = threading.Thread(target=run_web)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
