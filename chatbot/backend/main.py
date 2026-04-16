from fastapi import FastAPI
from llm import generate_sql
from validator import validate_sql
from db import run_query

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI SQL Chatbot Running"}


@app.post("/chat")
def chat(user_input: str):

    # 🤖 Generate SQL
    sql_query = generate_sql(user_input)

    # 🔐 Validate
    is_valid, message = validate_sql(sql_query)

    if not is_valid:
        return {
            "error": message,
            "generated_query": sql_query
        }

    # ⚡ Execute
    try:
        data = run_query(sql_query)
    except Exception as e:
        return {
            "error": str(e),
            "query": sql_query
        }

    return {
        "query": sql_query,
        "data": data
    }