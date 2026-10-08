import pytest

from app.config import Settings


def test_settings_read_secret_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SECRET_KEY", "unit-secret-abc")
    monkeypatch.setenv("ENCRYPTION_KEY", "unit-enc-xyz")
    settings = Settings(_env_file=None)
    assert settings.secret_key == "unit-secret-abc"
    assert settings.encryption_key == "unit-enc-xyz"
    assert settings.secret_key != settings.encryption_key


def test_settings_defaults_for_non_secret_vars() -> None:
    settings = Settings(_env_file=None, SECRET_KEY="s", ENCRYPTION_KEY="e")
    assert settings.token_ttl_hours == 12
    assert settings.cookie_secure is False
    assert settings.app_env == "development"
    assert settings.log_level == "INFO"
    assert settings.db_port == 5432
