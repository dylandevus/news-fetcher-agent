import yaml
import datetime
from typing import Any, List
from ..app_types.post import Post
from ..apis.database import SessionLocal
from ..apis.models import Posts, SourceEnum


def load_yaml_config(filepath: str) -> Any:
    """
    Loads a YAML configuration file.

    Args:
        filepath (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML content.
    """
    with open(filepath, "r") as file:
        return yaml.safe_load(file)


def save_posts_to_database(posts: List[Post]):
    """
    Save a list of Post objects to the database using SQLAlchemy ORM
    """
    db = SessionLocal()
    try:
        # Track statistics
        total_posts = len(posts)
        new_posts = 0
        skipped_posts = 0
        
        # Create Posts models from Post pydantic models
        for post in posts:
            # Check if post with this ID already exists in database
            if post.id:
                existing_post = db.query(Posts).filter(Posts.post_id == post.id).first()
                if existing_post:
                    # Post already exists, skip adding
                    print(f"Skipping ID: {post.id}, Title: {post.title}")
                    skipped_posts += 1
                    continue
            
            # Create a new Posts database model
            source_enum = None
            if post.source:
                # Convert the string source to SourceEnum
                try:
                    source_enum = SourceEnum[post.source.value]
                except (KeyError, AttributeError):
                    # If conversion fails, try direct assignment (in case it's already the right enum)
                    try:
                        source_enum = SourceEnum(post.source)
                    except (ValueError, TypeError):
                        # If all conversions fail, leave as None
                        pass

            db_post = Posts(
                post_id=post.id,
                title=post.title,
                text=post.text,
                author=post.author,
                upvotes=post.upvotes,
                url=post.url,
                published_date=post.published_date,
                comment_url=post.comment_url,
                source=source_enum,
                sub=post.sub,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
            )
            db.add(db_post)
        
        # Commit all posts to the database
        db.commit()
        print(f"Successfully saved {len(posts)} posts to the database")
    except Exception as e:
        db.rollback()
        print(f"Error saving posts to database: {e}")
    finally:
        db.close()
