# Strategy Documentation

## Overview

This project provides 8 trading strategies for freqtrade on KuCoin.
Strategies are selected via the `STRATEGY` environment variable.

## Strategy Comparison

| Strategy               | TF  | Signals          | Stop  | ROI   |
|------------------------|-----|------------------|-------|-------|
| RSIStrategy            | 1h  | RSI <30 / >70    | -5%   | 8%    |
| EMAStrategy            | 4h  | EMA 9/21 cross   | -7%   | 12%   |
| BollingerBandsStrategy | 1h  | BB squeeze break | -4%   | 6%    |
| MACDStrategy           | 4h  | MACD cross       | -6%   | 10%   |
| SuperTrendStrategy     | 4h  | ST direction flip| -8%   | 15%   |
| VolumeBreakoutStrategy | 1h  | Vol 2x + high    | -4%   | 6%    |
| StochasticRSIStrategy  | 1h  | StochRSI cross   | -4%   | 5%    |
| CombinedSignalStrategy | 4h  | 3-of-5 signals   | -6%   | 10%   |

## Hyperopt

All strategies support hyperopt via `IntParameter` and `DecimalParameter`.

```bash
make hyperopt STRATEGY=RSIStrategy TIMERANGE=20230101-20231231
```

## Backtesting

```bash
make download-data TIMERANGE=20230101-20231231
make backtest STRATEGY=EMAStrategy TIMERANGE=20230101-20231231
```
