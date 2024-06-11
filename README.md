
# PDF Service

[![Run Tests and Generate Coverage](https://github.com/lotharthesavior/pdf-text-api/actions/workflows/test-and-coverage.yml/badge.svg)](https://github.com/lotharthesavior/pdf-text-api/actions/workflows/test-and-coverage.yml)

Aims to provide a simple service to extract content from PDFs via API.

## API

### PDF API

#### Endpoint: Extract Text from PDF

This endpoint is for extracting text from a specified page of a PDF file.

- **URL**: `/pdf-text`
- **Method**: `GET`
- **Description**: Extracts text from a specified page of a given PDF file.
- **Parameters**:
  - `pdf_file` (string, required): The name of the PDF file (must be in the `uploads` directory).
  - `page` (integer, required): The page number from which to extract text (1-based index).
- **Responses**:
  - `200 OK`: Successfully extracted text.
    - Content:
      ```json
      {
          "number_of_pages": int,
          "text": str,
          "page": int
      }
      ```
  - `400 Bad Request`: Invalid input parameters.
    - Content:
      ```json
      {
          "description": str
      }
      ```
  - `500 Internal Server Error`: Failed to extract text from the specified page.
    - Content:
      ```json
      {
          "description": str
      }
      ```

##### Request Example

**GET** `/extract-text?pdf_file=example.pdf&page=1`

##### Response Example

**Success (200 OK)**:
```json
{
    "number_of_pages": 5,
    "text": "Extracted text from the specified page...",
    "page": 1
}
```

**Error (400 Bad Request)**:
```json
{
    "description": "Parameter 'pdf_file' is required and must be a non-empty string."
}
```

**Error (500 Internal Server Error)**:
```json
{
    "description": "Failed to extract text from page 1: <error message>"
}
```

##### Detailed Explanation

1. **Validation**:
   - The `validate_text_input` function checks if `pdf_file` is a valid non-empty string, exists in the `uploads` directory, and has a `.pdf` extension.
   - It also validates that `page` is an integer.

2. **Text Extraction**:
   - The `extract_text_from_pdf` function uses `PdfReader` to read the specified PDF file and extract text from the given page.
   - The function logs the operation and handles any exceptions that occur during text extraction.

3. **Responses**:
   - Returns the total number of pages in the PDF, the extracted text, and the page number.
   - Handles and returns appropriate error messages for invalid inputs or extraction failures.

### Document Management API

This API provides endpoints for uploading, listing, retrieving, updating, and deleting documents. It is built using Flask and SQLAlchemy.

#### Upload Document

- **URL**: `/documents/`
- **Method**: `POST`
- **Description**: Upload a new document.
- **Request**:
  - Content-Type: `multipart/form-data`
  - Parameters: `file` (required)
- **Responses**:
  - `200 OK`: Document successfully uploaded.
  - `422 Unprocessable Entity`: No file part, no selected file, or file not allowed.

#### List Documents

- **URL**: `/documents/`
- **Method**: `GET`
- **Description**: List all documents.
- **Responses**:
  - `200 OK`: Returns a list of documents.

#### Retrieve Document

- **URL**: `/documents/<int:id>`
- **Method**: `GET`
- **Description**: Retrieve a document by its ID.
- **Responses**:
  - `200 OK`: Document found.
  - `404 Not Found`: No document found with the given ID.

#### Update Document

- **URL**: `/documents/<int:id>`
- **Method**: `PATCH`
- **Description**: Update a document's details.
- **Request**:
  - Content-Type: `application/json`
  - Parameters: `name`, `path`
- **Responses**:
  - `200 OK`: Document successfully updated.
  - `404 Not Found`: No document found with the given ID.

#### Delete Document

- **URL**: `/documents/<int:id>`
- **Method**: `DELETE`
- **Description**: Delete a document by its ID.
- **Responses**:
  - `204 No Content`: Document successfully deleted.
  - `404 Not Found`: No document found with the given ID.

