# 🚀 빠른 시작 가이드

테슬라 모니터링 시스템을 5분 안에 시작하는 방법입니다.

## 📋 선택하기: 어떤 방법이 나에게 맞을까?

### 방법 1: changedetection.io + Railway (추천 - 초보자)
- ✅ GUI로 쉽게 설정
- ✅ JavaScript 렌더링 지원
- ✅ 스크린샷 자동 캡처
- ❌ 비용 높음 (~$21/월, 최적화 시 ~$2/월)
- **난이도**: ⭐⭐ (쉬움)

### 방법 2: 순수 Python + GitHub Actions (추천 - 무료!)
- ✅ 완전 무료 (GitHub Actions 무료 티어)
- ✅ 커스터마이징 가능
- ❌ GitHub 사용법 필요
- ❌ JavaScript 렌더링 제한
- **난이도**: ⭐⭐⭐ (보통)

### 방법 3: 순수 Python + Railway Cron
- ✅ 저렴 (~$1-2/월)
- ✅ 안정적
- ✅ 커스터마이징 가능
- **난이도**: ⭐⭐⭐ (보통)

---

## 🎯 방법 1: changedetection.io + Railway

### Step 1: X API 키 발급 (10분)
1. https://developer.twitter.com/en/portal/dashboard 접속
2. "Create App" → 앱 이름 입력
3. Settings → "Read and Write" 권한 설정
4. Keys and tokens → API 키 4개 복사:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret

⚠️ **주의**: 2026년 기준 X API는 Basic Plan ($100/월) 필요
**무료 대안**: [Telegram Bot](#telegram-bot-대안-무료) 또는 Mastodon

### Step 2: Railway 계정 생성 (2분)
1. https://railway.app 접속
2. GitHub 계정으로 로그인
3. 무료 $5 크레딧 확인

### Step 3: GitHub에 프로젝트 업로드 (3분)
```bash
cd /Users/malife/tesla-monitor
git init
git add .
git commit -m "Initial commit"

# GitHub에서 새 repository 생성 후:
git remote add origin https://github.com/YOUR_USERNAME/tesla-monitor.git
git push -u origin main
```

### Step 4: Railway에 배포 (5분)

#### 4.1 FastAPI 서버 배포
1. Railway → "New Project" → "Deploy from GitHub"
2. Repository 선택: `tesla-monitor`
3. Root Directory: `/fastapi-webhook`
4. 환경 변수 설정:
```
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_token
X_ACCESS_SECRET=your_token_secret
```
5. 생성된 URL 복사 (예: `https://fastapi-webhook-production.up.railway.app`)

#### 4.2 changedetection.io 배포
1. Railway → "New Service" → "Docker Image"
2. Image: `ghcr.io/dgtlmoon/changedetection.io:latest`
3. 환경 변수:
```
PUID=1000
PGID=1000
TZ=Asia/Seoul
```
4. Volume 추가: Mount Path `/datastore`
5. 생성된 URL 접속

### Step 5: changedetection.io 설정 (5분)
1. changedetection.io URL 접속
2. "Add Watch" 클릭
3. URL: `https://www.tesla.com/model3`
4. Settings:
   - Check every: `15 minutes`
5. Notifications:
   - Notification URLs: `json://YOUR_FASTAPI_URL/tesla-update`
6. "Check now"로 테스트

### Step 6: 추가 페이지 설정
위 과정을 반복해서 다음 페이지들 추가:
- https://www.tesla.com/cybertruck
- https://www.tesla.com/modely
- https://www.tesla.com/ko_kr
- (더 추가...)

✅ **완료!** 이제 변경 사항이 자동으로 X에 포스팅됩니다.

---

## 🆓 방법 2: 순수 Python + GitHub Actions (완전 무료!)

### Step 1: X API 키 발급
위 방법 1과 동일

### Step 2: GitHub에 프로젝트 업로드
```bash
cd /Users/malife/tesla-monitor
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/tesla-monitor.git
git push -u origin main
```

### Step 3: GitHub Secrets 설정 (3분)
1. GitHub Repository → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. 다음 4개 추가:
   - `X_API_KEY`: your_api_key
   - `X_API_SECRET`: your_api_secret
   - `X_ACCESS_TOKEN`: your_token
   - `X_ACCESS_TOKEN_SECRET`: your_token_secret

### Step 4: GitHub Actions 활성화
1. Repository → Actions 탭
2. "I understand my workflows, go ahead and enable them" 클릭
3. "Tesla Monitor" workflow 선택
4. "Run workflow" → "Run workflow" (수동 실행)

### Step 5: 확인
1. Actions 탭에서 실행 로그 확인
2. X에서 트윗 확인

✅ **완료!** 15분마다 자동으로 실행됩니다. 완전 무료!

**비용**: $0/월 (GitHub Actions 2,000분/월 무료)
**예상 사용량**: ~1,440분/월 ✅ 충분

---

## 💰 방법 3: 순수 Python + Railway Cron

### Step 1-2: 위와 동일

### Step 3: Railway 배포
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
cd /Users/malife/tesla-monitor/python-monitor
railway init

# 환경 변수 설정
railway variables set X_API_KEY="your_key"
railway variables set X_API_SECRET="your_secret"
railway variables set X_ACCESS_TOKEN="your_token"
railway variables set X_ACCESS_SECRET="your_token_secret"
railway variables set DATA_DIR="/app/data"

# 배포
railway up
```

### Step 4: Cron 설정
1. Railway Dashboard → 서비스 선택
2. Settings → Cron Jobs
3. Schedule: `*/15 * * * *` (15분마다)
4. Command: `python monitor.py`

✅ **완료!** ~$1-2/월로 운영 가능

---

## 📱 Telegram Bot 대안 (무료!)

X API가 비싸다면 Telegram Bot 사용 (완전 무료):

### Step 1: Telegram Bot 생성
1. Telegram에서 @BotFather 검색
2. `/newbot` 명령어
3. 봇 이름 입력
4. Token 복사 (예: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Step 2: Chat ID 확인
1. @userinfobot에게 메시지 보내기
2. Your ID 복사 (예: `987654321`)

### Step 3: 코드 수정
`fastapi-webhook/main.py` 또는 `python-monitor/monitor.py`:

```python
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def post_to_telegram(message: str) -> bool:
    """Telegram으로 메시지 전송"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    })
    return response.status_code == 200
```

### Step 4: 환경 변수 설정
```bash
# Railway
railway variables set TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
railway variables set TELEGRAM_CHAT_ID="987654321"

# GitHub Actions
# Secrets에 TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID 추가
```

✅ **완전 무료!** X API 대신 Telegram 사용

---

## 🧪 테스트 방법

### 로컬 테스트 (방법 1)
```bash
cd /Users/malife/tesla-monitor
docker-compose up -d

# FastAPI 테스트
curl http://localhost:8000/health

# 테스트 트윗
curl -X POST http://localhost:8000/test-tweet \
  -H "Content-Type: application/json" \
  -d '{"message": "테스트"}'
```

### 로컬 테스트 (방법 2, 3)
```bash
cd /Users/malife/tesla-monitor/python-monitor

# 환경 변수 설정
cp env.example .env
nano .env

# 실행
pip install -r requirements.txt
python monitor.py
```

---

## 🐛 문제 해결

### "X API 인증 실패"
1. API 키 확인 (공백, 줄바꿈 없는지)
2. Read and Write 권한 확인
3. Access Token 재발급

### "Railway 비용 초과"
1. Cron Jobs로 전환 (연속 실행 → 주기적 실행)
2. Playwright 제거
3. 모니터링 주기 늘리기 (15분 → 30분)

### "GitHub Actions가 실행 안됨"
1. Actions 탭에서 활성화 확인
2. Secrets 설정 확인
3. workflow 파일 경로 확인 (`.github/workflows/monitor.yml`)

---

## 📚 더 자세한 가이드

- [Railway 배포 가이드](RAILWAY_DEPLOY_GUIDE.md) - 상세 Railway 설정
- [X API 설정 가이드](X_API_SETUP_GUIDE.md) - X API 키 발급
- [로컬 개발 가이드](LOCAL_DEVELOPMENT.md) - Docker로 로컬 테스트
- [Python 대안](PURE_PYTHON_ALTERNATIVE.md) - changedetection.io 없이 구현

---

## 🎯 다음 단계

시스템이 잘 작동하면:
1. ✅ 모니터링 페이지 추가 (Roadster, 에너지 등)
2. ✅ 필터링 키워드 커스터마이징
3. ✅ 트윗 메시지 포맷 변경
4. ✅ 데이터베이스 연동
5. ✅ 웹 대시보드 구축

---

## 💡 프로 팁

### 비용 절감
- GitHub Actions 사용 (무료)
- Telegram Bot 사용 (무료)
- Railway Cron Jobs ($1-2/월)
- 모니터링 주기 늘리기

### 성능 향상
- 중요한 페이지만 모니터링
- CSS Selector로 특정 영역만 감지
- 키워드 필터링 강화

### 보안
- 환경 변수로 API 키 관리
- `.gitignore`에 `.env` 추가
- GitHub Secrets 사용
- Railway 암호화 변수 사용

---

**5분 만에 시작 완료! 🎉**

질문이 있으면 GitHub Issues에 남겨주세요!
