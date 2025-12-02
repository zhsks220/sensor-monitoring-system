import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

print("="*60)
print("API 테스트 시작")
print("="*60)

# 1. 센서 목록 조회
print("\n[테스트 1] GET /api/sensors/")
response = requests.get(f"{BASE_URL}/api/sensors/")
print(f"상태 코드: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"결과: 센서 {len(data['sensors'])}개 조회 성공")
    for sensor in data['sensors'][:2]:
        print(f"  - {sensor['name']} ({sensor['sensor_id']})")
else:
    print(f"실패: {response.text}")

# 2. 센서 상세 정보 조회
print("\n[테스트 2] GET /api/sensors/TEMP001/")
response = requests.get(f"{BASE_URL}/api/sensors/TEMP001/")
print(f"상태 코드: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"결과: {data['sensor']['name']} 상세 정보")
    print(f"  최근 데이터: {len(data['recent_data'])}개")
else:
    print(f"실패: {response.text}")

# 3. 센서 데이터 전송
print("\n[테스트 3] POST /api/data/receive/")
test_data = {
    "sensor_id": "TEMP001",
    "value": 28.5,
    "unit": "°C",
    "quality": 100
}
response = requests.post(
    f"{BASE_URL}/api/data/receive/",
    json=test_data,
    headers={"Content-Type": "application/json"}
)
print(f"상태 코드: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"결과: {data['message']}")
else:
    print(f"실패: {response.text}")

# 4. 알람 목록 조회
print("\n[테스트 4] GET /api/alerts/")
response = requests.get(f"{BASE_URL}/api/alerts/")
print(f"상태 코드: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"결과: 알람 {len(data['alerts'])}개")
    for alert in data['alerts']:
        print(f"  - [{alert['severity']}] {alert['title']}")
else:
    print(f"실패: {response.text}")

# 5. 통계 조회
print("\n[테스트 5] GET /api/statistics/")
response = requests.get(f"{BASE_URL}/api/statistics/")
print(f"상태 코드: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"결과:")
    print(f"  전체 센서: {data['total_sensors']}개")
    print(f"  활성 센서: {data['active_sensors']}개")
    print(f"  데이터 포인트: {data['total_data_points']}개")
    print(f"  활성 알람: {data['active_alerts']}개")
else:
    print(f"실패: {response.text}")

print("\n" + "="*60)
print("API 테스트 완료!")
print("="*60)
