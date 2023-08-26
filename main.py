import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modal import Image, asgi_app

from src.fastapi import router
from src.config import modal_stub


load_dotenv()
web_app = FastAPI()
image = Image.debian_slim()

web_app.include_router(router)
web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@modal_stub.function(image=image)
@asgi_app()
def fastapi_app():
    return web_app


if __name__ == "__main__":
    # modal_stub.deploy("webapp")
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)
