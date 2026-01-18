# 로컬 개발 환경 설정 가이드

Railway에 배포하기 전에 로컬에서 테스트하는 방법입니다.

## 📋 목차
1. [사전 요구사항](#1-사전-요구사항)
2. [Docker Compose로 전체 시스템 실행](#2-docker-compose로-전체-시스템-실행)
3. [개별 서비스 실행](#3-개별-서비스-실행)
4. [테스트](#4-테스트)
5. [문제 해결](#5-문제-해결)

---

## 1. 사전 요구사항

### 1.1 필수 도구 설치
```bash
# macOS (Homebrew)
brew install docker docker-compose
brew install python@3.11

# Docker Desktop 실행
open -a Docker
```

### 1.2 프로젝트 클론
```bash
cd /Users/malife
git clone https://github.com/YOUR_USERNAME/tesla-monitor.git
cd tesla-monitor
```

### 1.3 환경 변수 설정
```bash
# FastAPI 환경 변수
cd fastapi-webhook
cp env.example .env
nano .env  # 또는 vim, code 등으로 편집
```

`.env` 파일 내용:
```bash
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_SECRET=your_access_token_secret_here
PORT=8000
```

---

## 2. Docker Compose로 전체 시스템 실행

### 2.1 Docker Compose 시작
```bash
# 프로젝트 루트로 이동
cd /Users/malife/tesla-monitor

# 전체 시스템 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 2.2 서비스 확인
```bash
# 실행 중인 컨테이너 확인
docker-compose ps

# 예상 출력:
# NAME                       STATUS              PORTS
# tesla-changedetection      Up                  0.0.0.0:5000->5000/tcp
# tesla-playwright-chrome    Up                  0.0.0.0:3000->3000/tcp
# tesla-fastapi-webhook      Up                  0.0.0.0:8000->8000/tcp
```

### 2.3 서비스 접속
- **changedetection.io**: http://localhost:5000
- **FastAPI Docs**: http://localhost:8000/docs
- **Playwright Chrome**: http://localhost:3000 (DevTools)

### 2.4 시스템 종료
```bash
# 정상 종료
docker-compose down

# 볼륨까지 삭제 (데이터 초기화)
docker-compose down -v
```

---

## 3. 개별 서비스 실행

Docker 없이 개별적으로 실행하는 방법입니다.

### 3.1 FastAPI 서버만 실행

#### Python 가상환경 생성
```bash
cd fastapi-webhook

# venv 생성
python3 -m venv venv

# 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

#### 서버 실행
```bash
# 개발 모드 (자동 리로드)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 또는
python main.py
```

#### 서버 확인
```bash
# 다른 터미널에서
curl http://localhost:8000/health
# 예상 출력: {"status":"ok"}

# API 문서 확인
open http://localhost:8000/docs
```

### 3.2 changedetection.io만 실행

#### Docker로 실행
```bash
# changedetection.io만 실행
docker run -d \
  --name changedetection \
  -p 5000:5000 \
  -v changedetection-data:/datastore \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Asia/Seoul \
  ghcr.io/dgtlmoon/changedetection.io:latest

# 로그 확인
docker logs -f changedetection

# 접속
open http://localhost:5000
```

#### Playwright Chrome 추가
```bash
docker run -d \
  --name playwright-chrome \
  -p 3000:3000 \
  -e SCREEN_WIDTH=1920 \
  -e SCREEN_HEIGHT=1080 \
  -e DEFAULT_BLOCK_ADS=true \
  -e DEFAULT_STEALTH=true \
  browserless/chrome:latest
```

changedetection.io 설정:
- Settings → Fetching → Browser Steps
- Playwright Driver URL: `ws://host.docker.internal:3000`

---

## 4. 테스트

### 4.1 FastAPI 헬스 체크
```bash
curl http://localhost:8000/health
```

예상 출력:
```json
{"status":"ok"}
```

### 4.2 테스트 트윗 포스팅
```bash
curl -X POST http://localhost:8000/test-tweet \
  -H "Content-Type: application/json" \
  -d '{"message": "🚗⚡ 로컬 테스트 #Tesla"}'
```

예상 출력:
```json
{"status":"success","message":"Test tweet posted"}
```

### 4.3 Webhook 테스트
```bash
curl -X POST http://localhost:8000/tesla-update \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tesla.com/model3",
    "title": "Model 3",
    "body": "Price changed from $40,000 to $38,000",
    "screenshot": null
  }'
```

예상 출력:
```json
{
  "status":"success",
  "message":"Posted to X",
  "url":"https://www.tesla.com/model3"
}
```

### 4.4 changedetection.io에서 Watch 추가
1. http://localhost:5000 접속
2. "Add Watch" 클릭
3. URL: `https://www.tesla.com/model3`
4. Notifications → Notification URLs:
   ```
   json://host.docker.internal:8000/tesla-update
   ```
5. "Check now" 클릭하여 수동 트리거

### 4.5 전체 플로우 테스트
1. changedetection.io에 Tesla 페이지 추가
2. Notification URL에 FastAPI webhook 설정
3. "Check now"로 수동 트리거
4. FastAPI 로그 확인:
   ```bash
   docker-compose logs -f fastapi-webhook
   ```
5. X에서 트윗 확인

---

## 5. 문제 해결

### 5.1 Docker 오류

#### "Cannot connect to Docker daemon"
```bash
# Docker Desktop이 실행 중인지 확인
docker ps

# Docker Desktop 재시작
killall Docker && open -a Docker
```

#### "Port already in use"
```bash
# 포트를 사용하는 프로세스 찾기
lsof -i :8000  # FastAPI
lsof -i :5000  # changedetection.io

# 프로세스 종료
kill -9 <PID>

# 또는 Docker Compose 포트 변경
# docker-compose.yml에서:
ports:
  - "8001:8000"  # 8000 → 8001로 변경
```

### 5.2 FastAPI 오류

#### "Module not found"
```bash
# 가상환경 활성화 확인
which python
# /Users/malife/tesla-monitor/fastapi-webhook/venv/bin/python

# 의존성 재설치
pip install -r requirements.txt
```

#### "X API 인증 실패"
```bash
# .env 파일 확인
cat .env

# 환경 변수 로드 확인
python -c "import os; print(os.getenv('X_API_KEY'))"
```

### 5.3 changedetection.io 오류

#### "Playwright connection failed"
```bash
# Playwright Chrome 컨테이너 상태 확인
docker logs playwright-chrome

# 재시작
docker restart playwright-chrome

# changedetection.io에서 URL 확인:
# ws://playwright-chrome:3000  (Docker Compose 내부 네트워크)
# ws://host.docker.internal:3000  (macOS/Windows)
# ws://172.17.0.1:3000  (Linux)
```

#### "Webhook 전송 안됨"
```bash
# FastAPI 서버가 실행 중인지 확인
curl http://localhost:8000/health

# changedetection.io에서 Notification URL 확인:
# Docker Compose: json://fastapi-webhook:8000/tesla-update
# 개별 실행: json://host.docker.internal:8000/tesla-update
```

### 5.4 네트워크 오류

#### Docker 컨테이너 간 통신 안됨
```bash
# Docker 네트워크 확인
docker network ls
docker network inspect tesla-network

# 같은 네트워크에 있는지 확인
docker inspect changedetection | grep NetworkMode
docker inspect fastapi-webhook | grep NetworkMode

# 수동으로 네트워크 생성
docker network create tesla-network
docker run --network tesla-network ...
```

---

## 6. 개발 팁

### 6.1 핫 리로드 (자동 재시작)
```bash
# FastAPI 개발 모드
uvicorn main:app --reload
# 파일 수정 시 자동으로 서버 재시작
```

### 6.2 로그 레벨 조정
`main.py`에서:
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # INFO → DEBUG
```

### 6.3 Interactive API 문서
```bash
# Swagger UI
open http://localhost:8000/docs

# ReDoc
open http://localhost:8000/redoc
```

### 6.4 Docker Compose 개발 모드
`docker-compose.yml`에 볼륨 마운트 추가:
```yaml
services:
  fastapi-webhook:
    volumes:
      - ./fastapi-webhook:/app  # 코드 변경 시 자동 반영
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6.5 VS Code 디버깅
`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": true,
      "envFile": "${workspaceFolder}/fastapi-webhook/.env"
    }
  ]
}
```

---

## 7. 다음 단계

로컬 테스트가 완료되면:
1. ✅ 코드를 GitHub에 푸시
2. ✅ Railway에 배포 (RAILWAY_DEPLOY_GUIDE.md 참고)
3. ✅ 프로덕션 환경에서 테스트

---

## 📚 추가 리소스
- [Docker Compose 문서](https://docs.docker.com/compose/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Uvicorn 문서](https://www.uvicorn.org/)
- [changedetection.io 문서](https://github.com/dgtlmoon/changedetection.io/wiki)

개발 환경 설정 완료! 🎉
