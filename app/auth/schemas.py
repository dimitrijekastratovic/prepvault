from sqlmodel import SQLModel
from datetime import datetime

class UserLogin(SQLModel):
    email: str
    password: str

class UserCreate(SQLModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime
