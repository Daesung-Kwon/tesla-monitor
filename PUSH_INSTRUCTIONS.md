# GitHub 푸시 가이드

코드가 준비되었습니다! 이제 GitHub에 푸시하는 방법입니다.

## 현재 상태 ✅

```bash
✅ Git 초기화 완료
✅ 25개 파일 커밋 완료 (4,563줄)
✅ Remote 설정 완료
⏳ 푸시 대기 중 (인증 필요)
```

---

## 방법 1: Personal Access Token (추천)

### Step 1: GitHub Token 생성

1. GitHub 웹사이트 접속
2. 우측 상단 프로필 → **Settings**
3. 좌측 메뉴 맨 아래 → **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token** → **Generate new token (classic)**
6. 설정:
   - Note: `tesla-monitor`
   - Expiration: `90 days` (또는 원하는 기간)
   - Scopes: ✅ **repo** (전체 체크)
7. **Generate token** 클릭
8. 생성된 Token 복사 (예: `ghp_xxxxxxxxxxxxxxxxxxxx`)
   ⚠️ 이 페이지를 벗어나면 다시 볼 수 없습니다!

### Step 2: 터미널에서 푸시

```bash
cd /Users/malife/tesla-monitor

# 푸시 (Username과 Password 입력 요청됨)
git push -u origin main
```

**입력 요청 시:**
- Username: `Daesung-Kwon`
- Password: `ghp_xxxxxxxxxxxxxxxxxxxx` (생성한 Token)

---

## 방법 2: SSH Key 사용

### Step 1: SSH Key 생성 (없는 경우)

```bash
# SSH Key 존재 확인
ls -la ~/.ssh/id_*.pub

# 없으면 생성
ssh-keygen -t ed25519 -C "your_email@example.com"
# Enter 3번 (기본 설정)

# Public Key 복사
cat ~/.ssh/id_ed25519.pub
```

### Step 2: GitHub에 SSH Key 등록

1. GitHub → Settings → **SSH and GPG keys**
2. **New SSH key** 클릭
3. Title: `MacBook`
4. Key: (복사한 public key 붙여넣기)
5. **Add SSH key** 클릭

### Step 3: Remote URL 변경 및 푸시

```bash
cd /Users/malife/tesla-monitor

# HTTPS → SSH로 변경
git remote set-url origin git@github.com:Daesung-Kwon/tesla-monitor.git

# 푸시
git push -u origin main
```

---

## 방법 3: GitHub Desktop 사용 (가장 쉬움!)

### Step 1: GitHub Desktop 설치

```bash
# Homebrew로 설치
brew install --cask github
```

### Step 2: GitHub Desktop에서 푸시

1. GitHub Desktop 실행
2. **File** → **Add Local Repository**
3. `/Users/malife/tesla-monitor` 선택
4. 상단의 **Publish repository** 클릭
5. **Name**: `tesla-monitor`
6. ✅ **Keep this code private** (이미 선택됨)
7. **Publish Repository** 클릭

---

## 추천 순서

**초보자**: 방법 3 (GitHub Desktop) → 가장 쉬움
**일반**: 방법 1 (Personal Access Token) → 한 번만 설정
**고급**: 방법 2 (SSH Key) → 영구적, 안전함

---

## 푸시 완료 확인

푸시 후 확인:
```
https://github.com/Daesung-Kwon/tesla-monitor
```

다음이 보이면 성공! ✅
- README.md
- 25 files
- "Initial commit: Tesla Monitor with Telegram Bot"

---

## 다음 단계

푸시가 완료되면:

1. ✅ **GitHub Secrets 설정**
   - Repository → Settings → Secrets and variables → Actions
   - `TELEGRAM_BOT_TOKEN` 추가
   - `TELEGRAM_CHAT_ID` 추가

2. ✅ **GitHub Actions 활성화**
   - Repository → Actions 탭
   - "I understand my workflows, go ahead and enable them" 클릭

3. ✅ **수동 실행 테스트**
   - Actions → Tesla Monitor → Run workflow

4. ✅ **로그 확인**
   - 실행 중인 workflow 클릭
   - "Run monitor" 단계 확인

---

## 문제 해결

### "Authentication failed"
→ Token이 잘못되었거나 만료됨. 다시 생성하세요.

### "Permission denied (publickey)"
→ SSH Key가 등록되지 않음. 방법 2의 Step 2 확인

### "Repository not found"
→ Repository URL 확인:
```bash
git remote -v
# origin	https://github.com/Daesung-Kwon/tesla-monitor.git
```

---

준비 완료! 위 방법 중 하나를 선택해서 푸시하세요! 🚀
