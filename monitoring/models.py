from django.db import models
from django.utils import timezone


class Sensor(models.Model):
    """센서 정보 모델"""
    SENSOR_TYPES = [
        ('temperature', '온도'),
        ('humidity', '습도'),
        ('pressure', '압력'),
        ('gas', '가스'),
    ]
    
    STATUSES = [
        ('active', '정상'),
        ('warning', '경고'),
        ('error', '오류'),
        ('offline', '오프라인'),
    ]
    
    sensor_id = models.CharField(max_length=50, unique=True, verbose_name='센서 ID')
    name = models.CharField(max_length=100, verbose_name='센서 이름')
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES, verbose_name='센서 타입')
    location = models.CharField(max_length=200, verbose_name='설치 위치')
    status = models.CharField(max_length=20, choices=STATUSES, default='active', verbose_name='상태')
    description = models.TextField(blank=True, verbose_name='설명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        db_table = 'sensors'
        verbose_name = '센서'
        verbose_name_plural = '센서 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.sensor_id})"


class SensorData(models.Model):
    """센서 데이터 모델 (시계열 데이터)"""
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='data', verbose_name='센서')
    value = models.FloatField(verbose_name='측정값')
    unit = models.CharField(max_length=20, verbose_name='단위')
    timestamp = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='측정 시간')
    quality = models.IntegerField(default=100, verbose_name='데이터 품질 (%)')
    remarks = models.TextField(blank=True, verbose_name='비고')
    
    class Meta:
        db_table = 'sensor_data'
        verbose_name = '센서 데이터'
        verbose_name_plural = '센서 데이터 목록'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.sensor.name} - {self.value}{self.unit} at {self.timestamp}"


class Alert(models.Model):
    """알람 모델"""
    SEVERITY_LEVELS = [
        ('low', '낮음'),
        ('medium', '보통'),
        ('high', '높음'),
        ('critical', '심각'),
    ]
    
    ALERT_STATUSES = [
        ('active', '활성'),
        ('acknowledged', '확인됨'),
        ('resolved', '해결됨'),
    ]
    
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='alerts', verbose_name='센서')
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, verbose_name='심각도')
    status = models.CharField(max_length=20, choices=ALERT_STATUSES, default='active', verbose_name='상태')
    title = models.CharField(max_length=200, verbose_name='제목')
    message = models.TextField(verbose_name='메시지')
    threshold_value = models.FloatField(verbose_name='임계값')
    actual_value = models.FloatField(verbose_name='실제값')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='발생 시간')
    acknowledged_at = models.DateTimeField(null=True, blank=True, verbose_name='확인 시간')
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='해결 시간')
    
    class Meta:
        db_table = 'alerts'
        verbose_name = '알람'
        verbose_name_plural = '알람 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"[{self.severity}] {self.title}"
