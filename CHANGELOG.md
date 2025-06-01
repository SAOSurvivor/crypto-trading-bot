# Changelog

All notable changes are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [2.1.0] - 2026-02-15
### Changed
- Updated all dependencies to latest stable versions
- Python 3.12 as primary supported version
- Minor documentation improvements

## [2.0.0] - 2025-05-01
### Added
- Numpy 2.0 and pandas 2.2 compatibility
- CombinedSignalStrategy hyperopt support
### Changed
- All strategies updated for pandas 2.x API

## [1.5.0] - 2024-04-05
### Added
- Telegram notification configuration
- strategy_selector.py factory module
- STRATEGY environment variable support

## [1.4.0] - 2023-09-10
### Added
- CombinedSignalStrategy (multi-indicator, 4h)
- Hyperopt parameters on all 8 strategies

## [1.3.0] - 2023-03-10
### Changed
- Migrated from ta-lib to pandas-ta
- Fixed pandas 2.0 deprecation warnings (iteritems, append)

## [1.2.0] - 2022-10-15
### Added
- Comprehensive pytest suite (70%+ coverage)
- Pre-commit hooks: black, isort, flake8, bandit
- GitHub Actions CI/CD pipeline

## [1.1.0] - 2022-08-10
### Added
- SuperTrendStrategy (ATR-based, 4h)
- VolumeBreakoutStrategy (1h)
- StochasticRSIStrategy (1h)

## [1.0.0] - 2021-11-10
### Added
- RSIStrategy, EMAStrategy, BollingerBandsStrategy, MACDStrategy
- KuCoin configuration with environment variables
- Docker + docker-compose setup
- Makefile with common commands
