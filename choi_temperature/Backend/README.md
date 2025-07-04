# REST API 설계
## 상태 정보 전달하기
  1. Endpoint
     * POST / status
  2. Request body
     * temperature (int) : 내부 온도, 필수
     * fan (bool) : 팬 작동 상태, 필수
     * heater (bool) : 히터 작동 상태, 필수
~~~
{
  "temperature": 24,
  "fan": True,
  "heater": False
}
~~~
  3. Description
     * 아두이노가 센서로 내부 온도, 히터/팬 작동 유무를 읽어와서 보낸다.
  4. Response body
     * result (string): Entered, failed
     * time (string): 입력 성공 시, 데이터 입력 시간
     * reason (string): 입력 실패 시, 실패 원인
~~~
{
  "result": "Entered",
  "time": "2025-07-04, 13:04"
}
{
  "result": "failed",
  "reason": "Data is not Entered."
}
~~~

## 온도 설정하기
### 사용자가 온도를 설정하기
  1. Endpoint
     * POST / setting
  2. Request body
     * temperature (int) : 사용자가 설정할 온도, 필수
  3. Description
     * 사용자가 실내 온도를 설정한다.
     * 아두이노는 사용자가 설정한 온도를 읽고 fan/heater 작동 유무를 결정한다.
  4. Response body
     * result (string): Entered, failed
     * temperature (int): 입력 성공 시, 설정한 내부 온도
     * reason (string): 입력 실패 시, 실패 원인
~~~
{
  "result": "Entered",
  "temperature": 22
}
{
  "result": "failed",
  "reason": "Put setting temperature."
}
~~~

### 아두이노가 설정된 온도 가져가기
  1. Endpoint
     * GET / setting
  2. Request body
     * 없음
  3. Description
     * 아두이노가 내부 온도를 확인하고 팬과 히터 작동을 조절한다.
     * temperature가 -1 이면, fan/heater 모두 작동을 중지한다.
  4. Response body
     * result (string): selected
     * temperature (int): 내부 온도
~~~
{
  "result": "selected",
  "temperature": 20
}
~~~
