#!/usr/bin/env python3
import os, requests, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_client, generate
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST)
today_str = today.strftime("%Y-%m-%d")
doy = today.timetuple().tm_yday  # 날짜별로 다른 주제 선택

# 도깨비불 — 매일 다른 과학적 각도
GHOST_FIRE_ANGLES = [
    "인화수소(PH₃)와 자연발화 원리",
    "전 세계 문화권에서 목격된 도깨비불 사례",
    "습지 메탄 가스와 발광 현상",
    "한국 전통 설화 속 도깨비불의 기원",
    "현대 과학이 재현한 도깨비불 실험",
    "도깨비불과 날씨·습도의 관계",
    "생물발광과 도깨비불의 차이",
    "중세 유럽 '잭오랜턴' 전설과 도깨비불",
    "도깨비불의 색깔(파란색·녹색·흰색) 변화 이유",
    "도시화로 사라진 도깨비불과 생태계",
    "도깨비불과 철학 — 허상이 현실에 미치는 영향",
    "질소 화합물과 도깨비불의 화학 반응",
    "북유럽 신화 속 도깨비불(Corpse Candle)",
    "도깨비불과 무덤·부패의 과학",
    "현대 과학수사에서 도깨비불 원리 활용",
]

# 오리 — 매일 다른 과학적 각도
DUCK_ANGLES = [
    "반구적 수면(Unihemispheric sleep) — 뇌의 절반만 잠든다",
    "깃털의 방수 원리 — 기름샘과 나노구조",
    "오리의 나침반 — 지구 자기장 감지 능력",
    "오리 무리의 집단지성과 의사결정",
    "새끼 오리의 각인(Imprinting) 심리학",
    "오리 부리의 필터링 구조 — 진흙 속 먹이 찾기",
    "오리의 체온 조절 — 영하에서도 발이 얼지 않는 이유",
    "오리 울음소리와 사회적 커뮤니케이션",
    "오리의 시야 — 340도 시야각과 위협 감지",
    "오리의 포란 — 알 온도 0.1도 단위 감지",
    "오리와 공감 능력 — 동료의 고통에 반응하는 연구",
    "오리의 기억력 — 장소와 얼굴 기억",
    "철새 오리의 이동 거리 — 수천 km 비행",
    "오리의 수명과 노화 메커니즘",
    "오리와 생태계 — 씨앗 전파자 역할",
]

ghost_angle = GHOST_FIRE_ANGLES[doy % len(GHOST_FIRE_ANGLES)]
duck_angle  = DUCK_ANGLES[doy % len(DUCK_ANGLES)]

client = get_client()
text = generate(client, f"""오늘은 {today_str}.

SYMPLE은 두 가지 제품을 가진 멘탈헬스 스타트업이다:
- **KKEBI(꺼비)**: 목소리 분석으로 번아웃을 조기 탐지하는 AI — "보이지 않는 경고등을 먼저 감지한다"
- **오리의 꿈**: CBT 기반 멘탈케어 앱 — "치료가 아닌 습관으로, 병원이 아닌 일상에서"

오늘의 도깨비불 각도: {ghost_angle}
오늘의 오리 각도: {duck_angle}

위 각도로, 아래 형식을 **정확히** 따라 작성하라. 다른 말 없이 형식만 출력. 총 1900자 이내.

---
🔥 오늘의 도깨비불 Fun Fact
[도깨비불에 관한 굵은 제목 — 핵심 사실 한 줄]

[{ghost_angle}에 대한 과학적 사실 3-4문장. 구체적 화학식·수치·연구 포함. 마지막 문장은 반드시 인식의 반전으로 끝내라.]
🎯 KKEBI 마케팅 훅
[도깨비불의 과학적 특성을 번아웃·KKEBI와 연결한 강력한 마케팅 메시지. 마지막에 큰따옴표로 카피라이팅 한 줄.]
📣 SYMPLE IR 연결
[투자자에게 설득력 있는 한 문단. KKEBI의 기술적 차별점을 도깨비불 은유로 연결.]

🦆 오늘의 오리 Fun Fact
[오리에 관한 굵은 제목 — 핵심 사실 한 줄]

[{duck_angle}에 대한 과학적 사실 3-4문장. 구체적 수치·연구기관 포함. 마지막 문장은 인간 삶과 연결.]
🎯 오리의 꿈 마케팅 훅
[오리의 특성을 번아웃·오리의꿈 앱과 연결한 따뜻하고 강력한 메시지. 마지막에 큰따옴표로 카피라이팅 한 줄.]
📣 SYMPLE IR 연결
[오리의꿈 앱의 CBT 게임화 접근과 오리 특성을 연결한 투자자용 한 문단.]

🩻 SYMPLE One-liner
[도깨비불(KKEBI)과 오리(오리의꿈)를 하나로 묶는 SYMPLE의 강력한 한 문장 포지셔닝.]

SYMPLE Daily Insight · {today_str}
---

⚠️ 중요: 위 형식의 모든 텍스트는 반드시 한국어로만 작성하세요. 영어는 화학식·수치·고유명사 외 절대 포함하지 마세요.""", max_tokens=1200)

r = requests.post(os.environ["DISCORD_FUN_FACTS"], json={"content": text[:2000]}, timeout=30)
print(f"fun_facts → {r.status_code}")
