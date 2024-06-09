import os
from dotenv import dotenv_values

config = dotenv_values(".env")

class Config:
    SQLALCHEMY_DATABASE_URI = config['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf'}
