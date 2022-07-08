"""Tests for VolumeBreakoutStrategy."""
import pytest


class TestVolumeBreakoutStrategy:
    def test_strategy_attributes(self):
        from user_data.strategies.VolumeBreakoutStrategy import VolumeBreakoutStrategy
        assert VolumeBreakoutStrategy.timeframe == "1h"
        assert VolumeBreakoutStrategy.INTERFACE_VERSION == 3

    def test_populate_indicators_columns(self, sample_ohlcv, meta):
        from user_data.strategies.VolumeBreakoutStrategy import VolumeBreakoutStrategy
        s = VolumeBreakoutStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert "volume_sma" in df.columns
        assert "volume_ratio" in df.columns
        assert "price_high_n" in df.columns
        assert "rsi" in df.columns

    def test_no_division_by_zero(self, sample_ohlcv, meta):
        """Regression: volume_ratio must not be inf when volume_sma is zero."""
        from user_data.strategies.VolumeBreakoutStrategy import VolumeBreakoutStrategy
        s = VolumeBreakoutStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert not df["volume_ratio"].isin([float("inf"), float("-inf")]).any()

    def test_volume_ratio_non_negative(self, sample_ohlcv, meta):
        from user_data.strategies.VolumeBreakoutStrategy import VolumeBreakoutStrategy
        s = VolumeBreakoutStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert (df["volume_ratio"].dropna() >= 0).all()

    def test_entry_exit_columns(self, sample_ohlcv, meta):
        from user_data.strategies.VolumeBreakoutStrategy import VolumeBreakoutStrategy
        s = VolumeBreakoutStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_entry_trend(df, meta)
        df = s.populate_exit_trend(df, meta)
        assert "enter_long" in df.columns
        assert "exit_long" in df.columns
