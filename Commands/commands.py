from telegram.ext import Application, CommandHandler
import asyncio
import os
from Indicator.EMA_TREND import EMA_TREND
from services.bybit_service import get_data
from dotenv import load_dotenv
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal

load_dotenv()

# =========================
# COMMANDS
# =========================
# =========================
# /trend
# =========================
async def trend(update, context):

    df = get_data()

    price = df["close"].iloc[-1]

    trend = EMA_TREND.check(df)

    if trend == "BULLISH":
        emoji = "📈"

    elif trend == "BEARISH":
        emoji = "📉"

    else:
        emoji = "➿"

    trend_signal = f"""
{emoji} MARKET TREND

Trend: {trend}
Price: ${price}
"""

    await update.message.reply_text(trend_signal)

# ====================
# /zone
# ====================    

async def zone(update, context):

    print("🔥 RSI ENGINE RUN - SOURCE: ZONE COMMAND")

    df = get_data()

    # get current trend (optional but useful context)
    trend = EMA_TREND.check(df)

    # run RSI logic WITHOUT triggering signal
    RSI_Trend_Continue_signal.check(df, trend)

    current_zone = RSI_Trend_Continue_signal.current_zone
    previous_zone = RSI_Trend_Continue_signal.previous_zone
    pending_signal = RSI_Trend_Continue_signal.pending_signal
    pending_target_zone = RSI_Trend_Continue_signal.pending_target_zone

    rsi_value = df["close"].iloc[-1]  # we can improve later to real RSI value

    message = f"""
📊 RSI ZONE DEBUG

Trend: {trend}

Previous Zone: {previous_zone}
Current Zone: {current_zone}
Pending Signal: {pending_signal}
Pending Target Zone: {pending_target_zone}

Price: {rsi_value}
"""

    await update.message.reply_text(message)


# DELETE
def print_zone_debug():
    from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal

    print("━━━━━━━━━━━━━━━━━━━━")
    print("📊 ZONE DEBUG")
    print(f"Previous Zone: {RSI_Trend_Continue_signal.previous_zone}")
    print(f"Current Zone:  {RSI_Trend_Continue_signal.current_zone}")
    print(f"Pending Signal:{RSI_Trend_Continue_signal.pending_signal}")
    print(f"Pending Target:{RSI_Trend_Continue_signal.pending_target_zone}")
    print("━━━━━━━━━━━━━━━━━━━━")