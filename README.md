# 🚗⚡ Tesla Website Monitor

테슬라 공식 홈페이지의 중요한 업데이트를 실시간으로 감지하고 Telegram으로 자동 알림을 보내는 시스템입니다.

**💰 완전 무료 ($0/월)** | **⏱️ 10분이면 완성!**

[![Railway Deploy](https://img.shields.io/badge/Deploy%20on-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## 📖 개요

이 프로젝트는 다음과 같은 구조로 작동합니다:

1. **changedetection.io** - 테슬라 웹사이트의 변경 사항을 주기적으로 감지
2. **FastAPI Webhook** - 변경 사항을 받아서 필터링 및 처리
3. **X API v2** - 중요한 변경 사항만 X(Twitter)에 자동 포스팅

### 🎯 주요 기능

- ✅ 테슬라 주요 페이지 실시간 모니터링 (차량, 에너지, 소프트웨어 등)
- ✅ 스마트 필터링 (가격, 신제품, 업데이트 등 중요 변경만 감지)
- ✅ Telegram 자동 알림 (한국어, HTML 포맷)
- ✅ GitHub Actions 자동 실행 (15분마다)
- ✅ 순수 Python 구현 (외부 의존성 최소)
- ✅ 완전 무료 ($0/월)
- ✅ 10분이면 설정 완료

### 📊 모니터링 대상

- 🚗 차량 페이지: Model 3, Model Y, Model S, Model X, Cybertruck, Roadster
- ⚡ 에너지: Powerwall, Solar Roof
- 💻 소프트웨어 업데이트
- 🌍 한국 및 주요 국가별 페이지

---

## 🚀 빠른 시작 (10분)

### ⭐ 추천: Telegram + GitHub Actions (완전 무료!)

**→ [START_HERE.md](START_HERE.md) ← 여기서 시작!**

**→ [TELEGRAM_SETUP_GUIDE.md](TELEGRAM_SETUP_GUIDE.md) ← 상세 가이드**

### 간단 요약:

```bash
# 1. Telegram Bot 생성 (3분)
#    @BotFather에게 /newbot → Token 받기
#    @userinfobot에게 /start → Chat ID 받기

# 2. GitHub에 업로드 (3분)
cd /Users/malife/tesla-monitor
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/tesla-monitor.git
git push -u origin main

# 3. GitHub Secrets 설정 (2분)
#    Settings → Secrets → Actions
#    - TELEGRAM_BOT_TOKEN
#    - TELEGRAM_CHAT_ID

# 4. GitHub Actions 활성화 (1분)
#    Actions → Enable workflows → Run workflow

# 5. 완료! 15분마다 자동 실행 🎉
```

### 비용: $0/월 ✅

---

## 📁 프로젝트 구조

```
tesla-monitor/
├── README.md                       # 이 파일
├── docker-compose.yml              # 로컬 개발 환경
├── docs/                           # 상세 가이드
│   ├── RAILWAY_DEPLOY_GUIDE.md    # Railway 배포 가이드
│   ├── X_API_SETUP_GUIDE.md       # X API 설정 가이드
│   ├── LOCAL_DEVELOPMENT.md       # 로컬 개발 가이드
│   └── PURE_PYTHON_ALTERNATIVE.md # Python 대안 (changedetection.io 없이)
├── fastapi-webhook/                # FastAPI 서버
│   ├── main.py                    # 메인 애플리케이션
│   ├── requirements.txt           # Python 의존성
│   ├── Procfile                   # Railway 배포 설정
│   ├── railway.toml               # Railway 설정
│   ├── Dockerfile                 # Docker 이미지
│   └── env.example                # 환경 변수 예시
└── changedetection/                # changedetection.io 설정 (선택)
```

---

## 🔧 주요 설정

### 환경 변수

`fastapi-webhook/.env`:
```bash
# X (Twitter) API 인증
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_SECRET=your_access_token_secret_here

# 서버 포트
PORT=8000
```

### changedetection.io Notification URL

```
json://YOUR_FASTAPI_URL/tesla-update
```

또는 Railway 내부 네트워크:
```
json://fastapi-webhook.railway.internal:8000/tesla-update
```

---

## 📝 사용 방법

### 1. changedetection.io에서 Watch 추가

1. http://localhost:5000 접속 (또는 Railway URL)
2. "Add Watch" 클릭
3. URL 입력: `https://www.tesla.com/model3`
4. Settings:
   - **Check every**: 10-15 minutes
   - **Filters**: CSS Selector로 특정 영역만 모니터링
   - **JavaScript**: Playwright 활성화
5. Notifications:
   - Notification URLs: `json://YOUR_FASTAPI_URL/tesla-update`
   - Format: JSON

### 2. 필터링 로직 커스터마이즈

`fastapi-webhook/main.py`:
```python
IMPORTANT_KEYWORDS = [
    'price', 'pricing', '₩', 'won',  # 가격
    'new', 'launch', 'delivery',      # 신제품
    'update', 'refresh', 'version',   # 업데이트
    # ... 더 추가
]
```

### 3. 트윗 메시지 포맷 변경

```python
def format_tweet_message(url: str, diff_snippet: str) -> str:
    # 여기서 메시지 포맷 커스터마이즈
    return f"🚗⚡ 변경 감지!\n\n{diff_snippet}\n\n{url}"
```

---

## 🧪 테스트

### FastAPI 헬스 체크
```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

### 테스트 트윗
```bash
curl -X POST http://localhost:8000/test-tweet \
  -H "Content-Type: application/json" \
  -d '{"message": "테스트 트윗"}'
```

### Webhook 테스트
```bash
curl -X POST http://localhost:8000/tesla-update \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.tesla.com/model3",
    "body": "Price: $39,000 → $38,000"
  }'
```

---

## 💰 비용 분석 (2026년 1월 기준)

### ✅ 현재 구성 (Telegram + GitHub Actions)

```
Telegram Bot API:     $0/월 (무료!)
GitHub Actions:       $0/월 (2,000분 무료)
저장 공간:            $0/월 (Artifacts 무료)
───────────────────────────────
총 비용:              $0/월 🎉
```

**예상 사용량:**
- 30분마다 실행: 48회/일 × 30일 = 1,440분/월
- GitHub Actions 무료 한도: 2,000분/월
- 여유분: 560분 ✅

### 💡 대안 비교

| 방법 | SNS | 인프라 | 월 비용 |
|------|-----|--------|---------|
| **현재 (추천)** | Telegram | GitHub | **$0** ✅ |
| changedetection.io | X API | Railway | $124 ❌ |
| 순수 Python | X API | Railway Cron | $102 ❌ |
| 순수 Python | X API | GitHub | $100 ❌ |

**결론: Telegram + GitHub Actions = 최고!** 🏆

---

## 🔐 보안

- ✅ 환경 변수로 API 키 관리
- ✅ `.gitignore`에 `.env` 추가
- ✅ Railway 암호화된 환경 변수 사용
- ✅ Rate Limiting 구현
- ✅ 권한 최소화 (Read and Write만)

---

## 🐛 문제 해결

### Webhook이 전송되지 않음
1. FastAPI 로그 확인: `docker-compose logs fastapi-webhook`
2. changedetection.io 로그 확인
3. Notification URL 형식 확인 (`json://` 또는 `webhook://`)

### 트윗 포스팅 실패
1. X API 키 확인 (Read and Write 권한)
2. 환경 변수 확인: `railway variables list`
3. 트윗 길이 제한 (280자) 확인

### Playwright 렌더링 실패
1. Playwright Chrome 상태 확인: `docker ps`
2. changedetection.io에서 Browser Steps 활성화
3. 메모리 부족 → Railway RAM 증량

더 많은 해결 방법: [docs/LOCAL_DEVELOPMENT.md#5-문제-해결](docs/LOCAL_DEVELOPMENT.md#5-문제-해결)

---

## 🚀 고급 기능

### 1. 데이터베이스 연동
PostgreSQL로 변경 이력 저장:
```python
# TODO: PostgreSQL 연동 코드
```

### 2. 웹 대시보드
React + Railway로 대시보드 구축:
```bash
# TODO: 프론트엔드 코드
```

### 3. AI 분석
OpenAI GPT-4로 중요도 자동 분석:
```python
# TODO: OpenAI API 연동
```

### 4. 멀티 플랫폼
X + Mastodon + Telegram + Slack:
```python
# TODO: 멀티 플랫폼 포스팅
```

---

## 📚 문서

- [Railway 배포 가이드](docs/RAILWAY_DEPLOY_GUIDE.md) - Railway.dev에 배포하는 전체 가이드
- [X API 설정 가이드](docs/X_API_SETUP_GUIDE.md) - X API 키 발급 및 설정
- [로컬 개발 가이드](docs/LOCAL_DEVELOPMENT.md) - Docker Compose로 로컬 테스트
- [Python 대안](docs/PURE_PYTHON_ALTERNATIVE.md) - changedetection.io 없이 구현

---

## 🤝 기여

버그 리포트, 기능 제안, PR 환영합니다!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

---

## 🙏 감사

- [changedetection.io](https://github.com/dgtlmoon/changedetection.io) - 웹사이트 모니터링
- [FastAPI](https://fastapi.tiangolo.com/) - 빠른 API 프레임워크
- [Tweepy](https://www.tweepy.org/) - X API 라이브러리
- [Railway.app](https://railway.app/) - 간편한 배포 플랫폼

---

## 📞 연락처

질문이나 제안이 있으시면 이슈를 열어주세요!

- GitHub Issues: [tesla-monitor/issues](https://github.com/YOUR_USERNAME/tesla-monitor/issues)
- Email: your-email@example.com
- X: [@YourHandle](https://x.com/YourHandle)

---

## ⭐ Star History

프로젝트가 마음에 드셨다면 ⭐️ Star를 눌러주세요!

---

**Made with ❤️ by Tesla Enthusiasts**

🚗⚡ Happy Monitoring! 🚗⚡
