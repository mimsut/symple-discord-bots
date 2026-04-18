#!/usr/bin/env python3
import os, requests, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_model, generate
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

model = get_model(os.environ["GEMINI_API_KEY"])
text = generate(model, f"""오늘은 {today}. 당신은 멘탈헬스 과학 커뮤니케이터입니다.

CBT 기반 멘탈케어 앱 SYMPLE(Duck's Dream) 팀을 위한 오늘의 심리학/정신건강 Fun Fact를 하나 작성하세요.
날짜({today})를 기반으로 매일 다른 주제를 선택하세요.

아래 형식 그대로만 출력:

🧠 **SYMPLE Fun Fact | {today}**

**[팩트 제목 — 15자 이내]**
[구체적 수치·연구기관·연도 포함. 3-4문장.]

💡 **SYMPLE 인사이트:** [Duck's Dream 제품 또는 B2B2C 전략에 주는 시사점 1-2문장]

총 600자 이내.""")

r = requests.post(os.environ["DISCORD_FUN_FACTS"], json={"content": text[:2000]}, timeout=30)
print(f"fun_facts → {r.status_code}")
