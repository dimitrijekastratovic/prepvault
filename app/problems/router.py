from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.db import get_session
from app.problems.models import Problem, Topic, ProblemTopic, ProblemTestCase
from app.problems.schemas import ProblemRead

router = APIRouter()

def create_problem_read(problem: Problem, session: Session) -> ProblemRead:
    problem_topics = session.exec(
        select(Topic)
        .join(ProblemTopic, ProblemTopic.topic_id == Topic.id)
        .where(ProblemTopic.problem_id == problem.id)
    ).all()

    problem_test_cases = session.exec(
        select(ProblemTestCase)
        .where(ProblemTestCase.problem_id == problem.id)
    ).all()

    return ProblemRead(
        id=problem.id,
        title=problem.title,
        description=problem.description,
        constraints=problem.constraints,
        difficulty=problem.difficulty,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit,
        topics=[pt.name for pt in problem_topics],
        test_cases=problem_test_cases
    )

@router.get("/problems", 
            response_model=list[ProblemRead],
            status_code=status.HTTP_200_OK)
def get_problems(session: Session = Depends(get_session)):
    problems = session.exec(select(Problem)).all()
    result = []
    for problem in problems:
        problem_read = create_problem_read(problem, session)
        result.append(problem_read)

    return result

@router.get("/problems/{problem_id}", 
            response_model=ProblemRead,
            status_code=status.HTTP_200_OK)
def get_problem(problem_id: int, session: Session = Depends(get_session)):
    problem = session.get(Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    problem_read = create_problem_read(problem, session)
    return problem_read
