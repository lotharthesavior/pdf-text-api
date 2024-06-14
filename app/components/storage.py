from flask import current_app
import boto3
from botocore.client import Config

# Example usage:
# upload_file_to_minio('path/to/your/file.txt', 'my-bucket', 'file.txt')
def upload_file_to_minio(file_path, bucket_name, object_name):
    minio_url = current_app.config['STORAGE_URL']
    access_key = current_app.config['STORAGE_ACCESS_KEY']
    secret_key = current_app.config['STORAGE_SECRET_KEY']
    region_name = current_app.config['STORAGE_REGION']

    # Initialize a session using MinIO credentials
    s3_client = boto3.client(
        's3',
        endpoint_url=minio_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4'),
        region_name=region_name
    )

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error occurred: {e}")
