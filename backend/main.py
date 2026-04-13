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
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def list_all_files():
    files = []
    continuation_token = None

    while True:
        if continuation_token:
            response = s3.list_objects_v2(
                Bucket=BUCKET,
                Prefix=FILE_KEY,
                ContinuationToken=continuation_token
            )
        else:
            response = s3.list_objects_v2(
                Bucket=BUCKET,
                Prefix=FILE_KEY
            )

        for obj in response.get("Contents", []):
            files.append(obj["Key"])

        # check if more files exist
        if response.get("IsTruncated"):
            continuation_token = response.get("NextContinuationToken")
        else:
            break

    return files   

def load_data():
    files = list_all_files()
    
    df_list = []
    
    for file_key in files:
        obj = s3.get_object(Bucket=BUCKET, Key=file_key)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        df_list.append(df)
    
    return pd.concat(df_list, ignore_index=True)

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
