"""Tests for EMAStrategy."""
import pytest


class TestEMAStrategy:
    def test_strategy_attributes(self):
        from user_data.strategies.EMAStrategy import EMAStrategy
        assert EMAStrategy.timeframe == "4h"
        assert EMAStrategy.INTERFACE_VERSION == 3
        assert EMAStrategy.stoploss < 0

    def test_populate_indicators_columns(self, sample_ohlcv, meta):
        from user_data.strategies.EMAStrategy import EMAStrategy
        s = EMAStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert "ema_fast" in df.columns
        assert "ema_slow" in df.columns
        assert "ema_trend" in df.columns
        assert "ema_cross_up" in df.columns
        assert "ema_cross_down" in df.columns

    def test_entry_signal_columns(self, sample_ohlcv, meta):
        from user_data.strategies.EMAStrategy import EMAStrategy
        s = EMAStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_entry_trend(df, meta)
        assert "enter_long" in df.columns

    def test_exit_signal_columns(self, sample_ohlcv, meta):
        from user_data.strategies.EMAStrategy import EMAStrategy
        s = EMAStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        df = s.populate_exit_trend(df, meta)
        assert "exit_long" in df.columns

    def test_cross_up_is_boolean(self, sample_ohlcv, meta):
        from user_data.strategies.EMAStrategy import EMAStrategy
        s = EMAStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        assert df["ema_cross_up"].dtype == bool

    def test_ema_fast_below_slow_at_death_cross(self, sample_ohlcv, meta):
        from user_data.strategies.EMAStrategy import EMAStrategy
        s = EMAStrategy()
        df = s.populate_indicators(sample_ohlcv.copy(), meta)
        crosses = df[df["ema_cross_down"]]
        if len(crosses) > 0:
            for idx in crosses.index:
                assert df.loc[idx, "ema_fast"] < df.loc[idx, "ema_slow"]
