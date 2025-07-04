
## 아두이노 기반 온도 조절 장치와 서버 간 통신을 위한 REST API 명세서

<br>

```
• REST API 설계
  • 상태 정보 전달하기
    • POST /status
      • request body: { "temperature": xx, "fan": false, "heater": true }

  • 온도 설정하기
    • GET /setting
      • response body: { "temperature": yy }
        • 아두이노가 설정된 온도를 가져가기 위함
        • temperature 가 -1 이면, fan, heater 모두 끄기

  • POST /setting
    • request body: { "temperature": zz }
      • 사용자가 온도를 설정하기 위함
```
<br>

### 1. 상태 정보 전달 API
- POST /status
  - 설명: 아두이노가 현재 장치의 상태 정보를 서버로 전송
  - request body(요청 본문):
 ```
{
  "temperature": 26.7,
  "fan": true,
  "heater": false
}
```
| 필드명         | 타입      | 필수 | 설명             |
| ----------- | ------- | -- | -------------- |
| temperature | float   | ㅇ  | 현재 측정된 온도 (°C) |
| fan         | boolean | ㅇ  | 팬 작동 여부        |
| heater      | boolean | ㅇ  | 히터 작동 여부       |
  - response body(응답 본문):
```
{
  "message": "상태 정보 수신 완료"
}
```

<br>

### 2. 온도 설정 조회 API
- GET/setting
  - 설명 : 아두이노가 서버에서 설정된 목표 온도를 가져갈 때 사용
  - 요청 파라미터 : 없음
  - response body(응답 본문):
```
{
"temperture" : 24
}
```
| 필드명         | 타입  | 설명                          |
| ----------- | --- | --------------------------- |
| temperature | int | 설정된 목표 온도. -1이면 모두 off 신호 |

- GET /setting의 응답에서 "temperature": -1이면:
  - 아두이노는 팬과 히터를 모두 꺼야 함


<br>

### 3. 온도 설정 API
- POST /setting
  - 설명: 사용자가 웹/앱에서 목표 온도를 설정합니다.
  - request body(요청 본문):
```
{
  "temperature": 22
}
```
| 필드명         | 타입  | 필수 | 설명           |
| ----------- | --- | -- | ------------ |
| temperature | int | ㅇ  | 새로 설정할 목표 온도 |

  - response body(응답 본문):
```
{
  "message": "온도 설정 완료"
}
```

```
[사용자] → POST /setting → 서버에 설정 온도 저장

[아두이노] → GET /setting → 서버에서 설정 온도 받아옴

[아두이노] → POST /status → 현재 상태 서버에 보고
```















