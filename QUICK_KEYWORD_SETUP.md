# ⚡ 키워드 필터 빠른 설정 (1분)

## 🎯 목표
특정 키워드(예: Cybertruck, FSD, 가격)가 포함된 뉴스만 받기!

---

## 🚀 설정 방법 (3단계)

### 1️⃣ GitHub Settings 접속
```
https://github.com/YOUR_USERNAME/tesla-monitor/settings/secrets/actions
```

### 2️⃣ Secret 2개 추가

#### Secret #1: 필터 ON
- **Name:** `KEYWORD_FILTER_ENABLED`
- **Value:** `true`

#### Secret #2: 키워드 입력
- **Name:** `FILTER_KEYWORDS`
- **Value:** (아래에서 선택)

### 3️⃣ 완료!
15분 후 자동 적용 ✅

---

## 📋 키워드 프리셋 (복사해서 사용)

### 🚙 Cybertruck 팬
```
cybertruck,사이버트럭
```

### 🤖 FSD/자율주행 관심
```
fsd,autopilot,자율주행,full self-driving
```

### 💰 가격/할인 알림
```
price,가격,discount,할인,sale
```

### 🇰🇷 한국 관련
```
korea,한국,seoul,서울
```

### 🔄 소프트웨어 업데이트
```
update,업데이트,software,firmware
```

### 🎯 종합 (추천)
```
cybertruck,fsd,price,korea,update,한국,가격
```

### 📈 투자자용
```
stock,tsla,earnings,delivery,production,주가,실적
```

---

## 🎬 실제 예시

### 설정 전 (필터 OFF)
```
📨 하루 5-10개 알림
- Tesla opens new factory in Texas
- Model 3 gets minor update
- Tesla hiring engineers
- Cybertruck production doubles
- Tesla stock rises 3%
- ... (모든 뉴스)
```

### 설정 후 (Cybertruck 필터)
```
📨 하루 1-2개 알림
- Cybertruck production doubles ✅
- (나머지는 스킵)
```

---

## 🔄 키워드 변경하고 싶을 때

1. Settings → Secrets → Actions
2. `FILTER_KEYWORDS` 클릭
3. Update secret
4. 새 키워드 입력 → Update

---

## ❌ 필터 끄고 싶을 때

**Option 1:** Secret 삭제
```
KEYWORD_FILTER_ENABLED 삭제
FILTER_KEYWORDS 삭제
```

**Option 2:** Value 변경
```
KEYWORD_FILTER_ENABLED = false
```

---

## 📊 예상 알림 수

| 설정 | 하루 | 주간 |
|------|------|------|
| 필터 OFF (전체) | 5-10 | 30-70 |
| Cybertruck | 1-3 | 7-21 |
| 여러 키워드 | 2-5 | 14-35 |

---

## 💡 팁

### 알림이 너무 적을 때
키워드 추가:
```
# Before
cybertruck

# After
cybertruck,사이버트럭,cyber truck
```

### 알림이 너무 많을 때
키워드 줄이기:
```
# Before
tesla,car,electric,update,news

# After
cybertruck,fsd
```

---

**자세한 설명:** [KEYWORD_FILTER_GUIDE.md](KEYWORD_FILTER_GUIDE.md)

**문제 발생:** Issues 페이지에 남겨주세요!
