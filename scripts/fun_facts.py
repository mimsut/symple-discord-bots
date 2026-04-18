#!/usr/bin/env python3
"""SYMPLE Fun Facts — Gemini 무료 AI, 매일 새 콘텐츠"""
import os, requests
import google.generativeai as genai
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(f"""오늘은 {today}. 당신은 멘탈헬스 과학 커뮤니케이터입니다.

CBT 기반 멘탈케어 앱 SYMPLE(Duck's Dream) 팀을 위한 오늘의 심리학/정신건강 Fun Fact를 하나 작성하세요.
매일 다른 주제여야 하며, 실제 연구 기반의 구체적인 팩트여야 합니다.
날짜 ({today})를 시드로 사용해 다양한 주제를 다루세요.

아래 형식 그대로 출력 (다른 말 없이):

🧠 **SYMPLE Fun Fact | {today}**

**[팩트 제목 — 15자 이내]**
[팩트 설명 3-4문장. 구체적인 수치·연구기관·연구년도 포함. 흥미롭고 실용적으로.]

💡 **SYMPLE 인사이트:** [이 팩트가 Duck's Dream 제품 또는 B2B2C 전략에 주는 시사점 1-2문장]

총 600자 이내.""")

text = response.text.strip()[:2000]
r = requests.post(os.environ["DISCORD_FUN_FACTS"], json={"content": text}, timeout=30)
print(f"fun_facts → Discord: {r.status_code}")
