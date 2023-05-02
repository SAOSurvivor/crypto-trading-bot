"""MACD Signal Crossover Strategy. Developed 2021, updated 2025."""
import logging
from functools import reduce

import pandas_ta as ta
from pandas import DataFrame

from freqtrade.strategy import IntParameter, IStrategy

logger = logging.getLogger(__name__)


class MACDStrategy(IStrategy):
    INTERFACE_VERSION = 3  # noqa: E501
    timeframe = "4h"
    can_short = False
    startup_candle_count: int = 100

    minimal_roi = {"0": 0.10, "120": 0.05, "240": 0.02}
    stoploss = -0.06
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True

    macd_fast = IntParameter(8, 20, default=12, space="buy", optimize=True)
    macd_slow = IntParameter(20, 40, default=26, space="buy", optimize=True)
    macd_signal = IntParameter(5, 15, default=9, space="buy", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        f, sl, sg = self.macd_fast.value, self.macd_slow.value, self.macd_signal.value
        macd = ta.macd(dataframe["close"], fast=f, slow=sl, signal=sg)
        dataframe["macd"] = macd[f"MACD_{f}_{sl}_{sg}"]
        dataframe["macd_signal"] = macd[f"MACDs_{f}_{sl}_{sg}"]
        dataframe["macd_hist"] = macd[f"MACDh_{f}_{sl}_{sg}"]
        dataframe["ema200"] = ta.ema(dataframe["close"], length=200)
        dataframe["macd_cross_up"] = (
            (dataframe["macd"] > dataframe["macd_signal"])
            & (dataframe["macd"].shift(1) <= dataframe["macd_signal"].shift(1))
        )
        dataframe["macd_cross_down"] = (
            (dataframe["macd"] < dataframe["macd_signal"])
            & (dataframe["macd"].shift(1) >= dataframe["macd_signal"].shift(1))
        )
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [
            dataframe["macd_cross_up"],
            dataframe["macd_hist"] > 0,
            dataframe["close"] > dataframe["ema200"],
        ]
        dataframe.loc[reduce(lambda x, y: x & y, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["macd_cross_down"], "exit_long"] = 1
        return dataframe
