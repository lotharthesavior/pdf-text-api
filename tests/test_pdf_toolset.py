import os
import sys
import pytest
from flask import Flask
from werkzeug.exceptions import HTTPException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import handle_http_exception
from components.pdf_toolset import pdf_toolset

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(pdf_toolset, url_prefix='/pdf_toolset')
    app.register_error_handler(HTTPException, handle_http_exception)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_cant_extract_text_from_pdf_without_pdf_file(client):
    response = client.get('/pdf_toolset/')
    assert response.status_code == 400
    assert b"Parameter 'pdf_file' is required and must be a non-empty string." in response.data

def test_cant_extract_text_from_pdf_with_invalid_page(client):
    dummy_file = "uploads/test.pdf"
    with open(dummy_file, "w") as f:
        f.write("This is a test file.")

    response = client.get('/pdf_toolset/?pdf_file=test.pdf&page=invalid')
    assert response.status_code == 400
    assert b"Parameter 'page' must be an integer." in response.data

    # Clean up the dummy file
    os.remove(dummy_file)

def test_cant_extract_text_from_pdf_file_when_not_exist(client):
    response = client.get('/pdf_toolset/?pdf_file=nonexistent.pdf&page=1')
    assert response.status_code == 400
    assert b"The specified file does not exist." in response.data

def test_extract_text_from_pdf_not_pdf(client):
    # Create a dummy file
    dummy_file = "uploads/test.txt"
    with open(dummy_file, "w") as f:
        f.write("This is a test file.")

    response = client.get('/pdf_toolset/?pdf_file=test.txt&page=1')
    assert response.status_code == 400
    assert b"The specified file must be a PDF." in response.data

    # Clean up the dummy file
    os.remove(dummy_file)

def test_extract_text_from_pdf_success(client):
    # Create a dummy PDF file
    dummy_pdf = "uploads/test.pdf"
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(dummy_pdf, pagesize=letter)
    c.drawString(100, 750, "This is a test PDF file.")
    c.showPage()
    c.save()

    response = client.get('/pdf_toolset/?pdf_file=test.pdf&page=1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['number_of_pages'] == 1
    assert "This is a test PDF file." in data['text']

    # Clean up the dummy PDF file
    os.remove(dummy_pdf)
