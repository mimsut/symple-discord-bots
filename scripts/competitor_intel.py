#!/usr/bin/env python3
"""SYMPLE 경쟁사 인텔리전스 — 실시간 뉴스 + Gemini 전략 분석"""
import os, requests, feedparser
import google.generativeai as genai
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

SYMPLE_CONTEXT = """SYMPLE 소개:
- 한국 멘탈헬스 스타트업. CEO: 김민수 (연세대 심리학 학·석사 4년, 18학점 남음)
- 제품: CBT 기반 멘탈케어 앱 Duck's Dream. 한국 B2C → 미국 B2B2C (기업 웰니스) 피벗 중
- 주요 성과: 토스 미니앱 신규 4위, 텀블벅 크라우드펀딩, 대한디지털치료학회 우수포스터, SF MARU 3주, 정주영창업경진대회
- 경쟁사: Calm, Headspace, Lyra Health, Spring Health, BetterUp, Modern Health, Woebot, Wysa, 트로스트, 마인드카페"""

QUERIES = [
    "Lyra Health OR Spring Health OR BetterUp OR Modern Health corporate wellness",
    "Calm OR Headspace OR Woebot mental health app 2025",
    "digital therapeutics EAP employee mental health startup funding",
    "트로스트 OR 마인드카페 멘탈헬스 기업",
]

entries = []
seen = set()
for q in QUERIES:
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        for e in feed.entries[:4]:
            t = e.get("title", "").strip()
            if t and t not in seen:
                seen.add(t)
                date = e.get("published", "")[:10]
                if " - " in t:
                    t = t.rsplit(" - ", 1)[0].strip()
                entries.append(f"• {t} ({date})")
    except:
        pass

news_text = "\n".join(entries[:15]) or "• 오늘 관련 뉴스 없음"

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(f"""오늘은 {today}.

{SYMPLE_CONTEXT}

오늘 수집된 경쟁사 뉴스:
{news_text}

아래 형식 그대로 Discord 메시지 작성 (다른 말 없이, 1800자 이내):

🔍 **SYMPLE 경쟁사 인텔리전스 | {today}**

**오늘의 주요 동향**
[뉴스 기반으로 경쟁사 동향 2-3개. 각 항목에 회사명과 구체적 내용 포함. bullet point.]

**📊 SYMPLE 전략 인사이트 TOP 3**
[뉴스와 SYMPLE 현황을 연결한 구체적 전략 시사점 3개. 숫자와 사실 포함.]

**⚡ 이번 주 SYMPLE 액션**
→ [가장 중요한 구체적 행동 1가지]""")

text = response.text.strip()[:2000]
r = requests.post(os.environ["DISCORD_COMPETITOR_INTEL"], json={"content": text}, timeout=30)
print(f"competitor_intel → Discord: {r.status_code}")
