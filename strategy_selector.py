"""Strategy loader - selects strategy from STRATEGY env var."""
import os
import sys

STRATEGIES = [
    "RSIStrategy",
    "EMAStrategy",
    "BollingerBandsStrategy",
    "MACDStrategy",
]


def get_strategy():
    name = os.environ.get("STRATEGY", "RSIStrategy")
    if name not in STRATEGIES:
        print(f"Unknown strategy: {name}. Available: {STRATEGIES}")
        sys.exit(1)
    return name


if __name__ == "__main__":
    print(get_strategy())
