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
class DetailedPostResponse:
    post: PostType
    surroundingPosts: List[PostType]


@strawberry.type
class Query:
    @strawberry.field
    def posts(self, info, limit: Optional[int] = None, interweave: bool = False) -> List[PostType]:
        """Get all posts from the database, with optional limit parameter
        
        If interweave=True, posts will be returned in an interwoven order from different sources/subs
        based on their upvotes
        """
        db = next(get_db())
        query = db.query(models.Posts)

        # Get all distinct sources and subs
        if interweave:
            distinct_sources_query = db.query(models.Posts.source, models.Posts.sub).distinct().all()
            distinct_sources = [(src.value if src else None, sub) for src, sub in distinct_sources_query]
            
            # Dictionary to store posts by source and sub
            posts_by_category = {}
            
            # Create post buckets by source and sub
            for source, sub in distinct_sources:
                # Skip entries with None values
                if source is None:
                    continue
                
                category_key = f"{source}:{sub}" if sub else source
                # Fetch the top posts for this category, ordered by upvotes
                category_posts = db.query(models.Posts).filter(
                    models.Posts.source == source if source else True,
                    models.Posts.sub == sub if sub else True
                ).order_by(
                    models.Posts.upvotes.desc().nullslast()
                ).all()
                
                if category_posts:
                    posts_by_category[category_key] = category_posts
            
            # Interweave posts from different categories
            result = []
            max_posts_per_category = 0
            if posts_by_category:
                max_posts_per_category = max(len(posts) for posts in posts_by_category.values())
            
            # Round-robin through each category, taking the next highest voted post
            for i in range(max_posts_per_category):
                for category in posts_by_category:
                    category_posts = posts_by_category[category]
                    if i < len(category_posts):
                        post = category_posts[i]
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
            
            # Apply limit if provided
            if limit is not None and len(result) > limit:
                result = result[:limit]
                
            return result
        else:
            # Original behavior
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

    @strawberry.field
    def get_detailed_posts(self, info, id: str, surrounding_ids: List[str]) -> DetailedPostResponse:
        """Get a specific post by id and fetch surrounding posts by their IDs"""
        db = next(get_db())

        # Fetch the main post
        main_post = db.query(models.Posts).filter(models.Posts.post_id == id).first()
        if not main_post:
            raise ValueError("Post not found")
        
        print("id: ", id)
        print("surrounding_ids: ", surrounding_ids)

        # Fetch surrounding posts by their IDs
        surrounding_posts = (
            db.query(models.Posts)
            .filter(models.Posts.post_id.in_(surrounding_ids))
            .all()
        )

        # Convert posts to GraphQL types
        surrounding_posts_data = [
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
            for post in surrounding_posts
        ]

        return DetailedPostResponse(
            post=PostType(
                id=main_post.post_id,
                title=main_post.title,
                text=main_post.text,
                author=main_post.author,
                upvotes=main_post.upvotes,
                url=main_post.url,
                published_date=main_post.published_date,
                comment_url=main_post.comment_url,
                comment_html=main_post.comment_html,
                source=main_post.source.value if main_post.source else None,
                sub=main_post.sub,
            ),
            surroundingPosts=surrounding_posts_data,
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
