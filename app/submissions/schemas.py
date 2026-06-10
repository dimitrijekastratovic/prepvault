from sqlmodel import SQLModel
from datetime import datetime

from app.submissions.models import SubmissionStatus

class SubmissionCreate(SQLModel):
    problem_id: int
    code: str
    language: str

class SubmissionRead(SQLModel):
    id: int
    problem_id: int
    code: str
    language: str
    status: SubmissionStatus
    stdout: str | None
    stderr: str | None
    compile_output: str | None
    runtime_ms: int | None
    memory_kb: int | None
    created_at: datetime