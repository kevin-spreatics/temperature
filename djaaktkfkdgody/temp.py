from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# MySQL 연결 설정
db = pymysql.connect(
    host='localhost',
    user='gamza',
    password='gamzagoguma',
    database='temperature_dohee',
    charset='utf8',
    autocommit=True
)

# ▶ POST /status
# 아두이노가 상태 정보 전송


@app.route('/status', methods=['POST'])
def post_status():
    data = request.get_json()

    temperature = data.get("temperature")
    fan = data.get("fan")
    heater = data.get("heater")

    if temperature is None or fan is None or heater is None:
        return jsonify({"error": "잘못된 요청"}), 400

    try:
        with db.cursor() as cursor:
            sql = """
                INSERT INTO status (temperature, fan, heater)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (temperature, fan, heater))
        return jsonify({"message": "상태 저장 완료"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ▶ GET /setting
# 아두이노가 설정 온도를 받아감
@app.route('/setting', methods=['GET'])
def get_setting():
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT temperature FROM setting ORDER BY temperature DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                return jsonify({"temperature": row[0]}), 200
            else:
                return jsonify({"temperature": -1}), 200  # 기본값: 장치 OFF
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ▶ POST /setting
# 사용자 또는 앱이 설정 온도 전송
@app.route('/setting', methods=['POST'])
def post_setting():
    data = request.get_json()
    new_temp = data.get("temperature")

    if new_temp is None:
        return jsonify({"error": "온도 값 누락"}), 400

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO setting (temperature) VALUES (%s)"
            cursor.execute(sql, (new_temp,))
        return jsonify({"message": "온도 설정 완료"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
