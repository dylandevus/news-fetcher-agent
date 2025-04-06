import requests
from typing import List, Union
from pydantic import ValidationError
from agents import function_tool
from datetime import datetime, timedelta
from app_types.post import Post, SourceEnum


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
            # print("story_data", story_data)

            # Filter posts published within the last 7 days
            published_date = datetime.fromtimestamp(story_data.get("time", 0))
            if published_date >= one_week_ago:
                title = story_data.get("title", "").lower()
                if (
                    any(keyword in title for keyword in keywords)
                    and story_data.get("score") > 20
                ):
                    try:
                        post = Post(
                            source=SourceEnum.hnews,
                            sub=None,
                            id=str(story_id),  # Include the Hacker News post ID
                            title=story_data.get("title"),
                            text=story_data.get("text"),
                            author=story_data.get("by"),
                            upvotes=story_data.get("score"),
                            url=story_data.get("url"),
                            published_date=datetime.fromtimestamp(
                                int(story_data.get("time"))
                            ).strftime("%Y-%m-%d %H:%M:%S"),
                            comment_url=f"https://news.ycombinator.com/item?id={story_id}",  # Generate comment URL
                        )
                        posts.append(post)
                    except ValidationError as e:
                        posts.append({"error": str(e)})
                    except Exception as e:
                        posts.append({"error": str(e)})
        return posts
    except requests.RequestException as e:
        print(e)
        return [{"error": str(e)}]
    except Exception as e:
        print(e)
        return [{"error": str(e)}]
