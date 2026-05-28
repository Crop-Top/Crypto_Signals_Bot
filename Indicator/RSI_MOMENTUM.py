from ta.momentum import RSIIndicator


class RSI_Trend_Continue_signal:

    # persistent state (remembers last known RSI zone)
    current_zone = None
    previous_zone = None

    # -------------------------
    # ZONE CLASSIFICATION
    # -------------------------
    @classmethod
    def get_zone(cls, rsi):

        if rsi <= 45:
            return "LOW"

        elif rsi >= 55:
            return "HIGH"

        else:
            return "MID"

    # -------------------------
    # INITIAL STATE RECOVERY (COLD START FIX)
    # -------------------------
    @classmethod
    def initialize_zone(cls, df):

        df["rsi"] = RSIIndicator(
            close=df["close"],
            window=14
        ).rsi()

        # scan backwards to find last meaningful zone
        for i in range(-2, -len(df), -1):

            rsi = df["rsi"].iloc[i]
            zone = cls.get_zone(rsi)

            # ignore neutral zone
            if zone != "MID":

                cls.current_zone = zone
                print(f"[INIT] RSI starting zone: {zone}")
                return zone

        # fallback if everything is neutral
        cls.current_zone = "MID"
        return "MID"

    # -------------------------
    # LIVE SIGNAL CHECK
    # -------------------------
    @classmethod
    def check(cls, df, trend):

        df["rsi"] = RSIIndicator(
            close=df["close"],
            window=14
        ).rsi()

        rsi = df["rsi"].iloc[-2]
        new_zone = cls.get_zone(rsi)

        # -------------------------
        # INIT IF FIRST RUN
        # -------------------------
        if cls.current_zone is None:
            cls.initialize_zone(df)
            return None

        old_zone = cls.current_zone

        # update previous FIRST
        cls.previous_zone = old_zone

        # then update current
        cls.current_zone = new_zone

        # -------------------------
        # CONTINUATION SIGNALS
        # -------------------------

        # BULLISH CONTINUATION
        if trend == "BULLISH":

            if old_zone == "LOW" and new_zone == "HIGH":
                return "BUY_CONTINUATION"

        # BEARISH CONTINUATION
        if trend == "BEARISH":

            if old_zone == "HIGH" and new_zone == "LOW":
                return "SELL_CONTINUATION"

        return None


class RSI_Reversal_Signal:

    @classmethod
    def check(cls, df, trend):

        df["rsi"] = RSIIndicator(
            close=df["close"],
            window=14
        ).rsi()

        rsi_prev = df["rsi"].iloc[-3]
        rsi_curr = df["rsi"].iloc[-2]

        # -------------------------
        # BUY REVERSAL
        # -------------------------
        if trend in ["BEARISH", "NEUTRAL"]:

            # cross up 30
            if rsi_prev < 30 and rsi_curr > 30:
                return "BUY_REVERSAL"

        # -------------------------
        # SELL REVERSAL
        # -------------------------
        if trend in ["BULLISH", "NEUTRAL"]:

            # cross down 70
            if rsi_prev > 70 and rsi_curr < 70:
                return "SELL_REVERSAL"

        return None