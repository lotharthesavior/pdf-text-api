
# PDF Service

[![Run Tests and Generate Coverage](https://github.com/lotharthesavior/pdf-text-api/actions/workflows/test-and-coverage.yml/badge.svg)](https://github.com/lotharthesavior/pdf-text-api/actions/workflows/test-and-coverage.yml)

Aims to provide a simple service to extract content from PDFs via API.

## API

### PDF API

### Updated Documentation for the `extract_text_from_pdf` Endpoint

#### Endpoint: Extract Text from PDF

This endpoint extracts text from a specified page of a PDF file.

- **URL**: `/pdf-text/<int:id>?page=<int:page>`
- **Method**: `GET`
- **Description**: Extracts text from a specified page of a given PDF file (by document id).
- **Responses**:
  - `200 OK`: Successfully extracted text.
    - Content:
      ```json
      {
          "document_name": "str",
          "number_of_pages": int,
          "text": "str",
          "page": int
      }
      ```
  - `400 Bad Request`: Invalid input parameters.
    - Content:
      ```json
      {
          "description": "str"
      }
      ```
  - `404 Not Found`: Document not found.
    - Content:
      ```json
      {
          "description": "Document with id <id> not found."
      }
      ```
  - `500 Internal Server Error`: Failed to extract text from the specified page.
    - Content:
      ```json
      {
          "description": "str"
      }
      ```

##### Request Example

**GET** `/pdf-text/1?page=1`

##### Response Examples

**Success (200 OK)**:
```json
{
    "document_name": "example.pdf",
    "number_of_pages": 3,
    "text": "This is the text extracted from page 1.",
    "page": 1
}
```

**Error (400 Bad Request)**:
```json
{
    "description": "Invalid page number: <error_message>"
}
```

**Error (404 Not Found)**:
```json
{
    "description": "Document with id 1 not found."
}
```

**Error (500 Internal Server Error)**:
```json
{
    "description": "Failed to extract text from page 1: <error_message>"
}
```

##### Detailed Explanation

1. **Validation**:
   - The endpoint retrieves the document text by its ID. If the document is not found, a `404 Not Found` error is returned.
   - If the validation fails, a `400 Bad Request` error is returned.

2. **Responses**:
   - **Success (200 OK)**: Returns the document name, total number of pages, extracted text, and the page number.
   - **Error (400 Bad Request)**: Returns a description of the error if the input parameters are invalid.
   - **Error (404 Not Found)**: Returns a description if the document is not found.
   - **Error (500 Internal Server Error)**: Returns a description of the error if text extraction fails.

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

