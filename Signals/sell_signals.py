from Indicator.EMA_TREND import EMA_TREND
from Indicator.RSI_MOMENTUM import RSI_Trend_Continue_signal, RSI_Reversal_Signal
from services.bybit_service import get_data


class SellSignals:

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
        # SELL CONDITIONS ONLY
        # -------------------------

        if rsi_signal == "SELL_CONTINUATION" and trend == "BEARISH":
            return "📉 SELL CONTINUATION SIGNAL"

        return None