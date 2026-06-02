from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .content.router import router as content
from .auth.router import router as auth
from .problems.router import router as problems

from sqlmodel import SQLModel
from .auth.models import User  # noqa: F401
from .problems.models import Problem, Topic, ProblemTopic, ProblemTestCase  # noqa: F401
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO(ticket-3): replace create_all with Alembic `upgrade head`.
    from .core.db import get_engine
    SQLModel.metadata.create_all(get_engine())
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(content)
app.include_router(auth, prefix="/auth")
app.include_router(problems, prefix="/api")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return FileResponse("app/static/landing.html")

@app.get("/study")
def study():
    return FileResponse("app/static/study.html")

@app.get("/login")
def login():
    return FileResponse("app/static/login.html")

@app.get("/register")
def register():
    return FileResponse("app/static/register.html")