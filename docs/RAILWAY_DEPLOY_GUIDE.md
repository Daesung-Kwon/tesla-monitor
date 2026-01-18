# Railway 배포 가이드 (2026년 1월 최신)

테슬라 모니터링 시스템을 Railway에 배포하는 전체 가이드입니다.

## 📋 목차
1. [Railway 프로젝트 설정](#1-railway-프로젝트-설정)
2. [changedetection.io Docker 배포](#2-changedetectionio-docker-배포)
3. [FastAPI Webhook 서버 배포](#3-fastapi-webhook-서버-배포)
4. [환경 변수 설정](#4-환경-변수-설정)
5. [Webhook 연결](#5-webhook-연결)
6. [모니터링 페이지 설정](#6-모니터링-페이지-설정)
7. [비용 관리](#7-비용-관리)

---

## 1. Railway 프로젝트 설정

### 1.1 Railway 계정 생성
1. https://railway.app 접속
2. GitHub 계정으로 로그인
3. 무료 플랜: $5 크레딧 제공 (월별 리셋)
   - 약 500시간/월 소형 서비스 운영 가능
   - 두 서비스 합쳐서 예상 비용: $3-4/월

### 1.2 새 프로젝트 생성
1. Dashboard → "New Project" 클릭
2. 프로젝트 이름: `tesla-monitor`
3. Region: `us-west1` (또는 가장 가까운 리전)

### 1.3 GitHub Repository 연결
1. GitHub에 이 프로젝트 업로드
```bash
cd /Users/malife/tesla-monitor
git init
git add .
git commit -m "Initial commit: Tesla monitor system"
git remote add origin https://github.com/YOUR_USERNAME/tesla-monitor.git
git push -u origin main
```

2. Railway에서 GitHub 연동
   - Settings → "Connect to GitHub"
   - Repository 선택: `tesla-monitor`

---

## 2. changedetection.io Docker 배포

### 2.1 Docker 서비스 추가
1. Railway 프로젝트에서 "New Service" 클릭
2. "Docker Image" 선택
3. Image: `ghcr.io/dgtlmoon/changedetection.io:latest`
4. 서비스 이름: `changedetection`

### 2.2 환경 변수 설정
Settings → Variables에서 추가:
```bash
PUID=1000
PGID=1000
TZ=Asia/Seoul
PLAYWRIGHT_DRIVER_URL=ws://playwright-chrome:3000
```

### 2.3 포트 설정
Settings → Networking:
- Port: `5000`
- Public Networking 활성화
- 생성된 URL 메모 (예: `https://changedetection-production.up.railway.app`)

### 2.4 Volume 설정 (데이터 지속화)
1. Settings → Volumes 클릭
2. "Add Volume" 클릭
3. Mount Path: `/datastore`
4. Volume 크기: 1GB (충분함)

### 2.5 Playwright Chrome 서비스 추가 (JavaScript 렌더링)
1. "New Service" → "Docker Image"
2. Image: `browserless/chrome:latest`
3. 서비스 이름: `playwright-chrome`
4. 환경 변수:
```bash
SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080
ENABLE_DEBUGGER=false
PREBOOT_CHROME=true
DEFAULT_BLOCK_ADS=true
DEFAULT_STEALTH=true
```
5. Port: `3000` (내부 네트워크만 사용, Public 불필요)

---

## 3. FastAPI Webhook 서버 배포

### 3.1 GitHub Repo로 서비스 추가
1. "New Service" → "GitHub Repo"
2. Repository: `tesla-monitor`
3. Root Directory: `/fastapi-webhook`
4. 서비스 이름: `fastapi-webhook`

### 3.2 빌드 설정
Railway가 자동 감지하지만, 수동 설정:
- Settings → Build:
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

또는 `railway.toml` 파일 사용 (이미 포함됨):
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### 3.3 포트 설정
Settings → Networking:
- Railway가 자동으로 PORT 환경 변수 할당
- Public Networking 활성화
- 생성된 URL 메모 (예: `https://fastapi-webhook-production.up.railway.app`)

---

## 4. 환경 변수 설정

### 4.1 X (Twitter) API 키 발급
1. https://developer.twitter.com/en/portal/dashboard 접속
2. "Create App" (또는 기존 앱 사용)
3. App Settings → "Keys and tokens"
4. 다음 4개 키 발급:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret

⚠️ **주의**: Access Token은 "Read and Write" 권한으로 생성해야 합니다!

### 4.2 FastAPI 서비스에 환경 변수 추가
`fastapi-webhook` 서비스 → Settings → Variables:
```bash
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_SECRET=your_access_token_secret_here
```

### 4.3 환경 변수 암호화 (선택)
Railway는 기본적으로 환경 변수를 암호화하여 저장합니다.

---

## 5. Webhook 연결

### 5.1 내부 네트워크 활용
Railway의 내부 네트워크를 사용하면 빠르고 안전:
- 형식: `http://SERVICE_NAME.railway.internal:PORT/path`
- 예: `http://fastapi-webhook.railway.internal:8000/tesla-update`

하지만 changedetection.io가 내부 네트워크를 지원하지 않을 수 있으므로, Public URL 사용:
- `https://fastapi-webhook-production.up.railway.app/tesla-update`

### 5.2 Webhook URL 확인
```bash
# FastAPI 서비스 URL 확인
echo "Webhook URL: https://YOUR_FASTAPI_URL/tesla-update"

# 테스트
curl https://YOUR_FASTAPI_URL/health
```

---

## 6. 모니터링 페이지 설정

### 6.1 changedetection.io UI 접속
1. changedetection.io 서비스 URL 접속 (예: `https://changedetection-production.up.railway.app`)
2. 초기 비밀번호 설정 (Settings에서)

### 6.2 Playwright 설정
1. Settings → "Fetching" 탭
2. "Browser Steps / Playwright" 활성화
3. "Playwright Driver URL": `ws://playwright-chrome.railway.internal:3000`
   - 또는 Public URL: `wss://playwright-chrome-production.up.railway.app`

### 6.3 모니터링 페이지 추가
각 페이지마다 "Add Watch" 클릭:

#### 6.3.1 메인 페이지
- URL: `https://www.tesla.com/`
- Check every: `15 minutes`
- Filters:
  - CSS/JSON Selector: `body` (전체 페이지)
  - Ignore text: `cookie, analytics` (노이즈 제거)

#### 6.3.2 차량 페이지들
다음 페이지들을 각각 추가:
```
https://www.tesla.com/cybertruck
https://www.tesla.com/model3
https://www.tesla.com/modely
https://www.tesla.com/modelx
https://www.tesla.com/models
https://www.tesla.com/roadster
```

설정:
- Check every: `10 minutes`
- Filters: `#price, .pricing, .delivery, .inventory` (가격/재고 정보)
- JavaScript rendering: 활성화 (Playwright)

#### 6.3.3 소프트웨어 업데이트
- URL: `https://www.tesla.com/support/software-updates`
- Check every: `30 minutes`
- Filters: `.release-notes, .version`

#### 6.3.4 에너지 제품
- URL: `https://www.tesla.com/energy`
- Check every: `30 minutes`

#### 6.3.5 한국 및 주요 국가
```
https://www.tesla.com/ko_kr
https://www.tesla.com/ja_jp
https://www.tesla.com/zh_cn
https://www.tesla.com/de_de
https://www.tesla.com/en_gb
```

### 6.4 Notification 설정 (Webhook)
각 Watch 설정에서:
1. "Edit" → "Notifications" 탭
2. "Notification URLs" 추가:
```
json://YOUR_FASTAPI_URL/tesla-update
```

또는 표준 webhook:
```
webhook://YOUR_FASTAPI_URL/tesla-update
```

3. "Notification format": JSON
4. "Notification body":
```json
{
  "url": "{watch_url}",
  "title": "{watch_title}",
  "body": "{diff}",
  "screenshot": "{screenshot_url}"
}
```

### 6.5 고급 필터링 (선택)
- **CSS Selector로 특정 영역만 모니터링**:
  ```css
  .pricing-section, #delivery-estimate, .inventory-card
  ```

- **정규식으로 특정 패턴 감지**:
  ```
  price.*\$\d+
  delivery.*\d+.*week
  ```

---

## 7. 비용 관리

### 7.1 Railway 요금제 (2026년 1월 기준)
- **Free Tier**: $5 크레딧/월
  - 512MB RAM, 1 vCPU per service
  - 500시간/월 실행 시간 (약 20일 continuous)
  - 100GB 아웃바운드 트래픽

- **Pro Plan**: $20/월 + 사용량
  - 8GB RAM, 8 vCPU
  - 무제한 실행 시간
  - 100GB 트래픽 포함

### 7.2 예상 비용 (Free Tier)
우리 시스템:
- changedetection.io: ~200MB RAM → $0.01/hr = $7.20/월
- playwright-chrome: ~300MB RAM → $0.015/hr = $10.80/월
- fastapi-webhook: ~100MB RAM → $0.005/hr = $3.60/월

**총 예상 비용**: ~$21/월

⚠️ **Free Tier 초과!** 아래 최적화 필요:

### 7.3 비용 절감 방법

#### 옵션 1: Cron Jobs 사용 (권장)
Railway Cron Jobs로 주기적 실행:
1. Settings → Cron Jobs 추가
2. Schedule: `*/15 * * * *` (15분마다)
3. Command: `curl https://changedetection-url/api/watch/all/check`
4. 비용: ~$2/월 (실행 시간만 과금)

#### 옵션 2: 외부 Cron 서비스
- Cron-job.org (무료)
- EasyCron (무료 티어)
- GitHub Actions (무료, 2000분/월)

예시 GitHub Actions:
```yaml
name: Trigger Tesla Monitor
on:
  schedule:
    - cron: '*/15 * * * *'  # 15분마다
jobs:
  trigger:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger changedetection.io
        run: curl -X POST ${{ secrets.CHANGEDETECTION_TRIGGER_URL }}
```

#### 옵션 3: Playwright 제거
JavaScript 렌더링이 필요 없는 페이지만 모니터링:
- 비용 $10.80 절감
- 총 비용: ~$10/월

#### 옵션 4: 순수 Python으로 구현
changedetection.io 대신 Python 스크립트:
- Railway Cron으로 실행
- 비용: ~$1-2/월
- 단점: 직접 구현 필요 (아래 코드 예시 제공)

### 7.4 모니터링 & 알림
Railway Dashboard에서 실시간 확인:
- Metrics → CPU, Memory, Network
- Logs → 각 서비스 로그
- Usage → 월간 비용

비용 초과 알림 설정:
- Settings → Billing → "Usage Alerts"
- $4 초과 시 이메일 알림

---

## 8. 배포 후 테스트

### 8.1 헬스 체크
```bash
# FastAPI 서버 확인
curl https://YOUR_FASTAPI_URL/health

# changedetection.io 확인
curl https://YOUR_CHANGEDETECTION_URL/
```

### 8.2 테스트 트윗 포스팅
```bash
curl -X POST https://YOUR_FASTAPI_URL/test-tweet \
  -H "Content-Type: application/json" \
  -d '{"message": "🚗⚡ 테슬라 모니터링 시스템 가동 #Tesla"}'
```

### 8.3 수동 변경 감지 트리거
changedetection.io UI에서:
1. Watch 선택
2. "Check now" 클릭
3. Logs에서 webhook 전송 확인

### 8.4 로그 확인
Railway에서 각 서비스 로그 확인:
```
fastapi-webhook → Logs
changedetection → Logs
```

---

## 9. 문제 해결

### 9.1 Webhook이 전송되지 않음
- changedetection.io Logs 확인
- Notification URL 형식 확인 (`json://` 또는 `webhook://`)
- FastAPI 서버 로그에서 요청 수신 확인

### 9.2 트윗 포스팅 실패
- X API 키 확인 (Read and Write 권한)
- FastAPI 로그에서 에러 메시지 확인
- 트윗 길이 제한 (280자) 확인

### 9.3 JavaScript 렌더링 실패
- Playwright Chrome 서비스 상태 확인
- changedetection.io에서 "Browser Steps" 활성화 확인
- 메모리 부족 → Railway에서 RAM 증량

### 9.4 비용 초과
- Cron Jobs로 전환
- 모니터링 주기 늘리기 (15분 → 30분)
- Playwright 비활성화

---

## 10. 다음 단계

### 10.1 고급 기능 추가
- [ ] 변경 사항 데이터베이스 저장 (PostgreSQL)
- [ ] 웹 대시보드 구축 (React + Railway)
- [ ] 이메일 알림 추가 (SendGrid)
- [ ] Slack 알림 연동
- [ ] AI로 중요도 분석 (OpenAI GPT-4)

### 10.2 모니터링 확대
- [ ] 테슬라 블로그 (tesla.com/blog)
- [ ] 테슬라 IR (ir.tesla.com)
- [ ] Reddit r/teslamotors
- [ ] YouTube 테슬라 채널

---

## 📚 추가 리소스
- [Railway 공식 문서](https://docs.railway.app/)
- [changedetection.io GitHub](https://github.com/dgtlmoon/changedetection.io)
- [Tweepy 문서](https://docs.tweepy.org/)
- [X API v2 문서](https://developer.twitter.com/en/docs/twitter-api)

---

## 🆘 지원
- Railway Discord: https://discord.gg/railway
- changedetection.io Discord: https://discord.gg/QZSpfJ9c
- X Developer Forums: https://twittercommunity.com/

배포 완료! 🎉
