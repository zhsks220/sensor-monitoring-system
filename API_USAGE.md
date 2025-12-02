# API 사용 가이드

## 개요

이 문서는 센서 모니터링 시스템의 REST API 사용법을 설명합니다.

## Base URL

```
http://localhost:8000
```

## 인증

현재 버전은 인증이 필요하지 않습니다. (개발 단계)

## API 엔드포인트

### 1. 센서 목록 조회

**Endpoint:** `GET /api/sensors/`

**응답 예시:**
```json
{
  "sensors": [
    {
      "id": 1,
      "sensor_id": "TEMP001",
      "name": "1호기 온도센서",
      "type": "temperature",
      "location": "A동 1층",
      "status": "active"
    }
  ]
}
```

### 2. 센서 상세 정보 조회

**Endpoint:** `GET /api/sensors/<sensor_id>/`

**예시:** `GET /api/sensors/TEMP001/`

**응답:**
```json
{
  "sensor": {
    "id": 1,
    "sensor_id": "TEMP001",
    "name": "1호기 온도센서",
    "type": "temperature",
    "location": "A동 1층",
    "status": "active"
  },
  "recent_data": [
    {
      "timestamp": "2024-12-01T10:30:00Z",
      "value": 25.5,
      "unit": "°C"
    }
  ]
}
```

### 3. 센서 데이터 전송

**Endpoint:** `POST /api/data/receive/`

**요청 헤더:**
```
Content-Type: application/json
```

**요청 Body:**
```json
{
  "sensor_id": "TEMP001",
  "value": 25.5,
  "unit": "°C",
  "quality": 100,
  "remarks": ""
}
```

**응답 (성공):**
```json
{
  "status": "success",
  "message": "Data received successfully",
  "data_id": 123
}
```

**응답 (실패):**
```json
{
  "status": "error",
  "message": "Sensor not found"
}
```

### 4. 알람 목록 조회

**Endpoint:** `GET /api/alerts/`

**쿼리 파라미터:**
- `status`: active, acknowledged, resolved (기본값: active)

**예시:** `GET /api/alerts/?status=active`

**응답:**
```json
{
  "alerts": [
    {
      "id": 1,
      "sensor_name": "1호기 온도센서",
      "severity": "high",
      "status": "active",
      "title": "온도 과다",
      "message": "현재 온도: 35°C (임계값: 30°C)",
      "created_at": "2024-12-01T10:30:00Z"
    }
  ]
}
```

### 5. 통계 조회

**Endpoint:** `GET /api/statistics/`

**응답:**
```json
{
  "total_sensors": 10,
  "active_sensors": 9,
  "total_data_points": 1234,
  "active_alerts": 2,
  "sensor_types": [
    {
      "type": "temperature",
      "name": "온도",
      "count": 5,
      "avg_value": 25.3
    }
  ]
}
```

## Python 클라이언트 예시

### 센서 데이터 전송

```python
import requests
import time
import random

API_URL = "http://localhost:8000/api/data/receive/"

def send_sensor_data(sensor_id, value, unit):
    data = {
        "sensor_id": sensor_id,
        "value": value,
        "unit": unit,
        "quality": 100
    }
    
    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        print(f"✅ {result['message']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# 예시: 5초마다 온도 데이터 전송
while True:
    temp = random.uniform(20, 30)
    send_sensor_data("TEMP001", temp, "°C")
    time.sleep(5)
```

### 알람 모니터링

```python
import requests
import time

API_URL = "http://localhost:8000/api/alerts/"

def check_alerts():
    try:
        response = requests.get(API_URL, params={"status": "active"})
        data = response.json()
        
        alerts = data.get('alerts', [])
        if alerts:
            print(f"🚨 활성 알람: {len(alerts)}개")
            for alert in alerts:
                print(f"  - [{alert['severity']}] {alert['title']}")
        else:
            print("✅ 활성 알람 없음")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# 10초마다 알람 체크
while True:
    check_alerts()
    time.sleep(10)
```

## cURL 예시

### 데이터 전송
```bash
curl -X POST http://localhost:8000/api/data/receive/ \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "TEMP001",
    "value": 25.5,
    "unit": "°C"
  }'
```

### 센서 목록 조회
```bash
curl http://localhost:8000/api/sensors/
```

### 알람 조회
```bash
curl "http://localhost:8000/api/alerts/?status=active"
```
