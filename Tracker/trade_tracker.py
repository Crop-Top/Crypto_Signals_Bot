from datetime import datetime


class TradeTracker:

    active_trade = None

    @classmethod
    def open_trade(
        cls,
        signal,
        entry_price,
        trend,
        rsi,
        zone_transition
    ):

        cls.active_trade = {

            "signal": signal,
            "entry_price": entry_price,
            "entry_time": datetime.now(),

            "trend": trend,
            "rsi": rsi,
            "zone_transition": zone_transition,

            "highest_price": entry_price,
            "lowest_price": entry_price

        }

        print(f"[TRACKER] Opened {signal}")

    @classmethod
    def update_trade(cls, current_price):

        if cls.active_trade is None:
            return

        cls.active_trade["highest_price"] = max(
            cls.active_trade["highest_price"],
            current_price
        )

        cls.active_trade["lowest_price"] = min(
            cls.active_trade["lowest_price"],
            current_price
        )

    @classmethod
    def print_trade(cls):

        print("\n===== ACTIVE TRADE =====")

        if cls.active_trade is None:
            print("No Active Trade")
            return

        for key, value in cls.active_trade.items():
            print(f"{key}: {value}")

        print("========================\n")

    @classmethod
    def close_trade(cls, exit_price):

        if cls.active_trade is None:
            return None

        trade = cls.active_trade

        entry = trade["entry_price"]
        high = trade["highest_price"]
        low = trade["lowest_price"]

        direction = trade["signal"]
        entry_time = trade["entry_time"]
        exit_time = datetime.now()

        # -------------------------
        # BUY TRADE LOGIC
        # -------------------------
        if "BUY" in direction:

            mfe = (high - entry) / entry * 100
            mae = (low - entry) / entry * 100
            pnl = (exit_price - entry) / entry * 100

        # -------------------------
        # SELL TRADE LOGIC
        # -------------------------
        else:

            mfe = (entry - low) / entry * 100
            mae = (entry - high) / entry * 100
            pnl = (entry - exit_price) / entry * 100

        duration_minutes = (exit_time - entry_time).total_seconds() / 60

        closed_trade = {
            "signal": direction,
            "entry_price": entry,
            "exit_price": exit_price,
            "entry_time": entry_time,
            "exit_time": exit_time,

            "trend": trade["trend"],
            "rsi": trade["rsi"],
            "zone_transition": trade["zone_transition"],

            "mfe_pct": round(mfe, 2),
            "mae_pct": round(mae, 2),
            "pnl_pct": round(pnl, 2),
            "duration_min": round(duration_minutes, 2)
        }

        # save it before clearing active trade
        cls.save_trade(closed_trade)

        cls.active_trade = None

        print("[TRACKER] Trade closed")

        return closed_trade

    @classmethod
    def save_trade(cls, trade):

        print("\n================ TRADE CLOSED ================")
        print(f"Signal: {trade['signal']}")
        print(f"Entry: {trade['entry_price']}")
        print(f"Exit: {trade['exit_price']}")

        print(f"MFE %: {trade['mfe_pct']}")
        print(f"MAE %: {trade['mae_pct']}")
        print(f"PnL %: {trade['pnl_pct']}")

        print(f"Duration: {trade['duration_min']} min")
        print(f"Trend: {trade['trend']}")
        print(f"RSI: {trade['rsi']}")
        print(f"Zone: {trade['zone_transition']}")
        print("============================================\n")