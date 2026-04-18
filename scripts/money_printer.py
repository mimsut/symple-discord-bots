#!/usr/bin/env python3
"""Money Printer 모닝브리핑 — 무료 API만 사용, API 키 없음"""
import os, requests, feedparser
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today_str = datetime.now(KST).strftime("%Y-%m-%d")

def safe_get(url, params=None):
    try:
        return requests.get(url, params=params, timeout=10).json()
    except:
        return {}

# 크립토 (CoinGecko 무료)
crypto = safe_get(
    "https://api.coingecko.com/api/v3/simple/price",
    params={"ids": "bitcoin,ethereum,solana", "vs_currencies": "usd,krw", "include_24hr_change": "true"},
)
btc = crypto.get("bitcoin", {})
eth = crypto.get("ethereum", {})
sol = crypto.get("solana", {})

# Fear & Greed (alternative.me 무료)
fng_data = safe_get("https://api.alternative.me/fng/?limit=1")
fng = fng_data.get("data", [{}])[0]
fng_val = fng.get("value", "N/A")
fng_class = fng.get("value_classification", "N/A")

# 금융 뉴스 (RSS)
def get_fin_news(query, n=3):
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    try:
        feed = feedparser.parse(url)
        return [e.title[:80] for e in feed.entries[:n]]
    except:
        return []

macro_news = get_fin_news("Fed 금리 거시경제 증시", 3)
kr_news    = get_fin_news("KOSPI KOSDAQ 한국 증시", 3)

def fmt_change(v):
    try:
        f = float(v)
        return f"{f:+.2f}%"
    except:
        return "N/A"

def fmt_price(v, comma=True):
    try:
        return f"${int(v):,}" if comma else str(v)
    except:
        return "N/A"

macro_str = "\n".join(f"• {h}" for h in macro_news) if macro_news else "• 뉴스 로딩 실패"
kr_str    = "\n".join(f"• {h}" for h in kr_news)    if kr_news    else "• 뉴스 로딩 실패"

msg = f"""💰 **Money Printer 모닝브리핑 | {today_str} 08:00 KST**

🌍 **글로벌 매크로**
{macro_str}

🇰🇷 **한국 증시 헤드라인**
{kr_str}

🪙 **크립토 실시간**
- BTC {fmt_price(btc.get('usd'))} ({fmt_change(btc.get('usd_24h_change'))}) | ₩{int(btc.get('krw',0)):,}
- ETH {fmt_price(eth.get('usd'))} ({fmt_change(eth.get('usd_24h_change'))}) | ₩{int(eth.get('krw',0)):,}
- SOL {fmt_price(sol.get('usd'))} ({fmt_change(sol.get('usd_24h_change'))})
- 공포·탐욕 지수: **{fng_val}/100** ({fng_class})

⚡ **오늘의 판단 기준**
F&G {fng_val} → {'극단적 탐욕 — 신중하게. 고점 매도 고려' if int(fng_val or 0) >= 75 else '극단적 공포 — 분할 매수 기회 검토' if int(fng_val or 0) <= 25 else '중립 구간 — 추세 추종, 뚜렷한 시그널 없음'}

📌 데이터 기준: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"""

r = requests.post(os.environ["DISCORD_MONEY_PRINTER"], json={"content": msg[:2000]}, timeout=30)
print(f"money_printer → Discord: {r.status_code}")
