#!/usr/bin/env python3
"""SYMPLE Fun Facts Daily Bot — 09:00 KST"""
import anthropic, os, requests
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=600,
    messages=[{"role": "user", "content": f"""오늘은 {today}입니다. 당신은 멘탈헬스 과학 커뮤니케이터입니다.

CBT 기반 멘탈케어 앱(SYMPLE)을 개발하고 있는 팀과 한국 사용자들에게 유용한,
근거 기반의 흥미로운 심리학/정신건강 팩트 하나를 공유해 주세요.

Discord 메시지 형식, 최대 600자:

🧠 **SYMPLE Fun Fact | {today}**

[팩트를 2-3문장으로 설명]

💡 **SYMPLE 인사이트:** [이 팩트가 SYMPLE 제품/전략에 어떻게 적용될 수 있는지 1문장]

한국어로 작성해주세요."""}]
)

text = msg.content[0].text[:2000]
r = requests.post(os.environ["DISCORD_FUN_FACTS"], json={"content": text}, timeout=30)
print(f"fun_facts → Discord: {r.status_code}")
if r.status_code not in (200, 204):
    print(r.text)
