from fastapi import (APIRouter, Request)
from fastapi.responses import PlainTextResponse
from ..modules.line_bot import handle_message
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.post("", response_class=PlainTextResponse)
async def calback(request: Request):
    body = (await request.body()).decode("utf-8")
    signature = request.headers["X-Line-Signature"]
    return await handle_message(body, signature)
