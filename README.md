# 🚗⚡ Tesla News Monitor

Tesla 관련 뉴스를 RSS 피드로 모니터링하여 Telegram으로 실시간 알림을 보내는 시스템입니다.

**💰 완전 무료 ($0/월)** | **⏱️ 10분이면 완성!** | **🚫 차단 걱정 없음!**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)

## 📖 개요

이 프로젝트는 다음과 같은 구조로 작동합니다:

```
[RSS 피드] → [Python 스크립트] → [Telegram Bot] → [내 스마트폰]
   ↓              ↓                    ↓              ↓
5개 뉴스 소스   자동 필터링         즉시 알림        실시간 수신
```

### 🎯 주요 기능

- ✅ **RSS 피드 모니터링** - 5개 주요 Tesla 뉴스 소스
- ✅ **자동 필터링** - Tesla 관련 기사만 선별
- ✅ **중복 제거** - 같은 기사는 한 번만 알림
- ✅ **Telegram 알림** - 실시간 푸시 알림
- ✅ **GitHub Actions** - 15분마다 자동 실행
- ✅ **완전 무료** - $0/월, 제약 없음
- ✅ **차단 없음** - RSS는 공개 API

### 📰 모니터링 뉴스 소스

1. **Tesla 공식 블로그** - 공식 발표 및 업데이트
2. **Electrek** - Tesla 전문 뉴스 사이트
3. **Teslarati** - Tesla 뉴스 & 심층 분석
4. **InsideEVs** - 전기차 업계 뉴스
5. **Tesla North** - Tesla 캐나다 뉴스

---

## 🚀 빠른 시작 (10분)

### ⭐ Step 1: Telegram Bot 생성 (3분)

**→ [START_HERE.md](START_HERE.md) ← 여기서 시작!**

**→ [TELEGRAM_SETUP_GUIDE.md](TELEGRAM_SETUP_GUIDE.md) ← 상세 가이드**

```
1. Telegram에서 @BotFather 검색
2. /newbot 명령어 → Bot 생성
3. Token 받기: 123456789:ABC...

4. @userinfobot 검색
5. /start 명령어 → Chat ID 받기
6. Your ID: 987654321
```

### ⭐ Step 2: GitHub 설정 (5분)

```bash
# 1. Repository 생성 (GitHub 웹사이트)
#    https://github.com/new
#    Name: tesla-monitor
#    Private 선택

# 2. 코드 푸시 (이미 완료!)
#    git push -u origin main

# 3. GitHub Secrets 설정
#    Settings → Secrets and variables → Actions
#    - TELEGRAM_BOT_TOKEN (Bot Token)
#    - TELEGRAM_CHAT_ID (Chat ID)

# 4. GitHub Actions 활성화
#    Actions → Enable workflows → Run workflow
```

### ⭐ Step 3: 완료! (2분)

```
✅ 첫 실행: 기존 기사 저장 (알림 없음)
✅ 다음 실행: 새 기사만 알림
✅ 15분마다 자동 실행
✅ Tesla 뉴스 발행 시 즉시 Telegram 알림!
```

---

## 📁 프로젝트 구조

```
tesla-monitor/
│
├── README.md                           # 이 파일
├── START_HERE.md                       # 빠른 시작 가이드
├── TELEGRAM_SETUP_GUIDE.md             # Telegram 설정 상세 가이드
│
├── python-monitor/                     # 메인 모니터링 스크립트
│   ├── monitor_rss.py                  # RSS 피드 모니터링 (메인)
│   ├── requirements.txt                # Python 의존성
│   ├── test_local.sh                   # 로컬 테스트 스크립트
│   ├── env.example                     # 환경 변수 예시
│   ├── README.md                       # 사용 가이드
│   └── backup/                         # 백업 파일
│       └── monitor_website_scraping.py # 이전 버전 (참고용)
│
├── .github/workflows/
│   └── monitor.yml                     # GitHub Actions 설정
│
└── docs/                               # 추가 문서
    ├── QUICKSTART.md
    ├── RAILWAY_DEPLOY_GUIDE.md
    └── ...
```

---

## 🔧 환경 변수 설정

### python-monitor/.env (로컬 테스트용)

```bash
# Telegram Bot 설정
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321

# 데이터 저장 디렉토리
DATA_DIR=./data
```

### GitHub Secrets (프로덕션용)

```
Repository → Settings → Secrets and variables → Actions

Name: TELEGRAM_BOT_TOKEN
Secret: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz

Name: TELEGRAM_CHAT_ID
Secret: 987654321
```

---

## 📝 작동 방식

### 1단계: RSS 피드 파싱
```python
feed = feedparser.parse("https://electrek.co/guides/tesla/feed/")
# 최신 10개 기사 가져오기
```

### 2단계: Tesla 관련 필터링
```python
if 'tesla' in article.title.lower():
    # Tesla 관련 기사!
```

### 3단계: 중복 체크
```python
if article_id not in seen_articles:
    # 새 기사 발견!
```

### 4단계: Telegram 전송
```python
post_to_telegram(article)
# 🚗⚡ Tesla 뉴스 업데이트!
```

### 5단계: 기사 ID 저장
```python
seen_articles.add(article_id)
save_to_file()
# 다음번 중복 방지
```

---

## 🧪 로컬 테스트

### 방법 1: 자동 스크립트 (추천)

```bash
cd python-monitor
./test_local.sh
```

### 방법 2: 수동 실행

```bash
cd python-monitor

# 환경 변수 설정
cp env.example .env
nano .env  # Token과 Chat ID 입력

# 의존성 설치
pip install -r requirements.txt

# 실행
python monitor_rss.py
```

### 예상 출력

```
============================================================
Tesla RSS Monitor 시작: 2026-01-18 15:30:00
============================================================
피드 체크: Tesla Blog
피드 체크: Electrek
피드 체크: Teslarati
...
새 기사 총 5개 발견
포스팅: 5개
============================================================
모니터링 완료!
============================================================
```

---

## 💰 비용 분석 (2026년 1월 기준)

### ✅ 완전 무료!

```
RSS 피드 API:         $0/월 (공개 표준)
Telegram Bot API:     $0/월 (무료!)
GitHub Actions:       $0/월 (2,000분 무료)
저장 공간:            $0/월 (Artifacts 무료)
───────────────────────────────────────
총 비용:              $0/월 🎉
연간 비용:            $0/년 🎉
```

**예상 사용량:**
- 15분마다 실행: 96회/일
- 1회 실행 시간: ~30초
- 일일 사용량: 48분
- 월간 사용량: 1,440분
- GitHub 무료 한도: 2,000분 ✅

### 💡 다른 방법과 비교

| 방법 | 모니터링 | 알림 | 월 비용 | 차단 위험 |
|------|----------|------|---------|-----------|
| **현재 (RSS + Telegram)** | RSS 피드 | Telegram | **$0** ✅ | ❌ 없음 |
| 웹 스크래핑 + X API | Tesla.com | Twitter | $100+ | ✅ 높음 |
| changedetection.io | Tesla.com | Twitter | $120+ | ✅ 높음 |

**결론: RSS + Telegram = 최고의 조합!** 🏆

---

## 🎯 커스터마이징

### RSS 피드 추가/제거

`python-monitor/monitor_rss.py`:
```python
RSS_FEEDS = {
    "Tesla Blog": "https://www.tesla.com/blog/rss",
    "Electrek": "https://electrek.co/guides/tesla/feed/",
    # 원하는 피드 추가
    "Your Feed": "https://example.com/feed/",
}
```

### 키워드 필터링 변경

```python
tesla_keywords = [
    'tesla', 'model 3', 'cybertruck',
    'elon musk', 'fsd', 'autopilot',
    # 원하는 키워드 추가
    '한국', 'korea', '가격',
]
```

### 알림 개수 조정

```python
for article in all_new_articles[:5]:  # 5 → 원하는 숫자
    post_to_telegram(article)
```

### 체크 주기 변경

`.github/workflows/monitor.yml`:
```yaml
schedule:
  # 15분마다 (기본)
  - cron: '*/15 * * * *'
  
  # 30분마다로 변경하려면:
  # - cron: '*/30 * * * *'
```

---

## 📱 Telegram 알림 예시

```
🚗⚡ Tesla 뉴스 업데이트!

Tesla Announces Major Model 3 Software Update

📰 출처: Electrek
📅 2026-01-18 15:30

Tesla has announced a significant software 
update for Model 3 owners, including new 
Autopilot features and improved range...

🔗 자세히 보기

#Tesla #테슬라 #TeslaNews
```

---

## 🐛 문제 해결

### Telegram 알림이 안 옴

**1. Secrets 확인**
```
GitHub → Settings → Secrets
- TELEGRAM_BOT_TOKEN 값 확인
- TELEGRAM_CHAT_ID 값 확인
```

**2. Bot 활성화**
```
Telegram에서 Bot 검색
/start 명령어 전송
```

**3. 로그 확인**
```
Actions → Tesla Monitor → 최근 실행 → Logs
```

### "이미 본 기사"만 나옴

**정상입니다!**
- 첫 실행: 기존 기사를 "본 것"으로 저장
- 다음 실행부터: 새 기사만 알림
- 15분 후 다시 확인하세요

### RSS 피드 파싱 실패

**일시적 오류일 수 있습니다**
- 다음 실행에서 자동 재시도
- 일부 피드만 실패해도 다른 피드는 정상 작동

### GitHub Actions가 실행 안됨

**1. Workflow 활성화 확인**
```
Actions → Enable workflows
```

**2. 수동 실행**
```
Actions → Tesla Monitor → Run workflow
```

---

## 📊 프로젝트 통계

```
언어:        Python 3.11
라이브러리:  feedparser, requests
실행 환경:   GitHub Actions
알림:        Telegram Bot
비용:        $0/월
업타임:      99.9%+
```

---

## 🚀 고급 기능 (향후 추가 가능)

### 1. 데이터베이스 연동
```python
# PostgreSQL에 기사 히스토리 저장
# 통계 및 분석 가능
```

### 2. 웹 대시보드
```python
# React + FastAPI로 대시보드 구축
# 기사 히스토리, 통계 시각화
```

### 3. AI 요약
```python
# OpenAI GPT-4로 기사 요약
# 중요도 자동 분석
```

### 4. 멀티 플랫폼
```python
# Telegram + Discord + Slack
# 여러 채널에 동시 알림
```

---

## 📚 문서

- **[START_HERE.md](START_HERE.md)** - 빠른 시작 가이드 (필독!)
- **[TELEGRAM_SETUP_GUIDE.md](TELEGRAM_SETUP_GUIDE.md)** - Telegram 설정 상세 가이드
- **[python-monitor/README.md](python-monitor/README.md)** - RSS 모니터링 가이드
- [docs/QUICKSTART.md](docs/QUICKSTART.md) - 빠른 시작 (구버전)
- [docs/X_API_SETUP_GUIDE.md](docs/X_API_SETUP_GUIDE.md) - X API 설정 (참고용)

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

- [feedparser](https://github.com/kurtmckee/feedparser) - RSS 파싱 라이브러리
- [Telegram Bot API](https://core.telegram.org/bots/api) - 무료 알림 서비스
- [GitHub Actions](https://github.com/features/actions) - 무료 CI/CD
- Tesla 뉴스 사이트들 - Electrek, Teslarati, InsideEVs, Tesla North

---

## 📞 연락처

질문이나 제안이 있으시면 이슈를 열어주세요!

- GitHub Issues: [tesla-monitor/issues](https://github.com/Daesung-Kwon/tesla-monitor/issues)
- GitHub Discussions: 질문 및 토론

---

## ⭐ Star History

프로젝트가 마음에 드셨다면 ⭐️ Star를 눌러주세요!

---

## 🎓 학습 자료

이 프로젝트를 통해 배울 수 있는 것:
- ✅ RSS 피드 파싱 및 모니터링
- ✅ Telegram Bot API 사용
- ✅ GitHub Actions CI/CD
- ✅ Python 자동화 스크립트
- ✅ 무료 인프라 활용

---

**Made with ❤️ by Tesla Enthusiasts**

🚗⚡ Happy Monitoring! 🚗⚡

---

## 🎯 빠른 체크리스트

```
□ Telegram Bot 생성 (@BotFather)
□ Chat ID 확인 (@userinfobot)
□ GitHub Repository 생성
□ 코드 푸시 (git push)
□ GitHub Secrets 설정
□ GitHub Actions 활성화
□ 첫 실행 확인
□ Telegram에서 알림 확인
□ 완료! 🎉
```

**지금 바로 시작하세요!** → [START_HERE.md](START_HERE.md)
