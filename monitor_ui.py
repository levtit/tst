import curses
import time

from btc_price import fetch_coinbase
from wyckoff.data import fetch_klines
from wyckoff.features import compute_features
from wyckoff_live import detect_wyckoff


def draw_screen(stdscr: curses.window) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    while True:
        stdscr.erase()
        try:
            price = fetch_coinbase()
            df = fetch_klines(limit=200)
            feat = compute_features(df)
            wyckoff = detect_wyckoff(feat)
            stdscr.addstr(0, 0, "BTC Live Monitor", curses.A_BOLD)
            stdscr.addstr(2, 0, f"Price: ${price:.2f}")
            status = "DETECTED" if wyckoff else "None"
            stdscr.addstr(3, 0, f"Wyckoff accumulation: {status}")
        except Exception as exc:
            stdscr.addstr(5, 0, f"Error: {exc}")
        stdscr.addstr(7, 0, "Press 'q' to quit. Updates every minute.")
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
