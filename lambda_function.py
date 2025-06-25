import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("QueryMetrics")  # Replace if your table name differs

def lambda_handler(event, context):
    try:
        if "body" in event and isinstance(event["body"], str):
            event = json.loads(event["body"])

        print("📥 Event received:", event)

        query_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        item = {
            "query_id": query_id,
            "question": event.get("question", "N/A"),
            "answer": event.get("answer", "N/A"),
            "source": event.get("source", "unknown"),
            "timestamp": timestamp
        }

        table.put_item(Item=item)
        print("✅ Stored in DynamoDB")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Stored successfully", "id": query_id})
        }

    except Exception as e:
        print("❌ Lambda error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
