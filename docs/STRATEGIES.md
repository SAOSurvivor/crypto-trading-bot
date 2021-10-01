# Strategy Documentation

## Overview

This project provides 8 trading strategies for freqtrade on KuCoin.
Strategies are selected via the `STRATEGY` environment variable.

## Strategy Comparison

| Strategy               | TF  | Signals          | Stop  | ROI   |
|------------------------|-----|------------------|-------|-------|
| RSIStrategy            | 1h  | RSI <30 / >70    | -5%   | 8%    |
| EMAStrategy            | 4h  | EMA 9/21 cross   | -7%   | 12%   |
| BollingerBandsStrategy | 1h  