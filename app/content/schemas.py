from sqlmodel import SQLModel


class TopicRead(SQLModel):
    topic: str
    articles: list[str]


class TopicsRead(SQLModel):
    topics: list[TopicRead]


class ArticleRead(SQLModel):
    content: str
