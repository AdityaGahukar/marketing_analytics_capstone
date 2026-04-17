# from google import genai   # ✅ NEW SDK
# import os
# import re
# from dotenv import load_dotenv

# # 🔐 Load env
# load_dotenv()

# # 🔑 Configure client
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# def clean_sql(response_text: str) -> str:
#     """
#     Clean Gemini output to extract pure SQL
#     """

#     if not response_text:
#         return None

#     text = response_text.strip()

#     # Remove markdown ```sql ```
#     text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
#     text = re.sub(r"```", "", text)

#     # Extract SELECT query
#     match = re.search(r"(SELECT .*?LIMIT \d+)", text, re.IGNORECASE | re.DOTALL)

#     if match:
#         return match.group(1).strip()

#     return text


# def generate_sql(user_input: str) -> str:
#     """
#     Convert natural language → SQL using Gemini
#     """

#     prompt = f"""
#     You are an expert SQL generator.

#     Convert the user question into a SQL query.

#     STRICT RULES:
#     - Only SELECT queries allowed
#     - No DELETE, UPDATE, INSERT, DROP
#     - No joins
#     - No subqueries
#     - Avoid SELECT *
#     - Always include LIMIT 100
#     - Prefer aggregation (SUM, COUNT) when possible
#     - Return ONLY SQL query
#     - Do NOT include explanation
#     - Do NOT include markdown

#     User Question:
#     {user_input}
#     """

#     try:
#         response = client.models.generate_content(
#             model="gemini-2.0-flash",   # ✅ correct model usage
#             contents=prompt
#         )

#         raw_text = response.text

#         sql_query = clean_sql(raw_text)

#         # 🔴 Fallback
#         if not sql_query or "SELECT" not in sql_query.upper():
#             return None

#         return sql_query

#     except Exception as e:
#         print("LLM Error:", str(e))
#         return None


import os
import re
import requests
from dotenv import load_dotenv


# 🔐 Load env
load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def clean_sql(response_text: str) -> str:
   """
   Clean LLM output to extract pure SQL
   """
   if not response_text:
       return None


   text = response_text.strip()


   # Remove markdown ```sql ```
   text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
   text = re.sub(r"```", "", text)


   # Extract SELECT query
   match = re.search(r"(SELECT .*?LIMIT \d+)", text, re.IGNORECASE | re.DOTALL)


   if match:
       return match.group(1).strip()


   return text


def generate_sql(user_input: str) -> str:
   """
   Convert natural language → SQL using OpenRouter Free API
   """
  
   system_prompt = """
   You are an expert SQL generator.


   Convert the user question into a SQL query.


   STRICT RULES:
   - Only SELECT queries allowed
   - No DELETE, UPDATE, INSERT, DROP
   - No joins
   - No subqueries
   - Avoid SELECT *
   - Always include LIMIT 100
   - Prefer aggregation (SUM, COUNT) when possible
   - Return ONLY SQL query
   - Do NOT include explanation
   - Do NOT include markdown
   """


   # OpenRouter API Endpoint
   url = "https://openrouter.ai/api/v1/chat/completions"


   # Headers strictly following OpenRouter Docs
   headers = {
       "Authorization": f"Bearer {OPENROUTER_API_KEY}",
       "Content-Type": "application/json",
       "HTTP-Referer": "http://localhost", # Optional, but good practice
       "X-OpenRouter-Title": "Local SQL Generator App" # Optional
   }


   # Payload with a FREE model
   payload = {
       # Using a highly capable free model on OpenRouter (Llama 3 8B)
       # You can also use "google/gemma-2-9b-it:free" or "qwen/qwen-2-7b-instruct:free"
       "model": "openrouter/elephant-alpha",
       "messages": [
           {"role": "system", "content": system_prompt},
           {"role": "user", "content": f"User Question:\n{user_input}"}
       ],
       "temperature": 0.0 # 🎯 Keep at 0 for strict SQL generation
   }


   try:
       # Using requests to post the data
       response = requests.post(url, headers=headers, json=payload)
      
       # Raise an exception if the HTTP request failed (e.g., 401 Unauthorized)
       response.raise_for_status()
      
       # Parse the JSON response
       response_data = response.json()


       # Extract the text from the standard OpenRouter/OpenAI JSON format
       raw_text = response_data["choices"][0]["message"]["content"]


       sql_query = clean_sql(raw_text)


       # 🔴 Fallback validation
       if not sql_query or "SELECT" not in sql_query.upper():
           return None


       return sql_query


   except requests.exceptions.RequestException as e:
       print("HTTP Request Error:", str(e))
       # Attempt to print the exact error message from OpenRouter if available
       if 'response' in locals() and response.text:
            print("OpenRouter Details:", response.text)
       return None
   except Exception as e:
       print("General Error:", str(e))
       return None


# --- Example Usage ---
if __name__ == "__main__":
   test_question = "What are the names of the top 10 highest paying customers?"
   sql = generate_sql(test_question)
   print(f"Generated SQL: \n{sql}")