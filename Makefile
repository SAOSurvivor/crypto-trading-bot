.PHONY: help install install-dev lint format test test-cov backtest hyperopt \
        docker-build docker-up docker-down docker-logs clean

STRATEGY ?= RSIStrategy
TIMERANGE ?= 20230101-20231231

help:
	@echo "Targets: install install-dev lint format test test-cov backtest hyperopt"
	@echo "         docker-build docker-up docker-down docker-logs clean"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

lint:
	flake8 user_data/strategies/ strategy_selector.py tests/ --max-line-length=100
	bandit -r user_data/strategies/ strategy_selector.py -c pyproject.toml

format:
	black user_data/strategies/ strategy_selector.py tests/
	isort user_data/strategies/ strategy_selector.py tests/

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=user_data/strategies --cov=strategy_selector \
	       --cov-report=term-missing --cov-report=html --cov-fail-under=70

backtest:
	freqtrade backtesting \
	    --config user_data/config.json \
	    --strategy $(STRATEGY) \
	    --timerange $(TIMERANGE) \
	    --timeframe 1h

hyperopt:
	freqtrade hyperopt \
	    --config user_data/config.json \
	    --hyperopt-loss SharpeHyperOptLoss \
	    --strategy $(STRATEGY) \
	    --epochs 100 \
	    --timerange $(TIMERANGE)

download-data:
	freqtrade download-data \
	    --config user_data/config.json \
	    --timerange $(TIMERANGE) \
	    --timeframes 1h 4h

docker-build:
	docker compose build

docker-up:
	STRATEGY=$(STRATEGY) docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f freqtrade

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -f .coverage 2>/dev/null || true
