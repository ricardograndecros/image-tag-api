from email.mime import image
import os
from tkinter import NO
from typing import Union
import requests
from imagekitio import ImageKit
from sqlalchemy import null
from ..config.config import ExternalApiConfig

def upload_online_image(config:ExternalApiConfig, image_name:str, image :str) -> Union[str, str, int]:
    imagekit = ImageKit(
        public_key=config.api_key,
        private_key=config.api_secret,
        url_endpoint=config.api_url
    )
    
    upload_response = imagekit.upload(
        file=image,
        file_name=f"{image_name}.jpg",
    )

    if upload_response.response_metadata.http_status_code != 200:
        print("Error uploading file")
        raise Exception("Error uploading file")
    return upload_response.file_id, upload_response.url, upload_response.size

def delete_online_image(config: ExternalApiConfig, file_id:str):
    imagekit = ImageKit(
        public_key=config.api_key,
        private_key=config.api_secret,
        url_endpoint=config.api_url
    )

    result = imagekit.delete_file(file_id=file_id)

    if result.response_metadata.http_status_code != 204:
        print(f"Error deleting file {file_id}")
        raise Exception("Error deleting file")
    
    return
    

def extract_tags(config:ExternalApiConfig, image_url:str, confidence:int) -> list[dict]:
    response = requests.get(
        f"{config.api_url}/tags?image_url={image_url}",
        auth=(config.api_key, config.api_secret)
    )

    tags = [
        {
            "tag": tag["tag"]["en"],
            "confidence": tag["confidence"]
        }
        for tag in response.json()["result"]["tags"]
        if tag["confidence"] > confidence
    ]

    return tags

def load_image_from_file(path:str) -> str:
    with open(path, "rb") as file:
        content = file.read()
    return content

def get_image_size(path:str) -> int:
    # return size in KB
    return os.path.getsize(path) // 1024

