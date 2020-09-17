from .camera import camera
import logging

logging.basicConfig(level=logging.INFO)


async def handle_message():
    photo = await camera.get_photo()
    logging.info(photo["img"].data)
    return {}
