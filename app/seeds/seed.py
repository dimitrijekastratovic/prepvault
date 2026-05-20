import json
from sqlmodel import Session, select
from app.database import engine

from app.models.problem import Problem
from app.models.problem_topics import ProblemTopic
from app.models.topic import Topic
from app.models.test_case import ProblemTestCase

path_to_json = "./app/seeds/problems.json"

def seed():
    with open(path_to_json, "r") as f:
        data = json.load(f)

    with Session(engine) as session:
        for problem_data in data:
            problem = Problem(
                title=problem_data["title"],
                description=problem_data["description"],
                constraints=problem_data["constraints"],
                difficulty=problem_data["difficulty"],
                time_limit=problem_data["time_limit"],
                memory_limit=problem_data["memory_limit"]
            )

            existing_problem = session.exec(select(Problem).where(Problem.title == problem.title)).first()
            if not existing_problem:
                session.add(problem)
                session.commit()
                session.refresh(problem)
            else:
                problem = existing_problem

            for topic_name in problem_data["topics"]:
                topic = session.exec(select(Topic).where(Topic.name == topic_name)).first()
                if not topic:
                    topic = Topic(name=topic_name)
                    session.add(topic)
                    session.commit()
                    session.refresh(topic)

                problem_topic = ProblemTopic(problem_id=problem.id, topic_id=topic.id)
                existing_problem_topic = session.exec(
                    select(ProblemTopic)
                    .where(ProblemTopic.problem_id == problem.id)
                    .where(ProblemTopic.topic_id == topic.id)
                ).first()
                if not existing_problem_topic:
                    session.add(problem_topic)
                    session.commit()
                    session.refresh(problem_topic)

            for test_case in problem_data["test_cases"]:
                tc = ProblemTestCase(
                    problem_id=problem.id,
                    input=test_case["input"],
                    expected_output=test_case["expected_output"]
                )

                existing_test_case = session.exec(
                    select(ProblemTestCase)
                    .where(ProblemTestCase.problem_id == problem.id)
                    .where(ProblemTestCase.input == tc.input)
                    .where(ProblemTestCase.expected_output == tc.expected_output)
                ).first()
                if not existing_test_case:
                    session.add(tc)
                    session.commit()
                    session.refresh(tc)

if __name__ == "__main__":
    seed()