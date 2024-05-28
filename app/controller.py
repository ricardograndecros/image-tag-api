from base64 import b64decode
from ctypes import Union
from datetime import datetime
import uuid
from .utils import image_utils, keys
from .config.config import AppConfig
from .model import add_picture, add_tag

responseDto = {
    "id": "",
    "size": 0,
    "date": "",
    "tags": [],
    "data": ""
}

errorResponseDto = {
    "error": ""
}

def process_image(config: AppConfig, b64_image: str, min_confidence: int) -> dict:
    image_uuid = uuid_generator()
    # store it in imagekit.io
    file_id, file_url, file_size = image_utils.upload_online_image(config.externalApis[keys.IMAGEKIT], image_uuid, b64_image)
    # get tags using imagga.com
    tags = image_utils.extract_tags(config.externalApis[keys.IMAGGA], file_url, min_confidence)
    # remove image from imagekit.io
    image_utils.delete_online_image(config.externalApis[keys.IMAGEKIT], file_id)
    # store image file (convert base64 to image file and store it in a folder)
    image = b64decode(b64_image)
    filename = f"{config.image_store.path}/{image_uuid}.jpg"
    with open(filename, "wb") as file:
        file.write(image)

    # store image in database
    now = datetime.now()
    try: 
        add_picture(image_uuid, filename, now)
        for tag in tags:
            add_tag(tag["tag"], image_uuid, tag["confidence"], now)
    except Exception as e:
        raise Exception(f"Error storing data: {str(e)}")


    responseDto["id"] = image_uuid
    responseDto["size"] = file_size
    responseDto["date"] = now
    responseDto["tags"] = [{"tag": tag["tag"], "confidence": tag["confidence"]} for tag in tags]
    responseDto["data"] = b64_image

    return responseDto

def uuid_generator():
    return str(uuid.uuid4())