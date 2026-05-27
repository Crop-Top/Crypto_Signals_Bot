from ta.trend import EMAIndicator
from datetime import datetime


class EMA:

    last_signal = None

    @classmethod
    def check(cls, df):

        df["ema9"] = EMAIndicator(
            close=df["close"],
            window=9
        ).ema_indicator()

        df["ema21"] = EMAIndicator(
            close=df["close"],
            window=21
        ).ema_indicator()

        # closed candles
        previous_ema9 = df["ema9"].iloc[-3]
        previous_ema21 = df["ema21"].iloc[-3]

        current_ema9 = df["ema9"].iloc[-2]
        current_ema21 = df["ema21"].iloc[-2]

        price = df["close"].iloc[-1]

        print(f'9EMA Value: {current_ema9} {datetime.now().strftime("%H:%M:%S")}')
        print(f'21EMA Value: {current_ema21} {datetime.now().strftime("%H:%M:%S")}')

        # BUY
        if previous_ema9 < previous_ema21 and current_ema9 > current_ema21:

            if cls.last_signal != "BUY":

                cls.last_signal = "BUY"

                return f""" Market Swop To Bullish"""

        # SELL
        elif previous_ema9 > previous_ema21 and current_ema9 < current_ema21:

            if cls.last_signal != "SELL":

                cls.last_signal = "SELL"

                return f"""Market Swop To Bearish"""

        return None
    
class MarketTrend:
    last_signal = None

    @classmethod
    def check(cls, df):

        df["ema9"] = EMAIndicator(
            close=df["close"],
            window=9
        ).ema_indicator()

        df["ema21"] = EMAIndicator(
            close=df["close"],
            window=21
        ).ema_indicator()

        # Get Current EMA position
        current_ema9 = df["ema9"].iloc[-2]
        current_ema21 = df["ema21"].iloc[-2]

        price = df["close"].iloc[-1]

        # Market Direction
        if current_ema9 > current_ema21:
            return f"""
                    📈 MARKET TREND

                    Trend: Bullish
                    Price: {price}
                    """

        # Market Direction
        elif current_ema9 < current_ema21:
            return f"""
                    📉 MARKET TREND

                    Trend: Bearish
                    Price: {price}
                    """