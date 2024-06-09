from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from components.upload import insight_upload
from components.pdf_toolset import pdf_toolset

db = SQLAlchemy()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # modules
    app.register_blueprint(insight_upload, url_prefix='/upload')
    app.register_blueprint(pdf_toolset, url_prefix='/pdf-text')

    with app.app_context():
        db.create_all()

    return app
