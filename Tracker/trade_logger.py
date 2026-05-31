import csv
import os


class TradeLogger:

    FILE = "trades.csv"

    @classmethod
    def init_file(cls):

        if not os.path.exists(cls.FILE):
            with open(cls.FILE, mode="w", newline="") as f:
                writer = csv.writer(f)

                writer.writerow([
                    "signal",
                    "entry_price",
                    "exit_price",
                    "entry_time",
                    "exit_time",
                    "trend",
                    "rsi",
                    "zone_transition",
                    "highest_price",
                    "lowest_price",
                    "mfe_pct",
                    "mae_pct",
                    "pnl_pct",
                    "duration_min"
                ])

    @classmethod
    def save_trade(cls, trade):

        cls.init_file()

        with open(cls.FILE, mode="a", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                trade.get("signal"),
                trade.get("entry_price"),
                trade.get("exit_price"),
                trade.get("entry_time"),
                trade.get("exit_time"),
                trade.get("trend"),
                trade.get("rsi"),
                trade.get("zone_transition"),
                trade.get("highest_price"),
                trade.get("lowest_price"),
                trade.get("mfe"),
                trade.get("mae"),
                trade.get("pnl"),
                trade.get("duration")
            ])