def validate_sql(query):

    if not query:
        return False, "No query generated"

    query_upper = query.upper()

    # Only SELECT allowed
    if not query_upper.startswith("SELECT"):
        return False, "Only SELECT queries allowed"

    # Block dangerous keywords
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]

    for word in forbidden:
        if word in query_upper:
            return False, f"Forbidden keyword: {word}"

    # Require LIMIT
    if "LIMIT" not in query_upper:
        return False, "LIMIT missing"

    return True, "Valid query"