from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum

Base = declarative_base()


class SourceEnum(enum.Enum):
    HNEWS = "HNEWS"
    REDDIT = "REDDIT"


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, index=True, nullable=True)
    title = Column(String, nullable=True)
    text = Column(String, nullable=True)
    author = Column(String, nullable=True)
    upvotes = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    published_date = Column(String, nullable=True)
    comment_url = Column(String, nullable=True)
    comment_html = Column(String, nullable=True)
    source = Column(SQLAlchemyEnum(SourceEnum), nullable=True)
    sub = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f"<Posts(id={self.id}, title='{self.title}', source='{self.source}')>"
