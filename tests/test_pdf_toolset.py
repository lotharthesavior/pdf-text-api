import os
import sys
import pytest
from moto import mock_aws

from app.database.factories.DocumentFactory import DocumentFactory

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db, create_app

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = 'test_uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STORAGE_TYPE = 'local'
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

@mock_aws
def test_cant_extract_text_from_pdf_with_invalid_page(client):
    document = DocumentFactory()
    document.path = "uploads/test.pdf"
    db.session.commit()

    dummy_file = document.path
    with open(dummy_file, "w") as f:
        f.write("This is a test file.")

    response = client.get(f'/pdf-text/{document.id}?page=invalid')
    assert response.status_code == 400
    assert b"Invalid page number" in response.data

    # Clean up the dummy file
    os.remove(dummy_file)

@mock_aws
def test_cant_extract_text_from_pdf_file_when_not_exist(client):
    document_id = 9999999
    response = client.get(f'/pdf-text/{document_id}?page=1')
    assert response.status_code == 404
    assert f"Document with id {document_id} not found." in str(response.data)

@mock_aws
def test_extract_text_from_pdf_success(client):
    document = DocumentFactory()
    document.path = "uploads/test.pdf"
    db.session.commit()

    # Create a dummy PDF file
    dummy_pdf = document.path
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(dummy_pdf, pagesize=letter)
    c.drawString(100, 750, "This is a test PDF file.")
    c.showPage()
    c.save()

    response = client.get(f"/pdf-text/{document.id}?page=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data['number_of_pages'] == 1
    assert "This is a test PDF file." in data['text']

    # Clean up the dummy PDF file
    os.remove(dummy_pdf)
