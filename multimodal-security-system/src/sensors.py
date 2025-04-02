import random
import time

class Sensor:
    def read_temperature(self):
        return round(random.uniform(20.0, 30.0), 2)  # 온도 (°C)

    def read_humidity(self):
        return round(random.uniform(30.0, 60.0), 2)  # 습도 (%)

    def read_air_quality(self):
        return round(random.uniform(0, 500), 2)  # 공기질 (AQI)

    def read_light_level(self):
        return round(random.uniform(0, 1000), 2)  # 조도 (lux)

if __name__ == "__main__":
    sensor = Sensor()
    while True:
        print(f"온도: {sensor.read_temperature()}°C, 습도: {sensor.read_humidity()}%, 공기질: {sensor.read_air_quality()}, 조도: {sensor.read_light_level()} lux")
        time.sleep(2)  # 2초마다 데이터 갱신
