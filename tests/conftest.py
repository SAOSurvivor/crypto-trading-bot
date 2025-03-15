"""Shared pytest fixtures for all strategy tests."""
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_ohlcv():
    """200 bars of synthetic OHLCV data (seed=42 for reproducibility)."""
    np.random.seed(42)  # fixed seed
    n = 200
    dates = pd.date_range("2023-01-01", periods=n, freq="1h")
    returns = np.random.normal(0.001, 0.02, n)
    close = 30000 * np.exp(np.cumsum(returns))
    high = close * (1 + np.abs(np.random.normal(0, 0.005, n)))
    low = close * (1 - np.abs(np.random.normal(0, 0.005, n)))
    open_ = close * (1 + np.random.normal(0, 0.002, n))
    volume = np.random.lognormal(10, 1, n)
    df = pd.DataFrame(
        {"date": dates, "open": open_, "high": high, "low": low, "close": close, "volume": volume}
    )
    df.set_index("date", inplace=True)
    return df


@pytest.fixture
def meta():
    return {"pair": "BTC/USDT"}
