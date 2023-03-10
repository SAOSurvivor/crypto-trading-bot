"""Bollinger Bands Squeeze/Breakout Strategy. Developed 2021, updated 2024."""
import logging
from functools import reduce

import numpy as np
import pandas_ta as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy

logger = logging.getLogger(__name__)


class BollingerBandsStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "1h"
    can_short = False
    startup_candle_count: int = 40

    minimal_roi = {"0": 0.06, "30": 0.04, "90": 0.02}
    stoploss = -0.04
    trailing_stop = False

    bb_period = IntParameter(15, 30, default=20, space="buy", optimize=True)
    bb_stddev = DecimalParameter(1.5, 3.0, default=2.0, space="buy", optimize=True)
    squeeze_threshold = DecimalParameter(0.01, 0.05, default=0.02, space="buy", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        p, s = self.bb_period.value, self.bb_stddev.value
        bb = ta.bbands(dataframe["close"], length=p, std=s)
        dataframe["bb_lower"] = bb[f"BBL_{p}_{s}"]
        dataframe["bb_mid"] = bb[f"BBM_{p}_{s}"]
        dataframe["bb_upper"] = bb[f"BBU_{p}_{s}"]
        dataframe["bb_bandwidth"] = (
            (dataframe["bb_upper"] - dataframe["bb_lower"])
            / dataframe["bb_mid"].replace(0, np.nan)
        ).fillna(0)
        dataframe["bb_squeeze"] = dataframe["bb_bandwidth"] < self.squeeze_threshold.value
        dataframe["post_squeeze"] = dataframe["bb_squeeze"].shift(1) | dataframe["bb_squeeze"].shift(2)
        dataframe["rsi"] = ta.rsi(dataframe["close"], length=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [
            dataframe["close"].shift(1) > dataframe["bb_upper"].shift(1),
            dataframe["post_squeeze"],
            dataframe["rsi"] < 75,
            dataframe["volume"] > dataframe["volume"].rolling(window=20).mean() * 1.2,
        ]
        dataframe.loc[reduce(lambda x, y: x & y, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["close"] < dataframe["bb_mid"], "exit_long"] = 1
        return dataframe
