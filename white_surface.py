import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import requests


def fetch_price() -> float | None:
    """Return the latest BTC price in USDT from Binance."""
    try:
        resp = requests.get(
            "https://api.binance.com/api/v3/ticker/price",
            params={"symbol": "BTCUSDT"},
            timeout=10,
        )
        resp.raise_for_status()
        return float(resp.json()["price"])
    except Exception:
        return None


def fetch_candles() -> pd.DataFrame:
    """Return recent 15m candle data for BTC/USDT from Binance."""
    url = "https://api.binance.com/api/v3/klines"
    resp = requests.get(
        url, params={"symbol": "BTCUSDT", "interval": "15m", "limit": "50"}, timeout=10
    )
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(
        data,
        columns=[
            "Open time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close time",
            "Quote asset volume",
            "Number of trades",
            "Taker buy base",
            "Taker buy quote",
            "Ignore",
        ],
    )
    df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
    df.set_index("Open time", inplace=True)
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = df[col].astype(float)
    return df[["Open", "High", "Low", "Close", "Volume"]]


def main() -> None:
    root = tk.Tk()
    root.title("Jeff")
    root.configure(bg="white")
    root.geometry("400x300")

    price_label = tk.Label(root, text="BTC Price: --", bg="white", font=("Arial", 12))
    price_label.pack(pady=5)

    output = ScrolledText(root, height=10, width=40, state="disabled", bg="white", relief="sunken")
    output.pack(padx=10, pady=10, fill="both", expand=True)

    def show_welcome() -> None:
        output.configure(state="normal")
        output.insert(tk.END, "Welcome to Jeff!\n")
        output.configure(state="disabled")

    tk.Button(root, text="Show Welcome", command=show_welcome).pack(pady=5)

    # Chart window
    chart_win = tk.Toplevel(root)
    chart_win.title("BTC 15m Chart")
    fig, ax = plt.subplots(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=chart_win)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_price() -> None:
        price = fetch_price()
        if price is not None:
            price_label.config(text=f"BTC Price: ${price:,.2f}")
        root.after(15000, update_price)

    def update_chart() -> None:
        try:
            df = fetch_candles()
            ax.clear()
            mpf.plot(df, type="candle", style="charles", ax=ax, volume=False)
            fig.tight_layout()
            canvas.draw()
        finally:
            chart_win.after(60000, update_chart)

    update_price()
    update_chart()

    root.mainloop()


if __name__ == "__main__":
    main()
