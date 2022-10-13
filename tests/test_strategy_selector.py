"""Tests for strategy_selector.py."""
import os
import sys
import pytest


class TestStrategySelector:
    def test_default_strategy(self, monkeypatch):
        monkeypatch.delenv("STRATEGY", raising=False)
        from strategy_selector import get_strategy_name
        assert get_strategy_name() == "RSIStrategy"

    def test_valid_strategy_from_env(self, monkeypatch):
        monkeypatch.setenv("STRATEGY", "EMAStrategy")
        from strategy_selector import get_strategy_name
        assert get_strategy_name() == "EMAStrategy"

    def test_invalid_strategy_exits(self, monkeypatch):
        monkeypatch.setenv("STRATEGY", "NonExistentStrategy")
        with pytest.raises(SystemExit):
            from strategy_selector import get_strategy_name
            get_strategy_name()

    def test_all_strategies_available(self):
        from strategy_selector import AVAILABLE_STRATEGIES
        expected = {
            "RSIStrategy", "EMAStrategy", "BollingerBandsStrategy", "MACDStrategy",
            "SuperTrendStrategy", "VolumeBreakoutStrategy",
            "StochasticRSIStrategy", "CombinedSignalStrategy",
        }
        assert expected == set(AVAILABLE_STRATEGIES.keys())
