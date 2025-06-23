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

## Live Wyckoff Monitor

`wyckoff_live.py` combines the price printer with a simple Wyckoff accumulation detector. It fetches fresh data from Binance, calculates several indicators and prints the current BTC price. When the heuristic conditions indicate a possible Wyckoff accumulation phase, a message is shown.

Run it after installing the requirements:

```bash
pip install -r requirements.txt
python wyckoff_live.py
```

## Interactive Monitor

`monitor_ui.py` displays a simple text-based interface showing the current BTC price and whether the heuristic Wyckoff accumulation detector is triggered. It updates automatically every minute.

Run it with:

```bash
pip install -r requirements.txt
# Windows users also need the optional curses package
pip install windows-curses
python monitor_ui.py
```

On Linux and macOS the built-in `curses` module is used automatically, but
on Windows the `windows-curses` package must be installed separately.
