from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, ImageSendMessage)
from .camera import camera
import asyncio
import os
import logging

logging.basicConfig(level=logging.INFO)

API_DOMAIN = os.environ["API_DOMAIN"]
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

accepted_photo_requests = [
    "たまー",
    "タマー",
    "げんき？",
    "元気？",
    "げんき?",
    "元気?"
]


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text in accepted_photo_requests:
        photo = camera.get_photo()
        img_datetime = photo["datetime"]
        with open(f"/static/{img_datetime}.jpg", "wb") as f:
            f.write(photo["img"].data)
        img_url = f"https://{API_DOMAIN}/hamcam/static/{img_datetime}.jpg"
        message = ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
        )
        line_bot_api.reply_message(event.reply_token, message)


async def handle_message(body, signature):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None, handler.handle, body, signature)
    return "OK"
