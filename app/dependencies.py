from sqlmodel import Session


def get_session():
    # Engine import is deferred to call time so test environments can override
    # this dependency without triggering app.database's import-time validation
    # of DATABASE_URL.
    from app.database import engine

    with Session(engine) as session:
        yield session
