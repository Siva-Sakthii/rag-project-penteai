import boto3
import os

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = "pdf-query-siva"

def upload_file_to_s3(file_path, s3_key):
    try:
        s3.upload_file(file_path, BUCKET_NAME, s3_key)
        return f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{s3_key}"
    except Exception as e:
        print("❌ S3 Upload Failed:", e)
        return None
