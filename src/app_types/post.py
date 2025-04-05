from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SourceEnum(str, Enum):
    hnews = "HNEWS"
    reddit_python = "REDDIT-PYTHON"


class Post(BaseModel):
    source: Optional[SourceEnum]
    id: Optional[str]  # Add the Hacker News post ID
    title: Optional[str]
    author: Optional[str]
    upvotes: Optional[int]
    url: Optional[str]
    published_date: Optional[str]
    comment_url: Optional[str]  # Add the Hacker News comment URL
