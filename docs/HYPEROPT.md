# Hyperopt Guide

## Overview

Hyperopt tunes strategy parameters (RSI thresholds, EMA periods, etc.)
to maximize a loss function (e.g., Sharpe ratio).

## Running Hyperopt

```bash
make download-data TIMERANGE=20230101-20231231
make hyperopt STRATEGY=RSIStrategy TIMERANGE=20230101-20231231
```

## Loss Functions

- `SharpeHyperOptLoss` (default) — Sharpe ratio
- `SortinoHyperOptLoss` — Sortino ratio
- `OnlyProfitHyperOptLoss` — Pure profit

## Applying Results

After hyperopt, apply the best parameters:

```bash
freqtrade hyperopt-show --best -n 5
```

Then update the strategy's `IntParameter`/`DecimalParameter` defaults.
