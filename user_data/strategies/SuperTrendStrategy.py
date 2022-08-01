"""SuperTrend ATR-based Trend Following Strategy. Developed 2022, updated 2025."""
import logging
from functools import reduce

import pandas_ta as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy

logger = logging.getLogger(__name__)


class SuperTrendStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "4h"
    can_short = False
    startup_candle_count: int = 50

    minimal_roi = {"0": 0.15, "120": 0.08, "360": 0.04}
    stoploss = -0.08
    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.06
    trailing_only_offset_is_reached = True

    atr_period = IntParameter(7, 20, default=10, space="buy", optimize=True)
    atr_multiplier = DecimalParameter(2.0, 4.0, default=3.0, space="buy", optimize=True)

    def _supertrend(self, dataframe: DataFrame, period: int, multiplier: float) -> DataFrame:
        st = ta.supertrend(dataframe["high"], dataframe["low"], dataframe["close"],
                           length=period, multiplier=multiplier)
        col_dir = f"SUPERTd_{period}_{multiplier}"
        col_val = f"SUPERT_{period}_{multiplier}"
        if col_dir in st.columns:
            dataframe["supertrend_dir"] = st[col_dir]
            dataframe["supertrend_val"] = st[col_val]
        else:
            dataframe["supertrend_dir"] = 1
            dataframe["supertrend_val"] = dataframe["close"]
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self._supertrend(dataframe, self.atr_period.value, float(self.atr_multiplier.value))
        dataframe["st_bull"] = (dataframe["supertrend_dir"] == 1) & (dataframe["supertrend_dir"].shift(1) == -1)
        dataframe["st_bear"] = (dataframe["supertrend_dir"] == -1) & (dataframe["supertrend_dir"].shift(1) == 1)
        dataframe["rsi"] = ta.rsi(dataframe["close"], length=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = [dataframe["st_bull"], dataframe["rsi"] < 65]
        dataframe.loc[reduce(lambda x, y: x & y, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[dataframe["st_bear"], "exit_long"] = 1
        return dataframe
