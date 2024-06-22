from app.storage import get_client

# Example usage:
# upload_file_to_minio('path/to/your/file.txt', 'my-bucket', 'file.txt')
def upload_file_to_minio(file_path, bucket_name, object_name):
    try:
        get_client().upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error occurred: {e}")
