"""Tests for RSIStrategy."""
import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

# Mock freqtrade if not installed
try:
    from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
except ImportError:
    mock_ft = MagicMock()
    sys.modules.setdefault("freqtrade", mock_ft)
    sys.modules.setdefault("freqtrade.strategy", mock_ft.strategy)
    IStrategy = object
    IntParameter = lambda *a, **kw: MagicMock(value=kw.get("default", a[1]))
    DecimalParameter = lambda *a, **kw: MagicMock(value=kw.get("default", a[1]))


def _get_strategy():
    import importlib, sys
    # Patch freqtrade imports for isolation
    mock = MagicMock()
    mock.strategy.IStrategy = object
    mock.strategy.IntParameter = lambda *a, **kw: MagicMock(value=kw.get("default", a[1] if len(a) > 1 else 14))
    mock.strategy.DecimalParameter = lambda *a, **kw: MagicMock(value=kw.get("default", a[1] if len(a) > 1 else 2.0))
    with patch.dict(sys.modules, {"freqtrade": mock, "freqtrade.strategy": mock.strategy,
                                   "pandas_ta": __import__("pandas_ta") if _has_pandas_ta() else MagicMock()}):
        spec = importlib.util.spec_from_file_location("RSIStrategy", "user_data/strategies/RSIStrategy.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.RSIStrategy()


def _has_pandas_ta():
    try:
        import pandas_ta
        return True
    except ImportError:
        return False


class TestRSIStrategy:
    def test_strategy_attributes(self):
        from user_data.strategies.RSIStrategy import RSIStrategy
        assert RSIStrategy.timeframe == "1h"
        assert RSIStrategy.INTERFACE_VERSION == 3
        assert RSIStrategy.stoploss < 0

    def test_populate_indicators_columns(self, sample_ohlcv, meta):
        from user_data.strategies.RSIStrategy import RSIStrategy
        s = RSIStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert "rsi" in df.columns
        assert "volume_mean" in df.columns
        assert "atr" in df.columns

    def test_rsi_bounds(self, sample_ohlcv, meta):
        from user_data.strategies.RSIStrategy import RSIStrategy
        s = RSIStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        rsi_valid = df["rsi"].dropna()
        assert (rsi_valid >= 0).all()
        assert (rsi_valid <= 100).all()

    def test_entry_signal_columns(self, sample_ohlcv, meta):
        from user_data.strategies.RSIStrategy import RSIStrategy
        s = RSIStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_entry_trend(df, meta)
        assert "enter_long" in df.columns

    def test_exit_signal_columns(self, sample_ohlcv, meta):
        from user_data.strategies.RSIStrategy import RSIStrategy
        s = RSIStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_exit_trend(df, meta)
        assert "exit_long" in df.columns

    def test_minimal_roi_defined(self):
        from user_data.strategies.RSIStrategy import RSIStrategy
        assert isinstance(RSIStrategy.minimal_roi, dict)
        assert len(RSIStrategy.minimal_roi) > 0

    def test_stoploss_negative(self):
        from user_data.strategies.RSIStrategy import RSIStrategy
        assert RSIStrategy.stoploss < 0
