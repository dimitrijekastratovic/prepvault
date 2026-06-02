from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum


class Difficulty(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"


class Problem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, unique=True)
    description: str
    constraints: str
    difficulty: Difficulty
    time_limit: int
    memory_limit: int


class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)


class ProblemTopic(SQLModel, table=True):
    problem_id: int = Field(foreign_key="problem.id", primary_key=True)
    topic_id: int = Field(foreign_key="topic.id", primary_key=True)


class ProblemTestCase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    problem_id: int = Field(foreign_key="problem.id")
    input: str
    expected_output: str
