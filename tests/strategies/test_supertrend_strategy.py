"""Tests for SuperTrendStrategy."""
import pytest


class TestSuperTrendStrategy:
    def test_strategy_attributes(self):
        from user_data.strategies.SuperTrendStrategy import SuperTrendStrategy
        assert SuperTrendStrategy.timeframe == "4h"
        assert SuperTrendStrategy.INTERFACE_VERSION == 3

    def test_populate_indicators_columns(self, sample_ohlcv, meta):
        from user_data.strategies.SuperTrendStrategy import SuperTrendStrategy
        s = SuperTrendStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert "supertrend_dir" in df.columns
        assert "st_bull" in df.columns
        assert "st_bear" in df.columns
        assert "rsi" in df.columns

    def test_supertrend_direction_binary(self, sample_ohlcv, meta):
        from user_data.strategies.SuperTrendStrategy import SuperTrendStrategy
        s = SuperTrendStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        valid = df["supertrend_dir"].dropna()
        assert valid.isin([1, -1]).all()

    def test_entry_exit_columns(self, sample_ohlcv, meta):
        from user_data.strategies.SuperTrendStrategy import SuperTrendStrategy
        s = SuperTrendStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_entry_trend(df, meta)
        df = s.populate_exit_trend(df, meta)
        assert "enter_long" in df.columns
        assert "exit_long" in df.columns
