#!/usr/bin/env python3
import os, requests, feedparser, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_utils import get_client, generate
import yfinance as yf
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today_kst = datetime.now(KST).strftime("%Y년 %m월 %d일")

def safe_get(url, params=None):
    try:
        return requests.get(url, params=params, timeout=10).json()
    except:
        return {}

def get_ticker(symbol):
    try:
        hist = yf.Ticker(symbol).history(period="2d")
        if len(hist) >= 2:
            prev, close = hist["Close"].iloc[-2], hist["Close"].iloc[-1]
            return close, (close - prev) / prev * 100
        elif len(hist) == 1:
            return hist["Close"].iloc[-1], 0.0
    except:
        pass
    return None, None

def fmt(v, prefix="$", dec=0):
    try:
        return f"{prefix}{float(v):,.{dec}f}"
    except:
        return "N/A"

def chg(v):
    try:
        return f"({float(v):+.2f}%)"
    except:
        return ""

# 주식
sp_p, sp_c     = get_ticker("^GSPC")
nq_p, nq_c     = get_ticker("^IXIC")
ks_p, ks_c     = get_ticker("^KS11")
kq_p, kq_c     = get_ticker("^KQ11")
au_p, au_c     = get_ticker("GC=F")

# 크립토
crypto = safe_get("https://api.coingecko.com/api/v3/simple/price",
    params={"ids":"bitcoin,ethereum,solana","vs_currencies":"usd","include_24hr_change":"true"})
btc = crypto.get("bitcoin", {})
eth = crypto.get("ethereum", {})
sol = crypto.get("solana", {})

# Fear & Greed
fng_data = safe_get("https://api.alternative.me/fng/?limit=1")
fng = fng_data.get("data",[{}])[0]
fng_val  = fng.get("value","N/A")
fng_cls  = fng.get("value_classification","N/A")

# 뉴스
def news(q, n=3):
    url = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=ko&gl=KR&ceid=KR:ko"
    try:
        return [e.title[:80] for e in feedparser.parse(url).entries[:n]]
    except:
        return []

macro = news("Fed 금리 미국 증시 경제", 3)
kr    = news("KOSPI KOSDAQ 한국 증시", 3)

data = f"""주식: S&P500 {fmt(sp_p,'')} {chg(sp_c)} | NASDAQ {fmt(nq_p,'')} {chg(nq_c)} | Gold {fmt(au_p)} {chg(au_c)}
한국: KOSPI {fmt(ks_p,'')} {chg(ks_c)} | KOSDAQ {fmt(kq_p,'')} {chg(kq_c)}
크립토: BTC {fmt(btc.get('usd'))} {chg(btc.get('usd_24h_change'))} | ETH {fmt(eth.get('usd'))} {chg(eth.get('usd_24h_change'))} | SOL {fmt(sol.get('usd'))} {chg(sol.get('usd_24h_change'))}
Fear&Greed: {fng_val}/100 ({fng_cls})
매크로뉴스: {' | '.join(macro)}
한국뉴스: {' | '.join(kr)}"""

client = get_client()
text = generate(client, f"""오늘은 {today_kst} 08:00 KST. 당신은 세계적 수준의 퀀트 트레이더·애널리스트입니다.

실시간 데이터:
{data}

아래 형식 그대로만 출력 (1900자 이내):

💰 **Money Printer 모닝브리핑 | {today_kst} KST**

🌍 **글로벌 매크로 (2-3 bullets)**
[위 뉴스·주가 데이터 해석. 핵심 이슈만.]

🇰🇷 **한국 시장 오늘**
• KOSPI: {fmt(ks_p,'')} {chg(ks_c)} — [한 줄 해석]
• KOSDAQ: {fmt(kq_p,'')} {chg(kq_c)} — [한 줄 해석]
• 주목 종목: [오늘 모멘텀·뉴스 기반 2개, 근거 포함]

🪙 **크립토 스냅샷**
• BTC: {fmt(btc.get('usd'))} {chg(btc.get('usd_24h_change'))} | 지지 [레벨] / 저항 [레벨]
• ETH: {fmt(eth.get('usd'))} {chg(eth.get('usd_24h_change'))}
• Fear & Greed: {fng_val}/100 ({fng_cls})

⚡ **매매 시그널**
[고확신: "[매수/매도] [자산] @ [가격] → Target [가격] | Stop [가격] — [근거]" / 없으면: "오늘은 관망"]

📌 **오늘의 인사이트**
[대부분 개인 투자자가 놓칠 비자명적 인사이트 1개]""")

r = requests.post(os.environ["DISCORD_MONEY_PRINTER"], json={"content": text[:2000]}, timeout=30)
print(f"money_printer → {r.status_code}")
