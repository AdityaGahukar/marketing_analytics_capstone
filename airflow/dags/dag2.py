from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import boto3
import os

# ============================================================
# CONFIGURATION — Change these for each batch run
# ============================================================
STUDENT = "team2"
PROJECT = "marketing_analytics"
BATCH_ID = "batch_01"  # Change this: batch_02, batch_03, batch_04, batch_05

# Databricks notebook paths (update with your workspace path)


# Local batch file location (inside Airflow container)
# Astro CLI mounts the project folder to /usr/local/airflow/
LOCAL_BATCH_DIR = "/usr/local/airflow/batch_data"

default_args = {
    "owner": STUDENT,
    "depends_on_past": False,
    "retries": 0,
}


# with DAG(
#     dag_id="safecity360_abhinav_pipeline",
#     schedule=None,
#     start_date=datetime(2025, 1, 1),
#     catchup=False,
# ) as dag:






# ============================================================
# FUNCTION: Upload batch CSV from local folder to S3
# ============================================================
# def upload_batch_csv_to_s3(**kwargs):
#     """
#     Reads the batch CSV file from the local folder (mounted from Mac)
#     and uploads it to the correct S3 path using boto3.
#     """
#     batch_id = kwargs["batch_id"]
#     bucket = kwargs["bucket"]
#     project = kwargs["project"]


#     local_file = f"{LOCAL_BATCH_DIR}/crimes_2020_01.csv"
#     # local_file = f"{LOCAL_BATCH_DIR}/crimes_{batch_id}.csv"
#     s3_key = f"{project}/batch_data/{batch_id}/crimes_{batch_id}.csv"

#     if not os.path.exists(local_file):
#         raise FileNotFoundError(
#             f"Batch file not found: {local_file}\n"
#             f"Make sure you copied the CSV to your batch_data/ folder:\n"
#             f"  cp /path/to/crimes_{batch_id}.csv batch_data/"
#         )

#     s3 = boto3.client("s3", aws_access_key_id=AWS_KEY,
#         aws_secret_access_key=AWS_SECRET, region_name=REGION)

#     file_size = os.path.getsize(local_file)
#     print(f"Uploading {local_file} ({file_size} bytes) to s3://{bucket}/{s3_key}")
#     s3.upload_file(local_file, bucket, s3_key)
#     print(f"Upload complete: s3://{bucket}/{s3_key}")

# ============================================================
# DAG DEFINITION
# ============================================================
with DAG(
    dag_id="arnav_test_pipeline",
    default_args=default_args,
    description="marketing_analytics end-to-end DE pipeline",
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=[PROJECT, STUDENT],
) as dag:

    # TASK 1: Upload batch CSV from local Mac folder to S3
    # upload_csv_to_s3 = PythonOperator(
    #     task_id="upload_csv_to_s3",
    #     python_callable=upload_batch_csv_to_s3,
    #     op_kwargs={"batch_id": BATCH_ID, "bucket": BUCKET, "project": PROJECT},
    # )

    # TASK 2: Bronze
    run_bronze = DatabricksSubmitRunOperator(
    task_id="run_bronze",
    databricks_conn_id="databricks_default",
    json={
        "tasks": [
            {
                "task_key": "bronze_task",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/202251023@iiitvadodara.ac.in/marketing_analytics_capstone/notebooks/bronze_layer",
                    "base_parameters": {
                        "batch_id": "batch_01"
                    }
                }
            }
        ]
    }
)
    
    # upload_csv_to_s3 = PythonOperator(
    #     task_id="upload_csv_to_s3",
    #     python_callable=upload_batch_csv_to_s3,
    # )


    # run_bronze = DatabricksSubmitRunOperator(
    #     task_id="run_bronze",
    #     databricks_conn_id="databricks_default",
    # )

    

    
    # run_bronze = DatabricksSubmitRunOperator(
    #     task_id="run_bronze", databricks_conn_id="databricks_default",
    #     notebook_task={"notebook_path": f"{NOTEBOOK_ROOT}/01_bronze",
    #                    "base_parameters": {"batch_id": BATCH_ID}})

    # TASK 3: Silver

#     run_silver = DatabricksSubmitRunOperator(
#     task_id="run_silver",
#     databricks_conn_id="databricks_default",
#     json={
#         "tasks": [
#             {
#                 "task_key": "silver_task",
#                 "notebook_task": {
#                     "notebook_path": "/Workspace/Users/abhinav66623@gmail.com/SafeCity_1/02_silver"
#                 }
#             }
#         ]
#     }
# )
#     # run_silver = DatabricksSubmitRunOperator(
#     #     task_id="run_silver", databricks_conn_id="databricks_default",
#     #     notebook_task={"notebook_path": f"{NOTEBOOK_ROOT}/02_silver"})

#     # TASK 4: Gold

#     run_gold = DatabricksSubmitRunOperator(
#     task_id="run_gold",
#     databricks_conn_id="databricks_default",
#     json={
#         "tasks": [
#             {
#                 "task_key": "gold_task",
#                 "notebook_task": {
#                     "notebook_path": "/Workspace/Users/abhinav66623@gmail.com/SafeCity_1/03_gold"
#                 }
#             }
#         ]
#     }
# )
    
#     # run_gold = DatabricksSubmitRunOperator(
#     #     task_id="run_gold", databricks_conn_id="databricks_default",
#     #     notebook_task={"notebook_path": f"{NOTEBOOK_ROOT}/03_gold"})

#     # TASK 5: DQ Checks

#     run_dq = DatabricksSubmitRunOperator(
#     task_id="run_dq",
#     databricks_conn_id="databricks_default",
#     json={
#         "tasks": [
#             {
#                 "task_key": "dq",
#                 "notebook_task": {
#                     "notebook_path": "/Workspace/Users/abhinav66623@gmail.com/SafeCity_1/04_dq"
#                 }
#             }
#         ]
#     }
# )
    
#     # TASK 6: Export Gold to S3
#     export_gold_to_s3 = DatabricksSubmitRunOperator(
#     task_id="export_gold_to_s3",
#     databricks_conn_id="databricks_default",
#     json={
#         "tasks": [
#             {
#                 "task_key": "export_gold_to_s3",
#                 "notebook_task": {
#                     "notebook_path": f"{NOTEBOOK_ROOT}/05_export_gold_to_s3"
#                 }
#             }
#         ]
#     }
# )

#     # TASK 7: Refresh Snowflake
#     refresh_snowflake = SQLExecuteQueryOperator(
#         task_id="refresh_snowflake", conn_id="snowflake_default",
#         sql="""USE DATABASE SAFECITY360_DB; USE SCHEMA STAGING; USE WAREHOUSE SAFECITY360_WH;
#             TRUNCATE TABLE IF EXISTS STAGING.DIM_DATE; COPY INTO STAGING.DIM_DATE FROM @STAGING.SAFECITY360_STAGE/dim_date.parquet FILE_FORMAT=(TYPE='PARQUET') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
#             TRUNCATE TABLE IF EXISTS STAGING.DIM_DISTRICT; COPY INTO STAGING.DIM_DISTRICT FROM @STAGING.SAFECITY360_STAGE/dim_district.parquet FILE_FORMAT=(TYPE='PARQUET') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
#             TRUNCATE TABLE IF EXISTS STAGING.DIM_IUCR_CODE; COPY INTO STAGING.DIM_IUCR_CODE FROM @STAGING.SAFECITY360_STAGE/dim_iucr_code.parquet FILE_FORMAT=(TYPE='PARQUET') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
#             TRUNCATE TABLE IF EXISTS STAGING.DIM_LOCATION_TYPE; COPY INTO STAGING.DIM_LOCATION_TYPE FROM @STAGING.SAFECITY360_STAGE/dim_location_type.parquet FILE_FORMAT=(TYPE='PARQUET') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
#             TRUNCATE TABLE IF EXISTS STAGING.DIM_TIME_BLOCK; COPY INTO STAGING.DIM_TIME_BLOCK FROM @STAGING.SAFECITY360_STAGE/dim_time_block.parquet FILE_FORMAT=(TYPE='PARQUET') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
#             TRUNCATE TABLE IF EXISTS STAGING.FACT_CRIME_INCIDENTS; COPY INTO STAGING.FACT_CRIME_INCIDENTS FROM @STAGING.SAFECITY360_STAGE/fact_crime_incidents.parquet FILE_FORMAT=(TYPE='PARQUET') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
#             TRUNCATE TABLE IF EXISTS STAGING.FACT_MONTHLY_DISTRICT_SUMMARY; COPY INTO STAGING.FACT_MONTHLY_DISTRICT_SUMMARY FROM @STAGING.SAFECITY360_STAGE/fact_monthly_district_summary.parquet FILE_FORMAT=(TYPE='PARQUET') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
#         """)

#     # PIPELINE ORDER (7 tasks)
#     upload_csv_to_s3 >> run_bronze >> run_silver >> run_gold >> run_dq >> export_gold_to_s3 >> refresh_snowflake
