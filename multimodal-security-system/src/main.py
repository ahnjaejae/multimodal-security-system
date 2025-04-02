import threading
import src.sensors as sensors
import src.camera_ai as camera_ai

def run_sensors():
    sensor = sensors.Sensor()
    while True:
        print(f"온도: {sensor.read_temperature()}°C, 습도: {sensor.read_humidity()}%, 공기질: {sensor.read_air_quality()}, 조도: {sensor.read_light_level()} lux")

def run_camera():
    camera_ai.detect_faces()

if __name__ == "__main__":
    t1 = threading.Thread(target=run_sensors)
    t2 = threading.Thread(target=run_camera)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
