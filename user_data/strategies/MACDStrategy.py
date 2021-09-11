# MACDStrategy - MACD signal crossover
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib


class MACDStrategy(IStrategy):
    INTERFACE_VERSION = 2
    timeframe = "4h"
    minimal_roi = {"0": 0.10, "240": 0.02}
    stoploss = -0.06
    trailing_stop = False
    startup_candle_count: int = 50

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        macd, signal, hist = talib.MACD(dataframe["close"], fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe["macd"] = macd
        dataframe["macd_signal"] = signal
        dataframe["macd_hist"] = hist
        dataframe["ema200"] = talib.EMA(dataframe["close"], timeperiod=200)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["macd"] > dataframe["macd_signal"])
            & (dataframe["macd"].shift(1) <= dataframe["macd_signal"].shift(1))
            & (dataframe["close"] > dataframe["ema200"]),
            "buy",
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["macd"] < dataframe["macd_signal"])
            & (dataframe["macd"].shift(1) >= dataframe["macd_signal"].shift(1)),
            "sell",
        ] = 1
        return dataframe
