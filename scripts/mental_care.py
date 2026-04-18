#!/usr/bin/env python3
"""멘탈케어 · 심리학 데일리 — 실시간 뉴스 + Gemini 한국어 요약"""
import os, requests, feedparser
import google.generativeai as genai
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

SOURCES = [
    "https://www.sciencedaily.com/rss/mind_brain/psychology.xml",
    "https://www.apa.org/news/press/releases/index.aspx",  # fallback
    "https://news.google.com/rss/search?q=mental+health+psychology+research+therapy&hl=en&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=site:psypost.org+OR+site:sciencedaily.com+mental+health&hl=en&gl=US&ceid=US:en",
    "https://womensmentalhealth.org/feed/",
]

entries = []
seen = set()
for src in SOURCES:
    try:
        feed = feedparser.parse(src)
        for e in feed.entries[:6]:
            t = e.get("title", "").strip()
            if t and t not in seen:
                seen.add(t)
                link = e.get("link", "")
                date = e.get("published", "")[:10]
                summary = e.get("summary", "")[:300]
                # 언론사 파싱
                source_name = ""
                if " - " in t:
                    parts = t.rsplit(" - ", 1)
                    t = parts[0].strip()
                    source_name = parts[1].strip()
                entries.append({"title": t, "link": link, "date": date,
                                "summary": summary, "source": source_name})
    except:
        pass
    if len(entries) >= 10:
        break

news_text = "\n".join(
    f"{i+1}. {e['title']}"
    + (f" — {e['source']}" if e['source'] else "")
    + f" | {e['date']} | {e['link']}"
    + (f"\n   [{e['summary'][:200]}]" if e['summary'] else "")
    for i, e in enumerate(entries[:10])
)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(f"""오늘은 {today}. 아래 뉴스 목록에서 가장 중요한 5개를 골라 Discord 메시지를 작성하세요.

뉴스 목록:
{news_text}

아래 형식 그대로 출력 (다른 말 없이, 총 1900자 이내):

🧠 **멘탈케어 · 심리학 데일리 — {today}**

1) [영문 원제목]
🇰🇷 [한국어 제목 번역]
[한국어 요약 2-3문장. 구체적 수치·연구 결과 포함. 전문적이되 이해하기 쉽게.]
[Source Name] · [날짜] | [URL]

2) ~ 5) 동일 형식

— 출처: APA · NIMH · ScienceDaily · PsyPost · MGH Women's MH""")

text = response.text.strip()[:2000]
r = requests.post(os.environ["DISCORD_MENTAL_CARE"], json={"content": text}, timeout=30)
print(f"mental_care → Discord: {r.status_code}")
