from flask import Blueprint, request, jsonify, abort, current_app
from pypdf import PdfReader, PdfWriter
import logging

from pypdf.generic import NameObject, ArrayObject

from app.logger import logger
from app.models import Document
import io

from app.storage import get_client

pdf_toolset = Blueprint('pdf_toolset', __name__)

def get_document_record_by_id(document_id):
    document = Document.query.filter_by(id=document_id).first()
    if not document:
        logger.error(f"Document with id {document_id} not found.")
        abort(404, description=f"Document with id {document_id} not found.")
    return document

def sanitize_pdf(input, output):
    print(f"Sanitizing PDF {input} to {output}")

    with open(input, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()

        writer.add_metadata({})

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]

            if "/Annots" in page:
                page[NameObject("/Annots")] = ArrayObject()

            writer.add_page(page)

        with open(output, 'wb') as output_file:
            print(f"Writing sanitized PDF to {output}")
            writer.write(output_file)

@pdf_toolset.route('/<int:id>', methods=['GET'])
def extract_text_from_pdf(id: int):
    page = request.args.get('page')
    logging.info(f"Extracting text from page {page} of document {id}")

    document = get_document_record_by_id(id)

    try:
        page = int(page)
    except Exception as e:
        logger.error(f"Invalid page number: {str(e)}")
        abort(400, description=f"Invalid page number: {str(e)}")

    if (current_app.config['STORAGE_TYPE'] == 'minio'):
        response_object = get_client().get_object(Bucket=current_app.config['STORAGE_DOCUMENTS_BUCKET'], Key=document.unique_name)
        pdf_data = response_object['Body'].read()
        pdf_stream = io.BytesIO(pdf_data)
        reader = PdfReader(pdf_stream)
    else:
        reader = PdfReader(f"{document.path}")

    number_of_pages = len(reader.pages)

    try:
        text = reader.pages[int(page) - 1].extract_text()
    except Exception as e:
        logger.error(f"Failed to extract text from page {page}: {str(e)}")
        abort(500, description=f"Failed to extract text from page {page}: {str(e)}")

    logger.info(f"Successfully extracted text from page {page} of document {id}")
    return jsonify({
        "document_name": document.name,
        "number_of_pages": number_of_pages,
        "text": text,
        "page": page
    })
