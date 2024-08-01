# Freqtrade KuCoin Trading Strategies

[![CI](https://github.com/user/trade-strats/actions/workflows/ci.yml/badge.svg)](https://github.com/user/trade-strats/actions)
[![Coverage](https://codecov.io/gh/user/trade-strats/branch/main/graph/badge.svg)](https://codecov.io/gh/user/trade-strats)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)

A collection of 8 battle-tested trading strategies for [freqtrade](https://freqtrade.io)
on KuCoin exchange. Actively maintained since 2021.

## Strategies

| Strategy               | Timeframe | Approach             | Best Market  |
|------------------------|-----------|----------------------|--------------|
| RSIStrategy            | 1h        | Mean reversion       | Ranging      |
| EMAStrategy            | 4h        | Trend following      | Trending     |
| BollingerBandsStrategy | 1h        | Squeeze breakout     | Volatile     |
| MACDStrategy           | 4h        | Momentum crossover   | Trending     |
| SuperTrendStrategy     | 4h        | ATR trend following  | Strong trend |
| VolumeBreakoutStrategy | 1h        | Volume + price break | Volatile     |
| StochasticRSIStrategy  | 1h        | StochRSI crossover   | Ranging      |
| CombinedSignalStrategy | 4h        | Multi-confirmation   | All markets  |

## Quick Start

```bash
cp .env.example .env
# Edit .env: fill in KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE
make docker-build
STRATEGY=RSIStrategy make docker-up
```

## Switch Strategy

```bash
export STRATEGY=EMAStrategy
docker compose up -d
```

Options: `RSIStrategy`, `EMAStrategy`, `BollingerBandsStrategy`, `MACDStrategy`,
`SuperTrendStrategy`, `VolumeBreakoutStrategy`, `StochasticRSIStrategy`, `CombinedSignalStrategy`

## Development

```bash
make install-dev    # Install deps + pre-commit hooks
make test-cov       # Tests with coverage (70%+ required)
make lint           # flake8 + bandit
make backtest STRATEGY=EMAStrategy TIMERANGE=20230101-20231231
make hyperopt STRATEGY=RSIStrategy
```

## KuCoin Setup

Requires three credentials (unique to KuCoin):
- `KUCOIN_API_KEY`
- `KUCOIN_API_SECRET`
- `KUCOIN_API_PASSPHRASE`

Set in `.env` file (never committed to git).

## Project Structure

```
user_data/strategies/   8 trading strategy files
user_data/config.json   Bot configuration
tests/                  Pytest suite (70%+ coverage)
.github/workflows/      CI/CD pipelines
docs/                   Documentation
```

See [docs/STRATEGIES.md](docs/STRATEGIES.md) for detailed strategy documentation.
See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.
