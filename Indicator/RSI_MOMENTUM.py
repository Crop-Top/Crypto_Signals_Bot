from ta.momentum import RSIIndicator


class RSI_Trend_Continue_signal:

    # -------------------------
    # PERSISTENT STATE
    # -------------------------
    current_zone = None
    previous_zone = None

    pending_signal = None
    pending_target_zone = None

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
    # INITIAL STATE RECOVERY
    # -------------------------
    @classmethod
    def initialize_zone(cls, df):

        df["rsi"] = RSIIndicator(
            close=df["close"],
            window=14
        ).rsi()

        # scan backwards for last REAL zone
        for i in range(-2, -len(df), -1):

            rsi = df["rsi"].iloc[i]
            zone = cls.get_zone(rsi)

            if zone != "MID":

                cls.current_zone = zone
                cls.previous_zone = zone

                print(f"[INIT] RSI starting zone: {zone}")

                return zone

        # fallback
        cls.current_zone = "MID"
        cls.previous_zone = "MID"

        return "MID"

    # -------------------------
    # LIVE SIGNAL CHECK
    # -------------------------
    @classmethod
    def check(cls, df, trend):

        print("🔥 RSI ENGINE RUN - SOURCE: SIGNAL LOOP")

        # -------------------------
        # CALCULATE RSI
        # -------------------------
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

        # -------------------------
        # DEBUG
        # -------------------------
        print("------ RSI CHECK ------")
        print(f"Trend: {trend}")
        print(f"Previous Zone: {cls.previous_zone}")
        print(f"Current Zone: {cls.current_zone}")
        print(f"New Zone: {new_zone}")
        print(f"Pending Signal: {cls.pending_signal}")
        print("-----------------------")

        # =====================================================
        # 1. CONFIRM EXISTING PENDING SIGNALS FIRST
        # =====================================================

        # CONFIRM BUY
        if cls.pending_signal == "BUY_CONTINUATION":

            if trend == "BULLISH" and cls.current_zone == "HIGH":

                cls.pending_signal = None
                cls.pending_target_zone = None

                print("[CONFIRMED] BUY continuation")

                return "BUY_CONTINUATION"


        # CONFIRM SELL
        if cls.pending_signal == "SELL_CONTINUATION":

            if trend == "BEARISH" and cls.current_zone == "LOW":

                cls.pending_signal = None
                cls.pending_target_zone = None

                print("[CONFIRMED] SELL continuation")

                return "SELL_CONTINUATION"

        # =====================================================
        # 2. IGNORE MID ZONES
        # =====================================================

        if new_zone == "MID":
            return None

        # =====================================================
        # 3. IGNORE DUPLICATE ZONES
        # =====================================================

        if new_zone == cls.current_zone:
            return None

        # =====================================================
        # 4. DETECT TRANSITIONS
        # =====================================================

        old_zone = cls.current_zone

        # update state
        cls.previous_zone = old_zone
        cls.current_zone = new_zone

        # -------------------------
        # CREATE BUY SETUP
        # -------------------------
        if old_zone == "LOW" and new_zone == "HIGH":

            cls.pending_signal = "BUY_CONTINUATION"
            cls.pending_target_zone = "HIGH"

            print("[PENDING] BUY setup created")

        # -------------------------
        # CREATE SELL SETUP
        # -------------------------
        if old_zone == "HIGH" and new_zone == "LOW":

            cls.pending_signal = "SELL_CONTINUATION"
            cls.pending_target_zone = "LOW"

            print("[PENDING] SELL setup created")

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