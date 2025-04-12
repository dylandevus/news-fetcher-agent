import strawberry
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session

from .database import get_db, engine
from . import models


# Create tables in the database
models.Base.metadata.create_all(bind=engine)


@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class News:
    title: str
    content: str


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)

    @strawberry.field
    def news(self) -> list[News]:
        return [
            News(title="News 1", content="Content of News 1"),
            News(title="News 2", content="Content of News 2"),
        ]


schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

app.include_router(graphql_app, prefix="/graphql")
