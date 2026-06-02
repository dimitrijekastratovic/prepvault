from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Optional so that test runs (which read TEST_DATABASE_URL via conftest and
    # override get_session) don't fail Settings() instantiation at import time.
    # The engine builder in db.py enforces presence at actual use, so production
    # still fails loudly if DATABASE_URL is missing.
    database_url: str | None = None
    database_debug: bool = False

    secret_key: str = "test-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
