import os
from typing import Optional

import cohere
import pymongo
from dotenv import load_dotenv
from fastapi import FastAPI, Header
from modal import Image, Stub, asgi_app, web_endpoint
from pydantic import BaseModel


load_dotenv()
web_app = FastAPI()
stub = Stub("example-fastapi-app")
image = Image.debian_slim()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

client = pymongo.MongoClient(
    "mongodb+srv://<username>:<password>@<cluster-name>/test?retryWrites=true&w=majority")


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    return web_app


# --- Slack portion ---
"""
TODO Incoming webhooks
- Save the incoming messages and store in list[list[str]]. Embed the
messages and find average embedding
"""


# --- FastAPI app ---
"""
TODO Endpoints
- All users
- Current user
- Given a prompt, give back top 5 examples
"""


class Item(BaseModel):
    name: str


@web_app.get("/")
async def handle_root(user_agent: Optional[str] = Header(None)):
    print(f"GET /     - received user_agent={user_agent}")
    return "Hello World"


@web_app.post("/foo")
async def handle_foo(item: Item, user_agent: Optional[str] = Header(None)):
    print(
        f"POST /foo - received user_agent={user_agent}, item.name={item.name}"
    )
    return item


@stub.function()
@web_endpoint(method="POST")
def f(item: Item):
    return "Hello " + item.name


if __name__ == "__main__":
    stub.deploy("webapp")
