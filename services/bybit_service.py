from pybit.unified_trading import HTTP
import pandas as pd


session = HTTP(testnet=False)


def get_data():

    response = session.get_kline(
        category="linear",
        symbol="BTCUSDT",
        interval="5",
        limit=1000
    )

    data = response["result"]["list"]

    df = pd.DataFrame(data)

    df.columns = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "turnover"
    ]

    df = df.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    })

    df = df[::-1]

    return df