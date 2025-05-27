import asyncio
import re
from telethon import TelegramClient, events
from calculate_position import calculate_position   
from binance_handler import open_long, open_short
from binance_handler import close_position, handle_tp_update
from keep_alive import keep_alive
keep_alive()


# Telegram API credentials
api_id = 22874799      # ← Replace with your API ID
api_hash = '1173f8b66f57f86cbdf61fb7526a7c80'  # ← Replace with your API HASH
channel_id = -1002430397970  # ← Your private Telegram channel ID

client = TelegramClient('session', api_id, api_hash)

# Parse signal text from Telegram messages
def parse_signal(text):
    data = {}

    if "Opening LONG" in text:
        data["action"] = "buy"
    elif "Opening SHORT" in text:
        data["action"] = "sell"
    elif "Closing" in text:
        data["action"] = "close"
    elif "Partial Close" in text:
        data["action"] = "partial_close"

    match_symbol = re.search(r'Symbol:\s*(\w+)', text)
    if match_symbol:
        data["symbol"] = match_symbol.group(1)

    match_price = re.search(r'Price:\s*([\d.]+)', text)
    if match_price:
        data["entry"] = float(match_price.group(1))
        if "symbol" in data:
            data["position_size"] = calculate_position(data["entry"], data["symbol"])

    match_sl = re.search(r'Stop Loss:\s*([\d.]+)', text)
    if match_sl:
        data["sl"] = float(match_sl.group(1))

    targets = re.findall(r'TP\d:\s*([\d.]+)', text)
    if targets:
        data["tp"] = [float(t) for t in targets]

    if "First target reached" in text:
        data["tp_hit"] = 1
    elif "Second target reached" in text:
        data["tp_hit"] = 2
    elif "3rd target reached" in text or "Third target reached" in text:
        data["tp_hit"] = 3

    if "tp_hit" in data:
        if data["tp_hit"] == 1:
            data["new_sl"] = round(data["entry"] * (1 - 0.01), 6)
        elif data["tp_hit"] == 2 and "tp" in data:
            data["new_sl"] = round(data["tp"][0] * (1 - 0.01), 6)
        elif data["tp_hit"] == 3 and "tp" in data:
            data["new_sl"] = round(data["tp"][1] * (1 - 0.01), 6)

    return data

@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    text = event.raw_text
    print("=" * 40)
    print("📨 New message received:")
    print(text)

    result = parse_signal(text)
    print("\n📊 Parsed data:")
    print(result)

    if result.get("tp_hit"):
        print("🔁 TP hit detected. Updating Stop Loss...")
        handle_tp_update(
            symbol=result["symbol"],
            side=result["action"],
            quantity=result["position_size"],
            tp_hit=result["tp_hit"],
            entry=result.get("entry"),
            tps=result.get("tp", [])
        )

    if result.get("action") == "buy":
        print(f"🚀 Executing LONG on {result['symbol']} for {result['position_size']} units")
        open_long(result["symbol"], result["position_size"], tps=result.get("tp", []), sl=result.get("sl"), entry=result.get("entry"))

    elif result.get("action") == "sell":
        print(f"📉 Executing SHORT on {result['symbol']} for {result['position_size']} units")
        open_short(result["symbol"], result["position_size"], tps=result.get("tp", []), sl=result.get("sl"), entry=result.get("entry"))

    elif result.get("action") == "close":
        print(f"❌ Closing position on {result['symbol']}")
        close_position(result["symbol"], "buy")

    else:
        print("ℹ️ No trade action to execute.")

async def main():
    print("🔄 Starting Telegram-Binance bot...")
    await client.start()
    print("✅ Telegram client connected.")
    await client.run_until_disconnected()

asyncio.run(main())