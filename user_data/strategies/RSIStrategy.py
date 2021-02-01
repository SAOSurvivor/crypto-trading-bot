# RSIStrategy - initial implementation
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib


class RSIStrategy(IStrategy):
    INTERFACE_VERSION = 2
    timeframe = "1h"
    minimal_roi = {"0": 0.08, "30": 0.04}
    stoploss = -0.10
    trailing_stop = False
    startup_candle_count: int = 20

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["rsi"] = talib.RSI(dataframe["close"], timeperiod=14)
        dataframe["volume_mean"] = dataframe["volume"].rolling(20).mean()
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["rsi"] < 30) & (dataframe["volume"] > dataframe["volume_mean"]),
            "buy",
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(dataframe["rsi"] > 70), "sell"] = 1
        return dataframe
