"""Hand-worked checks for every Part 2 metric. Expected values are worked out in the comments."""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from curation.metrics import add_metrics, add_rag, prepare  # noqa: E402


def frame(close, bond=None, missing=None):
    n = len(close)
    return pd.DataFrame({
        "date": pd.bdate_range("2026-01-05", periods=n),
        "close": close, "volume": 1.0,
        "bond10y": bond if bond is not None else [4.0] * n,
        "bond10y_missing": missing if missing is not None else [False] * n,
    })


def test_daily_return_three_rows_by_hand():
    # 100 -> 102 is +2.000%; 102 -> 99.96 is -2.000%
    out = add_metrics(frame([100.0, 102.0, 99.96]))
    assert math.isnan(out.loc[0, "daily_return_pct"])
    assert out.loc[1, "daily_return_pct"] == pytest.approx(2.0)
    assert out.loc[2, "daily_return_pct"] == pytest.approx(-2.0)


def test_rows_are_sorted_before_returns_are_calculated():
    df = frame([100.0, 102.0, 99.96]).iloc[[2, 0, 1]]        # arrive out of order
    out = add_metrics(df)
    assert out.loc[1, "daily_return_pct"] == pytest.approx(2.0)


def test_duplicate_dates_are_refused():
    df = frame([100.0, 101.0])
    df.loc[1, "date"] = df.loc[0, "date"]
    with pytest.raises(ValueError, match="duplicate"):
        prepare(df)


def test_20_day_average_by_hand():
    # closes 1..21: day 20 average = mean(1..20) = 10.5; day 21 = mean(2..21) = 11.5
    out = add_metrics(frame([float(c) for c in range(1, 22)]))
    assert out["close_ma20"].iloc[:19].isna().all()          # warm-up rows blank, never zero
    assert out.loc[19, "close_ma20"] == 10.5
    assert out.loc[20, "close_ma20"] == 11.5
    assert out.loc[20, "close_vs_ma20_pct"] == pytest.approx((21 / 11.5 - 1) * 100)


def test_14_day_volatility_matches_independent_calculation():
    rng = np.random.default_rng(3)
    close = list(100 * np.cumprod(1 + rng.normal(0, 0.006, 30)))
    out = add_metrics(frame(close))
    r = np.diff(close)[-14:] / np.array(close[-15:-1]) * 100
    assert out["volatility_14d"].iloc[-1] == pytest.approx(r.std(ddof=1))


def test_carried_forward_yields_are_left_out_of_the_correlation():
    # Day 3's yield is a copy of day 2's. Its change (0 bp) and day 4's change are not real.
    out = add_metrics(frame([100.0, 101.0, 100.0, 99.0, 100.0],
                            bond=[4.00, 4.05, 4.05, 4.10, 4.08],
                            missing=[False, False, True, False, False]))
    assert out.loc[1, "yield_change_bp"] == pytest.approx(5.0)
    assert out["yield_change_bp"].iloc[2:4].isna().all()
    assert out.loc[4, "yield_change_bp"] == pytest.approx(-2.0)
    assert out.loc[4, "corr_30d_pairs"] == 2


def test_correlation_is_blank_until_20_real_pairs():
    n = 25
    close = list(100 + np.arange(n) * 0.5)
    bond = list(4 - np.arange(n) * 0.01)
    miss = [False] * n
    for i in range(1, 8):  # 7 filled days; each also voids the next day's change, leaving 10 real pairs
        miss[i * 3] = True
    out = add_metrics(frame(close, bond, miss))
    assert out.loc[24, "corr_30d_pairs"] == 10
    assert math.isnan(out.loc[24, "corr_30d"])


def test_rag_percentile_bands():
    n = 252
    base = list(np.linspace(0.30, 1.30, n))                   # a year of volatility readings
    df = pd.DataFrame({"volatility_14d": base + [0.50, 0.90, 1.20]})
    out = add_rag(df)
    # 0.50 beats 51 of 252 (20%) -> Green; 0.90 beats 151 (60%) -> Amber; 1.20 beats 226 (90%) -> Red
    assert list(out["rag"].iloc[-3:]) == ["Green", "Amber", "Red"]
    assert out["rag"].iloc[n - 1] == "Not enough history"
