from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    # 웹 페이지
    path('', views.dashboard, name='dashboard'),
    
    # API 엔드포인트
    path('api/sensors/', views.sensor_list, name='sensor_list'),
    path('api/sensors/<str:sensor_id>/', views.sensor_detail, name='sensor_detail'),
    path('api/data/receive/', views.receive_sensor_data, name='receive_data'),
    path('api/alerts/', views.alert_list, name='alert_list'),
    path('api/statistics/', views.statistics, name='statistics'),
]
