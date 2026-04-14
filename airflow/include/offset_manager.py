from include.s3_utils import read_json_from_s3, upload_json_to_s3
from include.config import S3_BUCKET, OFFSET_KEY


def get_offset():
    data = read_json_from_s3(S3_BUCKET, OFFSET_KEY)
    if data is None:
        return 0
    
    print(f"Offset we get is {data.get('offset',0)}")
    return data.get("offset", 0)


def update_offset(new_offset):
    upload_json_to_s3(
        S3_BUCKET,
        OFFSET_KEY,
        {"offset": new_offset}
    )