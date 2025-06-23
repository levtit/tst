import time
import pandas as pd

from btc_price import fetch_coinbase
from wyckoff.data import fetch_klines
from wyckoff.features import compute_features


def detect_wyckoff(df: pd.DataFrame) -> bool:
    """Simple heuristic to detect possible Wyckoff accumulation phase."""
    df = df.copy()
    df["sma_50"] = df["close"].rolling(50).mean()
    latest = df.iloc[-1]
    cond_price_above_sma = latest["close"] > latest["sma_50"]
    cond_rsi = latest["rsi"] > 50
    cond_macd = latest["macd_diff"] > 0
    return cond_price_above_sma and cond_rsi and cond_macd


def main() -> None:
    while True:
        try:
            price = fetch_coinbase()
            df = fetch_klines(limit=200)
            feat = compute_features(df)
            if detect_wyckoff(feat):
                print(f"BTC price ${price:.2f} - Possible Wyckoff accumulation detected")
            else:
                print(f"BTC price: ${price:.2f}")
        except Exception as exc:
            print(f"Error: {exc}")
        time.sleep(300)


if __name__ == "__main__":
    main()
