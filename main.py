import time
import requests
from datetime import datetime
from keep_alive import keep_alive

def send_telegram(message):
    token = "7863553125:AAFcUIKGAb4NhfbwelZ6HJ7OnTLgxkZa0uQ"
    chat_id = "5768567714"
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": message})
    except Exception as e:
        print("Telegram Error:", e)

def get_meme_tokens():
    try:
        res = requests.get("https://api.dexscreener.com/latest/dex/pairs/solana")
        pairs = res.json().get("pairs", [])
        results = []
        for p in pairs:
            try:
                sym = p["baseToken"]["symbol"].lower()
                age = int(p.get("ageMinutes", 0))
                if any(m in sym for m in ["pepe", "doge", "elon", "rekt", "inu", "pump", "moon"]) and age <= 120:
                    liq = float(p["liquidity"]["usd"])
                    vol = float(p["volume"]["h24"])
                    if liq >= 3000 and vol >= 8000:
                        results.append(p)
            except:
                continue
        return results
    except:
        return []

def estimate_hold_time(vol, liq):
    if vol > 100000:
        return "2–4 hours max (high initial pump)"
    elif vol > 50000:
        return "4–8 hours (steady hype)"
    else:
        return "Hold 1–2 days max (low but climbing)"

def hype_score(vol, liq):
    base = 50
    if vol > 150000: base += 25
    elif vol > 80000: base += 15
    if liq > 15000: base += 10
    elif liq > 8000: base += 5
    return min(base, 100)

def emoji_tag(score):
    if score >= 85:
        return "🚀🔥"
    elif score >= 70:
        return "🚀"
    elif score >= 50:
        return "⚠️"
    else:
        return "💀"

def run_bot():
    send_telegram("📡 PhantomScalerX v7.1 – Meme Alerts + Hype Scoring Live")
    seen = set()
    while True:
        tokens = get_meme_tokens()
        for t in tokens:
            token_id = t['pairAddress']
            if token_id not in seen:
                seen.add(token_id)
                sym = t['baseToken']['symbol']
                price = t['priceUsd']
                liq = float(t['liquidity']['usd'])
                vol = float(t['volume']['h24'])
                hold_time = estimate_hold_time(vol, liq)
                score = hype_score(vol, liq)
                emoji = emoji_tag(score)
                msg = (
                    f"{emoji} *NEW MEME COIN ALERT*

"
                    f"• Symbol: {sym}
"
                    f"• Price: ${price}
"
                    f"• Liquidity: ${liq:,.0f}
"
                    f"• Volume (24h): ${vol:,.0f}
"
                    f"• Suggested Hold: {hold_time}
"
                    f"• Hype Score: {score}/100
"
                    f"• Risk Level: Medium
"
                    f"• Discovered: {datetime.utcnow().strftime('%H:%M UTC')}"
                )
                send_telegram(msg)
        time.sleep(90)

if __name__ == "__main__":
    keep_alive()
    run_bot()