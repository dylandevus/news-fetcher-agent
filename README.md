# news-fetcher-agent

News Fetcher Agent using:

*   OpenAI Agents SDK
*   Structured ouput (pydantic)
*   Crawl4ai
*   Yaml config file to specify news source
*   News sources: Hacker News, Reddit Subs
*   Unit tests using pytest, pytest-cov
*   Webapp Backend: FastAPI, Strawberry GraphQL, Pydantic, Alembic + Mako, SQLAlchemy ORM
*   Webapp Frontend: Vite, React, TS, GraphQL, @Apollo/client, Tailwind CSS

### DEVELOPMENT

#### Require:

*   `uv venv --python 3.13`
*   `uv init`
*   `source .venv/bin/activate`
*   `pre-commit install`

#### Install:

```
$ uv venv
$ uv sync
$ python3 src/main.py

$ ./run.py format
$ ./run.py check
$ ./run.py pyright
$ ./run.py mypy

OR:
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
$ cd src
$ python3 main.py
```

To debug - use: enable_verbose_stdout_logging()

To run tests:

```
$ uv run pytest src/utils/app_utils_test.py

$ uv run pytest --cov=src/utils --cov-report=html
$ open htmlcov/index.html
```

#### Webapp - Backend

Backend:
- ./src/apis

Scripts:

```
Install  $ uv add "fastapi[standard]" alembic graphene graphql-core httptools mako python-dateutil six sqlalchemy uvloop watchfiles websockets strawberry-graphql pydantic uvicorn

Run      $ uvicorn src.apis.main:app --reload

Test GraphQL endpoint: http://localhost:8000/graphql

query {
  news {
    title
    content
  }
}
```

Database:

```
Make a change         $ alembic revision --autogenerate -m "Description of your change"
Apply the migration   $ alembic upgrade head

Seed data    $ python scripts/seed_database.py

```

#### Webapp - Frontend

Scripts:

```
Install  $ pnpm i
Run      $ cd ui && pnpm dev
```

#### Output sample:

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