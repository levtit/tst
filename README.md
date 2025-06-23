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

## Wyckoff Accumulation Detector

The `wyckoff` package provides tools to train a machine learning model that tries
to detect Wyckoff accumulation phases in 5 minute Bitcoin data. Historical data
is pulled from Binance, technical indicators are computed with the `ta`
library and a random forest model is trained. The resulting model and dataset
are stored on disk so training can be resumed.

### Example

```bash
pip install -r requirements.txt
python -m wyckoff.main train --limit 1000
python -m wyckoff.main predict --model wyckoff.pkl --limit 50
```
