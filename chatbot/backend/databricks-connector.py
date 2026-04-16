from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

def run_query(query):

    conn = sql.connect(
        server_hostname=os.getenv("DATABRICKS_HOST"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN")
    )

    cursor = conn.cursor()
    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(zip(columns, row)) for row in rows]