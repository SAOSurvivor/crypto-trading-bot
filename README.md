# freqtrade-kucoin-bot

KuCoin crypto trading bot using [freqtrade](https://github.com/freqtrade/freqtrade).

## Strategies

- RSIStrategy - RSI mean reversion (1h)
- EMAStrategy - EMA 9/21 crossover (4h)
- BollingerBandsStrategy - BB squeeze breakout (1h)
- MACDStrategy - MACD signal crossover (4h)

## Setup

```bash
cp .env.example .env
# Fill in your KuCoin API credentials
make docker-build
make docker-up
```

## Docker

```bash
docker compose up -d
docker compose logs -f
```
