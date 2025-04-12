import asyncio
import json
import datetime
from crawl4ai import AsyncWebCrawler  # type: ignore
from typing import List
from agents import Agent, Runner, enable_verbose_stdout_logging

# from utils.reddit_fetch import fetch_reddit_top_posts
from utils.hnews_fetch import fetch_hackernews_top_posts
from utils.yaml_fetch import fetch_reddit
from dotenv import load_dotenv
from app_types.post import Post
from apis.database import SessionLocal
from apis.models import Posts, SourceEnum


load_dotenv()

VERBOSE = True
if VERBOSE:
    enable_verbose_stdout_logging()  # from agents import enable_verbose_stdout_logging


def save_posts_to_database(posts: List[Post]):
    """
    Save a list of Post objects to the database using SQLAlchemy ORM
    """
    db = SessionLocal()
    try:
        # Create Posts models from Post pydantic models
        for post in posts:
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


async def crawl_page(url: str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        print(result.markdown)  # type: ignore


agent = Agent(
    name="News Fetcher",
    instructions="You are an agent that fetches top Hacker News and Reddit posts.",
    tools=[fetch_hackernews_top_posts, fetch_reddit],
    output_type=List[Post],
)


async def main():
    # await crawl_page("https://www.nbcnews.com/business")

    result = await Runner.run(
        agent,
        input="Fetch the top 10 Reddit sub 'reactjs' posts. Also show title, link, link to comments, published date, author, upvotes.",
    )
    
    # Save posts to the database using SQLAlchemy ORM
    if result.final_output and isinstance(result.final_output, list) and len(result.final_output) > 0:
        save_posts_to_database(result.final_output)
    
    # Convert the output to JSON and print it
    json_output = json.dumps(
        [post.model_dump() for post in result.final_output], indent=4
    )
    print(json_output)


if __name__ == "__main__":
    asyncio.run(main())
