# 🔬 산업용 센서 데이터 모니터링 시스템

Python/Django 기반의 실시간 산업용 센서 데이터 수집 및 모니터링 웹 애플리케이션

## 📋 프로젝트 개요

이 프로젝트는 산업 현장의 다양한 센서(온도, 습도, 압력, 가스 등)로부터 데이터를 수집하고, 
실시간으로 모니터링하며, 임계값 초과 시 자동으로 알람을 발생시키는 시스템입니다.

### 주요 기능

- ✅ **실시간 센서 데이터 수집** - REST API를 통한 센서 데이터 수신
- ✅ **대시보드 모니터링** - 센서 상태 및 데이터 실시간 표시
- ✅ **자동 알람 시스템** - 임계값 초과 시 자동 알람 생성
- ✅ **센서 관리** - 센서 등록, 수정, 삭제 기능
- ✅ **통계 분석** - 센서 타입별 평균값 및 통계 제공
- ✅ **관리자 페이지** - Django Admin을 통한 데이터 관리

## 🛠 기술 스택

### Backend
- **Python 3.10+**
- **Django 4.2.7** - 웹 프레임워크
- **PostgreSQL 14+** - 데이터베이스

### Frontend
- **HTML5 / CSS3** - 반응형 웹 디자인
- **JavaScript (Vanilla)** - 실시간 데이터 업데이트
- **Chart.js** - 데이터 시각화 (예정)

### 기타
- **Django CORS Headers** - API CORS 설정
- **python-dotenv** - 환경 변수 관리

## 📂 프로젝트 구조

```
sensor-monitoring-system/
├── config/                 # Django 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── monitoring/             # 모니터링 앱
│   ├── models.py          # 데이터 모델 (Sensor, SensorData, Alert)
│   ├── views.py           # API 및 웹 뷰
│   ├── urls.py            # URL 라우팅
│   └── admin.py           # 관리자 페이지 설정
├── templates/             # HTML 템플릿
│   └── dashboard.html     # 메인 대시보드
├── manage.py              # Django 관리 명령
├── requirements.txt       # Python 패키지 목록
└── .env.example          # 환경 변수 예시
```

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/zhsks220/sensor-monitoring-system.git
cd sensor-monitoring-system
```

### 2. 가상환경 생성 및 활성화
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 열어서 데이터베이스 정보 입력
```

`.env` 파일 예시:
```
DB_NAME=sensor_monitoring
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. PostgreSQL 데이터베이스 생성
```sql
CREATE DATABASE sensor_monitoring;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE sensor_monitoring TO postgres;
```

### 6. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. 관리자 계정 생성
```bash
python manage.py createsuperuser
```

### 8. 서버 실행
```bash
python manage.py runserver
```

접속: http://localhost:8000

## 📊 데이터 모델

### Sensor (센서)
- `sensor_id`: 센서 고유 ID
- `name`: 센서 이름
- `sensor_type`: 센서 타입 (temperature, humidity, pressure, gas)
- `location`: 설치 위치
- `status`: 상태 (active, warning, error, offline)

### SensorData (센서 데이터)
- `sensor`: 센서 참조
- `value`: 측정값
- `unit`: 단위
- `timestamp`: 측정 시간
- `quality`: 데이터 품질 (0-100%)

### Alert (알람)
- `sensor`: 센서 참조
- `severity`: 심각도 (low, medium, high, critical)
- `status`: 상태 (active, acknowledged, resolved)
- `title`: 알람 제목
- `message`: 알람 메시지
- `threshold_value`: 임계값
- `actual_value`: 실제 측정값

## 🔌 API 엔드포인트

### 센서 관리
- `GET /api/sensors/` - 센서 목록 조회
- `GET /api/sensors/<sensor_id>/` - 센서 상세 정보 및 최근 데이터

### 데이터 수집
- `POST /api/data/receive/` - 센서 데이터 수신

**요청 예시:**
```json
{
    "sensor_id": "TEMP001",
    "value": 25.5,
    "unit": "°C",
    "quality": 100,
    "remarks": ""
}
```

### 알람
- `GET /api/alerts/` - 알람 목록 조회
- `GET /api/alerts/?status=active` - 활성 알람만 조회

### 통계
- `GET /api/statistics/` - 전체 시스템 통계

## 🎯 사용 시나리오

### 1. 센서 등록
관리자 페이지에서 새로운 센서를 등록합니다.

### 2. 데이터 수신
외부 센서 장비에서 API를 통해 데이터를 전송합니다.
```python
import requests

data = {
    "sensor_id": "TEMP001",
    "value": 28.5,
    "unit": "°C"
}

response = requests.post(
    "http://localhost:8000/api/data/receive/",
    json=data
)
```

### 3. 실시간 모니터링
대시보드에서 센서 상태와 데이터를 실시간으로 확인합니다.

### 4. 알람 확인
임계값 초과 시 자동 생성된 알람을 확인하고 조치합니다.

## ⚙️ 설정

### 알람 임계값 설정
`monitoring/views.py`의 `check_alert_threshold` 함수에서 임계값을 설정할 수 있습니다.

```python
# 온도 센서: 30도 이상 경고
if sensor.sensor_type == 'temperature' and sensor_data.value > 30:
    Alert.objects.create(...)

# 습도 센서: 80% 이상 경고
elif sensor.sensor_type == 'humidity' and sensor_data.value > 80:
    Alert.objects.create(...)
```

## 📸 스크린샷

### 메인 대시보드
- 전체 센서 현황 카드
- 센서별 실시간 데이터 표시
- 활성 알람 목록

### 관리자 페이지
- 센서 등록 및 관리
- 센서 데이터 조회
- 알람 관리

## 🔧 개발 로드맵

- [x] 기본 센서 모델 및 데이터 수집
- [x] 대시보드 UI
- [x] 알람 시스템
- [ ] Chart.js 실시간 차트 구현
- [ ] WebSocket 실시간 업데이트
- [ ] Excel 리포트 생성
- [ ] 사용자 권한 관리
- [ ] 모바일 반응형 개선

## 🤝 기여

프로젝트 개선을 위한 제안이나 버그 리포트는 언제나 환영합니다!

## 📄 라이선스

MIT License

## 👤 개발자

- **GitHub**: [@zhsks220](https://github.com/zhsks220)

## 🙏 프로젝트 소개

산업 현장의 온도, 습도, 압력, 가스 센서 데이터를 실시간으로 수집하고 모니터링하는 시스템입니다.

---

**개발 기간**: 2025.12 (1주)  
**주요 기술**: Python, Django, PostgreSQL, JavaScript  
**프로젝트 타입**: 실시간 모니터링 시스템
