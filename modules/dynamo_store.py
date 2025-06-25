import boto3
import os
import uuid
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

TABLE_NAME = "PDFMetadata"  # ← Make sure this table exists with 'id' as primary key

import uuid

def save_pdf_metadata(filename, s3_url, chunk_count):
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.put_item(Item={
            "id": filename,
            "s3_url": s3_url,
            "chunk_count": chunk_count
        })
        print(f"📄 Metadata saved for {filename}")
        return response
    except Exception as e:
        print(f"❌ DynamoDB save failed for {filename}: {e}")
        return None

