#!/usr/bin/env python3
"""
Database seed script to clear and re-insert sample post data.
Run this script anytime you want to reset the database to a known state.
"""

import datetime
import sys
import os
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path to make src importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the models and database connection
from src.apis.database import engine


def clear_and_seed_database():
    """Clear all data from the posts table and seed it with sample data."""
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Clear all existing data
        print("Clearing existing data...")
        db.execute(text("DELETE FROM posts"))
        db.commit()
        print("Data cleared successfully.")

        print("Inserting sample data...")
        # Insert using direct SQL to ensure all required fields are properly set
        post_data = [
            {
                "post_id": "hn1",
                "title": "New Developments in AI Research",
                "text": "Researchers at OpenAI have announced a breakthrough in language model training...",
                "author": "AIResearcher",
                "upvotes": 342,
                "url": "https://example.com/ai-research",
                "published_date": "2025-04-01",
                "comment_url": "https://news.ycombinator.com/item?id=12345",
                "source": "HNEWS",
                "sub": None,
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow(),
            },
            {
                "post_id": "hn2",
                "title": "The Future of Quantum Computing",
                "text": "Quantum computing is set to revolutionize computational capabilities...",
                "author": "QuantumPro",
                "upvotes": 221,
                "url": "https://example.com/quantum",
                "published_date": "2025-04-02",
                "comment_url": "https://news.ycombinator.com/item?id=12346",
                "source": "HNEWS",
                "sub": None,
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow(),
            },
            {
                "post_id": "reddit1",
                "title": "Introducing React 19",
                "text": "React 19 comes with exciting new features for better performance and developer experience...",
                "author": "ReactTeam",
                "upvotes": 1520,
                "url": "https://example.com/react-19",
                "published_date": "2025-04-03",
                "comment_url": "https://reddit.com/r/reactjs/comments/123456",
                "source": "REDDIT",
                "sub": "reactjs",
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow(),
            },
            {
                "post_id": "reddit2",
                "title": "Tutorial: Building a News Fetcher with FastAPI and React",
                "text": "Learn how to build a news aggregator application using FastAPI, GraphQL, and React...",
                "author": "WebDevExpert",
                "upvotes": 987,
                "url": "https://example.com/news-fetcher-tutorial",
                "published_date": "2025-04-04",
                "comment_url": "https://reddit.com/r/reactjs/comments/123457",
                "source": "REDDIT",
                "sub": "reactjs",
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow(),
            },
            {
                "post_id": "reddit3",
                "title": "Optimizing Tailwind CSS for Production",
                "text": "Here's how to optimize your Tailwind CSS setup for production, reducing bundle size by up to 90%...",
                "author": "CSSGuru",
                "upvotes": 645,
                "url": "https://example.com/tailwind-optimization",
                "published_date": "2025-04-05",
                "comment_url": "https://reddit.com/r/reactjs/comments/123458",
                "source": "REDDIT",
                "sub": "reactjs",
                "created_at": datetime.datetime.utcnow(),
                "updated_at": datetime.datetime.utcnow(),
            },
        ]

        # Insert each post item using direct SQL
        for item in post_data:
            db.execute(
                text("""
                    INSERT INTO posts (
                        post_id, title, text, author, upvotes, url, 
                        published_date, comment_url, source, sub, created_at, updated_at
                    ) VALUES (
                        :post_id, :title, :text, :author, :upvotes, :url,
                        :published_date, :comment_url, :source, :sub, :created_at, :updated_at
                    )
                """),
                item,
            )

        db.commit()
        print(f"Added {len(post_data)} sample posts successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    clear_and_seed_database()
