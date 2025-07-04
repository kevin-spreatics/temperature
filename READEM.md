# 온도조절 API

## 상태 전달하기
1. Endpoint
   - POST / status
2. Request body 
   - temperature (float) : 현재 온도
   - fan (boolean) : 팬 상태 (true: ON, false: OFF)
   - heater (boolean) : 히터 상태 (true: ON, false: OFF)
~~~
{
  "temperature": "25.5",
  "fan": "flase",
  "heater": "true"
}
~~~
3. Description
   - 아두이노가 현 상태를 서버에 전달
   - 아두이노가 주기적으로 호출하여 최신 상태 업데이트
4. Response body
   - status (string): success, failed
   - reason (string): 실패 시, 실패 원인
~~~
{
  "status": "success",
  "temperature" : 25.5
}
{
  "status": "failed",
  "reason": "invalid request body"
}
~~~

## 온도 설정하기 

### 사용자
1. Endpoint
   - POST / setting
2. Request body 
   - temperature (float) : 설정 온도
~~~
{
  "temperature": "24.8"
}
~~~
3. Description
   - 사용자가 설정한 온도를 서버에 저장
   - 아두이노가 새로운 설정값 
4. Response body
   - status (string): success, failed
   - reason (string): 실패 시, 실패 원인
~~~
{
  "status": "success"
}
{
  "status": "failed",
  "reason": "invalid request body"
}
~~~

### 아두이노
1. Endpoint
   - GET / setting
2. Request body 
   - 없음

3. Description
   - 아두이노가 현재 설정 온도를 가져감
   - 만약 Tempterature가 -1이면 fan,heater OFF
4. Response body
   - status (string): success, failed
   - temperature (float) : 설정된 목표 온도
   - reason (string): 실패 시, 실패 원인
~~~
{
  "status": "success",
  "temperature" : "24.8"
}
{
  "status": "failed",
  "reason": "server ERROR"
}
~~~


