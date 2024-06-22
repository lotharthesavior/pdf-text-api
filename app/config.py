from dotenv import dotenv_values

config = dotenv_values(".env")

class Config:
    SQLALCHEMY_DATABASE_URI = config['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = config.get('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf'}
    # Storage configuration
    STORAGE_TYPE = config.get('STORAGE_TYPE', 'local')
    STORAGE_DOCUMENTS_BUCKET = config.get('STORAGE_DOCUMENTS_BUCKET', None)
    STORAGE_BUCKET_PATH = config.get('STORAGE_BUCKET_PATH', '/')
    STORAGE_URL = config.get('STORAGE_URL', None)
    STORAGE_ACCESS_KEY = config.get('STORAGE_ACCESS_KEY', None)
    STORAGE_SECRET_KEY = config.get('STORAGE_SECRET_KEY', None)
    STORAGE_REGION = config.get('STORAGE_REGION', None)
    # PDF configuration
    PDF_SANITIZE = config.get('PDF_SANITIZE', False)

