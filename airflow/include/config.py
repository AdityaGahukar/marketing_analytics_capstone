import os

API_URL = os.getenv("API_URL")

S3_BUCKET = os.getenv("S3_BUCKET")
RAW_PREFIX = "MarketingAnalytics_Team2_AWS/raw/"

OFFSET_KEY = "MarketingAnalytics_Team2_AWS/metadata/offset.json"

BATCH_SIZE = 100