import asyncio
import json
from crawl4ai import AsyncWebCrawler  # type: ignore
from typing import List
from agents import Agent, Runner, enable_verbose_stdout_logging

# from utils.reddit_fetch import fetch_reddit_top_posts
from .utils.hnews_fetch import fetch_hackernews_top_posts
from .utils.yaml_fetch import fetch_reddit
from .utils.app_utils import save_posts_to_database
from dotenv import load_dotenv
from .app_types.post import Post


load_dotenv()

VERBOSE = True
if VERBOSE:
    enable_verbose_stdout_logging()  # from agents import enable_verbose_stdout_logging


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

    # sources: Hacker News, Reddit
    # subs: reactjs, ArtificialInteligence, ChatGPTPro, LocalLLaMA
    result = await Runner.run(
        agent,
        input="""
            Fetch the top 20 Reddit sub 'LocalLLaMA' posts.
            Also show title, link, link to comments, published date, author, upvotes.
        """,
    )

    # Save posts to the database using SQLAlchemy ORM
    if (
        result.final_output
        and isinstance(result.final_output, list)
        and len(result.final_output) > 0
    ):
        save_posts_to_database(result.final_output)

    # Convert the output to JSON and print it
    json_output = json.dumps(
        [post.model_dump() for post in result.final_output], indent=4
    )
    print(json_output)


if __name__ == "__main__":
    asyncio.run(main())
