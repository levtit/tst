import argparse
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

from wyckoff.data import fetch_klines


def fetch_initial(minutes: int) -> pd.DataFrame:
    """Return initial dataframe of given minutes."""
    df = fetch_klines(interval="1m", limit=minutes)
    df.set_index("open_time", inplace=True)
    return df


def update_df(df: pd.DataFrame, max_len: int) -> pd.DataFrame:
    """Fetch latest closed candle and append if new."""
    latest = fetch_klines(interval="1m", limit=2)
    latest.set_index("open_time", inplace=True)
    closed = latest.iloc[-2:-1]
    if closed.index[0] not in df.index:
        df = pd.concat([df, closed])
        df = df.tail(max_len)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Live BTC candlestick chart")
    parser.add_argument("--minutes", type=int, default=60, help="Displayed history length")
    parser.add_argument("--interval", type=int, default=60, help="Refresh interval in seconds")
    args = parser.parse_args()

    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()

    df = fetch_initial(args.minutes)

    while True:
        try:
            df = update_df(df, args.minutes)
            ax.clear()
            mpf.plot(df, type="candle", ax=ax, style="charles")
            ax.set_title("BTC/USDT live")
            plt.pause(args.interval)
        except Exception as exc:
            ax.clear()
            ax.text(0.5, 0.5, f"Error:\n{exc}", ha="center", va="center")
            plt.pause(args.interval)


if __name__ == "__main__":
    main()
