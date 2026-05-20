from sqlmodel import SQLModel, Field
from typing import Optional

class ProblemTestCase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    problem_id: int = Field(foreign_key="problem.id")
    input: str
    expected_output: str