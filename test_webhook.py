from services.webhook_service import send_signal
from services.bybit_service import get_data

df = get_data()
current_price = df["close"].iloc[-1]

test_signal = {
    "signal": "SELL_CONTINUATION",
    "side": "SELL",
    "symbol": "BTCUSDT",
    "price": float(current_price),
    "trend": "BEARISH",
    "rsi": 65.0,
    "tp": float(current_price * 0.995),
    "sl": float(current_price * 1.003),
    "timeframe": "5m"
}

success = send_signal(test_signal)
print(success)