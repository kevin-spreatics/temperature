import pymysql
from flask import Flask, request
from pymysql.cursors import DictCursor

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
       host='database-1.cts2qeeg0ot5.ap-northeast-2.rds.amazonaws.com',
        user='kevin',
        password='spreatics*',
        db='temperature_sohee',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 상태 전달
@app.route('/status', methods=['POST'])
def cur_status():
    data =  request.get_json()

    temperature = data['temperature']
    fan = data['fan']
    heater = data['heater']

    conn = get_connection()

    with conn.cursor() as cursor:
        try:
            sql = """
            INSERT INTO status (temperature, fan, heater)
                values (%s,%s,%s)
            """
            cursor.execute(sql, (temperature,fan,heater))
            conn.commit()


        except pymysql.err.IntegrityError as e:
            return {"status" : "failed", "reason" : str(e) }
    conn.close()

    return {
            "status": "success",
            "temperature" : temperature
    }

            


# 온도 설정

## 사용자 
@app.route('/setting', methods=['POST'])
def set_temp():
    data = request.get_json()
    temperature = data['temperature']

    conn = get_connection()
    with conn.cursor() as cursor:
        try:
            sql = "UPDATE setting SET temperature = %s"
            cursor.execute(sql, (temperature,))
            conn.commit()

        except pymysql.err.IntegrityError as e:
            return {"status" : "failed", "reason" : str(e) }
    conn.close()

    return {
            "status": "success",
            "temperature" : temperature
    }

## 아두이노
@app.route('/setting', methods=['GET'])
def get_setting():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            
            sql = "SELECT temperature FROM setting"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result:
                temperature = result['temperature']
            else:
                temperature = -1   # 기본값 (-1) 반환

    except pymysql.err.IntegrityError as e:
            return {"status" : "failed", "reason" : str(e) }

    conn.close()

    return {
        "status": "success",
        "temperature": temperature
    }

app.run(debug=True, host='0.0.0.0', port=5001)