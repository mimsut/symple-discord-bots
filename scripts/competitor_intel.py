#!/usr/bin/env python3
"""SYMPLE 경쟁사 인텔리전스 — Google News RSS, API 키 없음"""
import os, requests, feedparser
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today_str = datetime.now(KST).strftime("%Y-%m-%d")

QUERIES = [
    "Lyra Health OR Spring Health OR BetterUp OR Modern Health",
    "Calm OR Headspace mental health app",
    "digital therapeutics corporate wellness startup",
    "mental health startup funding 2025",
]

def get_news(query, n=3):
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:n]
    except:
        return []

entries = []
seen = set()
for q in QUERIES:
    for e in get_news(q, 3):
        if e.title not in seen:
            seen.add(e.title)
            entries.append(e)
    if len(entries) >= 8:
        break

lines = [f"🔍 **SYMPLE 경쟁사 인텔리전스 | {today_str}**\n"]
lines.append("**📰 오늘의 주요 동향**")
for e in entries[:6]:
    title = e.title[:110]
    date  = e.get("published", "")[:10]
    if " - " in title:
        title = title.rsplit(" - ", 1)[0].strip()
    lines.append(f"• {title} *(~{date})*")

lines.append("")
lines.append("**💡 SYMPLE 관점 체크리스트**")
lines.append("□ 경쟁사 신규 B2B 파트너십 → SYMPLE 목표 기업에 선제 접근")
lines.append("□ 신기능 출시 → 차별화 포인트 재점검")
lines.append("□ 펀딩 소식 → 투자자 레이더 업데이트")
lines.append("")
lines.append("**⚡ 이번 주 액션**")
lines.append("위 뉴스 중 SYMPLE에 가장 위협적인 동향 1개를 골라 대응 전략을 문서화하세요.")

text = "\n".join(lines)[:2000]
r = requests.post(os.environ["DISCORD_COMPETITOR_INTEL"], json={"content": text}, timeout=30)
print(f"competitor_intel → Discord: {r.status_code}")
