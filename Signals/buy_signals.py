from Indicator.EMA_TREND import EMA_TREND
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal, RSI_Reversal_Signal
from services.bybit_service import get_data
from ta.momentum import RSIIndicator
from datetime import datetime
from services.bybit_service import calculate_tp_sl


class BuySignals:

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
        # BUY CONDITIONS ONLY
        # -------------------------

        if rsi_signal == "BUY_CONTINUATION" and trend == "BULLISH":
            tp, sl = calculate_tp_sl(price, "BUY")

            return {
                "signal": "BUY_CONTINUATION",
                "side": "BUY",
                "symbol": "BTCUSDT",
                "price": float(price),
                "tp": tp,
                "sl": sl,
                "rsi": float(rsi),
                "trend": trend,
                "timeframe": "5m",
                "zone_transition": "LOW->HIGH"
            }

 
        return None