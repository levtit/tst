import time
import requests

COINBASE_URL = "https://api.coinbase.com/v2/prices/spot"
KRAKEN_URL = "https://api.kraken.com/0/public/Ticker"


def fetch_coinbase() -> float:
    """Return current BTC price in USD from Coinbase."""
    resp = requests.get(COINBASE_URL, params={"currency": "USD"}, timeout=10)
    resp.raise_for_status()
    return float(resp.json()["data"]["amount"])


def fetch_kraken() -> float:
    """Return current BTC price in USD from Kraken."""
    resp = requests.get(KRAKEN_URL, params={"pair": "BTCUSD"}, timeout=10)
    resp.raise_for_status()
    data = resp.json()["result"]
    pair = next(iter(data))
    return float(data[pair]["c"][0])


def main() -> None:
    """Print BTC price every minute, verifying across two sources."""
    while True:
        try:
            coinbase_price = fetch_coinbase()
            kraken_price = fetch_kraken()
            diff = abs(coinbase_price - kraken_price)
            if diff > coinbase_price * 0.05:
                print(
                    f"Warning: price mismatch! Coinbase ${coinbase_price:.2f} vs Kraken ${kraken_price:.2f}"
                )
            else:
                print(f"BTC price: ${coinbase_price:.2f}")
        except Exception as exc:
            print(f"Error fetching price: {exc}")
        time.sleep(60)


if __name__ == "__main__":
    main()
