from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

from include.api_client import fetch_data
from include.offset_manager import get_offset, update_offset
from include.s3_utils import upload_json_to_s3
from include.config import S3_BUCKET, RAW_PREFIX

logger = logging.getLogger(__name__)


def ingest_api_to_s3():
    try:
        # Step 1: Get last offset
        offset = get_offset()
        logger.info(f"Starting from offset: {offset}")

        # Step 2: Fetch data
        response = fetch_data(offset)

        data = response.get("data", [])
        next_offset = response.get("next_offset")
        has_more = response.get("has_more")

        if not data:
            logger.info("No new data found")
            return

        # Step 3: Store in S3 (partitioned by timestamp)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        s3_key = f"{RAW_PREFIX}data_{timestamp}.json"

        upload_json_to_s3(S3_BUCKET, s3_key, data)

        # Step 4: Update offset
        update_offset(next_offset)

        logger.info(f"Offset updated to {next_offset}")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise


default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="api_to_s3_incremental",
    start_date=datetime(2024, 1, 1),
    schedule="*/15 * * * *",  # every 15 mins
    catchup=False,
    default_args=default_args,
    tags=["api", "s3", "incremental"]
) as dag:

    ingest_task = PythonOperator(
        task_id="fetch_and_store_api_data",
        python_callable=ingest_api_to_s3
    )