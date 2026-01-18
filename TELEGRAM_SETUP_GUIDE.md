# 🚀 Tesla Monitor - Telegram 버전 시작 가이드

**완전 무료 ($0/월)** 조합으로 테슬라 모니터링 시작하기!

```
✅ Python + GitHub Actions + Telegram Bot
💰 월 비용: $0
⏱️ 소요 시간: 10분
```

---

## 📋 전체 흐름

```
[Tesla.com] ← 15분마다 체크
     ↓
[GitHub Actions] ← 무료 실행
     ↓
[monitor.py] ← 변경 감지
     ↓
[Telegram Bot] ← 알림 전송
     ↓
[내 Telegram] ← 메시지 수신 🎉
```

---

## 🎯 Step 1: Telegram Bot 생성 (3분)

### 1-1. BotFather에게 Bot 생성 요청

1. **Telegram 앱 열기** (모바일/데스크톱)

2. **@BotFather 검색**
   - 검색창에 `@BotFather` 입력
   - 파란색 체크마크 있는 공식 봇 선택

3. **대화 시작**
   ```
   /start
   ```

4. **새 봇 생성**
   ```
   /newbot
   ```

5. **봇 이름 입력** (원하는 이름, 한글 가능)
   ```
   Tesla Monitor Bot
   ```

6. **봇 유저네임 입력** (영문, 숫자, 밑줄만 / 반드시 'bot'으로 끝나야 함)
   ```
   teslamonitor_bot
   ```

7. **Token 받기** 🔑
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
   
   ⚠️ **중요**: 이 Token을 안전하게 복사해두세요!

### 1-2. Chat ID 확인

1. **@userinfobot 검색**

2. **메시지 보내기**
   ```
   /start
   ```

3. **Your ID 복사** (숫자)
   ```
   987654321
   ```

### 1-3. 테스트 (선택)

터미널에서 테스트:
```bash
# Token과 Chat ID를 실제 값으로 변경
curl -X POST "https://api.telegram.org/bot123456789:ABCdef.../sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "987654321",
    "text": "🚗⚡ Tesla Monitor 테스트!"
  }'
```

성공하면 Telegram에 메시지가 도착합니다! ✅

---

## 🐙 Step 2: GitHub Repository 생성 (3분)

### 2-1. GitHub에 새 Repository 생성

1. **GitHub 접속**: https://github.com

2. **New repository** 클릭

3. **Repository 정보 입력**:
   - Repository name: `tesla-monitor`
   - Description: `Tesla website monitoring with Telegram notifications`
   - Public 또는 Private (둘 다 무료)
   - ✅ Add a README file (체크)

4. **Create repository** 클릭

### 2-2. 로컬 코드 업로드

```bash
# 프로젝트 디렉토리로 이동
cd /Users/malife/tesla-monitor

# Git 초기화 (이미 했다면 스킵)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Tesla Monitor with Telegram"

# GitHub repository 연결 (YOUR_USERNAME을 실제 GitHub 유저명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/tesla-monitor.git

# 푸시
git branch -M main
git push -u origin main
```

**완료!** 코드가 GitHub에 업로드되었습니다.

---

## 🔐 Step 3: GitHub Secrets 설정 (2분)

Telegram Bot Token과 Chat ID를 안전하게 저장합니다.

### 3-1. Secrets 페이지 접속

1. GitHub Repository 페이지에서:
   ```
   Settings → Secrets and variables → Actions
   ```

2. **"New repository secret"** 클릭

### 3-2. TELEGRAM_BOT_TOKEN 추가

- **Name**: `TELEGRAM_BOT_TOKEN`
- **Secret**: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` (Step 1에서 받은 Token)
- **Add secret** 클릭

### 3-3. TELEGRAM_CHAT_ID 추가

- **Name**: `TELEGRAM_CHAT_ID`
- **Secret**: `987654321` (Step 1에서 받은 Chat ID)
- **Add secret** 클릭

**완료!** 이제 2개의 Secret이 등록되었습니다:
- ✅ TELEGRAM_BOT_TOKEN
- ✅ TELEGRAM_CHAT_ID

---

## ▶️ Step 4: GitHub Actions 활성화 (1분)

### 4-1. Actions 탭으로 이동

Repository 페이지에서 **"Actions"** 탭 클릭

### 4-2. Workflows 활성화

초록색 버튼 클릭:
```
I understand my workflows, go ahead and enable them
```

### 4-3. 수동 실행 (첫 테스트)

1. **"Tesla Monitor"** workflow 클릭

2. **"Run workflow"** 버튼 클릭 (오른쪽)

3. **"Run workflow"** (초록색 버튼) 다시 클릭

4. **실행 시작!** ⚡

---

## ✅ Step 5: 확인 및 테스트

### 5-1. 실행 로그 확인

1. Actions 탭에서 방금 실행된 workflow 클릭

2. **"monitor"** job 클릭

3. **"Run monitor"** 단계 확인

예상 출력:
```
Tesla Monitor 시작: 2026-01-18 14:30:00
모니터링 시작: https://www.tesla.com/
첫 실행 - 초기 데이터 저장: https://www.tesla.com/
모니터링 시작: https://www.tesla.com/cybertruck
첫 실행 - 초기 데이터 저장: https://www.tesla.com/cybertruck
...
모니터링 완료!
포스팅: 0/9
```

✅ **성공!** 첫 실행이라 초기 데이터만 저장했습니다.

### 5-2. 15분 후 자동 실행 확인

**GitHub Actions는 15분마다 자동 실행됩니다!**

Cron 스케줄:
```yaml
schedule:
  - cron: '*/15 * * * *'  # 15분마다
```

### 5-3. 실제 변경 시 Telegram 알림

Tesla.com이 실제로 변경되면:
```
🚗⚡ 모델3 페이지에 변경 감지!

📝 Price: $39,000 → $38,000
    Delivery: 2-4 weeks

🔗 자세히 보기
https://www.tesla.com/model3

#Tesla #테슬라 #TeslaUpdates
```

이런 메시지가 Telegram으로 도착합니다!

---

## 🎨 Step 6: 커스터마이징 (선택)

### 6-1. 모니터링 페이지 추가/제거

`python-monitor/monitor.py` 수정:

```python
# 모니터링 대상 URL
TESLA_URLS = [
    "https://www.tesla.com/",
    "https://www.tesla.com/cybertruck",
    "https://www.tesla.com/model3",
    "https://www.tesla.com/modely",
    # 추가하고 싶은 페이지 여기에 추가
    "https://www.tesla.com/roadster",
    "https://www.tesla.com/semi",
]
```

### 6-2. 중요 키워드 변경

```python
# 중요 키워드 (이 단어가 포함된 변경만 알림)
IMPORTANT_KEYWORDS = [
    'price', 'pricing', '₩', 'won', 'krw', 'usd', '$', '원',
    'new', 'launch', 'available', 'delivery', 'inventory',
    'order', 'reserve', 'update', 'refresh', 'facelift',
    'software', 'fsd', 'autopilot', 'version',
    'event', 'reveal', 'unveil', '한국', 'korea',
    # 원하는 키워드 추가
    '가격', '출시', '예약',
]
```

### 6-3. 메시지 포맷 변경

```python
def format_message(url: str, diff_snippet: str) -> str:
    # 원하는 형태로 메시지 커스터마이징
    message = f"""🔔 <b>테슬라 업데이트!</b>

<i>{summary}</i>

<a href="{url}">링크</a>"""
    
    return message
```

### 6-4. 체크 주기 변경

`.github/workflows/monitor.yml` 수정:

```yaml
schedule:
  # 15분마다 (기본)
  - cron: '*/15 * * * *'
  
  # 30분마다로 변경하려면:
  # - cron: '*/30 * * * *'
  
  # 1시간마다로 변경하려면:
  # - cron: '0 * * * *'
```

변경 후 GitHub에 푸시:
```bash
git add .
git commit -m "Update monitoring settings"
git push
```

---

## 🔍 모니터링 및 관리

### 실행 상태 확인

```
GitHub Repository → Actions 탭
```

여기서 확인 가능:
- ✅ 마지막 실행 시간
- ✅ 성공/실패 여부
- ✅ 로그 상세 내역
- ✅ 다음 예정 실행 시간

### 일시 정지

**방법 1: Workflow 비활성화**
```
Actions → Tesla Monitor → ⋯ (메뉴) → Disable workflow
```

**방법 2: workflow 파일 삭제**
```bash
git rm .github/workflows/monitor.yml
git commit -m "Pause monitoring"
git push
```

### 재개

**방법 1: Workflow 활성화**
```
Actions → Tesla Monitor → ⋯ (메뉴) → Enable workflow
```

**방법 2: workflow 파일 복구**
```bash
git revert HEAD
git push
```

---

## 🐛 문제 해결

### Telegram 메시지가 안 옴

**1. Secrets 확인**
```
Settings → Secrets and variables → Actions
```
- TELEGRAM_BOT_TOKEN이 정확한지
- TELEGRAM_CHAT_ID가 정확한지

**2. Bot이 차단되지 않았는지**
- Telegram에서 Bot과 대화 시작
- `/start` 명령어 보내기

**3. Token 재생성**
- @BotFather에게 `/mybots` 전송
- 내 Bot 선택 → API Token → Revoke current token
- 새 Token으로 GitHub Secrets 업데이트

### GitHub Actions가 실행 안됨

**1. Workflow 활성화 확인**
```
Actions 탭 → 초록색 배너 확인
```

**2. workflow 파일 확인**
```bash
cat .github/workflows/monitor.yml
```

**3. 수동 실행 테스트**
```
Actions → Tesla Monitor → Run workflow
```

### "첫 실행"만 계속 나옴

**정상입니다!** 
- 첫 실행은 초기 데이터만 저장
- 15분 후부터 변경 감지 시작
- Tesla.com이 실제로 변경되어야 알림 옴

**강제로 테스트하려면:**
```bash
# 로컬에서 실행
cd /Users/malife/tesla-monitor/python-monitor
python monitor.py

# data/ 폴더의 파일 일부 삭제
rm data/*.html

# 다시 실행 (변경으로 인식됨)
python monitor.py
```

---

## 📊 비용 및 제약

### ✅ 완전 무료!

```
Telegram Bot API:     $0/월
GitHub Actions:       $0/월 (2,000분 무료)
저장 공간:            $0/월 (Artifacts 무료)
──────────────────────────
총 비용:              $0/월 🎉
```

### GitHub Actions 제약

**무료 플랜:**
- ✅ 2,000분/월 (충분함!)
- ✅ Public Repository 무제한
- ✅ Private Repository도 2,000분 가능

**예상 사용량:**
```
15분마다 실행: 96회/일
1회 실행 시간: 약 1분
──────────────────────────
일일 사용량: 96분
월간 사용량: 96 × 30 = 2,880분 ⚠️ 초과!

→ 해결: 30분마다 실행으로 변경
   30분마다: 48회/일 × 30일 = 1,440분 ✅
```

**30분으로 조정:**
```yaml
schedule:
  - cron: '*/30 * * * *'  # 30분마다
```

또는 **Private Repository를 Public으로:**
- Public Repository는 무제한!

---

## 🎉 완료!

축하합니다! Tesla Monitor가 가동 중입니다! 🚗⚡

### 다음 단계

1. ✅ **15-30분 기다리기** - 자동 실행 확인
2. ✅ **Telegram 확인** - 실제 변경 시 알림
3. ✅ **커스터마이징** - 페이지/키워드 추가
4. ✅ **친구와 공유** - Bot을 그룹에 추가

### 고급 기능 (향후)

- [ ] 이미지 첨부 (스크린샷)
- [ ] 데이터베이스 저장 (히스토리)
- [ ] 웹 대시보드 구축
- [ ] AI 요약 (GPT-4)
- [ ] 다중 언어 지원

---

## 📞 지원

- **GitHub Issues**: 버그 리포트
- **GitHub Discussions**: 질문/토론
- **Telegram**: @YOUR_USERNAME

---

## 📚 추가 문서

- [프로젝트 전체 요약](PROJECT_SUMMARY.md)
- [비용 분석](docs/QUICKSTART.md)
- [로컬 테스트](docs/LOCAL_DEVELOPMENT.md)

---

**Made with ❤️ by Tesla Enthusiasts**

🚗⚡ Happy Monitoring! 🚗⚡
