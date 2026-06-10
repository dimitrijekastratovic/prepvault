from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .content.router import router as content
from .auth.router import router as auth
from .problems.router import router as problems
from .submissions.router import router as submissions

app = FastAPI()
app.include_router(content)
app.include_router(auth, prefix="/auth")
app.include_router(problems, prefix="/api")
app.include_router(submissions, prefix="/api")
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
