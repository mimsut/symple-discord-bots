#!/usr/bin/env python3
"""SYMPLE Founder Feedback Bot — 22:00 KST"""
import anthropic, os, requests
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=900,
    messages=[{"role": "user", "content": f"""당신은 Paul Graham + Sam Altman 스타일의 냉혹하게 솔직한 YC 파트너입니다. 오늘은 {today}입니다.

SYMPLE 창업자 민수에게 필요한 불편한 진실을 말해줄 시간입니다.

SYMPLE 현황:
- 멘탈헬스 스타트업, CBT 기반 앱, 미국 B2B2C 기업 웰니스 피벗 중
- 창업자: 김민수 (연세대 심리학 학·석사 4년, 18학점 남음)
- 최근: 토스 미니앱 출시, 텀블벅 크라우드펀딩, SF MARU 3주, 정주영창업경진대회

오늘의 직언. Discord 메시지 형식, 최대 1800자:

⚡ **민수에게 — YC 파트너의 직언 | {today}**

**🚨 지금 가장 큰 실수/블라인드 스팟:**
[구체적이고 가혹한 진실]

**🙈 피하고 있는 것:**
[그가 직면해야 하지만 피하고 있는 #1 문제]

**⏰ 다음 48시간 안에 할 것:**
[대부분의 창업자가 건너뛰는 구체적 액션]

**📊 반드시 알아야 하는 숫자:**
[차갑게 외워야 할 핵심 지표 하나]

**💪 한 마디:**
[진심 어린 응원 한 문장]

한국어로. 날카롭고 구체적으로. 빈말 없이."""}]
)

text = msg.content[0].text[:2000]
r = requests.post(os.environ["DISCORD_YC_FEEDBACK"], json={"content": text}, timeout=30)
print(f"founder_feedback → Discord: {r.status_code}")
if r.status_code not in (200, 204):
    print(r.text)
