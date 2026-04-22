import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()



def run_query(query):
    # Establish connection using Snowflake-specific credentials
    ctx = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"), # Ensure no .snowflakecomputing.com here
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role="chatbot_readonly"
    )
    
    try:
        cs = ctx.cursor()
        cs.execute(query)
        
        # Capture column names and zip with row data for the frontend
        columns = [col[0] for col in cs.description]
        return [dict(zip(columns, row)) for row in cs.fetchall()]
    finally:
        cs.close()
        ctx.close()