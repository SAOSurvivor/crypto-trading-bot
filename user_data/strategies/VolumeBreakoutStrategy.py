"""Volume Surge + Price Breakout Strategy. Developed 2022, updated 2025."""
import logging
from functools import reduce

import numpy as np
import pandas_ta as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy

logger = logging.getLogger(__name__)


class VolumeBreakoutStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "1h"
    can_short = False
    startup_candle_count: int = 30

    minimal_roi = {"0": 0.06, "60": 0.04, "120": 0.02}
    stoploss = -0.04
    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True

    volume_mult = DecimalParameter(1.5, 3.0, default=2.0, space="buy", optimize=True)
    breakout_period = IntParameter(10, 30, default=20, space="buy", optimize=True)
    vol_sma_period = IntParameter(15, 30, default=20, space="buy", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["volume_sma"] = dataframe["volume"].rolling(window=self.vol_sma_period.value).mean()
        dataframe["volume_ratio"] = (
            dataframe["volume"] / dataframe["volume_sma"].replace(0, np.nan)
        ).fillna(0)
        dataframe["price_high_n"] = dataframe["high"].shift(1).rolling(window=self.breakout_period.value).max()
        dataframe["rsi"] = ta.rsi(dataframe["close"], length=14)
        dataframe["atr"] = ta.atr(dataframe["high"], dataframe["low"], dataframe["close"], length=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [
            dataframe["volume_ratio"] >= self.volume_mult.value,
            dataframe["close"] > dataframe["price_high_n"],
            dataframe["rsi"].between(40, 65),
        ]
        dataframe.loc[reduce(lambda x, y: x & y, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [
            dataframe["volume"] < dataframe["volume_sma"] * 0.5,
            dataframe["rsi"] > 70,
        ]
        dataframe.loc[reduce(lambda x, y: x | y, conditions), "exit_long"] = 1
        return dataframe
