import yaml
import datetime
import asyncio
from typing import Any, List, Optional
from playwright.async_api import async_playwright
from sqlalchemy import inspect, text
from ..apis.database import engine, SessionLocal
from ..apis.models import Posts, SourceEnum
from ..app_types import Post


def ensure_comment_html_column_exists():
    """
    Ensure that the comment_html column exists in the posts table.
    This is a workaround for Alembic migration issues.
    """
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            
            if 'posts' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('posts')]
                
                if 'comment_html' not in columns:
                    # Add the column directly with SQL
                    conn.execute(text("ALTER TABLE posts ADD COLUMN comment_html TEXT"))
                    conn.commit()
                    print("✅ Successfully added comment_html column to posts table")
                else:
                    print("ℹ️ comment_html column already exists in posts table")
            else:
                print("❓ posts table does not exist in the database yet")
    except Exception as e:
        print(f"❌ Error checking/adding comment_html column: {str(e)}")


async def scrape_comments_with_playwright(comment_url: str) -> Optional[str]:
    """
    Scrapes comments from a provided URL using Playwright.

    Args:
        comment_url (str): URL of the page containing comments

    Returns:
        Optional[str]: HTML content of the comments section, or None if scraping failed
    """
    if not comment_url:
        return None

    try:
        async with async_playwright() as p:
            # Launch a headless browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Set headers to mimic a real browser
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })

            # Navigate to the comment URL
            await page.goto(comment_url, wait_until="domcontentloaded")

            # Extract comments based on source
            if "reddit.com" in comment_url:
                # Wait for comments to load by waiting for a specific element
                try:
                    await page.wait_for_selector('[data-testid="comment"]', timeout=10000)  # Wait up to 20 seconds
                    await page.evaluate("window.scrollBy(0, window.innerHeight)")  # Scroll down to load more comments
                except Exception as e:
                    print(f"Timeout or error waiting for comments to load: {str(e)}")

                # Log more of the page content for debugging
                page_content = await page.content()
                print("Full page content loaded for debugging:", page_content[:1000])

                # Updated Reddit comment selector with broader approach
                comments_html = await page.evaluate("""
                    () => {
                        const commentElements = document.querySelectorAll('[data-testid="comment"], .Comment');
                        if (commentElements.length > 0) {
                            return Array.from(commentElements).map(el => el.outerHTML).join('\\n');
                        }
                        return '';
                    }
                """)
            elif "news.ycombinator.com" in comment_url:
                # HackerNews comments are in a specific table structure
                comments_html = await page.evaluate("""
                    () => {
                        const commentsContainer = document.querySelector('.comment-tree');
                        return commentsContainer ? commentsContainer.outerHTML : '';
                    }
                """)
            else:
                # Generic approach for unknown sites
                comments_html = await page.evaluate("""
                    () => {
                        // Look for common comment containers
                        const possibleCommentSelectors = [
                            '.comments', '#comments', '.comment-section', 
                            '[data-testid="comments-section"]', '.discussion-thread'
                        ];

                        for (const selector of possibleCommentSelectors) {
                            const element = document.querySelector(selector);
                            if (element) return element.outerHTML;
                        }

                        return '';
                    }
                """)

            await browser.close()
            return comments_html
    except Exception as e:
        print(f"Error scraping comments from {comment_url}: {str(e)}")
        return None


async def update_post_with_comments(post_id: str):
    """
    Update a post with scraped comments.

    Args:
        post_id (str): The ID of the post to update
    """
    db = SessionLocal()
    try:
        # Get the post from the database
        post = db.query(Posts).filter(Posts.post_id == post_id).first()
        if not post or not post.comment_url:
            return
            
        # Scrape comments
        comments_html = await scrape_comments_with_playwright(post.comment_url)
        if comments_html:
            # Update the post with the scraped comments
            post.comment_html = comments_html
            db.commit()
            print(f"Successfully updated comments for post ID: {post_id}")
    except Exception as e:
        db.rollback()
        print(f"Error updating post with comments: {e}")
    finally:
        db.close()


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
    and asynchronously scrape comments for new posts
    """
    db = SessionLocal()
    new_post_ids = []
    
    try:
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
            
            # Keep track of new post IDs for scraping comments later
            if post.id and post.comment_url:
                new_post_ids.append(post.id)

        # Commit all posts to the database
        db.commit()
        print(f"Successfully saved {len(posts)} posts to the database")
        
        # Asynchronously scrape comments for new posts in the background
        if new_post_ids:
            # Start the scraping process in the background without waiting for it
            asyncio.create_task(_scrape_comments_for_posts(new_post_ids))
            print(f"Started background comment scraping for {len(new_post_ids)} new posts")
            
    except Exception as e:
        db.rollback()
        print(f"Error saving posts to database: {e}")
    finally:
        db.close()
        
        
async def _scrape_comments_for_posts(post_ids: List[str]):
    """
    Scrape comments for multiple posts in parallel

    Args:
        post_ids (List[str]): List of post IDs to scrape comments for
    """
    print(f"Starting comment scraping for {len(post_ids)} posts with IDs: {post_ids}")

    # Create tasks for each post
    tasks = [update_post_with_comments(post_id) for post_id in post_ids]

    # Run tasks in parallel with a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent browser instances

    async def _scrape_with_semaphore(task):
        async with semaphore:
            return await task

    try:
        # Wait for all tasks to complete
        await asyncio.gather(*[_scrape_with_semaphore(task) for task in tasks])
        print(f"✅ Comment scraping completed successfully for all {len(post_ids)} posts")
    except Exception as e:
        print(f"❌ Error during comment scraping: {str(e)}")
