"""
Strategy Selector - dynamically loads a strategy based on STRATEGY env var.

Supported strategies:
  RSIStrategy, EMAStrategy, BollingerBandsStrategy, MACDStrategy,
  SuperTrendStrategy, VolumeBreakoutStrategy, StochasticRSIStrategy,
  CombinedSignalStrategy

Usage:
    export STRATEGY=EMAStrategy
    freqtrade trade --strategy $(python strategy_selector.py)
"""
import importlib
import logging
import os
import sys

logger = logging.getLogger(__name__)

AVAILABLE_STRATEGIES = {
    "RSIStrategy": "user_data.strategies.RSIStrategy",
    "EMAStrategy": "user_data.strategies.EMAStrategy",
    "BollingerBandsStrategy": "user_data.strategies.BollingerBandsStrategy",
    "MACDStrategy": "user_data.strategies.MACDStrategy",
    "SuperTrendStrategy": "user_data.strategies.SuperTrendStrategy",
    "VolumeBreakoutStrategy": "user_data.strategies.VolumeBreakoutStrategy",
    "StochasticRSIStrategy": "user_data.strategies.StochasticRSIStrategy",
    "CombinedSignalStrategy": "user_data.strategies.CombinedSignalStrategy",
}


def get_strategy_name() -> str:
    name = os.environ.get("STRATEGY", "RSIStrategy")
    if name not in AVAILABLE_STRATEGIES:
        logger.error(f"Unknown strategy '{name}'. Available: {list(AVAILABLE_STRATEGIES)}")
        sys.exit(1)
    return name


def load_strategy_class(name: str):
    module_path = AVAILABLE_STRATEGIES[name]
    module_name, class_name = module_path.rsplit(".", 1)
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        logger.error(f"Failed to load strategy '{name}': {e}")
        raise


if __name__ == "__main__":
    print(get_strategy_name())
