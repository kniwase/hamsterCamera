from fastapi import (APIRouter, WebSocket, Response)
from ..modules.camera import camera

router = APIRouter()


@router.get("/getPhoto", )
async def get_photo():
    photo = await camera.get_photo()
    return Response(content=photo, media_type="image/jpeg")


@router.get("/getBatteryStatus", )
async def get_battery_status():
    return await camera.get_battery_status()


@router.websocket("/ws")
async def create_connection(websocket: WebSocket):
    await camera.create_connection(websocket)
