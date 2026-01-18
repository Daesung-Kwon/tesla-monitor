"""
Tesla Website Monitor - FastAPI Webhook Server
changedetection.io로부터 webhook을 받아 X(Twitter)에 포스팅
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import tweepy
import os
import difflib
import re
from datetime import datetime
from typing import Optional
import logging
import httpx

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tesla Monitor Webhook")

# X API 설정 (환경 변수에서 로드)
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")

# 필터링 키워드 (중요한 변경만 감지)
IMPORTANT_KEYWORDS = [
    # 가격 관련
    'price', 'pricing', '₩', 'won', 'krw', 'usd', '$', '원',
    # 제품 관련
    'new', 'launch', 'available', 'delivery', 'inventory', 
    'order', 'reserve', 'pre-order',
    # 업데이트 관련
    'update', 'refresh', 'facelift', 'redesign', 'announce',
    # 소프트웨어
    'software', 'fsd', 'autopilot', 'version',
    # 이벤트
    'event', 'reveal', 'unveil',
    # 한국 관련
    '한국', '서울', '부산', 'korea',
]

# 무시할 키워드 (노이즈 필터링)
IGNORE_KEYWORDS = [
    'cookie', 'analytics', 'tracking', 'javascript',
    'css', 'stylesheet', 'font', 'src='
]


def init_twitter_client() -> Optional[tweepy.Client]:
    """X API v2 클라이언트 초기화"""
    if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET]):
        logger.warning("X API 인증 정보가 설정되지 않았습니다.")
        return None
    
    try:
        client = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_SECRET
        )
        logger.info("X API 클라이언트 초기화 성공")
        return client
    except Exception as e:
        logger.error(f"X API 클라이언트 초기화 실패: {e}")
        return None


def is_significant_change(text_diff: str, url: str) -> bool:
    """변경 사항이 중요한지 필터링"""
    
    # 무시 키워드 체크
    text_lower = text_diff.lower()
    for ignore_word in IGNORE_KEYWORDS:
        if ignore_word in text_lower:
            logger.info(f"무시 키워드 감지: {ignore_word}")
            return False
    
    # 중요 키워드 체크
    for keyword in IMPORTANT_KEYWORDS:
        if keyword.lower() in text_lower:
            logger.info(f"중요 키워드 감지: {keyword}")
            return True
    
    # 변경량이 너무 작으면 무시 (공백, CSS 등)
    lines = text_diff.split('\n')
    meaningful_lines = [l for l in lines if l.strip() and len(l.strip()) > 3]
    
    if len(meaningful_lines) < 2:
        logger.info("변경량이 너무 작음")
        return False
    
    return True


def format_tweet_message(url: str, diff_snippet: str) -> str:
    """트윗 메시지 포맷팅"""
    
    # URL에서 페이지 종류 파악
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
    elif "roadster" in url.lower():
        page_name = "로드스터 페이지"
    elif "energy" in url.lower():
        page_name = "에너지 페이지"
    elif "software" in url.lower():
        page_name = "소프트웨어 업데이트 페이지"
    elif "ko_kr" in url.lower():
        page_name = "테슬라 한국 페이지"
    
    # diff 요약 (너무 길면 자르기)
    diff_summary = diff_snippet[:150].strip()
    if len(diff_snippet) > 150:
        diff_summary += "..."
    
    # 트윗 메시지 구성
    message = f"""🚗⚡ {page_name}에 변경 감지!

{diff_summary}

자세히 보기: {url}

#Tesla #테슬라 #TeslaUpdates"""
    
    # 트윗 길이 제한 (280자)
    if len(message) > 280:
        # URL과 해시태그는 유지하고 diff_summary만 줄이기
        max_diff_len = 280 - 150  # 나머지 텍스트 길이 고려
        diff_summary = diff_snippet[:max_diff_len].strip() + "..."
        message = f"""🚗⚡ {page_name}에 변경 감지!

{diff_summary}

{url}

#Tesla #테슬라"""
    
    return message


async def post_to_twitter(message: str, image_url: Optional[str] = None) -> bool:
    """X에 포스팅"""
    
    client = init_twitter_client()
    if not client:
        logger.error("X API 클라이언트를 초기화할 수 없습니다.")
        return False
    
    try:
        # 이미지가 있으면 다운로드 후 업로드 (v1.1 API 사용)
        media_id = None
        if image_url:
            try:
                # tweepy v1.1 API로 미디어 업로드
                auth = tweepy.OAuth1UserHandler(
                    X_API_KEY, X_API_SECRET,
                    X_ACCESS_TOKEN, X_ACCESS_SECRET
                )
                api_v1 = tweepy.API(auth)
                
                # 이미지 다운로드
                async with httpx.AsyncClient() as http_client:
                    img_response = await http_client.get(image_url, timeout=10.0)
                    if img_response.status_code == 200:
                        # 임시 파일로 저장
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                            tmp.write(img_response.content)
                            tmp_path = tmp.name
                        
                        # 미디어 업로드
                        media = api_v1.media_upload(tmp_path)
                        media_id = media.media_id
                        logger.info(f"미디어 업로드 성공: {media_id}")
                        
                        # 임시 파일 삭제
                        os.unlink(tmp_path)
            except Exception as e:
                logger.warning(f"이미지 업로드 실패 (텍스트만 포스팅): {e}")
        
        # 트윗 포스팅 (v2 API)
        if media_id:
            response = client.create_tweet(text=message, media_ids=[media_id])
        else:
            response = client.create_tweet(text=message)
        
        logger.info(f"트윗 포스팅 성공: {response.data}")
        return True
        
    except Exception as e:
        logger.error(f"트윗 포스팅 실패: {e}")
        return False


@app.get("/")
async def root():
    """헬스 체크"""
    return {
        "status": "healthy",
        "service": "Tesla Monitor Webhook",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    """Railway 헬스 체크"""
    return {"status": "ok"}


@app.post("/tesla-update")
async def receive_tesla_update(request: Request):
    """
    changedetection.io로부터 webhook 수신
    
    Expected payload (Apprise webhook format):
    {
        "title": "Watch title",
        "body": "Diff content",
        "url": "https://www.tesla.com/...",
        "diff_url": "http://...",
        "current_snapshot": "...",
        "screenshot": "http://..."
    }
    """
    try:
        # Webhook 데이터 파싱
        payload = await request.json()
        logger.info(f"Webhook 수신: {payload.keys()}")
        
        # 기본 정보 추출
        url = payload.get("url", "")
        body = payload.get("body", "")
        title = payload.get("title", "")
        screenshot = payload.get("screenshot")
        
        if not url or not body:
            logger.warning("URL 또는 body가 없습니다.")
            return JSONResponse(
                status_code=400,
                content={"error": "Missing url or body"}
            )
        
        logger.info(f"변경 감지: {url}")
        logger.info(f"Diff 내용 길이: {len(body)} characters")
        
        # 중요한 변경인지 필터링
        if not is_significant_change(body, url):
            logger.info("중요하지 않은 변경으로 판단, 스킵")
            return JSONResponse(
                status_code=200,
                content={"status": "skipped", "reason": "not significant"}
            )
        
        # 트윗 메시지 생성
        message = format_tweet_message(url, body)
        logger.info(f"트윗 메시지: {message}")
        
        # X에 포스팅
        success = await post_to_twitter(message, screenshot)
        
        if success:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Posted to X",
                    "url": url
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Failed to post to X"
                }
            )
            
    except Exception as e:
        logger.error(f"Webhook 처리 오류: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/test-tweet")
async def test_tweet(request: Request):
    """테스트용 트윗 포스팅 엔드포인트"""
    try:
        data = await request.json()
        message = data.get("message", "🚗⚡ 테슬라 모니터링 시스템 테스트 #Tesla")
        
        success = await post_to_twitter(message)
        
        if success:
            return {"status": "success", "message": "Test tweet posted"}
        else:
            return {"status": "error", "message": "Failed to post test tweet"}
            
    except Exception as e:
        logger.error(f"테스트 트윗 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
