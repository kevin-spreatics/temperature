from flask import Flask, request, jsonify
import pymysql
from datetime import datetime 
import time
app = Flask(__name__)
def get_connection():
    return pymysql.connect(
        host='database-1.cts2qeeg0ot5.ap-northeast-2.rds.amazonaws.com',
        user='kevin',
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
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO status_log (temperature, fan, heater) VALUES (%s, %s, %s)",
                (temperature, fan, heater)
            )
        conn.commit()
        return {"status": "success"}
    finally :
        conn.close()
@app.route('/setting', methods=['GET'])
def get_setting():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 가장 최근 온도 1개만 가져오기
            cursor.execute("SELECT temperature FROM setting ORDER BY created_at DESC LIMIT 1")
            row = cursor.fetchone()
            temp = row['temperature']
            if temp == -1:
                return {
                    "temperature": -1,
                    "fan": False,
                    "heater": False
                }
            else:
                return {
                    "temperature": temp
                }
    finally:
        conn.close()
#3. 사용자가 온도 설정하기 
@app.route('/setting', methods=['POST'])
def set_setting():
    data = request.get_json()
    temperature = data.get('temperature')
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO setting (temperature) VALUES (%s)",
                (temperature,)
            )
        conn.commit()
        return {
            "status": "success",
            "temperature": temperature
        }
    finally :
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port = 5000, host = "0.0.0.0" )

