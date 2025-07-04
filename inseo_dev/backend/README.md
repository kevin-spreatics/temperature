# REST API Spec.

- version 0.1 (2025/7/4)

# 상태 정보 전달하기

1. Endpoint

   - POST /status

2. Request body
   - temperature (int): 현재 온도, 필수
   - fan (bool): 팬의 작동 여부, 필수
   - heater (bool): 히터의 작동 여부, 필수

```
{
    "temperature": xx,
    "fan": false,
    "heater": true
}
```

3. Description

   - 현재 아두이노의 상태 정보를 서버에 보내준다.
   - 온도와 팬,히터의 작동여부는 필수 입력값이다.

4. Response body
   - status (string): success, failed
   - info (object): 전달한 정보들
     - temperature (int) : 현재 온도
     - fan (bool): 팬 작동여부
     - heater (bool): 히터 작동여부
   - reason (string): 실패 시, 실패 원인

```
{
    "status":"success",
    "info":{
        "temperature": xx,
        "fan": false,
        "heater": true
    }
}
```

```
{
    "status":"failed",
    "reason":"Temperature, fan, and heater are required inputs."
}
```

# 온도 설정하기

## 아두이노가 설정된 온도 가져오기

1. Endpoint

   - GET /setting

2. Request body

3. Description

   - 현재 설정된 온도를 가져온다.

4. Response body

   - status (string): success, failed
   - input_temperature (int) : 설정된 온도
   - reason (string): 실패 시, 실패 원인

```
{
    "status":"success",
    "input_temperature":yy
}
```

```
{
    "status":"failed",
    "reason":"..."
}
```

## 사용자가 온도 설정하기

1. Endpoint

   - POST /setting

2. Request body
   - temperature (int): 현재 온도, 필수

```
{
    "temperature": zz
}
```

3. Description

   - 사용자가 원하는 온도를 설정한다.
   - 온도는 필수 입력값이다.

4. Response body

   - status (string): success, failed
   - input_temperature (int) : 사용자 설정 온도
   - reason (string): 실패 시, 실패 원인

```
{
    "status":"success",
    "input_temperature":yy
}
```

```
{
    "status":"failed",
    "reason":"..."
}
```
