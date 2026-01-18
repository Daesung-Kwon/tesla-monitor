"""
Tesla News Monitor - RSS Feed Version
Tesla 관련 RSS 피드를 모니터링하여 Telegram으로 알림
완전 무료 & 차단 없음!
"""

import feedparser
import requests
import hashlib
import os
import time
from datetime import datetime
from typing import Optional, List, Dict
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

# Tesla 관련 RSS 피드 목록
RSS_FEEDS = {
    "Tesla Blog": "https://www.tesla.com/blog/rss",
    "Electrek": "https://electrek.co/guides/tesla/feed/",
    "Teslarati": "https://www.teslarati.com/feed/",
    "InsideEVs Tesla": "https://insideevs.com/news/feed/",
    "Tesla North": "https://teslanorth.com/feed/",
}

# 데이터 저장 경로
DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)
SEEN_FILE = os.path.join(DATA_DIR, "seen_articles.json")


def load_seen_articles() -> set:
    """이미 본 기사 ID 로드"""
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, 'r') as f:
                data = json.load(f)
                return set(data)
        except Exception as e:
            logger.error(f"seen_articles 로드 실패: {e}")
    return set()


def save_seen_articles(seen: set):
    """본 기사 ID 저장"""
    try:
        with open(SEEN_FILE, 'w') as f:
            json.dump(list(seen), f)
        logger.info(f"seen_articles 저장 완료: {len(seen)}개")
    except Exception as e:
        logger.error(f"seen_articles 저장 실패: {e}")


def get_article_id(entry: Dict) -> str:
    """기사의 고유 ID 생성"""
    # link를 기준으로 해시 생성
    link = entry.get('link', '')
    return hashlib.md5(link.encode()).hexdigest()


def is_tesla_related(entry: Dict) -> bool:
    """Tesla 관련 기사인지 확인"""
    title = entry.get('title', '').lower()
    summary = entry.get('summary', '').lower()
    
    # Tesla 키워드
    tesla_keywords = [
        'tesla', 'elon musk', 'model 3', 'model y', 'model s', 'model x',
        'cybertruck', 'roadster', 'semi', 'supercharger', 'autopilot',
        'fsd', 'full self-driving', '테슬라', '일론 머스크'
    ]
    
    text = f"{title} {summary}"
    return any(keyword in text for keyword in tesla_keywords)


def format_telegram_message(entry: Dict, source: str) -> str:
    """Telegram 메시지 포맷팅"""
    title = entry.get('title', 'No Title')
    link = entry.get('link', '')
    published = entry.get('published', '')
    summary = entry.get('summary', '')
    
    # HTML 태그 제거 (간단한 방법)
    import re
    summary = re.sub('<[^<]+?>', '', summary)
    summary = summary.strip()[:300]  # 300자로 제한
    
    # 날짜 포맷팅
    try:
        from datetime import datetime
        pub_date = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %z')
        date_str = pub_date.strftime('%Y-%m-%d %H:%M')
    except:
        date_str = published[:16] if published else ''
    
    message = f"""🚗⚡ <b>Tesla 뉴스 업데이트!</b>

<b>{title}</b>

📰 출처: {source}
📅 {date_str}

{summary}...

🔗 <a href="{link}">자세히 보기</a>

#Tesla #테슬라 #TeslaNews"""
    
    # Telegram 메시지 길이 제한 (4096자)
    if len(message) > 4000:
        message = message[:3997] + "..."
    
    return message


def post_to_telegram(message: str) -> bool:
    """Telegram으로 메시지 전송"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram 설정 없음")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        response = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }, timeout=10)
        
        if response.status_code == 200:
            logger.info("Telegram 전송 성공!")
            return True
        else:
            logger.error(f"Telegram 전송 실패: {response.status_code} - {response.text}")
            return False
        
    except Exception as e:
        logger.error(f"Telegram 전송 오류: {e}")
        return False


def check_feed(feed_name: str, feed_url: str, seen_articles: set) -> List[Dict]:
    """RSS 피드 체크하고 새 기사 반환"""
    try:
        logger.info(f"피드 체크: {feed_name}")
        
        # RSS 피드 파싱
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:
            logger.warning(f"피드 파싱 경고: {feed_name} - {feed.bozo_exception}")
        
        new_articles = []
        
        for entry in feed.entries[:10]:  # 최신 10개만 체크
            article_id = get_article_id(entry)
            
            # 이미 본 기사는 스킵
            if article_id in seen_articles:
                continue
            
            # Tesla 관련 기사만
            if not is_tesla_related(entry):
                logger.info(f"Tesla 무관: {entry.get('title', '')[:50]}")
                continue
            
            logger.info(f"새 기사 발견: {entry.get('title', '')[:50]}")
            new_articles.append({
                'entry': entry,
                'source': feed_name,
                'id': article_id
            })
        
        return new_articles
        
    except Exception as e:
        logger.error(f"피드 체크 실패 {feed_name}: {e}")
        return []


def monitor_all_feeds():
    """모든 RSS 피드 모니터링"""
    logger.info("=" * 60)
    logger.info(f"Tesla RSS Monitor 시작: {datetime.now()}")
    logger.info("=" * 60)
    
    # 이전에 본 기사 로드
    seen_articles = load_seen_articles()
    logger.info(f"이미 본 기사: {len(seen_articles)}개")
    
    all_new_articles = []
    
    # 각 피드 체크
    for feed_name, feed_url in RSS_FEEDS.items():
        try:
            new_articles = check_feed(feed_name, feed_url, seen_articles)
            all_new_articles.extend(new_articles)
            time.sleep(2)  # Rate limiting
        except Exception as e:
            logger.error(f"피드 처리 오류 {feed_name}: {e}")
    
    logger.info(f"새 기사 총 {len(all_new_articles)}개 발견")
    
    # 새 기사를 Telegram으로 전송
    posted = 0
    for article in all_new_articles[:5]:  # 최대 5개만 (스팸 방지)
        try:
            message = format_telegram_message(
                article['entry'],
                article['source']
            )
            
            if post_to_telegram(message):
                posted += 1
                seen_articles.add(article['id'])
                time.sleep(3)  # Telegram rate limit
            
        except Exception as e:
            logger.error(f"기사 포스팅 오류: {e}")
    
    # 본 기사 저장
    save_seen_articles(seen_articles)
    
    # 결과 요약
    logger.info("=" * 60)
    logger.info("모니터링 완료!")
    logger.info(f"새 기사: {len(all_new_articles)}개")
    logger.info(f"포스팅: {posted}개")
    logger.info("=" * 60)


if __name__ == "__main__":
    monitor_all_feeds()
