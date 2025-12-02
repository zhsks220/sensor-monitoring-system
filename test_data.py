import os
import sys
import django

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from monitoring.models import Sensor, SensorData, Alert
from django.utils import timezone
import random

print("테스트 데이터 생성 시작...")

# 기존 데이터 삭제
Sensor.objects.all().delete()
print("기존 데이터 삭제 완료")

# 센서 생성
sensors_data = [
    {"sensor_id": "TEMP001", "name": "1호기 온도센서", "sensor_type": "temperature", "location": "A동 1층"},
    {"sensor_id": "TEMP002", "name": "2호기 온도센서", "sensor_type": "temperature", "location": "A동 2층"},
    {"sensor_id": "HUM001", "name": "1호기 습도센서", "sensor_type": "humidity", "location": "B동 1층"},
    {"sensor_id": "PRES001", "name": "압력센서", "sensor_type": "pressure", "location": "C동"},
    {"sensor_id": "GAS001", "name": "가스센서", "sensor_type": "gas", "location": "D동"},
]

sensors = []
for data in sensors_data:
    sensor = Sensor.objects.create(**data)
    sensors.append(sensor)
    print(f"센서 생성: {sensor.name}")

# 센서 데이터 생성
print("\n센서 데이터 생성 중...")
for sensor in sensors:
    for i in range(10):
        if sensor.sensor_type == 'temperature':
            value = random.uniform(20, 35)
            unit = '°C'
        elif sensor.sensor_type == 'humidity':
            value = random.uniform(40, 85)
            unit = '%'
        elif sensor.sensor_type == 'pressure':
            value = random.uniform(950, 1050)
            unit = 'hPa'
        else:
            value = random.uniform(0, 100)
            unit = 'ppm'
        
        SensorData.objects.create(
            sensor=sensor,
            value=value,
            unit=unit,
            quality=random.randint(90, 100)
        )
    print(f"{sensor.name}: 10개 데이터 생성")

# 알람 생성
print("\n테스트 알람 생성 중...")
temp_sensor = sensors[0]
Alert.objects.create(
    sensor=temp_sensor,
    severity='high',
    title=f'{temp_sensor.name} 온도 과다',
    message=f'현재 온도: 32.5°C (임계값: 30°C)',
    threshold_value=30.0,
    actual_value=32.5
)
print("테스트 알람 생성 완료")

print("\n" + "="*50)
print("테스트 데이터 생성 완료!")
print("="*50)
print(f"센서: {Sensor.objects.count()}개")
print(f"센서 데이터: {SensorData.objects.count()}개")
print(f"알람: {Alert.objects.count()}개")
print("\n브라우저에서 확인: http://localhost:8000")
