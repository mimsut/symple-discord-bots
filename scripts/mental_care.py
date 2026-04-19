#!/usr/bin/env python3
import os, requests, feedparser, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_client, generate
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

QUERIES = [
    "depression anxiety treatment therapy 2024",
    "burnout workplace stress mental health",
    "CBT cognitive behavioral therapy research",
    "mindfulness meditation mental health study",
    "panic disorder PTSD therapy treatment",
    "sleep disorder insomnia mental health",
    "addiction recovery mental health",
    "mental health app digital therapy",
]

entries, seen = [], set()
for q in QUERIES:
    try:
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en&gl=US&ceid=US:en"
        for e in feedparser.parse(url).entries[:3]:
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
client = get_client()
text = generate(client, f"""오늘은 {today}. 아래 뉴스에서 가장 중요한 5개를 골라 Discord 메시지를 작성하세요.

뉴스:
{news_text}

아래 형식 그대로만 출력 (총 1900자 이내):

🧠 **멘탈케어 · 심리학 데일리 — {today}**

1) [영문 원제목]
🇰🇷 [한국어 제목 번역]
[한국어 요약 2-3문장. 구체적 수치·연구 결과 포함.]
[Source Name] · [날짜] | [URL]

2) ~ 5) 동일 형식

— 출처: APA · NIMH · ScienceDaily · PsyPost · MGH Women's MH

⚠️ 중요: 영문 원제목(1번 줄)을 제외한 모든 텍스트는 반드시 한국어로만 작성하세요. 번역·요약·출처 설명 등 어떤 부분도 영어로 쓰지 마세요.""")

r = requests.post(os.environ["DISCORD_MENTAL_CARE"], json={"content": text[:2000]}, timeout=30)
print(f"mental_care → {r.status_code}")
