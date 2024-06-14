from dotenv import dotenv_values

config = dotenv_values(".env")

class Config:
    SQLALCHEMY_DATABASE_URI = config['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf'}
    STORAGE_TYPE = config['STORAGE_TYPE']
    STORAGE_URL = config['STORAGE_URL']
    STORAGE_ACCESS_KEY = config['STORAGE_ACCESS_KEY']
    STORAGE_SECRET_KEY = config['STORAGE_SECRET_KEY']
    STORAGE_REGION = config['STORAGE_REGION']

