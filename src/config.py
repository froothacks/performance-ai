import os

import cohere
import pymongo
from modal import Stub
from slack_sdk.web.async_client import AsyncWebClient


mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = mongo_client.myDatabase
# co = cohere.Client(os.getenv("COHERE_API_KEY"))
modal_stub = Stub("example-fastapi-app")
slack_client = AsyncWebClient()
