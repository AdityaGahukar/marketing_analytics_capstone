# from databricks import sql
# import os
# from dotenv import load_dotenv
# from globalconn import get_connection
# load_dotenv()
# # conn = sql.connect(
# #         server_hostname=os.getenv("DATABRICKS_HOST"),
# #         http_path=os.getenv("DATABRICKS_HTTP_PATH"),
# #         access_token=os.getenv("DATABRICKS_TOKEN")
# #     )

# _conn = None

#     # conn = sql.connect(
#     #     server_hostname=os.getenv("DATABRICKS_HOST"),
#     #     http_path=os.getenv("DATABRICKS_HTTP_PATH"),
#     #     access_token=os.getenv("DATABRICKS_TOKEN")
#     # )

# conn=get_connection()

# def run_query(query):
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute(query)
        
#         # 🔥 Fetch data as an Arrow table (much faster than fetchall)
#         arrow_table = cursor.fetchall_arrow()
        
#         if arrow_table is None:
#             return []
            
#         # 🔥 Convert the Arrow table directly to a list of dictionaries
#         return arrow_table.to_pylist()
        
#     finally:
#         cursor.close()