from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.auth.models import User
from app.problems.models import Problem
from app.submissions.exceptions import ProblemNotFound, SubmissionConflict, SubmissionNotFound, SubmissionForbidden
from app.submissions.execution.base import CodeExecutionService
from app.submissions.models import Submission
from app.submissions.schemas import SubmissionCreate, SubmissionRead


def get_existing_submission(user_id: int, idempotency_key: str, session: Session) -> Submission | None:
    return session.exec(
        select(Submission)
        .where(Submission.user_id == user_id)
        .where(Submission.idempotency_key == idempotency_key)
    ).first()

def get_submission_by_id(submission_id: int, user_id: int, session: Session) -> Submission:
    submission = session.get(Submission, submission_id)
    if submission is None:
        raise SubmissionNotFound(submission_id)
    if submission.user_id != user_id:
        raise SubmissionForbidden(submission_id)
    return submission


async def create_submission(user: User,
                            session: Session,
                            payload: SubmissionCreate,
                            execution_service: CodeExecutionService,
                            idempotency_key: str | None) -> tuple[SubmissionRead, bool]:

    if idempotency_key:
        existing_submission = get_existing_submission(user.id, idempotency_key, session)
        if existing_submission:
            return SubmissionRead.model_validate(existing_submission), False

    existing_problem = session.get(Problem, payload.problem_id)
    if not existing_problem:
        raise ProblemNotFound(payload.problem_id)

    submission = Submission(
        problem_id=payload.problem_id,
        code=payload.code,
        language=payload.language,
        user_id=user.id,
        idempotency_key=idempotency_key,
    )

    try:
        session.add(submission)
        session.commit()
        session.refresh(submission)
    except IntegrityError:
        session.rollback()

        existing_submission = get_existing_submission(user.id, idempotency_key, session)
        if existing_submission:
            return SubmissionRead.model_validate(existing_submission), False
        raise SubmissionConflict()

    result = await execution_service.execute(payload.code, payload.language)
    submission.status = result.status
    submission.stdout = result.stdout
    submission.stderr = result.stderr
    submission.compile_output = result.compile_output
    submission.runtime_ms = result.runtime_ms
    submission.memory_kb = result.memory_kb
    submission.judge0_token = result.provider_token
    session.add(submission)
    session.commit()
    session.refresh(submission)

    return SubmissionRead.model_validate(submission), True
