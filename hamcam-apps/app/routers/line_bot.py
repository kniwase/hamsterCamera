from fastapi import (APIRouter, WebSocket, Response)
from ..modules.line_bot import handle_message

router = APIRouter()


@router.post("")
async def calback():
    return await handle_message()
