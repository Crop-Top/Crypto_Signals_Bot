from ta.trend import EMAIndicator
from datetime import datetime

# class for EMA indicator for strategy
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

        df["ema50"] = EMAIndicator(
            close=df["close"],
            window=50
        ).ema_indicator()

        # closed candles
        previous_ema9 = df["ema9"].iloc[-3]
        previous_ema21 = df["ema21"].iloc[-3]

        current_ema9 = df["ema9"].iloc[-2]
        current_ema21 = df["ema21"].iloc[-2]
        current_ema50 = df["ema50"].iloc[-2]

        price = df["close"].iloc[-1]

        print(f'9EMA Value: {current_ema9} {datetime.now().strftime("%H:%M:%S")}')
        print(f'21EMA Value: {current_ema21} {datetime.now().strftime("%H:%M:%S")}')
        print(f'50EMA Value: {current_ema50} {datetime.now().strftime("%H:%M:%S")}')

        # BUY
        if previous_ema9 < previous_ema21 and current_ema9 > current_ema21 and price > current_ema50:

            if cls.last_signal != "BUY":

                cls.last_signal = "BUY"

                return f"""🚀 BTCUSDT 5M BUY SIGNAL

                        EMA 9 crossed ABOVE EMA 21
                        Price is above EMA 50

                        Price: {price}"""

        # SELL
        elif previous_ema9 > previous_ema21 and current_ema9 < current_ema21 and price < current_ema50:

            if cls.last_signal != "SELL":

                cls.last_signal = "SELL"

                return f"""🔻 BTCUSDT 5M SELL SIGNAL

                    EMA 9 crossed BELOW EMA 21
                    Price is below EMA 50

                    Price: {price}"""

        return None

# class to check trend of market "/trend"    
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