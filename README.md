# BTC Price Printer

This repository contains a small Python script that prints the current Bitcoin price every minute.
The script queries the price from Coinbase and verifies it against Kraken. If the prices differ by
more than 5%, a warning is shown.

## Usage

Install the required dependency and run the script with Python 3:

```bash
pip install requests
python btc_price.py
```
