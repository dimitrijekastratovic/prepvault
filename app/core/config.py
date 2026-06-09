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

    # judge0_url is optional/lazy for the same reason as database_url: it's
    # overridden per environment and unit tests mock the HTTP layer, so the app
    # must import without it set. The auth token gets a placeholder default (like
    # secret_key) so Settings() instantiates in tests. The real fail-loud check —
    # url is set, token isn't still "change-me" — lives where the Judge0 client is
    # constructed, not here.
    judge0_url: str | None = None
    judge0_auth_token: str = "change-me"


settings = Settings()
