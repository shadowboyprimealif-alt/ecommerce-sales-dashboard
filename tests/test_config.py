from __future__ import annotations

from src import config


def test_config_values() -> None:
    assert config.APP_NAME
    assert ".csv" in config.SUPPORTED_EXTENSIONS
    assert ".xlsx" in config.SUPPORTED_EXTENSIONS
    assert "order_id" in config.REQUIRED_COLUMNS
    assert config.MAX_UPLOAD_BYTES > 0