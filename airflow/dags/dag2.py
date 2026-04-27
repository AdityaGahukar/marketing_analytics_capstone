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



# ============================================================
# DAG DEFINITION
# ============================================================
with DAG(
    dag_id="run_etl_pipeline",
    default_args=default_args,
    description="marketing_analytics end-to-end DE pipeline",
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=[PROJECT, STUDENT],
) as dag:

    # # TASK 1: Upload batch CSV from local Mac folder to S3
    # upload_csv_to_s3 = PythonOperator(
    #     task_id="upload_csv_to_s3",
    #     python_callable=upload_batch_csv_to_s3,
    #     op_kwargs={"batch_id": BATCH_ID, "bucket": BUCKET, "project": PROJECT},
    # )

    # TASK 1: Bronze
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
    
 

    # TASK 2: Silver

    run_silver = DatabricksSubmitRunOperator(
    task_id="run_silver",
    databricks_conn_id="databricks_default",
    json={
        "tasks": [
            {
                "task_key": "silver_task",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/202251023@iiitvadodara.ac.in/marketing_analytics_capstone/notebooks/silver_layer"
                }
            }
        ]
    }
)
    

#   TASK 3.   Run silver Data quality checks
    run_silver_dq = DatabricksSubmitRunOperator(
    task_id="run_silver_data_quality",
    databricks_conn_id="databricks_default",
    json={
        "tasks": [
            {
                "task_key": "silver_task",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/202252302@iiitvadodara.ac.in/marketing_analytics_capstone/notebooks/Silver_dataquality_version2"
                }
            }
        ]
    }
)
    
    run_gold= DatabricksSubmitRunOperator(
    task_id="run_gold_layer",
    databricks_conn_id="databricks_default",
    json={
        "tasks": [
            {
                "task_key": "gold_task",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/202251023@iiitvadodara.ac.in/marketing_analytics_capstone/notebooks/gold_layer"
                }
            }
        ]
    }
)
    
    run_gold_dq= DatabricksSubmitRunOperator(
    task_id="run_gold__data_quality_layer",
    databricks_conn_id="databricks_default",
    json={
        "tasks": [
            {
                "task_key": "gold_quality_task",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/202251023@iiitvadodara.ac.in/marketing_analytics_capstone/notebooks/data_quality_check_gold_layer"
                }
            }
        ]
    }
)





    snowflake_step = SQLExecuteQueryOperator(
        task_id="snowflake_transformation",
        conn_id="snowflake_default",
        sql="sql/snowflake_t2.sql"
    )


run_bronze >> run_silver >>run_silver_dq>>  run_gold >> run_gold_dq >> snowflake_step

# run_silver_dq>>snowflake_step


# snowflake_step