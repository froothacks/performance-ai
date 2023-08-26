from typing import TypedDict
from itertools import islice
import modal

import numpy as np
from fastapi import APIRouter, Request
from modal import web_endpoint
from pydantic import BaseModel

from .llm import filter_thread, synthesize_threads_jsonformer
from .config import modal_stub, slack_client, db, co, image


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
    profile_pic: str


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


@modal_stub.function(image=image, secret=modal.Secret.from_name("envs"))
@web_endpoint(method="GET")
async def all_users() -> list[User]:
    """Gets all slack users
    https://api.slack.com/methods/users.list
    """
    return [
        User(id=x["id"], name=x["name"], profile_pic=x["profile"]["image_32"])
        for x in (await get_slack_users())["members"]
    ]


thread = db.thread  # collection


async def embed(text: str) -> list[float]:
    """Embed text using cohere"""
    resp = await co.embed(text)
    return resp.embeddings[0]


def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def average_embeddings(
    embeddings: list[list[float | int]], chunk_lengths: list[int]
) -> list[float | int]:
    # https://github.com/openai/openai-cookbook/blob/main/examples/Embedding_long_inputs.ipynb
    chunk_embeddings = np.average(embeddings, axis=0, weights=chunk_lengths)
    chunk_embeddings = chunk_embeddings / np.linalg.norm(
        chunk_embeddings
    )  # normalizes length to 1
    return chunk_embeddings.tolist()


@modal_stub.function(image=image, secret=modal.Secret.from_name("envs"))
@web_endpoint(method="POST")
async def slack_webhook(request: Request):
    """
    Processes Slack messages and stores in MongoDB

    Collection schema:
    {
    "id": "mongo auto id",
    "user_ids": [],
    "slack_thread_id": str,
    "channel": "C05Q1RZMBA5",
    "messages": [{
            "id": "slack message id", "text": "message text", "user_id": "user id", "name": "user name"
        }]
    }
    """

    data: dict = await request.json()
    if (challenge := data.get("challenge")) is not None:
        return challenge

    event = data["event"]
    if event["type"] != "message":
        return ""

    user_id = event["user"]
    user = await slack_client.users_info(user=user_id)
    user_name = user.data["user"]["name"]
    text = event["text"]

    if not filter_thread(user_name, event):
        return ""

    if event.get("thread_ts") is None or event["thread_ts"] == event["event_ts"]:
        await thread.insert_one(
            {
                "slack_thread_id": event["event_ts"],
                "user_ids": [user_id],
                "channel": event["channel"],
                "messages": [
                    {
                        "text": text,
                        "user_id": user_id,
                        "name": user_name,
                    }
                ],
            }
        )
    else:
        rec = await thread.find_one({"slack_thread_id": event["thread_ts"]})
        filter_push = {
            "messages": {
                "text": text,
                "user_id": user_id,
                "name": user_name,
            },
        }
        update = {"$push": filter_push}
        if rec["user_ids"] is None:
            update["$set"] = {"user_ids": [user_id]}
        elif user_id not in rec["user_ids"]:
            filter_push["user_ids"] = user_id
        await thread.update_one(
            {"slack_thread_id": event["thread_ts"]},
            update,
        )

    return ""


class ThreadQuery(BaseModel):
    prompt: str
    user_id: str


class ThreadQueryResp(BaseModel):
    summarized: str
    thread_id: str
    thread_link: str


@modal_stub.function(image=image, secret=modal.Secret.from_name("envs"))
@web_endpoint(method="POST")
async def query_threads(data: ThreadQuery) -> list[ThreadQueryResp]:
    """Queries threads and returns top 5 results"""

    prompt = data.prompt
    user_id = data.user_id
    # https://stackoverflow.com/questions/12437849/how-to-query-an-element-from-a-list-in-pymongo
    recs = [x async for x in thread.find({"user_ids": {"$in": [user_id]}})]
    user = await slack_client.users_info(user=user_id)
    user_name = user.data["user"]["name"]
    if not recs:
        return []
    summary = await synthesize_threads_jsonformer(
        user_name,
        prompt,
        [
            {
                "thread_id": rec["slack_thread_id"],
                "messages": [(x["name"], x["text"]) for x in rec["messages"]],
            }
            for rec in recs
        ],
    )
    base_url = "https://performanceaigroup.slack.com/archives/"
    return [
        ThreadQueryResp(
            summarized=x["evidence_synthesis"],
            thread_id=x["thread_id"],
            # https://performanceaigroup.slack.com/archives/C05Q1UNAY5P/p1693081393304879
            # https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693082233454459
            # https://performanceaigroup.slack.com/archives/C05PGS91WNS/p1693082273157719?thread_ts=1693082233.454459&cid=C05PGS91WNS
            thread_link=f"{base_url}{x['channel']}/p{x['slack_thread_id'].replace('.', '')}",
        )
        for x in summary["threads"]
    ]
