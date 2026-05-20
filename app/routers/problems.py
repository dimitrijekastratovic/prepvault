from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models.problem import Problem
from app.models.problem_topics import ProblemTopic
from app.models.topic import Topic

router = APIRouter()

@router.get("/problems")
def get_problems(session: Session = Depends(get_session)):
    problems = session.exec(select(Problem)).all()
    result = []
    for problem in problems:
        problem_topics = session.exec(
            select(Topic)
            .join(ProblemTopic, ProblemTopic.topic_id == Topic.id)
            .where(ProblemTopic.problem_id == problem.id)
            ).all()
        result.append({
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "constraints": problem.constraints,
            "difficulty": problem.difficulty,
            "time_limit": problem.time_limit,
            "memory_limit": problem.memory_limit,
            "topic": [pt.name for pt in problem_topics],
        })
    return {"problems": result}