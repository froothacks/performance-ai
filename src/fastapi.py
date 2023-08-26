from typing import Optional

from fastapi import APIRouter, Header, Request
from fastapi.templating import Jinja2Templates
from modal import web_endpoint
from pydantic import BaseModel

from .config import modal_stub


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# --- FastAPI app ---
"""
TODO Endpoints
- All users
- Current user
- Given a prompt, give back top 5 examples
"""


class Item(BaseModel):
    name: str


@router.get("/")
async def handle_root(request: Request, user_agent: Optional[str] = Header(None)):
    print(f"GET /     - received user_agent={user_agent}")
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/foo")
async def handle_foo(item: Item, user_agent: Optional[str] = Header(None)):
    print(
        f"POST /foo - received user_agent={user_agent}, item.name={item.name}"
    )
    return item


@modal_stub.function()
@web_endpoint(method="POST")
def f(item: Item):
    return "Hello " + item.name
