from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/api/sensors')
def get_sensor_data():
    return jsonify({
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 60.0), 2),
        "air_quality": round(random.uniform(0, 500), 2),
        "light_level": round(random.uniform(0, 1000), 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
