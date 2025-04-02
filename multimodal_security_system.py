import threading
import random
import time
import cv2
from flask import Flask, jsonify

# 전역 변수 (센서 데이터 공유)
sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "air_quality": 0.0,
    "light_level": 0.0
}

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
    global sensor_data
    sensor = Sensor()
    while True:
        sensor_data["temperature"] = sensor.read_temperature()
        sensor_data["humidity"] = sensor.read_humidity()
        sensor_data["air_quality"] = sensor.read_air_quality()
        sensor_data["light_level"] = sensor.read_light_level()

        print(f"🌡️ 온도: {sensor_data['temperature']}°C, 💧 습도: {sensor_data['humidity']}%, 🌫️ 공기질: {sensor_data['air_quality']}, 💡 조도: {sensor_data['light_level']} lux")
        time.sleep(2)

# Camera AI Detection
def detect_faces():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # 카메라 장치 번호 자동 탐색
    cap = None
    for i in range(3):  # 0, 1, 2 순서로 테스트
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"✅ 카메라 장치 {i} 사용 중")
            break
    else:
        print("❌ 사용 가능한 카메라 없음")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 카메라 캡처 실패")
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
@app.route('/')
def home():
    return "<h1>멀티모달 보안 시스템</h1><p>/api/sensors 에서 센서 데이터를 확인하세요.</p>"

@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)

def run_web():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_sensors, daemon=True)
    t2 = threading.Thread(target=run_camera, daemon=True)
    t3 = threading.Thread(target=run_web, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
