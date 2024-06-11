from flask import Blueprint, request, current_app, jsonify, make_response
from sqlalchemy import select
from werkzeug.utils import secure_filename
import os
import logging
import uuid

from app.extensions import db
from app.models import Document

documents = Blueprint('upload', __name__)

logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@documents.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return make_response(jsonify({
            'status': 'error',
            'result': 'No file part'
        }), 422)

    file = request.files['file']

    if file.filename == '':
        logger.info('No selected file')
        return make_response(jsonify({
            'status': 'error',
            'result': 'No selected file'
        }), 422)

    if file and not allowed_file(file.filename):
        return make_response(jsonify({
            'status': 'error',
            'result': 'File not allowed'
        }), 422)

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

    try:
        file.save(filepath)
        logger.info(f'File {filename} uploaded')

        document_record = Document(
            name=filename,
            path=filepath
        )
        db.session.add(document_record)
        db.session.commit()
        logger.info(f'Document {filename} persisted')
    except Exception as e:
        db.session.rollback()
        os.remove(filepath)
        logger.error(f'Error saving document: {e}')
        return make_response(jsonify({
            'status': 'error',
            'result': 'Internal Server Error',
            'error': str(e)
        }), 500)

    return make_response(jsonify(document_record.to_dict()), 200)

@documents.route('/', methods=['GET'])
def list_documents():
    try:
        stmt = select(Document)
        results = db.session.execute(stmt).scalars().all()
        documents = [doc.to_dict() for doc in results]
    except Exception as e:
        return make_response(jsonify({
            'status': 'error',
            'result': 'Internal Server Error',
            'error': str(e)
        }), 500)

    return make_response(jsonify(documents), 200)