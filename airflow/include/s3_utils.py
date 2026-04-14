import boto3
import json
import logging

logger = logging.getLogger(__name__)

s3 = boto3.client("s3")
print(s3.list_buckets())


def upload_json_to_s3(bucket, key, data):
    try:
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(data)
        )
        logger.info(f"Uploaded data to {key}")
    except Exception as e:
        logger.error(f"Error uploading to S3: {str(e)}")
        raise


def read_json_from_s3(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return json.loads(response['Body'].read())
    except s3.exceptions.NoSuchKey:
        logger.warning("Offset file not found, starting from 0")
        return None
    except Exception as e:
        logger.error(f"Error reading from S3: {str(e)}")
        raise