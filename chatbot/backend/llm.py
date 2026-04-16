import google.generativeai as genai
import os
from dotenv import load_dotenv
from data_dict import DATA_DICTIONARY

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_sql(user_input):

    prompt = f"""
    {DATA_DICTIONARY}

    Convert the user question into SQL query.

    Strict Rules:
    - Only SELECT queries allowed
    - No DELETE, UPDATE, INSERT
    - No joins
    - No subqueries
    - Must include LIMIT 100
    - Return ONLY SQL (no explanation)

    User Question: {user_input}
    """

    response = model.generate_content(prompt)

    return response.text.strip()