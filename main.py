import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from Indicator.EMA_TREND import EMA_TREND
from services.bybit_service import get_data
from Signals.buy_signals import BuySignals
from Signals.sell_signals import SellSignals
from telegram.ext import Application, CommandHandler
import asyncio
from Commands.commands import trend, zone, print_zone_debug

load_dotenv()
# =========================
# Command settings
# =========================
app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

# bind commands
app.add_handler(CommandHandler("trend", trend))
app.add_handler(CommandHandler("zone", zone))

# =========================
# TELEGRAM SETTINGS
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# TELEGRAM FUNCTION
# =========================

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)

async def wait_for_next_5min():
    now = datetime.now()

    # seconds passed in current 5m block
    seconds_passed = (now.minute % 5) * 60 + now.second

    # seconds until next 5m candle
    sleep_time = 300 - seconds_passed

    print(f"Waiting {sleep_time:.0f}s until next 5m candle...")

    await asyncio.sleep(sleep_time)


async def signal_loop():

    while True:

        await wait_for_next_5min()

        try:

            df = get_data()

            trend = EMA_TREND.check(df)

            print_zone_debug(df, trend)

            buy_signal = BuySignals.check(df)
            sell_signal = SellSignals.check(df)

            if buy_signal:
                send_telegram(buy_signal)
                print(buy_signal)

            if sell_signal:
                send_telegram(sell_signal)
                print(sell_signal)

            print("Checked signals...")

        except Exception as e:
            print("Signal Loop Error:", e)

# =========================
# MAIN LOOP
# =========================

print(f'Bot started... {datetime.now().strftime("%H:%M:%S")}')
send_telegram("✅ EMA Signal Bot Online")

async def main():

    print("Bot started...")

    # start telegram bot
    await app.initialize()
    await app.start()

    # start polling
    await app.updater.start_polling()

    # start signal loop
    asyncio.create_task(signal_loop())

    # keep app alive forever
    while True:
        await asyncio.sleep(3600)


asyncio.run(main())

# while True:

#     wait_for_next_5min()

#     current_time = datetime.now().strftime("%H:%M:%S")
#     print(f"\nChecking signals at {current_time}")

#     try:

#         df = get_data()

#         buy_signal = BuySignals.check(df)
#         sell_signal = SellSignals.check(df)

#         if buy_signal:
#             send_telegram(buy_signal)
#             print(buy_signal)

#         if sell_signal:
#             send_telegram(sell_signal)
#             print(sell_signal)

#         # DELETE
#         print(" ")
#         print(" ")
#         trend = EMA_TREND.check(df)
#         print_zone_debug(df, trend)
#         print(" ")
#         print(" ")

#     except Exception as e:
#         print("Error:", e)