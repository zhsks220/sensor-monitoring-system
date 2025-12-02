# 설치 가이드

## 시스템 요구사항

- Python 3.10 이상
- PostgreSQL 14 이상
- pip (Python 패키지 관리자)
- Git

## 상세 설치 단계

### 1. Python 설치 확인

```bash
python --version
# Python 3.10.0 이상이어야 함
```

Python이 설치되지 않았다면: https://www.python.org/downloads/

### 2. PostgreSQL 설치 및 설정

#### Windows
1. https://www.postgresql.org/download/windows/ 에서 다운로드
2. 설치 시 비밀번호 설정 기억하기
3. pgAdmin 함께 설치

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Mac
```bash
brew install postgresql
brew services start postgresql
```

### 3. 데이터베이스 생성

```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE sensor_monitoring;

# 사용자 권한 부여
GRANT ALL PRIVILEGES ON DATABASE sensor_monitoring TO postgres;

# 종료
\q
```

### 4. 프로젝트 설정

```bash
# 저장소 클론
git clone https://github.com/yourusername/sensor-monitoring-system.git
cd sensor-monitoring-system

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Linux/Mac)
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집하여 DB 정보 입력

# 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 관리자 계정 생성
python manage.py createsuperuser

# 서버 실행
python manage.py runserver
```

### 5. 접속 확인

- 메인 대시보드: http://localhost:8000
- 관리자 페이지: http://localhost:8000/admin

## 문제 해결

### PostgreSQL 연결 오류
```
FATAL: password authentication failed for user "postgres"
```
→ .env 파일의 DB_PASSWORD 확인

### 모듈 import 오류
```
ModuleNotFoundError: No module named 'django'
```
→ 가상환경이 활성화되었는지 확인

### 포트 이미 사용 중
```
Error: That port is already in use.
```
→ 다른 포트 사용: `python manage.py runserver 8080`
