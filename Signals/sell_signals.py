from Indicator.EMA_TREND import EMA_TREND
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal, RSI_Reversal_Signal
from services.bybit_service import get_data
from ta.momentum import RSIIndicator
from datetime import datetime


class SellSignals:

    @classmethod
    def check(cls, df, trend, rsi_signal):
        price = df["close"].iloc[-1]

        df["rsi"] = RSIIndicator(
            close=df["close"],
            window=14
        ).rsi()

        rsi = df["rsi"].iloc[-2]

        zone = RSI_Trend_Continue_signal.get_zone(rsi)
        # -------------------------
        # SELL CONDITIONS ONLY
        # -------------------------

        if rsi_signal == "SELL_CONTINUATION" and trend == "BEARISH" and zone == "LOW":
            
            return f"""
🔻 SELL CONTINUATION SIGNAL

📉 Trend: Bearish
💰 Symbol: BTCUSDT
💵 Price: ${price:,.2f}

📊 Indicator: RSI Momentum
🔄 Setup: HIGH → LOW Zone
📉 RSI: {rsi:.2f}

⏰ Timeframe: 5m
🕒 Time: {datetime.now().strftime("%H:%M:%S")}
"""

        return None