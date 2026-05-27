from pybit.unified_trading import HTTP
import pandas as pd
import requests
import time
from ta.trend import EMAIndicator
from dotenv import load_dotenv
import os
from datetime import datetime
from Indicator.EMA import EMA
from services.bybit_service import get_data

load_dotenv()
# =========================
# TELEGRAM SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# BYBIT SESSION
# =========================

session = HTTP(testnet=False)

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

# =========================
# GET CANDLE DATA
# =========================

# def get_data():
#     response = session.get_kline(
#         category="linear",
#         symbol="BTCUSDT",
#         interval="5",
#         limit=1000
#     )

#     data = response["result"]["list"]

#     df = pd.DataFrame(data)

#     df.columns = [
#         "timestamp",
#         "open",
#         "high",
#         "low",
#         "close",
#         "volume",
#         "turnover"
#     ]

#     df = df.astype({
#         "open": float,
#         "high": float,
#         "low": float,
#         "close": float,
#         "volume": float
#     })

#     df = df[::-1]

#     return df

# =========================
# SIGNAL DETECTION
# =========================
df = get_data()

signal = EMA.check(df)

if signal:
    send_telegram(signal)
    print(signal)

def wait_for_next_5min():
    now = datetime.now()

    # seconds passed in current 5m block
    seconds_passed = (now.minute % 5) * 60 + now.second

    # seconds until next 5m candle
    sleep_time = 300 - seconds_passed

    print(f"Waiting {sleep_time:.0f}s until next 5m candle...")

    time.sleep(sleep_time)

# =========================
# MAIN LOOP
# =========================

print(f'Bot started... {datetime.now().strftime("%H:%M:%S")}')
send_telegram("✅ EMA Signal Bot Online")

while True:

    wait_for_next_5min()

    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"\nChecking signals at {current_time}")

    try:

        df = get_data()

        signal = EMA.check(df)

        if signal:
            send_telegram(signal)
            print(signal)

    except Exception as e:
        print("Error:", e)


