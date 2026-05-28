from ta.trend import EMAIndicator
from datetime import datetime

# class for EMA indicator for strategy
class EMA:

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

        current_ema9 = df["ema9"].iloc[-2]
        current_ema21 = df["ema21"].iloc[-2]
        current_ema50 = df["ema50"].iloc[-2]

        price_closed = df["close"].iloc[-2]

        print(f'9EMA Value: {current_ema9} {datetime.now().strftime("%H:%M:%S")}')
        print(f'21EMA Value: {current_ema21} {datetime.now().strftime("%H:%M:%S")}')
        print(f'50EMA Value: {current_ema50} {datetime.now().strftime("%H:%M:%S")}')

        # Market Direction
        if current_ema9 > current_ema21 and price_closed > current_ema50:
            return "BULLISH"

        # Market Direction
        elif current_ema9 < current_ema21 and price_closed < current_ema50:
            return "BEARISH"
        
        else:
            return "NEUTRAL"