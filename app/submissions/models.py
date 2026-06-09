from sqlmodel import Index, SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import sqlalchemy as sa


class SubmissionStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    wrong_answer = "wrong_answer"
    runtime_error = "runtime_error"
    compile_error = "compile_error"
    time_limit_exceeded = "time_limit_exceeded"
    memory_limit_exceeded = "memory_limit_exceeded"
    internal_error = "internal_error"

class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    problem_id: int = Field(index=True, foreign_key="problem.id")
    code: str
    language: str
    status: SubmissionStatus = Field(default=SubmissionStatus.pending,
                                     sa_column_kwargs={"server_default": SubmissionStatus.pending.value})
    judge0_token: Optional[str] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    compile_output: Optional[str] = None
    runtime_ms: Optional[int] = None
    memory_kb: Optional[int] = None
    idempotency_key: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        ),
    )

    __table_args__ = (
        Index(
            "ix_submission_user_idempotency",
            "user_id", "idempotency_key",
            unique=True,
            postgresql_where="idempotency_key IS NOT NULL"
        ),
        sa.Index(
            "ix_submission_created_at",
            sa.text("created_at DESC")
        ),
    )