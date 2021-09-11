"""Tests for MACDStrategy."""
import pytest


class TestMACDStrategy:
    def test_strategy_attributes(self):
        from user_data.strategies.MACDStrategy import MACDStrategy
        assert MACDStrategy.timeframe == "4h"
        assert MACDStrategy.INTERFACE_VERSION == 3

    def test_populate_indicators_columns(self, sample_ohlcv, meta):
        from user_data.strategies.MACDStrategy import MACDStrategy
        s = MACDStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert "macd" in df.columns
        assert "macd_signal" in df.columns
        assert "macd_hist" in df.columns
        assert "ema200" in df.columns

    def test_entry_signal_columns(self, sample_ohlcv, meta):
        from user_data.strategies.MACDStrategy import MACDStrategy
        s = MACDStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_entry_trend(df, meta)
        assert "enter_long" in df.columns

    def test_ema200_requires_sufficient_data(self, sample_ohlcv, meta):
        from user_data.strategies.MACDStrategy import MACDStrategy
        s = MACDStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        # With 200 bars, EMA200 should have at least some valid values
        assert df["ema200"].notna().sum() > 0
