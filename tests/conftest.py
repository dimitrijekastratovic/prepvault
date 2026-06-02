import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from app.core.db import get_session
from app.main import app
from sqlalchemy import event
import os

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "")
DATABASE_DEBUG = os.environ.get("DATABASE_DEBUG", "").lower() == "true"

if TEST_DATABASE_URL == "":
    raise ValueError("TEST_DATABASE_URL environment variable is not set")

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL, echo=DATABASE_DEBUG)
    SQLModel.metadata.create_all(engine)
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

@pytest.fixture
def client(session):
    return TestClient(app)
