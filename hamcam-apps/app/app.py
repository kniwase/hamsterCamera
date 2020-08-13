from fastapi import FastAPI
from .routers.camera import router as camera_router

api = FastAPI(
    title="ハムスターカメラAPI",
    description="ハムスターのかわいさを提供します",
    version="0.0.1",
    openapi_url="/hamcam/api/openapi.json",
    docs_url=None,
    redoc_url="/hamcam/api/redoc"
)

api.include_router(
    camera_router,
    prefix="/hamcam/api/camera"
)
