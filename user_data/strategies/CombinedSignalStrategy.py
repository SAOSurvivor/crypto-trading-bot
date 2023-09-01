"""Multi-Indicator Confirmation Strategy. Developed 2023, updated 2025."""
import logging

import pandas_ta as ta
from pandas import DataFrame

from freqtrade.strategy import IntParameter, IStrategy

logger = logging.getLogger(__name__)


class CombinedSignalStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "4h"
    can_short = False
    startup_candle_count: int = 100

    minimal_roi = {"0": 0.10, "120": 0.06, "240": 0.03}
    stoploss = -0.06
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True

    rsi_threshold = IntParameter(25, 45, default=35, space="buy", optimize=True)
    min_signals = IntParameter(2, 5, default=3, space="buy", optimize=True)
    ema_period = IntParameter(40, 100, default=50, space="buy", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["rsi"] = ta.rsi(dataframe["close"], length=14)
        macd = ta.macd(dataframe["close"], fast=12, slow=26, signal=9)
        dataframe["macd"] = macd["MACD_12_26_9"]
        dataframe["macd_signal_line"] = macd["MACDs_12_26_9"]
        dataframe["macd_hist"] = macd["MACDh_12_26_9"]
        dataframe["ema_trend"] = ta.ema(dataframe["close"], length=self.ema_period.value)
        bb = ta.bbands(dataframe["close"], length=20, std=2.0)
        dataframe["bb_lower"] = bb["BBL_20_2.0"]
        dataframe["bb_upper"] = bb["BBU_20_2.0"]
        srsi = ta.stochrsi(dataframe["close"], length=14)
        dataframe["stochrsi_k"] = srsi["STOCHRSIk_14_14_3_3"]
        dataframe["stochrsi_d"] = srsi["STOCHRSId_14_14_3_3"]
        dataframe["volume_sma"] = dataframe["volume"].rolling(window=20).mean()
        dataframe["s_rsi"] = (dataframe["rsi"] < self.rsi_threshold.value).astype(int)
        dataframe["s_macd"] = (
            (dataframe["macd"] > dataframe["macd_signal_line"]) & (dataframe["macd_hist"] > 0)
        ).astype(int)
        dataframe["s_ema"] = (dataframe["close"] > dataframe["ema_trend"]).astype(int)
        dataframe["s_stochrsi"] = (
            (dataframe["stochrsi_k"] > dataframe["stochrsi_d"]) & (dataframe["stochrsi_k"] < 50)
        ).astype(int)
        dataframe["s_volume"] = (dataframe["volume"] > dataframe["volume_sma"]).astype(int)
        dataframe["signal_count"] = (
            dataframe["s_rsi"] + dataframe["s_macd"] + dataframe["s_ema"]
            + dataframe["s_stochrsi"] + dataframe["s_volume"]
        )
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["signal_count"] >= self.min_signals.value, "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["signal_count"] <= 1, "exit_long"] = 1
        return dataframe
