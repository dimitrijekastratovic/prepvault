import os
from sqlmodel import create_engine

DATABASE_URL = os.environ.get("DATABASE_URL", "")
DATABASE_DEBUG = os.environ.get("DATABASE_DEBUG", "").lower() == "true"

if DATABASE_URL == "":
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, echo=DATABASE_DEBUG)