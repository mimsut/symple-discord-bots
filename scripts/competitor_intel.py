#!/usr/bin/env python3
import os, requests, feedparser, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_client, generate
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

QUERIES = [
    "Lyra Health OR Spring Health OR BetterUp OR Modern Health corporate wellness",
    "Calm OR Headspace OR Woebot mental health app",
    "digital therapeutics EAP employee mental health startup",
    "트로스트 OR 마인드카페 멘탈헬스 기업",
]

entries, seen = [], set()
for q in QUERIES:
    try:
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en&gl=US&ceid=US:en"
        for e in feedparser.parse(url).entries[:4]:
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
client = get_client()
text = generate(client, f"""오늘은 {today}.

SYMPLE: CBT 기반 멘탈헬스 앱 Duck's Dream. CEO 김민수(연세대 심리학). 한국 B2C → 미국 B2B2C 피벗 중.
성과: 토스 미니앱 신규 4위, 텀블벅, 대한디지털치료학회 우수포스터, SF MARU 3주.
경쟁사: Calm, Headspace, Lyra Health, Spring Health, BetterUp, Modern Health, Woebot, 트로스트, 마인드카페.

오늘 경쟁사 뉴스:
{news_text}

아래 형식 그대로만 출력 (1800자 이내):

🔍 **SYMPLE 경쟁사 인텔리전스 | {today}**

**오늘의 주요 동향**
[경쟁사 동향 2-3개. 회사명·구체적 내용 포함. bullet point.]

**📊 SYMPLE 전략 인사이트 TOP 3**
[SYMPLE 현황과 연결한 구체적 전략 시사점 3개. 숫자·사실 포함.]

**⚡ 이번 주 SYMPLE 액션**
→ [구체적 행동 1가지]""")

r = requests.post(os.environ["DISCORD_COMPETITOR_INTEL"], json={"content": text[:2000]}, timeout=30)
print(f"competitor_intel → {r.status_code}")
