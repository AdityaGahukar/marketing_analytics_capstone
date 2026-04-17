# from fastapi import FastAPI
# from llm import generate_sql
# from validator import validate_sql
# from databrickconn  import run_query

# app = FastAPI()


# @app.get("/")
# def home():
#     return {"message": "AI SQL Chatbot Running"}


# @app.post("/chat")
# def chat(user_input: str):

#     # 🤖 Generate SQL
#     sql_query = generate_sql(user_input)

#     # # 🔐 Validate
#     # is_valid, message = validate_sql(sql_query)

#     # if not is_valid:
#     #     return {
#     #         "error": message,
#     #         "generated_query": sql_query
#     #     }

#     # # ⚡ Execute
#     # try:
#     #     data = run_query(sql_query)
#     # except Exception as e:
#     #     return {
#     #         "error": str(e),
#     #         "query": sql_query
#     #     }

#     return {
#         "query": sql_query
#         # "data": data
#     }


from fastapi import FastAPI
from pydantic import BaseModel

# your modules
from llm import generate_sql
from validator import validate_sql
from databrickconn import run_query

app = FastAPI()


# ✅ Request schema (IMPORTANT FIX)
class ChatRequest(BaseModel):
    user_input: str


@app.get("/")
def home():
    return {"message": "AI SQL Chatbot Running"}


@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.user_input

    # 🤖 Generate SQL
    sql_query = generate_sql(user_input)

    
    is_valid, message = validate_sql(sql_query)
    if not is_valid:
        return {
            "status": "error",
            "error": message,
            "generated_sql": "That doesn't seem like a valid query.Please try again"
        }

    
    try:
        data = run_query(sql_query)
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "generated_sql": "Unexpected error occured.Please Try again later"
        }

    return {
        "status": "success",
        "user_input": user_input,
        "generated_sql": data
        # "data": data
    }