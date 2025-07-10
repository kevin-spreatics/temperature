from flask import Flask, request, jsonify
import pymysql

def get_connection():
    return pymysql.connect(
        host="database-1.cts2qeeg0ot5.ap-northeast-2.rds.amazonaws.com",
        user="kevin",
        db="temperature_choi",
        password="spreatics*",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

app = Flask(__name__)
# 아두이노 센서 값을 읽어와 DB로 보내기
@app.route('/status', methods=['POST'])
def temp_status():
    data = request.get_json()

    temperature = data['temperature']
    fan = data['fan']
    heater = data['heater']

    if((temperature is None) or (fan is None) or (heater is None)):
        return jsonify({"result": "failed", "reason": "Data is not entered."})
    
    conn = get_connection()

    with conn.cursor() as cursor:
        sql = """insert into status(temperature, fan, heater) 
                 values (%s, %s, %s);"""
        cursor.execute(sql, (temperature, fan, heater))
        conn.commit()

    with conn.cursor() as cursor:
        sql = """select *
                 from status
                 order by time desc
                 limit 1;"""
        cursor.execute(sql)

        rows = cursor.fetchall()

        return jsonify({"result": "Entered", "time": rows[0]['time']})
    
# 사용자가 온도 설정하기
@app.route('/setting', methods=['POST'])
def user_temp_set():
    data = request.get_json()

    temperature = data['temperature']

    if(temperature is None):
        return jsonify({"result": "failed", "reason": "Put setting temperature."})
    
    conn = get_connection()

    with conn.cursor() as cursor:
        sql = """insert into setting(temperature) 
                 values(%s);"""
        cursor.execute(sql, (temperature, ))
        conn.commit()

        return jsonify({"result": "Entered", "temperature": temperature})
    
# 아두이노가 설정된 온도를 가져오기
@app.route('/setting')
def get_set_temp():
    conn = get_connection()

    with conn.cursor() as cursor:
        sql = """select *
                 from setting
                 order by set_time desc
                 limit 1;"""
        cursor.execute(sql)

        rows = cursor.fetchall()

        return jsonify({"result": "selected", "temperature": rows[0]['temperature']})
    
app.run(debug=True, host='0.0.0.0', port=5000)