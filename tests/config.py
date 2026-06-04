from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    """Test-only config, read from .env.test (auto-loaded by pytest-dotenv).

    Lives under tests/ rather than app/core/ because it is test scaffolding,
    not application config.
    """

    model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")

    test_database_url: str | None = None
    database_debug: bool = False


settings = TestSettings()
