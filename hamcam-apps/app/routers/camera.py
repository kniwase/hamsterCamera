from fastapi import APIRouter, WebSocket
from ..modules.camera import camera

router = APIRouter()


@router.websocket("/ws")
async def create_connection(websocket: WebSocket):
    await camera.create_connection(websocket)
