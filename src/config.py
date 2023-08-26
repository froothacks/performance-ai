import os

import cohere
# import pymongo
import motor.motor_asyncio
from modal import Stub
from slack_sdk.web.async_client import AsyncWebClient


# mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
# db = mongo_client.myDatabase

db = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
co = cohere.Client(os.getenv("COHERE_API_KEY"))
modal_stub = Stub("example-fastapi-app")
slack_client = AsyncWebClient(os.environ["SLACK_BOT_TOKEN"])
