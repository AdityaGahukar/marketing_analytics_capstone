from fastapi import FastAPI
import pandas as pd
import boto3
import io
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")

BUCKET = os.getenv("S3_BUCKET")
FILE_KEY = os.getenv("S3_FILE_KEY")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)



def load_data():
    obj = s3.get_object(Bucket=BUCKET, Key=FILE_KEY)
    return pd.read_csv(io.BytesIO(obj['Body'].read()))

df = load_data()

@app.get("/get-data")
def get_data(offset: int = 0):
    start = offset
    end = offset + BATCH_SIZE
    
    data = df.iloc[start:end].to_dict(orient="records")
    
    return {
        "next_offset": end,
        "data": data,
        "has_more": end < len(df)
    }
