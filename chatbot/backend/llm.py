from google import genai   # ✅ NEW SDK
import os
import re
from dotenv import load_dotenv

# 🔐 Load env
load_dotenv()

# 🔑 Configure client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def clean_sql(response_text: str) -> str:
    """
    Clean Gemini output to extract pure SQL
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
    Convert natural language → SQL using Gemini
    """

    prompt = f"""
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

    User Question:
    {user_input}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",   # ✅ correct model usage
            contents=prompt
        )

        raw_text = response.text

        sql_query = clean_sql(raw_text)

        # 🔴 Fallback
        if not sql_query or "SELECT" not in sql_query.upper():
            return None

        return sql_query

    except Exception as e:
        print("LLM Error:", str(e))
        return None