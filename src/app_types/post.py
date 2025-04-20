from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SourceEnum(str, Enum):
    hnews = "HNEWS"
    reddit = "REDDIT"


class SubEnum(str, Enum):
    reddit_artificialinteligence = "ArtificialInteligence"


class Post(BaseModel):
    source: Optional[SourceEnum]
    sub: Optional[str]
    id: Optional[str]  # Add the Hacker News post ID
    title: Optional[str]
    text: Optional[str]  # HNews text
    author: Optional[str]
    upvotes: Optional[int]
    url: Optional[str]
    published_date: Optional[str]
    comment_url: Optional[str]  # Add the Hacker News comment URL
    comment_html: Optional[str]
