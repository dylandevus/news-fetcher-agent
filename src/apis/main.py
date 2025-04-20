import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

from .database import get_db, engine
from . import models

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
    comment_html: Optional[str]


@strawberry.type
class Query:
    @strawberry.field
    def posts(self, info, limit: Optional[int] = None) -> List[PostType]:
        """Get all posts from the database, with optional limit parameter"""
        db = next(get_db())
        query = db.query(models.Posts)
        
        # Apply limit if provided
        if limit is not None:
            query = query.limit(limit)
            
        db_posts = query.all()

        # Convert database model to GraphQL type
        result = []
        for post in db_posts:
            result.append(
                PostType(
                    id=post.post_id,
                    title=post.title,
                    text=post.text,
                    author=post.author,
                    upvotes=post.upvotes,
                    url=post.url,
                    published_date=post.published_date,
                    comment_url=post.comment_url,
                    comment_html=post.comment_html,
                    source=post.source.value if post.source else None,
                    sub=post.sub,
                )
            )
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
            comment_html=posts.comment_html,
            source=posts.source.value if posts.source else None,
            sub=posts.sub,
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
