import os
import re
import requests
from dotenv import load_dotenv
from knowledgebase import data_dict,query_patterns,business_rules,build_system_prompt

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
   Convert natural language → Snowflake SQL using OpenRouter
   """
  
   # 🛠️ UPDATED SYSTEM PROMPT WITH YOUR SNOWFLAKE SCHEMA
#    system_prompt = """
#    You are an expert Snowflake SQL generator.
   
#    CRITICAL: You MUST use the table name: FACT_CAMPAIGN_PERFORMANCE
   
#    TABLE SCHEMA:
#    - FACT_CAMPAIGN_PERFORMANCE:
#      - campaign_id (STRING)
#      - date (DATE)
#      - channel_used (STRING)
#      - total_clicks (INTEGER)
#      - total_cost (FLOAT)
#      - avg_roi (FLOAT)

#    STRICT RULES:
#    - Only SELECT queries allowed.
#    - Use uppercase for table and column names.
#    - Always include LIMIT 100.
#    - Use SUM or AVG for metrics like total_clicks or avg_roi when grouping.
#    - Return ONLY the SQL query text. No markdown, no explanations.
#    """

   system_prompt=build_system_prompt(data_dict,business_rules,query_patterns)

   url = "https://openrouter.ai/api/v1/chat/completions"
   headers = {
       "Authorization": f"Bearer {OPENROUTER_API_KEY}",
       "Content-Type": "application/json",
       "HTTP-Referer": "http://localhost",
       "X-OpenRouter-Title": "Snowflake SQL Generator"
   }

   payload = {
       "model": "openrouter/elephant-alpha", # You can also use "google/gemini-2.0-flash-001"
       "messages": [
           {"role": "system", "content": system_prompt},
           {"role": "user", "content": f"User Question:\n{user_input}"}
       ],
       "temperature": 0.0 
   }

   try:
       response = requests.post(url, headers=headers, json=payload)
       response.raise_for_status()
       response_data = response.json()
       raw_text = response_data["choices"][0]["message"]["content"]

       sql_query = clean_sql(raw_text)

       if not sql_query or "SELECT" not in sql_query.upper():
           return None

       return sql_query

   except Exception as e:
       print("LLM Error:", str(e))
       return None

if __name__ == "__main__":
   test_question = "What is the total cost for each channel?"
   sql = generate_sql(test_question)
   print(f"Generated SQL: \n{sql}")