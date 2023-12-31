import os

import cohere
from dotenv import load_dotenv

# import pymongo
import motor.motor_asyncio
from modal import Image, Stub
from slack_sdk.web.async_client import AsyncWebClient


load_dotenv()
# mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
# db = mongo_client.myDatabase

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = mongo_client.performance
co = cohere.AsyncClient(os.getenv("COHERE_API_KEY"))
modal_stub = Stub("example-fastapi-app")
image = (
    Image.debian_slim()
    .pip_install_from_requirements("requirements.txt")
    .extend(
        dockerfile_commands=[
            "FROM base",
            "RUN update-ca-certificates",
        ]
    )
)
slack_client = AsyncWebClient(os.environ["SLACK_BOT_TOKEN"])
