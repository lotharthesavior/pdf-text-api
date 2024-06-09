from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
import os
import logging

documents = Blueprint('upload', __name__)

logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@documents.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        logger.info('No selected file')
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        logger.info(f'File {filename} uploaded')
        return 'File successfully uploaded'
    return 'File not allowed'
