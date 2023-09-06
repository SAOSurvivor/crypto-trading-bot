"""Tests for CombinedSignalStrategy."""
import pytest


class TestCombinedSignalStrategy:
    def test_strategy_attributes(self):
        from user_data.strategies.CombinedSignalStrategy import CombinedSignalStrategy
        assert CombinedSignalStrategy.timeframe == "4h"
        assert CombinedSignalStrategy.INTERFACE_VERSION == 3

    def test_populate_indicators_columns(self, sample_ohlcv, meta):
        from user_data.strategies.CombinedSignalStrategy import CombinedSignalStrategy
        s = CombinedSignalStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        for col in ["rsi", "macd", "ema_trend", "signal_count",
                    "s_rsi", "s_macd", "s_ema", "s_stochrsi", "s_volume"]:
            assert col in df.columns

    def test_signal_count_range(self, sample_ohlcv, meta):
        from user_data.strategies.CombinedSignalStrategy import CombinedSignalStrategy
        s = CombinedSignalStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        valid = df["signal_count"].dropna()
        assert (valid >= 0).all()
        assert (valid <= 5).all()

    def test_entry_requires_min_signals(self, sample_ohlcv, meta):
        from user_data.strategies.CombinedSignalStrategy import CombinedSignalStrategy
        s = CombinedSignalStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_entry_trend(df, meta)
        entries = df[df.get("enter_long", 0) == 1]
        if len(entries) > 0:
            assert (entries["signal_count"] >= s.min_signals.value).all()

    def test_entry_exit_columns(self, sample_ohlcv, meta):
        from user_data.strategies.CombinedSignalStrategy import CombinedSignalStrategy
        s = CombinedSignalStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_entry_trend(df, meta)
        df = s.populate_exit_trend(df, meta)
        assert "enter_long" in df.columns
        assert "exit_long" in df.columns
