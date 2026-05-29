from Indicator.EMA_TREND import EMA_TREND
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal, RSI_Reversal_Signal
from services.bybit_service import get_data


class SellSignals:

    @classmethod
    def check(cls, df, trend, rsi_signal):

        # -------------------------
        # SELL CONDITIONS ONLY
        # -------------------------

        if rsi_signal == "SELL_CONTINUATION" and trend == "BEARISH":
            return "📉 SELL CONTINUATION SIGNAL"

        return None