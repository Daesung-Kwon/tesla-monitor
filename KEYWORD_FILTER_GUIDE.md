# 🎯 키워드 필터링 가이드

특정 키워드가 포함된 Tesla 뉴스만 받는 방법입니다.

## 📖 개요

**기본 동작 (필터 OFF):**
- 모든 Tesla 관련 뉴스 수신
- 하루 5-10개 정도 알림

**필터 활성화 (필터 ON):**
- 특정 키워드가 포함된 뉴스만 수신
- 관심 있는 주제만 집중적으로!

---

## 🚀 빠른 설정

### Step 1: GitHub Secrets 추가

1. **Repository Settings 이동**
   ```
   https://github.com/YOUR_USERNAME/tesla-monitor/settings/secrets/actions
   ```

2. **"New repository secret" 클릭**

3. **KEYWORD_FILTER_ENABLED 추가**
   - Name: `KEYWORD_FILTER_ENABLED`
   - Secret: `true` (활성화) 또는 `false` (비활성화)

4. **FILTER_KEYWORDS 추가**
   - Name: `FILTER_KEYWORDS`
   - Secret: `cybertruck,fsd,korea` (원하는 키워드, 쉼표로 구분)

### Step 2: 완료!

다음 실행(15분 후)부터 자동 적용됩니다!

---

## 🎯 프리셋 (복사해서 사용)

### 1. Cybertruck 팬
```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=cybertruck,cyber truck,사이버트럭,cybertrk
```

**알림 예시:**
- ✅ "Tesla Cybertruck production doubles"
- ✅ "Cybertruck gets new features"
- ❌ "Tesla Model 3 update" (Cybertruck 없음)

---

### 2. FSD/자율주행 관심
```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=fsd,full self-driving,autopilot,자율주행,오토파일럿,autonomous
```

**알림 예시:**
- ✅ "Tesla FSD Beta v12 released"
- ✅ "Autopilot 개선 업데이트"
- ❌ "Tesla opens new factory" (FSD 없음)

---

### 3. 가격/할인 관심
```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=price,pricing,discount,sale,deal,가격,할인,세일,프로모션
```

**알림 예시:**
- ✅ "Tesla drops Model Y price by $5000"
- ✅ "테슬라 한국 가격 인하"
- ❌ "Tesla battery technology" (가격 없음)

---

### 4. 한국 관련
```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=korea,korean,한국,seoul,서울,busan,부산,gigafactory korea
```

**알림 예시:**
- ✅ "Tesla Korea opens new Supercharger"
- ✅ "한국에서 테슬라 판매 급증"
- ❌ "Tesla US factory update" (한국 없음)

---

### 5. 소프트웨어 업데이트
```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=update,software,version,firmware,release,업데이트,버전,릴리스
```

**알림 예시:**
- ✅ "Tesla software update 2024.44.2"
- ✅ "새로운 펌웨어 업데이트"
- ❌ "Tesla sales report" (업데이트 없음)

---

### 6. 종합 (여러 관심사)
```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=cybertruck,fsd,price,korea,update,한국,가격,자율주행
```

**알림 예시:**
- ✅ Cybertruck 관련 뉴스
- ✅ FSD 관련 뉴스
- ✅ 가격 관련 뉴스
- ✅ 한국 관련 뉴스
- ✅ 업데이트 관련 뉴스
- ❌ 그 외 일반 뉴스

---

### 7. 투자자용
```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=stock,tsla,earnings,revenue,profit,delivery,production,주가,실적,매출
```

**알림 예시:**
- ✅ "Tesla Q4 earnings beat estimates"
- ✅ "TSLA stock rises 10%"
- ❌ "Tesla unveils new feature" (재무 무관)

---

## 🔧 고급 설정

### 복합 키워드

**AND 조건 (둘 다 포함):**
- 현재는 OR 조건만 지원
- 원하는 기능이면 요청해주세요!

**OR 조건 (하나라도 포함):**
- 현재 방식 (쉼표로 구분)
- `cybertruck,model y,korea`
  → Cybertruck OR Model Y OR Korea

### 대소문자 구분 안함

```
FILTER_KEYWORDS=FSD,fsd,Fsd
```
→ 모두 같은 의미

### 영문/한글 혼용 가능

```
FILTER_KEYWORDS=price,가격,sale,세일
```

---

## 📊 필터링 로직

```python
# 1단계: Tesla 관련인가?
if "tesla" in article:
    # 2단계: 필터 활성화?
    if KEYWORD_FILTER_ENABLED:
        # 3단계: 키워드 있나?
        if any(keyword in article for keyword in FILTER_KEYWORDS):
            ✅ 알림 전송
        else:
            ⏭️  스킵
    else:
        ✅ 알림 전송 (모든 Tesla 뉴스)
```

---

## 🧪 테스트

### 로컬에서 테스트

```bash
cd python-monitor

# .env 파일 수정
nano .env

# 다음 추가:
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=cybertruck,fsd

# 실행
python monitor_rss.py
```

### GitHub Actions에서 확인

```
Actions → 최근 실행 → Run monitor

키워드 필터: 활성화
필터 키워드: cybertruck, fsd
⏭️  필터 키워드 없음: Tesla opens new factory...
✨ 새 기사: Tesla Cybertruck production...
```

---

## 💡 사용 예시

### 시나리오 1: 처음엔 모든 뉴스

```
KEYWORD_FILTER_ENABLED=false
```

→ 어떤 뉴스가 나오는지 파악

### 시나리오 2: 관심 주제 발견

"아, Cybertruck 뉴스가 가장 재미있네!"

```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=cybertruck
```

→ Cybertruck 뉴스만 수신

### 시나리오 3: 관심사 추가

"FSD 뉴스도 궁금하다"

```
KEYWORD_FILTER_ENABLED=true
FILTER_KEYWORDS=cybertruck,fsd
```

→ Cybertruck + FSD 뉴스 수신

---

## 🔄 필터 변경 방법

### GitHub Secrets 수정

1. **Settings → Secrets → Actions**

2. **FILTER_KEYWORDS 클릭**

3. **Update secret**

4. **새 키워드 입력**
   ```
   cybertruck,fsd,korea,price
   ```

5. **Update secret** 클릭

6. **다음 실행(15분 후)부터 자동 적용!**

---

## 📊 통계 (참고)

**필터 OFF (기본):**
- 하루 알림: 5-10개
- 주간 알림: 30-70개

**필터 ON (Cybertruck):**
- 하루 알림: 1-3개
- 주간 알림: 7-21개

**필터 ON (여러 키워드):**
- 하루 알림: 2-5개
- 주간 알림: 14-35개

---

## 🎯 추천 조합

### 일반 팬
```
# 모든 Tesla 뉴스 (기본)
KEYWORD_FILTER_ENABLED=false
```

### 특정 모델 소유자
```
# Model 3 소유자
FILTER_KEYWORDS=model 3,model3,업데이트,가격,software

# Cybertruck 예약자
FILTER_KEYWORDS=cybertruck,delivery,production,생산
```

### 투자자
```
FILTER_KEYWORDS=stock,tsla,earnings,delivery,production,주가
```

### 한국 거주자
```
FILTER_KEYWORDS=korea,한국,가격,price,delivery,배송
```

---

## 🐛 문제 해결

### 알림이 너무 적게 옴

**원인:** 키워드가 너무 구체적
```
# 너무 구체적
FILTER_KEYWORDS=cybertruck stainless steel

# 더 넓게
FILTER_KEYWORDS=cybertruck
```

### 알림이 너무 많이 옴

**원인:** 키워드가 너무 일반적
```
# 너무 일반적
FILTER_KEYWORDS=tesla,car,electric

# 더 구체적으로
FILTER_KEYWORDS=cybertruck,fsd
```

### 필터가 작동 안함

**확인 사항:**
1. `KEYWORD_FILTER_ENABLED=true` 설정?
2. `FILTER_KEYWORDS` 값 입력?
3. GitHub Secrets에 추가?
4. 로그에서 "키워드 필터: 활성화" 확인?

---

## 📚 추가 기능 (향후)

- [ ] AND 조건 지원
- [ ] 부정 키워드 (특정 단어 제외)
- [ ] 키워드별 우선순위
- [ ] 시간대별 필터
- [ ] 웹 UI로 키워드 관리

---

**원하는 기능이 있으면 알려주세요!** 🚀
