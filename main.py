import uvicorn

from fastapi import FastAPI
from modal import asgi_app
import modal

from src.fastapi import router
from src.config import modal_stub as stub, image

web_app = FastAPI()

web_app.include_router(router)


@stub.function(image=image, secret=modal.Secret.from_name("envs"))
@asgi_app()
def fastapi_app():
    return web_app


# Local dev
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)
