from fastapi import FastAPI
from pydantic import BaseModel

# 🔄 CHANGE THIS IMPORT:
# Replace 'from databrickconn import run_query' with:
from snowflake_conn import run_query 

from llm import generate_sql
from validator import validate_sql
# from databrickconn import run_query
# from databricks import sql
import os
from dotenv import load_dotenv

from sqlSecurity import run_security_pipeline, build_schema_registry
from knowledgebase import data_dict
load_dotenv()

app = FastAPI()


SCHEMA_REGISTRY = build_schema_registry(data_dict)


# ✅ Request schema (IMPORTANT FIX)
class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
def home():
    return {"message": "AI SQL Chatbot Running on Snowflake"}

@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.user_input

    # 🤖 1. Generate SQL (Ensure llm.py is updated with Snowflake schema)
    sql_query = generate_sql(user_input)
    
    print(sql_query)

    # 🔐 2. Validate (Ensure validator.py allows FACT_CAMPAIGN_PERFORMANCE)
    # is_valid, message = run_security_pipeline(user_input, sql_query, SCHEMA_REGISTRY)
    # if not is_valid:
    #     return {
    #         "status": "error",
    #         "error": message,
    #         "generated_sql": "That doesn't seem like a valid query. Please try again."
    #     }

    # ⚡ 3. Execute against Snowflake
    try:
        print('Querying Snowflake...')
        data = run_query(sql_query)
        
        return {
            "status": "success",
            "user_input": user_input,
            "generated_sql": data  # This now contains your Snowflake results
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "generated_sql": "Unexpected error occurred. Please try again later."
        }