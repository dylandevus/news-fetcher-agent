import strawberry
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .database import get_db, engine
from . import models
from src.app_types.post import Post, SourceEnum

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Create a strawberry version of the Post type for GraphQL # TODO: find a way to reuse Post class from app_types
@strawberry.type
class PostType:
    source: Optional[str]
    sub: Optional[str]
    id: Optional[str]
    title: Optional[str]
    text: Optional[str]
    author: Optional[str]
    upvotes: Optional[int]
    url: Optional[str]
    published_date: Optional[str]
    comment_url: Optional[str]

@strawberry.type
class Query:
    @strawberry.field
    def posts(self, info) -> List[PostType]:
        """Get all posts from the database"""
        db = next(get_db())
        db_posts = db.query(models.Posts).all()
        
        # Convert database model to GraphQL type
        result = []
        for post in db_posts:
            result.append(PostType(
                id=post.post_id,
                title=post.title,
                text=post.text,
                author=post.author,
                upvotes=post.upvotes,
                url=post.url,
                published_date=post.published_date,
                comment_url=post.comment_url,
                source=post.source.value if post.source else None,
                sub=post.sub
            ))
        return result
    
    @strawberry.field
    def post(self, info, id: int) -> Optional[PostType]:
        """Get a specific post by id"""
        db = next(get_db())
        posts = db.query(models.Posts).filter(models.Posts.id == id).first()
        if not posts:
            return None
            
        return PostType(
            id=posts.post_id,
            title=posts.title,
            text=posts.text,
            author=posts.author,
            upvotes=posts.upvotes,
            url=posts.url,
            published_date=posts.published_date,
            comment_url=posts.comment_url,
            source=posts.source.value if posts.source else None,
            sub=posts.sub
        )

schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

app.include_router(graphql_app, prefix="/graphql")
