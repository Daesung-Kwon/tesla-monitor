# Tesla Monitor - RSS Feed Version

Tesla 관련 RSS 피드를 모니터링하여 Telegram으로 알림을 보냅니다.
**완전 무료 & 차단 없음!**

## 🎯 모니터링 대상

### RSS 피드 목록
- **Tesla 공식 블로그**: https://www.tesla.com/blog/rss
- **Electrek**: Tesla 전문 뉴스 사이트
- **Teslarati**: Tesla 뉴스 & 업데이트
- **InsideEVs**: 전기차 뉴스
- **Tesla North**: Tesla 캐나다 뉴스

### 자동 필터링
- ✅ Tesla 관련 기사만 선별
- ✅ 중복 제거 (이미 본 기사는 스킵)
- ✅ 최신 뉴스 우선

## 🚀 빠른 시작

### 1. 로컬 실행

```bash
# 환경 변수 설정
cp env.example .env
nano .env  # Telegram Bot Token & Chat ID 입력

# 테스트 실행
./test_local.sh

# 또는 수동:
pip install -r requirements.txt
python monitor_rss.py
```

### 2. GitHub Actions 배포

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
[RSS 피드들] ← feedparser로 파싱
     ↓
[새 기사 감지] ← 이전 기사와 비교
     ↓
[Tesla 관련 필터링] ← 키워드 체크
     ↓
[Telegram 전송] ← 최대 5개까지
     ↓
[기사 ID 저장] ← 중복 방지
```

## 🎯 주요 기능

- ✅ **RSS 피드 모니터링**: 5개 주요 뉴스 소스
- ✅ **자동 필터링**: Tesla 관련 기사만
- ✅ **중복 제거**: 같은 기사는 한 번만
- ✅ **스팸 방지**: 한 번에 최대 5개 알림
- ✅ **차단 없음**: RSS는 공개 API
- ✅ **완전 무료**: $0/월

## 💰 비용

```
RSS 피드:         무료 ✅
Telegram Bot:     무료 ✅
GitHub Actions:   무료 ✅
──────────────────────
총 비용: $0/월 🎉
```

## 🔧 커스터마이징

### RSS 피드 추가/제거

`monitor_rss.py`:
```python
RSS_FEEDS = {
    "Tesla Blog": "https://www.tesla.com/blog/rss",
    "Electrek": "https://electrek.co/guides/tesla/feed/",
    # 여기에 추가
    "Your Feed": "https://example.com/feed/",
}
```

### 키워드 변경

```python
tesla_keywords = [
    'tesla', 'model 3', 'cybertruck',
    # 원하는 키워드 추가
    '한국', 'korea', '출시',
]
```

### 알림 개수 조정

```python
for article in all_new_articles[:5]:  # 5 → 원하는 숫자
```

## 📝 파일 구조

```
python-monitor/
├── monitor_rss.py       # RSS 피드 모니터링 (메인)
├── monitor.py           # 웹사이트 직접 모니터링 (사용 안함)
├── requirements.txt     # Python 의존성
├── test_local.sh        # 로컬 테스트 스크립트
└── data/
    └── seen_articles.json  # 본 기사 ID 저장
```

## 📊 예상 동작

### 첫 실행
```
Tesla RSS Monitor 시작
피드 체크: Tesla Blog
피드 체크: Electrek
...
새 기사 총 15개 발견
포스팅: 5개 (스팸 방지)
```

### 다음 실행 (15분 후)
```
이미 본 기사: 15개
새 기사 총 2개 발견
포스팅: 2개
```

### Telegram 메시지
```
🚗⚡ Tesla 뉴스 업데이트!

Tesla Announces New Model 3 Update

📰 출처: Electrek
📅 2026-01-18 15:30

Tesla has announced a major update...

🔗 자세히 보기

#Tesla #테슬라 #TeslaNews
```

## 🐛 문제 해결

### "이미 본 기사"만 나옴
정상입니다! 첫 실행은 기존 기사를 모두 "본 것"으로 표시합니다.
다음 실행부터 새 기사만 알림을 보냅니다.

### RSS 피드 파싱 실패
일부 피드가 일시적으로 접근 불가할 수 있습니다.
다음 실행에서 자동으로 재시도됩니다.

### Telegram 전송 실패
- Bot Token / Chat ID 확인
- Bot과 대화 시작 (`/start`)

## 🎓 RSS vs 웹사이트 직접 모니터링

| 항목 | RSS 피드 | 웹사이트 직접 |
|------|----------|--------------|
| 차단 위험 | ❌ 없음 | ✅ 높음 (403) |
| 안정성 | ✅ 높음 | ❌ 낮음 |
| 속도 | ✅ 빠름 | ❌ 느림 |
| 비용 | ✅ 무료 | ✅ 무료 |
| 정보 품질 | ✅ 공식 뉴스 | ⚠️ HTML 파싱 |

**결론**: RSS 피드가 훨씬 좋습니다! 🎉

## 📚 추가 문서

- [Telegram 설정 가이드](../TELEGRAM_SETUP_GUIDE.md)
- [프로젝트 전체 요약](../PROJECT_SUMMARY.md)

---

**Made with ❤️ for Tesla Fans**

🚗⚡ Happy Monitoring! 🚗⚡
