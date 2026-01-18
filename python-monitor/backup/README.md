# 백업 파일

이 폴더에는 사용하지 않는 이전 버전의 코드가 보관되어 있습니다.

## monitor_website_scraping.py

**웹사이트 직접 스크래핑 방식** (사용 안함)

**문제점:**
- Tesla.com → 403 Forbidden 에러
- CloudFlare 차단
- cloudscraper로도 우회 불가
- 불안정

**대체:**
- `monitor_rss.py` 사용 (RSS 피드 방식)
- 차단 없음, 안정적

**보관 이유:**
- 향후 참고용
- 다른 사이트에 적용 가능
