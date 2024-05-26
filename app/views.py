from flask import Blueprint, make_response

bp = Blueprint('images', __name__, url_prefix='/')

@bp.post("/image")
def post_image():
    return make_response({"error": "not implemented"}, 500)

@bp.get("/images")
def get_images():
    return make_response({"error": "not implemented"}, 500)

@bp.get("/image")
def get_image():
    return make_response({"error": "not implemented"}, 500)

@bp.get("/tags")
def get_tags():
    return make_response({"error": "not implemented"}, 500)