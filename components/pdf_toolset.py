from flask import Blueprint, request, jsonify, abort
from pypdf import PdfReader
import logging
import os

pdf_toolset = Blueprint('pdf_toolset', __name__)

logger = logging.getLogger(__name__)

def validate_text_input(pdf_file: str, page):
    # Validate pdf_file
    if not pdf_file or not isinstance(pdf_file, str):
        abort(400, description="Parameter 'pdf_file' is required and must be a non-empty string.")

    file_path = f"uploads/{pdf_file}"
    if not os.path.exists(file_path):
        abort(400, description="The specified file does not exist.")

    if not pdf_file.lower().endswith('.pdf'):
        abort(400, description="The specified file must be a PDF.")

    # Validate page
    try:
        page = int(page)
    except (ValueError, TypeError):
        abort(400, description="Parameter 'page' must be an integer.")

@pdf_toolset.route('/', methods=['GET'])
def extract_text_from_pdf():
    pdf_file = request.args.get('pdf_file')
    page = request.args.get('page')
    logging.info(f"Extracting text from page {page} of {pdf_file}")
    validate_text_input(pdf_file, page)

    reader = PdfReader(f"uploads/{pdf_file}")
    number_of_pages = len(reader.pages)

    try:
        text = reader.pages[int(page) - 1].extract_text()
    except Exception as e:
        abort(500, description=f"Failed to extract text from page {page}: {str(e)}")

    return jsonify({
        "number_of_pages": number_of_pages,
        "text": text,
        "page": page
    })
