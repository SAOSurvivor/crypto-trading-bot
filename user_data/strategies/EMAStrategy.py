# EMAStrategy - EMA 9/21 crossover
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib


class EMAStrategy(IStrategy):
    INTERFACE_VERSION = 2
    timeframe = "4h"
    minimal_roi = {"0": 0.10, "120": 0.05}
    stoploss = -0.07
    trailing_stop = False
    startup_candle_count: int = 30

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema9"] = talib.EMA(dataframe["close"], timeperiod=9)
        dataframe["ema21"] = talib.EMA(dataframe["close"], timeperiod=21)
        dataframe["ema50"] = talib.EMA(dataframe["close"], timeperiod=50)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["ema9"] > dataframe["ema21"])
            & (dataframe["ema9"].shift(1) <= dataframe["ema21"].shift(1))
            & (dataframe["close"] > dataframe["ema50"]),
            "buy",
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["ema9"] < dataframe["ema21"])
            & (dataframe["ema9"].shift(1) >= dataframe["ema21"].shift(1)),
            "sell",
        ] = 1
        return dataframe
