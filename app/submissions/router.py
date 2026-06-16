from fastapi import APIRouter, Depends, HTTPException, Response, status, Header
from sqlmodel import Session
from app.auth.models import User
from app.auth.service import get_current_user
from app.core.db import get_session
from app.submissions.exceptions import SubmissionConflict, ProblemNotFound
from app.submissions.execution.judge0 import get_code_execution_service
from app.submissions.schemas import SubmissionCreate, SubmissionRead
from app.submissions.service import create_submission
from app.submissions.execution.base import CodeExecutionService

router = APIRouter()

@router.post("/submissions", 
             response_model=SubmissionRead,
             status_code=status.HTTP_201_CREATED)
async def submit(payload: SubmissionCreate,
                response: Response,
                current_user: User = Depends(get_current_user),
                session: Session = Depends(get_session),
                execution_service: CodeExecutionService = Depends(get_code_execution_service),
                idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    
    try:
        submission, created = await create_submission(user=current_user, 
                                                      session=session, 
                                                      payload=payload, 
                                                      execution_service=execution_service, 
                                                      idempotency_key=idempotency_key)
    except ProblemNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SubmissionConflict:
        raise HTTPException(status_code=409, detail="Submission with the same idempotency key already exists")
    
    if not created:
        response.status_code = status.HTTP_200_OK
    return submission

