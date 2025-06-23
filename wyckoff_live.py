import time
import pandas as pd

from btc_price import fetch_coinbase
from wyckoff.data import fetch_klines
from wyckoff.features import compute_features


def detect_wyckoff(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """Return whether Wyckoff conditions are met and the reasons."""
    df = df.copy()
    df["sma_50"] = df["close"].rolling(50).mean()
    latest = df.iloc[-1]

    reasons = []
    cond_price_above_sma = latest["close"] > latest["sma_50"]
    if cond_price_above_sma:
        reasons.append("price above SMA50")
    cond_rsi = latest["rsi"] > 50
    if cond_rsi:
        reasons.append("RSI > 50")
    cond_macd = latest["macd_diff"] > 0
    if cond_macd:
        reasons.append("MACD diff > 0")

    is_detected = cond_price_above_sma and cond_rsi and cond_macd
    return is_detected, reasons


def main() -> None:
    last_time = None
    while True:
        try:
            price = fetch_coinbase()
            df = fetch_klines(interval="1m", limit=200)
            feat = compute_features(df)
            latest_time = feat.iloc[-1]["open_time"]
            if latest_time != last_time:
                detected, reasons = detect_wyckoff(feat)
                if detected:
                    reason_str = ", ".join(reasons)
                    print(
                        f"{latest_time} - BTC price ${price:.2f} - Possible Wyckoff accumulation detected ({reason_str})"
                    )
                else:
                    print(f"{latest_time} - BTC price: ${price:.2f}")
                last_time = latest_time
        except Exception as exc:
            print(f"Error: {exc}")
        time.sleep(60)


if __name__ == "__main__":
    main()
