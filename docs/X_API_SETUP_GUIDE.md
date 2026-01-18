# X (Twitter) API 설정 가이드

테슬라 모니터링 시스템에서 자동 트윗 포스팅을 위한 X API 설정 방법입니다.

## 📋 목차
1. [Developer Portal 계정 생성](#1-developer-portal-계정-생성)
2. [App 생성 및 설정](#2-app-생성-및-설정)
3. [API 키 발급](#3-api-키-발급)
4. [권한 설정](#4-권한-설정)
5. [테스트](#5-테스트)

---

## 1. Developer Portal 계정 생성

### 1.1 X Developer Portal 접속
1. https://developer.twitter.com/en/portal/dashboard 접속
2. X 계정으로 로그인
3. "Sign up for Free Account" (처음 사용하는 경우)

### 1.2 개발자 계정 신청
**2026년 기준**: X는 이제 Free Tier를 폐지하고 Basic ($100/월) 이상만 제공합니다.

⚠️ **중요 변경사항**:
- **Free Tier (2023년 4월 폐지)**: 더 이상 무료로 API 사용 불가
- **Basic Plan ($100/월)**:
  - 3,000 posts/월
  - Read/Write 권한
  - OAuth 1.0a & 2.0 지원

**대안 방법**:
1. **기존에 발급받은 API 키가 있다면**: 계속 사용 가능 (Grandfathered)
2. **새로 시작하는 경우**: Basic Plan 구독 필요
3. **무료 대안**: 
   - Mastodon API (오픈소스 SNS)
   - Bluesky API (초대제, 무료)
   - 직접 Telegram Bot으로 알림

### 1.3 신청 양식 작성 (Basic Plan 기준)
```
Use Case: Monitoring website changes and posting updates
Will you make Twitter content available to government entities? No
App Name: Tesla Monitor Bot
App Description: Monitors Tesla.com for updates and posts to Twitter
Website: https://github.com/YOUR_USERNAME/tesla-monitor
```

---

## 2. App 생성 및 설정

### 2.1 새 App 만들기
1. Dashboard → "Projects & Apps"
2. "Create App" 클릭
3. App name: `tesla-monitor-bot`
4. Environment: `Production`

### 2.2 App 설정
Settings → User authentication settings:
- **App permissions**: `Read and Write` (중요!)
- **Type of App**: `Web App, Automated App or Bot`
- **Callback URL**: `https://YOUR_FASTAPI_URL/callback` (필수 아님)
- **Website URL**: `https://github.com/YOUR_USERNAME/tesla-monitor`

---

## 3. API 키 발급

### 3.1 API Key & Secret 발급
1. App → "Keys and tokens" 탭
2. **API Key and Secret** 섹션:
   - "Regenerate" 클릭 (또는 처음이면 자동 생성)
   - API Key (Consumer Key) 복사
   - API Key Secret (Consumer Secret) 복사
   
⚠️ **주의**: Secret은 한 번만 표시되므로 안전하게 저장!

### 3.2 Access Token & Secret 발급
1. **Authentication Tokens** 섹션:
   - "Generate" 클릭
   - Access Token 복사
   - Access Token Secret 복사

⚠️ **권한 확인**: `Read and Write` 권한인지 확인!

### 3.3 발급받은 키 정리
```bash
API Key (Consumer Key):        xxxxxxxxxxxxxxxxxxxxxxxxxxx
API Secret (Consumer Secret):   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Access Token:                   1234567890-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Access Token Secret:            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 4. 권한 설정

### 4.1 읽기/쓰기 권한 확인
App → Settings → "App permissions":
- ✅ `Read and Write` (트윗 포스팅 가능)
- ❌ `Read only` (트윗 불가)
- ❌ `Read, Write and Direct Messages` (불필요)

### 4.2 Rate Limits (Basic Plan)
- **Posts (트윗)**: 3,000 posts/월
- **Reads**: 10,000 reads/월
- **월간 비용**: $100

우리 시스템 예상 사용량:
- 하루 평균 10-20 트윗 (중요 변경만)
- 월 300-600 트윗 → **충분함**

---

## 5. 테스트

### 5.1 로컬에서 테스트
`.env` 파일 생성:
```bash
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_SECRET=your_access_token_secret_here
```

### 5.2 Python 테스트 스크립트
```python
import tweepy
import os

# API 인증
client = tweepy.Client(
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_SECRET")
)

# 테스트 트윗
try:
    response = client.create_tweet(text="🚗⚡ 테슬라 모니터링 시스템 테스트 #Tesla")
    print(f"트윗 성공! ID: {response.data['id']}")
except Exception as e:
    print(f"오류: {e}")
```

### 5.3 FastAPI 서버로 테스트
```bash
# 서버 실행
cd fastapi-webhook
python main.py

# 다른 터미널에서 테스트
curl -X POST http://localhost:8000/test-tweet \
  -H "Content-Type: application/json" \
  -d '{"message": "테스트 트윗"}'
```

---

## 6. Railway에 환경 변수 설정

### 6.1 Railway Dashboard
1. `fastapi-webhook` 서비스 선택
2. Settings → Variables
3. 다음 4개 추가:

```bash
X_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxx
X_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
X_ACCESS_TOKEN=1234567890-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
X_ACCESS_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 6.2 Railway CLI로 설정 (대안)
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 환경 변수 설정
railway variables set X_API_KEY="your_key"
railway variables set X_API_SECRET="your_secret"
railway variables set X_ACCESS_TOKEN="your_token"
railway variables set X_ACCESS_SECRET="your_token_secret"
```

---

## 7. 무료 대안 (X API 대신)

### 7.1 Mastodon (오픈소스 SNS)
- 완전 무료
- API 무제한
- Python 라이브러리: `Mastodon.py`

```python
from mastodon import Mastodon

# 인증
mastodon = Mastodon(
    client_id='your_client_id',
    client_secret='your_client_secret',
    access_token='your_access_token',
    api_base_url='https://mastodon.social'  # 또는 다른 인스턴스
)

# 포스팅
mastodon.status_post("🚗⚡ 테슬라 업데이트!")
```

### 7.2 Bluesky (AT Protocol)
- 무료 (초대제)
- Python 라이브러리: `atproto`

```python
from atproto import Client

client = Client()
client.login('your_handle', 'your_password')
client.send_post(text="🚗⚡ 테슬라 업데이트!")
```

### 7.3 Telegram Bot (추천!)
- 완전 무료
- API 무제한
- 설정 간단

```python
import requests

BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    })
```

**Telegram Bot 생성**:
1. Telegram에서 @BotFather 검색
2. `/newbot` 명령어
3. 봇 이름 설정
4. Token 받기
5. 내 Chat ID 확인: @userinfobot

---

## 8. 문제 해결

### 8.1 "403 Forbidden" 오류
- **원인**: 권한 부족 또는 Access Token이 Read-only
- **해결**:
  1. App Settings → Permissions → `Read and Write` 변경
  2. Access Token 재발급
  3. Railway 환경 변수 업데이트

### 8.2 "401 Unauthorized" 오류
- **원인**: API 키가 잘못됨
- **해결**:
  1. API 키 다시 확인
  2. 공백이나 줄바꿈 없는지 확인
  3. Secret을 Key로 잘못 입력하지 않았는지 확인

### 8.3 "429 Too Many Requests" 오류
- **원인**: Rate Limit 초과
- **해결**:
  1. 포스팅 주기 늘리기
  2. 중요한 변경만 필터링
  3. 월간 사용량 모니터링

### 8.4 "Duplicate content" 오류
- **원인**: 같은 내용을 중복 포스팅
- **해결**:
  1. 메시지에 타임스탬프 추가
  2. 이미 포스팅한 URL 캐싱

---

## 9. 보안 Best Practices

### 9.1 API 키 관리
- ✅ 환경 변수로 저장 (코드에 직접 입력 X)
- ✅ `.gitignore`에 `.env` 추가
- ✅ Railway에서 암호화된 환경 변수 사용
- ❌ GitHub에 절대 업로드 금지

### 9.2 권한 최소화
- 필요한 권한만 부여 (`Read and Write`만)
- Direct Messages 권한 불필요

### 9.3 Rate Limiting
- 애플리케이션 레벨에서 제한 (1분에 1트윗 이하)
- 중복 포스팅 방지

### 9.4 모니터링
- X Developer Portal에서 API 사용량 확인
- 이상 활동 감지 시 즉시 키 재발급

---

## 📚 추가 리소스
- [X API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Tweepy Documentation](https://docs.tweepy.org/)
- [X Developer Community](https://twittercommunity.com/)
- [X API Pricing](https://developer.twitter.com/en/products/twitter-api)

---

## 💰 비용 요약 (2026년 1월 기준)

| 플랜 | 월 비용 | Posts | Reads | 추천 |
|------|---------|-------|-------|------|
| Free | $0 | 0 | 0 | ❌ 폐지됨 |
| Basic | $100 | 3,000 | 10,000 | ✅ 개인용 |
| Pro | $5,000 | 무제한 | 1M | ❌ 과도함 |

**우리 프로젝트**: Basic Plan으로 충분 ($100/월)

**무료 대안**: Telegram Bot 또는 Mastodon 추천! 🎯
