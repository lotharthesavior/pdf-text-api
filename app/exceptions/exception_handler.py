import logging

from flask import Blueprint, jsonify

exception_handler = Blueprint('exception_handler', __name__)

logger = logging.getLogger(__name__)

def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }).get_data()
    response.content_type = "application/json"
    return response
