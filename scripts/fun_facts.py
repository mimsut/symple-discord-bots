#!/usr/bin/env python3
import os, requests, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_client, generate
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST)
today_str = today.strftime("%Y-%m-%d")
day_of_year = today.timetuple().tm_yday

# 날짜별로 다른 주제 — 365개 주제를 커버하도록 로테이션
TOPICS = [
    "수면과 꿈의 심리학", "CBT(인지행동치료)의 원리", "감사일기의 뇌과학적 효과",
    "불안과 회피 행동의 관계", "자기연민 vs 자기비판", "운동이 우울증에 미치는 영향",
    "마음챙김 명상의 뇌 변화", "번아웃의 3단계와 회복법", "감정 억압의 신체 반응",
    "사회적 연결과 수명의 관계", "완벽주의와 심리적 고통", "스트레스 호르몬 코르티솔",
    "행동 활성화 치료(BA)", "인지 왜곡의 종류", "심리적 안전감의 중요성",
    "외로움의 신체 건강 영향", "루틴과 정신건강의 관계", "감정 어휘력과 스트레스 관리",
    "노출 치료의 원리", "긍정 심리학의 PERMA 모델", "회복탄력성을 기르는 법",
    "디지털 미디어와 불안의 관계", "장-뇌 축(Gut-Brain Axis)", "공황발작의 오해와 진실",
    "애착 유형과 대인관계", "자기효능감(Self-efficacy)의 힘", "인지 유연성 훈련법",
    "의사결정 피로와 정신건강", "심리적 거리두기 기법", "트라우마와 신체 기억",
]

topic = TOPICS[day_of_year % len(TOPICS)]

client = get_client()
text = generate(client, f"""오늘은 {today_str}. 오늘의 주제: **{topic}**

당신은 SYMPLE 앱의 두 캐릭터입니다:
- 🦆 **오리**: 따뜻하고 공감적. 사용자 입장에서 이야기함.
- 🔥 **도깨비불**: 호기심 많고 과학적. 연구 결과와 수치를 좋아함.

오늘의 주제 "{topic}"에 대한 심리학/멘탈헬스 Fun Fact를 두 캐릭터의 대화 형식으로 작성하세요.
매일 다른 내용이어야 하며, 오늘({today_str}) 날짜에만 어울리는 구체적 팩트를 담으세요.

아래 형식 그대로만 출력 (600자 이내, 다른 말 없이):

🦆🔥 **오리의 꿈 — 오늘의 Fun Fact | {today_str}**
*주제: {topic}*

🔥 "[도깨비불이 흥미로운 연구 결과나 수치를 소개하는 말 — 구체적 수치·연구기관 포함]"

🦆 "[오리가 이것이 일상에서 어떤 의미인지 따뜻하게 해석하는 말]"

💡 **SYMPLE 인사이트:** [Duck's Dream 앱 또는 CBT 기능과 연결한 시사점 1문장]""", max_tokens=500)

r = requests.post(os.environ["DISCORD_FUN_FACTS"], json={"content": text[:2000]}, timeout=30)
print(f"fun_facts → {r.status_code}")
