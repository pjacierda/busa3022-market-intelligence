"""Part 2 (data curation): calculated metrics on the clean file data/clean/market_daily.csv.

Input is the team's five-column data contract, one row per ASX trading day (Sydney dates):
    date, close, volume, bond10y, bond10y_missing
Plain-language definitions of every metric are in docs/metric_definitions.md and were
written before this code. Each function matches one definition, and tests/test_metrics.py
checks each one against rows worked by hand.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

CONTRACT = ["date", "close", "volume", "bond10y", "bond10y_missing"]

MA_WINDOW = 20          # M1: about one trading month
VOL_WINDOW = 14         # M2: as suggested in the brief
CORR_WINDOW = 30        # M3: 30 trading days
CORR_MIN_PAIRS = 20     # M3 is blank if fewer than 20 days in the window have a real yield
RAG_BASELINE = 252      # about one trading year
RAG_AMBER, RAG_RED = 0.50, 0.80


def load(path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    missing = [c for c in CONTRACT if c not in df.columns]
    if missing:
        raise ValueError(f"clean file breaks the data contract, missing {missing}")
    return prepare(df)


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Sort by date and refuse duplicates, so every window counts trading days in order."""
    df = df.sort_values("date").reset_index(drop=True)
    if df["date"].duplicated().any():
        raise ValueError("duplicate trading dates in the clean file")
    df["bond10y_missing"] = df["bond10y_missing"].astype(bool)
    return df


def add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = prepare(df.copy())

    # Building block: daily % change in the ASX 200 close.
    df["daily_return_pct"] = df["close"].pct_change() * 100

    # M1: close against its 20-trading-day average (includes today, like the chart line).
    df["close_ma20"] = df["close"].rolling(MA_WINDOW, min_periods=MA_WINDOW).mean()
    df["close_vs_ma20_pct"] = (df["close"] / df["close_ma20"] - 1) * 100

    # M2: 14-day volatility = sample standard deviation (ddof=1) of the last 14 daily % returns.
    # Kept as "% a day", not annualised, so a non-technical reader can relate it to daily moves.
    df["volatility_14d"] = df["daily_return_pct"].rolling(VOL_WINDOW, min_periods=VOL_WINDOW).std(ddof=1)

    # M3: 30-day correlation between ASX daily return and the daily change in the 10-year yield.
    # A carried-forward yield is not a real observation: its change would be a fake 0, so any day
    # whose yield (or the day before's) was filled is left out of the pair.
    change = df["bond10y"].diff() * 100                       # basis points
    real = ~df["bond10y_missing"] & ~df["bond10y_missing"].shift(1, fill_value=True)
    df["yield_change_bp"] = change.where(real)
    pair_ok = df["yield_change_bp"].notna() & df["daily_return_pct"].notna()
    df["corr_30d"] = (df["daily_return_pct"].where(pair_ok)
                      .rolling(CORR_WINDOW, min_periods=CORR_MIN_PAIRS)
                      .corr(df["yield_change_bp"].where(pair_ok)))
    df["corr_30d_pairs"] = pair_ok.rolling(CORR_WINDOW, min_periods=1).sum().astype(int)
    return df


def add_rag(df: pd.DataFrame) -> pd.DataFrame:
    """Green below the 50th, Amber 50th to below 80th, Red 80th percentile or above,
    comparing today's M2 with the previous 252 trading days (today not in its own baseline)."""
    df = df.copy()
    df["vol_percentile"] = (df["volatility_14d"]
                            .rolling(RAG_BASELINE + 1, min_periods=RAG_BASELINE + 1)
                            .apply(lambda w: (w[:-1] < w[-1]).mean(), raw=True))
    rag = np.select([df["vol_percentile"] >= RAG_RED, df["vol_percentile"] >= RAG_AMBER],
                    ["Red", "Amber"], default="Green").astype(object)
    rag[df["vol_percentile"].isna().to_numpy()] = "Not enough history"
    df["rag"] = rag
    return df


def build(path_in="data/clean/market_daily.csv", path_out="data/clean/market_metrics.csv") -> pd.DataFrame:
    out = add_rag(add_metrics(load(path_in)))
    out.to_csv(path_out, index=False)
    return out


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    res = build(*args) if args else build()
    print(res.tail(5)[["date", "close", "close_vs_ma20_pct", "volatility_14d", "corr_30d", "corr_30d_pairs", "rag"]])
