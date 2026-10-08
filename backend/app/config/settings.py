from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str = "turnos"
    db_password: str = ""
    db_name: str = "turnos"
    db_port: int = 5432
    database_url: str = "postgresql://turnos:@db:5432/turnos"

    secret_key: str
    encryption_key: str

    token_ttl_hours: int = 12
    cookie_secure: bool = False
    app_env: str = "development"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=(".env", "../.env"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
