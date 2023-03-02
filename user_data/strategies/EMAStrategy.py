"""EMA Crossover Strategy (9/21). Developed 2021, updated 2025."""
import logging
from functools import reduce

import pandas_ta as ta
from pandas import DataFrame

from freqtrade.strategy import IntParameter, IStrategy

logger = logging.getLogger(__name__)


class EMAStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "4h"
    can_short = False
    startup_candle_count: int = 60

    minimal_roi = {"0": 0.12, "60": 0.08, "120": 0.04, "240": 0.02}
    stoploss = -0.07
    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    ema_fast = IntParameter(5, 15, default=9, space="buy", optimize=True)
    ema_slow = IntParameter(15, 30, default=21, space="buy", optimize=True)
    ema_trend = IntParameter(40, 100, default=50, space="buy", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema_fast"] = ta.ema(dataframe["close"], length=self.ema_fast.value)
        dataframe["ema_slow"] = ta.ema(dataframe["close"], length=self.ema_slow.value)
        dataframe["ema_trend"] = ta.ema(dataframe["close"], length=self.ema_trend.value)
        dataframe["ema_cross_up"] = (
            (dataframe["ema_fast"] > dataframe["ema_slow"])
            & (dataframe["ema_fast"].shift(1) <= dataframe["ema_slow"].shift(1))
        )
        dataframe["ema_cross_down"] = (
            (dataframe["ema_fast"] < dataframe["ema_slow"])
            & (dataframe["ema_fast"].shift(1) >= dataframe["ema_slow"].shift(1))
        )
        dataframe["volume_sma"] = dataframe["volume"].rolling(window=20).mean()
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [
            dataframe["ema_cross_up"],
            dataframe["close"] > dataframe["ema_trend"],
            dataframe["volume"] > dataframe["volume_sma"],
        ]
        dataframe.loc[reduce(lambda x, y: x & y, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["ema_cross_down"], "exit_long"] = 1
        return dataframe
