from telegram.ext import Application, CommandHandler
import asyncio
import os
from Indicator.EMA_TREND import EMA_TREND
from services.bybit_service import get_data
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
import os

from services.bybit_service import get_data
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal
from Indicator.EMA_TREND import EMA_TREND

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

        trend_signal = f"""
📈 MARKET TREND

Trend: Bullish
Price: ${price}
"""

    elif trend == "BEARISH":

        trend_signal = f"""
📉 MARKET TREND

Trend: Bearish
Price: ${price}
"""

    else:

        trend_signal = f"""
➿ MARKET TREND

Trend: Neutral
Price: ${price}
"""

    await update.message.reply_text(trend_signal)

# ====================
# /zone
# ====================    

async def zone(update, context):

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

# =========================
# MAIN
# =========================
app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

# bind commands
app.add_handler(CommandHandler("trend", trend))
app.add_handler(CommandHandler("zone", zone))

app.run_polling()