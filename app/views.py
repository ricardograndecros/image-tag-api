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
    return make_response({"error": "not implemented"}, 500)

@bp.get("/image")
def get_image():
    return make_response({"error": "not implemented"}, 500)

@bp.get("/tags")
def get_tags():
    return make_response({"error": "not implemented"}, 500)