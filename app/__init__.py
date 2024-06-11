from app.components.documents import documents
from app.components.pdf_toolset import pdf_toolset
from app.exceptions.exception_handler import handle_http_exception
from app.extensions import db
from flask import Flask
from werkzeug.exceptions import HTTPException
from app.logger import logger

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    app.register_error_handler(HTTPException, handle_http_exception)

    # modules
    app.register_blueprint(documents, url_prefix='/documents')
    app.register_blueprint(pdf_toolset, url_prefix='/pdf-text')

    with app.app_context():
        db.create_all()

    return app
