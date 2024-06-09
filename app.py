from flask import jsonify
from db import create_app
import logging
from werkzeug.exceptions import HTTPException

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)

app = create_app()

def handle_http_exception(e):
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }).get_data()
    response.content_type = "application/json"
    return response

app.register_error_handler(HTTPException, handle_http_exception)

@app.route("/")
def home():
    return "{status: 'ok'}"

if __name__ == '__main__':
    app.run(debug=True)