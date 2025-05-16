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

def get_all_tokens():
    try:
        res = requests.get("https://api.dexscreener.com/latest/dex/pairs/solana", timeout=10)
        pairs = res.json().get("pairs", [])
        results = []
        for p in pairs:
            try:
                age = int(p.get("ageMinutes", 0))
                liq = float(p["liquidity"]["usd"])
                vol = float(p["volume"]["h24"])
                if age <= 120 and liq >= 100 and vol >= 500:
                    results.append(p)
            except:
                continue
        return results
    except Exception as e:
        print(f"Request Error: {e}")
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
    send_telegram("📡 PhantomScalerX v7.5 – High-Frequency Scanner Live (10s)")
    print("✅ Bot is scanning every 10 seconds...")
    seen = set()
    while True:
        tokens = get_all_tokens()
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
                    f"{emoji} *FRESH SOLANA TOKEN ALERT*\n\n"
                    f"• Symbol: {sym}\n"
                    f"• Price: ${price}\n"
                    f"• Liquidity: ${liq:,.0f}\n"
                    f"• Volume (24h): ${vol:,.0f}\n"
                    f"• Suggested Hold: {hold_time}\n"
                    f"• Hype Score: {score}/100\n"
                    f"• Risk Level: Medium\n"
                    f"• Discovered: {datetime.utcnow().strftime('%H:%M UTC')}"
                )
                print(f"📬 Alert sent for: {sym}")
                send_telegram(msg)
        time.sleep(10)

if __name__ == "__main__":
    from threading import Thread
    Thread(target=keep_alive).start()
    run_bot()