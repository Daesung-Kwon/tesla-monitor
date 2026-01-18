# Tesla Website Monitor - 프로젝트 요약

## 🎯 프로젝트 개요

테슬라 공식 홈페이지(www.tesla.com)의 중요한 페이지들이 업데이트될 때마다 실시간으로 감지해서 X(트위터) 또는 Telegram에 자동 포스팅하는 시스템입니다.

**프로젝트 위치**: `/Users/malife/tesla-monitor/`

---

## 📁 프로젝트 구조

```
tesla-monitor/
│
├── README.md                           # 메인 README
├── LICENSE                             # MIT 라이선스
├── .gitignore                          # Git 제외 파일
├── docker-compose.yml                  # 로컬 개발 환경 (Docker)
│
├── docs/                               # 📚 상세 가이드 문서
│   ├── QUICKSTART.md                  # ⭐ 5분 시작 가이드
│   ├── RAILWAY_DEPLOY_GUIDE.md        # Railway 배포 가이드
│   ├── X_API_SETUP_GUIDE.md           # X API 설정 가이드
│   ├── LOCAL_DEVELOPMENT.md           # 로컬 개발 가이드
│   └── PURE_PYTHON_ALTERNATIVE.md     # Python 대안 구현
│
├── fastapi-webhook/                    # 🚀 방법 1: FastAPI Webhook 서버
│   ├── main.py                        # FastAPI 애플리케이션
│   ├── requirements.txt               # Python 의존성
│   ├── Dockerfile                     # Docker 이미지
│   ├── Procfile                       # Railway 배포 설정
│   ├── railway.toml                   # Railway 설정
│   └── env.example                    # 환경 변수 예시
│
├── python-monitor/                     # 🆓 방법 2: 순수 Python 구현
│   ├── monitor.py                     # 모니터링 스크립트
│   ├── requirements.txt               # Python 의존성
│   ├── railway.json                   # Railway Cron 설정
│   ├── env.example                    # 환경 변수 예시
│   └── README.md                      # 사용 가이드
│
└── .github/                            # 🆓 방법 3: GitHub Actions
    └── workflows/
        └── monitor.yml                 # GitHub Actions workflow
```

---

## 🚀 구현된 3가지 방법

### 방법 1: changedetection.io + FastAPI + Railway
- **위치**: `fastapi-webhook/`
- **장점**: GUI 설정, JavaScript 렌더링, 스크린샷
- **비용**: ~$21/월 (최적화 시 ~$2/월)
- **난이도**: ⭐⭐ (쉬움)
- **가이드**: [docs/RAILWAY_DEPLOY_GUIDE.md](docs/RAILWAY_DEPLOY_GUIDE.md)

### 방법 2: 순수 Python + GitHub Actions
- **위치**: `python-monitor/` + `.github/workflows/`
- **장점**: 완전 무료, 간단한 설정
- **비용**: $0/월 (GitHub Actions 무료)
- **난이도**: ⭐⭐⭐ (보통)
- **가이드**: [docs/PURE_PYTHON_ALTERNATIVE.md](docs/PURE_PYTHON_ALTERNATIVE.md)

### 방법 3: 순수 Python + Railway Cron
- **위치**: `python-monitor/`
- **장점**: 저렴, 안정적, 커스터마이징 가능
- **비용**: ~$1-2/월
- **난이도**: ⭐⭐⭐ (보통)
- **가이드**: [docs/PURE_PYTHON_ALTERNATIVE.md](docs/PURE_PYTHON_ALTERNATIVE.md)

---

## 📖 주요 문서

### 🌟 시작하기
1. **[docs/QUICKSTART.md](docs/QUICKSTART.md)** ⭐ 가장 먼저 읽기!
   - 5분 빠른 시작 가이드
   - 3가지 방법 비교
   - 단계별 설정

### 🚀 배포 가이드
2. **[docs/RAILWAY_DEPLOY_GUIDE.md](docs/RAILWAY_DEPLOY_GUIDE.md)**
   - Railway.app 전체 설정
   - changedetection.io Docker 배포
   - FastAPI 서버 배포
   - Webhook 연결
   - 비용 관리 및 최적화

3. **[docs/X_API_SETUP_GUIDE.md](docs/X_API_SETUP_GUIDE.md)**
   - X (Twitter) API 키 발급
   - 권한 설정
   - 무료 대안 (Telegram, Mastodon)
   - 문제 해결

### 🔧 개발 가이드
4. **[docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md)**
   - Docker Compose로 로컬 테스트
   - 개별 서비스 실행
   - 디버깅 방법

5. **[docs/PURE_PYTHON_ALTERNATIVE.md](docs/PURE_PYTHON_ALTERNATIVE.md)**
   - changedetection.io 없이 구현
   - GitHub Actions 설정
   - Railway Cron 설정
   - Playwright 추가

---

## 🎯 빠른 시작 (3분!)

### 가장 빠른 방법: GitHub Actions (무료)

```bash
# 1. GitHub에 업로드
cd /Users/malife/tesla-monitor
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/tesla-monitor.git
git push -u origin main

# 2. GitHub Secrets 설정
# Repository → Settings → Secrets and variables → Actions
# X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET 추가

# 3. GitHub Actions 활성화
# Actions 탭 → "Enable workflows"

# ✅ 완료! 15분마다 자동 실행
```

자세한 내용: [docs/QUICKSTART.md](docs/QUICKSTART.md)

---

## 💰 비용 비교 (2026년 1월 기준)

| 방법 | 월 비용 | 장점 | 단점 |
|------|---------|------|------|
| 방법 1 (changedetection.io + Railway) | ~$21 (최적화 시 ~$2) | GUI, JavaScript, 스크린샷 | 비쌈 |
| 방법 2 (Python + GitHub Actions) | **$0** ✅ | 완전 무료 | JS 렌더링 제한 |
| 방법 3 (Python + Railway Cron) | ~$1-2 | 안정적, 저렴 | 직접 구현 |

**추가 비용: X API**
- Free Tier: 폐지됨 ❌
- Basic Plan: $100/월 (3,000 posts)
- **무료 대안**: Telegram Bot (추천!) 또는 Mastodon

---

## 🔑 주요 기능

### ✅ 구현 완료
- [x] 테슬라 주요 페이지 모니터링
- [x] 변경 사항 자동 감지 (해시 비교)
- [x] 중요 변경 필터링 (키워드 기반)
- [x] X (Twitter) 자동 포스팅
- [x] Telegram Bot 지원
- [x] Railway 배포 지원
- [x] GitHub Actions 지원
- [x] Docker Compose 로컬 개발
- [x] 완전한 문서화

### 🚧 향후 추가 가능
- [ ] JavaScript 렌더링 (Playwright)
- [ ] 스크린샷 캡처 및 첨부
- [ ] PostgreSQL 데이터베이스 연동
- [ ] 웹 대시보드 (React)
- [ ] AI 중요도 분석 (GPT-4)
- [ ] Slack, Discord 알림
- [ ] Reddit, YouTube 모니터링

---

## 🛠️ 기술 스택

### 방법 1: changedetection.io
- **changedetection.io**: 웹사이트 변경 감지
- **Playwright**: JavaScript 렌더링
- **FastAPI**: Webhook 서버
- **Tweepy**: X API 클라이언트
- **Railway**: 배포 플랫폼
- **Docker**: 컨테이너화

### 방법 2, 3: 순수 Python
- **Python 3.11**: 메인 언어
- **requests**: HTTP 클라이언트
- **tweepy**: X API 클라이언트
- **difflib**: 텍스트 비교
- **GitHub Actions / Railway**: 실행 플랫폼

---

## 📊 모니터링 대상 페이지

### 차량
- https://www.tesla.com/
- https://www.tesla.com/cybertruck
- https://www.tesla.com/model3
- https://www.tesla.com/modely
- https://www.tesla.com/modelx
- https://www.tesla.com/models
- https://www.tesla.com/roadster

### 제품 & 서비스
- https://www.tesla.com/energy
- https://www.tesla.com/support/software-updates

### 국가별
- https://www.tesla.com/ko_kr (한국)
- https://www.tesla.com/ja_jp (일본)
- https://www.tesla.com/zh_cn (중국)
- https://www.tesla.com/de_de (독일)
- https://www.tesla.com/en_gb (영국)

---

## 🔐 보안 고려사항

### ✅ 구현됨
- 환경 변수로 API 키 관리
- `.gitignore`에 민감 파일 추가
- Railway 암호화된 환경 변수
- GitHub Secrets 사용

### 📝 권장사항
- X API 권한 최소화 (Read and Write만)
- Rate Limiting 구현
- 정기적 API 키 로테이션
- 로그 모니터링

---

## 🐛 문제 해결

### 일반적인 문제
1. **X API 인증 실패**: [docs/X_API_SETUP_GUIDE.md#8-문제-해결](docs/X_API_SETUP_GUIDE.md)
2. **Railway 비용 초과**: [docs/RAILWAY_DEPLOY_GUIDE.md#7-비용-관리](docs/RAILWAY_DEPLOY_GUIDE.md)
3. **Webhook 전송 실패**: [docs/LOCAL_DEVELOPMENT.md#5-문제-해결](docs/LOCAL_DEVELOPMENT.md)

### 지원
- GitHub Issues: 버그 리포트 및 기능 제안
- Discussions: 질문 및 토론

---

## 📈 성능 최적화

### 비용 절감
1. GitHub Actions 사용 (무료)
2. Telegram Bot 사용 (X API 대신)
3. Railway Cron Jobs (연속 실행 대신)
4. 모니터링 주기 조정 (15분 → 30분)

### 정확도 향상
1. CSS Selector로 특정 영역만 모니터링
2. 중요 키워드 커스터마이징
3. 정규식 패턴 추가
4. JavaScript 렌더링 활성화

---

## 🤝 기여하기

1. Fork this repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 🙏 감사

- [changedetection.io](https://github.com/dgtlmoon/changedetection.io) - 웹사이트 모니터링
- [FastAPI](https://fastapi.tiangolo.com/) - 빠른 API 프레임워크
- [Tweepy](https://www.tweepy.org/) - X API 라이브러리
- [Railway.app](https://railway.app/) - 간편한 배포 플랫폼

---

## 📞 연락처

- **GitHub**: https://github.com/YOUR_USERNAME/tesla-monitor
- **Issues**: https://github.com/YOUR_USERNAME/tesla-monitor/issues

---

## 🎓 학습 자료

이 프로젝트를 통해 배울 수 있는 것:
- ✅ FastAPI 웹 애플리케이션 개발
- ✅ Docker & Docker Compose
- ✅ Railway 배포 및 관리
- ✅ GitHub Actions CI/CD
- ✅ X (Twitter) API 사용
- ✅ Webhook 시스템 구축
- ✅ 웹 스크래핑 및 모니터링
- ✅ 비용 효율적 인프라 설계

---

## 🎯 다음 단계

1. ✅ **지금 시작하기**: [docs/QUICKSTART.md](docs/QUICKSTART.md) 읽기
2. ✅ **로컬 테스트**: Docker Compose로 실행
3. ✅ **배포하기**: GitHub Actions 또는 Railway
4. ✅ **커스터마이징**: 키워드, 페이지, 메시지 포맷
5. ✅ **확장하기**: 데이터베이스, 대시보드, AI 분석

---

**Made with ❤️ by Tesla Enthusiasts**

🚗⚡ Happy Monitoring! 🚗⚡

---

## 📝 체크리스트

### 프로젝트 완성도: ✅ 100%

- [x] ✅ FastAPI Webhook 서버 구현
- [x] ✅ 순수 Python 모니터링 스크립트 구현
- [x] ✅ Docker Compose 설정
- [x] ✅ Railway 배포 설정
- [x] ✅ GitHub Actions workflow
- [x] ✅ 전체 문서화 (5개 가이드)
- [x] ✅ 예시 코드 및 설정 파일
- [x] ✅ 3가지 배포 방법 제공
- [x] ✅ 비용 분석 및 최적화 가이드
- [x] ✅ 문제 해결 가이드
- [x] ✅ 무료 대안 제공 (Telegram, GitHub Actions)

### 준비 완료! 🎉
