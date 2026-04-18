#!/usr/bin/env python3
"""Money Printer Morning Brief Bot — 08:00 KST (runs 23:00 UTC prev day)"""
import anthropic, os, requests
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
today_kst = datetime.now(KST).strftime("%Y-%m-%d")

def safe_get(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()
    except Exception as e:
        print(f"API error {url}: {e}")
        return {}

# Crypto prices
crypto = safe_get(
    "https://api.coingecko.com/api/v3/simple/price",
    params={"ids": "bitcoin,ethereum", "vs_currencies": "usd", "include_24hr_change": "true"}
)
btc = crypto.get("bitcoin", {})
eth = crypto.get("ethereum", {})

# Fear & Greed
fng_data = safe_get("https://api.alternative.me/fng/?limit=1")
fng = fng_data.get("data", [{}])[0]
fng_val = fng.get("value", "N/A")
fng_class = fng.get("value_classification", "N/A")

market_data = f"""
📊 실시간 데이터:
- BTC: ${btc.get('usd', 'N/A'):,} (24h: {float(btc.get('usd_24h_change', 0)):.1f}%)
- ETH: ${eth.get('usd', 'N/A'):,} (24h: {float(eth.get('usd_24h_change', 0)):.1f}%)
- Fear & Greed Index: {fng_val} ({fng_class})
"""

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": f"""당신은 세계 최고 수준의 퀀트 트레이더이자 애널리스트입니다. 오늘은 {today_kst} 08:00 KST입니다.

{market_data}

위 실시간 데이터와 당신의 시장 지식을 바탕으로 모닝 브리핑을 작성하세요.
Discord 메시지 형식, 최대 1900자:

💰 **Money Printer 모닝브리핑 | {today_kst} 08:00 KST**

🌍 **글로벌 매크로 (2-3 bullets)**
[간밤 주요 이슈 — Fed, 지정학, 매크로 데이터]

🇰🇷 **한국 시장 오늘**
[KOSPI/KOSDAQ 전망, 주목할 종목 2-3개 (모멘텀/실적/뉴스 기반)]

🪙 **크립토 스냅샷**
- BTC: ${btc.get('usd', 'N/A'):,} → [주요 지지/저항 레벨]
- ETH: ${eth.get('usd', 'N/A'):,} → [주요 지지/저항 레벨]
- Fear & Greed: {fng_val} ({fng_class})
[모멘텀 있는 알트코인 있으면 언급]

⚡ **매매 시그널 (가장 중요)**
[고확신 셋업이 있으면: "[매수/매도] [자산] @ [가격] — 목표: [가격] — 손절: [가격] — 근거: [1문장]"
없으면: "오늘은 관망 (No clear signal today)"]

📌 **하나의 인사이트**
[대부분의 개인 투자자가 놓칠 비자명적 인사이트]

한국어로 작성."""}]
)

text = msg.content[0].text[:2000]
r = requests.post(os.environ["DISCORD_MONEY_PRINTER"], json={"content": text}, timeout=30)
print(f"money_printer → Discord: {r.status_code}")
if r.status_code not in (200, 204):
    print(r.text)
