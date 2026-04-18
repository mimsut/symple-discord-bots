#!/usr/bin/env python3
"""SYMPLE Mental Care Daily Bot — 09:30 KST"""
import anthropic, os, requests, feedparser
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

def get_news(query, n=8):
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(url)
        items = []
        for e in feed.entries[:n]:
            items.append({
                "title": e.title,
                "link": e.link,
                "date": e.get("published", "")[:16],
            })
        return items
    except Exception as ex:
        print(f"RSS error: {ex}")
        return []

news = get_news("mental health therapy app research 2025", 10)
news_text = "\n".join(
    f"{i+1}. {n['title']} | {n['date']} | {n['link']}"
    for i, n in enumerate(news)
)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1800,
    messages=[{"role": "user", "content": f"""오늘은 {today}입니다.

아래는 오늘의 멘탈헬스 관련 영문 뉴스 목록입니다:
{news_text}

이 중 가장 중요한 5개를 선택하여 아래 형식의 Discord 메시지를 작성해 주세요.

형식:
🏥 **멘탈케어 데일리 | {today}**

1. **[영문 제목 그대로]**
   🇰🇷 **[한국어 제목 번역]**
   [한국어 요약 2-3문장]
   출처: [언론사] · [날짜] | [URL]

2. ...
(5개까지)

총 1900자 이내로 작성해주세요."""}]
)

text = msg.content[0].text[:2000]
r = requests.post(os.environ["DISCORD_MENTAL_CARE"], json={"content": text}, timeout=30)
print(f"mental_care → Discord: {r.status_code}")
if r.status_code not in (200, 204):
    print(r.text)
