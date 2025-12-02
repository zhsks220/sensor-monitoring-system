from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Avg, Max, Min, Count
from datetime import timedelta
import json
from .models import Sensor, SensorData, Alert


def dashboard(request):
    """메인 대시보드"""
    time_24h_ago = timezone.now() - timedelta(hours=24)

    sensors = Sensor.objects.all()
    alerts = Alert.objects.filter(status='active').order_by('-created_at')[:10]

    # 각 센서에 최신 데이터 추가
    for sensor in sensors:
        latest_data = SensorData.objects.filter(sensor=sensor).order_by('-timestamp').first()
        if latest_data:
            sensor.latest_value = latest_data.value
            sensor.latest_unit = latest_data.unit
        else:
            sensor.latest_value = None
            sensor.latest_unit = None

    # 센서 타입별 카운트
    temp_count = Sensor.objects.filter(sensor_type='temperature').count()
    humidity_count = Sensor.objects.filter(sensor_type='humidity').count()
    pressure_count = Sensor.objects.filter(sensor_type='pressure').count()
    gas_count = Sensor.objects.filter(sensor_type='gas').count()

    context = {
        'sensors': sensors,
        'alerts': alerts,
        'active_count': Sensor.objects.filter(status='active').count(),
        'data_count': SensorData.objects.filter(timestamp__gte=time_24h_ago).count(),
        'temp_count': temp_count or 1,
        'humidity_count': humidity_count or 1,
        'pressure_count': pressure_count or 1,
        'gas_count': gas_count or 1,
    }
    return render(request, 'dashboard.html', context)


def sensor_list(request):
    """센서 목록 API"""
    sensors = Sensor.objects.all()
    data = [{
        'id': s.id,
        'sensor_id': s.sensor_id,
        'name': s.name,
        'type': s.sensor_type,
        'location': s.location,
        'status': s.status,
    } for s in sensors]
    return JsonResponse({'sensors': data})


def sensor_detail(request, sensor_id):
    """센서 상세 정보 API"""
    sensor = get_object_or_404(Sensor, sensor_id=sensor_id)
    
    # 최근 24시간 데이터
    time_24h_ago = timezone.now() - timedelta(hours=24)
    recent_data = SensorData.objects.filter(
        sensor=sensor,
        timestamp__gte=time_24h_ago
    ).order_by('-timestamp')[:100]
    
    data = {
        'sensor': {
            'id': sensor.id,
            'sensor_id': sensor.sensor_id,
            'name': sensor.name,
            'type': sensor.sensor_type,
            'location': sensor.location,
            'status': sensor.status,
        },
        'recent_data': [{
            'timestamp': d.timestamp.isoformat(),
            'value': d.value,
            'unit': d.unit,
        } for d in recent_data]
    }
    return JsonResponse(data)


@csrf_exempt
def receive_sensor_data(request):
    """센서 데이터 수신 API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor = get_object_or_404(Sensor, sensor_id=data['sensor_id'])
            
            # 센서 데이터 저장
            sensor_data = SensorData.objects.create(
                sensor=sensor,
                value=float(data['value']),
                unit=data.get('unit', ''),
                quality=data.get('quality', 100),
                remarks=data.get('remarks', '')
            )
            
            # 알람 체크
            check_alert_threshold(sensor, sensor_data)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Data received successfully',
                'data_id': sensor_data.id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)


def check_alert_threshold(sensor, sensor_data):
    """임계값 체크 및 알람 생성"""
    # 온도 센서 예시: 30도 이상이면 경고
    if sensor.sensor_type == 'temperature' and sensor_data.value > 30:
        Alert.objects.create(
            sensor=sensor,
            severity='high',
            title=f'{sensor.name} 온도 과다',
            message=f'현재 온도: {sensor_data.value}°C (임계값: 30°C)',
            threshold_value=30.0,
            actual_value=sensor_data.value
        )
    
    # 습도 센서 예시: 80% 이상이면 경고
    elif sensor.sensor_type == 'humidity' and sensor_data.value > 80:
        Alert.objects.create(
            sensor=sensor,
            severity='medium',
            title=f'{sensor.name} 습도 과다',
            message=f'현재 습도: {sensor_data.value}% (임계값: 80%)',
            threshold_value=80.0,
            actual_value=sensor_data.value
        )


def alert_list(request):
    """알람 목록 API"""
    status = request.GET.get('status', 'active')
    alerts = Alert.objects.filter(status=status).order_by('-created_at')[:50]
    
    data = [{
        'id': a.id,
        'sensor_name': a.sensor.name,
        'severity': a.severity,
        'status': a.status,
        'title': a.title,
        'message': a.message,
        'created_at': a.created_at.isoformat(),
    } for a in alerts]
    
    return JsonResponse({'alerts': data})


def statistics(request):
    """통계 데이터 API"""
    time_24h_ago = timezone.now() - timedelta(hours=24)
    
    stats = {
        'total_sensors': Sensor.objects.count(),
        'active_sensors': Sensor.objects.filter(status='active').count(),
        'total_data_points': SensorData.objects.filter(timestamp__gte=time_24h_ago).count(),
        'active_alerts': Alert.objects.filter(status='active').count(),
    }
    
    # 센서 타입별 통계
    sensor_type_stats = []
    for sensor_type, name in Sensor.SENSOR_TYPES:
        sensors = Sensor.objects.filter(sensor_type=sensor_type)
        if sensors.exists():
            recent_avg = SensorData.objects.filter(
                sensor__sensor_type=sensor_type,
                timestamp__gte=time_24h_ago
            ).aggregate(avg_value=Avg('value'))
            
            sensor_type_stats.append({
                'type': sensor_type,
                'name': name,
                'count': sensors.count(),
                'avg_value': round(recent_avg['avg_value'] or 0, 2)
            })
    
    stats['sensor_types'] = sensor_type_stats
    
    return JsonResponse(stats)
