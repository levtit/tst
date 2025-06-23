import os
try:
    import curses
except ModuleNotFoundError as exc:
    if os.name == "nt":
        raise ModuleNotFoundError(
            "curses is required. Install it with 'pip install windows-curses' on Windows"
        ) from exc
    raise
import time

from btc_price import fetch_coinbase
from wyckoff.data import fetch_klines
from wyckoff.features import compute_features
from wyckoff_live import detect_wyckoff


def draw_screen(stdscr: curses.window) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    last_time = None
    last_detected = False
    last_reasons: list[str] = []
    while True:
        stdscr.erase()
        try:
            price = fetch_coinbase()
            df = fetch_klines(interval="1m", limit=200)
            feat = compute_features(df)
            latest_time = feat.iloc[-1]["open_time"]
            if latest_time != last_time:
                last_detected, last_reasons = detect_wyckoff(feat)
                last_time = latest_time

            stdscr.addstr(0, 0, "BTC Live Monitor", curses.A_BOLD)
            stdscr.addstr(2, 0, f"Price: ${price:.2f}")
            status = "DETECTED" if last_detected else "None"
            stdscr.addstr(3, 0, f"Wyckoff accumulation: {status}")
            if last_detected:
                stdscr.addstr(4, 0, ", ".join(last_reasons))
            stdscr.addstr(5, 0, f"Last close: {latest_time}")
        except Exception as exc:
            stdscr.addstr(7, 0, f"Error: {exc}")
        stdscr.addstr(9, 0, "Press 'q' to quit. Updates every minute.")
        stdscr.refresh()
        for _ in range(60):
            ch = stdscr.getch()
            if ch == ord('q'):
                return
            time.sleep(1)


def main() -> None:
    curses.wrapper(draw_screen)


if __name__ == "__main__":
    main()
