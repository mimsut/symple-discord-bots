#!/usr/bin/env python3
"""멘탈케어 데일리 — Google News RSS, API 키 없음"""
import os, requests, feedparser
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today_str = datetime.now(KST).strftime("%Y-%m-%d")

QUERIES = [
    "mental health therapy digital app",
    "depression anxiety treatment research",
    "mindfulness CBT wellness study",
]

def get_news(query, n=4):
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        return feed.entries[:n]
    except:
        return []

entries = []
seen = set()
for q in QUERIES:
    for e in get_news(q, 4):
        if e.title not in seen:
            seen.add(e.title)
            entries.append(e)
        if len(entries) >= 5:
            break
    if len(entries) >= 5:
        break

lines = [f"🏥 **멘탈케어 데일리 | {today_str}**\n"]
for i, e in enumerate(entries[:5], 1):
    title = e.title[:100]
    date  = e.get("published", "")[:10]
    link  = e.link
    # 출처명: 제목 끝 " - Source" 패턴 파싱
    source = ""
    if " - " in title:
        parts = title.rsplit(" - ", 1)
        title  = parts[0].strip()
        source = parts[1].strip()
    lines.append(f"**{i}. {title}**")
    if source:
        lines.append(f"   출처: {source} · {date} | {link}")
    else:
        lines.append(f"   {date} | {link}")
    lines.append("")

text = "\n".join(lines)[:2000]
r = requests.post(os.environ["DISCORD_MENTAL_CARE"], json={"content": text}, timeout=30)
print(f"mental_care → Discord: {r.status_code}")
