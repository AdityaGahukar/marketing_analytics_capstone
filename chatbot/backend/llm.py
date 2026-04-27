import os
import re
import json
import boto3
from dotenv import load_dotenv
from knowledgebase import data_dict, query_patterns, business_rules

# 🔐 Load env
load_dotenv()

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION            = os.getenv("AWS_REGION", "us-east-1")

MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "eu.anthropic.claude-3-5-haiku-20241022-v1:0")
print("Using model:", MODEL_ID)
print("Using region:", AWS_REGION)

kb_client = boto3.client(
    "bedrock-agent-runtime",
    region_name='eu-north-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def get_kb_context(user_input: str):

    response = kb_client.retrieve(
        knowledgeBaseId="Z1GRIDQL5Q", 
        retrievalQuery={
            "text": user_input
        },
        retrievalConfiguration={
            "vectorSearchConfiguration": {
                "numberOfResults": 3   # keep small
            }
        }
    )

    results = response.get("retrievalResults", [])

    context = ""
    for r in results:
        context += r["content"]["text"] + "\n\n"

    return context

def clean_sql(response_text: str) -> str:
    if not response_text:
        return None
    text = response_text.strip()
    text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    match = re.search(r"(SELECT .*?LIMIT \d+)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_sql(user_input: str) -> str:

    #  Step 1: get context from KB
    kb_context = get_kb_context(user_input)
    print("kb_context is ",kb_context)

    #  Step 2: build prompt
    system_prompt = f"""
You are a Snowflake SQL expert.

### STRICT RULES
- Only generate SELECT queries
- Always include LIMIT <= 100
- Never use SELECT *
- Use ONLY tables present in CONTEXT

### BUSINESS RULES
{business_rules}

### EXAMPLES
{query_patterns}

### CONTEXT (from Knowledge Base)
{kb_context}

### some instructions 
If GROUP BY is used:
- All non-grouped columns MUST be aggregated using SUM, AVG, COUNT, etc.
-Never select raw metric columns (TOTAL_CLICKS, TOTAL_IMPRESSIONS, TOTAL_COST)
without aggregation when GROUP BY is present.

Return ONLY SQL query and dont give comments and other thing only gave me just sql querey.

"""

    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": system_prompt + "\n\nUser Question:\n" + user_input}
                ]
            }
        ],
        "inferenceConfig": {
            "temperature": 0.0,
            "maxTokens": 1024,
        }
    }

    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(payload),
        contentType="application/json",
        accept="application/json",
    )

    raw_text = json.loads(response["body"].read())["output"]["message"]["content"][0]["text"]

    return clean_sql(raw_text)
    # except Exception as e:
    #     print("Bedrock Error:", str(e))
    #     return None

if __name__ == "__main__":
    test_question = "What is the total cost for each channel?"
    sql = generate_sql(test_question)
    print(f"Generated SQL:\n{sql}")