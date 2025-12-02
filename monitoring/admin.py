from django.contrib import admin
from .models import Sensor, SensorData, Alert


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['sensor_id', 'name', 'sensor_type', 'location', 'status', 'created_at']
    list_filter = ['sensor_type', 'status', 'created_at']
    search_fields = ['sensor_id', 'name', 'location']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'value', 'unit', 'timestamp', 'quality']
    list_filter = ['sensor', 'timestamp']
    search_fields = ['sensor__name', 'sensor__sensor_id']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'severity', 'status', 'title', 'created_at']
    list_filter = ['severity', 'status', 'created_at']
    search_fields = ['sensor__name', 'title', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
