from databricks import sql
import os
from dotenv import load_dotenv
load_dotenv()
conn = None

def get_connection():
    global conn
    if conn is None:
        conn = sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOST"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
    return conn