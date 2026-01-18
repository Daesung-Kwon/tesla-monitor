# 순수 Python 대안 (changedetection.io 없이)

changedetection.io 대신 순수 Python으로 직접 구현하는 방법입니다.
Railway Cron Jobs 또는 GitHub Actions로 실행하면 비용이 훨씬 저렴합니다 ($1-2/월).

## 📋 장단점 비교

### changedetection.io 방식
✅ GUI로 쉽게 설정
✅ Playwright 렌더링 내장
✅ 스크린샷 자동 캡처
❌ 비용 높음 (~$21/월)
❌ 커스터마이징 제한

### 순수 Python 방식
✅ 완전한 커스터마이징
✅ 비용 매우 낮음 (~$1-2/월)
✅ 코드 제어 가능
❌ 직접 구현 필요
❌ JavaScript 렌더링 복잡

---

## 🚀 구현 코드

### 1. Python 모니터링 스크립트

`monitor.py`:
```python
"""
Tesla Website Monitor - Pure Python Implementation
changedetection.io 없이 순수 Python으로 구현
"""

import requests
import tweepy
import hashlib
import os
import time
import difflib
from datetime import datetime
from typing import Optional, Dict, List
import json
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# X API 설정
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")

# 모니터링 대상 URL
TESLA_URLS = [
    "https://www.tesla.com/",
    "https://www.tesla.com/cybertruck",
    "https://www.tesla.com/model3",
    "https://www.tesla.com/modely",
    "https://www.tesla.com/modelx",
    "https://www.tesla.com/models",
    "https://www.tesla.com/energy",
    "https://www.tesla.com/ko_kr",
    "https://www.tesla.com/support/software-updates",
]

# 중요 키워드
IMPORTANT_KEYWORDS = [
    'price', 'pricing', '₩', 'won', 'krw', 'usd', '$', '원',
    'new', 'launch', 'available', 'delivery', 'inventory',
    'order', 'reserve', 'update', 'refresh', 'facelift',
    'software', 'fsd', 'autopilot', 'version',
    'event', 'reveal', 'unveil', '한국', 'korea',
]

# 데이터 저장 경로
DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)


def get_page_content(url: str) -> Optional[str]:
    """웹페이지 내용 가져오기"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"페이지 가져오기 실패 {url}: {e}")
        return None


def get_content_hash(content: str) -> str:
    """내용의 해시값 계산"""
    return hashlib.sha256(content.encode()).hexdigest()


def load_previous_hash(url: str) -> Optional[str]:
    """이전 해시값 불러오기"""
    filename = os.path.join(DATA_DIR, f"{hashlib.md5(url.encode()).hexdigest()}.hash")
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read().strip()
    return None


def save_current_hash(url: str, content_hash: str):
    """현재 해시값 저장"""
    filename = os.path.join(DATA_DIR, f"{hashlib.md5(url.encode()).hexdigest()}.hash")
    with open(filename, 'w') as f:
        f.write(content_hash)


def load_previous_content(url: str) -> Optional[str]:
    """이전 내용 불러오기"""
    filename = os.path.join(DATA_DIR, f"{hashlib.md5(url.encode()).hexdigest()}.html")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def save_current_content(url: str, content: str):
    """현재 내용 저장"""
    filename = os.path.join(DATA_DIR, f"{hashlib.md5(url.encode()).hexdigest()}.html")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def get_text_diff(old_content: str, new_content: str) -> str:
    """두 내용의 차이 계산"""
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    
    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        lineterm='',
        n=0  # 컨텍스트 줄 수
    )
    
    diff_text = '\n'.join(diff)
    return diff_text


def is_significant_change(diff: str, url: str) -> bool:
    """중요한 변경인지 판단"""
    if not diff or len(diff) < 50:
        return False
    
    diff_lower = diff.lower()
    
    # 중요 키워드 체크
    for keyword in IMPORTANT_KEYWORDS:
        if keyword.lower() in diff_lower:
            logger.info(f"중요 키워드 감지: {keyword}")
            return True
    
    # 변경량이 충분히 큰지
    lines = [l for l in diff.split('\n') if l.startswith('+') or l.startswith('-')]
    if len(lines) > 10:
        return True
    
    return False


def format_tweet_message(url: str, diff_snippet: str) -> str:
    """트윗 메시지 포맷팅"""
    page_name = "테슬라 홈페이지"
    if "cybertruck" in url.lower():
        page_name = "사이버트럭 페이지"
    elif "model3" in url.lower():
        page_name = "모델3 페이지"
    elif "modely" in url.lower():
        page_name = "모델Y 페이지"
    elif "modelx" in url.lower():
        page_name = "모델X 페이지"
    elif "models" in url.lower():
        page_name = "모델S 페이지"
    elif "energy" in url.lower():
        page_name = "에너지 페이지"
    elif "software" in url.lower():
        page_name = "소프트웨어 업데이트"
    elif "ko_kr" in url.lower():
        page_name = "테슬라 한국"
    
    # diff에서 의미있는 변경만 추출
    added_lines = [l[1:].strip() for l in diff_snippet.split('\n') 
                   if l.startswith('+') and len(l.strip()) > 5]
    
    if added_lines:
        summary = added_lines[0][:100]
    else:
        summary = "중요한 변경 감지"
    
    message = f"""🚗⚡ {page_name}에 변경 감지!

{summary}

{url}

#Tesla #테슬라 #TeslaUpdates"""
    
    # 280자 제한
    if len(message) > 280:
        summary = summary[:100] + "..."
        message = f"🚗⚡ {page_name} 업데이트!\n\n{summary}\n\n{url}\n\n#Tesla"
    
    return message


def post_to_twitter(message: str) -> bool:
    """X에 포스팅"""
    if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET]):
        logger.error("X API 인증 정보 없음")
        return False
    
    try:
        client = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_SECRET
        )
        
        response = client.create_tweet(text=message)
        logger.info(f"트윗 성공: {response.data['id']}")
        return True
        
    except Exception as e:
        logger.error(f"트윗 실패: {e}")
        return False


def monitor_url(url: str) -> bool:
    """URL 하나 모니터링"""
    logger.info(f"모니터링 시작: {url}")
    
    # 현재 내용 가져오기
    current_content = get_page_content(url)
    if not current_content:
        return False
    
    # 현재 해시 계산
    current_hash = get_content_hash(current_content)
    
    # 이전 해시 불러오기
    previous_hash = load_previous_hash(url)
    
    # 첫 실행 (이전 데이터 없음)
    if not previous_hash:
        logger.info(f"첫 실행 - 초기 데이터 저장: {url}")
        save_current_hash(url, current_hash)
        save_current_content(url, current_content)
        return False
    
    # 변경 없음
    if current_hash == previous_hash:
        logger.info(f"변경 없음: {url}")
        return False
    
    # 변경 감지!
    logger.info(f"변경 감지: {url}")
    
    # 이전 내용 불러오기
    previous_content = load_previous_content(url)
    if not previous_content:
        logger.warning("이전 내용 없음 - 저장만 하고 종료")
        save_current_hash(url, current_hash)
        save_current_content(url, current_content)
        return False
    
    # Diff 계산
    diff = get_text_diff(previous_content, current_content)
    
    # 중요한 변경인지 판단
    if not is_significant_change(diff, url):
        logger.info("중요하지 않은 변경 - 스킵")
        save_current_hash(url, current_hash)
        save_current_content(url, current_content)
        return False
    
    # 트윗 메시지 생성
    message = format_tweet_message(url, diff)
    logger.info(f"트윗 메시지:\n{message}")
    
    # X에 포스팅
    success = post_to_twitter(message)
    
    # 현재 상태 저장
    save_current_hash(url, current_hash)
    save_current_content(url, current_content)
    
    return success


def monitor_all():
    """모든 URL 모니터링"""
    logger.info("=" * 60)
    logger.info(f"Tesla Monitor 시작: {datetime.now()}")
    logger.info("=" * 60)
    
    results = []
    for url in TESLA_URLS:
        try:
            result = monitor_url(url)
            results.append((url, result))
            time.sleep(2)  # Rate limiting
        except Exception as e:
            logger.error(f"오류 발생 {url}: {e}")
            results.append((url, False))
    
    # 결과 요약
    logger.info("=" * 60)
    logger.info("모니터링 완료!")
    posted = sum(1 for _, r in results if r)
    logger.info(f"포스팅: {posted}/{len(results)}")
    logger.info("=" * 60)


if __name__ == "__main__":
    monitor_all()
```

---

## 2. Railway 배포 (Cron Jobs)

### 2.1 프로젝트 구조
```
tesla-monitor-python/
├── monitor.py
├── requirements.txt
└── railway.json
```

### 2.2 `requirements.txt`
```
requests==2.31.0
tweepy==4.14.0
```

### 2.3 `railway.json` (Cron Jobs)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "cronSchedule": "*/15 * * * *",
    "startCommand": "python monitor.py"
  }
}
```

### 2.4 Railway에 배포
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
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

### 2.5 비용
- **Cron Job**: 실행 시간만 과금
- **예상**: 15분마다 30초 실행 = 48분/일 = 1440분/월 = ~$1-2/월 ✅

---

## 3. GitHub Actions 대안 (완전 무료!)

### `.github/workflows/monitor.yml`
```yaml
name: Tesla Monitor

on:
  schedule:
    # 15분마다 실행
    - cron: '*/15 * * * *'
  workflow_dispatch:  # 수동 실행 가능

jobs:
  monitor:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install requests tweepy
      
      - name: Create data directory
        run: mkdir -p data
      
      - name: Download previous data
        uses: actions/download-artifact@v3
        with:
          name: monitor-data
          path: data
        continue-on-error: true
      
      - name: Run monitor
        env:
          X_API_KEY: ${{ secrets.X_API_KEY }}
          X_API_SECRET: ${{ secrets.X_API_SECRET }}
          X_ACCESS_TOKEN: ${{ secrets.X_ACCESS_TOKEN }}
          X_ACCESS_SECRET: ${{ secrets.X_ACCESS_SECRET }}
          DATA_DIR: ./data
        run: python monitor.py
      
      - name: Upload data
        uses: actions/upload-artifact@v3
        with:
          name: monitor-data
          path: data
          retention-days: 90
```

### GitHub Secrets 설정
1. Repository → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. 다음 4개 추가:
   - `X_API_KEY`
   - `X_API_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_SECRET`

### 비용
- **GitHub Actions**: 2,000분/월 무료
- **예상 사용량**: 48분/일 = 1,440분/월 ✅ 충분!
- **완전 무료** 🎉

---

## 4. Playwright로 JavaScript 렌더링 추가

일부 페이지는 JavaScript 렌더링이 필요합니다.

### 4.1 의존성 추가
```txt
playwright==1.40.0
```

### 4.2 코드 수정
```python
from playwright.sync_api import sync_playwright

def get_page_content_with_js(url: str) -> Optional[str]:
    """Playwright로 JavaScript 렌더링"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            content = page.content()
            browser.close()
            return content
    except Exception as e:
        logger.error(f"Playwright 오류 {url}: {e}")
        return None


# URL별로 선택적으로 사용
def get_page_content(url: str) -> Optional[str]:
    # JavaScript가 필요한 페이지
    if any(path in url for path in ['inventory', 'design', 'order']):
        return get_page_content_with_js(url)
    else:
        # 일반 requests
        return get_page_content_simple(url)
```

### 4.3 Railway 배포 시 주의
Playwright는 브라우저 바이너리가 필요하므로 Dockerfile 사용:

`Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Playwright 의존성
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install chromium

COPY . .

CMD ["python", "monitor.py"]
```

---

## 5. 고급 기능

### 5.1 스크린샷 캡처
```python
def capture_screenshot(url: str) -> Optional[str]:
    """스크린샷 캡처 후 이미지 경로 반환"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            
            screenshot_path = f"{DATA_DIR}/{hashlib.md5(url.encode()).hexdigest()}.png"
            page.screenshot(path=screenshot_path, full_page=False)
            browser.close()
            
            return screenshot_path
    except Exception as e:
        logger.error(f"스크린샷 실패: {e}")
        return None
```

### 5.2 이미지 첨부 트윗
```python
def post_to_twitter_with_image(message: str, image_path: str) -> bool:
    """이미지 첨부 트윗"""
    auth = tweepy.OAuth1UserHandler(
        X_API_KEY, X_API_SECRET,
        X_ACCESS_TOKEN, X_ACCESS_SECRET
    )
    api_v1 = tweepy.API(auth)
    
    # 이미지 업로드
    media = api_v1.media_upload(image_path)
    
    # 트윗 포스팅
    client = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET
    )
    
    response = client.create_tweet(text=message, media_ids=[media.media_id])
    return True
```

### 5.3 데이터베이스 저장
```python
import sqlite3

def init_db():
    conn = sqlite3.connect(f"{DATA_DIR}/monitor.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS changes (
            id INTEGER PRIMARY KEY,
            url TEXT,
            timestamp TEXT,
            diff TEXT,
            posted BOOLEAN
        )
    """)
    conn.commit()
    conn.close()

def save_change(url: str, diff: str, posted: bool):
    conn = sqlite3.connect(f"{DATA_DIR}/monitor.db")
    conn.execute(
        "INSERT INTO changes (url, timestamp, diff, posted) VALUES (?, ?, ?, ?)",
        (url, datetime.now().isoformat(), diff, posted)
    )
    conn.commit()
    conn.close()
```

### 5.4 이메일 알림
```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert(url: str, diff: str):
    """중요한 변경 시 이메일 알림"""
    msg = MIMEText(f"변경 감지: {url}\n\n{diff}")
    msg['Subject'] = f'Tesla Monitor Alert: {url}'
    msg['From'] = os.getenv('EMAIL_FROM')
    msg['To'] = os.getenv('EMAIL_TO')
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_FROM'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)
```

---

## 6. 비교: changedetection.io vs 순수 Python

| 항목 | changedetection.io | 순수 Python |
|------|-------------------|-------------|
| 설정 난이도 | ⭐⭐ 쉬움 | ⭐⭐⭐⭐ 어려움 |
| 월 비용 | ~$21 | ~$1-2 (또는 무료) |
| JavaScript | ✅ 내장 | ⚠️ Playwright 필요 |
| 스크린샷 | ✅ 자동 | 🔧 직접 구현 |
| 커스터마이징 | ⚠️ 제한적 | ✅ 완전 자유 |
| GUI | ✅ 있음 | ❌ 없음 |
| 유지보수 | ⭐⭐⭐ 쉬움 | ⭐⭐⭐⭐ 어려움 |

---

## 7. 추천 시나리오

### 시나리오 1: 빠른 시작 (초보자)
→ **changedetection.io + Railway**
- GUI로 쉽게 설정
- 비용은 비싸지만 관리 편함

### 시나리오 2: 비용 절약 (중급)
→ **순수 Python + GitHub Actions**
- 완전 무료
- 코딩 지식 필요

### 시나리오 3: 최고 성능 (고급)
→ **순수 Python + Railway Cron + Playwright**
- 완전 커스터마이징
- JavaScript 렌더링 지원
- 월 $2 정도

---

## 📚 추가 리소스
- [Playwright Python Docs](https://playwright.dev/python/)
- [Tweepy Documentation](https://docs.tweepy.org/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Railway Cron Jobs](https://docs.railway.app/reference/cron-jobs)

완벽한 대안 구현! 🎉
