# REST API Spec.
- version 0.0 (2025/7/04)
## 상태 정보 전달
1. Endpoint
   - POST /status
2. Request body 
   - temperature(float): 온도, 필수
   - fan(bool) : 팬 ,필수
   - heater(bool): 히터, 필수
~~~
{
  "temperature": 25,
  "heater": False,
  "fan": False
}
~~~
3. Description
  - 현재 온도와 팬과 히터의 on/off 상태 전달
4. response
  - status : 성공/실패

# 온도 설정하기
## 서버에서 온도 가져오기
1. Endpoint
  - GET/setting
2.  Request body
3.  Description
  - 서버가 가지고 있는 온도 정보를 가지고 온다
  - temperature가 -1이면 fan, heater를 끈다
4. response body
  - temperature(float)
  - fan (bool)
  - heater(bool)

## 사용자가 온도 설정하기
1. Endpoint
  - Post/setting
