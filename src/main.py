from typing import Union
import asyncio
import json
import requests
import asyncio
from crawl4ai import AsyncWebCrawler  # type: ignore
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from datetime import datetime, timedelta
from agents import Agent, Runner, function_tool
from utils.reddit_fetch import fetch_reddit_top_posts
from dotenv import load_dotenv

load_dotenv()


class Post(BaseModel):
    id: Optional[int]  # Add the Hacker News post ID
    title: Optional[str]
    author: Optional[str]
    upvotes: Optional[int]
    url: Optional[str]
    published_date: Optional[str]
    comment_url: Optional[str]  # Add the Hacker News comment URL


async def crawl_page(url: str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        print(result.markdown)




@function_tool
def fetch_hackernews_top_posts(limit: int) -> List[Union[Post, dict]]:
    """
    Fetches the top Hacker News posts of the week and their metadata, filtering for programming or AI-related posts.

    Args:
        limit (int): Number of top posts to fetch.

    Returns:
        List[Post]: A list of validated Post objects.
    """
    if limit is None:
        limit = 10

    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
    one_week_ago = datetime.now() - timedelta(days=7)
    keywords = [
        "program",
        "ML",
        "AI",
        "machine learning",
        "artificial intelligence",
        "agent",
        "coding",
        "developer",
        "development",
        "source",
        "code",
        "Open-source",
        "python",
        "javascript",
        "typescript",
        "css",
        "server",
        "browser",
    ]

    try:
        response = requests.get(top_stories_url)
        response.raise_for_status()
        top_story_ids = response.json()

        posts: List[Union[Post, dict]] = []
        for story_id in top_story_ids:
            if len(posts) >= limit:
                break

            story_response = requests.get(item_url.format(story_id))
            story_response.raise_for_status()
            story_data = story_response.json()

            # Filter posts published within the last 7 days
            published_date = datetime.fromtimestamp(story_data.get("time", 0))
            if published_date >= one_week_ago:
                title = story_data.get("title", "").lower()
                if any(keyword in title for keyword in keywords) and story_data.get("score") > 20:
                    try:
                        post = Post(
                            id=story_id,  # Include the Hacker News post ID
                            title=story_data.get("title"),
                            author=story_data.get("by"),
                            upvotes=story_data.get("score"),
                            url=story_data.get("url"),
                            published_date=datetime.fromtimestamp(int(story_data.get("time"))).strftime("%Y-%m-%d %H:%M:%S"),
                            comment_url=f"https://news.ycombinator.com/item?id={story_id}",  # Generate comment URL
                        )
                        posts.append(post)
                    except ValidationError as e:
                        posts.append({"error": str(e)})
        return posts
    except requests.RequestException as e:
        print(e)
        return [{"error": str(e)}]
    except Exception as e:
        print(e)
        return [{"error": str(e)}]


agent = Agent(
    name="Hacker News Fetcher",
    instructions="You are an agent that fetches top Hacker News and Reddit Python posts.",
    tools=[fetch_hackernews_top_posts, fetch_reddit_top_posts],
    output_type=List[Post],
)


async def main():
    # await crawl_page("https://www.nbcnews.com/business")

    result = await Runner.run(
        agent,
        input="Fetch the top 10 Reddit Python posts. Also show link, link to comments, published date, author, upvotes.",
    )
    # Convert the output to JSON and print it
    json_output = json.dumps(
        [post.model_dump() for post in result.final_output], indent=4
    )
    print(json_output)


if __name__ == "__main__":
    asyncio.run(main())
