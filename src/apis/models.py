from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum

Base = declarative_base()

class SourceEnum(enum.Enum):
    HNEWS = "HNEWS"
    REDDIT = "REDDIT"

class Posts(Base):
    __tablename__ = "news"

    # Auto-incrementing primary key (different from the post_id)
    id = Column(Integer, primary_key=True, index=True)
    
    # Fields from Post model
    post_id = Column(String, index=True, nullable=True)  # Post ID from source
    title = Column(String, nullable=True)
    text = Column(String, nullable=True)  # Same as 'content' in previous model
    author = Column(String, nullable=True)
    upvotes = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    published_date = Column(String, nullable=True)  # Keeping as string for flexibility
    comment_url = Column(String, nullable=True)
    
    # Source tracking
    source = Column(SQLAlchemyEnum(SourceEnum), nullable=True)
    sub = Column(String, nullable=True)  # Subreddit or subcategory
    
    # System fields
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', source='{self.source}')>"
