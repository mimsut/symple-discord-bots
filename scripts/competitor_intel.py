#!/usr/bin/env python3
"""SYMPLE Competitor Intel Bot — 21:00 KST"""
import anthropic, os, requests, feedparser
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

SYMPLE_CONTEXT = """
SYMPLE 소개:
- 한국 멘탈헬스 스타트업. CEO: 김민수 (연세대 심리학 학·석사 4년, 18학점)
- 제품: CBT 기반 멘탈케어 앱 (Duck's Dream). 한국 B2C → 미국 B2B2C(기업 웰니스) 피벗 중
- 최근 성과: 토스 미니앱 론칭(신규 4위), 텀블벅 크라우드펀딩 성공, 대한디지털치료학회 우수포스터, SF MARU 3주 체류, 정주영창업경진대회 참가
- 경쟁사: Calm, Headspace, Lyra Health, Spring Health, BetterUp, Modern Health, Woebot, Wysa, Noom, MindDoc, Sanvello
"""

def get_news(query, n=4):
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        return [f"- {e.title} ({e.get('published','')[:16]})" for e in feed.entries[:n]]
    except:
        return []

queries = [
    "Lyra Health Spring Health BetterUp Modern Health 2025",
    "Calm Headspace mental health app 2025",
    "digital therapeutics corporate wellness funding 2025",
]
all_news = []
for q in queries:
    all_news.extend(get_news(q, 4))
news_text = "\n".join(all_news[:15]) or "(뉴스 없음)"

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=900,
    messages=[{"role": "user", "content": f"""당신은 날카로운 YC 파트너이자 VC 투자자입니다. 오늘은 {today}입니다.

{SYMPLE_CONTEXT}

오늘 수집된 경쟁사 관련 뉴스:
{news_text}

이 정보를 바탕으로 SYMPLE을 위한 경쟁 분석을 작성해 주세요.
Discord 메시지 형식, 최대 1800자:

🔍 **SYMPLE 경쟁사 인텔리전스 | {today}**

**📰 주요 동향**
[뉴스 기반 2-3개 bullet point]

**💡 SYMPLE 전략 인사이트 TOP 3**
1. [인사이트]
2. [인사이트]
3. [인사이트]

**⚡ 이번 주 액션 아이템**
[구체적인 행동 1가지]

한국어로 작성, 날카롭고 구체적으로."""}]
)

text = msg.content[0].text[:2000]
r = requests.post(os.environ["DISCORD_COMPETITOR_INTEL"], json={"content": text}, timeout=30)
print(f"competitor_intel → Discord: {r.status_code}")
if r.status_code not in (200, 204):
    print(r.text)
