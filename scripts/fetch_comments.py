#!/usr/bin/env python3
"""
Script to fetch comments for recent posts in the database.
This script will:
1. Get the 20 most recent posts from the database
2. For each post, check if comment_url is empty or comment_html is empty
3. If comment_url is empty, try to construct it from post data
4. Call scrape_comments_with_playwright to fetch comments
5. Update the database with the fetched comments

Usage:
    python -m scripts.fetch_comments
"""

import requests
import asyncio
import sys
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

# Add the src directory to the Python path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.apis.database import SessionLocal
from src.apis.models import Posts, SourceEnum
from src.utils.app_utils import scrape_comments_with_playwright


async def update_post_comment(post, db):
    """Update a single post's comment_html in the database."""
    try:
        # Skip if post doesn't have a comment_url
        if not post.comment_url:
            # Try to construct comment_url if missing
            if post.source == SourceEnum.REDDIT and post.post_id:
                # For Reddit posts, construct URL from post_id
                new_comment_url = f"https://www.reddit.com/r/{post.sub}/comments/{post.post_id}"
                print(f"Constructed comment_url for post ID {post.post_id}: {new_comment_url}")
                post.comment_url = new_comment_url
                post.updated_at = datetime.utcnow()
                db.commit()
            elif post.source == SourceEnum.HNEWS and post.post_id:
                # For Hacker News posts, construct URL from post_id
                new_comment_url = f"https://news.ycombinator.com/item?id={post.post_id}"
                print(f"Constructed comment_url for post ID {post.post_id}: {new_comment_url}")
                post.comment_url = new_comment_url
                post.updated_at = datetime.utcnow()
                db.commit()
            else:
                print(f"⚠️ Skipping post {post.post_id}: No comment_url and unable to construct one")
                return False
        
        # Use local service instead of playwright to scrape comments
        print(f"Fetching comments for post {post.post_id} from {post.comment_url}")
        service_url = f"http://localhost:3033/get?s=&url={post.comment_url}"
        
        response = requests.get(service_url)
        if response.status_code == 200:
            comments_html = response.text
            
            if comments_html and comments_html.strip():
                # Update post with scraped comments
                post.comment_html = comments_html
                post.updated_at = datetime.utcnow()
                db.commit()
                print(f"✅ Successfully updated comments for post ID: {post.post_id}")
                print(f"   Comment HTML length: {len(comments_html)} characters")
                return True
            else:
                print(f"❌ No comments found for {post.post_id}")
                return False
        else:
            print(f"❌ Service returned status code {response.status_code} for {post.post_id}")
            return False
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating post {post.post_id} with comments: {str(e)}")
        return False


async def fetch_and_update_comments():
    """Fetch recent posts and update their comments."""
    db = SessionLocal()
    try:
        # Get 20 most recent posts that either:
        # 1. Don't have comment_html, or
        # 2. Have empty comment_html
        posts = db.query(Posts)\
            .filter((Posts.comment_html.is_(None)) | (Posts.comment_html == ''))\
            .order_by(Posts.created_at.desc())\
            .limit(20)\
            .all()
        
        print(f"Found {len(posts)} posts without comments. Starting scraping...")
        
        if not posts:
            print("No posts found that need comment updates.")
            return
        
        # Process posts one by one to avoid overloading the system
        success_count = 0
        for post in posts:
            if await update_post_comment(post, db):
                success_count += 1
            # Small delay between requests to avoid rate limiting
            await asyncio.sleep(1)
        
        print(f"✅ Completed comment scraping for {success_count}/{len(posts)} posts")
        
    except Exception as e:
        print(f"❌ Error fetching posts: {str(e)}")
    finally:
        db.close()


def main():
    """Main entry point for the script."""
    print("🔍 Starting comment scraping for recent posts")
    asyncio.run(fetch_and_update_comments())


if __name__ == "__main__":
    main()
