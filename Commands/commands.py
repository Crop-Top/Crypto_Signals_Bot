from telegram.ext import Application, CommandHandler
import asyncio
import os
from Indicator.EMA import EMA
from services.bybit_service import get_data
from dotenv import load_dotenv
load_dotenv()

# =========================
# COMMANDS
# =========================
async def trend(update, context):

    df = get_data()

    price = df["close"].iloc[-1]

    trend = EMA.check(df)

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

# =========================
# MAIN
# =========================
app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

# bind commands
app.add_handler(CommandHandler("trend", trend))

app.run_polling()