import sqlparse




def validate_sql(query):

    query_upper = query.upper()

   
    if not query_upper.startswith("SELECT"):
        return False, "Only SELECT queries allowed"

   
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", ";"]

    for word in forbidden:
        if word in query_upper:
            return False, f"Forbidden keyword: {word}"

    
    if "LIMIT" not in query_upper:
        return False, "LIMIT is required"

   
   

    return True, "Valid query"