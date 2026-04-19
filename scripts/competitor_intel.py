#!/usr/bin/env python3
import os, requests, feedparser, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_client, generate
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today = datetime.now(KST)
today_str = today.strftime("%Y-%m-%d")
doy = today.timetuple().tm_yday

# 매일 다른 경쟁사 그룹에 집중
FOCUS_GROUPS = [
    ("B2B 기업웰니스 강자", ["Lyra Health", "Spring Health", "Modern Health", "Headspace for Work"]),
    ("소비자 앱 대형사", ["Calm", "Headspace", "BetterUp", "Noom"]),
    ("AI·챗봇 멘탈헬스", ["Woebot", "Wysa", "Youper", "Replika"]),
    ("디지털치료제·FDA", ["Pear Therapeutics", "Click Therapeutics", "Big Health", "Limbix"]),
    ("한국·아시아 경쟁사", ["트로스트", "마인드카페", "산다", "뤼이드"]),
    ("기업웰니스 플랫폼", ["Wellhub", "Gympass", "Virgin Pulse", "Vida Health"]),
    ("VC·펀딩 동향", ["mental health startup funding", "digital therapeutics investment"]),
]

focus_label, focus_companies = FOCUS_GROUPS[doy % len(FOCUS_GROUPS)]

# 오늘의 포커스 그룹 + 항상 포함되는 광역 쿼리
QUERIES = [
    " OR ".join(f'"{c}"' for c in focus_companies) + " mental health",
    " OR ".join(focus_companies[:3]),
    "digital therapeutics EAP corporate wellness deal partnership",
    "mental health startup Series funding raise 2024 2025",
]

entries, seen = [], set()
for q in QUERIES:
    try:
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en&gl=US&ceid=US:en"
        for e in feedparser.parse(url).entries[:5]:
            raw_title = e.get("title", "").strip()
            if not raw_title or raw_title in seen:
                continue
            seen.add(raw_title)
            link = e.get("link", "")
            date = e.get("published", "")[:10]
            summary = e.get("summary", "")[:300]
            # 출처명 분리
            source = ""
            title = raw_title
            if " - " in raw_title:
                title, source = raw_title.rsplit(" - ", 1)
                title = title.strip()
                source = source.strip()
            entries.append({
                "title": title,
                "source": source,
                "date": date,
                "url": link,
                "summary": summary,
            })
    except:
        pass
    if len(entries) >= 12:
        break

news_lines = []
for i, e in enumerate(entries[:12], 1):
    line = f"[{i}] {e['title']}"
    if e["source"]:
        line += f" — {e['source']}"
    if e["date"]:
        line += f" ({e['date']})"
    if e["url"]:
        line += f"\n    URL: {e['url']}"
    if e["summary"]:
        line += f"\n    요약: {e['summary'][:200]}"
    news_lines.append(line)

news_text = "\n".join(news_lines) or "관련 뉴스 없음"

client = get_client()
text = generate(client, f"""오늘은 {today_str}. 오늘의 경쟁사 포커스: {focus_label} ({', '.join(focus_companies[:4])})

SYMPLE: CBT 기반 멘탈헬스 앱 Duck's Dream. CEO 김민수(연세대 심리학). 한국 B2C → 미국 B2B2C 피벗 중.
성과: 토스 미니앱 신규 4위, 텀블벅 크라우드펀딩, 대한디지털치료학회 우수포스터, SF MARU 3주.

오늘 수집된 뉴스 (출처·URL 포함):
{news_text}

아래 형식 그대로만 출력 (1900자 이내):

🔍 **SYMPLE 경쟁사 인텔리전스 | {today_str}**
📌 오늘 포커스: {focus_label}

**📰 주요 동향** (뉴스에서 가장 중요한 3개 선별, 반드시 출처와 URL 표기)
• [경쟁사명] [구체적 내용 — 수치·계약·기능·펀딩 등]
  📎 출처: [언론사명] | [URL]
• [동일 형식]
• [동일 형식]

**📊 SYMPLE 전략 인사이트**
① [위 뉴스와 연결한 SYMPLE에 대한 구체적 시사점. 숫자 포함.]
② [동일]
③ [동일]

**⚡ 이번 주 SYMPLE 액션**
→ [오늘 뉴스 기반 가장 급한 구체적 행동 1가지]

⚠️ 중요: 회사명·URL·언론사명 외 모든 텍스트는 반드시 한국어로만 작성하세요. URL은 절대 생략하지 마세요.""", max_tokens=900)

r = requests.post(os.environ["DISCORD_COMPETITOR_INTEL"], json={"content": text[:2000]}, timeout=30)
print(f"competitor_intel → {r.status_code}")
