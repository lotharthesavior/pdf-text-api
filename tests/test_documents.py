import os
import uuid
from io import BytesIO

import boto3
from moto import mock_aws
import pytest

from app import create_app
from app.database.factories.DocumentFactory import DocumentFactory
from app.extensions import db
from app.models import Document

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = 'test_uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STORAGE_TYPE = 'minio'
    STORAGE_URL = None
    STORAGE_ACCESS_KEY = 'fake_access_key'
    STORAGE_SECRET_KEY = 'fake_secret_key'
    STORAGE_REGION = 'us-east-1'
    STORAGE_DOCUMENTS_BUCKET = 'test_bucket'
    PDF_SANITIZE = False

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
    assert response.status_code == 422
    assert 'File not allowed' in response.data.decode()

@mock_aws
def test_upload_file_successfully_with_s3(client, monkeypatch):
    # Create a bucket
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket=TestConfig.STORAGE_DOCUMENTS_BUCKET)

    # Mock the UUID generation to get a predictable filename
    test_uuid = uuid.uuid4()
    monkeypatch.setattr(uuid, 'uuid4', lambda: test_uuid)

    data = {
        'file': (BytesIO(b"dummy data"), 'test.txt')
    }

    response = client.post('/documents/', data=data, content_type='multipart/form-data')

    expected_filename = f"{test_uuid}_test.txt"
    expected_filepath = os.path.join('test_uploads', expected_filename)

    body = conn.Object(TestConfig.STORAGE_DOCUMENTS_BUCKET, expected_filename).get()["Body"].read().decode("utf-8")

    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['name'] == 'test.txt'
    assert(body == "dummy data")

    # Clean up
    if os.path.exists(expected_filepath):
        os.remove(expected_filepath)

def test_upload_file_successfully(app, client, monkeypatch):
    # Mock the UUID generation to get a predictable filename
    test_uuid = uuid.uuid4()
    monkeypatch.setattr(uuid, 'uuid4', lambda: test_uuid)

    with app.app_context():
        app.config['STORAGE_TYPE'] = 'local'

        test_uuid = uuid.uuid4()
        monkeypatch.setattr(uuid, 'uuid4', lambda: test_uuid)

        data = {
            'file': (BytesIO(b"dummy data"), 'test.txt')
        }

        response = client.post('/documents/', data=data, content_type='multipart/form-data')

        expected_filename = f"{test_uuid}_test.txt"
        expected_filepath = os.path.join('test_uploads', expected_filename)
        cleaned_expected_filepath = os.path.join('test_uploads', f"cleaned-{expected_filename}")

        assert response.status_code == 200
        assert os.path.exists(cleaned_expected_filepath)
        response_json = response.get_json()
        assert response_json['name'] == 'test.txt'

        # Clean up
        if os.path.exists(expected_filepath):
            os.remove(expected_filepath)

        if os.path.exists(cleaned_expected_filepath):
            os.remove(cleaned_expected_filepath)

def test_list_documents_successfully(client):
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

def test_get_single_document_successfully(client):
    document = DocumentFactory()
    db.session.commit()

    response = client.get(f'/documents/{document.id}')
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json['id'] == document.id
    assert response_json['name'] == document.name
    assert response_json['path'] == document.path

def test_can_patch_document_successfully(client):
    document = DocumentFactory(name='old_name.txt')
    db.session.commit()
    expected_name = 'new_name.txt'

    response = client.patch(f'/documents/{document.id}', json={
        'name': expected_name
    })
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json['name'] == expected_name

def test_can_delete_document_successfully(client):
    document = DocumentFactory()
    db.session.commit()

    response = client.delete(f'/documents/{document.id}')
    assert response.status_code == 204

    assert db.session.get(Document, document.id) is None

def test_upload_file_too_large(app, client):
    large_data = b"a" * (4 * 1024 * 1024 + 1)  # 4MB + 1 byte
    data = {
        'file': (BytesIO(large_data), 'large_test.txt')
    }

    response = client.post('/documents/', data=data, content_type='multipart/form-data')
    assert response.status_code == 422
    assert response.get_json() == {
        'status': 'error',
        'result': 'File exceeds size limit of 4MB'
    }
