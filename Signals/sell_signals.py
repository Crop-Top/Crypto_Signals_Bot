from Indicator.EMA_TREND import EMA_TREND
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal, RSI_Reversal_Signal
from services.bybit_service import get_data
from ta.momentum import RSIIndicator
from datetime import datetime
from services.bybit_service import calculate_tp_sl


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

        if rsi_signal == "SELL_CONTINUATION" and trend == "BEARISH":
            tp, sl = calculate_tp_sl(price, "SELL")

            return {
                "signal": "SELL_CONTINUATION",
                "side": "SELL",
                "symbol": "BTCUSDT",
                "price": float(price),
                "tp": tp,
                "sl": sl,
                "rsi": float(rsi),
                "trend": trend,
                "timeframe": "5m",
                "zone_transition": "HIGH->LOW"
            }
        return None