"""StochasticRSI Crossover Strategy. Developed 2022, updated 2025."""
import logging
from functools import reduce

import pandas_ta as ta
from pandas import DataFrame

from freqtrade.strategy import IntParameter, IStrategy

logger = logging.getLogger(__name__)


class StochasticRSIStrategy(IStrategy):
    INTERFACE_VERSION = 3  # noqa: E501
    timeframe = "1h"
    can_short = False
    startup_candle_count: int = 60

    minimal_roi = {"0": 0.05, "60": 0.03, "120": 0.01}
    stoploss = -0.04
    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True

    period = IntParameter(10, 20, default=14, space="buy", optimize=True)
    smooth_k = IntParameter(2, 5, default=3, space="buy", optimize=True)
    smooth_d = IntParameter(2, 5, default=3, space="buy", optimize=True)
    oversold = IntParameter(10, 30, default=20, space="buy", optimize=True)
    overbought = IntParameter(70, 90, default=80, space="sell", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        p, k, d = self.period.value, self.smooth_k.value, self.smooth_d.value
        srsi = ta.stochrsi(dataframe["close"], length=p, rsi_length=p, k=k, d=d)
        dataframe["stochrsi_k"] = srsi[f"STOCHRSIk_{p}_{p}_{k}_{d}"]
        dataframe["stochrsi_d"] = srsi[f"STOCHRSId_{p}_{p}_{k}_{d}"]
        dataframe["cross_up"] = (
            (dataframe["stochrsi_k"] > dataframe["stochrsi_d"])
            & (dataframe["stochrsi_k"].shift(1) <= dataframe["stochrsi_d"].shift(1))
        )
        dataframe["cross_down"] = (
            (dataframe["stochrsi_k"] < dataframe["stochrsi_d"])
            & (dataframe["stochrsi_k"].shift(1) >= dataframe["stochrsi_d"].shift(1))
        )
        macd = ta.macd(dataframe["close"], fast=12, slow=26, signal=9)
        dataframe["macd_hist"] = macd["MACDh_12_26_9"]
        dataframe["ema50"] = ta.ema(dataframe["close"], length=50)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [
            dataframe["cross_up"],
            dataframe["stochrsi_k"].shift(1) < self.oversold.value,
            dataframe["macd_hist"] > 0,
            dataframe["close"] > dataframe["ema50"],
        ]
        dataframe.loc[reduce(lambda x, y: x & y, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [
            dataframe["cross_down"],
            dataframe["stochrsi_k"].shift(1) > self.overbought.value,
        ]
        dataframe.loc[reduce(lambda x, y: x & y, conditions), "exit_long"] = 1
        return dataframe
