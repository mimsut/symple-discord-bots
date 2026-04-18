#!/usr/bin/env python3
"""SYMPLE 창업자 직언 — Gemini, 매일 새 콘텐츠"""
import os, requests
import google.generativeai as genai
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST)
today_str = today.strftime("%Y년 %m월 %d일")
today_seed = today.strftime("%Y-%m-%d")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(f"""오늘 날짜: {today_str} (시드: {today_seed})
당신은 Paul Graham + Sam Altman 스타일의 냉혹하게 솔직한 YC 파트너입니다.

SYMPLE 현황:
- 멘탈헬스 스타트업, CBT 기반 앱 Duck's Dream
- 한국 B2C → 미국 B2B2C (기업 웰니스) 피벗 진행 중
- 창업자: 김민수, 연세대 심리학 학·석사 4년 (18학점 남음)
- 성과: 토스 미니앱 신규 4위, 텀블벅 크라우드펀딩, 대한디지털치료학회 우수포스터, SF MARU 3주, 정주영창업경진대회

날짜 시드({today_seed})를 활용해 매일 다른 주제와 각도로 직언을 작성하세요.
오늘의 각도: {today_seed[-2:]}일을 참고해 주제 선택.

아래 형식 그대로 출력 (다른 말 없이, 총 1800자 이내):

⚡ **민수에게 — YC 파트너의 직언 | {today_str}**

🔴 **지금 가장 큰 실수**
[구체적이고 냉혹한 직언. SYMPLE 상황에 맞는 실제 업계 수치·벤치마크 포함.]

🙈 **지금 회피하는 것**
[민수가 직면해야 하지만 피하고 있는 불편한 진실 1가지. 구체적으로.]

⏰ **48시간 내 해야 할 것**
→ [대부분의 창업자가 건너뛰는 구체적 행동. 명확하고 실행 가능하게.]

📊 **당장 대답할 수 있어야 하는 숫자**
"[민수가 모르면 안 되는 핵심 지표 — 따옴표 형태로. 실제 업계 벤치마크 포함.]"

💪 **마지막으로**
[진심 어린 응원 한 문장. 짧고 강하게.]""")

text = response.text.strip()[:2000]
r = requests.post(os.environ["DISCORD_YC_FEEDBACK"], json={"content": text}, timeout=30)
print(f"founder_feedback → Discord: {r.status_code}")
