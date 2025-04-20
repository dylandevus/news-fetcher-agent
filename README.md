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

*   `uv venv --python 3.13.2`
*   `uv init`
*   `source .venv/bin/activate`
*   `pre-commit install`

#### Install:

```
$ uv sync

$ ./run.py format
$ ./run.py check
$ ./run.py pyright
$ ./run.py mypy
```

To debug - use: enable_verbose_stdout_logging()

To run tests:

```
$ uv run pytest src/utils/app_utils_test.py

$ uv run pytest --cov=src/utils --cov-report=html
$ open htmlcov/index.html
```

#### Webapp - Backend

##### Backend:
- ./src/apis

Scripts: uv 

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

##### Fetch posts

`$ python3 -m src.main    (run as module to avoid relative import issues)`

##### Fetch Reddit comments

`python3 scripts/fetch_comments.py`

##### Database:

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
        "source": "REDDIT",
        "sub": "ArtificialInteligence",
        "id": "1js7k6z",
        "title": "There Was a Film Made Completely Through AI",
        "text": "",
        "author": "gnshgtr",
        "upvotes": 73,
        "url": "https://...",
        "published_date": "2025-04-05 09:39:00",
        "comment_url": null
    },...
]
```