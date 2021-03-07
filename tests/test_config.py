"""Tests for user_data/config.json."""
import json
import os
import pytest


class TestConfig:
    @pytest.fixture
    def config(self):
        with open("user_data/config.json") as f:
            return json.load(f)

    def test_valid_json(self):
        with open("user_data/config.json") as f:
            data = json.load(f)
        assert data is not None

    def test_exchange_is_kucoin(self, config):
        assert config["exchange"]["name"] == "kucoin"

    def test_dry_run_default(self, config):
        assert config["dry_run"] is True

    def test_kucoin_has_password_field(self, config):
        assert "password" in config["exchange"]

    def test_env_var_placeholders(self, config):
        assert "${KUCOIN_API_KEY}" in config["exchange"]["key"]
        assert "${KUCOIN_API_SECRET}" in config["exchange"]["secret"]
        assert "${KUCOIN_API_PASSPHRASE}" in config["exchange"]["password"]

    def test_pair_whitelist_non_empty(self, config):
        assert len(config["exchange"]["pair_whitelist"]) > 0

    def test_kcs_in_blacklist(self, config):
        assert "KCS/USDT" in config["exchange"]["pair_blacklist"]
