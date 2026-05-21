import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from app.database import get_session
from app.main import app
from app.models.user import User  # noqa: F401
import os

engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(engine)

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(autouse=True)
def reset_db():
    yield
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

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

def add_test_problem(title: str, description: str, constraints: str, difficulty: str, time_limit: int, memory_limit: int, topics: list[str], test_cases: list[dict]) -> int:
    from app.models.problem import Problem
    from app.models.topic import Topic
    from app.models.problem_topics import ProblemTopic
    from app.models.test_case import ProblemTestCase

    with Session(engine) as session:
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
def client():
    return TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
