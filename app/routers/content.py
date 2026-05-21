from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.schemas.content import TopicRead, TopicsRead, ArticleRead

router = APIRouter()
CONTENT_DIR = Path(__file__).parent.parent.parent / "content"
TOPIC_ORDER = ["data-structures", "algorithms", "system-design"]
ARTICLE_ORDER = {
    "data-structures": [
        "arrays", "stacks", "queues", "linked-lists", "hash-maps",
        "trees", "heaps", "graphs", "tries",
    ],
    "algorithms": [
        "binary-search", "two-pointers", "sliding-window", "recursion",
        "divide-and-conquer", "sorting-algorithms", "breadth-first-search",
        "depth-first-search", "backtracking", "greedy-algorithms",
        "monotonic-stack", "union-find", "dijkstra", "dynamic-programming",
    ],
    "system-design": ["scalability"],
}

@router.get("/topics", response_model=TopicsRead)
def get_topics():
    topics_read = TopicsRead(topics=[])
    for topic in TOPIC_ORDER:
        topic_dir = CONTENT_DIR / topic

        if not topic_dir.is_dir():
            continue

        existing = {f.stem for f in topic_dir.iterdir() if f.is_file() and f.suffix == ".md"}
        articles = [a for a in ARTICLE_ORDER.get(topic, []) if a in existing]

        topic_read = TopicRead(topic=topic, articles=articles)
        topics_read.topics.append(topic_read)
    return topics_read

@router.get("/topics/{topic}/{article}", response_model=ArticleRead)
def get_article(topic: str, article: str):
    article_path = CONTENT_DIR / topic / f"{article}.md"

    if not article_path.exists():
        raise HTTPException(status_code=404, detail="Article not found")
    
    content = article_path.read_text(encoding="utf-8")
    article = ArticleRead(content=content)
    return article