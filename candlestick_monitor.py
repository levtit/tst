import argparse
import matplotlib.pyplot as plt
import mplfinance as mpf

from wyckoff.data import fetch_klines


def fetch_last_30min() -> None:
    """Return last 30 minutes of 1m OHLC data."""
    df = fetch_klines(interval="1m", limit=30)
    df.set_index("open_time", inplace=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Live 30 minute candlestick chart")
    parser.add_argument("--interval", default=10, type=int, help="Refresh interval seconds")
    args = parser.parse_args()

    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()

    while True:
        try:
            df = fetch_last_30min()
        except Exception as exc:
            ax.clear()
            ax.text(0.5, 0.5, f"Error:\n{exc}", ha="center", va="center")
            plt.pause(args.interval)
            continue

        ax.clear()
        mpf.plot(df, type="candle", ax=ax, style="charles")
        ax.set_title("BTC/USDT last 30 minutes")
        plt.pause(args.interval)


if __name__ == "__main__":
    main()
