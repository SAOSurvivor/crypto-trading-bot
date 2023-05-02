"""RSI Mean Reversion Strategy. Developed 2021, updated 2025."""
import logging
from functools import reduce

import pandas_ta as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy

logger = logging.getLogger(__name__)


class RSIStrategy(IStrategy):
    INTERFACE_VERSION = 3  # noqa: E501
    timeframe = "1h"
    can_short = False
    startup_candle_count: int = 50

    minimal_roi = {"0": 0.08, "30": 0.05, "60": 0.03, "120": 0.01}
    stoploss = -0.05
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True

    rsi_buy = IntParameter(20, 40, default=30, space="buy", optimize=True)
    rsi_sell = IntParameter(60, 80, default=70, space="sell", optimize=True)
    rsi_period = IntParameter(10, 20, default=14, space="buy", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["rsi"] = ta.rsi(dataframe["close"], length=self.rsi_period.value)
        dataframe["volume_mean"] = dataframe["volume"].rolling(window=20).mean()
        dataframe["atr"] = ta.atr(dataframe["high"], dataframe["low"], dataframe["close"], length=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [
            dataframe["rsi"] < self.rsi_buy.value,
            dataframe["volume"] > dataframe["volume_mean"] * 0.8,
            dataframe["close"] > dataframe["low"].rolling(window=5).min(),
        ]
        dataframe.loc[reduce(lambda x, y: x & y, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["rsi"] > self.rsi_sell.value, "exit_long"] = 1
        return dataframe
