# Contributing

## Development Setup

```bash
git clone <repo>
cd trade-strats
make install-dev
```

This installs all dependencies and pre-commit hooks (black, isort, flake8, bandit).

## Adding a New Strategy

1. Create `user_data/strategies/MyStrategy.py` (implement `IStrategy`)
2. Add to `AVAILABLE_STRATEGIES` in `strategy_selector.py`
3. Add tests in `tests/strategies/test_my_strategy.py`
4. Document in `docs/STRATEGIES.md`
5. Update `CHANGELOG.md`

## Code Standards

- Line length: 100 characters (black + flake8)
- Imports sorted with isort (black profile)
- No security issues (bandit)
- Test coverage: 70%+ (`make test-cov`)

## Commit Convention

```
feat: add new strategy
fix: correct RSI calculation
test: add edge case tests
docs: update strategy docs
chore: upgrade dependencies
style: run black formatter
security: fix bandit finding
refactor: extract indicator helpers
```

## Pull Request Process

1. Branch from `main`: `git checkout -b feature/my-feature`
2. Make changes, run `make lint` and `make test-cov`
3. Commit with conventional commit messages
4. Open PR against `main`
