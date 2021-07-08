"""Tests for BollingerBandsStrategy."""
import pytest


class TestBollingerBandsStrategy:
    def test_strategy_attributes(self):
        from user_data.strategies.BollingerBandsStrategy import BollingerBandsStrategy
        assert BollingerBandsStrategy.timeframe == "1h"
        assert BollingerBandsStrategy.INTERFACE_VERSION == 3

    def test_populate_indicators_columns(self, sample_ohlcv, meta):
        from user_data.strategies.BollingerBandsStrategy import BollingerBandsStrategy
        s = BollingerBandsStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert "bb_lower" in df.columns
        assert "bb_mid" in df.columns
        assert "bb_upper" in df.columns
        assert "bb_bandwidth" in df.columns
        assert "bb_squeeze" in df.columns

    def test_no_division_by_zero(self, sample_ohlcv, meta):
        """Regression test: bb_bandwidth should never be NaN due to zero division."""
        from user_data.strategies.BollingerBandsStrategy import BollingerBandsStrategy
        s = BollingerBandsStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        import numpy as np
        assert not df["bb_bandwidth"].isin([float("inf"), float("-inf")]).any()

    def test_upper_band_above_lower(self, sample_ohlcv, meta):
        from user_data.strategies.BollingerBandsStrategy import BollingerBandsStrategy
        s = BollingerBandsStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        valid = df.dropna(subset=["bb_upper", "bb_lower"])
        assert (valid["bb_upper"] >= valid["bb_lower"]).all()

    def test_entry_uses_shifted_close(self, sample_ohlcv, meta):
        """Regression: entry should use shift(1) to avoid repainting."""
        from user_data.strategies.BollingerBandsStrategy import BollingerBandsStrategy
        import inspect
        src = inspect.getsource(BollingerBandsStrategy.populate_entry_trend)
        assert "shift(1)" in src
