import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from app.core.db import get_session
from app.main import app
from sqlalchemy import event

from alembic import command
from alembic.config import Config

from tests.config import settings

@pytest.fixture
def client(session):
    return TestClient(app)

@pytest.fixture(scope="session")
def engine():
    if settings.test_database_url is None:
        raise ValueError("TEST_DATABASE_URL environment variable is not set")
    engine = create_engine(settings.test_database_url, echo=settings.database_debug)

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.test_database_url)
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")

    yield engine
    engine.dispose()

@pytest.fixture(scope="session")
def connection(engine):
    with engine.connect() as conn:
        yield conn

@pytest.fixture(scope="function")
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(_session, inner_transaction):
        nonlocal nested
        if inner_transaction.nested and not inner_transaction._parent.nested:
            nested = connection.begin_nested()

    def override():
        yield session

    app.dependency_overrides[get_session] = override
    yield session
    session.close()
    transaction.rollback()
    app.dependency_overrides.pop(get_session, None)

@pytest.fixture
def test_user():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def test_problem():
    return {
        "title": "Test Problem",
        "description": "This is a test problem.",
        "constraints": "1 <= n <= 1000",
        "difficulty": "Easy",
        "time_limit": 1000,
        "memory_limit": 256,
        "topics": ["Array"],
        "test_cases": [{"input": "1\n2 3 4\n5", "expected_output": "0 1"}]
    }

@pytest.fixture
def test_problem2():
    return {
        "title": "Test Problem 2",
        "description": "This is another test problem.",
        "constraints": "1 <= n <= 1000",
        "difficulty": "Medium",
        "time_limit": 2000,
        "memory_limit": 512,
        "topics": ["String"],
        "test_cases": [{"input": "6\n7 8 9\n10", "expected_output": "2 3"}]
    }

@pytest.fixture
def user_id(session, test_user) -> int:
    return add_test_user(
        session,
        first_name=test_user["first_name"],
        last_name=test_user["last_name"],
        email=test_user["email"],
        password_hash=test_user["password"],
    )

@pytest.fixture
def problem_id(session, test_problem) -> int:
    return add_test_problem(
        session,
        title=test_problem["title"],
        description=test_problem["description"],
        constraints=test_problem["constraints"],
        difficulty=test_problem["difficulty"],
        time_limit=test_problem["time_limit"],
        memory_limit=test_problem["memory_limit"],
        topics=test_problem["topics"],
        test_cases=test_problem["test_cases"],
    )

@pytest.fixture
def idempotency_key() -> str:
    return "test-idempotency-key"

@pytest.fixture
def test_submission(user_id, problem_id, idempotency_key):
    return {
        "user_id": user_id,
        "problem_id": problem_id,
        "code": "print('Hello, World!')",
        "language": "python",
        "status": "pending",
        "judge0_token": None,
        "stdout": None,
        "stderr": None,
        "compile_output": None,
        "runtime_ms": None,
        "memory_kb": None,
        "idempotency_key": idempotency_key
    }

def add_test_user(session, first_name: str, last_name: str, email: str, password_hash: str) -> int:
    from app.auth.models import User

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user.id

def add_test_problem(session, title: str, description: str, constraints: str, difficulty: str, time_limit: int, memory_limit: int, topics: list[str], test_cases: list[dict]) -> int:
    from app.problems.models import Problem, Topic, ProblemTopic, ProblemTestCase

    problem = Problem(
        title=title,
        description=description,
        constraints=constraints,
        difficulty=difficulty,
        time_limit=time_limit,
        memory_limit=memory_limit
    )
    session.add(problem)
    session.commit()
    session.refresh(problem)
    for topic_name in topics:
        topic = Topic(name=topic_name)
        session.add(topic)
        session.commit()
        session.refresh(topic)
        problem_topic = ProblemTopic(problem_id=problem.id, topic_id=topic.id)
        session.add(problem_topic)
        session.commit()
        session.refresh(problem_topic)
    for test_case in test_cases:
        problem_test_case = ProblemTestCase(
            problem_id=problem.id,
            input=test_case["input"],
            expected_output=test_case["expected_output"]
        )
        session.add(problem_test_case)
        session.commit()
        session.refresh(problem_test_case)
    return problem.id

def add_test_submission(session, user_id: int, problem_id: int, code: str, language: str, status: str, judge0_token: str | None, stdout: str | None, stderr: str | None, compile_output: str | None, runtime_ms: int | None, memory_kb: int | None, idempotency_key: str | None) -> int:
    from app.submissions.models import Submission

    submission = Submission(
        user_id=user_id,
        problem_id=problem_id,
        code=code,
        language=language,
        status=status,
        judge0_token=judge0_token,
        stdout=stdout,
        stderr=stderr,
        compile_output=compile_output,
        runtime_ms=runtime_ms,
        memory_kb=memory_kb,
        idempotency_key=idempotency_key
    )
    session.add(submission)
    session.commit()
    session.refresh(submission)
    return submission.id
