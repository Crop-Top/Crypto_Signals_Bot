from datetime import datetime
from Tracker.trade_logger import TradeLogger

class TradeTracker:

    active_trade = None

    @classmethod
    def calculate_mae(cls):
        trade = cls.active_trade
        entry = trade["entry_price"]
        signal = trade["signal"]

        lowest = min(trade["prices"])
        highest = max(trade["prices"])

        # For a BUY, adverse is the lowest price. For a SELL, adverse is the highest price.
        if "BUY" in signal:
            mae = ((lowest - entry) / entry) * 100
        elif "SELL" in signal:
            mae = ((entry - highest) / entry) * 100
        else:
            mae = 0

        trade["lowest_price"] = lowest
        trade["highest_price"] = highest
        return mae

    @classmethod
    def calculate_mfe(cls):
        trade = cls.active_trade
        entry = trade["entry_price"]
        signal = trade["signal"]

        lowest = min(trade["prices"])
        highest = max(trade["prices"])

        # For a BUY, favorable is the highest price. For a SELL, favorable is the lowest price.
        if "BUY" in signal:
            mfe = ((highest - entry) / entry) * 100
        elif "SELL" in signal:
            mfe = ((entry - lowest) / entry) * 100
        else:
            mfe = 0

        trade["highest_price"] = highest
        trade["lowest_price"] = lowest
        return mfe

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
            "entry_price": float(entry_price),
            "entry_time": datetime.now(),

            "trend": trend,
            "rsi": rsi,
            "zone_transition": zone_transition,

            "highest_price": entry_price,
            "lowest_price": entry_price,
            "prices": [entry_price]

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

        cls.active_trade["prices"].append(float(current_price))

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
    def close_trade(cls, current_price):

        cls.active_trade["exit_price"] = current_price
        cls.active_trade["exit_time"] = datetime.now()

        entry = cls.active_trade["entry_price"]
        signal = cls.active_trade["signal"]

        # metrics (These will now use the updated methods above)
        cls.active_trade["mfe"] = cls.calculate_mfe()
        cls.active_trade["mae"] = cls.calculate_mae()

        # 🔥 PnL FIX: Check trade direction 🔥
        if "BUY" in signal:
            cls.active_trade["pnl"] = ((current_price - entry) / entry) * 100
        elif "SELL" in signal:
            cls.active_trade["pnl"] = ((entry - current_price) / entry) * 100
        else:
            cls.active_trade["pnl"] = 0

        cls.active_trade["duration"] = (
            cls.active_trade["exit_time"] - cls.active_trade["entry_time"]
        ).total_seconds() / 60

        # 🚨 THIS IS THE ONLY IMPORTANT ADDITION
        TradeLogger.save_trade(cls.active_trade)

        print("[TRACKER] Trade saved to CSV")

        cls.active_trade = None

    @classmethod
    def save_trade(cls, trade):

        print("\n================ TRADE CLOSED ================")
        print(f"Signal: {trade['signal']}")
        print(f"Entry: {trade['entry_price']}")
        print(f"Exit: {trade['exit_price']}")

        print(f"MFE %: {trade['mfe']}")
        print(f"MAE %: {trade['mae']}")
        print(f"PnL %: {trade['pnl']}")
        print(f"Duration: {trade['duration']}")
        print(f"Trend: {trade['trend']}")
        print(f"RSI: {trade['rsi']}")
        print(f"Zone: {trade['zone_transition']}")
        print("============================================\n")