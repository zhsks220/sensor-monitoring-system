# 프로젝트 요약

## 📌 프로젝트 정보

**프로젝트명:** 산업용 센서 데이터 모니터링 시스템  
**개발 기간:** 2024.11 ~ 2024.12 (1개월)  
**개발자:** [Your Name]  
**역할:** Full-stack Developer  

## 🎯 프로젝트 목표

산업 현장의 다양한 센서로부터 실시간으로 데이터를 수집하고, 
웹 대시보드를 통해 모니터링하며, 임계값 초과 시 자동으로 알람을 
발생시키는 웹 기반 모니터링 시스템 구축

## 💻 기술 스택

### Backend
- **Python 3.10+**
- **Django 4.2.7** - 웹 프레임워크
- **PostgreSQL 14+** - 관계형 데이터베이스
- **Django ORM** - 데이터베이스 ORM

### Frontend
- **HTML5 / CSS3** - 구조 및 스타일링
- **JavaScript (Vanilla)** - 동적 기능
- **Chart.js** - 데이터 시각화 라이브러리

### 통신 프로토콜
- **REST API** - 센서 데이터 수집
- **JSON** - 데이터 포맷

## 🏗 시스템 아키텍처

```
[센서 장비] → [REST API] → [Django Backend] → [PostgreSQL DB]
                                    ↓
                            [Web Dashboard]
                                    ↓
                            [알람 시스템]
```

## 📊 주요 기능

### 1. 센서 관리
- 센서 등록, 수정, 삭제
- 센서 타입: 온도, 습도, 압력, 가스
- 센서 상태 관리: 정상, 경고, 오류, 오프라인

### 2. 실시간 데이터 수집
- REST API를 통한 센서 데이터 수신
- 시계열 데이터 저장 (timestamp 기반)
- 데이터 품질 관리 (0-100%)

### 3. 웹 대시보드
- 전체 센서 현황 표시
- 센서별 실시간 데이터 모니터링
- 통계 카드 (전체 센서, 활성 알람, 시스템 상태)

### 4. 자동 알람 시스템
- 임계값 기반 자동 알람 생성
- 알람 심각도: 낮음, 보통, 높음, 심각
- 알람 상태 관리: 활성, 확인됨, 해결됨

### 5. 통계 분석
- 센서 타입별 평균값 계산
- 24시간 데이터 통계
- 활성 알람 카운트

## 📁 프로젝트 구조

```
sensor-monitoring-system/
├── config/                 # Django 설정
│   ├── settings.py        # 프로젝트 설정
│   ├── urls.py            # URL 라우팅
│   └── wsgi.py            # WSGI 설정
├── monitoring/            # 모니터링 앱
│   ├── models.py         # 데이터 모델
│   ├── views.py          # 뷰 로직
│   ├── urls.py           # 앱 URL
│   └── admin.py          # 관리자 페이지
├── templates/            # HTML 템플릿
│   └── dashboard.html    # 대시보드
├── requirements.txt      # 의존성
├── README.md            # 프로젝트 문서
├── INSTALLATION.md      # 설치 가이드
└── API_USAGE.md        # API 사용법
```

## 🔌 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | `/api/sensors/` | 센서 목록 조회 |
| GET | `/api/sensors/<id>/` | 센서 상세 정보 |
| POST | `/api/data/receive/` | 센서 데이터 수신 |
| GET | `/api/alerts/` | 알람 목록 조회 |
| GET | `/api/statistics/` | 시스템 통계 |

## 💾 데이터베이스 설계

### 테이블 구조

1. **sensors** - 센서 정보
   - sensor_id, name, type, location, status

2. **sensor_data** - 센서 데이터 (시계열)
   - sensor_id, value, unit, timestamp, quality

3. **alerts** - 알람 정보
   - sensor_id, severity, status, threshold, actual_value

## 🎨 UI/UX 특징

- **반응형 디자인** - Grid Layout 활용
- **직관적인 색상 구분**
  - 정상: 초록색
  - 경고: 주황색
  - 오류: 빨간색
  - 오프라인: 회색
- **실시간 업데이트** - 3초마다 통계 갱신
- **카드 기반 레이아웃** - 정보 구조화

## 🚀 성능 최적화

- **데이터베이스 인덱싱** - timestamp, sensor_id 인덱스
- **쿼리 최적화** - Django ORM select_related, prefetch_related
- **최근 데이터 제한** - 24시간 이내 데이터만 표시

## 🔒 보안 고려사항

- **환경 변수 관리** - .env 파일로 민감 정보 분리
- **CSRF 보호** - Django 기본 CSRF 미들웨어
- **입력 검증** - 센서 데이터 validation

## 📈 향후 개선 계획

1. **실시간 차트** - Chart.js 통합
2. **WebSocket** - 실시간 양방향 통신
3. **Excel 리포트** - 데이터 내보내기
4. **사용자 인증** - 로그인 및 권한 관리
5. **모바일 최적화** - 모바일 반응형 개선
6. **알람 알림** - 이메일/SMS 알림
7. **TimescaleDB** - 시계열 데이터 최적화

## 📝 개발 회고

### 잘한 점
- Django 프레임워크로 빠른 개발
- RESTful API 설계로 확장성 확보
- 직관적인 UI/UX 디자인

### 개선할 점
- 실시간 차트 미구현
- 테스트 코드 부족
- API 인증 미적용

### 배운 점
- Django ORM 활용법
- 시계열 데이터 처리
- REST API 설계 원칙
- 웹 대시보드 구현 경험

## 📞 연락처

- **GitHub**: [Repository Link]
- **Email**: your.email@example.com
- **Portfolio**: [Portfolio Link]
