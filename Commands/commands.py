from telegram.ext import Application, CommandHandler
import asyncio
import os
from Indicator.EMA import MarketTrend
from services.bybit_service import get_data
from dotenv import load_dotenv
load_dotenv()

# =========================
# COMMANDS
# =========================
async def trend(update, context):

    df = get_data()

    trend_signal = MarketTrend.check(df)

    await update.message.reply_text(trend_signal)

# =========================
# MAIN
# =========================
app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

# bind commands
app.add_handler(CommandHandler("trend", trend))

app.run_polling()