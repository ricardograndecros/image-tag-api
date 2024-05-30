from base64 import b64decode, b64encode
import base64
from copy import copy, deepcopy
from datetime import datetime
from operator import le
import uuid
from flask import current_app
from .utils import image_utils, keys
from .config.config import AppConfig
from .model import add_picture, add_tag, get_picture_with_tags, get_pictures_with_tags, get_tags

image_dto = {
    "id": "",
    "size": 0,
    "date": "",
    "tags": [],
    "data": ""
}

error_response_dto = {
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
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try: 
        add_picture(image_uuid, filename, now)
        for tag in tags:
            add_tag(tag["tag"], image_uuid, tag["confidence"], now)
    except Exception as e:
        raise Exception(f"Error storing data: {str(e)}")


    response = copy(image_dto)

    response["id"] = image_uuid
    response["size"] = file_size
    response["date"] = now
    response["tags"] = [{"tag": tag["tag"], "confidence": tag["confidence"]} for tag in tags]
    response["data"] = b64_image

    return response

def fetch_images(min_date: datetime, max_date: datetime, tags: str) -> list:
    # fetch images from database
    try :
        pictures = get_pictures_with_tags(min_date, max_date, tags)
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")
    
    current_app.logger.info(f"pictures: {pictures}")

    response = []
    for picture in pictures:
        image = deepcopy(image_dto)
        del image["data"]  # not needed in this endpoint
        image["id"] = picture.id 
        # obtain the image size in KB from the image path
        image["size"] = image_utils.get_image_size(picture.path)
        image["date"] = picture.date
        image["tags"] = [{"tag": tag, "confidence": float(confidence)} for tag, confidence in zip(picture.tags.split(','), picture.confidences.split(','))]
        response.append(image)

    return response

def fetch_image(image_id: str) -> dict:
    # fetch image from database
    try:
        current_app.logger.info(f"image_id: {image_id}")
        picture_tags = get_picture_with_tags(image_id)
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

    with open(picture_tags.path, "rb") as file:
        content = file.read()

    b64str = b64encode(content).decode("utf-8")

    response = deepcopy(image_dto)
    response["id"] = picture_tags.id
    response["size"] = image_utils.get_image_size(picture_tags.path)
    response["date"] = picture_tags.date
    response["tags"] = [{"tag": tag, "confidence": float(confidence)} for tag, confidence in zip(picture_tags.tags.split(','), picture_tags.confidences.split(','))]
    response["data"] = b64str

    return response

def fetch_tags(min_date: datetime, max_date: datetime) -> list:
    # fetch tags from database
    try:
        tags = get_tags(min_date, max_date)
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

    return tags

def uuid_generator():
    return str(uuid.uuid4())