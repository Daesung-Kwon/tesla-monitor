"""
Tesla Website Monitor - Pure Python Implementation
changedetection.io 없이 순수 Python으로 구현
Telegram Bot으로 알림 전송 (완전 무료!)
"""

import requests
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

# Telegram Bot 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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


def format_message(url: str, diff_snippet: str) -> str:
    """Telegram 메시지 포맷팅 (HTML)"""
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
        summary = added_lines[0][:200]
    else:
        summary = "중요한 변경 감지"
    
    # Telegram HTML 포맷 (제한 없음!)
    message = f"""🚗⚡ <b>{page_name}에 변경 감지!</b>

📝 <i>{summary}</i>

🔗 <a href="{url}">자세히 보기</a>

#Tesla #테슬라 #TeslaUpdates"""
    
    # Telegram은 4096자까지 가능
    if len(message) > 4000:
        summary = summary[:200] + "..."
        message = f"""🚗⚡ <b>{page_name} 업데이트!</b>

📝 <i>{summary}</i>

🔗 <a href="{url}">{url}</a>

#Tesla"""
    
    return message


def post_to_telegram(message: str) -> bool:
    """Telegram으로 메시지 전송 (완전 무료!)"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram 설정 없음 (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID 필요)")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # HTML 포맷으로 전송
        response = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"Telegram 전송 성공!")
            return True
        else:
            logger.error(f"Telegram 전송 실패: {response.status_code} - {response.text}")
            return False
        
    except Exception as e:
        logger.error(f"Telegram 전송 오류: {e}")
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
    
    # 메시지 생성
    message = format_message(url, diff)
    logger.info(f"메시지:\n{message}")
    
    # Telegram으로 전송
    success = post_to_telegram(message)
    
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
