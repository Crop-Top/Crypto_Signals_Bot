import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from Indicator.EMA_TREND import EMA_TREND
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal
from services.bybit_service import get_data
from Signals.buy_signals import BuySignals
from Signals.sell_signals import SellSignals
from telegram.ext import Application, CommandHandler
import asyncio
from Commands.commands import trend, zone, print_zone_debug, stopbot
from Tracker.trade_tracker import TradeTracker
from Tracker.trade_logger import TradeLogger
from services.webhook_service import send_signal
from Utils.telegram_formatter import format_signal

load_dotenv()
# =========================
# Command settings
# =========================
app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

# bind commands
app.add_handler(CommandHandler("trend", trend))
app.add_handler(CommandHandler("zone", zone))
app.add_handler(CommandHandler("stopbot", stopbot))

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
    #seconds_passed = (now.minute % 1) * 60 + now.second

    # seconds until next 5m candle
    sleep_time = 300 - seconds_passed
    #sleep_time = 60 - seconds_passed

    print(f"Waiting {sleep_time:.0f}s until next 5m candle...")

    await asyncio.sleep(sleep_time)


async def signal_loop():

    while True:

        await wait_for_next_5min()

        try:

            df = get_data()
            current_price = df["close"].iloc[-1]

            trend = EMA_TREND.check(df)
            rsi_signal = RSI_Trend_Continue_signal.check(df, trend)

            print_zone_debug(df)

            # =========================
            # 1. UPDATE EXISTING TRADE
            # =========================
            if TradeTracker.active_trade is not None:
                TradeTracker.update_trade(current_price)

            # =========================
            # 2. CHECK SIGNALS
            # =========================
            buy_signal = BuySignals.check(df, trend, rsi_signal)
            sell_signal = SellSignals.check(df, trend, rsi_signal)

            # =========================
            # 3. EXECUTION LOGIC
            # =========================

            if buy_signal:

                # close existing trade (OPTION A)
                if TradeTracker.active_trade is not None:
                    TradeTracker.close_trade(current_price)

                # open new trade
                TradeTracker.open_trade(
                    signal="BUY_CONTINUATION",
                    entry_price=buy_signal["price"],
                    trend=trend,
                    rsi=getattr(RSI_Trend_Continue_signal, "current_rsi", None),
                    zone_transition="LOW->HIGH"
                )

                success = send_signal(buy_signal)

                if success:
                    print("[WEBHOOK] Signal delivered")
                else:
                    print("[WEBHOOK] Signal delivery failed")

                telegram_message = format_signal(buy_signal)

                send_telegram(telegram_message)
                print(buy_signal)

            elif sell_signal:

                if TradeTracker.active_trade is not None:
                    TradeTracker.close_trade(current_price)

                TradeTracker.open_trade(
                    signal="SELL_CONTINUATION",
                    entry_price=sell_signal["price"],
                    trend=trend,
                    rsi=getattr(RSI_Trend_Continue_signal, "current_rsi", None),
                    zone_transition="HIGH->LOW"
                )

                success = send_signal(sell_signal)

                if success:
                    print("[WEBHOOK] Signal delivered")
                else:
                    print("[WEBHOOK] Signal delivery failed")

                telegram_message = format_signal(sell_signal)

                send_telegram(telegram_message)
                print(sell_signal)

            # =========================
            # DEBUG OUTPUT
            # =========================
            TradeTracker.print_trade()

            print("Checked signals...")

        except Exception as e:
            print("Signal Loop Error:", e)

# =========================
# MAIN LOOP
# =========================

print(f'Bot started... {datetime.now().strftime("%H:%M:%S")}')
send_telegram("✅ EMA Signal Bot Online")

async def main():
    TradeLogger.init_file()
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


try:
    asyncio.run(main())

except KeyboardInterrupt:
    print("\nBot stopped manually.")
    send_telegram("Bot stopped manually")