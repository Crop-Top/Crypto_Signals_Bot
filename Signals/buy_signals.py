from Indicator.EMA_TREND import EMA_TREND
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal, RSI_Reversal_Signal
from services.bybit_service import get_data


class BuySignals:

    @classmethod
    def check(cls, df):

        # -------------------------
        # GET TREND
        # -------------------------
        trend = EMA_TREND.check(df)

        # -------------------------
        # GET RSI SIGNAL
        # -------------------------
        rsi_signal = RSI_Trend_Continue_signal.check(df, trend)

        # -------------------------
        # BUY CONDITIONS ONLY
        # -------------------------

        if rsi_signal == "BUY_CONTINUATION" and trend == "BULLISH":
            return "🚀 BUY CONTINUATION SIGNAL"

        # later you can add reversal logic here
        # if RSIReversal.check(...) == "BUY_REVERSAL": ...

        return None