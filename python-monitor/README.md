# Tesla Monitor - Pure Python Version

changedetection.io 없이 순수 Python으로 구현한 버전입니다.
**Telegram Bot으로 알림 (완전 무료!)**

## 🚀 빠른 시작

### 1. Telegram Bot 설정

```bash
# 1. @BotFather에게 /newbot
# 2. Token 받기
# 3. @userinfobot에게 /start
# 4. Chat ID 받기
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
cp env.example .env

# 편집
nano .env
```

`.env` 내용:
```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=987654321
DATA_DIR=./data
```

### 3. 로컬 실행

```bash
# 방법 1: 자동 스크립트
./test_local.sh

# 방법 2: 수동 실행
pip install -r requirements.txt
python monitor.py
```

### 4. GitHub Actions 배포

```bash
# 1. GitHub에 푸시
git push

# 2. GitHub Secrets 설정
#    - TELEGRAM_BOT_TOKEN
#    - TELEGRAM_CHAT_ID

# 3. Actions 활성화
#    Actions → Enable workflows

# 4. 자동 실행 (15분마다)
```

## 📊 작동 방식

```
[Tesla.com] ← requests로 HTML 다운로드
     ↓
[해시 계산] ← SHA256
     ↓
[이전과 비교] ← 변경 감지
     ↓
[Diff 계산] ← difflib
     ↓
[키워드 필터링] ← 중요 변경만
     ↓
[Telegram 전송] ← 무료 알림!
```

## 🎯 모니터링 대상

- https://www.tesla.com/
- https://www.tesla.com/cybertruck
- https://www.tesla.com/model3
- https://www.tesla.com/modely
- https://www.tesla.com/modelx
- https://www.tesla.com/models
- https://www.tesla.com/energy
- https://www.tesla.com/ko_kr
- https://www.tesla.com/support/software-updates

`monitor.py`에서 추가/삭제 가능

## 💰 비용

**완전 무료!**

- Telegram Bot API: $0
- GitHub Actions: $0 (2,000분/월 무료)

## 🔧 커스터마이징

### 키워드 변경

`monitor.py`:
```python
IMPORTANT_KEYWORDS = [
    'price', 'pricing', '원',
    'new', 'launch', 'delivery',
    # 여기에 추가
]
```

### 메시지 포맷

```python
def format_message(url: str, diff_snippet: str) -> str:
    # 원하는 형태로 변경
    message = f"🚗⚡ 업데이트!\n\n{summary}\n\n{url}"
    return message
```

### 체크 주기

`.github/workflows/monitor.yml`:
```yaml
schedule:
  - cron: '*/30 * * * *'  # 30분마다
```

## 📝 파일 구조

```
python-monitor/
├── monitor.py           # 메인 스크립트
├── requirements.txt     # Python 의존성
├── railway.json         # Railway Cron 설정
├── env.example          # 환경 변수 예시
├── test_local.sh        # 로컬 테스트 스크립트
└── data/                # 데이터 저장 (자동 생성)
    ├── xxxxx.html       # 이전 HTML
    └── xxxxx.hash       # 이전 해시
```

## 🐛 문제 해결

### Telegram 메시지가 안 옴

1. Token/Chat ID 확인
2. Bot과 대화 시작 (`/start`)
3. 로그 확인: `python monitor.py`

### "첫 실행"만 나옴

정상입니다! 첫 실행은 초기 데이터만 저장합니다.
다시 실행하면 변경 감지를 시작합니다.

## 📚 추가 문서

- [Telegram 설정 가이드](../TELEGRAM_SETUP_GUIDE.md)
- [프로젝트 전체 요약](../PROJECT_SUMMARY.md)
- [비용 분석](../docs/QUICKSTART.md)

---

**Made with ❤️ by Tesla Enthusiasts**

🚗⚡ Happy Monitoring! 🚗⚡
