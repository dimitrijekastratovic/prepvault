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