from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

_conn = None

def get_connection():
    global _conn
    if _conn is None or getattr(_conn, 'closed', True):
        _conn = sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOST"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
    return _conn

def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        
        # 🔥 Fetch data as an Arrow table (much faster than fetchall)
        arrow_table = cursor.fetchall_arrow()
        
        if arrow_table is None:
            return []
            
        # 🔥 Convert the Arrow table directly to a list of dictionaries
        return arrow_table.to_pylist()
        
    finally:
        cursor.close()