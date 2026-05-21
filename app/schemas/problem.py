from sqlmodel import SQLModel


class ProblemTestCaseRead(SQLModel):
    input: str
    expected_output: str


class ProblemRead(SQLModel):
    id: int
    title: str
    description: str
    constraints: str
    difficulty: str
    time_limit: int
    memory_limit: int
    topics: list[str]
    test_cases: list[ProblemTestCaseRead]
