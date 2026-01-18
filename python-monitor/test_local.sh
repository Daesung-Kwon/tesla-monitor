#!/bin/bash
# 로컬 테스트 스크립트

echo "🚗⚡ Tesla Monitor - 로컬 테스트"
echo "================================"
echo ""

# 환경 변수 확인
if [ ! -f ".env" ]; then
    echo "❌ .env 파일이 없습니다!"
    echo ""
    echo "env.example을 복사하고 설정하세요:"
    echo "  cp env.example .env"
    echo "  nano .env"
    exit 1
fi

# .env 로드
export $(cat .env | grep -v '^#' | xargs)

# Telegram 설정 확인
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "❌ Telegram 설정이 없습니다!"
    echo ""
    echo ".env 파일에서 다음을 설정하세요:"
    echo "  TELEGRAM_BOT_TOKEN=..."
    echo "  TELEGRAM_CHAT_ID=..."
    exit 1
fi

echo "✅ 환경 변수 로드 완료"
echo ""

# Python 의존성 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3가 설치되지 않았습니다!"
    exit 1
fi

echo "📦 의존성 설치 중..."
pip install -q -r requirements.txt
echo "✅ 의존성 설치 완료"
echo ""

# 데이터 디렉토리 생성
mkdir -p data
echo "✅ 데이터 디렉토리 준비 완료"
echo ""

# 모니터링 실행
echo "🔍 RSS 피드 모니터링 시작..."
echo "================================"
python monitor_rss.py
echo "================================"
echo ""

echo "✅ 테스트 완료!"
echo ""
echo "💡 팁:"
echo "  - 첫 실행은 기존 기사를 저장합니다"
echo "  - 다음 실행부터 새 기사만 알림을 보냅니다"
echo "  - Telegram에서 메시지를 확인하세요!"
