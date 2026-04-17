def validate_sql(query):
    if not query:
        return False, "No query generated"

    query_upper = query.upper()
    
    # Check for the Snowflake table name in a case-insensitive way
    ALLOWED_TABLE = "FACT_CAMPAIGN_PERFORMANCE"

    if not query_upper.startswith("SELECT"):
        return False, "Only SELECT queries allowed"

    # Block dangerous keywords
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
    for word in forbidden:
        if word in query_upper:
            return False, f"Forbidden keyword: {word}"

    # Ensure the generated query actually targets your new Snowflake table
    if ALLOWED_TABLE not in query_upper:
        return False, f"Invalid table. Please query {ALLOWED_TABLE}."

    if "LIMIT" not in query_upper:
        return False, "LIMIT is required for performance safety."

    return True, "Valid query"