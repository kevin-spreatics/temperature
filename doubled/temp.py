from flask import Flask, request , jsonify
import pymysql
from datetime import datetime 
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

## 1. 상태 정보 전달하기
@app.route('/status', methods=['POST'])
def send_status():
    data = request.get_json()
    temperature = data.get('temperature')
    fan = data.get('fan')
    heater = data.get('heater')
    return { "temperature": temperature , "fan" : fan, "heater" : heater }
    

##2. 온도 설정하기
## 아두이노가 설정된 온도를 가져감
### temp 이 -1 이면 fan,heater 끄기
@app.route('/setting')
def getemp():
    data = request.get_json()
    temperature = data.get('temperature')    
    if temperature == -1:
        return {
            "temperature": -1,
            "fan": False,
            "heater": False
        }
    else:
        return {
            "temperature": temperature
        }

## 사용자가 온도를 설정함 
@app.route('/setting',method=['POST'])
def setemp():
    data = request.get_json()
    temperature = data.get('temperature')
    return {"message": "설정 완료", "temperature": temperature}