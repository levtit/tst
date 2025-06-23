import requests
import pandas as pd

BINANCE_URL = "https://api.binance.com/api/v3/klines"


def fetch_klines(symbol: str = "BTCUSDT", interval: str = "5m", limit: int = 1000) -> pd.DataFrame:
    """Fetch historical OHLCV data from Binance."""
    resp = requests.get(
        BINANCE_URL,
        params={"symbol": symbol, "interval": interval, "limit": limit},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    cols = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_volume",
        "n_trades",
        "taker_base",
        "taker_quote",
        "ignore",
    ]
    df = pd.DataFrame(data, columns=cols)
    df = df[["open_time", "open", "high", "low", "close", "volume"]]
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df[["open", "high", "low", "close", "volume"]] = df[
        ["open", "high", "low", "close", "volume"]
    ].astype(float)
    return df
