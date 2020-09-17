from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers.camera import router as camera_router
from .routers.line_bot import router as line_bot_router


api = FastAPI(
    title="ハムスターカメラAPI",
    description="ハムスターのかわいさを提供します",
    version="0.0.1",
    openapi_url="/hamcam/api/openapi.json",
    docs_url=None,
    redoc_url=None
)

api.include_router(
    camera_router,
    prefix="/hamcam/api/camera"
)

api.include_router(
    line_bot_router,
    prefix="/hamcam/api/callback"
)

api.mount(
    "/hamcam/static",
    StaticFiles(directory="/static"),
    name="static"
)
