import os
import uuid
from io import BytesIO
import pytest

from app import create_app
from app.database.factories.DocumentFactory import DocumentFactory
from app.extensions import db

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = 'test_uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)
    app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    if not os.path.exists('test_uploads'):
        os.makedirs('test_uploads')

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    # Clean up uploads folder after tests
    for filename in os.listdir('test_uploads'):
        file_path = os.path.join('test_uploads', filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)


@pytest.fixture
def client(app):
    return app.test_client()


def test_cant_upload_without_file(client):
    response = client.post('/documents/')
    assert response.status_code == 422
    assert 'No file part' in response.data.decode()


def test_cant_upload_when_no_selected_file(client):
    data = {
        'file': (None, '')
    }
    response = client.post('/documents/', data=data)
    assert response.status_code == 422
    assert 'No selected file' in response.data.decode()


def test_cant_upload_file_not_allowed_filetype(client):
    data = {
        'file': (BytesIO(b"dummy data"), 'test.exe')
    }
    response = client.post('/documents/', data=data, content_type='multipart/form-data')
    print(response.data)
    assert response.status_code == 422
    assert 'File not allowed' in response.data.decode()

def test_upload_file_successfully(client, monkeypatch):
    # Mock the UUID generation to get a predictable filename
    test_uuid = uuid.uuid4()
    monkeypatch.setattr(uuid, 'uuid4', lambda: test_uuid)

    data = {
        'file': (BytesIO(b"dummy data"), 'test.txt')
    }
    response = client.post('/documents/', data=data, content_type='multipart/form-data')

    expected_filename = f"{test_uuid}_test.txt"
    expected_filepath = os.path.join('test_uploads', expected_filename)

    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['name'] == 'test.txt'
    assert os.path.exists(expected_filepath)

    # Clean up
    if os.path.exists(expected_filepath):
        os.remove(expected_filepath)

def test_list_documents_successfully(client, monkeypatch):
    document1 = DocumentFactory()
    db.session.commit()

    document2 = DocumentFactory()
    db.session.commit()

    response = client.get('/documents/')
    assert response.status_code == 200

    response_json = response.get_json()
    assert len(response_json) == 2
    assert response_json[0]['name'] == document1.name
    assert response_json[1]['name'] == document2.name
