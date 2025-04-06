# news-fetcher-agent

News Fetcher Agent using:

*   OpenAI Agents SDK
*   Structured ouput (pydantic)
*   Crawl4ai
*   Yaml config file to specify news source
*   News sources: Hacker News, Reddit Subs

### DEVELOPMENT

Require:

*   `uv venv --python 3.13`
*   `uv init`
*   `pre-commit install`

Install:

```
$ uv venv
$ uv sync

$ ./run.py format
$ ./run.py check
$ ./run.py pyright
$ ./run.py mypy
```

To debug - use: enable_verbose_stdout_logging()

Output sample:

```
[
    {
        "id": 43555110,
        "title": "Is Python Code Sensitive to CPU Caching? (2024)",
        "author": "leonry",
        "upvotes": 62,
        "url": "https://lukasatkinson.de/2024/python-cpu-caching/",
        "published_date": 1743587582,
        "comment_url": "https://news.ycombinator.com/item?id=43555110"
    },
    {
        "id": 43555996,
        "title": "Coolify: Open-source and self-hostable Heroku / Netlify / Vercel alternative",
        "author": "vanschelven",
        "upvotes": 308,
        "url": "https://coolify.io/",
        "published_date": 1743597719,
        "comment_url": "https://news.ycombinator.com/item?id=43555996"
    },...
]
```