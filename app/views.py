from datetime import datetime
from flask import Blueprint, make_response, request, current_app
from .config.config import Config
from . import controller

bp = Blueprint('images', __name__, url_prefix='/')

@bp.post("/image")
def post_image():
    """Expects a request with 
    - query param:
    min_confidence (*optional*): enforce a minimum confidence in
    the labeling process

    - body:
    {"data": "<base64-encoded-image-string>"} 
    """
    try:
        min_confidence = int(request.args.get("min_confidence", 80))
    except:
        return make_response({"error": "invalid parameter value (min_confidence)"}, 400)
    
    # image comes in base64
    image = request.json['data']
    if image == "":
        return make_response("The body must include the field data", 400)

    cfg:Config = current_app.config["config"]

    try:
        response = controller.process_image(cfg.app, image, min_confidence)
    except Exception as e:
        return make_response({"error": str(e)}, 500)

    return make_response(response, 200)

@bp.get("/images")
def get_images():
    """Expects a request with
    - query param:
    min_date/ max_date (*optional*): filter images by date in the format YYYY-MM-DD HH:MM:SS
        If min_date is not provided, it will not be considered in the filter
        If max_date is not provided, it will not be considered in the filter
    tags (*optional*): filter images by a tag list string separated by commas. Results must include all tags
        Example tags="tag1,tag2,tag3"

    Returns:
        content: a list of objects with the following structure:
        {
            "id": "<image-id>",
            "size": "<image-size-kb>",
            "date": "<image-date>",
            "tags": [{"tag": "<tag>", "confidence": "<confidence>"}],
        }
    """
    try:
        # parse dates to datetime with the given format and tags from query params
        min_date = request.args.get("min_date", None)
        min_date = datetime.strptime(min_date, "%Y-%m-%d %H:%M:%S") if min_date else None
    except:
        return make_response({"error": "invalid parameter value (min_date)"}, 400)
    try:
        max_date = request.args.get("max_date", None)
        max_date = datetime.strptime(max_date, "%Y-%m-%d %H:%M:%S") if max_date else None
    except:
        return make_response({"error": "invalid parameter value (max_date)"}, 400)
    try:
        tags = request.args.get("tags", None)
        if tags:
            tags = tags.replace(' ', '').split(",")
    except:
        return make_response({"error": "invalid parameter value (tags)"}, 400)
    
    try:
        response = controller.fetch_images(min_date, max_date, tags)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    
    return make_response(response, 200)

@bp.get("/image/<image_id>")
def get_image(image_id):
    """Expects a request with
    - path param:
    id: the image id to fetch

    Returns:
        The image information with the following structure:
        {
            "id": "<image-id>",
            "size": "<image-size-kb>",
            "date": "<image-date>",
            "tags": [{"tag": "<tag>", "confidence": "<confidence>"}],
            "data": "<base64-encoded-image-string>"
        }
    """
    if not image_id:
        return make_response({"error": "invalid parameter value (id)"}, 400)
    
    try:
        response = controller.fetch_image(image_id)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    
    return make_response(response, 200)

@bp.get("/tags")
def get_tags():
    """Expects a request with
    - query param:
    min_date/ max_date (*optional*): filter tags by date in the format YYYY-MM-DD HH:MM:SS
        If min_date is not provided, it will not be considered in the filter
        If max_date is not provided, it will not be considered in the filter

    Returns:
        content: a list of objects with the following structure:
        {
            "tag": "<tag>",
            "n_images": <number of images with this tag>
            "min_confidence": <minimum confidence of the tag>
            "max_confidence": <maximum confidence of the tag>
            "mean_confidence": <mean confidence of the tag>
        }
    """
    try:
        # parse dates to datetime with the given format
        min_date = request.args.get("min_date", None)
        min_date = datetime.strptime(min_date, "%Y-%m-%d %H:%M:%S") if min_date else None
    except:
        return make_response({"error": "invalid parameter value (min_date)"}, 400)
    try:
        max_date = request.args.get("max_date", None)
        max_date = datetime.strptime(max_date, "%Y-%m-%d %H:%M:%S") if max_date else None
    except:
        return make_response({"error": "invalid parameter value (max_date)"}, 400)
    
    try:
        tags = controller.fetch_tags(min_date, max_date)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
    
    response = [ 
        {
            "tag": tag.tag,
            "n_images": tag.n_images,
            "min_confidence": tag.min_confidence,
            "max_confidence": tag.max_confidence,
            "mean_confidence": tag.mean_confidence
        }
        for tag in tags
    ]
    
    return make_response(response, 200)