import os

API_URL = os.getenv("API_URL")

S3_BUCKET = os.getenv("S3_BUCKET")
RAW_PREFIX = "raw/"

OFFSET_KEY = "metadata/offset.json"

BATCH_SIZE = 1000