import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pprint


"""
TODO Incoming webhooks
- Save the incoming messages and store in list[list[str]]. Embed the
messages and find average embedding
"""

# Docs https://slack.dev/python-slack-sdk/api-docs/slack_sdk/

pp = pprint.PrettyPrinter(indent=2)

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

try:
    response = client.chat_postMessage(channel='#random', text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")

# You probably want to use a database to store any user information ;)
users_store = {}


# Put users into the dict
def save_users(users_array):
    for user in users_array:
        # Key user info on their unique user ID
        user_id = user["id"]
        # Store the entire user object (you may not need all of the info)
        users_store[user_id] = user
    pp.pprint(users_store)

try:
    # Call the users.list method using the WebClient
    # users.list requires the users:read scope
    result = client.users_list()
    save_users(result["members"])

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))

### BOLT FOR PYTHON
import logging
logging.basicConfig(level=logging.DEBUG)

# from slack_bolt import App

# # export SLACK_SIGNING_SECRET=***
# # export SLACK_BOT_TOKEN=xoxb-***
# app = App()

# # Add functionality here

# if __name__ == "__main__":
#     app.start(3000)  # POST http://localhost:3000/slack/events

import os

import logging
logging.basicConfig(level=logging.DEBUG)

# -----------------------------
#  Bolt app
# -----------------------------

from slack_bolt.async_app import AsyncApp

app = AsyncApp(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)

@app.event("app_mention")
async def hello(event, say):
    await say(f"Hey <@{event['user']}>!")

# -----------------------------
#  Web app & server
# -----------------------------

import uvicorn
from fastapi import FastAPI, Request, Response
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

api = FastAPI()
handler = AsyncSlackRequestHandler(app)

@api.get("/")
async def root(req: Request):
    return Response(status_code=200, content="OK")

@api.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)

# python3 app.py
if __name__ == "__main__":
    uvicorn.run(
        "app:api",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )