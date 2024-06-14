from flask import Blueprint, request, current_app, jsonify, make_response
from sqlalchemy import select
from werkzeug.utils import secure_filename
import os
import uuid

from app.components.storage import upload_file_to_minio
from app.logger import logger
from app.extensions import db
from app.models import Document

documents = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@documents.route('/', methods=['POST'])
def upload_file():
    error = False

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

        if (current_app.config['STORAGE_TYPE'] is 'minio'):
            upload_file_to_minio(filepath, current_app.config['STORAGE_DOCUMENTS_BUCKET'], unique_filename)
            logger.info(f'File {unique_filename} uploaded')

        document_record = Document(
            name=filename,
            path=filepath
        )
        db.session.add(document_record)
        db.session.commit()
        logger.info(f'Document {filename} persisted')
    except Exception as e:
        error = True
        db.session.rollback()
        logger.error(f'Error saving document.', {
            'error': str(e)
        })
        return make_response(jsonify({
            'status': 'error',
            'result': 'Internal Server Error',
            'error': str(e)
        }), 500)
    finally:
        if (current_app.config['STORAGE_TYPE'] is not 'local') or error:
            os.remove(filepath)

    return make_response(jsonify(document_record.to_dict()), 200)

@documents.route('/', methods=['GET'])
def list_documents():
    try:
        stmt = select(Document)
        results = db.session.execute(stmt).scalars().all()
        documents = [doc.to_dict() for doc in results]
    except Exception as e:
        logger.error('Error listing documents', {
            'error': str(e),
        })
        return make_response(jsonify({
            'status': 'error',
            'result': 'Internal Server Error',
            'error': str(e)
        }), 500)

    return (make_response(jsonify(documents), 200))

@documents.route('/<int:id>', methods=['GET'])
def get_document_by_id(id: int):
    try:
        document = db.session.get(Document, id)
        if document is None:
            return make_response(jsonify({
                'status': 'error',
                'result': f'No document found with id {id}'
            }), 404)

        document_dict = document.to_dict()
    except Exception as e:
        logger.error('Error getting document by id', {
            'error': str(e),
            'id': id
        })
        return make_response(jsonify({
            'status': 'error',
            'result': 'Internal Server Error',
            'error': str(e)
        }), 500)

    return make_response(jsonify(document_dict), 200)

@documents.route('/<int:id>', methods=['PATCH'])
def patch_document_by_id(id: int):
    try:
        document = db.session.get(Document, id)
        if document is None:
            return make_response(jsonify({
                'status': 'error',
                'result': f'No document found with id {id}'
            }), 404)

        data = request.json
        if 'name' in data:
            document.name = data['name']
        if 'path' in data:
            document.path = data['path']

        db.session.commit()
    except Exception as e:
        logger.error(f'Error patching document: {str(e)}', {
            'error': str(e),
            'id': id
        })
        return make_response(jsonify({
            'status': 'error',
            'result': 'Internal Server Error',
            'error': str(e)
        }), 500)

    return make_response(jsonify(document.to_dict()), 200)

@documents.route('/<int:id>', methods=['DELETE'])
def delete_document_by_id(id: int):
    try:
        document = db.session.get(Document, id)
        if document is None:
            return make_response(jsonify({
                'status': 'error',
                'result': f'No document found with id {id}'
            }), 404)

        db.session.delete(document)
        db.session.commit()
    except Exception as e:
        print(str(e))
        logger.error('Error getting document by id', {
            'error': str(e),
            'id': id
        })
        return make_response(jsonify({
            'status': 'error',
            'result': 'Internal Server Error',
            'error': str(e)
        }), 500)

    return make_response('', 204)