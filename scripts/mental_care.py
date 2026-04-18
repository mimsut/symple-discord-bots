#!/usr/bin/env python3
import os, requests, feedparser, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_model, generate
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

FEEDS = [
    "https://www.sciencedaily.com/rss/mind_brain/psychology.xml",
    "https://news.google.com/rss/search?q=mental+health+psychology+research+therapy&hl=en&gl=US&ceid=US:en",
    "https://womensmentalhealth.org/feed/",
    "https://news.google.com/rss/search?q=site:psypost.org+mental+health&hl=en&gl=US&ceid=US:en",
]

entries, seen = [], set()
for src in FEEDS:
    try:
        for e in feedparser.parse(src).entries[:6]:
            t = e.get("title", "").strip()
            if t and t not in seen:
                seen.add(t)
                link = e.get("link", "")
                date = e.get("published", "")[:10]
                summary = e.get("summary", "")[:250]
                src_name = ""
                if " - " in t:
                    t, src_name = t.rsplit(" - ", 1)
                entries.append(f"• {t.strip()}" + (f" ({src_name.strip()})" if src_name else "") + f" | {date} | {link}" + (f"\n  [{summary}]" if summary else ""))
    except:
        pass
    if len(entries) >= 10:
        break

news_text = "\n".join(entries[:10])
model = get_model(os.environ["GEMINI_API_KEY"])
text = generate(model, f"""오늘은 {today}. 아래 뉴스에서 가장 중요한 5개를 골라 Discord 메시지를 작성하세요.

뉴스:
{news_text}

아래 형식 그대로만 출력 (총 1900자 이내):

🧠 **멘탈케어 · 심리학 데일리 — {today}**

1) [영문 원제목]
🇰🇷 [한국어 제목 번역]
[한국어 요약 2-3문장. 구체적 수치·연구 결과 포함.]
[Source Name] · [날짜] | [URL]

2) ~ 5) 동일 형식

— 출처: APA · NIMH · ScienceDaily · PsyPost · MGH Women's MH""")

r = requests.post(os.environ["DISCORD_MENTAL_CARE"], json={"content": text[:2000]}, timeout=30)
print(f"mental_care → {r.status_code}")
