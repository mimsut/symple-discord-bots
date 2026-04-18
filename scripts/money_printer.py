#!/usr/bin/env python3
"""Money Printer 모닝브리핑 — 실시간 시장 데이터 + Gemini 분석"""
import os, requests, feedparser
import google.generativeai as genai
import yfinance as yf
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today_kst = datetime.now(KST).strftime("%Y년 %m월 %d일")

def safe_get(url, params=None):
    try:
        return requests.get(url, params=params, timeout=10).json()
    except:
        return {}

def fmt(v, prefix="$", decimals=0):
    try:
        f = float(v)
        return f"{prefix}{f:,.{decimals}f}"
    except:
        return "N/A"

def fmt_chg(v):
    try:
        f = float(v)
        return f"({f:+.2f}%)"
    except:
        return ""

# ── 크립토 (CoinGecko 무료) ──────────────────────────────────────
crypto = safe_get(
    "https://api.coingecko.com/api/v3/simple/price",
    params={"ids": "bitcoin,ethereum,solana", "vs_currencies": "usd",
            "include_24hr_change": "true"},
)
btc = crypto.get("bitcoin", {})
eth = crypto.get("ethereum", {})
sol = crypto.get("solana", {})

# ── Fear & Greed ─────────────────────────────────────────────────
fng_data = safe_get("https://api.alternative.me/fng/?limit=1")
fng      = fng_data.get("data", [{}])[0]
fng_val  = fng.get("value", "N/A")
fng_class= fng.get("value_classification", "N/A")

# ── 주식 시장 (Yahoo Finance) ────────────────────────────────────
def get_ticker(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="2d")
        if len(hist) >= 2:
            prev  = hist["Close"].iloc[-2]
            close = hist["Close"].iloc[-1]
            chg   = (close - prev) / prev * 100
            return close, chg
        elif len(hist) == 1:
            return hist["Close"].iloc[-1], 0.0
    except:
        pass
    return None, None

sp500_p,  sp500_c  = get_ticker("^GSPC")
nasdaq_p, nasdaq_c = get_ticker("^IXIC")
kospi_p,  kospi_c  = get_ticker("^KS11")
kosdaq_p, kosdaq_c = get_ticker("^KQ11")
gold_p,   gold_c   = get_ticker("GC=F")

# ── 금융 뉴스 RSS ────────────────────────────────────────────────
def get_news(q, n=3):
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=ko&gl=KR&ceid=KR:ko"
    try:
        feed = feedparser.parse(url)
        return [e.title[:80] for e in feed.entries[:n]]
    except:
        return []

macro_news = get_news("Fed 금리 미국 증시 경제", 3)
kr_news    = get_news("KOSPI KOSDAQ 한국 증시", 3)

# ── 데이터 취합 ──────────────────────────────────────────────────
market_data = f"""
📈 글로벌 주식:
- S&P500:  {fmt(sp500_p,  '', 1)} {fmt_chg(sp500_c)}
- NASDAQ:  {fmt(nasdaq_p, '', 1)} {fmt_chg(nasdaq_c)}
- Gold:    {fmt(gold_p)}  {fmt_chg(gold_c)}

🇰🇷 한국 주식:
- KOSPI:  {fmt(kospi_p,  '', 2)} {fmt_chg(kospi_c)}
- KOSDAQ: {fmt(kosdaq_p, '', 2)} {fmt_chg(kosdaq_c)}

🪙 크립토:
- BTC: {fmt(btc.get('usd'))} {fmt_chg(btc.get('usd_24h_change'))}
- ETH: {fmt(eth.get('usd'))} {fmt_chg(eth.get('usd_24h_change'))}
- SOL: {fmt(sol.get('usd'))} {fmt_chg(sol.get('usd_24h_change'))}
- Fear & Greed: {fng_val}/100 ({fng_class})

📰 매크로 뉴스: {' | '.join(macro_news)}
📰 한국 뉴스:   {' | '.join(kr_news)}
"""

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(f"""오늘은 {today_kst} 08:00 KST.
당신은 세계적 수준의 퀀트 트레이더이자 시장 애널리스트입니다.

실시간 시장 데이터:
{market_data}

아래 형식 그대로 Discord 메시지 작성 (다른 말 없이, 총 1900자 이내):

💰 **Money Printer 모닝브리핑 | {today_kst} KST**

🌍 **글로벌 매크로 (2-3 bullets)**
[위 뉴스와 주가 데이터를 해석한 간밤 핵심 이슈]

🇰🇷 **한국 시장 오늘**
• KOSPI: [위 데이터 반영] — [한 줄 해석]
• KOSDAQ: [위 데이터 반영] — [한 줄 해석]
• 주목 종목: [오늘 모멘텀/뉴스 기반 2개, 근거 포함]

🪙 **크립토 스냅샷**
• BTC: [위 데이터] | 지지 [레벨] / 저항 [레벨]
• ETH: [위 데이터]
• Fear & Greed: {fng_val}/100 ({fng_class})

⚡ **매매 시그널**
[고확신 셋업: "[매수/매도] [자산] @ [가격] → Target: [가격] | Stop: [가격] — [근거 1문장]"
없으면: "오늘은 관망 (No clear signal today)"]

📌 **오늘의 인사이트**
[대부분의 개인 투자자가 놓칠 비자명적 인사이트 1개]""")

text = response.text.strip()[:2000]
r = requests.post(os.environ["DISCORD_MONEY_PRINTER"], json={"content": text}, timeout=30)
print(f"money_printer → Discord: {r.status_code}")
