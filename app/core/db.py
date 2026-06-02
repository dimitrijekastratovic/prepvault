from functools import lru_cache

from sqlmodel import Session, create_engine

from app.core.config import settings


@lru_cache
def get_engine():
    # Built lazily (not at import) so test environments can override get_session
    # without a DATABASE_URL being set. Cached so we reuse a single engine.
    if settings.database_url is None:
        raise ValueError("DATABASE_URL environment variable is not set")
    return create_engine(settings.database_url, echo=settings.database_debug)


def get_session():
    with Session(get_engine()) as session:
        yield session
