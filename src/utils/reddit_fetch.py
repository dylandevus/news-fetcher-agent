import requests
from typing import List, Union
from agents import function_tool
from datetime import datetime
from app_types.post import Post, SourceEnum


@function_tool
def fetch_reddit_top_posts(limit: int, sub: str) -> List[Union[Post, dict]]:
    """
    Fetches the top Reddit posts from the subreddit 'sub' for the past week.

    Args:
        limit (int): Number of top posts to fetch.
        sub (str): Name of the subreddit.

    Returns:
        List[dict]: A list of dictionaries containing post metadata.

    Return Sample:
        [{
            "source": "REDDIT",
            "sub": "ArtificialInteligence",
            "id": "1jo3o69",
            "title": "Are LLMs just predicting the next token?",
            "text": "",
            "author": "relegi",
            "upvotes": 158,
            "url": "https://www.reddit.com/r/ArtificialInteligence/comments/1jo3o69/are_llms_just_predicting_the_next_token/",
            "published_date": "2025-03-31 06:51:20",
            "comment_url": "https://www.reddit.com/r/ArtificialInteligence/comments/1jo3o69/are_llms_just_predicting_the_next_token/"
        }]
    """
    if limit is None:
        limit = 10

    if sub is None:
        sub = "Python"

    reddit_url = f"https://www.reddit.com/r/{sub}/top/.json?t=week"
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
                sub=sub,
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
