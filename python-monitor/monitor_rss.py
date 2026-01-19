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
from deep_translator import GoogleTranslator
import pytz
from dateutil import parser as date_parser

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Telegram Bot 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 키워드 필터링 설정
KEYWORD_FILTER_ENABLED = os.getenv("KEYWORD_FILTER_ENABLED", "false").lower() == "true"
FILTER_KEYWORDS_STR = os.getenv("FILTER_KEYWORDS", "")

# 키워드 필터 파싱 (쉼표로 구분)
if FILTER_KEYWORDS_STR:
    FILTER_KEYWORDS = [k.strip().lower() for k in FILTER_KEYWORDS_STR.split(",") if k.strip()]
else:
    FILTER_KEYWORDS = []

logger.info(f"키워드 필터: {'활성화' if KEYWORD_FILTER_ENABLED else '비활성화'}")
if KEYWORD_FILTER_ENABLED and FILTER_KEYWORDS:
    logger.info(f"필터 키워드: {', '.join(FILTER_KEYWORDS)}")

# Tesla 관련 RSS 피드 목록 (모두 검증됨)
RSS_FEEDS = {
    # Tesla 전문 뉴스 (공식 발표 즉시 커버)
    "Electrek": "https://electrek.co/guides/tesla/feed/",          # ⭐⭐⭐⭐⭐ 가장 빠름
    "Teslarati": "https://www.teslarati.com/feed/",                # ⭐⭐⭐⭐⭐ 심층 분석
    "Tesla North": "https://teslanorth.com/feed/",                 # ⭐⭐⭐⭐ 캐나다
    
    # 전기차 전반 (Tesla 심층 커버)
    "InsideEVs": "https://insideevs.com/rss/",                     # ⭐⭐⭐⭐⭐
    
    # 추가 Tesla 소스
    "Tesla Oracle": "https://www.teslaoracle.com/feed/",           # ⭐⭐⭐⭐
    "CleanTechnica": "https://cleantechnica.com/tag/tesla/feed/",  # ⭐⭐⭐⭐
    
    # 참고: Tesla Blog (tesla.com/blog)는 봇 차단으로 접근 불가
    # → Electrek/Teslarati가 Tesla 공식 발표를 몇 분 내로 커버
}

# 데이터 저장 경로
DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)
SEEN_FILE = os.path.join(DATA_DIR, "seen_articles.json")

# 기사 최신성 필터 (최근 N일 이내 기사만 처리)
MAX_ARTICLE_AGE_DAYS = int(os.getenv("MAX_ARTICLE_AGE_DAYS", "3"))  # 기본 3일
logger.info(f"기사 최신성 필터: 최근 {MAX_ARTICLE_AGE_DAYS}일 이내만 처리")


def load_seen_articles() -> set:
    """이미 본 기사 ID 로드"""
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, 'r') as f:
                data = json.load(f)
                logger.info(f"✅ seen_articles 로드 완료: {len(data)}개")
                logger.info(f"   파일 위치: {SEEN_FILE}")
                # 샘플 ID 출력 (디버깅용)
                if data:
                    logger.info(f"   샘플 ID: {data[0][:16]}...")
                return set(data)
        except Exception as e:
            logger.error(f"❌ seen_articles 로드 실패: {e}")
    else:
        logger.info(f"⚠️  seen_articles 파일 없음 (첫 실행)")
    return set()


def save_seen_articles(seen: set):
    """본 기사 ID 저장"""
    try:
        with open(SEEN_FILE, 'w') as f:
            json.dump(list(seen), f, indent=2)
        logger.info(f"✅ seen_articles 저장 완료: {len(seen)}개")
        logger.info(f"   파일 위치: {SEEN_FILE}")
        # 파일 크기 확인
        file_size = os.path.getsize(SEEN_FILE)
        logger.info(f"   파일 크기: {file_size} bytes")
    except Exception as e:
        logger.error(f"❌ seen_articles 저장 실패: {e}")


def get_article_id(entry: Dict) -> str:
    """기사의 고유 ID 생성"""
    # link를 기준으로 해시 생성
    link = entry.get('link', '')
    return hashlib.md5(link.encode()).hexdigest()


def is_article_recent(entry: Dict) -> bool:
    """기사가 최근 N일 이내인지 확인"""
    try:
        # published 날짜 파싱
        published = entry.get('published', '')
        if not published:
            # 날짜 정보 없으면 최신 기사로 간주 (보수적 접근)
            return True
        
        # 날짜 파싱
        pub_date = date_parser.parse(published)
        
        # 시간대 정보 없으면 UTC로 가정
        if pub_date.tzinfo is None:
            pub_date = pytz.utc.localize(pub_date)
        
        # 현재 시간 (UTC)
        now = datetime.now(pytz.utc)
        
        # 기사 나이 계산
        age = now - pub_date
        age_days = age.days
        
        # 최근 N일 이내인지 확인
        is_recent = age_days <= MAX_ARTICLE_AGE_DAYS
        
        if not is_recent:
            logger.debug(f"   ⏰ 오래된 기사: {age_days}일 전 (제한: {MAX_ARTICLE_AGE_DAYS}일)")
        
        return is_recent
        
    except Exception as e:
        # 날짜 파싱 실패하면 최신 기사로 간주
        logger.debug(f"   ⚠️  날짜 파싱 실패: {e}, 최신 기사로 간주")
        return True


def is_tesla_related(entry: Dict) -> bool:
    """Tesla 관련 기사인지 확인"""
    title = entry.get('title', '').lower()
    summary = entry.get('summary', '').lower()
    
    # Tesla 키워드 (기본)
    tesla_keywords = [
        'tesla', 'elon musk', 'model 3', 'model y', 'model s', 'model x',
        'cybertruck', 'roadster', 'semi', 'supercharger', 'autopilot',
        'fsd', 'full self-driving', '테슬라', '일론 머스크'
    ]
    
    text = f"{title} {summary}"
    
    # Tesla 관련 기사가 아니면 바로 제외
    if not any(keyword in text for keyword in tesla_keywords):
        return False
    
    # 키워드 필터가 활성화되어 있으면 추가 필터링
    if KEYWORD_FILTER_ENABLED and FILTER_KEYWORDS:
        # 설정한 키워드가 하나라도 있어야 함
        has_filter_keyword = any(keyword in text for keyword in FILTER_KEYWORDS)
        if not has_filter_keyword:
            logger.debug(f"   ⏭️  필터 키워드 없음: {entry.get('title', '')[:50]}")
            return False
    
    return True


def translate_to_korean(text: str) -> str:
    """영문을 한글로 번역"""
    try:
        translator = GoogleTranslator(source='en', target='ko')
        # 텍스트가 너무 길면 나눠서 번역
        if len(text) > 5000:
            text = text[:5000]
        translated = translator.translate(text)
        return translated
    except Exception as e:
        logger.warning(f"번역 실패: {e}")
        return text  # 번역 실패 시 원문 반환


def format_telegram_message(entry: Dict, source: str) -> str:
    """Telegram 메시지 포맷팅 (한글 번역)"""
    title = entry.get('title', 'No Title')
    link = entry.get('link', '')
    published = entry.get('published', '')
    summary = entry.get('summary', '')
    
    # HTML 태그 제거
    import re
    summary = re.sub('<[^<]+?>', '', summary)
    summary = summary.strip()[:500]  # 500자로 제한 (번역 전)
    
    # 한글 번역
    logger.info(f"번역 중: {title[:50]}...")
    title_kr = translate_to_korean(title)
    summary_kr = translate_to_korean(summary)
    
    # 날짜 포맷팅 (한국 시간으로 변환)
    try:
        # RSS 피드의 날짜를 파싱 (다양한 형식 지원)
        pub_date = date_parser.parse(published)
        
        # 한국 시간대(KST)로 변환
        kst = pytz.timezone('Asia/Seoul')
        if pub_date.tzinfo is None:
            # 시간대 정보가 없으면 UTC로 가정
            pub_date = pytz.utc.localize(pub_date)
        kst_time = pub_date.astimezone(kst)
        
        # 포맷팅: "2026-01-19 03:00 KST 🇰🇷"
        date_str = kst_time.strftime('%Y-%m-%d %H:%M KST 🇰🇷')
    except Exception as e:
        logger.warning(f"날짜 파싱 실패: {e}")
        date_str = f"{published[:16] if published else ''} (원본)"
    
    message = f"""🚗⚡ <b>테슬라 뉴스 업데이트!</b>

<b>{title_kr}</b>

📰 출처: {source}
📅 {date_str}

{summary_kr}...

🔗 <a href="{link}">원문 보기</a>

#Tesla #테슬라 #TeslaNews"""
    
    # Telegram 메시지 길이 제한 (4096자)
    if len(message) > 4000:
        # 너무 길면 요약 부분 줄이기
        summary_kr = summary_kr[:200] + "..."
        message = f"""🚗⚡ <b>테슬라 뉴스 업데이트!</b>

<b>{title_kr}</b>

📰 출처: {source}
📅 {date_str}

{summary_kr}

🔗 <a href="{link}">원문 보기</a>

#Tesla #테슬라 #TeslaNews"""
    
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
    """RSS 피드 체크하고 새 기사 반환 (강화된 파싱)"""
    try:
        logger.info(f"📰 피드 체크: {feed_name}")
        
        # User-Agent 헤더 추가 (봇 차단 방지)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        # requests로 먼저 가져오기
        response = requests.get(feed_url, headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status()
        
        # 여러 방법으로 파싱 시도
        feed = None
        
        # 방법 1: response.content로 파싱
        feed = feedparser.parse(response.content)
        
        # 방법 2: bozo 오류가 심각하면 response.text로 재시도
        if feed.bozo and not feed.entries:
            logger.info(f"   🔄 재시도 중 (다른 인코딩)...")
            feed = feedparser.parse(response.text)
        
        # 방법 3: URL로 직접 파싱 시도
        if feed.bozo and not feed.entries:
            logger.info(f"   🔄 재시도 중 (직접 URL)...")
            feed = feedparser.parse(feed_url)
        
        # bozo 오류가 있어도 entries가 있으면 계속 진행
        if feed.bozo:
            logger.warning(f"⚠️  피드 파싱 경고: {feed_name}")
            logger.warning(f"   오류 내용: {feed.bozo_exception}")
            if not feed.entries:
                logger.error(f"   ❌ 파싱 실패: 기사를 가져올 수 없습니다 (여러 방법 시도했지만 실패)")
                return []
            else:
                logger.info(f"   ⚡ 경고 무시하고 계속 진행 ({len(feed.entries)}개 기사 발견)")
        
        logger.info(f"   총 {len(feed.entries)}개 기사 발견")
        
        new_articles = []
        skipped_seen = 0
        skipped_unrelated = 0
        skipped_old = 0
        
        for entry in feed.entries[:10]:  # 최신 10개만 체크
            article_id = get_article_id(entry)
            title = entry.get('title', '')[:50]
            
            # 이미 본 기사는 스킵
            if article_id in seen_articles:
                logger.debug(f"   ⏭️  이미 본 기사: {title}")
                skipped_seen += 1
                continue
            
            # 오래된 기사는 스킵 (날짜 필터)
            if not is_article_recent(entry):
                logger.debug(f"   ⏭️  오래된 기사: {title}")
                skipped_old += 1
                continue
            
            # Tesla 관련 기사만
            if not is_tesla_related(entry):
                logger.debug(f"   ⏭️  Tesla 무관: {title}")
                skipped_unrelated += 1
                continue
            
            logger.info(f"   ✨ 새 기사: {title}")
            logger.info(f"      ID: {article_id[:16]}...")
            new_articles.append({
                'entry': entry,
                'source': feed_name,
                'id': article_id
            })
        
        logger.info(f"   결과: 새 기사 {len(new_articles)}개 | 이미 본 것 {skipped_seen}개 | 오래됨 {skipped_old}개 | 무관 {skipped_unrelated}개")
        return new_articles
        
    except Exception as e:
        logger.error(f"❌ 피드 체크 실패 {feed_name}: {e}")
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
                logger.info(f"포스팅 성공: {article['id']}")
                time.sleep(5)  # Telegram rate limit + 번역 API 쿨다운
            
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
