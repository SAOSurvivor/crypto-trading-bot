"""Tests for StochasticRSIStrategy."""
import pytest


class TestStochasticRSIStrategy:
    def test_strategy_attributes(self):
        from user_data.strategies.StochasticRSIStrategy import StochasticRSIStrategy
        assert StochasticRSIStrategy.timeframe == "1h"
        assert StochasticRSIStrategy.INTERFACE_VERSION == 3

    def test_populate_indicators_columns(self, sample_ohlcv, meta):
        from user_data.strategies.StochasticRSIStrategy import StochasticRSIStrategy
        s = StochasticRSIStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert "stochrsi_k" in df.columns
        assert "stochrsi_d" in df.columns
        assert "cross_up" in df.columns
        assert "cross_down" in df.columns
        assert "macd_hist" in df.columns

    def test_entry_exit_columns(self, sample_ohlcv, meta):
        from user_data.strategies.StochasticRSIStrategy import StochasticRSIStrategy
        s = StochasticRSIStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_entry_trend(df, meta)
        df = s.populate_exit_trend(df, meta)
        assert "enter_long" in df.columns
        assert "exit_long" in df.columns
