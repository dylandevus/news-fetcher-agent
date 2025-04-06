import requests
from typing import List, Union
from agents import function_tool
from datetime import datetime
from app_types.post import Post, SourceEnum


@function_tool
def fetch_reddit_top_posts(limit: int, reddit_sub: str) -> List[Union[Post, dict]]:
    """
    Fetches the top Reddit posts from the subreddit 'reddit_sub' for the past week.

    Args:
        limit (int): Number of top posts to fetch.
        reddit_sub (str): Name of the subreddit.

    Returns:
        List[dict]: A list of dictionaries containing post metadata.

    Return Sample:
        [{
            "source": "REDDIT-PYTHON",
            "id": "1jo8gvx",
            "title": "PEP 751 (a standardized lockfile for Python) is accepted!",
            "text": "",
            "author": "toxic_acro",
            "upvotes": 1127,
            "url": "https://www.reddit.com/r/Python/comments/1jo8gvx/pep_751_a_standardized_lockfile_for_python_is/",
            "published_date": "2025-03-31 10:14:57",
            "comment_url": "https://www.reddit.com/r/Python/comments/1jo8gvx/pep_751_a_standardized_lockfile_for_python_is/"
        }]
    """
    if limit is None:
        limit = 10

    if reddit_sub is None:
        reddit_sub = "Python"

    reddit_url = f"https://www.reddit.com/r/{reddit_sub}/top/.json?t=week"
    headers = {"User-Agent": "news-fetcher-agent"}

    try:
        response = requests.get(reddit_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        posts: List[Union[Post, dict]] = []
        for post in data["data"]["children"][:limit]:
            post_data = post["data"]
            post = Post(
                source=SourceEnum.reddit,
                sub=reddit_sub,
                id=post_data.get("id"),
                title=post_data.get("title"),
                text="",
                author=post_data.get("author"),
                upvotes=post_data.get("ups"),
                url=post_data.get("url"),
                comment_url=f"https://www.reddit.com{post_data.get('permalink')}",
                published_date=datetime.fromtimestamp(
                    post_data.get("created_utc")
                ).strftime("%Y-%m-%d %H:%M:%S"),
            )
            posts.append(post)

        return posts
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return [{"error": str(e)}]
    except Exception as e:
        print(f"Unexpected error: {e}")
        return [{"error": str(e)}]
