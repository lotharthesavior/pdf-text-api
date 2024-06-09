import os
import sys
from io import BytesIO
import pytest
from flask import Flask

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.components.documents import documents

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.register_blueprint(documents, url_prefix='/documents')

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    yield app

    # Clean up uploads folder after tests
    for filename in os.listdir('uploads'):
        file_path = os.path.join('uploads', filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)


@pytest.fixture
def client(app):
    return app.test_client()


def test_cant_upload_without_file(client):
    response = client.post('/upload/')
    assert response.data == b'No file part'
    assert response.status_code == 200


def test_cant_upload_when_no_selected_file(client):
    data = {
        'file': (None, '')
    }
    response = client.post('/upload/', data=data)
    assert response.data == b'No selected file'
    assert response.status_code == 200


def test_cant_upload_file_not_allowed_filetype(client):
    data = {
        'file': (BytesIO(b"dummy data"), 'test.exe')
    }
    response = client.post('/upload/', data=data, content_type='multipart/form-data')
    assert response.data == b'File not allowed'
    assert response.status_code == 200


def test_upload_file_successfully(client):
    data = {
        'file': (BytesIO(b"dummy data"), 'test.txt')
    }
    response = client.post('/upload/', data=data, content_type='multipart/form-data')
    assert response.data == b'File successfully uploaded'
    assert response.status_code == 200
    assert os.path.exists(os.path.join('uploads', 'test.txt'))
