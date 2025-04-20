"""
Script to migrate SQLite database (news.db) to Supabase PostgreSQL.
"""
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import sys

# Add the project root to the Python path so we can import the models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the models from the project
from src.apis.models import Base, Posts, SourceEnum

# Connection string for SQLite (source)
sqlite_conn_str = "sqlite:///news.db"
sqlite_engine = create_engine(sqlite_conn_str)
sqlite_session = sessionmaker(bind=sqlite_engine)()

# Connection string for PostgreSQL (target)
# Note: SQLAlchemy requires "postgresql://" not "postgres://" for the dialect name
# Using URL-encoding for special characters in the password
from urllib.parse import quote_plus
password = input("Enter your Supabase PostgreSQL password: ")
encoded_password = quote_plus(password)
postgres_conn_str = f"postgresql://postgres.yckclwyjevowdcxurdhw:{encoded_password}@aws-0-us-west-1.pooler.supabase.com:5432/postgres"
postgres_engine = None  # Will be initialized after password replacement

def migrate_schema():
    """Create tables in PostgreSQL based on the SQLAlchemy models."""
    print("Creating tables in PostgreSQL...")
    Base.metadata.create_all(postgres_engine)
    print("Schema migration complete.")

def migrate_data():
    """Copy data from SQLite to PostgreSQL."""
    print("Migrating data...")
    # Create a session for PostgreSQL
    postgres_session = sessionmaker(bind=postgres_engine)()
    
    # Get all posts from SQLite
    sqlite_posts = sqlite_session.query(Posts).all()
    print(f"Found {len(sqlite_posts)} posts to migrate.")
    
    # Insert each post into PostgreSQL
    for post in sqlite_posts:
        # Create a new post instance
        new_post = Posts(
            post_id=post.post_id,
            title=post.title,
            text=post.text,
            author=post.author,
            upvotes=post.upvotes,
            url=post.url,
            published_date=post.published_date,
            comment_url=post.comment_url,
            source=post.source,
            sub=post.sub,
            created_at=post.created_at,
            updated_at=post.updated_at
        )
        postgres_session.add(new_post)
    
    # Commit the changes
    postgres_session.commit()
    postgres_session.close()
    print("Data migration complete.")

def verify_migration():
    """Verify that the migration was successful by comparing record counts."""
    sqlite_count = sqlite_session.query(Posts).count()
    
    postgres_session = sessionmaker(bind=postgres_engine)()
    postgres_count = postgres_session.query(Posts).count()
    postgres_session.close()
    
    print(f"SQLite record count: {sqlite_count}")
    print(f"PostgreSQL record count: {postgres_count}")
    
    if sqlite_count == postgres_count:
        print("Migration verification successful! Record counts match.")
    else:
        print("Migration verification failed. Record counts do not match.")

if __name__ == "__main__":
    # Update the connection string with the actual password
    # if "[YOUR-PASSWORD]" in postgres_conn_str:
        # password = input("Enter your Supabase PostgreSQL password: ")
        # postgres_conn_str = postgres_conn_str.replace("[YOUR-PASSWORD]", password)
    postgres_engine = create_engine(postgres_conn_str)
    
    # Execute the migration
    try:
        migrate_schema()
        migrate_data()
        verify_migration()
        print("\nMigration completed successfully!")
    except Exception as e:
        print(f"\nError during migration: {e}")
    finally:
        sqlite_session.close()
