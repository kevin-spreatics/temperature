from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='doubled',
        password='spreatics*',
        db='temperature_doubled',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 1. 상태 정보 전달
@app.route('/status', methods=['POST'])
def receive_status():
    data = request.get_json()
    temperature = data.get('temperature')
    fan = data.get('fan')
    heater = data.get('heater')

    if temperature is None or fan is None or heater is None:
        return jsonify({"status": "failed", "reason": "필수 값 누락"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO status_log (temperature, fan, heater) VALUES (%s, %s, %s)",
                (temperature, fan, heater)
            )
        conn.commit()
        return jsonify({"status": "success"}), 200
    finally:
        conn.close()

# 2. 서버가 저장한 설정 온도 가져오기 
@app.route('/setting', methods=['GET'])
def get_setting():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT temperature FROM setting ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            temp = row['temperature']
            if temp == -1:
                return jsonify({
                    "temperature": -1,
                    "fan": False,
                    "heater": False
                }), 200
            else:
                return jsonify({
                    "temperature": temp
                }), 200
    finally:
        conn.close()

#3. 사용자가 온도 설정하기 
@app.route('/setting', methods=['POST'])
def set_setting():
    data = request.get_json()
    temperature = data.get('temperature')

    if temperature is None:
        return jsonify({"status": "failed", "reason": "temperature 값 없음"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO setting (temperature) VALUES (%s)",
                (temperature,)
            )
        conn.commit()
        return jsonify({
            "status": "success",
            "temperature": temperature
        }), 200
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
