# BollingerBandsStrategy - BB mean reversion
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib


class BollingerBandsStrategy(IStrategy):
    INTERFACE_VERSION = 2
    timeframe = "1h"
    minimal_roi = {"0": 0.06, "60": 0.03}
    stoploss = -0.04
    trailing_stop = False
    startup_candle_count: int = 30

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        upper, mid, lower = talib.BBANDS(dataframe["close"], timeperiod=20, nbdevup=2, nbdevdn=2)
        dataframe["bb_upper"] = upper
        dataframe["bb_mid"] = mid
        dataframe["bb_lower"] = lower
        dataframe["rsi"] = talib.RSI(dataframe["close"], timeperiod=14)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["close"] < dataframe["bb_lower"]) & (dataframe["rsi"] < 35),
            "buy",
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(dataframe["close"] > dataframe["bb_upper"]), "sell"] = 1
        return dataframe
