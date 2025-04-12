from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    source = Column(String)
    published_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}')>"
