import pandas as pd
import ta


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute technical indicators and return feature dataframe."""
    out = df.copy()
    out.set_index("open_time", inplace=True)
    out["rsi"] = ta.momentum.rsi(out["close"], window=14)
    out["atr"] = ta.volatility.average_true_range(out["high"], out["low"], out["close"], window=14)
    macd = ta.trend.MACD(out["close"])
    out["macd"] = macd.macd()
    out["macd_signal"] = macd.macd_signal()
    out["macd_diff"] = macd.macd_diff()
    out.dropna(inplace=True)
    return out.reset_index()
