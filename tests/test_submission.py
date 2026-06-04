import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import insert, select

from app.submissions.models import Submission, SubmissionStatus
from tests.conftest import add_test_submission, add_test_user

def test_add_submission_to_database(session, user_id, problem_id):
    submission_id = add_test_submission(
        session,
        user_id=user_id,
        problem_id=problem_id,
        code="print('Hello, World!')",
        language="python",
        status="pending",
        judge0_token=None,
        stdout=None,
        stderr=None,
        compile_output=None,
        runtime_ms=None,
        memory_kb=None,
        idempotency_key="test-idempotency-key",
    )
    submission = session.exec(select(Submission).where(Submission.id == submission_id)).first()

    assert submission is not None
    assert submission.user_id == user_id
    assert submission.problem_id == problem_id
    assert submission.code == "print('Hello, World!')"
    assert submission.language == "python"
    assert submission.status == "pending"
    assert submission.judge0_token is None
    assert submission.stdout is None
    assert submission.stderr is None
    assert submission.compile_output is None
    assert submission.runtime_ms is None
    assert submission.memory_kb is None
    assert submission.idempotency_key == "test-idempotency-key"
    assert submission.created_at is not None
    assert submission.updated_at is not None

def test_add_submission_returns_default_submission_status_enum(session, user_id, problem_id):
    submission_id = add_test_submission(
        session,
        user_id=user_id,
        problem_id=problem_id,
        code="print('Hello, World!')",
        language="python",
        status="pending",
        judge0_token=None,
        stdout=None,
        stderr=None,
        compile_output=None,
        runtime_ms=None,
        memory_kb=None,
        idempotency_key="test-idempotency-key",
    )
    submission = session.exec(select(Submission).where(Submission.id == submission_id)).first()

    assert submission is not None
    assert submission.status is SubmissionStatus.pending

def test_submission_created_at_and_updated_at_are_set_by_database(session, user_id, problem_id):
    # Raw Core insert bypasses SQLModel's Python default_factory, so the
    # timestamps can only come from the column server_default (now()).
    session.exec(
        insert(Submission).values(
            user_id=user_id,
            problem_id=problem_id,
            code="x",
            language="python",
        )
    )
    session.commit()
    submission = session.exec(select(Submission)).first()

    assert submission is not None
    assert submission.created_at is not None
    assert submission.updated_at is not None

def test_submission_idempotency_key_uniqueness_two_users(session, user_id, problem_id, idempotency_key):
    user2_id = add_test_user(
        session,
        first_name="User2",
        last_name="Test",
        email="user2@test.com",
        password_hash="password2"
    )

    submission_id1 = add_test_submission(
        session,
        user_id=user_id,
        problem_id=problem_id,
        code="print('Hello, World!')",
        language="python",
        status="pending",
        judge0_token=None,
        stdout=None,
        stderr=None,
        compile_output=None,
        runtime_ms=None,
        memory_kb=None,
        idempotency_key=idempotency_key,
    )

    submission_id2 = add_test_submission(
        session,
        user_id=user2_id,
        problem_id=problem_id,
        code="print('Hello, World!')",
        language="python",
        status="pending",
        judge0_token=None,
        stdout=None,
        stderr=None,
        compile_output=None,
        runtime_ms=None,
        memory_kb=None,
        idempotency_key=idempotency_key,  # Same idempotency key but different user
    )

    submission1 = session.exec(select(Submission).where(Submission.id == submission_id1)).first()
    assert submission1 is not None
    assert submission1.idempotency_key == idempotency_key

    submission2 = session.exec(select(Submission).where(Submission.id == submission_id2)).first()
    assert submission2 is not None
    assert submission2.idempotency_key == idempotency_key

def test_submission_idempotency_key_uniqueness_same_user(session, user_id, problem_id, idempotency_key):
    submission_id1 = add_test_submission(
        session,
        user_id=user_id,
        problem_id=problem_id,
        code="print('Hello, World!')",
        language="python",
        status="pending",
        judge0_token=None,
        stdout=None,
        stderr=None,
        compile_output=None,
        runtime_ms=None,
        memory_kb=None,
        idempotency_key=idempotency_key,
    )

    with pytest.raises(IntegrityError):
        add_test_submission(
            session,
            user_id=user_id,
            problem_id=problem_id,
            code="print('Hello, World!')",
            language="python",
            status="pending",
            judge0_token=None,
            stdout=None,
            stderr=None,
            compile_output=None,
            runtime_ms=None,
            memory_kb=None,
            idempotency_key=idempotency_key,  # Same idempotency key and same user - should raise an error
        )

    session.rollback()  # Rollback the failed transaction to clean up the session
    submission1 = session.exec(select(Submission).where(Submission.id == submission_id1)).first()
    assert submission1 is not None
    assert submission1.idempotency_key == idempotency_key