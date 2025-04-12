import requests
from typing import List, Dict, Any
from datetime import datetime  # type: ignore # noqa: F401
from ..app_types.post import Post
from agents import function_tool
from .app_utils import load_yaml_config


def fetch_from_yaml(config_path: str, **kwargs) -> List[Dict[str, Any]]:
    """
    Fetches data based on a YAML configuration file.

    Args:
        config_path (str): Path to the YAML configuration file.
        **kwargs: Additional parameters to override defaults in the YAML file.

    Returns:
        List[Dict[str, Any]]: Fetched and mapped data.
    """
    config = load_yaml_config(config_path)
    # print("--- config ", config)

    # Prepare the URL and headers
    url = config["url_template"].format(**kwargs)
    headers = config.get("headers", {})

    # Make the HTTP request
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Map the response to the desired format
    results = []
    for item in data["data"]["children"][
        : kwargs.get("limit", config["parameters"]["limit"])
    ]:
        mapped_item = {}
        post = item["data"]  # type: ignore # noqa: F841
        for mapping in config["response_mapping"]:
            # print("Processing mapping:", mapping)  # Debug: Print the entire mapping
            # Each `mapping` is a dictionary with a single key-value pair
            for key, value in mapping.items():
                try:
                    # print("key, value:", key, value)  # Debug: Print key-value pair
                    if "datetime" in value:
                        # Handle datetime conversion
                        mapped_item[key] = eval(value)
                    else:
                        mapped_item[key] = eval(value.format(**kwargs))
                except Exception:
                    # print(f"Error processing key '{key}' with value '{value}': {e}")
                    mapped_item[key] = None  # Set to None if an error occurs

            # print("- mapped_item so far:", mapped_item)  # Debug: Print the partially mapped item
        results.append(mapped_item)

    # print("Final results:", results)  # Debug: Print all results

    return results


@function_tool
def fetch_reddit(limit: int, reddit_sub: str) -> List[Dict[str, Post]]:
    """
    Fetches the top Reddit posts using a YAML configuration.

    Args:
        limit (int): Number of posts to fetch.
        reddit_sub (str): Subreddit to fetch posts from.

    Returns:
        List[dict]: Fetched posts.
    """
    return fetch_from_yaml(
        f"src/utils/reddit_{reddit_sub}.yaml",
        subreddit=reddit_sub,
        limit=limit,
    )
