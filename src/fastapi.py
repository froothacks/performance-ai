from typing import TypedDict

from fastapi import APIRouter, Request
from modal import web_endpoint
from pydantic import BaseModel

from .config import modal_stub, slack_client, db, co


router = APIRouter()

# class Item(BaseModel):
#     name: str
# @modal_stub.function()
# @web_endpoint(method="POST")
# def f(item: Item):
#     return "Hello " + item.name


class User(BaseModel):
    id: str
    name: str


async def get_slack_users():
    class GetAllUsersSlackRespMemberProfile(TypedDict):
        title: str
        phone: str
        skype: str
        real_name: str
        real_name_normalized: str
        display_name: str
        first_name: str
        last_name: str
        image_24: str
        image_32: str
        image_48: str
        image_72: str
        image_192: str
        image_512: str
        image_1024: str
        status_text: str
        status_emoji: str
        status_expiration: int
        avatar_hash: str
        always_active: bool
        team: str

    class GetAllUsersSlackRespMember(TypedDict):
        id: str
        team_id: str
        name: str
        deleted: bool
        color: str  # 757575
        real_name: str
        tz: str
        tz_offset: int
        profile: GetAllUsersSlackRespMemberProfile
        is_bot: bool

    class GetAllUsersSlackResp(TypedDict):
        ok: bool
        members: list[GetAllUsersSlackRespMember]

    data: GetAllUsersSlackResp = (await slack_client.users_list()).data
    return data


@router.get("/all-users")
async def get_all_users() -> list[User]:
    """Gets all slack users
    https://api.slack.com/methods/users.list
    """
    return [
        User(id=x["id"], name=x["name"])
        for x in (await get_slack_users())["members"]
    ]


thread = db.test_thread_1


@router.post("/slack-webhook")
async def slack_webhook():
    """
    Processes Slack messages and stores in MongoDB

    Collection schema:
    {
    "id": "mongo auto id",
    "slack_thread_id": "slack thread id",
    "thread averaged vector": "vector",
    "thread text": "thread text",
    "messages": {"id": "mongo id", "text": "message text", "vector"}
    }
    """

    return ""


class ThreadQuery(BaseModel):
    prompt: str


@router.post("/query-threads")
async def query_threads(request: Request, data: ThreadQuery):
    """Queries threads and returns top 5 results"""

    prompt = data.prompt

    document = await thread.find_one({'i': {'$lt': 1}})
    cursor = await thread.find({'i': {'$lt': 5}}).sort('i')
    for document in await cursor.to_list(length=100):
        print(document)
