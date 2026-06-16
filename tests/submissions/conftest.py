import pytest
from fastapi.testclient import TestClient

from app.auth.models import User
from app.auth.service import get_current_user
from app.main import app
from app.submissions.execution.base import CodeExecutionService, ExecutionResult
from app.submissions.execution.judge0 import get_code_execution_service
from app.submissions.models import SubmissionStatus

FAKE_RESULT = ExecutionResult(
    status=SubmissionStatus.accepted,
    stdout="1\n",
    stderr=None,
    compile_output=None,
    runtime_ms=5,
    memory_kb=1024,
    provider_token="fake-token-123",
)


class FakeExecutionService(CodeExecutionService):
    async def execute(self, code: str, language: str) -> ExecutionResult:
        return FAKE_RESULT

@pytest.fixture
def submission_payload(problem_id) -> dict:
    return {
        "problem_id": problem_id,
        "code": "print(1)",
        "language": "python",
    }

@pytest.fixture
def submission_payload2(problem_id) -> dict:
    return {
        "problem_id": problem_id,
        "code": "print(2)",
        "language": "python",
    }

@pytest.fixture
def bad_submission_payload(problem_id) -> dict:
    return {
        "problem_id": problem_id + 1,
        "code": "print(1)",
        "language": "python",
    }

@pytest.fixture
def idempotency_key() -> str:
    return "test-idempotency-key"

@pytest.fixture
def auth_user(session, user_id) -> User:
    return session.get(User, user_id)


@pytest.fixture
def client(session, auth_user):
    app.dependency_overrides[get_current_user] = lambda: auth_user
    app.dependency_overrides[get_code_execution_service] = lambda: FakeExecutionService()
    yield TestClient(app)
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(get_code_execution_service, None)


@pytest.fixture
def unauthenticated_client(session):
    app.dependency_overrides[get_code_execution_service] = lambda: FakeExecutionService()
    yield TestClient(app)
    app.dependency_overrides.pop(get_code_execution_service, None)

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
        idempotency_key=idempotency_key,
    )
    session.add(submission)
    session.commit()
    session.refresh(submission)
    return submission.id