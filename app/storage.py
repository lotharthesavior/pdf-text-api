from flask import current_app
import boto3
from botocore.client import Config

def get_client():
    minio_url = current_app.config['STORAGE_URL']
    access_key = current_app.config['STORAGE_ACCESS_KEY']
    secret_key = current_app.config['STORAGE_SECRET_KEY']
    region_name = current_app.config['STORAGE_REGION']

    return boto3.client(
        's3',
        endpoint_url=minio_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4'),
        region_name=region_name
    )